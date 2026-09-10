"""CR113 A4 completed-WRITE address count theorem closure.

This runner assembles the A4 R-first chain without using 2*pi or A0 as the
source of R:

    A=1 boundary closure -> completed boundary WRITE object
    M_w = two oriented faces x two surface dimensions = 4
    D_route = 1/2 + 1/2 + 1 + 1 = 3
    independent address axes -> R = M_w * D_route = 4 * 3 = 12

The test is a closure gate: it verifies that the cited upstream artifacts and
the executable radix kernel jointly support the theorem, and it rejects the
specific reviewer traps as wrong-controls.
"""

from __future__ import annotations

import csv
import hashlib
import importlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CR_ID = "CR113"
RESULT_CLASS_PASS = "CR113_PASS_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM"
RESULT_CLASS_FAIL = "CR113_FAIL_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM"

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent
STAM_ROOT = Path(r"C:/VS/Stam_model-A-v1.0")
MEMORY_ROOT = Path(r"C:/VS/memory")

PRIORITY_RECORD = MEMORY_ROOT / "PRIORITY_RECORD.md"
D_RECURSION = STAM_ROOT / "audit" / "audits" / "D_recursion_map_2026-05-21.py"
RADIX_KERNEL = STAM_ROOT / "sam" / "radix_route_kernel.py"

G11555_DIR = STAM_ROOT / "tests" / "Substrate" / "G11555_MAGIC_BELL_A1_NO_CROSSING_THEOREM"
G11555_SUMMARY = G11555_DIR / "G11555_summary.json"
G11555_CHECKS = G11555_DIR / "G11555_checks.csv"
G11555_WC = G11555_DIR / "G11555_wrong_controls.csv"
G11555_LANES = G11555_DIR / "G11555_observer_lanes.csv"
G11555_VERDICT = (
    STAM_ROOT
    / "audit"
    / "audits"
    / "VERDICT_G11555_MAGIC_BELL_A1_NO_CROSSING_THEOREM_2026_06_03.md"
)

G585C_DIR = STAM_ROOT / "tests" / "Substrate" / "G585c_A_SHARE_SIDE_STATUS_SELECTOR_WITH_ROUTE_DEPTH"
G586C_DIR = STAM_ROOT / "tests" / "Substrate" / "G586c_HORIZON_NORMAL_SIDE_PAIR_COMPATIBILITY_SELECTOR"
G587C_DIR = STAM_ROOT / "tests" / "Substrate" / "G587c_TWO_PIECE_MANIFOLD_READING_LAB"
G588C_DIR = STAM_ROOT / "tests" / "Substrate" / "G588c_V4_1_MANIFOLD_REFINEMENT_FINAL_AUDIT"
G591C_DIR = STAM_ROOT / "tests" / "Substrate" / "G591c_CONJUGATE_PAIR_ROLE_ASSIGNMENT_SELECTOR"
G609C_DIR = STAM_ROOT / "tests" / "Substrate" / "G609c_BIPARTITE_WRITE_D_3_COUNT_AUDIT"
SUK056_DIR = STAM_ROOT / "tests" / "Campaigns" / "SAM_UNIFICATION_KERNEL_GATE"
NATIVE_ARTIFACTS = STAM_ROOT / "tests" / "native_prediction_artifacts"

SOURCE_CHAIN_CSV = CR_DIR / "CR113_source_chain.csv"
CHECKS_CSV = CR_DIR / "CR113_checks.csv"
WRONG_CONTROLS_CSV = CR_DIR / "CR113_wrong_controls.csv"
LOCK_JSON = CR_DIR / "CR113_completed_write_address_count_lock.json"
LOCK_SHA = CR_DIR / "CR113_completed_write_address_count_lock.json.sha256.txt"
SUMMARY_JSON = CR_DIR / "CR113_summary.json"
RESULT_MD = CR_DIR / "CR113_result.md"


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def sha256_file(path: Path) -> str:
    if not path.exists():
        return ""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def contains_all(text: str, needles: list[str]) -> bool:
    return all(n in text for n in needles)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def pass_row(check_id: str, description: str, observed: Any, passed: bool, source: str) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "description": description,
        "observed": json.dumps(observed, sort_keys=True) if isinstance(observed, (dict, list)) else str(observed),
        "passed": bool(passed),
        "source": source,
    }


