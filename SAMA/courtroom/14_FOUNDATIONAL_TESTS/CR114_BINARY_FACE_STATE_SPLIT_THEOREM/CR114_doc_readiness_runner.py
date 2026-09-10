"""CR114 doc-readiness artifact builder.

This is not a new physics verdict. It packages the CR114 closure for the next
documentation pass:

* deterministic figure source/render, avoiding image-model text drift
* stale-language scan for the Higgs/split/carrier language surface
* lineage zipper showing CR114 -> QP091T/U -> QP092A/F/G source order
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import textwrap
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle


CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent
VS_ROOT = Path(r"C:/VS")
QUANTUM_ROOT = VS_ROOT / "quantum_phase"
SAMS_TOE = VS_ROOT / "SAMs_TOE"

CR114_SUMMARY = CR_DIR / "CR114_summary.json"
CR114_LOCK = CR_DIR / "CR114_binary_face_state_split_lock.json"
CR113_LOCK = BRANCH_DIR / "CR113_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM" / "CR113_completed_write_address_count_lock.json"

FIG_PNG = CR_DIR / "CR114_higgs_tensor_carrier_deterministic_figure.png"
FIG_SVG = CR_DIR / "CR114_higgs_tensor_carrier_deterministic_figure.svg"
STALE_SCAN_CSV = CR_DIR / "CR114_stale_language_scan.csv"
STALE_SCAN_MD = CR_DIR / "CR114_stale_language_scan.md"
LINEAGE_CSV = CR_DIR / "CR114_lineage_zipper.csv"
LINEAGE_MD = CR_DIR / "CR114_lineage_zipper.md"
LINEAGE_JSON = CR_DIR / "CR114_lineage_zipper.json"
SUMMARY_JSON = CR_DIR / "CR114_doc_readiness_summary.json"
LOCAL_HASHES = CR_DIR / "CR114_hashes.txt"
BRANCH_HASHES = BRANCH_DIR / "HASHES.txt"


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    if not path.exists():
        return ""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(COURTROOM_DIR))
    except ValueError:
        return str(path)


def branch_rel(path: Path) -> str:
    try:
        return str(path.relative_to(BRANCH_DIR))
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def wrap_text(text: str, width: int) -> str:
    out: list[str] = []
    for part in text.split("\n"):
        if not part:
            out.append("")
        else:
            out.extend(textwrap.wrap(part, width=width, break_long_words=False, replace_whitespace=False))
    return "\n".join(out)


def panel(ax, x: float, y: float, w: float, h: float, title: str, accent: str = "#0f766e") -> None:
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        linewidth=1.25,
        edgecolor="#a8b6bf",
        facecolor="#fbfdff",
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h - 0.038, title, ha="center", va="center", fontsize=13, weight="bold", color="#151515")
    ax.add_line(
        plt.Line2D(
            [x + 0.018, x + w - 0.018],
            [y + h - 0.066, y + h - 0.066],
            color=accent,
            linewidth=1.1,
            alpha=0.65,
            zorder=0.2,
        )
    )


def mini_box(ax, x: float, y: float, w: float, h: float, text: str, fc: str = "#eef7fb", ec: str = "#91a8b6", fs: float = 9.5, weight: str = "normal") -> None:
    rect = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.007,rounding_size=0.01",
        linewidth=1.0,
        edgecolor=ec,
        facecolor=fc,
    )
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color="#16313b", weight=weight)


def arrow(ax, x1: float, y1: float, x2: float, y2: float, color: str = "#0f766e") -> None:
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", lw=1.6, color=color, shrinkA=2, shrinkB=2),
    )


def render_figure() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "svg.fonttype": "none",
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        }
    )
    fig = plt.figure(figsize=(18, 14), dpi=180)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(
        0.5,
        0.972,
        "7.1 The Split Is the Write -- and the Higgs Exposes Tensor-Carrier Support, Not a Matter Row",
        ha="center",
        va="center",
        fontsize=22,
        weight="bold",
        color="#111111",
    )

    left_x, right_x = 0.035, 0.515
    w = 0.45
    h = 0.26
    y_rows = [0.67, 0.365, 0.06]

    # Panel 1
    x, y = left_x, y_rows[0]
    panel(ax, x, y, w, h, "STEP 1 - BINARY FACE-STATE SPLIT", "#0b6b8a")
    mini_box(ax, x + 0.055, y + 0.162, 0.34, 0.052, "H_native = R^2(1 - 2^-D)\nR=12, D=3", "#eef8ff", "#5f9fbd", 11, "bold")
    mini_box(ax, x + 0.025, y + 0.088, 0.13, 0.052, "2^D = 8\nface-states", "#ffffff", "#8aa1ad", 9.2)
    mini_box(ax, x + 0.172, y + 0.088, 0.13, 0.052, "1 unresolved\nstate = 1/8", "#fff8e6", "#d59d29", 9.2, "bold")
    mini_box(ax, x + 0.319, y + 0.088, 0.105, 0.052, "7 retained\nstates = 7/8", "#eefaf3", "#4e9d70", 9.2, "bold")
    arrow(ax, x + 0.155, y + 0.114, x + 0.172, y + 0.114, "#0b6b8a")
    arrow(ax, x + 0.302, y + 0.114, x + 0.319, y + 0.114, "#0b6b8a")
    mini_box(ax, x + 0.035, y + 0.025, 0.38, 0.043, "R^2 = 144  ->  loss = 18  ->  parent = 126", "#f5fbff", "#8aa1ad", 10.4, "bold")
    mini_box(ax, x + 0.047, y + 0.001, 0.356, 0.026, "LOCK: R^2/2^D = alpha_H.D^2 = 18", "#e8f2f8", "#5f9fbd", 9.7, "bold")

    # Panel 2
    x, y = right_x, y_rows[0]
    panel(ax, x, y, w, h, "STEP 2 - OBSERVED HIGGS SURFACE", "#0f766e")
    mini_box(ax, x + 0.07, y + 0.162, 0.31, 0.052, "H_observed = H_native - D^2/R\n126 - 9/12 = 125.25", "#effbf7", "#6ba68c", 11, "bold")
    mini_box(ax, x + 0.04, y + 0.084, 0.14, 0.06, "native parent\n126", "#ffffff", "#8aa1ad", 10, "bold")
    arrow(ax, x + 0.185, y + 0.113, x + 0.213, y + 0.113, "#0f766e")
    mini_box(ax, x + 0.215, y + 0.084, 0.14, 0.06, "surface debit\nD^2/R = 0.75", "#ffffff", "#8aa1ad", 10)
    arrow(ax, x + 0.36, y + 0.113, x + 0.382, y + 0.113, "#0f766e")
    mini_box(ax, x + 0.382, y + 0.084, 0.048, 0.06, "125.25", "#eaf8f1", "#4e9d70", 10.4, "bold")
    mini_box(ax, x + 0.04, y + 0.02, 0.38, 0.038, "wrong controls: not D/R, not D^2/R^2, not no debit", "#fff4f4", "#c87575", 9.4)

    # Panel 3
    x, y = left_x, y_rows[1]
    panel(ax, x, y, w, h, "STEP 3 - H -> ZZ* -> 4ell TOPOLOGY", "#0b6b8a")
    mini_box(ax, x + 0.075, y + 0.17, 0.30, 0.047, "H -> Z_on + Z*_off -> 4ell", "#eef8ff", "#5f9fbd", 12.5, "bold")
    route_y = y + 0.108
    labels = ["ee", "eμ", "μe", "μμ"]
    for i, label in enumerate(labels):
        mini_box(ax, x + 0.047 + i * 0.095, route_y, 0.07, 0.037, label, "#ffffff", "#8aa1ad", 10.5, "bold")
    mini_box(ax, x + 0.035, y + 0.054, 0.38, 0.036, "4e : 2e2μ : 4μ = 1 : 2 : 1", "#fff9e8", "#d59d29", 12, "bold")
    ax.text(x + 0.225, y + 0.023, "category surface, not a fitted branching knob", ha="center", va="center", fontsize=9.4, color="#38515a", style="italic")

    # Panel 4
    x, y = right_x, y_rows[1]
    panel(ax, x, y, w, h, "STEP 4 - TENSOR-CARRIER PACKET", "#0f766e")
    mini_box(ax, x + 0.055, y + 0.165, 0.34, 0.044, "1/8 carrier = 1/16 plus + 1/16 cross", "#effbf7", "#6ba68c", 11.5, "bold")
    mini_box(ax, x + 0.055, y + 0.12, 0.34, 0.034, "A=1 closure: 7/8 + 1/16 + 1/16 = 1", "#f5fbff", "#8aa1ad", 10.7, "bold")
    mini_box(ax, x + 0.09, y + 0.056, 0.12, 0.048, "+ mode\ntrace-zero", "#ffffff", "#8aa1ad", 10)
    mini_box(ax, x + 0.24, y + 0.056, 0.12, 0.048, "x mode\ntrace-zero", "#ffffff", "#8aa1ad", 10)
    ax.text(x + 0.225, y + 0.024, "carrier support, not rest mass", ha="center", va="center", fontsize=10, color="#38515a", weight="bold")

    # Panel 5
    x, y = left_x, y_rows[2]
    panel(ax, x, y, w, h, "STEP 5 - PARTICLE SURFACE GRAMMAR", "#0b6b8a")
    mini_box(ax, x + 0.075, y + 0.177, 0.30, 0.038, "M_observed = M_native - S_debit", "#eef8ff", "#5f9fbd", 11.5, "bold")
    table_x, table_y = x + 0.036, y + 0.07
    cols = ["native route", "sign", "magnitude", "surface", "qA"]
    col_w = [0.11, 0.055, 0.09, 0.085, 0.05]
    cx = table_x
    for c, cw in zip(cols, col_w):
        mini_box(ax, cx, table_y + 0.057, cw, 0.033, c, "#e8f2f8", "#8aa1ad", 8.2, "bold")
        cx += cw + 0.004
    vals = ["M_native", "+ / - / 0", "|S|", "M_obs", "source"]
    cx = table_x
    for v, cw in zip(vals, col_w):
        mini_box(ax, cx, table_y + 0.017, cw, 0.033, v, "#ffffff", "#c5d0d6", 8.2)
        cx += cw + 0.004
    ax.text(x + 0.225, y + 0.025, "general S_debit magnitude law remains open; Higgs parent/surface is closed", ha="center", va="center", fontsize=8.9, color="#38515a", style="italic")

    # Panel 6
    x, y = right_x, y_rows[2]
    panel(ax, x, y, w, h, "STEP 6 - INTERSECTIONS CREATE MATTER", "#0f766e")
    steps = ["open route\nsupport", "intersection", "closed\nroute", "matter\ncandidate", "observed\nsurface"]
    sx = x + 0.035
    for i, step in enumerate(steps):
        mini_box(ax, sx + i * 0.078, y + 0.152, 0.064, 0.046, step, "#ffffff", "#8aa1ad", 7.9, "bold" if i in (0, 3) else "normal")
        if i < len(steps) - 1:
            arrow(ax, sx + i * 0.078 + 0.064, y + 0.175, sx + (i + 1) * 0.078, y + 0.175, "#0f766e")
    chip_rows = [
        (y + 0.092, [("rejected fake", 0.085), ("carrier/source support", 0.14), ("stable matter candidate", 0.135)]),
        (y + 0.052, [("composite closure", 0.13), ("hidden source-only route", 0.155)]),
    ]
    for chip_y, chips in chip_rows:
        total_w = sum(cw for _, cw in chips) + 0.008 * (len(chips) - 1)
        cx = x + (w - total_w) / 2
        for chip, cw in chips:
            mini_box(ax, cx, chip_y, cw, 0.032, chip, "#f8fbfc", "#9fb0ba", 7.2)
            cx += cw + 0.008
    mini_box(ax, x + 0.06, y + 0.014, 0.33, 0.031, "18 is tensor-carrier support, not a matter row", "#fff8e6", "#d59d29", 10.6, "bold")

    footer = "CR114 PASS: 15/15 checks, 10/10 wrong controls rejected - one unresolved face-state gives the 1/8 split."
    footer_box = FancyBboxPatch((0.12, 0.012), 0.76, 0.032, boxstyle="round,pad=0.006,rounding_size=0.009", edgecolor="#91a8b6", facecolor="#edf7fb", linewidth=1.0)
    ax.add_patch(footer_box)
    ax.text(0.5, 0.028, footer, ha="center", va="center", fontsize=12.2, color="#16313b", weight="bold")

    fig.savefig(FIG_PNG, dpi=180, bbox_inches="tight", facecolor="white")
    fig.savefig(FIG_SVG, bbox_inches="tight", facecolor="white")
    plt.close(fig)


@dataclass(frozen=True)
class PatternSpec:
    pattern_id: str
    regex: re.Pattern[str]
    default_action: str


PATTERNS = [
    PatternSpec("two_pi_route", re.compile(r"2\s*\*\s*pi|2π|2\\pi|two[- ]pi", re.IGNORECASE), "REVIEW_DEMOTE_TO_HISTORICAL_CONTEXT"),
    PatternSpec("q_split_route", re.compile(r"\bq[_-]?split\b", re.IGNORECASE), "REVIEW_DEMOTE_TO_CONTEXT_UNLESS_QP091S_HISTORY"),
    PatternSpec("bounce_language", re.compile(r"\bbounce\b|r_bounce", re.IGNORECASE), "REVIEW_BOUNCE_TERM_SCOPE"),
    PatternSpec("one_eighth", re.compile(r"\b1/8\b|one[- ]eighth", re.IGNORECASE), "CITE_CR114_BINARY_FACE_STATE_SPLIT"),
    PatternSpec("seven_eighths", re.compile(r"\b7/8\b|seven[- ]eighths", re.IGNORECASE), "CITE_CR114_OR_QP092G_CONTEXT"),
    PatternSpec("higgs_gives_mass", re.compile(r"Higgs\s+gives\s+mass", re.IGNORECASE), "REPLACE_WITH_TENSOR_CARRIER_SUPPORT_LANGUAGE"),
    PatternSpec("higgs_gives_gravity", re.compile(r"Higgs\s+gives\s+gravity", re.IGNORECASE), "TEMPER_TITLE_OR_EXPLAIN_AS_SUPPORT_EXPOSURE"),
    PatternSpec("surface_debit", re.compile(r"D\^2\s*/\s*R|D2\s*/\s*R|D\^2/R", re.IGNORECASE), "KEEP_SEPARATE_FROM_1_8_CARRIER"),
    PatternSpec("higgs_surface_12525", re.compile(r"\b125\.25\b|\b125\.250", re.IGNORECASE), "CHECK_QP091T_QP091U_SURFACE_CITATION"),
    PatternSpec("split_loss_18", re.compile(r"alpha_H\s*\*?\s*D\^2|alpha_H\s*D\^2|α_H\s*[·*]?\s*D\^2|\b18\b", re.IGNORECASE), "CHECK_NOT_MATTER_ROW_WHEN_USED_AS_CARRIER"),
]


def target_files() -> list[Path]:
    targets: list[Path] = []
    explicit = [
        COURTROOM_DIR / "SAMs_TOE" / "SAMs_TOE_v0.2_with_glossary.md",
        COURTROOM_DIR / "docs" / "MANUSCRIPT_DRAFT.md",
        COURTROOM_DIR / "docs" / "SAMs_BIG_TOE_MANUSCRIPT_CORRECTIONS.md",
        SAMS_TOE / "manuscript" / "SAM_PREPRINT.md",
        SAMS_TOE / "manuscript" / "SOURCE_APPENDIX.md",
        SAMS_TOE / "manuscript" / "CLAIM_EVIDENCE_TABLE.md",
        SAMS_TOE / "manuscript" / "GLOSSARY.md",
    ]
    targets.extend([p for p in explicit if p.exists()])

    roots = [
        QUANTUM_ROOT / "docs" / "reports",
        QUANTUM_ROOT / "artifacts" / "qp091s",
        QUANTUM_ROOT / "artifacts" / "qp091t",
        QUANTUM_ROOT / "artifacts" / "qp091u",
        QUANTUM_ROOT / "artifacts" / "qp091x",
        QUANTUM_ROOT / "artifacts" / "qp092a_split_loss_tensor_carrier",
        QUANTUM_ROOT / "artifacts" / "qp092f_tensor_carrier_wave_mode",
        QUANTUM_ROOT / "artifacts" / "qp092g_tensor_carrier_bridge_packet",
        COURTROOM_DIR / "09a_PARTICLE_MASS_CHAIN",
        COURTROOM_DIR / "14_FOUNDATIONAL_TESTS",
    ]
    exts = {".md", ".txt", ".json", ".csv", ".py"}
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in exts:
                targets.append(path)

    for path in (QUANTUM_ROOT / "src").glob("qp091*.py"):
        targets.append(path)
    for path in (QUANTUM_ROOT / "src").glob("qp092*.py"):
        targets.append(path)

    # Stable order, no duplicates.
    excluded_exact = {
        str(STALE_SCAN_CSV).lower(),
        str(STALE_SCAN_MD).lower(),
        str(SUMMARY_JSON).lower(),
        str(LOCAL_HASHES).lower(),
        str(BRANCH_HASHES).lower(),
        str(Path(__file__).resolve()).lower(),
    }
    seen: set[str] = set()
    unique: list[Path] = []
    for path in sorted(targets, key=lambda p: str(p).lower()):
        key = str(path).lower()
        name = path.name.lower()
        if key in excluded_exact:
            continue
        if name.endswith(".sha256.txt") or name in {"hashes.txt", "cr114_hashes.txt"}:
            continue
        if name.startswith("cr114_stale_language_scan"):
            continue
        if key not in seen:
            seen.add(key)
            unique.append(path)
    return unique


def classify_match(path: Path, line: str, pattern_id: str, default_action: str) -> tuple[str, str]:
    lower = line.lower()
    path_s = str(path).replace("\\", "/").lower()
    source_artifact = "/artifacts/" in path_s or "/src/" in path_s or "/14_foundational_tests/" in path_s
    manuscript = "/docs/" in path_s or "/manuscript/" in path_s

    if pattern_id in {"two_pi_route", "q_split_route"}:
        if any(word in lower for word in ["context", "demoted", "near-lock", "historical", "supersedes"]):
            return "OK_CONTEXT", "No edit unless simplifying historical note."
        if manuscript:
            return "NEEDS_REVIEW", "Demote 2pi/q_split to historical near-lock context; exact parent now cites CR114 -> QP091T."
    if pattern_id == "bounce_language":
        if "r_bounce" in lower and any(word in lower for word in ["proton", "neutron", "baryon", "q_slot", "q-slot"]):
            return "OK_BARYON_SCOPE", "Baryon r_bounce usage can remain if G437/QP084 provenance is cited."
        if "higgs" in lower or "split" in lower or "carrier" in lower:
            return "NEEDS_REVIEW", "Avoid bounce wording for Higgs split; use binary face-state/tensor-carrier language."
    if pattern_id in {"one_eighth", "seven_eighths"}:
        if any(word in lower for word in ["cr114", "binary", "face-state", "tensor", "carrier", "qp092"]):
            return "OK_CONTEXT", "Already close to current language."
        return "NEEDS_REVIEW", "Add CR114 provenance for 1/8 or 7/8 language."
    if pattern_id == "higgs_gives_mass":
        return "NEEDS_REPLACE", "Replace with: Higgs exposes tensor-carrier support / surface grammar; not matter row."
    if pattern_id == "higgs_gives_gravity":
        return "NEEDS_REVIEW", "Temper to tensor-carrier support or source-field support unless title is intentionally informal."
    if pattern_id == "surface_debit":
        if "carrier" in lower and "separate" not in lower and "not" not in lower:
            return "NEEDS_REVIEW", "Make clear D^2/R is surface debit, not the 1/8 carrier."
        return "OK_CONTEXT", "Surface debit language present; verify QP091T/QP091U citation during docs edit."
    if pattern_id == "higgs_surface_12525":
        return ("OK_SOURCE_ARTIFACT" if source_artifact else "CHECK_CITATION", "Cite QP091T/QP091U for 125.25 surface.")
    if pattern_id == "split_loss_18":
        if "matter" in lower and "not" not in lower and "rejected" not in lower:
            return "NEEDS_REVIEW", "Avoid implying 18 is matter; cite QP092A/F/G as non-matter carrier support."
        return ("OK_SOURCE_ARTIFACT" if source_artifact else "CHECK_CITATION", "When using 18 as carrier, cite CR114 then QP092A.")
    return "CHECK", default_action


def run_stale_scan() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in target_files():
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for spec in PATTERNS:
                if not spec.regex.search(line):
                    continue
                status, action = classify_match(path, line, spec.pattern_id, spec.default_action)
                rows.append(
                    {
                        "status": status,
                        "pattern_id": spec.pattern_id,
                        "action": action,
                        "path": str(path),
                        "line": lineno,
                        "context": line.strip()[:300],
                    }
                )
    write_csv(STALE_SCAN_CSV, rows, ["status", "pattern_id", "action", "path", "line", "context"])

    counts: dict[str, int] = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    needs = [row for row in rows if row["status"].startswith("NEEDS") or row["status"] == "CHECK_CITATION"]
    md = ["# CR114 Stale-Language Scan\n\n"]
    md.append("Scope: manuscript/doc surfaces plus QP091/QP092/CR114 provenance files. This is a review ledger, not an automatic edit.\n\n")
    md.append("## Counts\n\n")
    for key in sorted(counts):
        md.append(f"- {key}: {counts[key]}\n")
    md.append("\n## Review Items\n\n")
    if not needs:
        md.append("No review items found.\n")
    else:
        for row in needs[:200]:
            md.append(f"- **{row['status']}** `{row['pattern_id']}` {row['path']}:{row['line']}\n")
            md.append(f"  - Action: {row['action']}\n")
            md.append(f"  - Context: `{row['context']}`\n")
    if len(needs) > 200:
        md.append(f"\nTruncated review list in markdown at 200 of {len(needs)} rows; CSV contains all rows.\n")
    STALE_SCAN_MD.write_text("".join(md), encoding="utf-8")
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "order": 1,
            "artifact_id": "CR113",
            "role": "supplies R=12 from completed-WRITE address count",
            "status": "PASS",
            "source_path": str(CR113_LOCK),
            "doc_rule": "Use for R=12 provenance; do not derive R from 2pi/A0.",
        },
        {
            "order": 2,
            "artifact_id": "CR114",
            "role": "derives 1/8 from D binary face-states",
            "status": "PASS",
            "source_path": str(CR114_LOCK),
            "doc_rule": "Cite this before QP092A whenever explaining why the carrier fraction is 1/8.",
        },
        {
            "order": 3,
            "artifact_id": "QP091T",
            "role": "applies 7/8 retention and D^2/R debit to Higgs parent/surface",
            "status": "PASS",
            "source_path": str(QUANTUM_ROOT / "artifacts" / "qp091t" / "QP091T_result.md"),
            "doc_rule": "Exact Higgs math: 126 parent, 125.25 observed surface; q_split is context only.",
        },
        {
            "order": 4,
            "artifact_id": "QP091U",
            "role": "hard-freezes QP091T and rejects D/R/debit wrong controls",
            "status": "PASS",
            "source_path": str(QUANTUM_ROOT / "artifacts" / "qp091u" / "QP091U_result.md"),
            "doc_rule": "Use for hash/freeze and wrong-control support.",
        },
        {
            "order": 5,
            "artifact_id": "QP092A",
            "role": "classifies split_loss=18 as unresolved tensor-carrier support, not matter",
            "status": "PASS",
            "source_path": str(QUANTUM_ROOT / "artifacts" / "qp092a_split_loss_tensor_carrier" / "QP092A_SPLIT_LOSS_TENSOR_CARRIER_result.md"),
            "doc_rule": "Now downstream of CR114; do not present QP092A's predeclared identity as first source of 1/8.",
        },
        {
            "order": 6,
            "artifact_id": "QP092F",
            "role": "packetizes carrier into two massless tensor modes",
            "status": "PASS",
            "source_path": str(QUANTUM_ROOT / "artifacts" / "qp092f_tensor_carrier_wave_mode" / "QP092F_TENSOR_CARRIER_WAVE_MODE_result.md"),
            "doc_rule": "Use for plus/cross 1/16 + 1/16 support and non-matter wave-mode guardrail.",
        },
        {
            "order": 7,
            "artifact_id": "QP092G",
            "role": "bridges weak field, A=1 boundary, and unresolved quantum support",
            "status": "PASS",
            "source_path": str(QUANTUM_ROOT / "artifacts" / "qp092g_tensor_carrier_bridge_packet" / "QP092G_TENSOR_CARRIER_BRIDGE_PACKET_result.md"),
            "doc_rule": "Use for A=1 closure: 7/8 + 1/16 + 1/16 = 1.",
        },
        {
            "order": 8,
            "artifact_id": "QP091X",
            "role": "adjacent surface-coefficient scan; does not close general S_debit magnitude law",
            "status": "PASS_WITH_OPEN_LAW",
            "source_path": str(QUANTUM_ROOT / "artifacts" / "qp091x" / "QP091X_result.md"),
            "doc_rule": "Use as caution: Higgs parent/surface is closed; general particle S_debit magnitude remains open.",
        },
    ]
    for row in rows:
        p = Path(row["source_path"])
        row["exists"] = p.exists()
        row["sha256"] = sha256_file(p)
    return rows


def write_lineage() -> list[dict[str, Any]]:
    rows = lineage_rows()
    write_csv(LINEAGE_CSV, rows, ["order", "artifact_id", "role", "status", "source_path", "exists", "sha256", "doc_rule"])
    payload = {
        "artifact": "CR114_DOC_READINESS_LINEAGE_ZIPPER",
        "generated_at_utc": now_utc(),
        "verdict": "DOC_READY_LINEAGE_SOURCE_ORDER_DEFINED",
        "rule": "CR114 is now the first citation for why the split fraction is 1/8; QP092A is downstream classification, not the primitive source.",
        "rows": rows,
    }
    write_json(LINEAGE_JSON, payload)

    md = ["# CR114 Lineage Zipper\n\n"]
    md.append("## Doc Rule\n\n")
    md.append("CR114 is now the first citation for why the split fraction is `1/8`. QP092A remains the downstream classification that says `18` is tensor-carrier/source support, not matter.\n\n")
    md.append("## Chain\n\n")
    md.append("| Order | Artifact | Role | Doc Rule |\n|---:|---|---|---|\n")
    for row in rows:
        md.append(f"| {row['order']} | {row['artifact_id']} | {row['role']} | {row['doc_rule']} |\n")
    md.append("\n## Canonical Wording\n\n")
    md.append("Use this wording when updating manuscript/docs:\n\n")
    md.append("> CR114 derives the split fraction from binary face-state geometry: `D=3` independent binary closure axes give `2^D=8` face-states, of which one is unresolved tensor-carrier support. Therefore the carrier fraction is `1/8` and the retained scalar fraction is `7/8`. QP091T applies this to the Higgs parent/surface, and QP092A/F/G classify the released `18` as tensor-carrier support, not a matter row.\n")
    LINEAGE_MD.write_text("".join(md), encoding="utf-8")
    return rows


def update_hash_ledgers(extra_artifacts: list[Path]) -> None:
    existing_cr114 = sorted(CR_DIR.glob("CR114*"))
    artifacts = []
    seen: set[str] = set()
    for path in existing_cr114 + extra_artifacts:
        if path.is_file() and path.name != LOCAL_HASHES.name:
            key = str(path).lower()
            if key not in seen:
                seen.add(key)
                artifacts.append(path)
    local_lines = [f"{sha256_file(path)}  {branch_rel(path)}" for path in artifacts]
    LOCAL_HASHES.write_text("\n".join(local_lines) + "\n", encoding="ascii")

    existing = BRANCH_HASHES.read_text(encoding="utf-8", errors="replace").splitlines() if BRANCH_HASHES.exists() else []
    prefix = "CR114_BINARY_FACE_STATE_SPLIT_THEOREM\\"
    kept = [line for line in existing if prefix not in line]
    branch_artifacts = artifacts + [LOCAL_HASHES]
    branch_lines = [f"{sha256_file(path)}  {branch_rel(path)}" for path in branch_artifacts]
    BRANCH_HASHES.write_text("\n".join(kept + branch_lines) + "\n", encoding="utf-8")


def main() -> int:
    print("CR114 doc-readiness runner: starting")
    cr114 = read_json(CR114_SUMMARY)
    if cr114.get("result_class") != "CR114_PASS_BINARY_FACE_STATE_SPLIT_THEOREM":
        raise SystemExit("CR114 must pass before doc-readiness packaging")

    render_figure()
    stale_rows = run_stale_scan()
    lineage = write_lineage()

    review_count = sum(1 for row in stale_rows if str(row["status"]).startswith("NEEDS") or row["status"] == "CHECK_CITATION")
    needs_replace = sum(1 for row in stale_rows if row["status"] == "NEEDS_REPLACE")
    figure_ok = FIG_PNG.exists() and FIG_SVG.exists() and sha256_file(FIG_PNG) and sha256_file(FIG_SVG)
    lineage_ok = all(row["exists"] and row["sha256"] for row in lineage)
    status = "DOC_READINESS_PASS_WITH_REVIEW_ITEMS" if figure_ok and lineage_ok else "DOC_READINESS_FAIL"

    summary = {
        "artifact": "CR114_DOC_READINESS_PACKAGE",
        "generated_at_utc": now_utc(),
        "result_class": status,
        "execution_status": "CLEAN" if figure_ok and lineage_ok else "CHECK",
        "figure_png": rel(FIG_PNG),
        "figure_svg": rel(FIG_SVG),
        "figure_png_sha256": sha256_file(FIG_PNG),
        "figure_svg_sha256": sha256_file(FIG_SVG),
        "stale_scan_csv": rel(STALE_SCAN_CSV),
        "stale_scan_md": rel(STALE_SCAN_MD),
        "stale_scan_rows": len(stale_rows),
        "review_item_count": review_count,
        "needs_replace_count": needs_replace,
        "lineage_csv": rel(LINEAGE_CSV),
        "lineage_md": rel(LINEAGE_MD),
        "lineage_json": rel(LINEAGE_JSON),
        "lineage_rows": len(lineage),
        "doc_rule": "When explaining 1/8, cite CR114 first; QP092A is downstream classification of 18 as non-matter tensor-carrier support.",
    }
    write_json(SUMMARY_JSON, summary)

    update_hash_ledgers([FIG_PNG, FIG_SVG, STALE_SCAN_CSV, STALE_SCAN_MD, LINEAGE_CSV, LINEAGE_MD, LINEAGE_JSON, SUMMARY_JSON])

    print(f"CR114 doc-readiness result_class={status}")
    print(f"CR114 deterministic figure={FIG_PNG}")
    print(f"CR114 stale scan rows={len(stale_rows)} review_items={review_count} needs_replace={needs_replace}")
    print(f"CR114 lineage rows={len(lineage)}")
    print("CR114 doc-readiness runner: complete")
    return 0 if figure_ok and lineage_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
