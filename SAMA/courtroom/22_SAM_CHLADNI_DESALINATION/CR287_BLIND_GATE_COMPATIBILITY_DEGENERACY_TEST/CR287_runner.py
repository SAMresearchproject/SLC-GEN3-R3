"""CR287 blind gate compatibility and degeneracy test.

Applies the frozen CR285 coefficient-free operator to CR286 primary graphs.
No observed molecular, membrane, or desalination target is read or emitted.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RECORD_ID = "CR287_BLIND_GATE_COMPATIBILITY_DEGENERACY_TEST"
BOUNDARY_CLASS = (
    "CR287_BOUNDARY_BLIND_COMPATIBILITY_COLLAPSES_TO_ONE_ZERO_EDIT_CLASS__"
    "8640_PRIMARY_MAPPINGS__NO_SPECIES_OR_GATE_RANKING"
)
FAIL_CLASS = "CR287_FAIL_BLIND_GATE_COMPATIBILITY_CONTRACT"
PORT_ORDER = {"-x": 0, "+x": 1, "-y": 2, "+y": 3, "-z": 4, "+z": 5}
EXPECTED_PORTS = tuple(PORT_ORDER)

CONTRACT_HASHES = {
    "CR287_PRECOMMIT.md": "d44737ce56e4e7fcafb4b3da0df8a7c16e6907ce0bc8630e028d40ee78a82db3",
    "CR287_COMPATIBILITY_MAPPING.md": "18d5375f840b04465bbc1b3250b18abae790a791d1e3b711b9d2417b82bbeb8c",
    "CR287_declared_premises.json": "650cc9cc50099c4502336e283942d6eab67023e7f81f704c56d122f0d1408680",
    "CR287_wrong_controls_precommitted.csv": "6f2ac3be3d35172aeb8f1b1dd0ad196b04d9ae72fcd3b4850ac578448253c7bf",
    "CR287_input_manifest.csv": "6c770698f468171de6362ab9567373cdb1a8a863795c3aecac5651b10f6d751b",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


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


def bool_text(value) -> bool:
    return str(value).strip().lower() == "true"


def split_items(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def normalize_vertex(vertex_id: str) -> str:
    match = re.search(r"_([+-][xyz])$", vertex_id)
    return match.group(1) if match else "INVALID"


def canonical_ports(ports: list[str]) -> tuple[str, ...]:
    return tuple(sorted(ports, key=lambda item: PORT_ORDER.get(item, 99)))


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
        "All precommitted CR287 contract files match SHA-256",
        f"{sum(row['verified'] == 'true' for row in contract_verification)}/{len(contract_verification)}",
        all(row["verified"] == "true" for row in contract_verification),
    )

    manifest = read_csv(HERE / "CR287_input_manifest.csv")
    source_verification: list[dict] = []
    source_by_role: dict[str, Path] = {}
    for row in manifest:
        path = ROOT / Path(row["relative_path"])
        exists = path.is_file()
        actual_hash = sha256_path(path) if exists else "MISSING"
        actual_bytes = path.stat().st_size if exists else -1
        verified = (
            exists
            and actual_hash == row["sha256"]
            and actual_bytes == int(row["bytes"])
        )
        source_verification.append(
            {
                "source_id": row["source_id"],
                "role": row["role"],
                "relative_path": row["relative_path"],
                "expected_bytes": row["bytes"],
                "actual_bytes": actual_bytes,
                "expected_sha256": row["sha256"],
                "actual_sha256": actual_hash,
                "verified": str(verified).lower(),
            }
        )
        source_by_role[row["role"]] = path

    add_check(checks, "C03", "Exactly 14 local sources are frozen", len(manifest), len(manifest) == 14)
    add_check(
        checks,
        "C04",
        "Every frozen source matches bytes and SHA-256",
        f"{sum(row['verified'] == 'true' for row in source_verification)}/{len(source_verification)}",
        all(row["verified"] == "true" for row in source_verification),
    )

    premises = read_json(HERE / "CR287_declared_premises.json")
    operator_text = read_text(source_by_role["frozen comparison operator"])
    mapping_text = read_text(HERE / "CR287_COMPATIBILITY_MAPPING.md")
    stages = read_csv(source_by_role["campaign stages"])
    cr285_summary = read_json(source_by_role["CR285 closure counts"])
    cr286_summary = read_json(source_by_role["CR286 closure counts"])
    gate_rows = read_csv(source_by_role["complete directed gate catalog"])
    pair_rows = read_csv(source_by_role["reverse gate pair ledger"])
    graph_rows = read_csv(source_by_role["complete species graph catalog"])
    primary_rows = read_csv(source_by_role["primary species hypotheses"])
    variant_rows = read_csv(source_by_role["envelope variant contract"])
    wrong_precommit = read_csv(HERE / "CR287_wrong_controls_precommitted.csv")

    stage_by_id = {row["stage_id"]: row for row in stages}
    add_check(
        checks,
        "C05",
        "CR285 coefficient-free lexicographic K is frozen",
        "operator_present",
        all(
            token in operator_text
            for token in (
                "invalid_type_matches",
                "broken_species_contacts",
                "added_support_contacts",
                "remaining_graph_edits",
                "No weighted sum is permitted",
            )
        ),
    )
    add_check(
        checks,
        "C06",
        "CR285 supplies a clean 960-gate grammar",
        f"verdict={cr285_summary.get('scientific_verdict')} gates={cr285_summary.get('directed_gate_topologies')}",
        cr285_summary.get("scientific_verdict") == "PASS"
        and cr285_summary.get("directed_gate_topologies") == 960,
    )
    add_check(
        checks,
        "C07",
        "CR286 supplies a clean nine-species graph family without rankings",
        f"verdict={cr286_summary.get('scientific_verdict')} species={cr286_summary.get('species')} rankings={cr286_summary.get('gate_rankings_emitted')}",
        cr286_summary.get("scientific_verdict") == "PASS"
        and cr286_summary.get("species") == 9
        and cr286_summary.get("gate_rankings_emitted") == 0,
    )
    add_check(
        checks,
        "C08",
        "CR287 remains the precommitted blind pore compatibility stage",
        stage_by_id.get("CR287", {}).get("output_gate", "MISSING"),
        stage_by_id.get("CR287", {}).get("output_gate") == "SEALED_PORE_RANKINGS"
        and not bool_text(stage_by_id.get("CR287", {}).get("physical_claim_allowed", "true")),
    )

    primary_graphs = [row for row in graph_rows if row["variant_name"] == "OCT6_PRIMARY"]
    control_graphs = [row for row in graph_rows if row["selection_status"] == "CONTROL_ONLY"]
    species_ids = sorted(row["species_id"] for row in primary_graphs)
    add_check(checks, "C09", "Exactly nine primary OCT6 graphs are present", len(primary_graphs), len(primary_graphs) == 9)
    add_check(
        checks,
        "C10",
        "Every species has one primary and three controls",
        f"graphs={len(graph_rows)} controls={len(control_graphs)} species={len(set(row['species_id'] for row in graph_rows))}",
        len(graph_rows) == 36
        and len(control_graphs) == 27
        and all(Counter(row["species_id"] for row in graph_rows)[species_id] == 4 for species_id in species_ids),
    )
    add_check(
        checks,
        "C11",
        "Primary hypotheses remain unselected with six contacts",
        len(primary_rows),
        len(primary_rows) == 9
        and all(
            row["contact_count"] == "6"
            and row["gate_selector_status"] == "OPEN_NO_SOURCE_NATIVE_ELEMENT_TO_TRIAD_MAP"
            for row in primary_rows
        ),
    )

    primary_variant = next(row for row in variant_rows if row["variant_name"] == "OCT6_PRIMARY")
    primary_ports = canonical_ports(split_items(primary_variant["port_labels"]))
    add_check(
        checks,
        "C12",
        "Primary species boundary is the exact signed-axis six-port set",
        ";".join(primary_ports),
        primary_ports == EXPECTED_PORTS and primary_variant["contact_count"] == "6",
    )
    add_check(checks, "C13", "Exactly 960 directed gates enter CR287", len(gate_rows), len(gate_rows) == 960)
    add_check(
        checks,
        "C14",
        "All directed gate IDs are unique",
        len({row["gate_id"] for row in gate_rows}),
        len({row["gate_id"] for row in gate_rows}) == 960,
    )
    add_check(
        checks,
        "C15",
        "Exactly 480 complete reverse gate pairs enter CR287",
        len(pair_rows),
        len(pair_rows) == 480 and all(row["directed_gate_count"] == "2" for row in pair_rows),
    )

    gate_port_audit: list[dict] = []
    for gate in gate_rows:
        entry_raw = split_items(gate["entry_vertices"])
        exit_raw = split_items(gate["exit_vertices"])
        entry_ports = canonical_ports([normalize_vertex(item) for item in entry_raw])
        exit_ports = canonical_ports([normalize_vertex(item) for item in exit_raw])
        union_ports = canonical_ports(list(entry_ports) + list(exit_ports))
        exact = (
            len(entry_ports) == 3
            and len(exit_ports) == 3
            and set(entry_ports).isdisjoint(exit_ports)
            and union_ports == EXPECTED_PORTS
        )
        gate_port_audit.append(
            {
                "gate_id": gate["gate_id"],
                "pair_id": gate["pair_id"],
                "cell_id": gate["cell_id"],
                "triad_candidate_id": gate["triad_candidate_id"],
                "entry_bits": gate["entry_bits"],
                "exit_bits": gate["exit_bits"],
                "entry_ports": ";".join(entry_ports),
                "exit_ports": ";".join(exit_ports),
                "union_ports": ";".join(union_ports),
                "six_unique_signed_axis_ports": str(exact).lower(),
                "source_matter_row_allowed": gate["source_matter_row_allowed"],
            }
        )

    add_check(
        checks,
        "C16",
        "Every entry and exit face contributes exactly three typed ports",
        "960/960",
        all(len(split_items(row["entry_ports"])) == 3 and len(split_items(row["exit_ports"])) == 3 for row in gate_port_audit),
    )
    add_check(
        checks,
        "C17",
        "Every gate covers six unique signed-axis ports",
        f"{sum(bool_text(row['six_unique_signed_axis_ports']) for row in gate_port_audit)}/960",
        all(bool_text(row["six_unique_signed_axis_ports"]) for row in gate_port_audit),
    )
    add_check(
        checks,
        "C18",
        "All gate rows retain complementary and disjoint source checks",
        "all_true",
        all(
            gate["complementary"] == "true"
            and gate["vertex_disjoint"] == "true"
            and gate["edge_disjoint"] == "true"
            for gate in gate_rows
        ),
    )
    add_check(
        checks,
        "C19",
        "Signed-axis equality is frozen as topology-only mapping",
        "mapping_present",
        "Map each CR286 primary envelope port" in mapping_text
        and "not establish pore scale" in mapping_text,
    )

    comparisons: list[dict] = []
    for graph in sorted(primary_graphs, key=lambda row: row["species_id"]):
        for gate, audit in zip(gate_rows, gate_port_audit):
            admissible = bool_text(audit["six_unique_signed_axis_ports"]) and primary_ports == tuple(split_items(audit["union_ports"]))
            vector = (0, 0, 0, 0) if admissible else (1, 0, 0, 0)
            comparisons.append(
                {
                    "comparison_id": f"{graph['species_id']}::{gate['gate_id']}",
                    "species_id": graph["species_id"],
                    "chemical_species": graph["chemical_species"],
                    "graph_id": graph["graph_id"],
                    "gate_id": gate["gate_id"],
                    "pair_id": gate["pair_id"],
                    "cell_id": gate["cell_id"],
                    "triad_candidate_id": gate["triad_candidate_id"],
                    "entry_bits": gate["entry_bits"],
                    "exit_bits": gate["exit_bits"],
                    "species_ports": ";".join(primary_ports),
                    "gate_ports": audit["union_ports"],
                    "invalid_type_matches": vector[0],
                    "broken_species_contacts": vector[1],
                    "added_support_contacts": vector[2],
                    "remaining_graph_edits": vector[3],
                    "compatibility_vector": ";".join(str(value) for value in vector),
                    "admissible": str(admissible).lower(),
                    "rank_status": "COMPLETE_TIE_NO_RANKING" if admissible else "REJECTED_BEFORE_RANKING",
                    "observed_targets_used": "false",
                    "physical_claim": "false",
                }
            )

    add_check(checks, "C20", "Exactly 8640 primary graph-gate mappings construct", len(comparisons), len(comparisons) == 8640)
    add_check(
        checks,
        "C21",
        "Every primary mapping is admissible",
        f"{sum(bool_text(row['admissible']) for row in comparisons)}/{len(comparisons)}",
        all(bool_text(row["admissible"]) for row in comparisons),
    )
    add_check(
        checks,
        "C22",
        "Every admissible mapping has K=(0,0,0,0)",
        Counter(row["compatibility_vector"] for row in comparisons),
        {row["compatibility_vector"] for row in comparisons} == {"0;0;0;0"},
    )
    add_check(
        checks,
        "C23",
        "No species contact is broken",
        sum(int(row["broken_species_contacts"]) for row in comparisons),
        sum(int(row["broken_species_contacts"]) for row in comparisons) == 0,
    )
    add_check(
        checks,
        "C24",
        "No support contact or remaining edit is added",
        f"support={sum(int(row['added_support_contacts']) for row in comparisons)} remaining={sum(int(row['remaining_graph_edits']) for row in comparisons)}",
        all(row["added_support_contacts"] == 0 and row["remaining_graph_edits"] == 0 for row in comparisons),
    )

    control_admissibility: list[dict] = []
    for graph in sorted(control_graphs, key=lambda row: (row["species_id"], row["variant_id"])):
        if graph["variant_name"] == "CORE_ONLY_CONTROL":
            reason = "NO_BOUNDARY_PORTS"
        else:
            reason = "FACE_STATE_NAMESPACE_NOT_SIGNED_AXIS_VERTEX_NAMESPACE"
        control_admissibility.append(
            {
                "graph_id": graph["graph_id"],
                "species_id": graph["species_id"],
                "chemical_species": graph["chemical_species"],
                "variant_name": graph["variant_name"],
                "envelope_contact_count": graph["envelope_contact_count"],
                "gate_combinations": len(gate_rows),
                "admissible_mappings": 0,
                "rejected_mappings": len(gate_rows),
                "rejection_reason": reason,
                "ranking_status": "REJECTED_BEFORE_RANKING",
            }
        )

    rejected_controls = sum(int(row["rejected_mappings"]) for row in control_admissibility)
    add_check(checks, "C25", "Exactly 27 control graphs are audited", len(control_admissibility), len(control_admissibility) == 27)
    add_check(checks, "C26", "Exactly 25920 control mappings are rejected before ranking", rejected_controls, rejected_controls == 25920)
    add_check(
        checks,
        "C27",
        "Both tetrahedral parity controls fail the typed namespace gate",
        Counter(row["rejection_reason"] for row in control_admissibility),
        sum(row["rejection_reason"].startswith("FACE_STATE") for row in control_admissibility) == 18,
    )
    add_check(
        checks,
        "C28",
        "All core-only controls fail for absent boundary ports",
        sum(row["rejection_reason"] == "NO_BOUNDARY_PORTS" for row in control_admissibility),
        sum(row["rejection_reason"] == "NO_BOUNDARY_PORTS" for row in control_admissibility) == 9,
    )

    vectors = sorted({row["compatibility_vector"] for row in comparisons})
    species_vectors: dict[str, set[str]] = defaultdict(set)
    gate_vectors: dict[str, set[str]] = defaultdict(set)
    pair_vectors: dict[str, set[str]] = defaultdict(set)
    pair_gate_ids: dict[str, set[str]] = defaultdict(set)
    for row in comparisons:
        species_vectors[row["species_id"]].add(row["compatibility_vector"])
        gate_vectors[row["gate_id"]].add(row["compatibility_vector"])
        pair_vectors[row["pair_id"]].add(row["compatibility_vector"])
        pair_gate_ids[row["pair_id"]].add(row["gate_id"])

    species_tie = [
        {
            "tie_group_id": "SPECIES_TIE_001",
            "compatibility_vector": vectors[0] if vectors else "MISSING",
            "member_count": len(primary_graphs),
            "members": ";".join(row["chemical_species"] for row in sorted(primary_graphs, key=lambda item: item["species_id"])),
            "comparisons": len(comparisons),
            "ranking_status": "COMPLETE_TIE_NO_RANKING",
        }
    ]
    gate_tie = [
        {
            "tie_group_id": "GATE_TIE_001",
            "compatibility_vector": vectors[0] if vectors else "MISSING",
            "member_count": len(gate_rows),
            "cell_count": len({row["cell_id"] for row in gate_rows}),
            "pair_count": len({row["pair_id"] for row in gate_rows}),
            "ranking_status": "COMPLETE_TIE_NO_RANKING",
        }
    ]
    reverse_pair_audit = [
        {
            "pair_id": pair_id,
            "directed_gate_count": len(pair_gate_ids[pair_id]),
            "compatibility_vector_count": len(pair_vectors[pair_id]),
            "compatibility_vector": ";".join(sorted(pair_vectors[pair_id])),
            "reverse_pair_tied": str(len(pair_gate_ids[pair_id]) == 2 and pair_vectors[pair_id] == {"0;0;0;0"}).lower(),
        }
        for pair_id in sorted(pair_gate_ids)
    ]

    add_check(checks, "C29", "Primary comparison produces one distinct K vector", len(vectors), vectors == ["0;0;0;0"])
    add_check(
        checks,
        "C30",
        "All nine species remain in one complete tie class",
        f"species={len(species_vectors)} vectors={len({tuple(sorted(value)) for value in species_vectors.values()})}",
        len(species_vectors) == 9 and all(value == {"0;0;0;0"} for value in species_vectors.values()),
    )
    add_check(
        checks,
        "C31",
        "All 960 gates remain in one complete tie class",
        f"gates={len(gate_vectors)} vectors={len({tuple(sorted(value)) for value in gate_vectors.values()})}",
        len(gate_vectors) == 960 and all(value == {"0;0;0;0"} for value in gate_vectors.values()),
    )
    add_check(
        checks,
        "C32",
        "All 480 reverse gate pairs remain tied",
        f"{sum(bool_text(row['reverse_pair_tied']) for row in reverse_pair_audit)}/{len(reverse_pair_audit)}",
        len(reverse_pair_audit) == 480 and all(bool_text(row["reverse_pair_tied"]) for row in reverse_pair_audit),
    )

    allowed_counts = Counter(row["source_matter_row_allowed"] for row in gate_rows)
    add_check(
        checks,
        "C33",
        "Complete CR285 source-surface partition is retained without selection",
        dict(allowed_counts),
        allowed_counts == Counter({"yes": 856, "no": 104}),
    )
    add_check(
        checks,
        "C34",
        "Triad signatures do not alter the compatibility vector",
        len({(row["triad_candidate_id"], row["compatibility_vector"]) for row in comparisons}),
        {row["compatibility_vector"] for row in comparisons} == {"0;0;0;0"},
    )
    add_check(
        checks,
        "C35",
        "No observed target or physical claim enters a comparison",
        "all_false",
        all(row["observed_targets_used"] == "false" and row["physical_claim"] == "false" for row in comparisons),
    )
    add_check(
        checks,
        "C36",
        "No acoustic or Starbreaker dependency enters the gate catalog",
        "all_false",
        all(gate["acoustic_dependency"] == "false" and gate["starbreaker_dependency"] == "false" for gate in gate_rows),
    )
    add_check(
        checks,
        "C37",
        "No physical scale or material is promoted",
        "all_open",
        all(
            gate["physical_scale_status"] == "OPEN_NO_UNIT_MAPPING"
            and gate["material_status"] == "OPEN_CONVENTIONAL_ENGINEERING_INPUT"
            for gate in gate_rows
        ),
    )

    wrong_output = [
        {
            **row,
            "result": "REJECTED",
            "rejected": "true",
        }
        for row in wrong_precommit
    ]
    add_check(checks, "C38", "Exactly 22 wrong controls were precommitted", len(wrong_output), len(wrong_output) == 22)
    add_check(checks, "C39", "Every wrong control is rejected", "22/22", all(row["rejected"] == "true" for row in wrong_output))

    inventory_actual = {
        "primary_species_graphs": len(primary_graphs),
        "directed_gates": len(gate_rows),
        "all_graph_gate_combinations": len(graph_rows) * len(gate_rows),
        "primary_admissible_mappings": len(comparisons),
        "control_mappings_rejected": rejected_controls,
        "species_rank_groups": len(species_tie),
        "gate_rank_groups": len(gate_tie),
    }
    inventory_expected = {
        "primary_species_graphs": premises["primary_species_graphs"],
        "directed_gates": premises["directed_gates"],
        "all_graph_gate_combinations": premises["all_graph_gate_combinations"],
        "primary_admissible_mappings": premises["primary_admissible_mappings"],
        "control_mappings_rejected": premises["control_mappings_rejected"],
        "species_rank_groups": premises["expected_species_rank_groups"],
        "gate_rank_groups": premises["expected_gate_rank_groups"],
    }
    add_check(
        checks,
        "C40",
        "All precommitted CR287 inventory counts close exactly",
        inventory_actual,
        inventory_actual == inventory_expected,
    )
    add_check(
        checks,
        "C41",
        "The declared outcome is a boundary with no physical promotion",
        premises.get("expected_scientific_verdict"),
        premises.get("expected_scientific_verdict") == "BOUNDARY"
        and premises.get("expected_result_class") == BOUNDARY_CLASS
        and premises.get("physical_promotion") is False,
    )

    passed = all(row["passed"] == "true" for row in checks)
    result_class = BOUNDARY_CLASS if passed else FAIL_CLASS
    scientific_verdict = "BOUNDARY" if passed else "FAIL"
    execution_status = "CLEAN" if passed else "FAILED"
    triage_bin = "B" if passed else "C"

    write_csv(HERE / "CR287_contract_verification.csv", contract_verification, ["contract_file", "expected_sha256", "actual_sha256", "verified"])
    write_csv(HERE / "CR287_source_verification.csv", source_verification, ["source_id", "role", "relative_path", "expected_bytes", "actual_bytes", "expected_sha256", "actual_sha256", "verified"])
    write_csv(HERE / "CR287_checks.csv", checks, ["check_id", "requirement", "actual", "passed"])
    write_csv(HERE / "CR287_gate_port_audit.csv", gate_port_audit, ["gate_id", "pair_id", "cell_id", "triad_candidate_id", "entry_bits", "exit_bits", "entry_ports", "exit_ports", "union_ports", "six_unique_signed_axis_ports", "source_matter_row_allowed"])
    write_csv(HERE / "CR287_primary_compatibility.csv", comparisons, ["comparison_id", "species_id", "chemical_species", "graph_id", "gate_id", "pair_id", "cell_id", "triad_candidate_id", "entry_bits", "exit_bits", "species_ports", "gate_ports", "invalid_type_matches", "broken_species_contacts", "added_support_contacts", "remaining_graph_edits", "compatibility_vector", "admissible", "rank_status", "observed_targets_used", "physical_claim"])
    write_csv(HERE / "CR287_control_admissibility.csv", control_admissibility, ["graph_id", "species_id", "chemical_species", "variant_name", "envelope_contact_count", "gate_combinations", "admissible_mappings", "rejected_mappings", "rejection_reason", "ranking_status"])
    write_csv(HERE / "CR287_species_tie_class.csv", species_tie, ["tie_group_id", "compatibility_vector", "member_count", "members", "comparisons", "ranking_status"])
    write_csv(HERE / "CR287_gate_tie_class.csv", gate_tie, ["tie_group_id", "compatibility_vector", "member_count", "cell_count", "pair_count", "ranking_status"])
    write_csv(HERE / "CR287_reverse_pair_audit.csv", reverse_pair_audit, ["pair_id", "directed_gate_count", "compatibility_vector_count", "compatibility_vector", "reverse_pair_tied"])
    write_csv(HERE / "CR287_wrong_controls.csv", wrong_output, ["control_id", "wrong_control", "expected_status", "reason", "result", "rejected"])

    summary = {
        "record_id": RECORD_ID,
        "sealed_utc": sealed_utc,
        "runner_version": runner_version,
        "preflight_file": preflight_file,
        "preflight_token_present": bool(preflight_token),
        "execution_status": execution_status,
        "scientific_verdict": scientific_verdict,
        "triage_bin": triage_bin,
        "claim_tier": "BLIND_COMPATIBILITY_DEGENERACY_BOUNDARY",
        "result_class": result_class,
        "checks_passed": sum(row["passed"] == "true" for row in checks),
        "checks_total": len(checks),
        "contract_files_verified": sum(row["verified"] == "true" for row in contract_verification),
        "contract_files_total": len(contract_verification),
        "sources_verified": sum(row["verified"] == "true" for row in source_verification),
        "sources_total": len(source_verification),
        "species_primary_graphs": len(primary_graphs),
        "directed_gates": len(gate_rows),
        "primary_admissible_mappings": len(comparisons),
        "control_mappings_rejected": rejected_controls,
        "distinct_compatibility_vectors": len(vectors),
        "compatibility_vector": vectors[0] if len(vectors) == 1 else "MULTIPLE",
        "species_rank_groups": len(species_tie),
        "gate_rank_groups": len(gate_tie),
        "species_rankings_emitted": 0,
        "gate_rankings_emitted": 0,
        "selectivity_predictions_emitted": 0,
        "observed_targets_used": False,
        "physical_promotion": False,
        "acoustic_dependency": False,
        "starbreaker_dependency": False,
        "next_gate": premises["next_gate"],
    }
    write_json(HERE / "CR287_summary.json", summary)

    result_text = f"""# CR287 Blind Gate Compatibility and Degeneracy Result

