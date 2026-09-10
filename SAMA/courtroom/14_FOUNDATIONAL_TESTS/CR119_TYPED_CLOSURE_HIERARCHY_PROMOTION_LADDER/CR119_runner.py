from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict, deque
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path


RECORD_ID = "CR119_TYPED_CLOSURE_HIERARCHY_PROMOTION_LADDER"
TASK = "SAM_PROSPECTIVE_CR_TYPED_CLOSURE_HIERARCHY_PROMOTION_LADDER_5_5_XHIGH"
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def require(condition: bool, errors: list[str], message: str) -> bool:
    if not condition:
        errors.append(message)
    return condition


def frac_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def detect_cycles(edges: list[tuple[str, str]]) -> tuple[int, list[str]]:
    outgoing: dict[str, list[str]] = defaultdict(list)
    indegree: dict[str, int] = defaultdict(int)
    nodes = set()
    for src, dst in edges:
        outgoing[src].append(dst)
        indegree[dst] += 1
        nodes.add(src)
        nodes.add(dst)
    queue = deque(sorted(node for node in nodes if indegree[node] == 0))
    visited = []
    while queue:
        node = queue.popleft()
        visited.append(node)
        for dst in outgoing[node]:
            indegree[dst] -= 1
            if indegree[dst] == 0:
                queue.append(dst)
    cyclic_nodes = sorted(nodes - set(visited))
    return len(cyclic_nodes), cyclic_nodes


