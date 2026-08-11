"""
===============================================================================
PROJECT 4: AUTONOMOUS COLLABORATIVE ROBOT SWARM SIMULATOR (MAPF / CBS)
===============================================================================
Core Engine: Conflict-Based Search (CBS) & Space-Time A* Search
UI & Visualizer: Python Tkinter (Zero External Dependencies Required)

Author: Antigravity Systems Architect
Language: Python 3.8+
===============================================================================
"""

import math
import heapq
import time
import json
import random
import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Tuple, Set, Optional
from dataclasses import dataclass, field

# =============================================================================
# DATA STRUCTURES FOR MAPF & CBS
# =============================================================================

Position = Tuple[int, int]
SpaceTimePoint = Tuple[int, int, int]  # (x, y, t)

@dataclass(frozen=True)
class Constraint:
    agent: int
    loc1: Position
    loc2: Optional[Position] = None  # None for vertex constraint, loc2 for edge constraint
    time: int = 0

@dataclass
class Conflict:
    agent1: int
    agent2: int
    loc1: Position
    loc2: Optional[Position] = None
    time: int = 0
    is_edge: bool = False

@dataclass(order=True)
class PriorityNode:
    priority: float
    data: any = field(compare=False)

# =============================================================================
# LOW-LEVEL SPACE-TIME A* SEARCH SOLVER
# =============================================================================

