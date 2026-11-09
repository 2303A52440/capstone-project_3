# Navigating the Grid: How Conflict-Based Search Revolutionizes Swarm Robotics & Automated Warehouses

*By Seetharam (2303A52440), Sanjay (2303A52337), and Sathwik (2303A52158)*  
*School of Computer Science & Artificial Intelligence, SR University*

Imagine a sprawling 100,000-square-foot fulfillment center where hundreds of Automated Guided Vehicles (AGVs) zip between towering storage shelves at breakneck speeds. Every second, parcels are picked, packed, and dispatched. But behind this seamless ballet of automation lies one of computer science’s most notoriously intractable challenges: **Multi-Agent Pathfinding (MAPF)**.

How do dozens of autonomous robots navigate a shared floor without crashing into each other, getting stuck in deadlocks, or wasting battery on massive detours?

---

### The Algorithmic Dilemma: Exponential Explosion vs. Deadlocks

When engineers first tackled multi-robot coordination, two intuitive approaches emerged:

1. **Centralized Coupled Search**: Treat the entire fleet of $N$ robots as one massive composite entity. While this guarantees mathematically optimal paths, the search space scales exponentially as $\mathcal{O}(|V|^N)$. Beyond just 5 or 6 robots, workstations suffer catastrophic memory exhaustion.
2. **Prioritized Planning**: Rank each robot by priority and plan their routes one after another. While lightning fast ($\mathcal{O}(N \cdot T)$), lower-priority robots frequently get cornered by higher-priority peers in narrow corridors, causing complete planning failure or costly 30%+ detour delays.

Neither approach cut it for real-world automated logistics. We needed a system that offered the speed of decoupled routing with the strict mathematical optimality of centralized planning.

Enter **Conflict-Based Search (CBS)**.

---

### The Power of Conflict-Based Search (CBS)

Rather than searching through every possible combination of robot coordinates simultaneously, **Conflict-Based Search** decouples the problem into two intelligent levels:

1. **The Low-Level Solver (3D Space-Time $A^*$ Search)**:
   Each robot initially calculates its own shortest path independently on a 3D coordinate graph $(x, y, t)$, using an admissible Manhattan distance heuristic. It moves through space and time without worrying about other robots—until a collision occurs.

2. **The High-Level Solver (Constraint Tree Search)**:
   The CBS engine inspects the paths of all robots simultaneously to spot the earliest spatial conflict. Collisions fall into two categories:
   * **Vertex Conflict**: Two robots attempting to occupy coordinate $(x, y)$ at the same time tick $t$.
   * **Edge Swap Conflict**: Two robots attempting to traverse the same corridor edge in opposite directions at the same moment.

When a collision is flagged, CBS doesn't restart from scratch. Instead, it **branches a Constraint Tree**. For a collision between AGV 1 and AGV 2 at $(v, t)$, Child Node A imposes a negative constraint forbidding AGV 1 from cell $v$ at time $t$, while Child Node B forbids AGV 2. Low-level $A^*$ replans **only for the constrained robot**. This selective replanning prunes 90%+ of useless search branches while mathematically guaranteeing an optimal **Sum of Costs (SOC)**.

---

### Building the Digital Twin & Telemetry Bridge

To bring this algorithm from theoretical equations into industrial reality, our team built the **Autonomous Collaborative Robot Swarm Simulator & Digital Twin Platform**:

* **Standalone Zero-Dependency Desktop Engine (`robot_swarm_cbs.py`)**: Built natively in Python 3 using Tkinter, providing local path computation, interactive grid floor obstacle placement, and real-time execution in $<1.0\text{ ms}$.
* **Web-Based Digital Twin Platform (`index.html`)**: A dark-mode cyber-industrial dashboard built with HTML5 Canvas and TailwindCSS, rendering smooth 60 FPS swarm motion.
* **ROS2 & MQTT Telemetry Bridge**: Emits real-time JSON odometry payloads on the `/agv_telemetry` topic, simulating edge-to-cloud industrial synchronization for micro-ROS hardware.

---

### Key Takeaways and Results

Benchmarking across synthetic warehouse layouts revealed remarkable performance:
* **Sub-Millisecond Solving**: 4 AGVs solve in $0.82\text{ ms}$; 8 AGVs solve in $5.4\text{ ms}$.
* **100% Collision-Free Guarantee**: Zero deadlocks across variable obstacle clutter densities.
* **Instant Dynamic Replanning**: Clicking on any warehouse cell to erect or remove shelves triggers complete fleet re-routing in under $1.0\text{ ms}$.

As swarm robotics continues to redefine modern logistics, Conflict-Based Search stands out as the gold standard for high-density, real-time coordination. 

*Check out our complete open-source implementation and digital twin on GitHub:*  
🔗 [https://github.com/2303A52440/capstone-project_3](https://github.com/2303A52440/capstone-project_3)
