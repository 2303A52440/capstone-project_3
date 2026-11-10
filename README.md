# 🤖 Autonomous Collaborative Robot Swarm Simulator & Digital Twin (MAPF / CBS)

[![License: MIT](https://img.shields.io/badge/License-MIT-amber.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![SR University](https://img.shields.io/badge/SR%20University-Capstone%202026--2027-0284C7.svg)](https://sru.edu.in)

> **Capstone Project — School of Computer Science & Artificial Intelligence, SR University, Warangal**  
> **Candidate**: Seetharam Ravula (2303A52440)  
> **Teammates**: Sanjay (2303A52337), Sathwik (2303A52158)  
> **Project Guide**: Dr. Sudha Rani, Assistant Professor  

---

## 🖼️ Academic Research Poster (A1 Conference Format)

![SR University Capstone Research Poster](2303A52440-Seetharam%20Poster.png)

*📄 [Download Print-Ready Vector PDF (A1 Size)](2303A52440-Seetharam%20Poster.pdf)*

---

A high-performance, full-spectrum implementation of **Multi-Agent Pathfinding (MAPF)** driven by **Conflict-Based Search (CBS)** and **Space-Time $A^*$ Search**. 

This repository provides both a **Web-Based Digital Twin Platform** and a **Standalone Zero-Dependency Python Desktop Application** for real-time Automated Guided Vehicle (AGV) fleet management and collision avoidance.

---

## 🌟 Key Features

* **Conflict-Based Search (CBS) MAPF Solver**: Resolves vertex conflicts $(a_i, a_j, v, t)$ and edge swap conflicts $(a_i, a_j, u, v, t)$ across multi-agent fleets.
* **Low-Level Space-Time $A^*$ Search**: Calculates optimal trajectories in 3D space-time $(x, y, t)$ obeying dynamic constraints.
* **Interactive Floor Grid**: Click on any grid cell to place/remove dynamic warehouse shelves; the solver re-routes paths in $<1\,\text{ms}$.
* **ROS2 / MQTT Telemetry Integration**: Emits real-time JSON telemetry payloads on `/agv_telemetry` topics for hardware integration.
* **Triple Execution Frontends**:
  1. **Swarm Dispatch Web App (`Swarm-Dispatch/`)**: Production-grade React 19, TypeScript, and Vite dispatch console and interactive puzzle simulator powered by Conflict-Based Search (CBS) with full Vitest test suite.
  2. **Web App (`index.html`)**: Dark-mode dashboard built with HTML5 Canvas, TailwindCSS, and Lucide icons.
  3. **Python App (`robot_swarm_cbs.py`)**: Native Tkinter desktop GUI requiring zero external `pip` dependencies.

---

## 📁 Repository Structure

```text
.
├── Swarm-Dispatch/                      # Modern React + Vite + TypeScript CBS Dispatch Game & Simulator
│   ├── src/                             # Application source code & UI components
│   │   ├── components/                  # SwarmGame, WarehousePreview, and UI library
│   │   ├── lib/swarm-game.ts            # Conflict-Based Search (CBS) & MAPF engine
│   │   └── lib/swarm-game.test.ts       # Automated CBS optimality & conflict tests
│   ├── package.json                     # Node.js dependencies & build scripts
│   └── README.md                        # Swarm Dispatch gameplay & solver documentation
├── index.html                           # Web-based Interactive Digital Twin & Swarm Simulator
├── robot_swarm_cbs.py                   # Python MAPF Engine & Tkinter Desktop Application
├── 2303A52440-Seetharam Poster.png      # Official A1 Conference Research Poster (PNG)
├── 2303A52440-Seetharam Poster.pdf      # Official Print-Ready A1 Research Poster (PDF)
├── 2303A52440-Seetharam PPT.pptx        # 16-Slide Final Presentation Deck
├── 2303A52440-Seetharam Final Report.docx # Complete Capstone Documentation
├── 2303A52440-Seetharam Prototype Demo.mp4 # Video Demonstration Recording
├── BLOG.md                              # 650-Word Original Technical Blog Post
├── SOCIAL_POSTS.md                      # LinkedIn & Twitter/X Social Announcements
├── VIDEO_DEMO_SCRIPT.md                 # 8-Minute Video Demonstration Script & Timeline
├── LINKS.txt                            # Official SRU Submission Links File
├── figures/                             # High-Resolution Architectural & Benchmark Charts
└── README.md                            # Technical Documentation & Setup Guide
```

---

## 🚀 Quick Start

### 1. Swarm Dispatch Modern Web App (`Swarm-Dispatch/`)
High-performance interactive puzzle and dispatch dashboard:

```bash
cd Swarm-Dispatch
npm install
npm run dev
```

Run automated CBS unit tests:
```bash
npm test
```

### 2. Web Application (`index.html`)
Simply open `index.html` in any modern web browser (Google Chrome, Microsoft Edge, Firefox, Safari):

```bash
# Double click index.html or open via browser
```

### 3. Python Desktop Application (`robot_swarm_cbs.py`)
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
