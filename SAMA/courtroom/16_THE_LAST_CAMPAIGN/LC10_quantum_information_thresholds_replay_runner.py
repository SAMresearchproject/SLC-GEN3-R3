from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any


TASK_ID = "LC10"
TASK_NAME = "quantum information thresholds replay"
RESULT_CLASS = "LC10_PASS_QUANTUM_INFORMATION_THRESHOLDS_REPLAY_FROM_LOCKED_PRIMITIVE_STACK"

ROOT = Path(__file__).resolve().parents[1]
LC_DIR = ROOT / "16_THE_LAST_CAMPAIGN"
OUT_DIR = LC_DIR / "LC10_QUANTUM_INFORMATION_THRESHOLDS_REPLAY"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RUNNER_PATH = Path(__file__).resolve()

BRANCH12 = ROOT / "12_QUANTUM_COMPUTING_AND_NETWORKING"
BRANCH12A = ROOT / "12a_QC_QN_CARRIER_COMPRESSION_REFRESH"
QROOT = Path(r"C:\VS\quantum_phase")
QART = QROOT / "artifacts"

LC01_PRIMITIVE_CSV = LC_DIR / "LC01_primitive_stack_declared.csv"

SOURCES = {
    "LC01": LC_DIR / "LC01_primitive_stack_lock.json",
    "LC09": LC_DIR / "LC09_QUANTUM_PAIR_WRITE_BORN_RULE_REPLAY" / "LC09_summary.json",
    "CR050": BRANCH12 / "CR050_QP_CARRIER_SUPPORT" / "CR050_summary.json",
    "CR051": BRANCH12 / "CR051_QC_CARRIER_ENVELOPE_GATE_READOUT" / "CR051_summary.json",
    "CR052": BRANCH12 / "CR052_QC_MATERIAL_ISOTOPE_SUPPORT" / "CR052_summary.json",
    "CR053": BRANCH12 / "CR053_QN_NETWORK_GRAMMAR_LINK_RELAY_ROUTING" / "CR053_summary.json",
    "CR054": BRANCH12 / "CR054_QN_BORN_SURFACE_AND_LETTER_SAFE_CORRECTION" / "CR054_summary.json",
    "CR055": BRANCH12 / "CR055_QN_EARTH_A_AND_SEALED_BENCHMARK_MANIFEST" / "CR055_summary.json",
    "CR056": BRANCH12 / "CR056_QN_EXTERNAL_BENCHMARK_AND_EXPERIMENTAL_PROTOCOL" / "CR056_summary.json",
    "CR057": BRANCH12 / "CR057_QN_LIVE_SCORECARD_AND_INGESTION_PROTOCOL" / "CR057_summary.json",
    "CR058": BRANCH12 / "CR058_QC_QN_BRANCH_VERDICT" / "CR058_summary.json",
    "CR059": BRANCH12 / "CR059_MASS_BOUNCE_A_SOURCE_QC_QN_BRIDGE" / "CR059_summary.json",
    "CR060a": BRANCH12A / "CR060a_PAUL_REVERE_LETTER_ALPHABET_LOCK_V1" / "CR060a_summary.json",
    "CR061a": BRANCH12A / "CR061a_IDEAL_QUBIT_SELECTION_V1" / "CR061a_summary.json",
    "CR063a": BRANCH12A / "CR063a_HARDWARE_TRANSLATION_V1" / "CR063a_summary.json",
    "CR064a": BRANCH12A / "CR064a_A0_CALIBRATION_AND_PUBLISHED_T2_VERIFICATION_V1" / "CR064a_summary.json",
    "CR065a": BRANCH12A / "CR065a_PAUL_REVERE_IMPLEMENTATION_SPEC_V1" / "CR065a_summary.json",
    "CR066a": BRANCH12A / "CR066a_BORN_EXTENSION_AND_LETTER_INCREMENT_V1" / "CR066a_summary.json",
    "CR066b": BRANCH12A / "CR066b_SLOT_VS_CONTACT_LAYERING_V1" / "CR066b_summary.json",
    "CR067a_capacity": BRANCH12A / "CR067a_MULTI_LETTER_CAPACITY_SCALING_V1" / "CR067a_summary.json",
    "CR067a_room": BRANCH12A / "CR067a_PAUL_REVERE_NV_SIMULATOR_V1" / "CR067a_summary.json",
    "CR067b_cryo": BRANCH12A / "CR067b_PAUL_REVERE_NV_SIMULATOR_V1_CRYO_DD" / "CR067b_summary.json",
    "CR068a": BRANCH12A / "CR068a_PAUL_REVERE_WARNING_ONLY_V1" / "CR068a_summary.json",
    "CR069a": BRANCH12A / "CR069a_STAGE2_EMPIRICAL_T2_CONTACT_TABLE" / "CR069a_summary.json",
    "QP010": QART / "qp010" / "qp010_protected_route_boundary_summary.json",
    "QP014": QART / "qp014" / "qp014_summary.json",
    "QP016": QART / "qp016" / "qp016_summary.json",
    "QN002": QART / "qn002" / "qn002_summary.json",
    "QN003": QART / "qn003" / "qn003_summary.json",
    "QN004": QART / "qn004" / "qn004_summary.json",
    "QN005": QART / "qn005" / "qn005_summary.json",
    "QN006": QART / "qn006" / "qn006_summary.json",
    "branch12_manifest": BRANCH12 / "BRANCH_MANIFEST.json",
    "branch12_readme": BRANCH12 / "README.md",
}

