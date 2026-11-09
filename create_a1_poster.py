import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

os.environ['MPLCONFIGDIR'] = r'C:\Users\SEETHARAM\.gemini\antigravity\scratch\capstone-project_3\figures'
base_dir = r'C:\Users\SEETHARAM\.gemini\antigravity\scratch\capstone-project_3'
fig_dir = os.path.join(base_dir, 'figures')

# Exact ISO A1 Dimensions: 594 mm x 841 mm (Aspect ratio: 1 : 1.4158)
# In inches: 23.386 x 33.11 inches
width_in = 23.386
height_in = 33.110

fig = plt.figure(figsize=(width_in, height_in), dpi=200)
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
ax.set_facecolor('#070B14') # Deep dark professional conference slate

# =========================================================================
# 1. TOP HEADER & BRANDING (SRU LOGO UPPER-RIGHT)
# =========================================================================
header_h = 0.115
rect_hdr = patches.Rectangle((0, 1.0 - header_h), 1.0, header_h, facecolor='#0F172A', edgecolor='#0284C7', lw=3)
ax.add_patch(rect_hdr)

# Subtle cyan glowing line under header
glow_line = patches.Rectangle((0, 1.0 - header_h - 0.003), 1.0, 0.003, facecolor='#00F2FE')
ax.add_patch(glow_line)

# Poster Title (Bold & Centered/Left)
ax.text(0.035, 0.965, "AUTONOMOUS COLLABORATIVE ROBOT SWARM SIMULATOR & DIGITAL TWIN",
        fontsize=24, fontweight='bold', color='#FFFFFF', va='center')
ax.text(0.035, 0.938, "Multi-Agent Pathfinding (MAPF) Driven by Conflict-Based Search (CBS) and Space-Time A* Search with Real-Time ROS2 / MQTT Telemetry",
        fontsize=14.5, color='#38BDF8', va='center')

# Author Name & Enrollment Number DIRECTLY BELOW TITLE (Mandated by SRU)
author_line = (
    "Candidate Name: SEETHARAM RAVULA (Enrollment No: 2303A52440)  |  "
    "Teammates: Sanjay (2303A52337), Sathwik (2303A52158)\n"
    "Project Guide: Dr. Sudha Rani, Assistant Professor  |  "
    "School of Computer Science and Artificial Intelligence, SR University, Warangal"
)
ax.text(0.035, 0.906, author_line, fontsize=12.5, fontweight='bold', color='#FFAB00', va='center', linespacing=1.3)

# UPPER RIGHT-HAND CORNER: SRU LOGO BRANDING (Mandated by SRU)
logo_path = os.path.join(fig_dir, "sru_logo.png")
if os.path.exists(logo_path):
    logo_img = Image.open(logo_path)
    # Place on upper right: x: [0.77, 0.97], y: [0.895, 0.985]
    ax.imshow(logo_img, extent=[0.77, 0.97, 0.895, 0.985], aspect='auto', zorder=10)

# =========================================================================
# HELPER: DRAW SECTION CARD
# =========================================================================
def draw_card(x, y, w, h, title, title_color='#00F2FE', tag=""):
    # Background panel
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012", facecolor='#111827', edgecolor='#1F2937', lw=2)
    ax.add_patch(rect)
    
    # Title bar inside panel
    rect_bar = patches.Rectangle((x+0.008, y+h-0.032), w-0.016, 0.026, facecolor='#1E293B')
    ax.add_patch(rect_bar)
    
    ax.text(x + 0.016, y + h - 0.019, title, fontsize=14, fontweight='bold', color=title_color, va='center')
    if tag:
        ax.text(x + w - 0.016, y + h - 0.019, tag, fontsize=10.5, fontweight='bold', color='#94A3B8', ha='right', va='center')
        
    return x + 0.016, y + h - 0.045, w - 0.032, h - 0.055

# =========================================================================
# 3-COLUMN A1 POSTER LAYOUT (16 WEEKS WORK FLOW)
# Column 1: x: [0.035, 0.335] (Width = 0.30)
# Column 2: x: [0.350, 0.650] (Width = 0.30)
# Column 3: x: [0.665, 0.965] (Width = 0.30)
# =========================================================================

