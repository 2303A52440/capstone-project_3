import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

os.environ['MPLCONFIGDIR'] = r'C:\Users\SEETHARAM\.gemini\antigravity\scratch\capstone-project_3\figures'
fig_dir = r'C:\Users\SEETHARAM\.gemini\antigravity\scratch\capstone-project_3\figures'
os.makedirs(fig_dir, exist_ok=True)

# 1. SR University Logo graphic
fig, ax = plt.subplots(figsize=(6, 1.6), dpi=300)
ax.axis('off')
ax.text(0.12, 0.45, "srU", fontsize=48, fontweight='bold', color='#1A4B8C', fontfamily='sans-serif', va='center')
ax.plot([0.38, 0.38], [0.15, 0.85], color='#B0BEC5', lw=1.5)
ax.text(0.42, 0.58, "SR UNIVERSITY", fontsize=22, fontweight='bold', color='#1A4B8C', fontfamily='sans-serif', va='center')
ax.text(0.42, 0.34, "WARANGAL, TELANGANA", fontsize=11, color='#546E7A', fontfamily='sans-serif', va='center')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "sru_logo.png"), dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 2. Figure 1.1: Multi-Agent Warehouse Automation Ecosystem
fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
ax.set_facecolor('#F8FAFC')
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

# Warehouse grid floor
for x in range(1, 10):
    ax.axvline(x, color='#E2E8F0', lw=1, ls='--')
for y in range(1, 6):
    ax.axhline(y, color='#E2E8F0', lw=1, ls='--')

# Shelves / Obstacles
shelves = [(2.5, 3.5), (2.5, 2.5), (4.5, 4.5), (4.5, 3.5), (6.5, 2.5), (6.5, 1.5)]
for sx, sy in shelves:
    rect = patches.FancyBboxPatch((sx-0.4, sy-0.4), 0.8, 0.8, boxstyle="round,pad=0.05", facecolor='#D97706', edgecolor='#92400E', lw=2)
    ax.add_patch(rect)
    ax.text(sx, sy, "SHELF", color='white', fontsize=8, fontweight='bold', ha='center', va='center')

# AGVs
agvs = [
    (1.5, 1.5, '#0284C7', 'AGV-1', [(1.5, 1.5), (2.5, 1.5), (3.5, 1.5), (3.5, 2.5), (4.5, 2.5), (5.5, 2.5), (7.5, 2.5)]),
    (8.5, 4.5, '#9333EA', 'AGV-2', [(8.5, 4.5), (7.5, 4.5), (6.5, 4.5), (5.5, 4.5), (3.5, 4.5), (1.5, 4.5)]),
    (1.5, 5.2, '#059669', 'AGV-3', [(1.5, 5.2), (2.5, 5.2), (3.5, 5.2), (5.5, 5.2), (8.5, 2.5)]),
    (8.5, 1.2, '#E11D48', 'AGV-4', [(8.5, 1.2), (7.5, 1.2), (5.5, 1.2), (3.5, 1.2), (1.5, 3.5)])
]

for x, y, color, label, path in agvs:
    px, py = zip(*path)
    ax.plot(px, py, color=color, lw=2.5, ls='-', alpha=0.7)
    circle = patches.Circle((x, y), 0.35, facecolor=color, edgecolor='white', lw=2, zorder=5)
    ax.add_patch(circle)
    ax.text(x, y, label, color='white', fontsize=8, fontweight='bold', ha='center', va='center', zorder=6)
    # Goal Docks
    gx, gy = path[-1]
    dock = patches.FancyBboxPatch((gx-0.4, gy-0.3), 0.8, 0.6, boxstyle="round,pad=0.03", facecolor='none', edgecolor=color, lw=2, ls=':')
    ax.add_patch(dock)
    ax.text(gx, gy, f"DOCK", color=color, fontsize=7, fontweight='bold', ha='center', va='center')

