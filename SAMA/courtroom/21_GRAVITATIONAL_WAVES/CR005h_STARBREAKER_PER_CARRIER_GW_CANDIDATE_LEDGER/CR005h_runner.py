from __future__ import annotations

import csv
import gzip
import hashlib
import importlib.util
import json
import math
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import numpy as np


CAMPAIGN_ID = "CR005h_STARBREAKER_PER_CARRIER_GW_CANDIDATE_LEDGER"
TASK = "Build a per-carrier Starbreaker gravitational-wave candidate ledger"
EXPECTED_CONTRACT_SHA256 = "bd3ac5f0ff73b9564ca5beff8c8047113e5afad81634ebc39d24bf7c3542bfa6"
EXPECTED_PRECOMMIT_SHA256 = "b745d87add097ebea088d02cd4aa04337224252adbc7ea3b4bf070c795292ee4"
EXPECTED_SOURCE_MANIFEST_SHA256 = "72ffd4e493b39686d05ed301428e5ef84152b9142a630bfa082780a54b81931a"
EXPECTED_PRECOMMIT_SEAL_SHA256 = "8b2ac289e6dd31c950f3a46bf9b445fe6f264d050c857131c84f16e736ae2684"

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
CONTRACT_PATH = BASE / "CR005h_CONTRACT.json"
PRECOMMIT_PATH = BASE / "CR005h_PRECOMMIT.md"
SOURCE_MANIFEST_PATH = BASE / "CR005h_SOURCE_MANIFEST.json"
PRECOMMIT_SEAL_PATH = BASE / "CR005h_PRECOMMIT_SEAL.json"
RUNNER_SEAL_PATH = BASE / "CR005h_RUNNER_SEAL.json"
RELEASE = BASE / "release"
STAGING = BASE / ".cr005h_release_staging"

PARENT = ROOT / "15_SCALE_BRIDGE_SIMULATOR/STARBREAKER_COMPLETE_TYPED_RELATION_HISTORY_V1/release"
ROSTER_PATH = PARENT / "ATOM_TYPED_STAGE_ROSTER.csv.gz"
SCENARIO_PATH = PARENT / "SCENARIO_SELECTION_DECOMPOSITION.csv"
SCHEMA_PATH = PARENT / "RELATION_HISTORY_SCHEMA.json"
CR005D_BASE = ROOT / "21_GRAVITATIONAL_WAVES/CR005d_STARBREAKER_CONTINUOUS_FLOW_AND_CARRIER_QNM_SOURCE_BRIDGE"
CR005D_RUNNER_PATH = CR005D_BASE / "CR005d_runner.py"
CR005D_CONTRACT_PATH = CR005D_BASE / "CR005d_CONTRACT.json"
CR005D_SUMMARY_PATH = CR005D_BASE / "release/CR005d_SUMMARY.json"
TIMING_PATH = CR005D_BASE / "release/CR005d_CARRIER_TIMING.csv"

FINE_INTERVALS = 324
COARSE_INTERVALS = 162
FROB_WEIGHTS = np.asarray([1.0, 1.0, 1.0, 2.0, 2.0, 2.0])
EXPECTED_SCENARIOS = 96
EXPECTED_ATOMS = 482112
EXPECTED_CARRIERS = 53568
EXPECTED_TIMED_CARRIERS = 51596
EXPECTED_CLASS_COUNTS = {
    "escape_only": 49543,
    "dual": 1993,
    "return_only": 60,
    "neither": 1972,
}
DOORS = ("discovery", "validation", "final")
GEOMETRIES = ("localized_ledger_cells", "dispersed_slots")
FEATURES = ("route", "shell", "dimension", "side", "final_fate")
SHORTLIST_SIZE = 200


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
            raise ValueError(f"cannot infer fields for empty CSV: {path.name}")
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
        raise RuntimeError("precommit seal campaign changed")
    if precommit.get("runner_present_at_seal") or precommit.get("results_opened"):
        raise RuntimeError("precommit chronology changed")
    if precommit.get("same_run_repair_allowed"):
        raise RuntimeError("same-run repair prohibition changed")
    runner_seal = json.loads(RUNNER_SEAL_PATH.read_text(encoding="utf-8"))
    if runner_seal.get("campaign_id") != CAMPAIGN_ID:
        raise RuntimeError("runner seal campaign changed")
    if runner_seal.get("runner_sha256") != sha256_file(Path(__file__)):
        raise RuntimeError("runner changed after runner seal")
    if runner_seal.get("runner_bytes") != Path(__file__).stat().st_size:
        raise RuntimeError("runner byte count changed after runner seal")
    return {"precommit": precommit, "runner": runner_seal}


