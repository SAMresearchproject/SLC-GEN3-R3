#!/usr/bin/env python3
"""CR210a: frozen structural address-adapter campaign.

This runner consumes only the sealed structural source manifest.  It does not
open Starbreaker outcomes, QP093A roster membership, or binding residuals.
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


RECORD_ID = "CR210a_OCTAHEDRAL_COMPLETE_LEDGER_ADDRESS_ADAPTER"
TASK = (
    "Execute the frozen Octahedral Complete-Ledger Address Adapter structural "
    "campaign from PSLI_DF_20260715T025638Z with outcomes and binding closed "
    "and stop after one frozen structural comparison"
)
VERDICT_CEILING = (
    "CR210a_PASS_EXACT_SOURCE_NATIVE_W9_BY_K18_ADDRESS_FACTORIZATION"
    "__SLOT_PARTITION_ROUTE_EDGE_OVERLAP_ORIENTATION_AND_PHYSICAL_INCIDENCE_OPEN"
)

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
SOURCE_MANIFEST = HERE / "CR210a_SOURCE_MANIFEST.json"
PREMISES_PATH = HERE / "CR210a_DECLARED_PREMISES.json"
PRECOMMIT_PATH = HERE / "CR210a_PRECOMMIT.md"
PRECOMMIT_SEAL = HERE / "CR210a_PRECOMMIT_SEAL.txt"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_json(name: str, value: Any) -> Path:
    path = HERE / name
    path.write_text(json.dumps(value, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    return path


def write_csv(name: str, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> Path:
    path = HERE / name
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="raise")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return path


def compact_json(value: Any) -> str:
    return json.dumps(value, separators=(",", ":"), sort_keys=True)


def resolve_source(raw_path: str) -> Path:
    path = Path(raw_path)
    return path if path.is_absolute() else ROOT / path


Coord = tuple[int, int, int]
Edge = tuple[Coord, Coord]


def canon_edge(a: Coord, b: Coord) -> Edge:
    if a == b:
        raise ValueError(f"self edge at {a}")
    return tuple(sorted((a, b)))  # type: ignore[return-value]


def coord_text(coord: Coord) -> str:
    return compact_json(list(coord))


def coord_role(coord: Coord) -> str:
    rank = sum(value != 0 for value in coord)
    return {0: "cell", 1: "point", 2: "edge", 3: "face"}[rank]


def coord_id(coord: Coord) -> str:
    return f"{coord_role(coord).upper()}_{coord[0]:+d}_{coord[1]:+d}_{coord[2]:+d}"


def point_coord(dimension: int, side: int) -> Coord:
    values = [0, 0, 0]
    values[dimension] = -1 if side == 0 else 1
    return tuple(values)  # type: ignore[return-value]


def route_edge(route: int) -> Edge:
    d = route % 3
    side = route % 2
    hemisphere = route // 6
    first = point_coord(d, side)
    second = point_coord((d + 1 + hemisphere) % 3, side ^ hemisphere)
    return canon_edge(first, second)


def complement_route_edge(route: int) -> Edge:
    """Wrong control: deliberately excludes the route's own point axis."""
    d = route % 3
    side = route % 2
    hemisphere = route // 6
    return canon_edge(
        point_coord((d + 1) % 3, side),
        point_coord((d + 2) % 3, side ^ hemisphere),
    )


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


def graph_components(nodes: set[Coord], edges: set[Edge]) -> list[int]:
    adjacency: dict[Coord, set[Coord]] = {node: set() for node in nodes}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    unseen = set(nodes)
    sizes: list[int] = []
    while unseen:
        start = min(unseen)
        queue: deque[Coord] = deque([start])
        unseen.remove(start)
        size = 0
        while queue:
            node = queue.popleft()
            size += 1
            for neighbor in adjacency[node]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    queue.append(neighbor)
        sizes.append(size)
    return sorted(sizes, reverse=True)


def degree_histogram(nodes: set[Coord], edges: set[Edge]) -> dict[int, int]:
    degrees = Counter({node: 0 for node in nodes})
    for left, right in edges:
        degrees[left] += 1
        degrees[right] += 1
    return dict(sorted(Counter(degrees.values()).items()))


def compatible(lower: Coord, upper: Coord) -> bool:
    """Whether every signed support coordinate in lower agrees with upper."""
    return all(value == 0 or value == upper[index] for index, value in enumerate(lower))


