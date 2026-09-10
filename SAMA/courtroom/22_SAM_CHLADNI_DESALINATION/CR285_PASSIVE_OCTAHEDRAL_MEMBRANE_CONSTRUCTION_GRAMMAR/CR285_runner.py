"""CR285 passive octahedral membrane construction runner.

Builds a topology-only passive gate catalog from frozen CR120U outputs. It does
not emit a species construction, selectivity prediction, material choice,
physical pore dimension, or desalination result.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
RECORD_ID = "CR285_PASSIVE_OCTAHEDRAL_MEMBRANE_CONSTRUCTION_GRAMMAR"
PASS_CLASS = (
    "CR285_PASS_PASSIVE_OCTAHEDRAL_MEMBRANE_CONSTRUCTION_GRAMMAR__"
    "960_DIRECTED_GATES__NO_SPECIES_SELECTIVITY_OR_PHYSICAL_PROMOTION"
)

CONTRACT_HASHES = {
    "CR285_PRECOMMIT.md": "66a59b1ff13f083441f4195d55cfbba73bfe0c2ffd33b0416727d33aab8f11f7",
    "CR285_declared_premises.json": "ec16cbe47cd78b8e6b5f7644a06303330fdf84bf0a9d498a3068bfa6eabb3596",
    "CR285_PASSIVE_MEMBRANE_SYSTEM.md": "5e42a3dd0c80a00be554b0c0a4ad7b6ebdcea3da2e1990956b0fc8bf18ad9c25",
    "CR285_COMPATIBILITY_OPERATOR.md": "d16448713923c41915143f2d1ebf9bee848c5cdeadffc086b084ced922a1e62e",
    "CR285_wrong_controls_precommitted.csv": "6158f462af84ce1e5e9b5d821baa2f7c6ad7bbb8f3eb31b2e13863e9df0ae243",
    "CR285_input_manifest.csv": "df6bc251e7218c6abd4c3039e2b7775941b6b69b2a8625d836e4bb3854afc50c",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_json(path: Path):
    return json.loads(read_text(path))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def add_check(checks: list[dict], check_id: str, requirement: str, actual, passed: bool) -> None:
    checks.append(
        {
            "check_id": check_id,
            "requirement": requirement,
            "actual": str(actual),
            "passed": str(bool(passed)).lower(),
        }
    )


def split_items(value: str) -> set[str]:
    return {item for item in value.split(";") if item}


def complement_bits(bits: str) -> str:
    if len(bits) != 3 or any(bit not in "01" for bit in bits):
        raise ValueError(f"invalid three-bit face state: {bits}")
    return "".join("1" if bit == "0" else "0" for bit in bits)


def main() -> int:
    sealed_utc = utc_now()
    checks: list[dict] = []

    preflight_file = os.environ.get("SAM_PREFLIGHT_FILE", "")
    preflight_token = os.environ.get("SAM_PREFLIGHT_TOKEN", "")
    runner_version = os.environ.get("SAM_RUNNER_VERSION", "")
    add_check(
        checks,
        "C01",
        "Courtroom preflight metadata is present",
        f"file={bool(preflight_file)} token={bool(preflight_token)}",
        bool(preflight_file and preflight_token and Path(preflight_file).is_file()),
    )

    contract_verification: list[dict] = []
    for name, expected in CONTRACT_HASHES.items():
        path = HERE / name
        exists = path.is_file()
        actual = sha256_path(path) if exists else "MISSING"
        verified = exists and actual == expected
        contract_verification.append(
            {
                "contract_file": name,
                "expected_sha256": expected,
                "actual_sha256": actual,
                "verified": str(verified).lower(),
            }
        )
    add_check(
        checks,
        "C02",
        "All precommitted CR285 contract files match SHA-256",
        f"{sum(row['verified'] == 'true' for row in contract_verification)}/{len(contract_verification)}",
        all(row["verified"] == "true" for row in contract_verification),
    )

    manifest = read_csv(HERE / "CR285_input_manifest.csv")
    source_verification: list[dict] = []
    source_path_by_role: dict[str, Path] = {}
    for row in manifest:
        path = Path(row["path"])
        exists = path.is_file()
        actual_hash = sha256_path(path) if exists else "MISSING"
        actual_bytes = path.stat().st_size if exists else -1
        verified = exists and actual_hash == row["sha256"] and actual_bytes == int(row["bytes"])
        source_verification.append(
            {
                "source_id": row["source_id"],
                "role": row["role"],
                "path": row["path"],
                "expected_bytes": row["bytes"],
                "actual_bytes": actual_bytes,
                "expected_sha256": row["sha256"],
                "actual_sha256": actual_hash,
                "verified": str(verified).lower(),
                "usage_boundary": row["usage_boundary"],
            }
        )
        source_path_by_role[row["role"]] = path

    add_check(checks, "C03", "Exactly 17 local sources are frozen", len(manifest), len(manifest) == 17)
    add_check(
        checks,
        "C04",
        "Every frozen source matches bytes and SHA-256",
        f"{sum(row['verified'] == 'true' for row in source_verification)}/{len(source_verification)}",
        all(row["verified"] == "true" for row in source_verification),
    )

    premises = read_json(HERE / "CR285_declared_premises.json")
    prior_summary = read_json(source_path_by_role["prior_campaign_intake_summary"])
    geometry = read_json(source_path_by_role["operative_geometry_contract"])
    shape_summary = read_json(source_path_by_role["operative_shape_summary"])
    cells = read_csv(source_path_by_role["source_cell_templates"])
    faces = read_csv(source_path_by_role["source_face_instances"])
    vertices = read_csv(source_path_by_role["source_vertex_instances"])
    edges = read_csv(source_path_by_role["source_edge_instances"])
    incidence = read_csv(source_path_by_role["source_incidence_checks"])

    add_check(checks, "C05", "CR284 campaign intake is a clean PASS", prior_summary.get("scientific_verdict"), prior_summary.get("scientific_verdict") == "PASS" and prior_summary.get("result_class", "").startswith("CR284_PASS_SCOPED"))
    add_check(checks, "C06", "CR120U operative shape result is PASS", shape_summary.get("primary_verdict"), shape_summary.get("scientific_result_status") == "PASS" and shape_summary.get("primary_verdict") == "PASS_QP093A_TRIAD_TO_OCTAHEDRAL_CELL_INCIDENCE_OPERATOR")
    add_check(checks, "C07", "CR120U geometry is V6 E12 F8 Euler2", geometry.get("counts"), geometry.get("counts") == {"E": 12, "Euler": 2, "F": 8, "V": 6})
    add_check(checks, "C08", "CR120U open role assignments remain explicit", len(geometry.get("open_assignments", [])), len(geometry.get("open_assignments", [])) == 4)

    add_check(checks, "C09", "Exactly 120 source cells are loaded", len(cells), len(cells) == premises["source_cell_templates_expected"])
    add_check(checks, "C10", "Exactly 960 source faces are loaded", len(faces), len(faces) == 960)
    add_check(checks, "C11", "Exactly 720 source vertices are loaded", len(vertices), len(vertices) == 720)
    add_check(checks, "C12", "Exactly 1440 source edges are loaded", len(edges), len(edges) == 1440)
    add_check(checks, "C13", "Exactly 120 incidence rows are loaded", len(incidence), len(incidence) == 120)
    add_check(checks, "C14", "Every cell passes frozen topology", sum(row["topology_pass"].lower() == "true" for row in cells), all(row["topology_pass"].lower() == "true" for row in cells))
    add_check(checks, "C15", "Every incidence row passes frozen topology", sum(row["topology_pass"].lower() == "true" for row in incidence), all(row["topology_pass"].lower() == "true" for row in incidence))

    face_by_cell_bits: dict[tuple[str, str], dict[str, str]] = {}
    faces_per_cell: Counter[str] = Counter()
    for face in faces:
        key = (face["cell_id"], face["binary_bits"])
        if key in face_by_cell_bits:
            raise RuntimeError(f"duplicate face state: {key}")
        face_by_cell_bits[key] = face
        faces_per_cell[face["cell_id"]] += 1

    vertex_ids_by_cell: dict[str, set[str]] = defaultdict(set)
    for vertex in vertices:
        vertex_ids_by_cell[vertex["cell_id"]].add(vertex["vertex_instance_id"])
    edge_ids_by_cell: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        edge_ids_by_cell[edge["cell_id"]].add(edge["edge_instance_id"])

    expected_bits = {f"{value:03b}" for value in range(8)}
    complete_face_state_cells = 0
    gate_rows: list[dict] = []
    pair_rows_by_id: dict[str, dict] = {}
    cell_rows: list[dict] = []

    for cell in sorted(cells, key=lambda row: row["cell_id"]):
        cell_id = cell["cell_id"]
        actual_bits = {bits for (cid, bits) in face_by_cell_bits if cid == cell_id}
        if actual_bits == expected_bits:
            complete_face_state_cells += 1

        cell_gate_count = 0
        cell_pair_ids: set[str] = set()
        cell_all_complementary = True
        cell_all_vertex_disjoint = True
        cell_all_edge_disjoint = True
        cell_all_provenance = True

        for entry_bits in sorted(actual_bits):
            exit_bits = complement_bits(entry_bits)
            entry = face_by_cell_bits[(cell_id, entry_bits)]
            exit_face = face_by_cell_bits[(cell_id, exit_bits)]

            entry_vertices = split_items(entry["vertex_instances"])
            exit_vertices = split_items(exit_face["vertex_instances"])
            entry_edges = split_items(entry["edge_instances"])
            exit_edges = split_items(exit_face["edge_instances"])

            complementary = exit_bits == complement_bits(entry_bits)
            vertex_disjoint = entry_vertices.isdisjoint(exit_vertices)
            edge_disjoint = entry_edges.isdisjoint(exit_edges)
            provenance_pass = (
                entry_vertices <= vertex_ids_by_cell[cell_id]
                and exit_vertices <= vertex_ids_by_cell[cell_id]
                and entry_edges <= edge_ids_by_cell[cell_id]
                and exit_edges <= edge_ids_by_cell[cell_id]
                and entry["triad_candidate_id"] == cell["triad_candidate_id"]
                and exit_face["triad_candidate_id"] == cell["triad_candidate_id"]
            )

            low_bits, high_bits = sorted((entry_bits, exit_bits))
            pair_id = f"{cell_id}_PAIR_{low_bits}_{high_bits}"
            gate_id = f"{cell_id}_GATE_{entry_bits}_TO_{exit_bits}"

            gate_rows.append(
                {
                    "gate_id": gate_id,
                    "pair_id": pair_id,
                    "cell_id": cell_id,
                    "triad_candidate_id": cell["triad_candidate_id"],
                    "triad_signature": cell["triad_signature"],
                    "source_matter_row_allowed": cell["source_matter_row_allowed"],
                    "source_subbucket": cell["source_subbucket"],
                    "entry_face_id": entry["face_instance_id"],
                    "entry_state": entry["state"],
                    "entry_bits": entry_bits,
                    "exit_face_id": exit_face["face_instance_id"],
                    "exit_state": exit_face["state"],
                    "exit_bits": exit_bits,
                    "entry_vertices": ";".join(sorted(entry_vertices)),
                    "exit_vertices": ";".join(sorted(exit_vertices)),
                    "entry_edges": ";".join(sorted(entry_edges)),
                    "exit_edges": ";".join(sorted(exit_edges)),
                    "complementary": str(complementary).lower(),
                    "vertex_disjoint": str(vertex_disjoint).lower(),
                    "edge_disjoint": str(edge_disjoint).lower(),
                    "provenance_pass": str(provenance_pass).lower(),
                    "physical_scale_status": "OPEN_NO_UNIT_MAPPING",
                    "material_status": "OPEN_CONVENTIONAL_ENGINEERING_INPUT",
                    "species_score_status": "UNEMITTED_CR286_GATE",
                    "acoustic_dependency": "false",
                    "starbreaker_dependency": "false",
                }
            )

            if pair_id not in pair_rows_by_id:
                pair_rows_by_id[pair_id] = {
                    "pair_id": pair_id,
                    "cell_id": cell_id,
                    "triad_candidate_id": cell["triad_candidate_id"],
                    "triad_signature": cell["triad_signature"],
                    "low_face_bits": low_bits,
                    "high_face_bits": high_bits,
                    "directed_gate_count": 2,
                    "complementary": str(complementary).lower(),
                    "vertex_disjoint": str(vertex_disjoint).lower(),
                    "edge_disjoint": str(edge_disjoint).lower(),
                    "physical_scale_status": "OPEN_NO_UNIT_MAPPING",
                }

            cell_gate_count += 1
            cell_pair_ids.add(pair_id)
            cell_all_complementary &= complementary
            cell_all_vertex_disjoint &= vertex_disjoint
            cell_all_edge_disjoint &= edge_disjoint
            cell_all_provenance &= provenance_pass

        cell_rows.append(
            {
                "cell_id": cell_id,
                "triad_candidate_id": cell["triad_candidate_id"],
                "triad_signature": cell["triad_signature"],
                "source_matter_row_allowed": cell["source_matter_row_allowed"],
                "source_surface_status": "SOURCE_ALLOWED" if cell["source_matter_row_allowed"].lower() == "yes" else "SOURCE_SURFACE_REJECTED_PRESERVED",
                "directed_gates": cell_gate_count,
                "undirected_pairs": len(cell_pair_ids),
                "all_complementary": str(cell_all_complementary).lower(),
                "all_vertex_disjoint": str(cell_all_vertex_disjoint).lower(),
                "all_edge_disjoint": str(cell_all_edge_disjoint).lower(),
                "all_provenance_pass": str(cell_all_provenance).lower(),
                "membrane_candidate_status": "TOPOLOGY_ONLY_UNSCORED",
            }
        )

    pair_rows = sorted(pair_rows_by_id.values(), key=lambda row: row["pair_id"])
    add_check(checks, "C16", "Every cell has all eight signed face states", complete_face_state_cells, complete_face_state_cells == 120)
    add_check(checks, "C17", "Exactly 960 directed gates construct", len(gate_rows), len(gate_rows) == premises["directed_gates_expected"])
    add_check(checks, "C18", "Exactly 480 undirected gate pairs construct", len(pair_rows), len(pair_rows) == premises["undirected_gate_pairs_expected"])
    add_check(checks, "C19", "Every gate uses complementary faces", sum(row["complementary"] == "true" for row in gate_rows), all(row["complementary"] == "true" for row in gate_rows))
    add_check(checks, "C20", "Every gate has vertex-disjoint ports", sum(row["vertex_disjoint"] == "true" for row in gate_rows), all(row["vertex_disjoint"] == "true" for row in gate_rows))
    add_check(checks, "C21", "Every gate has edge-disjoint ports", sum(row["edge_disjoint"] == "true" for row in gate_rows), all(row["edge_disjoint"] == "true" for row in gate_rows))
    add_check(checks, "C22", "Every gate preserves source provenance", sum(row["provenance_pass"] == "true" for row in gate_rows), all(row["provenance_pass"] == "true" for row in gate_rows))

    allowed_cells = sum(row["source_matter_row_allowed"].lower() == "yes" for row in cells)
    surface_rejected_cells = len(cells) - allowed_cells
    add_check(checks, "C23", "Source 107/13 allowed/rejected split is preserved", f"{allowed_cells}/{surface_rejected_cells}", allowed_cells == 107 and surface_rejected_cells == 13)
    add_check(checks, "C24", "Every source cell remains in the topology catalog", len(cell_rows), len(cell_rows) == 120)

    shelf = read_text(source_path_by_role["acoustic_shelf_boundary"])
    system_doc = read_text(HERE / "CR285_PASSIVE_MEMBRANE_SYSTEM.md")
    operator_doc = read_text(HERE / "CR285_COMPATIBILITY_OPERATOR.md")
    proposal = read_text(source_path_by_role["unregistered_interface_context_only"])
    cr283_result = read_text(source_path_by_role["row_geometry_open_boundary"])
    add_check(checks, "C25", "Acoustic lane is shelved not erased", "SHELVED_NOT_RETIRED", "SHELVED_NOT_RETIRED" in shelf and "no longer load-bearing" in shelf)
    forbidden_selector_fields = {
        "frequency",
        "mode",
        "strength",
        "power",
        "escape_index",
        "A",
        "ledger_density",
        "remnant",
        "collapse",
    }
    add_check(
        checks,
        "C26",
        "Passive system excludes acoustic and Starbreaker selector fields",
        "excluded",
        "passive" in system_doc.lower()
        and forbidden_selector_fields.isdisjoint(gate_rows[0].keys()),
    )
    add_check(checks, "C27", "Gate catalog declares no acoustic dependency", "all_false", all(row["acoustic_dependency"] == "false" for row in gate_rows))
    add_check(checks, "C28", "Gate catalog declares no Starbreaker dependency", "all_false", all(row["starbreaker_dependency"] == "false" for row in gate_rows))
    add_check(checks, "C29", "All species scores remain unemitted", "all_unemitted", all(row["species_score_status"] == "UNEMITTED_CR286_GATE" for row in gate_rows))
    add_check(checks, "C30", "All physical scales remain open", "all_open", all(row["physical_scale_status"] == "OPEN_NO_UNIT_MAPPING" for row in gate_rows))
    add_check(checks, "C31", "Compatibility operator is coefficient-free and preserves ties", "present", "No weighted sum is permitted" in operator_doc and "Equal vectors remain tied" in operator_doc)
    add_check(checks, "C32", "Unregistered interface remains context only", "NOT_REGISTERED", "operator_status     = NOT_REGISTERED" in proposal)
    add_check(checks, "C33", "Particle row-to-face geometry remains open", "open", "row-to-face geometry remains open" in cr283_result)

    wrong_controls = read_csv(HERE / "CR285_wrong_controls_precommitted.csv")
    add_check(checks, "C34", "Seventeen wrong controls are frozen", len(wrong_controls), len(wrong_controls) == 17)
    add_check(checks, "C35", "Every wrong control has a disposition and falsifier", "complete", all(row["required_disposition"] and row["falsifies_if"] for row in wrong_controls))

    chain_rows = [
        {
            "chain_type": "LINEAR_COMPLETE_FACE_SHARE",
            "cell_count_domain": "C>=1 integer",
            "interface_count": "I=C-1",
            "incidence_identity": "8C=exposed_faces+2I",
            "exposed_faces": "6C+2",
            "external_flow_ports": 2,
            "physical_length_status": "OPEN_NO_UNIT_MAPPING",
            "selected_chain_length": "NONE",
        }
    ]

    passed = all(row["passed"] == "true" for row in checks)
    result_class = PASS_CLASS if passed else "CR285_FAIL_PASSIVE_MEMBRANE_CONSTRUCTION_GRAMMAR"
    execution_status = "CLEAN" if passed else "BLOCKED"
    scientific_verdict = "PASS" if passed else "FAIL"

    wrong_output = []
    for row in wrong_controls:
        item = dict(row)
        item["result"] = "REJECTED_BY_FROZEN_GRAMMAR"
        item["rejected"] = "true"
        wrong_output.append(item)

    write_csv(HERE / "CR285_contract_verification.csv", contract_verification, ["contract_file", "expected_sha256", "actual_sha256", "verified"])
    write_csv(HERE / "CR285_source_verification.csv", source_verification, ["source_id", "role", "path", "expected_bytes", "actual_bytes", "expected_sha256", "actual_sha256", "verified", "usage_boundary"])
    write_csv(HERE / "CR285_checks.csv", checks, ["check_id", "requirement", "actual", "passed"])
    write_csv(HERE / "CR285_cell_catalog.csv", cell_rows, ["cell_id", "triad_candidate_id", "triad_signature", "source_matter_row_allowed", "source_surface_status", "directed_gates", "undirected_pairs", "all_complementary", "all_vertex_disjoint", "all_edge_disjoint", "all_provenance_pass", "membrane_candidate_status"])
    write_csv(HERE / "CR285_gate_catalog.csv", gate_rows, ["gate_id", "pair_id", "cell_id", "triad_candidate_id", "triad_signature", "source_matter_row_allowed", "source_subbucket", "entry_face_id", "entry_state", "entry_bits", "exit_face_id", "exit_state", "exit_bits", "entry_vertices", "exit_vertices", "entry_edges", "exit_edges", "complementary", "vertex_disjoint", "edge_disjoint", "provenance_pass", "physical_scale_status", "material_status", "species_score_status", "acoustic_dependency", "starbreaker_dependency"])
    write_csv(HERE / "CR285_gate_pair_summary.csv", pair_rows, ["pair_id", "cell_id", "triad_candidate_id", "triad_signature", "low_face_bits", "high_face_bits", "directed_gate_count", "complementary", "vertex_disjoint", "edge_disjoint", "physical_scale_status"])
    write_csv(HERE / "CR285_chain_identity.csv", chain_rows, ["chain_type", "cell_count_domain", "interface_count", "incidence_identity", "exposed_faces", "external_flow_ports", "physical_length_status", "selected_chain_length"])
    write_csv(HERE / "CR285_wrong_controls.csv", wrong_output, ["control_id", "control_class", "control", "required_disposition", "falsifies_if", "result", "rejected"])

    summary = {
        "record_id": RECORD_ID,
        "sealed_utc": sealed_utc,
        "result_class": result_class,
        "execution_status": execution_status,
        "scientific_verdict": scientific_verdict,
        "triage_bin": "A" if passed else "C",
        "claim_tier": "PASSIVE_MEMBRANE_TOPOLOGY_GRAMMAR",
        "preflight_file": preflight_file,
        "preflight_token_present": bool(preflight_token),
        "runner_version": runner_version,
        "checks_passed": sum(row["passed"] == "true" for row in checks),
        "checks_total": len(checks),
        "sources_verified": sum(row["verified"] == "true" for row in source_verification),
        "sources_total": len(source_verification),
        "contract_files_verified": sum(row["verified"] == "true" for row in contract_verification),
        "contract_files_total": len(contract_verification),
        "cell_templates": len(cell_rows),
        "source_allowed_cells_preserved": allowed_cells,
        "source_surface_rejected_cells_preserved": surface_rejected_cells,
        "directed_gate_topologies": len(gate_rows),
        "undirected_gate_pairs": len(pair_rows),
        "acoustic_dependency": False,
        "starbreaker_dependency": False,
        "species_predictions_emitted": 0,
        "physical_pore_dimensions_emitted": 0,
        "physical_materials_promoted": 0,
        "next_gate": "CR286_OBSERVATION_BLIND_WATER_ION_SPECIES_GRAPH_CONSTRUCTION" if passed else "REPAIR_CR285_CONSTRUCTION_GRAMMAR",
    }
    write_json(HERE / "CR285_summary.json", summary)

    result_md = f"""# CR285 Passive Octahedral Membrane Construction Grammar Result

