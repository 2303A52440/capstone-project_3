# Capstone Project Video Demonstration Script & Guide
## "Autonomous Collaborative Robot Swarm Simulator & Digital Twin (MAPF / CBS)"

**Target Video Duration**: 8 Minutes (Allowed Range: 5 to 12 Minutes)  
**Presenters**: Seetharam (2303A52440), Sanjay (2303A52337), Sathwik (2303A52158)  
**Guide**: Dr. Sudha Rani, School of CS&AI, SR University  

---

### University Video Guidelines Compliance Check:
- [x] **Initial 10-15 seconds**: Displays Project Title, Candidate Names, Enrollment Numbers, University Name, and Mentor Name.
- [x] **Last 10-15 seconds**: Displays Project Title, Candidate Names, Enrollment Numbers, University Name, and GitHub link.
- [x] **Presenter Visibility**: Presenter on webcam for at least 20% of the overall duration (picture-in-picture or full frame during intro and conclusion).
- [x] **Content**: Introduction, Problem Statement, CBS Algorithm, Live Desktop Demo, Live Web Digital Twin Demo, and Results.

---

### Step-by-Step Video Timeline & Script:

#### 1. Title Card & Introduction (0:00 - 0:45) [Full-Screen Presenter + Title Slide]
* **Visual**: Slide 1 displayed on screen with student webcam in bottom-right corner.
* **Spoken**: 
  > "Hello everyone, and welcome to the capstone project presentation and demonstration for our project: 'Autonomous Collaborative Robot Swarm Simulator & Digital Twin'. 
  > My name is Seetharam (Enrollment No: 2303A52440), and alongside my teammates Sanjay (2303A52337) and Sathwik (2303A52158), this project was completed under the guidance of Dr. Sudha Rani in the School of Computer Science & Artificial Intelligence at SR University, Warangal."

#### 2. Problem Statement & Motivation (0:45 - 2:00) [Slide 2 & Slide 3]
* **Visual**: Slides showing warehouse AGV clutter, vertex collisions, and edge swap collisions.
* **Spoken**: 
  > "In modern fulfillment centers like Amazon or Flipkart, hundreds of Automated Guided Vehicles (AGVs) navigate shared floors simultaneously. When robots plan paths independently, they suffer head-on deadlocks. On the other hand, traditional coupled A* has exponential complexity O(|V|^N), making it impossible to scale past 5 robots. Our goal is to achieve 100% collision-free navigation with guaranteed mathematical optimality and sub-millisecond dynamic replanning using Conflict-Based Search."

#### 3. Algorithmic Formulation: CBS & Space-Time A* (2:00 - 3:30) [Slide 4, 5, 6]
* **Visual**: Constraint Tree diagram and 3D space-time graph.
* **Spoken**: 
  > "Our solution operates on two levels: 
  > At the low level, each robot plans its route using 3D Space-Time A* search over (x, y, t) coordinates with Manhattan distance heuristics. 
  > At the high level, Conflict-Based Search detects vertex conflicts and counter-directional edge swaps. When a conflict occurs, CBS branches the Constraint Tree, placing negative constraints on the conflicting agents so that only the constrained agent replans. This prunes over 90% of search effort while guaranteeing minimal Sum of Costs."

#### 4. Live Demonstration: Python Tkinter Desktop Simulator (3:30 - 5:15) [Screen Capture]
* **Visual**: Switch to running `python robot_swarm_cbs.py`.
* **Action**:
  1. Show initial grid with 4 AGVs and obstacle shelves.
  2. Click **'Re-Solve CBS'** and highlight the log: `[CBS SOLVER SUCCESS] Found paths for 4 AGVs in 0.82ms!`.
  3. Click **'Start Swarm Motion'** to observe smooth multi-agent traversal without collisions.
  4. Click on an empty grid cell to dynamically place a new shelf directly in an AGV's path.
  5. Demonstrate how the solver re-routes in <1 ms around the new obstacle and resumes motion.
  6. Point out the telemetry log emitting ROS2 JSON packets on `/agv_telemetry`.

#### 5. Live Demonstration: Web-Based Digital Twin (5:15 - 6:45) [Screen Capture of `index.html`]
* **Visual**: Open `index.html` in Chrome/Edge.
* **Action**:
  1. Highlight the cyber-industrial dark mode UI, TailwindCSS glassmorphism cards, and Lucide icons.
  2. Show live AGV status cards (ID, speed, position, docking status).
  3. Click **'Start Swarm Dispatch'** and toggle simulation speeds (1x, 2x, 4x).
  4. Change swarm size from 4 AGVs to 6 and 8 AGVs.
  5. Dynamically toggle shelf obstacles on the canvas and observe instant trajectory re-renders.

#### 6. Performance Benchmarks & Conclusion (6:45 - 7:45) [Slide 11 & Slide 12]
* **Visual**: Runtime scaling charts and Sum of Costs comparison graphs.
* **Spoken**: 
  > "Our experimental results confirm that CBS executes in just 0.82 ms for 4 AGVs and 5.4 ms for 8 AGVs, compared to Coupled Joint A* which timed out. Furthermore, CBS achieved 100% optimal Sum of Costs, whereas Prioritized Planning incurred up to a 22.6% detour penalty. Our dynamic replanning latency averaged just 0.82 ms."

#### 7. Final Closing & Acknowledgements (7:45 - 8:00) [Presenter Face-Cam + Final Slide]
* **Visual**: Closing slide with team details, guide name, and GitHub repository URL.
* **Spoken**: 
  > "We thank Dr. Sudha Rani, Dr. CH. Sandeep, and the faculty of CS&AI at SR University for their continuous support. The complete open-source codebase is available on our GitHub repository. Thank you!"

---

### Free Video Recording & Upload Instructions:
1. **Recording Software**: Use **OBS Studio** (Free, open source) or **Loom** (Free browser recorder with webcam bubble).
2. **Upload**: Upload to **YouTube** as an **'Unlisted'** or **'Public'** video (so evaluators can click and watch without logging in).
3. **Copy Link**: Paste the generated YouTube link into `LINKS.txt`.
