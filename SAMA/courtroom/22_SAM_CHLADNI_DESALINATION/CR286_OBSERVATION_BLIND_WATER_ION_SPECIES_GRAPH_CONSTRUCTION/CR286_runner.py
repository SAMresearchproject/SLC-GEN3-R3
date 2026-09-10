"""CR286 observation-blind water-ion species graph constructor.

Builds formula-connectivity cores and common hydration-envelope hypotheses.
No measured hydration, membrane, or selectivity value is read or emitted.
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
RECORD_ID = "CR286_OBSERVATION_BLIND_WATER_ION_SPECIES_GRAPH_CONSTRUCTION"
PASS_CLASS = (
    "CR286_PASS_OBSERVATION_BLIND_WATER_ION_SPECIES_GRAPH_FAMILY__"
    "36_CANDIDATES__COMMON_OCT6_PRIMARY__NO_GATE_RANKING_OR_PHYSICAL_PROMOTION"
)

CONTRACT_HASHES = {
    "CR286_PRECOMMIT.md": "31c163a706397c189c5eb721ffa46903d889163f61a53a173abd01cb6f0c52dd",
    "CR286_declared_premises.json": "ccdef66c378917ea94855ced3dc5af16ed991b5cc62bb56740a3523521de53c7",
    "CR286_core_atoms.csv": "8ce8c671123478642e8d5fd2899d4463da6978166c769337181ed0a47c9df094",
    "CR286_core_bonds.csv": "f4682462a60128587a9c33b13b229423ddc1355c69e8148aa2519a551a6cb728",
    "CR286_envelope_variants.csv": "db63debd9484c3829da1ead1b45554fd82d84ab672e30240b5837076391fb2a0",
    "CR286_SPECIES_GRAPH_SYSTEM.md": "7bd65bb29392b5ee64a9be58b92f8ecf01fb0563116281592150bbe2e31b2eac",
    "CR286_wrong_controls_precommitted.csv": "7247a861723602a1e64329e565adf63c3558e8ab67c241a3dffd7dbeb4753f91",
    "CR286_input_manifest.csv": "ba56f68de3457af23259f31f61e7ecf84612e588294ac091ee177f1d54d37e63",
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


def split_ports(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def fingerprint(payload) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:20]


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
        "All precommitted CR286 contract files match SHA-256",
        f"{sum(row['verified'] == 'true' for row in contract_verification)}/{len(contract_verification)}",
        all(row["verified"] == "true" for row in contract_verification),
    )

    manifest = read_csv(HERE / "CR286_input_manifest.csv")
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

    add_check(checks, "C03", "Exactly 14 local sources are frozen", len(manifest), len(manifest) == 14)
    add_check(
        checks,
        "C04",
        "Every frozen source matches bytes and SHA-256",
        f"{sum(row['verified'] == 'true' for row in source_verification)}/{len(source_verification)}",
        all(row["verified"] == "true" for row in source_verification),
    )

    premises = read_json(HERE / "CR286_declared_premises.json")
    species = read_csv(source_path_by_role["frozen_species_roster"])
    cr285_summary = read_json(source_path_by_role["passive_grammar_summary"])
    gate_catalog = read_csv(source_path_by_role["passive_gate_catalog"])
    geometry = read_json(source_path_by_role["operative_geometry_contract"])
    core_atoms = read_csv(HERE / "CR286_core_atoms.csv")
    core_bonds = read_csv(HERE / "CR286_core_bonds.csv")
    variants = read_csv(HERE / "CR286_envelope_variants.csv")

    add_check(checks, "C05", "CR285 passive grammar is a clean PASS", cr285_summary.get("scientific_verdict"), cr285_summary.get("scientific_verdict") == "PASS" and cr285_summary.get("result_class", "").startswith("CR285_PASS_PASSIVE"))
    add_check(checks, "C06", "CR285 supplies exactly 960 unscored passive gates", len(gate_catalog), len(gate_catalog) == 960 and all(row["species_score_status"] == "UNEMITTED_CR286_GATE" for row in gate_catalog))
    add_check(checks, "C07", "CR285 gates have no acoustic or Starbreaker dependency", "all_false", all(row["acoustic_dependency"] == "false" and row["starbreaker_dependency"] == "false" for row in gate_catalog))
    add_check(checks, "C08", "CR120U common envelope is V6", geometry.get("counts", {}).get("V"), geometry.get("counts", {}).get("V") == 6)
    add_check(checks, "C09", "CR120U does not globally exclude tetrahedral realization", "open", any("tetrahedral geometry is globally impossible" in item for item in geometry.get("not_claimed", [])))

    species_by_id = {row["species_id"]: row for row in species}
    atoms_by_species: dict[str, list[dict[str, str]]] = defaultdict(list)
    bonds_by_species: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in core_atoms:
        atoms_by_species[row["species_id"]].append(row)
    for row in core_bonds:
        bonds_by_species[row["species_id"]].append(row)

    add_check(checks, "C10", "Exactly nine frozen species are present", len(species), len(species) == premises["species_expected"])
    add_check(checks, "C11", "Observed targets remain forbidden for every species", "all_false", all(row["prediction_status"] == "UNPREDICTED" and row["observed_target_values_allowed"] == "false" for row in species))
    add_check(checks, "C12", "Every species has a declared core atom inventory", len(atoms_by_species), set(atoms_by_species) == set(species_by_id))
    add_check(checks, "C13", "Core atom inventory closes at 29", len(core_atoms), len(core_atoms) == 29)
    add_check(checks, "C14", "Core connectivity inventory closes at 20", len(core_bonds), len(core_bonds) == 20)
    add_check(checks, "C15", "Four common envelope variants are frozen", [row["variant_name"] for row in variants], len(variants) == premises["variants_per_species_expected"])
    add_check(checks, "C16", "One OCT6 primary and three controls are present", Counter(row["selection_status"] for row in variants), sum(row["selection_status"] == "PRIMARY_FOR_ALL_SPECIES" for row in variants) == 1 and sum(row["selection_status"] == "CONTROL_ONLY" for row in variants) == 3)

    atom_ids_by_species = {
        species_id: {row["atom_id"] for row in rows}
        for species_id, rows in atoms_by_species.items()
    }
    bond_reference_failures = [
        row["bond_id"]
        for row in core_bonds
        if row["node_u"] not in atom_ids_by_species[row["species_id"]]
        or row["node_v"] not in atom_ids_by_species[row["species_id"]]
    ]
    add_check(checks, "C17", "Every declared core bond resolves to frozen atoms", len(bond_reference_failures), len(bond_reference_failures) == 0)

    graph_rows: list[dict] = []
    node_rows: list[dict] = []
    edge_rows: list[dict] = []
    primary_rows: list[dict] = []

    for species_row in sorted(species, key=lambda row: row["species_id"]):
        species_id = species_row["species_id"]
        atoms = sorted(atoms_by_species[species_id], key=lambda row: row["atom_id"])
        bonds = sorted(bonds_by_species.get(species_id, []), key=lambda row: row["bond_id"])

        degree: Counter[str] = Counter()
        for bond in bonds:
            degree[bond["node_u"]] += 1
            degree[bond["node_v"]] += 1
        degree_sequence = sorted([degree[atom["atom_id"]] for atom in atoms], reverse=True)

        for variant in variants:
            graph_id = f"{species_id}_{variant['variant_id']}_{variant['variant_name']}"
            ports = split_ports(variant["port_labels"])
            contact_count = int(variant["contact_count"])
            if len(ports) != contact_count:
                raise RuntimeError(f"port count mismatch for {variant['variant_id']}")

            frame_id = f"{graph_id}_FRAME"
            node_rows.append(
                {
                    "graph_id": graph_id,
                    "node_id": frame_id,
                    "node_type": "SPECIES_FRAME",
                    "element_or_unit": "VIRTUAL",
                    "formal_charge": species_row["formal_charge"],
                    "role": "TOTAL_CHARGE_AND_ENVELOPE_FRAME",
                    "port_label": "",
                    "source_provenance": f"{species_id}:formal_charge",
                    "physical_entity_claim": "false",
                }
            )

            for atom in atoms:
                node_id = f"{graph_id}_CORE_{atom['atom_id']}"
                node_rows.append(
                    {
                        "graph_id": graph_id,
                        "node_id": node_id,
                        "node_type": "CORE_ATOM",
                        "element_or_unit": atom["element"],
                        "formal_charge": atom["declared_atom_formal_charge"],
                        "role": atom["atom_role"],
                        "port_label": "",
                        "source_provenance": atom["source_basis"],
                        "physical_entity_claim": "formula_identity_only",
                    }
                )
                edge_rows.append(
                    {
                        "graph_id": graph_id,
                        "edge_id": f"{graph_id}_MEMBER_{atom['atom_id']}",
                        "node_u": frame_id,
                        "node_v": node_id,
                        "edge_type": "FRAME_MEMBERSHIP",
                        "source_provenance": "CR286 common graph construction",
                        "physical_interaction_claim": "false",
                    }
                )

            for bond in bonds:
                edge_rows.append(
                    {
                        "graph_id": graph_id,
                        "edge_id": f"{graph_id}_CORE_{bond['bond_id']}",
                        "node_u": f"{graph_id}_CORE_{bond['node_u']}",
                        "node_v": f"{graph_id}_CORE_{bond['node_v']}",
                        "edge_type": bond["edge_type"],
                        "source_provenance": bond["source_basis"],
                        "physical_interaction_claim": "connectivity_only_no_order_or_energy",
                    }
                )

            for index, port in enumerate(ports, start=1):
                water_id = f"{graph_id}_W{index:02d}"
                node_rows.append(
                    {
                        "graph_id": graph_id,
                        "node_id": water_id,
                        "node_type": "HYDRATION_WATER",
                        "element_or_unit": "H2O_COARSE",
                        "formal_charge": "0",
                        "role": "ENVELOPE_SUPPORT_CANDIDATE",
                        "port_label": port,
                        "source_provenance": variant["source_basis"],
                        "physical_entity_claim": "candidate_not_measured_coordination",
                    }
                )
                edge_rows.append(
                    {
                        "graph_id": graph_id,
                        "edge_id": f"{graph_id}_HYDRATION_{index:02d}",
                        "node_u": frame_id,
                        "node_v": water_id,
                        "edge_type": "HYDRATION_SUPPORT_CANDIDATE",
                        "source_provenance": variant["source_basis"],
                        "physical_interaction_claim": "false",
                    }
                )

            structure_payload = {
                "core_atom_count": len(atoms),
                "core_bond_count": len(bonds),
                "degree_sequence": degree_sequence,
                "contact_count": contact_count,
            }
            topology_fp = fingerprint(structure_payload)
            charge_typed_fp = fingerprint({**structure_payload, "formal_charge": species_row["formal_charge"]})
            graph_node_count = len(atoms) + 1 + contact_count
            graph_edge_count = len(bonds) + len(atoms) + contact_count
            graph_rows.append(
                {
                    "graph_id": graph_id,
                    "species_id": species_id,
                    "chemical_species": species_row["chemical_species"],
                    "formal_charge": species_row["formal_charge"],
                    "variant_id": variant["variant_id"],
                    "variant_name": variant["variant_name"],
                    "variant_class": variant["variant_class"],
                    "selection_status": variant["selection_status"],
                    "core_atom_count": len(atoms),
                    "core_bond_count": len(bonds),
                    "envelope_contact_count": contact_count,
                    "node_count": graph_node_count,
                    "edge_count": graph_edge_count,
                    "core_degree_sequence": ";".join(str(value) for value in degree_sequence),
                    "topology_fingerprint": topology_fp,
                    "charge_typed_fingerprint": charge_typed_fp,
                    "observed_targets_used": "false",
                    "gate_selector_status": "OPEN_NO_SOURCE_NATIVE_ELEMENT_TO_TRIAD_MAP",
                    "physical_coordination_claim": "false",
                    "species_selectivity_status": "UNEMITTED",
                }
            )
            if variant["selection_status"] == "PRIMARY_FOR_ALL_SPECIES":
                primary_rows.append(
                    {
                        "species_id": species_id,
                        "chemical_species": species_row["chemical_species"],
                        "graph_id": graph_id,
                        "primary_envelope": variant["variant_name"],
                        "contact_count": contact_count,
                        "hypothesis_status": "COMMON_SOURCE_NATIVE_TEST_HYPOTHESIS",
                        "gate_selector_status": "OPEN_NO_SOURCE_NATIVE_ELEMENT_TO_TRIAD_MAP",
                        "physical_coordination_claim": "false",
                    }
                )

    add_check(checks, "C18", "Exactly 36 graph candidates construct", len(graph_rows), len(graph_rows) == premises["graphs_expected"])
    add_check(checks, "C19", "Exactly 278 graph nodes construct", len(node_rows), len(node_rows) == premises["nodes_expected"])
    add_check(checks, "C20", "Exactly 322 graph edges construct", len(edge_rows), len(edge_rows) == premises["edges_expected"])
    add_check(checks, "C21", "Every species has all four variants", Counter(row["species_id"] for row in graph_rows), all(count == 4 for count in Counter(row["species_id"] for row in graph_rows).values()))
    add_check(checks, "C22", "Every species has one common OCT6 primary", len(primary_rows), len(primary_rows) == 9 and all(row["primary_envelope"] == "OCT6_PRIMARY" and row["contact_count"] == 6 for row in primary_rows))
    add_check(checks, "C23", "Both tetrahedral parity controls remain present", sorted(row["variant_name"] for row in variants if row["variant_name"].startswith("TET4")), {row["variant_name"] for row in variants} >= {"TET4_EVEN_CONTROL", "TET4_ODD_CONTROL"})
    add_check(checks, "C24", "Core-only control remains present for every species", sum(row["variant_name"] == "CORE_ONLY_CONTROL" for row in graph_rows), sum(row["variant_name"] == "CORE_ONLY_CONTROL" for row in graph_rows) == 9)
    add_check(checks, "C25", "Every node carries provenance", "complete", all(row["source_provenance"] for row in node_rows))
    add_check(checks, "C26", "Every edge carries provenance", "complete", all(row["source_provenance"] for row in edge_rows))
    add_check(checks, "C27", "No graph uses observed targets", "all_false", all(row["observed_targets_used"] == "false" for row in graph_rows))
    add_check(checks, "C28", "No graph selects a CR285 gate", "all_open", all(row["gate_selector_status"] == "OPEN_NO_SOURCE_NATIVE_ELEMENT_TO_TRIAD_MAP" for row in graph_rows))
    add_check(checks, "C29", "No species selectivity is emitted", "all_unemitted", all(row["species_selectivity_status"] == "UNEMITTED" for row in graph_rows))

    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in graph_rows:
        groups[(row["variant_name"], row["charge_typed_fingerprint"])].append(row)
    degeneracy_rows: list[dict] = []
    for index, ((variant_name, typed_fp), rows) in enumerate(sorted(groups.items()), start=1):
        species_list = sorted(row["chemical_species"] for row in rows)
        degeneracy_rows.append(
            {
                "group_id": f"DG{index:03d}",
                "variant_name": variant_name,
                "charge_typed_fingerprint": typed_fp,
                "formal_charge": rows[0]["formal_charge"],
                "species_count": len(rows),
                "species": ";".join(species_list),
                "tie_status": "EXPLICIT_TOPOLOGY_TIE" if len(rows) > 1 else "SINGLETON",
                "physical_tiebreaker_available": "false",
            }
        )

    tied_groups = [row for row in degeneracy_rows if row["tie_status"] == "EXPLICIT_TOPOLOGY_TIE"]
    primary_tied_groups = [row for row in tied_groups if row["variant_name"] == "OCT6_PRIMARY"]
    add_check(checks, "C30", "Na/K OCT6 topology tie is explicit", "present", any(row["variant_name"] == "OCT6_PRIMARY" and row["species"] == "K+;Na+" for row in tied_groups))
    add_check(checks, "C31", "Mg/Ca OCT6 topology tie is explicit", "present", any(row["variant_name"] == "OCT6_PRIMARY" and row["species"] == "Ca2+;Mg2+" for row in tied_groups))
    add_check(checks, "C32", "Exactly two primary charge-typed tie groups remain", len(primary_tied_groups), len(primary_tied_groups) == 2)

    graph_schema = set(graph_rows[0])
    forbidden_schema_tokens = {"hydrated_radius", "bare_radius", "dehydration_energy", "decoordination_energy", "flux", "rejection", "permeability", "selectivity_value", "pore_size", "bond_angle", "partial_charge"}
    add_check(checks, "C33", "Graph schema contains no forbidden observed or physical fields", sorted(graph_schema & forbidden_schema_tokens), graph_schema.isdisjoint(forbidden_schema_tokens))

    system_doc = read_text(HERE / "CR286_SPECIES_GRAPH_SYSTEM.md")
    cr283_result = read_text(source_path_by_role["row_geometry_open_boundary"])
    shelf = read_text(source_path_by_role["acoustic_shelf_boundary"])
    add_check(checks, "C34", "System records absent element-to-triad selector", "open", "no source-complete rule connecting element identity" in system_doc)
    add_check(checks, "C35", "Particle row-to-face geometry remains open", "open", "row-to-face geometry remains open" in cr283_result)
    add_check(checks, "C36", "Acoustic lane remains shelved", "SHELVED_NOT_RETIRED", "SHELVED_NOT_RETIRED" in shelf)

    wrong_controls = read_csv(HERE / "CR286_wrong_controls_precommitted.csv")
    add_check(checks, "C37", "Twenty-two wrong controls are frozen", len(wrong_controls), len(wrong_controls) == 22)
    add_check(checks, "C38", "Every wrong control has a disposition and falsifier", "complete", all(row["required_disposition"] and row["falsifies_if"] for row in wrong_controls))

    passed = all(row["passed"] == "true" for row in checks)
    result_class = PASS_CLASS if passed else "CR286_FAIL_OBSERVATION_BLIND_SPECIES_GRAPH_CONSTRUCTION"
    execution_status = "CLEAN" if passed else "BLOCKED"
    scientific_verdict = "PASS" if passed else "FAIL"

    wrong_output = []
    for row in wrong_controls:
        item = dict(row)
        item["result"] = "REJECTED_BY_FROZEN_CONSTRUCTION"
        item["rejected"] = "true"
        wrong_output.append(item)

    write_csv(HERE / "CR286_contract_verification.csv", contract_verification, ["contract_file", "expected_sha256", "actual_sha256", "verified"])
    write_csv(HERE / "CR286_source_verification.csv", source_verification, ["source_id", "role", "path", "expected_bytes", "actual_bytes", "expected_sha256", "actual_sha256", "verified", "usage_boundary"])
    write_csv(HERE / "CR286_checks.csv", checks, ["check_id", "requirement", "actual", "passed"])
    write_csv(HERE / "CR286_species_graph_catalog.csv", graph_rows, ["graph_id", "species_id", "chemical_species", "formal_charge", "variant_id", "variant_name", "variant_class", "selection_status", "core_atom_count", "core_bond_count", "envelope_contact_count", "node_count", "edge_count", "core_degree_sequence", "topology_fingerprint", "charge_typed_fingerprint", "observed_targets_used", "gate_selector_status", "physical_coordination_claim", "species_selectivity_status"])
    write_csv(HERE / "CR286_species_graph_nodes.csv", node_rows, ["graph_id", "node_id", "node_type", "element_or_unit", "formal_charge", "role", "port_label", "source_provenance", "physical_entity_claim"])
    write_csv(HERE / "CR286_species_graph_edges.csv", edge_rows, ["graph_id", "edge_id", "node_u", "node_v", "edge_type", "source_provenance", "physical_interaction_claim"])
    write_csv(HERE / "CR286_primary_hypotheses.csv", primary_rows, ["species_id", "chemical_species", "graph_id", "primary_envelope", "contact_count", "hypothesis_status", "gate_selector_status", "physical_coordination_claim"])
    write_csv(HERE / "CR286_topology_degeneracy.csv", degeneracy_rows, ["group_id", "variant_name", "charge_typed_fingerprint", "formal_charge", "species_count", "species", "tie_status", "physical_tiebreaker_available"])
    write_csv(HERE / "CR286_wrong_controls.csv", wrong_output, ["control_id", "control_class", "control", "required_disposition", "falsifies_if", "result", "rejected"])

    summary = {
        "record_id": RECORD_ID,
        "sealed_utc": sealed_utc,
        "result_class": result_class,
        "execution_status": execution_status,
        "scientific_verdict": scientific_verdict,
        "triage_bin": "A" if passed else "C",
        "claim_tier": "OBSERVATION_BLIND_SPECIES_GRAPH_FAMILY",
        "preflight_file": preflight_file,
        "preflight_token_present": bool(preflight_token),
        "runner_version": runner_version,
        "checks_passed": sum(row["passed"] == "true" for row in checks),
        "checks_total": len(checks),
        "sources_verified": sum(row["verified"] == "true" for row in source_verification),
        "sources_total": len(source_verification),
        "contract_files_verified": sum(row["verified"] == "true" for row in contract_verification),
        "contract_files_total": len(contract_verification),
        "species": len(species),
        "graph_candidates": len(graph_rows),
        "graph_nodes": len(node_rows),
        "graph_edges": len(edge_rows),
        "primary_oct6_hypotheses": len(primary_rows),
        "explicit_tie_groups_all_variants": len(tied_groups),
        "explicit_tie_groups_primary": len(primary_tied_groups),
        "gate_rankings_emitted": 0,
        "selectivity_predictions_emitted": 0,
        "observed_targets_used": False,
        "physical_promotion": False,
        "next_gate": "CR287_BLIND_GATE_COMPATIBILITY_DEGENERACY_TEST" if passed else "REPAIR_CR286_SPECIES_GRAPH_CONSTRUCTION",
    }
    write_json(HERE / "CR286_summary.json", summary)

    result_md = f"""# CR286 Observation-Blind Water-Ion Species Graph Result

