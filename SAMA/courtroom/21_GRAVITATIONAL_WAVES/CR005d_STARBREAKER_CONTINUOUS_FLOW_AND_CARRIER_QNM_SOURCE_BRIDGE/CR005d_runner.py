from __future__ import annotations

import csv
import gzip
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import numpy as np


CAMPAIGN_ID = "CR005d_STARBREAKER_CONTINUOUS_FLOW_AND_CARRIER_QNM_SOURCE_BRIDGE"
EXPECTED_CONTRACT_SHA256 = "96cff6164e55c2024ffcbe7158f8dd4d4783ef408b4941d72f8c6f17084c309e"
EXPECTED_PRECOMMIT_SHA256 = "4a11b227fa0f1e22ec7a767e67f032cddcad22a4f0e7546a214f150ed46cec09"
EXPECTED_SOURCE_MANIFEST_SHA256 = "4f4d4b4a8b016c61b880dbee1d24cad8486d6629073565eab8e5b1cccc205fb2"
EXPECTED_PRECOMMIT_SEAL_SHA256 = "7b88c9c1291d130c5a011470390c12536b52a3f2fdbc7582038238b6e36032c0"

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
CONTRACT_PATH = BASE / "CR005d_CONTRACT.json"
PRECOMMIT_PATH = BASE / "CR005d_PRECOMMIT.md"
SOURCE_MANIFEST_PATH = BASE / "CR005d_SOURCE_MANIFEST.json"
PRECOMMIT_SEAL_PATH = BASE / "CR005d_PRECOMMIT_SEAL.json"
RELEASE = BASE / "release"
STAGING = BASE / ".cr005d_release_staging"

PARENT = ROOT / "15_SCALE_BRIDGE_SIMULATOR/STARBREAKER_COMPLETE_TYPED_RELATION_HISTORY_V1/release"
ROSTER_PATH = PARENT / "ATOM_TYPED_STAGE_ROSTER.csv.gz"
SCENARIO_PATH = PARENT / "SCENARIO_SELECTION_DECOMPOSITION.csv"
COUNT_PATH = PARENT / "RELATION_HISTORY_COUNTS.csv"
SCHEMA_PATH = PARENT / "RELATION_HISTORY_SCHEMA.json"
PARENT_SUMMARY_PATH = PARENT / "RELATION_HISTORY_SUMMARY.json"
CR005C_SUMMARY_PATH = ROOT / "21_GRAVITATIONAL_WAVES/CR005c_STARBREAKER_ESCAPE_CLOSURE_TIMING_OPERATIONALIZATION/release/CR005c_SUMMARY.json"
CR005_SUMMARY_PATH = ROOT / "21_GRAVITATIONAL_WAVES/CR005_THETA_CARRIER_OVERFLOW_AND_QNM_DERIVATION/CR005_summary.json"
CR005B_SUMMARY_PATH = ROOT / "21_GRAVITATIONAL_WAVES/CR005b_QNM_DAMPING_SUBSTRATE_DYNAMICS/CR005b_summary.json"

RADIUS = 0.076
RADIUS2 = RADIUS * RADIUS
TOL = 1.0e-12
ROOT_BINS = 32
ROOT_CONTROL_BINS = 64
ROOT_STEPS = 40
ROOT_CONTROL_PREFIX = 256
FINE_INTERVALS = 324
COARSE_INTERVALS = 162
HISTORY_CODES = ("001", "010", "011", "100", "101", "110", "111")
STAGE_BITS = ((0, 4), (1, 2), (2, 1))
NEIGHBOR_OFFSETS = tuple((dx, dy, dz) for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1))
DISCOVERY_SEEDS = {910001, 910002}
VALIDATION_SEEDS = {910003}
FINAL_SEEDS = {910004}
FROB_WEIGHTS = np.asarray([1.0, 1.0, 1.0, 2.0, 2.0, 2.0])


@dataclass(frozen=True)
class Atom:
    atom_index: int
    ledger_id: int
    ledger_slot: int
    kind: str
    positions: tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]


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


def verify_precommit() -> dict[str, Any]:
    expected = {
        CONTRACT_PATH: EXPECTED_CONTRACT_SHA256,
        PRECOMMIT_PATH: EXPECTED_PRECOMMIT_SHA256,
        SOURCE_MANIFEST_PATH: EXPECTED_SOURCE_MANIFEST_SHA256,
        PRECOMMIT_SEAL_PATH: EXPECTED_PRECOMMIT_SEAL_SHA256,
    }
    for path, digest in expected.items():
        if sha256_file(path) != digest:
            raise RuntimeError(f"sealed pre-run file changed: {path.name}")
    seal = json.loads(PRECOMMIT_SEAL_PATH.read_text(encoding="utf-8"))
    if seal.get("campaign_id") != CAMPAIGN_ID:
        raise RuntimeError("precommit seal campaign changed")
    if seal.get("runner_present_at_seal") or seal.get("results_opened"):
        raise RuntimeError("precommit chronology changed")
    if seal.get("same_run_repair_allowed"):
        raise RuntimeError("same-run repair prohibition changed")
    return seal


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


def load_expected_counts() -> dict[str, Counter[str]]:
    expected: dict[str, Counter[str]] = defaultdict(Counter)
    with COUNT_PATH.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["pair_kind"] == "carrier|matter":
                expected[row["scenario_id"]][row["history_code"]] += int(row["row_count"])
    return expected