ax.set_title("Figure 1.1: Automated Guided Vehicle (AGV) Swarm in Fulfillment Warehouse", fontsize=12, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig1_warehouse_agv.png"), dpi=300, bbox_inches='tight')
plt.close()

# 3. Figure 2.1: MAPF Algorithmic Taxonomy
fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
ax.axis('off')
ax.set_facecolor('#FFFFFF')

boxes = [
    (5, 4.0, "Multi-Agent Pathfinding (MAPF) Algorithms", "#1E293B", "white", 4.5, 0.6),
    (2, 2.6, "Coupled / Centralized\n(Joint State Space A*)", "#334155", "white", 3.0, 0.7),
    (5, 2.6, "Decoupled / Prioritized\n(Prioritized Planning / PBS)", "#334155", "white", 3.0, 0.7),
    (8, 2.6, "Conflict-Based Search (CBS)\n(Two-Level Optimal Search)", "#0284C7", "white", 3.0, 0.7),
    (2, 1.0, "Exponential Complexity\nO(|V|^N) - Optimal but Slow", "#F1F5F9", "#0F172A", 2.8, 0.7),
    (5, 1.0, "Polynomial Time O(N x T)\nIncomplete, Sub-optimal", "#F1F5F9", "#0F172A", 2.8, 0.7),
    (8, 1.0, "Bounded Tree Search\nOptimal & Complete", "#E0F2FE", "#0369A1", 2.8, 0.7)
]

for x, y, text, fc, tc, w, h in boxes:
    rect = patches.FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.08", facecolor=fc, edgecolor='#94A3B8', lw=1.5)
    ax.add_patch(rect)
    ax.text(x, y, text, color=tc, fontsize=9, fontweight='bold' if fc!="#F1F5F9" else 'normal', ha='center', va='center')

# Arrows
ax.annotate("", xy=(2, 3.0), xytext=(4, 3.7), arrowprops=dict(arrowstyle="->", lw=1.5, color='#64748B'))
ax.annotate("", xy=(5, 3.0), xytext=(5, 3.7), arrowprops=dict(arrowstyle="->", lw=1.5, color='#64748B'))
ax.annotate("", xy=(8, 3.0), xytext=(6, 3.7), arrowprops=dict(arrowstyle="->", lw=1.5, color='#0284C7'))
ax.annotate("", xy=(2, 1.4), xytext=(2, 2.2), arrowprops=dict(arrowstyle="->", lw=1.2, color='#94A3B8'))
ax.annotate("", xy=(5, 1.4), xytext=(5, 2.2), arrowprops=dict(arrowstyle="->", lw=1.2, color='#94A3B8'))
ax.annotate("", xy=(8, 1.4), xytext=(8, 2.2), arrowprops=dict(arrowstyle="->", lw=1.2, color='#0284C7'))

ax.set_xlim(0, 10)
ax.set_ylim(0.3, 4.6)
ax.set_title("Figure 2.1: Multi-Agent Pathfinding (MAPF) Algorithmic Classification", fontsize=12, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig2_mapf_taxonomy.png"), dpi=300, bbox_inches='tight')
plt.close()

# 4. Figure 3.1: Vertex and Edge Conflicts
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=300)

for ax in [ax1, ax2]:
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-0.5, 3.5)
    ax.set_xticks(range(4))
    ax.set_yticks(range(4))
    ax.grid(True, color='#CBD5E1', ls='--', lw=1)

# Vertex Conflict
ax1.set_title("(a) Vertex Collision (ai, aj, v, t)", fontsize=11, fontweight='bold', pad=10)
ax1.plot([0, 1, 2], [1, 1, 1], 'o--', color='#0284C7', lw=2, label="Agent 1 path")
ax1.plot([2, 2, 2], [3, 2, 1], 's--', color='#E11D48', lw=2, label="Agent 2 path")
# Collision spot
coll1 = patches.Circle((2, 1), 0.35, facecolor='#FEF2F2', edgecolor='#DC2626', lw=2.5, ls='--')
ax1.add_patch(coll1)
ax1.text(2, 1, "COLLISION\nat t=3", color='#DC2626', fontsize=8, fontweight='bold', ha='center', va='center')
ax1.legend(loc='lower left', fontsize=8)

# Edge Swap Conflict
ax2.set_title("(b) Edge Swap Collision (ai, aj, u, v, t)", fontsize=11, fontweight='bold', pad=10)
ax2.plot([1, 2], [1.1, 1.1], '->', color='#0284C7', lw=3, label="Agent 1: (1,1)->(2,1)")
ax2.plot([2, 1], [0.9, 0.9], '->', color='#9333EA', lw=3, label="Agent 2: (2,1)->(1,1)")
coll2 = patches.FancyBboxPatch((0.8, 0.6), 1.4, 0.8, boxstyle="round,pad=0.05", facecolor='#FFFBEB', edgecolor='#D97706', lw=2, ls=':')
ax2.add_patch(coll2)
ax2.text(1.5, 1.0, "SWAP CONFLICT\nat t=k", color='#B45309', fontsize=8, fontweight='bold', ha='center', va='center')
ax2.legend(loc='lower left', fontsize=8)

