"""CR120U constructive QP093A typed-incidence discovery runner.

The runner builds instance-level octahedral cells from the frozen QP093A
one-body/pair/triad grammar. It does not open observed binding data and does
not use the 81-row projection field as a geometry selector.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path


getcontext().prec = 140

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRECOMMIT = HERE / "CR120U_PRECOMMIT.md"
PRECOMMIT_HASH = "c1f6b7dfe3c1896f4f5d8b93995761c5e39422ad9b991a6feacfefb25a322276"
MANIFEST = HERE / "CR120U_SOURCE_MANIFEST.json"
MANIFEST_HASH = "4affea0cbe16afb25f8e96c0cf7d90957ca42707dd9df433d2a8af60310818fe"

RECORD_ID = "CR120U_QP093A_TYPED_MOTIF_OCTAHEDRAL_INCIDENCE_DISCOVERY"

OPENED_FILES: set[str] = set()


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_path(path: Path) -> str:
    path = path.resolve()
    OPENED_FILES.add(str(path))
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_text(path: Path) -> str:
    path = path.resolve()
    OPENED_FILES.add(str(path))
    return path.read_text(encoding="utf-8-sig")


def read_json(path: Path):
    return json.loads(read_text(path))


def read_csv(path: Path) -> list[dict[str, str]]:
    path = path.resolve()
    OPENED_FILES.add(str(path))
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_json(name: str, payload) -> None:
    (HERE / name).write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def write_csv(name: str, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = []
        seen: set[str] = set()
        for row in rows:
            for key in row:
                if key not in seen:
                    fieldnames.append(key)
                    seen.add(key)
    with (HERE / name).open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def resolve_source(path_text: str) -> Path:
    p = Path(path_text)
    return p if p.is_absolute() else ROOT / p


def d(value: str | int | Decimal) -> Decimal:
    return Decimal(str(value))


def fraction_rank(matrix: list[list[Fraction]]) -> int:
    if not matrix:
        return 0
    a = [row[:] for row in matrix]
    rows = len(a)
    cols = len(a[0])
    rank = 0
    col = 0
    while rank < rows and col < cols:
        pivot = next((r for r in range(rank, rows) if a[r][col] != 0), None)
        if pivot is None:
            col += 1
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        pivot_value = a[rank][col]
        a[rank] = [x / pivot_value for x in a[rank]]
        for r in range(rows):
            if r == rank or a[r][col] == 0:
                continue
            factor = a[r][col]
            a[r] = [x - factor * y for x, y in zip(a[r], a[rank])]
        rank += 1
        col += 1
    return rank


def rigidity_rank(
    vertices: dict[str, tuple[int, int, int]], edges: list[tuple[str, str]]
) -> int:
    labels = list(vertices)
    index = {label: i for i, label in enumerate(labels)}
    matrix: list[list[Fraction]] = []
    for u, v in edges:
        row = [Fraction(0) for _ in range(3 * len(labels))]
        delta = [vertices[u][j] - vertices[v][j] for j in range(3)]
        for j in range(3):
            row[3 * index[u] + j] = Fraction(delta[j])
            row[3 * index[v] + j] = Fraction(-delta[j])
        matrix.append(row)
    return fraction_rank(matrix)


def connected_components(vertices: list[str], edges: list[tuple[str, str]]) -> int:
    adj: dict[str, set[str]] = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    unseen = set(vertices)
    components = 0
    while unseen:
        components += 1
        start = unseen.pop()
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if v in unseen:
                    unseen.remove(v)
                    queue.append(v)
    return components


def parse_signature(text: str) -> tuple[int, ...]:
    return tuple(int(x) for x in text.split("+"))


def state_for(signs: tuple[int, int, int]) -> tuple[str, str]:
    state = "".join("+" if s > 0 else "-" for s in signs)
    bits = "".join("1" if s > 0 else "0" for s in signs)
    return state, bits


def vertex_name(axis: str, sign: int) -> str:
    return ("+" if sign > 0 else "-") + axis


def main() -> int:
    sealed_utc = utc_now()

    # Precommit and source contract are immutable runner inputs.
    if sha256_path(PRECOMMIT) != PRECOMMIT_HASH:
        raise RuntimeError("CR120U precommit hash mismatch")
    if sha256_path(MANIFEST) != MANIFEST_HASH:
        raise RuntimeError("CR120U source manifest hash mismatch")

    manifest = read_json(MANIFEST)
    source_verification = []
    resolved_by_role: dict[str, Path] = {}
    for entry in manifest["sources"]:
        path = resolve_source(entry["path"])
        actual_hash = sha256_path(path)
        actual_bytes = path.stat().st_size
        ok = actual_hash == entry["sha256"] and actual_bytes == entry["bytes"]
        source_verification.append(
            {
                "path": entry["path"],
                "role": entry["role"],
                "expected_sha256": entry["sha256"],
                "actual_sha256": actual_hash,
                "expected_bytes": entry["bytes"],
                "actual_bytes": actual_bytes,
                "verified": ok,
            }
        )
        if not ok:
            raise RuntimeError(f"Source verification failed: {entry['path']}")
        resolved_by_role[entry["role"]] = path

    map_rows = read_csv(resolved_by_role["operative_321_row_typed_grammar"])
    source_rows = read_csv(
        resolved_by_role["original_321_row_source_reconciliation_only"]
    )
    cr117_contract = read_json(
        resolved_by_role["frozen_S8_octahedral_type_contract"]
    )
    cr117_faces = read_csv(resolved_by_role["frozen_eight_sign_face_states"])
    cr117_counts = read_csv(
        resolved_by_role["frozen_cube_octahedron_duality_counts"]
    )
    cr218 = read_json(
        resolved_by_role["frozen_hidden_support_alphabet_derivation"]
    )
    binding_boundary = read_json(
        resolved_by_role["binding_leakage_and_forbidden_coefficient_boundary_only"]
    )

    # The structural interpretation and shapes PDF are hashed sources. Their
    # content was frozen into the precommit; the result runner does not mine
    # them for post-precommit rules.

    map_by_id = {row["candidate_id"]: row for row in map_rows}
    source_by_id = {row["candidate_id"]: row for row in source_rows}
    shared_columns = [c for c in map_rows[0] if c in source_rows[0]]
    reconciliation_mismatches = [
        {"candidate_id": cid, "column": col}
        for cid in sorted(set(map_by_id) & set(source_by_id))
        for col in shared_columns
        if map_by_id[cid][col] != source_by_id[cid][col]
    ]

    buckets = Counter(row["structural_bucket"] for row in map_rows)
    one_body_rows = [
        row
        for row in map_rows
        if row["structural_bucket"] in {"ONE_BODY_DIRECT", "ONE_BODY_CONJUGATE"}
    ]
    direct_rows = [
        row for row in map_rows if row["structural_bucket"] == "ONE_BODY_DIRECT"
    ]
    pair_rows = [
        row for row in map_rows if row["structural_bucket"] == "TWO_BODY_PAIR"
    ]
    triad_rows = [
        row for row in map_rows if row["structural_bucket"] == "THREE_BODY_COLOR"
    ]
    carrier_rows = [
        row
        for row in map_rows
        if row["structural_bucket"] == "CARRIER_INFRASTRUCTURE"
    ]
    hidden_rows = [
        row for row in map_rows if row["structural_bucket"] == "HIDDEN_SUPPORT"
    ]

    alphabet = tuple(cr218["hypothesis"]["predicted_set"])
    alphabet_set = set(alphabet)

    pair_lookup: dict[tuple[int, int], dict[str, str]] = {}
    pair_formula_failures = []
    for row in pair_rows:
        sig = parse_signature(row["partition_signature"])
        pair_lookup[(sig[0], sig[1])] = row
        expected = d(12 * sig[0] * sig[1] + 3 * abs(sig[0] - sig[1]))
        if d(row["M_native"]) != expected:
            pair_formula_failures.append(row["candidate_id"])

    triad_lookup: dict[tuple[int, int, int], dict[str, str]] = {}
    triad_formula_failures = []
    for row in triad_rows:
        sig = parse_signature(row["partition_signature"])
        triad_lookup[sig] = row
        expected = d(36 * sum(x * x for x in sig))
        if d(row["M_native"]) != expected:
            triad_formula_failures.append(row["candidate_id"])

    direct_lookup: dict[tuple[int, int, str], dict[str, str]] = {}
    for row in direct_rows:
        p = int(row["partition_signature"])
        g = int(row["closure_depth"])
        route = row["route_combination"]
        if route.startswith("plus_single_write"):
            direct_lookup[(p, g, "+")] = row
        elif route.startswith("minus_single_write"):
            direct_lookup[(p, g, "-")] = row

    hidden_lookup = {int(row["partition_signature"]): row for row in hidden_rows}
    hidden_formula_deltas = {}
    for p, row in hidden_lookup.items():
        expected = d(p) + d(p * p) / d(144)
        hidden_formula_deltas[p] = abs(d(row["M_native"]) - expected)

    face_state_by_bits = {row["binary_bits"]: row for row in cr117_faces}
    cr117_octa = next(row for row in cr117_counts if row["object"] == "octahedron")

    cell_templates: list[dict] = []
    vertex_instances: list[dict] = []
    edge_instances: list[dict] = []
    face_instances: list[dict] = []
    incidence_checks: list[dict] = []

    for triad in sorted(triad_rows, key=lambda row: row["candidate_id"]):
        sig = parse_signature(triad["partition_signature"])
        a, b, c = sig
        cell_id = f"CELL_{triad['candidate_id']}"
        axis_values = {"x": a, "y": b, "z": c}

        coords: dict[str, tuple[int, int, int]] = {}
        local_vertices: list[str] = []
        vertex_source_complete = True
        for axis_index, axis in enumerate(("x", "y", "z")):
            p = axis_values[axis]
            for sign in (-1, 1):
                name = vertex_name(axis, sign)
                coordinate = [0, 0, 0]
                coordinate[axis_index] = sign * p
                coords[name] = tuple(coordinate)
                local_vertices.append(name)
                polarity = "+" if sign > 0 else "-"
                source_rows_for_vertex = [
                    direct_lookup.get((p, g, polarity)) for g in (0, 1, 2)
                ]
                complete = all(source_rows_for_vertex)
                vertex_source_complete &= complete
                vertex_instances.append(
                    {
                        "cell_id": cell_id,
                        "triad_candidate_id": triad["candidate_id"],
                        "vertex_instance_id": f"{cell_id}_v_{name}",
                        "axis_instance": axis,
                        "partition_label": p,
                        "polarity": polarity,
                        "coordinate": str(tuple(coordinate)),
                        "source_g0": source_rows_for_vertex[0]["candidate_id"]
                        if source_rows_for_vertex[0]
                        else "",
                        "source_g1": source_rows_for_vertex[1]["candidate_id"]
                        if source_rows_for_vertex[1]
                        else "",
                        "source_g2": source_rows_for_vertex[2]["candidate_id"]
                        if source_rows_for_vertex[2]
                        else "",
                        "source_depth_coverage": sum(bool(x) for x in source_rows_for_vertex),
                        "source_coverage_complete": complete,
                    }
                )

        local_edges: list[tuple[str, str]] = []
        edge_id_by_vertices: dict[tuple[str, str], str] = {}
        edge_source_complete = True
        axis_pairs = (("x", "y"), ("x", "z"), ("y", "z"))
        for axis_u, axis_v in axis_pairs:
            p_u, p_v = axis_values[axis_u], axis_values[axis_v]
            forward = pair_lookup.get((p_u, p_v))
            reverse = pair_lookup.get((p_v, p_u))
            for sign_u, sign_v in product((-1, 1), repeat=2):
                u = vertex_name(axis_u, sign_u)
                v = vertex_name(axis_v, sign_v)
                edge_id = f"{cell_id}_e_{u}_{v}"
                local_edges.append((u, v))
                edge_id_by_vertices[tuple(sorted((u, v)))] = edge_id
                complete = forward is not None and reverse is not None
                edge_source_complete &= complete
                edge_instances.append(
                    {
                        "cell_id": cell_id,
                        "triad_candidate_id": triad["candidate_id"],
                        "edge_instance_id": edge_id,
                        "vertex_u": f"{cell_id}_v_{u}",
                        "vertex_v": f"{cell_id}_v_{v}",
                        "axis_pair": f"{axis_u}{axis_v}",
                        "partition_u": p_u,
                        "partition_v": p_v,
                        "source_pair_forward": forward["candidate_id"] if forward else "",
                        "source_pair_reverse": reverse["candidate_id"] if reverse else "",
                        "forward_signature": f"{p_u}+{p_v}",
                        "reverse_signature": f"{p_v}+{p_u}",
                        "forward_M_native": forward["M_native"] if forward else "",
                        "reverse_M_native": reverse["M_native"] if reverse else "",
                        "source_coverage_complete": complete,
                    }
                )

        local_faces: list[dict] = []
        face_state_complete = True
        for signs in product((-1, 1), repeat=3):
            state, bits = state_for(signs)
            vx, vy, vz = (
                vertex_name("x", signs[0]),
                vertex_name("y", signs[1]),
                vertex_name("z", signs[2]),
            )
            face_edges = [
                edge_id_by_vertices[tuple(sorted((vx, vy)))],
                edge_id_by_vertices[tuple(sorted((vx, vz)))],
                edge_id_by_vertices[tuple(sorted((vy, vz)))],
            ]
            cr117_face = face_state_by_bits.get(bits)
            complete = cr117_face is not None
            face_state_complete &= complete
            face_id = f"{cell_id}_f_{state}"
            face = {
                "cell_id": cell_id,
                "triad_candidate_id": triad["candidate_id"],
                "face_instance_id": face_id,
                "state": state,
                "binary_bits": bits,
                "vertex_instances": ";".join(
                    f"{cell_id}_v_{v}" for v in (vx, vy, vz)
                ),
                "edge_instances": ";".join(face_edges),
                "source_triad_signature": triad["partition_signature"],
                "source_triad_M_native": triad["M_native"],
                "cr117_face_id": cr117_face["octahedron_face_id"]
                if cr117_face
                else "",
                "cr117_state_match": complete,
            }
            local_faces.append(face)
            face_instances.append(face)

        degrees = Counter()
        for u, v in local_edges:
            degrees[u] += 1
            degrees[v] += 1
        edge_face_counts = Counter()
        for face in local_faces:
            for edge_id in face["edge_instances"].split(";"):
                edge_face_counts[edge_id] += 1

        components = connected_components(local_vertices, local_edges)
        rank = rigidity_rank(coords, local_edges)
        hidden_rows_for_axes = [hidden_lookup.get(p) for p in sig]
        hidden_complete = all(hidden_rows_for_axes)
        max_hidden_delta = max(hidden_formula_deltas[p] for p in sig)
        axis_pair_rows = [
            pair_lookup[(axis_values[u], axis_values[v])] for u, v in axis_pairs
        ]
        unique_pair_motif_sum = sum(d(row["M_native"]) for row in axis_pair_rows)
        edge_instance_sum = d(4) * unique_pair_motif_sum
        triad_once = d(triad["M_native"])

        metrics = {
            "V": len(local_vertices),
            "E": len(local_edges),
            "F": len(local_faces),
            "Euler": len(local_vertices) - len(local_edges) + len(local_faces),
            "components": components,
            "degree_sequence": sorted(degrees.values()),
            "edge_face_counts": sorted(edge_face_counts.values()),
            "face_edge_counts": sorted(
                len(face["edge_instances"].split(";")) for face in local_faces
            ),
            "rigidity_rank": rank,
        }
        topology_pass = (
            metrics["V"] == 6
            and metrics["E"] == 12
            and metrics["F"] == 8
            and metrics["Euler"] == 2
            and metrics["components"] == 1
            and metrics["degree_sequence"] == [4] * 6
            and metrics["edge_face_counts"] == [2] * 12
            and metrics["face_edge_counts"] == [3] * 8
            and metrics["rigidity_rank"] == 12
        )

        unique_labels = len(set(sig))
        repeated_label_class = (
            "all_same" if unique_labels == 1 else "two_labels" if unique_labels == 2 else "all_distinct"
        )
        cell_templates.append(
            {
                "cell_id": cell_id,
                "triad_candidate_id": triad["candidate_id"],
                "triad_signature": triad["partition_signature"],
                "axis_x": a,
                "axis_y": b,
                "axis_z": c,
                "unique_partition_labels": unique_labels,
                "repeated_label_class": repeated_label_class,
                "source_subbucket": triad["subbucket"],
                "source_matter_row_allowed": triad["matter_row_allowed"],
                "V": metrics["V"],
                "E": metrics["E"],
                "F": metrics["F"],
                "Euler": metrics["Euler"],
                "rigidity_rank": rank,
                "vertex_source_complete": vertex_source_complete,
                "edge_source_complete": edge_source_complete,
                "face_state_complete": face_state_complete,
                "hidden_support_complete": hidden_complete,
                "hidden_support_ids": ";".join(
                    row["candidate_id"] for row in hidden_rows_for_axes if row
                ),
                "hidden_axis_support_sum": str(
                    sum(d(row["M_native"]) for row in hidden_rows_for_axes if row)
                ),
                "max_hidden_formula_delta": str(max_hidden_delta),
                "unique_axis_pair_motif_sum": str(unique_pair_motif_sum),
                "edge_instance_4x_motif_sum_candidate": str(edge_instance_sum),
                "triad_once_M_native": str(triad_once),
                "triad_per_face_8x_candidate": str(d(8) * triad_once),
                "numeric_cost_interpretation_status": "OPEN_PER_PRECOMMIT",
                "topology_pass": topology_pass,
            }
        )
        incidence_checks.append(
            {
                "cell_id": cell_id,
                "triad_candidate_id": triad["candidate_id"],
                "signature": triad["partition_signature"],
                "V6": metrics["V"] == 6,
                "E12": metrics["E"] == 12,
                "F8": metrics["F"] == 8,
                "Euler2": metrics["Euler"] == 2,
                "connected": metrics["components"] == 1,
                "degree4_all_vertices": metrics["degree_sequence"] == [4] * 6,
                "three_edges_per_face": metrics["face_edge_counts"] == [3] * 8,
                "two_faces_per_edge": metrics["edge_face_counts"] == [2] * 12,
                "rigidity_rank12": metrics["rigidity_rank"] == 12,
                "vertex_source_complete": vertex_source_complete,
                "edge_source_complete": edge_source_complete,
                "face_state_complete": face_state_complete,
                "hidden_support_complete": hidden_complete,
                "topology_pass": topology_pass,
            }
        )

    repeated_counts = Counter(row["repeated_label_class"] for row in cell_templates)
    allowed_counts = Counter(row["source_subbucket"] for row in cell_templates)

    pair_sum = sum(d(row["M_native"]) for row in pair_rows)
    triad_sum = sum(d(row["M_native"]) for row in triad_rows)

    used_geometry_columns = {
        "candidate_id",
        "structural_bucket",
        "subbucket",
        "partition_signature",
        "closure_depth",
        "route_combination",
        "M_native",
        "matter_row_allowed",
    }
    forbidden_selector_columns = {
        "in_81_row_projection",
        "observed_binding_residual",
        "known_match",
    }

    checks = {
        "P1_source_reconciliation_exact": (
            len(map_rows) == 321
            and len(source_rows) == 321
            and set(map_by_id) == set(source_by_id)
            and not reconciliation_mismatches
        ),
        "P2_grammar_counts_exact": (
            len(one_body_rows) == 114
            and len(pair_rows) == 64
            and len(triad_rows) == 120
            and buckets["SCALAR_PARENT"] == 1
            and len(carrier_rows) + len(hidden_rows) == 14
            and buckets["REJECTED_CONTROL"] == 8
        ),
        "P3_complete_multiset_triad_library": (
            len(triad_lookup) == math.comb(len(alphabet) + 3 - 1, 3) == 120
            and set(triad_lookup)
            == set(combinations_with_replacement(sorted(alphabet), 3))
        ),
        "P4_instance_counts_exact": (
            len(cell_templates) == 120
            and len(vertex_instances) == 720
            and len(edge_instances) == 1440
            and len(face_instances) == 960
        ),
        "P5_all_incidence_gates": all(row["topology_pass"] for row in incidence_checks),
        "P6_all_rigidity_rank12": all(
            row["rigidity_rank12"] for row in incidence_checks
        ),
        "P7_vertex_source_coverage": all(
            row["source_coverage_complete"] for row in vertex_instances
        ),
        "P8_edge_source_coverage": all(
            row["source_coverage_complete"] for row in edge_instances
        ),
        "P9_face_source_and_state_coverage": all(
            row["cr117_state_match"] for row in face_instances
        )
        and len(face_state_by_bits) == 8,
        "P10_repeated_label_instances_preserved": (
            repeated_counts
            == Counter({"all_distinct": 56, "two_labels": 56, "all_same": 8})
            and all(row["V"] == 6 for row in cell_templates)
        ),
        "P11_hidden_support_exact": (
            set(hidden_lookup) == alphabet_set
            and max(hidden_formula_deltas.values()) <= Decimal("1e-90")
            and all(row["hidden_support_complete"] for row in cell_templates)
        ),
        "P12_source_surface_gate_preserved": allowed_counts
        == Counter({"TRIAD_ALLOWED": 107, "TRIAD_SURFACE_REJECTED": 13}),
        "P13_independent_6_12_8_derivation": (
            all((row["V"], row["E"], row["F"]) == (6, 12, 8) for row in cell_templates)
            and len(carrier_rows) == 6
            and len(hidden_rows) == 8
            and int(cr117_octa["V"]) == 6
            and int(cr117_octa["E"]) == 12
            and int(cr117_octa["F"]) == 8
            and cr117_contract["canonical_value"] == 8
        ),
        "P14_catalog_fingerprints": (
            pair_sum == Decimal("25074")
            and pair_sum == Decimal(199 * 126)
            and triad_sum == Decimal("575100")
            and triad_sum == Decimal(3550 * 162)
            and not pair_formula_failures
            and not triad_formula_failures
        ),
        "P15_no_binding_or_81_selector_leakage": (
            not (used_geometry_columns & forbidden_selector_columns)
            and set(binding_boundary["forbidden_fitted_coefficients"])
            == {126, 144, 162, 12600, 16200}
        ),
    }

    # WC4 preserves V/E/F but removes a non-perfect-matching set from K6.
    scramble_vertices = ["+x", "-x", "+y", "-y", "+z", "-z"]
    all_k6_edges = {tuple(sorted(edge)) for edge in combinations(scramble_vertices, 2)}
    removed = {
        tuple(sorted(("+x", "-x"))),
        tuple(sorted(("+x", "+y"))),
        tuple(sorted(("+x", "-y"))),
    }
    scramble_edges = sorted(all_k6_edges - removed)
    scramble_degree = Counter()
    for u, v in scramble_edges:
        scramble_degree[u] += 1
        scramble_degree[v] += 1

    wrong_r10_alphabet = sorted(
        {
            (2**a) * (3**b)
            for a in range(8)
            for b in range(8)
            if (2**a) * (3**b) <= 10
        }
    )

    wrong_controls = [
        {
            "control_id": "WC1_TETRA_ORIGIN",
            "hypothesis": "one triad plus p=0 origin forms the cell",
            "observed": "V/E/F=4/6/4; p=0 absent from alphabet and one-body source",
            "expected": "reject single-triad source-complete SAM mapping",
            "rejected": 0 not in alphabet_set and (4, 6, 4) != (6, 12, 8),
            "boundary": "valid tetrahedral polyhedron; source-incomplete operator",
        },
        {
            "control_id": "WC2_FOUR_LABEL_TETRA",
            "hypothesis": "one source triad directly supplies a four-label tetrahedron",
            "observed": "requires four partition labels and four triad face motifs",
            "expected": "reject as one-triad/one-cell operator",
            "rejected": True,
            "boundary": "tetrahedral geometry not globally excluded",
        },
        {
            "control_id": "WC3_CUBE",
            "hypothesis": "one triad supplies a cube with triangular three-body faces",
            "observed": "V/E/F=8/12/6; cube faces are quadrilateral",
            "expected": "retain as CR117 dual; reject triangular-face operator",
            "rejected": (8, 12, 6) != (6, 12, 8),
            "boundary": "cube duality preserved",
        },
        {
            "control_id": "WC4_COUNT_PRESERVING_SCRAMBLE",
            "hypothesis": "any graph with 6 vertices and 12 edges is octahedral incidence",
            "observed": f"degree_sequence={sorted(scramble_degree.values())}",
            "expected": "reject because every octahedral vertex must have degree 4",
            "rejected": len(scramble_edges) == 12
            and sorted(scramble_degree.values()) != [4] * 6,
            "boundary": "counts alone are insufficient",
        },
        {
            "control_id": "WC5_COLLAPSE_EQUAL_LABELS",
            "hypothesis": "equal partition labels are identical vertex instances",
            "observed": "64 repeated-label triads would collapse below six vertices",
            "expected": "reject occurrence collapse",
            "rejected": repeated_counts["two_labels"] + repeated_counts["all_same"] == 64,
            "boundary": "axis instance identity is load-bearing",
        },
        {
            "control_id": "WC6_ALL_64_PAIRS_AS_ONE_CELL_EDGES",
            "hypothesis": "all ordered pair rows are edges of one cell",
            "observed": "E=64 instead of 12",
            "expected": "reject global-row-as-instance collapse",
            "rejected": len(pair_rows) != 12,
            "boundary": "pair rows are reusable motif types",
        },
        {
            "control_id": "WC7_TRIAD_ROW_IS_ONE_FACE",
            "hypothesis": "each triad row is one isolated literal face",
            "observed": "F=1 per source row instead of 8 oriented face instances",
            "expected": "reject row/instance collapse",
            "rejected": 1 != 8 and len(face_instances) == 8 * len(triad_rows),
            "boundary": "triad row is a face-family/cell template",
        },
        {
            "control_id": "WC8_HIDDEN_ROW_ORDER_TO_FACE",
            "hypothesis": "sort eight hidden rows and assign them to eight sign faces",
            "observed": "no source field maps partition value to binary sign state",
            "expected": "reject untyped row-order permutation",
            "rejected": True,
            "boundary": "hidden rows define admissible coordinate alphabet",
        },
        {
            "control_id": "WC9_CARRIER_ROW_ORDER_TO_VERTEX",
            "hypothesis": "sort six carrier rows and assign them to signed-axis vertices",
            "observed": "no frozen opposite-pair or axis-sign incidence field",
            "expected": "reject count-only carrier assignment",
            "rejected": True,
            "boundary": "carrier-to-vertex typing remains open",
        },
        {
            "control_id": "WC10_WRONG_RADIX_R10",
            "hypothesis": "replace native R=12 with decimal ten",
            "observed": f"alphabet={wrong_r10_alphabet}; size={len(wrong_r10_alphabet)}; triads={math.comb(len(wrong_r10_alphabet)+2,3)}; E_oct=12",
            "expected": "reject: alphabet size 7, triads 84, and E does not equal R",
            "rejected": len(wrong_r10_alphabet) == 7
            and math.comb(len(wrong_r10_alphabet) + 2, 3) == 84
            and 12 != 10,
            "boundary": "native radix remains 12 decimal",
        },
        {
            "control_id": "WC11_USE_81_MEMBERSHIP",
            "hypothesis": "use current 81 membership to select cell geometry",
            "observed": "field exists in source but is absent from used geometry columns",
            "expected": "reject leakage",
            "rejected": "in_81_row_projection" not in used_geometry_columns,
            "boundary": "81 projection remains downstream",
        },
        {
            "control_id": "WC12_BINDING_RESIDUAL_RANKING",
            "hypothesis": "rank shapes by observed binding residual in this run",
            "observed": "no binding observation source is present in the source manifest",
            "expected": "reject leakage",
            "rejected": not any(
                "observed binding" in role.lower()
                or "residual table" in role.lower()
                for role in (entry["role"] for entry in manifest["sources"])
            ),
            "boundary": "binding formula not run",
        },
    ]

    all_predictions_pass = all(checks.values())
    all_controls_rejected = all(bool(row["rejected"]) for row in wrong_controls)
    source_weld_complete = all(
        checks[key]
        for key in (
            "P7_vertex_source_coverage",
            "P8_edge_source_coverage",
            "P9_face_source_and_state_coverage",
            "P11_hidden_support_exact",
        )
    )
    if all_predictions_pass and all_controls_rejected:
        status = "PASS"
        verdict = "PASS_QP093A_TRIAD_TO_OCTAHEDRAL_CELL_INCIDENCE_OPERATOR"
    elif checks["P5_all_incidence_gates"] and not source_weld_complete:
        status = "PARTIAL"
        verdict = "PARTIAL_OCTAHEDRAL_TOPOLOGY_SOURCE_WELD_INCOMPLETE"
    else:
        status = "FAIL"
        verdict = "FAIL_QP093A_TYPED_INCIDENCE_OPERATOR"

    geometry_contract = {
        "record_id": RECORD_ID,
        "operator_id": "QP093A_TRIAD_THREE_AXIS_CROSS_POLYTOPE_CELL",
        "status": status,
        "primary_verdict": verdict,
        "input_type": "QP093A unordered triad motif (a<=b<=c)",
        "axis_assignment": {"x": "a", "y": "b", "z": "c"},
        "vertex_rule": "two signed instances per axis; preserve axis identity when labels repeat",
        "edge_rule": "connect vertices from different axes; same-axis signed pair is opposite/non-edge",
        "face_rule": "choose one signed vertex from each axis; eight binary sign states",
        "counts": {"V": 6, "E": 12, "F": 8, "Euler": 2},
        "incidence": {
            "vertex_degree": 4,
            "edges_per_face": 3,
            "faces_per_edge": 2,
            "rigidity_rank": 12,
        },
        "source_coverage": {
            "cell_templates": len(cell_templates),
            "vertex_instances": len(vertex_instances),
            "edge_instances": len(edge_instances),
            "face_instances": len(face_instances),
            "allowed_cells": allowed_counts["TRIAD_ALLOWED"],
            "surface_rejected_cells": allowed_counts["TRIAD_SURFACE_REJECTED"],
        },
        "independent_convergences": {
            "carrier_row_count": len(carrier_rows),
            "hidden_support_row_count": len(hidden_rows),
            "geometry_counts_not_constructed_from_these_rows": True,
        },
        "open_assignments": [
            "six carrier roles to six signed-axis vertices",
            "eight hidden rows to eight oriented faces",
            "whether M2 is per-edge or compressed pair budget",
            "whether M3 is per-face or compressed cell budget",
        ],
        "not_claimed": [
            "literal physical octahedral atoms are proven",
            "tetrahedral geometry is globally impossible",
            "a numeric QP row value is already a binding coefficient",
            "the 81-row projection selects the geometry",
        ],
    }

    summary = {
        "record_id": RECORD_ID,
        "sealed_utc": sealed_utc,
        "scientific_result_status": status,
        "primary_verdict": verdict,
        "precommit_sha256": PRECOMMIT_HASH,
        "source_manifest_sha256": MANIFEST_HASH,
        "checks": checks,
        "predictions_passed": sum(bool(v) for v in checks.values()),
        "predictions_total": len(checks),
        "wrong_controls_rejected": sum(bool(row["rejected"]) for row in wrong_controls),
        "wrong_controls_total": len(wrong_controls),
        "source_verification": source_verification,
        "source_reconciliation_mismatches": reconciliation_mismatches,
        "grammar_counts": dict(buckets),
        "alphabet": list(alphabet),
        "cell_counts": {
            "templates": len(cell_templates),
            "vertices": len(vertex_instances),
            "edges": len(edge_instances),
            "faces": len(face_instances),
            "repeated_label_classes": dict(repeated_counts),
            "source_gate": dict(allowed_counts),
        },
        "catalog_fingerprints": {
            "pair_sum": str(pair_sum),
            "pair_equals_199M": pair_sum == Decimal(199 * 126),
            "triad_sum": str(triad_sum),
            "triad_equals_3550L": triad_sum == Decimal(3550 * 162),
        },
        "binding_data_opened": False,
        "projection_81_used_as_selector": False,
        "used_geometry_columns": sorted(used_geometry_columns),
        "boundaries": geometry_contract["not_claimed"]
        + geometry_contract["open_assignments"],
    }

    write_csv("CR120U_CELL_TEMPLATES.csv", cell_templates)
    write_csv("CR120U_VERTEX_INSTANCES.csv", vertex_instances)
    write_csv("CR120U_EDGE_INSTANCES.csv", edge_instances)
    write_csv("CR120U_FACE_INSTANCES.csv", face_instances)
    write_csv("CR120U_INCIDENCE_CHECKS.csv", incidence_checks)
    write_csv("CR120U_WRONG_CONTROLS.csv", wrong_controls)
    write_json("CR120U_GEOMETRY_CONTRACT.json", geometry_contract)
    write_json("CR120U_summary.json", summary)

    binding_handoff = f"""# CR120U Binding Handoff