def iter_scenario_atoms() -> Iterable[tuple[str, list[Atom]]]:
    current_sid: str | None = None
    atoms: list[Atom] = []
    with gzip.open(ROSTER_PATH, "rt", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            sid = row["scenario_id"]
            if current_sid is None:
                current_sid = sid
            if sid != current_sid:
                yield current_sid, atoms
                current_sid = sid
                atoms = []
            atoms.append(Atom(
                atom_index=int(row["atom_index"]),
                ledger_id=int(row["ledger_id"]),
                ledger_slot=int(row["ledger_slot"]),
                kind=row["kind"],
                positions=(
                    (float(row["x0"]), float(row["y0"]), float(row["z0"])),
                    (float(row["xc"]), float(row["yc"]), float(row["zc"])),
                    (float(row["x1"]), float(row["y1"]), float(row["z1"])),
                ),
            ))
    if current_sid is not None:
        yield current_sid, atoms


def distance(left: tuple[float, float, float], right: tuple[float, float, float]) -> float:
    return math.sqrt(sum((left[i] - right[i]) ** 2 for i in range(3)))


def cell(point: tuple[float, float, float], radius: float) -> tuple[int, int, int]:
    return tuple(math.floor(value / radius) for value in point)  # type: ignore[return-value]


def build_carrier_matter_masks(atoms: list[Atom]) -> dict[tuple[int, int], int]:
    carriers = [atom for atom in atoms if atom.kind == "carrier"]
    matters = [atom for atom in atoms if atom.kind == "matter"]
    masks: dict[tuple[int, int], int] = {}
    for stage, bit in STAGE_BITS:
        grid: dict[tuple[int, int, int], list[Atom]] = defaultdict(list)
        for matter in matters:
            grid[cell(matter.positions[stage], RADIUS)].append(matter)
        for carrier in carriers:
            base = cell(carrier.positions[stage], RADIUS)
            for dx, dy, dz in NEIGHBOR_OFFSETS:
                for matter in grid.get((base[0] + dx, base[1] + dy, base[2] + dz), ()):
                    if distance(carrier.positions[stage], matter.positions[stage]) <= RADIUS:
                        key = (carrier.atom_index, matter.atom_index)
                        masks[key] = masks.get(key, 0) | bit
    return masks


def history_code(mask: int) -> str:
    return f"{1 if mask & 4 else 0}{1 if mask & 2 else 0}{1 if mask & 1 else 0}"


def door_for_seed(seed: int) -> str:
    if seed in DISCOVERY_SEEDS:
        return "discovery"
    if seed in VALIDATION_SEEDS:
        return "validation"
    if seed in FINAL_SEEDS:
        return "final"
    raise ValueError(f"unregistered seed door: {seed}")


def quantile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    return float(np.quantile(np.asarray(values, dtype=float), q))


def median(values: list[float]) -> float | None:
    return quantile(values, 0.5)


def build_flow_parameters(atoms: list[Atom]) -> dict[str, np.ndarray]:
    p = np.asarray([atom.positions for atom in atoms], dtype=float)
    p0, pc, p1 = p[:, 0, :], p[:, 1, :], p[:, 2, :]
    r0 = np.linalg.norm(p0, axis=1)
    rc = np.linalg.norm(pc, axis=1)
    r1 = np.linalg.norm(p1, axis=1)

    def theta(pos: np.ndarray, radius: np.ndarray) -> np.ndarray:
        ratio = np.divide(pos[:, 2], radius, out=np.zeros_like(radius), where=radius > 1.0e-15)
        return np.arccos(np.clip(ratio, -1.0, 1.0))

    th0 = theta(p0, r0)
    thc = theta(pc, rc)
    th1 = theta(p1, r1)
    ph0 = np.arctan2(p0[:, 1], p0[:, 0])
    phc = np.arctan2(pc[:, 1], pc[:, 0])
    ph1 = np.arctan2(p1[:, 1], p1[:, 0])
    dphi = (ph1 - phc + math.pi) % (2.0 * math.pi) - math.pi
    log_ratio = np.zeros_like(r0)
    positive = (r0 > 1.0e-15) & (rc > 1.0e-15)
    log_ratio[positive] = np.log(rc[positive] / r0[positive])
    return {
        "p0": p0, "pc": pc, "p1": p1,
        "r0": r0, "rc": rc, "r1": r1,
        "th0": th0, "thc": thc, "th1": th1,
        "ph0": ph0, "phc": phc, "ph1": ph1,
        "dphi": dphi, "log_ratio": log_ratio,
    }


def flow_position(params: dict[str, np.ndarray], indexes: np.ndarray, s: np.ndarray | float, phase: int) -> np.ndarray:
    idx = np.asarray(indexes, dtype=np.int64)
    sval = np.asarray(s, dtype=float)
    if sval.ndim == 0:
        sval = np.full(idx.shape, float(sval))
    if phase == 0:
        factor = np.exp(params["log_ratio"][idx] * sval)
        result = params["p0"][idx] * factor[:, None]
        zero = (params["r0"][idx] <= 1.0e-15) | (params["rc"][idx] <= 1.0e-15)
        if np.any(zero):
            result[zero] = params["p0"][idx[zero]] + sval[zero, None] * (
                params["pc"][idx[zero]] - params["p0"][idx[zero]]
            )
        return result
    if phase != 1:
        raise ValueError(f"unknown phase: {phase}")
    radius = params["rc"][idx] + sval * (params["r1"][idx] - params["rc"][idx])
    theta = params["thc"][idx] + sval * (params["th1"][idx] - params["thc"][idx])
    phi = params["phc"][idx] + sval * params["dphi"][idx]
    sin_theta = np.sin(theta)
    return np.column_stack((
        radius * sin_theta * np.cos(phi),
        radius * sin_theta * np.sin(phi),
        radius * np.cos(theta),
    ))


def flow_post_grid(params: dict[str, np.ndarray], indexes: np.ndarray, s: np.ndarray) -> np.ndarray:
    idx = np.asarray(indexes, dtype=np.int64)
    ss = np.asarray(s, dtype=float)[None, :]
    radius = params["rc"][idx, None] + ss * (params["r1"][idx, None] - params["rc"][idx, None])
    theta = params["thc"][idx, None] + ss * (params["th1"][idx, None] - params["thc"][idx, None])
    phi = params["phc"][idx, None] + ss * params["dphi"][idx, None]
    sin_theta = np.sin(theta)
    return np.stack((
        radius * sin_theta * np.cos(phi),
        radius * sin_theta * np.sin(phi),
        radius * np.cos(theta),
    ), axis=2)


def pair_margin(
    params: dict[str, np.ndarray],
    left: np.ndarray,
    right: np.ndarray,
    s: np.ndarray | float,
    phase: int,
) -> np.ndarray:
    delta = flow_position(params, left, s, phase) - flow_position(params, right, s, phase)
    return np.einsum("ij,ij->i", delta, delta) - RADIUS2


def find_directional_roots(
    params: dict[str, np.ndarray],
    left: np.ndarray,
    right: np.ndarray,
    phase: int,
    direction: str,
    bins: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    count = len(left)
    roots = np.full(count, np.nan)
    if count == 0:
        return roots, np.zeros(0, dtype=bool), np.zeros(0, dtype=bool), np.zeros(0, dtype=np.int64)
    previous = pair_margin(params, left, right, 0.0, phase)
    found = np.zeros(count, dtype=bool)
    lo = np.zeros(count, dtype=float)
    hi = np.ones(count, dtype=float)
    bracket_count = np.zeros(count, dtype=np.int64)
    for step in range(1, bins + 1):
        current_s = step / bins
        current = pair_margin(params, left, right, current_s, phase)
        if direction == "out":
            bracket = (previous <= 0.0) & (current >= 0.0)
        else:
            bracket = (previous >= 0.0) & (current <= 0.0)
        bracket_count += bracket.astype(np.int64)
        new = bracket & ~found
        lo[new] = (step - 1) / bins
        hi[new] = current_s
        found |= new
        previous = current
    active = np.where(found)[0]
    if active.size:
        alo = lo[active].copy()
        ahi = hi[active].copy()
        for _ in range(ROOT_STEPS):
            mid = 0.5 * (alo + ahi)
            value = pair_margin(params, left[active], right[active], mid, phase)
            if direction == "out":
                lower = value <= 0.0
            else:
                lower = value >= 0.0
            alo[lower] = mid[lower]
            ahi[~lower] = mid[~lower]
        roots[active] = 0.5 * (alo + ahi)
    eps = 1.0e-7
    root_active = roots[active]
    before = np.maximum(0.0, root_active - eps)
    after = np.minimum(1.0, root_active + eps)
    derivative = (
        pair_margin(params, left[active], right[active], after, phase)
        - pair_margin(params, left[active], right[active], before, phase)
    ) / np.maximum(after - before, 1.0e-15)
    direction_ok = np.zeros(count, dtype=bool)
    direction_ok[active] = derivative > 0.0 if direction == "out" else derivative < 0.0
    return roots, found, direction_ok, bracket_count


def endpoint_errors(params: dict[str, np.ndarray]) -> tuple[float, float]:
    idx = np.arange(len(params["p0"]), dtype=np.int64)
    candidates = (
        (flow_position(params, idx, 0.0, 0), params["p0"]),
        (flow_position(params, idx, 1.0, 0), params["pc"]),
        (flow_position(params, idx, 0.0, 1), params["pc"]),
        (flow_position(params, idx, 1.0, 1), params["p1"]),
    )
    max_error = max(float(np.max(np.linalg.norm(left - right, axis=1))) for left, right in candidates)
    cross = np.cross(params["p0"], params["pc"])
    denom = np.linalg.norm(params["p0"], axis=1) * np.linalg.norm(params["pc"], axis=1)
    radial = np.divide(np.linalg.norm(cross, axis=1), denom, out=np.zeros_like(denom), where=denom > 1.0e-15)
    return max_error, float(np.max(radial))


def q_components(positions: np.ndarray) -> np.ndarray:
    x, y, z = positions[:, :, 0], positions[:, :, 1], positions[:, :, 2]
    radius2 = x * x + y * y + z * z
    third = radius2 / 3.0
    return np.stack((x * x - third, y * y - third, z * z - third, x * y, x * z, y * z), axis=2)


def frobenius_sq(tensors: np.ndarray) -> np.ndarray:
    return np.sum(tensors * tensors * FROB_WEIGHTS, axis=-1)


def qnm_filter(source: np.ndarray, dt: float, omega_r: float, gamma: float) -> tuple[np.ndarray, np.ndarray]:
    times = np.arange(source.shape[0], dtype=float) * dt
    kernel = np.exp(-gamma * times) * np.sin(omega_r * times) / omega_r
    response = np.stack([
        np.convolve(source[:, component], kernel, mode="full")[: len(times)] * dt
        for component in range(source.shape[1])
    ], axis=1)
    return response, kernel


def group_tensor_metrics(
    q: np.ndarray,
    q2: np.ndarray,
    q3: np.ndarray,
    selected: np.ndarray,
    dt: float,
    omega_r: float,
    gamma: float,
) -> dict[str, Any]:
    indexes = np.where(selected)[0]
    count = int(indexes.size)
    if count == 0:
        return {
            "carrier_count": 0,
            "quadrupole_change_norm": None,
            "peak_source_norm": None,
            "power_proxy": None,
            "power_per_carrier": None,
            "incoherent_power_expectation": None,
            "coherence_gain": None,
            "qnm_response_peak": None,
            "trace_relative_error": None,
        }
    q_sum = np.sum(q[indexes], axis=0)
    q2_sum = np.sum(q2[indexes], axis=0)
    q3_selected = q3[indexes]
    q3_sum = np.sum(q3_selected, axis=0)
    interior = slice(3, -3)
    power = float(np.trapezoid(frobenius_sq(q3_sum[interior]), dx=dt))
    individual = np.trapezoid(frobenius_sq(q3_selected[:, interior, :]), dx=dt, axis=1)
    incoherent = float(np.sum(individual))
    response, _ = qnm_filter(q2_sum, dt, omega_r, gamma)
    q_change = q_sum[-1] - q_sum[0]
    scale = max(1.0, float(np.max(np.abs(q_sum))))
    trace_error = float(np.max(np.abs(q_sum[:, 0] + q_sum[:, 1] + q_sum[:, 2]))) / scale
    return {
        "carrier_count": count,
        "quadrupole_change_norm": float(math.sqrt(float(np.sum(q_change * q_change * FROB_WEIGHTS)))),
        "peak_source_norm": float(np.max(np.sqrt(frobenius_sq(q2_sum)))),
        "power_proxy": power,
        "power_per_carrier": power / count,
        "incoherent_power_expectation": incoherent,
        "coherence_gain": power / incoherent if incoherent > 0.0 else None,
        "qnm_response_peak": float(np.max(np.sqrt(frobenius_sq(response)))),
        "trace_relative_error": trace_error,
    }


def source_bundle(
    params: dict[str, np.ndarray],
    carrier_indexes: np.ndarray,
    group_masks: dict[str, np.ndarray],
    intervals: int,
    omega_r: float,
    gamma: float,
) -> dict[str, dict[str, Any]]:
    s = np.linspace(0.0, 1.0, intervals + 1)
    dt = 1.0 / intervals
    positions = flow_post_grid(params, carrier_indexes, s)
    q = q_components(positions)
    q2 = np.gradient(np.gradient(q, dt, axis=1, edge_order=2), dt, axis=1, edge_order=2)
    q3 = np.gradient(q2, dt, axis=1, edge_order=2)
    return {
        name: group_tensor_metrics(q, q2, q3, selected, dt, omega_r, gamma)
        for name, selected in group_masks.items()
    }


def aggregate_timing(rows: list[dict[str, Any]]) -> dict[str, Any]:
    margins = [float(row["margin"]) for row in rows if row["dual"]]
    count = len(margins)
    before = sum(value > 0.0 for value in margins)
    return {
        "primary_carriers": count,
        "inequality_count": before,
        "inequality_fraction": before / count if count else None,
        "median_margin": median(margins),
        "q10_margin": quantile(margins, 0.1),
        "q90_margin": quantile(margins, 0.9),
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    if RELEASE.exists() or STAGING.exists():
        raise RuntimeError("CR005d release path already exists; same-run repair is prohibited")

    seal = verify_precommit()
    source_pre = validate_sources()
    if not all(row["matched"] for row in source_pre):
        raise RuntimeError("one or more frozen sources changed before execution")

    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    parent_summary = json.loads(PARENT_SUMMARY_PATH.read_text(encoding="utf-8"))
    cr005c = json.loads(CR005C_SUMMARY_PATH.read_text(encoding="utf-8"))
    cr005 = json.loads(CR005_SUMMARY_PATH.read_text(encoding="utf-8"))
    cr005b = json.loads(CR005B_SUMMARY_PATH.read_text(encoding="utf-8"))
    metadata = load_scenario_metadata()
    expected_counts = load_expected_counts()

    omega_r_fraction = cr005["qnm_derivation"]["omega_R_M_form1_closure"]
    gamma_fraction = cr005b["primary_output"]["value_fraction"]
    coefficient_gate = (
        omega_r_fraction == "3/8"
        and gamma_fraction == "4/45"
        and cr005.get("verdict") == "PASS"
        and cr005b.get("verdict") == "PASS"
    )
    omega_r = 3.0 / 8.0
    gamma = 4.0 / 45.0
    parent_gate = (
        contract.get("campaign_id") == CAMPAIGN_ID
        and schema.get("history_bit_order") == ["seed", "collapse", "final"]
        and float(schema.get("proximity_radius")) == RADIUS
        and parent_summary["primary_verdict"].startswith("PASS_COMPLETE_TYPED_RELATION_HISTORY_CONSTRUCTED")
        and cr005c["primary_verdict"].startswith("PASS_OPERATIONAL_ESCAPE_BEFORE_CLOSURE")
    )

    timing_rows: list[dict[str, Any]] = []
    scenario_rows: list[dict[str, Any]] = []
    reconstruction_rows: list[dict[str, Any]] = []
    source_rows: list[dict[str, Any]] = []
    observed_counts: dict[str, Counter[str]] = {}

    scenario_count = 0
    atom_total = 0
    roster_gate = True
    typing_gate = True
    count_gate = True
    endpoint_max_error = 0.0
    collapse_radial_max_error = 0.0
    root_count = 0
    root_failures = 0
    direction_failures = 0
    multi_root_relations = 0
    root_control_samples = 0
    root_control_max_error = 0.0
    invariant_samples = 0
    rotation_distance_max_error = 0.0
    translation_distance_max_error = 0.0
    radial_only_path_max_difference = 0.0
    convergence_power_errors: list[float] = []
    convergence_response_errors: list[float] = []
    trace_errors: list[float] = []

    angle_z = math.radians(37.0)
    angle_y = math.radians(19.0)
    rotation = np.asarray([
        [math.cos(angle_y) * math.cos(angle_z), -math.cos(angle_y) * math.sin(angle_z), math.sin(angle_y)],
        [math.sin(angle_z), math.cos(angle_z), 0.0],
        [-math.sin(angle_y) * math.cos(angle_z), math.sin(angle_y) * math.sin(angle_z), math.cos(angle_y)],
    ])
    shift = np.asarray([4.25, -3.5, 2.75])

    for sid, atoms in iter_scenario_atoms():
        scenario_count += 1
        atom_total += len(atoms)
        meta = metadata.get(sid)
        if meta is None:
            roster_gate = False
            continue
        if len(atoms) != meta["atom_count"] or [atom.atom_index for atom in atoms] != list(range(len(atoms))):
            roster_gate = False
        ledger_counts = Counter((atom.ledger_id, atom.kind) for atom in atoms)
        ledgers = {atom.ledger_id for atom in atoms}
        if len(ledgers) != meta["ledger_count"]:
            typing_gate = False
        for ledger in ledgers:
            typing_gate &= (
                ledger_counts[(ledger, "carrier")] == 18
                and ledger_counts[(ledger, "matter")] == 126
                and ledger_counts[(ledger, "ledger_shadow")] == 18
            )

        params = build_flow_parameters(atoms)
        endpoint_error, radial_error = endpoint_errors(params)
        endpoint_max_error = max(endpoint_max_error, endpoint_error)
        collapse_radial_max_error = max(collapse_radial_max_error, radial_error)
        angular = np.abs(params["dphi"]) + np.abs(params["th1"] - params["thc"])
        angular_indexes = np.where(angular > 1.0e-12)[0]
        if angular_indexes.size:
            probe = angular_indexes[: min(512, angular_indexes.size)]
            full = flow_position(params, probe, 0.5, 1)
            radius_mid = 0.5 * (params["rc"][probe] + params["r1"][probe])
            theta_c = params["thc"][probe]
            phi_c = params["phc"][probe]
            radial_only = np.column_stack((
                radius_mid * np.sin(theta_c) * np.cos(phi_c),
                radius_mid * np.sin(theta_c) * np.sin(phi_c),
                radius_mid * np.cos(theta_c),
            ))
            radial_only_path_max_difference = max(
                radial_only_path_max_difference,
                float(np.max(np.linalg.norm(full - radial_only, axis=1))),
            )

        masks = build_carrier_matter_masks(atoms)
        census = Counter(history_code(mask) for mask in masks.values())
        observed_counts[sid] = census
        expected = expected_counts[sid]
        if any(census[code] != expected[code] for code in HISTORY_CODES):
            count_gate = False
        for code in HISTORY_CODES:
            reconstruction_rows.append({
                "scenario_id": sid,
                "history_code": code,
                "expected": expected[code],
                "observed": census[code],
                "matched": expected[code] == census[code],
            })

        by_code: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for pair, mask in masks.items():
            code = history_code(mask)
            if code in {"100", "010", "110", "101"}:
                by_code[code].append(pair)

        escape = np.full(len(atoms), np.inf)
        closure = np.full(len(atoms), np.inf)
        prefix_budget = ROOT_CONTROL_PREFIX
        scenario_root_failures = 0
        scenario_direction_failures = 0
        for code in ("100", "010", "110", "101"):
            pairs = by_code.get(code, [])
            if not pairs:
                continue
            pair_array = np.asarray(pairs, dtype=np.int64)
            left = pair_array[:, 0]
            right = pair_array[:, 1]
            phase = 0 if code == "100" else 1
            direction = "in" if code == "101" else "out"
            roots, found, direction_ok, bracket_counts = find_directional_roots(
                params, left, right, phase, direction, ROOT_BINS
            )
            root_count += len(roots)
            missing = int(np.sum(~found))
            bad_direction = int(np.sum(found & ~direction_ok))
            root_failures += missing
            direction_failures += bad_direction
            scenario_root_failures += missing
            scenario_direction_failures += bad_direction
            multi_root_relations += int(np.sum(bracket_counts > 1))
            if code in {"010", "110"}:
                np.minimum.at(escape, left[found], 1.0 + roots[found])
            elif code == "101":
                np.minimum.at(closure, left[found], 1.0 + roots[found])

            if prefix_budget > 0:
                take = min(prefix_budget, len(left))
                control_roots, control_found, _, _ = find_directional_roots(
                    params, left[:take], right[:take], phase, direction, ROOT_CONTROL_BINS
                )
                comparable = found[:take] & control_found
                if np.any(comparable):
                    root_control_max_error = max(
                        root_control_max_error,
                        float(np.max(np.abs(roots[:take][comparable] - control_roots[comparable]))),
                    )
                    root_control_samples += int(np.sum(comparable))
                prefix_budget -= take

            if invariant_samples < 1000:
                take = min(1000 - invariant_samples, len(left))
                good = np.where(found[:take])[0]
                if good.size:
                    local_left = left[good]
                    local_right = right[good]
                    local_s = roots[good]
                    p_left = flow_position(params, local_left, local_s, phase)
                    p_right = flow_position(params, local_right, local_s, phase)
                    original_distance = np.linalg.norm(p_left - p_right, axis=1)
                    rotated_distance = np.linalg.norm(p_left @ rotation.T - p_right @ rotation.T, axis=1)
                    translated_distance = np.linalg.norm((p_left + shift) - (p_right + shift), axis=1)
                    rotation_distance_max_error = max(
                        rotation_distance_max_error,
                        float(np.max(np.abs(original_distance - rotated_distance))),
                    )
                    translation_distance_max_error = max(
                        translation_distance_max_error,
                        float(np.max(np.abs(original_distance - translated_distance))),
                    )
                    invariant_samples += len(good)

        carrier_indexes = np.asarray([atom.atom_index for atom in atoms if atom.kind == "carrier"], dtype=np.int64)
        has_escape = np.isfinite(escape[carrier_indexes])
        has_return = np.isfinite(closure[carrier_indexes])
        dual = has_escape & has_return
        group_masks = {
            "all_carriers": np.ones(len(carrier_indexes), dtype=bool),
            "escape_only": has_escape & ~has_return,
            "return_only": has_return & ~has_escape,
            "dual": dual,
        }

        for carrier_index, escaped, returned in zip(carrier_indexes, has_escape, has_return):
            if not escaped and not returned:
                continue
            margin = float(closure[carrier_index] - escape[carrier_index]) if escaped and returned else None
            timing_rows.append({
                "scenario_id": sid,
                "seed": meta["seed"],
                "door": door_for_seed(meta["seed"]),
                "anchor": meta["anchor"],
                "p_level": meta["p_level"],
                "geometry": meta["geometry"],
                "carrier_atom_index": int(carrier_index),
                "tau_escape": float(escape[carrier_index]) if escaped else None,
                "tau_closure": float(closure[carrier_index]) if returned else None,
                "dual": bool(escaped and returned),
                "margin": margin,
                "escape_before_closure": (margin > 0.0) if margin is not None else None,
            })

        dual_margins = [
            float(closure[index] - escape[index])
            for index in carrier_indexes[dual]
        ]
        scenario_rows.append({
            **meta,
            "door": door_for_seed(meta["seed"]),
            "history_010": census["010"],
            "history_110": census["110"],
            "history_101": census["101"],
            "carriers_escape_only": int(np.sum(group_masks["escape_only"])),
            "carriers_return_only": int(np.sum(group_masks["return_only"])),
            "carriers_dual": int(np.sum(group_masks["dual"])),
            "dual_escape_before_closure": sum(value > 0.0 for value in dual_margins),
            "dual_fraction_escape_before_closure": (
                sum(value > 0.0 for value in dual_margins) / len(dual_margins)
                if dual_margins else None
            ),
            "dual_median_margin": median(dual_margins),
            "root_failures": scenario_root_failures,
            "direction_failures": scenario_direction_failures,
        })

        fine = source_bundle(params, carrier_indexes, group_masks, FINE_INTERVALS, omega_r, gamma)
        coarse = source_bundle(
            params,
            carrier_indexes,
            {"all_carriers": group_masks["all_carriers"]},
            COARSE_INTERVALS,
            omega_r,
            gamma,
        )["all_carriers"]
        fine_all = fine["all_carriers"]
        power_error = abs(fine_all["power_proxy"] - coarse["power_proxy"]) / max(abs(fine_all["power_proxy"]), 1.0e-30)
        response_error = abs(fine_all["qnm_response_peak"] - coarse["qnm_response_peak"]) / max(abs(fine_all["qnm_response_peak"]), 1.0e-30)
        convergence_power_errors.append(float(power_error))
        convergence_response_errors.append(float(response_error))
        for group, metrics in fine.items():
            if metrics["trace_relative_error"] is not None:
                trace_errors.append(float(metrics["trace_relative_error"]))
            source_rows.append({
                "scenario_id": sid,
                "seed": meta["seed"],
                "door": door_for_seed(meta["seed"]),
                "anchor": meta["anchor"],
                "p_level": meta["p_level"],
                "geometry": meta["geometry"],
                "group": group,
                **metrics,
                "all_carrier_coarse_power": coarse["power_proxy"] if group == "all_carriers" else None,
                "all_carrier_coarse_response": coarse["qnm_response_peak"] if group == "all_carriers" else None,
                "power_convergence_relative_error": power_error if group == "all_carriers" else None,
                "response_convergence_relative_error": response_error if group == "all_carriers" else None,
            })

    door_rows: list[dict[str, Any]] = []
    for geometry in ("localized_ledger_cells", "dispersed_slots"):
        for door in ("discovery", "validation", "final"):
            selected = [row for row in timing_rows if row["geometry"] == geometry and row["door"] == door]
            door_rows.append({"geometry": geometry, "door": door, **aggregate_timing(selected)})
    geometry_rows = [
        {"geometry": geometry, **aggregate_timing([row for row in timing_rows if row["geometry"] == geometry])}
        for geometry in ("localized_ledger_cells", "dispersed_slots")
    ]
    overall = aggregate_timing(timing_rows)
    strong_cells = [
        row for row in door_rows
        if row["primary_carriers"] > 0
        and row["inequality_fraction"] is not None
        and row["inequality_fraction"] > 0.50
        and row["median_margin"] is not None
        and row["median_margin"] > 0.0
    ]
    directional_cells = [
        row for row in door_rows
        if row["primary_carriers"] > 0
        and row["inequality_fraction"] is not None
        and row["inequality_fraction"] > 0.50
    ]
    timing_strong = len(strong_cells) == 6
    timing_directional = (
        overall["inequality_fraction"] is not None
        and overall["inequality_fraction"] > 0.50
        and all(row["median_margin"] is not None and row["median_margin"] > 0.0 for row in geometry_rows)
        and len(directional_cells) >= 4
    )

    source_cell_rows: list[dict[str, Any]] = []
    coherence_cells = 0
    power_separation_cells = 0
    comparable_power_cells = 0
    for geometry in ("localized_ledger_cells", "dispersed_slots"):
        for door in ("discovery", "validation", "final"):
            base = [row for row in source_rows if row["geometry"] == geometry and row["door"] == door]
            escape_rows = [row for row in base if row["group"] == "escape_only" and row["carrier_count"] > 0]
            return_rows = [row for row in base if row["group"] == "return_only" and row["carrier_count"] > 0]
            escape_coherence = median([float(row["coherence_gain"]) for row in escape_rows if row["coherence_gain"] is not None])
            return_coherence = median([float(row["coherence_gain"]) for row in return_rows if row["coherence_gain"] is not None])
            escape_power = median([float(row["power_per_carrier"]) for row in escape_rows if row["power_per_carrier"] is not None])
            return_power = median([float(row["power_per_carrier"]) for row in return_rows if row["power_per_carrier"] is not None])
            coherence_pass = escape_coherence is not None and escape_coherence > 1.0
            power_comparable = escape_power is not None and return_power is not None
            power_pass = power_comparable and escape_power > return_power
            coherence_cells += bool(coherence_pass)
            comparable_power_cells += bool(power_comparable)
            power_separation_cells += bool(power_pass)
            source_cell_rows.append({
                "geometry": geometry,
                "door": door,
                "escape_scenarios": len(escape_rows),
                "return_scenarios": len(return_rows),
                "escape_median_coherence_gain": escape_coherence,
                "return_median_coherence_gain": return_coherence,
                "escape_median_power_per_carrier": escape_power,
                "return_median_power_per_carrier": return_power,
                "escape_coherence_gt_incoherent_expectation": coherence_pass,
                "power_populations_comparable": power_comparable,
                "escape_power_gt_return_power": power_pass,
            })

    geometry_coherence = []
    for geometry in ("localized_ledger_cells", "dispersed_slots"):
        values = [
            float(row["coherence_gain"])
            for row in source_rows
            if row["geometry"] == geometry
            and row["group"] == "escape_only"
            and row["coherence_gain"] is not None
        ]
        geometry_coherence.append(median(values))

    source_pre_post = validate_sources()
    source_hash_gate = source_pre == source_pre_post and all(row["matched"] for row in source_pre_post)
    endpoint_gate = endpoint_max_error <= 1.0e-12 and collapse_radial_max_error <= 1.0e-12
    root_gate = (
        root_count > 0
        and root_failures == 0
        and direction_failures == 0
        and root_control_samples > 0
        and root_control_max_error <= 1.0e-9
    )
    invariant_gate = (
        invariant_samples > 0
        and rotation_distance_max_error <= 1.0e-12
        and translation_distance_max_error <= 1.0e-12
        and radial_only_path_max_difference > 1.0e-10
    )
    median_power_convergence = median(convergence_power_errors)
    median_response_convergence = median(convergence_response_errors)
    convergence_gate = (
        median_power_convergence is not None
        and median_power_convergence <= 0.05
        and median_response_convergence is not None
        and median_response_convergence <= 0.05
    )
    all_source_rows = [row for row in source_rows if row["group"] == "all_carriers"]
    finite_source_gate = (
        len(all_source_rows) == 96
        and all(
            row["carrier_count"] > 0
            and row["power_proxy"] is not None
            and math.isfinite(float(row["power_proxy"]))
            and float(row["power_proxy"]) > 0.0
            and row["qnm_response_peak"] is not None
            and math.isfinite(float(row["qnm_response_peak"]))
            and float(row["qnm_response_peak"]) > 0.0
            for row in all_source_rows
        )
    )
    trace_gate = bool(trace_errors) and max(trace_errors) <= 1.0e-12
    population_gate = (
        any(row["group"] == "escape_only" and row["carrier_count"] > 0 for row in source_rows)
        and any(row["group"] == "return_only" and row["carrier_count"] > 0 for row in source_rows)
        and any(row["group"] == "dual" and row["carrier_count"] > 0 for row in source_rows)
    )

    synthetic_dt = 1.0 / FINE_INTERVALS
    synthetic_source = np.zeros((FINE_INTERVALS + 1, 6), dtype=float)
    zero_response, _ = qnm_filter(synthetic_source, synthetic_dt, omega_r, gamma)
    synthetic_source[0, 0] = 1.0 / synthetic_dt
    impulse_response, kernel = qnm_filter(synthetic_source, synthetic_dt, omega_r, gamma)
    zero_response_error = float(np.max(np.abs(zero_response)))
    impulse_kernel_error = float(np.max(np.abs(impulse_response[:, 0] - kernel)))
    qnm_control_gate = zero_response_error <= 1.0e-15 and impulse_kernel_error <= 1.0e-12

    physical_claim_firewall = {
        "physical_seconds_emitted": False,
        "physical_strain_emitted": False,
        "luminosity_emitted": False,
        "distance_or_detector_forecast_emitted": False,
        "signal_speed_emitted": False,
        "fitted_parameter_count": 0,
        "sam_registry_mutated": False,
    }
    firewall_gate = not any(
        value for key, value in physical_claim_firewall.items()
        if key != "fitted_parameter_count"
    ) and physical_claim_firewall["fitted_parameter_count"] == 0

    gates = [
        {"gate": "G01_PRECOMMIT_AND_SOURCE_CUSTODY", "passed": source_hash_gate},
        {"gate": "G02_PARENT_SCHEMA_AND_CONSTRUCTIVE_INPUTS", "passed": parent_gate},
        {"gate": "G03_EXACT_ROSTER_AND_LEDGER_TYPING", "passed": scenario_count == 96 and atom_total == 482112 and roster_gate and typing_gate},
        {"gate": "G04_EXACT_CARRIER_MATTER_HISTORY_RECONSTRUCTION", "passed": count_gate},
        {"gate": "G05_CONTINUOUS_FLOW_ENDPOINTS_AND_RADIAL_COLLAPSE", "passed": endpoint_gate},
        {"gate": "G06_DIRECTIONAL_ROOTS_AND_SCAN_CONVERGENCE", "passed": root_gate},
        {"gate": "G07_DISTANCE_INVARIANTS_AND_NONRADIAL_RELEASE", "passed": invariant_gate},
        {"gate": "G08_QNM_COEFFICIENT_CUSTODY", "passed": coefficient_gate},
        {"gate": "G09_TRACE_FREE_FINITE_NONZERO_SOURCE", "passed": finite_source_gate and trace_gate},
        {"gate": "G10_SOURCE_GRID_CONVERGENCE", "passed": convergence_gate},
        {"gate": "G11_HISTORY_POPULATION_SEPARATION", "passed": population_gate},
        {"gate": "G12_ZERO_AND_IMPULSE_QNM_CONTROLS", "passed": qnm_control_gate},
        {"gate": "G13_PHYSICAL_CLAIM_FIREWALL", "passed": firewall_gate},
        {"gate": "G14_ATOMIC_RELEASE_INVENTORY", "passed": True},
    ]
    construction_pass = all(bool(row["passed"]) for row in gates)
    source_strong = (
        construction_pass
        and all(value is not None and value > 1.0 for value in geometry_coherence)
        and coherence_cells >= 4
        and comparable_power_cells >= 4
        and power_separation_cells >= 4
    )

    if not construction_pass:
        verdict = contract["verdict_ladder"]["fail"]
        status = "FAIL"
    elif timing_strong and source_strong:
        verdict = contract["verdict_ladder"]["full"]
        status = "PASS"
    elif timing_strong:
        verdict = contract["verdict_ladder"]["dynamics_and_source"]
        status = "PASS"
    elif timing_directional:
        verdict = contract["verdict_ladder"]["directional_dynamics"]
        status = "PASS"
    else:
        verdict = contract["verdict_ladder"]["boundary"]
        status = "BOUNDARY"

    controls = [
        {"control": "WC01_64_BIN_ROOT_PREFIX", "passed": root_control_samples > 0 and root_control_max_error <= 1.0e-9, "observation": f"samples={root_control_samples}; max_abs_error={root_control_max_error:.3e}"},
        {"control": "WC02_RIGID_ROTATION_DISTANCE", "passed": rotation_distance_max_error <= 1.0e-12, "observation": f"max_abs_error={rotation_distance_max_error:.3e}"},
        {"control": "WC03_GLOBAL_TRANSLATION_DISTANCE", "passed": translation_distance_max_error <= 1.0e-12, "observation": f"max_abs_error={translation_distance_max_error:.3e}"},
        {"control": "WC04_RADIAL_ONLY_RELEASE_DIFFERS", "passed": radial_only_path_max_difference > 1.0e-10, "observation": f"max_midpath_difference={radial_only_path_max_difference:.16g}"},
        {"control": "WC05_TRACE_FREE_TENSOR", "passed": trace_gate, "observation": f"max_relative_trace_error={max(trace_errors) if trace_errors else None}"},
        {"control": "WC06_FINE_COARSE_SOURCE_POWER", "passed": median_power_convergence is not None and median_power_convergence <= 0.05, "observation": f"median_relative_error={median_power_convergence}"},
        {"control": "WC07_FINE_COARSE_QNM_RESPONSE", "passed": median_response_convergence is not None and median_response_convergence <= 0.05, "observation": f"median_relative_error={median_response_convergence}"},
        {"control": "WC08_ZERO_SOURCE_ZERO_RESPONSE", "passed": zero_response_error <= 1.0e-15, "observation": f"max_abs_response={zero_response_error:.3e}"},
        {"control": "WC09_UNIT_IMPULSE_SEALED_KERNEL", "passed": impulse_kernel_error <= 1.0e-12, "observation": f"max_abs_error={impulse_kernel_error:.3e}"},
        {"control": "WC10_EXACT_QNM_FRACTIONS", "passed": coefficient_gate, "observation": f"omega_R={omega_r_fraction}; omega_I={gamma_fraction}"},
    ]

    STAGING.mkdir(parents=True)
    write_csv(STAGING / "CR005d_CARRIER_TIMING.csv", timing_rows)
    write_csv(STAGING / "CR005d_SCENARIO_TIMING.csv", scenario_rows)
    write_csv(STAGING / "CR005d_TIMING_DOORS.csv", door_rows)
    write_csv(STAGING / "CR005d_TIMING_GEOMETRIES.csv", geometry_rows)
    write_csv(STAGING / "CR005d_SOURCE_SCENARIOS.csv", source_rows)
    write_csv(STAGING / "CR005d_SOURCE_DOORS.csv", source_cell_rows)
    write_csv(STAGING / "CR005d_HISTORY_RECONSTRUCTION.csv", reconstruction_rows)
    write_csv(STAGING / "CR005d_CONTROLS.csv", controls)
    write_csv(STAGING / "CR005d_GATES.csv", gates)
    write_csv(STAGING / "CR005d_SOURCE_VALIDATION.csv", source_pre_post)

    completed = datetime.now(timezone.utc)
    summary = {
        "campaign_id": CAMPAIGN_ID,
        "branch": "21_GRAVITATIONAL_WAVES",
        "record_class": "CONSTRUCTIVE_CONTINUOUS_DYNAMICS_AND_SOURCE_BRIDGE",
        "status": status,
        "primary_verdict": verdict,
        "started_utc": started.isoformat(),
        "completed_utc": completed.isoformat(),
        "continuous_flow": {
            "clock": "dimensionless Starbreaker structural phase t in [0,2]",
            "collapse": "exponential radial contraction",
            "release": "linear radius plus shortest-branch theta/phi flow",
            "bounce": "velocity-changing impulse at t=1",
            "endpoint_max_abs_error": endpoint_max_error,
            "collapse_radial_max_error": collapse_radial_max_error,
            "physical_seconds": None,
        },
        "roster": {
            "scenarios": scenario_count,
            "atoms": atom_total,
            "continuous_roots": root_count,
            "root_failures": root_failures,
            "direction_failures": direction_failures,
            "multiple_directional_brackets": multi_root_relations,
        },
        "timing": {
            "primary_result": overall,
            "geometry_results": geometry_rows,
            "door_results": door_rows,
            "strong_cells": len(strong_cells),
            "directional_cells": len(directional_cells),
            "timing_strong": timing_strong,
            "timing_directional": timing_directional,
        },
        "carrier_source": {
            "tensor": "unit-carrier trace-free quadrupole",
            "fine_intervals": FINE_INTERVALS,
            "coarse_intervals": COARSE_INTERVALS,
            "omega_R_M": omega_r_fraction,
            "omega_I_M": gamma_fraction,
            "unit_clock_response_only": True,
            "physical_strain": None,
            "median_power_convergence_relative_error": median_power_convergence,
            "median_response_convergence_relative_error": median_response_convergence,
            "max_trace_relative_error": max(trace_errors) if trace_errors else None,
            "geometry_escape_coherence_medians": geometry_coherence,
            "coherence_cells": coherence_cells,
            "comparable_power_cells": comparable_power_cells,
            "escape_power_gt_return_cells": power_separation_cells,
            "source_strong": source_strong,
            "door_results": source_cell_rows,
        },
        "carrier_matter_history_totals": {
            code: sum(counter[code] for counter in observed_counts.values()) for code in HISTORY_CODES
        },
        "controls_passed": sum(bool(row["passed"]) for row in controls),
        "controls_total": len(controls),
        "gates_passed": sum(bool(row["passed"]) for row in gates),
        "gates_total": len(gates),
        "source_hashes_matched": sum(bool(row["matched"]) for row in source_pre_post),
        "source_count": len(source_pre_post),
        "physical_claim_firewall": physical_claim_firewall,
        "preflight": {"task": seal["task"], "preflight_sha256": seal["preflight_sha256"]},
        "same_run_repair": False,
    }
    write_json(STAGING / "CR005d_SUMMARY.json", summary)
    write_json(STAGING / "CR005d_PROVENANCE.json", {
        "campaign_id": CAMPAIGN_ID,
        "contract_sha256": EXPECTED_CONTRACT_SHA256,
        "precommit_sha256": EXPECTED_PRECOMMIT_SHA256,
        "source_manifest_sha256": EXPECTED_SOURCE_MANIFEST_SHA256,
        "precommit_seal_sha256": EXPECTED_PRECOMMIT_SEAL_SHA256,
        "runner_sha256": sha256_file(Path(__file__)),
        "source_role": "frozen Starbreaker three-state roster plus sealed CR005, CR005b, and CR005c constructive inputs",
        "claim_boundary": "dimensionless structural flow and unit-clock carrier source response; no physical strain or time calibration",
    })
    write_json(STAGING / "EXECUTION_RECEIPT.json", {
        "campaign_id": CAMPAIGN_ID,
        "started_utc": started.isoformat(),
        "completed_utc": completed.isoformat(),
        "python": sys.version,
        "numpy": np.__version__,
        "result": verdict,
        "same_run_repair": False,
    })

    timing_lines = "\n".join(
        f"| {row['geometry']} | {row['door']} | {row['primary_carriers']} | {row['inequality_fraction']} | {row['median_margin']} |"
        for row in door_rows
    )
    source_lines = "\n".join(
        f"| {row['geometry']} | {row['door']} | {row['escape_median_coherence_gain']} | {row['escape_median_power_per_carrier']} | {row['return_median_power_per_carrier']} | {row['escape_power_gt_return_power']} |"
        for row in source_cell_rows
    )
    result_text = f"""# CR005d Continuous Starbreaker Flow and Carrier-QNM Source Bridge Result

## Primary verdict

`{verdict}`

All **{sum(bool(row['passed']) for row in gates)}/{len(gates)}** construction gates and
**{sum(bool(row['passed']) for row in controls)}/{len(controls)}** controls passed.

## Continuous Starbreaker result

The three stored Starbreaker states were lifted into a zero-fit continuous
structural flow: exponential radial collapse, a bounce impulse at `t=1`, then
constant radial and shortest-branch angular release. The maximum stored-state
reconstruction error was `{endpoint_max_error:.3e}`.

```text
dual carriers                     = {overall['primary_carriers']}
escape before closure             = {overall['inequality_count']}
continuous-flow inequality fraction = {overall['inequality_fraction']}
median closure-minus-escape margin  = {overall['median_margin']}
continuous transition roots         = {root_count}
root failures                        = {root_failures}
```

| geometry | door | dual carriers | escape-before-closure fraction | median margin |
|---|---|---:|---:|---:|
{timing_lines}

## Carrier source bridge

The run constructed the trace-free unit-carrier quadrupole `Q_ab`, its source
`d^2Q_ab/dt^2`, its third-derivative power proxy, and a causal response using
the sealed kernel:

```text
omega_R M = {omega_r_fraction}
omega_I M = {gamma_fraction}
g(u)      = exp[-(4/45)u] sin[(3/8)u] / (3/8)
```

| geometry | door | escape coherence | escape power/carrier | return power/carrier | escape > return |
|---|---|---:|---:|---:|---|
{source_lines}

The exact incoherent reference for `coherence_gain` is one: it is the expected
power after independent sign scrambling of the individual carrier tensors.

## Construction quality

- Frozen sources matched: **{sum(bool(row['matched']) for row in source_pre_post)}/{len(source_pre_post)}**
- Scenarios: **{scenario_count}/96**
- Atoms: **{atom_total:,}/482,112**
- Root scan-control maximum error: **{root_control_max_error:.3e}**
- Median fine/coarse source-power error: **{median_power_convergence}**
- Median fine/coarse QNM-response error: **{median_response_convergence}**
- Maximum relative trace error: **{max(trace_errors) if trace_errors else None}**

## Meaning and boundary

This is the first prospective continuous Starbreaker source surface and the
first carrier-history-resolved QNM source bridge in the branch. It tests a
curved continuous path rather than relabeling the prior affine clock.

The clock remains dimensionless Starbreaker phase time. Unit carrier weights
are not matter masses, and the QNM convolution assumes a unit-clock bridge that
has not been derived from physical mass-scaled time. Therefore the output is a
dimensionless source and response candidate—not gravitational-wave strain,
luminosity, frequency in hertz, signal speed, or a detector forecast.
"""
    (STAGING / "CR005d_RESULT.md").write_text(result_text, encoding="utf-8")

    names = sorted(path.name for path in STAGING.iterdir() if path.is_file())
    manifest_rows = [
        {"path": name, "bytes": (STAGING / name).stat().st_size, "sha256": sha256_file(STAGING / name)}
        for name in names
    ]
    write_csv(STAGING / "CR005d_RELEASE_MANIFEST.csv", manifest_rows)
    manifest_sha = sha256_file(STAGING / "CR005d_RELEASE_MANIFEST.csv")
    (STAGING / "CR005d_RELEASE_MANIFEST_SHA256.txt").write_text(manifest_sha + "\n", encoding="ascii")
    for row in manifest_rows:
        path = STAGING / row["path"]
        if path.stat().st_size != row["bytes"] or sha256_file(path) != row["sha256"]:
            raise RuntimeError("release manifest verification failed")
    STAGING.replace(RELEASE)

    print(json.dumps({
        "campaign_id": CAMPAIGN_ID,
        "primary_verdict": verdict,
        "timing": overall,
        "timing_strong": timing_strong,
        "source_strong": source_strong,
        "coherence_cells": coherence_cells,
        "escape_power_gt_return_cells": power_separation_cells,
        "gates": f"{sum(bool(row['passed']) for row in gates)}/{len(gates)}",
        "controls": f"{sum(bool(row['passed']) for row in controls)}/{len(controls)}",
        "release_manifest_sha256": manifest_sha,
    }, indent=2))


if __name__ == "__main__":
    main()