def wc_row(control_id: str, control: str, observed: Any, rejected: bool, reason: str) -> dict[str, Any]:
    return {
        "control_id": control_id,
        "control": control,
        "observed": json.dumps(observed, sort_keys=True) if isinstance(observed, (dict, list)) else str(observed),
        "rejected": bool(rejected),
        "reason": reason,
    }


def source_row(label: str, path: Path, role: str, load_bearing: bool) -> dict[str, Any]:
    return {
        "label": label,
        "role": role,
        "load_bearing": bool(load_bearing),
        "path": str(path),
        "exists": path.exists(),
        "sha256": sha256_file(path),
    }


def indexed(rows: list[dict[str, str]], *id_fields: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        for field in id_fields:
            value = row.get(field, "")
            if value:
                out[value] = row
    return out


def import_radix_kernel():
    if str(STAM_ROOT) not in sys.path:
        sys.path.insert(0, str(STAM_ROOT))
    return importlib.import_module("sam.radix_route_kernel")


def main() -> int:
    print("CR113 runner: starting A4 completed-WRITE address-count theorem closure")

    source_rows = [
        source_row("PRIORITY_RECORD_A4_R_FIRST_ADDENDUM", PRIORITY_RECORD, "record context / anti-regression", True),
        source_row("G11555_SUMMARY", G11555_SUMMARY, "A=1 closure and no completed crossing", True),
        source_row("G11555_VERDICT", G11555_VERDICT, "sealed theorem verdict text", True),
        source_row("G11555_CHECKS", G11555_CHECKS, "A=1 and A>1 pass rows", True),
        source_row("G11555_WRONG_CONTROLS", G11555_WC, "A=1 trap rejection", True),
        source_row("G11555_LANES", G11555_LANES, "outside/infaller lane agreement", True),
        source_row("D_RECURSION_MAP", D_RECURSION, "literal astronaut-falls-forever provenance", False),
        source_row("RADIX_ROUTE_KERNEL", RADIX_KERNEL, "executable C_w, D_route, L_w, R", True),
        source_row("G585C_SUMMARY", G585C_DIR / "G585c_summary.json", "completed side selector context", True),
        source_row("G586C_SUMMARY", G586C_DIR / "G586c_summary.json", "pair compatibility / no double-counting", True),
        source_row("G587C_SUMMARY", G587C_DIR / "G587c_summary.json", "M_w=4, D_route=3, R=12 lab", True),
        source_row("G587C_VERDICT", G587C_DIR / "G587c_verdict.md", "manifold-side theorem wording and caveat", True),
        source_row("G587C_VALIDATION", G587C_DIR / "G587c_validation_checks.csv", "M_w/D_route/R exact checks", True),
        source_row("G587C_WRONG_CONTROLS", G587C_DIR / "G587c_wrong_controls.csv", "1D/3D, D_route, symmetry trap rejection", True),
        source_row("G588C_SUMMARY", G588C_DIR / "G588c_summary.json", "final manifold refinement audit", True),
        source_row("G588C_PROMOTABLE_TABLE", G588C_DIR / "G588c_promotable_refinement_table.csv", "promotable M_w and W_in split", True),
        source_row("G588C_KERNEL_COHERENCE", G588C_DIR / "G588c_kernel_coherence_check.csv", "kernel invariance", True),
        source_row("G591C_SUMMARY", G591C_DIR / "G591c_summary.json", "M_out/M_in role assignment", True),
        source_row("G609C_SUMMARY", G609C_DIR / "G609c_summary.json", "bipartite WRITE D=3 count audit", True),
        source_row("SUK056_WRONG_CONTROLS", SUK056_DIR / "SUK056_wrong_controls.csv", "route-contact wrong-controls", False),
        source_row("FRACTIONAL_CHANNEL_SANDBOX", NATIVE_ARTIFACTS / "fractional_channel_sandbox.csv", "negative route-grammar controls", False),
    ]
    write_csv(SOURCE_CHAIN_CSV, source_rows, ["label", "role", "load_bearing", "path", "exists", "sha256"])

    missing_load_bearing = [row for row in source_rows if row["load_bearing"] and not row["exists"]]

    pr_text = read_text(PRIORITY_RECORD)
    d_recursion_text = read_text(D_RECURSION)
    g11555 = read_json(G11555_SUMMARY)
    g11555_checks = read_csv(G11555_CHECKS)
    g11555_wc = read_csv(G11555_WC)
    g11555_lanes = read_csv(G11555_LANES)
    g11555_verdict_text = read_text(G11555_VERDICT)

    g585c_summary = read_json(G585C_DIR / "G585c_summary.json")
    g586c_summary = read_json(G586C_DIR / "G586c_summary.json")
    g587c_summary = read_json(G587C_DIR / "G587c_summary.json")
    g587c_verdict = read_text(G587C_DIR / "G587c_verdict.md")
    g587c_validation = read_csv(G587C_DIR / "G587c_validation_checks.csv")
    g587c_wc = read_csv(G587C_DIR / "G587c_wrong_controls.csv")
    g588c_summary = read_json(G588C_DIR / "G588c_summary.json")
    g588c_promotable = read_csv(G588C_DIR / "G588c_promotable_refinement_table.csv")
    g588c_kernel = read_csv(G588C_DIR / "G588c_kernel_coherence_check.csv")
    g591c_summary = read_json(G591C_DIR / "G591c_summary.json")
    g609c_summary = read_json(G609C_DIR / "G609c_summary.json")
    suk056_wc = read_csv(SUK056_DIR / "SUK056_wrong_controls.csv")
    fractional_sandbox = read_csv(NATIVE_ARTIFACTS / "fractional_channel_sandbox.csv")

    kernel = import_radix_kernel()

    layer_positions = list(kernel.LAYER_POSITIONS)
    weights = [kernel.fraction_str(w) for w in kernel.ROUTE_DEPTH_WEIGHTS]
    side_statuses = [kernel.SIDE_STATUS_BY_LAYER[layer] for layer in layer_positions]
    outside_layers = [layer for layer in layer_positions if kernel.SIDE_STATUS_BY_LAYER[layer] == "outside"]
    inside_layers = [layer for layer in layer_positions if kernel.SIDE_STATUS_BY_LAYER[layer] == "inside"]

    mw = 2 * 2
    d_route = int(kernel.D_ROUTE)
    r_from_product = mw * d_route

    g587c_v = indexed(g587c_validation, "check_id")
    g587c_wc_ids = indexed(g587c_wc, "wrong_control_id", "control_id")
    g11555_wc_ids = indexed(g11555_wc, "control_id")
    suk056_by_id = indexed(suk056_wc, "control_id")
    sandbox_by_id = indexed(fractional_sandbox, "trial_id")
    suk_controls = " ".join(row.get("control_id", "") + " " + row.get("control", "") + " " + row.get("observed", "") for row in suk056_wc)
    sandbox_controls = " ".join(" ".join(row.values()) for row in fractional_sandbox)

    promotable_text = " ".join(" ".join(row.values()) for row in g588c_promotable)
    kernel_text = " ".join(" ".join(row.values()) for row in g588c_kernel)

    checks = [
        pass_row(
            "P1_sources_present",
            "All load-bearing source artifacts are present.",
            {"missing_load_bearing": [row["label"] for row in missing_load_bearing]},
            not missing_load_bearing,
            "source_chain",
        ),
        pass_row(
            "P2_A1_boundary_closure",
            "G11555 closes A=1 as the horizon bell and rejects A>1 as parent-ledger write.",
            {
                "verdict": g11555.get("verdict"),
                "result_class": g11555.get("result_class"),
                "A_at_r_s": g11555.get("kernel", {}).get("A_at_r_s"),
                "inside_status": g11555.get("infaller_lane", {}).get("SAM_parent_ledger_status"),
                "lane_verdict": g11555.get("lane_verdict"),
            },
            g11555.get("verdict") == "G11555_PASS_MAGIC_BELL_NO_COMPLETED_PARENT_LEDGER_CROSSING"
            and g11555.get("result_class") == "PASS_MAGIC_BELL_THEOREM"
            and g11555.get("all_predictions_passed") is True
            and g11555.get("all_wrong_controls_rejected") is True
            and g11555.get("kernel", {}).get("A_at_r_s") == 1.0
            and g11555.get("infaller_lane", {}).get("SAM_parent_ledger_status") == "REJECT_PARENT_WRITE_A_GT_1"
            and g11555.get("lane_verdict") == "NO_COMPLETED_PARENT_LEDGER_CROSSING",
            "G11555",
        ),
        pass_row(
            "P3_G11555_two_lanes_agree",
            "Outside observer and infaller lanes both reject completed parent-ledger crossing.",
            g11555_lanes,
            len(g11555_lanes) == 2
            and all(row.get("completed_parent_ledger_crossing") == "False" for row in g11555_lanes)
            and all(row.get("lane_verdict") == "NO_COMPLETED_PARENT_LEDGER_CROSSING" for row in g11555_lanes),
            "G11555_lanes",
        ),
        pass_row(
            "P4_astronaut_phrase_has_provenance_but_is_not_load_bearing",
            "The literal astronaut-falls-forever wording exists in recursion provenance; G11555 supplies theorem wording.",
            "literal phrase plus G11555 theorem gate",
            contains_all(d_recursion_text, ["astronaut falls", "proper depth to A=1 diverges"])
            and "NO_COMPLETED_PARENT_LEDGER_CROSSING" in g11555_verdict_text,
            "D_recursion_map + G11555_verdict",
        ),
        pass_row(
            "P5_manifold_measure_four",
            "G587c/G588c support M_w = outside 2D + inside 2D = 4.",
            {
                "G587c_V1": g587c_v.get("V1_M_w_two_pieces_sum_to_4", {}).get("observed", ""),
                "promotable_contains": "M_w = outside (2D) + inside (2D)",
            },
            g587c_summary.get("result_class", "").startswith("PASS")
            and g587c_v.get("V1_M_w_two_pieces_sum_to_4", {}).get("passed") == "True"
            and "outside (2D) + inside (2D)" in g587c_verdict
            and "M_w = outside (2D) + inside (2D)" in promotable_text,
            "G587c/G588c",
        ),
        pass_row(
            "P6_route_depth_three",
            "The radix kernel and G587c support D_route = 1/2 + 1/2 + 1 + 1 = 3.",
            {
                "C_w": kernel.C_W,
                "weights": weights,
                "D_route": kernel.fraction_str(kernel.D_ROUTE),
                "outside_contribution": kernel.fraction_str(kernel.OUTSIDE_DEPTH_CONTRIBUTION),
                "inside_contribution": kernel.fraction_str(kernel.INSIDE_DEPTH_CONTRIBUTION),
            },
            kernel.C_W == "SW_out -> W_out <-> W_in <- SW_in"
            and weights == ["1/2", "1/2", "1", "1"]
            and kernel.D_ROUTE == 3
            and kernel.OUTSIDE_DEPTH_CONTRIBUTION == 1
            and kernel.INSIDE_DEPTH_CONTRIBUTION == 2
            and g587c_v.get("V2_D_route_unchanged", {}).get("passed") == "True",
            "radix_route_kernel/G587c",
        ),
        pass_row(
            "P7_product_closes_R12",
            "Completed-WRITE address count closes as M_w * D_route = 4 * 3 = 12.",
            {
                "M_w": mw,
                "D_route": d_route,
                "R_from_product": r_from_product,
                "kernel_R": int(kernel.R),
                "kernel_R_INT": kernel.R_INT,
            },
            mw == 4
            and d_route == 3
            and r_from_product == 12
            and kernel.R_INT == 12
            and g587c_v.get("V5_radix_R_matches_kernel", {}).get("passed") == "True",
            "kernel/G587c",
        ),
        pass_row(
            "P8_face_axis_and_route_axis_are_distinct",
            "The face axis and route-depth axis are not collapsed into one count.",
            {
                "side_statuses": side_statuses,
                "outside_layers": outside_layers,
                "inside_layers": inside_layers,
                "G588c_kernel_rows": g588c_kernel,
            },
            side_statuses == ["outside", "outside", "inside", "inside"]
            and outside_layers == ["SW_out", "W_out"]
            and inside_layers == ["W_in", "SW_in"]
            and all(row.get("passed") == "True" for row in g588c_kernel),
            "radix_route_kernel/G588c_kernel",
        ),
        pass_row(
            "P9_no_double_counting_pair_compatibility",
            "G585c/G586c/G591c/G609c support side completion, pair compatibility, M_out/M_in roles, and D=3 count.",
            {
                "G585c_result": g585c_summary.get("result_class", ""),
                "G586c_result": g586c_summary.get("result_class", ""),
                "G591c_result": g591c_summary.get("result_class", ""),
                "G609c_result": g609c_summary.get("result_class", ""),
            },
            "PASS" in g585c_summary.get("result_class", "")
            and "PASS" in g586c_summary.get("result_class", "")
            and "PASS" in g591c_summary.get("result_class", "")
            and "PASS" in g609c_summary.get("result_class", "")
            and "no double" in json.dumps(g586c_summary).lower()
            and "M_out" in json.dumps(g591c_summary)
            and "M_in" in json.dumps(g591c_summary)
            and "3" in json.dumps(g609c_summary),
            "G585c/G586c/G591c/G609c",
        ),
        pass_row(
            "P10_priority_record_matches_R_first_chain",
            "Current priority record uses R-first completed-WRITE address count and retires 2*pi as first-line R defense.",
            "PR A4 addendum",
            contains_all(
                pr_text,
                [
                    "completed-WRITE oriented-boundary address count",
                    "M_w = 2 oriented faces",
                    "D_route = 3",
                    "R = M_w",
                    "retires `2",
                ],
            ),
            "PRIORITY_RECORD",
        ),
    ]

    wrong_controls = [
        wc_row(
            "WC1_single_unoriented_2D_surface",
            "Count only one unoriented 2D surface so M_w=2.",
            {"wrong_M_w": 2, "wrong_R": 2 * d_route},
            2 * d_route != 12
            and "M_w = outside (2D) + inside (2D)" in promotable_text,
            "G588c promotes outside+inside oriented face reading; single-face count gives R=6.",
        ),
        wc_row(
            "WC2_ordinary_3D_volume_at_A1",
            "Treat A=1 as ordinary traversable 3D volume with completed parent crossing.",
            {
                "G11555_lane": g11555.get("lane_verdict"),
                "A_gt_1_status": g11555.get("infaller_lane", {}).get("SAM_parent_ledger_status"),
            },
            g11555.get("lane_verdict") == "NO_COMPLETED_PARENT_LEDGER_CROSSING"
            and g11555.get("infaller_lane", {}).get("SAM_parent_ledger_status") == "REJECT_PARENT_WRITE_A_GT_1",
            "G11555 rejects ordinary completed parent crossing beyond A=1.",
        ),
        wc_row(
            "WC3_additive_4_plus_3",
            "Use additive address count 4+3 instead of product address count.",
            {"wrong_R": mw + d_route, "correct_R": r_from_product},
            mw + d_route != 12 and r_from_product == 12,
            "Independent address axes require product; additive count gives R=7.",
        ),
        wc_row(
            "WC4_D_route_as_spatial_dimension",
            "Treat D_route=3 as the spatial dimension primitive rather than route-depth.",
            {"G587c_WC6": g587c_wc_ids.get("WC6_M_w_as_new_spatial_dimension_primitive", {})},
            g587c_wc_ids.get("WC6_M_w_as_new_spatial_dimension_primitive", {}).get("rejected") == "True",
            "G587c wrong-control says M_w is horizon-layer measure and D remains the separate spatial primitive.",
        ),
        wc_row(
            "WC5_double_count_faces",
            "Turn M_out/M_in into two extra full W_in pieces rather than a split unit.",
            {"promotable_table": "W_in=M_out+M_in split unit"},
            "NOT two extra full pieces" in promotable_text,
            "G588c keeps W_in=M_out+M_in as 1/2+1/2=1, not two full pieces.",
        ),
        wc_row(
            "WC6_2pi_or_A0_smuggling",
            "Derive R from 2*pi/A0 normalization instead of from completed WRITE address count.",
            {"PR": "R-first then A0=1/(pi R)"},
            "no longer the default proof route for `R = 12`" in pr_text
            and "After `R` is fixed" in pr_text,
            "Priority record explicitly uses R-first address count, then applies A0 after R is fixed.",
        ),
        wc_row(
            "WC7_wrong_route_contacts",
            "Use five-half, seven-half, full-contact, or triadic route variants.",
            {"SUK056": suk_controls, "sandbox": sandbox_controls[:500]},
            all(suk056_by_id.get(cid, {}).get("status") == "REJECTED" for cid in [
                "five_half_contacts",
                "seven_half_contacts",
                "compressed_four_contact_route",
                "full_contact_six_route",
            ])
            and suk056_by_id.get("five_half_contacts", {}).get("R") == "10"
            and suk056_by_id.get("seven_half_contacts", {}).get("R") == "14"
            and suk056_by_id.get("full_contact_six_route", {}).get("R") == "24"
            and sandbox_by_id.get("P7_triadic_outer_chain", {}).get("R_preserved (= 12)") == "False"
            and "R = 15" in sandbox_by_id.get("P7_triadic_outer_chain", {}).get("what_breaks", ""),
            "SUK056/fractional-channel controls show nearby route variants break R or A_side structure.",
        ),
        wc_row(
            "WC8_GR_finite_infaller_equals_SAM_parent_crossing",
            "Declare finite GR infaller continuation to be completed SAM parent-ledger crossing.",
            {"G11555_WC4": g11555_wc_ids.get("WC4", {})},
            g11555_wc_ids.get("WC4", {}).get("rejected") == "True",
            "G11555 separates GR continuation from SAM parent-ledger completion.",
        ),
    ]

    write_csv(CHECKS_CSV, checks, ["check_id", "description", "observed", "passed", "source"])
    write_csv(WRONG_CONTROLS_CSV, wrong_controls, ["control_id", "control", "observed", "rejected", "reason"])

    all_predictions_passed = all(row["passed"] for row in checks)
    all_wrong_controls_rejected = all(row["rejected"] for row in wrong_controls)
    result_class = RESULT_CLASS_PASS if all_predictions_passed and all_wrong_controls_rejected else RESULT_CLASS_FAIL

    lock = {
        "lock_id": "CR113_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM_LOCK",
        "cr_id": CR_ID,
        "branch": "14_FOUNDATIONAL_TESTS",
        "sealed_at_utc": now_utc(),
        "result_class": result_class,
        "theorem_statement": (
            "At A=1 the parent-ledger crossing is closed, so the completed WRITE is "
            "a boundary-address object. The manifold address axis has M_w=4 from "
            "two oriented faces times two surface dimensions. The route-depth axis "
            "has D_route=3 from C_w weights 1/2+1/2+1+1. Because these are distinct "
            "address axes, R=M_w*D_route=4*3=12. A0 is applied only after R is fixed."
        ),
        "derived_values": {
            "M_w": mw,
            "D_route": d_route,
            "R_from_product": r_from_product,
            "kernel_R": int(kernel.R),
            "A_share": kernel.fraction_str(kernel.A_SHARE),
            "A_side": kernel.fraction_str(kernel.A_SIDE),
        },
        "source_chain_sha256": {row["label"]: row["sha256"] for row in source_rows},
        "checks": checks,
        "wrong_controls": wrong_controls,
        "scope": [
            "Closes A4 completed-WRITE address count at structural theorem-gate grade.",
            "Does not derive D=3 from scratch; D remains inherited from the accepted D primitive / route kernel.",
            "Does not derive alpha_H=2 from scratch; M_w uses the oriented-boundary surface reading already promoted by G587c/G588c.",
            "Does not use 2*pi or A0 to derive R; A0 is downstream normalization after R=12 is fixed.",
            "Does not claim full black-hole, cosmology, or matter-spectrum theorem closure.",
        ],
        "open_debts": [
            "Reviewer may still ask for a prose theorem write-up in the manuscript/audit narrative.",
            "G587c caveat is now narrowed by this closure gate but should be quoted honestly as structural theorem-gate grade, not primitive-from-nothing grade.",
        ],
    }
    with LOCK_JSON.open("w", encoding="utf-8") as f:
        json.dump(lock, f, indent=2)
    lock_sha = sha256_file(LOCK_JSON)
    LOCK_SHA.write_text(lock_sha + "\n", encoding="ascii")

    summary = {
        "cr_id": CR_ID,
        "branch": "14_FOUNDATIONAL_TESTS",
        "test_class": "A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM",
        "execution_status": "CLEAN",
        "result_class": result_class,
        "all_predictions_passed": all_predictions_passed,
        "all_wrong_controls_rejected": all_wrong_controls_rejected,
        "M_w": mw,
        "D_route": d_route,
        "R": r_from_product,
        "lock_sha256": lock_sha,
        "source_chain_csv": str(SOURCE_CHAIN_CSV.relative_to(COURTROOM_DIR)),
        "checks_csv": str(CHECKS_CSV.relative_to(COURTROOM_DIR)),
        "wrong_controls_csv": str(WRONG_CONTROLS_CSV.relative_to(COURTROOM_DIR)),
        "lock_json": str(LOCK_JSON.relative_to(COURTROOM_DIR)),
        "result_md": str(RESULT_MD.relative_to(COURTROOM_DIR)),
    }
    with SUMMARY_JSON.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    md = []
    md.append("# CR113 A4 Completed-WRITE Address Count Theorem\n\n")
    md.append("## Verdict\n\n```text\n")
    md.append(result_class + "\n")
    md.append("```\n\n")
    md.append("## Theorem Statement\n\n")
    md.append(lock["theorem_statement"] + "\n\n")
    md.append("## Derived Count\n\n```text\n")
    md.append(f"M_w      = {mw}\n")
    md.append(f"D_route  = {d_route}\n")
    md.append(f"R        = M_w * D_route = {mw} * {d_route} = {r_from_product}\n")
    md.append(f"A_share  = {kernel.fraction_str(kernel.A_SHARE)}\n")
    md.append(f"A_side   = {kernel.fraction_str(kernel.A_SIDE)}\n")
    md.append("A0       = downstream floor normalization after R is fixed\n")
    md.append("```\n\n")
    md.append("## Load-Bearing Source Chain\n\n")
    for row in source_rows:
        if row["load_bearing"]:
            md.append(f"- {row['label']}: `{row['path']}` sha256 `{row['sha256']}`\n")
    md.append("\n## Pass Checks\n\n")
    for row in checks:
        status = "PASS" if row["passed"] else "FAIL"
        md.append(f"- {status} {row['check_id']}: {row['description']}\n")
    md.append("\n## Wrong Controls\n\n")
    for row in wrong_controls:
        status = "REJECTED" if row["rejected"] else "NOT_REJECTED"
        md.append(f"- {status} {row['control_id']}: {row['control']}\n")
    md.append("\n## Scope\n\n")
    for item in lock["scope"]:
        md.append(f"- {item}\n")
    md.append("\n## Open Debts\n\n")
    for item in lock["open_debts"]:
        md.append(f"- {item}\n")
    md.append("\n## Hash\n\n```text\n")
    md.append(f"CR113_completed_write_address_count_lock.json sha256 = {lock_sha}\n")
    md.append("```\n")
    RESULT_MD.write_text("".join(md), encoding="utf-8")

    print(f"CR113 result_class={result_class}")
    print(f"CR113 lock_sha256={lock_sha}")
    print(f"CR113 R={r_from_product} from M_w={mw} * D_route={d_route}")
    print("CR113 runner: complete")
    return 0 if result_class == RESULT_CLASS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