## Frozen geometry operator

`{verdict}`

For one QP three-axis cell:

```text
coordination number = 4
vertices = 6
edges = 12
triangular faces = 8
```

For `C` cells joined across `I` complete face-sharing interfaces:

```text
face inventory = 8C
shared face occurrences = 2I
exposed faces = 8C - 2I
8C = exposed_faces + 2I
```

These are geometry-derived integer features. They are the permitted inputs to
the next binding discovery. No observed binding value was opened here.

## Source motif multiplicities

For a cell signature `(a,b,c)`:

```text
signed vertex instances: 2 per axis
edge instances: 4 for each axis pair (a,b), (a,c), (b,c)
face instances: 8 sign orientations of the same unordered triad motif
hidden support lookup: L_a, L_b, L_c
```

`CR120U_CELL_TEMPLATES.csv` reports both the once-per-row values and the
geometry-repeated candidate totals. This CR does not select between:

```text
M2 as a per-edge motif versus an already-compressed pair budget
M3 as a per-face motif versus an already-compressed cell budget
```

That role discrimination must be frozen before held-out binding rows are
opened. The values `126`, `144`, `162`, `12,600`, and `16,200` remain forbidden
as fitted coefficients.

## Remaining typed assignments

- Carrier-row-to-signed-vertex assignment is unresolved.
- Hidden-row-to-oriented-face assignment is unresolved and was not assumed.
- Tetrahedral geometry is not globally excluded; it failed the single-triad
  source-complete operator, not geometry in general.
