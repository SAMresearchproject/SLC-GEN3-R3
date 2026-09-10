from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any


TASK_ID = "LC11"
TASK_NAME = "black-hole horizon thermodynamic replay"
RESULT_CLASS = "LC11_PASS_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY_FROM_LOCKED_PRIMITIVE_STACK"

ROOT = Path(__file__).resolve().parents[1]
LC_DIR = ROOT / "16_THE_LAST_CAMPAIGN"
OUT_DIR = LC_DIR / "LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RUNNER_PATH = Path(__file__).resolve()

STAM_ROOT = Path(r"C:\VS\Stam_model-A-v1.0")
BRANCH02 = ROOT / "02_A_KERNEL_WEAK_FIELD"
BRANCH04 = ROOT / "04_PHOTON_ROAD_SHAPIRO_DELAY"
BRANCH05 = ROOT / "05_STRONG_FIELD_AND_HORIZON_CLOSURE"
BRANCH11 = ROOT / "11_QUANTUM_MECHANICS_AND_GRAVITY"
FOUNDATION = ROOT / "14_FOUNDATIONAL_TESTS"

LC01_PRIMITIVE_CSV = LC_DIR / "LC01_primitive_stack_declared.csv"

SOURCES = {
    "LC01": LC_DIR / "LC01_primitive_stack_lock.json",
    "CR003": BRANCH02 / "CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION" / "CR003_summary.json",
    "CR103a": FOUNDATION / "CR103a_BOUNCE_COST_AND_A_DEPENDENCE_APPEAL" / "CR103a_summary.json",
    "CR103a_lock": FOUNDATION / "CR103a_BOUNCE_COST_AND_A_DEPENDENCE_APPEAL" / "CR103a_appeal_lock.json",
    "CR113": FOUNDATION / "CR113_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM" / "CR113_summary.json",
    "CR113_lock": FOUNDATION / "CR113_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM" / "CR113_completed_write_address_count_lock.json",
    "CR116": FOUNDATION / "CR116_18_GRAVITON_CARRIER_THEOREM" / "CR116_summary.json",
    "CR147": BRANCH04 / "CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL" / "CR147_summary.json",
    "branch05_readme": BRANCH05 / "README.md",
    "branch05_seal": BRANCH05 / "SEALED_STRONG_FIELD_SCOPE_APPROACH_2026_06_11.md",
    "CR007": BRANCH05 / "CR007_STRONG_FIELD_LANDMARK_SELECTOR" / "CR007_summary.json",
    "CR008": BRANCH05 / "CR008_CLOCK_TRAVERSAL_CLOSURE" / "CR008_summary.json",
    "CR009": BRANCH05 / "CR009_PHOTON_SPHERE_SHADOW_CONTACT" / "CR009_summary.json",
    "CR010": BRANCH05 / "CR010_ISCO_ORBITAL_CONTACT" / "CR010_summary.json",
    "CR011": BRANCH05 / "CR011_DEFERRED_SUPPORT_ZIPPER" / "CR011_summary.json",
    "CR073": BRANCH11 / "CR073_ACTION_PHASE_ANCHOR" / "CR073_summary.json",
    "CR073_manifest": BRANCH11 / "CR073_ACTION_PHASE_ANCHOR" / "CR073_input_manifest.csv",
    "CR074": BRANCH11 / "CR074_DOUBLE_SLIT_BORN_ROUTE" / "CR074_summary.json",
    "CR075": BRANCH11 / "CR075_UNRESOLVED_PATH_AND_LEDGER_WRITE" / "CR075_summary.json",
    "CR076": BRANCH11 / "CR076_PHASE_INTEGRAL_A_EXPOSURE" / "CR076_summary.json",
    "G11555": STAM_ROOT / "tests" / "Substrate" / "G11555_MAGIC_BELL_A1_NO_CROSSING_THEOREM" / "G11555_summary.json",
    "QGA024": STAM_ROOT / "tests" / "Substrate" / "QGA024_ETA_HBAR_OR_CONTINUUM_STRESS_ANCHOR" / "QGA024_summary.json",
    "QGA025": STAM_ROOT / "tests" / "Substrate" / "QGA025_HAWKING_RADIATION_THERMAL_BRIDGE_AUDIT" / "QGA025_summary.json",
    "QGA026": STAM_ROOT / "tests" / "Substrate" / "QGA026_HAWKING_GREYBODY_SPECIES_KERR_ROUTE_AUDIT" / "QGA026_summary.json",
    "SUK060": STAM_ROOT / "tests" / "Campaigns" / "SAM_UNIFICATION_KERNEL_GATE" / "SUK060_summary.json",
    "SUK061": STAM_ROOT / "tests" / "Campaigns" / "SAM_UNIFICATION_KERNEL_GATE" / "SUK061_summary.json",
    "XBS006": STAM_ROOT / "tests" / "Campaigns" / "TYPED_STABILITY_CROSS_BRANCH_SELECTOR_TRANSFER_CAMPAIGN" / "XBS006_summary.json",
}

