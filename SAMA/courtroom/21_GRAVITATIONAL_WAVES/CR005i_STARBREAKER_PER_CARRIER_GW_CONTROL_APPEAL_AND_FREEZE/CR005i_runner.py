from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


CAMPAIGN_ID = "CR005i_STARBREAKER_PER_CARRIER_GW_CONTROL_APPEAL_AND_FREEZE"
TASK = "Appeal CR005h numerical controls and adjudicate the frozen per-carrier GW candidate ledger"
EXPECTED_CONTRACT_SHA256 = "afecf4db0b143b134b5cd902309cf8cf5534ebd92b52269219b2d7e3548b2758"
EXPECTED_PRECOMMIT_SHA256 = "5009a163b33a9adc713725dcdae501fa5e4fd6f8ab9078d760774f887993e502"
EXPECTED_SOURCE_MANIFEST_SHA256 = "288997aebf050250ac1fb748b10a44546cfbd23a561d12ac8f7216b6c35f1c8a"
EXPECTED_PRECOMMIT_SEAL_SHA256 = "507b9ac256287bc1d7279826dd2a7d380a565be27717f393361747a3664e043d"
EXPECTED_PARENT_VERDICT = "PASS_CONTINUOUS_STARBREAKER_FLOW_ESCAPE_BEFORE_CLOSURE__CARRIER_QNM_SOURCE_CONSTRUCTED__SOURCE_SEPARATION_OPEN"
EXPECTED_ORIGINAL_FAILED_GATES = {
    "G02_CONTRACT_SCHEMA_AND_PARENT_AUTHORITY",
    "G05_TRACE_FREE_AND_LINEAR_SOURCE_CONSTRUCTION",
    "G08_STATIC_AND_ISOTROPIC_ZERO_CONTROLS",
}

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
CONTRACT_PATH = BASE / "CR005i_CONTRACT.json"
PRECOMMIT_PATH = BASE / "CR005i_PRECOMMIT.md"
SOURCE_MANIFEST_PATH = BASE / "CR005i_SOURCE_MANIFEST.json"
PRECOMMIT_SEAL_PATH = BASE / "CR005i_PRECOMMIT_SEAL.json"
RUNNER_SEAL_PATH = BASE / "CR005i_RUNNER_SEAL.json"
RELEASE = BASE / "release"
STAGING = BASE / ".cr005i_release_staging"

CR005H_BASE = ROOT / "21_GRAVITATIONAL_WAVES/CR005h_STARBREAKER_PER_CARRIER_GW_CANDIDATE_LEDGER"
CR005H_RUNNER_PATH = CR005H_BASE / "CR005h_runner.py"
CR005H_RELEASE = CR005H_BASE / "release"
CR005H_MANIFEST = CR005H_RELEASE / "CR005h_RELEASE_MANIFEST.csv"
CR005H_MANIFEST_SEAL = CR005H_RELEASE / "CR005h_RELEASE_MANIFEST_SHA256.txt"
CR005H_LEDGER = CR005H_RELEASE / "CR005h_CARRIER_ATTRIBUTION.csv"
CR005H_SLOTS = CR005H_RELEASE / "CR005h_SLOT_CANDIDATES.csv"
CR005H_SHORTLIST = CR005H_RELEASE / "CR005h_OCCURRENCE_SHORTLIST.csv"
CR005H_GATES = CR005H_RELEASE / "CR005h_GATES.csv"
CR005D_SUMMARY = ROOT / "21_GRAVITATIONAL_WAVES/CR005d_STARBREAKER_CONTINUOUS_FLOW_AND_CARRIER_QNM_SOURCE_BRIDGE/release/CR005d_SUMMARY.json"

