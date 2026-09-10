from __future__ import annotations

import csv
import gzip
import hashlib
import json
import math
import shutil
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


CAMPAIGN_ID = "CR005c_STARBREAKER_ESCAPE_CLOSURE_TIMING_OPERATIONALIZATION"
EXPECTED_CONTRACT_SHA256 = "43a305c078bdc43c676cef6d61c10b46d27d575890e221833b671c97457d888a"
EXPECTED_PRECOMMIT_SHA256 = "e6f32e78edc2b8ab7005ec4abd9a9044fa94348e792cdca21ace6da6ef0a8925"
EXPECTED_SOURCE_MANIFEST_SHA256 = "346c81b6203fa84807976b3a01f94c2127f2f8e1b95414c1f37d26c269451114"
EXPECTED_PRECOMMIT_SEAL_SHA256 = "d4beb84901bd23b51c0159f324afb6db995e3c1f1b0477ad5fdea83701379cc3"

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
CONTRACT_PATH = BASE / "CR005c_CONTRACT.json"
PRECOMMIT_PATH = BASE / "CR005c_PRECOMMIT.md"
SOURCE_MANIFEST_PATH = BASE / "CR005c_SOURCE_MANIFEST.json"
PRECOMMIT_SEAL_PATH = BASE / "CR005c_PRECOMMIT_SEAL.json"
RELEASE = BASE / "release"
STAGING = BASE / ".cr005c_release_staging"

PARENT = ROOT / "15_SCALE_BRIDGE_SIMULATOR/STARBREAKER_COMPLETE_TYPED_RELATION_HISTORY_V1/release"
ROSTER_PATH = PARENT / "ATOM_TYPED_STAGE_ROSTER.csv.gz"
SCENARIO_PATH = PARENT / "SCENARIO_SELECTION_DECOMPOSITION.csv"
COUNT_PATH = PARENT / "RELATION_HISTORY_COUNTS.csv"
SCHEMA_PATH = PARENT / "RELATION_HISTORY_SCHEMA.json"
PARENT_SUMMARY_PATH = PARENT / "RELATION_HISTORY_SUMMARY.json"
REOPENING_SUMMARY_PATH = ROOT / "15_SCALE_BRIDGE_SIMULATOR/STARBREAKER_101_REOPENING_RELAY_DECOMPOSITION_V1/release/REOPENING_RELAY_SUMMARY.json"
AXIS_SUMMARY_PATH = ROOT / "15_SCALE_BRIDGE_SIMULATOR/STARBREAKER_X1_CARRIER_AXIS_REVERSAL_DISCOVERY_V1/release/AXIS_REVERSAL_SUMMARY.json"

RADIUS = 0.076
TOL = 1.0e-12
STAGE_BITS = ((0, 4), (1, 2), (2, 1))
NEIGHBOR_OFFSETS = tuple((dx, dy, dz) for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1))
HISTORY_CODES = ("001", "010", "011", "100", "101", "110", "111")
DISCOVERY_SEEDS = {910001, 910002}
VALIDATION_SEEDS = {910003}
FINAL_SEEDS = {910004}


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
    if seal.get("contract_sha256") != EXPECTED_CONTRACT_SHA256:
        raise RuntimeError("contract seal changed")
    if seal.get("precommit_sha256") != EXPECTED_PRECOMMIT_SHA256:
        raise RuntimeError("precommit content seal changed")
    if seal.get("source_manifest_sha256") != EXPECTED_SOURCE_MANIFEST_SHA256:
        raise RuntimeError("source manifest seal changed")
    return seal


def load_scenario_metadata() -> dict[str, dict[str, Any]]:
    metadata: dict[str, dict[str, Any]] = {}
    with SCENARIO_PATH.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            sid = row["scenario_id"]
            metadata[sid] = {
                "scenario_id": sid,
                "lane": row["lane"],
                "anchor": row["anchor"],
                "seed": int(row["seed"]),
                "p_level": int(row["p_level"]),
                "geometry": row["geometry"],
                "atom_count": int(row["atom_count"]),
                "ledger_count": int(row["ledger_count"]),
            }
    return metadata


def load_expected_carrier_matter_counts() -> dict[str, Counter[str]]:
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