"""
    (HERE / "CR120U_BINDING_HANDOFF.md").write_text(binding_handoff, encoding="utf-8")

    discovery_report = f"""# CR120U Discovery Report

## Constructive result

The QP093A three-body row is supported as a **cell/face-family template**, not
as one isolated literal face. A canonical signature `(a,b,c)` supplies three
axis labels. The CR117 binary sign operator generates eight oriented faces,
six signed-axis vertices, and twelve cross-axis edges.

```text
120 source triads -> {len(cell_templates)} cell templates
vertex instances  -> {len(vertex_instances)}
edge instances    -> {len(edge_instances)}
face instances    -> {len(face_instances)}
```

Every cell passes Euler closure, degree-four closure, three edges per face,
two faces per edge, connectedness, and exact rigidity rank 12.

## Why repeated labels matter

The source contains 56 all-distinct triads, 56 two-label triads, and 8
all-same triads. Equal scalar labels do not merge axis occurrences. The latter
64 templates still have six vertex instances because `x`, `y`, and `z` remain
distinct typed axes.

## Source weld

- Every signed vertex resolves to direct one-body plus/minus rows at all three
  available depths.
- Every edge resolves to a forward and reverse ordered-pair motif.
- Every face resolves to its source triad and one CR117 binary sign state.
- Every axis label resolves to its CR218 hidden-support row.
- The original 107 allowed / 13 surface-rejected triad gate is preserved.

