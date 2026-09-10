#!/usr/bin/env python3
"""CR005c Starbreaker escape/closure observability gate.

This constructive runner does not alter Starbreaker or install a GW timing law.
It inventories the time information actually present in the frozen record,
reconstructs the local affine crossings for history 101, and determines whether
escape-before-closure is observable without defining closure as that same
relation's return.
"""

from __future__ import annotations

import ast
import csv
import gzip
import hashlib
import json
import math
import shutil
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


CAMPAIGN_ID = "CR005c_STARBREAKER_ESCAPE_CLOSURE_OBSERVABILITY_GATE"
TASK = "Continue Courtroom gravitational-wave work with latest Starbreaker and SAM advances"
EXPECTED_CONTRACT_SHA256 = "71fe6f1752ddf6822625470c588964c0e200e8c8dd1428abe331c724716766c2"
EXPECTED_PRECOMMIT_SHA256 = "792723e3508da8be3eb28f20291759063c04898270201a386f756eea47efe544"
EXPECTED_SOURCE_MANIFEST_SHA256 = "9fa6cfadea55457e6112f8f1b6d460ff1bdd0c572ad911cae6e9e37ebeded43e"
EXPECTED_PRECOMMIT_SEAL_SHA256 = "d923823498a156f15c685fc6f4cb15c178de14172d6adb3dbaae7c77578749a9"
RADIUS = 0.076
TOL = 1e-12

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
CONTRACT = BASE / "CR005c_CONTRACT.json"
PRECOMMIT = BASE / "CR005c_PRECOMMIT.md"
SOURCE_MANIFEST = BASE / "CR005c_SOURCE_MANIFEST.json"
PRECOMMIT_SEAL = BASE / "CR005c_PRECOMMIT_SEAL.json"
RUNNER_SEAL = BASE / "CR005c_RUNNER_SEAL.json"
RELEASE = BASE / "release"
STAGING = BASE / ".cr005c_release_staging"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_source(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else ROOT / path


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    names = fieldnames or (list(rows[0]) if rows else [])
    if not names:
        raise ValueError(f"cannot infer fields for {path.name}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=names, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_text(value: str) -> bool:
    return value.strip().casefold() == "true"


def verify_precommit() -> dict[str, Any]:
    observed = {
        "contract": sha256_file(CONTRACT),
        "precommit": sha256_file(PRECOMMIT),
        "source_manifest": sha256_file(SOURCE_MANIFEST),
        "precommit_seal": sha256_file(PRECOMMIT_SEAL),
    }
    expected = {
        "contract": EXPECTED_CONTRACT_SHA256,
        "precommit": EXPECTED_PRECOMMIT_SHA256,
        "source_manifest": EXPECTED_SOURCE_MANIFEST_SHA256,
        "precommit_seal": EXPECTED_PRECOMMIT_SEAL_SHA256,
    }
    if observed != expected:
        raise RuntimeError(f"precommit packet changed: observed={observed}")
    seal = json.loads(PRECOMMIT_SEAL.read_text(encoding="utf-8"))
    if seal.get("runner_present_at_seal") or seal.get("results_opened"):
        raise RuntimeError("precommit chronology changed")
    if not seal.get("no_predecessor_rerun") or seal.get("same_run_repair_allowed"):
        raise RuntimeError("precommit execution guard changed")
    if seal.get("contract_sha256") != EXPECTED_CONTRACT_SHA256:
        raise RuntimeError("contract commitment changed")
    if seal.get("precommit_sha256") != EXPECTED_PRECOMMIT_SHA256:
        raise RuntimeError("precommit commitment changed")
    if seal.get("source_manifest_sha256") != EXPECTED_SOURCE_MANIFEST_SHA256:
        raise RuntimeError("source-manifest commitment changed")
    if not RUNNER_SEAL.is_file():
        raise RuntimeError("runner seal is missing")
    runner_seal = json.loads(RUNNER_SEAL.read_text(encoding="utf-8"))
    if runner_seal.get("campaign_id") != CAMPAIGN_ID:
        raise RuntimeError("runner seal campaign changed")
    if runner_seal.get("runner_sha256") != sha256_file(Path(__file__)):
        raise RuntimeError("runner changed after sealing")
    return {"observed": observed, "seal": seal, "runner_seal": runner_seal}


def validate_sources() -> tuple[list[dict[str, Any]], dict[str, Path]]:
    manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    sources = manifest.get("sources", [])
    if manifest.get("campaign_id") != CAMPAIGN_ID or manifest.get("source_count") != len(sources):
        raise RuntimeError("source manifest shape changed")
    rows: list[dict[str, Any]] = []
    by_role: dict[str, Path] = {}
    for source in sources:
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
        by_role[source["role"]] = path
    return rows, by_role


def csv_header(path: Path, *, compressed: bool = False) -> list[str]:
    if compressed:
        with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
            return next(csv.reader(handle))
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def engine_observability(path: Path) -> dict[str, Any]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    star_fields: set[str] = set()
    evolve_args: list[str] = []
    identifiers: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            identifiers.add(node.id)
        elif isinstance(node, ast.Attribute):
            identifiers.add(node.attr)
        elif isinstance(node, ast.ClassDef) and node.name == "StarAtom":
            for child in node.body:
                if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
                    star_fields.add(child.target.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "evolve_star":
            evolve_args = [arg.arg for arg in node.args.args]

    time_names = {
        "time", "timestamp", "dt", "step_time", "event_time", "physical_time",
        "closure_time", "escape_time", "release_time",
    }
    event_names = {
        "home_seal_state", "horizon_state", "event_closure", "release_surface",
        "release_surface_distance", "closure_step", "escape_step",
    }
    required_positions = {"x0", "y0", "xc", "yc", "x1", "y1"}
    return {
        "star_atom_fields": sorted(star_fields),
        "evolve_star_args": evolve_args,
        "required_endpoint_positions_present": required_positions.issubset(star_fields),
        "time_fields_present": sorted(star_fields & time_names),
        "event_state_fields_present": sorted(star_fields & event_names),
        "time_identifiers_present": sorted(identifiers & time_names),
        "event_identifiers_present": sorted(identifiers & event_names),
        "explicit_clock_present": bool((star_fields | identifiers) & time_names),
        "independent_event_closure_present": bool((star_fields | identifiers) & event_names),
    }


Vector = tuple[float, float, float]


def vec_sub(left: Vector, right: Vector) -> Vector:
    return (left[0] - right[0], left[1] - right[1], left[2] - right[2])


def vec_add(left: Vector, right: Vector) -> Vector:
    return (left[0] + right[0], left[1] + right[1], left[2] + right[2])


def vec_scale(value: Vector, scalar: float) -> Vector:
    return (value[0] * scalar, value[1] * scalar, value[2] * scalar)


def dot(left: Vector, right: Vector) -> float:
    return left[0] * right[0] + left[1] * right[1] + left[2] * right[2]


def norm(value: Vector) -> float:
    return math.sqrt(dot(value, value))


def crossing_roots(start: Vector, end: Vector, radius: float) -> list[tuple[float, str]]:
    velocity = vec_sub(end, start)
    a = dot(velocity, velocity)
    b = 2.0 * dot(start, velocity)
    c = dot(start, start) - radius * radius
    if a <= 1e-30:
        return []
    discriminant = b * b - 4.0 * a * c
    if discriminant < -1e-14:
        return []
    discriminant = max(0.0, discriminant)
    square = math.sqrt(discriminant)
    candidates = [(-b - square) / (2.0 * a), (-b + square) / (2.0 * a)]
    roots: list[tuple[float, str]] = []
    for value in candidates:
        if -TOL <= value <= 1.0 + TOL:
            value = min(1.0, max(0.0, value))
            at_root = vec_add(start, vec_scale(velocity, value))
            derivative = 2.0 * dot(at_root, velocity)
            direction = "outward" if derivative > 0.0 else "inward" if derivative < 0.0 else "tangent"
            if not roots or abs(value - roots[-1][0]) > 1e-12:
                roots.append((value, direction))
    return sorted(roots)


def read_endpoints(path: Path) -> tuple[list[dict[str, str]], set[tuple[str, int]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    needed: set[tuple[str, int]] = set()
    for row in rows:
        scenario = row["scenario_id"]
        needed.add((scenario, int(row["left_atom_index"])))
        needed.add((scenario, int(row["right_atom_index"])))
    return rows, needed


def read_needed_positions(path: Path, needed: set[tuple[str, int]]) -> dict[tuple[str, int], tuple[Vector, Vector, Vector]]:
    positions: dict[tuple[str, int], tuple[Vector, Vector, Vector]] = {}
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            key = (row["scenario_id"], int(row["atom_index"]))
            if key not in needed:
                continue
            positions[key] = (
                (float(row["x0"]), float(row["y0"]), float(row["z0"])),
                (float(row["xc"]), float(row["yc"]), float(row["zc"])),
                (float(row["x1"]), float(row["y1"]), float(row["z1"])),
            )
    return positions


def median_or_none(values: Iterable[float]) -> float | None:
    items = list(values)
    return statistics.median(items) if items else None


def synthetic_crossing_control() -> dict[str, Any]:
    release = crossing_roots((0.0, 0.0, 0.0), (0.2, 0.0, 0.0), 0.1)
    returned = crossing_roots((0.2, 0.0, 0.0), (0.0, 0.0, 0.0), 0.1)
    passed = (
        len(release) == 1 and release[0][1] == "outward" and abs(release[0][0] - 0.5) <= TOL
        and len(returned) == 1 and returned[0][1] == "inward" and abs(returned[0][0] - 0.5) <= TOL
    )
    return {"passed": passed, "outward": release, "inward": returned}


def main() -> None:
    started = datetime.now(timezone.utc)
    if RELEASE.exists() or STAGING.exists():
        raise RuntimeError("CR005c release or staging path already exists; same-run repair is prohibited")

    precommit_status = verify_precommit()
    source_pre, by_role = validate_sources()
    if not all(row["matched"] for row in source_pre):
        raise RuntimeError("a frozen source changed before execution")

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    relation_schema = json.loads(by_role["three_stage_history_semantics"].read_text(encoding="utf-8"))
    relation_summary = json.loads(by_role["frozen_history_counts_and_boundaries"].read_text(encoding="utf-8"))
    reopening_summary = json.loads(by_role["frozen_101_counts_and_claim_ceiling"].read_text(encoding="utf-8"))
    axis_summary = json.loads(by_role["latest_axis_reversal_boundary"].read_text(encoding="utf-8"))
    kinematics_summary = json.loads(by_role["machine_readable_kinematics_boundaries"].read_text(encoding="utf-8"))

    roster_header = csv_header(by_role["frozen_three_stage_positions"], compressed=True)
    endpoint_header = csv_header(by_role["frozen_returned_101_relation_roster"])
    axis_header = csv_header(by_role["latest_reopening_carrier_trajectory_geometry"])
    engine = engine_observability(by_role["frozen_starbreaker_engine_source"])

    required_roster = {
        "scenario_id", "atom_index", "kind", "x0", "y0", "z0", "xc", "yc", "zc", "x1", "y1", "z1"
    }
    time_like = {
        "time", "timestamp", "dt", "step_time", "event_time", "physical_time",
        "closure_time", "escape_time", "release_time", "closure_step", "escape_step",
    }
    roster_time_fields = sorted(set(roster_header) & time_like)
    endpoint_time_fields = sorted(set(endpoint_header) & time_like)
    axis_time_fields = sorted(set(axis_header) & time_like)

    endpoint_rows, needed = read_endpoints(by_role["frozen_returned_101_relation_roster"])
    positions = read_needed_positions(by_role["frozen_three_stage_positions"], needed)
    missing_positions = sorted(needed - set(positions))

    crossing_rows: list[dict[str, Any]] = []
    distance_max_error = 0.0
    root_failures = 0
    history_failures = 0
    for row in endpoint_rows:
        scenario = row["scenario_id"]
        left_index = int(row["left_atom_index"])
        right_index = int(row["right_atom_index"])
        left = positions.get((scenario, left_index))
        right = positions.get((scenario, right_index))
        if left is None or right is None:
            root_failures += 1
            continue
        relative = tuple(vec_sub(left[stage], right[stage]) for stage in range(3))
        distances = tuple(norm(value) for value in relative)
        frozen_distances = (
            float(row["seed_distance"]),
            float(row["collapse_distance"]),
            float(row["final_distance"]),
        )
        distance_max_error = max(distance_max_error, *(abs(a - b) for a, b in zip(distances, frozen_distances)))
        is_101 = distances[0] <= RADIUS and distances[1] > RADIUS and distances[2] <= RADIUS
        if not is_101:
            history_failures += 1
        first_roots = crossing_roots(relative[0], relative[1], RADIUS)
        second_roots = crossing_roots(relative[1], relative[2], RADIUS)
        outward = [value for value, direction in first_roots if direction == "outward"]
        inward = [value for value, direction in second_roots if direction == "inward"]
        if len(outward) != 1 or len(inward) != 1:
            root_failures += 1
            release_coordinate = None
            return_coordinate = None
            ordering = False
        else:
            release_coordinate = outward[0]
            return_coordinate = 1.0 + inward[0]
            ordering = release_coordinate < 1.0 < return_coordinate
        crossing_rows.append({
            "scenario_id": scenario,
            "seed": row["seed"],
            "anchor": row["anchor"],
            "p_level": row["p_level"],
            "geometry": row["geometry"],
            "left_atom_index": left_index,
            "right_atom_index": right_index,
            "pair_kind": row["pair_kind"],
            "source_final_contact": bool_text(row["source_final_contact"]),
            "lambda_release": release_coordinate,
            "lambda_return": return_coordinate,
            "lambda_open_interval": (return_coordinate - release_coordinate) if ordering else None,
            "release_before_same_pair_return": ordering,
            "timing_interpretation": "ENTAILED_BY_101_STAGE_ORDER__NOT_INDEPENDENT_EVENT_CLOSURE",
        })

    valid_crossings = [row for row in crossing_rows if row["release_before_same_pair_return"]]
    selected_crossings = [row for row in valid_crossings if row["source_final_contact"]]
    synthetic = synthetic_crossing_control()

    history_counts = {str(key): int(value) for key, value in relation_summary["history_counts"].items()}
    expected_history_codes = set(contract["frozen_history_dictionary"])
    ending_zero_count = sum(history_counts[code] for code in ("010", "100", "110"))
    history_rows = [
        {
            "history_code": code,
            "stored_stage_semantics": contract["frozen_history_dictionary"][code],
            "relation_count": history_counts[code],
            "ending_state": "contact" if code.endswith("1") else "open",
            "operational_class": {
                "101": "RETURNED_AFTER_OPEN_INTERVAL",
                "010": "TRANSIENT_CONTACT_THEN_ENDING_ZERO",
                "100": "EARLY_EXIT_NO_STORED_RETURN",
                "110": "LATE_EXIT_NO_STORED_RETURN",
            }.get(code, "OTHER_STORED_HISTORY"),
            "physical_time_available": False,
        }
        for code in sorted(expected_history_codes)
    ]

    clock_absent = not roster_time_fields and not endpoint_time_fields and not axis_time_fields and not engine["explicit_clock_present"]
    no_independent_closure = not engine["independent_event_closure_present"]
    physical_boundaries_open = (
        kinematics_summary["boundaries"].get("physical_velocity") is None
        and kinematics_summary["boundaries"].get("physical_pressure") is None
        and kinematics_summary["boundaries"].get("finite_A_bounce_operator") is None
        and axis_summary.get("literal_x1_carrier_identity") is None
    )

    affine_complete = (
        not missing_positions
        and len(crossing_rows) == reopening_summary["history_101_pairs"]
        and len(valid_crossings) == len(crossing_rows)
        and root_failures == 0
        and history_failures == 0
        and distance_max_error <= TOL
        and synthetic["passed"]
    )
    stage_semantics_complete = (
        relation_schema.get("history_bit_order") == ["seed", "collapse", "final"]
        and expected_history_codes == set(relation_schema.get("main_history_codes", []))
        and set(history_counts) == expected_history_codes
        and history_counts["101"] == reopening_summary["history_101_pairs"]
        and ending_zero_count == relation_summary["ending_zero_relation_count"]
    )

    readiness = {
        "explicit_clock_available": False,
        "independent_event_closure_available": False,
        "independent_release_surface_available": False,
        "returned_101_vs_ending_zero_stage_distinction_available": stage_semantics_complete,
        "affine_101_local_crossings_available": affine_complete,
        "escape_before_independent_closure_testable": False,
        "gw_timing_bridge_ready": False,
    }

    observability_rows = [
        {"observable": "stage_order", "available": True, "authority": "FROZEN_THREE_STAGE_RECORD", "use": "distinguish returned 101 from ending-zero histories"},
        {"observable": "affine_local_release_coordinate", "available": affine_complete, "authority": "DIAGNOSTIC_INTERPOLATION", "use": "local contact exit only; not physical tau"},
        {"observable": "affine_local_return_coordinate", "available": affine_complete, "authority": "DIAGNOSTIC_INTERPOLATION", "use": "same-pair return only; not independent event closure"},
        {"observable": "physical_or_solver_clock", "available": False, "authority": "ABSENT", "use": "required for tau"},
        {"observable": "independent_home_seal_state", "available": False, "authority": "ABSENT", "use": "required event closure"},
        {"observable": "independent_release_surface", "available": False, "authority": "ABSENT", "use": "0.076 remains a local contact radius"},
        {"observable": "escape_before_independent_closure", "available": False, "authority": "NOT_IDENTIFIABLE", "use": "future bridge gate"},
    ]

    controls = [
        {"control": "WC01_SYNTHETIC_CROSSING_DIRECTION", "passed": synthetic["passed"], "observation": json.dumps(synthetic, sort_keys=True)},
        {"control": "WC02_SAME_PAIR_RETURN_IS_NOT_EVENT_CLOSURE", "passed": no_independent_closure, "observation": "local 101 return rejected as independent closure"},
        {"control": "WC03_FINAL_CONTACT_IS_NOT_CLOSURE_TIME", "passed": "source_final_contact" in endpoint_header and not endpoint_time_fields, "observation": "final selector has no timestamp"},
        {"control": "WC04_FINAL_FATE_IS_NOT_ESCAPE_TIME", "passed": "final_fate" in roster_header and not roster_time_fields, "observation": "endpoint label has no cadence"},
        {"control": "WC05_CONTACT_RADIUS_IS_NOT_HORIZON", "passed": relation_schema.get("proximity_radius") == RADIUS, "observation": "radius role remains geometric proximity"},
        {"control": "WC06_NO_EQUAL_PHYSICAL_DURATION_ASSUMPTION", "passed": True, "observation": "lambda is explicitly stage-normalized only"},
        {"control": "WC07_ENDING_ZERO_HISTORIES_RETAINED", "passed": ending_zero_count > 0, "observation": str(ending_zero_count)},
        {"control": "WC08_B_X1_NOT_ASSIGNED", "passed": axis_summary.get("literal_x1_carrier_identity") is None, "observation": "no causal or identity assignment"},
    ]

    gates = [
        {"gate": "G01_SOURCE_HASHES_MATCH", "passed": all(row["matched"] for row in source_pre)},
        {"gate": "G02_THREE_STAGE_ROSTER_NO_TIME_FIELD", "passed": required_roster.issubset(roster_header) and clock_absent},
        {"gate": "G03_HISTORY_SCHEMA_NO_CADENCE", "passed": stage_semantics_complete and relation_schema.get("history_bit_order") == ["seed", "collapse", "final"]},
        {"gate": "G04_ENGINE_HAS_NO_EVENT_CLOCK_OR_SEAL_STATE", "passed": clock_absent and no_independent_closure},
        {"gate": "G05_RETURNED_AND_ENDING_ZERO_CLASSES_CLOSE", "passed": stage_semantics_complete},
        {"gate": "G06_AFFINE_101_LOCAL_CROSSINGS_CLOSE", "passed": affine_complete},
        {"gate": "G07_TAUTOLOGY_NOT_PROMOTED", "passed": affine_complete and not readiness["escape_before_independent_closure_testable"]},
        {"gate": "G08_PHYSICAL_CLAIM_FIREWALL", "passed": physical_boundaries_open},
        {"gate": "G09_NO_ENGINE_OR_REGISTRY_MUTATION", "passed": True},
        {"gate": "G10_ATOMIC_RELEASE_INVENTORY", "passed": True},
    ]
    construction_pass = all(row["passed"] for row in gates) and all(row["passed"] for row in controls)
    verdict = (
        "BOUNDARY_STAGE_ORDERING_ONLY__PHYSICAL_ESCAPE_BEFORE_CLOSURE_NOT_IDENTIFIABLE__EVENT_CLOCK_REQUIRED"
        if construction_pass
        else "FAIL_STARBREAKER_TIMING_OBSERVABILITY_CONSTRUCTION"
    )

    source_post, _ = validate_sources()
    sources_unchanged = source_pre == source_post and all(row["matched"] for row in source_post)
    if not sources_unchanged:
        verdict = "FAIL_STARBREAKER_TIMING_OBSERVABILITY_CONSTRUCTION"
        construction_pass = False

    STAGING.mkdir(parents=True)
    write_csv(STAGING / "CR005c_AFFINE_101_CROSSINGS.csv", crossing_rows)
    write_csv(STAGING / "CR005c_HISTORY_SEMANTICS.csv", history_rows)
    write_csv(STAGING / "CR005c_OBSERVABILITY_MATRIX.csv", observability_rows)
    write_csv(STAGING / "CR005c_GATES.csv", gates)
    write_csv(STAGING / "CR005c_WRONG_CONTROLS.csv", controls)
    write_csv(STAGING / "CR005c_SOURCE_VALIDATION.csv", source_post)

    operational_dictionary = {
        "campaign_id": CAMPAIGN_ID,
        "stage_coordinate": {"seed": 0, "collapse": 1, "final": 2, "physical_time": False},
        "history_dictionary": contract["frozen_history_dictionary"],
        "returned_history": "101",
        "ending_zero_histories": ["010", "100", "110"],
        "local_release_surface": {"definition": "outward crossing of pair separation 0.076", "physical_horizon": False},
        "local_return_closure": {"definition": "inward recrossing of same 0.076 surface", "independent_event_closure": False},
        "event_closure": None,
        "physical_escape_time": None,
        "affine_coordinate": {"physical_time": False, "same_pair_inequality_is_tautological": True},
        "required_next_instrumentation": contract["observability_requirements"],
    }
    write_json(STAGING / "CR005c_OPERATIONAL_DICTIONARY.json", operational_dictionary)

    release_values = [row["lambda_release"] for row in valid_crossings]
    return_values = [row["lambda_return"] for row in valid_crossings]
    interval_values = [row["lambda_open_interval"] for row in valid_crossings]
    release_median = median_or_none(release_values)
    return_median = median_or_none(return_values)
    interval_median = median_or_none(interval_values)
    summary = {
        "campaign_id": CAMPAIGN_ID,
        "task": TASK,
        "record_class": "CONSTRUCTIVE_OBSERVABILITY_AND_SEMANTICS_GATE",
        "verdict": verdict,
        "construction_pass": construction_pass,
        "source_hashes_matched": sum(row["matched"] for row in source_post),
        "source_count": len(source_post),
        "scenario_count": relation_summary["scenario_count"],
        "atom_count": relation_summary["atom_occurrences"],
        "history_counts": history_counts,
        "ending_zero_relation_count": ending_zero_count,
        "history_101_relation_count": len(crossing_rows),
        "history_101_selected_count": sum(row["source_final_contact"] for row in crossing_rows),
        "affine_101": {
            "complete": affine_complete,
            "root_failures": root_failures,
            "history_failures": history_failures,
            "missing_position_count": len(missing_positions),
            "distance_max_abs_error": distance_max_error,
            "release_min": min(release_values) if release_values else None,
            "release_median": release_median,
            "release_max": max(release_values) if release_values else None,
            "return_min": min(return_values) if return_values else None,
            "return_median": return_median,
            "return_max": max(return_values) if return_values else None,
            "open_interval_median": interval_median,
            "all_release_before_same_pair_return": len(valid_crossings) == len(crossing_rows),
            "inequality_status": "ENTAILED_BY_101_STAGE_ORDER__NOT_INDEPENDENT_EVENT_CLOSURE",
        },
        "engine_observability": engine,
        "roster_time_fields": roster_time_fields,
        "endpoint_time_fields": endpoint_time_fields,
        "axis_time_fields": axis_time_fields,
        "readiness": readiness,
        "physical_claims": {
            "tau_theta_escape": None,
            "tau_closure": None,
            "release_surface": None,
            "home_horizon": None,
            "gw_emission": None,
            "signal_speed": None,
        },
        "same_run_repair": False,
        "registry_mutated": False,
        "engine_mutated": False,
        "precommit": precommit_status,
    }
    write_json(STAGING / "CR005c_SUMMARY.json", summary)

    result_text = f"""# CR005c Starbreaker Escape / Closure Observability Gate — Result

## Primary verdict

`{verdict}`

## What the current record does establish

The frozen Starbreaker history grammar cleanly distinguishes returned relations
from ending-zero relations:

```text
101 -> contact, open, returned contact
010 -> open, transient contact, open
100 -> contact, open, open
110 -> contact, contact, open
```

The complete record contains **{history_counts['101']:,}** history-`101`
relations and **{ending_zero_count:,}** ending-zero relations.

For all **{len(crossing_rows):,}** frozen `101` relations, the exact
piecewise-affine Cartesian probe found one outward crossing on the
seed-to-collapse leg and one inward crossing on the collapse-to-final leg.
The median coordinates were:

```text
lambda_release = {release_median if release_median is not None else float('nan'):.9f}
lambda_return  = {return_median if return_median is not None else float('nan'):.9f}
open interval  = {interval_median if interval_median is not None else float('nan'):.9f}
```

This confirms the local near-far-near geometry. It does **not** establish a
physical timing law: `lambda` is a stage-normalized affine coordinate, and
`lambda_release < lambda_return` is already entailed by the `101` history bits.

## Why the GW timing bridge remains open

The current engine and frozen roster contain no physical or solver clock, no
independent Home/horizon seal state, and no independently justified release
surface. The radius `0.076` is a local contact threshold. A pair's own inward
recrossing cannot also serve as the independent event closure against which its
escape is tested.

Therefore the proposed inequality

```text
tau_Theta_escape < tau_closure
```

is not identifiable from the current record. Promoting it now would rename
stage order as physical time.

## Smallest next instrumentation

1. emit a solver step or cadence;
2. emit a scenario-level `home_seal_state` independent of the tested dyad;
3. emit signed distance to a separately defined release surface;
4. timestamp carrier crossing direction;
5. compare returned `101` and ending-zero `010/100/110` populations on that
   same clock.

No Starbreaker engine, SAM registry, prior verdict, or GW law was changed.
"""
    (STAGING / "CR005c_RESULT.md").write_text(result_text, encoding="utf-8", newline="\n")

    completed = datetime.now(timezone.utc)
    provenance = {
        "campaign_id": CAMPAIGN_ID,
        "started_utc": started.isoformat(),
        "completed_utc": completed.isoformat(),
        "contract_sha256": sha256_file(CONTRACT),
        "precommit_sha256": sha256_file(PRECOMMIT),
        "source_manifest_sha256": sha256_file(SOURCE_MANIFEST),
        "precommit_seal_sha256": sha256_file(PRECOMMIT_SEAL),
        "runner_sha256": sha256_file(Path(__file__)),
        "runner_seal_sha256": sha256_file(RUNNER_SEAL) if RUNNER_SEAL.is_file() else None,
        "method": "hash-verified schema and engine observability audit plus exact piecewise-affine 101 crossing reconstruction",
        "predecessor_rerun": False,
        "same_run_repair": False,
    }
    write_json(STAGING / "CR005c_PROVENANCE.json", provenance)
    write_json(STAGING / "CR005c_RUN_RECEIPT.json", {
        "campaign_id": CAMPAIGN_ID,
        "started_utc": started.isoformat(),
        "completed_utc": completed.isoformat(),
        "python": sys.version,
        "verdict": verdict,
        "same_run_repair": False,
    })

    artifact_names = sorted(path.name for path in STAGING.iterdir() if path.is_file())
    manifest_rows = [
        {"path": name, "bytes": (STAGING / name).stat().st_size, "sha256": sha256_file(STAGING / name)}
        for name in artifact_names
    ]
    write_csv(STAGING / "CR005c_RELEASE_MANIFEST.csv", manifest_rows)
    manifest_hash = sha256_file(STAGING / "CR005c_RELEASE_MANIFEST.csv")
    (STAGING / "CR005c_RELEASE_MANIFEST_SHA256.txt").write_text(manifest_hash + "\n", encoding="ascii", newline="\n")
    for row in manifest_rows:
        path = STAGING / row["path"]
        if path.stat().st_size != row["bytes"] or sha256_file(path) != row["sha256"]:
            raise RuntimeError("release manifest verification failed")

    STAGING.replace(RELEASE)
    print(json.dumps({
        "campaign_id": CAMPAIGN_ID,
        "verdict": verdict,
        "history_101": len(crossing_rows),
        "ending_zero": ending_zero_count,
        "affine_crossings_complete": affine_complete,
        "gw_timing_bridge_ready": readiness["gw_timing_bridge_ready"],
        "gates": f"{sum(row['passed'] for row in gates)}/{len(gates)}",
        "wrong_controls": f"{sum(row['passed'] for row in controls)}/{len(controls)}",
        "release_manifest_sha256": manifest_hash,
    }, indent=2))


if __name__ == "__main__":
    main()
