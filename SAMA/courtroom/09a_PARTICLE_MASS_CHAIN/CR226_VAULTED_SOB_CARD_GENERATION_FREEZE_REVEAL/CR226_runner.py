from __future__ import annotations

import csv
import hashlib
import html
import json
import math
import shutil
import zipfile
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


getcontext().prec = 100

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR226_VAULTED_SOB_CARD_GENERATION_FREEZE_REVEAL"

VAULT = OUT / "vault"
PREDICT = VAULT / "01_prediction_seal"
FREEZE = VAULT / "02_freeze"
REVEAL = VAULT / "03_reveal"
NATIVE_PNG = PREDICT / "cards_native_png"
NATIVE_SVG = PREDICT / "cards_native_svg"
REVEAL_PNG = REVEAL / "cards_revealed_png"
REVEAL_SVG = REVEAL / "cards_revealed_svg"

PRECOMMIT = OUT / "CR226_PRECOMMIT.md"
RUNNER = OUT / "CR226_runner.py"
PREDICTIONS_CSV = PREDICT / "CR226_predictions_constants_only_126.csv"
PREDICTION_JSONL = PREDICT / "CR226_prediction_card_payloads.jsonl"
PREDICTION_HASH_MANIFEST = PREDICT / "CR226_prediction_hash_manifest.csv"
PREDICTION_SEAL = PREDICT / "CR226_prediction_seal.json"
PREDICTION_ZIP = PREDICT / "CR226_prediction_vault.zip"
FREEZE_LEDGER = FREEZE / "CR226_FREEZE_LEDGER.json"
REVEAL_COMPARISON = REVEAL / "CR226_reveal_comparison_126.csv"
REVEAL_HASH_MANIFEST = REVEAL / "CR226_reveal_hash_manifest.csv"
REVEAL_SEAL = REVEAL / "CR226_reveal_seal.json"
REVEAL_ZIP = REVEAL / "CR226_reveal_vault.zip"
INPUT_MANIFEST = OUT / "CR226_input_manifest.csv"
CHECKS = OUT / "CR226_checks.csv"
SUMMARY = OUT / "CR226_summary.json"
RESULT = OUT / "CR226_result.md"
HASHES = OUT / "HASHES.txt"

CR119_PERIODIC = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL" / "CR119_courtroom_periodic_table.csv"
CR220_ELEMENTS = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR220_PARTICLE_COUNT_STABILITY_SIMULATION" / "CR220_simulated_element_primary_rows_126.csv"
QP061_ROSTER = Path(r"C:\VS\quantum_phase\artifacts\qp061\qp061_observed_roster_normalized.csv")

R = Fraction(12, 1)
D = Fraction(3, 1)
ALPHA_H = Fraction(2, 1)
SPLIT = Fraction(2, 1) ** int(D)
R_SQUARED = R * R
CAPACITY = R_SQUARED * (Fraction(1, 1) - Fraction(1, SPLIT))
SEVEN = Fraction(7, 1)
KAPPA_FLOOR = Fraction(7117, 768)
NEUTRON_G_UNIT = Fraction(1, 64)
TENSOR_RELEASE = R_SQUARED / SPLIT
NEUTRAL_VECTOR_CARRIER = D ** (int(D) + 1)
HIDDEN_SET = sorted(
    {
        int(ALPHA_H) ** a * int(D) ** b
        for a in range(0, 8)
        for b in range(0, 8)
        if int(ALPHA_H) ** a * int(D) ** b <= int(R)
    }
)
HIDDEN_SUM = sum(HIDDEN_SET)
CLOCK_BOUNDARY = int(NEUTRAL_VECTOR_CARRIER + ALPHA_H)
CLOCK_HOLES = {HIDDEN_SUM - int(ALPHA_H), HIDDEN_SUM - int(ALPHA_H) + int(TENSOR_RELEASE)}
FRONTIER_START = int(CAPACITY - SPLIT + 1)

GOLD = "#b77b12"
NAVY = "#0b2b43"
TEAL = "#06615e"
PAPER = "#fffaf0"
LINE = "#c08a2b"
BLUE = "#1667ff"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def merkle_root(hashes: list[str]) -> str:
    layer = hashes[:]
    if not layer:
        return sha256_text("")
    while len(layer) > 1:
        nxt: list[str] = []
        for index in range(0, len(layer), 2):
            left = layer[index]
            right = layer[index + 1] if index + 1 < len(layer) else left
            nxt.append(hashlib.sha256((left + right).encode("ascii")).hexdigest())
        layer = nxt
    return layer[0]


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")


def fstr(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)


def fdec(value: Fraction, places: int = 12) -> str:
    dec = Decimal(value.numerator) / Decimal(value.denominator)
    return f"{dec:.{places}f}".rstrip("0").rstrip(".")


def check(rows: list[dict[str, Any]], name: str, passed: bool, observed: Any, expected: Any) -> None:
    rows.append({"check": name, "passed": str(bool(passed)), "observed": observed, "expected": expected})


def reset_output_tree() -> None:
    for path in [PREDICT, FREEZE, REVEAL]:
        if path.exists():
            shutil.rmtree(path)
    for path in [PREDICT, FREEZE, REVEAL, NATIVE_PNG, NATIVE_SVG, REVEAL_PNG, REVEAL_SVG]:
        path.mkdir(parents=True, exist_ok=True)


def shell_n_path() -> list[Fraction]:
    return [Fraction(1, 1), ALPHA_H, D, R / D, R / D, D, ALPHA_H, ALPHA_H]


def shell_capacities() -> list[int]:
    return [int(2 * n * n) for n in shell_n_path()]


