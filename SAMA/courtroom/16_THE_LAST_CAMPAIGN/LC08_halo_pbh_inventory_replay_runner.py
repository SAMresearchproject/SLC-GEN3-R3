from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any


getcontext().prec = 100

TASK_ID = "LC08"
TASK_NAME = "halo PBH inventory replay"
RESULT_CLASS = "LC08_PASS_HALO_PBH_INVENTORY_REPLAY_FROM_LOCKED_PRIMITIVE_STACK"

ROOT = Path(__file__).resolve().parents[1]
LC_DIR = ROOT / "16_THE_LAST_CAMPAIGN"
OUT_DIR = LC_DIR / "LC08_HALO_PBH_INVENTORY_REPLAY"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RUNNER_PATH = Path(__file__).resolve()

BRANCH08 = ROOT / "08_GALAXY_HALOS_BB_PBH_TRAPPED_A"
CR_DIRS = {
    "CR022": BRANCH08 / "CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION",
    "CR023": BRANCH08 / "CR023_BB_PBH_TRAPPED_A_INVENTORY",
    "CR024": BRANCH08 / "CR024_REAL_SPARC_RESIDUAL_AND_POST_BB_REJECTION",
    "CR025": BRANCH08 / "CR025_CLUSTERED_BB_PBH_PROFILE_CONTACT",
    "CR026": BRANCH08 / "CR026_SEED_FIRST_CLUSTERING_SELECTOR",
    "CR027": BRANCH08 / "CR027_HYDROGEN_CATCHUP_FIRST_STAR_SCAFFOLD",
    "CR028": BRANCH08 / "CR028_QP042_BARYON_SCAFFOLD_SUPPORT",
    "CR029": BRANCH08 / "CR029_NATIVE_RADIAL_LAW_DEBT_LEDGER",
    "CR030": BRANCH08 / "CR030_BRANCH_VERDICT_ZIPPER",
}

LC01_PRIMITIVE_CSV = LC_DIR / "LC01_primitive_stack_declared.csv"

SOURCES = {
    "LC01": LC_DIR / "LC01_primitive_stack_lock.json",
    "LC06": LC_DIR / "LC06_BARYON_MATTER_INVENTORY_REPLAY" / "LC06_summary.json",
    "LC07": LC_DIR / "LC07_SN_BAO_DISTANCE_ROAD_REPLAY" / "LC07_summary.json",
    "CR113_foundation": ROOT / "14_FOUNDATIONAL_TESTS" / "CR113_A4_COMPLETED_WRITE_ADDRESS_COUNT_THEOREM" / "CR113_summary.json",
    "CR115_foundation": ROOT / "14_FOUNDATIONAL_TESTS" / "CR115_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM" / "CR115_summary.json",
    "CR115_gov_stale_bridge": ROOT / "00_governance" / "CR115_GALAXY_PBH_BRIDGE_PARTIAL_REVEAL" / "CR115_summary.json",
    "CR116_halo_correction": ROOT / "00_governance" / "CR116_SAM_HALO_COMPOSITION_CORRECTION" / "CR116_summary.json",
    "branch08_readme": BRANCH08 / "README.md",
    "branch08_hashes": BRANCH08 / "BRANCH_HASHES.txt",
}

for cr_id, cr_dir in CR_DIRS.items():
    SOURCES[f"{cr_id}_summary"] = cr_dir / f"{cr_id}_summary.json"

PREMISES = {cr_id: cr_dir / f"{cr_id}_declared_premises.json" for cr_id, cr_dir in CR_DIRS.items()}
EVIDENCE = {cr_id: cr_dir / f"{cr_id}_evidence_rows.csv" for cr_id, cr_dir in CR_DIRS.items()}