# -------------------------------------------------------------------------
# COLUMN 1: INTRODUCTION & PROBLEM FORMULATION (WEEKS 1 - 6)
# -------------------------------------------------------------------------
# 1. Introduction & Motivation (Weeks 1-3)
x1, y1, w1, h1 = draw_card(0.035, 0.615, 0.30, 0.255, "1. INTRODUCTION & MOTIVATION", '#38BDF8', "WEEKS 1 - 3")
p1_text = (
    "• Background: In automated fulfillment centers (e.g. Amazon, Flipkart),\n"
    "  dense swarms of Automated Guided Vehicles (AGVs) navigate shared\n"
    "  floors transporting storage racks to packing stations.\n"
    "• Industrial Challenge: Prevent multi-robot collisions and deadlocks\n"
    "  while minimizing battery consumption and transit delays.\n"
    "• Algorithmic Dilemma:\n"
    "  - Coupled Joint A*: O(|V|^N) exponential explosion -> memory failure.\n"
    "  - Prioritized Planning: Fast O(N*T) but incomplete -> deadlocks & detours.\n"
    "• Project Aim: Architect a Conflict-Based Search (CBS) platform guaranteeing\n"
    "  100% collision-freedom, optimal Sum of Costs, and <1.0ms replanning."
)
ax.text(x1, y1, p1_text, fontsize=10.5, color='#F3F4F6', va='top', linespacing=1.35)

# Embed Figure 1.1 in Card 1
img_wh = Image.open(os.path.join(fig_dir, "fig1_warehouse_agv.png"))
ax.imshow(img_wh, extent=[0.05, 0.32, 0.625, 0.730], aspect='auto', zorder=5)

# 2. Problem Statement & Mathematical Formulation (Weeks 4-6)
x2, y2, w2, h2 = draw_card(0.035, 0.245, 0.30, 0.355, "2. PROBLEM FORMULATION & CONFLICTS", '#FFAB00', "WEEKS 4 - 6")
p2_text = (
    "• Discrete Graph Model: G = (V, E) with obstacle set O and free space V_free.\n"
    "  N agents A = {a1, a2, ..., aN} with start positions s_i and goal docks g_i.\n"
    "• Discrete Time Steps: t in {0, 1, 2, ..., T}. Actions: Move orthogonal or Wait.\n"
    "• Fundamental Conflict Primitives:\n"
    "  1. Vertex Conflict (ai, aj, v, t): Two AGVs occupy identical cell v at time t.\n"
    "  2. Edge Swap Conflict (ai, aj, u, v, t): AGVs traverse same edge oppositely:\n"
    "     p_i(t-1)=u, p_i(t)=v  AND  p_j(t-1)=v, p_j(t)=u.\n"
    "• Optimization Metric: Minimize Sum of Costs (SOC) = SUM_{i=1}^N len(path_i)."
)
ax.text(x2, y2, p2_text, fontsize=10.5, color='#F3F4F6', va='top', linespacing=1.35)

# Embed Conflict Primitives (Figure 3.1)
img_conf = Image.open(os.path.join(fig_dir, "fig3_conflicts.png"))
ax.imshow(img_conf, extent=[0.05, 0.32, 0.255, 0.415], aspect='auto', zorder=5)

# -------------------------------------------------------------------------
# COLUMN 2: SYSTEM ARCHITECTURE & CBS ENGINE (WEEKS 7 - 12)
# -------------------------------------------------------------------------
# 3. Two-Level CBS Search Architecture (Weeks 7-9)
x3, y3, w3, h3 = draw_card(0.350, 0.535, 0.30, 0.335, "3. CONFLICT-BASED SEARCH (CBS)", '#00F2FE', "WEEKS 7 - 9")
p3_text = (
    "• Two-Level Algorithmic Decomposition:\n"
    "  1. High-Level Constraint Tree (CT): Best-first search over conflict space.\n"
    "     Each node represents a constraint set, solution paths, and total cost.\n"
    "  2. Low-Level Space-Time A*: Searches 3D graph (x, y, t) with Manhattan\n"
    "     distance heuristic: f(v, t) = g(v, t) + h(v), where g(v, t) = t.\n"
    "• Selective Replanning: When branching on a conflict (ai, aj, v, t), only\n"
    "  constrained agent replans! Prunes 90%+ useless states."
)
ax.text(x3, y3, p3_text, fontsize=10.5, color='#F3F4F6', va='top', linespacing=1.35)