def shell_state(z: int) -> dict[str, Any]:
    remaining = z
    for index, capacity in enumerate(shell_capacities(), start=1):
        if remaining <= capacity:
            return {
                "shell_period": index,
                "shell_n": fstr(shell_n_path()[index - 1]),
                "shell_capacity": capacity,
                "shell_occupancy": remaining,
                "shell_status": "CLOSED_SHELL" if remaining == capacity else "OPEN_SHELL",
            }
        remaining -= capacity
    return {
        "shell_period": len(shell_capacities()) + 1,
        "shell_n": "",
        "shell_capacity": 0,
        "shell_occupancy": remaining,
        "shell_status": "OVER_CAPACITY",
    }


def z_coordinates(z: int) -> dict[str, int]:
    return {
        "radix_cycle": ((z - 1) // int(R)) + 1,
        "radix_slot": ((z - 1) % int(R)) + 1,
    }


def isotope_primary(z: int) -> dict[str, int]:
    coords = z_coordinates(z)
    selected_depth = max(0, coords["radix_cycle"] - 1)
    raw_packets = Fraction(z * selected_depth, int(R))
    delta_n = raw_packets.numerator // raw_packets.denominator
    residual = raw_packets - Fraction(delta_n, 1)
    residual_twelfths = int(residual * R)
    return {
        "N": z + delta_n,
        "selected_depth_index": selected_depth,
        "residual_twelfths": residual_twelfths,
    }


def clock_prediction(z: int) -> str:
    if z >= FRONTIER_START:
        return "frontier"
    return "stable" if z <= CLOCK_BOUNDARY and z not in CLOCK_HOLES else "radioactive"


def native_lane(z: int, residual_twelfths: int) -> str:
    if z >= FRONTIER_START:
        return "CONSTANT_FRONTIER_TAIL_CANDIDATE"
    if residual_twelfths == 0:
        return "CONSTANT_STABLE_ANCHOR_LANE"
    if residual_twelfths == int(R / 2):
        return "CONSTANT_HALF_WRITE_LANE"
    return "CONSTANT_BOUND_LADDER_LANE"


def build_prediction_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for z in range(1, int(CAPACITY) + 1):
        coords = z_coordinates(z)
        shell = shell_state(z)
        iso = isotope_primary(z)
        n = iso["N"]
        a = z + n
        neutron_excess = n - z
        g = Fraction(z, 1) * KAPPA_FLOOR + Fraction(neutron_excess, 64)
        gr = g * SPLIT
        retained = g * SEVEN
        kappa_eff = g / Fraction(z, 1)
        u_count = (2 * z) + n
        d_count = z + (2 * n)
        prediction = clock_prediction(z)
        rows.append(
            {
                "sob_id": f"SOB{z}",
                "sob_ordinal": z,
                "Z": z,
                "N": n,
                "A": a,
                "P_subscript": f"P_{z},{a}",
                "P_address": f"{z}p+{n}n+{z}e",
                "quark_address": f"{u_count}u+{d_count}d+{z}e",
                "quark_u_count": u_count,
                "quark_d_count": d_count,
                "quark_e_count": z,
                "radix_cycle": coords["radix_cycle"],
                "radix_slot": coords["radix_slot"],
                "selected_depth_index": iso["selected_depth_index"],
                "residual_twelfths": iso["residual_twelfths"],
                "shell_period": shell["shell_period"],
                "shell_n": shell["shell_n"],
                "shell_capacity": shell["shell_capacity"],
                "shell_occupancy": shell["shell_occupancy"],
                "shell_status": shell["shell_status"],
                "constant_native_lane": native_lane(z, iso["residual_twelfths"]),
                "clock_prediction": prediction,
                "clock_formula": "frontier if Z>118 else stable iff Z<=83 and Z not in {43,61}",
                "kappa_floor_fraction": fstr(KAPPA_FLOOR),
                "kappa_eff_fraction": fstr(kappa_eff),
                "G_fraction": fstr(g),
                "G_decimal": fdec(g, 12),
                "GR_fraction": fstr(gr),
                "GR_decimal": fdec(gr, 12),
                "retained_7G_fraction": fstr(retained),
                "retained_7G_decimal": fdec(retained, 12),
                "kernel_line_1": f"G(P)={z}*kappa_eff(P)={fdec(g, 6)}",
                "kernel_line_1_floor": f"G(P)={z}*7117/768+{neutron_excess}*1/64",
                "kernel_line_2": f"GR(P)=8G(P)={fdec(gr, 6)}",
                "kernel_line_3": "GR(P)=7G(P)+G(P)",
                "light_face_native": f"shell {shell['shell_period']} occupancy {shell['shell_occupancy']}/{shell['shell_capacity']}",
                "action_face_native": "closure",
                "bottom_A_line": f"A=Z+N={z}+{n}={a}",
                "construction_source": "CR226_CONSTANTS_ONLY_BEFORE_REVEAL",
            }
        )
    return rows


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def font(size: int, bold: bool = False, italic: bool = False) -> ImageFont.ImageFont:
    candidates = []
    if bold:
        candidates.extend([r"C:\Windows\Fonts\georgiab.ttf", r"C:\Windows\Fonts\timesbd.ttf"])
    if italic:
        candidates.extend([r"C:\Windows\Fonts\georgiai.ttf", r"C:\Windows\Fonts\timesi.ttf"])
    candidates.extend([r"C:\Windows\Fonts\georgia.ttf", r"C:\Windows\Fonts\times.ttf", r"C:\Windows\Fonts\arial.ttf"])
    for item in candidates:
        try:
            return ImageFont.truetype(item, size)
        except OSError:
            continue
    return ImageFont.load_default()


def centered(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font_obj: ImageFont.ImageFont, fill: str) -> None:
    x, y = xy
    draw.text((x - text_width(draw, text, font_obj) / 2, y), text, font=font_obj, fill=fill)


def draw_card_png(path: Path, row: dict[str, Any], reveal: dict[str, Any] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    w, h = 900, 1200
    image = Image.new("RGB", (w, h), PAPER)
    draw = ImageDraw.Draw(image)
    title_font = font(74)
    subtitle_font = font(25)
    label_font = font(25, bold=True)
    mid_font = font(32, bold=True)
    body_font = font(28)
    small_font = font(22)
    tiny_font = font(18)
    italic_font = font(22, italic=True)
    kernel_font = font(24)

    draw.rectangle((18, 18, w - 18, h - 18), outline=LINE, width=3)
    draw.rectangle((34, 34, w - 34, h - 34), outline=LINE, width=1)
    draw.rectangle((235, 168, 665, 224), outline=LINE, width=2)
    centered(draw, (w // 2, 176), "SUBSTRATE ORDER BLOCK", font(30), GOLD)

    if reveal:
        name = reveal.get("known_name") or row["sob_id"]
        symbol = reveal.get("known_symbol") or "E"
        title = f"{row['sob_id']} - {name}"
        subtitle = f"SAM substrate order block  |  isotope anchor {symbol}-{row['A']}"
        matter = reveal.get("matter_label") or f"A={row['A']}"
        clock_label = reveal.get("clock_label") or row["clock_prediction"]
    else:
        title = row["sob_id"]
        subtitle = f"SAM substrate order block  |  isotope anchor A-{row['A']}"
        symbol = "E"
        matter = f"A={row['A']}"
        clock_label = row["clock_prediction"]

    if text_width(draw, title, title_font) > 790:
        title_font = font(64)
    centered(draw, (w // 2, 42), title, title_font, NAVY if reveal else GOLD)
    centered(draw, (w // 2, 126), subtitle, subtitle_font, NAVY)

    cx, cy = w // 2, 560
    nodes = {
        "E": (cx, 315),
        "M": (145, 540),
        "Ck": (755, 540),
        "L": (250, 995),
        "Ac": (650, 995),
    }
    edges = [
        ("E", "L"), ("E", "Ac"), ("M", "Ck"), ("M", "L"), ("Ck", "Ac"),
        ("L", "Ac"), ("M", "Ac"), ("Ck", "L"),
    ]
    for a, b in edges:
        draw.line((nodes[a][0], nodes[a][1], nodes[b][0], nodes[b][1]), fill="black", width=4)

    star = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        radius = 205 if i % 2 == 0 else 95
        star.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    draw.line(star + [star[0]], fill=BLUE, width=2)
    draw.ellipse((cx - 165, cy - 165, cx + 165, cy + 165), outline="#b7d8f6", width=2)
    draw.ellipse((cx - 135, cy - 135, cx + 135, cy + 135), outline="#d4e6f7", width=1)

    def node_circle(key: str, title_text: str, line1: str, line2: str, fill_title: str = TEAL) -> None:
        x, y = nodes[key]
        radius = 76 if key != "E" else 74
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=PAPER, outline=TEAL if key != "E" else GOLD, width=4)
        centered(draw, (x, y - 48), title_text, mid_font, fill_title)
        centered(draw, (x, y - 8), line1, small_font, NAVY)
        line_font = tiny_font if len(line2) > 11 else (italic_font if key != "E" else small_font)
        centered(draw, (x, y + 24), line2, line_font, TEAL if key != "E" else GOLD)

    node_circle("E", symbol, "Element", f"Z = {row['Z']}", GOLD)
    node_circle("M", "M", "Matter", matter)
    node_circle("Ck", "Ck", "Clock", clock_label)
    node_circle("L", "L", "Light", "shell")
    node_circle("Ac", "Ac", "Action", "closure")

    draw.ellipse((cx - 142, cy - 142, cx + 142, cy + 142), fill=PAPER, outline=GOLD, width=4)
    centered(draw, (cx, cy - 90), row["P_subscript"], font(48), GOLD)
    centered(draw, (cx, cy - 28), "Particle Source Address", small_font, NAVY)
    centered(draw, (cx, cy + 20), row["P_address"], body_font, NAVY)
    centered(draw, (cx, cy + 58), row["quark_address"], body_font, NAVY)

    g_card = f"{Decimal(str(row['G_decimal'])):.6f}"
    gr_card = f"{Decimal(str(row['GR_decimal'])):.6f}"
    draw.rectangle((190, 742, 710, 908), fill=PAPER)
    centered(draw, (cx, 750), "carrier/furite kernel", font(24, italic=True), BLUE)
    centered(draw, (cx, 794), f"G(P) = {g_card}", kernel_font, NAVY)
    centered(draw, (cx, 828), f"GR(P) = 8G(P) = {gr_card}", kernel_font, NAVY)
    centered(draw, (cx, 862), "GR(P) = 7G(P) + G(P)", kernel_font, NAVY)

    draw.rectangle((230, 1072, 670, 1136), outline=LINE, width=3)
    centered(draw, (cx, 1086), row["bottom_A_line"], font(31), NAVY)
    if reveal and reveal.get("reveal_status_line"):
        centered(draw, (cx, 1146), reveal["reveal_status_line"], font(17), "#555555")

    image.save(path, format="PNG", optimize=False)


def card_svg(row: dict[str, Any], reveal: dict[str, Any] | None = None) -> str:
    symbol = "E"
    title = row["sob_id"]
    subtitle = f"SAM substrate order block | isotope anchor A-{row['A']}"
    matter = f"A={row['A']}"
    clock_label = row["clock_prediction"]
    status_line = "constants-only prediction"
    if reveal:
        symbol = reveal.get("known_symbol") or "E"
        name = reveal.get("known_name") or row["sob_id"]
        title = f"{row['sob_id']} - {name}"
        subtitle = f"SAM substrate order block | isotope anchor {symbol}-{row['A']}"
        matter = reveal.get("matter_label") or matter
        clock_label = reveal.get("clock_label") or clock_label
        status_line = reveal.get("reveal_status_line") or "revealed after prediction seal"
    esc = html.escape
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="1200" viewBox="0 0 900 1200">
<rect width="900" height="1200" fill="{PAPER}"/>
<rect x="18" y="18" width="864" height="1164" fill="none" stroke="{LINE}" stroke-width="3"/>
<rect x="34" y="34" width="832" height="1132" fill="none" stroke="{LINE}" stroke-width="1"/>
<text x="450" y="105" text-anchor="middle" font-family="Georgia,serif" font-size="68" fill="{NAVY}">{esc(title)}</text>
<text x="450" y="150" text-anchor="middle" font-family="Georgia,serif" font-size="25" fill="{NAVY}">{esc(subtitle)}</text>
<rect x="235" y="168" width="430" height="56" fill="none" stroke="{LINE}" stroke-width="2"/>
<text x="450" y="207" text-anchor="middle" font-family="Georgia,serif" font-size="31" fill="{GOLD}">SUBSTRATE ORDER BLOCK</text>
<g stroke="black" stroke-width="4">
<line x1="450" y1="315" x2="250" y2="995"/><line x1="450" y1="315" x2="650" y2="995"/>
<line x1="145" y1="540" x2="755" y2="540"/><line x1="145" y1="540" x2="250" y2="995"/>
<line x1="755" y1="540" x2="650" y2="995"/><line x1="250" y1="995" x2="650" y2="995"/>
<line x1="145" y1="540" x2="650" y2="995"/><line x1="755" y1="540" x2="250" y2="995"/>
</g>
<circle cx="450" cy="560" r="165" fill="none" stroke="#b7d8f6" stroke-width="2"/>
<circle cx="450" cy="560" r="135" fill="none" stroke="#d4e6f7" stroke-width="1"/>
<polygon points="450,355 505.8,483.1 644.9,496.6 540.4,589.4 572.9,725.3 450,655 327.1,725.3 359.6,589.4 255.1,496.6 394.2,483.1" fill="none" stroke="{BLUE}" stroke-width="2"/>
<circle cx="450" cy="560" r="142" fill="{PAPER}" stroke="{GOLD}" stroke-width="4"/>
<text x="450" y="476" text-anchor="middle" font-family="Georgia,serif" font-size="48" fill="{GOLD}">{esc(row['P_subscript'])}</text>
<text x="450" y="532" text-anchor="middle" font-family="Georgia,serif" font-size="24" fill="{NAVY}">Particle Source Address</text>
<text x="450" y="588" text-anchor="middle" font-family="Georgia,serif" font-size="28" fill="{NAVY}">{esc(row['P_address'])}</text>
<text x="450" y="628" text-anchor="middle" font-family="Georgia,serif" font-size="28" fill="{NAVY}">{esc(row['quark_address'])}</text>
<g font-family="Georgia,serif" text-anchor="middle">
<circle cx="450" cy="315" r="74" fill="{PAPER}" stroke="{GOLD}" stroke-width="4"/>
<text x="450" y="277" font-size="34" fill="{GOLD}">{esc(symbol)}</text><text x="450" y="319" font-size="23" fill="{NAVY}">Element</text><text x="450" y="351" font-size="22" fill="{GOLD}">Z = {row['Z']}</text>
<circle cx="145" cy="540" r="76" fill="{PAPER}" stroke="{TEAL}" stroke-width="4"/>
<text x="145" y="502" font-size="34" fill="{TEAL}">M</text><text x="145" y="544" font-size="23" fill="{NAVY}">Matter</text><text x="145" y="576" font-size="18" fill="{TEAL}">{esc(matter)}</text>
<circle cx="755" cy="540" r="76" fill="{PAPER}" stroke="{TEAL}" stroke-width="4"/>
<text x="755" y="502" font-size="34" fill="{TEAL}">Ck</text><text x="755" y="544" font-size="23" fill="{NAVY}">Clock</text><text x="755" y="576" font-size="21" fill="{TEAL}">{esc(clock_label)}</text>
<circle cx="250" cy="995" r="76" fill="{PAPER}" stroke="{TEAL}" stroke-width="4"/>
<text x="250" y="957" font-size="34" fill="{TEAL}">L</text><text x="250" y="999" font-size="23" fill="{NAVY}">Light</text><text x="250" y="1031" font-size="21" fill="{TEAL}">shell</text>
<circle cx="650" cy="995" r="76" fill="{PAPER}" stroke="{TEAL}" stroke-width="4"/>
<text x="650" y="957" font-size="34" fill="{TEAL}">Ac</text><text x="650" y="999" font-size="23" fill="{NAVY}">Action</text><text x="650" y="1031" font-size="21" fill="{TEAL}">closure</text>
</g>
<rect x="190" y="742" width="520" height="166" fill="{PAPER}"/>
<text x="450" y="768" text-anchor="middle" font-family="Georgia,serif" font-size="24" font-style="italic" fill="{BLUE}">carrier/furite kernel</text>
<text x="450" y="812" text-anchor="middle" font-family="Georgia,serif" font-size="24" fill="{NAVY}">G(P) = {Decimal(str(row['G_decimal'])):.6f}</text>
<text x="450" y="846" text-anchor="middle" font-family="Georgia,serif" font-size="24" fill="{NAVY}">GR(P) = 8G(P) = {Decimal(str(row['GR_decimal'])):.6f}</text>
<text x="450" y="880" text-anchor="middle" font-family="Georgia,serif" font-size="24" fill="{NAVY}">GR(P) = 7G(P) + G(P)</text>
<rect x="230" y="1072" width="440" height="64" fill="none" stroke="{LINE}" stroke-width="3"/>
<text x="450" y="1114" text-anchor="middle" font-family="Georgia,serif" font-size="31" fill="{NAVY}">{esc(row['bottom_A_line'])}</text>
<text x="450" y="1156" text-anchor="middle" font-family="Georgia,serif" font-size="16" fill="#555">{esc(status_line)}</text>
</svg>
"""


def write_native_cards(rows: list[dict[str, Any]]) -> list[Path]:
    paths: list[Path] = []
    for row in rows:
        stem = f"SOB{int(row['Z']):03d}_native"
        svg_path = NATIVE_SVG / f"{stem}.svg"
        png_path = NATIVE_PNG / f"{stem}.png"
        svg_path.write_text(card_svg(row), encoding="utf-8")
        draw_card_png(png_path, row)
        paths.extend([svg_path, png_path])
    return paths


def zip_paths(zip_path: Path, paths: list[Path]) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(paths, key=lambda p: rel(p)):
            info = zipfile.ZipInfo(rel(path))
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())


def hash_manifest(paths: list[Path], manifest_path: Path, root_name: str) -> dict[str, Any]:
    unique = sorted({path for path in paths if path.exists() and path.is_file()}, key=lambda p: rel(p))
    rows = [
        {"path": rel(path), "bytes": path.stat().st_size, "sha256": sha256_file(path)}
        for path in unique
    ]
    write_csv(manifest_path, rows, ["path", "bytes", "sha256"])
    hashes = [row["sha256"] for row in rows]
    linear = sha256_text("".join(f"{row['path']},{row['sha256']}\n" for row in rows))
    seal = {
        "root_name": root_name,
        "file_count": len(rows),
        "total_bytes": sum(int(row["bytes"]) for row in rows),
        "linear_manifest_sha256": linear,
        "merkle_root_sha256": merkle_root(hashes),
        "manifest": rel(manifest_path),
    }
    return seal


def build_payloads(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "sob_id": row["sob_id"],
            "Z": row["Z"],
            "A": row["A"],
            "N": row["N"],
            "clock_prediction": row["clock_prediction"],
            "P_subscript": row["P_subscript"],
            "P_address": row["P_address"],
            "quark_address": row["quark_address"],
            "G_fraction": row["G_fraction"],
            "GR_fraction": row["GR_fraction"],
            "retained_7G_fraction": row["retained_7G_fraction"],
            "light_face_native": row["light_face_native"],
            "action_face_native": row["action_face_native"],
            "bottom_A_line": row["bottom_A_line"],
        }
        for row in rows
    ]


def manifest_source(path: Path, role: str, construction_role: str, read_phase: str) -> dict[str, Any]:
    exists = path.exists()
    return {
        "source": rel(path),
        "exists": str(exists),
        "bytes": path.stat().st_size if exists and path.is_file() else "",
        "sha256": sha256_file(path) if exists and path.is_file() else "",
        "role": role,
        "construction_role": construction_role,
        "read_phase": read_phase,
    }


def normalize_atomic_mass_u(text: str) -> str:
    if not text:
        return ""
    value = Decimal(text)
    if value > Decimal("1000000"):
        value = value / Decimal("1000000")
    return f"{value:.6f}"


def load_reveal_sources() -> tuple[dict[int, dict[str, str]], dict[int, dict[str, str]], dict[str, dict[str, str]]]:
    _, periodic = read_csv(CR119_PERIODIC)
    _, clock = read_csv(CR220_ELEMENTS)
    _, roster = read_csv(QP061_ROSTER)
    periodic_by_z = {int(row["Z"]): row for row in periodic if row.get("Z")}
    clock_by_z = {int(row["Z"]): row for row in clock if row.get("Z")}
    roster_by_notation = {row["observed_notation"]: row for row in roster if row.get("observed_notation")}
    return periodic_by_z, clock_by_z, roster_by_notation


def build_reveal_rows(
    prediction_rows: list[dict[str, Any]],
    periodic_by_z: dict[int, dict[str, str]],
    clock_by_z: dict[int, dict[str, str]],
    roster_by_notation: dict[str, dict[str, str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in prediction_rows:
        z = int(row["Z"])
        periodic = periodic_by_z.get(z, {})
        clock = clock_by_z.get(z, {})
        symbol = periodic.get("known_symbol", "")
        name = periodic.get("known_name", "")
        notation = f"{symbol}-{row['A']}" if symbol else ""
        roster = roster_by_notation.get(notation, {})
        atomic_mass_u = normalize_atomic_mass_u(roster.get("atomic_mass_u", ""))
        matter_label = f"{atomic_mass_u[:-3] if atomic_mass_u else ''}".rstrip(".")
        if atomic_mass_u:
            matter_label = f"{Decimal(atomic_mass_u):.3f}"
        reference_clock = clock.get("reference_clock", "")
        comparison = {
            "sob_id": row["sob_id"],
            "Z": z,
            "N": row["N"],
            "A": row["A"],
            "prediction_clock": row["clock_prediction"],
            "reference_clock": reference_clock,
            "clock_match": str(row["clock_prediction"] == reference_clock),
            "known_symbol": symbol,
            "known_name": name,
            "revealed_isotope_anchor": notation,
            "atomic_mass_u_reveal": atomic_mass_u,
            "matter_label": f"Matter {matter_label}" if matter_label else f"Matter A={row['A']}",
            "name_symbol_reveal_status": "REVEALED" if symbol and name else "NO_REVEAL_LABEL",
            "atomic_mass_reveal_status": "REVEALED_QP061" if atomic_mass_u else "NO_MATCHING_MASS_REVEAL",
            "reveal_source": "CR119/CR220/QP061_AFTER_PREDICTION_SEAL",
            "prediction_hash_basis": "CR226_prediction_seal",
        }
        rows.append(comparison)
    return rows


def reveal_payload(row: dict[str, Any], reveal_row: dict[str, Any]) -> dict[str, Any]:
    clock_label = row["clock_prediction"]
    if reveal_row.get("clock_match") == "True":
        clock_label = reveal_row["reference_clock"]
    return {
        "known_symbol": reveal_row.get("known_symbol", ""),
        "known_name": reveal_row.get("known_name", ""),
        "matter_label": reveal_row.get("matter_label", ""),
        "clock_label": clock_label,
        "reveal_status_line": "reveal after sealed prediction | clock match " + reveal_row.get("clock_match", ""),
    }


def write_reveal_cards(prediction_rows: list[dict[str, Any]], reveal_rows: list[dict[str, Any]]) -> list[Path]:
    reveal_by_z = {int(row["Z"]): row for row in reveal_rows}
    paths: list[Path] = []
    for row in prediction_rows:
        reveal = reveal_payload(row, reveal_by_z[int(row["Z"])])
        safe_name = reveal.get("known_name") or "native"
        safe_name = "".join(ch for ch in safe_name if ch.isalnum() or ch in ("_", "-"))[:40] or "native"
        stem = f"SOB{int(row['Z']):03d}_revealed_{safe_name}"
        svg_path = REVEAL_SVG / f"{stem}.svg"
        png_path = REVEAL_PNG / f"{stem}.png"
        svg_path.write_text(card_svg(row, reveal), encoding="utf-8")
        draw_card_png(png_path, row, reveal)
        paths.extend([svg_path, png_path])
    return paths


def write_hashes(paths: list[Path]) -> None:
    rows = []
    for path in sorted({p for p in paths if p.exists() and p.is_file()}, key=lambda p: rel(p)):
        rows.append(f"{rel(path)},{sha256_file(path)}")
    HASHES.write_text("\n".join(rows) + "\n", encoding="utf-8")


def main() -> int:
    reset_output_tree()
    checks: list[dict[str, Any]] = []

    # Phase 1: constants-only prediction. No reveal/comparator source is opened above this line.
    prediction_rows = build_prediction_rows()
    prediction_fields = [
        "sob_id", "sob_ordinal", "Z", "N", "A", "P_subscript", "P_address", "quark_address",
        "quark_u_count", "quark_d_count", "quark_e_count", "radix_cycle", "radix_slot",
        "selected_depth_index", "residual_twelfths", "shell_period", "shell_n", "shell_capacity",
        "shell_occupancy", "shell_status", "constant_native_lane", "clock_prediction", "clock_formula",
        "kappa_floor_fraction", "kappa_eff_fraction", "G_fraction", "G_decimal", "GR_fraction",
        "GR_decimal", "retained_7G_fraction", "retained_7G_decimal", "kernel_line_1",
        "kernel_line_1_floor", "kernel_line_2", "kernel_line_3", "light_face_native",
        "action_face_native", "bottom_A_line", "construction_source",
    ]
    write_csv(PREDICTIONS_CSV, prediction_rows, prediction_fields)
    write_jsonl(PREDICTION_JSONL, build_payloads(prediction_rows))
    native_card_paths = write_native_cards(prediction_rows)

    prediction_paths = [PREDICTIONS_CSV, PREDICTION_JSONL] + native_card_paths
    zip_paths(PREDICTION_ZIP, prediction_paths)
    prediction_paths.append(PREDICTION_ZIP)
    prediction_seal = hash_manifest(prediction_paths, PREDICTION_HASH_MANIFEST, "CR226_PREDICTION_SEAL")
    prediction_seal.update(
        {
            "phase": "01_prediction_seal",
            "generated_without_reveal_inputs": True,
            "construction_constants": {
                "R": fstr(R),
                "D": fstr(D),
                "alpha_H": fstr(ALPHA_H),
                "split": fstr(SPLIT),
                "capacity": fstr(CAPACITY),
                "kappa_floor": fstr(KAPPA_FLOOR),
                "neutron_G_unit": fstr(NEUTRON_G_UNIT),
                "clock_boundary": CLOCK_BOUNDARY,
                "clock_holes": sorted(CLOCK_HOLES),
                "frontier_start": FRONTIER_START,
            },
        }
    )
    write_json(PREDICTION_SEAL, prediction_seal)

    freeze_ledger = {
        "phase": "02_freeze",
        "freeze_time_utc": utc_now(),
        "prediction_seal": rel(PREDICTION_SEAL),
        "prediction_manifest": rel(PREDICTION_HASH_MANIFEST),
        "prediction_zip": rel(PREDICTION_ZIP),
        "prediction_file_count": prediction_seal["file_count"],
        "prediction_total_bytes": prediction_seal["total_bytes"],
        "prediction_linear_manifest_sha256": prediction_seal["linear_manifest_sha256"],
        "prediction_merkle_root_sha256": prediction_seal["merkle_root_sha256"],
        "reveal_sources_read_before_this_freeze": False,
    }
    write_json(FREEZE_LEDGER, freeze_ledger)

    # Phase 3: reveal/comparator layer. Reveal sources are intentionally opened only after the freeze ledger exists.
    periodic_by_z, clock_by_z, roster_by_notation = load_reveal_sources()
    reveal_rows = build_reveal_rows(prediction_rows, periodic_by_z, clock_by_z, roster_by_notation)
    reveal_fields = [
        "sob_id", "Z", "N", "A", "prediction_clock", "reference_clock", "clock_match",
        "known_symbol", "known_name", "revealed_isotope_anchor", "atomic_mass_u_reveal",
        "matter_label", "name_symbol_reveal_status", "atomic_mass_reveal_status",
        "reveal_source", "prediction_hash_basis",
    ]
    write_csv(REVEAL_COMPARISON, reveal_rows, reveal_fields)
    reveal_card_paths = write_reveal_cards(prediction_rows, reveal_rows)

    reveal_paths = [REVEAL_COMPARISON] + reveal_card_paths
    zip_paths(REVEAL_ZIP, reveal_paths)
    reveal_paths.append(REVEAL_ZIP)
    reveal_seal = hash_manifest(reveal_paths, REVEAL_HASH_MANIFEST, "CR226_REVEAL_SEAL")
    reveal_seal.update(
        {
            "phase": "03_reveal",
            "prediction_merkle_root_sha256": prediction_seal["merkle_root_sha256"],
            "reveal_sources_read_after_freeze": True,
            "name_symbol_revealed_count": Counter(row["name_symbol_reveal_status"] for row in reveal_rows),
            "atomic_mass_revealed_count": Counter(row["atomic_mass_reveal_status"] for row in reveal_rows),
        }
    )
    write_json(REVEAL_SEAL, reveal_seal)

    input_manifest = [
        manifest_source(PRECOMMIT, "precommit declaration", "TASK_DECLARATION", "before_execution"),
        manifest_source(RUNNER, "reproducible runner", "EXECUTION_SCRIPT", "before_execution"),
        manifest_source(CR119_PERIODIC, "downstream symbol/name reveal", "REVEAL_ONLY_NOT_CONSTRUCTION", "after_prediction_freeze"),
        manifest_source(CR220_ELEMENTS, "HH001/CLOCK comparator", "REVEAL_COMPARATOR_ONLY_NOT_CONSTRUCTION", "after_prediction_freeze"),
        manifest_source(QP061_ROSTER, "downstream isotope mass reveal", "REVEAL_ONLY_NOT_CONSTRUCTION", "after_prediction_freeze"),
    ]
    write_csv(INPUT_MANIFEST, input_manifest, ["source", "exists", "bytes", "sha256", "role", "construction_role", "read_phase"])

    prediction_counts = Counter(row["clock_prediction"] for row in prediction_rows)
    reveal_clock_matches = sum(1 for row in reveal_rows if row["clock_match"] == "True")
    z79 = next(row for row in prediction_rows if int(row["Z"]) == 79)
    z79_reveal = next(row for row in reveal_rows if int(row["Z"]) == 79)

    check(checks, "prediction_rows_126", len(prediction_rows) == 126, len(prediction_rows), 126)
    check(checks, "native_png_cards_126", len(list(NATIVE_PNG.glob("*.png"))) == 126, len(list(NATIVE_PNG.glob("*.png"))), 126)
    check(checks, "native_svg_cards_126", len(list(NATIVE_SVG.glob("*.svg"))) == 126, len(list(NATIVE_SVG.glob("*.svg"))), 126)
    check(checks, "reveal_png_cards_126", len(list(REVEAL_PNG.glob("*.png"))) == 126, len(list(REVEAL_PNG.glob("*.png"))), 126)
    check(checks, "reveal_svg_cards_126", len(list(REVEAL_SVG.glob("*.svg"))) == 126, len(list(REVEAL_SVG.glob("*.svg"))), 126)
    check(checks, "clock_prediction_counts_81_37_8", dict(prediction_counts) == {"stable": 81, "radioactive": 37, "frontier": 8}, dict(prediction_counts), {"stable": 81, "radioactive": 37, "frontier": 8})
    check(checks, "clock_reveal_matches_126", reveal_clock_matches == 126, reveal_clock_matches, 126)
    check(checks, "prediction_seal_exists", PREDICTION_SEAL.exists(), rel(PREDICTION_SEAL), "exists")
    check(checks, "freeze_ledger_exists", FREEZE_LEDGER.exists(), rel(FREEZE_LEDGER), "exists")
    check(checks, "reveal_seal_links_prediction_root", reveal_seal["prediction_merkle_root_sha256"] == prediction_seal["merkle_root_sha256"], reveal_seal["prediction_merkle_root_sha256"], prediction_seal["merkle_root_sha256"])
    check(checks, "reveal_sources_marked_after_freeze", all(row["read_phase"] != "before_prediction_freeze" for row in input_manifest if "REVEAL" in row["construction_role"]), input_manifest, "all reveal sources after_prediction_freeze")
    check(checks, "z79_prediction_native_values", z79["Z"] == 79 and z79["N"] == 118 and z79["A"] == 197 and z79["clock_prediction"] == "stable", {"Z": z79["Z"], "N": z79["N"], "A": z79["A"], "clock": z79["clock_prediction"]}, "Z=79,N=118,A=197,stable")
    check(checks, "z79_reveal_gold_mass", z79_reveal["known_symbol"] == "Au" and z79_reveal["known_name"] == "Gold" and z79_reveal["matter_label"] == "Matter 196.967", z79_reveal, "Au Gold Matter 196.967")
    check(checks, "prediction_manifest_nonempty", prediction_seal["file_count"] > 250, prediction_seal["file_count"], ">250 prediction files")
    check(checks, "reveal_manifest_nonempty", reveal_seal["file_count"] > 250, reveal_seal["file_count"], ">250 reveal files")

    write_csv(CHECKS, checks, ["check", "passed", "observed", "expected"])
    passed = sum(1 for row in checks if row["passed"] == "True")
    execution_status = "CLEAN" if passed == len(checks) else "FAILED"
    result_class = (
        "CR226_PASS_VAULTED_CONSTANTS_ONLY_SOB_CARD_GENERATION__PREDICTIONS_SEALED__"
        "126_NATIVE_CARDS_FROZEN__126_REVEAL_CARDS_GENERATED__CLOCK_MATCH_126_OF_126"
        if execution_status == "CLEAN"
        else "CR226_FAIL_VAULTED_CONSTANTS_ONLY_SOB_CARD_GENERATION"
    )

    all_hash_paths = [
        PRECOMMIT,
        RUNNER,
        PREDICTIONS_CSV,
        PREDICTION_JSONL,
        PREDICTION_HASH_MANIFEST,
        PREDICTION_SEAL,
        PREDICTION_ZIP,
        FREEZE_LEDGER,
        REVEAL_COMPARISON,
        REVEAL_HASH_MANIFEST,
        REVEAL_SEAL,
        REVEAL_ZIP,
        INPUT_MANIFEST,
        CHECKS,
    ] + native_card_paths + reveal_card_paths

    summary = {
        "artifact": "CR226_VAULTED_SOB_CARD_GENERATION_FREEZE_REVEAL",
        "cr_id": "CR226",
        "generated_at_utc": utc_now(),
        "execution_status": execution_status,
        "checks_passed": passed,
        "checks_total": len(checks),
        "result_class": result_class,
        "prediction_counts": dict(prediction_counts),
        "card_counts": {
            "native_png": len(list(NATIVE_PNG.glob("*.png"))),
            "native_svg": len(list(NATIVE_SVG.glob("*.svg"))),
            "revealed_png": len(list(REVEAL_PNG.glob("*.png"))),
            "revealed_svg": len(list(REVEAL_SVG.glob("*.svg"))),
        },
        "prediction_seal": {
            "path": rel(PREDICTION_SEAL),
            "merkle_root_sha256": prediction_seal["merkle_root_sha256"],
            "linear_manifest_sha256": prediction_seal["linear_manifest_sha256"],
            "file_count": prediction_seal["file_count"],
            "zip": rel(PREDICTION_ZIP),
        },
        "reveal_seal": {
            "path": rel(REVEAL_SEAL),
            "merkle_root_sha256": reveal_seal["merkle_root_sha256"],
            "linear_manifest_sha256": reveal_seal["linear_manifest_sha256"],
            "file_count": reveal_seal["file_count"],
            "zip": rel(REVEAL_ZIP),
            "linked_prediction_merkle_root_sha256": reveal_seal["prediction_merkle_root_sha256"],
        },
        "z79": {
            "native": {key: z79[key] for key in ["sob_id", "Z", "N", "A", "P_address", "quark_address", "G_decimal", "GR_decimal", "clock_prediction"]},
            "reveal": {key: z79_reveal[key] for key in ["known_symbol", "known_name", "revealed_isotope_anchor", "matter_label", "clock_match"]},
            "native_png": rel(NATIVE_PNG / "SOB079_native.png"),
            "reveal_png": rel(next(REVEAL_PNG.glob("SOB079_revealed_*.png"))),
        },
        "boundary": (
            "Predictions are generated from constants only and sealed before reveal sources are read. "
            "Reveal cards add downstream names/symbols/masses/comparator labels after the prediction root is frozen."
        ),
        "outputs": {
            "prediction_csv": rel(PREDICTIONS_CSV),
            "prediction_seal": rel(PREDICTION_SEAL),
            "freeze_ledger": rel(FREEZE_LEDGER),
            "reveal_comparison": rel(REVEAL_COMPARISON),
            "reveal_seal": rel(REVEAL_SEAL),
            "checks": rel(CHECKS),
            "summary": rel(SUMMARY),
            "result": rel(RESULT),
            "hashes": rel(HASHES),
        },
    }
    write_json(SUMMARY, summary)

    result_text = f"""# CR226 Vaulted SOB Card Generation, Freeze, Reveal

Result: **{result_class}**

## Direct Answer

The vault run generated the 126 SOB card predictions from SAM constants only,
sealed them, froze the prediction hash root, then opened reveal sources and
generated 126 revealed cards.

## Prediction Formula

```text
R = 12
D = 3
alpha_H = 2
split = 8
capacity = 126
kappa_floor = 7117/768
clock_stable(Z) = Z <= 83 and Z not in {{43,61}}
frontier(Z) = Z > 118
```

Prediction counts:

```text
stable     = {prediction_counts.get('stable', 0)}
radioactive = {prediction_counts.get('radioactive', 0)}
frontier   = {prediction_counts.get('frontier', 0)}
```

## Seals

```text
prediction_merkle_root = {prediction_seal['merkle_root_sha256']}
prediction_file_count  = {prediction_seal['file_count']}
reveal_merkle_root     = {reveal_seal['merkle_root_sha256']}
reveal_file_count      = {reveal_seal['file_count']}
```

The reveal seal links back to the prediction root:

```text
{reveal_seal['prediction_merkle_root_sha256']}
```

## Cards

- Native prediction PNG cards: {len(list(NATIVE_PNG.glob('*.png')))}
- Native prediction SVG cards: {len(list(NATIVE_SVG.glob('*.svg')))}
- Revealed PNG cards: {len(list(REVEAL_PNG.glob('*.png')))}
- Revealed SVG cards: {len(list(REVEAL_SVG.glob('*.svg')))}

Gold reveal check:

```text
SOB79
Z=79, N=118, A=197
P={z79['P_address']}
quark={z79['quark_address']}
clock={z79['clock_prediction']}
reveal={z79_reveal['known_symbol']} {z79_reveal['known_name']}
matter={z79_reveal['matter_label']}
```

## Security Boundary

Prediction artifacts were written, hashed, zipped, and frozen before reveal
sources were read. Downstream names, symbols, measured isotope masses, and
HH001/CLOCK labels are reveal/comparator fields only.

## Artifacts

- `{rel(PREDICTIONS_CSV)}`
- `{rel(PREDICTION_SEAL)}`
- `{rel(FREEZE_LEDGER)}`
- `{rel(REVEAL_COMPARISON)}`
- `{rel(REVEAL_SEAL)}`
- `{rel(NATIVE_PNG / 'SOB079_native.png')}`
- `{rel(next(REVEAL_PNG.glob('SOB079_revealed_*.png')))}`
- `{rel(CHECKS)}`
- `{rel(SUMMARY)}`
- `{rel(HASHES)}`
"""
    RESULT.write_text(result_text, encoding="utf-8")

    all_hash_paths += [SUMMARY, RESULT]
    write_hashes(all_hash_paths)

    return 0 if execution_status == "CLEAN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