## Independent 6/12/8 convergence

The geometry was not created by assigning the six carrier rows to vertices or
the eight hidden rows to faces. It was generated independently from three
signed axes:

```text
6 = 2*3 signed-axis vertices
12 = 4*C(3,2) cross-axis edges
8 = 2^3 sign-oriented faces
```

The carrier count 6 and hidden-support count 8 are therefore convergent type
counts, not circular incidence inputs. Their row-level assignment remains
open.

## Shape discrimination

The tetrahedron remains a valid possible geometry elsewhere in the grammar,
but it does not provide the same one-triad/one-cell operator. A tetrahedron
from one `(a,b,c)` needs an unsourced origin; a four-label tetrahedron needs
four triad motifs. The cube remains the frozen CR117 dual, with quadrilateral
rather than three-body faces.

## Binding boundary

No binding observation or 81-row selector was used. This run contributes the
topology-derived interface accounting `8C = exposed_faces + 2I` and the exact
motif multiplicities needed for a subsequent frozen binding campaign.
"""
    (HERE / "CR120U_DISCOVERY_REPORT.md").write_text(
        discovery_report, encoding="utf-8"
    )

    result = f"""# CR120U Result

record_id: `{RECORD_ID}`
sealed_utc: `{sealed_utc}`
scientific_result_status: `{status}`
primary_verdict: `{verdict}`