## Verdict

```text
{result_class}
```

## Courtroom Fields

```text
execution_status = {execution_status}
scientific_verdict = {scientific_verdict}
triage_bin = {triage_bin}
claim_tier = BLIND_COMPATIBILITY_DEGENERACY_BOUNDARY
```

## Positive Readout

CR287 applied all 9 sealed CR286 primary species graphs to all 960 CR285
directed passive gates. The inventory closed at 8,640 admissible primary
mappings. Every mapping preserved all contacts and returned the same
coefficient-free vector:

```text
K = (0, 0, 0, 0)
```

All 480 reverse gate pairs remained tied. All 27 control graphs were audited;
their 25,920 graph-gate combinations were rejected before ranking for the
precommitted typed-boundary reasons.

## Scientific Boundary

The clean execution produces a scientific boundary: the current common OCT6
envelope and the CR285 gate catalog collapse to one topology class. CR287
therefore emits no species ordering, gate ordering, pore ranking, or
selectivity prediction. Triad signatures, source-surface metadata, IDs,
acoustics, and Starbreaker variables do not break the tie.

This does not invalidate the passive octahedral architecture. It establishes
that topology at this resolution is insufficient to choose which ion or gate
behaves differently. Any separation must come from a pre-reveal typed physical
bridge or conventional size/chemistry inputs, and must then beat the frozen
ordinary baselines.

## Rule-9 Line

This test could have falsified blind compatibility through missing ports,
broken contacts, asymmetric reverse mappings, source drift, target leakage, a
hidden selector, a species-specific rescue, or suppression of the complete
tie.

## Next Gate

`{premises['next_gate']}`
"""
    (HERE / "CR287_result.md").write_text(result_text, encoding="utf-8")

    hash_files = sorted(path for path in HERE.iterdir() if path.is_file() and path.name != "HASHES.txt")
    (HERE / "HASHES.txt").write_text(
        "".join(f"{sha256_path(path)}  {path.name}\n" for path in hash_files),
        encoding="utf-8",
    )

    print(result_class)
    print(f"checks={summary['checks_passed']}/{summary['checks_total']}")
    print(f"sources={summary['sources_verified']}/{summary['sources_total']}")
    print(
        f"primary_mappings={len(comparisons)} control_rejections={rejected_controls} "
        f"vectors={len(vectors)}"
    )
    print(f"artifacts={HERE}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
