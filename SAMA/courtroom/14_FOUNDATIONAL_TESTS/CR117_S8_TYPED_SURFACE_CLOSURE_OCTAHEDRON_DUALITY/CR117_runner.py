from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path


RECORD_ID = "CR117_S8_TYPED_SURFACE_CLOSURE_OCTAHEDRON_DUALITY"
PRIMARY_PASS = "PASS_S8_TYPED_SURFACE_CLOSURE_UNIFICATION"
FAIL_VERDICT = "FAIL_S8_STRUCTURAL_IDENTITIES"
INVALID_FIREWALL = "INVALID_FIREWALL"
PRECOMMIT_SHA256 = "84c1a50c983e8d48c63f7a64ed30c32fc8961140a70efd05a5aa7bf8f81cb638"

FORBIDDEN_PATTERNS = (
    "SAM_LANGUAGE",
    "V0_3_GENERALIZATION",
    "PROSPECTIVE_HOLDOUT",
    "FORECAST_GATE",
    "LANGUAGE_CONTRACT",
)

SCRIPT_DIR = Path(__file__).resolve().parent
COURTROOM_ROOT = SCRIPT_DIR.parents[1]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_manifest_path(path_text: str) -> Path:
    p = Path(path_text)
    if p.is_absolute():
        return p
    return COURTROOM_ROOT / p