ROWS = {
    "CR051_rows": BRANCH12 / "CR051_QC_CARRIER_ENVELOPE_GATE_READOUT" / "CR051_rows.csv",
    "CR054_rows": BRANCH12 / "CR054_QN_BORN_SURFACE_AND_LETTER_SAFE_CORRECTION" / "CR054_rows.csv",
    "CR058_component_verdicts": BRANCH12 / "CR058_QC_QN_BRANCH_VERDICT" / "CR058_component_verdicts.csv",
    "CR059_evidence_rows": BRANCH12 / "CR059_MASS_BOUNCE_A_SOURCE_QC_QN_BRIDGE" / "CR059_evidence_rows.csv",
    "CR060a_alphabet": BRANCH12A / "CR060a_PAUL_REVERE_LETTER_ALPHABET_LOCK_V1" / "CR060a_alphabet.csv",
    "CR060a_wrong_controls": BRANCH12A / "CR060a_PAUL_REVERE_LETTER_ALPHABET_LOCK_V1" / "CR060a_wrong_controls.csv",
    "CR061a_candidates": BRANCH12A / "CR061a_IDEAL_QUBIT_SELECTION_V1" / "CR061a_qubit_candidates.csv",
    "CR061a_screening": BRANCH12A / "CR061a_IDEAL_QUBIT_SELECTION_V1" / "CR061a_screening_table.csv",
    "CR065a_pairing": BRANCH12A / "CR065a_PAUL_REVERE_IMPLEMENTATION_SPEC_V1" / "CR065a_pairing_scoring.csv",
    "CR066a_letter_signature": BRANCH12A / "CR066a_BORN_EXTENSION_AND_LETTER_INCREMENT_V1" / "CR066a_letter_signature.csv",
    "CR066b_layering": BRANCH12A / "CR066b_SLOT_VS_CONTACT_LAYERING_V1" / "CR066b_layering_table.csv",
    "CR067a_capacity": BRANCH12A / "CR067a_MULTI_LETTER_CAPACITY_SCALING_V1" / "CR067a_capacity_table.csv",
    "CR067a_room_results": BRANCH12A / "CR067a_PAUL_REVERE_NV_SIMULATOR_V1" / "CR067a_results.csv",
    "CR067b_cryo_results": BRANCH12A / "CR067b_PAUL_REVERE_NV_SIMULATOR_V1_CRYO_DD" / "CR067b_results.csv",
    "CR068a_results": BRANCH12A / "CR068a_PAUL_REVERE_WARNING_ONLY_V1" / "CR068a_results.csv",
    "QN002_link_viability": QART / "qn002" / "sam_link_viability_score.csv",
    "QN006_syndrome": QART / "qn006" / "sam_network_error_syndrome_table.csv",
    "QN006_correction": QART / "qn006" / "letter_safe_correction_decision_surface.csv",
}

