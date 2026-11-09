import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

os.environ['MPLCONFIGDIR'] = r'C:\Users\SEETHARAM\.gemini\antigravity\scratch\capstone-project_3\figures'
base_dir = r'C:\Users\SEETHARAM\.gemini\antigravity\scratch\capstone-project_3'
fig_dir = os.path.join(base_dir, 'figures')

# Create A1 Academic Poster (Aspect ratio roughly 1 : 1.414, e.g. 14 x 19.8 inches at 300 DPI)
fig = plt.figure(figsize=(14, 19.8), dpi=300)
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
ax.set_facecolor('#0B0F19')

# Top Banner Header (Navy / Dark Slate)
header_rect = patches.Rectangle((0, 0.88), 1.0, 0.12, facecolor='#141B2D', edgecolor='#0284C7', lw=2)
ax.add_patch(header_rect)

# Title Text
ax.text(0.04, 0.955, "AUTONOMOUS COLLABORATIVE ROBOT SWARM SIMULATOR & DIGITAL TWIN", fontsize=20, fontweight='bold', color='#FFFFFF', va='center')
ax.text(0.04, 0.925, "Multi-Agent Pathfinding (MAPF) Driven by Conflict-Based Search (CBS) and Space-Time A* with ROS2 / MQTT Telemetry", fontsize=11.5, color='#38BDF8', va='center')

# Team & Guide metadata
ax.text(0.04, 0.895, "Students: Sanjay (2303A52337) | Sathwik (2303A52158) | Seetharam (2303A52440)  •  Guide: Dr. Sudha Rani  •  School of CS&AI, SR University", fontsize=9.5, color='#94A3B8', va='center')

# Upper Right SRU Branding
ax.text(0.85, 0.945, "SR UNIVERSITY", fontsize=15, fontweight='bold', color='#FFAB00', ha='center', va='center')
ax.text(0.85, 0.92, "WARANGAL, TELANGANA", fontsize=8.5, color='#E2E8F0', ha='center', va='center')
ax.text(0.85, 0.898, "Capstone Project 2026-2027", fontsize=8, color='#00E676', ha='center', va='center')

# Left Column (x: 0.04 to 0.48), Right Column (x: 0.52 to 0.96)
def add_card(x, y, w, h, title, title_color='#00F2FE'):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015", facecolor='#141B2D', edgecolor='#334155', lw=1.5)
    ax.add_patch(rect)
    ax.text(x + 0.02, y + h - 0.025, title, fontsize=12, fontweight='bold', color=title_color, va='top')
    return x + 0.02, y + h - 0.045, w - 0.04, h - 0.06

# 1. Motivation & Problem Statement (Left Top)
tx, ty, tw, th = add_card(0.04, 0.70, 0.45, 0.165, "1. MOTIVATION & PROBLEM STATEMENT")
text_p1 = (
    "• In dense automated fulfillment centers, fleets of Automated Guided Vehicles (AGVs)\n"
    "  must navigate without collisions while minimizing arrival time and battery draw.\n"
    "• Coupled Joint A* scales exponentially: O(|V|^N) -> catastrophic memory exhaustion.\n"
    "• Decoupled Prioritized Planning is fast O(N*T) but sub-optimal and suffers from deadlocks.\n"
    "• Research Goal: Design a two-level Conflict-Based Search (CBS) engine guaranteeing\n"
    "  100% collision-free, globally optimal paths with sub-millisecond dynamic replanning."
)
ax.text(tx, ty, text_p1, fontsize=8.5, color='#E2E8F0', va='top', linespacing=1.4)

# 2. Mathematical Formulation & Conflict Primitives (Right Top)
tx, ty, tw, th = add_card(0.51, 0.70, 0.45, 0.165, "2. FORMULATION & CONFLICT PRIMITIVES", '#FFAB00')
text_p2 = (
    "• Discrete 4-Connected Spatial Grid Graph G = (V, E) with obstacle set O.\n"
    "• Space-Time A* Cost Function: f(v, t) = g(v, t) + h(v), where h(v) is Manhattan distance.\n"
    "• Vertex Collision: Exists if two AGVs occupy same cell at same time: p_i(t) = p_j(t) = v.\n"
    "• Edge Swap Collision: Exists if AGVs cross same edge oppositely: p_i(t-1)=u, p_i(t)=v AND p_j(t-1)=v, p_j(t)=u.\n"
    "• Objective: Minimize Sum of Costs (SOC) = SUM(len(path_i)) across all N agents."
)
ax.text(tx, ty, text_p2, fontsize=8.5, color='#E2E8F0', va='top', linespacing=1.4)

# 3. Two-Level Conflict-Based Search Architecture (Left Middle)
tx, ty, tw, th = add_card(0.04, 0.40, 0.45, 0.285, "3. SYSTEM ARCHITECTURE & CBS ENGINE")
img_cbs = Image.open(os.path.join(fig_dir, "fig4_cbs_tree.png"))
ax.imshow(img_cbs, extent=[0.06, 0.47, 0.41, 0.63], aspect='auto', zorder=5)

# 4. Digital Twin Dual Execution Frontends (Right Middle)
tx, ty, tw, th = add_card(0.51, 0.40, 0.45, 0.285, "4. DIGITAL TWIN DUAL FRONTENDS", '#00E676')
img_gui = Image.open(os.path.join(fig_dir, "fig6_web_dashboard.png"))
ax.imshow(img_gui, extent=[0.53, 0.94, 0.41, 0.63], aspect='auto', zorder=5)

# 5. Experimental Results & Performance Benchmarks (Left Bottom)
tx, ty, tw, th = add_card(0.04, 0.12, 0.45, 0.265, "5. PERFORMANCE BENCHMARKS")
img_bench = Image.open(os.path.join(fig_dir, "fig7_runtime_comparison.png"))
ax.imshow(img_bench, extent=[0.06, 0.47, 0.13, 0.33], aspect='auto', zorder=5)

# 6. Solution Optimality & ROS2 Telemetry (Right Bottom)
tx, ty, tw, th = add_card(0.51, 0.12, 0.45, 0.265, "6. SOC OPTIMALITY & TELEMETRY", '#FF2E93')
img_soc = Image.open(os.path.join(fig_dir, "fig7_sum_of_costs.png"))
ax.imshow(img_soc, extent=[0.53, 0.94, 0.13, 0.33], aspect='auto', zorder=5)

# Bottom Footer
foot_rect = patches.Rectangle((0, 0), 1.0, 0.10, facecolor='#141B2D', edgecolor='#334155', lw=1.5)
ax.add_patch(foot_rect)
footer_text = (
    "KEY OUTCOMES: 100% Collision Avoidance | Globally Optimal Sum-of-Costs | <1.0ms Solving Time | Sub-millisecond Dynamic Floor Replanning\n"
    "ROS2 / MQTT JSON Telemetry Bridge at 50 Hz | Standalone Zero-Dependency Python Desktop GUI & Web Digital Twin Platform\n"
    "GitHub Repository: https://github.com/2303A52440/capstone-project_3.git  •  School of CS&AI, SR University, Warangal"
)
ax.text(0.5, 0.05, footer_text, fontsize=9.5, fontweight='bold', color='#FFFFFF', ha='center', va='center', linespacing=1.4)

poster_path = os.path.join(base_dir, "2303A52440-Seetharam Poster.png")
fig.savefig(poster_path, dpi=300, facecolor='#0B0F19')
plt.close()
print("Poster successfully created at:", poster_path)