# Embed Constraint Tree (Figure 4.1)
img_cbs = Image.open(os.path.join(fig_dir, "fig4_cbs_tree.png"))
ax.imshow(img_cbs, extent=[0.365, 0.635, 0.545, 0.700], aspect='auto', zorder=5)

# 4. Digital Twin & Telemetry Bridge (Weeks 10-12)
x4, y4, w4, h4 = draw_card(0.350, 0.245, 0.30, 0.275, "4. DIGITAL TWIN & ROS2 TELEMETRY", '#10B981', "WEEKS 10 - 12")
p4_text = (
    "• Dual Execution Frontends:\n"
    "  - Desktop App (robot_swarm_cbs.py): Pure Python Tkinter GUI.\n"
    "  - Web Platform (index.html): Dark-mode HTML5 Canvas + TailwindCSS.\n"
    "• ROS2 / MQTT JSON Telemetry Bridge:\n"
    "  Broadcasts 50 Hz JSON payloads on /agv_telemetry topic (timestamp,\n"
    "  timestep, AGV positions, transit/docked states) for micro-ROS hardware.\n"
    "• Dynamic Floor Mutation: Click to insert/delete warehouse shelves;\n"
    "  solver re-routes paths in <1.0 ms without thread locking."
)
ax.text(x4, y4, p4_text, fontsize=10.5, color='#F3F4F6', va='top', linespacing=1.35)

# Embed Web Dashboard (Figure 6.2)
img_dash = Image.open(os.path.join(fig_dir, "fig6_web_dashboard.png"))
ax.imshow(img_dash, extent=[0.365, 0.635, 0.255, 0.365], aspect='auto', zorder=5)

# -------------------------------------------------------------------------
# COLUMN 3: EXPERIMENTAL RESULTS & CONCLUSION (WEEKS 13 - 16)
# -------------------------------------------------------------------------
# 5. Experimental Results & Benchmark Analysis (Weeks 13-15)
x5, y5, w5, h5 = draw_card(0.665, 0.495, 0.30, 0.375, "5. EXPERIMENTAL RESULTS", '#EC4899', "WEEKS 13 - 15")
p5_text = (
    "• Benchmark Platform: AMD Ryzen 7, 20x12 grid, 2 to 16 AGVs.\n"
    "• Runtime Scaling: CBS solves 4 AGVs in 0.82 ms and 16 AGVs in 45.6 ms,\n"
    "  whereas Coupled Joint A* experiences exponential timeouts (>10s).\n"
    "• Optimality: CBS delivers 100% optimal Sum of Costs, whereas Prioritized\n"
    "  Planning suffers a 4.3% to 22.6% detour penalty (excess battery drain).\n"
    "• Dynamic Replanning Latency: Mean 0.82 ms (99th percentile: 1.45 ms)."
)
ax.text(x5, y5, p5_text, fontsize=10.5, color='#F3F4F6', va='top', linespacing=1.35)

# Embed Runtime Graph (Figure 7.1)
img_rt = Image.open(os.path.join(fig_dir, "fig7_runtime_comparison.png"))
ax.imshow(img_rt, extent=[0.680, 0.950, 0.640, 0.740], aspect='auto', zorder=5)

# Embed SOC Bar Graph (Figure 7.2)
img_soc = Image.open(os.path.join(fig_dir, "fig7_sum_of_costs.png"))
ax.imshow(img_soc, extent=[0.680, 0.950, 0.505, 0.615], aspect='auto', zorder=5)

