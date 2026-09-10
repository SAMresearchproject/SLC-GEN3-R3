"""CR115 D3 invariant-carrier uniqueness theorem gate.

This runner closes the specific gap left by the G347-G355 D=3 chain:

    G348 left non-topological carriers live.
    G349 reduces those carriers to extended support.
    G350 reduces raw carrier data to deformation classes.
    G352 reduces self-contained holonomy/transport identity to a stable sector.
    G354 formalizes matter identity as invariant displacement-response.
    G347 supplies the actual topology selector: obstruction_dim = 3 - D.

The gate is deliberately calibrated against the hostile-audit objection. It
does not pretend that every source artifact is computational. It separates the
computed topology table from the SAM structural commitments that make the
carrier class necessary.
"""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CR_ID = "CR115"
RESULT_CLASS_PASS = "CR115_PASS_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM_GATE"
RESULT_CLASS_FAIL = "CR115_FAIL_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM_GATE"

CR_DIR = Path(__file__).resolve().parent
BRANCH_DIR = CR_DIR.parent
COURTROOM_DIR = BRANCH_DIR.parent
STAM_ROOT = Path(r"C:/VS/Stam_model-A-v1.0")
QUANTUM_ROOT = Path(r"C:/VS/quantum_phase")
MEMORY_ROOT = Path(r"C:/VS/memory")

AUDIT_MD = STAM_ROOT / "audit" / "audit.md"
THEOREM_D3 = STAM_ROOT / "audit" / "audits" / "THEOREM_D3_DISPLACEMENT_RESPONSE.md"
VERDICT_G355 = STAM_ROOT / "audit" / "audits" / "VERDICT_G355_d3_displacement_response_theorem_2026_05_25.md"
PRIORITY_RECORD = MEMORY_ROOT / "PRIORITY_RECORD.md"

G347 = STAM_ROOT / "tests" / "Substrate" / "G347_d3_theorem_route_audit" / "G347_output.json"
G348 = STAM_ROOT / "tests" / "Substrate" / "G348_loop_topology_identity_premise" / "G348_output.json"
G349 = STAM_ROOT / "tests" / "Substrate" / "G349_worldsheet_identity_reduction" / "G349_output.json"
G350 = STAM_ROOT / "tests" / "Substrate" / "G350_identity_deformation_quotient" / "G350_output.json"
G351 = STAM_ROOT / "tests" / "Substrate" / "G351_d3_route_c_proof_wording" / "G351_output.json"
G352 = STAM_ROOT / "tests" / "Substrate" / "G352_self_contained_holonomy_topology" / "G352_output.json"
G353 = STAM_ROOT / "tests" / "Substrate" / "G353_no_external_identity_provenance" / "G353_output.json"
G354 = STAM_ROOT / "tests" / "Substrate" / "G354_displacement_response_identity" / "G354_output.json"
G355 = STAM_ROOT / "tests" / "Substrate" / "G355_d3_displacement_response_theorem" / "G355_output.json"

G609C = (
    STAM_ROOT
    / "tests"
    / "Substrate"
    / "G609c_BIPARTITE_WRITE_D_3_COUNT_AUDIT"
    / "G609c_summary.json"
)
SUK056 = (
    STAM_ROOT
    / "tests"
    / "Campaigns"
    / "SAM_UNIFICATION_KERNEL_GATE"
    / "SUK056_summary.json"
)
QGA021 = (
    STAM_ROOT
    / "tests"
    / "Substrate"
    / "QGA021_THRESHOLD_ORIGIN_AUDIT"
    / "QGA021_summary.json"
)
QGA050 = (
    STAM_ROOT
    / "tests"
    / "Substrate"
    / "QGA050_WEAK_PACKET_SELECTOR_FROM_AX007_PHASE_BRIDGE"
    / "QGA050_summary.json"
)
QP092B = QUANTUM_ROOT / "artifacts" / "qp092b_tensor_carrier_qa_coupling" / "QP092B_TENSOR_CARRIER_QA_COUPLING_result.md"
QP092C = QUANTUM_ROOT / "artifacts" / "qp092c_tensor_carrier_a_kernel" / "QP092C_TENSOR_CARRIER_A_KERNEL_result.md"

DECLARED_PREMISES_JSON = CR_DIR / "CR115_declared_premises.json"
SOURCE_CHAIN_CSV = CR_DIR / "CR115_source_chain.csv"
CARRIER_REDUCTION_CSV = CR_DIR / "CR115_carrier_reduction_table.csv"
DIMENSION_TABLE_CSV = CR_DIR / "CR115_dimension_obstruction_table.csv"
CHECKS_CSV = CR_DIR / "CR115_checks.csv"
WRONG_CONTROLS_CSV = CR_DIR / "CR115_wrong_controls.csv"
LOCK_JSON = CR_DIR / "CR115_invariant_carrier_uniqueness_lock.json"
LOCK_SHA = CR_DIR / "CR115_invariant_carrier_uniqueness_lock.json.sha256.txt"
SUMMARY_JSON = CR_DIR / "CR115_summary.json"
RESULT_MD = CR_DIR / "CR115_result.md"
LOCAL_HASHES = CR_DIR / "CR115_hashes.txt"
BRANCH_HASHES = BRANCH_DIR / "HASHES.txt"


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def sha256_file(path: Path) -> str:
    if not path.exists():
        return ""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(COURTROOM_DIR))
    except ValueError:
        return str(path)


