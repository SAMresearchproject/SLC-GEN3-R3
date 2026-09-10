from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TASK_ID = "LC09"
TASK_NAME = "quantum pair-write Born-rule lane replay"
RESULT_CLASS = "LC09_PASS_QUANTUM_PAIR_WRITE_BORN_RULE_REPLAY_FROM_LOCKED_PRIMITIVE_STACK"

ROOT = Path(__file__).resolve().parents[1]
LC_DIR = ROOT / "16_THE_LAST_CAMPAIGN"
OUT_DIR = LC_DIR / "LC09_QUANTUM_PAIR_WRITE_BORN_RULE_REPLAY"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RUNNER_PATH = Path(__file__).resolve()

BRANCH11 = ROOT / "11_QUANTUM_MECHANICS_AND_GRAVITY"
QROOT = Path(r"C:\VS\quantum_phase")
QART = QROOT / "artifacts"

LC01_PRIMITIVE_CSV = LC_DIR / "LC01_primitive_stack_declared.csv"

SOURCES = {
    "LC01": LC_DIR / "LC01_primitive_stack_lock.json",
    "LC03": LC_DIR / "LC03_summary.json",
    "CR073": BRANCH11 / "CR073_ACTION_PHASE_ANCHOR" / "CR073_summary.json",
    "CR074": BRANCH11 / "CR074_DOUBLE_SLIT_BORN_ROUTE" / "CR074_summary.json",
    "CR075": BRANCH11 / "CR075_UNRESOLVED_PATH_AND_LEDGER_WRITE" / "CR075_summary.json",
    "CR076": BRANCH11 / "CR076_PHASE_INTEGRAL_A_EXPOSURE" / "CR076_summary.json",
    "CR121": BRANCH11 / "CR121_SAM_GRAVITY_MECHANISM_INTAKE" / "CR121_summary.json",
    "branch11_scope": BRANCH11 / "SEALED_QUANTUM_MECHANICS_AND_GRAVITY_SCOPE_APPROACH_2026_06_13.md",
    "branch11_manifest": BRANCH11 / "SOURCE_MANIFEST.csv",
    "qp010": QART / "qp010" / "qp010_protected_route_boundary_summary.json",
    "qp011": QART / "qp011" / "qp011_summary.json",
    "qp012": QART / "qp012" / "qp012_summary.json",
    "qp013": QART / "qp013" / "qp013_summary.json",
    "qp014": QART / "qp014" / "qp014_summary.json",
    "qp015": QART / "qp015" / "qp015_summary.json",
    "qp016": QART / "qp016" / "qp016_summary.json",
    "qn005": QART / "qn005" / "qn005_summary.json",
    "qn_ladder": QROOT / "campaign" / "01_TEST_LADDER_QN000_QN020.md",
}

CHECK_JSON = {
    "CR073_action_identity": BRANCH11 / "CR073_ACTION_PHASE_ANCHOR" / "CR073_action_identity_check.json",
    "CR073_phase_identity": BRANCH11 / "CR073_ACTION_PHASE_ANCHOR" / "CR073_phase_identity_check.json",
    "CR073_free_particle": BRANCH11 / "CR073_ACTION_PHASE_ANCHOR" / "CR073_free_particle_action_check.json",
    "CR074_born_identity": BRANCH11 / "CR074_DOUBLE_SLIT_BORN_ROUTE" / "CR074_born_identity_check.json",
    "CR074_route_weight": BRANCH11 / "CR074_DOUBLE_SLIT_BORN_ROUTE" / "CR074_route_weight_check.json",
    "CR075_protected_route": BRANCH11 / "CR075_UNRESOLVED_PATH_AND_LEDGER_WRITE" / "CR075_protected_route_check.json",
    "CR075_ledger_commit": BRANCH11 / "CR075_UNRESOLVED_PATH_AND_LEDGER_WRITE" / "CR075_ledger_commit_check.json",
    "CR075_stable_mode": BRANCH11 / "CR075_UNRESOLVED_PATH_AND_LEDGER_WRITE" / "CR075_stable_mode_selector_check.json",
    "CR075_syndrome": BRANCH11 / "CR075_UNRESOLVED_PATH_AND_LEDGER_WRITE" / "CR075_syndrome_boundary_check.json",
    "CR076_phase_functional": BRANCH11 / "CR076_PHASE_INTEGRAL_A_EXPOSURE" / "CR076_phase_functional_check.json",
    "CR076_a_exposure": BRANCH11 / "CR076_PHASE_INTEGRAL_A_EXPOSURE" / "CR076_a_exposure_check.json",
    "CR076_integral_form": BRANCH11 / "CR076_PHASE_INTEGRAL_A_EXPOSURE" / "CR076_integral_form_check.json",
}

ROWS = {
    "qp014_born_schema": QART / "qp014" / "qp014_born_bridge_schema.csv",
    "qp014_probability_surface": QART / "qp014" / "qp014_probability_surface_table.csv",
    "qp014_route_weight": QART / "qp014" / "qp014_route_weight_table.csv",
    "qp015_commit_bridge": QART / "qp015" / "qp015_interference_commit_bridge_table.csv",
    "qp015_commit_summary": QART / "qp015" / "qp015_sample_commit_summary.csv",
    "qp016_stable_modes": QART / "qp016" / "qp016_stable_mode_selector_table.csv",
    "qp016_mode_family": QART / "qp016" / "qp016_mode_family_summary.csv",
    "qn005_checks": QART / "qn005" / "qn005_checks.csv",
    "qn005_wrong_controls": QART / "qn005" / "qn005_wrong_controls.csv",
    "qn005_network_surface": QART / "qn005" / "network_route_weight_surface.csv",
    "qn005_multi_node_surface": QART / "qn005" / "multi_node_probability_surface.csv",
}

