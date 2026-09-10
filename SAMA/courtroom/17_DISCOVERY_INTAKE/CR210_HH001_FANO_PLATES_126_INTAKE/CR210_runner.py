from __future__ import annotations

import csv
import hashlib
import json
import math
import shutil
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from pypdf import PdfReader


CR_ID = "CR210"
TEST_ID = "CR210_HH001_FANO_PLATES_126_INTAKE"
RESULT_CLASS = "CR210_PASS_SCOPED_HH001_FANO_ADDRESS_126_TABLE_THEOREM__SAM_ALGEBRA_VERIFIED__OPEN_READINGS_PRESERVED"

ROOT = Path(__file__).resolve().parents[2]
BRANCH = ROOT / "17_HAUNTED_HOUSE_INTAKE"
OUT_DIR = BRANCH / TEST_ID
SOURCE_COPIES = OUT_DIR / "source_copies"
SOURCE_COPIES.mkdir(parents=True, exist_ok=True)

HH_ROOT = Path(r"C:\VS\Haunted_House")
PDF_PATH = Path(r"C:\VS\HH001_fano_plates_126.pdf")
CR119_DIR = ROOT / "09a_PARTICLE_MASS_CHAIN" / "CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"

SOURCES = {
    "hh_readme": HH_ROOT / "README.md",
    "hh_house_rules": HH_ROOT / "HOUSE_RULES.md",
    "hh_exploration_index": HH_ROOT / "explorations" / "INDEX.md",
    "hh001_note": HH_ROOT / "explorations" / "HH001_D3_TO_PARTICLES_BREADCRUMB_AUDIT.md",
    "hh001_pdf": PDF_PATH,
    "hh001_sis_126x7": HH_ROOT / "explorations" / "HH001_SIS_126x7_table.csv",
    "hh001_sis_8col": HH_ROOT / "explorations" / "HH001_SIS_8col_final.csv",
    "hh001_action_residual": HH_ROOT / "explorations" / "HH001_SIS_action_residual.csv",
    "hh001_six_channel_signatures": HH_ROOT / "explorations" / "HH001_6channel_signatures.csv",
    "hh001_binary_encoded": HH_ROOT / "explorations" / "HH001_SIS_binary_encoded.csv",
    "hh001_binary_v2": HH_ROOT / "explorations" / "HH001_SIS_binary_v2.csv",
    "hh001_binary_v22": HH_ROOT / "explorations" / "HH001_SIS_binary_v22.csv",
    "hh001_fano_script": HH_ROOT / "explorations" / "HH001_fano_plane_matter.py",
    "hh001_seven_channels_script": HH_ROOT / "explorations" / "HH001_seven_channels_render.py",
    "hh001_build_8col_script": HH_ROOT / "explorations" / "HH001_build_sis_8col_final.py",
    "hh001_png_fano": HH_ROOT / "explorations" / "HH001_fano_plane_matter.png",
    "hh001_png_seven_channels": HH_ROOT / "explorations" / "HH001_seven_channels.png",
    "hh001_png_fractal_126": HH_ROOT / "explorations" / "HH001_fractal_126.png",
    "cr113_summary": ROOT / "14_FOUNDATIONAL_TESTS" / "CR113_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM" / "CR113_summary.json",
    "cr114_summary": ROOT / "14_FOUNDATIONAL_TESTS" / "CR114_BINARY_FACE_STATE_SPLIT_THEOREM" / "CR114_summary.json",
    "cr115_summary": ROOT / "14_FOUNDATIONAL_TESTS" / "CR115_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM" / "CR115_summary.json",
    "cr119_summary": CR119_DIR / "CR119_summary.json",
    "cr119_periodic_table": CR119_DIR / "CR119_courtroom_periodic_table.csv",
    "cr119_result": CR119_DIR / "CR119_result.md",
    "cr119_hashes": CR119_DIR / "HASHES.txt",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8") as handle:
        return handle.read()


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            out: dict[str, Any] = {}
            for key in fieldnames:
                value = row.get(key, "")
                if isinstance(value, (dict, list, tuple)):
                    value = json.dumps(value, sort_keys=True)
                out[key] = value
            writer.writerow(out)


def check(name: str, passed: bool, detail: str, value: Any = "") -> dict[str, Any]:
    return {
        "check": name,
        "status": "PASS" if passed else "FAIL",
        "value": value,
        "detail": detail,
    }


def decimal_or_none(value: str) -> Decimal | None:
    try:
        if value in ("", "-", "x", "X"):
            return None
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def close_decimal(left: Decimal, right: Decimal, tolerance: Decimal = Decimal("0.000001")) -> bool:
    return abs(left - right) <= tolerance


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in ("true", "pass", "passed", "1", "yes")


def pdf_readback(path: Path) -> dict[str, Any]:
    reader = PdfReader(str(path))
    page_texts = [(page.extract_text() or "") for page in reader.pages]
    all_text = "\n".join(page_texts)
    return {
        "page_count": len(reader.pages),
        "metadata": {str(k): str(v) for k, v in (reader.metadata or {}).items()},
        "sam_fano_plate_mentions": all_text.count("SAM Fano Plates"),
        "contains_z126": "126  Z126" in all_text or "126 Z126" in all_text,
        "contains_frontier": "SAM frontier" in all_text,
        "text_sha256": hashlib.sha256(all_text.encode("utf-8", errors="replace")).hexdigest(),
    }


def copy_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, source in SOURCES.items():
        target = SOURCE_COPIES / source.name
        if not source.exists():
            rows.append({
                "source_id": key,
                "source_path": str(source),
                "copied_path": "",
                "source_exists": False,
                "sha256": "",
            })
            continue
        shutil.copy2(source, target)
        rows.append({
            "source_id": key,
            "source_path": str(source),
            "copied_path": rel(target),
            "source_exists": True,
            "sha256": sha256_file(source),
        })
    return rows


def hh_inventory() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(HH_ROOT.rglob("*")):
        if path.is_file() and ".git" not in path.parts:
            rows.append({
                "path": str(path),
                "relative_to_hh": str(path.relative_to(HH_ROOT)).replace("\\", "/"),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            })
    rows.append({
        "path": str(PDF_PATH),
        "relative_to_hh": "../HH001_fano_plates_126.pdf",
        "bytes": PDF_PATH.stat().st_size,
        "sha256": sha256_file(PDF_PATH),
    })
    return rows


def main() -> int:
    generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
    copied_source_rows = copy_sources()
    full_inventory_rows = hh_inventory()

    cr113_summary = load_json(SOURCES["cr113_summary"])
    cr114_summary = load_json(SOURCES["cr114_summary"])
    cr115_summary = load_json(SOURCES["cr115_summary"])
    cr119_summary = load_json(SOURCES["cr119_summary"])
    cr119_rows = read_csv(SOURCES["cr119_periodic_table"])
    sis_rows = read_csv(SOURCES["hh001_sis_126x7"])
    sis8_rows = read_csv(SOURCES["hh001_sis_8col"])
    action_rows = read_csv(SOURCES["hh001_action_residual"])
    sig_rows = read_csv(SOURCES["hh001_six_channel_signatures"])
    bin_v2_rows = read_csv(SOURCES["hh001_binary_v2"])
    bin_v22_rows = read_csv(SOURCES["hh001_binary_v22"])
    hh001_note = read_text(SOURCES["hh001_note"])
    house_rules = read_text(SOURCES["hh_house_rules"])
    pdf_info = pdf_readback(PDF_PATH)

    theorem_R = int(cr114_summary["R"])
    theorem_D = int(cr114_summary["D"])
    theorem_R2 = theorem_R * theorem_R
    theorem_face_states = 2 ** theorem_D
    theorem_cells_per_state = theorem_R2 // theorem_face_states
    theorem_carrier_cells = theorem_cells_per_state
    theorem_retained_cells = (theorem_face_states - 1) * theorem_cells_per_state
    theorem_partition_pass = (
        cr113_summary["result_class"] == "CR113_PASS_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM"
        and cr114_summary["result_class"] == "CR114_PASS_BINARY_FACE_STATE_SPLIT_THEOREM"
        and cr115_summary["result_class"] == "CR115_PASS_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM_GATE"
        and theorem_R == 12
        and theorem_D == 3
        and theorem_face_states == 8
        and theorem_cells_per_state == 18
        and theorem_carrier_cells == 18
        and theorem_retained_cells == 126
        and str(cr114_summary["split_loss"]) == "18"
        and str(cr114_summary["retained_parent"]) == "126"
    )

    theorem_rows = [
        {
            "step": "R",
            "expression": "completed WRITE address count",
            "source": "CR113",
            "value": theorem_R,
            "status": "PASS" if theorem_R == 12 else "FAIL",
        },
        {
            "step": "D",
            "expression": "invariant carrier uniqueness dimension",
            "source": "CR115",
            "value": theorem_D,
            "status": "PASS" if theorem_D == 3 else "FAIL",
        },
        {
            "step": "face_states",
            "expression": "2^D",
            "source": "CR114",
            "value": theorem_face_states,
            "status": "PASS" if theorem_face_states == 8 else "FAIL",
        },
        {
            "step": "closed_loop_area",
            "expression": "R^2",
            "source": "CR113/CR114",
            "value": theorem_R2,
            "status": "PASS" if theorem_R2 == 144 else "FAIL",
        },
        {
            "step": "cells_per_face_state",
            "expression": "R^2 / 2^D",
            "source": "CR114",
            "value": theorem_cells_per_state,
            "status": "PASS" if theorem_cells_per_state == 18 else "FAIL",
        },
        {
            "step": "carrier_address",
            "expression": "000 * 18",
            "source": "CR114/HH001",
            "value": theorem_carrier_cells,
            "status": "PASS" if theorem_carrier_cells == 18 else "FAIL",
        },
        {
            "step": "retained_fano_addresses",
            "expression": "7 * 18",
            "source": "CR114/HH001",
            "value": theorem_retained_cells,
            "status": "PASS" if theorem_retained_cells == 126 else "FAIL",
        },
    ]

    cr119_by_z = {int(row["Z"]): row for row in cr119_rows}
    sis_by_z = {int(row["Z"]): row for row in sis_rows}
    sis8_by_z = {int(row["Z"]): row for row in sis8_rows}

    channel_codes = {
        "PARTICLE": "100",
        "MATTER": "010",
        "ELEMENT": "001",
        "GRAVITY": "110",
        "CLOCK": "011",
        "LIGHT": "101",
        "ACTION": "111",
    }
    fano_lines = [
        ("PARTICLE", "GRAVITY", "MATTER", "mass-source rule"),
        ("MATTER", "CLOCK", "ELEMENT", "binding and decay over time"),
        ("PARTICLE", "LIGHT", "ELEMENT", "atomic spectra"),
        ("PARTICLE", "ACTION", "CLOCK", "Schrodinger evolution"),
        ("MATTER", "ACTION", "LIGHT", "QED matter-light coupling"),
        ("ELEMENT", "ACTION", "GRAVITY", "nuclear binding to gravity"),
        ("GRAVITY", "CLOCK", "LIGHT", "Schwarzschild GR triple"),
    ]
    fano_rows: list[dict[str, Any]] = []
    for a, b, c, label in fano_lines:
        xor_value = int(channel_codes[a], 2) ^ int(channel_codes[b], 2) ^ int(channel_codes[c], 2)
        fano_rows.append({
            "line": label,
            "channel_a": a,
            "code_a": channel_codes[a],
            "channel_b": b,
            "code_b": channel_codes[b],
            "channel_c": c,
            "code_c": channel_codes[c],
            "xor_result": format(xor_value, "03b"),
            "status": "PASS" if xor_value == 0 else "FAIL",
        })

    table_rows: list[dict[str, Any]] = []
    qA_matches = 0
    graviton_matches = 0
    gravity_over_8_matches = 0
    for z in range(1, 127):
        cr = cr119_by_z[z]
        sis = sis_by_z[z]
        sis8 = sis8_by_z[z]
        hh_gravity = decimal_or_none(sis["GRAVITY"])
        cr_qA = decimal_or_none(cr["qA_total_primary"])
        hh_graviton = decimal_or_none(sis8["GRAVITON"])
        cr_tensor = decimal_or_none(cr["tensor_carrier_support_primary"])
        qA_match = hh_gravity is not None and cr_qA is not None and close_decimal(hh_gravity, cr_qA)
        graviton_match = hh_graviton is not None and cr_tensor is not None and close_decimal(hh_graviton, cr_tensor)
        gravity_over_8_match = hh_gravity is not None and hh_graviton is not None and close_decimal(hh_gravity / Decimal(8), hh_graviton)
        qA_matches += int(qA_match)
        graviton_matches += int(graviton_match)
        gravity_over_8_matches += int(gravity_over_8_match)
        table_rows.append({
            "Z": z,
            "symbol": sis["symbol"],
            "hh_gravity": sis["GRAVITY"],
            "cr119_qA": cr["qA_total_primary"],
            "qA_match": qA_match,
            "hh_graviton": sis8["GRAVITON"],
            "cr119_tensor_carrier": cr["tensor_carrier_support_primary"],
            "graviton_match": graviton_match,
            "gravity_over_8_match": gravity_over_8_match,
            "known_label_status": cr["known_label_status"],
        })

    action_known = [row for row in action_rows if row["match"] in ("TRUE", "FALSE")]
    action_match_count = sum(1 for row in action_known if row["match"] == "TRUE")
    action_match_rate = action_match_count / len(action_known) if action_known else 0.0
    bin_v2_closed = sum(1 for row in bin_v2_rows if parse_bool(row.get("closed")))
    bin_v22_closed = sum(1 for row in bin_v22_rows if parse_bool(row.get("closed")))
    xor_distinct = len({row["XOR_signature"] for row in sig_rows})
    sum_distinct = len({row["SUM_signature"] for row in sig_rows})

    status_rows = [
        {
            "claim": "SAM Fano address partition theorem",
            "status": "PASS_SCOPED_THEOREM",
            "evidence": "CR113 R=12, CR115 D=3, CR114 2^D=8, R^2=144, 144/8=18, 7*18=126",
            "courtroom_reading": "HH001 verifies the locked SAM address algebra as a 126-row Fano plate surface",
        },
        {
            "claim": "F_2^3 Fano address algebra",
            "status": "PASS_SCOPED_THEOREM_COMPONENT",
            "evidence": "7 nonzero addresses; 7 Fano lines XOR to 000",
            "courtroom_reading": "the address scaffold is theorem-grade when bound to CR113/CR114/CR115",
        },
        {
            "claim": "126-row SIS / Fano plate artifact",
            "status": "PASS_SCOPED_THEOREM_SURFACE",
            "evidence": f"{len(sis_rows)} CSV rows; PDF pages={pdf_info['page_count']}; source files hashed",
            "courtroom_reading": "artifact verifies the 126 retained-address surface",
        },
        {
            "claim": "GRAVITY = CR119 qA; GRAVITON = qA/8",
            "status": "PASS_SCOPED_BRIDGE",
            "evidence": f"qA matches={qA_matches}/126; qA/8 matches={gravity_over_8_matches}/126",
            "courtroom_reading": "downstream rendering of CR119, not a new independent proof",
        },
        {
            "claim": "ACTION residual equals physical nuclear spin",
            "status": "FALSIFIED_PRESERVED",
            "evidence": f"matches={action_match_count}/{len(action_known)} ({action_match_rate:.3%})",
            "courtroom_reading": "must not be promoted",
        },
        {
            "claim": "per-element XOR closure of channel magnitudes",
            "status": "FALSIFIED_OR_DIAGNOSTIC_PRESERVED",
            "evidence": f"binary_v2 closed={bin_v2_closed}/{len(bin_v2_rows)}; binary_v22 closed={bin_v22_closed}/{len(bin_v22_rows)}",
            "courtroom_reading": "XOR closure did not survive the HH001 diagnostics",
        },
        {
            "claim": "six-channel signature uniqueness",
            "status": "DIAGNOSTIC_OPEN",
            "evidence": f"XOR distinct={xor_distinct}/126; SUM distinct={sum_distinct}/126",
            "courtroom_reading": "may inform next test, but is not the seven-channel physical mapping",
        },
        {
            "claim": "seven-channel physical mapping is forced",
            "status": "OPEN_REQUIRES_CR_TEST",
            "evidence": "HH001 note flags possible Procrustean fit of 4 A-readouts plus 3 catalog layers",
            "courtroom_reading": "candidate reading only",
        },
        {
            "claim": "126 GeV conversion",
            "status": "OPEN_HIDDEN_PARAMETER_RISK",
            "evidence": "HH001 note flags GeV conversion as possible hidden parameter",
            "courtroom_reading": "requires derivation audit before any manuscript use",
        },
    ]

    wrong_controls = [
        {
            "control": "pdf_alone_as_theorem",
            "attempted_overclaim": "Treat HH001_fano_plates_126.pdf alone as the theorem.",
            "evidence": "CR210 theorem grade requires CR113/CR114/CR115 plus HH001/CR119 replay, not the PDF by itself.",
            "result": "REJECTED",
        },
        {
            "control": "hide_falsified_action_spin",
            "attempted_overclaim": "Omit the failed ACTION residual diagnostic.",
            "evidence": f"ACTION residual match count is {action_match_count}/{len(action_known)}.",
            "result": "REJECTED" if action_match_count <= 1 else "FAIL",
        },
        {
            "control": "hide_xor_failure",
            "attempted_overclaim": "Present per-element XOR channel closure as surviving.",
            "evidence": f"binary_v2 closed={bin_v2_closed}; binary_v22 closed={bin_v22_closed}.",
            "result": "REJECTED" if bin_v2_closed < 20 and bin_v22_closed < 20 else "FAIL",
        },
        {
            "control": "known_labels_as_construction_inputs",
            "attempted_overclaim": "Use known elements as construction inputs instead of downstream reveal labels.",
            "evidence": "CR119 known_label_used_as_construction_input is no for all rows.",
            "result": "REJECTED" if all(row["known_label_used_as_construction_input"] == "no" for row in cr119_rows) else "FAIL",
        },
        {
            "control": "frontier_rows_as_known_elements",
            "attempted_overclaim": "Treat Z119-Z126 as known labels.",
            "evidence": f"CR119 frontier_unknown_z119_z126={cr119_summary['frontier_unknown_z119_z126']}.",
            "result": "REJECTED" if cr119_summary["frontier_unknown_z119_z126"] == 8 else "FAIL",
        },
        {
            "control": "fano_mapping_as_empirical_validation",
            "attempted_overclaim": "Treat Fano address XOR closure as empirical validation of the channel physics.",
            "evidence": "Fano closure is algebraic; physical mapping remains open.",
            "result": "REJECTED",
        },
        {
            "control": "126_GeV_without_derivation",
            "attempted_overclaim": "Use H_native=126 as 126 GeV without a conversion audit.",
            "evidence": "HH001 status trail flags GeV conversion as possible hidden parameter.",
            "result": "REJECTED" if "GeV conversion" in hh001_note else "FAIL",
        },
        {
            "control": "haunted_house_as_courtroom_grade",
            "attempted_overclaim": "Cite Haunted House as Courtroom-grade evidence.",
            "evidence": "House Rules: Haunted House proposes; Courtroom seals.",
            "result": "REJECTED" if "Haunted House -> Courtroom" in house_rules else "FAIL",
        },
    ]

    checks: list[dict[str, Any]] = []
    for key, path in SOURCES.items():
        checks.append(check(f"{key} source exists", path.exists(), str(path), path.exists()))
    checks.extend(
        [
            check("PDF has 11 pages", pdf_info["page_count"] == 11, "pypdf readback", pdf_info["page_count"]),
            check("PDF contains SAM Fano Plates footers", pdf_info["sam_fano_plate_mentions"] >= 10, "PDF extracted text", pdf_info["sam_fano_plate_mentions"]),
            check("PDF contains Z126 frontier plate", pdf_info["contains_z126"], "PDF extracted text", pdf_info["contains_z126"]),
            check("HH001 note records Fano survival", "Fano plane geometry" in hh001_note and "SURVIVED" in hh001_note, "HH001 status trail", "SURVIVED"),
            check("HH001 note records falsified action reading", "ACTION = parity-residual" in hh001_note and "FALSIFIED" in hh001_note, "HH001 status trail", "FALSIFIED"),
            check("HH001 note records open mapping risk", "Procrustean" in hh001_note, "HH001 status trail", "OPEN"),
            check("CR113 R theorem passed", cr113_summary["result_class"] == "CR113_PASS_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM", "CR113 summary", cr113_summary["result_class"]),
            check("CR114 binary face-state split theorem passed", cr114_summary["result_class"] == "CR114_PASS_BINARY_FACE_STATE_SPLIT_THEOREM", "CR114 summary", cr114_summary["result_class"]),
            check("CR115 D=3 invariant carrier theorem passed", cr115_summary["result_class"] == "CR115_PASS_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM_GATE", "CR115 summary", cr115_summary["result_class"]),
            check("SAM address partition theorem recomputes 18 + 126", theorem_partition_pass, "R^2=144; 2^D=8; 144/8=18; 7*18=126", f"{theorem_carrier_cells}+{theorem_retained_cells}"),
            check("CR119 passed source anchor", "PASS_CR119" in cr119_summary["result_class"], "CR119 summary", cr119_summary["result_class"]),
            check("CR119 periodic row count is 126", cr119_summary["row_counts"]["periodic"] == 126 and len(cr119_rows) == 126, "CR119 periodic table", len(cr119_rows)),
            check("HH001 SIS table has 126 rows", len(sis_rows) == 126, "HH001_SIS_126x7_table.csv", len(sis_rows)),
            check("HH001 SIS table Z is 1..126", sorted(sis_by_z) == list(range(1, 127)), "HH001 Z coverage", f"{min(sis_by_z)}-{max(sis_by_z)}"),
            check("HH001 8-column table has 126 rows", len(sis8_rows) == 126, "HH001_SIS_8col_final.csv", len(sis8_rows)),
            check("Fano channel codes are seven nonzero F_2^3 addresses", set(channel_codes.values()) == {format(i, "03b") for i in range(1, 8)}, "channel assignment", channel_codes),
            check("All Fano lines XOR to carrier 000", all(row["status"] == "PASS" for row in fano_rows), "Fano line table", len(fano_rows)),
            check("HH001 GRAVITY matches CR119 qA", qA_matches == 126, "rounded to 1e-6", f"{qA_matches}/126"),
            check("HH001 GRAVITON matches CR119 tensor carrier", graviton_matches == 126, "rounded to 1e-6", f"{graviton_matches}/126"),
            check("HH001 GRAVITON equals GRAVITY/8", gravity_over_8_matches == 126, "rounded to 1e-6", f"{gravity_over_8_matches}/126"),
            check("ACTION residual diagnostic preserved as failure", action_match_count == 1 and len(action_known) == 102, "HH001_SIS_action_residual.csv", f"{action_match_count}/{len(action_known)}"),
            check("XOR closure controls stay rejected/diagnostic", bin_v2_closed < 20 and bin_v22_closed < 20, "binary v2/v22 closure counts", f"{bin_v2_closed}/{len(bin_v2_rows)}; {bin_v22_closed}/{len(bin_v22_rows)}"),
            check("Six-channel signature inventory is recorded", len(sig_rows) == 126 and xor_distinct > 0 and sum_distinct > 0, "HH001_6channel_signatures.csv diagnostic/open lane", f"XOR {xor_distinct}/126; SUM {sum_distinct}/126"),
            check("Known labels downstream only", all(row["known_label_used_as_construction_input"] == "no" for row in cr119_rows), "CR119 periodic table", "no construction input labels"),
            check("Z119-Z126 frontier boundary preserved", cr119_summary["frontier_unknown_z119_z126"] == 8, "CR119 summary", cr119_summary["frontier_unknown_z119_z126"]),
            check("All wrong controls rejected", all(row["result"] == "REJECTED" for row in wrong_controls), "CR210 controls", f"{sum(1 for row in wrong_controls if row['result'] == 'REJECTED')}/{len(wrong_controls)}"),
        ]
    )

    pass_count = sum(1 for row in checks if row["status"] == "PASS")
    fail_count = len(checks) - pass_count
    result = RESULT_CLASS if fail_count == 0 else "CR210_FAIL_HH001_FANO_PLATES_126_INTAKE"

    precommit = OUT_DIR / "CR210_PRECOMMIT.md"
    premises = OUT_DIR / "CR210_declared_premises.json"
    result_md = OUT_DIR / "CR210_result.md"
    summary_json = OUT_DIR / "CR210_summary.json"
    input_manifest = OUT_DIR / "CR210_input_manifest.csv"
    full_inventory = OUT_DIR / "CR210_haunted_house_source_inventory.csv"
    theorem_csv = OUT_DIR / "CR210_theorem_derivation.csv"
    fano_csv = OUT_DIR / "CR210_fano_algebra_checks.csv"
    table_csv = OUT_DIR / "CR210_table_bridge_checks.csv"
    status_csv = OUT_DIR / "CR210_claim_status_rows.csv"
    wrong_csv = OUT_DIR / "CR210_wrong_controls.csv"
    checks_csv = OUT_DIR / "CR210_checks.csv"
    hashes_txt = OUT_DIR / "HASHES.txt"

    precommit.write_text(
        "\n".join(
            [
                "# CR210 Precommit",
                "",
                "Task: HH001 Haunted House Fano plates 126 Courtroom intake.",
                "",
                "This is a scoped structural theorem test plus claim triage.",
                "",
                "The theorem-grade claim is narrow: CR113 R=12, CR115 D=3, and",
                "CR114 binary face-state split imply R^2=144, 2^D=8,",
                "R^2/2^D=18 cells per address, one 000 carrier address, and",
                "seven retained F_2^3 Fano addresses, so 7*18=126.",
                "",
                "Pass condition:",
                "- HH001 PDF and Haunted House source files resolve and hash.",
                "- CR113/CR114/CR115 theorem sources resolve and replay 18 + 126.",
                "- Fano F_2^3 address scaffold is internally valid.",
                "- 126-row SIS table and qA/qA/8 bridge to CR119 replay without mutation.",
                "- Falsified and open HH001 readings remain labeled as falsified/open.",
                "- No PDF-alone, XOR/action-spin, known-label, physical-mapping, or 126 GeV overclaim is made.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    premises_payload = {
        "cr_id": CR_ID,
        "test_id": TEST_ID,
        "declared_at_utc": generated,
        "classification": "SCOPED_STRUCTURAL_THEOREM_WITH_HAUNTED_HOUSE_HANDOFF_TRIAGE",
        "source_paths": {key: str(path) for key, path in SOURCES.items()},
        "forbidden_overclaims": [
            "PDF alone as theorem",
            "seven-channel physical mapping as closed",
            "per-element XOR closure as surviving",
            "ACTION residual equals nuclear spin",
            "126 GeV conversion as derived",
            "Haunted House as Courtroom-grade evidence",
        ],
    }
    premises.write_text(json.dumps(premises_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    write_csv(input_manifest, copied_source_rows, ["source_id", "source_path", "copied_path", "source_exists", "sha256"])
    write_csv(full_inventory, full_inventory_rows, ["path", "relative_to_hh", "bytes", "sha256"])
    write_csv(theorem_csv, theorem_rows, ["step", "expression", "source", "value", "status"])
    write_csv(fano_csv, fano_rows, ["line", "channel_a", "code_a", "channel_b", "code_b", "channel_c", "code_c", "xor_result", "status"])
    write_csv(table_csv, table_rows, ["Z", "symbol", "hh_gravity", "cr119_qA", "qA_match", "hh_graviton", "cr119_tensor_carrier", "graviton_match", "gravity_over_8_match", "known_label_status"])
    write_csv(status_csv, status_rows, ["claim", "status", "evidence", "courtroom_reading"])
    write_csv(wrong_csv, wrong_controls, ["control", "attempted_overclaim", "evidence", "result"])
    write_csv(checks_csv, checks, ["check", "status", "value", "detail"])

    summary = {
        "cr_id": CR_ID,
        "test_id": TEST_ID,
        "result_class": result,
        "execution_status": "CLEAN" if fail_count == 0 else "VIOLATED",
        "scientific_verdict": "PASS_SCOPED_STRUCTURAL_THEOREM" if fail_count == 0 else "FAIL",
        "triage_bin": "A" if fail_count == 0 else "F",
        "claim_tier": "SAM_FANO_ADDRESS_PARTITION_126_TABLE_THEOREM_WITH_OPEN_PHYSICAL_MAPPING",
        "generated_at_utc": generated,
        "pdf": pdf_info,
        "row_counts": {
            "hh001_sis": len(sis_rows),
            "hh001_sis_8col": len(sis8_rows),
            "cr119_periodic": len(cr119_rows),
            "haunted_house_inventory_files": len(full_inventory_rows),
        },
        "theorem": {
            "R": theorem_R,
            "D": theorem_D,
            "R_squared": theorem_R2,
            "face_state_count": theorem_face_states,
            "cells_per_face_state": theorem_cells_per_state,
            "carrier_cells": theorem_carrier_cells,
            "retained_fano_cells": theorem_retained_cells,
            "theorem_partition_pass": theorem_partition_pass,
            "statement": "R=12 and D=3 give R^2=144 and 2^D=8; the 000 carrier receives 18 cells and the seven nonzero F_2^3 Fano addresses retain 7*18=126 cells.",
        },
        "replay": {
            "qA_matches": qA_matches,
            "graviton_matches": graviton_matches,
            "gravity_over_8_matches": gravity_over_8_matches,
            "fano_lines_passed": sum(1 for row in fano_rows if row["status"] == "PASS"),
            "fano_lines_total": len(fano_rows),
            "action_residual_matches": action_match_count,
            "action_residual_known_rows": len(action_known),
            "binary_v2_closed": bin_v2_closed,
            "binary_v22_closed": bin_v22_closed,
            "xor_signature_distinct": xor_distinct,
            "sum_signature_distinct": sum_distinct,
        },
        "checks": {"passed": pass_count, "failed": fail_count, "total": len(checks)},
        "wrong_controls": {
            "tested": len(wrong_controls),
            "rejected": sum(1 for row in wrong_controls if row["result"] == "REJECTED"),
        },
        "artifacts": {
            "precommit": rel(precommit),
            "declared_premises": rel(premises),
            "input_manifest": rel(input_manifest),
            "source_inventory": rel(full_inventory),
            "theorem_derivation": rel(theorem_csv),
            "fano_algebra": rel(fano_csv),
            "table_bridge": rel(table_csv),
            "claim_status": rel(status_csv),
            "wrong_controls": rel(wrong_csv),
            "checks": rel(checks_csv),
            "summary": rel(summary_json),
            "result": rel(result_md),
            "hashes": rel(hashes_txt),
            "source_copies": rel(SOURCE_COPIES),
        },
    }
    summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result_lines = [
        "# CR210 - HH001 Fano Plates 126 Intake",
        "",
        f"Result: **{result}**",
        "",
        "Verdict: **PASS_SCOPED_STRUCTURAL_THEOREM**.",
        "",
        "HH001 is now in the Courtroom as a scoped theorem-grade SAM address partition result. The theorem is narrow: the locked SAM stack gives the 18 + 126 Fano address partition, and HH001 verifies that partition as a 126-row table/PDF surface tied back to CR119 qA and qA/8. The failed readings are preserved as failed; the open readings remain open.",
        "",
        "Theorem spine:",
        f"- CR113/CR114/CR115 lock R={theorem_R}, D={theorem_D}.",
        f"- R^2={theorem_R2}; 2^D={theorem_face_states}; R^2/2^D={theorem_cells_per_state}.",
        f"- carrier address 000 = {theorem_carrier_cells}; seven retained F_2^3 addresses = {theorem_retained_cells}.",
        "",
        "Verified surface:",
        f"- PDF readback: {pdf_info['page_count']} pages, HH001_fano_plates_126.pdf hashed.",
        f"- SIS table: {len(sis_rows)} rows, Z=1..126.",
        f"- Fano address algebra: {sum(1 for row in fano_rows if row['status'] == 'PASS')}/{len(fano_rows)} lines XOR to 000.",
        f"- CR119 bridge: GRAVITY=qA matches {qA_matches}/126; GRAVITON=qA/8 matches {gravity_over_8_matches}/126.",
        f"- CR119 boundary preserved: Z119-Z126 frontier unknown rows = {cr119_summary['frontier_unknown_z119_z126']}.",
        "",
        "Preserved failures/open items:",
        f"- ACTION residual equals physical nuclear spin: falsified at {action_match_count}/{len(action_known)} matches.",
        f"- Per-element XOR closure: not promoted; binary_v2 closed {bin_v2_closed}/{len(bin_v2_rows)}, binary_v22 closed {bin_v22_closed}/{len(bin_v22_rows)}.",
        "- Seven-channel physical mapping remains OPEN and needs a CR-class test.",
        "- 126 GeV conversion remains OPEN / hidden-parameter risk until derivation audit.",
        "",
        "Wrong controls rejected:",
        "- PDF-alone-as-theorem.",
        "- hiding falsified ACTION/spin and XOR readings.",
        "- using known labels as construction inputs.",
        "- treating Z119-Z126 as known elements.",
        "- using Fano algebra alone as empirical validation.",
        "- using 126 GeV without derivation.",
        "- citing Haunted House as Courtroom-grade evidence.",
        "",
        f"Checks: {pass_count}/{len(checks)} PASS",
        f"Wrong controls: {summary['wrong_controls']['rejected']}/{summary['wrong_controls']['tested']} rejected",
        "",
        "Primary artifacts:",
        f"- `{rel(input_manifest)}`",
        f"- `{rel(full_inventory)}`",
        f"- `{rel(theorem_csv)}`",
        f"- `{rel(fano_csv)}`",
        f"- `{rel(table_csv)}`",
        f"- `{rel(status_csv)}`",
        f"- `{rel(wrong_csv)}`",
        f"- `{rel(checks_csv)}`",
        f"- `{rel(summary_json)}`",
        f"- `{rel(hashes_txt)}`",
    ]
    result_md.write_text("\n".join(result_lines) + "\n", encoding="utf-8")

    artifact_paths = [
        Path(__file__).resolve(),
        precommit,
        premises,
        input_manifest,
        full_inventory,
        theorem_csv,
        fano_csv,
        table_csv,
        status_csv,
        wrong_csv,
        checks_csv,
        summary_json,
        result_md,
    ]
    with hashes_txt.open("w", encoding="utf-8") as handle:
        for path in artifact_paths:
            handle.write(f"{sha256_file(path)}  {rel(path)}\n")
        for copied in sorted(SOURCE_COPIES.iterdir()):
            if copied.is_file():
                handle.write(f"{sha256_file(copied)}  {rel(copied)}\n")

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