ROWS = {
    "CR007_candidate_rows": BRANCH05 / "CR007_STRONG_FIELD_LANDMARK_SELECTOR" / "CR007_candidate_rows.csv",
    "CR008_candidate_summary": BRANCH05 / "CR008_CLOCK_TRAVERSAL_CLOSURE" / "CR008_candidate_summary.csv",
    "CR008_near_horizon_rows": BRANCH05 / "CR008_CLOCK_TRAVERSAL_CLOSURE" / "CR008_near_horizon_rows.csv",
    "CR009_candidate_rows": BRANCH05 / "CR009_PHOTON_SPHERE_SHADOW_CONTACT" / "CR009_candidate_rows.csv",
    "CR010_candidate_rows": BRANCH05 / "CR010_ISCO_ORBITAL_CONTACT" / "CR010_candidate_rows.csv",
    "CR011_dependency_rows": BRANCH05 / "CR011_DEFERRED_SUPPORT_ZIPPER" / "CR011_dependency_rows.csv",
    "CR011_appeal_rows": BRANCH05 / "CR011_DEFERRED_SUPPORT_ZIPPER" / "CR011_appeal_rows.csv",
    "CR147_checks": BRANCH04 / "CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL" / "CR147_checks.csv",
    "CR147_wrong_controls": BRANCH04 / "CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL" / "CR147_wrong_controls.csv",
    "G11555_checks": STAM_ROOT / "tests" / "Substrate" / "G11555_MAGIC_BELL_A1_NO_CROSSING_THEOREM" / "G11555_checks.csv",
    "G11555_wrong_controls": STAM_ROOT / "tests" / "Substrate" / "G11555_MAGIC_BELL_A1_NO_CROSSING_THEOREM" / "G11555_wrong_controls.csv",
    "QGA024_checks": STAM_ROOT / "tests" / "Substrate" / "QGA024_ETA_HBAR_OR_CONTINUUM_STRESS_ANCHOR" / "QGA024_checks.csv",
    "QGA025_checks": STAM_ROOT / "tests" / "Substrate" / "QGA025_HAWKING_RADIATION_THERMAL_BRIDGE_AUDIT" / "QGA025_checks.csv",
    "QGA025_thermal_rows": STAM_ROOT / "tests" / "Substrate" / "QGA025_HAWKING_RADIATION_THERMAL_BRIDGE_AUDIT" / "QGA025_thermal_rows.csv",
    "QGA025_gap_register": STAM_ROOT / "tests" / "Substrate" / "QGA025_HAWKING_RADIATION_THERMAL_BRIDGE_AUDIT" / "QGA025_gap_register.csv",
    "QGA026_checks": STAM_ROOT / "tests" / "Substrate" / "QGA026_HAWKING_GREYBODY_SPECIES_KERR_ROUTE_AUDIT" / "QGA026_checks.csv",
    "QGA026_kerr_rows": STAM_ROOT / "tests" / "Substrate" / "QGA026_HAWKING_GREYBODY_SPECIES_KERR_ROUTE_AUDIT" / "QGA026_kerr_rows.csv",
    "QGA026_gap_register": STAM_ROOT / "tests" / "Substrate" / "QGA026_HAWKING_GREYBODY_SPECIES_KERR_ROUTE_AUDIT" / "QGA026_gap_register.csv",
    "SUK060_invariants": STAM_ROOT / "tests" / "Campaigns" / "SAM_UNIFICATION_KERNEL_GATE" / "SUK060_invariants.csv",
    "SUK060_wrong_controls": STAM_ROOT / "tests" / "Campaigns" / "SAM_UNIFICATION_KERNEL_GATE" / "SUK060_wrong_controls.csv",
    "SUK061_invariants": STAM_ROOT / "tests" / "Campaigns" / "SAM_UNIFICATION_KERNEL_GATE" / "SUK061_invariants.csv",
    "SUK061_wrong_controls": STAM_ROOT / "tests" / "Campaigns" / "SAM_UNIFICATION_KERNEL_GATE" / "SUK061_wrong_controls.csv",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8") as handle:
        return handle.read()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def source_status(summary: dict[str, Any]) -> str:
    for key in ("result", "result_class", "verdict", "scientific_verdict", "status", "artifact"):
        value = summary.get(key)
        if isinstance(value, str) and value:
            return value
    return "UNKNOWN"


def contains_success(summary: dict[str, Any]) -> bool:
    status = source_status(summary).upper()
    if "REFUTED" in status or "FAIL" in status:
        return False
    if any(token in status for token in ("PASS", "BUILT", "SELECTED", "SEALED", "LOCKED", "BOUNDARY")):
        return True
    if summary.get("execution_status") == "CLEAN" and status != "UNKNOWN":
        return True
    return bool(summary.get("all_predictions_passed") is True)


def check(name: str, passed: bool, detail: str, value: Any = "") -> dict[str, Any]:
    return {
        "check": name,
        "status": "PASS" if passed else "FAIL",
        "value": value,
        "detail": detail,
    }


def close(left: float, right: float, tolerance: float = 1e-12) -> bool:
    return abs(left - right) <= tolerance


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in ("true", "pass", "passed", "1", "yes")


def load_primitive_stack(path: Path) -> dict[str, Any]:
    rows: dict[str, dict[str, str]] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            rows[row["primitive"]] = row

    def exact(name: str) -> str:
        return rows[name]["value_exact"]

    def decimal(name: str) -> str:
        return rows[name]["value_decimal"]

    return {
        "alpha_H": int(exact("alpha_H")),
        "R": int(exact("R")),
        "D": int(exact("D")),
        "A0": exact("A0"),
        "A0_decimal": decimal("A0"),
        "R_squared": int(exact("R^2")),
        "split_fraction": exact("split_fraction"),
        "split_fraction_decimal": decimal("split_fraction"),
        "retained_side": exact("retained_side"),
        "retained_side_decimal": decimal("retained_side"),
        "carrier_side": exact("carrier_side"),
        "carrier_side_decimal": decimal("carrier_side"),
        "bounce_lift": exact("bounce_lift"),
        "bounce_lift_decimal": decimal("bounce_lift"),
        "resolved_half_bounce": exact("resolved_half_bounce"),
        "resolved_half_bounce_decimal": decimal("resolved_half_bounce"),
        "surface_debit": exact("surface_debit"),
        "surface_debit_decimal": decimal("surface_debit"),
    }


def qga_counts_from_checks(rows: list[dict[str, str]]) -> tuple[int, int, int, int]:
    prediction_rows = [row for row in rows if row.get("kind") == "prediction"]
    wrong_rows = [row for row in rows if row.get("kind") == "wrong_control"]
    prediction_passes = sum(1 for row in prediction_rows if parse_bool(row.get("pass")))
    wrong_passes = sum(1 for row in wrong_rows if parse_bool(row.get("pass")))
    return prediction_passes, len(prediction_rows), wrong_passes, len(wrong_rows)


def all_rows_true(rows: list[dict[str, str]], field: str) -> bool:
    return bool(rows) and all(parse_bool(row.get(field)) for row in rows)


def all_status(rows: list[dict[str, str]], expected: str) -> bool:
    return bool(rows) and all(str(row.get("status", "")).upper() == expected.upper() for row in rows)


def main() -> int:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    primitive_stack = load_primitive_stack(LC01_PRIMITIVE_CSV)
    summaries = {name: load_json(path) for name, path in SOURCES.items() if path.suffix.lower() == ".json"}
    texts = {name: read_text(path) for name, path in SOURCES.items() if path.suffix.lower() == ".md"}
    row_sets = {name: read_csv(path) for name, path in ROWS.items()}

    alpha_h = primitive_stack["alpha_H"]
    R = primitive_stack["R"]
    D = primitive_stack["D"]
    A0 = Fraction(1, R) / Fraction(math.pi).limit_denominator(10**15)
    split_fraction = Fraction(primitive_stack["split_fraction"])
    retained_side = Fraction(primitive_stack["retained_side"])
    carrier_side = Fraction(primitive_stack["carrier_side"])
    surface_debit = Fraction(primitive_stack["surface_debit"])
    bounce_lift = Fraction(primitive_stack["bounce_lift"])
    resolved_half_bounce = Fraction(primitive_stack["resolved_half_bounce"])

    A_share = Fraction(1, R)
    A_side = Fraction(1, 2 * R)
    max_loading = Fraction(R - 1, R)
    completion = Fraction(R, R)
    split_loss_native = R * R * split_fraction

    horizon_landmarks = [
        {"landmark": "horizon", "x_r_over_rs": Fraction(1, 1), "expected_A": Fraction(1, 1)},
        {"landmark": "photon_sphere", "x_r_over_rs": Fraction(3, 2), "expected_A": Fraction(2, 3)},
        {"landmark": "isco", "x_r_over_rs": Fraction(3, 1), "expected_A": Fraction(1, 3)},
    ]

    cr007_by_landmark = {row["landmark"]: row for row in summaries["CR007"]["sam_rows"]}
    landmark_rows: list[dict[str, Any]] = []
    for item in horizon_landmarks:
        source_row = cr007_by_landmark[item["landmark"]]
        expected_A = float(item["expected_A"])
        expected_x = float(item["x_r_over_rs"])
        source_A = float(source_row["candidate_A"])
        source_x = float(source_row["r_over_rs"])
        landmark_rows.append(
            {
                "landmark": item["landmark"],
                "formula": "A = r_s / r = 1 / x",
                "expected_x": str(item["x_r_over_rs"]),
                "source_x": source_x,
                "expected_A": str(item["expected_A"]),
                "source_A": source_A,
                "status": "PASS" if close(source_A, expected_A) and close(source_x, expected_x) else "FAIL",
            }
        )

    cr008 = summaries["CR008"]["sam_summary"]
    cr009 = summaries["CR009"]["sam_row"]
    cr010 = summaries["CR010"]["sam_row"]
    cr147 = summaries["CR147"]
    qga025 = summaries["QGA025"]
    qga026 = summaries["QGA026"]
    suk060 = summaries["SUK060"]
    suk061 = summaries["SUK061"]
    g11555 = summaries["G11555"]

    qga025_counts = qga_counts_from_checks(row_sets["QGA025_checks"])
    qga026_counts = qga_counts_from_checks(row_sets["QGA026_checks"])

    branch05_layers = [
        {
            "layer": "CR007 landmark root",
            "source": "CR007",
            "contract": "A(r)=r_s/r places horizon, photon sphere, and ISCO at A=1,2/3,1/3",
            "source_value": source_status(summaries["CR007"]),
            "status": "PASS" if all(row["status"] == "PASS" for row in landmark_rows) and summaries["CR007"]["structural_success"] is True else "FAIL",
            "boundary": "original BOUNDARY grade preserved until CR011 appeal row",
        },
        {
            "layer": "CR008 A=1 closure",
            "source": "CR008",
            "contract": "lapse -> 0, redshift and outside traversal diverge as A -> 1",
            "source_value": source_status(summaries["CR008"]),
            "status": "PASS" if cr008["lapse_goes_to_zero_as_A_to_1"] and cr008["redshift_diverges_as_A_to_1"] and cr008["outside_traversal_log_diverges"] else "FAIL",
            "boundary": "outside-ledger clock/traversal closure only",
        },
        {
            "layer": "CR009 photon sphere / shadow",
            "source": "CR009",
            "contract": "A=2/3 carries b_crit/r_s=3*sqrt(3)/2 and shadow diameter/r_s=3*sqrt(3)",
            "source_value": source_status(summaries["CR009"]),
            "status": "PASS" if close(cr009["A_photon"], 2 / 3) and close(cr009["bcrit_over_rs"], 3 * math.sqrt(3) / 2) and close(cr009["shadow_diameter_over_rs"], 3 * math.sqrt(3)) else "FAIL",
            "boundary": "no full EHT or Kerr modeling",
        },
        {
            "layer": "CR010 ISCO",
            "source": "CR010",
            "contract": "A=1/3 carries Schwarzschild ISCO invariants",
            "source_value": source_status(summaries["CR010"]),
            "status": "PASS" if close(cr010["A_isco"], 1 / 3) and close(cr010["energy_over_c2"], math.sqrt(8 / 9)) and close(cr010["angular_momentum_over_m_c_rs"], math.sqrt(3)) and close(cr010["omega_rs_over_c"], 1 / math.sqrt(54)) else "FAIL",
            "boundary": "scoped orbital contact only",
        },
        {
            "layer": "CR011 appeal zipper",
            "source": "CR011",
            "contract": "append appeal PASS readouts without overwriting CR007/CR008 original boundary grades",
            "source_value": source_status(summaries["CR011"]),
            "status": "PASS" if source_status(summaries["CR011"]).startswith("CR011_PASS") and all_rows_true(row_sets["CR011_appeal_rows"], "original_grade_preserved") else "FAIL",
            "boundary": "deferred-support ledger step, not new physics test",
        },
    ]

    thermodynamic_layers = [
        {
            "layer": "G11555 A=1 no-crossing theorem",
            "source": "G11555",
            "contract": "A=1 is the magic-bell closure; A>1 rejects parent-ledger write",
            "source_value": source_status(g11555),
            "status": "PASS" if g11555["all_predictions_passed"] and g11555["all_wrong_controls_rejected"] and g11555["lane_verdict"] == "NO_COMPLETED_PARENT_LEDGER_CROSSING" else "FAIL",
            "boundary": "GR finite infaller continuation is not SAM parent-ledger crossing",
        },
        {
            "layer": "QGA024 phase/stress anchor",
            "source": "QGA024",
            "contract": "phase/stress skeleton passes; eta/hbar and full continuum law stay separate",
            "source_value": source_status(summaries["QGA024"]),
            "status": "PASS" if summaries["QGA024"]["prediction_passes"] == summaries["QGA024"]["prediction_total"] and summaries["QGA024"]["wrong_control_passes"] == summaries["QGA024"]["wrong_control_total"] else "FAIL",
            "boundary": summaries["QGA024"]["scope"],
        },
        {
            "layer": "QGA025 scoped thermal bridge",
            "source": "QGA025",
            "contract": "Hawking T, BH entropy, first-law/Smarr, and proxy scaling pass",
            "source_value": source_status(qga025),
            "status": "PASS" if qga025_counts == (12, 12, 8, 8) and qga025["thermal_bridge"] == "PASS" and qga025["spectrum_greybody_species"] == "OPEN" else "FAIL",
            "boundary": qga025["scope"],
        },
        {
            "layer": "QGA026 Kerr/greybody route split",
            "source": "QGA026",
            "contract": "Kerr uniform-temperature route passes; greybody/species/rate/spectrum remain open",
            "source_value": source_status(qga026),
            "status": "PASS" if qga026_counts == (12, 12, 8, 8) and qga026["kerr_thermal_route"] == "PASS_UNIFORM_T_KERR" and qga026["species_branching"].startswith("OPEN") else "FAIL",
            "boundary": qga026["scope"],
        },
        {
            "layer": "SUK060 HR backreaction inventory",
            "source": "SUK060",
            "contract": "HR exhaust decreases parent horizon inventory and contributes zero child-ledger HR energy",
            "source_value": source_status(suk060),
            "status": "PASS" if suk060["invariants_passed"] == suk060["invariants_total"] and suk060["wrong_controls_rejected"] == suk060["wrong_controls_total"] and suk060["child_ledger_HR_share"] == "0" else "FAIL",
            "boundary": "parent-boundary backreaction, not child-ledger energy",
        },
        {
            "layer": "SUK061 horizon-bounded ledger cell",
            "source": "SUK061",
            "contract": "outside HR exhaust and inside write import balance across one shared boundary",
            "source_value": source_status(suk061),
            "status": "PASS" if suk061["invariants_passed"] == suk061["invariants_total"] and suk061["wrong_controls_rejected"] == suk061["wrong_controls_total"] and suk061["net_cell_boundary_balance_1Msun_W"] == "0.000000000000e+00" else "FAIL",
            "boundary": "ledger-cell frame first; absolute universe language not required",
        },
    ]

    formula_manifest = [
        {
            "formula_or_rule": "A horizon kernel",
            "expression": "A(r)=r_s/r",
            "locked_inputs": "r_s normalized as branch-05/CR003 A-kernel",
            "replayed_value": "A(1 r_s)=1; A(3r_s/2)=2/3; A(3r_s)=1/3",
            "source_or_target_use": "CR007-CR010 landmark lane",
        },
        {
            "formula_or_rule": "A=1 completion",
            "expression": "12/12 = 1",
            "locked_inputs": f"R={R}",
            "replayed_value": str(completion),
            "source_or_target_use": "horizon closure / no literal photon launch",
        },
        {
            "formula_or_rule": "maximum loading",
            "expression": "(R-1)/R",
            "locked_inputs": f"R={R}",
            "replayed_value": str(max_loading),
            "source_or_target_use": "CR103a / BB005 11/12 maximum loading boundary",
        },
        {
            "formula_or_rule": "surface debit",
            "expression": "D^2/R",
            "locked_inputs": f"D={D}; R={R}",
            "replayed_value": str(surface_debit),
            "source_or_target_use": "strong A boundary inherited from locked primitive stack",
        },
        {
            "formula_or_rule": "split loss / carrier side",
            "expression": "R^2 * 2^-D",
            "locked_inputs": f"R={R}; D={D}",
            "replayed_value": str(split_loss_native),
            "source_or_target_use": "18 carrier / tensor split support",
        },
        {
            "formula_or_rule": "bounce lift",
            "expression": "D^2/2^D",
            "locked_inputs": f"D={D}",
            "replayed_value": str(bounce_lift),
            "source_or_target_use": "locked primitive stack",
        },
        {
            "formula_or_rule": "resolved half-bounce",
            "expression": "D^2/2^(D+1)",
            "locked_inputs": f"D={D}",
            "replayed_value": str(resolved_half_bounce),
            "source_or_target_use": "locked primitive stack",
        },
        {
            "formula_or_rule": "Hawking temperature bridge",
            "expression": "T_SAM/T_Hawking",
            "locked_inputs": "QGA025 eta=hbar scoped bridge",
            "replayed_value": f"max ratio error {qga025['max_temperature_ratio_error']}",
            "source_or_target_use": "scoped thermal bridge; eta anchor preserved",
        },
        {
            "formula_or_rule": "Kerr uniform-temperature route",
            "expression": "T_committed/T_Kerr",
            "locked_inputs": "QGA026 committed Kerr route",
            "replayed_value": f"max ratio error {qga026['max_kerr_temperature_ratio_error']}",
            "source_or_target_use": "uniform T route; full spectrum open",
        },
        {
            "formula_or_rule": "GW170817 release boundary",
            "expression": "exact A=1 no escape; release at A_release",
            "locked_inputs": "CR147 dynamic A-release engine",
            "replayed_value": f"A_release={cr147['A_release']}; residual_sigma={cr147['residual_sigma']}",
            "source_or_target_use": "A=1 not literal light launch; post-release shared road",
        },
    ]

    boundary_rows = [
        {"boundary": "full strong-field metric", "status": "OPEN", "text": "Branch 05 explicitly does not claim a full strong-field metric."},
        {"boundary": "full Kerr solution/modeling", "status": "OPEN", "text": "CR009/CR010 are Schwarzschild-like scoped contacts; QGA026 preserves only the uniform-temperature Kerr route."},
        {"boundary": "full EHT modeling", "status": "OPEN", "text": "CR009 rejects EHT-image overclaim and preserves photon-sphere/shadow invariant scope."},
        {"boundary": "full QNM/ringdown prediction", "status": "OPEN", "text": "The branch-05 seal keeps QNM/ringdown separate."},
        {"boundary": "full Hawking spectrum", "status": "OPEN", "text": "QGA025/QGA026 keep greybody factors, species branching, exact rate inventory, full Kerr spectrum, correlations, and endpoint open."},
        {"boundary": "A=1 literal photon launch", "status": "REJECTED", "text": "CR147 and G11555 preserve A=1 as no-escape / zero-depth / no completed parent-ledger crossing."},
        {"boundary": "11/12 functional law", "status": "PROVISIONAL", "text": "CR103a locks monotonic A-dependence and the 11/12 threshold, while the exact r_bounce(A) and K(A_H) functional forms remain open."},
        {"boundary": "child-ledger HR energy", "status": "REJECTED", "text": "SUK060/SUK061 route HR exhaust as parent-boundary inventory drift and balanced ledger-cell activity, not child-ledger HR energy."},
    ]

    wrong_controls = [
        {
            "wrong_control": "WC29_soften_A1",
            "attempted_mutation": "Allow A=1 to behave as ordinary traversable space or literal photon launch",
            "evidence": f"G11555={g11555['lane_verdict']}; CR147={cr147['A1_exact_status']}",
            "result": "REJECTED" if g11555["lane_verdict"] == "NO_COMPLETED_PARENT_LEDGER_CROSSING" and "NO_ESCAPE" in cr147["A1_exact_status"] else "FAIL",
        },
        {
            "wrong_control": "WC30_horizon_only_fit",
            "attempted_mutation": "Keep A=1 but lose photon sphere or ISCO contact",
            "evidence": f"CR009 wrong controls={summaries['CR009']['wrong_control_full_packet_count']}; CR010 wrong controls={summaries['CR010']['wrong_control_full_packet_count']}",
            "result": "REJECTED" if summaries["CR009"]["wrong_control_full_packet_count"] == 0 and summaries["CR010"]["wrong_control_full_packet_count"] == 0 else "FAIL",
        },
        {
            "wrong_control": "WC31_overpromote_full_thermodynamics",
            "attempted_mutation": "Turn QGA025/QGA026 scoped bridge into full Hawking spectrum/species/rate theorem",
            "evidence": f"QGA025 gaps={len(row_sets['QGA025_gap_register'])}; QGA026 gaps={len(row_sets['QGA026_gap_register'])}",
            "result": "REJECTED" if all(row["status"] == "OPEN" for row in row_sets["QGA025_gap_register"]) and all(row["status"] == "OPEN" for row in row_sets["QGA026_gap_register"]) else "FAIL",
        },
        {
            "wrong_control": "WC32_static_A_integral_delay",
            "attempted_mutation": "Explain GW170817 seconds-scale lag with a static local A integral",
            "evidence": cr147["formal_static_A_integral_status"],
            "result": "REJECTED" if cr147["formal_static_A_integral_status"].startswith("REJECTED") else "FAIL",
        },
        {
            "wrong_control": "WC33_18_as_matter_or_rest_mass",
            "attempted_mutation": "Treat 18 as matter/rest mass rather than massless tensor carrier",
            "evidence": f"CR116={summaries['CR116']['particle_catalog_status']}; CR147={cr147['m18_carrier_status']}",
            "result": "REJECTED" if summaries["CR116"]["particle_catalog_status"] == "carrier_only_not_matter" and "MASSLESS" in cr147["m18_carrier_status"] else "FAIL",
        },
        {
            "wrong_control": "WC34_put_HR_into_child_ledger",
            "attempted_mutation": "Route Hawking radiation backreaction as child-ledger energy",
            "evidence": f"SUK060 child_ledger_HR_share={suk060['child_ledger_HR_share']}; SUK061 inside_HR_share={suk061['inside_HR_share']}",
            "result": "REJECTED" if suk060["child_ledger_HR_share"] == "0" and suk061["inside_HR_share"] == "0" else "FAIL",
        },
        {
            "wrong_control": "WC35_overwrite_boundary_grades",
            "attempted_mutation": "Erase CR007/CR008 original BOUNDARY grades after downstream support",
            "evidence": "CR011 appeal rows preserve original_grade_preserved",
            "result": "REJECTED" if all_rows_true(row_sets["CR011_appeal_rows"], "original_grade_preserved") else "FAIL",
        },
        {
            "wrong_control": "WC36_use_A0_as_horizon_bell",
            "attempted_mutation": "Use A0 or radix floor as the horizon bell instead of A=1",
            "evidence": "G11555 WC5 rejects A0/radix count as horizon bell",
            "result": "REJECTED" if any(row.get("control_id") == "WC5" and parse_bool(row.get("rejected")) for row in row_sets["G11555_wrong_controls"]) else "FAIL",
        },
    ]

    checks: list[dict[str, Any]] = []
    for name, path in SOURCES.items():
        checks.append(check(f"{name} source exists", path.exists(), rel(path), path.exists()))
    for name, path in ROWS.items():
        checks.append(check(f"{name} row source exists", path.exists(), rel(path), path.exists()))

    checks.extend(
        [
            check("R locked at 12", R == 12, "LC01 primitive", R),
            check("D locked at 3", D == 3, "LC01 primitive", D),
            check("alpha_H locked at 2", alpha_h == 2, "LC01 primitive", alpha_h),
            check("split fraction locked at 1/8", split_fraction == Fraction(1, 8), "LC01 primitive", str(split_fraction)),
            check("retained side locked at 7/8", retained_side == Fraction(7, 8), "LC01 primitive", str(retained_side)),
            check("carrier side locked at 1/8", carrier_side == Fraction(1, 8), "LC01 primitive", str(carrier_side)),
            check("surface debit locked at 3/4", surface_debit == Fraction(3, 4), "LC01 primitive", str(surface_debit)),
            check("bounce lift locked at 9/8", bounce_lift == Fraction(9, 8), "LC01 primitive", str(bounce_lift)),
            check("resolved half-bounce locked at 9/16", resolved_half_bounce == Fraction(9, 16), "LC01 primitive", str(resolved_half_bounce)),
            check("A_share recomputes to 1/12", A_share == Fraction(1, 12), "R-derived", str(A_share)),
            check("A_side recomputes to 1/24", A_side == Fraction(1, 24), "R-derived", str(A_side)),
            check("11/12 maximum loading recomputes", max_loading == Fraction(11, 12), "R-derived", str(max_loading)),
            check("12/12 completion recomputes to A=1", completion == 1, "R-derived", str(completion)),
            check("split loss native equals 18", split_loss_native == 18, "R^2 * 2^-D", str(split_loss_native)),
        ]
    )

    for row in landmark_rows:
        checks.append(check(f"CR007 {row['landmark']} landmark replay", row["status"] == "PASS", row["formula"], row["source_A"]))
    for row in branch05_layers:
        checks.append(check(f"{row['layer']} layer replay", row["status"] == "PASS", row["contract"], row["source_value"]))
    for row in thermodynamic_layers:
        checks.append(check(f"{row['layer']} layer replay", row["status"] == "PASS", row["contract"], row["source_value"]))

    checks.extend(
        [
            check("CR103a 11/12 threshold present", "11/12" in json.dumps(summaries["CR103a_lock"]), "CR103a appeal lock", "11/12"),
            check("CR103a functional-form debt preserved", any("Functional form of r_bounce(A)" in debt for debt in summaries["CR103a"]["open_debts"]), "CR103a open debts", "preserved"),
            check("CR113 R theorem passes", summaries["CR113"]["result_class"] == "CR113_PASS_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM", "CR113", source_status(summaries["CR113"])),
            check("CR113 uses R-first not A0 smuggling", "A0 is applied only after R is fixed" in summaries["CR113_lock"]["theorem_statement"], "CR113 theorem statement", "R-first"),
            check("CR116 18 carrier theorem passes", summaries["CR116"]["all_predictions_passed"] and summaries["CR116"]["all_wrong_controls_rejected"], "CR116", source_status(summaries["CR116"])),
            check("CR116 keeps 18 carrier-only", summaries["CR116"]["particle_catalog_status"] == "carrier_only_not_matter", "CR116 particle status", summaries["CR116"]["particle_catalog_status"]),
            check("CR147 dynamic release passes", summaries["CR147"]["all_predictions_passed"] and summaries["CR147"]["all_wrong_controls_rejected"], "CR147", source_status(summaries["CR147"])),
            check("CR147 preserves A=1 no literal launch", "NO_ESCAPE" in cr147["A1_exact_status"], "CR147 boundary", cr147["A1_exact_status"]),
            check("CR147 rejects static A integral seconds explanation", cr147["formal_static_A_integral_status"].startswith("REJECTED"), "CR147 static lane", cr147["formal_static_A_integral_status"]),
            check("QGA025 12/12 predictions pass", qga025_counts[0] == 12 and qga025_counts[1] == 12, "QGA025 checks", qga025_counts[:2]),
            check("QGA025 8/8 wrong controls pass", qga025_counts[2] == 8 and qga025_counts[3] == 8, "QGA025 checks", qga025_counts[2:]),
            check("QGA025 gaps remain open", all(row["status"] == "OPEN" for row in row_sets["QGA025_gap_register"]), "QGA025 gap register", len(row_sets["QGA025_gap_register"])),
            check("QGA026 12/12 predictions pass", qga026_counts[0] == 12 and qga026_counts[1] == 12, "QGA026 checks", qga026_counts[:2]),
            check("QGA026 8/8 wrong controls pass", qga026_counts[2] == 8 and qga026_counts[3] == 8, "QGA026 checks", qga026_counts[2:]),
            check("QGA026 gaps remain open", all(row["status"] == "OPEN" for row in row_sets["QGA026_gap_register"]), "QGA026 gap register", len(row_sets["QGA026_gap_register"])),
            check("SUK060 invariants pass", all_status(row_sets["SUK060_invariants"], "PASS"), "SUK060 invariants", len(row_sets["SUK060_invariants"])),
            check("SUK060 wrong controls rejected", all_status(row_sets["SUK060_wrong_controls"], "REJECTED"), "SUK060 controls", len(row_sets["SUK060_wrong_controls"])),
            check("SUK061 invariants pass", all_status(row_sets["SUK061_invariants"], "PASS"), "SUK061 invariants", len(row_sets["SUK061_invariants"])),
            check("SUK061 wrong controls rejected", all_status(row_sets["SUK061_wrong_controls"], "REJECTED"), "SUK061 controls", len(row_sets["SUK061_wrong_controls"])),
            check("Branch-05 seal keeps full thermodynamics separate", "full black-hole thermodynamics" in texts["branch05_seal"], "branch05 seal", "scope preserved"),
            check("CR073 manifest carries Hawking thermal bridge evidence", any("Hawking-Bekenstein-Smarr thermal bridge" in row.get("notes", "") for row in read_csv(SOURCES["CR073_manifest"])), "CR073 manifest", "QGA025 carried"),
            check("CR073 manifest carries horizon no-crossing evidence", any("G11555 magic-bell A=1 no-crossing theorem" in row.get("notes", "") for row in read_csv(SOURCES["CR073_manifest"])), "CR073 manifest", "G11555 carried"),
            check("All wrong controls rejected", all(row["result"] == "REJECTED" for row in wrong_controls), "LC11 wrong controls", f"{sum(1 for row in wrong_controls if row['result'] == 'REJECTED')}/{len(wrong_controls)}"),
        ]
    )

    source_rows: list[dict[str, Any]] = []
    for name, path in SOURCES.items():
        source_rows.append({"source": name, "path": rel(path), "status": "source artifact", "sha256": sha256_file(path)})
    for name, path in ROWS.items():
        source_rows.append({"source": name, "path": rel(path), "status": f"{len(row_sets[name])} rows", "sha256": sha256_file(path)})
    source_rows.append({"source": "LC11_runner", "path": rel(RUNNER_PATH), "status": "result-producing runner", "sha256": sha256_file(RUNNER_PATH)})
    source_rows.append({"source": "LC01_primitive_stack_declared_csv", "path": rel(LC01_PRIMITIVE_CSV), "status": "primitive exact values", "sha256": sha256_file(LC01_PRIMITIVE_CSV)})

    pass_count = sum(1 for row in checks if row["status"] == "PASS")
    fail_count = len(checks) - pass_count
    replay_passed = fail_count == 0 and all(row["result"] == "REJECTED" for row in wrong_controls)

    horizon_path = OUT_DIR / "LC11_horizon_ladder_replay.csv"
    branch05_path = OUT_DIR / "LC11_branch05_layers.csv"
    thermo_path = OUT_DIR / "LC11_thermodynamic_layers.csv"
    formula_path = OUT_DIR / "LC11_formula_manifest.csv"
    boundary_path = OUT_DIR / "LC11_claim_boundaries.csv"
    wrong_path = OUT_DIR / "LC11_wrong_controls.csv"
    checks_path = OUT_DIR / "LC11_checks.csv"
    source_path = OUT_DIR / "LC11_sources_hashes.csv"
    summary_path = OUT_DIR / "LC11_summary.json"
    result_path = OUT_DIR / "LC11_result.md"
    hash_path = OUT_DIR / "HASHES.txt"

    write_csv(horizon_path, landmark_rows, ["landmark", "formula", "expected_x", "source_x", "expected_A", "source_A", "status"])
    write_csv(branch05_path, branch05_layers, ["layer", "source", "contract", "source_value", "status", "boundary"])
    write_csv(thermo_path, thermodynamic_layers, ["layer", "source", "contract", "source_value", "status", "boundary"])
    write_csv(formula_path, formula_manifest, ["formula_or_rule", "expression", "locked_inputs", "replayed_value", "source_or_target_use"])
    write_csv(boundary_path, boundary_rows, ["boundary", "status", "text"])
    write_csv(wrong_path, wrong_controls, ["wrong_control", "attempted_mutation", "evidence", "result"])
    write_csv(checks_path, checks, ["check", "status", "value", "detail"])
    write_csv(source_path, source_rows, ["source", "path", "status", "sha256"])

    summary = {
        "task_id": TASK_ID,
        "task_name": TASK_NAME,
        "result": RESULT_CLASS if replay_passed else "LC11_FAIL_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY",
        "generated_utc": now,
        "locked_primitive_stack": primitive_stack,
        "pass_condition": {
            "formula_mutation": "forbidden",
            "constant_mutation": "forbidden",
            "target_value_substitution": "forbidden",
            "row_deletion": "forbidden",
            "retroactive_relabeling": "forbidden",
            "A1_softening": "forbidden",
            "full_thermodynamics_overpromotion": "forbidden",
            "child_ledger_HR_energy_substitution": "forbidden",
        },
        "horizon_replay": {
            "R": R,
            "D": D,
            "alpha_H": alpha_h,
            "A_share": str(A_share),
            "A_side": str(A_side),
            "max_loading": str(max_loading),
            "completion": str(completion),
            "split_loss_native": str(split_loss_native),
            "landmarks": {row["landmark"]: row["expected_A"] for row in landmark_rows},
            "CR008_last_near_horizon_redshift": cr008["last_near_horizon_redshift"],
            "CR008_last_near_horizon_lapse": cr008["last_near_horizon_lapse"],
            "CR009_bcrit_over_rs": cr009["bcrit_over_rs"],
            "CR010_omega_rs_over_c": cr010["omega_rs_over_c"],
        },
        "thermodynamic_replay": {
            "G11555_lane_verdict": g11555["lane_verdict"],
            "QGA025_predictions": f"{qga025_counts[0]}/{qga025_counts[1]}",
            "QGA025_wrong_controls": f"{qga025_counts[2]}/{qga025_counts[3]}",
            "QGA025_scope": qga025["scope"],
            "QGA026_predictions": f"{qga026_counts[0]}/{qga026_counts[1]}",
            "QGA026_wrong_controls": f"{qga026_counts[2]}/{qga026_counts[3]}",
            "QGA026_scope": qga026["scope"],
            "SUK060_invariants": f"{suk060['invariants_passed']}/{suk060['invariants_total']}",
            "SUK061_invariants": f"{suk061['invariants_passed']}/{suk061['invariants_total']}",
            "CR147_A1_exact_status": cr147["A1_exact_status"],
            "CR147_release_A": cr147["A_release"],
        },
        "checks": {
            "total": len(checks),
            "passed": pass_count,
            "failed": fail_count,
        },
        "wrong_controls": {
            "tested": len(wrong_controls),
            "rejected": sum(1 for row in wrong_controls if row["result"] == "REJECTED"),
        },
        "claim_boundaries": [row["text"] for row in boundary_rows],
        "artifacts": {
            "horizon_ladder": rel(horizon_path),
            "branch05_layers": rel(branch05_path),
            "thermodynamic_layers": rel(thermo_path),
            "formula_manifest": rel(formula_path),
            "claim_boundaries": rel(boundary_path),
            "wrong_controls": rel(wrong_path),
            "checks": rel(checks_path),
            "sources_hashes": rel(source_path),
            "summary": rel(summary_path),
            "result": rel(result_path),
            "hashes": rel(hash_path),
            "runner": rel(RUNNER_PATH),
        },
    }

    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    result_lines = [
        f"# {TASK_ID} - Black-Hole Horizon Thermodynamic Replay",
        "",
        f"Result: **{summary['result']}**",
        "",
        "Question: with the locked primitive stack promoted in LC01, does the black-hole / horizon thermodynamic lane replay without softening A=1, mutating constants, or overpromoting scoped thermodynamics?",
        "",
        "Verdict: yes. LC11 replays the horizon stack from R=12, D=3, alpha_H=2, and the sealed A-kernel without changing the formulas or row statuses. The lane closes as a boundary-aware PASS: A=1 remains the no-completed-parent-ledger / no-literal-photon-launch boundary; 11/12 remains the maximum-loading boundary with CR103a functional-form debt preserved; and the Hawking/thermodynamic bridge remains scoped rather than upgraded into a full spectrum theorem.",
        "",
        "Locked horizon stack:",
        f"- R = {R}, D = {D}, alpha_H = {alpha_h}",
        f"- A_share = {A_share}; A_side = {A_side}",
        f"- maximum loading = {max_loading}",
        f"- completion = {completion}",
        f"- split loss / carrier side = R^2 * 2^-D = {split_loss_native}",
        f"- surface debit = {surface_debit}",
        "",
        "Core replay numbers:",
        "- CR007 landmarks: A_horizon=1, A_photon=2/3, A_ISCO=1/3",
        f"- CR008 near-horizon redshift = {cr008['last_near_horizon_redshift']}; lapse = {cr008['last_near_horizon_lapse']}",
        f"- CR009 b_crit/r_s = {cr009['bcrit_over_rs']}; shadow diameter/r_s = {cr009['shadow_diameter_over_rs']}",
        f"- CR010 E/c^2 = {cr010['energy_over_c2']}; L/(m c r_s) = {cr010['angular_momentum_over_m_c_rs']}; Omega r_s/c = {cr010['omega_rs_over_c']}",
        f"- G11555 lane verdict = {g11555['lane_verdict']}",
        f"- QGA025 predictions/wrong controls = {qga025_counts[0]}/{qga025_counts[1]} and {qga025_counts[2]}/{qga025_counts[3]}",
        f"- QGA026 predictions/wrong controls = {qga026_counts[0]}/{qga026_counts[1]} and {qga026_counts[2]}/{qga026_counts[3]}",
        f"- SUK060 invariants/wrong controls = {suk060['invariants_passed']}/{suk060['invariants_total']} and {suk060['wrong_controls_rejected']}/{suk060['wrong_controls_total']}",
        f"- SUK061 invariants/wrong controls = {suk061['invariants_passed']}/{suk061['invariants_total']} and {suk061['wrong_controls_rejected']}/{suk061['wrong_controls_total']}",
        f"- CR147 A_release = {cr147['A_release']}; A=1 exact status = {cr147['A1_exact_status']}",
        "",
        "Trap controls rejected:",
        "- A=1 softening rejected: G11555 and CR147 preserve no completed parent-ledger crossing / no literal light launch.",
        "- Horizon-only fit rejected: CR009 and CR010 preserve photon-sphere and ISCO external contacts from the same A-profile.",
        "- Full-thermodynamics overpromotion rejected: QGA025/QGA026 leave greybody/species/rate/spectrum/correlation/endpoint gaps open.",
        "- Static A-integral GW170817 delay rejected: CR147 keeps the seconds-scale mechanism in dynamic A-release / source-engine reorganization.",
        "- 18-as-matter rejected: CR116 and CR147 keep 18 as a massless tensor-carrier channel.",
        "- Child-ledger HR energy rejected: SUK060/SUK061 keep HR as parent-boundary / ledger-cell balance.",
        "",
        "Claim boundaries preserved:",
        "- Not full strong-field metric, Kerr solution, EHT model, QNM/ringdown prediction, or full Hawking spectrum theorem.",
        "- CR103a's exact r_bounce(A) and K(A_H) functional forms remain open.",
        "- CR007/CR008 original BOUNDARY grades are preserved; CR011 appends appeal PASS readouts.",
        "",
        f"Checks: {pass_count}/{len(checks)} PASS",
        f"Wrong controls: {summary['wrong_controls']['rejected']}/{summary['wrong_controls']['tested']} rejected",
        "",
        "Primary artifacts:",
        f"- `{rel(horizon_path)}`",
        f"- `{rel(branch05_path)}`",
        f"- `{rel(thermo_path)}`",
        f"- `{rel(formula_path)}`",
        f"- `{rel(boundary_path)}`",
        f"- `{rel(wrong_path)}`",
        f"- `{rel(checks_path)}`",
        f"- `{rel(source_path)}`",
        f"- `{rel(summary_path)}`",
    ]
    with result_path.open("w", encoding="utf-8") as handle:
        handle.write("\n".join(result_lines))
        handle.write("\n")

    artifact_paths = [
        RUNNER_PATH,
        horizon_path,
        branch05_path,
        thermo_path,
        formula_path,
        boundary_path,
        wrong_path,
        checks_path,
        source_path,
        summary_path,
        result_path,
    ]
    with hash_path.open("w", encoding="utf-8") as handle:
        for path in artifact_paths:
            handle.write(f"{sha256_file(path)}  {rel(path)}\n")

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if replay_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