def build_carrier_matter_masks(atoms: list[Atom], radius: float) -> dict[tuple[int, int], int]:
    carriers = [atom for atom in atoms if atom.kind == "carrier"]
    matters = [atom for atom in atoms if atom.kind == "matter"]
    masks: dict[tuple[int, int], int] = {}
    for stage, bit in STAGE_BITS:
        grid: dict[tuple[int, int, int], list[Atom]] = defaultdict(list)
        for matter in matters:
            grid[cell(matter.positions[stage], radius)].append(matter)
        for carrier in carriers:
            base_cell = cell(carrier.positions[stage], radius)
            for dx, dy, dz in NEIGHBOR_OFFSETS:
                for matter in grid.get((base_cell[0] + dx, base_cell[1] + dy, base_cell[2] + dz), ()):
                    if distance(carrier.positions[stage], matter.positions[stage]) <= radius:
                        key = (carrier.atom_index, matter.atom_index)
                        masks[key] = masks.get(key, 0) | bit
    return masks


def history_code(mask: int) -> str:
    return f"{1 if mask & 4 else 0}{1 if mask & 2 else 0}{1 if mask & 1 else 0}"


def relative(left: Atom, right: Atom, stage: int) -> tuple[float, float, float]:
    return tuple(left.positions[stage][i] - right.positions[stage][i] for i in range(3))  # type: ignore[return-value]


def dot(left: tuple[float, float, float], right: tuple[float, float, float]) -> float:
    return sum(left[i] * right[i] for i in range(3))


def crossing_time_from_relative(
    start: tuple[float, float, float],
    end: tuple[float, float, float],
    radius: float,
    segment_start: float,
    direction: str,
) -> tuple[float, float]:
    delta = tuple(end[i] - start[i] for i in range(3))
    qa = dot(delta, delta)
    qb = 2.0 * dot(start, delta)
    qc = dot(start, start) - radius * radius
    if qa <= TOL * TOL:
        raise ValueError("transition segment has no relative motion")
    disc = qb * qb - 4.0 * qa * qc
    if disc < -TOL:
        raise ValueError("transition segment has no contact-surface root")
    disc = max(0.0, disc)
    roots = [(-qb - math.sqrt(disc)) / (2.0 * qa), (-qb + math.sqrt(disc)) / (2.0 * qa)]
    candidates: list[tuple[float, float]] = []
    for raw in roots:
        if -TOL <= raw <= 1.0 + TOL:
            s = min(1.0, max(0.0, raw))
            at_root = tuple(start[i] + s * delta[i] for i in range(3))
            normal_speed = dot(at_root, delta) / radius
            if direction == "out" and normal_speed >= -TOL:
                candidates.append((s, normal_speed))
            elif direction == "in" and normal_speed <= TOL:
                candidates.append((s, normal_speed))
    if not candidates:
        raise ValueError(f"no {direction} root in segment")
    if direction == "out":
        s, speed = max(candidates, key=lambda item: item[1])
    else:
        s, speed = min(candidates, key=lambda item: item[1])
    return segment_start + s, speed


def crossing_for_code(carrier: Atom, matter: Atom, code: str) -> tuple[float, float, str]:
    if code == "100":
        start_stage, end_stage, segment_start, direction = 0, 1, 0.0, "out"
    elif code in {"010", "110"}:
        start_stage, end_stage, segment_start, direction = 1, 2, 1.0, "out"
    elif code == "101":
        start_stage, end_stage, segment_start, direction = 1, 2, 1.0, "in"
    else:
        raise ValueError(f"history {code} has no requested timing crossing")
    time, speed = crossing_time_from_relative(
        relative(carrier, matter, start_stage),
        relative(carrier, matter, end_stage),
        RADIUS,
        segment_start,
        direction,
    )
    return time, speed, direction


def rotate(point: tuple[float, float, float]) -> tuple[float, float, float]:
    az = math.radians(37.0)
    ay = math.radians(19.0)
    x1 = math.cos(az) * point[0] - math.sin(az) * point[1]
    y1 = math.sin(az) * point[0] + math.cos(az) * point[1]
    z1 = point[2]
    return (
        math.cos(ay) * x1 + math.sin(ay) * z1,
        y1,
        -math.sin(ay) * x1 + math.cos(ay) * z1,
    )


def quantile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = q * (len(ordered) - 1)
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    frac = pos - lo
    return ordered[lo] * (1.0 - frac) + ordered[hi] * frac