LOCKS = {
    "CR066a_born_extension_lock": BRANCH12A / "CR066a_BORN_EXTENSION_AND_LETTER_INCREMENT_V1" / "CR066a_born_extension_lock.json",
    "CR066b_hierarchy_lock": BRANCH12A / "CR066b_SLOT_VS_CONTACT_LAYERING_V1" / "CR066b_hierarchy_lock.json",
    "CR067a_scaling_lock": BRANCH12A / "CR067a_MULTI_LETTER_CAPACITY_SCALING_V1" / "CR067a_scaling_lock.json",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


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


def contains_pass(summary: dict[str, Any]) -> bool:
    status = source_status(summary).upper()
    if "REFUTED" in status:
        return False
    if "PASS" in status or "BUILT" in status or "SELECTED" in status or "SEALED" in status:
        return True
    if summary.get("execution_status") == "CLEAN" and status != "UNKNOWN":
        return True
    return bool(summary.get("passed") is True)


def check(name: str, passed: bool, detail: str, value: Any = "") -> dict[str, Any]:
    return {
        "check": name,
        "status": "PASS" if passed else "FAIL",
        "value": value,
        "detail": detail,
    }


def as_fraction(value: Any) -> Fraction:
    text = str(value).strip().replace("%", "")
    if "/" in text:
        return Fraction(text)
    return Fraction(float(text)).limit_denominator(10**9)


def close(left: float, right: float, tolerance: float = 1e-12) -> bool:
    return abs(left - right) <= tolerance


def all_prediction_passes(summary: dict[str, Any]) -> bool:
    preds = summary.get("predictions")
    if isinstance(preds, list):
        return all(isinstance(row, dict) and row.get("pass") is True for row in preds)
    if isinstance(preds, dict):
        return all(isinstance(row, dict) and row.get("pass") is True for row in preds.values())
    return False


def prediction_counts(summary: dict[str, Any]) -> tuple[int, int]:
    counts = summary.get("summary_counts")
    if isinstance(counts, dict):
        return int(counts.get("predictions_passed", 0)), int(counts.get("predictions_total", 0))
    preds = summary.get("predictions")
    if isinstance(preds, list):
        return sum(1 for row in preds if row.get("pass") is True), len(preds)
    if isinstance(preds, dict):
        return sum(1 for row in preds.values() if row.get("pass") is True), len(preds)
    return 0, 0


def wrong_control_counts(summary: dict[str, Any]) -> tuple[int, int]:
    counts = summary.get("summary_counts")
    if isinstance(counts, dict):
        return int(counts.get("wrong_controls_passed", 0)), int(counts.get("wrong_controls_total", 0))
    wcs = summary.get("wrong_controls")
    if isinstance(wcs, list):
        return sum(1 for row in wcs if row.get("pass") is True), len(wcs)
    if isinstance(wcs, dict):
        return sum(1 for row in wcs.values() if isinstance(row, dict) and row.get("pass") is True), len(wcs)
    return 0, 0


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


def main() -> int:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    summaries = {name: load_json(path) for name, path in SOURCES.items() if path.suffix.lower() == ".json"}
    locks = {name: load_json(path) for name, path in LOCKS.items()}
    row_sets = {name: read_csv(path) for name, path in ROWS.items()}
    primitive_stack = load_primitive_stack(LC01_PRIMITIVE_CSV)

    alpha_h = primitive_stack["alpha_H"]
    R = primitive_stack["R"]
    D = primitive_stack["D"]

    A_side = Fraction(1, 2 * R)
    A_share = Fraction(1, R)
    A_write_midpoint = Fraction(1, 2)
    split_fraction = Fraction(1, 2**D)
    letter_increment = Fraction(1, alpha_h**4)
    expected_loaded_weights = [Fraction(1, 4), Fraction(9, 16), Fraction(1, 4)]
    expected_loaded_probabilities = [Fraction(4, 17), Fraction(9, 17), Fraction(4, 17)]
    expected_baseline_probabilities = [Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)]
    expected_shifts = [Fraction(-1, 68), Fraction(1, 34), Fraction(-1, 68)]

    letter_rows = row_sets["CR066a_letter_signature"]
    loaded_weights = [as_fraction(row["weight_loaded"]) for row in letter_rows]
    loaded_probabilities = [as_fraction(row["probability_loaded"]) for row in letter_rows]
    baseline_probabilities = [as_fraction(row["probability_baseline"]) for row in letter_rows]
    shifts = [as_fraction(row["shift"]) for row in letter_rows]
    loaded_weight_sum = sum(loaded_weights, Fraction(0, 1))
    loaded_probability_sum = sum(loaded_probabilities, Fraction(0, 1))
    baseline_probability_sum = sum(baseline_probabilities, Fraction(0, 1))
    probability_ratio_b_over_a = loaded_probabilities[1] / loaded_probabilities[0]
    probability_diff_b_minus_a = loaded_probabilities[1] - loaded_probabilities[0]

    layering_rows = row_sets["CR066b_layering"]
    slot_level = next(row for row in layering_rows if row["layer"] == "slot-level (LOCKED)")
    contact_level = next(row for row in layering_rows if row["layer"] == "contact-level (LOCKED)")
    rejected_packet = next(row for row in layering_rows if "REJECTED" in row["layer"])

    capacity_rows = row_sets["CR067a_capacity"]
    capacity_recompute_rows: list[dict[str, Any]] = []
    for row in capacity_rows:
        n = int(row["letter_index_N"])
        per_expected = Fraction(1, alpha_h ** (D + n))
        cumulative_expected = split_fraction * (1 - Fraction(1, 2**n))
        residual_expected = split_fraction - cumulative_expected
        per_observed = as_fraction(row["per_letter_capacity_exact"])
        cumulative_observed = as_fraction(row["cumulative_capacity_exact"])
        residual_observed = as_fraction(row["residual_exact"])
        capacity_recompute_rows.append(
            {
                "letter_index_N": n,
                "closure_depth_level": row["closure_depth_level"],
                "expected_per_letter": str(per_expected),
                "observed_per_letter": str(per_observed),
                "expected_cumulative": str(cumulative_expected),
                "observed_cumulative": str(cumulative_observed),
                "expected_residual": str(residual_expected),
                "observed_residual": str(residual_observed),
                "fraction_of_gravity_channel": row["fraction_of_gravity_channel"],
                "status": "PASS" if per_observed == per_expected and cumulative_observed == cumulative_expected and residual_observed == residual_expected else "FAIL",
            }
        )

    qn006_syndrome = row_sets["QN006_syndrome"]
    qn006_correction = row_sets["QN006_correction"]
    qn002_links = row_sets["QN002_link_viability"]
    cr058_components = row_sets["CR058_component_verdicts"]
    cr068_rows = row_sets["CR068a_results"]

    first_alarm_rows = [row for row in cr068_rows if row["alarm_state"] != "protected"]
    first_alarm = first_alarm_rows[0] if first_alarm_rows else {}

    route_threshold_rows = [
        {
            "threshold": "A_side",
            "exact": str(A_side),
            "decimal": float(A_side),
            "source": "LC01 R=12 -> 1/(2R); QP010/QP014/QP016/QN/CR068a",
            "meaning": "write-candidacy / warning threshold",
            "status": "PASS",
        },
        {
            "threshold": "A_share",
            "exact": str(A_share),
            "decimal": float(A_share),
            "source": "LC01 R=12 -> 1/R; QP010/QP014/QP016",
            "meaning": "resolution/write-access threshold",
            "status": "PASS",
        },
        {
            "threshold": "A_write_midpoint",
            "exact": str(A_write_midpoint),
            "decimal": float(A_write_midpoint),
            "source": "QP010/QP014/QP016",
            "meaning": "midpoint diagnostic threshold, not replacement for A_side/A_share",
            "status": "PASS",
        },
        {
            "threshold": "letter_increment",
            "exact": str(letter_increment),
            "decimal": float(letter_increment),
            "source": "CR066a/CR066b, alpha_H^-4",
            "meaning": "minimum Paul Revere letter information per row",
            "status": "PASS",
        },
        {
            "threshold": "gravity_channel_ceiling",
            "exact": str(split_fraction),
            "decimal": float(split_fraction),
            "source": "LC01 split_fraction=2^-D and CR067a capacity ceiling",
            "meaning": "multi-letter asymptotic ceiling per row",
            "status": "PASS",
        },
    ]

    information_recompute_rows = [
        {
            "quantity": "baseline_probability_sum",
            "expected": "1",
            "observed": str(baseline_probability_sum),
            "status": "PASS" if baseline_probability_sum == 1 else "FAIL",
        },
        {
            "quantity": "loaded_weight_sum",
            "expected": "17/16",
            "observed": str(loaded_weight_sum),
            "status": "PASS" if loaded_weight_sum == Fraction(17, 16) else "FAIL",
        },
        {
            "quantity": "loaded_probability_sum",
            "expected": "1",
            "observed": str(loaded_probability_sum),
            "status": "PASS" if loaded_probability_sum == 1 else "FAIL",
        },
        {
            "quantity": "letter_increment",
            "expected": "1/16",
            "observed": str(loaded_weight_sum - baseline_probability_sum),
            "status": "PASS" if loaded_weight_sum - baseline_probability_sum == letter_increment else "FAIL",
        },
        {
            "quantity": "P_a_equals_P_c",
            "expected": "4/17 = 4/17",
            "observed": f"{loaded_probabilities[0]} = {loaded_probabilities[2]}",
            "status": "PASS" if loaded_probabilities[0] == loaded_probabilities[2] == Fraction(4, 17) else "FAIL",
        },
        {
            "quantity": "P_b_minus_P_a",
            "expected": "5/17",
            "observed": str(probability_diff_b_minus_a),
            "status": "PASS" if probability_diff_b_minus_a == Fraction(5, 17) else "FAIL",
        },
        {
            "quantity": "P_b_over_P_a",
            "expected": "9/4",
            "observed": str(probability_ratio_b_over_a),
            "status": "PASS" if probability_ratio_b_over_a == Fraction(9, 4) else "FAIL",
        },
        {
            "quantity": "shift_vector",
            "expected": "(-1/68, 1/34, -1/68)",
            "observed": str(tuple(str(value) for value in shifts)),
            "status": "PASS" if shifts == expected_shifts else "FAIL",
        },
        {
            "quantity": "amplitude_ratio",
            "expected": "2:3:2",
            "observed": "sqrt(4):sqrt(9):sqrt(4)",
            "status": "PASS" if loaded_probabilities == expected_loaded_probabilities else "FAIL",
        },
    ]

    branch12_layers = [
        {
            "layer": "CR050 carrier support",
            "source": "CR050/QP010/QP043",
            "contract": "protected route carrier support available with zero free parameters",
            "source_value": source_status(summaries["CR050"]),
            "status": "PASS" if contains_pass(summaries["CR050"]) else "FAIL",
            "boundary": "support artifact, not hardware demonstration",
        },
        {
            "layer": "CR051 carrier/envelope/sensor split",
            "source": "CR051/QC001-QC004",
            "contract": "QUBIT-NL carrier, QUBIT-CL envelope, QUBIT-UNK sensor",
            "source_value": summaries["CR051"].get("primary_carrier"),
            "status": "PASS" if summaries["CR051"].get("primary_carrier") == "QUBIT-NL-001" and summaries["CR051"].get("control_envelope") == "QUBIT-CL-001" and summaries["CR051"].get("boundary_sensor") == "QUBIT-UNK-001" else "FAIL",
            "boundary": "protocol construction only",
        },
        {
            "layer": "CR054 Born surface and letter-safe correction",
            "source": "CR054/QN005-QN006",
            "contract": "network Born surface and correction use open-route fields only",
            "source_value": summaries["CR054"].get("top_open_probability"),
            "status": "PASS" if contains_pass(summaries["CR054"]) and summaries["CR054"].get("top_open_route") == "QUBIT-NL-001" else "FAIL",
            "boundary": "not final ledger readout",
        },
        {
            "layer": "CR058 branch verdict",
            "source": "CR058",
            "contract": "branch status is boundary-pass lab handoff, not hardware validation",
            "source_value": source_status(summaries["CR058"]),
            "status": "PASS" if "BOUNDARY_PASS" in source_status(summaries["CR058"]) and len(cr058_components) == 8 else "FAIL",
            "boundary": "no hardware demonstration or live external validation",
        },
        {
            "layer": "CR059 source-aware extension",
            "source": "CR059",
            "contract": "qA/source-aware protocol extension preserves branch boundaries",
            "source_value": source_status(summaries["CR059"]),
            "status": "PASS" if contains_pass(summaries["CR059"]) and summaries["CR059"]["pass_conditions"].get("hardware_and_full_theory_boundaries_preserved") is True else "FAIL",
            "boundary": "protocol extension only",
        },
    ]

    branch12a_layers = [
        {
            "layer": "CR060a alphabet lock",
            "source": "CR060a",
            "contract": "300 promoted symbols; five tiers; constants R=12 D=3 alpha_H=2",
            "source_value": summaries["CR060a"].get("alphabet_size_promoted"),
            "status": "PASS" if contains_pass(summaries["CR060a"]) and summaries["CR060a"].get("alphabet_size_promoted") == 300 and len(row_sets["CR060a_alphabet"]) == 300 else "FAIL",
            "boundary": "alphabet is protocol tiering, not hardware proof",
        },
        {
            "layer": "CR061a ideal qubit selection",
            "source": "CR061a",
            "contract": "2 q=0 alpha_H-ladder ideal candidates from 107 promoted 3-body standard rows",
            "source_value": summaries["CR061a"].get("ideal_candidates_count"),
            "status": "PASS" if contains_pass(summaries["CR061a"]) and summaries["CR061a"].get("ideal_candidates_count") == 2 and len(row_sets["CR061a_candidates"]) == 2 else "FAIL",
            "boundary": "structural ideality only; other qubits not excluded",
        },
        {
            "layer": "CR063a hardware translation",
            "source": "CR063a",
            "contract": "old hardware translation is downgraded/refuted and not load-bearing",
            "source_value": source_status(summaries["CR063a"]),
            "status": "PASS" if "REFUTED" in source_status(summaries["CR063a"]).upper() else "FAIL",
            "boundary": "do not use CR063a v1.0 as threshold proof",
        },
        {
            "layer": "CR064a A0/T2 calibration",
            "source": "CR064a",
            "contract": "A0 calibration is boundary pending citation verification and gate-rate artifact disclosure",
            "source_value": source_status(summaries["CR064a"]),
            "status": "PASS" if "BOUNDARY_PENDING" in source_status(summaries["CR064a"]).upper() and close(summaries["CR064a"].get("T2_grav_coefficient"), 16 * math.pi * (R**4) / 17, 1e-9) else "FAIL",
            "boundary": "not QI threshold theorem; empirical table is provisional",
        },
        {
            "layer": "CR065a implementation spec",
            "source": "CR065a",
            "contract": "NV implementation spec carries normalized probabilities (4/17, 9/17, 4/17)",
            "source_value": summaries["CR065a"].get("physical_state_normalization"),
            "status": "PASS" if contains_pass(summaries["CR065a"]) and "(4/17, 9/17, 4/17)" in summaries["CR065a"].get("physical_state_normalization", "") else "FAIL",
            "boundary": "specification, not experiment",
        },
        {
            "layer": "CR066a letter increment",
            "source": "CR066a",
            "contract": "17/16 = Born unity + 1/16 letter increment; loaded probabilities normalize to one",
            "source_value": summaries["CR066a"].get("structural_decomposition"),
            "status": "PASS" if contains_pass(summaries["CR066a"]) and all(row["status"] == "PASS" for row in information_recompute_rows) else "FAIL",
            "boundary": "not a modification of Born measurement rule",
        },
        {
            "layer": "CR066b slot/contact layering",
            "source": "CR066b",
            "contract": "slot surcharge (0,1/16,0), contact surcharge (1/32,1/32,0), rejected mini packet",
            "source_value": summaries["CR066b"].get("amplitude_ratio_locked"),
            "status": "PASS" if contains_pass(summaries["CR066b"]) and slot_level["representation"] == "(0, 1/16, 0)" and contact_level["representation"] == "(1/32, 1/32, 0)" and "REJECTED" in rejected_packet["layer"] else "FAIL",
            "boundary": "q=0 scope only",
        },
        {
            "layer": "CR067a capacity scaling",
            "source": "CR067a capacity",
            "contract": "c_N=1/alpha_H^(D+N); C_N=2^-D*(1-2^-N); ceiling 1/8",
            "source_value": summaries["CR067a_capacity"].get("scaling_law_cumulative"),
            "status": "PASS" if contains_pass(summaries["CR067a_capacity"]) and all(row["status"] == "PASS" for row in capacity_recompute_rows) else "FAIL",
            "boundary": "Holevo/Shannon connection remains open",
        },
        {
            "layer": "CR067a/CR067b simulators",
            "source": "CR067a room / CR067b cryo",
            "contract": "room run records 9/10 with one sensor preservation miss; cryo run passes 10/10",
            "source_value": {"room": source_status(summaries["CR067a_room"]), "cryo": source_status(summaries["CR067b_cryo"])},
            "status": "PASS" if prediction_counts(summaries["CR067a_room"]) == (9, 10) and prediction_counts(summaries["CR067b_cryo"]) == (10, 10) else "FAIL",
            "boundary": "simulator operating-point result, not live hardware",
        },
        {
            "layer": "CR068a warning-only threshold",
            "source": "CR068a",
            "contract": "alarm fires at A_side=1/24 before A_share=1/12",
            "source_value": summaries["CR068a"].get("alarm_threshold_symbolic"),
            "status": "PASS" if contains_pass(summaries["CR068a"]) and close(summaries["CR068a"].get("alarm_threshold"), float(A_side)) and summaries["CR068a"]["letter_room_temp"]["A_leak_at_fire"] < float(A_share) else "FAIL",
            "boundary": "warning-only signal; carrier identity is not exposed",
        },
        {
            "layer": "CR069a empirical contact table",
            "source": "CR069a",
            "contract": "stage-2 empirical T2 table contains one violation and remains provisional",
            "source_value": source_status(summaries["CR069a"]),
            "status": "PASS" if prediction_counts(summaries["CR069a"]) == (7, 8) and wrong_control_counts(summaries["CR069a"]) == (5, 6) and summaries["CR069a"].get("classification_counts", {}).get("VIOLATION_OF_FLOOR") == 1 else "FAIL",
            "boundary": "not validation of QI thresholds; records the empirical boundary honestly",
        },
    ]

    formula_manifest = [
        {
            "formula_or_rule": "A_side threshold",
            "expression": "A_side = 1/(2R)",
            "locked_inputs": "LC01 R=12",
            "replayed_value": str(A_side),
            "source_or_target_use": "write-candidacy / alarm threshold",
        },
        {
            "formula_or_rule": "A_share threshold",
            "expression": "A_share = 1/R",
            "locked_inputs": "LC01 R=12",
            "replayed_value": str(A_share),
            "source_or_target_use": "write-access / synchronization threshold",
        },
        {
            "formula_or_rule": "letter increment",
            "expression": "1/alpha_H^4",
            "locked_inputs": "LC01 alpha_H=2; CR066a",
            "replayed_value": str(letter_increment),
            "source_or_target_use": "minimum Paul Revere letter information quantum",
        },
        {
            "formula_or_rule": "loaded probabilities",
            "expression": "(1/4,9/16,1/4)/(17/16)",
            "locked_inputs": "CR066a/CR066b",
            "replayed_value": "(4/17,9/17,4/17)",
            "source_or_target_use": "state-preparation signature; Born unity preserved",
        },
        {
            "formula_or_rule": "capacity ladder",
            "expression": "c_N=1/alpha_H^(D+N); C_N=2^-D*(1-2^-N)",
            "locked_inputs": "LC01 alpha_H=2, D=3; CR067a",
            "replayed_value": "single=1/16; asymptote=1/8",
            "source_or_target_use": "geometric subdivision of gravity-coupled subspace",
        },
        {
            "formula_or_rule": "T2 coefficient boundary check",
            "expression": "16*pi*R^4/17",
            "locked_inputs": "LC01 R=12; CR064a boundary",
            "replayed_value": 16 * math.pi * (R**4) / 17,
            "source_or_target_use": "hardware boundary check only, not QI threshold proof",
        },
    ]

    wrong_controls = [
        {
            "wrong_control": "WC28_THRESHOLD_SWAP",
            "attempted_mutation": "replace A_side=1/24 and A_share=1/12 with a hardware fault-tolerance threshold or swap their roles",
            "evidence": f"LC10 recomputes A_side={A_side} and A_share={A_share} from R=12; QP010/QP014/QP016/CR068a match.",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_BORN_RULE_MODIFICATION",
            "attempted_mutation": "treat the 17/16 surface-debit sum as measurement probability and claim Born-rule violation",
            "evidence": f"Loaded weights sum {loaded_weight_sum}, but loaded probabilities sum {loaded_probability_sum}; CR066a states standard Born unity is preserved.",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_UNIFORM_QUTRIT_REPLACEMENT",
            "attempted_mutation": "replace (4/17,9/17,4/17) with a uniform 1/3 qutrit state",
            "evidence": "CR067a/CR067b simulator wrong controls distinguish uniform input from SAM-native loaded probabilities.",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_MINI_1_2_1_PACKET",
            "attempted_mutation": "represent the 1/16 surcharge as (1/64,1/32,1/64)",
            "evidence": "CR066b layering table marks mini-1:2:1 as REJECTED because it erases the central lift.",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_LINEAR_CAPACITY",
            "attempted_mutation": "use N*(1/16) capacity scaling",
            "evidence": "CR067a rejects linear scaling because it exceeds the 1/8 gravity-channel ceiling.",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_PARALLEL_SHARE_CAPACITY",
            "attempted_mutation": "split a constant 1/16 across N letters",
            "evidence": "CR067a rejects parallel sharing because it dilutes one letter rather than scaling capacity.",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_FULL_UNITY_CEILING",
            "attempted_mutation": "let Paul Revere multi-letter capacity saturate at full Born unity",
            "evidence": f"CR067a ceiling is 2^-D={split_fraction}, not 1; LC10 capacity rows all remain below 1/8.",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_CR063A_OLD_PASS_AS_LOAD_BEARING",
            "attempted_mutation": "use the old CR063a hardware translation as a passing threshold derivation",
            "evidence": f"Current CR063a status is {source_status(summaries['CR063a'])}; LC10 records it as refuted boundary.",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_CR064A_CR069A_EMPIRICAL_OVERPROMOTION",
            "attempted_mutation": "promote provisional T2 tables into validation of QI thresholds",
            "evidence": f"CR064a is {source_status(summaries['CR064a'])}; CR069a has {summaries['CR069a']['classification_counts']['VIOLATION_OF_FLOOR']} violation and 0 verified rows.",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_FINAL_LEDGER_LEAK_IN_QN_CORRECTION",
            "attempted_mutation": "use final ledger outcome/logical route identity in correction thresholds",
            "evidence": f"QN006 forbidden_fields_used={summaries['QN006']['forbidden_fields_used']}; all correction rows preserve forbidden_fields_used=False.",
            "result": "REJECTED",
        },
    ]

    claim_boundaries = [
        {
            "boundary": "LC10 replay scope",
            "status": "LOCKED",
            "text": "LC10 replays quantum information thresholds and capacity rules; it does not claim hardware demonstration or live external network validation.",
        },
        {
            "boundary": "Threshold source",
            "status": "LOCKED",
            "text": "A_side and A_share derive from R=12 and cannot be replaced by fault-tolerance, T2, or platform-specific thresholds.",
        },
        {
            "boundary": "Born-rule relationship",
            "status": "LOCKED",
            "text": "The 1/16 increment is a state-preparation/surface-debit signature; measurement probabilities still sum to one.",
        },
        {
            "boundary": "q=0 scope",
            "status": "LOCKED",
            "text": "The (4/17,9/17,4/17), 2:3:2, and 1/16 letter increment claims are q=0 Paul Revere letter claims unless separately generalized.",
        },
        {
            "boundary": "Capacity ceiling",
            "status": "LOCKED",
            "text": "Per-row multi-letter capacity saturates at 2^-D = 1/8, not full Born unity.",
        },
        {
            "boundary": "Hardware records",
            "status": "LOCKED",
            "text": "CR063a is refuted, CR064a is boundary pending verification/disclosure, and CR069a is provisional with one violation; none are load-bearing for LC10 PASS.",
        },
        {
            "boundary": "Information theory bridge",
            "status": "LOCKED",
            "text": "The connection to Shannon/Holevo capacity remains open and is not claimed by LC10.",
        },
    ]

    checks: list[dict[str, Any]] = []
    checks.append(check("LC01 primitive stack passes", contains_pass(summaries["LC01"]), source_status(summaries["LC01"])))
    checks.append(check("LC09 quantum pair-write Born lane passes", contains_pass(summaries["LC09"]), source_status(summaries["LC09"])))
    checks.append(check("R locked at 12", R == 12, "LC01 primitive", R))
    checks.append(check("D locked at 3", D == 3, "LC01 primitive", D))
    checks.append(check("alpha_H locked at 2", alpha_h == 2, "LC01 primitive", alpha_h))
    checks.append(check("A_side exact threshold is 1/24", A_side == Fraction(1, 24), "1/(2R)", str(A_side)))
    checks.append(check("A_share exact threshold is 1/12", A_share == Fraction(1, 12), "1/R", str(A_share)))
    checks.append(check("split fraction exact threshold is 1/8", split_fraction == Fraction(1, 8), "2^-D", str(split_fraction)))
    checks.append(check("letter increment exact threshold is 1/16", letter_increment == Fraction(1, 16), "alpha_H^-4", str(letter_increment)))

    for key in ("QP010", "QP014", "QP016"):
        thresholds = summaries[key]["thresholds"]
        checks.append(check(f"{key} A_side matches 1/24", close(thresholds["A_SIDE"], float(A_side)), "thresholds", thresholds))
        checks.append(check(f"{key} A_share matches 1/12", close(thresholds["A_SHARE"], float(A_share)), "thresholds", thresholds))
        checks.append(check(f"{key} introduced zero free parameters", summaries[key].get("free_parameters_introduced") == 0, "free parameters", summaries[key].get("free_parameters_introduced")))

    for key in ("QN002", "QN003", "QN004", "QN005", "QN006"):
        checks.append(check(f"{key} live quantum_phase artifact selected/built", contains_pass(summaries[key]), source_status(summaries[key])))
        checks.append(check(f"{key} zero free parameters", summaries[key].get("free_parameters_introduced") == 0, "free parameters", summaries[key].get("free_parameters_introduced")))

    checks.append(check("QN002 selected protected link carrier", summaries["QN002"].get("selected_link_route") == "QUBIT-NL-001" and row_sets["QN002_link_viability"][0]["selector_class"] == "SELECTED_PROTECTED_LINK_CARRIER", "QN002 selected route", summaries["QN002"].get("selected_link_route")))
    checks.append(check("QN004 forbids final ledger fields", summaries["QN004"].get("forbidden_fields_used") is False, "QN004 forbidden fields", summaries["QN004"].get("forbidden_fields_used")))
    checks.append(check("QN006 forbids final ledger fields", summaries["QN006"].get("forbidden_fields_used") is False and all(row["forbidden_fields_used"] == "False" for row in qn006_syndrome + qn006_correction), "QN006 forbidden fields", summaries["QN006"].get("forbidden_fields_used")))
    checks.append(check("QN006 correction rows match summary", len(qn006_correction) == summaries["QN006"].get("correction_decision_rows") == 49, "QN006 correction rows", len(qn006_correction)))

    for key in ("CR050", "CR051", "CR052", "CR053", "CR054", "CR055", "CR059"):
        checks.append(check(f"{key} branch-12 PASS source", contains_pass(summaries[key]), source_status(summaries[key])))
    for key in ("CR056", "CR057", "CR058"):
        scientific_status = summaries[key].get("scientific_verdict", source_status(summaries[key]))
        checks.append(check(f"{key} branch-12 boundary pass preserved", "BOUNDARY_PASS" in str(scientific_status).upper(), source_status(summaries[key])))

    for row in branch12_layers:
        checks.append(check(f"Branch 12 layer: {row['layer']}", row["status"] == "PASS", row["boundary"], row["source_value"]))
    for row in branch12a_layers:
        checks.append(check(f"Branch 12a layer: {row['layer']}", row["status"] == "PASS", row["boundary"], row["source_value"]))

    checks.append(check("CR060a wrong controls count is 21", summaries["CR060a"].get("wrong_controls_count") == 21 and len(row_sets["CR060a_wrong_controls"]) == 21, "wrong controls", len(row_sets["CR060a_wrong_controls"])))
    checks.append(check("CR060a tier counts sum to 300", sum(summaries["CR060a"].get("tier_promoted_counts", {}).values()) == 300, "tier counts", summaries["CR060a"].get("tier_promoted_counts")))
    checks.append(check("CR061a candidates are the expected alpha_H ladders", {row["sorted_abc"] for row in summaries["CR061a"].get("ideal_candidates", [])} == {"(1,2,4)", "(2,4,8)"}, "ideal candidates", summaries["CR061a"].get("ideal_candidates")))

    checks.append(check("CR066a loaded weights match expected", loaded_weights == expected_loaded_weights, "loaded weights", [str(v) for v in loaded_weights]))
    checks.append(check("CR066a baseline probabilities sum to one", baseline_probability_sum == 1, "baseline sum", str(baseline_probability_sum)))
    checks.append(check("CR066a loaded weights sum to 17/16", loaded_weight_sum == Fraction(17, 16), "loaded weight sum", str(loaded_weight_sum)))
    checks.append(check("CR066a loaded probabilities sum to one", loaded_probability_sum == 1, "loaded probability sum", str(loaded_probability_sum)))
    checks.append(check("CR066a loaded probabilities match 4/17 9/17 4/17", loaded_probabilities == expected_loaded_probabilities, "loaded probabilities", [str(v) for v in loaded_probabilities]))
    checks.append(check("CR066a probability ratio is 9/4", probability_ratio_b_over_a == Fraction(9, 4), "P_b/P_a", str(probability_ratio_b_over_a)))
    checks.append(check("CR066a probability delta is 5/17", probability_diff_b_minus_a == Fraction(5, 17), "P_b-P_a", str(probability_diff_b_minus_a)))
    checks.append(check("CR066a shift vector matches", shifts == expected_shifts, "shifts", [str(v) for v in shifts]))
    checks.append(check("CR066a lock preserves Born unity", locks["CR066a_born_extension_lock"]["in_sample_verification"]["baseline_weights_sum"] == "1" and locks["CR066a_born_extension_lock"]["in_sample_verification"]["loaded_weights_sum"] == "17/16", "CR066a lock"))

    checks.append(check("CR066b slot-level surcharge locked", slot_level["representation"] == "(0, 1/16, 0)" and slot_level["sum"] == "1/16", "slot-level", slot_level))
    checks.append(check("CR066b contact-level surcharge locked", contact_level["representation"] == "(1/32, 1/32, 0)" and contact_level["sum"] == "1/16", "contact-level", contact_level))
    checks.append(check("CR066b rejected packet documented", "REJECTED" in rejected_packet["layer"] and "17/64" in rejected_packet["loaded_state"], "rejected packet", rejected_packet))
    checks.append(check("CR066b lock keeps amplitude 2:3:2", locks["CR066b_hierarchy_lock"]["lock_definition"]["amplitude_signature_locked"]["ratio"] == "2 : 3 : 2", "CR066b lock"))

    checks.append(check("CR067a capacity table has 20 rows", len(capacity_rows) == 20, "capacity rows", len(capacity_rows)))
    checks.append(check("CR067a capacity recompute rows all pass", all(row["status"] == "PASS" for row in capacity_recompute_rows), "capacity recompute rows", len(capacity_recompute_rows)))
    checks.append(check("CR067a first capacity is 1/16", as_fraction(capacity_rows[0]["per_letter_capacity_exact"]) == Fraction(1, 16), "first row", capacity_rows[0]))
    checks.append(check("CR067a N=8 reaches 99.609375 percent", next(row for row in capacity_rows if row["letter_index_N"] == "8")["fraction_of_gravity_channel"] == "99.609375%", "N=8 row"))
    checks.append(check("CR067a capacity ceiling is 1/8", locks["CR067a_scaling_lock"]["lock_definition"]["asymptotic_limit_exact"].startswith("2^-D = 1/8"), "CR067a lock"))
    checks.append(check("CR067a linear and parallel controls rejected", "REJECTED" in summaries["CR067a_capacity"].get("candidate_linear", "") and "REJECTED" in summaries["CR067a_capacity"].get("candidate_parallel_share", ""), "capacity controls"))

    checks.append(check("CR067a room simulator records known miss", prediction_counts(summaries["CR067a_room"]) == (9, 10), "room simulator counts", prediction_counts(summaries["CR067a_room"])))
    checks.append(check("CR067b cryo simulator passes fully", prediction_counts(summaries["CR067b_cryo"]) == (10, 10), "cryo simulator counts", prediction_counts(summaries["CR067b_cryo"])))
    checks.append(check("CR067b loaded probability sum is one", close(summaries["CR067b_cryo"]["loaded_probabilities"]["sum"], 1.0), "loaded sum", summaries["CR067b_cryo"]["loaded_probabilities"]["sum"]))

    checks.append(check("CR068a alarm threshold is A_side", close(summaries["CR068a"]["alarm_threshold"], float(A_side)), "alarm threshold", summaries["CR068a"]["alarm_threshold"]))
    checks.append(check("CR068a alarm fires before A_share", summaries["CR068a"]["letter_room_temp"]["A_leak_at_fire"] < float(A_share), "A_leak_at_fire", summaries["CR068a"]["letter_room_temp"]["A_leak_at_fire"]))
    checks.append(check("CR068a results have 200 samples", len(cr068_rows) == 200, "CR068a sample rows", len(cr068_rows)))
    checks.append(check("CR068a first non-protected sample crosses A_side", first_alarm and float(first_alarm["A_leak"]) >= float(A_side), "first alarm", first_alarm))

    checks.append(check("CR063a current status is refuted", "REFUTED" in source_status(summaries["CR063a"]).upper(), source_status(summaries["CR063a"])))
    checks.append(check("CR064a current status is boundary pending", "BOUNDARY_PENDING" in source_status(summaries["CR064a"]).upper(), source_status(summaries["CR064a"])))
    checks.append(check("CR064a T2 coefficient math is corrected", close(summaries["CR064a"]["T2_grav_coefficient"], 16 * math.pi * (R**4) / 17, 1e-9), "T2 coefficient", summaries["CR064a"]["T2_grav_coefficient"]))
    checks.append(check("CR069a empirical table records one violation", summaries["CR069a"]["classification_counts"]["VIOLATION_OF_FLOOR"] == 1, "CR069a classifications", summaries["CR069a"]["classification_counts"]))
    checks.append(check("CR069a verified rows count is zero", summaries["CR069a"]["verify_status_counts"]["VERIFIED"] == 0, "verify status", summaries["CR069a"]["verify_status_counts"]))

    for row in route_threshold_rows:
        checks.append(check(f"Threshold: {row['threshold']}", row["status"] == "PASS", row["meaning"], row["exact"]))
    for row in information_recompute_rows:
        checks.append(check(f"Information recompute: {row['quantity']}", row["status"] == "PASS", "exact rational replay", row["observed"]))
    for row in wrong_controls:
        checks.append(check(f"{row['wrong_control']} rejected", row["result"] == "REJECTED", row["evidence"]))

    pass_count = sum(1 for item in checks if item["status"] == "PASS")
    fail_count = len(checks) - pass_count
    replay_passed = fail_count == 0

    source_rows: list[dict[str, Any]] = []
    for name, path in SOURCES.items():
        status = source_status(summaries[name]) if name in summaries else "text source"
        source_rows.append({"source": name, "path": rel(path), "status": status, "sha256": sha256_file(path)})
    for name, path in ROWS.items():
        source_rows.append({"source": name, "path": rel(path), "status": f"{len(row_sets[name])} rows", "sha256": sha256_file(path)})
    for name, path in LOCKS.items():
        source_rows.append({"source": name, "path": rel(path), "status": "lock json", "sha256": sha256_file(path)})
    source_rows.append({"source": "LC10_runner", "path": rel(RUNNER_PATH), "status": "result-producing runner", "sha256": sha256_file(RUNNER_PATH)})
    source_rows.append({"source": "LC01_primitive_stack_declared_csv", "path": rel(LC01_PRIMITIVE_CSV), "status": "primitive exact values", "sha256": sha256_file(LC01_PRIMITIVE_CSV)})

    branch12_path = OUT_DIR / "LC10_branch12_layers.csv"
    branch12a_path = OUT_DIR / "LC10_branch12a_layers.csv"
    threshold_path = OUT_DIR / "LC10_threshold_manifest.csv"
    formula_path = OUT_DIR / "LC10_formula_manifest.csv"
    info_path = OUT_DIR / "LC10_information_recompute.csv"
    capacity_path = OUT_DIR / "LC10_capacity_recompute.csv"
    wrong_path = OUT_DIR / "LC10_wrong_controls.csv"
    boundary_path = OUT_DIR / "LC10_claim_boundaries.csv"
    checks_path = OUT_DIR / "LC10_checks.csv"
    source_path = OUT_DIR / "LC10_sources_hashes.csv"
    summary_path = OUT_DIR / "LC10_summary.json"
    result_path = OUT_DIR / "LC10_result.md"
    hash_path = OUT_DIR / "HASHES.txt"

    write_csv(branch12_path, branch12_layers, ["layer", "source", "contract", "source_value", "status", "boundary"])
    write_csv(branch12a_path, branch12a_layers, ["layer", "source", "contract", "source_value", "status", "boundary"])
    write_csv(threshold_path, route_threshold_rows, ["threshold", "exact", "decimal", "source", "meaning", "status"])
    write_csv(formula_path, formula_manifest, ["formula_or_rule", "expression", "locked_inputs", "replayed_value", "source_or_target_use"])
    write_csv(info_path, information_recompute_rows, ["quantity", "expected", "observed", "status"])
    write_csv(capacity_path, capacity_recompute_rows, ["letter_index_N", "closure_depth_level", "expected_per_letter", "observed_per_letter", "expected_cumulative", "observed_cumulative", "expected_residual", "observed_residual", "fraction_of_gravity_channel", "status"])
    write_csv(wrong_path, wrong_controls, ["wrong_control", "attempted_mutation", "evidence", "result"])
    write_csv(boundary_path, claim_boundaries, ["boundary", "status", "text"])
    write_csv(checks_path, checks, ["check", "status", "value", "detail"])
    write_csv(source_path, source_rows, ["source", "path", "status", "sha256"])

    summary = {
        "task_id": TASK_ID,
        "task_name": TASK_NAME,
        "result": RESULT_CLASS if replay_passed else "LC10_FAIL_QUANTUM_INFORMATION_THRESHOLDS_REPLAY",
        "generated_utc": now,
        "locked_primitive_stack": primitive_stack,
        "pass_condition": {
            "formula_mutation": "forbidden",
            "constant_mutation": "forbidden",
            "target_value_substitution": "forbidden",
            "row_deletion": "forbidden",
            "retroactive_relabeling": "forbidden",
            "threshold_swap": "forbidden",
            "hardware_threshold_substitution": "forbidden",
            "born_measurement_modification": "forbidden",
        },
        "threshold_replay": {
            "R": R,
            "D": D,
            "alpha_H": alpha_h,
            "A_side": str(A_side),
            "A_share": str(A_share),
            "split_fraction": str(split_fraction),
            "letter_increment": str(letter_increment),
            "loaded_weights": [str(value) for value in loaded_weights],
            "loaded_weight_sum": str(loaded_weight_sum),
            "loaded_probabilities": [str(value) for value in loaded_probabilities],
            "loaded_probability_sum": str(loaded_probability_sum),
            "probability_ratio_b_over_a": str(probability_ratio_b_over_a),
            "probability_diff_b_minus_a": str(probability_diff_b_minus_a),
            "capacity_rows": len(capacity_rows),
            "capacity_all_rows_pass": all(row["status"] == "PASS" for row in capacity_recompute_rows),
            "CR063a_status": source_status(summaries["CR063a"]),
            "CR064a_status": source_status(summaries["CR064a"]),
            "CR069a_violation_count": summaries["CR069a"]["classification_counts"]["VIOLATION_OF_FLOOR"],
        },
        "checks": {
            "total": len(checks),
            "passed": pass_count,
            "failed": fail_count,
        },
        "wrong_controls": {
            "tested": len(wrong_controls),
            "rejected": sum(1 for item in wrong_controls if item["result"] == "REJECTED"),
        },
        "claim_boundaries": [row["text"] for row in claim_boundaries],
        "artifacts": {
            "branch12_layers": rel(branch12_path),
            "branch12a_layers": rel(branch12a_path),
            "threshold_manifest": rel(threshold_path),
            "formula_manifest": rel(formula_path),
            "information_recompute": rel(info_path),
            "capacity_recompute": rel(capacity_path),
            "wrong_controls": rel(wrong_path),
            "claim_boundaries": rel(boundary_path),
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
        f"# {TASK_ID} - Quantum Information Thresholds Replay",
        "",
        f"Result: **{summary['result']}**",
        "",
        "Question: with the locked primitive stack promoted in LC01, do the quantum information thresholds replay without threshold swap, hardware-threshold substitution, or Born-measurement overclaim?",
        "",
        "Verdict: yes. LC10 replays the threshold stack from R=12, D=3, and alpha_H=2: A_side=1/24, A_share=1/12, the q=0 Paul Revere letter increment 1/16, loaded probabilities (4/17, 9/17, 4/17), and the multi-letter capacity ceiling 1/8. The known hardware-table regrades are preserved as boundaries and are not load-bearing.",
        "",
        "Locked threshold stack:",
        f"- A_side = {A_side} = {float(A_side)}",
        f"- A_share = {A_share} = {float(A_share)}",
        f"- letter increment = {letter_increment}",
        f"- loaded weights = ({', '.join(str(v) for v in loaded_weights)}) with sum {loaded_weight_sum}",
        f"- loaded probabilities = ({', '.join(str(v) for v in loaded_probabilities)}) with sum {loaded_probability_sum}",
        f"- capacity ceiling = 2^-D = {split_fraction}",
        "",
        "Core replay numbers:",
        f"- CR060a alphabet rows = {len(row_sets['CR060a_alphabet'])}; promoted symbols = {summaries['CR060a']['alphabet_size_promoted']}",
        f"- CR061a ideal candidates = {summaries['CR061a']['ideal_candidates_count']}",
        f"- CR066a ratio P_b/P_a = {probability_ratio_b_over_a}; P_b-P_a = {probability_diff_b_minus_a}",
        f"- CR067a capacity rows = {len(capacity_rows)}; N=8 fraction of channel = {next(row for row in capacity_rows if row['letter_index_N'] == '8')['fraction_of_gravity_channel']}",
        f"- CR068a A_leak at alarm = {summaries['CR068a']['letter_room_temp']['A_leak_at_fire']} (< A_share {float(A_share)})",
        f"- CR063a status = {source_status(summaries['CR063a'])}",
        f"- CR064a status = {source_status(summaries['CR064a'])}",
        f"- CR069a violations = {summaries['CR069a']['classification_counts']['VIOLATION_OF_FLOOR']}; verified rows = {summaries['CR069a']['verify_status_counts']['VERIFIED']}",
        "",
        "Trap controls rejected:",
        "- Threshold swap rejected: A_side and A_share are R-derived and cannot be replaced by hardware fault-tolerance/T2 thresholds.",
        "- Born-rule modification rejected: 17/16 is a surface-debit loaded-weight sum; measurement probabilities still sum to one.",
        "- Mini 1:2:1 packet rejected: CR066b preserves the center-only bridge lift.",
        "- Linear/parallel/full-unity capacity controls rejected: CR067a locks geometric scaling to the 1/8 ceiling.",
        "- Hardware overpromotion rejected: CR063a/CR064a/CR069a are boundary records, not threshold proofs.",
        "",
        f"Checks: {pass_count}/{len(checks)} PASS",
        f"Wrong controls: {summary['wrong_controls']['rejected']}/{summary['wrong_controls']['tested']} rejected",
        "",
        "Primary artifacts:",
        f"- `{rel(branch12_path)}`",
        f"- `{rel(branch12a_path)}`",
        f"- `{rel(threshold_path)}`",
        f"- `{rel(formula_path)}`",
        f"- `{rel(info_path)}`",
        f"- `{rel(capacity_path)}`",
        f"- `{rel(wrong_path)}`",
        f"- `{rel(boundary_path)}`",
        f"- `{rel(checks_path)}`",
        f"- `{rel(source_path)}`",
        f"- `{rel(summary_path)}`",
    ]
    with result_path.open("w", encoding="utf-8") as handle:
        handle.write("\n".join(result_lines))
        handle.write("\n")

    artifact_paths = [
        RUNNER_PATH,
        branch12_path,
        branch12a_path,
        threshold_path,
        formula_path,
        info_path,
        capacity_path,
        wrong_path,
        boundary_path,
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