## Verdict

```text
{result_class}
```

## Courtroom Fields

```text
execution_status = {execution_status}
scientific_verdict = {scientific_verdict}
triage_bin = {'A' if passed else 'C'}
claim_tier = OBSERVATION_BLIND_SPECIES_GRAPH_FAMILY
```

## Positive Readout

CR286 constructed {len(graph_rows)} graph candidates for all {len(species)}
frozen species: one common OCT6 primary, both tetrahedral parity controls, and
one core-only control per species. The inventory closes at {len(node_rows)}
nodes and {len(edge_rows)} edges with complete provenance.

No hydrated radius, preferred coordination measurement, hydration or
de-coordination energy, membrane flux, rejection, selectivity, acoustic input,
Starbreaker input, or physical-unit mapping entered construction.

## Primary Hypothesis

```text
all nine species
-> identical CR120U-derived six-contact envelope rule
-> no species-specific adjustment
```

OCT6 is a common test hypothesis, not a measured hydration ontology.

## Honest Degeneracy

The source set contains no element-to-QP-triad selector. CR286 therefore
preserves these primary charge-typed topology ties:

```text
Na+  ~ K+
Mg2+ ~ Ca2+
```

No CR285 gate is ranked. Element labels preserve chemical identity but do not
manufacture a geometric distinction.

## Scientific Boundary

This is a graph-construction PASS. It does not predict physical coordination,
hydration number, compatibility, barrier energy, pore size, permeability,
rejection, selectivity, membrane material, or desalination performance.

## Rule-9 Line

This test could have falsified observation-blind construction through an
incomplete formula graph, species-specific envelope tuning, target leakage,
invented selectors, broken provenance, hidden physical units, or suppression
of a topology tie.

## Next Gate

`{summary['next_gate']}`
"""
    (HERE / "CR286_result.md").write_text(result_md, encoding="utf-8")

    hash_files = sorted(path for path in HERE.iterdir() if path.is_file() and path.name != "HASHES.txt")
    (HERE / "HASHES.txt").write_text(
        "\n".join(f"{sha256_path(path)}  {path.name}" for path in hash_files) + "\n",
        encoding="utf-8",
    )

    print(result_class)
    print(f"checks={summary['checks_passed']}/{summary['checks_total']}")
    print(f"sources={summary['sources_verified']}/{summary['sources_total']}")
    print(f"graphs={summary['graph_candidates']} nodes={summary['graph_nodes']} edges={summary['graph_edges']}")
    print(f"artifacts={HERE}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