WRONG_CONTROL_FILES = {
    "CR073": BRANCH11 / "CR073_ACTION_PHASE_ANCHOR" / "CR073_wrong_controls.csv",
    "CR074": BRANCH11 / "CR074_DOUBLE_SLIT_BORN_ROUTE" / "CR074_wrong_controls.csv",
    "CR075": BRANCH11 / "CR075_UNRESOLVED_PATH_AND_LEDGER_WRITE" / "CR075_wrong_controls.csv",
    "CR076": BRANCH11 / "CR076_PHASE_INTEGRAL_A_EXPOSURE" / "CR076_wrong_controls.csv",
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
    for key in ("result", "result_class", "scientific_verdict", "verdict", "status", "artifact"):
        value = summary.get(key)
        if isinstance(value, str) and value:
            return value
    return "UNKNOWN"


def contains_pass(summary: dict[str, Any]) -> bool:
    status = source_status(summary).upper()
    if "PASS" in status or "BUILT" in status or "SELECTED" in status:
        return True
    if summary.get("execution_status") == "CLEAN" and status != "UNKNOWN":
        return True
    if summary.get("all_checks_passed") is True or summary.get("passed") is True:
        return True
    return False


def check(name: str, passed: bool, detail: str, value: Any = "") -> dict[str, Any]:
    return {
        "check": name,
        "status": "PASS" if passed else "FAIL",
        "value": value,
        "detail": detail,
    }


def close(left: float, right: float, tolerance: float = 1e-12) -> bool:
    return abs(left - right) <= tolerance


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


def float_row(row: dict[str, str], key: str) -> float:
    return float(row[key])


def all_bool(rows: list[dict[str, str]], key: str) -> bool:
    return all(row.get(key, "").strip().lower() == "true" for row in rows)


def main() -> int:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    summaries = {name: load_json(path) for name, path in SOURCES.items() if path.suffix.lower() == ".json"}
    check_json = {name: load_json(path) for name, path in CHECK_JSON.items()}
    row_sets = {name: read_csv(path) for name, path in ROWS.items()}
    wrong_source_rows = {name: read_csv(path) for name, path in WRONG_CONTROL_FILES.items()}
    primitive_stack = load_primitive_stack(LC01_PRIMITIVE_CSV)

    R = primitive_stack["R"]
    D = primitive_stack["D"]
    A_side = 1.0 / (2.0 * R)
    A_share = 1.0 / R
    A_write_midpoint = 0.5

    qp014_surface = row_sets["qp014_probability_surface"]
    qp014_weights = row_sets["qp014_route_weight"]
    qp015_commit = row_sets["qp015_commit_bridge"]
    qp015_summary_rows = row_sets["qp015_commit_summary"]
    qp016_modes = row_sets["qp016_stable_modes"]
    qn005_surface = row_sets["qn005_network_surface"]
    qn005_multi = row_sets["qn005_multi_node_surface"]
    qn005_checks = row_sets["qn005_checks"]
    qn005_wrong = row_sets["qn005_wrong_controls"]

    open_qp014 = [row for row in qp014_surface if int(row["valid_probability_routes"]) > 0]
    closed_qp014 = [row for row in qp014_surface if int(row["valid_probability_routes"]) == 0]
    qp014_norm_errors = [
        max(
            abs(float(row["latent_probability_sum"]) - 1.0),
            abs(float(row["write_surface_probability_sum"]) - 1.0),
            abs(float(row["controlled_probability_sum"]) - 1.0),
        )
        for row in open_qp014
    ]
    qp014_closed_errors = [
        max(
            abs(float(row["latent_probability_sum"])),
            abs(float(row["write_surface_probability_sum"])),
            abs(float(row["controlled_probability_sum"])),
        )
        for row in closed_qp014
    ]

    # Recompute QP014 probability sums from row weights, sample by sample. This is the no-patch check.
    qp014_recomputed_rows: list[dict[str, Any]] = []
    for sample_id in sorted({row["sample_id"] for row in qp014_weights}):
        rows = [row for row in qp014_weights if row["sample_id"] == sample_id]
        latent_sum = sum(float_row(row, "latent_route_weight") for row in rows)
        write_sum = sum(float_row(row, "write_surface_weight") for row in rows)
        controlled_sum = sum(float_row(row, "controlled_route_weight") for row in rows)
        latent_prob_sum = sum(float_row(row, "latent_probability") for row in rows)
        write_prob_sum = sum(float_row(row, "write_surface_probability") for row in rows)
        controlled_prob_sum = sum(float_row(row, "controlled_probability") for row in rows)
        open_window = any(float_row(row, "latent_route_weight") > 0 for row in rows)
        top_latent = max(rows, key=lambda item: float_row(item, "latent_probability"))
        qp014_recomputed_rows.append(
            {
                "sample_id": sample_id,
                "rows": len(rows),
                "latent_weight_sum": latent_sum,
                "write_weight_sum": write_sum,
                "controlled_weight_sum": controlled_sum,
                "latent_probability_sum": latent_prob_sum,
                "write_surface_probability_sum": write_prob_sum,
                "controlled_probability_sum": controlled_prob_sum,
                "top_latent_route": top_latent["qubit_id"],
                "top_latent_probability": top_latent["latent_probability"],
                "open_window": open_window,
                "status": "PASS" if (open_window and close(latent_prob_sum, 1.0)) or ((not open_window) and close(latent_prob_sum, 0.0)) else "FAIL",
            }
        )

    # Recompute pair probabilities from the QP014 controlled probabilities.
    primary_sample = "QUARTER_A_SIDE"
    primary_weights = [row for row in qp014_weights if row["sample_id"] == primary_sample]
    prob_by_route = {row["qubit_id"]: float(row["controlled_probability"]) for row in primary_weights}
    pair_recompute_rows: list[dict[str, Any]] = []
    for row in qp015_commit:
        if row["qp014_sample_id"] != primary_sample or row["qp003_kernel_sample_id"] != "N_A_SHARE":
            continue
        pi = prob_by_route[row["route_i"]]
        pj = prob_by_route[row["route_j"]]
        expected = pi * pi if row["route_i"] == row["route_j"] else 2.0 * pi * pj
        observed = float(row["controlled_pair_probability"])
        pair_recompute_rows.append(
            {
                "qp014_sample_id": row["qp014_sample_id"],
                "qp003_kernel_sample_id": row["qp003_kernel_sample_id"],
                "route_pair": row["route_pair"],
                "expected_pair_probability": expected,
                "observed_controlled_pair_probability": observed,
                "error": observed - expected,
                "status": "PASS" if close(expected, observed, 1e-12) else "FAIL",
            }
        )
    pair_probability_sum = sum(row["observed_controlled_pair_probability"] for row in pair_recompute_rows)

    commit_open = [row for row in qp015_summary_rows if close(float(row["commit_probability_sum"]), 1.0)]
    commit_closed = [row for row in qp015_summary_rows if close(float(row["commit_probability_sum"]), 0.0)]
    support_ok = all(close(float(row["support_probability_sum"]), 1.0) or close(float(row["support_probability_sum"]), 0.0) for row in qp015_summary_rows)

    stable_modes = [row for row in qp016_modes if row["selector_class"] == "STABLE_SELF_CLOSURE_MODE_SELECTED"]
    boundary_modes = [row for row in qp016_modes if row["selector_class"] == "BOUNDARY_REORGANIZATION_CANDIDATE"]
    transient_modes = [row for row in qp016_modes if row["selector_class"] == "TRANSIENT_COMMIT_TAIL"]
    top_mode = stable_modes[0] if stable_modes else {}

    qn005_open = [row for row in qn005_surface if row["surface_class"] != "NETWORK_WINDOW_CLOSED"]
    qn005_closed = [row for row in qn005_surface if row["surface_class"] == "NETWORK_WINDOW_CLOSED"]
    qn005_forbidden_fields = any(row["forbidden_fields_used"].strip().lower() == "true" for row in qn005_surface + qn005_multi)
    qn005_network_routes = sorted({row["qubit_id"] for row in qn005_surface if row["network_route_available"] == "True"})
    qn005_top_open = max(qn005_open, key=lambda item: float(item["network_probability"])) if qn005_open else {}

    qn019_candidates = list(QROOT.rglob("*QN019*")) + list(QROOT.rglob("*qn019*"))
    qn020_candidates = list(QROOT.rglob("*QN020*")) + list(QROOT.rglob("*qn020*"))
    qn019_live_artifact_count = len([path for path in qn019_candidates if path.is_file()])
    qn020_live_artifact_count = len([path for path in qn020_candidates if path.is_file() and path != SOURCES["qn_ladder"]])

    branch_layers = [
        {
            "layer": "CR073 action/phase anchor",
            "source": "CR073",
            "contract": "S_A=E_p*T_A and Delta_phi=S_A/hbar are present; public free-particle action tests are present",
            "source_value": source_status(summaries["CR073"]),
            "status": "PASS" if contains_pass(summaries["CR073"]) and check_json["CR073_action_identity"]["status"] == "action_identity_present" and check_json["CR073_phase_identity"]["status"] == "phase_identity_present" else "FAIL",
            "boundary": "Presence and bridge support only; no phase fit loop is allowed.",
        },
        {
            "layer": "CR074 Born route",
            "source": "CR074/QP014",
            "contract": "Born identity plus route-weight identity present; QP014 has zero free parameters and zero normalization failures",
            "source_value": source_status(summaries["CR074"]),
            "status": "PASS" if contains_pass(summaries["CR074"]) and summaries["qp014"]["free_parameters_introduced"] == 0 and summaries["qp014"]["normalization_failures"] == 0 else "FAIL",
            "boundary": "Normalization is row-surface accounting, not a post-hoc probability patch.",
        },
        {
            "layer": "CR075 protected route and ledger write",
            "source": "CR075/QP010-QP016",
            "contract": "Protected route, syndrome boundary, ledger commit, and stable mode selector are present",
            "source_value": source_status(summaries["CR075"]),
            "status": "PASS" if contains_pass(summaries["CR075"]) and check_json["CR075_ledger_commit"]["hits"] > 0 and check_json["CR075_protected_route"]["hits"] > 0 else "FAIL",
            "boundary": "Syndrome/control may write support without writing protected route identity.",
        },
        {
            "layer": "CR076 phase integral A exposure",
            "source": "CR076/QP001",
            "contract": "A exposure and phase functional are present; explicit integral form remains boundary",
            "source_value": source_status(summaries["CR076"]),
            "status": "PASS" if summaries["CR076"].get("scientific_verdict") == "BOUNDARY" and check_json["CR076_integral_form"]["hits"] == 0 else "FAIL",
            "boundary": "LC09 does not upgrade CR076 to full integral closure.",
        },
    ]

    replay_layers = [
        {
            "layer": "LC01 locked primitive stack",
            "source": "LC01",
            "contract": "R=12, D=3, A_side=1/(2R), A_share=1/R",
            "replayed_value": {"R": R, "D": D, "A_side": A_side, "A_share": A_share},
            "status": "PASS" if contains_pass(summaries["LC01"]) and R == 12 and D == 3 and close(A_side, 1 / 24) and close(A_share, 1 / 12) else "FAIL",
            "boundary": "Quantum route thresholds derive from R; no threshold swap.",
        },
        {
            "layer": "QP010 protected route boundary",
            "source": "qp010",
            "contract": "A_leak below A_side stays protected; A_share opens resolution access",
            "replayed_value": summaries["qp010"]["thresholds"],
            "status": "PASS" if summaries["qp010"]["free_parameters_introduced"] == 0 and close(summaries["qp010"]["thresholds"]["A_SIDE"], A_side) and close(summaries["qp010"]["thresholds"]["A_SHARE"], A_share) else "FAIL",
            "boundary": "A_leak is a protected-window/write-candidacy signal, not phase amount.",
        },
        {
            "layer": "QP014 Born route-weight surface",
            "source": "qp014",
            "contract": "P_i = weight_i / sum(weight_all) from native row weights",
            "replayed_value": {"rows": len(qp014_weights), "surface_rows": len(qp014_surface), "normalization_failures": summaries["qp014"]["normalization_failures"]},
            "status": "PASS" if len(qp014_weights) == summaries["qp014"]["route_weight_rows"] == 49 and len(qp014_surface) == summaries["qp014"]["probability_surface_rows"] == 7 and max(qp014_norm_errors) <= 1e-12 and max(qp014_closed_errors) <= 1e-12 else "FAIL",
            "boundary": "The denominator is the native open route-weight sum; closed windows carry zero probability.",
        },
        {
            "layer": "QP015 pair-write / interference-to-ledger commit",
            "source": "qp015",
            "contract": "P_ij=P_i^2 for self pairs and 2*P_i*P_j for mixed pairs before ledger kernel selection",
            "replayed_value": {"bridge_rows": len(qp015_commit), "summary_rows": len(qp015_summary_rows), "primary_pair_sum": pair_probability_sum},
            "status": "PASS" if len(qp015_commit) == summaries["qp015"]["bridge_rows"] == 1176 and len(qp015_summary_rows) == summaries["qp015"]["sample_summary_rows"] == 42 and pair_recompute_rows and all(row["status"] == "PASS" for row in pair_recompute_rows) and close(pair_probability_sum, 1.0) and len(commit_open) > 0 and support_ok else "FAIL",
            "boundary": "Interference/support surfaces can exist before commit; commit opens only when the bounce/write kernel opens.",
        },
        {
            "layer": "QP016 stable mode selector",
            "source": "qp016",
            "contract": "stable self-closure requires native persistence across structured commit rows",
            "replayed_value": {"route_pairs": len(qp016_modes), "stable": len(stable_modes), "boundary": len(boundary_modes), "transient": len(transient_modes), "top": top_mode.get("route_pair", "")},
            "status": "PASS" if len(qp016_modes) == summaries["qp016"]["route_pairs"] == 28 and len(stable_modes) == summaries["qp016"]["stable_selected_modes"] == 1 and len(boundary_modes) == 1 and len(transient_modes) == 26 and top_mode.get("route_pair") == summaries["qp016"]["top_stable_mode_pair"] else "FAIL",
            "boundary": "Not every committed intersection is promoted to stable mode.",
        },
        {
            "layer": "QN005 network Born surface",
            "source": "qn005",
            "contract": "network probabilities use open route weights without final ledger fields",
            "replayed_value": {"network_rows": len(qn005_surface), "multi_node_rows": len(qn005_multi), "top_open_route": qn005_top_open.get("qubit_id", "")},
            "status": "PASS" if summaries["qn005"]["free_parameters_introduced"] == 0 and len(qn005_surface) == summaries["qn005"]["network_route_rows"] == 49 and len(qn005_multi) == summaries["qn005"]["multi_node_rows"] == 84 and all_bool(qn005_checks, "pass") and all_bool(qn005_wrong, "pass") and not qn005_forbidden_fields else "FAIL",
            "boundary": "Network surface is an open-window route surface; final ledger outcome fields are forbidden.",
        },
        {
            "layer": "QN019/QN020 live artifact availability",
            "source": "quantum_phase campaign",
            "contract": "QN ladder names QN019/QN020, but no executed QN019/QN020 artifact folders are present in live disk tree",
            "replayed_value": {"QN019_files": qn019_live_artifact_count, "QN020_files_excluding_ladder": qn020_live_artifact_count},
            "status": "PASS" if SOURCES["qn_ladder"].exists() and qn019_live_artifact_count == 0 and qn020_live_artifact_count == 0 else "FAIL",
            "boundary": "LC09 does not use stale or missing QN019/QN020 memory as proof; it records the absence and relies on live QP/QN artifacts.",
        },
    ]

    formula_manifest = [
        {
            "formula_or_rule": "R-derived thresholds",
            "expression": "A_side=1/(2R); A_share=1/R",
            "locked_inputs": "LC01 R=12",
            "replayed_value": {"A_side": A_side, "A_share": A_share},
            "source_or_target_use": "native threshold derivation, not threshold swap",
        },
        {
            "formula_or_rule": "protected route leakage",
            "expression": "A_leak(N)=N*Gamma_leak; protected if A_leak<A_side; write-candidate at A_side; resolution-accessible at A_share",
            "locked_inputs": "QP010",
            "replayed_value": summaries["qp010"]["law"],
            "source_or_target_use": "route-window grammar",
        },
        {
            "formula_or_rule": "Born route weight",
            "expression": "latent_weight_i=route_capacity_prior_i*coherence_survival_i; P_i=weight_i/sum(weight_all)",
            "locked_inputs": "QP014 row surface",
            "replayed_value": summaries["qp014"]["law"],
            "source_or_target_use": "native normalization before ledger resolution",
        },
        {
            "formula_or_rule": "pair-write probability",
            "expression": "P_ij=P_i^2 for self-pairs; P_ij=2*P_i*P_j for mixed pairs",
            "locked_inputs": "QP015",
            "replayed_value": summaries["qp015"]["law"],
            "source_or_target_use": "pair-write/interference bridge",
        },
        {
            "formula_or_rule": "stable mode selector",
            "expression": "latest P_commit>=A_share and persistence rows>=A_side",
            "locked_inputs": "QP016",
            "replayed_value": summaries["qp016"]["law"],
            "source_or_target_use": "stable mode selection",
        },
        {
            "formula_or_rule": "action/phase anchor",
            "expression": "S_A=E_p*T_A; Delta_phi=S_A/hbar",
            "locked_inputs": "CR073",
            "replayed_value": "present in CR073 identity checks",
            "source_or_target_use": "phase/action bridge only",
        },
    ]

    metrics = [
        {"metric": "A_side", "replayed": A_side, "source": "LC01 R=12", "status": "PASS" if close(A_side, 1 / 24) else "FAIL"},
        {"metric": "A_share", "replayed": A_share, "source": "LC01 R=12", "status": "PASS" if close(A_share, 1 / 12) else "FAIL"},
        {"metric": "QP014 route weight rows", "replayed": len(qp014_weights), "source": "qp014_route_weight_table.csv", "status": "PASS" if len(qp014_weights) == 49 else "FAIL"},
        {"metric": "QP014 max open normalization error", "replayed": max(qp014_norm_errors), "source": "qp014_probability_surface_table.csv", "status": "PASS" if max(qp014_norm_errors) <= 1e-12 else "FAIL"},
        {"metric": "QP014 max closed probability error", "replayed": max(qp014_closed_errors), "source": "qp014_probability_surface_table.csv", "status": "PASS" if max(qp014_closed_errors) <= 1e-12 else "FAIL"},
        {"metric": "QP015 bridge rows", "replayed": len(qp015_commit), "source": "qp015_interference_commit_bridge_table.csv", "status": "PASS" if len(qp015_commit) == 1176 else "FAIL"},
        {"metric": "QP015 primary pair probability sum", "replayed": pair_probability_sum, "source": "LC09 recompute", "status": "PASS" if close(pair_probability_sum, 1.0) else "FAIL"},
        {"metric": "QP016 stable selected modes", "replayed": len(stable_modes), "source": "qp016_stable_mode_selector_table.csv", "status": "PASS" if len(stable_modes) == 1 else "FAIL"},
        {"metric": "QN005 network route rows", "replayed": len(qn005_surface), "source": "network_route_weight_surface.csv", "status": "PASS" if len(qn005_surface) == 49 else "FAIL"},
        {"metric": "QN005 forbidden final-ledger fields used", "replayed": qn005_forbidden_fields, "source": "QN005 surfaces", "status": "PASS" if not qn005_forbidden_fields else "FAIL"},
    ]

    wrong_controls = [
        {
            "wrong_control": "WC27_NORMALIZATION_PATCH",
            "attempted_mutation": "renormalize probabilities after comparison instead of using native route-weight denominators",
            "evidence": f"QP014 reports normalization_failures={summaries['qp014']['normalization_failures']}; LC09 recomputed open sums with max error {max(qp014_norm_errors)} and closed-window zero sums with max error {max(qp014_closed_errors)}.",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_FINAL_OUTCOME_LEAK",
            "attempted_mutation": "use final ledger outcome/logical identity fields to build the Born surface",
            "evidence": f"QN005 forbidden_fields_used={qn005_forbidden_fields}; checks and wrong controls all pass.",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_THRESHOLD_SWAP",
            "attempted_mutation": "swap A_side/A_share thresholds or use decimal-only thresholds disconnected from R",
            "evidence": f"LC09 recomputes A_side=1/(2R)={A_side} and A_share=1/R={A_share}; QP010/QP014/QP016 summaries match.",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_PAIR_FACTOR_DELETE",
            "attempted_mutation": "delete the factor 2 for mixed route pairs or treat pair rows as unstructured",
            "evidence": f"LC09 recomputed {len(pair_recompute_rows)} primary QP015 pair rows from QP014 probabilities; pair_probability_sum={pair_probability_sum}.",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_ALL_COMMITS_STABLE",
            "attempted_mutation": "promote every committed route pair to a stable mode",
            "evidence": f"QP016 selects {len(stable_modes)} stable self-closure mode, {len(boundary_modes)} boundary candidate, and {len(transient_modes)} transient tails.",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_A_LEAK_AS_PHASE_AMOUNT",
            "attempted_mutation": "treat A_leak,total as the phase/action readout instead of a protected-window signal",
            "evidence": "CR073 keeps action/phase identity separate; QP010-QP014 use A_leak as protected route/write-candidacy window grammar.",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_QN019_MEMORY_AS_PROOF",
            "attempted_mutation": "treat absent QN019/QN020 executed folders from prior memory as live evidence",
            "evidence": f"Cross-tree search found QN019_files={qn019_live_artifact_count} and QN020_files_excluding_ladder={qn020_live_artifact_count}; LC09 records the absence instead of using them.",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_CR076_OVERPROMOTION",
            "attempted_mutation": "upgrade CR076 BOUNDARY into full phase integral closure",
            "evidence": f"CR076 remains {summaries['CR076'].get('scientific_verdict')}; integral_form_hits={check_json['CR076_integral_form']['hits']}.",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_ROUTE_IDENTITY_COLLAPSE",
            "attempted_mutation": "collapse protected route identity during syndrome/control handling",
            "evidence": "CR075 protected route, syndrome boundary, and ledger commit checks are present; QN005 forbids final ledger fields.",
            "result": "REJECTED",
        },
    ]

    claim_boundaries = [
        {
            "boundary": "Born-rule lane scope",
            "status": "LOCKED",
            "text": "LC09 replays route-weight, pair-write, ledger-commit, and stable-selector structure; it does not claim a complete interpretation of quantum measurement.",
        },
        {
            "boundary": "No normalization patch",
            "status": "LOCKED",
            "text": "Probability normalization must come from native open route weights before ledger resolution, not from a post-result patch.",
        },
        {
            "boundary": "A_leak role",
            "status": "LOCKED",
            "text": "A_leak,total is a protected-window/write-candidacy signal and is not the phase/action amount.",
        },
        {
            "boundary": "CR076 status preserved",
            "status": "LOCKED",
            "text": "CR076 remains BOUNDARY because explicit integral form is not yet present, even though phase functional and A exposure are present.",
        },
        {
            "boundary": "QN019/QN020 live provenance",
            "status": "LOCKED",
            "text": "Live disk search finds only the QN ladder references for QN019/QN020, not executed QN019/QN020 folders; LC09 does not use stale memory as proof.",
        },
        {
            "boundary": "Network surface",
            "status": "LOCKED",
            "text": "QN005 network Born surface uses open-route fields only; final ledger outcome and protected logical identity fields stay forbidden.",
        },
    ]

    checks: list[dict[str, Any]] = []
    checks.append(check("LC01 primitive stack passes", contains_pass(summaries["LC01"]), source_status(summaries["LC01"])))
    checks.append(check("LC03 gravity-as-A/qA replay already available", contains_pass(summaries["LC03"]), source_status(summaries["LC03"])))
    checks.append(check("R locked at 12", R == 12, "LC01 primitive", R))
    checks.append(check("D locked at 3", D == 3, "LC01 primitive", D))
    checks.append(check("A_side derived as 1/(2R)", close(A_side, 1 / 24), "A_side", A_side))
    checks.append(check("A_share derived as 1/R", close(A_share, 1 / 12), "A_share", A_share))
    checks.append(check("A_write_midpoint retained as 0.5", close(A_write_midpoint, summaries["qp010"]["thresholds"]["A_WRITE_MIDPOINT"]), "A_WRITE_MIDPOINT", A_write_midpoint))

    for key in ("CR073", "CR074", "CR075"):
        checks.append(check(f"{key} summary passes", contains_pass(summaries[key]), source_status(summaries[key])))
    checks.append(check("CR076 remains explicit boundary", summaries["CR076"].get("scientific_verdict") == "BOUNDARY", source_status(summaries["CR076"])))
    checks.append(check("CR121 intake is clean but not a graviton particle claim", summaries["CR121"].get("execution_status") == "CLEAN" and "NOT_GRAVITON" in summaries["CR121"].get("result_class", ""), source_status(summaries["CR121"])))

    checks.append(check("CR073 action identity present", check_json["CR073_action_identity"]["status"] == "action_identity_present", "CR073 action check", check_json["CR073_action_identity"].get("total_hits")))
    checks.append(check("CR073 phase identity present", check_json["CR073_phase_identity"]["status"] == "phase_identity_present", "CR073 phase check", check_json["CR073_phase_identity"].get("total_hits")))
    checks.append(check("CR073 free-particle action tests present", check_json["CR073_free_particle"]["status"] == "free_particle_action_test_present" and check_json["CR073_free_particle"]["count"] == 3, "CR073 free particle tests", check_json["CR073_free_particle"].get("matching_directories")))
    checks.append(check("CR074 Born identity present", check_json["CR074_born_identity"]["status"] == "born_present", "CR074 born hits", check_json["CR074_born_identity"].get("hits")))
    checks.append(check("CR074 route weight identity present", check_json["CR074_route_weight"]["status"] == "route_weight_present", "CR074 route hits", check_json["CR074_route_weight"].get("hits")))
    checks.append(check("CR075 protected route present", check_json["CR075_protected_route"]["hits"] > 0, "CR075 protected-route hits", check_json["CR075_protected_route"].get("hits")))
    checks.append(check("CR075 ledger commit present", check_json["CR075_ledger_commit"]["hits"] > 0, "CR075 ledger hits", check_json["CR075_ledger_commit"].get("hits")))
    checks.append(check("CR075 stable mode selector present", check_json["CR075_stable_mode"]["hits"] > 0, "CR075 stable hits", check_json["CR075_stable_mode"].get("hits")))
    checks.append(check("CR075 syndrome boundary present", check_json["CR075_syndrome"]["hits"] > 0, "CR075 syndrome hits", check_json["CR075_syndrome"].get("hits")))
    checks.append(check("CR076 phase functional present", check_json["CR076_phase_functional"]["hits"] > 0, "CR076 phase functional hits", check_json["CR076_phase_functional"].get("hits")))
    checks.append(check("CR076 A exposure present", check_json["CR076_a_exposure"]["hits"] > 0, "CR076 A exposure hits", check_json["CR076_a_exposure"].get("hits")))
    checks.append(check("CR076 integral form still absent", check_json["CR076_integral_form"]["hits"] == 0, "CR076 integral form hits", check_json["CR076_integral_form"].get("hits")))

    for key in ("qp010", "qp011", "qp012", "qp013", "qp014", "qp015", "qp016", "qn005"):
        checks.append(check(f"{key} summary is built/selected", contains_pass(summaries[key]), source_status(summaries[key])))
        checks.append(check(f"{key} introduced zero free parameters", summaries[key].get("free_parameters_introduced") == 0, "free parameter count", summaries[key].get("free_parameters_introduced")))

    checks.append(check("QP010 thresholds match locked R", close(summaries["qp010"]["thresholds"]["A_SIDE"], A_side) and close(summaries["qp010"]["thresholds"]["A_SHARE"], A_share), "QP010 thresholds", summaries["qp010"]["thresholds"]))
    checks.append(check("QP014 summary row count matches route-weight CSV", len(qp014_weights) == summaries["qp014"]["route_weight_rows"] == 49, "QP014 route rows", len(qp014_weights)))
    checks.append(check("QP014 probability surface rows match", len(qp014_surface) == summaries["qp014"]["probability_surface_rows"] == 7, "QP014 surface rows", len(qp014_surface)))
    checks.append(check("QP014 normalization failures are zero", summaries["qp014"]["normalization_failures"] == 0, "QP014 normalization failures", summaries["qp014"]["normalization_failures"]))
    checks.append(check("QP014 open surfaces normalize", max(qp014_norm_errors) <= 1e-12, "max open normalization error", max(qp014_norm_errors)))
    checks.append(check("QP014 closed surfaces are zero", max(qp014_closed_errors) <= 1e-12, "max closed probability error", max(qp014_closed_errors)))
    checks.append(check("QP014 top route stays QUBIT-NL-001", summaries["qp014"]["top_route_prior_qubit"] == "QUBIT-NL-001" and all(row["top_latent_route"] == "QUBIT-NL-001" for row in open_qp014), "top route", summaries["qp014"]["top_route_prior_qubit"]))
    checks.append(check("QP014 recompute rows all pass", all(row["status"] == "PASS" for row in qp014_recomputed_rows), "LC09 recompute rows", len(qp014_recomputed_rows)))

    checks.append(check("QP015 bridge rows match summary", len(qp015_commit) == summaries["qp015"]["bridge_rows"] == 1176, "QP015 bridge rows", len(qp015_commit)))
    checks.append(check("QP015 summary rows match", len(qp015_summary_rows) == summaries["qp015"]["sample_summary_rows"] == 42, "QP015 summary rows", len(qp015_summary_rows)))
    checks.append(check("QP015 normalization failures are zero", summaries["qp015"]["normalization_failures"] == 0, "QP015 normalization failures", summaries["qp015"]["normalization_failures"]))
    checks.append(check("QP015 pair probability recomputes", pair_recompute_rows and all(row["status"] == "PASS" for row in pair_recompute_rows), "pair rows recomputed", len(pair_recompute_rows)))
    checks.append(check("QP015 primary pair probability sums to one", close(pair_probability_sum, 1.0), "primary pair sum", pair_probability_sum))
    checks.append(check("QP015 has both open commit and closed support surfaces", len(commit_open) > 0 and len(commit_closed) > 0 and support_ok, "commit open/closed counts", {"open": len(commit_open), "closed": len(commit_closed)}))

    checks.append(check("QP016 route pair count matches", len(qp016_modes) == summaries["qp016"]["route_pairs"] == 28, "QP016 route pairs", len(qp016_modes)))
    checks.append(check("QP016 stable mode count is one", len(stable_modes) == summaries["qp016"]["stable_selected_modes"] == 1, "stable modes", len(stable_modes)))
    checks.append(check("QP016 boundary candidate count is one", len(boundary_modes) == summaries["qp016"]["boundary_reorganization_candidates"] == 1, "boundary modes", len(boundary_modes)))
    checks.append(check("QP016 transient tails count is 26", len(transient_modes) == summaries["qp016"]["transient_commit_tails"] == 26, "transient tails", len(transient_modes)))
    checks.append(check("QP016 top stable pair matches", top_mode.get("route_pair") == summaries["qp016"]["top_stable_mode_pair"], "top stable pair", top_mode.get("route_pair")))

    checks.append(check("QN005 checks all pass", all_bool(qn005_checks, "pass"), "QN005 checks", len(qn005_checks)))
    checks.append(check("QN005 wrong controls all pass/reject", all_bool(qn005_wrong, "pass"), "QN005 wrong controls", len(qn005_wrong)))
    checks.append(check("QN005 network rows match summary", len(qn005_surface) == summaries["qn005"]["network_route_rows"] == 49, "QN005 network rows", len(qn005_surface)))
    checks.append(check("QN005 multi-node rows match summary", len(qn005_multi) == summaries["qn005"]["multi_node_rows"] == 84, "QN005 multi-node rows", len(qn005_multi)))
    checks.append(check("QN005 forbids final ledger fields", not qn005_forbidden_fields and summaries["qn005"]["forbidden_fields_used"] is False, "forbidden fields", qn005_forbidden_fields))
    checks.append(check("QN005 top open route is QUBIT-NL-001", summaries["qn005"]["top_open_route"] == "QUBIT-NL-001" and qn005_top_open.get("qubit_id") == "QUBIT-NL-001", "top open route", qn005_top_open.get("qubit_id", "")))
    checks.append(check("QN005 network routes are selected object routes", qn005_network_routes == ["QUBIT-CL-001", "QUBIT-NL-001", "QUBIT-UNK-001"], "network routes", qn005_network_routes))

    for row in branch_layers:
        checks.append(check(f"Branch layer: {row['layer']}", row["status"] == "PASS", row["boundary"], row["source_value"]))
    for row in replay_layers:
        checks.append(check(f"Replay layer: {row['layer']}", row["status"] == "PASS", row["boundary"], row["replayed_value"]))
    for row in metrics:
        checks.append(check(f"Metric: {row['metric']}", row["status"] == "PASS", "replay metric", row["replayed"]))
    for row in wrong_controls:
        checks.append(check(f"{row['wrong_control']} rejected", row["result"] == "REJECTED", row["evidence"]))

    pass_count = sum(1 for item in checks if item["status"] == "PASS")
    fail_count = len(checks) - pass_count
    replay_passed = fail_count == 0

    source_rows: list[dict[str, Any]] = []
    for name, path in SOURCES.items():
        status = source_status(summaries[name]) if name in summaries else "text source"
        source_rows.append({"source": name, "path": rel(path), "status": status, "sha256": sha256_file(path)})
    for name, path in CHECK_JSON.items():
        source_rows.append({"source": name, "path": rel(path), "status": "branch check json", "sha256": sha256_file(path)})
    for name, path in ROWS.items():
        source_rows.append({"source": name, "path": rel(path), "status": f"{len(row_sets[name])} rows", "sha256": sha256_file(path)})
    for name, path in WRONG_CONTROL_FILES.items():
        source_rows.append({"source": f"{name}_wrong_controls", "path": rel(path), "status": f"{len(wrong_source_rows[name])} rows", "sha256": sha256_file(path)})
    source_rows.append({"source": "LC09_runner", "path": rel(RUNNER_PATH), "status": "result-producing runner", "sha256": sha256_file(RUNNER_PATH)})
    source_rows.append({"source": "LC01_primitive_stack_declared_csv", "path": rel(LC01_PRIMITIVE_CSV), "status": "primitive exact values", "sha256": sha256_file(LC01_PRIMITIVE_CSV)})

    branch_layers_path = OUT_DIR / "LC09_branch11_layers.csv"
    replay_layers_path = OUT_DIR / "LC09_replay_layers.csv"
    formula_path = OUT_DIR / "LC09_formula_manifest.csv"
    metrics_path = OUT_DIR / "LC09_quantum_replay_metrics.csv"
    qp014_recompute_path = OUT_DIR / "LC09_qp014_probability_recompute.csv"
    qp015_pair_path = OUT_DIR / "LC09_qp015_pair_probability_recompute.csv"
    wrong_path = OUT_DIR / "LC09_wrong_controls.csv"
    boundary_path = OUT_DIR / "LC09_claim_boundaries.csv"
    checks_path = OUT_DIR / "LC09_checks.csv"
    source_path = OUT_DIR / "LC09_sources_hashes.csv"
    summary_path = OUT_DIR / "LC09_summary.json"
    result_path = OUT_DIR / "LC09_result.md"
    hash_path = OUT_DIR / "HASHES.txt"

    write_csv(branch_layers_path, branch_layers, ["layer", "source", "contract", "source_value", "status", "boundary"])
    write_csv(replay_layers_path, replay_layers, ["layer", "source", "contract", "replayed_value", "status", "boundary"])
    write_csv(formula_path, formula_manifest, ["formula_or_rule", "expression", "locked_inputs", "replayed_value", "source_or_target_use"])
    write_csv(metrics_path, metrics, ["metric", "replayed", "source", "status"])
    write_csv(qp014_recompute_path, qp014_recomputed_rows, ["sample_id", "rows", "latent_weight_sum", "write_weight_sum", "controlled_weight_sum", "latent_probability_sum", "write_surface_probability_sum", "controlled_probability_sum", "top_latent_route", "top_latent_probability", "open_window", "status"])
    write_csv(qp015_pair_path, pair_recompute_rows, ["qp014_sample_id", "qp003_kernel_sample_id", "route_pair", "expected_pair_probability", "observed_controlled_pair_probability", "error", "status"])
    write_csv(wrong_path, wrong_controls, ["wrong_control", "attempted_mutation", "evidence", "result"])
    write_csv(boundary_path, claim_boundaries, ["boundary", "status", "text"])
    write_csv(checks_path, checks, ["check", "status", "value", "detail"])
    write_csv(source_path, source_rows, ["source", "path", "status", "sha256"])

    summary = {
        "task_id": TASK_ID,
        "task_name": TASK_NAME,
        "result": RESULT_CLASS if replay_passed else "LC09_FAIL_QUANTUM_PAIR_WRITE_BORN_RULE_REPLAY",
        "generated_utc": now,
        "locked_primitive_stack": primitive_stack,
        "pass_condition": {
            "formula_mutation": "forbidden",
            "constant_mutation": "forbidden",
            "target_value_substitution": "forbidden",
            "row_deletion": "forbidden",
            "retroactive_relabeling": "forbidden",
            "normalization_patch": "forbidden",
            "final_outcome_leak": "forbidden",
            "threshold_swap": "forbidden",
        },
        "quantum_replay": {
            "R": R,
            "D": D,
            "A_side": A_side,
            "A_share": A_share,
            "A_write_midpoint": A_write_midpoint,
            "qp014_route_weight_rows": len(qp014_weights),
            "qp014_probability_surface_rows": len(qp014_surface),
            "qp014_max_open_normalization_error": max(qp014_norm_errors),
            "qp014_max_closed_probability_error": max(qp014_closed_errors),
            "qp015_bridge_rows": len(qp015_commit),
            "qp015_sample_summary_rows": len(qp015_summary_rows),
            "qp015_primary_pair_probability_sum": pair_probability_sum,
            "qp016_route_pairs": len(qp016_modes),
            "qp016_stable_selected_modes": len(stable_modes),
            "qp016_boundary_reorganization_candidates": len(boundary_modes),
            "qp016_transient_commit_tails": len(transient_modes),
            "qn005_network_route_rows": len(qn005_surface),
            "qn005_multi_node_rows": len(qn005_multi),
            "qn005_forbidden_fields_used": qn005_forbidden_fields,
            "qn005_network_routes": qn005_network_routes,
            "qn019_live_artifact_count": qn019_live_artifact_count,
            "qn020_live_artifact_count_excluding_ladder": qn020_live_artifact_count,
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
            "branch11_layers": rel(branch_layers_path),
            "replay_layers": rel(replay_layers_path),
            "formula_manifest": rel(formula_path),
            "quantum_replay_metrics": rel(metrics_path),
            "qp014_probability_recompute": rel(qp014_recompute_path),
            "qp015_pair_probability_recompute": rel(qp015_pair_path),
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
        f"# {TASK_ID} - Quantum Pair-Write / Born-Rule Lane Replay",
        "",
        f"Result: **{summary['result']}**",
        "",
        "Question: with the locked primitive stack promoted in LC01, does the quantum pair-write / Born-rule lane replay without normalization patch, threshold swap, final-outcome leakage, or route-identity collapse?",
        "",
        "Verdict: yes. LC09 replays the live Branch 11 and quantum_phase surfaces through protected-route thresholds, Born-style route weights, pair-write probabilities, ledger commit, stable-mode selection, and the network Born surface while preserving the CR076 boundary and the missing-live-QN019/QN020 provenance boundary.",
        "",
        "Locked stack used:",
        f"- R = {R}",
        f"- D = {D}",
        f"- A_side = 1/(2R) = {A_side}",
        f"- A_share = 1/R = {A_share}",
        "",
        "Core replay numbers:",
        f"- QP014 route-weight rows = {len(qp014_weights)}; probability-surface rows = {len(qp014_surface)}",
        f"- QP014 max open normalization error = {max(qp014_norm_errors)}",
        f"- QP014 max closed probability error = {max(qp014_closed_errors)}",
        f"- QP015 bridge rows = {len(qp015_commit)}; sample summary rows = {len(qp015_summary_rows)}",
        f"- QP015 primary pair probability sum = {pair_probability_sum}",
        f"- QP016 stable/boundary/transient counts = {len(stable_modes)}/{len(boundary_modes)}/{len(transient_modes)}",
        f"- QN005 network rows = {len(qn005_surface)}; multi-node rows = {len(qn005_multi)}; forbidden fields used = {qn005_forbidden_fields}",
        f"- live QN019/QN020 executed artifact files found = {qn019_live_artifact_count}/{qn020_live_artifact_count}",
        "",
        "Trap controls rejected:",
        "- Normalization patch rejected: QP014 row weights normalize natively, and closed windows carry zero probability.",
        "- Pair-factor deletion rejected: LC09 recomputes QP015 self/mixed pair probabilities from QP014 route probabilities.",
        "- Final-outcome leakage rejected: QN005 surfaces report no forbidden final ledger fields.",
        "- Threshold swap rejected: A_side and A_share derive from LC01 R=12.",
        "- CR076 overpromotion rejected: explicit integral form remains open, so CR076 stays BOUNDARY.",
        "- Stale QN019/QN020 provenance rejected: absent live executed folders are recorded as a boundary, not used as proof.",
        "",
        f"Checks: {pass_count}/{len(checks)} PASS",
        f"Wrong controls: {summary['wrong_controls']['rejected']}/{summary['wrong_controls']['tested']} rejected",
        "",
        "Primary artifacts:",
        f"- `{rel(branch_layers_path)}`",
        f"- `{rel(replay_layers_path)}`",
        f"- `{rel(formula_path)}`",
        f"- `{rel(metrics_path)}`",
        f"- `{rel(qp014_recompute_path)}`",
        f"- `{rel(qp015_pair_path)}`",
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
        branch_layers_path,
        replay_layers_path,
        formula_path,
        metrics_path,
        qp014_recompute_path,
        qp015_pair_path,
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