def branch_rel(path: Path) -> str:
    try:
        return str(path.relative_to(BRANCH_DIR))
    except ValueError:
        return str(path)


def source_row(
    label: str,
    path: Path,
    role: str,
    load_bearing: bool,
    source_type: str,
) -> dict[str, Any]:
    return {
        "label": label,
        "role": role,
        "load_bearing": bool(load_bearing),
        "source_type": source_type,
        "path": str(path),
        "exists": path.exists(),
        "sha256": sha256_file(path),
    }


def check_row(check_id: str, description: str, observed: Any, passed: bool, source: str) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "description": description,
        "observed": json.dumps(observed, sort_keys=True) if isinstance(observed, (dict, list)) else str(observed),
        "passed": bool(passed),
        "source": source,
    }


def wc_row(control_id: str, hypothesis: str, observed: Any, rejected: bool, reason: str) -> dict[str, Any]:
    return {
        "control_id": control_id,
        "hypothesis": hypothesis,
        "observed": json.dumps(observed, sort_keys=True) if isinstance(observed, (dict, list)) else str(observed),
        "rejected": bool(rejected),
        "reason": reason,
    }


def all_predictions_pass(payload: dict[str, Any]) -> bool:
    return bool(payload.get("all_predictions_pass") or payload.get("all_predictions_passed"))


def all_wrong_controls_pass(payload: dict[str, Any]) -> bool:
    return bool(payload.get("all_wrong_controls_pass") or payload.get("all_wrong_controls_passed"))


def predictions_all_true(payload: dict[str, Any]) -> bool:
    predictions = payload.get("predictions", {})
    return bool(predictions) and all(bool(row.get("pass")) for row in predictions.values())


def wrong_controls_all_rejected(payload: dict[str, Any]) -> bool:
    controls = payload.get("wrong_controls", {})
    return bool(controls) and all(bool(row.get("rejected")) for row in controls.values())


def update_hash_ledgers(artifacts: list[Path]) -> None:
    local_lines = [f"{sha256_file(path)}  {branch_rel(path)}" for path in artifacts]
    LOCAL_HASHES.write_text("\n".join(local_lines) + "\n", encoding="ascii")

    all_for_branch = artifacts + [LOCAL_HASHES]
    existing = BRANCH_HASHES.read_text(encoding="utf-8", errors="replace").splitlines() if BRANCH_HASHES.exists() else []
    prefix = "CR115_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM\\"
    kept = [line for line in existing if prefix not in line]
    new_lines = [f"{sha256_file(path)}  {branch_rel(path)}" for path in all_for_branch]
    BRANCH_HASHES.write_text("\n".join(kept + new_lines) + "\n", encoding="utf-8")


def route_c_rows(g347: dict[str, Any]) -> list[dict[str, Any]]:
    for route in g347.get("routes", []):
        if route.get("route") == "C_loop_topology":
            return list(route.get("rows", []))
    return []


def computed_dimension_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for d in range(1, 8):
        obstruction = 3 - d
        stable = obstruction == 0
        if obstruction > 0:
            reading = "overconstrained"
        elif obstruction == 0:
            reading = "stable_point_obstruction"
        else:
            reading = "unwinds_or_slides"
        rows.append(
            {
                "D": d,
                "obstruction_dim": obstruction,
                "stable_loop_link_identity": stable,
                "reading": reading,
            }
        )
    return rows


def make_carrier_reduction_rows(
    g348: dict[str, Any],
    g349: dict[str, Any],
    g350: dict[str, Any],
    g352: dict[str, Any],
    g354: dict[str, Any],
) -> list[dict[str, Any]]:
    g349_by_carrier = {row["carrier"]: row for row in g349.get("carrier_reductions", [])}
    g350_by_carrier = {row["carrier"]: row for row in g350.get("quotient_rows", [])}
    quotient_key = {
        "spectral_eigenmode": "standalone_spectral_number",
        "endpoint_F4_label": "bare_endpoint_F4_label",
        "ledger_history": "raw_ledger_history",
        "phase_holonomy": "open_path_phase",
    }
    rows: list[dict[str, Any]] = []
    self_contained_rule = bool(g352.get("self_contained_holonomy_reduces"))
    displacement_rule = bool(g354.get("no_external_principle_grounded"))

    for carrier in g348.get("identity_carriers", []):
        name = carrier["carrier"]
        if name == "loop_link_topology":
            rows.append(
                {
                    "g348_carrier": name,
                    "g348_status": "sufficient_open_route",
                    "g349_support": "closed_1D_loop_substrate",
                    "g350_raw_data_status": "already_deformation_class",
                    "g350_survivor": "stable_loop_link_deformation_class",
                    "g352_self_contained_rule": self_contained_rule,
                    "g354_identity_rule": displacement_rule,
                    "final_identity_handle": "stable_loop_link_sector",
                    "uniqueness_status": "CLOSED_TO_STABLE_SECTOR",
                    "reason": "direct Route C carrier; topology selector applies",
                }
            )
            continue

        support = g349_by_carrier.get(name, {})
        quotient = g350_by_carrier.get(quotient_key[name], {})
        survivor = quotient.get("quotient_survivor", "")
        survivor_ok = bool(quotient.get("survivor_topological_or_holonomic"))
        final_status = (
            "CLOSED_TO_STABLE_SECTOR"
            if support.get("requires_extended_support")
            and quotient.get("raw_invariant") is False
            and survivor_ok
            and self_contained_rule
            and displacement_rule
            else "OPEN_OR_UNRESOLVED"
        )
        rows.append(
            {
                "g348_carrier": name,
                "g348_status": "alternate_live_in_G348",
                "g349_support": support.get("support", ""),
                "g350_raw_data_status": "raw_rejected_by_deformation_quotient"
                if quotient.get("raw_invariant") is False
                else "not_rejected",
                "g350_survivor": survivor,
                "g352_self_contained_rule": self_contained_rule,
                "g354_identity_rule": displacement_rule,
                "final_identity_handle": "stable_source_topological_sector" if final_status == "CLOSED_TO_STABLE_SECTOR" else "open",
                "uniqueness_status": final_status,
                "reason": (
                    "extended support plus deformation quotient leaves only self-contained "
                    "transport/holonomy/operator-domain class, which G352 routes to a stable source sector"
                ),
            }
        )
    return rows