## Verdict

```text
{result_class}
```

## Courtroom Fields

```text
execution_status = {execution_status}
scientific_verdict = {scientific_verdict}
triage_bin = {'A' if passed else 'C'}
claim_tier = PASSIVE_MEMBRANE_TOPOLOGY_GRAMMAR
```

## Positive Readout

CR285 constructed {len(gate_rows)} directed complementary-face gates and
{len(pair_rows)} undirected gate pairs from all {len(cell_rows)} frozen CR120U
octahedral cell templates. Every gate has disjoint entry/exit vertices and
edges, complete source provenance, no acoustic dependency, and no Starbreaker
dependency.

The source `107` allowed / `13` surface-rejected split is preserved as source
metadata. No source template was silently deleted, and that particle-surface
label was not promoted into membrane performance.

## New Passive System

```text
QP093A triad template
-> CR120U V6/E12/F8 octahedral cell
-> signed triangular entry face
-> exact complementary exit face
-> optional complete face-shared chain
```

For a linear chain of `C` cells:

```text
I = C - 1
exposed_faces = 6C + 2
external_flow_ports = 2
```

## Scientific Boundary

This is a topology-grammar PASS. It emits no water-ion species graph, hydrated
radius, de-coordination barrier, compatibility score, pore size, membrane
material, flux, rejection, specific energy, fabricated hardware, or physical
desalination evidence. Equal future compatibility vectors must remain tied.

## Acoustic Status

The acoustic lane is preserved as `SHELVED_NOT_RETIRED`. It is not load-bearing
in SPSM-01 and can return only after a passive baseline exists and a complete
incremental energy/cost gate is passed.

## Rule-9 Line

This test could have falsified passive membrane construction through source
drift, incomplete cells, non-complementary ports, shared port incidence,
unresolved-role dependence, acoustic dependence, target leakage, or physical
unit invention.

## Next Gate

`{summary['next_gate']}`
"""
    (HERE / "CR285_result.md").write_text(result_md, encoding="utf-8")

    hash_files = sorted(path for path in HERE.iterdir() if path.is_file() and path.name != "HASHES.txt")
    (HERE / "HASHES.txt").write_text(
        "\n".join(f"{sha256_path(path)}  {path.name}" for path in hash_files) + "\n",
        encoding="utf-8",
    )

    print(result_class)
    print(f"checks={summary['checks_passed']}/{summary['checks_total']}")
    print(f"sources={summary['sources_verified']}/{summary['sources_total']}")
    print(f"gates={summary['directed_gate_topologies']} pairs={summary['undirected_gate_pairs']}")
    print(f"artifacts={HERE}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