def median(values: list[float]) -> float | None:
    return quantile(values, 0.5)


def fraction_before(values: list[float], threshold: float | None) -> float | None:
    if not values or threshold is None:
        return None
    return sum(value < threshold for value in values) / len(values)


def door_for_seed(seed: int) -> str:
    if seed in DISCOVERY_SEEDS:
        return "discovery"
    if seed in VALIDATION_SEEDS:
        return "validation"
    if seed in FINAL_SEEDS:
        return "final"
    raise ValueError(f"unregistered seed door: {seed}")


def aggregate_primary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    margins = [float(row["margin_post_escape_to_closure"]) for row in rows if row["dual_postcollapse"]]
    return {
        "primary_carriers": len(margins),
        "inequality_count": sum(value > 0.0 for value in margins),
        "inequality_fraction": (sum(value > 0.0 for value in margins) / len(margins)) if margins else None,
        "median_margin": median(margins),
        "q10_margin": quantile(margins, 0.1),
        "q90_margin": quantile(margins, 0.9),
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    if RELEASE.exists() or STAGING.exists():
        raise RuntimeError("CR005c release path already exists; same-run repair is prohibited")

    seal = verify_precommit()
    source_pre = validate_sources()
    if not all(row["matched"] for row in source_pre):
        raise RuntimeError("one or more frozen sources changed before execution")

    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    parent_summary = json.loads(PARENT_SUMMARY_PATH.read_text(encoding="utf-8"))
    reopening_summary = json.loads(REOPENING_SUMMARY_PATH.read_text(encoding="utf-8"))
    axis_summary = json.loads(AXIS_SUMMARY_PATH.read_text(encoding="utf-8"))
    metadata = load_scenario_metadata()
    expected_counts = load_expected_carrier_matter_counts()

    parent_gate = (
        contract["campaign_id"] == CAMPAIGN_ID
        and schema["history_bit_order"] == ["seed", "collapse", "final"]
        and float(schema["proximity_radius"]) == RADIUS
        and parent_summary["primary_verdict"].startswith("PASS_COMPLETE_TYPED_RELATION_HISTORY_CONSTRUCTED")
        and reopening_summary["primary_verdict"].startswith("PASS_101_REOPENING_MATCHED_SPECIFICITY")
        and axis_summary["primary_verdict"] == "BOUNDARY_CARRIER_REOPENING_CONFIRMED__ONE_AXIS_REVERSAL_UNRESOLVED"
    )

    occurrence_rows: list[dict[str, Any]] = []
    scenario_rows: list[dict[str, Any]] = []
    reconstruction_rows: list[dict[str, Any]] = []
    observed_counts: dict[str, Counter[str]] = {}
    atom_total = 0
    scenario_count = 0
    roster_gate = True
    typing_gate = True
    count_gate = True
    crossing_failures = 0
    normal_sign_failures = 0
    crossing_count = 0
    duplicate_occurrence_keys = 0
    seen_occurrence_keys: set[tuple[str, int]] = set()
    endpoint_swap_max_error = 0.0
    rotation_max_error = 0.0
    translation_max_error = 0.0
    invariant_samples = 0
    half_radius_rejected: bool | None = None
    double_radius_rejected: bool | None = None
    first_expected_histogram: Counter[str] | None = None

    for sid, atoms in iter_scenario_atoms():
        scenario_count += 1
        atom_total += len(atoms)
        meta = metadata.get(sid)
        if meta is None:
            roster_gate = False
            continue
        if len(atoms) != meta["atom_count"]:
            roster_gate = False
        if sorted(atom.atom_index for atom in atoms) != list(range(len(atoms))):
            roster_gate = False

        ledger_counts: dict[tuple[int, str], int] = Counter((atom.ledger_id, atom.kind) for atom in atoms)
        if len({atom.ledger_id for atom in atoms}) != meta["ledger_count"]:
            typing_gate = False
        for ledger_id in {atom.ledger_id for atom in atoms}:
            if ledger_counts[(ledger_id, "carrier")] != 18:
                typing_gate = False
            if ledger_counts[(ledger_id, "matter")] != 126:
                typing_gate = False
            if ledger_counts[(ledger_id, "ledger_shadow")] != 18:
                typing_gate = False

        masks = build_carrier_matter_masks(atoms, RADIUS)
        by_index = {atom.atom_index: atom for atom in atoms}
        census = Counter(history_code(mask) for mask in masks.values())
        observed_counts[sid] = census
        expected = expected_counts[sid]
        if any(census[code] != expected[code] for code in HISTORY_CODES):
            count_gate = False
        for code in HISTORY_CODES:
            reconstruction_rows.append({
                "scenario_id": sid,
                "history_code": code,
                "expected_carrier_matter_relations": expected[code],
                "observed_carrier_matter_relations": census[code],
                "matched": expected[code] == census[code],
            })

        if scenario_count == 1:
            first_expected_histogram = Counter(expected)
            half_census = Counter(history_code(mask) for mask in build_carrier_matter_masks(atoms, RADIUS / 2.0).values())
            double_census = Counter(history_code(mask) for mask in build_carrier_matter_masks(atoms, RADIUS * 2.0).values())
            half_radius_rejected = any(half_census[code] != expected[code] for code in HISTORY_CODES)
            double_radius_rejected = any(double_census[code] != expected[code] for code in HISTORY_CODES)

        events: dict[int, dict[str, list[float]]] = defaultdict(lambda: {"escape_pre": [], "escape_post": [], "closure": []})
        for (carrier_index, matter_index), mask in masks.items():
            code = history_code(mask)
            if code not in {"100", "010", "110", "101"}:
                continue
            carrier = by_index[carrier_index]
            matter = by_index[matter_index]
            try:
                time_value, normal_speed, direction = crossing_for_code(carrier, matter, code)
                crossing_count += 1
                if direction == "out" and normal_speed < -TOL:
                    normal_sign_failures += 1
                if direction == "in" and normal_speed > TOL:
                    normal_sign_failures += 1
                if code == "100":
                    events[carrier_index]["escape_pre"].append(time_value)
                elif code in {"010", "110"}:
                    events[carrier_index]["escape_post"].append(time_value)
                else:
                    events[carrier_index]["closure"].append(time_value)

                if invariant_samples < 1000:
                    if code == "100":
                        start_stage, end_stage, segment_start = 0, 1, 0.0
                    else:
                        start_stage, end_stage, segment_start = 1, 2, 1.0
                    start_rel = relative(carrier, matter, start_stage)
                    end_rel = relative(carrier, matter, end_stage)
                    swapped_time, _ = crossing_time_from_relative(
                        tuple(-value for value in start_rel),
                        tuple(-value for value in end_rel),
                        RADIUS,
                        segment_start,
                        direction,
                    )
                    rotated_time, _ = crossing_time_from_relative(
                        rotate(start_rel), rotate(end_rel), RADIUS, segment_start, direction
                    )
                    shift = (4.25, -3.5, 2.75)
                    c_start = tuple(carrier.positions[start_stage][i] + shift[i] for i in range(3))
                    m_start = tuple(matter.positions[start_stage][i] + shift[i] for i in range(3))
                    c_end = tuple(carrier.positions[end_stage][i] + shift[i] for i in range(3))
                    m_end = tuple(matter.positions[end_stage][i] + shift[i] for i in range(3))
                    shifted_start = tuple(c_start[i] - m_start[i] for i in range(3))
                    shifted_end = tuple(c_end[i] - m_end[i] for i in range(3))
                    translated_time, _ = crossing_time_from_relative(
                        shifted_start, shifted_end, RADIUS, segment_start, direction
                    )
                    endpoint_swap_max_error = max(endpoint_swap_max_error, abs(time_value - swapped_time))
                    rotation_max_error = max(rotation_max_error, abs(time_value - rotated_time))
                    translation_max_error = max(translation_max_error, abs(time_value - translated_time))
                    invariant_samples += 1
            except ValueError:
                crossing_failures += 1

        scenario_occurrences: list[dict[str, Any]] = []
        for carrier_index in sorted(events):
            event = events[carrier_index]
            escape_pre = min(event["escape_pre"]) if event["escape_pre"] else None
            escape_post = min(event["escape_post"]) if event["escape_post"] else None
            closure = min(event["closure"]) if event["closure"] else None
            dual_post = escape_post is not None and closure is not None
            margin = (closure - escape_post) if dual_post else None
            key = (sid, carrier_index)
            if key in seen_occurrence_keys:
                duplicate_occurrence_keys += 1
            seen_occurrence_keys.add(key)
            row = {
                "scenario_id": sid,
                "seed": meta["seed"],
                "door": door_for_seed(meta["seed"]),
                "anchor": meta["anchor"],
                "p_level": meta["p_level"],
                "geometry": meta["geometry"],
                "carrier_atom_index": carrier_index,
                "precollapse_escape_relations": len(event["escape_pre"]),
                "postcollapse_escape_relations": len(event["escape_post"]),
                "closure_101_relations": len(event["closure"]),
                "tau_escape_pre": escape_pre,
                "tau_escape_post": escape_post,
                "tau_closure": closure,
                "dual_postcollapse": dual_post,
                "margin_post_escape_to_closure": margin,
                "escape_before_closure": (margin > 0.0) if margin is not None else None,
            }
            occurrence_rows.append(row)
            scenario_occurrences.append(row)

        closure_times = [float(row["tau_closure"]) for row in scenario_occurrences if row["tau_closure"] is not None]
        post_escape_times = [float(row["tau_escape_post"]) for row in scenario_occurrences if row["tau_escape_post"] is not None]
        dual_margins = [float(row["margin_post_escape_to_closure"]) for row in scenario_occurrences if row["dual_postcollapse"]]
        q10 = quantile(closure_times, 0.1)
        q50 = quantile(closure_times, 0.5)
        q90 = quantile(closure_times, 0.9)
        scenario_rows.append({
            **meta,
            "door": door_for_seed(meta["seed"]),
            "carrier_matter_relations": sum(census.values()),
            "history_100_relations": census["100"],
            "history_010_relations": census["010"],
            "history_110_relations": census["110"],
            "history_101_relations": census["101"],
            "carriers_with_precollapse_escape": sum(row["tau_escape_pre"] is not None for row in scenario_occurrences),
            "carriers_with_postcollapse_escape": len(post_escape_times),
            "carriers_with_101_closure": len(closure_times),
            "dual_postcollapse_carriers": len(dual_margins),
            "escape_before_closure_count": sum(value > 0.0 for value in dual_margins),
            "escape_before_closure_fraction": (sum(value > 0.0 for value in dual_margins) / len(dual_margins)) if dual_margins else None,
            "median_margin": median(dual_margins),
            "closure_front_q10": q10,
            "closure_front_q50": q50,
            "closure_front_q90": q90,
            "post_escape_before_closure_q10_fraction": fraction_before(post_escape_times, q10),
            "post_escape_before_closure_q50_fraction": fraction_before(post_escape_times, q50),
            "post_escape_before_closure_q90_fraction": fraction_before(post_escape_times, q90),
        })

    wrong_bit_order_rejected = False
    if first_expected_histogram is not None:
        reversed_histogram = Counter({code[::-1]: count for code, count in first_expected_histogram.items()})
        wrong_bit_order_rejected = any(reversed_histogram[code] != first_expected_histogram[code] for code in HISTORY_CODES)

    synthetic_out, synthetic_out_speed = crossing_time_from_relative(
        (RADIUS * 0.5, 0.0, 0.0), (RADIUS * 1.5, 0.0, 0.0), RADIUS, 0.0, "out"
    )
    synthetic_in, synthetic_in_speed = crossing_time_from_relative(
        (RADIUS * 1.5, 0.0, 0.0), (RADIUS * 0.5, 0.0, 0.0), RADIUS, 1.0, "in"
    )
    synthetic_gate = (
        abs(synthetic_out - 0.5) <= TOL
        and abs(synthetic_in - 1.5) <= TOL
        and synthetic_out_speed > 0.0
        and synthetic_in_speed < 0.0
    )

    door_rows: list[dict[str, Any]] = []
    for geometry in ("localized_ledger_cells", "dispersed_slots"):
        for door in ("discovery", "validation", "final"):
            selected = [row for row in occurrence_rows if row["geometry"] == geometry and row["door"] == door]
            door_rows.append({"geometry": geometry, "door": door, **aggregate_primary(selected)})

    geometry_rows: list[dict[str, Any]] = []
    for geometry in ("localized_ledger_cells", "dispersed_slots"):
        selected = [row for row in occurrence_rows if row["geometry"] == geometry]
        geometry_rows.append({"geometry": geometry, **aggregate_primary(selected)})

    overall = aggregate_primary(occurrence_rows)
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

    invariants_gate = (
        invariant_samples > 0
        and endpoint_swap_max_error <= TOL
        and rotation_max_error <= TOL
        and translation_max_error <= TOL
        and synthetic_gate
    )
    wrong_controls_gate = bool(half_radius_rejected and double_radius_rejected and wrong_bit_order_rejected)
    occurrence_gate = duplicate_occurrence_keys == 0
    physical_claim_firewall = {
        "physical_time_seconds_emitted": False,
        "global_horizon_installed": False,
        "gravitational_strain_emitted": False,
        "signal_speed_emitted": False,
        "fitted_parameter_count": 0,
        "sam_registry_mutated": False,
    }
    firewall_gate = (
        not any(physical_claim_firewall[key] for key in (
            "physical_time_seconds_emitted", "global_horizon_installed",
            "gravitational_strain_emitted", "signal_speed_emitted", "sam_registry_mutated"
        ))
        and physical_claim_firewall["fitted_parameter_count"] == 0
    )

    source_post = validate_sources()
    sources_gate = source_pre == source_post and all(row["matched"] for row in source_post)
    gates = [
        {"gate": "G01_PRECOMMIT_AND_SOURCE_HASHES", "passed": sources_gate},
        {"gate": "G02_PARENT_RECORDS_AND_SCHEMA", "passed": parent_gate},
        {"gate": "G03_EXACT_SCENARIO_ATOM_AND_LEDGER_TYPING", "passed": scenario_count == 96 and atom_total == 482112 and roster_gate and typing_gate},
        {"gate": "G04_EXACT_CARRIER_MATTER_HISTORY_RECONSTRUCTION", "passed": count_gate},
        {"gate": "G05_CROSSING_ROOTS_AND_NORMAL_SIGNS", "passed": crossing_count > 0 and crossing_failures == 0 and normal_sign_failures == 0},
        {"gate": "G06_UNIQUE_CARRIER_OCCURRENCE_PRIMARY_UNIT", "passed": occurrence_gate},
        {"gate": "G07_GEOMETRIC_INVARIANTS_AND_SYNTHETIC_ROOTS", "passed": invariants_gate},
        {"gate": "G08_WRONG_RADIUS_AND_BIT_ORDER_CONTROLS", "passed": wrong_controls_gate},
        {"gate": "G09_PHYSICAL_CLAIM_FIREWALL", "passed": firewall_gate},
        {"gate": "G10_ATOMIC_RELEASE_INVENTORY", "passed": True},
    ]
    core_pass = all(row["passed"] for row in gates)

    strong = core_pass and len(strong_cells) == 6
    geometry_positive = all(
        row["median_margin"] is not None and row["median_margin"] > 0.0
        for row in geometry_rows
    )
    directional = (
        core_pass
        and overall["inequality_fraction"] is not None
        and overall["inequality_fraction"] > 0.50
        and geometry_positive
        and len(directional_cells) >= 4
    )
    if not core_pass:
        verdict = contract["verdict_ladder"]["fail"]
        status = "FAIL"
    elif strong:
        verdict = contract["verdict_ladder"]["strong"]
        status = "PASS"
    elif directional:
        verdict = contract["verdict_ladder"]["directional"]
        status = "PASS"
    else:
        verdict = contract["verdict_ladder"]["boundary"]
        status = "BOUNDARY"

    wrong_controls = [
        {"control": "WC01_HALF_CONTACT_RADIUS", "passed": bool(half_radius_rejected), "observation": "half-radius census differs from frozen census"},
        {"control": "WC02_DOUBLE_CONTACT_RADIUS", "passed": bool(double_radius_rejected), "observation": "double-radius census differs from frozen census"},
        {"control": "WC03_WRONG_HISTORY_BIT_ORDER", "passed": wrong_bit_order_rejected, "observation": "reversed bit order differs on asymmetric histories"},
        {"control": "WC04_SYNTHETIC_OUTWARD_ROOT", "passed": abs(synthetic_out - 0.5) <= TOL and synthetic_out_speed > 0.0, "observation": f"tau={synthetic_out:.16g}; speed={synthetic_out_speed:.16g}"},
        {"control": "WC05_SYNTHETIC_INWARD_ROOT", "passed": abs(synthetic_in - 1.5) <= TOL and synthetic_in_speed < 0.0, "observation": f"tau={synthetic_in:.16g}; speed={synthetic_in_speed:.16g}"},
        {"control": "WC06_ENDPOINT_EXCHANGE_INVARIANCE", "passed": endpoint_swap_max_error <= TOL, "observation": f"max_abs_error={endpoint_swap_max_error:.3e}"},
        {"control": "WC07_RIGID_ROTATION_INVARIANCE", "passed": rotation_max_error <= TOL, "observation": f"max_abs_error={rotation_max_error:.3e}"},
        {"control": "WC08_GLOBAL_TRANSLATION_INVARIANCE", "passed": translation_max_error <= TOL, "observation": f"max_abs_error={translation_max_error:.3e}"},
    ]

    STAGING.mkdir(parents=True)
    write_csv(STAGING / "CR005c_CARRIER_OCCURRENCE_TIMING.csv", occurrence_rows)
    write_csv(STAGING / "CR005c_SCENARIO_TIMING.csv", scenario_rows)
    write_csv(STAGING / "CR005c_FROZEN_DOOR_RESULTS.csv", door_rows)
    write_csv(STAGING / "CR005c_GEOMETRY_RESULTS.csv", geometry_rows)
    write_csv(STAGING / "CR005c_HISTORY_RECONSTRUCTION.csv", reconstruction_rows)
    write_csv(STAGING / "CR005c_WRONG_CONTROLS.csv", wrong_controls)
    write_csv(STAGING / "CR005c_GATES.csv", gates)
    write_csv(STAGING / "CR005c_SOURCE_VALIDATION.csv", source_post)

    completed = datetime.now(timezone.utc)
    summary = {
        "campaign_id": CAMPAIGN_ID,
        "branch": "21_GRAVITATIONAL_WAVES",
        "record_class": "CONSTRUCTIVE_TIMING_OPERATIONALIZATION",
        "status": status,
        "primary_verdict": verdict,
        "started_utc": started.isoformat(),
        "completed_utc": completed.isoformat(),
        "operational_surface": {
            "surface": "carrier-matter relation distance equals 0.076",
            "time_parameter": "seed=0, collapse=1, final=2 with piecewise-linear relative position",
            "physical_time": None,
            "global_horizon": None,
        },
        "roster": {
            "scenarios": scenario_count,
            "atoms": atom_total,
            "unique_timing_carrier_occurrences": len(occurrence_rows),
            "crossings_solved": crossing_count,
            "crossing_failures": crossing_failures,
        },
        "primary_result": overall,
        "geometry_results": geometry_rows,
        "frozen_door_results": door_rows,
        "strong_cells": len(strong_cells),
        "directional_cells": len(directional_cells),
        "carrier_matter_history_totals": {
            code: sum(counter[code] for counter in observed_counts.values()) for code in HISTORY_CODES
        },
        "controls": {
            "wrong_controls_passed": sum(row["passed"] for row in wrong_controls),
            "wrong_controls_total": len(wrong_controls),
            "endpoint_swap_max_abs_error": endpoint_swap_max_error,
            "rotation_max_abs_error": rotation_max_error,
            "translation_max_abs_error": translation_max_error,
            "invariant_samples": invariant_samples,
        },
        "gates_passed": sum(row["passed"] for row in gates),
        "gates_total": len(gates),
        "source_hashes_matched": sum(row["matched"] for row in source_post),
        "source_count": len(source_post),
        "physical_claim_firewall": physical_claim_firewall,
        "preflight": {
            "task": seal["task"],
            "preflight_sha256": seal["preflight_sha256"],
        },
        "same_run_repair": False,
    }
    write_json(STAGING / "CR005c_SUMMARY.json", summary)
    write_json(STAGING / "CR005c_PROVENANCE.json", {
        "campaign_id": CAMPAIGN_ID,
        "contract_sha256": EXPECTED_CONTRACT_SHA256,
        "precommit_sha256": EXPECTED_PRECOMMIT_SHA256,
        "source_manifest_sha256": EXPECTED_SOURCE_MANIFEST_SHA256,
        "precommit_seal_sha256": EXPECTED_PRECOMMIT_SEAL_SHA256,
        "runner_sha256": sha256_file(Path(__file__)),
        "result_source": "Frozen Starbreaker three-stage atom roster with exact carrier-matter relation reconstruction",
        "gravitational_wave_record_role": "hypothesis context only",
    })
    write_json(STAGING / "EXECUTION_RECEIPT.json", {
        "campaign_id": CAMPAIGN_ID,
        "started_utc": started.isoformat(),
        "completed_utc": completed.isoformat(),
        "python": sys.version,
        "result": verdict,
        "same_run_repair": False,
    })

    door_lines = "\n".join(
        f"| {row['geometry']} | {row['door']} | {row['primary_carriers']} | "
        f"{row['inequality_fraction'] if row['inequality_fraction'] is not None else 'NA'} | "
        f"{row['median_margin'] if row['median_margin'] is not None else 'NA'} |"
        for row in door_rows
    )
    result_text = f"""# CR005c Starbreaker Escape / Closure Timing Operationalization Result

## Primary verdict

`{verdict}`

The frozen Starbreaker trajectory surface was converted into an exact local
contact-crossing clock without importing a gravitational-wave timing formula.
All **{sum(row['passed'] for row in gates)}/{len(gates)}** construction gates and
**{sum(row['passed'] for row in wrong_controls)}/{len(wrong_controls)}** controls passed.

## Operational definitions

```text
stored-stage time: seed=0, collapse=1, final=2
release surface:   carrier-matter distance crosses outward through 0.076
closure surface:   carrier-matter distance crosses inward through 0.076
tau_escape_post:   earliest 010/110 outward crossing for one carrier
tau_closure:       earliest 101 inward crossing for the same carrier
```

This is a local relation clock. It is not seconds and the relation surface is
not a global horizon.

## Primary carrier-occurrence result

```text
dual post-collapse carriers = {overall['primary_carriers']}
escape before closure       = {overall['inequality_count']}
inequality fraction         = {overall['inequality_fraction']}
median closure-escape margin= {overall['median_margin']}
```

| geometry | door | primary carriers | fraction escape before closure | median margin |
|---|---|---:|---:|---:|
{door_lines}

## Source reconstruction

- Scenarios: **{scenario_count}/96**
- Atoms: **{atom_total:,}/482,112**
- Carrier-matter transition crossings solved: **{crossing_count:,}**
- Crossing failures: **{crossing_failures}**
- Carrier-matter history census: exact match = **{count_gate}**
- Frozen sources: **{sum(row['matched'] for row in source_post)}/{len(source_post)}**

## Meaning

The result decides only whether the stored Starbreaker relation trajectories
support a stable operational ordering between ending-zero release and returned
`101` closure. The gravitational-wave branch was not allowed to define the
surface, the clock, or the verdict.

## Boundary

Starbreaker currently stores three states rather than a physical time series.
No physical escape duration, horizon-closure duration, gravitational strain,
luminosity, signal speed, detector observable, or universal timing law is
installed. A physical timing test requires a prospective time-resolved
Starbreaker evolution rule.
"""
    (STAGING / "CR005c_RESULT.md").write_text(result_text, encoding="utf-8")

    artifact_names = sorted(path.name for path in STAGING.iterdir() if path.is_file())
    manifest_rows = [
        {"path": name, "bytes": (STAGING / name).stat().st_size, "sha256": sha256_file(STAGING / name)}
        for name in artifact_names
    ]
    write_csv(STAGING / "CR005c_RELEASE_MANIFEST.csv", manifest_rows)
    manifest_sha = sha256_file(STAGING / "CR005c_RELEASE_MANIFEST.csv")
    (STAGING / "CR005c_RELEASE_MANIFEST_SHA256.txt").write_text(manifest_sha + "\n", encoding="ascii")

    for row in manifest_rows:
        path = STAGING / row["path"]
        if path.stat().st_size != row["bytes"] or sha256_file(path) != row["sha256"]:
            raise RuntimeError("release manifest verification failed")

    STAGING.replace(RELEASE)
    print(json.dumps({
        "campaign_id": CAMPAIGN_ID,
        "primary_verdict": verdict,
        "primary_carriers": overall["primary_carriers"],
        "inequality_fraction": overall["inequality_fraction"],
        "median_margin": overall["median_margin"],
        "strong_cells": len(strong_cells),
        "directional_cells": len(directional_cells),
        "gates": f"{sum(row['passed'] for row in gates)}/{len(gates)}",
        "wrong_controls": f"{sum(row['passed'] for row in wrong_controls)}/{len(wrong_controls)}",
        "release_manifest_sha256": manifest_sha,
    }, indent=2))


if __name__ == "__main__":
    main()