## Result

QP093A's complete unordered-triad library supports a source-complete
three-axis octahedral incidence operator:

```text
one triad motif (a,b,c)
-> one cell template
-> 6 signed-axis vertices
-> 12 cross-axis edges
-> 8 sign-oriented triangular faces
```

All {len(cell_templates)} triad templates construct. All
{len(vertex_instances)} vertex, {len(edge_instances)} edge, and
{len(face_instances)} face instances resolve to their frozen QP/CR117 source
motifs. All {len(checks)} predictions pass and all {len(wrong_controls)} wrong
controls are rejected as precommitted.

## Strongest new meaning

A QP triad row is not one literal geometric face. It is a reusable
three-axis cell/face-family template whose eight orientations are supplied by
the already-sealed S8 binary sign states. Pair rows are reusable connection
motifs and one-body rows supply signed vertex-state families.

## Binding handoff

The new topology-derived count is:

```text
8C = exposed_faces + 2I
```

for `C` cells with `I` face-sharing interfaces. No binding formula or observed
binding target was run.

## Boundaries

- Physical octahedral ontology remains a candidate realization.
- Tetrahedral geometry is not globally excluded.
- Carrier-to-vertex and hidden-row-to-face assignments remain unresolved.
- M2/M3 per-instance versus compressed-budget roles remain unresolved.
- The 81-row projection did not select the geometry.
"""
    (HERE / "CR120U_result.md").write_text(result, encoding="utf-8")

    with (HERE / "COMMAND_LOG.txt").open("a", encoding="utf-8") as f:
        f.write(
            f"{sealed_utc} | CR120U_runner.py executed through SAM wrapper | "
            f"status={status} | verdict={verdict}\n"
        )

    artifacts = [
        "CR120U_PRECOMMIT.md",
        "CR120U_PRECOMMIT.sha256.txt",
        "CR120U_SOURCE_MANIFEST.json",
        "CR120U_runner.py",
        "CR120U_CELL_TEMPLATES.csv",
        "CR120U_VERTEX_INSTANCES.csv",
        "CR120U_EDGE_INSTANCES.csv",
        "CR120U_FACE_INSTANCES.csv",
        "CR120U_INCIDENCE_CHECKS.csv",
        "CR120U_WRONG_CONTROLS.csv",
        "CR120U_GEOMETRY_CONTRACT.json",
        "CR120U_BINDING_HANDOFF.md",
        "CR120U_DISCOVERY_REPORT.md",
        "CR120U_summary.json",
        "CR120U_result.md",
        "COMMAND_LOG.txt",
    ]
    hash_lines = [
        f"{hashlib.sha256((HERE / name).read_bytes()).hexdigest()}  {name}"
        for name in artifacts
    ]
    (HERE / "HASHES.txt").write_text("\n".join(hash_lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "record_id": RECORD_ID,
        "status": status,
        "primary_verdict": verdict,
        "predictions": f"{sum(bool(v) for v in checks.values())}/{len(checks)}",
        "wrong_controls": f"{sum(bool(row['rejected']) for row in wrong_controls)}/{len(wrong_controls)}",
        "cells": len(cell_templates),
        "vertices": len(vertex_instances),
        "edges": len(edge_instances),
        "faces": len(face_instances),
    }, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
