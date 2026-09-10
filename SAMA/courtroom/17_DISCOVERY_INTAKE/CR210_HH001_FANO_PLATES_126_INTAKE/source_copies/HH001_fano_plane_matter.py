"""
HH001 supporting visual.

Render the Fano plane structure that the math forces at D=3:
  F_2^3 has 8 elements
  1 is the origin (000) = carrier = 18 cells
  7 are non-zero vectors = matter modes, arranged as the Fano plane
  Each matter point holds 18 cells, total 7 * 18 = 126
  R^2 = 144 = 18 + 126

The 7 Fano lines (3 triangle sides + 3 medians + 1 inscribed circle)
each connect 3 matter points whose XOR sums to 000 (the carrier).
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

OUTPUT_PATH = r"C:/VS/Haunted_House/explorations/HH001_fano_plane_matter.png"

BG = "#0a0a12"
LINE = "#6db6ff"
POINT = "#ffd54a"
TEXT = "#f0f0f5"
DIM = "#a0a0b0"
CARRIER = "#ff5b6b"

fig, ax = plt.subplots(figsize=(12, 13))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(-1.7, 1.7)
ax.set_ylim(-1.95, 1.85)
ax.set_aspect("equal")
ax.axis("off")

# Three equilateral-triangle corners
theta = [np.pi / 2, np.pi / 2 + 2 * np.pi / 3, np.pi / 2 + 4 * np.pi / 3]
R = 1.05
corners = [(R * np.cos(t), R * np.sin(t)) for t in theta]

# F_2^3 labeling: corners = 100, 010, 001
pts = {
    "100": corners[0],
    "010": corners[1],
    "001": corners[2],
}

# Edge midpoints = XOR of the two adjacent corners
pts["110"] = ((pts["100"][0] + pts["010"][0]) / 2, (pts["100"][1] + pts["010"][1]) / 2)
pts["011"] = ((pts["010"][0] + pts["001"][0]) / 2, (pts["010"][1] + pts["001"][1]) / 2)
pts["101"] = ((pts["100"][0] + pts["001"][0]) / 2, (pts["100"][1] + pts["001"][1]) / 2)

# Geometric center = 111 (XOR of all three basis vectors)
pts["111"] = (0.0, 0.0)

# Verify the Fano lines (each triple XORs to 000)
def xor_triple(a, b, c):
    ai, bi, ci = int(a, 2), int(b, 2), int(c, 2)
    return ai ^ bi ^ ci

sides = [
    ("100", "110", "010"),
    ("010", "011", "001"),
    ("100", "101", "001"),
]
medians = [
    ("100", "111", "011"),
    ("010", "111", "101"),
    ("001", "111", "110"),
]
incircle = ["110", "011", "101"]

for trip in sides + medians + [tuple(incircle)]:
    assert xor_triple(*trip) == 0, f"line {trip} does not XOR to 000"

# Draw triangle sides
for s in sides:
    xs = [pts[p][0] for p in s]
    ys = [pts[p][1] for p in s]
    ax.plot(xs, ys, color=LINE, linewidth=2.6, alpha=0.85, zorder=2)

# Draw medians
for m in medians:
    xs = [pts[p][0] for p in m]
    ys = [pts[p][1] for p in m]
    ax.plot(xs, ys, color=LINE, linewidth=2.6, alpha=0.85, zorder=2)

# Draw inscribed circle through the 3 edge midpoints
mid_xs = [pts[m][0] for m in incircle]
mid_ys = [pts[m][1] for m in incircle]
cx, cy = sum(mid_xs) / 3, sum(mid_ys) / 3
rad = np.hypot(mid_xs[0] - cx, mid_ys[0] - cy)
ax.add_patch(Circle((cx, cy), rad, fill=False, color=LINE, linewidth=2.6, alpha=0.85, zorder=2))

# Mark the carrier (origin 000) as an algebraic-only annotation
# It sits *behind* everything, visually represented as a soft glow at center
glow = Circle((0, 0), 0.45, color=CARRIER, alpha=0.10, zorder=1)
ax.add_patch(glow)
glow2 = Circle((0, 0), 0.30, color=CARRIER, alpha=0.15, zorder=1)
ax.add_patch(glow2)

# Draw the 7 matter points
for label, (x, y) in pts.items():
    ax.scatter([x], [y], s=900, c=POINT, edgecolor="white", linewidth=2.2, zorder=5)
    ax.text(x, y, label, ha="center", va="center",
            fontsize=11, fontweight="bold", color=BG, zorder=6)

# Annotate each point with "18 cells"
offsets = {
    "100": (0.00, 0.22),
    "010": (-0.22, -0.05),
    "001": (0.22, -0.05),
    "110": (-0.16, 0.05),
    "011": (0.00, -0.22),
    "101": (0.16, 0.05),
    "111": (0.21, -0.18),
}
for label, (dx, dy) in offsets.items():
    x, y = pts[label]
    ax.text(x + dx, y + dy, "18 cells",
            ha="center", va="center",
            fontsize=8.5, color=TEXT, zorder=6)

# Title and headline equation
ax.text(0, 1.72, "F_2^3  at  D = 3",
        ha="center", fontsize=20, fontweight="bold", color=TEXT)
ax.text(0, 1.55, "R^2  =  144  =  18  +  126  =  8 x 18",
        ha="center", fontsize=15, color=POINT)

# Carrier callout (the 000 origin is not a Fano point)
ax.text(0, -1.45,
        "carrier  =  000  =  18 cells  (the algebraic origin)",
        ha="center", fontsize=12, color=CARRIER, fontweight="bold")
ax.text(0, -1.58,
        "every Fano line is a triple of matter points whose XOR = 000",
        ha="center", fontsize=11, color=TEXT)
ax.text(0, -1.70,
        "the carrier sits at the geometric center where every line closes back",
        ha="center", fontsize=10, color=DIM, style="italic")
ax.text(0, -1.82,
        "(the labeled point at center is 111, the seventh matter mode, not the carrier)",
        ha="center", fontsize=8.5, color=DIM, style="italic")

# Legend in upper left
legend_x = -1.6
ax.text(legend_x, 1.72, "Fano plane structure:",
        fontsize=10.5, color=TEXT, fontweight="bold")
ax.text(legend_x, 1.60, "- 7 points (matter modes)", fontsize=9.5, color=TEXT)
ax.text(legend_x, 1.50, "- 7 lines  (3 sides + 3 medians + 1 circle)",
        fontsize=9.5, color=TEXT)
ax.text(legend_x, 1.40, "- each line: 3 collinear points",
        fontsize=9.5, color=TEXT)
ax.text(legend_x, 1.30, "- each line XORs back to 000",
        fontsize=9.5, color=TEXT)

# Right-side: closed-loop accounting
right_x = 0.72
ax.text(right_x, 1.72, "closed-loop accounting:",
        fontsize=10.5, color=TEXT, fontweight="bold")
ax.text(right_x, 1.60, "R = 12,  D = 3", fontsize=9.5, color=TEXT)
ax.text(right_x, 1.50, "2^D = 8 face-states", fontsize=9.5, color=TEXT)
ax.text(right_x, 1.40, "R^2 / 2^D = 18 cells/state", fontsize=9.5, color=TEXT)
ax.text(right_x, 1.30, "7 retained + 1 released", fontsize=9.5, color=TEXT)

plt.savefig(OUTPUT_PATH, dpi=220, bbox_inches="tight", facecolor=BG)
plt.close()
print(f"PNG saved: {OUTPUT_PATH}")