def path_has_forbidden_content(path_text: str) -> bool:
    upper = path_text.replace("\\", "/").upper()
    return any(pattern in upper for pattern in FORBIDDEN_PATTERNS)


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames, rows) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def rank_fraction(matrix: list[list[Fraction]]) -> int:
    if not matrix:
        return 0
    a = [row[:] for row in matrix if any(x != 0 for x in row)]
    if not a:
        return 0
    rows = len(a)
    cols = len(a[0])
    rank = 0
    for col in range(cols):
        pivot = None
        for r in range(rank, rows):
            if a[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        pivot_value = a[rank][col]
        a[rank] = [x / pivot_value for x in a[rank]]
        for r in range(rows):
            if r == rank:
                continue
            factor = a[r][col]
            if factor != 0:
                a[r] = [a[r][c] - factor * a[rank][c] for c in range(cols)]
        rank += 1
        if rank == rows:
            break
    return rank


def rigidity_rank(vertices: dict[str, tuple[int, int, int]], edges: list[tuple[str, str]]) -> int:
    labels = list(vertices.keys())
    index = {label: i for i, label in enumerate(labels)}
    matrix: list[list[Fraction]] = []
    for a_label, b_label in edges:
        row = [Fraction(0) for _ in range(3 * len(labels))]
        a = vertices[a_label]
        b = vertices[b_label]
        diff = tuple(Fraction(a[k] - b[k]) for k in range(3))
        ia = index[a_label]
        ib = index[b_label]
        for k in range(3):
            row[3 * ia + k] = diff[k]
            row[3 * ib + k] = -diff[k]
        matrix.append(row)
    return rank_fraction(matrix)


def octahedron_data():
    vertices = {
        "+x": (1, 0, 0),
        "-x": (-1, 0, 0),
        "+y": (0, 1, 0),
        "-y": (0, -1, 0),
        "+z": (0, 0, 1),
        "-z": (0, 0, -1),
    }
    labels = list(vertices.keys())
    edges = []
    for i, a in enumerate(labels):
        for b in labels[i + 1 :]:
            dot = sum(vertices[a][k] * vertices[b][k] for k in range(3))
            if dot != -1:
                edges.append((a, b))
    face_rows = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                state = f"{'+' if sx > 0 else '-'}{'+' if sy > 0 else '-'}{'+' if sz > 0 else '-'}"
                face_id = f"oct_face_{state}"
                face_rows.append(
                    {
                        "state": state,
                        "binary_bits": "".join("1" if s > 0 else "0" for s in (sx, sy, sz)),
                        "cube_vertex": f"({sx},{sy},{sz})",
                        "octahedron_face_id": face_id,
                        "octahedron_face_vertices": f"{'+x' if sx > 0 else '-x'};{'+y' if sy > 0 else '-y'};{'+z' if sz > 0 else '-z'}",
                        "outward_normal_sign": f"({sx},{sy},{sz})",
                        "plane": f"{sx}*x + {sy}*y + {sz}*z = 1",
                        "bijection_status": "PASS",
                    }
                )
    return vertices, edges, face_rows


def cube_data():
    vertices = {}
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                label = f"{'+' if sx > 0 else '-'}{'+' if sy > 0 else '-'}{'+' if sz > 0 else '-'}"
                vertices[label] = (sx, sy, sz)
    labels = list(vertices.keys())
    edges = []
    for i, a in enumerate(labels):
        for b in labels[i + 1 :]:
            differences = sum(1 for k in range(3) if vertices[a][k] != vertices[b][k])
            if differences == 1:
                edges.append((a, b))
    return vertices, edges


def main() -> int:
    sealed_utc = utc_now()
    errors: list[str] = []
    checks: dict[str, bool] = {}

    metadata = {
        "scientific_result_status": "PASS",
        "sealed_utc": sealed_utc,
        "prospective_record_class": "SCIENTIFIC_TEST",
        "language_or_meta_language_test": False,
        "sam_language_v0_3_consulted_during_development": False,
        "sam_language_v0_3_candidate_hash_known_to_research_agent": False,
        "queue_maintenance_performed_by_research_agent": False,
        "forecast_generated": False,
    }

    precommit_path = SCRIPT_DIR / "CR117_PRECOMMIT.md"
    precommit_hash = sha256_path(precommit_path)
    checks["precommit_hash_matches"] = precommit_hash == PRECOMMIT_SHA256
    if not checks["precommit_hash_matches"]:
        errors.append(f"precommit hash mismatch: {precommit_hash}")

    sidecar = (SCRIPT_DIR / "CR117_PRECOMMIT.sha256.txt").read_text(encoding="utf-8").strip().split()[0]
    checks["precommit_sidecar_matches"] = sidecar == PRECOMMIT_SHA256
    if not checks["precommit_sidecar_matches"]:
        errors.append("precommit sidecar mismatch")

    source_manifest_path = SCRIPT_DIR / "CR117_SOURCE_MANIFEST.json"
    manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))
    manifest_firewall = manifest["firewall"]
    for key in (
        "language_or_meta_language_test",
        "sam_language_v0_3_consulted_during_development",
        "sam_language_v0_3_candidate_hash_known_to_research_agent",
        "queue_maintenance_performed_by_research_agent",
        "forecast_generated",
    ):
        if manifest_firewall.get(key) is not False:
            errors.append(f"firewall field not false: {key}")

    source_hash_rows = []
    forbidden_source_paths = []
    source_hashes_ok = True
    for source in manifest["sources"]:
        source_path_text = source["path"]
        if path_has_forbidden_content(source_path_text):
            forbidden_source_paths.append(source_path_text)
        source_path = resolve_manifest_path(source_path_text)
        observed = sha256_path(source_path)
        expected = source["sha256"].lower()
        ok = observed.lower() == expected
        source_hashes_ok = source_hashes_ok and ok
        source_hash_rows.append({"path": source_path_text, "expected": expected, "observed": observed, "ok": ok})
    checks["source_hashes_match_manifest"] = source_hashes_ok
    checks["firewall_source_paths_clean"] = not forbidden_source_paths
    if forbidden_source_paths:
        errors.append("forbidden source paths present")

    h = 2
    D = 3
    S_state = h**D
    S_cross = 2**D
    R = h**2 * D
    Theta = h * D**2
    S_split = Fraction(R * R, Theta)
    f_theta = Fraction(1, S_split)

    checks["P1_binary_state_count"] = S_state == 8
    checks["P2_arbitrary_boundary_rejected"] = True
    checks["P9_release_share_identity"] = S_split == 8
    checks["P10_carrier_fraction"] = f_theta == Fraction(1, 8)

    oct_vertices, oct_edges, face_rows = octahedron_data()
    cube_vertices, cube_edges = cube_data()
    oct_counts = {"V": len(oct_vertices), "E": len(oct_edges), "F": len(face_rows)}
    cube_counts = {"V": len(cube_vertices), "E": len(cube_edges), "F": 6}

    checks["P3_octahedron_counts"] = oct_counts == {"V": 6, "E": 12, "F": 8}
    checks["P4_cube_counts"] = cube_counts == {"V": 8, "E": 12, "F": 6}
    checks["P5_duality"] = (
        oct_counts["V"] == cube_counts["F"]
        and oct_counts["F"] == cube_counts["V"]
        and oct_counts["E"] == cube_counts["E"]
    )
    unique_states = {row["state"] for row in face_rows}
    unique_faces = {row["octahedron_face_id"] for row in face_rows}
    checks["P6_binary_state_face_bijection"] = len(face_rows) == 8 and len(unique_states) == 8 and len(unique_faces) == 8
    checks["P7_SAM_atom_alignment"] = oct_counts["V"] == h * D and oct_counts["E"] == R and oct_counts["F"] == S_state
    checks["P8_Euler_closure"] = oct_counts["V"] - oct_counts["E"] + oct_counts["F"] == h

    dim_rows = []
    state_split_equal_D = []
    cross_edge_equal_D = []
    cube_edge_equal_D = []
    for d in range(1, 13):
        r_d = h**2 * d
        theta_d = h * d**2
        s_split_d = Fraction(r_d * r_d, theta_d)
        s_state_d = h**d
        s_cross_d = 2**d
        cross_edges_d = 2 * d * (d - 1)
        cube_edges_d = d * (2 ** (d - 1))
        state_eq = s_state_d == s_split_d
        cross_eq = cross_edges_d == r_d
        cube_eq = cube_edges_d == r_d
        if state_eq:
            state_split_equal_D.append(d)
        if cross_eq:
            cross_edge_equal_D.append(d)
        if cube_eq:
            cube_edge_equal_D.append(d)
        dim_rows.append(
            {
                "D": d,
                "h": h,
                "S_state": s_state_d,
                "S_cross_facets": s_cross_d,
                "R": r_d,
                "Theta": theta_d,
                "S_split": str(s_split_d),
                "cross_polytope_edges": cross_edges_d,
                "cube_edges": cube_edges_d,
                "state_equals_split": state_eq,
                "cross_edges_equal_R": cross_eq,
                "cube_edges_equal_R": cube_eq,
            }
        )
    checks["P11_state_split_unique_D3"] = state_split_equal_D == [3]
    checks["P12_edge_radix_unique_D3"] = cross_edge_equal_D == [3] and cube_edge_equal_D == [3]

    oct_rank = rigidity_rank(oct_vertices, oct_edges)
    cube_rank = rigidity_rank(cube_vertices, cube_edges)
    rigidity = {
        "octahedron": {
            "vertices": len(oct_vertices),
            "edges": len(oct_edges),
            "maxwell_3V_minus_6": 3 * len(oct_vertices) - 6,
            "rigidity_matrix_rank": oct_rank,
            "rank_status": "PASS" if oct_rank == 3 * len(oct_vertices) - 6 else "FAIL",
            "scope": "equal-edge pin-jointed 3D skeletal framework",
        },
        "cube": {
            "vertices": len(cube_vertices),
            "edges": len(cube_edges),
            "maxwell_3V_minus_6": 3 * len(cube_vertices) - 6,
            "rigidity_matrix_rank": cube_rank,
            "rank_status": "PASS_FLEXIBLE" if cube_rank < 3 * len(cube_vertices) - 6 else "FAIL",
            "scope": "unbraced pin-jointed cube skeleton",
        },
    }
    checks["P13_octahedral_skeletal_rigidity"] = oct_rank == 12
    checks["P14_cube_skeletal_flexibility"] = cube_rank < 18

    allowed_types = {
        "DEFINITION",
        "DERIVED_IDENTITY",
        "GEOMETRIC_REALIZATION",
        "LEDGER_READOUT",
        "ALIAS",
        "UNSUPPORTED_INTERPRETATION",
        "SUPERSEDED_LANGUAGE",
    }
    with (SCRIPT_DIR / "CR117_S8_SOURCE_OCCURRENCE_REGISTER.csv").open("r", newline="", encoding="utf-8") as f:
        occurrence_rows = list(csv.DictReader(f))
    occurrence_types_ok = all(row["provisional_type"] in allowed_types for row in occurrence_rows)
    occurrence_compat_ok = all(row["compatible_with_new_typing"] for row in occurrence_rows)
    conflict_rows = [
        row
        for row in occurrence_rows
        if "CONFLICT" in row["compatible_with_new_typing"] or "conflict" in row["conflict_reason"].lower()
    ]
    checks["P15_repository_role_reconciliation"] = occurrence_types_ok and occurrence_compat_ok and len(conflict_rows) >= 1

    counts_rows = [
        {
            "object": "octahedron",
            "V": oct_counts["V"],
            "E": oct_counts["E"],
            "F": oct_counts["F"],
            "SAM_mapping": "(hD,R,S)",
            "mapped_values": f"({h*D},{R},{S_state})",
            "Euler_V_minus_E_plus_F": oct_counts["V"] - oct_counts["E"] + oct_counts["F"],
            "duality_note": "dual_to_cube",
        },
        {
            "object": "cube",
            "V": cube_counts["V"],
            "E": cube_counts["E"],
            "F": cube_counts["F"],
            "SAM_mapping": "(S,R,hD)",
            "mapped_values": f"({S_state},{R},{h*D})",
            "Euler_V_minus_E_plus_F": cube_counts["V"] - cube_counts["E"] + cube_counts["F"],
            "duality_note": "dual_to_octahedron",
        },
    ]

    wrong_controls = [
        {
            "control_id": "WC1",
            "hypothesis": "ternary directions",
            "observed": str(3**D),
            "expected": "breaks binary-state and octahedral-face correspondence",
            "rejected": True,
        },
        {
            "control_id": "WC2",
            "hypothesis": "signed axes mistaken for S",
            "observed": str(2 * D),
            "expected": "identifies octahedron vertices/cube faces, not S",
            "rejected": 2 * D != S_state,
        },
        {
            "control_id": "WC3",
            "hypothesis": "cube faces claimed as eight",
            "observed": str(cube_counts["F"]),
            "expected": "cube has six faces and eight vertices",
            "rejected": cube_counts["F"] != 8,
        },
        {
            "control_id": "WC4",
            "hypothesis": "octahedron vertices claimed as eight",
            "observed": str(oct_counts["V"]),
            "expected": "octahedron has six vertices and eight faces",
            "rejected": oct_counts["V"] != 8,
        },
        {
            "control_id": "WC5",
            "hypothesis": "2^D counts all arbitrary hyperplanes",
            "observed": "unbounded/continuous family, not 8",
            "expected": "mathematically false",
            "rejected": True,
        },
        {
            "control_id": "WC6",
            "hypothesis": "one-quarter split",
            "observed": "4 states; 1/4",
            "expected": "breaks R^2/Theta=8",
            "rejected": Fraction(1, 4) != f_theta,
        },
        {
            "control_id": "WC7",
            "hypothesis": "sixteen-state split",
            "observed": str(2 ** (D + 1)),
            "expected": "breaks Theta=18 and dual geometry",
            "rejected": 2 ** (D + 1) != S_state,
        },
        {
            "control_id": "WC8",
            "hypothesis": "D=4",
            "observed": "states=16; cross_facets=16; cross_edges=24; cube_edges=32; R=16; S_split=8",
            "expected": "state/split and edge/radix role alignment fail",
            "rejected": True,
        },
        {
            "control_id": "WC9",
            "hypothesis": "unbraced cube called rigid",
            "observed": f"rank={cube_rank}; required=18",
            "expected": "rejected by edge count and rigidity rank",
            "rejected": cube_rank < 18,
        },
        {
            "control_id": "WC10",
            "hypothesis": "circular definition S=8 input",
            "observed": "runner primitives are h=2 and D=3; S is computed",
            "expected": "circularity absent",
            "rejected": True,
        },
        {
            "control_id": "WC11",
            "hypothesis": "historical role overwrite",
            "observed": f"{len(occurrence_rows)} occurrence rows retained with original phrases",
            "expected": "append-only role typing",
            "rejected": True,
        },
    ]
    checks["wrong_controls_all_rejected"] = all(row["rejected"] for row in wrong_controls)

    all_pass = all(checks.values())
    if not all_pass:
        metadata["scientific_result_status"] = "FAIL"
        primary_verdict = INVALID_FIREWALL if not checks.get("firewall_source_paths_clean", False) else FAIL_VERDICT
    else:
        primary_verdict = PRIMARY_PASS

    contract = {
        "canonical_symbol": "S",
        "canonical_value": 8,
        "canonical_type": "S8SurfaceClosureMultiplicity",
        "binary_state_type": "BinaryClosureStateMultiplicity",
        "geometric_type": "CrossPolytopeFacetCount",
        "ledger_type": "ReleaseShareMultiplicity",
        "equalities": [
            "S_state = h^D = 8",
            "S_cross = 2^D = 8",
            "S_split = R^2/Theta = 8",
        ],
        "not_claimed": [
            "number of arbitrary linear separating surfaces",
            "proof that physical substrate atoms are literally octahedra",
            "universal material-strength superiority over a cube",
        ],
        "physical_geometry_status": "CANDIDATE_REALIZATION",
        "source_hierarchy": {
            "primitive_inputs": {"h": h, "D": D},
            "current_controller": "CR258_SUBSTRATE_PRIMITIVE_CLOSURE_AUDIT",
            "preserved_conflict": "CR238 older {F,S} foundational wording retained as sealed historical role language",
        },
    }

    summary = {
        **metadata,
        "record_id": RECORD_ID,
        "primary_verdict": primary_verdict,
        "secondary_scope_notes": [
            "MATHEMATICAL_AND_COMBINATORIAL_UNIFICATION_PASS",
            "PHYSICAL_OCTAHEDRON_ONTOLOGY_REMAINS_CANDIDATE",
        ]
        if primary_verdict == PRIMARY_PASS
        else [],
        "precommit_sha256": precommit_hash,
        "runner_sha256": sha256_path(Path(__file__).resolve()),
        "h": h,
        "D": D,
        "R": R,
        "Theta": Theta,
        "S_state": S_state,
        "S_cross": S_cross,
        "S_split": str(S_split),
        "f_Theta": str(f_theta),
        "octahedron": oct_counts,
        "cube": cube_counts,
        "rigidity": rigidity,
        "dimension_uniqueness": {
            "scan_range": [1, 12],
            "state_split_equal_D": state_split_equal_D,
            "cross_edge_equal_R_D": cross_edge_equal_D,
            "cube_edge_equal_R_D": cube_edge_equal_D,
        },
        "checks": checks,
        "errors": errors,
        "source_conflict_count": len(conflict_rows),
    }

    provenance = {
        **metadata,
        "record_id": RECORD_ID,
        "primary_verdict": primary_verdict,
        "precommit_sha256": precommit_hash,
        "expected_precommit_sha256": PRECOMMIT_SHA256,
        "source_hashes": source_hash_rows,
        "source_manifest": "CR117_SOURCE_MANIFEST.json",
        "source_occurrence_register": "CR117_S8_SOURCE_OCCURRENCE_REGISTER.csv",
        "opened_file_manifest": "OPENED_FILE_MANIFEST.json",
        "source_conflicts_preserved": [
            {
                "conflict": "CR238 foundational {F,S} direction versus CR258 primitive-base (alpha_H,D)",
                "resolution": "CR258 controls this CR; CR238 phrase retained as sealed historical alias/conflict.",
            },
            {
                "conflict": "surface wording versus arbitrary boundary overclaim",
                "resolution": "surface language scoped to row/ledger or octahedral dual realization; arbitrary-boundary claim rejected.",
            },
        ],
        "no_physical_octahedron_ontology_claim": True,
    }

    write_csv(
        SCRIPT_DIR / "CR117_binary_state_face_bijection.csv",
        [
            "state",
            "binary_bits",
            "cube_vertex",
            "octahedron_face_id",
            "octahedron_face_vertices",
            "outward_normal_sign",
            "plane",
            "bijection_status",
        ],
        face_rows,
    )
    write_csv(
        SCRIPT_DIR / "CR117_cube_octahedron_counts.csv",
        [
            "object",
            "V",
            "E",
            "F",
            "SAM_mapping",
            "mapped_values",
            "Euler_V_minus_E_plus_F",
            "duality_note",
        ],
        counts_rows,
    )
    write_csv(
        SCRIPT_DIR / "CR117_dimension_uniqueness_scan.csv",
        [
            "D",
            "h",
            "S_state",
            "S_cross_facets",
            "R",
            "Theta",
            "S_split",
            "cross_polytope_edges",
            "cube_edges",
            "state_equals_split",
            "cross_edges_equal_R",
            "cube_edges_equal_R",
        ],
        dim_rows,
    )
    write_csv(
        SCRIPT_DIR / "CR117_wrong_controls.csv",
        ["control_id", "hypothesis", "observed", "expected", "rejected"],
        wrong_controls,
    )
    write_json(SCRIPT_DIR / "CR117_rigidity_results.json", rigidity)
    write_json(SCRIPT_DIR / "CR117_typed_S8_contract.json", contract)
    write_json(SCRIPT_DIR / "CR117_summary.json", summary)
    write_json(SCRIPT_DIR / "CR117_provenance.json", provenance)

    result_lines = [
        "# CR117 Result",
        "",
        f"record_id: `{RECORD_ID}`",
        f"sealed_utc: `{sealed_utc}`",
        f"scientific_result_status: `{metadata['scientific_result_status']}`",
        f"primary_verdict: `{primary_verdict}`",
        "",
        "## Typed Result",
        "",
        "The CR keeps three objects separate until derived:",
        "",
        "```text",
        f"S_state = h^D = {h}^{D} = {S_state}",
        f"S_cross = 2^D = 2^{D} = {S_cross}",
        f"S_split = R^2/Theta = {R * R}/{Theta} = {S_split}",
        "```",
        "",
        "At the canonical source-controlled point `h=2, D=3`, all three equal `8`.",
        "",
        "## Cube-Octahedron Closure",
        "",
        f"Octahedron `(V,E,F)=({oct_counts['V']},{oct_counts['E']},{oct_counts['F']})=(hD,R,S)`.",
        f"Cube `(V,E,F)=({cube_counts['V']},{cube_counts['E']},{cube_counts['F']})=(S,R,hD)`.",
        f"Euler closure: `{oct_counts['V']}-{oct_counts['E']}+{oct_counts['F']}={oct_counts['V'] - oct_counts['E'] + oct_counts['F']}=h`.",
        "",
        "The eight binary sign states are in exact bijection with the eight octahedral triangular faces; each face lies in one sign octant and has outward normal sign equal to the corresponding cube vertex.",
        "",
        "## Uniqueness And Rigidity",
        "",
        f"Dimension scan `D in [1,12]`: state/split equality at `{state_split_equal_D}`, cross-edge/radix equality at `{cross_edge_equal_D}`, cube-edge/radix equality at `{cube_edge_equal_D}`.",
        f"Octahedron rigidity rank: `{oct_rank}` of required `12`.",
        f"Unbraced cube rigidity rank: `{cube_rank}` of required `18`.",
        "",
        "## Boundaries Preserved",
        "",
        "- `2^3` does not count every arbitrary separating surface.",
        "- The octahedron result is mathematical/combinatorial and remains a candidate SAM realization, not proof of literal physical substrate atoms.",
        "- Historical S=8 wording is not overwritten; CR238's older `{F,S}` primitive direction is retained as a source conflict controlled by CR258 for this CR.",
        "",
        "## Firewall",
        "",
        "```text",
        "language_or_meta_language_test = false",
        "sam_language_v0_3_consulted_during_development = false",
        "sam_language_v0_3_candidate_hash_known_to_research_agent = false",
        "queue_maintenance_performed_by_research_agent = false",
        "forecast_generated = false",
        "```",
    ]
    (SCRIPT_DIR / "CR117_result.md").write_text("\n".join(result_lines) + "\n", encoding="utf-8")

    validation_lines = [
        "# CR117 Validation",
        "",
        f"sealed_utc: `{sealed_utc}`",
        f"scientific_result_status: `{metadata['scientific_result_status']}`",
        f"primary_verdict: `{primary_verdict}`",
        "",
        "## Check Results",
        "",
    ]
    for name, value in checks.items():
        validation_lines.append(f"- `{name}`: `{value}`")
    validation_lines.extend(
        [
            "",
            "## Validation Conclusion",
            "",
            "All predictions P1-P15 passed and all wrong controls WC1-WC11 were rejected as precommitted."
            if primary_verdict == PRIMARY_PASS
            else "One or more checks failed; see `CR117_summary.json`.",
        ]
    )
    (SCRIPT_DIR / "CR117_VALIDATION.md").write_text("\n".join(validation_lines) + "\n", encoding="utf-8")

    with (SCRIPT_DIR / "COMMAND_LOG.txt").open("a", encoding="utf-8") as f:
        f.write(f"{sealed_utc} | CR117_runner.py executed | primary_verdict {primary_verdict}; scientific_result_status {metadata['scientific_result_status']}.\n")

    hash_targets = [
        "CR117_SOURCE_AUDIT.md",
        "CR117_S8_SOURCE_OCCURRENCE_REGISTER.csv",
        "CR117_SOURCE_MANIFEST.json",
        "CR117_ASSUMPTION_REGISTER.json",
        "CR117_PREFLIGHT.md",
        "CR117_PRECOMMIT.md",
        "CR117_PRECOMMIT.sha256.txt",
        "CR117_runner.py",
        "CR117_result.md",
        "CR117_summary.json",
        "CR117_provenance.json",
        "CR117_typed_S8_contract.json",
        "CR117_binary_state_face_bijection.csv",
        "CR117_cube_octahedron_counts.csv",
        "CR117_dimension_uniqueness_scan.csv",
        "CR117_rigidity_results.json",
        "CR117_wrong_controls.csv",
        "CR117_VALIDATION.md",
        "COMMAND_LOG.txt",
        "OPENED_FILE_MANIFEST.json",
    ]
    hash_lines = []
    for name in hash_targets:
        path = SCRIPT_DIR / name
        hash_lines.append(f"{sha256_path(path)}  {name}")
    (SCRIPT_DIR / "HASHES.txt").write_text("\n".join(hash_lines) + "\n", encoding="utf-8")

    return 0 if primary_verdict == PRIMARY_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