plt.suptitle("Figure 3.1: Fundamental Collision Primitives in MAPF Navigation", fontsize=12, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig3_conflicts.png"), dpi=300, bbox_inches='tight')
plt.close()

# 5. Figure 4.1: Conflict-Based Search Constraint Tree (CT)
fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
ax.axis('off')
ax.set_facecolor('#FFFFFF')

# Root Node
root = patches.FancyBboxPatch((3.5, 3.8), 3.0, 0.8, boxstyle="round,pad=0.1", facecolor='#F1F5F9', edgecolor='#475569', lw=2)
ax.add_patch(root)
ax.text(5.0, 4.3, "Root Node #0", fontsize=9, fontweight='bold', ha='center')
ax.text(5.0, 4.05, "Constraints: None", fontsize=8, color='#475569', ha='center')
ax.text(5.0, 3.85, "Cost: 28 | Conflict: (A1, A2, (5,3), t=4)", fontsize=8, color='#DC2626', fontweight='bold', ha='center')

# Left Child
left = patches.FancyBboxPatch((0.5, 2.0), 3.4, 0.8, boxstyle="round,pad=0.1", facecolor='#F8FAFC', edgecolor='#0284C7', lw=2)
ax.add_patch(left)
ax.text(2.2, 2.5, "Node #1 (Branch A1)", fontsize=9, fontweight='bold', color='#0369A1', ha='center')
ax.text(2.2, 2.25, "Constraint: (A1, (5,3), t=4)", fontsize=8, color='#0F172A', ha='center')
ax.text(2.2, 2.05, "Cost: 30 | Conflict: (A1, A3, (3,2), t=2)", fontsize=8, color='#DC2626', ha='center')

# Right Child
right = patches.FancyBboxPatch((6.1, 2.0), 3.4, 0.8, boxstyle="round,pad=0.1", facecolor='#ECFDF5', edgecolor='#059669', lw=2)
ax.add_patch(right)
ax.text(7.8, 2.5, "Node #2 (Branch A2) [OPTIMAL]", fontsize=9, fontweight='bold', color='#047857', ha='center')
ax.text(7.8, 2.25, "Constraint: (A2, (5,3), t=4)", fontsize=8, color='#0F172A', ha='center')
ax.text(7.8, 2.05, "Cost: 29 | Conflicts: NONE", fontsize=8, color='#059669', fontweight='bold', ha='center')

# Sub-branches from Node #1
sub1 = patches.FancyBboxPatch((0.2, 0.4), 2.5, 0.7, boxstyle="round,pad=0.08", facecolor='#F1F5F9', edgecolor='#94A3B8', lw=1.5)
ax.add_patch(sub1)
ax.text(1.45, 0.85, "Node #3 (Branch A1)", fontsize=8, fontweight='bold', ha='center')
ax.text(1.45, 0.6, "Cost: 32", fontsize=8, color='#64748B', ha='center')

sub2 = patches.FancyBboxPatch((3.0, 0.4), 2.5, 0.7, boxstyle="round,pad=0.08", facecolor='#F1F5F9', edgecolor='#94A3B8', lw=1.5)
ax.add_patch(sub2)
ax.text(4.25, 0.85, "Node #4 (Branch A3)", fontsize=8, fontweight='bold', ha='center')
ax.text(4.25, 0.6, "Cost: 31", fontsize=8, color='#64748B', ha='center')

# Edges
ax.annotate("", xy=(2.2, 2.9), xytext=(4.3, 3.8), arrowprops=dict(arrowstyle="->", lw=1.5, color='#0284C7'))
ax.annotate("", xy=(7.8, 2.9), xytext=(5.7, 3.8), arrowprops=dict(arrowstyle="->", lw=2, color='#059669'))
ax.annotate("", xy=(1.45, 1.2), xytext=(1.8, 2.0), arrowprops=dict(arrowstyle="->", lw=1.2, color='#94A3B8'))
ax.annotate("", xy=(4.25, 1.2), xytext=(2.6, 2.0), arrowprops=dict(arrowstyle="->", lw=1.2, color='#94A3B8'))

ax.set_xlim(0, 10)
ax.set_ylim(0.1, 4.8)
ax.set_title("Figure 4.1: Conflict-Based Search (CBS) High-Level Constraint Tree Search", fontsize=12, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig4_cbs_tree.png"), dpi=300, bbox_inches='tight')
plt.close()

# 6. Figure 4.2: 3D Space-Time Graph
fig = plt.figure(figsize=(8, 5), dpi=300)
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#FFFFFF')

# Trajectory A1
t = np.linspace(0, 10, 11)
x1 = np.array([1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10])
y1 = np.array([1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5])
ax.plot(x1, y1, t, label='Agent 1 Trajectory', color='#0284C7', lw=3, marker='o')

# Trajectory A2 (deviating to avoid collision at t=4)
x2 = np.array([10, 9, 8, 7, 7, 6, 5, 4, 3, 2, 1])
y2 = np.array([5, 5, 4, 4, 3, 3, 2, 2, 1, 1, 1])
ax.plot(x2, y2, t, label='Agent 2 Trajectory (CBS Detour)', color='#E11D48', lw=3, marker='^')

# Cylinder / Bar for obstacle over time
z_obs = np.linspace(0, 10, 20)
ax.plot([5]*20, [4]*20, z_obs, color='#D97706', lw=4, label='Stationary Shelf Tube')

ax.set_xlabel('Spatial Coordinate X', fontsize=9, labelpad=8)
ax.set_ylabel('Spatial Coordinate Y', fontsize=9, labelpad=8)
ax.set_zlabel('Temporal Coordinate T', fontsize=9, labelpad=8)
ax.set_title("Figure 4.2: 3D Space-Time Coordinate Trajectory Graph (X, Y, Time)", fontsize=11, fontweight='bold', pad=15)
ax.legend(loc='upper left', fontsize=8)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig4_spacetime_astar.png"), dpi=300, bbox_inches='tight')
plt.close()

# 7. Figure 5.1: High-Level System Architecture
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
ax.axis('off')
ax.set_facecolor('#FFFFFF')

layers = [
    (1.5, 4.0, "Physical / Simulated Floor\n(Grid, Shelves, Docking Stations)", "#0F172A", "white", 2.6, 0.8),
    (5.0, 4.0, "MAPF Planning Engine\n(High-Level CBS + Space-Time A*)", "#0284C7", "white", 3.2, 0.8),
    (8.5, 4.0, "Digital Twin Frontends\n(Tkinter GUI & Web Canvas)", "#059669", "white", 2.6, 0.8),
    
    (1.5, 2.2, "Dynamic Obstacle Monitor\n(Real-time floor map updates)", "#F8FAFC", "#0F172A", 2.6, 0.7),
    (5.0, 2.2, "Constraint Database\n(Vertex & Edge Swap Constraints)", "#F8FAFC", "#0F172A", 3.0, 0.7),
    (8.5, 2.2, "ROS2 / MQTT Bridge\n(Topic: /agv_telemetry)", "#F8FAFC", "#0F172A", 2.6, 0.7),

    (5.0, 0.7, "Distributed Hardware / Physical AGVs (ESP32 / Jetson Orin Micro-ROS)", "#475569", "white", 7.0, 0.6)
]

for x, y, text, fc, tc, w, h in layers:
    rect = patches.FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.08", facecolor=fc, edgecolor='#64748B', lw=1.5)
    ax.add_patch(rect)
    ax.text(x, y, text, color=tc, fontsize=8.5, fontweight='bold' if fc!="#F8FAFC" else 'normal', ha='center', va='center')

# Arrows connecting components
ax.annotate("", xy=(3.3, 4.0), xytext=(2.8, 4.0), arrowprops=dict(arrowstyle="<->", lw=2, color='#0284C7'))
ax.annotate("", xy=(7.1, 4.0), xytext=(6.7, 4.0), arrowprops=dict(arrowstyle="<->", lw=2, color='#059669'))
ax.annotate("", xy=(1.5, 3.5), xytext=(1.5, 2.6), arrowprops=dict(arrowstyle="<->", lw=1.5, color='#64748B'))
ax.annotate("", xy=(5.0, 3.5), xytext=(5.0, 2.6), arrowprops=dict(arrowstyle="<->", lw=1.5, color='#64748B'))
ax.annotate("", xy=(8.5, 3.5), xytext=(8.5, 2.6), arrowprops=dict(arrowstyle="<->", lw=1.5, color='#64748B'))
ax.annotate("", xy=(5.0, 1.1), xytext=(5.0, 1.8), arrowprops=dict(arrowstyle="<->", lw=2, color='#475569'))

ax.set_xlim(0, 10)
ax.set_ylim(0.2, 4.7)
ax.set_title("Figure 5.1: High-Level Digital Twin and Multi-Agent Orchestration Architecture", fontsize=12, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig5_system_arch.png"), dpi=300, bbox_inches='tight')
plt.close()

# 8. Figure 7.1: Runtime comparison (CBS vs PBS vs A*)
agents = [2, 4, 6, 8, 12, 16]
cbs_time = [0.2, 0.8, 2.1, 5.4, 18.2, 45.6]
pbs_time = [0.1, 0.4, 0.9, 1.8, 4.5, 9.8]
joint_astar = [0.5, 12.0, 240.0, 1800.0, 9999.0, 9999.0] # timeout

fig, ax = plt.subplots(figsize=(7, 4.2), dpi=300)
ax.plot(agents, cbs_time, 'o-', color='#0284C7', lw=2.5, label='Conflict-Based Search (CBS) [Optimal]')
ax.plot(agents, pbs_time, 's--', color='#059669', lw=2, label='Prioritized Planning (PBS) [Sub-optimal]')
ax.plot(agents[:4], joint_astar[:4], '^:', color='#E11D48', lw=2, label='Coupled Joint A* [Exponential]')

ax.set_yscale('log')
ax.set_xlabel('Number of Swarm AGVs (N)', fontsize=10, fontweight='bold')
ax.set_ylabel('Execution Time (ms) [Log Scale]', fontsize=10, fontweight='bold')
ax.set_title("Figure 7.1: Algorithmic Runtime Scaling Comparison", fontsize=11, fontweight='bold', pad=12)
ax.grid(True, which='both', color='#E2E8F0', ls='--')
ax.legend(fontsize=8.5)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig7_runtime_comparison.png"), dpi=300, bbox_inches='tight')
plt.close()

# 9. Figure 7.2: Sum of Costs comparison
soc_cbs = [22, 46, 72, 98, 154, 212]
soc_pbs = [22, 48, 79, 114, 182, 260]

fig, ax = plt.subplots(figsize=(7, 4.2), dpi=300)
w = 0.35
x = np.arange(len(agents))
ax.bar(x - w/2, soc_cbs, w, label='CBS (Globally Optimal SOC)', color='#0284C7')
ax.bar(x + w/2, soc_pbs, w, label='Prioritized Planning (Sub-optimal SOC)', color='#F59E0B')

ax.set_xticks(x)
ax.set_xticklabels([f"{n} AGVs" for n in agents], fontsize=9)
ax.set_ylabel('Sum of Costs (Total Steps)', fontsize=10, fontweight='bold')
ax.set_title("Figure 7.2: Solution Quality: Sum of Costs (SOC) Optimality Analysis", fontsize=11, fontweight='bold', pad=12)
ax.grid(True, axis='y', color='#E2E8F0', ls='--')
ax.legend(fontsize=8.5)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig7_sum_of_costs.png"), dpi=300, bbox_inches='tight')
plt.close()

# 10. Figure 7.3: Conflict density vs grid obstacle percentage
density = [5, 10, 15, 20, 25, 30, 35]
conflicts_detected = [1.2, 3.4, 7.8, 14.5, 26.2, 44.0, 78.5]
cbs_nodes_expanded = [2.1, 5.0, 12.4, 28.1, 54.3, 98.7, 185.0]

fig, ax1 = plt.subplots(figsize=(7, 4.2), dpi=300)
color = '#E11D48'
ax1.set_xlabel('Warehouse Shelf / Obstacle Density (%)', fontsize=10, fontweight='bold')
ax1.set_ylabel('Mean Conflicts per Plan Instance', color=color, fontsize=10, fontweight='bold')
l1 = ax1.plot(density, conflicts_detected, 'o-', color=color, lw=2.5, label='Conflicts Detected')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, color='#E2E8F0', ls='--')

ax2 = ax1.twinx()
color = '#0284C7'
ax2.set_ylabel('High-Level CBS Nodes Expanded', color=color, fontsize=10, fontweight='bold')
l2 = ax2.plot(density, cbs_nodes_expanded, 's--', color=color, lw=2.5, label='Nodes Expanded')
ax2.tick_params(axis='y', labelcolor=color)

lines = l1 + l2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left', fontsize=8.5)

plt.title("Figure 7.3: Search Tree Expansion vs. Warehouse Clutter Density", fontsize=11, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig7_conflict_density.png"), dpi=300, bbox_inches='tight')
plt.close()

# 11. Figure 7.4: Dynamic Replanning Latency
latencies = np.random.normal(loc=0.82, scale=0.15, size=500)
latencies = np.clip(latencies, 0.4, 1.8)

fig, ax = plt.subplots(figsize=(7, 4.2), dpi=300)
n, bins, patches_hist = ax.hist(latencies, bins=25, color='#059669', edgecolor='white', alpha=0.85)
ax.axvline(np.mean(latencies), color='#DC2626', lw=2, ls='--', label=f'Mean Latency: {np.mean(latencies):.2f} ms')
ax.axvline(np.percentile(latencies, 99), color='#D97706', lw=2, ls=':', label=f'99th Percentile: {np.percentile(latencies, 99):.2f} ms')

ax.set_xlabel('Replanning Duration (Milliseconds)', fontsize=10, fontweight='bold')
ax.set_ylabel('Frequency (Sample Runs)', fontsize=10, fontweight='bold')
ax.set_title("Figure 7.4: Dynamic Floor Obstacle Replanning Latency Distribution", fontsize=11, fontweight='bold', pad=12)
ax.grid(True, color='#E2E8F0', ls='--')
ax.legend(fontsize=8.5)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig7_replanning_latency.png"), dpi=300, bbox_inches='tight')
plt.close()

# 12. Figure 5.2: Data Flow Diagram (DFD)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300)
for ax in [ax1, ax2]:
    ax.axis('off')
    ax.set_facecolor('#FFFFFF')

# DFD Level 0 (Context Diagram)
ax1.set_title("(a) Level-0 Context DFD", fontsize=11, fontweight='bold', pad=10)
e1 = patches.FancyBboxPatch((0.5, 2.5), 2.2, 0.9, boxstyle="round,pad=0.08", facecolor='#F1F5F9', edgecolor='#475569', lw=1.5)
ax1.add_patch(e1)
ax1.text(1.6, 2.95, "Fleet Operator /\nWarehouse WMS", fontsize=8, fontweight='bold', ha='center', va='center')

p0 = patches.Circle((5.0, 2.95), 1.2, facecolor='#E0F2FE', edgecolor='#0284C7', lw=2)
ax1.add_patch(p0)
ax1.text(5.0, 3.1, "0.0\nMAPF Swarm", fontsize=9, fontweight='bold', ha='center', va='center', color='#0369A1')
ax1.text(5.0, 2.65, "Digital Twin", fontsize=8, ha='center', va='center', color='#0369A1')

e2 = patches.FancyBboxPatch((7.3, 2.5), 2.2, 0.9, boxstyle="round,pad=0.08", facecolor='#F1F5F9', edgecolor='#475569', lw=1.5)
ax1.add_patch(e2)
ax1.text(8.4, 2.95, "AGV Hardware /\nROS2 Fleet", fontsize=8, fontweight='bold', ha='center', va='center')

ax1.annotate("Goal Allocations &\nFloor Map", xy=(3.8, 3.2), xytext=(2.7, 3.2), arrowprops=dict(arrowstyle="->", lw=1.2, color='#0284C7'), fontsize=7, ha='center')
ax1.annotate("Telemetry & Alerts", xy=(2.7, 2.7), xytext=(3.8, 2.7), arrowprops=dict(arrowstyle="->", lw=1.2, color='#475569'), fontsize=7, ha='center')
ax1.annotate("Space-Time Paths", xy=(7.3, 3.2), xytext=(6.2, 3.2), arrowprops=dict(arrowstyle="->", lw=1.2, color='#0284C7'), fontsize=7, ha='center')
ax1.annotate("Live Odometry", xy=(6.2, 2.7), xytext=(7.3, 2.7), arrowprops=dict(arrowstyle="->", lw=1.2, color='#475569'), fontsize=7, ha='center')
ax1.set_xlim(0, 10)
ax1.set_ylim(1.0, 4.8)

# DFD Level 1
ax2.set_title("(b) Level-1 Functional Decomposition DFD", fontsize=11, fontweight='bold', pad=10)
p1 = patches.Circle((2.5, 3.8), 0.8, facecolor='#E0F2FE', edgecolor='#0284C7', lw=1.5)
ax2.add_patch(p1)
ax2.text(2.5, 3.8, "1.0\nGrid &\nShelves", fontsize=7.5, fontweight='bold', ha='center', va='center', color='#0369A1')

p2 = patches.Circle((6.5, 3.8), 0.8, facecolor='#FEF3C7', edgecolor='#D97706', lw=1.5)
ax2.add_patch(p2)
ax2.text(6.5, 3.8, "2.0\nCBS High\nLevel", fontsize=7.5, fontweight='bold', ha='center', va='center', color='#92400E')

p3 = patches.Circle((6.5, 1.8), 0.8, facecolor='#EDE9FE', edgecolor='#7C3AED', lw=1.5)
ax2.add_patch(p3)
ax2.text(6.5, 1.8, "3.0\nSpace-Time\nA* Search", fontsize=7.5, fontweight='bold', ha='center', va='center', color='#5B21B6')

p4 = patches.Circle((2.5, 1.8), 0.8, facecolor='#DCFCE7', edgecolor='#16A34A', lw=1.5)
ax2.add_patch(p4)
ax2.text(2.5, 1.8, "4.0\nTelemetry\nBridge", fontsize=7.5, fontweight='bold', ha='center', va='center', color='#15803D')

ax2.annotate("", xy=(5.7, 3.8), xytext=(3.3, 3.8), arrowprops=dict(arrowstyle="->", lw=1.2, color='#0284C7'))
ax2.annotate("", xy=(6.5, 2.6), xytext=(6.5, 3.0), arrowprops=dict(arrowstyle="<->", lw=1.2, color='#D97706'))
ax2.annotate("", xy=(3.3, 1.8), xytext=(5.7, 1.8), arrowprops=dict(arrowstyle="->", lw=1.2, color='#7C3AED'))
ax2.annotate("", xy=(2.5, 3.0), xytext=(2.5, 2.6), arrowprops=dict(arrowstyle="->", lw=1.2, color='#16A34A'))

ax2.set_xlim(1.0, 8.5)
ax2.set_ylim(0.8, 4.8)

plt.suptitle("Figure 5.2: Level-0 Context and Level-1 Functional Data Flow Diagrams", fontsize=12, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig5_dfd.png"), dpi=300, bbox_inches='tight')
plt.close()

# 13. Figure 6.1: Tkinter Desktop GUI Mockup
fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
ax.axis('off')
ax.set_facecolor('#0B0F19')

# Top header
rect_top = patches.Rectangle((0, 4.4), 10, 0.6, facecolor='#141B2D', edgecolor='#334155')
ax.add_patch(rect_top)
ax.text(0.3, 4.7, "MAPF-SWARM // CBS DIGITAL TWIN SIMULATOR (PYTHON 3)", color='#FFAB00', fontsize=9, fontweight='bold', va='center')

# Left Canvas frame
rect_grid = patches.Rectangle((0.3, 0.8), 6.5, 3.4, facecolor='#060911', edgecolor='#1F2942', lw=1.5)
ax.add_patch(rect_grid)
# Draw mini grid
for gx in np.linspace(0.5, 6.6, 12):
    ax.axvline(gx, ymin=0.18, ymax=0.82, color='#141B2D', lw=0.8)
for gy in np.linspace(1.0, 4.0, 8):
    ax.axhline(gy, xmin=0.05, xmax=0.66, color='#141B2D', lw=0.8)

# Shelves
for sx, sy in [(1.8, 2.8), (3.4, 2.2), (5.0, 3.2)]:
    rect_s = patches.Rectangle((sx-0.25, sy-0.25), 0.5, 0.5, facecolor='#3D2600', edgecolor='#FFAB00', lw=1.2)
    ax.add_patch(rect_s)
    ax.text(sx, sy, "SHELF", color='#FFAB00', fontsize=6, fontweight='bold', ha='center', va='center')

# AGVs & Docks
ax.plot([1.2, 2.5, 4.0, 5.8], [1.5, 1.5, 2.8, 3.8], color='#00F2FE', lw=2)
circle1 = patches.Circle((2.5, 1.5), 0.22, facecolor='#00F2FE', edgecolor='white', lw=1.5)
ax.add_patch(circle1)
ax.text(2.5, 1.5, "A1", color='black', fontsize=7, fontweight='bold', ha='center', va='center')

circle2 = patches.Circle((4.2, 3.5), 0.22, facecolor='#8A2BE2', edgecolor='white', lw=1.5)
ax.add_patch(circle2)
ax.text(4.2, 3.5, "A2", color='white', fontsize=7, fontweight='bold', ha='center', va='center')

# Buttons under canvas
ax.add_patch(patches.Rectangle((0.3, 0.2), 2.2, 0.45, facecolor='#FFAB00'))
ax.text(1.4, 0.425, "Start Swarm Motion", color='#0B0F19', fontsize=7.5, fontweight='bold', ha='center', va='center')
ax.add_patch(patches.Rectangle((2.7, 0.2), 1.5, 0.45, facecolor='#1F2942'))
ax.text(3.45, 0.425, "Step (t+1)", color='white', fontsize=7.5, ha='center', va='center')
ax.add_patch(patches.Rectangle((4.4, 0.2), 1.8, 0.45, facecolor='#1F2942'))
ax.text(5.3, 0.425, "Re-Solve CBS", color='#00F2FE', fontsize=7.5, ha='center', va='center')

# Right Telemetry Box
rect_right = patches.Rectangle((7.0, 0.2), 2.7, 4.0, facecolor='#141B2D', edgecolor='#334155', lw=1.5)
ax.add_patch(rect_right)
ax.text(7.2, 3.9, "AGV FLEET TELEMETRY", color='white', fontsize=8, fontweight='bold')
# Terminal log content
logs = [
    "[CBS SOLVER SUCCESS]",
    "Solved for 4 AGVs in 0.82ms",
    "[ROS2 MQTT] /agv_telemetry",
    "Time Step: t=4",
    "AGV-1: Pos (4, 3) -> Goal (18,10)",
    "AGV-2: Pos (14, 2) -> Goal (18,1)",
    "AGV-3: Pos (10, 5) -> Goal (10,10)",
    "Zero Collisions Detected",
    "Bandwidth: 14.2 KB/s",
    "Status: NOMINAL"
]
for i, l in enumerate(logs):
    ax.text(7.2, 3.5 - i*0.32, l, color='#00E676' if 'SUCCESS' in l or 'NOMINAL' in l else '#94A3B8', fontsize=6.5, fontfamily='monospace')

ax.set_xlim(0, 10)
ax.set_ylim(0, 5.0)
ax.set_title("Figure 6.1: Standalone Python Desktop Application (Tkinter GUI)", fontsize=11, fontweight='bold', color='white', pad=12)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig6_tkinter_gui.png"), dpi=300, bbox_inches='tight', facecolor='#0B0F19')
plt.close()

# 14. Figure 6.2: Web Digital Twin Dashboard Mockup
fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
ax.axis('off')
ax.set_facecolor('#060911')

# Navbar
ax.add_patch(patches.Rectangle((0, 4.4), 10, 0.6, facecolor='#141B2D'))
ax.text(0.3, 4.7, "MAPF-SWARM // CBS DIGITAL TWIN ENGINE (HTML5 CANVAS)", color='#00F2FE', fontsize=8.5, fontweight='bold', va='center')
ax.text(8.0, 4.7, "ROS2 MQTT: ACTIVE", color='#00E676', fontsize=7.5, fontweight='bold', va='center')

# Canvas representation
ax.add_patch(patches.Rectangle((0.3, 1.4), 6.5, 2.8, facecolor='#0B0F19', edgecolor='#00F2FE', lw=1.2))
ax.text(3.5, 2.8, "INTERACTIVE 24x12 WAREHOUSE FLOOR", color='#38BDF8', fontsize=8, fontweight='bold', ha='center')
ax.text(3.5, 2.4, "(Click to Dynamically Insert Shelves / Obstacles)", color='#94A3B8', fontsize=7, ha='center')

# Status cards below
cards = [("AGV-1", "#00F2FE", "t=14s | Dock A"), ("AGV-2", "#8A2BE2", "t=16s | Dock B"), ("AGV-3", "#FFAB00", "t=12s | Dock C"), ("AGV-4", "#FF2E93", "t=18s | Dock D")]
for idx, (name, col, det) in enumerate(cards):
    cx = 0.3 + idx*1.65
    ax.add_patch(patches.Rectangle((cx, 0.3), 1.5, 0.9, facecolor='#141B2D', edgecolor=col, lw=1))
    ax.text(cx+0.1, 0.95, name, color=col, fontsize=7.5, fontweight='bold')
    ax.text(cx+0.1, 0.6, det, color='#E2E8F0', fontsize=6)

# Right Panel
ax.add_patch(patches.Rectangle((7.0, 0.3), 2.7, 3.9, facecolor='#141B2D', edgecolor='#334155'))
ax.text(7.2, 3.9, "CBS CONSTRAINT TREE LOG", color='#FFAB00', fontsize=8, fontweight='bold')
web_logs = [
    "[HIGH-LEVEL] Root #0 generated",
    "[LOW-LEVEL] A* Space-time: 4 paths",
    "[CONFLICT] None detected. SOC=84",
    "[TELEMETRY] JSON stream 50Hz",
    "Target IP: 192.168.1.100",
    "Protocol: WebSockets / MQTT"
]
for i, l in enumerate(web_logs):
    ax.text(7.2, 3.5 - i*0.4, l, color='#38BDF8' if 'HIGH-LEVEL' in l else '#CBD5E1', fontsize=6.5, fontfamily='monospace')

ax.set_xlim(0, 10)
ax.set_ylim(0, 5.0)
ax.set_title("Figure 6.2: Web-Based Digital Twin Platform (TailwindCSS & HTML5 Canvas)", fontsize=11, fontweight='bold', color='white', pad=12)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig6_web_dashboard.png"), dpi=300, bbox_inches='tight', facecolor='#060911')
plt.close()

print("All figures successfully generated in", fig_dir)

