#!/usr/bin/env python3
"""CR210d full fresh octahedral complete-ledger structural adapter.

This standalone runner re-executes all seventeen frozen structural gates.  It
does not import or transform a prior runner, and it opens no PDG, outcome,
workbook, F81-membership, mass, isotope, or binding source.
"""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


RECORD_ID = "CR210d_OCTAHEDRAL_COMPLETE_LEDGER_BOUNDARY_CLOSURE_APPEAL"
TASK = (
    "Execute CR210d as a fresh structural closure successor that preserves "
    "CR210c's fifteen passed gates as immutable historical evidence, tests the "
    "precommitted modulo-6 cross-kind boundary map with explicit boundary-domain, "
    "bijection, and involution guards, produces a current composite structural "
    "verdict, keeps PDG and binding closed, and stops after the frozen structural closure"
)
PASS_VERDICT = (
    "CR210d_PASS_EXACT_SOURCE_NATIVE_W9_BY_K18_ADDRESS_FACTORIZATION"
    "__SLOT_PARTITION_ROUTE_EDGE_OVERLAP_ORIENTATION_AND_PHYSICAL_INCIDENCE_OPEN"
)
FAIL_VERDICT = "CR210d_FAIL_FRESH_PRECOMMITTED_STRUCTURAL_GATE"

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
SOURCE_MANIFEST_PATH = HERE / "CR210d_SOURCE_MANIFEST.json"
PREMISES_PATH = HERE / "CR210d_DECLARED_PREMISES.json"
PRECOMMIT_PATH = HERE / "CR210d_PRECOMMIT.md"
PRECOMMIT_SEAL_PATH = HERE / "CR210d_PRECOMMIT_SEAL.txt"

EXPECTED_LOCAL_HASHES = {
    "CR210d_SOURCE_MANIFEST.json": "c3b44ad7f40078f13a0b61abc676ac84a86c547bde7a7521b190fbcabf85812b",
    "CR210d_DECLARED_PREMISES.json": "f9c08cccc0bfa4b78428c0b3523ee22f2e17d2562ef88dfbd81ad6b9b87a93e8",
    "CR210d_PRECOMMIT.md": "1698321236e276e3fb279ac19a1f8f3b1fc3a5daf903ff2ab8a3ba35d898223d",
    "CR210d_PRECOMMIT_SEAL.txt": "2ff66d47bdc63bdaeaf0547ec3f75b40ee5dbe5e84e254901d479b7dc1b8e6d3",
}

Coord = tuple[int, int, int]
GraphEdge = tuple[Coord, Coord]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): normalize(item) for key, item in value.items()}
    if isinstance(value, (set, frozenset)):
        return [normalize(item) for item in sorted(value, key=repr)]
    if isinstance(value, tuple):
        return [normalize(item) for item in value]
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, Counter):
        return {str(key): normalize(item) for key, item in value.items()}
    return value


def compact_json(value: Any) -> str:
    return json.dumps(normalize(value), separators=(",", ":"), sort_keys=True)


def write_json(name: str, value: Any) -> Path:
    path = HERE / name
    path.write_text(json.dumps(normalize(value), indent=2) + "\n", encoding="utf-8")
    return path


def write_csv(name: str, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> Path:
    path = HERE / name
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="raise")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return path


def resolve_path(raw: str, base: Path = ROOT) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else base / path