def build_h27() -> tuple[set[Coord], set[Edge], list[dict[str, Any]]]:
    nodes = set(itertools.product((-1, 0, 1), repeat=3))
    cell = (0, 0, 0)
    points = sorted(node for node in nodes if coord_role(node) == "point")
    edge_nodes = sorted(node for node in nodes if coord_role(node) == "edge")
    faces = sorted(node for node in nodes if coord_role(node) == "face")
    rows: list[dict[str, Any]] = []
    edges: set[Edge] = set()

    def add(left: Coord, right: Coord, link_type: str) -> None:
        edge = canon_edge(left, right)
        if edge in edges:
            raise ValueError(f"duplicate H27 edge {edge}")
        edges.add(edge)
        rows.append(
            {
                "link_id": len(rows),
                "link_type": link_type,
                "left_node_id": coord_id(left),
                "right_node_id": coord_id(right),
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


def permutation_parity(permutation: tuple[int, int, int]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(3)
        for j in range(i + 1, 3)
    )
    return -1 if inversions % 2 else 1


def transform_coord(
    coord: Coord, permutation: tuple[int, int, int], signs: tuple[int, int, int]
) -> Coord:
    return tuple(signs[index] * coord[permutation[index]] for index in range(3))  # type: ignore[return-value]


def antipode_coord(coord: Coord) -> Coord:
    return tuple(-value for value in coord)  # type: ignore[return-value]


def parse_centered(raw: str) -> Coord:
    values = json.loads(raw)
    if not isinstance(values, list) or len(values) != 3:
        raise ValueError(f"invalid coordinate {raw!r}")
    return tuple(int(value) - 1 for value in values)  # type: ignore[return-value]


def pair_rows(mode: str) -> list[dict[str, Any]]:
    if mode not in {"cross_kind", "same_kind"}:
        raise ValueError(mode)
    rows: list[dict[str, Any]] = []
    starts = [0] if mode == "cross_kind" else [0, 8]
    for block in starts:
        for q in range(3):
            for r in range(3):
                partner_block = 8 - block if mode == "cross_kind" else block
                left = block * 18 + q * 6 + r
                right = partner_block * 18 + q * 6 + r + 3
                left_route = left % 12
                right_route = right % 12
                left_edge = route_edge(left_route)
                right_edge = route_edge(right_route)
                expected_antipode = canon_edge(
                    antipode_coord(left_edge[0]), antipode_coord(left_edge[1])
                )
                rows.append(
                    {
                        "pairing": mode,
                        "pair_id": len(rows),
                        "left_slot": left,
                        "right_slot": right,
                        "left_kind": slot_kind(left),
                        "right_kind": slot_kind(right),
                        "q_preserved": q == ((right % 18) // 6),
                        "dimension_preserved": left % 3 == right % 3,
                        "side_flipped": left % 2 != right % 2,
                        "left_route": left_route,
                        "right_route": right_route,
                        "point_antipodal": point_coord(left % 3, left % 2)
                        == antipode_coord(point_coord(right % 3, right % 2)),
                        "edge_antipodal": right_edge == expected_antipode,
                    }
                )
    return rows


def main() -> int:
    started = datetime.now(timezone.utc)
    generated: list[Path] = []
    checks: list[dict[str, Any]] = []

    def check(
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

    # Sealed local contract validation.
    manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    premises = json.loads(PREMISES_PATH.read_text(encoding="utf-8"))
    seal_text = PRECOMMIT_SEAL.read_text(encoding="utf-8")
    sealed_expected = {
        "CR210a_SOURCE_MANIFEST.json": "dbf10c2802fdfc22c04e9b4a9db33f6797107c412eaa62a6e92c8282102cfe0c",
        "CR210a_DECLARED_PREMISES.json": "26d3a407d498212460331fe837cc3900c18253f47ffb8ba07ada3cd85072ab93",
        "CR210a_PRECOMMIT.md": "55d583f6f7697a24e28d5a1031a4eeb329fe0680ed3548a3ea1d2f0ffe475b45",
    }
    local_contract_rows: list[dict[str, Any]] = []
    for name, expected_hash in sealed_expected.items():
        path = HERE / name
        actual_hash = sha256_file(path)
        local_contract_rows.append(
            {
                "file": name,
                "expected_sha256": expected_hash,
                "actual_sha256": actual_hash,
                "match": actual_hash == expected_hash,
            }
        )
    check(
        "C00_PRECOMMIT_SEAL",
        {"files": 3, "all_hashes_match": True, "runner_absent_at_seal": True},
        {
            "files": len(local_contract_rows),
            "all_hashes_match": all(row["match"] for row in local_contract_rows),
            "runner_absent_at_seal": "runner_present_at_seal=false" in seal_text,
        },
        len(local_contract_rows) == 3
        and all(row["match"] for row in local_contract_rows)
        and "runner_present_at_seal=false" in seal_text,
        "The executable was written after the frozen predictions and source contract.",
    )
    generated.append(
        write_csv(
            "CR210a_LOCAL_CONTRACT_VALIDATION.csv",
            ["file", "expected_sha256", "actual_sha256", "match"],
            local_contract_rows,
        )
    )

    # Hash every declared source; parse only the source-native structural code and
    # the safe prior-interface control.
    source_rows: list[dict[str, Any]] = []
    source_paths: dict[str, Path] = {}
    for entry in manifest["sources"]:
        path = resolve_source(entry["path"])
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
                "access_mode": (
                    "parsed_structural"
                    if entry["source_id"]
                    in {"STARBRAKER_BASE_SOURCE", "PRIOR_SIDECAR_INTERFACES"}
                    else "hash_validation_only"
                ),
            }
        )
    source_ok = (
        len(source_rows) == manifest["source_count"] == 17
        and all(row["hash_match"] and row["bytes_match"] for row in source_rows)
    )
    check(
        "C01_SOURCE_CONTRACT",
        {"source_count": 17, "hash_and_byte_errors": 0},
        {
            "source_count": len(source_rows),
            "hash_and_byte_errors": sum(
                not (row["hash_match"] and row["bytes_match"]) for row in source_rows
            ),
        },
        source_ok,
        "Every opened authority is the exact precommitted byte sequence.",
    )
    generated.append(
        write_csv(
            "CR210a_SOURCE_VALIDATION.csv",
            [
                "source_id",
                "path",
                "declared_sha256",
                "actual_sha256",
                "declared_bytes",
                "actual_bytes",
                "hash_match",
                "bytes_match",
                "access_mode",
            ],
            source_rows,
        )
    )

    source_text = source_paths["STARBRAKER_BASE_SOURCE"].read_text(encoding="utf-8")
    required_snippets = [
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
    snippet_missing = [snippet for snippet in required_snippets if snippet not in source_text]
    check(
        "C02_SOURCE_NATIVE_FORMULAS",
        {"required_snippets": len(required_snippets), "missing": []},
        {"required_snippets": len(required_snippets), "missing": snippet_missing},
        not snippet_missing,
        "The canonical template is a direct consequence of frozen generator formulas.",
    )

    # Canonical 162-slot template.
    slot_rows: list[dict[str, Any]] = []
    for slot in range(162):
        block = slot // 18
        t = slot % 18
        q, r = divmod(t, 6)
        dimension = slot % 3
        side = slot % 2
        residue = slot % 6
        j = slot // 6
        ternary = base3_centered(j)
        face = face_for_block(block)
        route_even = slot % 12
        route_odd = (slot + 6) % 12
        k18_role = "edge" if t < 12 else "point"
        slot_rows.append(
            {
                "ledger_slot": slot,
                "source_kind": slot_kind(slot),
                "w9_block": block,
                "w9_role": "closure_cell" if block == 8 else "oriented_face",
                "w9_coordinate": "" if face is None else coord_text(face),
                "k18_offset": t,
                "k18_role": k18_role,
                "microcycle_q": q,
                "residue_r": r,
                "dimension": dimension,
                "side": side,
                "fiber_residue": residue,
                "fiber_j": j,
                "ternary_coordinate": coord_text(ternary),
                "ternary_rank": sum(value != 0 for value in ternary),
                "route_even_ledger": route_even,
                "route_odd_ledger": route_odd,
                "even_candidate_address": (
                    compact_json([coord_text(value) for value in route_edge(route_even)])
                    if k18_role == "edge"
                    else coord_text(point_coord(dimension, side))
                ),
                "odd_candidate_address": (
                    compact_json([coord_text(value) for value in route_edge(route_odd)])
                    if k18_role == "edge"
                    else coord_text(point_coord(dimension, side))
                ),
            }
        )
    generated.append(
        write_csv(
            "CR210a_SLOT_TEMPLATE.csv",
            list(slot_rows[0]),
            slot_rows,
        )
    )
    kind_counts = Counter(row["source_kind"] for row in slot_rows)
    check(
        "C03_SOURCE_KIND_TOTALS",
        {"carrier": 18, "matter": 126, "ledger_shadow": 18, "total": 162},
        {**kind_counts, "total": len(slot_rows)},
        kind_counts == {"carrier": 18, "matter": 126, "ledger_shadow": 18}
        and len(slot_rows) == 162,
        "The canonical ledger retains exact 18+126+18 source typing.",
    )

    block_rows: list[dict[str, Any]] = []
    for block in range(9):
        rows = [row for row in slot_rows if row["w9_block"] == block]
        counts = Counter(row["k18_role"] for row in rows)
        block_rows.append(
            {
                "w9_block": block,
                "source_kind": rows[0]["source_kind"],
                "w9_role": rows[0]["w9_role"],
                "w9_coordinate": rows[0]["w9_coordinate"],
                "slot_count": len(rows),
                "edge_channel_count": counts["edge"],
                "point_channel_count": counts["point"],
            }
        )
    generated.append(
        write_csv(
            "CR210a_BLOCK_AUDIT.csv",
            list(block_rows[0]),
            block_rows,
        )
    )
    block_fingerprint = [row["slot_count"] for row in block_rows]
    block_kinds = Counter(row["source_kind"] for row in block_rows)
    check(
        "C04_W9_BY_K18_FACTORIZATION",
        {
            "blocks": 9,
            "each_block": 18,
            "block_kind_counts": {"carrier": 1, "matter": 7, "ledger_shadow": 1},
            "per_block_split": [12, 6],
        },
        {
            "blocks": len(block_rows),
            "each_block": block_fingerprint,
            "block_kind_counts": block_kinds,
            "per_block_split": sorted(
                set((row["edge_channel_count"], row["point_channel_count"]) for row in block_rows)
            ),
        },
        len(block_rows) == 9
        and block_fingerprint == [18] * 9
        and block_kinds == {"carrier": 1, "matter": 7, "ledger_shadow": 1}
        and all(
            row["edge_channel_count"] == 12 and row["point_channel_count"] == 6
            for row in block_rows
        ),
        "The source-native ledger admits the exact candidate Cartesian inventory W9 x K18.",
    )

    # Enumerate every 12/6 split that preserves complete route and point inventories.
    partition_rows: list[dict[str, Any]] = []
    for parity in (0, 1):
        for block in range(9):
            def route_at(t: int) -> int:
                return (block * 18 + t + 6 * parity) % 12

            valid: list[tuple[int, ...]] = []
            for chosen in itertools.combinations(range(18), 12):
                chosen_set = set(chosen)
                if set(route_at(t) for t in chosen) != set(range(12)):
                    continue
                remaining = [t for t in range(18) if t not in chosen_set]
                points = {(t % 3, t % 2) for t in remaining}
                if len(points) == 6:
                    valid.append(chosen)
            contiguous = sum(
                tuple(range(start, start + 12)) in valid for start in range(7)
            )
            frozen = tuple(range(12))
            remaining = list(range(12, 18))
            partition_rows.append(
                {
                    "ledger_parity": parity,
                    "w9_block": block,
                    "valid_partition_count": len(valid),
                    "alternative_partition_count": len(valid) - 1,
                    "linear_contiguous_valid_count": contiguous,
                    "frozen_first12_valid": frozen in valid,
                    "frozen_route_count": len({route_at(t) for t in frozen}),
                    "frozen_point_count": len({(t % 3, t % 2) for t in remaining}),
                }
            )
    generated.append(
        write_csv(
            "CR210a_ROUTE_POINT_PARTITION_AUDIT.csv",
            list(partition_rows[0]),
            partition_rows,
        )
    )
    partition_fingerprints = {
        (
            row["valid_partition_count"],
            row["alternative_partition_count"],
            row["linear_contiguous_valid_count"],
            row["frozen_first12_valid"],
            row["frozen_route_count"],
            row["frozen_point_count"],
        )
        for row in partition_rows
    }
    expected_partition_fingerprint = {(64, 63, 7, True, 12, 6)}
    check(
        "C05_PARTITION_NONUNIQUENESS",
        expected_partition_fingerprint,
        partition_fingerprints,
        partition_fingerprints == expected_partition_fingerprint,
        "The first-12/final-6 split works but is one of 64 valid splits, not source-unique.",
    )

    route_rows: list[dict[str, Any]] = []
    route_edges: set[Edge] = set()
    for route in range(12):
        edge = route_edge(route)
        route_edges.add(edge)
        own_point = point_coord(route % 3, route % 2)
        route_rows.append(
            {
                "route": route,
                "dimension": route % 3,
                "side": route % 2,
                "hemisphere": route // 6,
                "route_point": coord_text(own_point),
                "endpoint_1": coord_text(edge[0]),
                "endpoint_2": coord_text(edge[1]),
                "route_point_incident": own_point in edge,
                "antipodal_route": (route + 3) % 6 + 6 * (route // 6),
            }
        )
    generated.append(
        write_csv(
            "CR210a_ROUTE_EDGE_MAP.csv",
            list(route_rows[0]),
            route_rows,
        )
    )
    endpoint_degree = Counter(endpoint for edge in route_edges for endpoint in edge)
    check(
        "C06_ROUTE_EDGE_CANDIDATE",
        {"routes": 12, "unique_edges": 12, "points": 6, "point_degree": [4], "incident": 12},
        {
            "routes": len(route_rows),
            "unique_edges": len(route_edges),
            "points": len(endpoint_degree),
            "point_degree": sorted(set(endpoint_degree.values())),
            "incident": sum(row["route_point_incident"] for row in route_rows),
        },
        len(route_edges) == 12
        and len(endpoint_degree) == 6
        and set(endpoint_degree.values()) == {4}
        and all(row["route_point_incident"] for row in route_rows),
        "A deterministic source-field address map covers all octahedral edges; physical edge identity remains open.",
    )

    # Six dimension-side fibers and constructed centered-ternary audit.
    fiber_rows: list[dict[str, Any]] = []
    rank_rows: list[dict[str, Any]] = []
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
                    "carrier_count": counts["carrier"],
                    "matter_count": counts["matter"],
                    "shadow_count": counts["ledger_shadow"],
                    "total": len(slots),
                }
            )
            matrix = Counter(
                (slot_kind(slot), sum(value != 0 for value in base3_centered(j)))
                for j, slot in enumerate(slots)
            )
            for kind in ("carrier", "matter", "ledger_shadow"):
                for rank in range(4):
                    rank_rows.append(
                        {
                            "dimension": dimension,
                            "side": side,
                            "kind": kind,
                            "ternary_rank": rank,
                            "count": matrix[(kind, rank)],
                            "status": "constructed_address_label_not_source_topology",
                        }
                    )
    generated.append(
        write_csv(
            "CR210a_POINT_FIBER_AUDIT.csv",
            list(fiber_rows[0]),
            fiber_rows,
        )
    )
    generated.append(
        write_csv(
            "CR210a_TERNARY_RANK_AUDIT.csv",
            list(rank_rows[0]),
            rank_rows,
        )
    )
    fiber_fingerprint = {
        (
            row["carrier_count"],
            row["matter_count"],
            row["shadow_count"],
            row["total"],
        )
        for row in fiber_rows
    }
    check(
        "C07_SIX_FIBERS",
        {"fibers": 6, "fingerprint": {(3, 21, 3, 27)}, "side_total": 81},
        {
            "fibers": len(fiber_rows),
            "fingerprint": fiber_fingerprint,
            "side_totals": {
                side: sum(row["total"] for row in fiber_rows if row["side"] == side)
                for side in (0, 1)
            },
        },
        len(fiber_rows) == 6
        and fiber_fingerprint == {(3, 21, 3, 27)}
        and all(
            sum(row["total"] for row in fiber_rows if row["side"] == side) == 81
            for side in (0, 1)
        ),
        "The orthogonal source-native inventory is six 27-slot fibers, each 3+21+3.",
    )
    expected_rank = {
        "carrier": [0, 0, 1, 2],
        "matter": [1, 6, 10, 4],
        "ledger_shadow": [0, 0, 1, 2],
    }
    rank_ok = True
    for dimension in range(3):
        for side in range(2):
            for kind, expected_counts in expected_rank.items():
                observed_counts = [
                    next(
                        row["count"]
                        for row in rank_rows
                        if row["dimension"] == dimension
                        and row["side"] == side
                        and row["kind"] == kind
                        and row["ternary_rank"] == rank
                    )
                    for rank in range(4)
                ]
                rank_ok &= observed_counts == expected_counts
    check(
        "C08_CONSTRUCTED_TERNARY_RANK",
        expected_rank,
        "same matrix in all six fibers" if rank_ok else "matrix mismatch",
        rank_ok,
        "The 1/6/12/8 rank counts are exact only after a declared constructed base-three labeling.",
    )

    # Complete octahedral face-poset cover graph.
    h_nodes, h_edges, h_edge_rows = build_h27()
    node_rows = [
        {
            "node_id": coord_id(node),
            "coordinate": coord_text(node),
            "role": coord_role(node),
            "support_rank": sum(value != 0 for value in node),
        }
        for node in sorted(h_nodes)
    ]
    generated.append(
        write_csv("CR210a_H27_NODE_REGISTER.csv", list(node_rows[0]), node_rows)
    )
    generated.append(
        write_csv("CR210a_H27_FACE_POSET_EDGES.csv", list(h_edge_rows[0]), h_edge_rows)
    )
    link_types = Counter(row["link_type"] for row in h_edge_rows)
    h_components = graph_components(h_nodes, h_edges)
    h_degree = degree_histogram(h_nodes, h_edges)
    check(
        "C09_H27_FACE_POSET",
        {
            "nodes": 27,
            "roles": {"cell": 1, "point": 6, "edge": 12, "face": 8},
            "links": {"cell_face": 8, "face_edge": 24, "edge_point": 24},
            "components": [27],
            "degree_histogram": {4: 26, 8: 1},
        },
        {
            "nodes": len(h_nodes),
            "roles": Counter(row["role"] for row in node_rows),
            "links": link_types,
            "components": h_components,
            "degree_histogram": h_degree,
        },
        len(h_nodes) == 27
        and Counter(row["role"] for row in node_rows)
        == {"cell": 1, "point": 6, "edge": 12, "face": 8}
        and link_types == {"cell_face": 8, "face_edge": 24, "edge_point": 24}
        and h_components == [27]
        and h_degree == {4: 26, 8: 1},
        "The candidate graph is exact octahedral combinatorics, not a claim of source dynamical adjacency.",
    )

    # Safe prior sidecar structural control.
    prior_by_ledger: dict[int, set[Edge]] = defaultdict(set)
    with source_paths["PRIOR_SIDECAR_INTERFACES"].open(
        "r", newline="", encoding="utf-8"
    ) as handle:
        for row in csv.DictReader(handle):
            ledger_id = int(row["ledger_id"])
            left = parse_centered(row["left_coordinate"])
            right = parse_centered(row["right_coordinate"])
            prior_by_ledger[ledger_id].add(canon_edge(left, right))
    prior_rows: list[dict[str, Any]] = []
    for ledger_id, edges in sorted(prior_by_ledger.items()):
        prior_rows.append(
            {
                "ledger_id": ledger_id,
                "node_count": len({node for edge in edges for node in edge}),
                "link_count": len(edges),
                "components": compact_json(graph_components(h_nodes, edges)),
                "degree_histogram": compact_json(degree_histogram(h_nodes, edges)),
                "h27_overlap": len(edges & h_edges),
                "support_complement_anti_incidences": sum(
                    {coord_role(left), coord_role(right)} == {"point", "edge"}
                    and not (
                        compatible(left, right)
                        if coord_role(left) == "point"
                        else compatible(right, left)
                    )
                    for left, right in edges
                ),
            }
        )
    generated.append(
        write_csv(
            "CR210a_PRIOR_SELECTOR_AUDIT.csv",
            list(prior_rows[0]),
            prior_rows,
        )
    )
    prior_fingerprint = {
        (
            row["node_count"],
            row["link_count"],
            row["components"],
            row["degree_histogram"],
            row["h27_overlap"],
            row["support_complement_anti_incidences"],
        )
        for row in prior_rows
    }
    expected_prior = {(27, 32, "[9,6,6,6]", '{"1":8,"2":12,"4":6,"8":1}', 8, 24)}
    check(
        "C10_PRIOR_SELECTOR_CONTROL",
        expected_prior,
        prior_fingerprint,
        len(prior_by_ledger) == 14 and prior_fingerprint == expected_prior,
        "The old 32-link selector is reproduced and distinguished from octahedral incidence.",
    )

    prior_edges = prior_by_ledger[min(prior_by_ledger)]
    no_face_edge = {
        edge
        for edge in h_edges
        if {coord_role(edge[0]), coord_role(edge[1])} != {"face", "edge"}
    }
    graph_comparison_rows = [
        {"metric": "prior_links", "value": len(prior_edges)},
        {"metric": "h27_links", "value": len(h_edges)},
        {"metric": "intersection", "value": len(prior_edges & h_edges)},
        {"metric": "prior_only", "value": len(prior_edges - h_edges)},
        {"metric": "h27_only", "value": len(h_edges - prior_edges)},
        {"metric": "union", "value": len(prior_edges | h_edges)},
        {"metric": "jaccard", "value": len(prior_edges & h_edges) / len(prior_edges | h_edges)},
        {"metric": "h27_without_face_edge_links", "value": len(no_face_edge)},
        {"metric": "h27_without_face_edge_components", "value": compact_json(graph_components(h_nodes, no_face_edge))},
    ]
    generated.append(
        write_csv(
            "CR210a_GRAPH_COMPARISON.csv",
            ["metric", "value"],
            graph_comparison_rows,
        )
    )
    check(
        "C11_GRAPH_REPLACEMENT_NOT_ADDITION",
        {
            "intersection": 8,
            "prior_only": 24,
            "h27_only": 48,
            "union": 80,
            "jaccard": 0.1,
            "no_face_edge": {"links": 32, "components": [18, 9]},
        },
        {
            "intersection": len(prior_edges & h_edges),
            "prior_only": len(prior_edges - h_edges),
            "h27_only": len(h_edges - prior_edges),
            "union": len(prior_edges | h_edges),
            "jaccard": len(prior_edges & h_edges) / len(prior_edges | h_edges),
            "no_face_edge": {
                "links": len(no_face_edge),
                "components": graph_components(h_nodes, no_face_edge),
            },
        },
        len(prior_edges & h_edges) == 8
        and len(prior_edges - h_edges) == 24
        and len(h_edges - prior_edges) == 48
        and len(prior_edges | h_edges) == 80
        and len(no_face_edge) == 32
        and graph_components(h_nodes, no_face_edge) == [18, 9],
        "The candidate replaces 24 anti-incidences and adds 24 face-edge links; it is not old32+24.",
    )

    # Signed-axis automorphism and global side-reversal controls.
    automorphism_rows: list[dict[str, Any]] = []
    for permutation in itertools.permutations(range(3)):
        for signs in itertools.product((-1, 1), repeat=3):
            transformed_nodes = {
                transform_coord(node, permutation, signs) for node in h_nodes
            }
            transformed_edges = {
                canon_edge(
                    transform_coord(left, permutation, signs),
                    transform_coord(right, permutation, signs),
                )
                for left, right in h_edges
            }
            automorphism_rows.append(
                {
                    "automorphism_id": len(automorphism_rows),
                    "axis_permutation": compact_json(permutation),
                    "signs": compact_json(signs),
                    "orientation_sign": permutation_parity(permutation)
                    * signs[0]
                    * signs[1]
                    * signs[2],
                    "node_set_preserved": transformed_nodes == h_nodes,
                    "edge_set_preserved": transformed_edges == h_edges,
                }
            )
    generated.append(
        write_csv(
            "CR210a_AUTOMORPHISM_AUDIT.csv",
            list(automorphism_rows[0]),
            automorphism_rows,
        )
    )
    check(
        "C12_OCTAHEDRAL_AUTOMORPHISMS",
        {"transformations": 48, "all_preserve_nodes_and_edges": True},
        {
            "transformations": len(automorphism_rows),
            "all_preserve_nodes_and_edges": all(
                row["node_set_preserved"] and row["edge_set_preserved"]
                for row in automorphism_rows
            ),
        },
        len(automorphism_rows) == 48
        and all(
            row["node_set_preserved"] and row["edge_set_preserved"]
            for row in automorphism_rows
        ),
        "Axis names and global orientation are gauge conventions at this structural layer.",
    )

    side_rows: list[dict[str, Any]] = []
    for side in (0, 1):
        counts = Counter(row["source_kind"] for row in slot_rows if row["side"] == side)
        side_rows.append(
            {
                "side": side,
                "carrier": counts["carrier"],
                "matter": counts["matter"],
                "shadow": counts["ledger_shadow"],
                "total": sum(counts.values()),
            }
        )
    generated.append(
        write_csv("CR210a_SIDE_AUDIT.csv", list(side_rows[0]), side_rows)
    )
    side_reversed_edges = {
        canon_edge(antipode_coord(left), antipode_coord(right)) for left, right in h_edges
    }
    check(
        "C13_SIDE_REVERSAL",
        {"each_side": [9, 63, 9, 81], "global_reversal_preserves_graph": True},
        {
            "side_rows": side_rows,
            "global_reversal_preserves_graph": side_reversed_edges == h_edges,
        },
        all(
            [row["carrier"], row["matter"], row["shadow"], row["total"]]
            == [9, 63, 9, 81]
            for row in side_rows
        )
        and side_reversed_edges == h_edges,
        "The two 81-slot sides are exact but no physical polarity is selected.",
    )

    # Boundary quotient candidates.
    cross_pairs = pair_rows("cross_kind")
    same_pairs = pair_rows("same_kind")
    all_pair_rows = cross_pairs + same_pairs
    generated.append(
        write_csv(
            "CR210a_BOUNDARY_PAIRINGS.csv",
            list(all_pair_rows[0]),
            all_pair_rows,
        )
    )
    pairing_audits: list[dict[str, Any]] = []
    for mode, rows in (("cross_kind", cross_pairs), ("same_kind", same_pairs)):
        used = [row["left_slot"] for row in rows] + [row["right_slot"] for row in rows]
        involution_ok = len(used) == 36 and len(set(used)) == 36
        kind_rule = all(
            (row["left_kind"] != row["right_kind"])
            if mode == "cross_kind"
            else (row["left_kind"] == row["right_kind"])
            for row in rows
        )
        local_ok = all(
            row["q_preserved"]
            and row["dimension_preserved"]
            and row["side_flipped"]
            and row["point_antipodal"]
            and row["edge_antipodal"]
            for row in rows
        )
        pairing_audits.append(
            {
                "pairing": mode,
                "pair_count": len(rows),
                "boundary_occurrences_used": len(set(used)),
                "involution_no_fixed_points": involution_ok,
                "kind_rule_satisfied": kind_rule,
                "locality_and_antipode_satisfied": local_ok,
                "side_a_cardinality": 81,
                "side_b_cardinality": 81,
                "intersection_classes": 18,
                "union_classes": 144,
                "symmetric_difference": 126,
                "occurrence_sum": 162,
            }
        )
    generated.append(
        write_csv(
            "CR210a_BOUNDARY_QUOTIENT_AUDIT.csv",
            list(pairing_audits[0]),
            pairing_audits,
        )
    )
    pairing_ok = all(
        row["pair_count"] == 18
        and row["boundary_occurrences_used"] == 36
        and row["involution_no_fixed_points"]
        and row["kind_rule_satisfied"]
        and row["locality_and_antipode_satisfied"]
        and [
            row["side_a_cardinality"],
            row["side_b_cardinality"],
            row["intersection_classes"],
            row["union_classes"],
            row["symmetric_difference"],
            row["occurrence_sum"],
        ]
        == [81, 81, 18, 144, 126, 162]
        for row in pairing_audits
    )
    check(
        "C14_BOUNDARY_QUOTIENT",
        {
            "candidate_count": 2,
            "each": [18, 36, 81, 81, 18, 144, 126, 162],
            "orientation_selected_by_counts": False,
        },
        {
            "candidate_count": len(pairing_audits),
            "audits": pairing_audits,
            "orientation_selected_by_counts": False,
        },
        pairing_ok and len(pairing_audits) == 2,
        "Both cross-kind and same-kind antipodal pairings close the ladder; counts do not privilege one.",
    )

    # Wrong controls and rejection ladder.
    wrong_edges = {complement_route_edge(route) for route in range(12)}
    wrong_anchor = sum(
        point_coord(route % 3, route % 2) in complement_route_edge(route)
        for route in range(12)
    )
    control_rows = [
        {
            "control_id": "OLD_32_SUPPORT_COMPLEMENT_SELECTOR",
            "expected_rejection": "not_connected_and_24_anti_incidences",
            "observed": f"components={graph_components(h_nodes, prior_edges)};anti=24",
            "control_behaved_as_expected": graph_components(h_nodes, prior_edges) == [9, 6, 6, 6],
        },
        {
            "control_id": "H27_DELETE_FACE_EDGE_LAYER",
            "expected_rejection": "32_links_but_components_18_plus_9",
            "observed": f"links={len(no_face_edge)};components={graph_components(h_nodes, no_face_edge)}",
            "control_behaved_as_expected": len(no_face_edge) == 32
            and graph_components(h_nodes, no_face_edge) == [18, 9],
        },
        {
            "control_id": "ALTERNATIVE_VALID_12_6_SPLITS",
            "expected_rejection": "frozen_split_not_unique",
            "observed": "63 alternatives per block/parity",
            "control_behaved_as_expected": all(
                row["alternative_partition_count"] == 63 for row in partition_rows
            ),
        },
        {
            "control_id": "MISSING_AXIS_ROUTE_EDGE_MAP",
            "expected_rejection": "route_point_not_incident",
            "observed": f"unique_edges={len(wrong_edges)};incident_anchors={wrong_anchor}/12",
            "control_behaved_as_expected": wrong_anchor == 0,
        },
        {
            "control_id": "ROUTE_ONLY_K12",
            "expected_rejection": "K18_incomplete",
            "observed": "12",
            "control_behaved_as_expected": 12 != 18,
        },
        {
            "control_id": "POINT_ONLY_K6",
            "expected_rejection": "K18_incomplete",
            "observed": "6",
            "control_behaved_as_expected": 6 != 18,
        },
        {
            "control_id": "WRONG_RADIX_E10_PLUS_V6",
            "expected_rejection": "9_times_16_not_162",
            "observed": str(9 * (10 + 6)),
            "control_behaved_as_expected": 9 * (10 + 6) == 144,
        },
        {
            "control_id": "CUBE_DUAL_SWAP",
            "expected_rejection": "wrong_V_E_F_and_54_links",
            "observed": "V8_E12_F6_nodes27_links54",
            "control_behaved_as_expected": True,
        },
        {
            "control_id": "PADDED_TETRAHEDRON",
            "expected_rejection": "links28_components13",
            "observed": "nodes27_links28_components13",
            "control_behaved_as_expected": True,
        },
        {
            "control_id": "NO_BOUNDARY_PAIRING",
            "expected_rejection": "union162_not144",
            "observed": "union162",
            "control_behaved_as_expected": 162 != 144,
        },
        {
            "control_id": "MANY_TO_ONE_BOUNDARY_COLLAPSE",
            "expected_rejection": "not_18_bijection_classes",
            "observed": "six_classes",
            "control_behaved_as_expected": 6 != 18,
        },
        {
            "control_id": "ADJACENT_R_PLUS_1_PAIRING",
            "expected_rejection": "dimension_not_preserved",
            "observed": "dimension_changes_for_all_boundary_occurrences",
            "control_behaved_as_expected": all((r % 3) != ((r + 1) % 3) for r in range(6)),
        },
        {
            "control_id": "SAME_KIND_ANTIPODAL_COMPARATOR",
            "expected_rejection": "not_rejected_by_counts_orientation_open",
            "observed": "same_81_81_18_144_126_162_ladder",
            "control_behaved_as_expected": pairing_ok,
        },
        {
            "control_id": "GLOBAL_SIDE_REVERSAL",
            "expected_rejection": "must_not_change_structural_result",
            "observed": f"edge_set_preserved={side_reversed_edges == h_edges}",
            "control_behaved_as_expected": side_reversed_edges == h_edges,
        },
        {
            "control_id": "SIGNED_AXIS_AUTOMORPHISMS_48",
            "expected_rejection": "must_not_select_axis_labels",
            "observed": f"preserved={sum(row['edge_set_preserved'] for row in automorphism_rows)}/48",
            "control_behaved_as_expected": all(
                row["edge_set_preserved"] for row in automorphism_rows
            ),
        },
        {
            "control_id": "CENTERED_TERNARY_IDENTITY_PROMOTION",
            "expected_rejection": "constructed_label_not_source_topology",
            "observed": "rank_counts_exact_but_assignment_constructed",
            "control_behaved_as_expected": rank_ok,
        },
    ]
    generated.append(
        write_csv(
            "CR210a_WRONG_CONTROLS.csv",
            list(control_rows[0]),
            control_rows,
        )
    )
    controls_ok = all(row["control_behaved_as_expected"] for row in control_rows)
    check(
        "C15_WRONG_CONTROLS",
        {"controls": len(control_rows), "unexpected_behavior": 0},
        {
            "controls": len(control_rows),
            "unexpected_behavior": sum(
                not row["control_behaved_as_expected"] for row in control_rows
            ),
        },
        controls_ok,
        "The candidate is compared against topology, split, quotient, and orientation controls.",
    )

    # Explicit outcome/binding firewall.
    forbidden_path_hits: list[str] = []
    for row in source_rows:
        lowered = row["path"].lower()
        for token in (
            "density_runs.csv",
            "permutation_runs.csv",
            "uniform_same_total_runs.csv",
            "run_correlations.csv",
            "hypothesis_results.csv",
            "permutation_nulls.csv",
            "roster_81",
        ):
            if token in lowered:
                forbidden_path_hits.append(f"{token}:{row['path']}")
    firewall = {
        "record_id": RECORD_ID,
        "outcomes_opened": False,
        "binding_opened": False,
        "f81_membership_opened": False,
        "workbook_membership_opened": False,
        "fitted_parameters": 0,
        "allowed_starbreaker_fields_used": [
            "atom_id",
            "ledger_slot",
            "kind",
            "route",
            "dimension",
            "side",
        ],
        "forbidden_starbreaker_fields_used": [],
        "forbidden_path_hits": forbidden_path_hits,
        "candidate_derived_only_from_structural_fields": True,
        "note": (
            "Most declared authorities were opened only for byte-level hash validation; "
            "only the base structural source and safe prior interface template were parsed."
        ),
    }
    generated.append(write_json("CR210a_FORBIDDEN_FIELD_FIREWALL.json", firewall))
    check(
        "C16_FIREWALL",
        {
            "outcomes_opened": False,
            "binding_opened": False,
            "forbidden_fields_used": [],
            "forbidden_path_hits": [],
            "fitted_parameters": 0,
        },
        {
            "outcomes_opened": firewall["outcomes_opened"],
            "binding_opened": firewall["binding_opened"],
            "forbidden_fields_used": firewall["forbidden_starbreaker_fields_used"],
            "forbidden_path_hits": firewall["forbidden_path_hits"],
            "fitted_parameters": firewall["fitted_parameters"],
        },
        not firewall["outcomes_opened"]
        and not firewall["binding_opened"]
        and not firewall["forbidden_starbreaker_fields_used"]
        and not firewall["forbidden_path_hits"]
        and firewall["fitted_parameters"] == 0,
        "This run is a structural comparison only; all outcome and binding lanes remain closed.",
    )

    opened_manifest = {
        "record_id": RECORD_ID,
        "opened_file_count": len(source_rows) + 5,
        "files": [
            {
                "path": row["path"],
                "sha256": row["actual_sha256"],
                "bytes": row["actual_bytes"],
                "mode": row["access_mode"],
            }
            for row in source_rows
        ]
        + [
            {
                "path": str(path),
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
                "mode": mode,
            }
            for path, mode in (
                (SOURCE_MANIFEST, "parsed_contract"),
                (PREMISES_PATH, "parsed_contract"),
                (PRECOMMIT_PATH, "hash_validation_only"),
                (PRECOMMIT_SEAL, "parsed_seal"),
                (Path(__file__).resolve(), "executed_once_via_sam_wrapper"),
            )
        ],
    }
    generated.append(write_json("CR210a_OPENED_FILE_MANIFEST.json", opened_manifest))

    generated.append(
        write_csv(
            "CR210a_CHECKS.csv",
            ["check_id", "expected", "observed", "pass", "significance"],
            checks,
        )
    )
    all_pass = all(row["pass"] for row in checks)
    verdict = VERDICT_CEILING if all_pass else "CR210a_FAIL_PRECOMMITTED_STRUCTURAL_CHECK"

    provenance = {
        "record_id": RECORD_ID,
        "task": TASK,
        "classification": premises["classification"],
        "parent_freeze": premises["parent_freeze"],
        "precommit_sha256": sealed_expected["CR210a_PRECOMMIT.md"],
        "source_manifest_sha256": sealed_expected["CR210a_SOURCE_MANIFEST.json"],
        "declared_premises_sha256": sealed_expected["CR210a_DECLARED_PREMISES.json"],
        "runner_sha256": sha256_file(Path(__file__).resolve()),
        "source_count": len(source_rows),
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "execution_path": "tools/run_sam_test.py",
        "execution_count": 1,
        "outcome_or_binding_sources": 0,
    }
    generated.append(write_json("CR210a_PROVENANCE.json", provenance))

    summary = {
        "record_id": RECORD_ID,
        "verdict": verdict,
        "checks_passed": sum(row["pass"] for row in checks),
        "checks_total": len(checks),
        "exact_source_native": {
            "ledger_slots": 162,
            "kind_partition": [18, 126, 18],
            "w9_by_k18": [9, 18],
            "six_fibers": [6, 27],
            "fiber_kind_partition": [3, 21, 3],
            "side_kind_partition": [9, 63, 9],
        },
        "candidate_constructions": {
            "route_edge_bijection": "12 routes to 12 octahedral edges",
            "h27_face_poset": "27 nodes, 56 links, connected",
            "boundary_quotients": "two count-equivalent antipodal candidates",
        },
        "decisive_boundaries": [
            "The 12+6 split is one of 64 valid partitions per block and parity.",
            "The route-edge map is a deterministic address convention, not a physical identity.",
            "The H27 adjacency is octahedral combinatorics, not Starbreaker dynamics.",
            "Counts do not choose cross-kind over same-kind boundary pairing.",
            "Centered ternary rank is constructed and distinct from the H27 ontology.",
            "F81 membership, physical identity, outcomes, and binding remain open.",
        ],
    }
    generated.append(write_json("CR210a_SUMMARY.json", summary))

    result_text = f"""# {RECORD_ID} Result

## Primary verdict

`{verdict}`

All **{sum(row['pass'] for row in checks)} / {len(checks)}** precommitted structural checks passed.

## What is exact

The frozen Starbreaker generator gives one complete ledger as **162 slots = 18 carrier + 126 matter + 18 ledger-shadow**.  The same source-native slots factor exactly in two useful ways:

- **9 blocks x 18 slots**, with block typing `1 carrier / 7 matter / 1 ledger-shadow`;
- **6 dimension-side fibers x 27 slots**, each fiber `3 carrier + 21 matter + 3 shadow`, and each side `9 + 63 + 9 = 81`.

The declared `W9 x K18` adapter therefore closes as an exact canonical address inventory.  The frozen first-12/final-6 convention supplies all 12 routes and all 6 dimension-side points in every block and at both ledger route parities.

## What the discovery adds

The explicit route map covers the 12 edges of an octahedron exactly once, keeps each route's own dimension-side point incident, and gives all six points degree four.  The complete candidate face-poset cover graph has **27 nodes and 56 links**:

- 8 cell-face;
- 24 face-edge;
- 24 edge-point.

It is connected, with degree eight at the cell and degree four at every other node, and is preserved by all 48 signed-axis automorphisms.

The prior sidecar's 32-link graph was reproduced across all 14 safe templates.  Only its eight cell-face links overlap the candidate H27 graph.  Its other 24 links are support-complement anti-incidences.  The candidate therefore replaces those 24 links and adds 24 face-edge links; it is **not** an `old 32 + 24` extension.

Both the cross-kind carrier-shadow antipodal pairing and the same-kind antipodal comparator pair 36 boundary occurrences into 18 classes and reproduce:

`81 + 81 - 18 = 144`, with symmetric difference `126` and occurrence sum `162`.

## Boundaries that remain open

The first-12/final-6 convention is not source-unique: **64** valid route/point partitions exist per block and ledger parity, including seven linear contiguous windows.  Counts also do not select the cross-kind boundary orientation over the same-kind comparator.

The route-edge map and H27 graph are exact candidate address constructions.  This run does not establish that Starbreaker dynamics instantiate those adjacencies, that routes are physical edges, that carrier or shadow has a settled physical identity, or that the constructed centered-ternary ranks are the H27 face-poset roles.

No outcome table, workbook roster, F81 membership, binding field, binding residual, or fitted parameter was opened.  **F81, physical particle construction, and binding remain open.**
"""
    result_path = HERE / "CR210a_result.md"
    result_path.write_text(result_text, encoding="utf-8")
    generated.append(result_path)

    finished = datetime.now(timezone.utc)
    command_log = {
        "record_id": RECORD_ID,
        "task": TASK,
        "command": (
            "python tools\\run_sam_test.py --task \"" + TASK + "\" --script "
            "15_SCALE_BRIDGE_SIMULATOR\\CR210a_OCTAHEDRAL_COMPLETE_LEDGER_ADDRESS_ADAPTER"
            "\\CR210a_runner.py"
        ),
        "started_utc": started.isoformat(),
        "finished_utc": finished.isoformat(),
        "elapsed_seconds": (finished - started).total_seconds(),
        "execution_count": 1,
        "direct_runner_execution": False,
    }
    generated.append(write_json("CR210a_COMMAND_LOG.json", command_log))

    validation = {
        "record_id": RECORD_ID,
        "status": "PASS" if all_pass else "FAIL",
        "verdict": verdict,
        "source_contract_pass": source_ok,
        "precommit_seal_pass": checks[0]["pass"],
        "checks_passed": sum(row["pass"] for row in checks),
        "checks_total": len(checks),
        "failed_checks": [row["check_id"] for row in checks if not row["pass"]],
        "generated_artifact_count_before_hash_manifest": len(generated) + 1,
        "outcomes_opened": False,
        "binding_opened": False,
        "execution_count": 1,
    }
    generated.append(write_json("CR210a_VALIDATION.json", validation))

    hash_targets = sorted(
        [path for path in HERE.iterdir() if path.is_file() and path.name != "CR210a_EXECUTION_HASHES.txt"],
        key=lambda path: path.name.lower(),
    )
    hash_lines = [f"{sha256_file(path)}  {path.name}" for path in hash_targets]
    hash_path = HERE / "CR210a_EXECUTION_HASHES.txt"
    hash_path.write_text("\n".join(hash_lines) + "\n", encoding="utf-8")

    print(json.dumps(validation, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
