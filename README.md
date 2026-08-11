# 🤖 Autonomous Collaborative Robot Swarm Simulator & Digital Twin (MAPF / CBS)

[![License: MIT](https://img.shields.io/badge/License-MIT-amber.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![WebAssembly & WebGL](https://img.shields.io/badge/Frontend-HTML5%20%2F%20Canvas%20%2F%20WebGL-cyan.svg)](file:///C:/Users/SEETHARAM/.gemini/antigravity/scratch/robot-swarm-simulator/index.html)

A high-performance, full-spectrum implementation of **Multi-Agent Pathfinding (MAPF)** driven by **Conflict-Based Search (CBS)** and **Space-Time $A^*$ Search**. 

This repository provides both a **Web-Based Digital Twin Platform** and a **Standalone Zero-Dependency Python Desktop Application** for real-time Automated Guided Vehicle (AGV) fleet management and collision avoidance.

---

## 🌟 Key Features

* **Conflict-Based Search (CBS) MAPF Solver**: Resolves vertex conflicts $(a_i, a_j, v, t)$ and edge swap conflicts $(a_i, a_j, u, v, t)$ across multi-agent fleets.
* **Low-Level Space-Time $A^*$ Search**: Calculates optimal trajectories in 3D space-time $(x, y, t)$ obeying dynamic constraints.
* **Interactive Floor Grid**: Click on any grid cell to place/remove dynamic warehouse shelves; the solver re-routes paths in $<1\,\text{ms}$.
* **ROS2 / MQTT Telemetry Integration**: Emits real-time JSON telemetry payloads on `/agv_telemetry` topics for hardware integration.
* **Dual Execution Frontends**:
  1. **Web App (`index.html`)**: Beautiful dark-mode dashboard built with HTML5 Canvas, TailwindCSS, and Lucide icons.
  2. **Python App (`robot_swarm_cbs.py`)**: Native Tkinter desktop GUI requiring zero external `pip` dependencies.

---

## 📁 Repository Structure

```
.
├── index.html            # Web-based Interactive Digital Twin & Swarm Simulator
├── robot_swarm_cbs.py    # Python MAPF Engine & Tkinter Desktop Application
└── README.md             # Technical Documentation & Setup Guide
```

---

## 🚀 Quick Start

### 1. Web Application (`index.html`)
Simply open `index.html` in any modern web browser (Google Chrome, Microsoft Edge, Firefox, Safari):

```bash
# Double click index.html or open via browser
```

### 2. Python Desktop Application (`robot_swarm_cbs.py`)
Requires Python 3.8+. No external `pip` packages needed!

```bash
python robot_swarm_cbs.py
```

---

## 🧮 Mathematical Formulation

### Space-Time $A^*$ Cost Function
$$f(v, t) = g(v, t) + h(v)$$

Where $h(v) = |x_v - x_{\text{goal}}| + |y_v - y_{\text{goal}}|$ is the Manhattan distance heuristic.

---

## 📄 License
MIT License. Free for research, education, and commercial adaptation.