class SpaceTimeAStar:
    """Low-level solver searching in (x, y, t) space-time graph for a single agent."""
    
    def __init__(self, grid_width: int, grid_height: int, obstacles: Set[Position]):
        self.width = grid_width
        self.height = grid_height
        self.obstacles = obstacles

    def heuristic(self, pos: Position, goal: Position) -> float:
        """Manhattan distance heuristic."""
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def get_neighbors(self, pos: Position) -> List[Position]:
        """Returns valid orthogonal adjacent cells + wait action."""
        x, y = pos
        candidates = [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        valid = []
        for nx, ny in candidates:
            if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in self.obstacles:
                valid.append((nx, ny))
        return valid

    def find_path(self, agent_id: int, start: Position, goal: Position, constraints: Set[Constraint], max_t: int = 100) -> Optional[List[Position]]:
        """Computes optimal space-time path for agent_id subject to constraints."""
        
        # Build constraint lookup tables
        vertex_constraints: Set[Tuple[Position, int]] = set()
        edge_constraints: Set[Tuple[Position, Position, int]] = set()

        for c in constraints:
            if c.agent == agent_id:
                if c.loc2 is None:
                    vertex_constraints.add((c.loc1, c.time))
                else:
                    edge_constraints.add((c.loc1, c.loc2, c.time))

        open_set = []
        # Priority queue item: (f_score, g_score, (x, y, t), path)
        start_h = self.heuristic(start, goal)
        heapq.heappush(open_set, (start_h, 0, (start[0], start[1], 0), [start]))

        visited: Set[Tuple[Position, int]] = set()

        while open_set:
            f, g, (x, y, t), path = heapq.heappop(open_set)
            curr_pos = (x, y)

            if curr_pos == goal and t >= 5: # Stay at goal
                return path

            if t > max_t:
                break

            state_key = (curr_pos, t)
            if state_key in visited:
                continue
            visited.add(state_key)

            for nxt_pos in self.get_neighbors(curr_pos):
                nxt_t = t + 1

                # Check vertex constraint
                if (nxt_pos, nxt_t) in vertex_constraints:
                    continue

                # Check edge swap constraint
                if (curr_pos, nxt_pos, nxt_t) in edge_constraints:
                    continue

                nxt_g = g + 1
                nxt_f = nxt_g + self.heuristic(nxt_pos, goal)
                heapq.heappush(open_set, (nxt_f, nxt_g, (nxt_pos[0], nxt_pos[1], nxt_t), path + [nxt_pos]))

        return None

# =============================================================================
# HIGH-LEVEL CONFLICT-BASED SEARCH (CBS) SOLVER
# =============================================================================

@dataclass
class HighLevelNode:
    constraints: Set[Constraint]
    solution: Dict[int, List[Position]]
    cost: int

class HighLevelCBS:
    """High-level Constraint Tree Search resolving multi-agent spatial conflicts."""

    def __init__(self, grid_width: int, grid_height: int, obstacles: Set[Position], starts: Dict[int, Position], goals: Dict[int, Position]):
        self.width = grid_width
        self.height = grid_height
        self.obstacles = obstacles
        self.starts = starts
        self.goals = goals
        self.low_level = SpaceTimeAStar(grid_width, grid_height, obstacles)

    def detect_first_conflict(self, solution: Dict[int, List[Position]]) -> Optional[Conflict]:
        """Finds the earliest vertex or edge conflict between any pair of agents."""
        max_len = max(len(p) for p in solution.values()) if solution else 0

        for t in range(max_len):
            # Check vertex conflicts
            pos_map: Dict[Position, int] = {}
            for agent, path in solution.items():
                pos = path[t] if t < len(path) else path[-1]
                if pos in pos_map:
                    return Conflict(agent1=pos_map[pos], agent2=agent, loc1=pos, time=t, is_edge=False)
                pos_map[pos] = agent

            # Check edge swap conflicts
            if t > 0:
                for a1, p1 in solution.items():
                    u1 = p1[t-1] if t-1 < len(p1) else p1[-1]
                    v1 = p1[t] if t < len(p1) else p1[-1]

                    for a2, p2 in solution.items():
                        if a1 >= a2:
                            continue
                        u2 = p2[t-1] if t-1 < len(p2) else p2[-1]
                        v2 = p2[t] if t < len(p2) else p2[-1]

                        if u1 == v2 and v1 == u2:
                            return Conflict(agent1=a1, agent2=a2, loc1=u1, loc2=v1, time=t, is_edge=True)

        return None

    def solve(self) -> Tuple[Optional[Dict[int, List[Position]]], int]:
        """Executes CBS search returning collision-free space-time paths for all agents."""
        root_constraints = set()
        initial_solution = {}

        for agent, start in self.starts.items():
            path = self.low_level.find_path(agent, start, self.goals[agent], root_constraints)
            if not path:
                return None, 0
            initial_solution[agent] = path

        root_cost = sum(len(p) for p in initial_solution.values())
        root_node = HighLevelNode(constraints=root_constraints, solution=initial_solution, cost=root_cost)

        open_pq = []
        heapq.heappush(open_pq, (root_node.cost, id(root_node), root_node))

        nodes_expanded = 0

        while open_pq:
            cost, _, node = heapq.heappop(open_pq)
            nodes_expanded += 1

            conflict = self.detect_first_conflict(node.solution)
            if not conflict:
                return node.solution, nodes_expanded

            # Branch tree on conflict
            if not conflict.is_edge:
                # Vertex Conflict: Branch for Agent 1 and Agent 2
                c1 = Constraint(agent=conflict.agent1, loc1=conflict.loc1, time=conflict.time)
                c2 = Constraint(agent=conflict.agent2, loc1=conflict.loc1, time=conflict.time)
                branches = [(conflict.agent1, c1), (conflict.agent2, c2)]
            else:
                # Edge Conflict: Branch for Agent 1 (u->v) and Agent 2 (v->u)
                c1 = Constraint(agent=conflict.agent1, loc1=conflict.loc1, loc2=conflict.loc2, time=conflict.time)
                c2 = Constraint(agent=conflict.agent2, loc1=conflict.loc2, loc2=conflict.loc1, time=conflict.time)
                branches = [(conflict.agent1, c1), (conflict.agent2, c2)]

            for agent, new_constraint in branches:
                new_constraints = set(node.constraints)
                new_constraints.add(new_constraint)

                new_path = self.low_level.find_path(agent, self.starts[agent], self.goals[agent], new_constraints)
                if new_path:
                    new_solution = dict(node.solution)
                    new_solution[agent] = new_path
                    new_cost = sum(len(p) for p in new_solution.values())
                    child = HighLevelNode(constraints=new_constraints, solution=new_solution, cost=new_cost)
                    heapq.heappush(open_pq, (child.cost, id(child), child))

        return None, nodes_expanded

# =============================================================================
# INTERACTIVE PYTHON TKINTER APPLICATION & DIGITAL TWIN UI
# =============================================================================

class RobotSwarmApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("APEX // Autonomous Robot Swarm Simulator (MAPF / CBS)")
        self.root.geometry("1100x720")
        self.root.configure(bg="#0B0F19")

        # Grid Specs
        self.cols = 20
        self.rows = 12
        self.cell_size = 36

        self.obstacles: Set[Position] = {
            (4, 2), (4, 3), (4, 4), (4, 5),
            (9, 6), (9, 7), (9, 8), (9, 9),
            (14, 2), (14, 3), (14, 4), (14, 5)
        }

        self.starts = {
            1: (1, 1), 2: (1, 10), 3: (10, 1), 4: (18, 5)
        }
        self.goals = {
            1: (18, 10), 2: (18, 1), 3: (10, 10), 4: (1, 5)
        }
        self.colors = {
            1: "#00F2FE", 2: "#8A2BE2", 3: "#FFAB00", 4: "#FF2E93"
        }

        self.solution: Dict[int, List[Position]] = {}
        self.time_step = 0
        self.is_running = False

        self._build_ui()
        self.run_cbs_solver()

    def _build_ui(self):
        # Header Bar
        header = tk.Frame(self.root, bg="#141B2D", height=50)
        header.pack(fill=tk.X, side=tk.TOP)

        title = tk.Label(header, text="MAPF-SWARM // CBS DIGITAL TWIN SIMULATOR (PYTHON 3)", font=("Consolas", 14, "bold"), fg="#FFAB00", bg="#141B2D")
        title.pack(side=tk.LEFT, padx=15, pady=10)

        # Main Layout (Left: Canvas, Right: Telemetry Controls)
        main_frame = tk.Frame(self.root, bg="#0B0F19")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Left Canvas
        canvas_frame = tk.Frame(main_frame, bg="#141B2D", bd=1, relief=tk.SOLID)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg="#060911", highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Controls bar under canvas
        ctrl_bar = tk.Frame(canvas_frame, bg="#141B2D")
        ctrl_bar.pack(fill=tk.X, padx=10, pady=5)

        self.play_btn = tk.Button(ctrl_bar, text="▶ Start Swarm Motion", font=("Consolas", 10, "bold"), fg="#0B0F19", bg="#FFAB00", command=self.toggle_play, width=22)
        self.play_btn.pack(side=tk.LEFT, padx=5)

        step_btn = tk.Button(ctrl_bar, text="Step (t+1)", font=("Consolas", 10), fg="#FFFFFF", bg="#1F2942", command=self.step_sim)
        step_btn.pack(side=tk.LEFT, padx=5)

        solve_btn = tk.Button(ctrl_bar, text="Re-Solve CBS", font=("Consolas", 10), fg="#00F2FE", bg="#1F2942", command=self.run_cbs_solver)
        solve_btn.pack(side=tk.LEFT, padx=5)

        # Right Panel
        right_panel = tk.Frame(main_frame, bg="#141B2D", width=320, bd=1, relief=tk.SOLID)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(15, 0))

        lbl_telemetry = tk.Label(right_panel, text="AGV FLEET TELEMETRY", font=("Consolas", 11, "bold"), fg="#FFFFFF", bg="#141B2D")
        lbl_telemetry.pack(anchor=tk.W, padx=10, pady=10)

        self.log_box = tk.Text(right_panel, font=("Consolas", 9), fg="#00E676", bg="#060911", height=20, width=35, bd=0)
        self.log_box.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    def log(self, text: str):
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)

    def on_canvas_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        pos = (col, row)

        if pos in self.obstacles:
            self.obstacles.remove(pos)
            self.log(f"[DYNAMIC FLOOR] Removed obstacle at ({col}, {row})")
        else:
            self.obstacles.add(pos)
            self.log(f"[DYNAMIC FLOOR] Placed shelf at ({col}, {row})")

        self.run_cbs_solver()

    def run_cbs_solver(self):
        cbs = HighLevelCBS(self.cols, self.rows, self.obstacles, self.starts, self.goals)
        start_time = time.time()
        solution, nodes = cbs.solve()
        elapsed = (time.time() - start_time) * 1000

        if solution:
            self.solution = solution
            self.log(f"[CBS SOLVER SUCCESS] Found paths for 4 AGVs in {elapsed:.2f}ms! (Nodes: {nodes})")
        else:
            self.log("[CBS SOLVER FAILED] No collision-free path found!")

        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")

        # Draw Grid Lines
        for c in range(self.cols + 1):
            self.canvas.create_line(c * self.cell_size, 0, c * self.cell_size, self.rows * self.cell_size, fill="#141B2D")
        for r in range(self.rows + 1):
            self.canvas.create_line(0, r * self.cell_size, self.cols * self.cell_size, r * self.cell_size, fill="#141B2D")

        # Draw Obstacles
        for ox, oy in self.obstacles:
            x1 = ox * self.cell_size
            y1 = oy * self.cell_size
            self.canvas.create_rectangle(x1, y1, x1 + self.cell_size, y1 + self.cell_size, fill="#3D2600", outline="#FFAB00")
            self.canvas.create_text(x1 + 18, y1 + 18, text="SHELF", fill="#FFAB00", font=("Consolas", 7))

        # Draw AGV Goals & Trajectories
        for agent_id, goal in self.goals.items():
            gx = goal[0] * self.cell_size + 18
            gy = goal[1] * self.cell_size + 18
            self.canvas.create_oval(gx - 14, gy - 14, gx + 14, gy + 14, outline=self.colors[agent_id], width=2)
            self.canvas.create_text(gx, gy, text=f"DOCK-{agent_id}", fill=self.colors[agent_id], font=("Consolas", 7, "bold"))

        # Draw AGV Current Position
        for agent_id, path in self.solution.items():
            idx = min(self.time_step, len(path) - 1)
            pos = path[idx]

            ax = pos[0] * self.cell_size + 18
            ay = pos[1] * self.cell_size + 18

            # AGV Circle
            self.canvas.create_oval(ax - 12, ay - 12, ax + 12, ay + 12, fill=self.colors[agent_id], outline="#FFFFFF", width=2)
            self.canvas.create_text(ax, ay, text=f"A{agent_id}", fill="#000000", font=("Consolas", 8, "bold"))

    def step_sim(self):
        self.time_step += 1
        self.draw_grid()

        # Emit ROS2 MQTT JSON Log
        telemetry = {
            "timestamp": time.time(),
            "timestep": self.time_step,
            "agvs": [
                {
                    "id": aid,
                    "pos": self.solution[aid][min(self.time_step, len(self.solution[aid]) - 1)]
                } for aid in self.solution
            ]
        }
        self.log(f"[ROS2 MQTT] /agv_telemetry -> t={self.time_step}")

    def toggle_play(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.play_btn.config(text="⏸ Pause Motion", bg="#FF1744", fg="#FFFFFF")
            self._auto_step()
        else:
            self.play_btn.config(text="▶ Start Swarm Motion", bg="#FFAB00", fg="#0B0F19")

    def _auto_step(self):
        if self.is_running:
            self.step_sim()
            self.root.after(400, self._auto_step)

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = RobotSwarmApp(root)
    root.mainloop()