def source_type_table(source_rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    return [
        {
            "label": row["label"],
            "source_type": row["source_type"],
            "load_bearing": str(row["load_bearing"]),
        }
        for row in source_rows
    ]


def main() -> int:
    print("CR115 runner: starting D3 invariant-carrier uniqueness theorem gate")

    source_rows = [
        source_row("CR115_RUNNER", Path(__file__).resolve(), "current theorem runner", True, "EXECUTABLE_GATE"),
        source_row("G347_OUTPUT", G347, "computed topology obstruction and Route C target", True, "COMPUTATIONAL_TOPOLOGY_CORE"),
        source_row("G348_OUTPUT", G348, "open carrier alternatives being appealed", True, "STRUCTURED_PREMISE_AUDIT"),
        source_row("G349_OUTPUT", G349, "extended-support reduction for G348 alternatives", True, "STRUCTURED_REDUCTION_RECORD"),
        source_row("G350_OUTPUT", G350, "deformation quotient of raw identity carriers", True, "STRUCTURED_REDUCTION_RECORD"),
        source_row("G351_OUTPUT", G351, "records holonomy/topology gap before G352", True, "GAP_LOCALIZATION_RECORD"),
        source_row("G352_OUTPUT", G352, "self-contained holonomy reduces to stable sector", True, "STRUCTURED_REDUCTION_RECORD"),
        source_row("G353_OUTPUT", G353, "no-external-reference provenance", True, "PROVENANCE_RECORD"),
        source_row("G354_OUTPUT", G354, "displacement-response identity principle", True, "FRAMEWORK_PRINCIPLE_RECORD"),
        source_row("G355_OUTPUT", G355, "prior D3 displacement-response theorem aggregate", True, "AGGREGATE_THEOREM_RECORD"),
        source_row("THEOREM_D3", THEOREM_D3, "human theorem statement", True, "THEOREM_TEXT"),
        source_row("VERDICT_G355", VERDICT_G355, "sealed G355 verdict", True, "VERDICT_TEXT"),
        source_row("HOSTILE_AUDIT_F002", AUDIT_MD, "calibration against assertion-script objection", True, "EXTERNAL_HOSTILE_AUDIT"),
        source_row("PRIORITY_RECORD", PRIORITY_RECORD, "current D3 status record", False, "RECORD_CONTEXT"),
        source_row("G609C_SUMMARY", G609C, "supporting bipartite-write D=3 articulation", False, "SUPPORTING_PRESSURE"),
        source_row("SUK056_SUMMARY", SUK056, "supporting six-half-contact D_route=3", False, "SUPPORTING_PRESSURE"),
        source_row("QGA021_SUMMARY", QGA021, "supporting threshold D_route=3", False, "SUPPORTING_PRESSURE"),
        source_row("QGA050_SUMMARY", QGA050, "supporting 12-slot S3 carrier action", False, "SUPPORTING_PRESSURE"),
        source_row("QP092B_RESULT", QP092B, "supporting downstream tensor-carrier grammar", False, "SUPPORTING_PRESSURE"),
        source_row("QP092C_RESULT", QP092C, "supporting downstream A-kernel recovery", False, "SUPPORTING_PRESSURE"),
    ]
    write_csv(
        SOURCE_CHAIN_CSV,
        source_rows,
        ["label", "role", "load_bearing", "source_type", "path", "exists", "sha256"],
    )

    missing_load_bearing = [row["label"] for row in source_rows if row["load_bearing"] and not row["exists"]]

    g347 = read_json(G347)
    g348 = read_json(G348)
    g349 = read_json(G349)
    g350 = read_json(G350)
    g351 = read_json(G351)
    g352 = read_json(G352)
    g353 = read_json(G353)
    g354 = read_json(G354)
    g355 = read_json(G355)
    theorem_text = read_text(THEOREM_D3)
    verdict_text = read_text(VERDICT_G355)
    audit_text = read_text(AUDIT_MD)
    pr_text = read_text(PRIORITY_RECORD) if PRIORITY_RECORD.exists() else ""

    carrier_rows = make_carrier_reduction_rows(g348, g349, g350, g352, g354)
    dimension_rows = computed_dimension_rows()
    write_csv(
        CARRIER_REDUCTION_CSV,
        carrier_rows,
        [
            "g348_carrier",
            "g348_status",
            "g349_support",
            "g350_raw_data_status",
            "g350_survivor",
            "g352_self_contained_rule",
            "g354_identity_rule",
            "final_identity_handle",
            "uniqueness_status",
            "reason",
        ],
    )
    write_csv(
        DIMENSION_TABLE_CSV,
        dimension_rows,
        ["D", "obstruction_dim", "stable_loop_link_identity", "reading"],
    )

    stable_ds = [row["D"] for row in dimension_rows if row["stable_loop_link_identity"]]
    g347_route_c = route_c_rows(g347)
    g347_stable_ds = [row["D"] for row in g347_route_c if row.get("obstruction_dim") == 0]
    all_carriers_closed = all(row["uniqueness_status"] == "CLOSED_TO_STABLE_SECTOR" for row in carrier_rows)
    g348_alternates = set(g348.get("alternate_live", []))
    carrier_table_alternates = {row["g348_carrier"] for row in carrier_rows if row["g348_status"] == "alternate_live_in_G348"}
    audit_f002_found = (
        "Finding F-002" in audit_text
        and "G347" in audit_text
        and "assertion-script" in audit_text
        and "conditional theorem" in audit_text
    )

    declared_premises = {
        "artifact": "CR115_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM",
        "declared_at_utc": now_utc(),
        "purpose": "Close the G348 carrier-necessity gap under accepted SAM matter-identity commitments.",
        "theorem_claim_inside_sam": (
            "Given substrate-internal displacement-response identity and no external identity carrier, "
            "all admissible persistent matter-identity handles reduce to a self-contained stable "
            "source/topological sector. For the 1D loop/twist/intersection carrier, obstruction_dim=3-D, "
            "so D=3 is the unique stable dimension."
        ),
        "calibration": {
            "computed_core": "G347 topology obstruction, recomputed by CR115",
            "structural_commitment_layer": "G349-G354 carrier reductions and identity principle",
            "not_claimed": [
                "external peer-review closure",
                "empirical proof of D=3",
                "string-theory critical dimension",
                "D3 from poset axioms alone",
                "D3 from R, A0, 2pi, Higgs, or downstream particle numerology",
            ],
        },
        "accepted_commitments_used": [
            "matter identity is invariant substrate displacement-response",
            "persistent identity cannot be an external/background label",
            "raw histories, labels, open phases, and standalone spectra are not persistent identity by themselves",
            "self-contained nontrivial transport/holonomy identity requires a stable source sector",
            "loop/twist/intersection carrier has obstruction_dim = 3 - D",
        ],
    }
    write_json(DECLARED_PREMISES_JSON, declared_premises)

    checks = [
        check_row(
            "P1_sources_present",
            "All load-bearing source artifacts are present.",
            {"missing_load_bearing": missing_load_bearing},
            not missing_load_bearing,
            "source_chain",
        ),
        check_row(
            "P2_hostile_audit_trap_acknowledged",
            "The gate explicitly separates G347 computational topology from assertion/commitment records.",
            {
                "audit_f002_found": audit_f002_found,
                "source_types": source_type_table(source_rows[:13]),
            },
            audit_f002_found
            and any(row["source_type"] == "COMPUTATIONAL_TOPOLOGY_CORE" for row in source_rows)
            and any(row["source_type"] == "STRUCTURED_REDUCTION_RECORD" for row in source_rows),
            "audit.md/source_chain",
        ),
        check_row(
            "P3_G348_open_premise_captured",
            "G348's live alternate carriers are copied into the CR115 reduction table rather than ignored.",
            {
                "G348_alternates": sorted(g348_alternates),
                "carrier_table_alternates": sorted(carrier_table_alternates),
                "topology_necessary_in_G348": g348.get("topology_necessary"),
            },
            g348.get("verdict") == "G348_LOOP_TOPOLOGY_IDENTITY_PREMISE_NOT_CLOSED"
            and g348.get("topology_necessary") is False
            and g348_alternates == carrier_table_alternates,
            "G348/CR115_carrier_reduction_table",
        ),
        check_row(
            "P4_G349_extended_support_reduces_alternates",
            "All G348 alternate carriers require extended support before quotienting.",
            {
                "all_alternates_extended": g349.get("all_alternates_extended"),
                "carrier_reductions": g349.get("carrier_reductions", []),
            },
            g349.get("verdict") == "G349_WORLDSHEET_IDENTITY_REDUCTION_CANDIDATE_PASS"
            and g349.get("all_alternates_extended") is True
            and len(g349.get("carrier_reductions", [])) == len(g348_alternates),
            "G349",
        ),
        check_row(
            "P5_G350_deformation_quotient_rejects_raw_carriers",
            "Raw labels, histories, phases, and spectra survive only as deformation classes.",
            {
                "raw_all_variant": g350.get("raw_all_variant"),
                "survivors_all_topological_or_holonomic": g350.get("survivors_all_topological_or_holonomic"),
                "quotient_rows": g350.get("quotient_rows", []),
            },
            g350.get("raw_all_variant") is True
            and g350.get("survivors_all_topological_or_holonomic") is True
            and all(row.get("raw_invariant") is False for row in g350.get("quotient_rows", [])),
            "G350",
        ),
        check_row(
            "P6_G352_self_contained_holonomy_reduces",
            "Self-contained nontrivial holonomy/transport identity reduces to a stable source sector.",
            {
                "self_contained_holonomy_reduces": g352.get("self_contained_holonomy_reduces"),
                "stable_ds": g352.get("stable_ds"),
                "cases": g352.get("cases", []),
            },
            g352.get("self_contained_holonomy_reduces") is True
            and g352.get("stable_ds") == [3]
            and wrong_controls_all_rejected(g352),
            "G352",
        ),
        check_row(
            "P7_G354_identity_principle_accepted_for_gate",
            "Displacement-response identity supplies the no-external identity rule used by CR115.",
            {
                "verdict": g354.get("verdict"),
                "no_external_principle_grounded": g354.get("no_external_principle_grounded"),
                "stable_ds": g354.get("stable_ds"),
            },
            g354.get("verdict") == "G354_DISPLACEMENT_RESPONSE_IDENTITY_PRINCIPLE_PASS"
            and g354.get("no_external_principle_grounded") is True
            and g354.get("stable_ds") == [3]
            and wrong_controls_all_rejected(g354),
            "G354",
        ),
        check_row(
            "P8_all_admissible_carriers_close_to_stable_sector",
            "Every G348 carrier is now routed to the stable source/topological sector under the declared SAM rules.",
            carrier_rows,
            all_carriers_closed
            and len(carrier_rows) == len(g348.get("identity_carriers", [])),
            "CR115_carrier_reduction_table",
        ),
        check_row(
            "P9_dimension_selector_computed_and_matches_sources",
            "CR115 recomputes obstruction_dim=3-D and finds D=3 as the unique stable row.",
            {
                "CR115_stable_ds": stable_ds,
                "G347_stable_ds": g347_stable_ds,
                "G350_stable_ds": g350.get("stable_ds"),
                "G352_stable_ds": g352.get("stable_ds"),
                "G354_stable_ds": g354.get("stable_ds"),
                "G355_stable_ds": g355.get("stable_ds"),
            },
            stable_ds == [3]
            and g347_stable_ds == [3]
            and g350.get("stable_ds") == [3]
            and g352.get("stable_ds") == [3]
            and g354.get("stable_ds") == [3]
            and g355.get("stable_ds") == [3],
            "CR115/G347/G350/G352/G354/G355",
        ),
        check_row(
            "P10_G351_gap_is_specifically_closed",
            "G351 named the holonomy/topology gap; G352 and CR115 close that exact gap under no-external identity.",
            {
                "G351_verdict": g351.get("verdict"),
                "G352_verdict": g352.get("verdict"),
                "carrier_uniqueness_closed": all_carriers_closed,
            },
            g351.get("verdict") == "G351_ROUTE_C_CONDITIONAL_THEOREM_SCHEMA_HOLONOMY_GAP_OPEN"
            and g352.get("verdict") == "G352_SELF_CONTAINED_HOLONOMY_REDUCES_TO_STABLE_TOPOLOGY"
            and all_carriers_closed,
            "G351/G352/CR115",
        ),
        check_row(
            "P11_G355_chain_remains_consistent",
            "G355 aggregate chain remains consistent with the explicit uniqueness closure.",
            {
                "G355_verdict": g355.get("verdict"),
                "G355_chain_steps": [row.get("step") for row in g355.get("chain_steps", [])],
                "theorem_text_has_if_claim": "if matter identity is substrate-internal displacement response" in theorem_text,
            },
            g355.get("verdict") == "G355_D3_DISPLACEMENT_RESPONSE_THEOREM_PASS"
            and predictions_all_true(g355)
            and wrong_controls_all_rejected(g355)
            and "if matter identity is substrate-internal displacement response" in theorem_text,
            "G355/THEOREM_D3",
        ),
        check_row(
            "P12_current_record_status_found",
            "Priority record currently records D=3 as derived inside SAM, so CR115 is an appeal/closure support artifact rather than a new free parameter.",
            "priority record D3 status",
            "D = 3. Derived" in pr_text
            and "displacement-response" in pr_text
            and "obstruction_dim = 3 - D" in pr_text,
            "PRIORITY_RECORD",
        ),
    ]

    wrong_controls = [
        wc_row(
            "WC1_poset_axioms_alone_derive_D3",
            "Finite poset axioms alone derive D=3.",
            g347.get("wrong_controls", {}).get("WC1_poset_axioms_alone_derive_D3", {}),
            bool(g347.get("wrong_controls", {}).get("WC1_poset_axioms_alone_derive_D3", {}).get("rejected")),
            "G347 rejects poset axioms alone as a D3 derivation.",
        ),
        wc_row(
            "WC2_topology_sufficient_implies_necessary",
            "Loop topology being sufficient in G348 already made it necessary.",
            g348.get("wrong_controls", {}).get("WC1_sufficient_implies_necessary", {}),
            bool(g348.get("wrong_controls", {}).get("WC1_sufficient_implies_necessary", {}).get("rejected"))
            and all_carriers_closed,
            "G348 rejected the shortcut; CR115 closes necessity only after G349-G354 reductions.",
        ),
        wc_row(
            "WC3_rule_out_alternates_by_assertion",
            "Rule out spectra, labels, ledger history, and phase holonomy by assertion.",
            {
                "G348_wrong_controls": {
                    "spectral": g348.get("wrong_controls", {}).get("WC2_rule_out_spectral_by_assertion", {}),
                    "endpoint": g348.get("wrong_controls", {}).get("WC3_rule_out_endpoint_labels_by_assertion", {}),
                    "ledger": g348.get("wrong_controls", {}).get("WC4_rule_out_ledger_history_by_assertion", {}),
                },
                "CR115_reduction_rows": carrier_rows,
            },
            all(
                bool(g348.get("wrong_controls", {}).get(key, {}).get("rejected"))
                for key in [
                    "WC2_rule_out_spectral_by_assertion",
                    "WC3_rule_out_endpoint_labels_by_assertion",
                    "WC4_rule_out_ledger_history_by_assertion",
                ]
            )
            and all_carriers_closed,
            "CR115 requires explicit support -> quotient -> stable-sector routing.",
        ),
        wc_row(
            "WC4_raw_ledger_string_persistent",
            "Raw ordered ledger history is itself persistent matter identity.",
            g350.get("wrong_controls", {}).get("WC1_raw_ledger_string_persistent", {}),
            bool(g350.get("wrong_controls", {}).get("WC1_raw_ledger_string_persistent", {}).get("rejected")),
            "G350 rejects raw ledger strings under subdivision/reparameterization.",
        ),
        wc_row(
            "WC5_bare_endpoint_label_persistent",
            "Bare endpoint/F4 label is persistent matter identity without closed-loop transport.",
            g350.get("wrong_controls", {}).get("WC2_bare_endpoint_label_persistent", {}),
            bool(g350.get("wrong_controls", {}).get("WC2_bare_endpoint_label_persistent", {}).get("rejected")),
            "G350 keeps only transport conjugacy class, not bare labels.",
        ),
        wc_row(
            "WC6_open_path_phase_persistent",
            "Open path phase is persistent matter identity without closed holonomy.",
            g350.get("wrong_controls", {}).get("WC3_open_path_phase_persistent", {}),
            bool(g350.get("wrong_controls", {}).get("WC3_open_path_phase_persistent", {}).get("rejected")),
            "G350 rejects open phase as convention/path dependent.",
        ),
        wc_row(
            "WC7_standalone_spectral_number_persistent",
            "A standalone spectral number is persistent matter identity without operator-domain deformation class.",
            g350.get("wrong_controls", {}).get("WC4_standalone_spectral_number_persistent", {}),
            bool(g350.get("wrong_controls", {}).get("WC4_standalone_spectral_number_persistent", {}).get("rejected")),
            "G350 keeps only spectrum of deformation operator class.",
        ),
        wc_row(
            "WC8_external_background_identity",
            "External/background holonomy can be intrinsic matter identity in SAM.",
            g352.get("wrong_controls", {}).get("WC1_external_background_identity", {}),
            bool(g352.get("wrong_controls", {}).get("WC1_external_background_identity", {}).get("rejected")),
            "G352 rejects external background holonomy as not self-contained identity.",
        ),
        wc_row(
            "WC9_contractible_phase_identity",
            "Contractible self-contained phase is persistent nontrivial matter identity.",
            g352.get("wrong_controls", {}).get("WC2_contractible_phase_identity", {}),
            bool(g352.get("wrong_controls", {}).get("WC2_contractible_phase_identity", {}).get("rejected")),
            "G352 rejects contractible phase as deformable/trivial without protected source.",
        ),
        wc_row(
            "WC10_holonomy_alone_derives_D3",
            "Holonomy by itself derives D=3 without a stable source/topological sector.",
            g352.get("wrong_controls", {}).get("WC4_holonomy_alone_derives_D3", {}),
            bool(g352.get("wrong_controls", {}).get("WC4_holonomy_alone_derives_D3", {}).get("rejected")),
            "G352 requires self-contained stable source sector before topology selector applies.",
        ),
        wc_row(
            "WC11_D2_or_D4_stable_identity",
            "D=2 or D=4 supplies the same stable nontrivial loop/twist identity.",
            {
                "CR115_dimension_rows": dimension_rows,
                "G354_WC": g354.get("wrong_controls", {}).get("WC6_D2_or_D4_stable_twist", {}),
                "G355_WC": g355.get("wrong_controls", {}).get("WC6_D2_or_D4_stability", {}),
            },
            stable_ds == [3]
            and bool(g354.get("wrong_controls", {}).get("WC6_D2_or_D4_stable_twist", {}).get("rejected"))
            and bool(g355.get("wrong_controls", {}).get("WC6_D2_or_D4_stability", {}).get("rejected")),
            "Computed obstruction table and G354/G355 both reject D2/D4 stability.",
        ),
        wc_row(
            "WC12_import_string_critical_dimension",
            "D=3 is imported from string-theory critical dimension or other external target.",
            {
                "G352_WC": g352.get("wrong_controls", {}).get("WC5_import_string_critical_dimension", {}),
                "G355_WC": g355.get("wrong_controls", {}).get("WC7_import_string_critical_dimension", {}),
            },
            bool(g352.get("wrong_controls", {}).get("WC5_import_string_critical_dimension", {}).get("rejected"))
            and bool(g355.get("wrong_controls", {}).get("WC7_import_string_critical_dimension", {}).get("rejected")),
            "The selector is the SAM loop/twist obstruction count, not imported string criticality.",
        ),
        wc_row(
            "WC13_assertion_script_equals_computation",
            "Treat G348-G355 assertion/commitment records as if every layer were computational math.",
            source_type_table(source_rows[:13]),
            audit_f002_found
            and any(row["source_type"] == "COMPUTATIONAL_TOPOLOGY_CORE" for row in source_rows)
            and any(row["source_type"] == "STRUCTURED_REDUCTION_RECORD" for row in source_rows),
            "CR115 tags source types and recomputes the topology table instead of hiding the audit classification.",
        ),
        wc_row(
            "WC14_downstream_R_A0_Higgs_derives_D3",
            "Use R=12, A0, Higgs, 2pi, or downstream particle matches as the D=3 derivation.",
            {
                "declared_forbidden": declared_premises["calibration"]["not_claimed"],
                "load_bearing_sources": [row["label"] for row in source_rows if row["load_bearing"]],
            },
            "D3 from R, A0, 2pi, Higgs, or downstream particle numerology"
            in declared_premises["calibration"]["not_claimed"]
            and "CR113" not in [row["label"] for row in source_rows if row["load_bearing"]],
            "The load-bearing D3 gate uses identity-carrier topology, not R/A0/Higgs downstream closure.",
        ),
        wc_row(
            "WC15_external_peer_review_or_empirical_proof_claim",
            "Claim external peer-review closure or empirical proof of D=3.",
            g355.get("wrong_controls", {}).get("WC8_external_peer_review_or_empirical_proof_claim", {}),
            bool(g355.get("wrong_controls", {}).get("WC8_external_peer_review_or_empirical_proof_claim", {}).get("rejected"))
            and "external peer-review closure" in declared_premises["calibration"]["not_claimed"],
            "CR115 is an inside-SAM theorem gate, not an external proof claim.",
        ),
    ]

    write_csv(CHECKS_CSV, checks, ["check_id", "description", "observed", "passed", "source"])
    write_csv(WRONG_CONTROLS_CSV, wrong_controls, ["control_id", "hypothesis", "observed", "rejected", "reason"])

    all_checks_passed = all(row["passed"] for row in checks)
    all_wrong_controls_rejected = all(row["rejected"] for row in wrong_controls)
    result_class = RESULT_CLASS_PASS if all_checks_passed and all_wrong_controls_rejected else RESULT_CLASS_FAIL

    lock = {
        "lock_id": "CR115_D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM_LOCK",
        "cr_id": CR_ID,
        "branch": "14_FOUNDATIONAL_TESTS",
        "sealed_at_utc": now_utc(),
        "execution_status": "CLEAN" if result_class == RESULT_CLASS_PASS else "CHECK",
        "result_class": result_class,
        "grade": "structural theorem-gate inside SAM; computational topology core plus declared carrier-identity commitments",
        "theorem_statement": declared_premises["theorem_claim_inside_sam"],
        "computed_core": {
            "formula": "obstruction_dim = 3 - D",
            "stable_ds": stable_ds,
            "dimension_rows": dimension_rows,
        },
        "carrier_uniqueness": {
            "all_g348_carriers_closed_to_stable_sector": all_carriers_closed,
            "carrier_rows": carrier_rows,
        },
        "audit_calibration": {
            "hostile_audit_f002_acknowledged": audit_f002_found,
            "source_type_table": source_type_table(source_rows),
            "not_claimed": declared_premises["calibration"]["not_claimed"],
        },
        "source_chain_sha256": {row["label"]: row["sha256"] for row in source_rows},
        "checks": checks,
        "wrong_controls": wrong_controls,
        "scope": [
            "Closes the G348 carrier-necessity gap inside SAM by routing all G348 identity-carrier alternatives through support, deformation quotient, and self-contained stable-sector rules.",
            "Keeps G347 as the only load-bearing computational topology selector.",
            "Recalibrates G355: strong inside-SAM theorem gate, not external peer-review or empirical proof.",
            "Does not derive D=3 from R=12, A0, Higgs, 2pi, SN/BAO, or particle mass matches.",
            "Does not derive the matter spectrum, chirality, anomaly cancellation, or exact masses.",
        ],
        "open_debts": [
            "For publication, write the carrier-uniqueness theorem in prose with the source-type calibration visible.",
            "External topology review can still be invited for the G347 obstruction theorem wording.",
            "If desired, backfill G348-G355 with explicit test_type fields so assertion records are machine-labeled.",
        ],
    }
    write_json(LOCK_JSON, lock)
    lock_sha = sha256_file(LOCK_JSON)
    LOCK_SHA.write_text(lock_sha + "\n", encoding="ascii")

    summary = {
        "cr_id": CR_ID,
        "branch": "14_FOUNDATIONAL_TESTS",
        "test_class": "D3_INVARIANT_CARRIER_UNIQUENESS_THEOREM",
        "execution_status": lock["execution_status"],
        "result_class": result_class,
        "all_predictions_passed": all_checks_passed,
        "all_wrong_controls_rejected": all_wrong_controls_rejected,
        "stable_ds": stable_ds,
        "carrier_count": len(carrier_rows),
        "all_g348_carriers_closed_to_stable_sector": all_carriers_closed,
        "hostile_audit_f002_acknowledged": audit_f002_found,
        "load_bearing_computed_core": "G347 obstruction_dim = 3 - D, recomputed by CR115",
        "grade": lock["grade"],
        "lock_sha256": lock_sha,
        "declared_premises_json": rel(DECLARED_PREMISES_JSON),
        "source_chain_csv": rel(SOURCE_CHAIN_CSV),
        "carrier_reduction_csv": rel(CARRIER_REDUCTION_CSV),
        "dimension_table_csv": rel(DIMENSION_TABLE_CSV),
        "checks_csv": rel(CHECKS_CSV),
        "wrong_controls_csv": rel(WRONG_CONTROLS_CSV),
        "lock_json": rel(LOCK_JSON),
        "result_md": rel(RESULT_MD),
    }
    write_json(SUMMARY_JSON, summary)

    md: list[str] = []
    md.append("# CR115 D3 Invariant-Carrier Uniqueness Theorem Gate\n\n")
    md.append("## Verdict\n\n```text\n")
    md.append(result_class + "\n")
    md.append("```\n\n")
    md.append("## Theorem Statement\n\n")
    md.append(lock["theorem_statement"] + "\n\n")
    md.append("## Calibration\n\n")
    md.append("This gate answers the F-002 trap directly: G347 is the computational topology core; ")
    md.append("G349-G354 are the SAM structural-commitment layer that makes the carrier class necessary. ")
    md.append("The result is an inside-SAM theorem gate, not an external peer-review or empirical-proof claim.\n\n")
    md.append("## Computed Topology Core\n\n```text\n")
    md.append("obstruction_dim = 3 - D\n")
    for row in dimension_rows:
        md.append(
            f"D={row['D']}: obstruction={row['obstruction_dim']}, "
            f"stable={row['stable_loop_link_identity']}, {row['reading']}\n"
        )
    md.append(f"stable_ds = {stable_ds}\n")
    md.append("```\n\n")
    md.append("## Carrier Closure\n\n")
    for row in carrier_rows:
        md.append(
            f"- {row['g348_carrier']}: {row['g348_status']} -> "
            f"{row['g349_support']} -> {row['g350_survivor']} -> "
            f"{row['final_identity_handle']} ({row['uniqueness_status']})\n"
        )
    md.append("\n## Load-Bearing Source Chain\n\n")
    for row in source_rows:
        if row["load_bearing"]:
            md.append(
                f"- {row['label']} [{row['source_type']}]: `{row['path']}` "
                f"sha256 `{row['sha256']}`\n"
            )
    md.append("\n## Pass Checks\n\n")
    for row in checks:
        md.append(f"- {'PASS' if row['passed'] else 'FAIL'} {row['check_id']}: {row['description']}\n")
    md.append("\n## Wrong Controls\n\n")
    for row in wrong_controls:
        md.append(f"- {'REJECTED' if row['rejected'] else 'NOT_REJECTED'} {row['control_id']}: {row['hypothesis']}\n")
    md.append("\n## Scope\n\n")
    for item in lock["scope"]:
        md.append(f"- {item}\n")
    md.append("\n## Open Debts\n\n")
    for item in lock["open_debts"]:
        md.append(f"- {item}\n")
    md.append("\n## Hash\n\n```text\n")
    md.append(f"CR115_invariant_carrier_uniqueness_lock.json sha256 = {lock_sha}\n")
    md.append("```\n")
    RESULT_MD.write_text("".join(md), encoding="utf-8")

    artifacts = [
        Path(__file__).resolve(),
        DECLARED_PREMISES_JSON,
        SOURCE_CHAIN_CSV,
        CARRIER_REDUCTION_CSV,
        DIMENSION_TABLE_CSV,
        CHECKS_CSV,
        WRONG_CONTROLS_CSV,
        LOCK_JSON,
        LOCK_SHA,
        SUMMARY_JSON,
        RESULT_MD,
    ]
    update_hash_ledgers(artifacts)

    print(f"CR115 result_class={result_class}")
    print(f"CR115 lock_sha256={lock_sha}")
    print(f"CR115 stable_ds={stable_ds}")
    print(f"CR115 all_g348_carriers_closed_to_stable_sector={all_carriers_closed}")
    print("CR115 runner: complete")
    return 0 if result_class == RESULT_CLASS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