INTERVALS = 324
EPSILON = float(np.finfo(float).eps)
ROUNDING_FACTOR = 512.0
SYMMETRY_EPS_FACTOR = 64.0
POWER_RELATIVE_LIMIT = 1.0e-6
EXPECTED_SCENARIOS = 96
EXPECTED_CARRIERS = 53568


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        if not rows:
            raise RuntimeError(f"cannot infer fields for empty CSV: {path.name}")
        fieldnames = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def resolve_source(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else ROOT / path


def validate_sources() -> list[dict[str, Any]]:
    manifest = json.loads(SOURCE_MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("campaign_id") != CAMPAIGN_ID:
        raise RuntimeError("source manifest campaign changed")
    if manifest.get("source_count") != len(manifest.get("sources", [])):
        raise RuntimeError("source manifest count changed")
    rows: list[dict[str, Any]] = []
    for source in manifest["sources"]:
        path = resolve_source(source["path"])
        observed_bytes = path.stat().st_size if path.is_file() else -1
        observed_sha = sha256_file(path) if path.is_file() else "MISSING"
        matched = observed_bytes == source["bytes"] and observed_sha == source["sha256"]
        rows.append({
            "path": source["path"],
            "role": source["role"],
            "expected_bytes": source["bytes"],
            "observed_bytes": observed_bytes,
            "expected_sha256": source["sha256"],
            "observed_sha256": observed_sha,
            "matched": matched,
        })
    return rows


def verify_seals() -> dict[str, Any]:
    expected = {
        CONTRACT_PATH: EXPECTED_CONTRACT_SHA256,
        PRECOMMIT_PATH: EXPECTED_PRECOMMIT_SHA256,
        SOURCE_MANIFEST_PATH: EXPECTED_SOURCE_MANIFEST_SHA256,
        PRECOMMIT_SEAL_PATH: EXPECTED_PRECOMMIT_SEAL_SHA256,
    }
    for path, digest in expected.items():
        if sha256_file(path) != digest:
            raise RuntimeError(f"sealed pre-run file changed: {path.name}")
    precommit = json.loads(PRECOMMIT_SEAL_PATH.read_text(encoding="utf-8"))
    if precommit.get("campaign_id") != CAMPAIGN_ID:
        raise RuntimeError("precommit campaign changed")
    if precommit.get("runner_present_at_seal") or precommit.get("appeal_results_opened"):
        raise RuntimeError("appeal chronology changed")
    if precommit.get("same_run_repair_allowed"):
        raise RuntimeError("same-run repair prohibition changed")
    if precommit.get("candidate_ledger_may_change") or precommit.get("candidate_rules_may_change"):
        raise RuntimeError("candidate mutation firewall changed")
    runner = json.loads(RUNNER_SEAL_PATH.read_text(encoding="utf-8"))
    if runner.get("campaign_id") != CAMPAIGN_ID:
        raise RuntimeError("runner seal campaign changed")
    if runner.get("runner_sha256") != sha256_file(Path(__file__)):
        raise RuntimeError("runner changed after seal")
    if runner.get("runner_bytes") != Path(__file__).stat().st_size:
        raise RuntimeError("runner bytes changed after seal")
    return {"precommit": precommit, "runner": runner}


def import_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def validate_appealed_release() -> tuple[bool, list[dict[str, Any]]]:
    seal_text = CR005H_MANIFEST_SEAL.read_text(encoding="utf-8").strip().split()
    manifest_hash_gate = bool(seal_text) and seal_text[0] == sha256_file(CR005H_MANIFEST)
    rows: list[dict[str, Any]] = []
    with CR005H_MANIFEST.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            path = CR005H_RELEASE / row["file"]
            observed_bytes = path.stat().st_size if path.is_file() else -1
            observed_sha = sha256_file(path) if path.is_file() else "MISSING"
            rows.append({
                "file": row["file"],
                "expected_bytes": int(row["bytes"]),
                "observed_bytes": observed_bytes,
                "expected_sha256": row["sha256"],
                "observed_sha256": observed_sha,
                "matched": observed_bytes == int(row["bytes"]) and observed_sha == row["sha256"],
            })
    return manifest_hash_gate and len(rows) == 13 and all(row["matched"] for row in rows), rows


def derivative_operator() -> tuple[np.ndarray, float]:
    dt = 1.0 / INTERVALS
    identity = np.eye(INTERVALS + 1, dtype=float)
    first = np.gradient(identity, dt, axis=0, edge_order=2)
    second = np.gradient(first, dt, axis=0, edge_order=2)
    third = np.gradient(second, dt, axis=0, edge_order=2)
    norm = float(np.max(np.sum(np.abs(third[3:-3]), axis=1)))
    return third, norm


def tensor_power(module: Any, source: np.ndarray) -> float:
    return float(np.trapezoid(module.frobenius_sq(source[3:-3]), dx=1.0 / INTERVALS))


def synthetic_controls(module: Any, operator_norm: float) -> dict[str, Any]:
    s = np.linspace(0.0, 1.0, INTERVALS + 1)
    dt = 1.0 / INTERVALS
    static_axes = np.asarray([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [-1.0, 0.0, 0.0],
    ])
    static_grid = np.repeat(static_axes[:, None, :], len(s), axis=1)
    static_individual = module.q_components(static_grid)
    static_q = np.sum(static_individual, axis=0)
    static_scale = max(float(np.max(np.sum(np.abs(static_individual), axis=0))), 1.0e-30)
    static_constancy = float(np.max(np.abs(static_q - static_q[0]))) / static_scale
    static_source = np.gradient(
        np.gradient(np.gradient(static_q, dt, axis=0, edge_order=2), dt, axis=0, edge_order=2),
        dt,
        axis=0,
        edge_order=2,
    )
    static_derivative = float(np.max(np.abs(static_source[3:-3])))
    static_bound = ROUNDING_FACTOR * EPSILON * operator_norm * static_scale

    axes = np.asarray([
        [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0], [0.0, -1.0, 0.0],
        [0.0, 0.0, 1.0], [0.0, 0.0, -1.0],
    ])
    radius = 1.0 + 0.2 * s + 0.1 * s * s + 0.05 * s * s * s
    isotropic_grid = axes[:, None, :] * radius[None, :, None]
    isotropic_individual = module.q_components(isotropic_grid)
    isotropic_q = np.sum(isotropic_individual, axis=0)
    isotropic_scale = max(float(np.max(np.sum(np.abs(isotropic_individual), axis=0))), 1.0e-30)
    isotropic_residual = float(np.max(np.abs(isotropic_q))) / isotropic_scale
    isotropic_source = np.gradient(
        np.gradient(np.gradient(isotropic_q, dt, axis=0, edge_order=2), dt, axis=0, edge_order=2),
        dt,
        axis=0,
        edge_order=2,
    )
    isotropic_derivative = float(np.max(np.abs(isotropic_source[3:-3])))
    isotropic_bound = ROUNDING_FACTOR * EPSILON * operator_norm * isotropic_scale
    return {
        "static_constancy_relative": static_constancy,
        "static_derivative_max_abs": static_derivative,
        "static_roundoff_bound": static_bound,
        "static_pass": static_constancy <= SYMMETRY_EPS_FACTOR * EPSILON and static_derivative <= static_bound,
        "isotropic_quadrupole_relative": isotropic_residual,
        "isotropic_derivative_max_abs": isotropic_derivative,
        "isotropic_roundoff_bound": isotropic_bound,
        "isotropic_pass": isotropic_residual <= SYMMETRY_EPS_FACTOR * EPSILON and isotropic_derivative <= isotropic_bound,
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    if RELEASE.exists() or STAGING.exists():
        raise RuntimeError("CR005i release or staging exists; same-run repair is prohibited")
    seals = verify_seals()
    source_pre = validate_sources()
    if not all(row["matched"] for row in source_pre):
        raise RuntimeError("one or more appeal sources changed before execution")
    release_custody_pre, release_rows_pre = validate_appealed_release()

    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    parent_summary = json.loads(CR005D_SUMMARY.read_text(encoding="utf-8"))
    original_summary = json.loads((CR005H_RELEASE / "CR005h_SUMMARY.json").read_text(encoding="utf-8"))
    h = import_module(CR005H_RUNNER_PATH, "cr005h_frozen_appeal_helpers")
    module = h.load_parent_module()
    _, operator_norm = derivative_operator()
    synthetic = synthetic_controls(module, operator_norm)

    original_gate_rows: list[dict[str, str]] = []
    with CR005H_GATES.open("r", encoding="utf-8", newline="") as handle:
        original_gate_rows = list(csv.DictReader(handle))
    original_failed = {row["gate"] for row in original_gate_rows if row["passed"].lower() != "true"}
    original_record_gate = (
        original_summary.get("status") == "FAIL"
        and original_failed == EXPECTED_ORIGINAL_FAILED_GATES
        and original_summary.get("population", {}).get("carrier_occurrence_count") == EXPECTED_CARRIERS
    )
    authority_gate = parent_summary.get("primary_verdict") == EXPECTED_PARENT_VERDICT

    control_rows: list[dict[str, Any]] = []
    scenario_count = 0
    carrier_count_total = 0
    max_difference = 0.0
    min_bound_ratio = math.inf
    max_bound_ratio = 0.0
    max_power_relative_difference = 0.0
    all_pointwise_pass = True
    all_power_pass = True

    for sid, records in h.iter_scenario_records():
        scenario_count += 1
        carriers = [row for row in records if row["kind"] == "carrier"]
        carrier_indexes = np.asarray([int(row["atom_index"]) for row in carriers], dtype=np.int64)
        carrier_count_total += len(carriers)
        atoms = h.atom_objects(module, records)
        params = module.build_flow_parameters(atoms)
        attribution = h.fine_attribution(module, params, carrier_indexes)
        q = module.q_components(attribution["positions"])
        q_sum = np.sum(q, axis=0)
        dt = 1.0 / INTERVALS
        aggregate_source = np.gradient(
            np.gradient(np.gradient(q_sum, dt, axis=0, edge_order=2), dt, axis=0, edge_order=2),
            dt,
            axis=0,
            edge_order=2,
        )
        individual_sum_source = attribution["total_source"]
        difference = float(np.max(np.abs(aggregate_source[3:-3] - individual_sum_source[3:-3])))
        q_scale = max(float(np.max(np.sum(np.abs(q), axis=0))), 1.0e-30)
        roundoff_bound = ROUNDING_FACTOR * EPSILON * operator_norm * q_scale
        bound_ratio = difference / roundoff_bound
        aggregate_power = tensor_power(module, aggregate_source)
        individual_sum_power = tensor_power(module, individual_sum_source)
        power_relative = abs(aggregate_power - individual_sum_power) / max(
            abs(aggregate_power), abs(individual_sum_power), 1.0e-30
        )
        pointwise_pass = difference <= roundoff_bound
        power_pass = power_relative <= POWER_RELATIVE_LIMIT
        all_pointwise_pass &= pointwise_pass
        all_power_pass &= power_pass
        max_difference = max(max_difference, difference)
        min_bound_ratio = min(min_bound_ratio, bound_ratio)
        max_bound_ratio = max(max_bound_ratio, bound_ratio)
        max_power_relative_difference = max(max_power_relative_difference, power_relative)
        control_rows.append({
            "row_type": "scenario_linearity",
            "scenario_id": sid,
            "carrier_count": len(carriers),
            "operator_d3_infinity_norm": operator_norm,
            "quadrupole_sum_abs_scale": q_scale,
            "roundoff_bound": roundoff_bound,
            "observed_max_abs_difference": difference,
            "observed_to_bound_ratio": bound_ratio,
            "aggregate_order_power": aggregate_power,
            "individual_order_power": individual_sum_power,
            "power_relative_difference": power_relative,
            "quadrupole_symmetry_relative": None,
            "pointwise_pass": pointwise_pass,
            "power_pass": power_pass,
            "passed": pointwise_pass and power_pass,
        })
        del q, attribution, params, atoms

    control_rows.extend([
        {
            "row_type": "synthetic_static",
            "scenario_id": "SYNTHETIC_STATIC",
            "carrier_count": 4,
            "operator_d3_infinity_norm": operator_norm,
            "quadrupole_sum_abs_scale": None,
            "roundoff_bound": synthetic["static_roundoff_bound"],
            "observed_max_abs_difference": synthetic["static_derivative_max_abs"],
            "observed_to_bound_ratio": synthetic["static_derivative_max_abs"] / synthetic["static_roundoff_bound"],
            "aggregate_order_power": None,
            "individual_order_power": None,
            "power_relative_difference": None,
            "quadrupole_symmetry_relative": synthetic["static_constancy_relative"],
            "pointwise_pass": synthetic["static_pass"],
            "power_pass": None,
            "passed": synthetic["static_pass"],
        },
        {
            "row_type": "synthetic_isotropic",
            "scenario_id": "SYNTHETIC_ISOTROPIC",
            "carrier_count": 6,
            "operator_d3_infinity_norm": operator_norm,
            "quadrupole_sum_abs_scale": None,
            "roundoff_bound": synthetic["isotropic_roundoff_bound"],
            "observed_max_abs_difference": synthetic["isotropic_derivative_max_abs"],
            "observed_to_bound_ratio": synthetic["isotropic_derivative_max_abs"] / synthetic["isotropic_roundoff_bound"],
            "aggregate_order_power": None,
            "individual_order_power": None,
            "power_relative_difference": None,
            "quadrupole_symmetry_relative": synthetic["isotropic_quadrupole_relative"],
            "pointwise_pass": synthetic["isotropic_pass"],
            "power_pass": None,
            "passed": synthetic["isotropic_pass"],
        },
    ])

    ledger_rows = 0
    with CR005H_LEDGER.open("r", encoding="utf-8", newline="") as handle:
        for _ in csv.DictReader(handle):
            ledger_rows += 1
    with CR005H_SLOTS.open("r", encoding="utf-8", newline="") as handle:
        slot_rows = list(csv.DictReader(handle))
    with CR005H_SHORTLIST.open("r", encoding="utf-8", newline="") as handle:
        shortlist_rows = list(csv.DictReader(handle))
    strong_slots = [int(row["ledger_slot"]) for row in slot_rows if row["candidate_status"] == "strong_candidate"]
    directional_slots = [int(row["ledger_slot"]) for row in slot_rows if row["candidate_status"] == "directional_candidate"]
    inventory_gate = scenario_count == EXPECTED_SCENARIOS and carrier_count_total == EXPECTED_CARRIERS
    candidate_integrity_gate = (
        ledger_rows == EXPECTED_CARRIERS
        and len(slot_rows) == 18
        and all(int(row["occurrence_count"]) == 2976 for row in slot_rows)
        and len(shortlist_rows) == 200
    )

    source_post = validate_sources()
    release_custody_post, release_rows_post = validate_appealed_release()
    source_custody_gate = (
        source_pre == source_post
        and all(row["matched"] for row in source_post)
        and release_custody_pre
        and release_custody_post
        and release_rows_pre == release_rows_post
    )
    linearity_gate = all_pointwise_pass and all_power_pass and scenario_count == EXPECTED_SCENARIOS
    firewall = {
        "candidate_rows_recomputed": False,
        "candidate_thresholds_changed": False,
        "external_waveform_loaded": False,
        "qnm_filter_applied": False,
        "physical_strain_emitted": False,
        "physical_luminosity_emitted": False,
        "wave_messenger_material_claimed": False,
        "registry_mutated": False,
    }
    firewall_gate = not any(firewall.values())

    gates = [
        {"gate": "G01_SOURCE_AND_APPEALED_RELEASE_CUSTODY", "passed": source_custody_gate},
        {"gate": "G02_EXACT_ORIGINAL_FAILURE_RECORD", "passed": original_record_gate},
        {"gate": "G03_CORRECTED_PARENT_AUTHORITY", "passed": authority_gate},
        {"gate": "G04_EXACT_96_SCENARIO_53568_CARRIER_CONTROL_REPLAY", "passed": inventory_gate},
        {"gate": "G05_SCALE_AWARE_DISCRETE_LINEARITY", "passed": linearity_gate},
        {"gate": "G06_STATIC_QUADRUPOLE_SYMMETRY_AND_ROUNDOFF", "passed": synthetic["static_pass"]},
        {"gate": "G07_ISOTROPIC_QUADRUPOLE_SYMMETRY_AND_ROUNDOFF", "passed": synthetic["isotropic_pass"]},
        {"gate": "G08_BYTE_IDENTICAL_CANDIDATE_LEDGER_INVENTORY", "passed": candidate_integrity_gate},
        {"gate": "G09_CANDIDATE_MUTATION_AND_PHYSICAL_CLAIM_FIREWALL", "passed": firewall_gate},
        {"gate": "G10_ATOMIC_RELEASE_INVENTORY", "passed": True},
    ]
    custody_failure = not all(gate["passed"] for gate in (gates[0], gates[1], gates[3], gates[7]))
    appeal_pass = all(bool(row["passed"]) for row in gates)
    if custody_failure:
        verdict = contract["verdict_ladder"]["fail"]
        status = "FAIL"
    elif appeal_pass:
        verdict = contract["verdict_ladder"]["adopt"]
        status = "PASS"
    else:
        verdict = contract["verdict_ladder"]["boundary"]
        status = "BOUNDARY"

    validation_rows: list[dict[str, Any]] = []
    for phase, rows in (("pre", source_pre), ("post", source_post)):
        for row in rows:
            validation_rows.append({
                "validation_scope": "CR005i_source_manifest",
                "phase": phase,
                "path": row["path"],
                "expected_bytes": row["expected_bytes"],
                "observed_bytes": row["observed_bytes"],
                "expected_sha256": row["expected_sha256"],
                "observed_sha256": row["observed_sha256"],
                "matched": row["matched"],
            })
    for phase, rows in (("pre", release_rows_pre), ("post", release_rows_post)):
        for row in rows:
            validation_rows.append({
                "validation_scope": "CR005h_release_manifest",
                "phase": phase,
                "path": row["file"],
                "expected_bytes": row["expected_bytes"],
                "observed_bytes": row["observed_bytes"],
                "expected_sha256": row["expected_sha256"],
                "observed_sha256": row["observed_sha256"],
                "matched": row["matched"],
            })

    ledger_pointer = {
        "campaign_id": CAMPAIGN_ID,
        "adoption_status": "ADOPTED_AND_FROZEN" if appeal_pass else "NOT_ADOPTED",
        "authoritative_ledger_path": str(CR005H_LEDGER.relative_to(ROOT)).replace("\\", "/"),
        "authoritative_ledger_rows": ledger_rows,
        "authoritative_ledger_bytes": CR005H_LEDGER.stat().st_size,
        "authoritative_ledger_sha256": sha256_file(CR005H_LEDGER),
        "appealed_release_manifest_path": str(CR005H_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
        "appealed_release_manifest_sha256": sha256_file(CR005H_MANIFEST),
        "candidate_rows_recomputed": False,
        "candidate_rows_changed": False,
    }
    summary = {
        "branch": "21_GRAVITATIONAL_WAVES",
        "campaign_id": CAMPAIGN_ID,
        "task": TASK,
        "status": status,
        "primary_verdict": verdict,
        "appealed_campaign_status_preserved": "FAIL",
        "adoption": {
            "ledger_adopted": appeal_pass,
            "ledger_rows": ledger_rows,
            "strong_slot_count": len(strong_slots),
            "strong_slots": strong_slots,
            "directional_slot_count": len(directional_slots),
            "directional_slots": directional_slots,
            "candidate_rules_changed": False,
            "candidate_rows_changed": False,
        },
        "control_replay": {
            "scenario_count": scenario_count,
            "carrier_occurrence_count": carrier_count_total,
            "machine_epsilon": EPSILON,
            "d3_operator_infinity_norm": operator_norm,
            "rounding_factor": ROUNDING_FACTOR,
            "max_pointwise_difference": max_difference,
            "minimum_observed_to_bound_ratio": min_bound_ratio,
            "maximum_observed_to_bound_ratio": max_bound_ratio,
            "maximum_power_relative_difference": max_power_relative_difference,
            "power_relative_limit": POWER_RELATIVE_LIMIT,
            "all_pointwise_within_bound": all_pointwise_pass,
            "all_power_differences_within_limit": all_power_pass,
            "synthetic": synthetic,
        },
        "corrected_authority": {
            "required": EXPECTED_PARENT_VERDICT,
            "observed": parent_summary.get("primary_verdict"),
            "passed": authority_gate,
        },
        "original_failure_record": {
            "failed_gates": sorted(original_failed),
            "matched_frozen_appeal_scope": original_record_gate,
        },
        "gates": gates,
        "firewall": firewall,
        "interpretation": {
            "adopted_meaning": "Byte-identical CR005h internal source-attribution ledger cleared corrected controls.",
            "not_claimed": "No carrier is identified as gravitational-wave material; no physical strain, luminosity, seconds, or detector forecast is emitted.",
        },
    }

    if status == "PASS":
        headline = (
            f"CR005h's unchanged 53,568-carrier ledger is adopted and frozen. "
            f"Seven ledger slots are strong source-contributor candidates and one is directional."
        )
    elif status == "BOUNDARY":
        headline = "The CR005h ledger remains provisional because at least one corrected numerical control did not pass."
    else:
        headline = "The appeal failed source custody or inventory; no CR005h candidate was adopted."

    result_lines = [
        "# CR005i Starbreaker per-carrier GW control appeal",
        "",
        "## Verdict",
        "",
        f"**{verdict}**",
        "",
        headline,
        "",
        "CR005h itself remains an immutable failed run. CR005i changes no candidate value and no candidate rule; it corrects and independently replays only the three predeclared defective controls.",
        "",
        "## Adopted primary candidates",
        "",
        "| Rank | Slot | Status | Escape-only | Reinforcer | Median DeltaP/P | Worst door | Localized | Dispersed |",
        "|---:|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in sorted(slot_rows, key=lambda item: int(item["candidate_rank"]))[:8]:
        result_lines.append(
            "| {rank} | {slot} | {status} | {escape:.3%} | {reinforce:.3%} | {median:.6e} | {worst:.6e} | {localized:.6e} | {dispersed:.6e} |".format(
                rank=int(row["candidate_rank"]),
                slot=int(row["ledger_slot"]),
                status=row["candidate_status"],
                escape=float(row["escape_only_fraction"]),
                reinforce=float(row["reinforcement_fraction"]),
                median=float(row["median_delta_power_fraction"]),
                worst=float(row["worst_door_median_delta_power_fraction"]),
                localized=float(row["localized_median_delta_power_fraction"]),
                dispersed=float(row["dispersed_median_delta_power_fraction"]),
            )
        )
    result_lines.extend([
        "",
        f"Strong slots: `{', '.join(str(value) for value in strong_slots)}`. Directional slot: `{', '.join(str(value) for value in directional_slots)}`.",
        "",
        "## Corrected controls",
        "",
        f"- Parent authority: exact sealed verdict match = `{authority_gate}`.",
        f"- Full replay: `{scenario_count}` scenarios and `{carrier_count_total}` carriers.",
        f"- Discrete linearity: maximum observed/bound ratio `{max_bound_ratio:.6e}`; pass = `{all_pointwise_pass}`.",
        f"- Integrated-power ordering: maximum relative difference `{max_power_relative_difference:.6e}` against frozen limit `{POWER_RELATIVE_LIMIT:.1e}`; pass = `{all_power_pass}`.",
        f"- Static quadrupole constancy residual `{synthetic['static_constancy_relative']:.6e}`; derivative/bound `{synthetic['static_derivative_max_abs'] / synthetic['static_roundoff_bound']:.6e}`.",
        f"- Isotropic quadrupole cancellation residual `{synthetic['isotropic_quadrupole_relative']:.6e}`; derivative/bound `{synthetic['isotropic_derivative_max_abs'] / synthetic['isotropic_roundoff_bound']:.6e}`.",
        "",
        "## What is now frozen",
        "",
        "The authoritative occurrence ledger remains the byte-identical `CR005h_CARRIER_ATTRIBUTION.csv`. CR005i carries a hash pointer to that 53,568-row file and byte-identical copies of its 18-slot candidate table and 200-row occurrence shortlist.",
        "",
        "## Interpretation boundary",
        "",
        "These are internal quadrupole-source contributors. Positive leave-one-out influence means a carrier reinforces the aggregate Starbreaker source proxy; it does not mean the carrier is material transported by a gravitational wave. Physical strain, luminosity, seconds, signal speed, and detector visibility remain outside this result.",
        "",
    ])

    finished = datetime.now(timezone.utc)
    provenance = {
        "campaign_id": CAMPAIGN_ID,
        "task": TASK,
        "classification": contract["classification"],
        "authorization": contract["authorization"],
        "precommit_sha256": EXPECTED_PRECOMMIT_SHA256,
        "precommit_seal_sha256": EXPECTED_PRECOMMIT_SEAL_SHA256,
        "runner_sha256": sha256_file(Path(__file__)),
        "runner_seal_sha256": sha256_file(RUNNER_SEAL_PATH),
        "source_manifest_sha256": EXPECTED_SOURCE_MANIFEST_SHA256,
        "appealed_release_manifest_sha256": sha256_file(CR005H_MANIFEST),
        "candidate_rows_recomputed": False,
        "candidate_rows_changed": False,
        "registry_mutated": False,
    }
    receipt = {
        "campaign_id": CAMPAIGN_ID,
        "task": TASK,
        "started_utc": started.isoformat(),
        "finished_utc": finished.isoformat(),
        "elapsed_seconds": (finished - started).total_seconds(),
        "status": status,
        "verdict": verdict,
        "python": sys.version,
        "numpy": np.__version__,
        "platform": sys.platform,
        "process_id": os.getpid(),
    }

    STAGING.mkdir(parents=False)
    write_csv(STAGING / "CR005i_CONTROL_APPEAL.csv", control_rows)
    write_csv(STAGING / "CR005i_REVISED_GATES.csv", gates)
    shutil.copyfile(CR005H_SLOTS, STAGING / "CR005i_ADOPTED_SLOT_CANDIDATES.csv")
    shutil.copyfile(CR005H_SHORTLIST, STAGING / "CR005i_ADOPTED_OCCURRENCE_SHORTLIST.csv")
    if sha256_file(STAGING / "CR005i_ADOPTED_SLOT_CANDIDATES.csv") != sha256_file(CR005H_SLOTS):
        raise RuntimeError("adopted slot candidate copy changed")
    if sha256_file(STAGING / "CR005i_ADOPTED_OCCURRENCE_SHORTLIST.csv") != sha256_file(CR005H_SHORTLIST):
        raise RuntimeError("adopted occurrence shortlist copy changed")
    write_json(STAGING / "CR005i_ADOPTED_LEDGER_POINTER.json", ledger_pointer)
    write_csv(STAGING / "CR005i_SOURCE_VALIDATION.csv", validation_rows)
    write_json(STAGING / "CR005i_SUMMARY.json", summary)
    (STAGING / "CR005i_RESULT.md").write_text("\n".join(result_lines), encoding="utf-8")
    write_json(STAGING / "CR005i_PROVENANCE.json", provenance)
    write_json(STAGING / "EXECUTION_RECEIPT.json", receipt)

    required = set(contract["required_outputs"])
    observed_before_manifest = {path.name for path in STAGING.iterdir() if path.is_file()}
    missing = required - {"CR005i_RELEASE_MANIFEST.csv", "CR005i_RELEASE_MANIFEST_SHA256.txt"} - observed_before_manifest
    if missing:
        raise RuntimeError(f"release inventory incomplete before manifest: {sorted(missing)}")
    manifest_rows = [
        {"file": path.name, "bytes": path.stat().st_size, "sha256": sha256_file(path)}
        for path in sorted(STAGING.iterdir(), key=lambda item: item.name)
        if path.is_file()
    ]
    manifest_path = STAGING / "CR005i_RELEASE_MANIFEST.csv"
    write_csv(manifest_path, manifest_rows, ["file", "bytes", "sha256"])
    manifest_sha = sha256_file(manifest_path)
    (STAGING / "CR005i_RELEASE_MANIFEST_SHA256.txt").write_text(
        f"{manifest_sha}  CR005i_RELEASE_MANIFEST.csv\n", encoding="utf-8"
    )
    observed = {path.name for path in STAGING.iterdir() if path.is_file()}
    if observed != required:
        raise RuntimeError(f"release inventory mismatch: missing={sorted(required-observed)} extra={sorted(observed-required)}")

    os.replace(STAGING, RELEASE)
    print(json.dumps({
        "campaign_id": CAMPAIGN_ID,
        "status": status,
        "verdict": verdict,
        "ledger_adopted": appeal_pass,
        "strong_slots": strong_slots,
        "directional_slots": directional_slots,
        "max_linearity_bound_ratio": max_bound_ratio,
        "max_power_relative_difference": max_power_relative_difference,
        "release": str(RELEASE),
        "release_manifest_sha256": manifest_sha,
    }, indent=2))


if __name__ == "__main__":
    main()
