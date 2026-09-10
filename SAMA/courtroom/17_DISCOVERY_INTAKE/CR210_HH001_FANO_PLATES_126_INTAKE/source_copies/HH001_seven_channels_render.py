"""HH001 - Seven-channel Fano plane visualizations.

Two PNGs:
  (1) HH001_seven_channels.png
      One Fano plane with the 7 SAM A-field readout channels labeled at the
      7 points, and the 7 closure laws labeled along the 7 lines.

  (2) HH001_fractal_126.png
      126 mini Fano planes arranged as 7 channel-rows x 18 cells-per-channel,
      showing the recursion: each of the 126 matter cells is itself a Fano
      plane carrying all seven channel readouts.

Channel-to-binary assignment (verified: every Fano line XORs to 000):
    100 PARTICLE         110 GRAVITY        011 CLOCK
    010 MATTER           101 LIGHT          111 ACTION
    001 ELEMENT

Lines (each triple XORs to 000 = the carrier):
    sides:      {PARTICLE, GRAVITY, MATTER}     - mass-source rule
                {MATTER, CLOCK, ELEMENT}        - binding/decay over time
                {PARTICLE, LIGHT, ELEMENT}      - atomic spectra
    medians:    {PARTICLE, ACTION, CLOCK}       - Schrodinger evolution
                {MATTER, ACTION, LIGHT}         - QED matter-light coupling
                {ELEMENT, ACTION, GRAVITY}      - nuclear binding <-> gravity
    in-circle:  {GRAVITY, CLOCK, LIGHT}         - Schwarzschild GR triple
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

BG          = "#0a0a14"
TEXT        = "#f5f5fa"
DIM         = "#a0a0b0"
GOLD        = "#ffd54a"
TEAL        = "#5be0d2"
RED         = "#ff5b6b"
LINE_SIDE   = "#6db6ff"
LINE_MED    = "#b89cff"
LINE_CIRC   = "#5be0a0"

CHANNEL = {
    "100": ("PARTICLE", GOLD),
    "010": ("MATTER",   GOLD),
    "001": ("ELEMENT",  GOLD),
    "110": ("GRAVITY",  TEAL),
    "011": ("CLOCK",    TEAL),
    "101": ("LIGHT",    TEAL),
    "111": ("ACTION",   TEAL),
}

SIDES = [
    (("100", "110", "010"), "mass-source rule",            LINE_SIDE),
    (("010", "011", "001"), "binding & decay over time",   LINE_SIDE),
    (("100", "101", "001"), "atomic spectra",              LINE_SIDE),
]
MEDIANS = [
    (("100", "111", "011"), "Schrodinger evolution",       LINE_MED),
    (("010", "111", "101"), "QED matter-light coupling",   LINE_MED),
    (("001", "111", "110"), "nuclear binding <-> gravity", LINE_MED),
]
CIRCLE_LINE = (("110", "011", "101"), "Schwarzschild GR triple", LINE_CIRC)


def fano_positions(R=1.0):
    theta = [np.pi/2, np.pi/2 + 2*np.pi/3, np.pi/2 + 4*np.pi/3]
    corners = [(R*np.cos(t), R*np.sin(t)) for t in theta]
    pts = {
        "100": corners[0],
        "010": corners[1],
        "001": corners[2],
    }
    pts["110"] = ((pts["100"][0] + pts["010"][0])/2, (pts["100"][1] + pts["010"][1])/2)
    pts["011"] = ((pts["010"][0] + pts["001"][0])/2, (pts["010"][1] + pts["001"][1])/2)
    pts["101"] = ((pts["100"][0] + pts["001"][0])/2, (pts["100"][1] + pts["001"][1])/2)
    pts["111"] = (0.0, 0.0)
    return pts


def verify_lines():
    """Cross-check every Fano line XORs to 000."""
    def xt(a, b, c):
        return int(a, 2) ^ int(b, 2) ^ int(c, 2)
    for trip, _, _ in SIDES + MEDIANS:
        assert xt(*trip) == 0, f"side/median {trip} does not XOR to 000"
    assert xt(*CIRCLE_LINE[0]) == 0, f"circle line does not XOR to 000"


def label_along(ax, p1, p3, text, color, perp_offset, fontsize=10):
    mx = (p1[0]+p3[0])/2
    my = (p1[1]+p3[1])/2
    dx, dy = p3[0]-p1[0], p3[1]-p1[1]
    angle = np.degrees(np.arctan2(dy, dx))
    if angle > 90 or angle < -90:
        angle += 180
    norm = np.hypot(dx, dy)
    if norm > 0:
        mx += -dy/norm * perp_offset
        my += dx/norm * perp_offset
    ax.text(mx, my, text, ha="center", va="center",
            fontsize=fontsize, color=color, rotation=angle,
            zorder=4, fontweight="bold")


def make_seven_channels(output_path):
    pts = fano_positions(R=1.05)

    fig, ax = plt.subplots(figsize=(14, 14))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(-1.95, 1.95)
    ax.set_ylim(-1.95, 1.95)
    ax.set_aspect("equal")
    ax.axis("off")

    # Carrier glow at center
    for r_glow, alpha in [(0.70, 0.04), (0.55, 0.06), (0.40, 0.09), (0.27, 0.14)]:
        ax.add_patch(Circle((0, 0), r_glow, color=RED, alpha=alpha, zorder=1))

    # Draw triangle sides
    for trip, _, color in SIDES:
        xs = [pts[p][0] for p in trip]
        ys = [pts[p][1] for p in trip]
        ax.plot(xs, ys, color=color, linewidth=2.6, alpha=0.85, zorder=2)

    # Draw medians
    for trip, _, color in MEDIANS:
        xs = [pts[p][0] for p in trip]
        ys = [pts[p][1] for p in trip]
        ax.plot(xs, ys, color=color, linewidth=2.6, alpha=0.85, zorder=2)

    # Inscribed circle through three edge midpoints
    mid = CIRCLE_LINE[0]
    mid_xs = [pts[m][0] for m in mid]
    mid_ys = [pts[m][1] for m in mid]
    cx_circ = sum(mid_xs)/3
    cy_circ = sum(mid_ys)/3
    rad = np.hypot(mid_xs[0]-cx_circ, mid_ys[0]-cy_circ)
    ax.add_patch(Circle((cx_circ, cy_circ), rad, fill=False,
                        color=LINE_CIRC, linewidth=2.6, alpha=0.85, zorder=2))

    # Nodes
    for code, (x, y) in pts.items():
        name, color = CHANNEL[code]
        ax.scatter([x], [y], s=1900, c=color, edgecolor="white",
                   linewidth=2.5, zorder=5)
        ax.text(x, y+0.025, name, ha="center", va="center",
                fontsize=10, color=BG, fontweight="bold", zorder=6)
        ax.text(x, y-0.075, code, ha="center", va="center",
                fontsize=6.5, color=BG, zorder=6)

    # Side labels (triangle edges)
    label_along(ax, pts[SIDES[0][0][0]], pts[SIDES[0][0][2]],
                SIDES[0][1], LINE_SIDE,  0.20)
    label_along(ax, pts[SIDES[1][0][0]], pts[SIDES[1][0][2]],
                SIDES[1][1], LINE_SIDE, -0.20)
    label_along(ax, pts[SIDES[2][0][0]], pts[SIDES[2][0][2]],
                SIDES[2][1], LINE_SIDE,  0.20)

    # Median labels: place between corner and center
    for trip, text, color in MEDIANS:
        corner = pts[trip[0]]
        center = pts[trip[1]]
        mx = (corner[0]+center[0])/2
        my = (corner[1]+center[1])/2
        dx, dy = center[0]-corner[0], center[1]-corner[1]
        angle = np.degrees(np.arctan2(dy, dx))
        if angle > 90 or angle < -90:
            angle += 180
        norm = np.hypot(dx, dy)
        perp = 0.12
        ax.text(mx + -dy/norm*perp, my + dx/norm*perp, text,
                ha="center", va="center", fontsize=9.5,
                color=color, rotation=angle, zorder=4, fontweight="bold")

    # Inscribed circle label - placed below the action node along the arc
    ax.text(0, -0.62, CIRCLE_LINE[1], ha="center", va="center",
            fontsize=10, color=LINE_CIRC, zorder=4, fontweight="bold")

    # Title block
    ax.text(0, 1.78, "ONE  of  126  Substrate  Units",
            ha="center", fontsize=22, fontweight="bold", color=TEXT)
    ax.text(0, 1.62, "Each unit is a Fano plane",
            ha="center", fontsize=13, color=DIM)
    ax.text(0, 1.50,
            "7 channel readouts at the 7 points    |    7 closure laws along the 7 lines",
            ha="center", fontsize=10.5, color=DIM)

    # Legend
    ax.text(-1.85, 1.78, "Channel types:", fontsize=11, color=TEXT, fontweight="bold")
    ax.text(-1.85, 1.65, "gold = structural (PARTICLE / MATTER / ELEMENT)",
            fontsize=9, color=GOLD)
    ax.text(-1.85, 1.55, "teal = field      (GRAVITY / CLOCK / LIGHT / ACTION)",
            fontsize=9, color=TEAL)
    ax.text(-1.85, 1.40, "Line types:", fontsize=11, color=TEXT, fontweight="bold")
    ax.text(-1.85, 1.30, "blue   = triangle sides (3)", fontsize=9, color=LINE_SIDE)
    ax.text(-1.85, 1.20, "purple = medians (3)",      fontsize=9, color=LINE_MED)
    ax.text(-1.85, 1.10, "green  = inscribed circle (1)", fontsize=9, color=LINE_CIRC)

    # Bottom
    ax.text(0, -1.50,
            "CARRIER  (000)  =  gravity write  =  the algebraic center every line XORs to",
            ha="center", fontsize=11, color=RED, fontweight="bold")
    ax.text(0, -1.65,
            "Seven physics.  One Fano plane.  One closure rule.",
            ha="center", fontsize=12, color=TEXT, fontweight="bold")
    ax.text(0, -1.78,
            "Recursion: each Fano point holds its own internal Fano plane.   Repeat 126 times.",
            ha="center", fontsize=10, color=DIM, style="italic")

    plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"Saved: {output_path}")


def draw_mini_fano(ax, cx, cy, size, color, alpha=0.95):
    theta = [np.pi/2, np.pi/2 + 2*np.pi/3, np.pi/2 + 4*np.pi/3]
    corners = [(cx + size*np.cos(t), cy + size*np.sin(t)) for t in theta]
    midpoints = [
        ((corners[0][0]+corners[1][0])/2, (corners[0][1]+corners[1][1])/2),
        ((corners[1][0]+corners[2][0])/2, (corners[1][1]+corners[2][1])/2),
        ((corners[0][0]+corners[2][0])/2, (corners[0][1]+corners[2][1])/2),
    ]
    # sides
    for i in range(3):
        x1, y1 = corners[i]
        x2, y2 = corners[(i+1) % 3]
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=0.5,
                alpha=alpha*0.7, zorder=2)
    # medians
    for c in corners:
        ax.plot([c[0], cx], [c[1], cy], color=color, linewidth=0.5,
                alpha=alpha*0.5, zorder=2)
    # inscribed circle through the three midpoints
    rad = np.hypot(midpoints[0][0]-cx, midpoints[0][1]-cy)
    ax.add_patch(Circle((cx, cy), rad, fill=False, color=color,
                        linewidth=0.5, alpha=alpha*0.55, zorder=2))
    # dots
    for x, y in corners + midpoints + [(cx, cy)]:
        ax.scatter([x], [y], s=6, c=color, edgecolor="none",
                   alpha=alpha, zorder=3)


def make_fractal_126(output_path):
    channels = ["PARTICLE", "MATTER", "ELEMENT", "GRAVITY", "CLOCK", "LIGHT", "ACTION"]
    binary   = ["100",      "010",     "001",     "110",      "011",   "101",   "111"]
    row_colors = ["#ffd54a", "#ffaa3d", "#ff7a3a",
                  "#5be0d2", "#5bd6e0", "#5b9bff", "#b89cff"]

    n_rows = 7
    n_cols = 18
    spacing = 1.0
    mini_size = 0.34

    fig, ax = plt.subplots(figsize=(22, 11))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(-3.0, n_cols*spacing + 0.5)
    ax.set_ylim(-1.8, n_rows*spacing + 1.7)
    ax.set_aspect("equal")
    ax.axis("off")

    cx_title = (n_cols*spacing)/2 - 1.0
    ax.text(cx_title, n_rows*spacing + 0.85,
            "126  Fano  planes  =  7  channel  rows  x  18  cells",
            ha="center", fontsize=22, fontweight="bold", color=TEXT)
    ax.text(cx_title, n_rows*spacing + 0.40,
            "Each cell is itself a Fano plane carrying the same seven channels.",
            ha="center", fontsize=13, color=DIM)
    ax.text(cx_title, n_rows*spacing + 0.05,
            "The substrate is fractally self-similar:  the closure law repeats at every scale.",
            ha="center", fontsize=11, color=DIM, style="italic")

    for row in range(n_rows):
        color = row_colors[row]
        y = (n_rows - 1 - row) * spacing
        ax.text(-0.8, y+0.04, channels[row], ha="right", va="center",
                fontsize=13, color=color, fontweight="bold")
        ax.text(-0.8, y-0.30, binary[row], ha="right", va="center",
                fontsize=8.5, color="#777")
        for col in range(n_cols):
            cx = col*spacing + 0.5
            cy = y
            draw_mini_fano(ax, cx, cy, mini_size, color, alpha=0.95)

    ax.text(cx_title, -0.85,
            "144  =  18  +  126        126  =  7  x  18        each cell  =  8 sub-face-states  =  7 sub-channels + 1 sub-carrier",
            ha="center", fontsize=12, color=TEXT, fontweight="bold")
    ax.text(cx_title, -1.30,
            "7 rows = the 7 channels of physics.    Each row's 18 cells = the substrate inventory for that channel.",
            ha="center", fontsize=10, color=DIM, style="italic")

    plt.savefig(output_path, dpi=180, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    verify_lines()
    make_seven_channels("C:/VS/Haunted_House/explorations/HH001_seven_channels.png")
    make_fractal_126("C:/VS/Haunted_House/explorations/HH001_fractal_126.png")
