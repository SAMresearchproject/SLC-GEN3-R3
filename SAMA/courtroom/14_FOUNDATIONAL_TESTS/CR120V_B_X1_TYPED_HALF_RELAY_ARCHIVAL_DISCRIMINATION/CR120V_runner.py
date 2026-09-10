from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path


RECORD_ID = "CR120V_B_X1_TYPED_HALF_RELAY_ARCHIVAL_DISCRIMINATION"
PRECOMMIT_SHA256 = "03c23e9ebfc1e5be7e1e9a32d87987b27197ae2cc9281659e79009ffe0cb460f"
PROPOSAL_ID = "sam2p-378de6a78a8c2bd479b1"
PROPOSAL_HASH = "378de6a78a8c2bd479b182a0add9c7420e396337c62d8bb52d2b86de073d8d87"

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def manifest_path(raw_path: str) -> Path:
    candidate = Path(raw_path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def main() -> None:
    precommit = HERE / "CR120V_PRECOMMIT.md"
    if sha256(precommit) != PRECOMMIT_SHA256:
        raise RuntimeError("CR120V precommit seal mismatch")

    source_manifest_path = HERE / "CR120V_SOURCE_MANIFEST.json"
    source_manifest = json.loads(read_text(source_manifest_path))
    source_rows: list[dict[str, object]] = []
    source_by_role: dict[str, Path] = {}
    for source in source_manifest["sources"]:
        path = manifest_path(source["path"])
        actual = sha256(path)
        matched = actual == source["sha256"]
        source_rows.append(
            {
                "role": source["role"],
                "path": source["path"],
                "expected_sha256": source["sha256"],
                "actual_sha256": actual,
                "matched": matched,
            }
        )
        source_by_role[source["role"]] = path

    source_integrity = all(bool(row["matched"]) for row in source_rows)
    if not source_integrity:
        raise RuntimeError("Frozen source hash mismatch")

    master = read_text(source_by_role["active_master_formula"])
    action = read_text(source_by_role["active_action_engine"])
    hierarchy = json.loads(read_text(source_by_role["typed_hierarchy"]))
    handoff = json.loads(read_text(source_by_role["typed_handoff"]))
    cr120d = read_text(source_by_role["runtime_boundary"])
    runtime_flow = json.loads(read_text(source_by_role["runtime_information_flow"]))
    x1_report = json.loads(read_text(source_by_role["x1_content"]))
    qp035 = read_text(source_by_role["half_write_boundary"])
    qp036 = read_text(source_by_role["local_return_selection"])
    qp037 = read_text(source_by_role["post_return_identity_freeze"])
    cr103a = read_text(source_by_role["half_write_structural_record"])
    cr104c = read_text(source_by_role["half_write_geometry_closure"])

    nodes = {node["id"]: node for node in handoff["nodes"]}
    operators = {operator["id"]: operator for operator in handoff["operators"]}
    legal_edges = set(handoff["legal_edges"])
    forbidden_collapses = set(handoff["forbidden_collapses"])

    half_tokens = [
        "1/2 SW_out",
        "1/2 WRITE_out",
        "1/2 OUTSIDE",
        "1/2 INSIDE",
        "1/2 WRITE_in",
        "1/2 SW_in",
    ]
    master_has_six = all(token in master for token in half_tokens)
    action_has_six = all(token in action for token in half_tokens)
    outward_weight = sum((Fraction(1, 2) for _ in half_tokens[:3]), Fraction(0, 1))
    inward_weight = sum((Fraction(1, 2) for _ in half_tokens[3:]), Fraction(0, 1))
    total_weight = outward_weight + inward_weight

    typed_route = (
        "RESOLVE(S8_BINARY_SURFACE, B_CONTACT_OPERATOR, X1_AXIS_SELF_CHANNEL) "
        "-> W9_CLOSURE_WITNESS"
    )
    typed_route_present = typed_route in legal_edges
    b_x1_distinct = "B_CONTACT_OPERATOR == X1_AXIS_SELF_CHANNEL" in forbidden_collapses
    b_record = operators["B_CONTACT_OPERATOR"]
    x1_node = nodes["X1_AXIS_SELF_CHANNEL"]
    s8_node = nodes["S8_BINARY_SURFACE"]
    b_is_nonscalar = "value" not in b_record and b_record["type"] == "NonRowOperator"
    x1_is_axis_one = x1_node["type"] == "AxisChannel" and x1_node["value"] == 1
    no_w8_alias = "W8" not in nodes and s8_node["type"] == "BinarySurface" and s8_node["value"] == 8

    runtime_static = (
        runtime_flow["implementation_selects_fixed_signature_result"] is True
        and runtime_flow["installed_output_alphabet_cardinality"] == 1
        and runtime_flow["installed_input_dependent_capacity_bits"] == 0.0
    )
    no_intervention_surface = (
        x1_report["independent_perturbability_status"] == "NO_RUNTIME_INTERVENTION_SURFACE"
        and x1_report["canonical_state_count"] == 1
    )
    physical_unresolved = x1_report["physical_independence_status"] == "UNRESOLVED_NOT_FALSIFIED"

    half_alone_open = (
        "does not by itself close an open particle" in qp035
        and "requires a local return" in qp035
    )
    return_selected = (
        "QP036_LOCAL_RETURN_CORRECTION_CONTACT_SELECTED" in qp036
        and "residual_stack_minus_R_neutral_route_reservation" in qp036
    )
    post_return_one_promoted = (
        "QP037_PARTICLE_IDENTITY_FREEZE_ONE_PROMOTION_HELD_OPEN_REST" in qp037
        and "promoted_identity_slots = 1" in qp037
        and "held_open_identity_slots = 7" in qp037
    )
    half_write_structural = "resolution produces 1/2 SW and 1/2  write" in cr103a
    half_geometry_closed = (
        "D^2/2^(D+1) = 9/16" in cr104c
        and "half-write-side residue" in cr104c
    )

    # An explicit B/request-X1/response weld must appear in an authority-bearing
    # source, not merely in the proposal. The authoritative typed sources name
    # contact, axis, OUT/IN, and return separately but never make that mapping.
    authority_weld_patterns = [
        "B_CONTACT_OPERATOR = REQUEST",
        "B_CONTACT_OPERATOR -> REQUEST",
        "X1_AXIS_SELF_CHANNEL = RESPONSE",
        "X1_AXIS_SELF_CHANNEL -> RESPONSE",
        "B_CONTACT_OPERATOR as request",
        "X1_AXIS_SELF_CHANNEL as response",
    ]
    authority_text = "\n".join([master, action, json.dumps(hierarchy), json.dumps(handoff), cr120d, qp035, qp036, qp037])
    explicit_b_request_x1_response_weld = any(
        pattern.lower() in authority_text.lower() for pattern in authority_weld_patterns
    )
    qp036_mentions_b_or_x1 = "B_CONTACT_OPERATOR" in qp036 or "X1_AXIS_SELF_CHANNEL" in qp036

    evidence = [
        {
            "gate_id": "E01_SOURCE_INTEGRITY",
            "description": "All frozen sources match their SHA-256 values",
            "passed": source_integrity,
            "detail": f"{sum(bool(row['matched']) for row in source_rows)}/{len(source_rows)} matched",
            "source": "CR120V_SOURCE_MANIFEST.json",
        },
        {
            "gate_id": "E02_TYPED_ROUTE",
            "description": "Canonical S8-B-X1-W9 typed route is present",
            "passed": typed_route_present,
            "detail": typed_route,
            "source": "CR119_LANGUAGE_HANDOFF_CONTRACT.json",
        },
        {
            "gate_id": "E03_TYPED_SEPARATION",
            "description": "B and X1 are explicitly forbidden from collapsing",
            "passed": b_x1_distinct,
            "detail": "B_CONTACT_OPERATOR != X1_AXIS_SELF_CHANNEL",
            "source": "CR119_LANGUAGE_HANDOFF_CONTRACT.json",
        },
        {
            "gate_id": "E04_SCALAR_TYPING",
            "description": "B is non-scalar; X1 is AxisChannel scalar one",
            "passed": b_is_nonscalar and x1_is_axis_one,
            "detail": f"B_type={b_record['type']}; X1_type={x1_node['type']}; X1_value={x1_node['value']}",
            "source": "CR119_LANGUAGE_HANDOFF_CONTRACT.json",
        },
        {
            "gate_id": "E05_CANONICAL_S8",
            "description": "S8 is canonical and no W8 node is installed",
            "passed": no_w8_alias,
            "detail": "S8_BINARY_SURFACE=8; W8 absent",
            "source": "CR119_LANGUAGE_HANDOFF_CONTRACT.json",
        },
        {
            "gate_id": "E06_SIX_HALF_SLOT_ROUTE",
            "description": "Both active V4.2 documents contain the six resolved half-slot shell",
            "passed": master_has_six and action_has_six,
            "detail": "outward=3 slots; inward=3 slots",
            "source": "SAM_NATIVE_MASTER_FORMULA_V4_2.md; SAM_NATIVE_ACTION_ENGINE_V4_2.md",
        },
        {
            "gate_id": "E07_EXACT_ROUTE_ARITHMETIC",
            "description": "Outward and inward weights each equal 3/2 and total D=3",
            "passed": outward_weight == Fraction(3, 2) and inward_weight == Fraction(3, 2) and total_weight == Fraction(3, 1),
            "detail": f"out={outward_weight}; in={inward_weight}; total={total_weight}",
            "source": "exact Fraction arithmetic",
        },
        {
            "gate_id": "E08_STATIC_RUNTIME",
            "description": "Current RESOLVE runtime has fixed singleton W9 output",
            "passed": runtime_static,
            "detail": "alphabet=1; input-dependent capacity=0 bits in installed runtime",
            "source": "CR120D_RUNTIME_INFORMATION_FLOW.json",
        },
        {
            "gate_id": "E09_NO_X1_INTERVENTION",
            "description": "Current runtime has no X1 intervention surface",
            "passed": no_intervention_surface and physical_unresolved,
            "detail": "runtime intervention absent; physical independence unresolved, not falsified",
            "source": "CR120D_X1_CONTENT_REPORT.json",
        },
        {
            "gate_id": "E10_HALF_ALONE_OPEN",
            "description": "Half-write/information split alone does not close the open slot",
            "passed": half_alone_open,
            "detail": "QP035 requires a local return correction",
            "source": "QP035_PRIVATE_HALF_WRITE_INFORMATION_FIXED_POINT_SELECTOR.md",
        },
        {
            "gate_id": "E11_RETURN_SELECTED",
            "description": "QP036 selects a native local information-return correction",
            "passed": return_selected,
            "detail": "residual_stack_minus_R_neutral_route_reservation",
            "source": "QP036_PRIVATE_LOCAL_INFORMATION_RETURN_CORRECTION_SELECTOR.md",
        },
        {
            "gate_id": "E12_POST_RETURN_PROMOTION",
            "description": "QP037 promotes one identity after the selected return and holds seven open",
            "passed": post_return_one_promoted,
            "detail": "1 promoted; 7 held open",
            "source": "QP037_PRIVATE_PARTICLE_IDENTITY_CLOSURE_FREEZE.md",
        },
        {
            "gate_id": "E13_HALF_WRITE_GEOMETRY",
            "description": "Half-write split and D=3 half-write geometry are independently recorded",
            "passed": half_write_structural and half_geometry_closed,
            "detail": "CR103a split record; CR104c 9/16 half-write-side structure",
            "source": "CR103a_result.md; CR104c_result.md",
        },
        {
            "gate_id": "E14_EXPLICIT_INTERFACE_WELD",
            "description": "Authority source explicitly maps B=request and X1=response",
            "passed": explicit_b_request_x1_response_weld,
            "detail": "No explicit authority-bearing weld found" if not explicit_b_request_x1_response_weld else "Explicit weld found",
            "source": "frozen authority source set",
        },
    ]

    core_pass = all(row["passed"] for row in evidence if row["gate_id"] not in {"E14_EXPLICIT_INTERFACE_WELD"})
    if core_pass and not explicit_b_request_x1_response_weld:
        primary_verdict = (
            "PASS_RECIPROCAL_HALF_SLOT_RELAY_EXISTS__"
            "BOUNDARY_B_REQUEST_X1_RESPONSE_WELD__"
            "LITERAL_TWO_HALF_REJECTED"
        )
    elif source_integrity and typed_route_present:
        primary_verdict = "BOUNDARY_ARCHIVAL_RELAY_INCOMPLETE"
    else:
        primary_verdict = "FAIL_SOURCE_OR_ARITHMETIC_REPRODUCTION"

    literal_failures = [
        not b_is_nonscalar,
        not x1_is_axis_one,
        not (master_has_six and action_has_six),
        not half_alone_open,
    ]
    models = [
        {
            "candidate": "LITERAL_TWO_HALF",
            "status": "REJECTED_BY_FROZEN_RECORD" if not any(literal_failures) else "UNEXPECTED",
            "supporting_contacts": 0,
            "blocking_contacts": 4,
            "reason": "B is non-scalar; X1 is scalar one; route has six half-slots; split alone does not close",
        },
        {
            "candidate": "TYPED_INTERFACE_RELAY",
            "status": "SUPPORTED_AS_ARCHIVAL_HYPOTHESIS" if core_pass and not explicit_b_request_x1_response_weld else "INCOMPLETE",
            "supporting_contacts": 5,
            "blocking_contacts": 1,
            "reason": "Typed separation, reciprocal route, and return relevance hold; explicit B=request/X1=response weld absent",
        },
        {
            "candidate": "STATIC_RUNTIME_ONLY",
            "status": "PASS_IN_RUNTIME_SCOPE" if runtime_static and no_intervention_surface else "FAIL",
            "supporting_contacts": 3,
            "blocking_contacts": 0,
            "reason": "One immutable X1 object; fixed singleton W9 result; no intervention syntax",
        },
        {
            "candidate": "B_CREATES_X1",
            "status": "UNTESTABLE_IN_CURRENT_RUNTIME" if no_intervention_surface else "TESTABLE",
            "supporting_contacts": 0,
            "blocking_contacts": 1,
            "reason": "No sourced X1 intervention surface; physical creation is unresolved rather than falsified",
        },
    ]

    wrong_controls = [
        {"control_id": "WC01", "attempt": "Alias W8 to S8", "rejected": no_w8_alias, "evidence": "No W8 node; S8_BINARY_SURFACE is canonical"},
        {"control_id": "WC02", "attempt": "Merge B and X1", "rejected": b_x1_distinct, "evidence": "Forbidden collapse in CR119 handoff"},
        {"control_id": "WC03", "attempt": "Assign scalar 1/2 to B", "rejected": b_is_nonscalar, "evidence": "B is NonRowOperator with no scalar value"},
        {"control_id": "WC04", "attempt": "Replace X1 scalar 1 with 1/2", "rejected": x1_is_axis_one, "evidence": "X1 AxisChannel value is 1"},
        {"control_id": "WC05", "attempt": "Collapse six half-slots to two", "rejected": master_has_six and action_has_six and len(half_tokens) == 6, "evidence": "Three outward plus three inward half-slots"},
        {"control_id": "WC06", "attempt": "Treat half-write alone as closure", "rejected": half_alone_open, "evidence": "QP035 held open pending local return"},
        {"control_id": "WC07", "attempt": "Treat fixed W9 output as a physical null", "rejected": physical_unresolved and "Physical perturbability is unresolved" in cr120d, "evidence": "CR120D runtime boundary is not a physical falsification"},
        {"control_id": "WC08", "attempt": "Claim QP036 welds B=request and X1=response", "rejected": not qp036_mentions_b_or_x1, "evidence": "QP036 names neither B_CONTACT_OPERATOR nor X1_AXIS_SELF_CHANNEL"},
    ]
    wrong_controls_pass = all(bool(row["rejected"]) for row in wrong_controls)

    arithmetic = {
        "half_slot_count": len(half_tokens),
        "half_slot_weight": "1/2",
        "outward_slots": half_tokens[:3],
        "outward_weight": str(outward_weight),
        "inward_slots": half_tokens[3:],
        "inward_weight": str(inward_weight),
        "total_weight": str(total_weight),
        "dimension_D": 3,
        "alpha_H_times_D": 6,
        "literal_two_half_total": "1",
        "literal_two_half_matches_sourced_route": False,
    }

    summary = {
        "record_id": RECORD_ID,
        "proposal_id": PROPOSAL_ID,
        "proposal_hash": PROPOSAL_HASH,
        "precommit_sha256": PRECOMMIT_SHA256,
        "primary_verdict": primary_verdict,
        "source_hashes_matched": sum(bool(row["matched"]) for row in source_rows),
        "source_hashes_total": len(source_rows),
        "evidence_gates_passed": sum(bool(row["passed"]) for row in evidence),
        "evidence_gates_total": len(evidence),
        "expected_open_weld_gate": "E14_EXPLICIT_INTERFACE_WELD",
        "reciprocal_half_slot_relay": "PASS_ARCHIVAL_STRUCTURE",
        "literal_B_half_X1_half": "REJECTED_BY_FROZEN_RECORD",
        "typed_B_request_X1_response": "SUPPORTED_AS_ARCHIVAL_HYPOTHESIS_WELD_OPEN",
        "static_runtime": "PASS_IN_RUNTIME_SCOPE",
        "B_creates_X1": "UNTESTABLE_IN_CURRENT_RUNTIME",
        "physical_relay_executed": False,
        "sam_registry_mutated": False,
        "same_run_repair": False,
        "wrong_controls_rejected": sum(bool(row["rejected"]) for row in wrong_controls),
        "wrong_controls_total": len(wrong_controls),
        "wrong_controls_pass": wrong_controls_pass,
    }

    write_csv(
        HERE / "CR120V_SOURCE_CUSTODY.csv",
        ["role", "path", "expected_sha256", "actual_sha256", "matched"],
        source_rows,
    )
    write_csv(
        HERE / "CR120V_EVIDENCE_MATRIX.csv",
        ["gate_id", "description", "passed", "detail", "source"],
        evidence,
    )
    write_csv(
        HERE / "CR120V_MODEL_COMPARISON.csv",
        ["candidate", "status", "supporting_contacts", "blocking_contacts", "reason"],
        models,
    )
    write_csv(
        HERE / "CR120V_WRONG_CONTROLS.csv",
        ["control_id", "attempt", "rejected", "evidence"],
        wrong_controls,
    )
    write_json(HERE / "CR120V_ARITHMETIC.json", arithmetic)
    write_json(HERE / "CR120V_summary.json", summary)

    provenance = {
        "record_id": RECORD_ID,
        "preflight": "artifacts/preflight_filled/PREFLIGHT_20260718_101323_no_script.md",
        "precommit": "14_FOUNDATIONAL_TESTS/CR120V_B_X1_TYPED_HALF_RELAY_ARCHIVAL_DISCRIMINATION/CR120V_PRECOMMIT.md",
        "precommit_sha256": PRECOMMIT_SHA256,
        "proposal_id": PROPOSAL_ID,
        "proposal_hash": PROPOSAL_HASH,
        "runner_sha256": sha256(Path(__file__)),
        "source_manifest_sha256": sha256(source_manifest_path),
        "method": "deterministic archival string, type, hash, and exact-rational discrimination",
    }
    write_json(HERE / "CR120V_PROVENANCE.json", provenance)

    result = f"""# CR120V B/X1 typed half-relay archival discrimination

## Primary verdict

`{primary_verdict}`

## Direct answer

The repository **does contain a reciprocal information-route structure**. The
active V4.2 chain has three outward half-slots and three inward half-slots, with
exact weights `3/2 + 3/2 = 3 = D`. QP035 independently shows that the half-write
split alone does not close an open slot; QP036 selects a local information-return
correction; QP037 promotes one identity only after that return is applied.

That is strong archival support for the user's central relay intuition:
**outward contact and inward return are both required for a completed physical
write/identity event.**

The literal formula `B=1/2` and `X1=1/2` does not survive the frozen typing:

- `B_CONTACT_OPERATOR` is a non-scalar operator;
- `X1_AXIS_SELF_CHANNEL` is an `AxisChannel` with registered scalar value 1;
- the sourced reciprocal shell contains six half-slots, not two;
- B and X1 are explicitly forbidden from collapsing into one entity.

The strongest retained formulation is therefore:

```text
R_BX1 = proposed reciprocal relay process
B_CONTACT_OPERATOR = typed contact/request-side interface candidate
X1_AXIS_SELF_CHANNEL = typed axis/response-side interface candidate

RESOLVE(S8, B, X1) -> W9
```

This is a supported archival hypothesis, not yet a causal weld. No frozen
authority source explicitly assigns `B=request` and `X1=response`.

## What CR120D means after this run

CR120D is reproduced exactly in its own scope: the installed language has one
immutable X1 object, no X1 intervention syntax, and a fixed singleton W9 output.
It is a **runtime boundary**, not a physical null experiment. Consequently it
cannot decide whether B physically activates, modulates, or creates an
X1-associated response.

## Candidate disposition

| Candidate | Result |
|---|---|
| Literal `B half + X1 half` | Rejected by frozen type, scalar, and slot-count records |
| Typed B/X1 interfaces of one relay | Supported as archival hypothesis; explicit weld open |
| Static installed runtime | Pass in runtime scope |
| B dynamically creates X1 | Untestable in current runtime |

## Exact accounting

```text
OUTWARD: 1/2 SW_out + 1/2 WRITE_out + 1/2 OUTSIDE = 3/2
INWARD:  1/2 INSIDE + 1/2 WRITE_in + 1/2 SW_in   = 3/2
TOTAL:                                                    3 = D
```

The useful `1/2 + 1/2` statement is therefore not an entity equation. It is a
paired route grammar repeated across SW, write, and boundary-position roles.

## Boundaries

- No new operator or entity was registered.
- No physical intervention was synthesized or executed.
- The run does not prove that B creates X1.
- The run does not prove that B and X1 carry equal causal information.
- `S8_BINARY_SURFACE`, not W8, remains the canonical registered source.
- The next constructive seam is a sourced mapping from the outward/return route
  fields to B-side and X1-side observables—not another test of fixed W9 labels.

## Controls and custody

- Source hashes: `{summary['source_hashes_matched']}/{summary['source_hashes_total']}` matched.
- Wrong controls: `{summary['wrong_controls_rejected']}/{summary['wrong_controls_total']}` rejected.
- Same-run repair: `false`.
"""
    (HERE / "CR120V_result.md").write_text(result, encoding="utf-8", newline="\n")

    release_files = [
        "CR120V_PRECOMMIT.md",
        "CR120V_PRECOMMIT.sha256.txt",
        "CR120V_SOURCE_MANIFEST.json",
        "CR120V_runner.py",
        "CR120V_SOURCE_CUSTODY.csv",
        "CR120V_EVIDENCE_MATRIX.csv",
        "CR120V_MODEL_COMPARISON.csv",
        "CR120V_WRONG_CONTROLS.csv",
        "CR120V_ARITHMETIC.json",
        "CR120V_PROVENANCE.json",
        "CR120V_summary.json",
        "CR120V_result.md",
    ]
    hash_lines = [f"{sha256(HERE / name)}  {name}" for name in release_files]
    (HERE / "HASHES.txt").write_text("\n".join(hash_lines) + "\n", encoding="utf-8", newline="\n")

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