# 6. Conclusion, Outcomes & Future Scope (Week 16)
x6, y6, w6, h6 = draw_card(0.665, 0.245, 0.30, 0.235, "6. CONCLUSION & FUTURE WORK", '#A855F7', "WEEK 16")
p6_text = (
    "• Summary of Outcomes:\n"
    "  - Successfully formulated and implemented CBS + Space-Time A* in Python.\n"
    "  - Validated 100% collision-freedom across variable clutter densities.\n"
    "  - Integrated ROS2 / MQTT telemetry bridge for Industry 4.0 applications.\n"
    "• Future Directions:\n"
    "  - Continuous kinodynamics (turning radius and acceleration curves).\n"
    "  - Reinforcement Learning for CBS conflict branch prioritization.\n"
    "  - Physical deployment on ESP32 Mecanum robot swarms via micro-ROS."
)
ax.text(x6, y6, p6_text, fontsize=10.5, color='#F3F4F6', va='top', linespacing=1.35)

# =========================================================================
# BOTTOM SPAN: REFERENCES & PROJECT REPOSITORY ARTIFACTS
# =========================================================================
x_bot, y_bot, w_bot, h_bot = draw_card(0.035, 0.035, 0.930, 0.195, "7. REFERENCES & PROJECT DELIVERABLES (IEEE COMPLIANT)", '#FFFFFF', "SR UNIVERSITY CAPSTONE 2026-2027")

col_ref_text = (
    "KEY REFERENCES:\n"
    "[1] G. Sharon, R. Stern, A. Felner, N. Sturtevant, 'Conflict-Based Search for Optimal Multi-Agent Pathfinding', AI Journal, 2015.\n"
    "[2] R. Stern et al., 'Multi-Agent Pathfinding: Definitions, Variants, and Benchmarks', SoCS, 2019.\n"
    "[3] P. E. Hart, N. J. Nilsson, B. Raphael, 'A Formal Basis for Heuristic Determination of Minimum Cost Paths', IEEE SSC, 1968.\n"
    "[4] S. Macenski et al., 'Robot Operating System 2: Design, Architecture, and Uses in the Wild', Science Robotics, 2022.\n"
    "[5] P. R. Wurman, R. D'Andrea, M. Mountz, 'Coordinating Hundreds of Cooperative Autonomous Vehicles in Warehouses', AI Mag, 2008."
)
ax.text(0.05, 0.180, col_ref_text, fontsize=9.5, color='#CBD5E1', va='top', linespacing=1.3)

# Verified Deliverables Box
box_deliv = patches.FancyBboxPatch((0.63, 0.045), 0.32, 0.155, boxstyle="round,pad=0.01", facecolor='#1E293B', edgecolor='#38BDF8', lw=1.5)
ax.add_patch(box_deliv)

ax.text(0.645, 0.180, "VERIFIED SUBMISSION DELIVERABLES:", fontsize=11, fontweight='bold', color='#38BDF8', va='top')
deliv_list = (
    "• GitHub Codebase: https://github.com/2303A52440/capstone-project_3\n"
    "• Author Profile: https://www.linkedin.com/in/seetharam-ravula-422499381\n"
    "• Standalone Engine: robot_swarm_cbs.py (Pure Python 3 standard lib)\n"
    "• Web Digital Twin: index.html (TailwindCSS & HTML5 Canvas 60 FPS)\n"
    "• Capstone Documentation: 2303A52440-Seetharam Final Report.docx\n"
    "• Presentation Slide Deck: 2303A52440-Seetharam PPT.pptx (16 Slides)"
)
ax.text(0.645, 0.155, deliv_list, fontsize=9.5, color='#F3F4F6', va='top', linespacing=1.35)

# Save high-resolution A1 PNG and PDF
png_out = os.path.join(base_dir, "2303A52440-Seetharam Poster.png")
pdf_out = os.path.join(base_dir, "2303A52440-Seetharam Poster.pdf")

plt.savefig(png_out, dpi=200, facecolor='#070B14')
plt.savefig(pdf_out, dpi=200, facecolor='#070B14')
plt.close()

print("A1 Poster successfully generated in PNG and PDF formats!")
print("PNG:", png_out)
print("PDF:", pdf_out)