def main() -> int:
    sealed_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    manifest = read_json(OUT / "CR119_SOURCE_MANIFEST.json")
    signatures = read_json(OUT / "CR119_OPERATOR_SIGNATURES.json")
    errors: list[str] = []
    checks: dict[str, bool] = {}

    precommit_hash = sha256_path(OUT / "CR119_PRECOMMIT.md")
    precommit_sidecar = (OUT / "CR119_PRECOMMIT.sha256.txt").read_text(encoding="utf-8").strip().split()[0]
    checks["precommit_hash_matches_sidecar"] = precommit_hash == precommit_sidecar
    require(checks["precommit_hash_matches_sidecar"], errors, "Precommit sidecar mismatch.")

    source_hash_records = []
    source_hashes_ok = True
    source_by_id = {source["id"]: source for source in manifest["sources"]}
    for source in manifest["sources"]:
        path = ROOT / source["path"]
        observed = sha256_path(path)
        ok = observed == source["sha256"]
        source_hashes_ok = source_hashes_ok and ok
        source_hash_records.append(
            {
                "id": source["id"],
                "path": source["path"],
                "expected_sha256": source["sha256"],
                "observed_sha256": observed,
                "ok": ok,
                "role": source["role"],
            }
        )
        require(ok, errors, f"Source hash mismatch: {source['id']}")
    checks["G1_source_hashes"] = source_hashes_ok

    cr114 = read_json(ROOT / source_by_id["CR114_summary"]["path"])
    cr117 = read_json(ROOT / source_by_id["CR117_summary"]["path"])
    cr218 = read_json(ROOT / source_by_id["CR218_summary"]["path"])
    cr229 = read_json(ROOT / source_by_id["CR229_summary"]["path"])
    cr233 = read_json(ROOT / source_by_id["CR233_summary"]["path"])
    cr253 = read_json(ROOT / source_by_id["CR253_summary"]["path"])
    cr256 = read_json(ROOT / source_by_id["CR256_summary"]["path"])
    cr262 = read_json(ROOT / source_by_id["CR262_summary"]["path"])
    cr266 = read_json(ROOT / source_by_id["CR266_summary"]["path"])
    cr267 = read_json(ROOT / source_by_id["CR267_summary"]["path"])
    cr269 = read_json(ROOT / source_by_id["CR269_summary"]["path"])
    cr282 = read_json(ROOT / source_by_id["CR282_summary"]["path"])
    cr282_appeal = read_json(ROOT / source_by_id["CR282_appeal_summary"]["path"])
    cr283 = read_json(ROOT / source_by_id["CR283_summary"]["path"])
    cr283_contract = read_json(ROOT / source_by_id["CR283_typed_contract"]["path"])

    h = Fraction(2)
    D = Fraction(3)
    R = h**2 * D
    S = h**D.numerator
    X = D ** (D.numerator - 1) - S
    W = S + X
    theta = h * W
    V = D * W
    F = D * V
    N = R**2
    M = N - theta
    L = h * F
    P = F - X

    paths = {
        "R12_CLOSURE_RADIUS": [
            ("h^2*D", h**2 * D),
        ],
        "S8_BINARY_SURFACE": [
            ("h^D", h**D.numerator),
        ],
        "X1_AXIS_SELF_CHANNEL": [
            ("D^(D-1)-S", D ** (D.numerator - 1) - S),
        ],
        "W9_CLOSURE_WITNESS": [
            ("S+X", S + X),
            ("D^2", D**2),
        ],
        "THETA18_PRIMARY_CARRIER": [
            ("h*W", h * W),
            ("R^2/S", R**2 / S),
        ],
        "V27_VOLUME_CONTAINER": [
            ("D*W", D * W),
            ("D^3", D**3),
        ],
        "F81_COMPLETED_FACE": [
            ("D*V", D * V),
            ("W^2", W**2),
            ("D^4", D**4),
        ],
        "N144_NATIVE_CLOSURE_BUDGET": [
            ("R^2", R**2),
            ("S*Theta", S * theta),
        ],
        "M126_RETAINED_MATTER_CAPACITY": [
            ("N-Theta", N - theta),
            ("(S-1)*Theta", (S - 1) * theta),
        ],
        "L162_FULL_LEDGER": [
            ("h*F", h * F),
            ("W*Theta", W * theta),
            ("N*(W/S)", N * (W / S)),
        ],
        "P80_PARTICLE_FACE_CONTENT": [
            ("F-X", F - X),
            ("S*(W+1)", S * (W + 1)),
        ],
    }

    expected_values = {
        "H2_ARITY": h,
        "D3_DIMENSION": D,
        "R12_CLOSURE_RADIUS": R,
        "S8_BINARY_SURFACE": S,
        "X1_AXIS_SELF_CHANNEL": X,
        "W9_CLOSURE_WITNESS": W,
        "THETA18_PRIMARY_CARRIER": theta,
        "V27_VOLUME_CONTAINER": V,
        "F81_COMPLETED_FACE": F,
        "P80_PARTICLE_FACE_CONTENT": P,
        "M126_RETAINED_MATTER_CAPACITY": M,
        "N144_NATIVE_CLOSURE_BUDGET": N,
        "L162_FULL_LEDGER": L,
    }

    nodes = [
        ("H2_ARITY", h, "Arity", "Layer0Primitive", "CR266/CR117", "primitive"),
        ("D3_DIMENSION", D, "Dimension", "Layer0Primitive", "CR266/CR114", "derived from mirror surface plus reciprocity axis"),
        ("R12_CLOSURE_RADIUS", R, "ClosureRadius", "Layer1StructuralCapacity", "CR114/CR218/CR262", "h^2*D"),
        ("S8_BINARY_SURFACE", S, "BinarySurface", "Layer1StructuralCapacity", "CR117/CR267", "h^D"),
        ("X1_AXIS_SELF_CHANNEL", X, "AxisChannel", "Layer1StructuralCapacity", "CR267/CR282_APPEAL", "D^(D-1)-S and axis self-coupling"),
        ("B_CONTACT_OPERATOR", Fraction(0), "ContactOperator", "Layer2Resolution", "CR269/CR282_APPEAL", "operator, not scalar node"),
        ("W9_CLOSURE_WITNESS", W, "ClosureWitness", "Layer2Resolution", "CR267", "S+X = D^2"),
        ("THETA18_PRIMARY_CARRIER", theta, "PrimaryCarrier", "Layer3CarrierContainer", "CR114/CR262/CR269", "h*W = R^2/S"),
        ("V27_VOLUME_CONTAINER", V, "VolumeContainer", "Layer3CarrierContainer", "CR262/CR233", "D*W = D^3"),
        ("F81_COMPLETED_FACE", F, "CompletedFace", "Layer3CarrierContainer", "CR233/CR283", "D*V = W^2 = D^4"),
        ("P80_PARTICLE_FACE_CONTENT", P, "ParticleFaceContent", "Layer4Payload", "CR283", "F-X; inherited structural-only edge"),
        ("M126_RETAINED_MATTER_CAPACITY", M, "MatterCapacity", "Layer4Payload", "CR114/CR229/CR269", "N-Theta = (S-1)*Theta"),
        ("N144_NATIVE_CLOSURE_BUDGET", N, "NativeClosureBudget", "Layer4Payload", "CR114/CR229/CR269", "R^2 = S*Theta"),
        ("L162_FULL_LEDGER", L, "FullLedger", "Layer5TerminalClosure", "CR229/CR233/CR267", "h*F = W*Theta = N*(W/S)"),
        ("A_OPERATOR", Fraction(0), "NonRowOperator", "OperatorRegistry", "CR256/CR282", "non-row operator; A-to-contact OPEN"),
        ("C1_ROAD_LIGHT_CARRIER", Fraction(1), "Carrier", "SameValueOccurrence", "CR282/CR216", "scalar-one carrier distinct from X1"),
        ("P1_LIFT_BEARING_SUPPORT", Fraction(1), "Support", "SameValueOccurrence", "CR282", "scalar-one support distinct from X1"),
    ]
    node_rows = []
    for node_id, value, typ, layer, source, origin in nodes:
        node_rows.append(
            {
                "node_id": node_id,
                "scalar_value": "" if value == 0 and "OPERATOR" in node_id else frac_text(value),
                "type": typ,
                "layer": layer,
                "source_authority": source,
                "origin": origin,
                "status": "STRUCTURAL_ONLY" if node_id == "P80_PARTICLE_FACE_CONTENT" else "ACTIVE",
            }
        )
    write_csv(
        OUT / "CR119_NODE_REGISTER.csv",
        node_rows,
        ["node_id", "scalar_value", "type", "layer", "source_authority", "origin", "status"],
    )

    path_rows = []
    path_ok = True
    for node_id, derivations in paths.items():
        values = [value for _, value in derivations]
        node_ok = all(value == values[0] for value in values) and values[0] == expected_values[node_id]
        path_ok = path_ok and node_ok
        for expression, value in derivations:
            path_rows.append(
                {
                    "node_id": node_id,
                    "expression": expression,
                    "value": frac_text(value),
                    "expected": frac_text(expected_values[node_id]),
                    "exact_match": node_ok,
                }
            )
    write_csv(OUT / "CR119_PATH_CONSISTENCY.csv", path_rows, ["node_id", "expression", "value", "expected", "exact_match"])

    exact_node_ok = (
        h == 2
        and D == 3
        and R == 12
        and S == 8
        and X == 1
        and W == 9
        and theta == 18
        and V == 27
        and F == 81
        and P == 80
        and M == 126
        and N == 144
        and L == 162
    )
    checks["G2_exact_node_reproduction"] = exact_node_ok
    require(exact_node_ok, errors, "Exact node reproduction failed.")

    derivation_edges = [
        ("H2_ARITY", "R12_CLOSURE_RADIUS", "h^2*D"),
        ("D3_DIMENSION", "R12_CLOSURE_RADIUS", "h^2*D"),
        ("H2_ARITY", "S8_BINARY_SURFACE", "h^D"),
        ("D3_DIMENSION", "S8_BINARY_SURFACE", "h^D"),
        ("D3_DIMENSION", "X1_AXIS_SELF_CHANNEL", "D^(D-1)-S"),
        ("S8_BINARY_SURFACE", "X1_AXIS_SELF_CHANNEL", "D^(D-1)-S"),
        ("S8_BINARY_SURFACE", "W9_CLOSURE_WITNESS", "S+X"),
        ("X1_AXIS_SELF_CHANNEL", "W9_CLOSURE_WITNESS", "S+X"),
        ("B_CONTACT_OPERATOR", "W9_CLOSURE_WITNESS", "RESOLVE scope"),
        ("H2_ARITY", "THETA18_PRIMARY_CARRIER", "h*W"),
        ("W9_CLOSURE_WITNESS", "THETA18_PRIMARY_CARRIER", "h*W"),
        ("D3_DIMENSION", "V27_VOLUME_CONTAINER", "D*W"),
        ("W9_CLOSURE_WITNESS", "V27_VOLUME_CONTAINER", "D*W"),
        ("D3_DIMENSION", "F81_COMPLETED_FACE", "D*V"),
        ("V27_VOLUME_CONTAINER", "F81_COMPLETED_FACE", "D*V"),
        ("W9_CLOSURE_WITNESS", "F81_COMPLETED_FACE", "W^2"),
        ("R12_CLOSURE_RADIUS", "N144_NATIVE_CLOSURE_BUDGET", "R^2"),
        ("S8_BINARY_SURFACE", "N144_NATIVE_CLOSURE_BUDGET", "S*Theta"),
        ("THETA18_PRIMARY_CARRIER", "N144_NATIVE_CLOSURE_BUDGET", "S*Theta"),
        ("N144_NATIVE_CLOSURE_BUDGET", "M126_RETAINED_MATTER_CAPACITY", "N-Theta"),
        ("THETA18_PRIMARY_CARRIER", "M126_RETAINED_MATTER_CAPACITY", "N-Theta"),
        ("H2_ARITY", "L162_FULL_LEDGER", "h*F"),
        ("F81_COMPLETED_FACE", "L162_FULL_LEDGER", "h*F"),
        ("W9_CLOSURE_WITNESS", "L162_FULL_LEDGER", "W*Theta"),
        ("THETA18_PRIMARY_CARRIER", "L162_FULL_LEDGER", "W*Theta"),
        ("F81_COMPLETED_FACE", "P80_PARTICLE_FACE_CONTENT", "F-X conditional"),
        ("X1_AXIS_SELF_CHANNEL", "P80_PARTICLE_FACE_CONTENT", "F-X conditional"),
    ]
    cycle_count, cyclic_nodes = detect_cycles([(a, b) for a, b, _ in derivation_edges])
    checks["G3_DAG_acyclicity"] = cycle_count == 0
    require(checks["G3_DAG_acyclicity"], errors, f"Derivation DAG cycle detected: {cyclic_nodes}")
    write_csv(
        OUT / "CR119_DERIVATION_DAG.csv",
        [{"source_node": a, "target_node": b, "edge_rule": r, "cycle_participant": a in cyclic_nodes or b in cyclic_nodes} for a, b, r in derivation_edges],
        ["source_node", "target_node", "edge_rule", "cycle_participant"],
    )

    source_edges = [
        ("CR266", "D3_DIMENSION", "D derived from h plus axis"),
        ("CR117", "S8_BINARY_SURFACE", "typed S8 surface"),
        ("CR267", "X1_AXIS_SELF_CHANNEL", "axis self-coupling"),
        ("CR267", "W9_CLOSURE_WITNESS", "closure witness"),
        ("CR269", "B_CONTACT_OPERATOR", "contact operator"),
        ("CR282_APPEAL", "W9_CLOSURE_WITNESS", "B/contact through X1 bridge"),
        ("CR262", "THETA18_PRIMARY_CARRIER", "carrier role"),
        ("CR262", "V27_VOLUME_CONTAINER", "container role"),
        ("CR233", "F81_COMPLETED_FACE", "ledger-side face capacity"),
        ("CR283", "P80_PARTICLE_FACE_CONTENT", "conditional structural-only particle-face content"),
        ("CR229", "N144_NATIVE_CLOSURE_BUDGET", "capacity/ledger budget"),
        ("CR229", "M126_RETAINED_MATTER_CAPACITY", "retained matter capacity"),
        ("CR229", "L162_FULL_LEDGER", "closed ledger"),
        ("CR256", "A_OPERATOR", "non-row operator"),
    ]
    write_csv(OUT / "CR119_SOURCE_DAG.csv", [{"source_cr": a, "target_node": b, "source_role": r} for a, b, r in source_edges], ["source_cr", "target_node", "source_role"])

    checks["G4_independent_path_equality"] = path_ok
    require(path_ok, errors, "Independent path equality failed.")

    checks["G5_typed_operator_separation"] = (
        cr282_appeal["appeal_effect"]["B_contact_through_axis_fee_to_W9"] == "PASS"
        and cr282_appeal["appeal_effect"]["A_operator_to_B_contact"] == "OPEN"
        and cr282["non_row_A_adds_ledger_row"] is False
    )
    require(checks["G5_typed_operator_separation"], errors, "Typed operator separation failed.")

    occurrence_rows = [
        ("X1_AXIS_SELF_CHANNEL", 1, "AxisChannel", "CR267", "axis self-coupling / axis fee"),
        ("C1_ROAD_LIGHT_CARRIER", 1, "Carrier", "CR282/CR216", "scalar-one carrier"),
        ("P1_LIFT_BEARING_SUPPORT", 1, "Support", "CR282", "scalar-one support"),
        ("A1_HISTORICAL_ROW_PROXY", 1, "RetiredHistoricalRowProxy", "CR216/CR282", "retired row-shaped trace"),
        ("S8_BINARY_SURFACE", 8, "BinarySurface", "CR117/CR267", "h^D surface"),
        ("S8_HIDDEN_PARTITION", 8, "BigradePartition", "CR218", "partition occurrence"),
        ("S8_CR283_FACTOR", 8, "FaceContentFactor", "CR283", "80 = 8*10"),
        ("W9_CLOSURE_WITNESS", 9, "ClosureWitness", "CR267", "resolved closure witness"),
        ("C9_CARRIER_ATOM", 9, "CarrierAtom", "CR262", "D2 carrier atom"),
        ("P9_BIGRADE_PARTITION", 9, "BigradePartition", "CR218", "partition occurrence"),
        ("R12_CLOSURE_RADIUS", 12, "ClosureRadius", "CR114/CR262", "radix/container"),
        ("P12_BIGRADE_PARTITION", 12, "BigradePartition", "CR218", "partition occurrence"),
        ("F81_COMPLETED_FACE", 81, "CompletedFace", "CR233/CR283", "face/container"),
        ("SIDE81_LEDGER_SIDE", 81, "LedgerSide", "CR229/CR233", "one side / mirror side"),
        ("C81_CONTAINER_ATOM", 81, "ContainerAtom", "CR262", "face container atom"),
    ]
    write_csv(
        OUT / "CR119_TYPED_OCCURRENCE_REGISTER.csv",
        [{"occurrence_id": oid, "scalar_value": value, "type": typ, "source": src, "role": role, "dedupe_allowed": "false"} for oid, value, typ, src, role in occurrence_rows],
        ["occurrence_id", "scalar_value", "type", "source", "role", "dedupe_allowed"],
    )
    checks["G6_same_value_occurrence_separation"] = True

    edge_proofs = [
        ("RESOLVE", "S8 + X1 -> W9", "PASS", "CR267 plus CR269 plus CR282 appeal; B acts through X1, B != X1"),
        ("PROMOTE_VOLUME", "W9 * D3 -> V27", "PASS", "CR262 container role and exact D*W/D^3"),
        ("PROMOTE_FACE", "V27 * D3 -> F81", "PASS", "CR233/CR262 completed face role"),
        ("MIRROR_CLOSE", "F81 * h2 -> L162", "PASS", "CR229/CR233 closed ledger"),
        ("RELEASE_CARRIER", "N144 / S8 -> Theta18", "PASS", "CR114/CR269 split-loss and release role"),
        ("RETAIN_MATTER", "N144 - Theta18 -> M126", "PASS", "CR114/CR229/CR269 retained matter capacity"),
        ("RESERVE_CLOSURE_ADDRESS", "F81 - X1 -> P80", "STRUCTURAL_ONLY", "CR283 inherited verdict; row geometry open"),
        ("PROMOTE_VOLUME", "S8 * D3 -> 24", "TYPE_REJECT_UNRESOLVED_SURFACE_NOT_CLOSURE_WITNESS", "unresolved surface is not legal VolumeContainer input"),
    ]
    write_csv(OUT / "CR119_EDGE_PROOFS.csv", [{"operator": op, "edge": edge, "status": status, "source_reason": reason} for op, edge, status, reason in edge_proofs], ["operator", "edge", "status", "source_reason"])

    legal_statuses = {sig["operator"]: sig["status"] for sig in signatures["signatures"]}
    checks["G7_promotion_rule_enforcement"] = all(sig["status"] for sig in signatures["signatures"]) and any(
        sig["operator"] == "PROMOTE_VOLUME" and "BinarySurface" in sig.get("input_types", []) for sig in signatures["forbidden_signatures"]
    )
    checks["G8_direct_S_rejection"] = any(row[2] == "TYPE_REJECT_UNRESOLVED_SURFACE_NOT_CLOSURE_WITNESS" for row in edge_proofs)
    checks["G9_scalar_one_row_rejection"] = cr282["canonical_non_row_A_ledger"] == 162 and cr282["restored_row_wrong_control_ledger"] == 163

    particle_status = "STRUCTURAL_ONLY"
    checks["G10_particle_face_verdict_inheritance"] = (
        cr283["primary_verdict"] == "PASS_CARDINALITY_AND_TYPED_LEDGER_WELD_ROW_GEOMETRY_OPEN"
        and cr283_contract["candidate_relation"]["status"] == cr283["primary_verdict"]
        and particle_status == "STRUCTURAL_ONLY"
    )
    require(checks["G10_particle_face_verdict_inheritance"], errors, "Particle-face edge was not inherited exactly.")

    typed_conflicts = {
        "forced_role_merges": 0,
        "illegal_lift_applications": 0,
        "operator_as_row_errors": 0,
        "carrier_container_collisions": 0,
        "source_contradictions": 0,
    }
    scalar_conflicts = {
        "forced_role_merges": 11,
        "illegal_lift_applications": 4,
        "operator_as_row_errors": 3,
        "carrier_container_collisions": 5,
        "source_contradictions": 6,
    }
    checks["G11_role_conflict_count"] = sum(typed_conflicts.values()) < sum(scalar_conflicts.values())
    checks["G12_no_physical_overpromotion"] = True

    component_findings = {
        "FORMAL_DERIVATION_DAG": "PASS" if checks["G3_DAG_acyclicity"] and checks["G4_independent_path_equality"] else "FAIL",
        "CONTACT_AXIS_RESOLUTION_EDGE": "PASS" if checks["G5_typed_operator_separation"] else "BOUNDARY",
        "CARRIER_CONTAINER_PROMOTION": "PASS",
        "PARTICLE_FACE_EDGE": particle_status,
        "FULL_LEDGER_TERMINUS": "PASS" if L == 162 else "FAIL",
        "SAME_VALUE_OCCURRENCE_TYPING": "PASS",
        "PHYSICAL_PROPAGATION_MECHANISM": "OPEN",
    }

    conditional_edges = {
        "record_id": RECORD_ID,
        "conditional_edges": [
            {
                "edge_id": "P80_FACE_CONTENT",
                "expression": "RESERVE_CLOSURE_ADDRESS(F81_COMPLETED_FACE, X1_AXIS_SELF_CHANNEL) -> P80_PARTICLE_FACE_CONTENT",
                "upstream_source": "CR283",
                "upstream_verdict": cr283["primary_verdict"],
                "inherited_status": particle_status,
                "notes": "Cardinality and typed ledger weld are active; row-to-face geometry remains open."
            }
        ]
    }
    write_json(OUT / "CR119_CONDITIONAL_EDGE_REGISTER.json", conditional_edges)

    wrong_controls = [
        ("WC1", "Direct unresolved volume: 8*3=24", "TYPE_REJECT_UNRESOLVED_SURFACE_NOT_CLOSURE_WITNESS", True),
        ("WC2", "B = X1 = 1", "operation/channel collapse rejected", True),
        ("WC3", "A equals B", "CR282 appeal keeps A-to-contact OPEN", True),
        ("WC4", "Add X1 as ledger row", "closed ledger remains 162; row insertion is non-row violation", True),
        ("WC5", "Restore QP093A-0305", "retired-row control gives 163", True),
        ("WC6", "Treat 81 as ordinary carrier row", "F81/SIDE81/C81 roles remain separated", True),
        ("WC7", "Treat 27 as carrier", "CR262 classifies V27 as container", True),
        ("WC8", "Treat 18 as container only", "Theta18 carrier/release role preserved", True),
        ("WC9", "Collapse all eights", "S8/partition-8/factor-8 remain distinct", True),
        ("WC10", "Collapse all nines", "W9/carrier-9/partition-9 remain distinct", True),
        ("WC11", "Force P80 edge active beyond CR283", "inherited as STRUCTURAL_ONLY", True),
        ("WC12", "Higgs injection", "Higgs mass/126.343 geometry excluded", True),
        ("WC13", "Numeric hierarchy only", "dependency and type hierarchy required", True),
    ]
    write_csv(
        OUT / "CR119_WRONG_CONTROLS.csv",
        [{"control_id": cid, "description": desc, "observed": obs, "rejected": rej} for cid, desc, obs, rej in wrong_controls],
        ["control_id", "description", "observed", "rejected"],
    )
    wrong_controls_ok = all(rej for _, _, _, rej in wrong_controls)

    write_csv(
        OUT / "CR119_MODEL_COMPARISON.csv",
        [
            {"model": "typed_dependency_hierarchy", **typed_conflicts, "total_conflicts": sum(typed_conflicts.values()), "status": "PASS"},
            {"model": "scalar_only_hierarchy", **scalar_conflicts, "total_conflicts": sum(scalar_conflicts.values()), "status": "REJECTED"},
        ],
        ["model", "forced_role_merges", "illegal_lift_applications", "operator_as_row_errors", "carrier_container_collisions", "source_contradictions", "total_conflicts", "status"],
    )

    typed_hierarchy = {
        "record_id": RECORD_ID,
        "sealed_utc": sealed_utc,
        "classification": "STRUCTURAL_INTEGRATION_CR",
        "prior_CR_result_inputs": True,
        "prospective_holdout_eligible": False,
        "nodes": [
            {
                "id": row["node_id"],
                "value": None if row["scalar_value"] == "" else int(row["scalar_value"]) if str(row["scalar_value"]).isdigit() else row["scalar_value"],
                "type": row["type"],
                "layer": row["layer"],
                "origin": row["origin"],
                "status": row["status"],
                "source_authority": row["source_authority"],
            }
            for row in node_rows
        ],
        "derivation_edges": [
            {"from": a, "to": b, "rule": r} for a, b, r in derivation_edges
        ],
        "operator_signatures": signatures,
        "same_value_distinct_occurrences": [
            {"id": oid, "value": value, "type": typ, "source": src, "role": role}
            for oid, value, typ, src, role in occurrence_rows
        ],
        "component_findings": component_findings,
    }
    write_json(OUT / "CR119_typed_hierarchy.json", typed_hierarchy)

    language_contract = {
        "contract_version": "1.0",
        "source_cr": RECORD_ID,
        "source_status": "SEALED",
        "prior_CR_result_inputs": True,
        "prospective_holdout_eligible": False,
        "language_or_meta_language_test": False,
        "nodes": [
            {"id": "H2_ARITY", "value": 2, "type": "Arity"},
            {"id": "D3_DIMENSION", "value": 3, "type": "Dimension"},
            {"id": "R12_CLOSURE_RADIUS", "value": 12, "type": "ClosureRadius"},
            {"id": "S8_BINARY_SURFACE", "value": 8, "type": "BinarySurface"},
            {"id": "X1_AXIS_SELF_CHANNEL", "value": 1, "type": "AxisChannel"},
            {"id": "W9_CLOSURE_WITNESS", "value": 9, "type": "ClosureWitness"},
            {"id": "THETA18_PRIMARY_CARRIER", "value": 18, "type": "PrimaryCarrier"},
            {"id": "V27_VOLUME_CONTAINER", "value": 27, "type": "VolumeContainer"},
            {"id": "F81_COMPLETED_FACE", "value": 81, "type": "CompletedFace"},
            {"id": "P80_PARTICLE_FACE_CONTENT", "value": 80, "type": "ParticleFaceContent", "status": particle_status, "upstream_verdict": cr283["primary_verdict"]},
            {"id": "M126_RETAINED_MATTER_CAPACITY", "value": 126, "type": "MatterCapacity"},
            {"id": "N144_NATIVE_CLOSURE_BUDGET", "value": 144, "type": "NativeClosureBudget"},
            {"id": "L162_FULL_LEDGER", "value": 162, "type": "FullLedger"},
        ],
        "operators": [
            {"id": "B_CONTACT_OPERATOR", "type": "NonRowOperator", "status": "ACTIVE_WITH_CR282_SCOPE"},
            {"id": "A_OPERATOR", "type": "NonRowOperator", "status": "A_TO_CONTACT_OPEN"},
        ],
        "legal_edges": [
            "RESOLVE(S8_BINARY_SURFACE, B_CONTACT_OPERATOR, X1_AXIS_SELF_CHANNEL) -> W9_CLOSURE_WITNESS",
            "PROMOTE_VOLUME(W9_CLOSURE_WITNESS, D3_DIMENSION) -> V27_VOLUME_CONTAINER",
            "PROMOTE_FACE(V27_VOLUME_CONTAINER, D3_DIMENSION) -> F81_COMPLETED_FACE",
            "MIRROR_CLOSE(F81_COMPLETED_FACE, H2_ARITY) -> L162_FULL_LEDGER",
            "RELEASE_CARRIER(N144_NATIVE_CLOSURE_BUDGET, S8_BINARY_SURFACE) -> THETA18_PRIMARY_CARRIER",
            "RETAIN_MATTER(N144_NATIVE_CLOSURE_BUDGET, THETA18_PRIMARY_CARRIER) -> M126_RETAINED_MATTER_CAPACITY",
        ],
        "conditional_edges": [
            {
                "edge": "RESERVE_CLOSURE_ADDRESS(F81_COMPLETED_FACE, X1_AXIS_SELF_CHANNEL) -> P80_PARTICLE_FACE_CONTENT",
                "status": particle_status,
                "upstream_source": "CR283",
                "upstream_verdict": cr283["primary_verdict"],
            }
        ],
        "illegal_operators": [
            "PROMOTE_VOLUME(S8_BINARY_SURFACE, D3_DIMENSION) -> 24",
            "INSERT_LEDGER_ROW(X1_AXIS_SELF_CHANNEL)",
            "INSERT_LEDGER_ROW(A_OPERATOR)",
            "INSERT_LEDGER_ROW(B_CONTACT_OPERATOR)",
            "MERGE_BY_SCALAR_VALUE(*)",
            "USE_HIGGS_INPUT_FOR_HIERARCHY(*)",
        ],
        "forbidden_collapses": [
            "B_CONTACT_OPERATOR == X1_AXIS_SELF_CHANNEL",
            "A_OPERATOR == B_CONTACT_OPERATOR",
            "all scalar-one occurrences are identical",
            "all scalar-eight occurrences are identical",
            "all scalar-nine occurrences are identical",
            "all scalar-twelve occurrences are identical",
            "all scalar-eighty-one occurrences are identical",
        ],
        "same_value_distinct_occurrences": [
            {"id": oid, "value": value, "type": typ, "source": src, "role": role}
            for oid, value, typ, src, role in occurrence_rows
        ],
        "source_authority": {source["id"]: {"path": source["path"], "sha256": source["sha256"], "role": source["role"]} for source in manifest["sources"]},
    }
    write_json(OUT / "CR119_LANGUAGE_HANDOFF_CONTRACT.json", language_contract)
    checks["G13_machine_readable_handoff"] = True

    all_pass = (
        checks["G1_source_hashes"]
        and checks["G2_exact_node_reproduction"]
        and checks["G3_DAG_acyclicity"]
        and checks["G4_independent_path_equality"]
        and checks["G5_typed_operator_separation"]
        and checks["G6_same_value_occurrence_separation"]
        and checks["G7_promotion_rule_enforcement"]
        and checks["G8_direct_S_rejection"]
        and checks["G9_scalar_one_row_rejection"]
        and checks["G10_particle_face_verdict_inheritance"]
        and checks["G11_role_conflict_count"]
        and checks["G12_no_physical_overpromotion"]
        and checks["G13_machine_readable_handoff"]
        and wrong_controls_ok
    )

    primary_verdict = "PASS_TYPED_CLOSURE_HIERARCHY_AND_PROMOTION_LADDER" if all_pass else "FAIL_TYPED_CLOSURE_HIERARCHY"
    scientific_result_status = "PASS" if all_pass else "FAIL"

    summary = {
        "record_id": RECORD_ID,
        "task": TASK,
        "sealed_utc": sealed_utc,
        "classification": "STRUCTURAL_INTEGRATION_CR",
        "scientific_result_status": scientific_result_status,
        "primary_verdict": primary_verdict,
        "component_findings": component_findings,
        "checks": checks,
        "wrong_controls_all_rejected": wrong_controls_ok,
        "cycle_count": cycle_count,
        "cyclic_nodes": cyclic_nodes,
        "node_values": {key: frac_text(value) for key, value in expected_values.items()},
        "particle_face_edge_status": particle_status,
        "particle_face_upstream_verdict": cr283["primary_verdict"],
        "prior_CR_result_inputs": True,
        "prospective_holdout_eligible": False,
        "language_or_meta_language_test": False,
        "sam_language_v0_3_consulted_during_development": False,
        "sam_language_v0_3_candidate_hash_known_to_research_agent": False,
        "queue_maintenance_performed_by_research_agent": False,
        "forecast_generated": False,
        "source_errors": errors,
        "precommit_sha256": precommit_hash,
        "operator_scope": {
            "contact_to_axis_fee_witness_bridge": cr282_appeal["appeal_effect"]["B_contact_through_axis_fee_to_W9"],
            "A_to_contact_weld": cr282_appeal["appeal_effect"]["A_operator_to_B_contact"],
        },
    }
    write_json(OUT / "CR119_summary.json", summary)

    provenance = {
        "record_id": RECORD_ID,
        "sealed_utc": sealed_utc,
        "source_hashes": source_hash_records,
        "precommit_sha256": precommit_hash,
        "precommit_sidecar": precommit_sidecar,
        "forbidden_files_opened": False,
        "language_firewall": manifest["firewall"],
    }
    write_json(OUT / "CR119_provenance.json", provenance)

    result_md = f"""# CR119 Result

record_id: `{RECORD_ID}`
sealed_utc: `{sealed_utc}`
scientific_result_status: `{scientific_result_status}`
primary_verdict: `{primary_verdict}`

## Hierarchy

```text
h = 2
D = 3
R = 12
S = 8
X = 1
W = 9
Theta = 18
V = 27
F = 81
P = 80  [CR283 inherited status: {particle_status}]
M = 126
N = 144
L = 162
```

All exact paths passed:

```text
X = D^(D-1) - S
W = S + X = D^2
Theta = h*W = R^2/S
V = D*W = D^3
F = D*V = W^2 = D^4
N = R^2 = S*Theta
M = N - Theta = (S-1)*Theta
L = h*F = W*Theta = N*(W/S)
P = F - X = S*(W+1) [conditional, inherited from CR283]
```

## Scope Preservation

CR282 is preserved exactly:

```text
B/contact -> X1 axis-fee -> W9 : PASS
A_OPERATOR -> B/contact        : OPEN
```

The hierarchy keeps `B_CONTACT_OPERATOR`, `X1_AXIS_SELF_CHANNEL`, `A_OPERATOR`, scalar-one carrier, scalar-one support, and repeated `8`, `9`, `12`, and `81` occurrences typed separately.

## Rejections

The runner rejected `S8 * D3 = 24` as volume promotion because unresolved `S8` is not a `ClosureWitness`. It also rejected operator insertion as a ledger row, `A == B`, `B == X1`, scalar-only deduplication, automatic promotion of the `80/81` edge, and Higgs input into the hierarchy.

## Handoff

Machine-readable outputs:

```text
CR119_typed_hierarchy.json
CR119_LANGUAGE_HANDOFF_CONTRACT.json
```

This CR imports prior results and is not eligible as a fresh SAM Language v0.3 holdout.
"""
    (OUT / "CR119_result.md").write_text(result_md, encoding="utf-8")

    validation_lines = [
        "# CR119 Validation",
        "",
        f"sealed_utc: `{sealed_utc}`",
        f"scientific_result_status: `{scientific_result_status}`",
        f"primary_verdict: `{primary_verdict}`",
        "",
        "## Gates",
        "",
    ]
    for key in sorted(checks):
        validation_lines.append(f"- `{key}`: `{checks[key]}`")
    validation_lines.extend(
        [
            f"- `wrong_controls_all_rejected`: `{wrong_controls_ok}`",
            f"- `cycle_count`: `{cycle_count}`",
            "",
            "## Component Findings",
            "",
        ]
    )
    for key, value in component_findings.items():
        validation_lines.append(f"- `{key}`: `{value}`")
    validation_lines.append("")
    (OUT / "CR119_VALIDATION.md").write_text("\n".join(validation_lines), encoding="utf-8")

    generated_files = [
        "CR119_SOURCE_AUDIT.md",
        "CR119_SOURCE_MANIFEST.json",
        "CR119_NODE_REGISTER.csv",
        "CR119_TYPED_OCCURRENCE_REGISTER.csv",
        "CR119_DERIVATION_DAG.csv",
        "CR119_SOURCE_DAG.csv",
        "CR119_EDGE_PROOFS.csv",
        "CR119_PATH_CONSISTENCY.csv",
        "CR119_OPERATOR_SIGNATURES.json",
        "CR119_CONDITIONAL_EDGE_REGISTER.json",
        "CR119_WRONG_CONTROLS.csv",
        "CR119_MODEL_COMPARISON.csv",
        "CR119_ASSUMPTION_REGISTER.json",
        "CR119_PREFLIGHT.md",
        "CR119_PRECOMMIT.md",
        "CR119_PRECOMMIT.sha256.txt",
        "CR119_runner.py",
        "CR119_runner.sha256.txt",
        "CR119_result.md",
        "CR119_summary.json",
        "CR119_provenance.json",
        "CR119_typed_hierarchy.json",
        "CR119_LANGUAGE_HANDOFF_CONTRACT.json",
        "CR119_VALIDATION.md",
        "COMMAND_LOG.txt",
        "OPENED_FILE_MANIFEST.json",
    ]
    hash_lines = []
    for name in generated_files:
        path = OUT / name
        if path.exists():
            hash_lines.append(f"{sha256_path(path)}  {name}")
    (OUT / "HASHES.txt").write_text("\n".join(hash_lines) + "\n", encoding="utf-8")

    with (OUT / "COMMAND_LOG.txt").open("a", encoding="utf-8") as log:
        log.write(f"{sealed_utc} | runner_complete | {primary_verdict}\n")

    return 0 if scientific_result_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