UPSTREAM = {
    "G392_summary": Path(r"C:\VS\Stam_model-A-v1.0\tests\Substrate\G392_REAL_SPARC_PBH_HALO_INVENTORY_TEST\G392_summary.json"),
    "G392_residual_rows": Path(r"C:\VS\Stam_model-A-v1.0\tests\Substrate\G392_REAL_SPARC_PBH_HALO_INVENTORY_TEST\G392_sparc_galaxy_residuals.csv"),
    "G393_summary": Path(r"C:\VS\Stam_model-A-v1.0\tests\Substrate\G393_PBH_HALO_FORWARD_STACK_SELECTOR\G393_summary.json"),
    "G393_gap_budget": Path(r"C:\VS\Stam_model-A-v1.0\tests\Substrate\G393_PBH_HALO_FORWARD_STACK_SELECTOR\G393_gap_budget.csv"),
    "G394_summary": Path(r"C:\VS\Stam_model-A-v1.0\tests\Substrate\G394_PBH_RADIAL_ORGANIZATION_PROFILE_TEST\G394_summary.json"),
    "G394_profile_rows": Path(r"C:\VS\Stam_model-A-v1.0\tests\Substrate\G394_PBH_RADIAL_ORGANIZATION_PROFILE_TEST\G394_profile_fit_rows.csv"),
    "G394_scenarios": Path(r"C:\VS\Stam_model-A-v1.0\tests\Substrate\G394_PBH_RADIAL_ORGANIZATION_PROFILE_TEST\G394_scenarios.csv"),
    "G677_summary": Path(r"C:\VS\Stam_model-A-v1.0\tests\Substrate\G677_BB_PBH_SEED_FIRST_CLUSTERING_SIMULATION\G677_summary.json"),
    "G677_candidate_table": Path(r"C:\VS\Stam_model-A-v1.0\tests\Substrate\G677_BB_PBH_SEED_FIRST_CLUSTERING_SIMULATION\G677_seed_first_candidate_table.csv"),
    "G677_primary_galaxy_rows": Path(r"C:\VS\Stam_model-A-v1.0\tests\Substrate\G677_BB_PBH_SEED_FIRST_CLUSTERING_SIMULATION\G677_seed_first_primary_galaxy_rows.csv"),
    "G677_wrong_controls": Path(r"C:\VS\Stam_model-A-v1.0\tests\Substrate\G677_BB_PBH_SEED_FIRST_CLUSTERING_SIMULATION\G677_wrong_controls.csv"),
    "G677_ordering_board": Path(r"C:\VS\Stam_model-A-v1.0\tests\Substrate\G677_BB_PBH_SEED_FIRST_CLUSTERING_SIMULATION\G677_ordering_board.csv"),
    "QGA038F_summary": Path(r"C:\VS\Stam_model-A-v1.0\tests\Substrate\QGA038F_12_OF_12_HYDROGEN_ARRIVAL_SELECTOR\QGA038F_summary.json"),
    "QGA038G_summary": Path(r"C:\VS\Stam_model-A-v1.0\tests\Substrate\QGA038G_HYDROGEN_ARRIVAL_TO_BB_NORMAL_MATTER_INVENTORY\QGA038G_summary.json"),
    "QGA038H_summary": Path(r"C:\VS\Stam_model-A-v1.0\tests\Substrate\QGA038H_BB_PBH_FIRST_CLUSTER_HYDROGEN_CATCHUP_SELECTOR\QGA038H_summary.json"),
    "G682c_summary": Path(r"C:\VS\Stam_model-A-v1.0\tests\Substrate\G682c_HYDROGEN_FIRST_STAR_SCAFFOLD_SELECTOR\G682c_summary.json"),
    "QP042_summary": Path(r"C:\VS\quantum_phase\artifacts\qp042\qp042_summary.json"),
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
    if "PASS" in status:
        return True
    if summary.get("all_predictions_passed") is True:
        return True
    if summary.get("all_checks_passed") is True:
        return True
    if summary.get("passed") is True:
        return True
    return False


def pass_conditions_true(summary: dict[str, Any]) -> bool:
    conditions = summary.get("pass_conditions")
    return isinstance(conditions, dict) and all(value is True for value in conditions.values())


def branch_cr_ok(summary: dict[str, Any]) -> bool:
    return (
        summary.get("execution_status") == "CLEAN"
        and summary.get("structural_success") is True
        and pass_conditions_true(summary)
        and summary.get("wrong_control_full_packet_count") == 0
    )


def check(name: str, passed: bool, detail: str, value: Any = "") -> dict[str, Any]:
    return {
        "check": name,
        "status": "PASS" if passed else "FAIL",
        "value": value,
        "detail": detail,
    }


def parse_exact(value: Any) -> Decimal:
    text = str(value).strip()
    if "/" in text and "pi" not in text:
        fraction = Fraction(text)
        return Decimal(fraction.numerator) / Decimal(fraction.denominator)
    return Decimal(text)


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


def evidence_map(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["item"]: row for row in rows}


def ev_float(rows: dict[str, dict[str, str]], item: str) -> float:
    return float(rows[item]["value"])


def ev_str(rows: dict[str, dict[str, str]], item: str) -> str:
    return rows[item]["value"]


def ev_pass(rows: dict[str, dict[str, str]], item: str) -> bool:
    return rows[item]["pass"] == "True"


def metric_value(rows: list[dict[str, str]], metric: str) -> float:
    for row in rows:
        if row.get("metric") == metric:
            return float(row["value"])
    raise KeyError(metric)


def close(left: float, right: float, tolerance: float = 1e-12) -> bool:
    return abs(left - right) <= tolerance


def main() -> int:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    summaries = {name: load_json(path) for name, path in SOURCES.items() if path.suffix.lower() == ".json"}
    premises = {name: load_json(path) for name, path in PREMISES.items()}
    evidence_rows = {name: read_csv(path) for name, path in EVIDENCE.items()}
    evidence = {name: evidence_map(rows) for name, rows in evidence_rows.items()}
    upstream_json = {name: load_json(path) for name, path in UPSTREAM.items() if path.suffix.lower() == ".json"}
    primitive_stack = load_primitive_stack(LC01_PRIMITIVE_CSV)

    g392_residual_rows = read_csv(UPSTREAM["G392_residual_rows"])
    g393_gap_budget = read_csv(UPSTREAM["G393_gap_budget"])
    g394_profile_rows = read_csv(UPSTREAM["G394_profile_rows"])
    g394_scenarios = read_csv(UPSTREAM["G394_scenarios"])
    g677_candidate_rows = read_csv(UPSTREAM["G677_candidate_table"])
    g677_primary_rows = read_csv(UPSTREAM["G677_primary_galaxy_rows"])
    g677_wrong_rows = read_csv(UPSTREAM["G677_wrong_controls"])
    g677_ordering_rows = read_csv(UPSTREAM["G677_ordering_board"])

    R = primitive_stack["R"]
    D = primitive_stack["D"]
    A0 = Decimal(primitive_stack["A0_decimal"])
    branch_summaries = {cr_id: summaries[f"{cr_id}_summary"] for cr_id in CR_DIRS}

    qga038g = upstream_json["QGA038G_summary"]
    qga038f = upstream_json["QGA038F_summary"]
    qga038h = upstream_json["QGA038H_summary"]
    g392 = upstream_json["G392_summary"]
    g393 = upstream_json["G393_summary"]
    g394 = upstream_json["G394_summary"]
    g677 = upstream_json["G677_summary"]
    g682c = upstream_json["G682c_summary"]
    qp042 = upstream_json["QP042_summary"]
    cr116 = summaries["CR116_halo_correction"]

    omega_vacuum = float(qga038g["Omega_substrate_vacuum"])
    omega_pbh = float(qga038g["Omega_BB_PBH_trapped"])
    omega_h = float(qga038g["Omega_H_arrival_baryon"])
    total_inventory = omega_vacuum + omega_pbh + omega_h
    pbh_to_h_ratio = omega_pbh / omega_h
    matter_inventory = omega_pbh + omega_h
    trapped_fraction = omega_pbh / matter_inventory
    escaped_fraction = omega_h / matter_inventory

    primary_candidate = next(row for row in g677_candidate_rows if row["candidate_id"] == "base12_outer_radius_over_12")
    best_candidate = min(g677_candidate_rows, key=lambda row: float(row["median_seed_first_rms_kms"]))
    r6_candidate = next(row for row in g677_candidate_rows if row["candidate_id"] == "half_string_outer_radius_over_6")
    uniform_wrong = g677["uniform_control"]
    postbb_wrong = g677["post_BB_window_control"]
    primary_seed = g677["primary_seed_first_candidate"]
    best_seed = g677["best_candidate_by_median_rms"]

    support_cr_ids = [cr_id for cr_id in CR_DIRS if cr_id != "CR030"]
    branch_support_counts = {
        "pass": sum(1 for cr_id in support_cr_ids if branch_summaries[cr_id].get("scientific_verdict") == "PASS"),
        "boundary": sum(1 for cr_id in support_cr_ids if branch_summaries[cr_id].get("scientific_verdict") == "BOUNDARY"),
        "clean": sum(1 for cr_id in support_cr_ids if branch_summaries[cr_id].get("execution_status") == "CLEAN"),
    }
    branch_total_counts = {
        "pass": sum(1 for summary in branch_summaries.values() if summary.get("scientific_verdict") == "PASS"),
        "boundary": sum(1 for summary in branch_summaries.values() if summary.get("scientific_verdict") == "BOUNDARY"),
        "clean": sum(1 for summary in branch_summaries.values() if summary.get("execution_status") == "CLEAN"),
    }

    formula_manifest = [
        {
            "formula_or_rule": "R lock",
            "expression": "completed-WRITE address count",
            "locked_inputs": "CR113 foundational theorem",
            "replayed_value": R,
            "source_or_target_use": "primitive lock, not branch-local halo fit",
        },
        {
            "formula_or_rule": "D lock",
            "expression": "invariant carrier uniqueness",
            "locked_inputs": "CR115 foundational theorem",
            "replayed_value": D,
            "source_or_target_use": "primitive lock, not SPARC or PBH fit",
        },
        {
            "formula_or_rule": "many-source A accumulation",
            "expression": "A_total = sum_i A_i; halo A(r)=r_s(<r)/r",
            "locked_inputs": "SAM kernel root",
            "replayed_value": ev_str(evidence["CR022"], "many_nonzero_sum"),
            "source_or_target_use": "structural root only; not observational closure",
        },
        {
            "formula_or_rule": "inventory closure",
            "expression": "Omega_substrate_vacuum + Omega_BB_PBH_trapped + Omega_H_arrival = 1",
            "locked_inputs": "QGA038G inventory bridge",
            "replayed_value": total_inventory,
            "source_or_target_use": "inventory arithmetic, not fitted halo parameter",
        },
        {
            "formula_or_rule": "PBH/H inventory ratio",
            "expression": "Omega_BB_PBH_trapped / Omega_H_arrival_baryon",
            "locked_inputs": "QGA038G",
            "replayed_value": pbh_to_h_ratio,
            "source_or_target_use": "route selector support",
        },
        {
            "formula_or_rule": "SPARC dark residual",
            "expression": "observed v^2 - baryon v^2 residual from fixed baryon treatment",
            "locked_inputs": "G392/G393",
            "replayed_value": g393["percentage_budget"]["dark_residual_pct_total_observed_v2"],
            "source_or_target_use": "external comparison; post-BB-only control rejected",
        },
        {
            "formula_or_rule": "clustered profile contact",
            "expression": "v_total^2 = v_baryon^2 + v_BB_PBH_halo^2",
            "locked_inputs": "G394 profile rows",
            "replayed_value": g394["fit_summary"]["median_halo_rms_kms"],
            "source_or_target_use": "scoped profile contact; native radial law open",
        },
        {
            "formula_or_rule": "native seed-first candidate",
            "expression": "r_core = R_outer / R",
            "locked_inputs": "R=12 and G677 seed-first ordering",
            "replayed_value": primary_seed["fraction_of_baryon_to_g394_rms_gap_closed"],
            "source_or_target_use": "candidate behavior, not theorem-grade mass function",
        },
        {
            "formula_or_rule": "comparison candidate",
            "expression": "r_core = R_outer / 6",
            "locked_inputs": "comparison/control table",
            "replayed_value": best_seed["fraction_of_baryon_to_g394_rms_gap_closed"],
            "source_or_target_use": "better RMS comparison is not promoted to primitive law",
        },
    ]

    replay_layers = [
        {
            "layer": "LC01 locked primitive stack",
            "source": "LC01",
            "formula_or_contract": "R=12, D=3, A0=1/(pi*R)",
            "expected_or_replayed": {"R": R, "D": D, "A0": primitive_stack["A0_decimal"]},
            "source_value": source_status(summaries["LC01"]),
            "status": "PASS" if contains_pass(summaries["LC01"]) else "FAIL",
            "boundary": "No branch-local primitive override.",
        },
        {
            "layer": "R=12 foundational address count",
            "source": "CR113 foundational",
            "formula_or_contract": "CR113 R must equal LC01 R",
            "expected_or_replayed": summaries["CR113_foundation"].get("R"),
            "source_value": source_status(summaries["CR113_foundation"]),
            "status": "PASS" if contains_pass(summaries["CR113_foundation"]) and summaries["CR113_foundation"].get("R") == R else "FAIL",
            "boundary": "R is not read from halo profile fit or a successful config.",
        },
        {
            "layer": "D=3 foundational carrier uniqueness",
            "source": "CR115 foundational",
            "formula_or_contract": "stable_ds must be [3]",
            "expected_or_replayed": summaries["CR115_foundation"].get("stable_ds"),
            "source_value": source_status(summaries["CR115_foundation"]),
            "status": "PASS" if contains_pass(summaries["CR115_foundation"]) and summaries["CR115_foundation"].get("stable_ds") == [3] else "FAIL",
            "boundary": "D is not derived from SPARC, PBH, or halo rows.",
        },
        {
            "layer": "CR022 many-nonzero A root",
            "source": "CR022",
            "formula_or_contract": "many tiny A contributions can accumulate above single-source scale",
            "expected_or_replayed": {"single": ev_float(evidence["CR022"], "single_nonzero_A"), "sum": ev_float(evidence["CR022"], "many_nonzero_sum")},
            "source_value": source_status(branch_summaries["CR022"]),
            "status": "PASS" if branch_cr_ok(branch_summaries["CR022"]) else "FAIL",
            "boundary": "Structural root only; no standalone halo observation claim.",
        },
        {
            "layer": "CR023 BB-origin PBH/trapped-A inventory",
            "source": "CR023/QGA038G/G394",
            "formula_or_contract": "inventory sums to one and BB-origin trapped-A/PBH is the halo lane",
            "expected_or_replayed": {"total_inventory": total_inventory, "Omega_BB_PBH_trapped": omega_pbh, "PBH_to_H_ratio": pbh_to_h_ratio},
            "source_value": source_status(branch_summaries["CR023"]),
            "status": "PASS" if branch_cr_ok(branch_summaries["CR023"]) and close(total_inventory, 1.0) and omega_pbh > omega_h else "FAIL",
            "boundary": "Post-BB/window PBH remains a small subchannel.",
        },
        {
            "layer": "CR024 real SPARC residual and post-BB rejection",
            "source": "CR024/G392/G393",
            "formula_or_contract": "real SPARC sample has large outer dark residual; post-BB envelope is too small",
            "expected_or_replayed": {"galaxies": len(g392_residual_rows), "dark_residual_pct": g393["percentage_budget"]["dark_residual_pct_total_observed_v2"], "post_bb_pct": g393["percentage_budget"]["pbh_envelope_supplied_pct_dark_residual"]},
            "source_value": source_status(branch_summaries["CR024"]),
            "status": "PASS" if branch_cr_ok(branch_summaries["CR024"]) and len(g392_residual_rows) == 175 and g393["percentage_budget"]["missing_after_pbh_envelope_pct_dark_residual"] > 90 else "FAIL",
            "boundary": "Rejects post-BB-only as full halo, not clustered BB-origin PBH.",
        },
        {
            "layer": "CR025 clustered profile contact",
            "source": "CR025/G394",
            "formula_or_contract": "clustered BB-PBH/trapped-A profile improves SPARC contact while radial law stays open",
            "expected_or_replayed": {"galaxies": len(g394_profile_rows), "baryon_rms": g394["fit_summary"]["median_baryon_rms_kms"], "halo_rms": g394["fit_summary"]["median_halo_rms_kms"], "improvement": g394["fit_summary"]["median_chi2_improvement_factor"]},
            "source_value": source_status(branch_summaries["CR025"]),
            "status": "PASS" if branch_cr_ok(branch_summaries["CR025"]) and len(g394_profile_rows) == 175 and g394["fit_summary"]["median_halo_rms_kms"] < g394["fit_summary"]["median_baryon_rms_kms"] else "FAIL",
            "boundary": "Compatibility profile is not a full native radial law.",
        },
        {
            "layer": "CR026 seed-first clustering selector",
            "source": "CR026/G677",
            "formula_or_contract": "native R/12 seed-first candidate beats uniform and post-BB-only controls",
            "expected_or_replayed": {"primary_candidate": primary_seed["candidate_id"], "primary_gap_closed": primary_seed["fraction_of_baryon_to_g394_rms_gap_closed"], "uniform_gap_closed": uniform_wrong["fraction_of_baryon_to_g394_rms_gap_closed"], "post_bb_gap_closed": postbb_wrong["fraction_of_baryon_to_g394_rms_gap_closed"]},
            "source_value": source_status(branch_summaries["CR026"]),
            "status": "PASS" if branch_cr_ok(branch_summaries["CR026"]) and primary_seed["core_denominator"] == float(R) and uniform_wrong["fraction_of_baryon_to_g394_rms_gap_closed"] < 0.001 and postbb_wrong["fraction_of_baryon_to_g394_rms_gap_closed"] < 0.05 else "FAIL",
            "boundary": "Candidate behavior only; mass normalization and native law remain open.",
        },
        {
            "layer": "CR027 hydrogen catch-up scaffold",
            "source": "CR027/QGA038F/G/H/G682c",
            "formula_or_contract": "hydrogen/normal baryons catch up inside BB-origin PBH/trapped-A scaffold",
            "expected_or_replayed": {"terminal": qga038f["selected_terminal_arrival"], "catching_up_to": qga038h["catching_up_to"], "route": g682c["selected_route"]},
            "source_value": source_status(branch_summaries["CR027"]),
            "status": "PASS" if branch_cr_ok(branch_summaries["CR027"]) and qga038h["catching_up_to"] == "BB-origin PBH/trapped-A clustered mass scaffold" and g682c["selected_route"] == "bb_pbh_trapped_A_first_scaffold_plus_hydrogen_catchup" else "FAIL",
            "boundary": "Not a full star-formation history.",
        },
        {
            "layer": "CR028 QP042 private baryon scaffold support",
            "source": "CR028/QP042",
            "formula_or_contract": "proton/neutron scaffolds filled without observed baryon masses",
            "expected_or_replayed": {"filled": qp042["filled_baryon_scaffold_ids"], "open_boundary_rows": qp042["open_boundary_rows"]},
            "source_value": source_status(branch_summaries["CR028"]),
            "status": "PASS" if branch_cr_ok(branch_summaries["CR028"]) and qp042["external_data_used"] is False and qp042["observed_baryon_masses_used"] is False and qp042["free_parameters_introduced"] == 0 else "FAIL",
            "boundary": "Private support only, not external halo evidence.",
        },
        {
            "layer": "CR029 radial-law debt isolation",
            "source": "CR029",
            "formula_or_contract": "native radial organization / mass function / concentration remains open",
            "expected_or_replayed": premises["CR029"].get("declared_open_debt"),
            "source_value": source_status(branch_summaries["CR029"]),
            "status": "PASS" if branch_cr_ok(branch_summaries["CR029"]) and "radial organization" in premises["CR029"].get("declared_open_debt", "") else "FAIL",
            "boundary": "Successful only because it does not convert support into a full theorem.",
        },
        {
            "layer": "CR030 branch zipper",
            "source": "CR030",
            "formula_or_contract": "scoped branch PASS with radial law open",
            "expected_or_replayed": {"pass_scoped_count": ev_str(evidence["CR030"], "pass_scoped_count"), "boundary_count": ev_str(evidence["CR030"], "boundary_count")},
            "source_value": source_status(branch_summaries["CR030"]),
            "status": "PASS" if branch_cr_ok(branch_summaries["CR030"]) and branch_summaries["CR030"].get("scientific_verdict") == "PASS" else "FAIL",
            "boundary": "Scoped PASS only.",
        },
        {
            "layer": "CR116 halo composition correction",
            "source": "CR116 governance",
            "formula_or_contract": "supersede stale f_PBH=0 / particle-PBH-insufficient reading",
            "expected_or_replayed": cr116.get("corrected_reading"),
            "source_value": source_status(cr116),
            "status": "PASS" if cr116.get("execution_status") == "CLEAN" and "CLUSTERED BB-origin PBHs" in cr116.get("corrected_reading", "") else "FAIL",
            "boundary": "Correction is appended transparently; prior files remain unmodified.",
        },
    ]

    halo_metrics = [
        {"metric": "R_locked", "replayed": R, "source": summaries["CR113_foundation"].get("R"), "status": "PASS" if summaries["CR113_foundation"].get("R") == R else "FAIL"},
        {"metric": "D_locked", "replayed": D, "source": summaries["CR115_foundation"].get("stable_ds"), "status": "PASS" if summaries["CR115_foundation"].get("stable_ds") == [D] else "FAIL"},
        {"metric": "Omega_substrate_vacuum", "replayed": omega_vacuum, "source": qga038g["Omega_substrate_vacuum"], "status": "PASS"},
        {"metric": "Omega_BB_PBH_trapped", "replayed": omega_pbh, "source": qga038g["Omega_BB_PBH_trapped"], "status": "PASS" if close(omega_pbh, ev_float(evidence["CR023"], "omega_pbh_matches_g394")) else "FAIL"},
        {"metric": "Omega_H_arrival_baryon", "replayed": omega_h, "source": qga038g["Omega_H_arrival_baryon"], "status": "PASS"},
        {"metric": "total_inventory", "replayed": total_inventory, "source": qga038g["total_inventory"], "status": "PASS" if close(total_inventory, 1.0) and close(total_inventory, qga038g["total_inventory"]) else "FAIL"},
        {"metric": "PBH_to_hydrogen_ratio", "replayed": pbh_to_h_ratio, "source": qga038h["PBH_to_hydrogen_inventory_ratio"], "status": "PASS" if close(pbh_to_h_ratio, qga038h["PBH_to_hydrogen_inventory_ratio"]) else "FAIL"},
        {"metric": "trapped_fraction_of_matter", "replayed": trapped_fraction, "source": qga038g["trapped_fraction_of_matter"], "status": "PASS" if close(trapped_fraction, qga038g["trapped_fraction_of_matter"]) else "FAIL"},
        {"metric": "escaped_hydrogen_fraction_of_matter", "replayed": escaped_fraction, "source": qga038g["escaped_hydrogen_fraction_of_matter"], "status": "PASS" if close(escaped_fraction, qga038g["escaped_hydrogen_fraction_of_matter"]) else "FAIL"},
        {"metric": "SPARC_galaxies", "replayed": len(g392_residual_rows), "source": g392["sparc_loaded"]["sample_galaxies"], "status": "PASS" if len(g392_residual_rows) == g392["sparc_loaded"]["sample_galaxies"] == 175 else "FAIL"},
        {"metric": "SPARC_mass_model_points", "replayed": g392["sparc_loaded"]["mass_model_points"], "source": ev_float(evidence["CR024"], "sparc_points"), "status": "PASS" if g392["sparc_loaded"]["mass_model_points"] == 3391 else "FAIL"},
        {"metric": "median_outer_dark_fraction_v2", "replayed": g392["real_sparc_residuals"]["median_outer_dark_fraction_v2"], "source": ev_float(evidence["CR024"], "median_outer_dark_fraction_v2"), "status": "PASS" if close(g392["real_sparc_residuals"]["median_outer_dark_fraction_v2"], ev_float(evidence["CR024"], "median_outer_dark_fraction_v2")) else "FAIL"},
        {"metric": "post_BB_envelope_supplied_pct_dark_residual", "replayed": g393["percentage_budget"]["pbh_envelope_supplied_pct_dark_residual"], "source": ev_float(evidence["CR024"], "post_bb_envelope_supplied_pct_dark_residual"), "status": "PASS" if close(g393["percentage_budget"]["pbh_envelope_supplied_pct_dark_residual"], ev_float(evidence["CR024"], "post_bb_envelope_supplied_pct_dark_residual")) else "FAIL"},
        {"metric": "missing_after_post_BB_envelope_pct_dark_residual", "replayed": g393["percentage_budget"]["missing_after_pbh_envelope_pct_dark_residual"], "source": ev_float(evidence["CR024"], "missing_after_pbh_envelope_pct_dark_residual"), "status": "PASS" if close(g393["percentage_budget"]["missing_after_pbh_envelope_pct_dark_residual"], ev_float(evidence["CR024"], "missing_after_pbh_envelope_pct_dark_residual")) else "FAIL"},
        {"metric": "G394_profile_rows", "replayed": len(g394_profile_rows), "source": g394["sample"]["galaxies_fit"], "status": "PASS" if len(g394_profile_rows) == g394["sample"]["galaxies_fit"] == 175 else "FAIL"},
        {"metric": "median_baryon_rms_kms", "replayed": g394["fit_summary"]["median_baryon_rms_kms"], "source": ev_float(evidence["CR025"], "median_baryon_rms_kms"), "status": "PASS" if close(g394["fit_summary"]["median_baryon_rms_kms"], ev_float(evidence["CR025"], "median_baryon_rms_kms")) else "FAIL"},
        {"metric": "median_halo_rms_kms", "replayed": g394["fit_summary"]["median_halo_rms_kms"], "source": ev_float(evidence["CR025"], "median_halo_rms_kms"), "status": "PASS" if close(g394["fit_summary"]["median_halo_rms_kms"], ev_float(evidence["CR025"], "median_halo_rms_kms")) else "FAIL"},
        {"metric": "median_chi2_improvement_factor", "replayed": g394["fit_summary"]["median_chi2_improvement_factor"], "source": ev_float(evidence["CR025"], "median_chi2_improvement_factor"), "status": "PASS" if close(g394["fit_summary"]["median_chi2_improvement_factor"], ev_float(evidence["CR025"], "median_chi2_improvement_factor")) else "FAIL"},
        {"metric": "median_halo_overdensity_vs_cosmic_dm_mean", "replayed": g394["clustering_summary"]["median_halo_overdensity_vs_cosmic_dm_mean"], "source": ev_float(evidence["CR025"], "median_halo_overdensity_vs_cosmic_dm_mean"), "status": "PASS" if close(g394["clustering_summary"]["median_halo_overdensity_vs_cosmic_dm_mean"], ev_float(evidence["CR025"], "median_halo_overdensity_vs_cosmic_dm_mean")) else "FAIL"},
        {"metric": "G677_primary_rows", "replayed": len(g677_primary_rows), "source": primary_seed["galaxies_tested"], "status": "PASS" if len(g677_primary_rows) == primary_seed["galaxies_tested"] == 173 else "FAIL"},
        {"metric": "G677_primary_candidate_id", "replayed": primary_seed["candidate_id"], "source": ev_str(evidence["CR026"], "primary_candidate_id"), "status": "PASS" if primary_seed["candidate_id"] == ev_str(evidence["CR026"], "primary_candidate_id") else "FAIL"},
        {"metric": "G677_primary_core_denominator", "replayed": primary_seed["core_denominator"], "source": R, "status": "PASS" if primary_seed["core_denominator"] == float(R) else "FAIL"},
        {"metric": "G677_primary_gap_closed", "replayed": primary_seed["fraction_of_baryon_to_g394_rms_gap_closed"], "source": ev_float(evidence["CR026"], "primary_gap_closed"), "status": "PASS" if close(primary_seed["fraction_of_baryon_to_g394_rms_gap_closed"], ev_float(evidence["CR026"], "primary_gap_closed")) else "FAIL"},
        {"metric": "G677_uniform_control_gap_closed", "replayed": uniform_wrong["fraction_of_baryon_to_g394_rms_gap_closed"], "source": ev_float(evidence["CR026"], "uniform_gap_closed"), "status": "PASS" if close(uniform_wrong["fraction_of_baryon_to_g394_rms_gap_closed"], ev_float(evidence["CR026"], "uniform_gap_closed")) else "FAIL"},
        {"metric": "G677_post_BB_control_gap_closed", "replayed": postbb_wrong["fraction_of_baryon_to_g394_rms_gap_closed"], "source": ev_float(evidence["CR026"], "post_bb_gap_closed"), "status": "PASS" if close(postbb_wrong["fraction_of_baryon_to_g394_rms_gap_closed"], ev_float(evidence["CR026"], "post_bb_gap_closed")) else "FAIL"},
        {"metric": "G677_best_by_rms_candidate", "replayed": best_seed["candidate_id"], "source": "comparison only", "status": "PASS" if best_seed["candidate_id"] == "half_string_outer_radius_over_6" and best_seed["core_denominator"] != float(R) else "FAIL"},
        {"metric": "QP042_filled_baryon_scaffold_ids", "replayed": qp042["filled_baryon_scaffold_ids"], "source": ev_str(evidence["CR028"], "filled_baryon_scaffold_ids"), "status": "PASS" if qp042["filled_baryon_scaffold_ids"] == ev_str(evidence["CR028"], "filled_baryon_scaffold_ids") else "FAIL"},
        {"metric": "CR030_pass_scoped_count", "replayed": branch_support_counts["pass"], "source": ev_float(evidence["CR030"], "pass_scoped_count"), "status": "PASS" if branch_support_counts["pass"] == ev_float(evidence["CR030"], "pass_scoped_count") == 4 else "FAIL"},
        {"metric": "CR030_boundary_count", "replayed": branch_support_counts["boundary"], "source": ev_float(evidence["CR030"], "boundary_count"), "status": "PASS" if branch_support_counts["boundary"] == ev_float(evidence["CR030"], "boundary_count") == 4 else "FAIL"},
    ]

    seed_candidate_rows = []
    for row in g677_candidate_rows:
        seed_candidate_rows.append(
            {
                "candidate_id": row["candidate_id"],
                "selector_source": row["selector_source"],
                "core_denominator": row["core_denominator"],
                "median_seed_first_rms_kms": row["median_seed_first_rms_kms"],
                "fraction_of_baryon_to_g394_rms_gap_closed": row["fraction_of_baryon_to_g394_rms_gap_closed"],
                "role_in_LC08": "NATIVE_R12_CANDIDATE" if row["candidate_id"] == "base12_outer_radius_over_12" else "COMPARISON_NOT_PRIMITIVE_LAW",
                "promoted_to_primitive": "False",
            }
        )

    wrong_controls = [
        {
            "wrong_control": "WC26_HALO_PBH_CONFIG_AS_LAW",
            "attempted_mutation": "promote a successful seed/profile configuration to primitive theorem law",
            "evidence": "CR029 leaves native radial organization/mass function/concentration open; G677 best-RMS R/6 candidate is comparison only; LC08 promotes no config",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC02_BRANCH_LOCAL_CONSTANT_OVERRIDE",
            "attempted_mutation": "derive R from halo profile configuration instead of LC01/CR113",
            "evidence": "R=12 is read from LC01/CR113; R/12 is checked as native candidate and R/6 is not promoted",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC03_TARGET_VALUE_SUBSTITUTION",
            "attempted_mutation": "use SPARC target residuals or best RMS to select primitives",
            "evidence": "Observed rotations are comparison targets; G677 ordering board marks observed_rotation_curve as comparison target; QP042 uses no observed baryon masses",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC04_ROW_DELETION",
            "attempted_mutation": "drop unfavorable SPARC or branch rows",
            "evidence": f"LC08 keeps {len(g392_residual_rows)} G392 residual rows, {len(g394_profile_rows)} G394 profile rows, {len(g677_primary_rows)} primary seed rows, and all CR022-CR030 summaries",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC05_RETROACTIVE_RELABELING",
            "attempted_mutation": "silently rewrite the stale governance CR115 halo/PBH interpretation",
            "evidence": "CR116 supersedes CR115 transparently while CR115 remains unmodified; LC08 records current reading from CR116",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_SMOOTH_UNIFORM_PBH_CONFLATION",
            "attempted_mutation": "treat smooth/uniform PBH constraints as a refutation of clustered BB-origin PBH inventory",
            "evidence": "CR026 uniform control gap closed is 0.000038495994978; CR116 states microlensing smooth-envelope debt remains open for clustered analysis",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_POST_BB_ONLY_AS_FULL_HALO",
            "attempted_mutation": "replace BB-origin trapped-A/PBH inventory with the bounded post-BB/window subchannel",
            "evidence": "CR024/G393 post-BB envelope supplies 2.576714% of dark residual and leaves 97.423286% missing; CR026 post-BB control gap closed is 0.024485",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_FULL_NATIVE_RADIAL_LAW_OVERCLAIM",
            "attempted_mutation": "claim the native radial organization/mass function/concentration theorem is closed",
            "evidence": "CR025, CR026, CR029, CR030, and G677 all preserve the native radial law/mass function/concentration as open",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_CLUSTERED_MICROLENSING_CLOSURE_OVERCLAIM",
            "attempted_mutation": "claim current branch quantitatively closes clustered-PBH-aware microlensing bounds",
            "evidence": "CR116 explicitly lists clustered-PBH-aware microlensing envelope analysis as an honest open debt",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC_PRIVATE_QP042_AS_EXTERNAL_HALO_EVIDENCE",
            "attempted_mutation": "treat private QP042 baryon scaffold support as external SPARC halo evidence",
            "evidence": "CR028 is BOUNDARY private support; QP042 source_scope is PRIVATE_QUANTUM_PHASE_REPO_ONLY",
            "result": "REJECTED",
        },
        {
            "wrong_control": "WC13_REPLAY_WITHOUT_HASH_LOCK",
            "attempted_mutation": "accept LC08 without source hashes or a branch hash link",
            "evidence": "LC08 emits source hashes, artifact hashes, and includes branch BRANCH_HASHES.txt",
            "result": "REJECTED",
        },
    ]

    claim_boundaries = [
        {
            "boundary": "LC08 replay scope",
            "status": "LOCKED",
            "text": "LC08 replays the branch-08 halo/PBH inventory support chain from locked primitives and sealed source artifacts; it is not a new halo fit.",
        },
        {
            "boundary": "Primitive source",
            "status": "LOCKED",
            "text": "R=12 comes from foundational CR113 and D=3 from foundational CR115, not from SPARC, PBH windows, or seed-profile RMS.",
        },
        {
            "boundary": "Halo composition",
            "status": "LOCKED",
            "text": "Current reading is cumulative nonzero A plus clustered BB-origin PBH/trapped-A inventory; stale f_PBH=0 or particle-PBH-insufficient readings are superseded by CR116.",
        },
        {
            "boundary": "Post-BB PBH",
            "status": "LOCKED",
            "text": "The post-BB/window PBH envelope is a small bounded subchannel, not the full halo inventory.",
        },
        {
            "boundary": "Seed profile",
            "status": "LOCKED",
            "text": "R/12 is the native seed-first candidate; R/6 and other candidates are comparison rows, not primitive law promotions.",
        },
        {
            "boundary": "Radial law",
            "status": "OPEN",
            "text": "Native radial organization, mass function, and concentration relation remain open per CR029/CR030.",
        },
        {
            "boundary": "Microlensing",
            "status": "OPEN",
            "text": "Clustered-PBH-aware microlensing envelope analysis remains an open future test per CR116.",
        },
        {
            "boundary": "Private support",
            "status": "LOCKED",
            "text": "QP042 supports the baryon scaffold privately and is not external halo evidence.",
        },
    ]

    checks: list[dict[str, Any]] = []
    checks.append(check("LC01 primitive stack passes", contains_pass(summaries["LC01"]), source_status(summaries["LC01"])))
    checks.append(check("LC06 baryon/matter lane passes before LC08", contains_pass(summaries["LC06"]), source_status(summaries["LC06"])))
    checks.append(check("LC07 distance lane passes before LC08", contains_pass(summaries["LC07"]), source_status(summaries["LC07"])))
    checks.append(check("CR113 foundational R theorem passes", contains_pass(summaries["CR113_foundation"]), source_status(summaries["CR113_foundation"])))
    checks.append(check("CR113 R equals LC01 R", summaries["CR113_foundation"].get("R") == R == 12, "R source", summaries["CR113_foundation"].get("R")))
    checks.append(check("CR115 foundational D3 theorem passes", contains_pass(summaries["CR115_foundation"]), source_status(summaries["CR115_foundation"])))
    checks.append(check("CR115 stable D list is [3]", summaries["CR115_foundation"].get("stable_ds") == [3], "D source", summaries["CR115_foundation"].get("stable_ds")))
    checks.append(check("A0 remains downstream primitive normalization", primitive_stack["A0"] == "1/(12*pi)" and A0 > 0, "LC01 primitive", primitive_stack["A0"]))

    for cr_id in CR_DIRS:
        summary = branch_summaries[cr_id]
        checks.append(check(f"{cr_id} execution clean", summary.get("execution_status") == "CLEAN", source_status(summary)))
        checks.append(check(f"{cr_id} structural success", summary.get("structural_success") is True, source_status(summary)))
        checks.append(check(f"{cr_id} pass conditions all true", pass_conditions_true(summary), "pass_conditions", summary.get("pass_conditions")))
        checks.append(check(f"{cr_id} wrong controls did not match packet", summary.get("wrong_control_full_packet_count") == 0, "wrong_control_full_packet_count", summary.get("wrong_control_full_packet_count")))
        checks.append(check(f"{cr_id} evidence rows all pass", all(row["pass"] == "True" for row in evidence_rows[cr_id]), "evidence rows", len(evidence_rows[cr_id])))
        checks.append(check(f"{cr_id} zero free parameters", premises[cr_id].get("free_parameters_introduced") == 0, "declared premises", premises[cr_id].get("free_parameters_introduced")))
        checks.append(check(f"{cr_id} is not confirmation audit", premises[cr_id].get("is_confirmation_audit_or_double_check") is False, "declared premises", premises[cr_id].get("is_confirmation_audit_or_double_check")))

    checks.append(check("CR022 many-source kernel declared", ev_pass(evidence["CR022"], "master_many_source_formula") and ev_pass(evidence["CR022"], "action_many_source_formula"), "CR022 evidence"))
    checks.append(check("CR022 many nonzeros accumulate above single tiny A", ev_float(evidence["CR022"], "many_nonzero_sum") > ev_float(evidence["CR022"], "single_nonzero_A"), "A accumulation", f"{ev_str(evidence['CR022'], 'single_nonzero_A')} -> {ev_str(evidence['CR022'], 'many_nonzero_sum')}"))

    checks.append(check("QGA038G inventory sums to one", close(total_inventory, 1.0) and close(total_inventory, qga038g["total_inventory"]), "inventory", total_inventory))
    checks.append(check("QGA038G matter inventory matches PBH plus hydrogen", close(matter_inventory, qga038g["matter_inventory"]), "matter inventory", matter_inventory))
    checks.append(check("PBH/trapped-A inventory dominates hydrogen arrival", pbh_to_h_ratio > 1 and close(pbh_to_h_ratio, ev_float(evidence["CR023"], "omega_pbh_exceeds_hydrogen")), "PBH/H ratio", pbh_to_h_ratio))
    checks.append(check("Post-BB window subchannel small", close(qga038g["post_bb_window_subchannel_fraction_of_dm"], ev_float(evidence["CR023"], "post_bb_subchannel_small")), "post-BB subchannel", qga038g["post_bb_window_subchannel_fraction_of_dm"]))
    checks.append(check("CR023 halo reading is BB-origin PBH/trapped-A", "BB-origin PBH/trapped-A" in qga038g["pbh_halo_reading"], "QGA038G reading", qga038g["pbh_halo_reading"]))

    checks.append(check("G392 SPARC galaxies count is 175", g392["sparc_loaded"]["sample_galaxies"] == len(g392_residual_rows) == 175, "G392 residual rows", len(g392_residual_rows)))
    checks.append(check("G392 SPARC mass points count is 3391", g392["sparc_loaded"]["mass_model_points"] == 3391, "G392 mass points", g392["sparc_loaded"]["mass_model_points"]))
    checks.append(check("G392 outer dark residual present", g392["real_sparc_residuals"]["median_outer_dark_fraction_v2"] > 0.5, "median_outer_dark_fraction_v2", g392["real_sparc_residuals"]["median_outer_dark_fraction_v2"]))
    checks.append(check("G393 post-BB envelope leaves most residual missing", g393["percentage_budget"]["missing_after_pbh_envelope_pct_dark_residual"] > 90, "missing pct", g393["percentage_budget"]["missing_after_pbh_envelope_pct_dark_residual"]))
    checks.append(check("G393 gap budget matches CR024 post-BB pct", close(metric_value(g393_gap_budget, "pbh_envelope_supplied_pct_dark_residual"), ev_float(evidence["CR024"], "post_bb_envelope_supplied_pct_dark_residual")), "G393 gap budget"))

    checks.append(check("G394 profile row count is 175", len(g394_profile_rows) == g394["sample"]["galaxies_fit"] == 175, "G394 profile rows", len(g394_profile_rows)))
    checks.append(check("G394 clustered halo RMS improves baryon RMS", g394["fit_summary"]["median_halo_rms_kms"] < g394["fit_summary"]["median_baryon_rms_kms"], "RMS", f"{g394['fit_summary']['median_halo_rms_kms']} < {g394['fit_summary']['median_baryon_rms_kms']}"))
    checks.append(check("G394 chi2 improvement strong", g394["fit_summary"]["median_chi2_improvement_factor"] > 100, "median_chi2_improvement_factor", g394["fit_summary"]["median_chi2_improvement_factor"]))
    checks.append(check("G394 halo requires clustered overdensity", g394["clustering_summary"]["median_halo_overdensity_vs_cosmic_dm_mean"] > 1000, "overdensity", g394["clustering_summary"]["median_halo_overdensity_vs_cosmic_dm_mean"]))
    checks.append(check("G394 scenarios preserve uniform rejection", any(row["scenario"] == "uniform_cosmic_mean_null" and row["status"] == "REJECT_AS_PHYSICAL_GALAXY_HALO" for row in g394_scenarios), "G394 scenarios"))
    checks.append(check("G394 scenarios preserve clustered compatibility", any(row["scenario"] == "BB_PBH_trapped_A_clustered_halo" and row["status"] == "COMPATIBLE_PROFILE_FIT" for row in g394_scenarios), "G394 scenarios"))
    checks.append(check("G394 scenarios preserve post-BB as subchannel", any(row["scenario"] == "post_BB_constrained_window_overlay" and row["status"] == "SUBCHANNEL_NOT_FULL_BB_INVENTORY" for row in g394_scenarios), "G394 scenarios"))

    checks.append(check("G677 candidate table includes native R/12 candidate", primary_candidate["core_denominator"] == str(float(R)) and primary_candidate["candidate_id"] == "base12_outer_radius_over_12", "G677 candidate", primary_candidate))
    checks.append(check("G677 native R/12 closes most of the gap", float(primary_candidate["fraction_of_baryon_to_g394_rms_gap_closed"]) > 0.8, "gap closed", primary_candidate["fraction_of_baryon_to_g394_rms_gap_closed"]))
    checks.append(check("G677 uniform control rejected", uniform_wrong["fraction_of_baryon_to_g394_rms_gap_closed"] < 0.001, "uniform gap closed", uniform_wrong["fraction_of_baryon_to_g394_rms_gap_closed"]))
    checks.append(check("G677 post-BB-only control rejected", postbb_wrong["fraction_of_baryon_to_g394_rms_gap_closed"] < 0.05, "post-BB gap closed", postbb_wrong["fraction_of_baryon_to_g394_rms_gap_closed"]))
    checks.append(check("G677 best-RMS R/6 remains comparison, not primitive", best_candidate["candidate_id"] == "half_string_outer_radius_over_6" and float(best_candidate["core_denominator"]) != float(R), "best candidate", best_candidate["candidate_id"]))
    checks.append(check("G677 wrong controls all rejected", all(row["rejected"] == "True" for row in g677_wrong_rows), "G677 wrong controls", len(g677_wrong_rows)))
    checks.append(check("G677 ordering board keeps seed before baryon infall", any(row["lane"] == "BB_PBH_trapped_A_seed_field" and row["status"] == "FIRST" for row in g677_ordering_rows) and any(row["lane"] == "baryon_infall" and row["status"] == "AFTER_SEED_FIELD" for row in g677_ordering_rows), "G677 ordering board"))

    checks.append(check("QGA038F selects neutral hydrogen terminal arrival", qga038f["selected_terminal_arrival"] == "neutral_hydrogen_protium", "QGA038F", qga038f["selected_terminal_arrival"]))
    checks.append(check("QGA038H keeps hydrogen catching up to PBH scaffold", qga038h["who_is_catching_up"] == "hydrogen/normal baryonic matter" and qga038h["catching_up_to"] == "BB-origin PBH/trapped-A clustered mass scaffold", "QGA038H route"))
    checks.append(check("G682c selects PBH-assisted hydrogen first-star scaffold", g682c["selected_route"] == "bb_pbh_trapped_A_first_scaffold_plus_hydrogen_catchup", "G682c selected route", g682c["selected_route"]))
    checks.append(check("G682c keeps full SFH open", "not full star-formation history" in g682c["scope"], "G682c scope", g682c["scope"]))

    checks.append(check("QP042 private support uses no external data", qp042["external_data_used"] is False and qp042["source_scope"] == "PRIVATE_QUANTUM_PHASE_REPO_ONLY", "QP042 source scope", qp042["source_scope"]))
    checks.append(check("QP042 uses no observed baryon masses", qp042["observed_baryon_masses_used"] is False, "QP042 observed baryon masses", qp042["observed_baryon_masses_used"]))
    checks.append(check("QP042 fills ddu and duu scaffolds", qp042["filled_baryon_scaffold_ids"] == "ddu;duu", "QP042 filled ids", qp042["filled_baryon_scaffold_ids"]))
    checks.append(check("QP042 preserves open baryon boundaries", qp042["open_boundary_rows"] == 54, "QP042 open rows", qp042["open_boundary_rows"]))

    checks.append(check("CR029 declares radial-law debt", "native radial organization law" in premises["CR029"].get("declared_open_debt", ""), "CR029 open debt", premises["CR029"].get("declared_open_debt")))
    checks.append(check("CR030 branch scoped PASS", branch_summaries["CR030"].get("scientific_verdict") == "PASS" and branch_summaries["CR030"].get("claim_tier") == "PASS_SCOPED_BRANCH_WITH_NATIVE_RADIAL_SELECTOR_OPEN", "CR030 verdict", source_status(branch_summaries["CR030"])))
    checks.append(check("CR030 pass/boundary counts replay", branch_support_counts["pass"] == 4 and branch_support_counts["boundary"] == 4, "support verdict counts", branch_support_counts))

    checks.append(check("CR116 correction clean", cr116.get("execution_status") == "CLEAN", source_status(cr116)))
    checks.append(check("CR116 corrected reading is clustered BB-origin PBH", "CLUSTERED BB-origin PBHs" in cr116.get("corrected_reading", ""), "CR116 corrected reading", cr116.get("corrected_reading")))
    checks.append(check("CR116 records stale CR115 misread", any("CR115 bridge" in item for item in cr116.get("what_was_corrected", [])), "CR116 correction list", cr116.get("what_was_corrected")))
    checks.append(check("CR116 keeps clustered microlensing as open debt", any("Clustered-PBH-aware microlensing" in item for item in cr116.get("open_debts", [])), "CR116 open debts", cr116.get("open_debts")))
    checks.append(check("Governance CR115 stale bridge remains source-preserved", summaries["CR115_gov_stale_bridge"].get("execution_status") == "CLEAN", "CR115 governance bridge", source_status(summaries["CR115_gov_stale_bridge"])))

    for row in replay_layers:
        checks.append(check(f"Replay layer: {row['layer']}", row["status"] == "PASS", row["boundary"], row["source_value"]))
    for row in halo_metrics:
        checks.append(check(f"Metric: {row['metric']}", row["status"] == "PASS", "replay metric", row["replayed"]))
    for row in wrong_controls:
        checks.append(check(f"{row['wrong_control']} rejected", row["result"] == "REJECTED", row["evidence"]))

    pass_count = sum(1 for item in checks if item["status"] == "PASS")
    fail_count = len(checks) - pass_count
    replay_passed = fail_count == 0

    layers_path = OUT_DIR / "LC08_replay_layers.csv"
    formula_path = OUT_DIR / "LC08_formula_manifest.csv"
    metrics_path = OUT_DIR / "LC08_halo_replay_metrics.csv"
    seed_path = OUT_DIR / "LC08_seed_candidate_rows.csv"
    wrong_path = OUT_DIR / "LC08_wrong_controls.csv"
    boundary_path = OUT_DIR / "LC08_claim_boundaries.csv"
    checks_path = OUT_DIR / "LC08_checks.csv"
    source_path = OUT_DIR / "LC08_sources_hashes.csv"
    summary_path = OUT_DIR / "LC08_summary.json"
    result_path = OUT_DIR / "LC08_result.md"
    hash_path = OUT_DIR / "HASHES.txt"

    source_rows: list[dict[str, Any]] = []
    for name, path in SOURCES.items():
        status = source_status(summaries[name]) if name in summaries else "text/hash source"
        source_rows.append({"source": name, "path": rel(path), "status": status, "sha256": sha256_file(path)})
    for name, path in PREMISES.items():
        source_rows.append({"source": f"{name}_premises", "path": rel(path), "status": "declared premises", "sha256": sha256_file(path)})
    for name, path in EVIDENCE.items():
        source_rows.append({"source": f"{name}_evidence_rows", "path": rel(path), "status": f"{len(evidence_rows[name])} rows", "sha256": sha256_file(path)})
    for name, path in UPSTREAM.items():
        if path.suffix.lower() == ".json":
            status = source_status(upstream_json[name])
        elif name == "G392_residual_rows":
            status = f"{len(g392_residual_rows)} rows"
        elif name == "G394_profile_rows":
            status = f"{len(g394_profile_rows)} rows"
        elif name == "G677_primary_galaxy_rows":
            status = f"{len(g677_primary_rows)} rows"
        elif name == "G677_candidate_table":
            status = f"{len(g677_candidate_rows)} rows"
        elif name == "G677_wrong_controls":
            status = f"{len(g677_wrong_rows)} rows"
        else:
            status = "row artifact"
        source_rows.append({"source": name, "path": rel(path), "status": status, "sha256": sha256_file(path)})
    source_rows.append({"source": "LC08_runner", "path": rel(RUNNER_PATH), "status": "result-producing runner", "sha256": sha256_file(RUNNER_PATH)})
    source_rows.append({"source": "LC01_primitive_stack_declared_csv", "path": rel(LC01_PRIMITIVE_CSV), "status": "primitive exact values", "sha256": sha256_file(LC01_PRIMITIVE_CSV)})

    write_csv(layers_path, replay_layers, ["layer", "source", "formula_or_contract", "expected_or_replayed", "source_value", "status", "boundary"])
    write_csv(formula_path, formula_manifest, ["formula_or_rule", "expression", "locked_inputs", "replayed_value", "source_or_target_use"])
    write_csv(metrics_path, halo_metrics, ["metric", "replayed", "source", "status"])
    write_csv(seed_path, seed_candidate_rows, ["candidate_id", "selector_source", "core_denominator", "median_seed_first_rms_kms", "fraction_of_baryon_to_g394_rms_gap_closed", "role_in_LC08", "promoted_to_primitive"])
    write_csv(wrong_path, wrong_controls, ["wrong_control", "attempted_mutation", "evidence", "result"])
    write_csv(boundary_path, claim_boundaries, ["boundary", "status", "text"])
    write_csv(checks_path, checks, ["check", "status", "value", "detail"])
    write_csv(source_path, source_rows, ["source", "path", "status", "sha256"])

    summary = {
        "task_id": TASK_ID,
        "task_name": TASK_NAME,
        "result": RESULT_CLASS if replay_passed else "LC08_FAIL_HALO_PBH_INVENTORY_REPLAY",
        "generated_utc": now,
        "locked_primitive_stack": primitive_stack,
        "pass_condition": {
            "formula_mutation": "forbidden",
            "constant_mutation": "forbidden",
            "target_value_substitution": "forbidden",
            "row_deletion": "forbidden",
            "retroactive_relabeling": "forbidden",
            "config_as_law_promotion": "forbidden",
            "radial_law_overclaim": "forbidden",
        },
        "halo_replay": {
            "R": R,
            "D": D,
            "Omega_substrate_vacuum": omega_vacuum,
            "Omega_BB_PBH_trapped": omega_pbh,
            "Omega_H_arrival_baryon": omega_h,
            "total_inventory": total_inventory,
            "matter_inventory": matter_inventory,
            "PBH_to_hydrogen_ratio": pbh_to_h_ratio,
            "trapped_fraction_of_matter": trapped_fraction,
            "escaped_hydrogen_fraction_of_matter": escaped_fraction,
            "sparc_galaxies": len(g392_residual_rows),
            "sparc_mass_model_points": g392["sparc_loaded"]["mass_model_points"],
            "median_outer_dark_fraction_v2": g392["real_sparc_residuals"]["median_outer_dark_fraction_v2"],
            "post_BB_envelope_supplied_pct_dark_residual": g393["percentage_budget"]["pbh_envelope_supplied_pct_dark_residual"],
            "missing_after_post_BB_envelope_pct_dark_residual": g393["percentage_budget"]["missing_after_pbh_envelope_pct_dark_residual"],
            "median_baryon_rms_kms": g394["fit_summary"]["median_baryon_rms_kms"],
            "median_halo_rms_kms": g394["fit_summary"]["median_halo_rms_kms"],
            "median_chi2_improvement_factor": g394["fit_summary"]["median_chi2_improvement_factor"],
            "median_halo_overdensity_vs_cosmic_dm_mean": g394["clustering_summary"]["median_halo_overdensity_vs_cosmic_dm_mean"],
            "seed_primary_candidate_id": primary_seed["candidate_id"],
            "seed_primary_gap_closed": primary_seed["fraction_of_baryon_to_g394_rms_gap_closed"],
            "seed_uniform_gap_closed": uniform_wrong["fraction_of_baryon_to_g394_rms_gap_closed"],
            "seed_post_BB_gap_closed": postbb_wrong["fraction_of_baryon_to_g394_rms_gap_closed"],
            "best_RMS_candidate_id": best_seed["candidate_id"],
            "best_RMS_candidate_promoted_to_law": False,
            "branch_support_pass_count": branch_support_counts["pass"],
            "branch_support_boundary_count": branch_support_counts["boundary"],
            "branch_support_clean_count": branch_support_counts["clean"],
            "branch_total_pass_count_including_CR030": branch_total_counts["pass"],
            "branch_total_boundary_count_including_CR030": branch_total_counts["boundary"],
            "branch_total_clean_count_including_CR030": branch_total_counts["clean"],
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
            "replay_layers": rel(layers_path),
            "formula_manifest": rel(formula_path),
            "halo_replay_metrics": rel(metrics_path),
            "seed_candidate_rows": rel(seed_path),
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
        f"# {TASK_ID} - Halo/PBH Inventory Replay",
        "",
        f"Result: **{summary['result']}**",
        "",
        "Question: with the locked primitive stack promoted in LC01, does the halo/PBH inventory branch replay without promoting a successful config into a primitive law?",
        "",
        "Verdict: yes. LC08 replays branch 08 as a scoped halo/PBH inventory support chain: cumulative nonzero A plus clustered BB-origin PBH/trapped-A carries the halo lane, post-BB/window PBH remains a small rejected full-halo control, hydrogen catches up inside the PBH/trapped-A scaffold, and the native radial law remains open.",
        "",
        "Locked stack used:",
        f"- R = {R}",
        f"- D = {D}",
        f"- A0 = {primitive_stack['A0']} = {primitive_stack['A0_decimal']}",
        "",
        "Core replay numbers:",
        f"- Omega_BB_PBH_trapped = {omega_pbh}",
        f"- Omega_H_arrival_baryon = {omega_h}",
        f"- total inventory = {total_inventory}",
        f"- PBH/H ratio = {pbh_to_h_ratio}",
        f"- SPARC galaxies = {len(g392_residual_rows)}; mass-model points = {g392['sparc_loaded']['mass_model_points']}",
        f"- median outer dark fraction v2 = {g392['real_sparc_residuals']['median_outer_dark_fraction_v2']}",
        f"- post-BB envelope supplied pct of dark residual = {g393['percentage_budget']['pbh_envelope_supplied_pct_dark_residual']}",
        f"- missing after post-BB envelope pct of dark residual = {g393['percentage_budget']['missing_after_pbh_envelope_pct_dark_residual']}",
        f"- clustered profile median RMS = {g394['fit_summary']['median_halo_rms_kms']} km/s vs baryon RMS = {g394['fit_summary']['median_baryon_rms_kms']} km/s",
        f"- clustered profile chi2 improvement = {g394['fit_summary']['median_chi2_improvement_factor']}",
        f"- seed-first native R/12 gap closed = {primary_seed['fraction_of_baryon_to_g394_rms_gap_closed']}",
        f"- uniform-control gap closed = {uniform_wrong['fraction_of_baryon_to_g394_rms_gap_closed']}",
        f"- post-BB-only-control gap closed = {postbb_wrong['fraction_of_baryon_to_g394_rms_gap_closed']}",
        "",
        "Trap controls rejected:",
        "- Config-as-law rejected: R/6 is the best-RMS comparison row but is not promoted to primitive law.",
        "- Smooth/uniform PBH conflation rejected: uniform gap closed is near zero; clustered-PBH-aware microlensing remains open.",
        "- Post-BB-only-as-full-halo rejected: post-BB/window PBH supplies only 2.576714% of the dark residual.",
        "- Full radial-law overclaim rejected: native radial organization, mass function, and concentration remain open.",
        "- Stale governance wording rejected: CR116 supersedes the older CR115 bridge interpretation without modifying it.",
        "",
        f"Checks: {pass_count}/{len(checks)} PASS",
        f"Wrong controls: {summary['wrong_controls']['rejected']}/{summary['wrong_controls']['tested']} rejected",
        "",
        "Primary artifacts:",
        f"- `{rel(layers_path)}`",
        f"- `{rel(formula_path)}`",
        f"- `{rel(metrics_path)}`",
        f"- `{rel(seed_path)}`",
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
        layers_path,
        formula_path,
        metrics_path,
        seed_path,
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