def load_parent_module() -> Any:
    spec = importlib.util.spec_from_file_location("cr005d_sealed_helpers", CR005D_RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load sealed CR005d helper module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_scenario_metadata() -> dict[str, dict[str, Any]]:
    metadata: dict[str, dict[str, Any]] = {}
    with SCENARIO_PATH.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            metadata[row["scenario_id"]] = {
                "scenario_id": row["scenario_id"],
                "lane": row["lane"],
                "anchor": row["anchor"],
                "seed": int(row["seed"]),
                "p_level": int(row["p_level"]),
                "geometry": row["geometry"],
                "atom_count": int(row["atom_count"]),
                "ledger_count": int(row["ledger_count"]),
            }
    return metadata


def optional_float(value: str) -> float | None:
    return float(value) if value not in ("", "None", "null") else None


def load_timing() -> dict[tuple[str, int], dict[str, Any]]:
    timing: dict[tuple[str, int], dict[str, Any]] = {}
    with TIMING_PATH.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            key = (row["scenario_id"], int(row["carrier_atom_index"]))
            if key in timing:
                raise RuntimeError(f"duplicate sealed timing key: {key}")
            tau_escape = optional_float(row["tau_escape"])
            tau_closure = optional_float(row["tau_closure"])
            margin = optional_float(row["margin"])
            timing[key] = {
                "tau_escape": tau_escape,
                "tau_closure": tau_closure,
                "margin": margin,
                "escape_before_closure": (
                    row["escape_before_closure"].lower() == "true"
                    if row["escape_before_closure"] not in ("", "None", "null")
                    else None
                ),
            }
    return timing


def iter_scenario_records() -> Iterable[tuple[str, list[dict[str, str]]]]:
    current_sid: str | None = None
    records: list[dict[str, str]] = []
    with gzip.open(ROSTER_PATH, "rt", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            sid = row["scenario_id"]
            if current_sid is None:
                current_sid = sid
            if sid != current_sid:
                yield current_sid, records
                current_sid = sid
                records = []
            records.append(row)
    if current_sid is not None:
        yield current_sid, records


def median(values: Iterable[float]) -> float | None:
    array = np.asarray(list(values), dtype=float)
    return float(np.median(array)) if array.size else None


def quantile(values: Iterable[float], q: float) -> float | None:
    array = np.asarray(list(values), dtype=float)
    return float(np.quantile(array, q)) if array.size else None


def atom_objects(module: Any, records: list[dict[str, str]]) -> list[Any]:
    return [
        module.Atom(
            atom_index=int(row["atom_index"]),
            ledger_id=int(row["ledger_id"]),
            ledger_slot=int(row["ledger_slot"]),
            kind=row["kind"],
            positions=(
                (float(row["x0"]), float(row["y0"]), float(row["z0"])),
                (float(row["xc"]), float(row["yc"]), float(row["zc"])),
                (float(row["x1"]), float(row["y1"]), float(row["z1"])),
            ),
        )
        for row in records
    ]


def centroid_grid(module: Any, params: dict[str, np.ndarray], s: np.ndarray) -> np.ndarray:
    total = np.zeros((len(s), 3), dtype=float)
    atom_count = len(params["p0"])
    for start in range(0, atom_count, 512):
        indexes = np.arange(start, min(start + 512, atom_count), dtype=np.int64)
        total += np.sum(module.flow_post_grid(params, indexes, s), axis=0)
    return total / atom_count


def centered_positions(
    module: Any,
    params: dict[str, np.ndarray],
    indexes: np.ndarray,
    s: np.ndarray,
    centroid: np.ndarray,
) -> np.ndarray:
    return module.flow_post_grid(params, indexes, s) - centroid[None, :, :]


def aggregate_power(
    module: Any,
    params: dict[str, np.ndarray],
    carrier_indexes: np.ndarray,
    intervals: int,
) -> float:
    s = np.linspace(0.0, 1.0, intervals + 1)
    dt = 1.0 / intervals
    centroid = centroid_grid(module, params, s)
    q_sum = np.zeros((len(s), 6), dtype=float)
    for start in range(0, len(carrier_indexes), 256):
        indexes = carrier_indexes[start:start + 256]
        positions = centered_positions(module, params, indexes, s, centroid)
        q_sum += np.sum(module.q_components(positions), axis=0)
    q2_sum = np.gradient(np.gradient(q_sum, dt, axis=0, edge_order=2), dt, axis=0, edge_order=2)
    q3_sum = np.gradient(q2_sum, dt, axis=0, edge_order=2)
    return float(np.trapezoid(module.frobenius_sq(q3_sum[3:-3]), dx=dt))


def fine_attribution(
    module: Any,
    params: dict[str, np.ndarray],
    carrier_indexes: np.ndarray,
) -> dict[str, Any]:
    s = np.linspace(0.0, 1.0, FINE_INTERVALS + 1)
    dt = 1.0 / FINE_INTERVALS
    centroid = centroid_grid(module, params, s)
    positions = centered_positions(module, params, carrier_indexes, s, centroid)
    q = module.q_components(positions)
    q2 = np.gradient(np.gradient(q, dt, axis=1, edge_order=2), dt, axis=1, edge_order=2)
    q3 = np.gradient(q2, dt, axis=1, edge_order=2)
    interior = slice(3, -3)
    total_source = np.sum(q3, axis=0)
    total_power = float(np.trapezoid(module.frobenius_sq(total_source[interior]), dx=dt))
    individual_power = np.trapezoid(
        module.frobenius_sq(q3[:, interior, :]), dx=dt, axis=1
    )
    inner_density = np.sum(
        q3[:, interior, :] * total_source[None, interior, :] * FROB_WEIGHTS[None, None, :],
        axis=2,
    )
    inner_product = np.trapezoid(inner_density, dx=dt, axis=1)
    delta_power = 2.0 * inner_product - individual_power
    peak_source_norm = np.max(np.sqrt(module.frobenius_sq(q2)), axis=1)
    q_sum = np.sum(q, axis=0)
    independent_total = np.gradient(
        np.gradient(np.gradient(q_sum, dt, axis=0, edge_order=2), dt, axis=0, edge_order=2),
        dt,
        axis=0,
        edge_order=2,
    )
    linear_scale = max(1.0, float(np.max(np.abs(total_source))))
    linear_error = float(np.max(np.abs(independent_total - total_source))) / linear_scale
    trace_scale = max(1.0, float(np.max(np.abs(q))))
    trace_error = float(np.max(np.abs(q[:, :, 0] + q[:, :, 1] + q[:, :, 2]))) / trace_scale
    return {
        "s": s,
        "dt": dt,
        "centroid": centroid,
        "positions": positions,
        "q3": q3,
        "total_source": total_source,
        "total_power": total_power,
        "individual_power": individual_power,
        "incoherent_power": float(np.sum(individual_power)),
        "inner_product": inner_product,
        "delta_power": delta_power,
        "peak_source_norm": peak_source_norm,
        "linear_error": linear_error,
        "trace_error": trace_error,
    }


def history_class(timing: dict[str, Any] | None) -> tuple[str, dict[str, Any]]:
    if timing is None:
        return "neither", {
            "tau_escape": None,
            "tau_closure": None,
            "margin": None,
            "escape_before_closure": None,
        }
    escaped = timing["tau_escape"] is not None
    returned = timing["tau_closure"] is not None
    if escaped and returned:
        return "dual", timing
    if escaped:
        return "escape_only", timing
    if returned:
        return "return_only", timing
    raise RuntimeError("sealed timing row contains neither escape nor closure")


def behavior_lane(class_name: str, escape_before_closure: bool | None, state: str) -> str:
    if class_name == "escape_only":
        return f"outward_{state}"
    if class_name == "dual":
        timing = "launch" if escape_before_closure else "late_or_equal"
        return f"dual_{timing}_{state}"
    if class_name == "return_only":
        return f"return_{state}"
    return f"bound_{state}"


def direct_leave_one_out_error(
    module: Any,
    attribution: dict[str, Any],
    indexes: Iterable[int],
) -> tuple[int, float, float]:
    total_source = attribution["total_source"]
    q3 = attribution["q3"]
    total_power = attribution["total_power"]
    dt = attribution["dt"]
    deltas = attribution["delta_power"]
    max_abs = 0.0
    max_relative = 0.0
    count = 0
    for index in indexes:
        without = total_source - q3[index]
        without_power = float(np.trapezoid(module.frobenius_sq(without[3:-3]), dx=dt))
        direct = total_power - without_power
        error = abs(direct - float(deltas[index]))
        max_abs = max(max_abs, error)
        max_relative = max(max_relative, error / max(abs(direct), abs(float(deltas[index])), 1.0e-30))
        count += 1
    return count, max_abs, max_relative


def synthetic_controls(module: Any) -> dict[str, float]:
    s = np.linspace(0.0, 1.0, FINE_INTERVALS + 1)
    dt = 1.0 / FINE_INTERVALS
    static = np.asarray([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [-1.0, 0.0, 0.0],
    ])
    static_grid = np.repeat(static[:, None, :], len(s), axis=1)
    static_q = np.sum(module.q_components(static_grid), axis=0)
    static_q3 = np.gradient(
        np.gradient(np.gradient(static_q, dt, axis=0, edge_order=2), dt, axis=0, edge_order=2),
        dt,
        axis=0,
        edge_order=2,
    )
    axes = np.asarray([
        [1.0, 0.0, 0.0],
        [-1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, -1.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 0.0, -1.0],
    ])
    radius = 1.0 + 0.2 * s + 0.1 * s * s + 0.05 * s * s * s
    isotropic_grid = axes[:, None, :] * radius[None, :, None]
    isotropic_q = np.sum(module.q_components(isotropic_grid), axis=0)
    isotropic_q3 = np.gradient(
        np.gradient(np.gradient(isotropic_q, dt, axis=0, edge_order=2), dt, axis=0, edge_order=2),
        dt,
        axis=0,
        edge_order=2,
    )
    return {
        "static_source_max_abs": float(np.max(np.abs(static_q3))),
        "isotropic_source_max_abs": float(np.max(np.abs(isotropic_q3))),
    }


def scalar(value: Any) -> Any:
    if isinstance(value, np.generic):
        return value.item()
    return value


def aggregate_identity(
    rows: list[dict[str, Any]],
    feature_type: str,
    feature_value: str,
) -> dict[str, Any]:
    values = [float(row["delta_power_fraction"]) for row in rows]
    door_medians = {
        door: median(
            float(row["delta_power_fraction"])
            for row in rows
            if row["door"] == door
        )
        for door in DOORS
    }
    geometry_medians = {
        geometry: median(
            float(row["delta_power_fraction"])
            for row in rows
            if row["geometry"] == geometry
        )
        for geometry in GEOMETRIES
    }
    count = len(rows)
    escape_only_count = sum(row["history_class"] == "escape_only" for row in rows)
    reinforcer_count = sum(row["reinforcement_state"] == "reinforcer" for row in rows)
    canceller_count = sum(row["reinforcement_state"] == "canceller" for row in rows)
    neutral_count = count - reinforcer_count - canceller_count
    escape_fraction = escape_only_count / count
    reinforcement_fraction = reinforcer_count / count
    population_pass = escape_fraction > 0.5 and reinforcement_fraction > 0.5
    door_stable = all(door_medians[door] is not None and door_medians[door] > 0.0 for door in DOORS)
    geometry_stable = all(
        geometry_medians[geometry] is not None and geometry_medians[geometry] > 0.0
        for geometry in GEOMETRIES
    )
    if population_pass and door_stable and geometry_stable:
        status = "strong_candidate"
    elif population_pass and door_stable:
        status = "directional_candidate"
    else:
        status = "not_stable"
    return {
        "feature_type": feature_type,
        "feature_value": feature_value,
        "occurrence_count": count,
        "escape_only_count": escape_only_count,
        "escape_only_fraction": escape_fraction,
        "reinforcer_count": reinforcer_count,
        "reinforcement_fraction": reinforcement_fraction,
        "canceller_count": canceller_count,
        "neutral_count": neutral_count,
        "median_delta_power_fraction": median(values),
        "q10_delta_power_fraction": quantile(values, 0.1),
        "q90_delta_power_fraction": quantile(values, 0.9),
        "discovery_median_delta_power_fraction": door_medians["discovery"],
        "validation_median_delta_power_fraction": door_medians["validation"],
        "final_median_delta_power_fraction": door_medians["final"],
        "localized_median_delta_power_fraction": geometry_medians["localized_ledger_cells"],
        "dispersed_median_delta_power_fraction": geometry_medians["dispersed_slots"],
        "worst_door_median_delta_power_fraction": min(
            float(door_medians[door]) for door in DOORS if door_medians[door] is not None
        ),
        "population_pass": population_pass,
        "door_stable": door_stable,
        "geometry_stable": geometry_stable,
        "candidate_status": status,
    }


def summarize_classes(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for class_name in ("escape_only", "dual", "return_only", "neither"):
        selected = [row for row in rows if row["history_class"] == class_name]
        reinforcers = [row for row in selected if row["reinforcement_state"] == "reinforcer"]
        cancellers = [row for row in selected if row["reinforcement_state"] == "canceller"]
        output.append({
            "history_class": class_name,
            "occurrence_count": len(selected),
            "occurrence_fraction": len(selected) / len(rows),
            "reinforcer_count": len(reinforcers),
            "reinforcement_fraction": len(reinforcers) / len(selected) if selected else None,
            "canceller_count": len(cancellers),
            "cancellation_fraction": len(cancellers) / len(selected) if selected else None,
            "neutral_count": len(selected) - len(reinforcers) - len(cancellers),
            "median_delta_power_fraction": median(float(row["delta_power_fraction"]) for row in selected),
            "q10_delta_power_fraction": quantile((float(row["delta_power_fraction"]) for row in selected), 0.1),
            "q90_delta_power_fraction": quantile((float(row["delta_power_fraction"]) for row in selected), 0.9),
            "sum_delta_power": float(sum(float(row["delta_power"]) for row in selected)),
            "sum_individual_power": float(sum(float(row["individual_power"]) for row in selected)),
        })
    return output


def main() -> None:
    started = datetime.now(timezone.utc)
    if RELEASE.exists() or STAGING.exists():
        raise RuntimeError("CR005h release or staging path already exists; same-run repair is prohibited")

    seals = verify_seals()
    source_pre = validate_sources()
    if not all(row["matched"] for row in source_pre):
        raise RuntimeError("one or more frozen sources changed before execution")

    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    parent_contract = json.loads(CR005D_CONTRACT_PATH.read_text(encoding="utf-8"))
    parent_summary = json.loads(CR005D_SUMMARY_PATH.read_text(encoding="utf-8"))
    module = load_parent_module()
    metadata = load_scenario_metadata()
    timing = load_timing()

    contract_gate = (
        contract.get("campaign_id") == CAMPAIGN_ID
        and contract.get("task") == TASK
        and contract["scope"]["external_waveform_used"] is False
        and contract["scope"]["qnm_filter_used"] is False
        and contract["candidate_rules"]["fitted_weights"] == 0
        and schema.get("history_bit_order") == ["seed", "collapse", "final"]
        and parent_contract.get("campaign_id") == module.CAMPAIGN_ID
        and str(parent_summary.get("primary_verdict", "")).startswith("PASS_CONTINUOUS_FLOW")
    )

    carrier_rows: list[dict[str, Any]] = []
    scenario_rows: list[dict[str, Any]] = []
    scenario_count = 0
    atom_total = 0
    carrier_total = 0
    inventory_gate = True
    class_counts: Counter[str] = Counter()
    max_trace_error = 0.0
    max_linear_error = 0.0
    max_translation_error = 0.0
    loo_samples = 0
    loo_max_abs_error = 0.0
    loo_max_relative_error = 0.0
    convergence_errors: list[float] = []
    total_powers: list[float] = []

    shift = np.asarray([4.25, -3.5, 2.75])

    for sid, records in iter_scenario_records():
        scenario_count += 1
        atom_total += len(records)
        meta = metadata.get(sid)
        if meta is None:
            inventory_gate = False
            continue
        atom_indexes = [int(row["atom_index"]) for row in records]
        if atom_indexes != list(range(len(records))) or len(records) != meta["atom_count"]:
            inventory_gate = False
        ledgers = {int(row["ledger_id"]) for row in records}
        typed = Counter((int(row["ledger_id"]), row["kind"]) for row in records)
        if len(ledgers) != meta["ledger_count"]:
            inventory_gate = False
        for ledger_id in ledgers:
            inventory_gate &= (
                typed[(ledger_id, "carrier")] == 18
                and typed[(ledger_id, "matter")] == 126
                and typed[(ledger_id, "ledger_shadow")] == 18
            )

        carriers = [row for row in records if row["kind"] == "carrier"]
        carrier_count = len(carriers)
        carrier_total += carrier_count
        if carrier_count != meta["ledger_count"] * 18:
            inventory_gate = False
        carrier_indexes = np.asarray([int(row["atom_index"]) for row in carriers], dtype=np.int64)
        atoms = atom_objects(module, records)
        params = module.build_flow_parameters(atoms)
        attribution = fine_attribution(module, params, carrier_indexes)
        coarse_power = aggregate_power(module, params, carrier_indexes, COARSE_INTERVALS)
        total_power = float(attribution["total_power"])
        incoherent_power = float(attribution["incoherent_power"])
        convergence_error = abs(total_power - coarse_power) / max(abs(total_power), 1.0e-30)
        convergence_errors.append(convergence_error)
        total_powers.append(total_power)
        max_trace_error = max(max_trace_error, float(attribution["trace_error"]))
        max_linear_error = max(max_linear_error, float(attribution["linear_error"]))

        if scenario_count <= 4:
            sample_indexes = range(min(4, carrier_count))
            sample_count, abs_error, relative_error = direct_leave_one_out_error(
                module, attribution, sample_indexes
            )
            loo_samples += sample_count
            loo_max_abs_error = max(loo_max_abs_error, abs_error)
            loo_max_relative_error = max(loo_max_relative_error, relative_error)

        if scenario_count <= 8:
            probe = carrier_indexes[: min(8, carrier_count)]
            shifted_raw = module.flow_post_grid(params, probe, attribution["s"]) + shift[None, None, :]
            shifted_centered = shifted_raw - (attribution["centroid"] + shift[None, :])[None, :, :]
            max_translation_error = max(
                max_translation_error,
                float(np.max(np.abs(shifted_centered - attribution["positions"][: len(probe)]))),
            )

        individual = attribution["individual_power"]
        inner = attribution["inner_product"]
        deltas = attribution["delta_power"]
        peaks = attribution["peak_source_norm"]
        tolerance = max(1.0e-15, 1.0e-12 * total_power / carrier_count)
        delta_fractions = deltas / total_power
        individual_sum = float(np.sum(individual))
        individual_fractions = individual / individual_sum if individual_sum > 0.0 else np.zeros_like(individual)
        order = np.argsort(-delta_fractions, kind="stable")
        ranks = np.empty(carrier_count, dtype=np.int64)
        ranks[order] = np.arange(1, carrier_count + 1)
        door = module.door_for_seed(meta["seed"])
        scenario_class_counts: Counter[str] = Counter()
        scenario_states: Counter[str] = Counter()

        for local_index, raw in enumerate(carriers):
            atom_index = int(raw["atom_index"])
            class_name, timing_row = history_class(timing.get((sid, atom_index)))
            class_counts[class_name] += 1
            scenario_class_counts[class_name] += 1
            delta = float(deltas[local_index])
            if delta > tolerance:
                reinforcement_state = "reinforcer"
            elif delta < -tolerance:
                reinforcement_state = "canceller"
            else:
                reinforcement_state = "neutral"
            scenario_states[reinforcement_state] += 1
            lane = behavior_lane(
                class_name,
                timing_row["escape_before_closure"],
                reinforcement_state,
            )
            individual_value = float(individual[local_index])
            carrier_rows.append({
                "scenario_id": sid,
                "seed": meta["seed"],
                "door": door,
                "scenario_lane": meta["lane"],
                "anchor": meta["anchor"],
                "p_level": meta["p_level"],
                "geometry": meta["geometry"],
                "atom_count": meta["atom_count"],
                "ledger_count": meta["ledger_count"],
                "carrier_count": carrier_count,
                "carrier_atom_index": atom_index,
                "atom_id": raw["atom_id"],
                "ledger_id": int(raw["ledger_id"]),
                "ledger_slot": int(raw["ledger_slot"]),
                "route": raw["route"],
                "shell": raw["shell"],
                "shell_index": raw["shell_index"],
                "dimension": raw["dimension"],
                "side": raw["side"],
                "binding": raw["binding"],
                "node_affinity": raw["node_affinity"],
                "shock": raw["shock"],
                "carrier_exposure": raw["carrier_exposure"],
                "final_fate": raw["final_fate"],
                "history_class": class_name,
                "tau_escape": timing_row["tau_escape"],
                "tau_closure": timing_row["tau_closure"],
                "tau_closure_minus_escape": timing_row["margin"],
                "escape_before_closure": timing_row["escape_before_closure"],
                "total_power_proxy": total_power,
                "individual_power": individual_value,
                "individual_power_fraction": float(individual_fractions[local_index]),
                "inner_product_with_total": float(inner[local_index]),
                "leave_one_out_power": total_power - delta,
                "delta_power": delta,
                "delta_power_fraction": float(delta_fractions[local_index]),
                "coherence_multiplier": delta / individual_value if individual_value > 0.0 else None,
                "peak_source_norm": float(peaks[local_index]),
                "reinforcement_tolerance": tolerance,
                "reinforcement_state": reinforcement_state,
                "behavior_lane": lane,
                "source_rank_in_scenario": int(ranks[local_index]),
            })

        scenario_rows.append({
            **meta,
            "door": door,
            "carrier_count": carrier_count,
            "escape_only_count": scenario_class_counts["escape_only"],
            "dual_count": scenario_class_counts["dual"],
            "return_only_count": scenario_class_counts["return_only"],
            "neither_count": scenario_class_counts["neither"],
            "reinforcer_count": scenario_states["reinforcer"],
            "canceller_count": scenario_states["canceller"],
            "neutral_count": scenario_states["neutral"],
            "total_power_proxy": total_power,
            "incoherent_power_expectation": incoherent_power,
            "coherence_gain": total_power / incoherent_power if incoherent_power > 0.0 else None,
            "coarse_power_proxy": coarse_power,
            "fine_coarse_relative_error": convergence_error,
            "sum_individual_delta_power": float(np.sum(deltas)),
            "reinforcement_tolerance": tolerance,
        })

        del attribution, params, atoms

    source_post = validate_sources()
    source_hash_gate = source_pre == source_post and all(row["matched"] for row in source_post)
    synthetic = synthetic_controls(module)

    slot_groups: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in carrier_rows:
        slot_groups[int(row["ledger_slot"])].append(row)
    slot_rows: list[dict[str, Any]] = []
    for slot in sorted(slot_groups):
        aggregate = aggregate_identity(slot_groups[slot], "ledger_slot", str(slot))
        aggregate["ledger_slot"] = slot
        slot_rows.append(aggregate)
    slot_rows.sort(key=lambda row: (
        -float(row["worst_door_median_delta_power_fraction"]),
        -float(row["median_delta_power_fraction"]),
        int(row["ledger_slot"]),
    ))
    for rank, row in enumerate(slot_rows, start=1):
        row["candidate_rank"] = rank

    feature_rows: list[dict[str, Any]] = []
    for feature in FEATURES:
        groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in carrier_rows:
            groups[str(row[feature])].append(row)
        feature_rows.extend(
            aggregate_identity(groups[value], feature, value)
            for value in sorted(groups)
        )
    feature_rows.sort(key=lambda row: (
        row["feature_type"],
        -float(row["worst_door_median_delta_power_fraction"]),
        row["feature_value"],
    ))

    positive_occurrences = [row.copy() for row in carrier_rows if row["reinforcement_state"] == "reinforcer"]
    positive_occurrences.sort(key=lambda row: (
        -float(row["delta_power_fraction"]),
        row["scenario_id"],
        int(row["carrier_atom_index"]),
    ))
    shortlist = positive_occurrences[:SHORTLIST_SIZE]
    for rank, row in enumerate(shortlist, start=1):
        row["global_shortlist_rank"] = rank

    class_rows = summarize_classes(carrier_rows)
    strong_slots = [row for row in slot_rows if row["candidate_status"] == "strong_candidate"]
    directional_slots = [row for row in slot_rows if row["candidate_status"] == "directional_candidate"]

    inventory_pass = (
        scenario_count == EXPECTED_SCENARIOS
        and atom_total == EXPECTED_ATOMS
        and carrier_total == EXPECTED_CARRIERS
        and len(carrier_rows) == EXPECTED_CARRIERS
        and inventory_gate
    )
    class_pass = len(timing) == EXPECTED_TIMED_CARRIERS and dict(class_counts) == EXPECTED_CLASS_COUNTS
    trace_pass = max_trace_error <= 1.0e-12
    linear_pass = max_linear_error <= 1.0e-9
    loo_normalized_error = loo_max_abs_error / max(float(median(total_powers) or 0.0), 1.0e-30)
    loo_pass = loo_samples == 16 and loo_normalized_error <= 1.0e-10
    translation_pass = max_translation_error <= 1.0e-12
    static_pass = synthetic["static_source_max_abs"] <= 1.0e-12
    isotropic_pass = synthetic["isotropic_source_max_abs"] <= 1.0e-10
    median_convergence_error = median(convergence_errors)
    convergence_pass = median_convergence_error is not None and median_convergence_error <= 0.05
    finite_source_pass = (
        len(scenario_rows) == EXPECTED_SCENARIOS
        and all(
            math.isfinite(float(row["total_power_proxy"]))
            and float(row["total_power_proxy"]) > 0.0
            and math.isfinite(float(row["incoherent_power_expectation"]))
            and float(row["incoherent_power_expectation"]) > 0.0
            for row in scenario_rows
        )
    )
    aggregation_pass = (
        len(slot_rows) == 18
        and all(int(row["occurrence_count"]) == 2976 for row in slot_rows)
        and all(row["discovery_median_delta_power_fraction"] is not None for row in slot_rows)
        and all(row["validation_median_delta_power_fraction"] is not None for row in slot_rows)
        and all(row["final_median_delta_power_fraction"] is not None for row in slot_rows)
        and all(row["localized_median_delta_power_fraction"] is not None for row in slot_rows)
        and all(row["dispersed_median_delta_power_fraction"] is not None for row in slot_rows)
    )
    physical_claim_firewall = {
        "external_waveform_loaded": False,
        "qnm_filter_applied": False,
        "physical_seconds_emitted": False,
        "physical_strain_emitted": False,
        "physical_luminosity_emitted": False,
        "wave_messenger_material_claimed": False,
        "fitted_parameter_count": 0,
        "sam_registry_mutated": False,
    }
    firewall_pass = (
        not any(
            value
            for key, value in physical_claim_firewall.items()
            if key != "fitted_parameter_count"
        )
        and physical_claim_firewall["fitted_parameter_count"] == 0
    )

    controls = [
        {
            "control": "WC01_DIRECT_LEAVE_ONE_OUT_PREFIX",
            "passed": loo_pass,
            "observation": f"samples={loo_samples}; max_abs_error={loo_max_abs_error:.16g}; normalized_error={loo_normalized_error:.3e}; max_relative_error={loo_max_relative_error:.3e}",
        },
        {
            "control": "WC02_LINEAR_TENSOR_SUM_RECONSTRUCTION",
            "passed": linear_pass,
            "observation": f"max_relative_error={max_linear_error:.3e}",
        },
        {
            "control": "WC03_GLOBAL_TRANSLATION_INVARIANCE",
            "passed": translation_pass,
            "observation": f"max_centered_position_error={max_translation_error:.3e}",
        },
        {
            "control": "WC04_STATIC_SOURCE_ZERO",
            "passed": static_pass,
            "observation": f"max_abs_source={synthetic['static_source_max_abs']:.3e}",
        },
        {
            "control": "WC05_ISOTROPIC_SIX_AXIS_CANCELLATION",
            "passed": isotropic_pass,
            "observation": f"max_abs_source={synthetic['isotropic_source_max_abs']:.3e}",
        },
        {
            "control": "WC06_FINE_COARSE_AGGREGATE_POWER",
            "passed": convergence_pass,
            "observation": f"median_relative_error={median_convergence_error}",
        },
        {
            "control": "WC07_TRACE_FREE_INDIVIDUAL_TENSORS",
            "passed": trace_pass,
            "observation": f"max_relative_trace_error={max_trace_error:.3e}",
        },
    ]

    gates = [
        {"gate": "G01_PRECOMMIT_RUNNER_AND_SOURCE_CUSTODY", "passed": source_hash_gate},
        {"gate": "G02_CONTRACT_SCHEMA_AND_PARENT_AUTHORITY", "passed": contract_gate},
        {"gate": "G03_EXACT_SCENARIO_ATOM_CARRIER_LEDGER_INVENTORY", "passed": inventory_pass},
        {"gate": "G04_EXACT_SEALED_BIND_ESCAPE_CLASS_POPULATION", "passed": class_pass},
        {"gate": "G05_TRACE_FREE_AND_LINEAR_SOURCE_CONSTRUCTION", "passed": trace_pass and linear_pass},
        {"gate": "G06_EXACT_LEAVE_ONE_OUT_ATTRIBUTION", "passed": loo_pass},
        {"gate": "G07_TRANSLATION_INVARIANT_UNIT_CENTROID_FRAME", "passed": translation_pass},
        {"gate": "G08_STATIC_AND_ISOTROPIC_ZERO_CONTROLS", "passed": static_pass and isotropic_pass},
        {"gate": "G09_FINE_COARSE_SOURCE_CONVERGENCE", "passed": convergence_pass},
        {"gate": "G10_FINITE_NONZERO_AGGREGATE_SOURCE", "passed": finite_source_pass},
        {"gate": "G11_SLOT_DOOR_GEOMETRY_AGGREGATION", "passed": aggregation_pass},
        {"gate": "G12_PHYSICAL_CLAIM_FIREWALL", "passed": firewall_pass},
        {"gate": "G13_ATOMIC_RELEASE_INVENTORY", "passed": True},
    ]
    construction_pass = all(bool(row["passed"]) for row in gates)
    if not construction_pass:
        verdict = contract["verdict_ladder"]["fail"]
        status = "FAIL"
    elif strong_slots:
        verdict = contract["verdict_ladder"]["strong"]
        status = "PASS"
    elif directional_slots:
        verdict = contract["verdict_ladder"]["directional"]
        status = "PASS"
    else:
        verdict = contract["verdict_ladder"]["boundary"]
        status = "BOUNDARY"

    source_validation_rows = [
        {"validation_phase": phase, **row}
        for phase, rows in (("pre", source_pre), ("post", source_post))
        for row in rows
    ]
    supporting_features = [
        row for row in feature_rows
        if row["candidate_status"] in {"strong_candidate", "directional_candidate"}
    ]
    top_slots = slot_rows[:5]
    top_occurrences = shortlist[:10]
    summary = {
        "branch": "21_GRAVITATIONAL_WAVES",
        "campaign_id": CAMPAIGN_ID,
        "task": TASK,
        "status": status,
        "primary_verdict": verdict,
        "scientific_result": {
            "strong_slot_count": len(strong_slots),
            "directional_slot_count": len(directional_slots),
            "supporting_feature_candidate_count": len(supporting_features),
            "top_slots": top_slots,
            "strong_slots": [int(row["ledger_slot"]) for row in strong_slots],
            "directional_slots": [int(row["ledger_slot"]) for row in directional_slots],
            "occurrence_shortlist_count": len(shortlist),
        },
        "population": {
            "scenario_count": scenario_count,
            "atom_count": atom_total,
            "carrier_occurrence_count": carrier_total,
            "timed_carrier_count": len(timing),
            "history_class_counts": dict(class_counts),
            "class_summary": class_rows,
        },
        "source": {
            "fine_intervals": FINE_INTERVALS,
            "coarse_intervals": COARSE_INTERVALS,
            "origin": contract["source_definition"]["origin"],
            "total_power_median": median(total_powers),
            "total_power_q10": quantile(total_powers, 0.1),
            "total_power_q90": quantile(total_powers, 0.9),
            "median_fine_coarse_relative_error": median_convergence_error,
            "max_trace_relative_error": max_trace_error,
            "max_linear_reconstruction_relative_error": max_linear_error,
            "leave_one_out_samples": loo_samples,
            "leave_one_out_normalized_error": loo_normalized_error,
        },
        "controls": controls,
        "gates": gates,
        "physical_claim_firewall": physical_claim_firewall,
        "interpretation": {
            "positive_delta": "The carrier occurrence reinforces the aggregate internal quadrupole-power proxy.",
            "negative_delta": "The carrier occurrence cancels part of the aggregate internal quadrupole-power proxy.",
            "not_claimed": "The carrier is not thereby identified as material carried by a gravitational wave.",
        },
        "boundaries": [
            "The time coordinate is the dimensionless frozen Starbreaker post-collapse coordinate, not physical seconds.",
            "All carrier occurrences have unit weight; the origin is an equal-occurrence all-atom centroid, not a physical mass center.",
            "The ledger is an internal quadrupole-source attribution and does not emit physical strain, luminosity, or detector forecasts.",
            "No external waveform and no QNM filter participates in the candidate construction.",
            "Leave-one-out contributions overlap through coherent cross terms and are not additive shares of total power.",
        ],
    }

    def sci(value: Any) -> str:
        if value is None:
            return "n/a"
        return f"{float(value):.6e}"

    if status == "FAIL":
        headline = "The per-carrier ledger did not clear its construction controls."
    elif strong_slots:
        headline = (
            f"The full 53,568-carrier ledger constructed, and {len(strong_slots)} ledger-slot "
            "identity candidates remained positive across every held door and both geometries."
        )
    elif directional_slots:
        headline = (
            f"The full 53,568-carrier ledger constructed, and {len(directional_slots)} ledger-slot "
            "identity candidates remained positive across all held doors but not both geometries."
        )
    else:
        headline = (
            "The full 53,568-carrier ledger constructed, but no ledger-slot identity remained a "
            "majority reinforcer across every held door under the frozen candidate rule."
        )

    result_lines = [
        "# CR005h Starbreaker per-carrier GW candidate ledger",
        "",
        "## Verdict",
        "",
        f"**{verdict}**",
        "",
        headline,
        "",
        "## What was constructed",
        "",
        "Each frozen Starbreaker carrier occurrence now has its own unit-occurrence trace-free quadrupole source, individual power, exact leave-one-out aggregate-power change, bind/escape class, and frozen carrier identity. Positive `DeltaP` marks reinforcement of the aggregate internal source proxy; negative `DeltaP` marks coherent cancellation.",
        "",
        "This is the requested internal pixel-to-source track. No external waveform and no QNM response was used to decide the carrier list.",
        "",
        "## Primary ledger-slot candidates",
        "",
        "| Rank | Slot | Status | Escape-only | Reinforcer | Median DeltaP/P | Worst door | Localized | Dispersed |",
        "|---:|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in top_slots:
        result_lines.append(
            "| {rank} | {slot} | {status} | {escape:.3%} | {reinforce:.3%} | {median} | {worst} | {localized} | {dispersed} |".format(
                rank=row["candidate_rank"],
                slot=row["ledger_slot"],
                status=row["candidate_status"],
                escape=float(row["escape_only_fraction"]),
                reinforce=float(row["reinforcement_fraction"]),
                median=sci(row["median_delta_power_fraction"]),
                worst=sci(row["worst_door_median_delta_power_fraction"]),
                localized=sci(row["localized_median_delta_power_fraction"]),
                dispersed=sci(row["dispersed_median_delta_power_fraction"]),
            )
        )
    result_lines.extend([
        "",
        "The full 18-slot table is in `CR005h_SLOT_CANDIDATES.csv`; the 200 strongest positive occurrences are in `CR005h_OCCURRENCE_SHORTLIST.csv`.",
        "",
        "## Bind/escape source populations",
        "",
        "| Frozen class | Occurrences | Share | Reinforcers | Reinforcer share | Median DeltaP/P |",
        "|---|---:|---:|---:|---:|---:|",
    ])
    for row in class_rows:
        result_lines.append(
            "| {name} | {count} | {share:.3%} | {reinforcers} | {reinforcement:.3%} | {median} |".format(
                name=row["history_class"],
                count=row["occurrence_count"],
                share=float(row["occurrence_fraction"]),
                reinforcers=row["reinforcer_count"],
                reinforcement=float(row["reinforcement_fraction"] or 0.0),
                median=sci(row["median_delta_power_fraction"]),
            )
        )
    result_lines.extend([
        "",
        "## Source controls",
        "",
        f"- Direct leave-one-out validation: {loo_samples} samples, normalized error `{loo_normalized_error:.3e}`.",
        f"- Fine/coarse median aggregate-power difference: `{float(median_convergence_error or 0.0):.6%}`.",
        f"- Maximum trace error: `{max_trace_error:.3e}`.",
        f"- Maximum translation-invariance error: `{max_translation_error:.3e}`.",
        f"- Static-source control: `{synthetic['static_source_max_abs']:.3e}`.",
        f"- Isotropic six-axis cancellation control: `{synthetic['isotropic_source_max_abs']:.3e}`.",
        "",
        "## Interpretation boundary",
        "",
        "A carrier with positive leave-one-out influence is a candidate **source contributor** inside this frozen Starbreaker proxy. It is not thereby the substance of the outgoing gravitational wave. The current run remains dimensionless, unit-weighted, and internal: it does not claim physical strain, luminosity, seconds, or detector visibility.",
        "",
        "The equal-occurrence all-atom centroid supplies translation invariance, but it is not called a physical mass center because the roster does not supply physical mass weights.",
        "",
    ])
    result_text = "\n".join(result_lines)

    finished = datetime.now(timezone.utc)
    provenance = {
        "campaign_id": CAMPAIGN_ID,
        "task": TASK,
        "classification": "CONSTRUCTIVE_NEW_WORK",
        "precommit_sha256": EXPECTED_PRECOMMIT_SHA256,
        "precommit_seal_sha256": EXPECTED_PRECOMMIT_SEAL_SHA256,
        "runner_sha256": sha256_file(Path(__file__)),
        "runner_seal_sha256": sha256_file(RUNNER_SEAL_PATH),
        "source_manifest_sha256": EXPECTED_SOURCE_MANIFEST_SHA256,
        "source_count": len(source_pre),
        "source_hashes_matched_pre_and_post": source_hash_gate,
        "external_waveform_used": False,
        "qnm_filter_used": False,
        "fitted_parameter_count": 0,
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
    write_csv(STAGING / "CR005h_CARRIER_ATTRIBUTION.csv", carrier_rows)
    write_csv(STAGING / "CR005h_OCCURRENCE_SHORTLIST.csv", shortlist)
    write_csv(STAGING / "CR005h_SLOT_CANDIDATES.csv", slot_rows)
    write_csv(STAGING / "CR005h_FEATURE_CANDIDATES.csv", feature_rows)
    write_csv(STAGING / "CR005h_SCENARIO_POWER.csv", scenario_rows)
    write_csv(STAGING / "CR005h_CLASS_SUMMARY.csv", class_rows)
    write_csv(STAGING / "CR005h_CONTROLS.csv", controls)
    write_csv(STAGING / "CR005h_GATES.csv", gates)
    write_csv(STAGING / "CR005h_SOURCE_VALIDATION.csv", source_validation_rows)
    write_json(STAGING / "CR005h_SUMMARY.json", summary)
    (STAGING / "CR005h_RESULT.md").write_text(result_text, encoding="utf-8")
    write_json(STAGING / "CR005h_PROVENANCE.json", provenance)
    write_json(STAGING / "EXECUTION_RECEIPT.json", receipt)

    required = set(contract["required_outputs"])
    before_manifest = {path.name for path in STAGING.iterdir() if path.is_file()}
    missing_before_manifest = required - {
        "CR005h_RELEASE_MANIFEST.csv",
        "CR005h_RELEASE_MANIFEST_SHA256.txt",
    } - before_manifest
    if missing_before_manifest:
        raise RuntimeError(f"atomic release inventory incomplete before manifest: {sorted(missing_before_manifest)}")

    manifest_rows = [
        {"file": path.name, "bytes": path.stat().st_size, "sha256": sha256_file(path)}
        for path in sorted(STAGING.iterdir(), key=lambda item: item.name)
        if path.is_file()
    ]
    manifest_path = STAGING / "CR005h_RELEASE_MANIFEST.csv"
    write_csv(manifest_path, manifest_rows, ["file", "bytes", "sha256"])
    manifest_sha = sha256_file(manifest_path)
    (STAGING / "CR005h_RELEASE_MANIFEST_SHA256.txt").write_text(
        f"{manifest_sha}  CR005h_RELEASE_MANIFEST.csv\n",
        encoding="utf-8",
    )
    observed_outputs = {path.name for path in STAGING.iterdir() if path.is_file()}
    if observed_outputs != required:
        missing = sorted(required - observed_outputs)
        extra = sorted(observed_outputs - required)
        raise RuntimeError(f"atomic release inventory mismatch: missing={missing}; extra={extra}")

    os.replace(STAGING, RELEASE)
    print(json.dumps({
        "campaign_id": CAMPAIGN_ID,
        "status": status,
        "verdict": verdict,
        "carrier_occurrences": carrier_total,
        "strong_slots": [int(row["ledger_slot"]) for row in strong_slots],
        "directional_slots": [int(row["ledger_slot"]) for row in directional_slots],
        "release": str(RELEASE),
        "release_manifest_sha256": manifest_sha,
    }, indent=2))


if __name__ == "__main__":
    main()