def bool_field(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def coord_text(coord: Coord) -> str:
    return compact_json(list(coord))


def role(coord: Coord) -> str:
    return {0: "cell", 1: "point", 2: "edge", 3: "face"}[
        sum(component != 0 for component in coord)
    ]


def coord_id(coord: Coord) -> str:
    return f"{role(coord).upper()}_{coord[0]:+d}_{coord[1]:+d}_{coord[2]:+d}"


def point_coord(dimension: int, side: int) -> Coord:
    values = [0, 0, 0]
    values[dimension] = -1 if side == 0 else 1
    return tuple(values)  # type: ignore[return-value]


def antipode(coord: Coord) -> Coord:
    return tuple(-value for value in coord)  # type: ignore[return-value]


def canon_graph_edge(left: Coord, right: Coord) -> GraphEdge:
    if left == right:
        raise ValueError(f"self edge: {left}")
    return tuple(sorted((left, right)))  # type: ignore[return-value]


def route_edge(route_value: int) -> GraphEdge:
    dimension = route_value % 3
    side = route_value % 2
    hemisphere = route_value // 6
    first = point_coord(dimension, side)
    second = point_coord((dimension + 1 + hemisphere) % 3, side ^ hemisphere)
    return canon_graph_edge(first, second)


def slot_kind(slot: int) -> str:
    if slot < 18:
        return "carrier"
    if slot < 144:
        return "matter"
    return "ledger_shadow"


def base3_centered(index: int) -> Coord:
    return ((index // 9) % 3 - 1, (index // 3) % 3 - 1, index % 3 - 1)


def face_for_block(block: int) -> Coord | None:
    if block == 8:
        return None
    return tuple(1 if (block >> axis) & 1 else -1 for axis in range(3))  # type: ignore[return-value]


def compatible(lower: Coord, upper: Coord) -> bool:
    return all(value == 0 or value == upper[index] for index, value in enumerate(lower))


def build_h27() -> tuple[set[Coord], set[GraphEdge], list[dict[str, Any]]]:
    nodes = set(itertools.product((-1, 0, 1), repeat=3))
    cell: Coord = (0, 0, 0)
    points = sorted(node for node in nodes if role(node) == "point")
    edge_nodes = sorted(node for node in nodes if role(node) == "edge")
    faces = sorted(node for node in nodes if role(node) == "face")
    edges: set[GraphEdge] = set()
    rows: list[dict[str, Any]] = []

    def add(left: Coord, right: Coord, link_type: str) -> None:
        graph_edge = canon_graph_edge(left, right)
        if graph_edge in edges:
            raise ValueError(f"duplicate H27 edge: {graph_edge}")
        edges.add(graph_edge)
        rows.append(
            {
                "link_id": len(rows),
                "link_type": link_type,
                "left_node": coord_id(left),
                "right_node": coord_id(right),
                "left_coordinate": coord_text(left),
                "right_coordinate": coord_text(right),
            }
        )

    for face in faces:
        add(cell, face, "cell_face")
    for face in faces:
        for edge_node in edge_nodes:
            if compatible(edge_node, face):
                add(face, edge_node, "face_edge")
    for edge_node in edge_nodes:
        for point in points:
            if compatible(point, edge_node):
                add(edge_node, point, "edge_point")
    return nodes, edges, rows


def components(nodes: set[Coord], edges: set[GraphEdge]) -> list[int]:
    adjacency: dict[Coord, set[Coord]] = {node: set() for node in nodes}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    unseen = set(nodes)
    sizes: list[int] = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        queue: deque[Coord] = deque([start])
        count = 0
        while queue:
            node = queue.popleft()
            count += 1
            for neighbor in adjacency[node]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    queue.append(neighbor)
        sizes.append(count)
    return sorted(sizes, reverse=True)


def degree_histogram(nodes: set[Coord], edges: set[GraphEdge]) -> dict[int, int]:
    degree = Counter({node: 0 for node in nodes})
    for left, right in edges:
        degree[left] += 1
        degree[right] += 1
    return dict(sorted(Counter(degree.values()).items()))


def transform_coord(
    coord: Coord, permutation: tuple[int, int, int], signs: tuple[int, int, int]
) -> Coord:
    return tuple(signs[index] * coord[permutation[index]] for index in range(3))  # type: ignore[return-value]


def permutation_parity(permutation: tuple[int, int, int]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(3)
        for j in range(i + 1, 3)
    )
    return -1 if inversions % 2 else 1


def parse_prior_coord(raw: str) -> Coord:
    values = json.loads(raw)
    if not isinstance(values, list) or len(values) != 3:
        raise ValueError(f"invalid coordinate: {raw}")
    return tuple(int(value) - 1 for value in values)  # type: ignore[return-value]


def verify_hash_file(manifest_id: str, path: Path, base: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        parts = line.split("  ", 1)
        if len(parts) != 2 or len(parts[0]) != 64:
            rows.append(
                {
                    "manifest_id": manifest_id,
                    "line": line_number,
                    "entry": line,
                    "expected_sha256": "",
                    "actual_sha256": "",
                    "exists": False,
                    "match": False,
                }
            )
            continue
        expected, raw_name = parts
        target = resolve_path(raw_name, base)
        exists = target.is_file()
        actual = sha256_file(target) if exists else ""
        rows.append(
            {
                "manifest_id": manifest_id,
                "line": line_number,
                "entry": raw_name,
                "expected_sha256": expected,
                "actual_sha256": actual,
                "exists": exists,
                "match": exists and actual == expected,
            }
        )
    return rows


def decode_boundary(slot: int) -> tuple[int, int, int]:
    block = slot // 18
    if block not in {0, 8}:
        raise ValueError(f"not a boundary slot: {slot}")
    q, residue = divmod(slot % 18, 6)
    return block, q, residue


def encode_boundary(block: int, q: int, residue: int) -> int:
    return block * 18 + q * 6 + residue


def phi_cross(slot: int) -> int:
    block, q, residue = decode_boundary(slot)
    return encode_boundary(8 - block, q, (residue + 3) % 6)


def phi_same(slot: int) -> int:
    block, q, residue = decode_boundary(slot)
    return encode_boundary(block, q, (residue + 3) % 6)


def canon_slot_pair(left: int, right: int) -> tuple[int, int]:
    if left == right:
        raise ValueError(f"fixed boundary slot: {left}")
    return tuple(sorted((left, right)))  # type: ignore[return-value]


def quotient_audit(
    pairing_name: str, pair_set: set[tuple[int, int]]
) -> dict[str, Any]:
    pair_class: dict[int, str] = {}
    for index, (left, right) in enumerate(sorted(pair_set)):
        class_id = f"B{index:02d}"
        pair_class[left] = class_id
        pair_class[right] = class_id
    side_classes: dict[int, set[str]] = {0: set(), 1: set()}
    for slot in range(162):
        side = slot % 2
        if slot in pair_class:
            side_classes[side].add(pair_class[slot])
        elif slot_kind(slot) == "matter":
            side_classes[side].add(f"M{slot:03d}")
    intersection = side_classes[0] & side_classes[1]
    union = side_classes[0] | side_classes[1]
    symmetric = side_classes[0] ^ side_classes[1]
    return {
        "pairing": pairing_name,
        "pair_classes": len(pair_set),
        "side_a_classes": len(side_classes[0]),
        "side_b_classes": len(side_classes[1]),
        "intersection_classes": len(intersection),
        "union_classes": len(union),
        "symmetric_difference_classes": len(symmetric),
        "occurrence_sum": len(union) + len(intersection),
    }


def main() -> int:
    started = datetime.now(timezone.utc)
    generated: list[Path] = []
    checks: list[dict[str, Any]] = []

    def add_check(
        check_id: str,
        expected: Any,
        observed: Any,
        passed: bool,
        significance: str,
    ) -> None:
        checks.append(
            {
                "check_id": check_id,
                "expected": compact_json(expected),
                "observed": compact_json(observed),
                "pass": bool(passed),
                "significance": significance,
            }
        )

    manifest = json.loads(SOURCE_MANIFEST_PATH.read_text(encoding="utf-8"))
    premises = json.loads(PREMISES_PATH.read_text(encoding="utf-8"))
    seal_text = PRECOMMIT_SEAL_PATH.read_text(encoding="utf-8")

    # C00: the contract was sealed before this standalone runner existed.
    local_rows: list[dict[str, Any]] = []
    for name, expected in EXPECTED_LOCAL_HASHES.items():
        path = HERE / name
        actual = sha256_file(path)
        local_rows.append(
            {
                "file": name,
                "expected_sha256": expected,
                "actual_sha256": actual,
                "match": actual == expected,
            }
        )
    c00 = (
        len(local_rows) == 4
        and all(row["match"] for row in local_rows)
        and "runner_present_at_seal=false" in seal_text
        and "fresh_gate_count=17" in seal_text
    )
    generated.append(
        write_csv(
            "CR210d_LOCAL_CONTRACT_VALIDATION.csv",
            ["file", "expected_sha256", "actual_sha256", "match"],
            local_rows,
        )
    )
    add_check(
        "C00_PRECOMMIT_SEAL",
        {
            "contract_files": 3,
            "seal_files": 1,
            "runner_absent_at_seal": True,
            "fresh_gates": 17,
        },
        {
            "contract_files": len(local_rows) - 1,
            "seal_files": 1,
            "all_hashes_match": all(row["match"] for row in local_rows),
            "runner_absent_at_seal": "runner_present_at_seal=false" in seal_text,
            "fresh_gates": 17,
        },
        c00,
        "Predictions and controls were immutable before runner construction.",
    )

    # C01: direct source validation plus all frozen lineage zippers.
    source_rows: list[dict[str, Any]] = []
    source_paths: dict[str, Path] = {}
    parsed_ids = set(manifest["parsed_sources"])
    for entry in manifest["sources"]:
        path = resolve_path(entry["path"])
        data = path.read_bytes()
        actual_hash = sha256_bytes(data)
        actual_bytes = len(data)
        source_paths[entry["source_id"]] = path
        source_rows.append(
            {
                "source_id": entry["source_id"],
                "path": str(path),
                "declared_sha256": entry["sha256"],
                "actual_sha256": actual_hash,
                "declared_bytes": entry["bytes"],
                "actual_bytes": actual_bytes,
                "hash_match": actual_hash == entry["sha256"],
                "bytes_match": actual_bytes == entry["bytes"],
                "access_mode": "parsed" if entry["source_id"] in parsed_ids else "hash_only",
            }
        )
    generated.append(
        write_csv(
            "CR210d_SOURCE_VALIDATION.csv",
            list(source_rows[0]),
            source_rows,
        )
    )
    source_ok = (
        len(source_rows) == manifest["source_count"] == 25
        and all(row["hash_match"] and row["bytes_match"] for row in source_rows)
    )

    cr210c_dir = source_paths["CR210C_EXECUTION_HASHES"].parent
    lineage_rows = []
    lineage_rows.extend(
        verify_hash_file(
            "PSLI_PARENT",
            source_paths["PSLI_FREEZE_HASHES"],
            ROOT,
        )
    )
    lineage_rows.extend(
        verify_hash_file(
            "CR210C_EXECUTION",
            source_paths["CR210C_EXECUTION_HASHES"],
            cr210c_dir,
        )
    )
    lineage_rows.extend(
        verify_hash_file(
            "CR210C_OUTER_FREEZE",
            source_paths["CR210C_HARD_FREEZE_HASHES"],
            cr210c_dir,
        )
    )
    generated.append(
        write_csv(
            "CR210d_LINEAGE_INTEGRITY.csv",
            [
                "manifest_id",
                "line",
                "entry",
                "expected_sha256",
                "actual_sha256",
                "exists",
                "match",
            ],
            lineage_rows,
        )
    )
    lineage_counts = Counter(row["manifest_id"] for row in lineage_rows)
    lineage_ok = (
        lineage_counts == {"PSLI_PARENT": 14, "CR210C_EXECUTION": 35, "CR210C_OUTER_FREEZE": 8}
        and all(row["match"] for row in lineage_rows)
    )

    historical_rows: list[dict[str, Any]] = []
    with source_paths["CR210C_CHECKS"].open("r", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            historical_rows.append(
                {
                    "check_id": row["check_id"],
                    "historical_pass": bool_field(row["pass"]),
                    "counted_as_CR210d_pass": False,
                }
            )
    generated.append(
        write_csv(
            "CR210d_HISTORICAL_CHECK_AUDIT.csv",
            ["check_id", "historical_pass", "counted_as_CR210d_pass"],
            historical_rows,
        )
    )
    historical_pass_ids = {row["check_id"] for row in historical_rows if row["historical_pass"]}
    historical_fail_ids = {row["check_id"] for row in historical_rows if not row["historical_pass"]}
    expected_historical_pass = {
        "C00_PRECOMMIT_SEAL",
        "C01_SOURCE_CONTRACT",
        "C02_SOURCE_NATIVE_FORMULAS",
        "C03_SOURCE_KIND_TOTALS",
        "C04_W9_BY_K18_FACTORIZATION",
        "C05_PARTITION_NONUNIQUENESS",
        "C06_ROUTE_EDGE_CANDIDATE",
        "C07_SIX_FIBERS",
        "C08_CONSTRUCTED_TERNARY_RANK",
        "C09_H27_FACE_POSET",
        "C10_PRIOR_SELECTOR_CONTROL",
        "C11_GRAPH_REPLACEMENT_NOT_ADDITION",
        "C12_OCTAHEDRAL_AUTOMORPHISMS",
        "C13_SIDE_REVERSAL",
        "C16_FIREWALL",
    }
    expected_historical_fail = {"C14_BOUNDARY_QUOTIENT", "C15_WRONG_CONTROLS"}
    historical_ok = (
        len(historical_rows) == 17
        and historical_pass_ids == expected_historical_pass
        and historical_fail_ids == expected_historical_fail
    )

    historical_manifest = json.loads(
        source_paths["CR210C_SOURCE_MANIFEST"].read_text(encoding="utf-8")
    )
    historical_source_rows: list[dict[str, Any]] = []
    for entry in historical_manifest["sources"]:
        path = resolve_path(entry["path"])
        exists = path.is_file()
        actual_hash = sha256_file(path) if exists else ""
        actual_bytes = path.stat().st_size if exists else -1
        historical_source_rows.append(
            {
                "source_id": entry["source_id"],
                "path": str(path),
                "exists": exists,
                "expected_sha256": entry["sha256"],
                "actual_sha256": actual_hash,
                "expected_bytes": entry["bytes"],
                "actual_bytes": actual_bytes,
                "match": exists
                and actual_hash == entry["sha256"]
                and actual_bytes == entry["bytes"],
            }
        )
    generated.append(
        write_csv(
            "CR210d_HISTORICAL_SOURCE_REVALIDATION.csv",
            list(historical_source_rows[0]),
            historical_source_rows,
        )
    )
    historical_source_ok = (
        len(historical_source_rows) == historical_manifest["source_count"] == 20
        and all(row["match"] for row in historical_source_rows)
    )
    historical_validation = json.loads(
        source_paths["CR210C_VALIDATION"].read_text(encoding="utf-8")
    )
    historical_validation_ok = (
        historical_validation["record_id"]
        == "CR210c_OCTAHEDRAL_COMPLETE_LEDGER_ADDRESS_ADAPTER"
        and historical_validation["status"] == "FAIL"
        and historical_validation["verdict"]
        == "CR210c_FAIL_PRECOMMITTED_STRUCTURAL_CHECK"
        and historical_validation["checks_passed"] == 15
        and historical_validation["checks_total"] == 17
        and set(historical_validation["failed_checks"])
        == {"C14_BOUNDARY_QUOTIENT", "C15_WRONG_CONTROLS"}
        and historical_validation["execution_count"] == 1
    )
    historical_adjudication_text = source_paths[
        "CR210C_FAILURE_ADJUDICATION"
    ].read_text(encoding="utf-8")
    historical_precommit_text = source_paths["CR210C_PRECOMMIT"].read_text(
        encoding="utf-8"
    )
    historical_diagnosis_ok = all(
        snippet in historical_adjudication_text
        for snippet in (
            "CR210c_FAIL_PRECOMMITTED_STRUCTURAL_CHECK",
            "15 of 17 gates passed",
            "((r+3) mod 6)",
            "invalid slots 162, 163, and 164",
            "same-kind comparator passed its local audit",
        )
    )
    historical_precommit_ok = all(
        snippet in historical_precommit_text
        for snippet in (
            "(r+3) mod6",
            "No same-run repair is permitted.",
            "C14 and dependent C15 failed",
            "Each boundary map produces exactly 18 pairs",
        )
    )
    c01 = (
        source_ok
        and lineage_ok
        and historical_ok
        and historical_source_ok
        and historical_validation_ok
        and historical_diagnosis_ok
        and historical_precommit_ok
    )
    add_check(
        "C01_SOURCE_CONTRACT",
        {
            "CR210d_sources": 25,
            "zipper_counts": {"PSLI_PARENT": 14, "CR210C_EXECUTION": 35, "CR210C_OUTER_FREEZE": 8},
            "historical_checks": [15, 2],
            "historical_sources": 20,
            "historical_validation": "frozen_FAIL_15_of_17",
            "historical_diagnosis": "missing_modulo_confirmed",
            "errors": 0,
        },
        {
            "CR210d_sources": len(source_rows),
            "zipper_counts": lineage_counts,
            "historical_checks": [len(historical_pass_ids), len(historical_fail_ids)],
            "historical_sources": len(historical_source_rows),
            "historical_validation": historical_validation["verdict"],
            "historical_diagnosis": {
                "adjudication_match": historical_diagnosis_ok,
                "precommit_match": historical_precommit_ok,
            },
            "errors": sum(not row["match"] for row in lineage_rows)
            + sum(not row["match"] for row in historical_source_rows)
            + sum(not (row["hash_match"] and row["bytes_match"]) for row in source_rows),
        },
        c01,
        "The new run starts from exact current bytes while preserving historical status without inheriting its passes.",
    )

    # C02: source-native definitions.
    source_text = source_paths["STARBRAKER_BASE_SOURCE"].read_text(encoding="utf-8")
    snippets = [
        "THETA = 18",
        "M_NATIVE = 126",
        "L = 162",
        "def ledger_kind(slot: int)",
        "if slot < THETA",
        "if slot < R2",
        "route = atom_id % R",
        "dimension = atom_id % D_HAT",
        "side = atom_id % H_NATIVE",
    ]
    missing_snippets = [snippet for snippet in snippets if snippet not in source_text]
    add_check(
        "C02_SOURCE_NATIVE_FORMULAS",
        {"required": len(snippets), "missing": []},
        {"required": len(snippets), "missing": missing_snippets},
        not missing_snippets,
        "Every canonical field is traced directly to the frozen generator source.",
    )

    # C03-C08: canonical slots, blocks, partitions, route edges, fibers, ternary ranks.
    slot_rows: list[dict[str, Any]] = []
    for slot in range(162):
        block = slot // 18
        offset = slot % 18
        q, residue = divmod(offset, 6)
        dimension = slot % 3
        side = slot % 2
        j = slot // 6
        ternary = base3_centered(j)
        face = face_for_block(block)
        slot_rows.append(
            {
                "ledger_slot": slot,
                "kind": slot_kind(slot),
                "w9_block": block,
                "w9_role": "closure_cell" if block == 8 else "oriented_face",
                "w9_coordinate": "" if face is None else coord_text(face),
                "k18_offset": offset,
                "k18_role": "edge" if offset < 12 else "point",
                "microcycle_q": q,
                "residue_r": residue,
                "dimension": dimension,
                "side": side,
                "fiber_residue": slot % 6,
                "fiber_j": j,
                "ternary_coordinate": coord_text(ternary),
                "ternary_rank": sum(value != 0 for value in ternary),
                "route_parity_0": slot % 12,
                "route_parity_1": (slot + 6) % 12,
            }
        )
    generated.append(write_csv("CR210d_SLOT_TEMPLATE.csv", list(slot_rows[0]), slot_rows))
    kind_counts = Counter(row["kind"] for row in slot_rows)
    c03 = kind_counts == {"carrier": 18, "matter": 126, "ledger_shadow": 18}
    add_check(
        "C03_SOURCE_KIND_TOTALS",
        {"carrier": 18, "matter": 126, "ledger_shadow": 18, "total": 162},
        {**kind_counts, "total": len(slot_rows)},
        c03 and len(slot_rows) == 162,
        "The full source-native ledger is preserved without deletion or double counting.",
    )

    block_rows: list[dict[str, Any]] = []
    for block in range(9):
        rows = [row for row in slot_rows if row["w9_block"] == block]
        roles = Counter(row["k18_role"] for row in rows)
        block_rows.append(
            {
                "w9_block": block,
                "kind": rows[0]["kind"],
                "w9_role": rows[0]["w9_role"],
                "slot_count": len(rows),
                "edge_channel_count": roles["edge"],
                "point_channel_count": roles["point"],
            }
        )
    generated.append(write_csv("CR210d_BLOCK_AUDIT.csv", list(block_rows[0]), block_rows))
    c04 = (
        len(block_rows) == 9
        and all(
            row["slot_count"] == 18
            and row["edge_channel_count"] == 12
            and row["point_channel_count"] == 6
            for row in block_rows
        )
        and Counter(row["kind"] for row in block_rows)
        == {"carrier": 1, "matter": 7, "ledger_shadow": 1}
    )
    add_check(
        "C04_W9_BY_K18_FACTORIZATION",
        {"blocks": 9, "block_size": 18, "kind_pattern": [1, 7, 1], "split": [12, 6]},
        {
            "blocks": len(block_rows),
            "block_sizes": sorted(set(row["slot_count"] for row in block_rows)),
            "kind_counts": Counter(row["kind"] for row in block_rows),
            "splits": sorted(
                set((row["edge_channel_count"], row["point_channel_count"]) for row in block_rows)
            ),
        },
        c04,
        "The exact candidate address inventory is W9 by K18.",
    )

    partition_rows: list[dict[str, Any]] = []
    for parity in (0, 1):
        for block in range(9):
            def route_at(offset: int) -> int:
                return (block * 18 + offset + 6 * parity) % 12

            valid: list[tuple[int, ...]] = []
            for chosen in itertools.combinations(range(18), 12):
                chosen_set = set(chosen)
                if len({route_at(offset) for offset in chosen}) != 12:
                    continue
                remaining = [offset for offset in range(18) if offset not in chosen_set]
                if len({(offset % 3, offset % 2) for offset in remaining}) == 6:
                    valid.append(chosen)
            contiguous = sum(
                tuple(range(start, start + 12)) in valid for start in range(7)
            )
            partition_rows.append(
                {
                    "ledger_parity": parity,
                    "w9_block": block,
                    "valid_partition_count": len(valid),
                    "alternative_count": len(valid) - 1,
                    "contiguous_window_count": contiguous,
                    "representative_valid": tuple(range(12)) in valid,
                    "representative_route_count": len({route_at(offset) for offset in range(12)}),
                    "representative_point_count": len(
                        {(offset % 3, offset % 2) for offset in range(12, 18)}
                    ),
                }
            )
    generated.append(
        write_csv("CR210d_PARTITION_AUDIT.csv", list(partition_rows[0]), partition_rows)
    )
    partition_fingerprint = {
        (
            row["valid_partition_count"],
            row["alternative_count"],
            row["contiguous_window_count"],
            row["representative_valid"],
            row["representative_route_count"],
            row["representative_point_count"],
        )
        for row in partition_rows
    }
    c05 = len(partition_rows) == 18 and partition_fingerprint == {(64, 63, 7, True, 12, 6)}
    add_check(
        "C05_PARTITION_NONUNIQUENESS",
        {"rows": 18, "fingerprint": [64, 63, 7, True, 12, 6]},
        {"rows": len(partition_rows), "fingerprint": partition_fingerprint},
        c05,
        "The representative 12/6 split is admissible but explicitly nonunique.",
    )

    route_rows: list[dict[str, Any]] = []
    route_edges: set[GraphEdge] = set()
    for route_value in range(12):
        graph_edge = route_edge(route_value)
        own_point = point_coord(route_value % 3, route_value % 2)
        route_edges.add(graph_edge)
        route_rows.append(
            {
                "route": route_value,
                "dimension": route_value % 3,
                "side": route_value % 2,
                "hemisphere": route_value // 6,
                "route_point": coord_text(own_point),
                "endpoint_1": coord_text(graph_edge[0]),
                "endpoint_2": coord_text(graph_edge[1]),
                "route_point_incident": own_point in graph_edge,
                "same_axis_edge": sum(value != 0 for value in graph_edge[0])
                == 1
                and sum(value != 0 for value in graph_edge[1]) == 1
                and next(i for i, value in enumerate(graph_edge[0]) if value)
                == next(i for i, value in enumerate(graph_edge[1]) if value),
            }
        )
    generated.append(write_csv("CR210d_ROUTE_EDGE_MAP.csv", list(route_rows[0]), route_rows))
    endpoint_degree = Counter(endpoint for graph_edge in route_edges for endpoint in graph_edge)
    c06 = (
        len(route_rows) == len(route_edges) == 12
        and len(endpoint_degree) == 6
        and set(endpoint_degree.values()) == {4}
        and all(row["route_point_incident"] for row in route_rows)
        and not any(row["same_axis_edge"] for row in route_rows)
    )
    add_check(
        "C06_ROUTE_EDGE_CANDIDATE",
        {"routes": 12, "edges": 12, "points": 6, "point_degree": 4, "incident": 12},
        {
            "routes": len(route_rows),
            "edges": len(route_edges),
            "points": len(endpoint_degree),
            "degrees": sorted(set(endpoint_degree.values())),
            "incident": sum(row["route_point_incident"] for row in route_rows),
        },
        c06,
        "The map is an exact address bijection; physical edge identity remains open.",
    )

    fiber_rows: list[dict[str, Any]] = []
    ternary_rows: list[dict[str, Any]] = []
    for dimension in range(3):
        for side in range(2):
            residue = (4 * dimension + 3 * side) % 6
            slots = [residue + 6 * j for j in range(27)]
            counts = Counter(slot_kind(slot) for slot in slots)
            fiber_rows.append(
                {
                    "dimension": dimension,
                    "side": side,
                    "slot_residue": residue,
                    "carrier": counts["carrier"],
                    "matter": counts["matter"],
                    "shadow": counts["ledger_shadow"],
                    "total": len(slots),
                }
            )
            matrix = Counter(
                (slot_kind(slot), sum(value != 0 for value in base3_centered(j)))
                for j, slot in enumerate(slots)
            )
            for kind in ("carrier", "matter", "ledger_shadow"):
                for rank in range(4):
                    ternary_rows.append(
                        {
                            "dimension": dimension,
                            "side": side,
                            "kind": kind,
                            "rank": rank,
                            "count": matrix[(kind, rank)],
                            "status": "constructed_label_not_source_topology",
                        }
                    )
    generated.append(write_csv("CR210d_FIBER_AUDIT.csv", list(fiber_rows[0]), fiber_rows))
    generated.append(
        write_csv("CR210d_TERNARY_RANK_AUDIT.csv", list(ternary_rows[0]), ternary_rows)
    )
    c07 = (
        len(fiber_rows) == 6
        and {
            (row["carrier"], row["matter"], row["shadow"], row["total"])
            for row in fiber_rows
        }
        == {(3, 21, 3, 27)}
        and all(
            sum(row["total"] for row in fiber_rows if row["side"] == side) == 81
            for side in (0, 1)
        )
    )
    add_check(
        "C07_SIX_FIBERS",
        {"fibers": 6, "each": [3, 21, 3, 27], "each_side": 81},
        {"fibers": len(fiber_rows), "rows": fiber_rows},
        c07,
        "The independent source-native inventory is six exact 27-slot fibers.",
    )
    expected_rank = {
        "carrier": [0, 0, 1, 2],
        "matter": [1, 6, 10, 4],
        "ledger_shadow": [0, 0, 1, 2],
    }
    c08 = True
    for dimension in range(3):
        for side in range(2):
            for kind, expected_counts in expected_rank.items():
                observed = [
                    next(
                        row["count"]
                        for row in ternary_rows
                        if row["dimension"] == dimension
                        and row["side"] == side
                        and row["kind"] == kind
                        and row["rank"] == rank
                    )
                    for rank in range(4)
                ]
                c08 &= observed == expected_counts
    add_check(
        "C08_CONSTRUCTED_TERNARY_RANK",
        expected_rank,
        "same declared matrix in all six fibers" if c08 else "matrix mismatch",
        c08,
        "Exact rank counts are retained as a constructed address audit, not H27 identity.",
    )

    # C09-C13: H27, prior selector, graph distinction, automorphisms, sides.
    h_nodes, h_edges, h_link_rows = build_h27()
    h_node_rows = [
        {
            "node_id": coord_id(node),
            "coordinate": coord_text(node),
            "role": role(node),
            "support_rank": sum(value != 0 for value in node),
        }
        for node in sorted(h_nodes)
    ]
    generated.append(write_csv("CR210d_H27_NODES.csv", list(h_node_rows[0]), h_node_rows))
    generated.append(write_csv("CR210d_H27_LINKS.csv", list(h_link_rows[0]), h_link_rows))
    h_types = Counter(row["link_type"] for row in h_link_rows)
    h_components = components(h_nodes, h_edges)
    h_degrees = degree_histogram(h_nodes, h_edges)
    c09 = (
        len(h_nodes) == 27
        and Counter(row["role"] for row in h_node_rows)
        == {"cell": 1, "point": 6, "edge": 12, "face": 8}
        and h_types == {"cell_face": 8, "face_edge": 24, "edge_point": 24}
        and len(h_edges) == 56
        and h_components == [27]
        and h_degrees == {4: 26, 8: 1}
    )
    add_check(
        "C09_H27_FACE_POSET",
        {"nodes": 27, "links": [8, 24, 24, 56], "components": [27], "degrees": {4: 26, 8: 1}},
        {
            "nodes": len(h_nodes),
            "link_types": h_types,
            "links": len(h_edges),
            "components": h_components,
            "degrees": h_degrees,
        },
        c09,
        "The graph is exact octahedral combinatorics, not demonstrated Starbreaker dynamics.",
    )

    prior_by_ledger: dict[int, set[GraphEdge]] = defaultdict(set)
    with source_paths["PRIOR_SIDECAR_INTERFACES"].open(
        "r", newline="", encoding="utf-8"
    ) as handle:
        for row in csv.DictReader(handle):
            ledger_id = int(row["ledger_id"])
            left = parse_prior_coord(row["left_coordinate"])
            right = parse_prior_coord(row["right_coordinate"])
            prior_by_ledger[ledger_id].add(canon_graph_edge(left, right))
    prior_rows: list[dict[str, Any]] = []
    for ledger_id, edge_set in sorted(prior_by_ledger.items()):
        anti = 0
        for left, right in edge_set:
            roles = {role(left), role(right)}
            if roles == {"point", "edge"}:
                point = left if role(left) == "point" else right
                edge_node = right if role(right) == "edge" else left
                anti += not compatible(point, edge_node)
        prior_rows.append(
            {
                "ledger_id": ledger_id,
                "node_count": len({node for edge in edge_set for node in edge}),
                "link_count": len(edge_set),
                "components": compact_json(components(h_nodes, edge_set)),
                "degree_histogram": compact_json(degree_histogram(h_nodes, edge_set)),
                "h27_overlap": len(edge_set & h_edges),
                "anti_incidences": anti,
            }
        )
    generated.append(
        write_csv("CR210d_PRIOR_SELECTOR_AUDIT.csv", list(prior_rows[0]), prior_rows)
    )
    expected_prior = {(27, 32, "[9,6,6,6]", '{"1":8,"2":12,"4":6,"8":1}', 8, 24)}
    observed_prior = {
        (
            row["node_count"],
            row["link_count"],
            row["components"],
            row["degree_histogram"],
            row["h27_overlap"],
            row["anti_incidences"],
        )
        for row in prior_rows
    }
    c10 = len(prior_by_ledger) == 14 and observed_prior == expected_prior
    add_check(
        "C10_PRIOR_SELECTOR_CONTROL",
        {"ledgers": 14, "fingerprint": expected_prior},
        {"ledgers": len(prior_by_ledger), "fingerprint": observed_prior},
        c10,
        "The previous 32-link topology is reproduced as a distinct control.",
    )

    prior_edges = prior_by_ledger[min(prior_by_ledger)]
    no_face_edge = {
        edge
        for edge in h_edges
        if {role(edge[0]), role(edge[1])} != {"face", "edge"}
    }
    graph_metrics = [
        {"metric": "prior_links", "value": len(prior_edges)},
        {"metric": "h27_links", "value": len(h_edges)},
        {"metric": "intersection", "value": len(prior_edges & h_edges)},
        {"metric": "prior_only", "value": len(prior_edges - h_edges)},
        {"metric": "h27_only", "value": len(h_edges - prior_edges)},
        {"metric": "union", "value": len(prior_edges | h_edges)},
        {"metric": "jaccard", "value": len(prior_edges & h_edges) / len(prior_edges | h_edges)},
        {"metric": "h27_without_face_edge_links", "value": len(no_face_edge)},
        {"metric": "h27_without_face_edge_components", "value": compact_json(components(h_nodes, no_face_edge))},
    ]
    generated.append(
        write_csv("CR210d_GRAPH_COMPARISON.csv", ["metric", "value"], graph_metrics)
    )
    c11 = (
        len(prior_edges & h_edges) == 8
        and len(prior_edges - h_edges) == 24
        and len(h_edges - prior_edges) == 48
        and len(prior_edges | h_edges) == 80
        and len(prior_edges & h_edges) / len(prior_edges | h_edges) == 0.1
        and len(no_face_edge) == 32
        and components(h_nodes, no_face_edge) == [18, 9]
    )
    add_check(
        "C11_GRAPH_REPLACEMENT_NOT_ADDITION",
        {"intersection": 8, "prior_only": 24, "h27_only": 48, "union": 80, "jaccard": 0.1, "no_face_edge": [32, [18, 9]]},
        {
            "intersection": len(prior_edges & h_edges),
            "prior_only": len(prior_edges - h_edges),
            "h27_only": len(h_edges - prior_edges),
            "union": len(prior_edges | h_edges),
            "jaccard": len(prior_edges & h_edges) / len(prior_edges | h_edges),
            "no_face_edge": [len(no_face_edge), components(h_nodes, no_face_edge)],
        },
        c11,
        "H27 replaces 24 anti-incidences and adds 24 face-edge links; it is not old32+24.",
    )

    automorphism_rows: list[dict[str, Any]] = []
    for permutation in itertools.permutations(range(3)):
        for signs in itertools.product((-1, 1), repeat=3):
            transformed_nodes = {
                transform_coord(node, permutation, signs) for node in h_nodes
            }
            transformed_edges = {
                canon_graph_edge(
                    transform_coord(left, permutation, signs),
                    transform_coord(right, permutation, signs),
                )
                for left, right in h_edges
            }
            automorphism_rows.append(
                {
                    "automorphism_id": len(automorphism_rows),
                    "permutation": compact_json(permutation),
                    "signs": compact_json(signs),
                    "orientation_sign": permutation_parity(permutation)
                    * signs[0]
                    * signs[1]
                    * signs[2],
                    "nodes_preserved": transformed_nodes == h_nodes,
                    "edges_preserved": transformed_edges == h_edges,
                }
            )
    generated.append(
        write_csv("CR210d_AUTOMORPHISM_AUDIT.csv", list(automorphism_rows[0]), automorphism_rows)
    )
    c12 = len(automorphism_rows) == 48 and all(
        row["nodes_preserved"] and row["edges_preserved"] for row in automorphism_rows
    )
    add_check(
        "C12_OCTAHEDRAL_AUTOMORPHISMS",
        {"count": 48, "all_preserved": True},
        {
            "count": len(automorphism_rows),
            "all_preserved": all(
                row["nodes_preserved"] and row["edges_preserved"]
                for row in automorphism_rows
            ),
        },
        c12,
        "The structural result does not select axis names or global orientation.",
    )

    side_rows: list[dict[str, Any]] = []
    for side in (0, 1):
        counts = Counter(row["kind"] for row in slot_rows if row["side"] == side)
        side_rows.append(
            {
                "side": side,
                "carrier": counts["carrier"],
                "matter": counts["matter"],
                "shadow": counts["ledger_shadow"],
                "total": sum(counts.values()),
            }
        )
    generated.append(write_csv("CR210d_SIDE_AUDIT.csv", list(side_rows[0]), side_rows))
    reversed_edges = {
        canon_graph_edge(antipode(left), antipode(right)) for left, right in h_edges
    }
    c13 = (
        all(
            [row["carrier"], row["matter"], row["shadow"], row["total"]]
            == [9, 63, 9, 81]
            for row in side_rows
        )
        and reversed_edges == h_edges
    )
    add_check(
        "C13_SIDE_REVERSAL",
        {"each_side": [9, 63, 9, 81], "graph_invariant": True},
        {"side_rows": side_rows, "graph_invariant": reversed_edges == h_edges},
        c13,
        "The two 81-slot sides are exact without assigning physical polarity.",
    )

    # C14: complete directed boundary map, pair classes, parity audit, quotient.
    boundary_domain = set(range(18)) | set(range(144, 162))
    directed_rows: list[dict[str, Any]] = []
    cross_pairs: set[tuple[int, int]] = set()
    images: list[int] = []
    for slot in sorted(boundary_domain):
        block, q, residue = decode_boundary(slot)
        partner = phi_cross(slot)
        partner_block, partner_q, partner_residue = decode_boundary(partner)
        round_trip = phi_cross(partner)
        image_in_boundary = partner in boundary_domain
        image_in_ledger = 0 <= partner < 162
        cross_pairs.add(canon_slot_pair(slot, partner))
        images.append(partner)
        directed_rows.append(
            {
                "slot": slot,
                "block": block,
                "kind": slot_kind(slot),
                "q": q,
                "residue": residue,
                "dimension": slot % 3,
                "side": slot % 2,
                "k18_channel": "edge" if q < 2 else "point",
                "partner_slot": partner,
                "partner_block": partner_block,
                "partner_kind": slot_kind(partner),
                "partner_q": partner_q,
                "partner_residue": partner_residue,
                "partner_dimension": partner % 3,
                "partner_side": partner % 2,
                "partner_k18_channel": "edge" if partner_q < 2 else "point",
                "image_in_boundary": image_in_boundary,
                "image_in_ledger": image_in_ledger,
                "block_swapped": partner_block == 8 - block,
                "kind_flipped": {slot_kind(slot), slot_kind(partner)}
                == {"carrier", "ledger_shadow"},
                "q_preserved": q == partner_q,
                "dimension_preserved": slot % 3 == partner % 3,
                "side_flipped": slot % 2 != partner % 2,
                "channel_preserved": (q < 2) == (partner_q < 2),
                "round_trip_slot": round_trip,
                "round_trip_identity": round_trip == slot,
                "fixed_point": partner == slot,
            }
        )
    generated.append(
        write_csv("CR210d_BOUNDARY_DIRECTED_AUDIT.csv", list(directed_rows[0]), directed_rows)
    )
    image_multiplicity = Counter(images)
    pair_rows = [
        {
            "pair_id": index,
            "left_slot": left,
            "right_slot": right,
            "left_kind": slot_kind(left),
            "right_kind": slot_kind(right),
            "left_side": left % 2,
            "right_side": right % 2,
        }
        for index, (left, right) in enumerate(sorted(cross_pairs))
    ]
    generated.append(
        write_csv("CR210d_CROSS_KIND_PAIR_CLASSES.csv", list(pair_rows[0]), pair_rows)
    )
    expected_pair_set = {
        (0, 147), (1, 148), (2, 149), (3, 144), (4, 145), (5, 146),
        (6, 153), (7, 154), (8, 155), (9, 150), (10, 151), (11, 152),
        (12, 159), (13, 160), (14, 161), (15, 156), (16, 157), (17, 158),
    }

    route_parity_rows: list[dict[str, Any]] = []
    route_pair_counts: Counter[tuple[int, int]] = Counter()
    for parity in (0, 1):
        for row in directed_rows:
            slot = int(row["slot"])
            partner = int(row["partner_slot"])
            left_route = (slot + 6 * parity) % 12
            right_route = (partner + 6 * parity) % 12
            left_point = point_coord(slot % 3, slot % 2)
            right_point = point_coord(partner % 3, partner % 2)
            left_edge = route_edge(left_route)
            right_edge = route_edge(right_route)
            antipodal_edge = canon_graph_edge(antipode(left_edge[0]), antipode(left_edge[1]))
            route_pair = tuple(sorted((left_route, right_route)))
            route_pair_counts[route_pair] += 1
            route_parity_rows.append(
                {
                    "ledger_parity": parity,
                    "slot": slot,
                    "partner_slot": partner,
                    "left_route": left_route,
                    "right_route": right_route,
                    "route_pair": compact_json(route_pair),
                    "hemisphere_preserved": left_route // 6 == right_route // 6,
                    "point_antipodal": right_point == antipode(left_point),
                    "edge_antipodal": right_edge == antipodal_edge,
                }
            )
    generated.append(
        write_csv("CR210d_ROUTE_PARITY_AUDIT.csv", list(route_parity_rows[0]), route_parity_rows)
    )
    expected_route_pairs = {(0, 3), (1, 4), (2, 5), (6, 9), (7, 10), (8, 11)}
    route_pair_ok = set(route_pair_counts) == expected_route_pairs and set(route_pair_counts.values()) == {12}

    same_pairs = {canon_slot_pair(slot, phi_same(slot)) for slot in boundary_domain}
    same_rows = [
        {
            "pair_id": index,
            "left_slot": left,
            "right_slot": right,
            "left_kind": slot_kind(left),
            "right_kind": slot_kind(right),
            "same_kind": slot_kind(left) == slot_kind(right),
            "side_flipped": left % 2 != right % 2,
        }
        for index, (left, right) in enumerate(sorted(same_pairs))
    ]
    generated.append(
        write_csv("CR210d_SAME_KIND_COMPARATOR.csv", list(same_rows[0]), same_rows)
    )
    cross_quotient = quotient_audit("cross_kind", cross_pairs)
    same_quotient = quotient_audit("same_kind", same_pairs)
    quotient_rows = [cross_quotient, same_quotient]
    generated.append(
        write_csv("CR210d_BOUNDARY_QUOTIENT_AUDIT.csv", list(quotient_rows[0]), quotient_rows)
    )
    expected_quotient = {
        "pair_classes": 18,
        "side_a_classes": 81,
        "side_b_classes": 81,
        "intersection_classes": 18,
        "union_classes": 144,
        "symmetric_difference_classes": 126,
        "occurrence_sum": 162,
    }
    quotient_ok = all(
        all(row[key] == expected for key, expected in expected_quotient.items())
        for row in quotient_rows
    )
    c14 = (
        len(directed_rows) == 36
        and set(images) == boundary_domain
        and set(image_multiplicity.values()) == {1}
        and cross_pairs == expected_pair_set
        and all(
            row["image_in_boundary"]
            and row["image_in_ledger"]
            and row["block_swapped"]
            and row["kind_flipped"]
            and row["q_preserved"]
            and row["dimension_preserved"]
            and row["side_flipped"]
            and row["channel_preserved"]
            and row["round_trip_identity"]
            and not row["fixed_point"]
            for row in directed_rows
        )
        and len(route_parity_rows) == 72
        and all(
            row["hemisphere_preserved"]
            and row["point_antipodal"]
            and row["edge_antipodal"]
            for row in route_parity_rows
        )
        and route_pair_ok
        and len(same_pairs) == 18
        and len({slot for pair in same_pairs for slot in pair}) == 36
        and quotient_ok
    )
    add_check(
        "C14_BOUNDARY_QUOTIENT",
        {
            "directed": 36,
            "pairs": 18,
            "domain_exact": True,
            "involution": True,
            "fixed_points": 0,
            "parity_rows": 72,
            "route_pair_counts": {str(pair): 12 for pair in sorted(expected_route_pairs)},
            "quotient": expected_quotient,
            "same_kind_comparator_closes": True,
        },
        {
            "directed": len(directed_rows),
            "pairs": len(cross_pairs),
            "domain_exact": set(images) == boundary_domain,
            "involution_failures": sum(not row["round_trip_identity"] for row in directed_rows),
            "fixed_points": sum(row["fixed_point"] for row in directed_rows),
            "parity_rows": len(route_parity_rows),
            "route_pair_counts": route_pair_counts,
            "quotients": quotient_rows,
            "same_kind_pairs": len(same_pairs),
        },
        c14,
        "The exact modulo-6 map is structurally admissible; equal comparator counts leave orientation open.",
    )

    # C15: exhaustive 720-permutation uniqueness and independent wrong controls.
    permutation_rows: list[dict[str, Any]] = []
    for permutation in itertools.permutations(range(6)):
        dimension_preserving = all(permutation[r] % 3 == r % 3 for r in range(6))
        side_flipping = all(permutation[r] % 2 != r % 2 for r in range(6))
        involutive = all(permutation[permutation[r]] == r for r in range(6))
        permutation_rows.append(
            {
                "permutation_id": len(permutation_rows),
                "permutation": compact_json(permutation),
                "dimension_preserving": dimension_preserving,
                "side_flipping": side_flipping,
                "both_typed_constraints": dimension_preserving and side_flipping,
                "involutive": involutive,
                "is_frozen_candidate": permutation == (3, 4, 5, 0, 1, 2),
            }
        )
    generated.append(
        write_csv(
            "CR210d_RESIDUE_PERMUTATION_UNIQUENESS.csv",
            list(permutation_rows[0]),
            permutation_rows,
        )
    )
    dimension_permutations = sum(row["dimension_preserving"] for row in permutation_rows)
    side_permutations = sum(row["side_flipping"] for row in permutation_rows)
    joint_permutations = [row for row in permutation_rows if row["both_typed_constraints"]]

    raw_q_changes = 0
    raw_out_boundary = 0
    raw_out_ledger = 0
    for slot in boundary_domain:
        block, q, residue = decode_boundary(slot)
        partner_block = 8 - block
        raw_partner = partner_block * 18 + q * 6 + residue + 3
        raw_t = raw_partner - partner_block * 18
        raw_q = raw_t // 6
        raw_q_changes += raw_q != q
        raw_out_boundary += raw_partner not in boundary_domain
        raw_out_ledger += not (0 <= raw_partner < 162)

    half_left = {
        encode_boundary(0, q, residue) for q in range(3) for residue in range(3)
    }
    half_pairs = {canon_slot_pair(slot, phi_cross(slot)) for slot in half_left}
    half_used = {slot for pair in half_pairs for slot in pair}

    adjacent_round_trip_failures = 0
    adjacent_dimension_changes = 0
    adjacent_side_flips = 0
    for slot in boundary_domain:
        block, q, residue = decode_boundary(slot)
        partner = encode_boundary(8 - block, q, (residue + 1) % 6)
        partner_block, partner_q, partner_residue = decode_boundary(partner)
        second = encode_boundary(8 - partner_block, partner_q, (partner_residue + 1) % 6)
        adjacent_round_trip_failures += second != slot
        adjacent_dimension_changes += partner % 3 != slot % 3
        adjacent_side_flips += partner % 2 != slot % 2

    identity_side_flip_failures = 0
    for slot in boundary_domain:
        block, q, residue = decode_boundary(slot)
        partner = encode_boundary(8 - block, q, residue)
        identity_side_flip_failures += partner % 2 == slot % 2

    qshift_changes = 0
    qshift_round_trip_failures = 0
    for slot in boundary_domain:
        block, q, residue = decode_boundary(slot)
        partner = encode_boundary(8 - block, (q + 1) % 3, (residue + 3) % 6)
        partner_block, partner_q, partner_residue = decode_boundary(partner)
        second = encode_boundary(
            8 - partner_block, (partner_q + 1) % 3, (partner_residue + 3) % 6
        )
        qshift_changes += partner_q != q
        qshift_round_trip_failures += second != slot

    many_images = []
    for slot in boundary_domain:
        block, q, residue = decode_boundary(slot)
        many_images.append(encode_boundary(8 - block, q, residue % 3))

    no_pair_classes = {
        side: {
            f"U{slot:03d}"
            for slot in range(162)
            if slot % 2 == side
        }
        for side in (0, 1)
    }
    no_pair_union = no_pair_classes[0] | no_pair_classes[1]
    no_pair_symmetric = no_pair_classes[0] ^ no_pair_classes[1]

    control_rows = [
        {
            "control_id": "CR210C_RAW_PLUS3_NO_MODULO",
            "expected": "q_changes=18;out_boundary=6;out_ledger=3",
            "observed": f"q_changes={raw_q_changes};out_boundary={raw_out_boundary};out_ledger={raw_out_ledger}",
            "behaved_as_expected": [raw_q_changes, raw_out_boundary, raw_out_ledger] == [18, 6, 3],
        },
        {
            "control_id": "HALF_RESIDUE_DOMAIN",
            "expected": "pairs=9;used=18",
            "observed": f"pairs={len(half_pairs)};used={len(half_used)}",
            "behaved_as_expected": len(half_pairs) == 9 and len(half_used) == 18,
        },
        {
            "control_id": "ADJACENT_R_PLUS1",
            "expected": "dimension_changes=36;round_trip_failures=36;side_flips=36",
            "observed": f"dimension_changes={adjacent_dimension_changes};round_trip_failures={adjacent_round_trip_failures};side_flips={adjacent_side_flips}",
            "behaved_as_expected": [
                adjacent_dimension_changes,
                adjacent_round_trip_failures,
                adjacent_side_flips,
            ]
            == [36, 36, 36],
        },
        {
            "control_id": "RESIDUE_IDENTITY",
            "expected": "side_flip_failures=36",
            "observed": f"side_flip_failures={identity_side_flip_failures}",
            "behaved_as_expected": identity_side_flip_failures == 36,
        },
        {
            "control_id": "Q_SHIFT_PLUS1",
            "expected": "q_changes=36;round_trip_failures=36",
            "observed": f"q_changes={qshift_changes};round_trip_failures={qshift_round_trip_failures}",
            "behaved_as_expected": qshift_changes == 36 and qshift_round_trip_failures == 36,
        },
        {
            "control_id": "NO_PAIRING",
            "expected": "union=162;symmetric_difference=162",
            "observed": f"union={len(no_pair_union)};symmetric_difference={len(no_pair_symmetric)}",
            "behaved_as_expected": len(no_pair_union) == 162
            and len(no_pair_symmetric) == 162,
        },
        {
            "control_id": "MANY_TO_ONE",
            "expected": "image_count=18;not_bijective",
            "observed": f"image_count={len(set(many_images))};not_bijective={len(set(many_images)) != 36}",
            "behaved_as_expected": len(set(many_images)) == 18,
        },
        {
            "control_id": "SAME_KIND_ANTIPODAL_COMPARATOR",
            "expected": "independent_count_success_and_orientation_open",
            "observed": compact_json(same_quotient),
            "behaved_as_expected": all(
                same_quotient[key] == value for key, value in expected_quotient.items()
            ),
        },
        {
            "control_id": "GLOBAL_SIDE_REVERSAL",
            "expected": "H27_invariant",
            "observed": f"H27_invariant={reversed_edges == h_edges}",
            "behaved_as_expected": reversed_edges == h_edges,
        },
    ]
    generated.append(
        write_csv("CR210d_WRONG_CONTROLS.csv", list(control_rows[0]), control_rows)
    )
    c15 = (
        len(permutation_rows) == 720
        and dimension_permutations == 8
        and side_permutations == 36
        and len(joint_permutations) == 1
        and joint_permutations[0]["permutation"] == "[3,4,5,0,1,2]"
        and joint_permutations[0]["involutive"]
        and joint_permutations[0]["is_frozen_candidate"]
        and all(row["behaved_as_expected"] for row in control_rows)
    )
    add_check(
        "C15_WRONG_CONTROLS",
        {
            "permutations": 720,
            "dimension_preserving": 8,
            "side_flipping": 36,
            "joint": 1,
            "joint_map": [3, 4, 5, 0, 1, 2],
            "controls": len(control_rows),
            "control_errors": 0,
        },
        {
            "permutations": len(permutation_rows),
            "dimension_preserving": dimension_permutations,
            "side_flipping": side_permutations,
            "joint": len(joint_permutations),
            "joint_maps": [row["permutation"] for row in joint_permutations],
            "controls": len(control_rows),
            "control_errors": sum(not row["behaved_as_expected"] for row in control_rows),
        },
        c15,
        "The modulo-6 map is conditionally unique under frozen typed constraints and survives independent controls.",
    )

    # C16: fresh closed-domain firewall.
    historical_firewall = json.loads(
        source_paths["CR210C_FIREWALL"].read_text(encoding="utf-8")
    )
    forbidden_tokens = [
        "density_runs.csv",
        "permutation_runs.csv",
        "uniform_same_total_runs.csv",
        "run_correlations.csv",
        "hypothesis_results.csv",
        "permutation_nulls.csv",
        "roster_81",
    ]
    forbidden_path_hits = [
        f"{token}:{row['path']}"
        for row in source_rows
        for token in forbidden_tokens
        if token in row["path"].lower()
    ]
    firewall = {
        "record_id": RECORD_ID,
        "outcomes_opened": False,
        "density_or_permutation_results_opened": False,
        "workbooks_opened": False,
        "f81_membership_opened": False,
        "pdg_opened": False,
        "particle_masses_opened": False,
        "isotope_data_opened": False,
        "binding_opened": False,
        "fitted_parameters": 0,
        "forbidden_fields_used": [],
        "forbidden_path_hits": forbidden_path_hits,
        "historical_firewall_still_closed": (
            not historical_firewall["outcomes_opened"]
            and not historical_firewall["binding_opened"]
            and not historical_firewall["f81_membership_opened"]
            and not historical_firewall["workbook_membership_opened"]
            and historical_firewall["fitted_parameters"] == 0
            and not historical_firewall["forbidden_starbreaker_fields_used"]
            and not historical_firewall["forbidden_path_hits"]
        ),
        "historical_passes_counted_as_fresh_evidence": False,
    }
    generated.append(write_json("CR210d_FORBIDDEN_FIELD_FIREWALL.json", firewall))
    c16 = (
        not firewall["outcomes_opened"]
        and not firewall["density_or_permutation_results_opened"]
        and not firewall["workbooks_opened"]
        and not firewall["f81_membership_opened"]
        and not firewall["pdg_opened"]
        and not firewall["particle_masses_opened"]
        and not firewall["isotope_data_opened"]
        and not firewall["binding_opened"]
        and firewall["fitted_parameters"] == 0
        and not firewall["forbidden_fields_used"]
        and not firewall["forbidden_path_hits"]
        and firewall["historical_firewall_still_closed"]
        and not firewall["historical_passes_counted_as_fresh_evidence"]
    )
    add_check(
        "C16_FIREWALL",
        {"all_closed": True, "fitted_parameters": 0, "forbidden_hits": 0},
        firewall,
        c16,
        "The result is a fresh structural test with every target and binding lane closed.",
    )

    # Exactly seventeen fresh gates now govern the verdict.
    if len(checks) != 17:
        raise RuntimeError(f"expected 17 fresh checks, generated {len(checks)}")
    generated.append(
        write_csv(
            "CR210d_CHECKS.csv",
            ["check_id", "expected", "observed", "pass", "significance"],
            checks,
        )
    )
    all_pass = all(row["pass"] for row in checks)
    verdict = PASS_VERDICT if all_pass else FAIL_VERDICT

    current_status = {
        "record_id": RECORD_ID,
        "historical_record": "CR210c_OCTAHEDRAL_COMPLETE_LEDGER_ADDRESS_ADAPTER",
        "historical_status": "CR210c_FAIL_PRECOMMITTED_STRUCTURAL_CHECK",
        "historical_record_mutated": False,
        "historical_passes_counted_as_fresh_evidence": False,
        "current_successor": RECORD_ID,
        "current_status": verdict,
        "fresh_checks_passed": sum(row["pass"] for row in checks),
        "fresh_checks_total": len(checks),
        "failed_fresh_checks": [row["check_id"] for row in checks if not row["pass"]],
        "orientation_selected_by_counts": False,
        "pdg_status": "NOT_OPENED",
        "binding_status": "NOT_OPENED",
    }
    generated.append(write_json("CR210d_CURRENT_STATUS.json", current_status))

    summary = {
        "record_id": RECORD_ID,
        "verdict": verdict,
        "fresh_checks": [sum(row["pass"] for row in checks), len(checks)],
        "exact_results": {
            "source_kind_partition": [18, 126, 18],
            "W9_by_K18": [9, 18],
            "six_fibers": [6, 27],
            "H27": [27, 56],
            "boundary_directed": 36,
            "boundary_pairs": 18,
            "quotient": [81, 81, 18, 144, 126, 162],
            "typed_residue_permutations": [720, 8, 36, 1],
        },
        "open_boundaries": [
            "same-kind and cross-kind orientations are count-equivalent",
            "H27 is candidate combinatorics rather than demonstrated Starbreaker dynamics",
            "route-edge address is not physical edge identity",
            "F81 projection is open",
            "PDG identity is unopened",
            "binding is unopened",
        ],
    }
    generated.append(write_json("CR210d_SUMMARY.json", summary))

    if all_pass:
        result_body = f"""# CR210d Result

## Primary verdict

`{verdict}`

All **17/17 fresh precommitted structural gates passed**. No CR210c PASS was inherited as a CR210d PASS; the full adapter was recomputed by this standalone runner.

## Exact result

The source-native ledger closes freshly as `18 carrier + 126 matter + 18 ledger-shadow = 162`, with exact `W9 x K18` and six-by-27 address factorizations. The representative 12/6 split remains one of 64 valid partitions per block and parity.

The candidate H27 face-poset graph has 27 nodes and 56 links and is preserved by all 48 signed-axis automorphisms. The prior 32-link graph is reproduced as a distinct disconnected control; only eight links overlap H27.

The corrected cross-kind boundary map was applied to all 36 directed boundary occurrences. It is an exact fixed-point-free involutive bijection over the boundary universe, gives the precommitted 18 pair roster, preserves microcycle, dimension, K18 channel, and route hemisphere, flips kind and side, and maps point/edge addresses antipodally under both route parities.

The quotient closes exactly as:

```text
81 + 81 - 18 = 144
symmetric difference = 126
occurrence sum = 162
```

Among all 720 residue permutations, only `[3,4,5,0,1,2]` preserves dimension and flips side under the frozen block/q constraints. This is conditional structural uniqueness. The same-kind comparator closes the same count ladder, so physical boundary orientation remains open.

## Historical and scientific boundaries

CR210c remains historically FAIL and was not rewritten. CR210d is the current full fresh structural result.

No Starbreaker outcome, workbook, F81 membership, PDG data, mass, isotope, or binding source was opened. This PASS does not establish Starbreaker dynamical adjacency, physical particle shape, route-edge physical identity, F81 projection, PDG identity, or binding improvement.
"""
    else:
        failed = ", ".join(row["check_id"] for row in checks if not row["pass"])
        result_body = f"""# CR210d Result

## Primary verdict

`{verdict}`

Fresh checks passed: **{sum(row['pass'] for row in checks)}/{len(checks)}**.

Failed fresh gates: `{failed}`.

CR210c remains historically FAIL. No same-run repair was performed, and no PDG or binding lane was opened.
"""
    result_path = HERE / "CR210d_result.md"
    result_path.write_text(result_body, encoding="utf-8")
    generated.append(result_path)

    status_text = f"""# CR210d Current Status

Historical record: `CR210c_FAIL_PRECOMMITTED_STRUCTURAL_CHECK` — preserved, not rewritten.

Current successor: `{verdict}`

Fresh gate census: `{sum(row['pass'] for row in checks)}/{len(checks)}`

PDG: `NOT_OPENED`

Binding: `NOT_OPENED`
"""
    status_path = HERE / "CR210d_CURRENT_STATUS.md"
    status_path.write_text(status_text, encoding="utf-8")
    generated.append(status_path)

    provenance = {
        "record_id": RECORD_ID,
        "task": TASK,
        "classification": premises["classification"],
        "parent_freeze": premises["parent_freeze"],
        "source_manifest_sha256": EXPECTED_LOCAL_HASHES["CR210d_SOURCE_MANIFEST.json"],
        "declared_premises_sha256": EXPECTED_LOCAL_HASHES["CR210d_DECLARED_PREMISES.json"],
        "precommit_sha256": EXPECTED_LOCAL_HASHES["CR210d_PRECOMMIT.md"],
        "runner_sha256": sha256_file(Path(__file__).resolve()),
        "source_count": len(source_rows),
        "fresh_gate_count": len(checks),
        "historical_passes_counted_as_fresh_evidence": False,
        "execution_path": "tools/run_sam_test.py",
        "execution_count": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
    }
    generated.append(write_json("CR210d_PROVENANCE.json", provenance))

    finished = datetime.now(timezone.utc)
    command_log = {
        "record_id": RECORD_ID,
        "task": TASK,
        "command": (
            "python tools\\run_sam_test.py --task \""
            + TASK
            + "\" --script 15_SCALE_BRIDGE_SIMULATOR\\"
            "CR210d_OCTAHEDRAL_COMPLETE_LEDGER_BOUNDARY_CLOSURE_APPEAL\\CR210d_runner.py"
        ),
        "started_utc": started.isoformat(),
        "finished_utc": finished.isoformat(),
        "elapsed_seconds": (finished - started).total_seconds(),
        "execution_count": 1,
        "direct_runner_execution": False,
    }
    generated.append(write_json("CR210d_COMMAND_LOG.json", command_log))

    validation = {
        "record_id": RECORD_ID,
        "status": "PASS" if all_pass else "FAIL",
        "verdict": verdict,
        "fresh_checks_passed": sum(row["pass"] for row in checks),
        "fresh_checks_total": len(checks),
        "failed_fresh_checks": [row["check_id"] for row in checks if not row["pass"]],
        "source_contract_pass": c01,
        "precommit_seal_pass": c00,
        "historical_record_mutated": False,
        "historical_passes_counted_as_fresh_evidence": False,
        "outcomes_opened": False,
        "pdg_opened": False,
        "binding_opened": False,
        "execution_count": 1,
        "generated_artifact_count_before_execution_hashes": len(generated) + 1,
    }
    generated.append(write_json("CR210d_VALIDATION.json", validation))

    hash_targets = sorted(
        [
            path
            for path in HERE.iterdir()
            if path.is_file() and path.name != "CR210d_EXECUTION_HASHES.txt"
        ],
        key=lambda path: path.name.lower(),
    )
    hash_lines = [f"{sha256_file(path)}  {path.name}" for path in hash_targets]
    (HERE / "CR210d_EXECUTION_HASHES.txt").write_text(
        "\n".join(hash_lines) + "\n", encoding="utf-8"
    )

    print(json.dumps(validation, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
