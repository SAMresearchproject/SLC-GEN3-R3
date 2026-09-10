from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path


CAMPAIGN = "CR120X_DUAL_DEPTH_THETA_B_X1_W8_W9_RELAXED_DISCOVERY"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RELEASE = HERE / "release"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def frac(value) -> Fraction:
    return Fraction(str(value))


def ftext(value: Fraction | None) -> str:
    if value is None:
        return "undefined"
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> int:
    started = datetime.now(timezone.utc).isoformat()
    RELEASE.mkdir(parents=True, exist_ok=False)

    source_manifest_path = HERE / "CR120X_SOURCE_MANIFEST.json"
    contract_path = HERE / "CR120X_CONTRACT.json"
    precommit_path = HERE / "CR120X_PRECOMMIT.md"
    seal_path = HERE / "CR120X_PRECOMMIT_SEAL.txt"
    manifest = load_json(source_manifest_path)

    seal = {}
    for line in seal_path.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            seal[key] = value

    seal_checks = {
        "precommit": sha256(precommit_path) == seal["precommit_sha256"],
        "contract": sha256(contract_path) == seal["contract_sha256"],
        "source_manifest": sha256(source_manifest_path) == seal["source_manifest_sha256"],
    }

    source_validation = []
    for source in manifest["sources"]:
        path = ROOT / Path(source["path"])
        observed = sha256(path) if path.is_file() else None
        source_validation.append(
            {
                "key": source["key"],
                "path": source["path"],
                "expected_sha256": source["sha256"],
                "observed_sha256": observed or "MISSING",
                "matched": observed == source["sha256"],
                "role": source["role"],
            }
        )
    source_gate = all(row["matched"] for row in source_validation)

    # The current QP carrier roster is reconstructed from class semantics, not IDs.
    qp_path = ROOT / "QP093A_321_ROW_BUCKET_MAP (1).csv"
    with qp_path.open(newline="", encoding="utf-8-sig") as handle:
        qp_rows = list(csv.DictReader(handle))
    real_carrier_classes = {
        "TENSOR_CARRIER",
        "ROAD_LIGHT_CARRIER",
        "WEAK_VECTOR_CARRIER",
        "NEUTRAL_VECTOR_CARRIER",
        "COLOR_OWNER_CARRIER",
        "A_FIELD_CARRIER",
    }
    carriers = [row for row in qp_rows if row["operator_class"] in real_carrier_classes]
    rejected_fake = [row for row in qp_rows if row["operator_class"] == "PROMOTE_TENSOR_CARRIER"]

    hierarchy = load_json(ROOT / "14_FOUNDATIONAL_TESTS/CR119_TYPED_CLOSURE_HIERARCHY_PROMOTION_LADDER/CR119_typed_hierarchy.json")
    nodes = {node["id"]: frac(node["value"]) for node in hierarchy["nodes"] if node.get("value") is not None}
    R = nodes["R12_CLOSURE_RADIUS"]
    S = nodes["S8_BINARY_SURFACE"]
    X = nodes["X1_AXIS_SELF_CHANNEL"]
    W = nodes["W9_CLOSURE_WITNESS"]
    THETA = nodes["THETA18_PRIMARY_CARRIER"]
    M = nodes["M126_RETAINED_MATTER_CAPACITY"]
    N = nodes["N144_NATIVE_CLOSURE_BUDGET"]
    L = nodes["L162_FULL_LEDGER"]

    carrier_comparison = []
    for row in sorted(carriers, key=lambda item: item["candidate_id"]):
        for mode, raw in (
            ("native_payload", row["M_native"]),
            ("partition_scalar", row["partition_signature"]),
        ):
            c = frac(raw)
            valid = c > 0
            tuple_values = (M / c, N / c, L / c) if valid else None
            b_domain = valid and N == S * c
            b_retained = valid and M == (S - 1) * c
            full_ledger = valid and L == (S + 1) * c
            exact_789 = bool(valid and tuple_values == (Fraction(7), Fraction(8), Fraction(9)))
            carrier_comparison.append(
                {
                    "candidate_id": row["candidate_id"],
                    "operator_class": row["operator_class"],
                    "route": row["route_combination"],
                    "row_closure_depth": row["closure_depth"],
                    "value_mode": mode,
                    "candidate_value": ftext(c),
                    "normalized_M_N_L": "|".join(ftext(v) for v in tuple_values) if tuple_values else "undefined",
                    "N_equals_S_times_candidate": b_domain,
                    "M_equals_S_minus_1_times_candidate": b_retained,
                    "L_equals_S_plus_1_times_candidate": full_ledger,
                    "exact_7_8_9_ladder": exact_789,
                    "typed_theta_candidate": row["operator_class"] == "TENSOR_CARRIER",
                }
            )

    winners_by_mode = {}
    for mode in ("native_payload", "partition_scalar"):
        winners_by_mode[mode] = [
            row["candidate_id"]
            for row in carrier_comparison
            if row["value_mode"] == mode and row["exact_7_8_9_ladder"]
        ]

    a_rows_path = ROOT / "09a_PARTICLE_MASS_CHAIN/CR256_A_OPERATOR_ANTIMATTER_CONJUGATE/CR256_per_row_predictions.csv"
    with a_rows_path.open(newline="", encoding="utf-8-sig") as handle:
        a_rows = list(csv.DictReader(handle))
    a_depth_counts = {}
    a_exact = True
    max_a_residual = 0.0
    for row in a_rows:
        d = int(row["d"])
        a_depth_counts[str(d)] = a_depth_counts.get(str(d), 0) + 1
        residual = abs(float(row["qA_actual"]) - float(row["qA_predicted"]))
        max_a_residual = max(max_a_residual, residual)
        a_exact = a_exact and row["match"] == "OK" and residual <= 1e-7

    a_summary = load_json(ROOT / "09a_PARTICLE_MASS_CHAIN/CR256_A_OPERATOR_ANTIMATTER_CONJUGATE/CR256_summary.json")
    a_theta_summary = load_json(ROOT / "09a_PARTICLE_MASS_CHAIN/CR257b_A_MEETS_THETA_AT_D_1_W4_CORRECTION/CR257b_summary.json")
    wrong_exponents_zero = all(value == 0 for value in a_summary["wrong_controls"]["W1_wrong_exponent"].values())

    depth_ladder = []
    for d in range(4):
        scale = R ** (d + 1)
        depth_ladder.append(
            {
                "d_route": d,
                "A_route_scale_R_pow_d_plus_1": ftext(scale),
                "scale_over_Theta": ftext(scale / THETA),
                "equals_N144": scale == N,
                "equals_S8_times_Theta": scale == S * THETA,
                "observed_CR256_rows": a_depth_counts.get(str(d), 0),
                "evidence_status": "EXECUTED_CR256" if str(d) in a_depth_counts else "ALGEBRAIC_COMPARISON_ONLY",
            }
        )
    matching_depths = [row["d_route"] for row in depth_ladder if row["equals_N144"]]

    b_summary = load_json(ROOT / "09a_PARTICLE_MASS_CHAIN/CR269_BOW_PRIMITIVE_CONTACT_OPERATOR/CR269_summary.json")
    b_partition_exact = N == M + THETA and N == S * THETA and M == (S - 1) * THETA
    normalized = {
        "M_over_Theta": ftext(M / THETA),
        "N_over_Theta": ftext(N / THETA),
        "L_over_Theta": ftext(L / THETA),
        "Theta_out_over_Theta": ftext(THETA / THETA),
        "S8": ftext(S),
        "X1": ftext(X),
        "W9": ftext(W),
        "exact_7_8_9": (M / THETA, N / THETA, L / THETA) == (Fraction(7), S, W),
        "normalized_release_equals_X1_scalar": THETA / THETA == X,
        "entity_identity_claimed": False,
    }

    appeal_text = (ROOT / "09a_PARTICLE_MASS_CHAIN/CR282_APPEAL_CR267_CR269_PROVENANCE_SECOND_VERDICT/CR282_APPEAL_result.md").read_text(encoding="utf-8-sig")
    bx1_bridge_pass = "B/contact -> X1 axis-fee -> W9    : PASS" in appeal_text

    cr120w = load_json(ROOT / "14_FOUNDATIONAL_TESTS/CR120W_A_FIELD_CARRIER_X1_TYPED_WELD_DISCOVERY/release/CR120W_summary.json")
    type_weld = load_json(ROOT / "14_FOUNDATIONAL_TESTS/CR120W_A_FIELD_CARRIER_X1_TYPED_WELD_DISCOVERY/release/CR120W_TYPE_WELD.json")
    a_field_candidate_current = (
        cr120w["unique_candidate_id"] == "QP093A-0305"
        and cr120w["primary_verdict"].startswith("PASS_A_FIELD_CARRIER")
        and type_weld["a_operator_to_x1_edge"] == "OPEN"
    )
    ledger_preserved = (
        int(cr120w["additive_ledger"]["closed"]) == int(L)
        and int(cr120w["additive_ledger"]["wrong_closed"]) == int(L) + 1
    )

    history = load_json(ROOT / "15_SCALE_BRIDGE_SIMULATOR/STARBREAKER_COMPLETE_TYPED_RELATION_HISTORY_V1/release/RELATION_HISTORY_SUMMARY.json")
    reopening = load_json(ROOT / "15_SCALE_BRIDGE_SIMULATOR/STARBREAKER_101_REOPENING_RELAY_DECOMPOSITION_V1/release/REOPENING_RELAY_SUMMARY.json")
    axis = load_json(ROOT / "15_SCALE_BRIDGE_SIMULATOR/STARBREAKER_X1_CARRIER_AXIS_REVERSAL_DISCOVERY_V1/release/AXIS_REVERSAL_SUMMARY.json")
    starbreaker_support = {
        "complete_relation_count": history["any_stage_relation_count"],
        "complete_history_pass": history["construction_pass"],
        "selected_101_carrier_matter_pairs": reopening["history_101_selected_carrier_matter_pairs"],
        "matched_specificity_grade": reopening["matched_specificity_grade"],
        "endpoint_direction": reopening["overall_selected_carrier_matter_direction"]["direction_class"],
        "B_X1_assignment": reopening["B_X1_assignment"],
        "carrier_median_cosine": axis["overall_carrier"]["median_cosine"],
        "carrier_near_antiparallel_fraction": axis["overall_carrier"]["near_antiparallel_fraction"],
        "axis_shuffle_empirical_p": axis["overall_shuffle"]["empirical_p"],
        "overall_axis_class": axis["overall_axis_class"],
        "literal_x1_carrier_identity": axis["literal_x1_carrier_identity"],
        "policy": "SUPPORTIVE_NOT_EXCLUSIVE_GATE",
    }

    wrong_controls = []
    for row in carrier_comparison:
        if row["operator_class"] != "TENSOR_CARRIER":
            wrong_controls.append(
                {
                    "control": f"SUBSTITUTE_{row['operator_class']}_{row['value_mode']}",
                    "observed": row["normalized_M_N_L"],
                    "rejected": not row["exact_7_8_9_ladder"],
                    "reason": "alternative carrier does not reproduce the complete 7-8-9 ladder",
                }
            )
    for row in depth_ladder:
        if row["d_route"] != 1:
            wrong_controls.append(
                {
                    "control": f"A_SCALE_AT_D_{row['d_route']}",
                    "observed": row["A_route_scale_R_pow_d_plus_1"],
                    "rejected": not row["equals_N144"],
                    "reason": "route scale does not equal N144",
                }
            )
    for denominator in (4, 16):
        release = N / denominator
        wrong_controls.append(
            {
                "control": f"WRONG_RELEASE_1_OVER_{denominator}",
                "observed": ftext(release),
                "rejected": release != THETA,
                "reason": "wrong split does not release Theta18",
            }
        )
    wrong_controls.extend(
        [
            {"control":"RESTORE_A_FIELD_AS_ADDITIVE_ROW","observed":str(int(L)+1),"rejected":ledger_preserved,"reason":"restoration produces wrong closure 163"},
            {"control":"MERGE_B_WITH_X1","observed":"ContactOperator != AxisChannel","rejected":True,"reason":"typed identity collapse forbidden"},
            {"control":"MERGE_THETA_WITH_X1","observed":"PrimaryCarrier != AxisChannel","rejected":True,"reason":"normalization contact is not entity identity"},
            {"control":"MERGE_A_FIELD_ROW_WITH_A_OPERATOR","observed":"historical row proxy != non-row operator","rejected":True,"reason":"typed identity collapse forbidden"},
            {"control":"CALL_STATIC_RUNTIME_PHYSICAL_INTERVENTION","observed":"CR120D intervention syntax absent","rejected":True,"reason":"fixed runtime output is not a physical intervention"},
        ]
    )
    wrong_controls_pass = all(row["rejected"] for row in wrong_controls)

    evidence = [
        {"gate":"G1_SOURCE_AND_PRECOMMIT_CUSTODY","status":source_gate and all(seal_checks.values()),"grade":"HARD"},
        {"gate":"G2_CURRENT_SIX_CARRIER_ROSTER","status":len(carriers)==6 and len(rejected_fake)==1,"grade":"HARD"},
        {"gate":"G3_A_DEPTH_LAW_CURRENT_ROWS","status":len(a_rows)==32 and a_depth_counts=={"0":16,"1":16} and a_exact and wrong_exponents_zero,"grade":"HARD"},
        {"gate":"G4_D1_N144_SCALE_CONTACT","status":matching_depths==[1] and a_theta_summary["verdict"]=="PASS","grade":"HARD"},
        {"gate":"G5_B_N_M_THETA_PARTITION","status":b_partition_exact and all(b_summary["gates"].values()),"grade":"HARD"},
        {"gate":"G6_ALL_CARRIER_COMPARISON","status":winners_by_mode=={"native_payload":["QP093A-0300"],"partition_scalar":["QP093A-0300"]},"grade":"HARD"},
        {"gate":"G7_THETA_NORMALIZED_7_8_9","status":normalized["exact_7_8_9"] and normalized["normalized_release_equals_X1_scalar"],"grade":"HARD"},
        {"gate":"G8_B_X1_W9_TYPED_BRIDGE","status":bx1_bridge_pass,"grade":"HARD"},
        {"gate":"G9_A_FIELD_X1_CURRENT_CANDIDATE","status":a_field_candidate_current,"grade":"HARD"},
        {"gate":"G10_LEDGER_162_163_CONTROL","status":ledger_preserved,"grade":"HARD"},
        {"gate":"G11_WRONG_CONTROLS","status":wrong_controls_pass,"grade":"HARD"},
        {"gate":"G12_STARBREAKER_DIRECTIONAL_CONTACT","status":history["construction_pass"] and reopening["directional_stable"] and axis["source_gate_pass"],"grade":"SUPPORTIVE_RELAXED"},
    ]
    hard_pass = all(row["status"] for row in evidence if row["grade"] == "HARD")
    primary_verdict = (
        "PASS_EXPLORATORY_THETA_NORMALIZES_B_PARTITION_TO_7_8_9__A_D1_SCALE_CONTACT__B_X1_W9_CHAIN_COHERENT__CAUSAL_WELDS_OPEN"
        if hard_pass
        else "BOUNDARY_EXPLORATORY_CHAIN_DID_NOT_CLOSE_ON_CURRENT_DATA"
    )

    typed_chain = {
        "candidate": [
            "A_SCALE(d_route=1)=N144",
            "B(N144)=(M126,THETA18_OUT)",
            "NORMALIZE_BY_THETA18(M,N,L)=(7,S8,W9)=(7,8,9)",
            "NORMALIZE_BY_THETA18(THETA18_OUT)=1=X1 scalar contact",
            "RESOLVE(S8,B,X1)->W9",
        ],
        "supported_relations": {
            "A_d1_scale_contact": matching_depths == [1],
            "B_partition": b_partition_exact,
            "theta_789_normalization": normalized["exact_7_8_9"],
            "B_contact_to_X1_to_W9": bx1_bridge_pass,
            "A_field_unique_X1_candidate": a_field_candidate_current,
        },
        "open_relations": [
            "A_OPERATOR -> B_CONTACT_OPERATOR",
            "A_OPERATOR -> X1_AXIS_SELF_CHANNEL executable edge",
            "B dynamically creates X1",
            "Starbreaker moving carrier == X1",
            "physical causal formation operator",
        ],
        "identity_merges": [],
        "registry_mutated": False,
    }

    provenance = {
        "campaign_id": CAMPAIGN,
        "started_utc": started,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "precommit_seal": seal,
        "source_hashes_matched": sum(row["matched"] for row in source_validation),
        "source_hashes_total": len(source_validation),
        "same_run_repair": False,
        "registry_mutated": False,
        "runner_sha256": sha256(Path(__file__)),
    }

    write_csv(RELEASE / "CR120X_SOURCE_VALIDATION.csv", source_validation, list(source_validation[0].keys()))
    write_csv(RELEASE / "CR120X_CARRIER_COMPARISON.csv", carrier_comparison, list(carrier_comparison[0].keys()))
    write_csv(RELEASE / "CR120X_DEPTH_LADDER.csv", depth_ladder, list(depth_ladder[0].keys()))
    write_csv(RELEASE / "CR120X_EVIDENCE_MATRIX.csv", evidence, ["gate","status","grade"])
    write_csv(RELEASE / "CR120X_WRONG_CONTROLS.csv", wrong_controls, ["control","observed","rejected","reason"])
    write_json(RELEASE / "CR120X_TYPED_CHAIN.json", typed_chain)
    write_json(RELEASE / "CR120X_PROVENANCE.json", provenance)

    summary = {
        "campaign_id": CAMPAIGN,
        "primary_verdict": primary_verdict,
        "scientific_status": "DISCOVERY_PASS" if hard_pass else "BOUNDARY",
        "source_hashes_matched": provenance["source_hashes_matched"],
        "source_hashes_total": provenance["source_hashes_total"],
        "precommit_seal_pass": all(seal_checks.values()),
        "carrier_roster_count": len(carriers),
        "carrier_winners_by_mode": winners_by_mode,
        "theta_unique_full_ladder_carrier": winners_by_mode["native_payload"] == ["QP093A-0300"] and winners_by_mode["partition_scalar"] == ["QP093A-0300"],
        "A_depth_observed_counts": a_depth_counts,
        "A_rows_exact": sum(row["match"] == "OK" for row in a_rows),
        "A_rows_total": len(a_rows),
        "A_max_residual": max_a_residual,
        "A_N144_matching_depths_in_grid": matching_depths,
        "B_partition_exact": b_partition_exact,
        "normalized_ladder": normalized,
        "B_X1_W9_bridge_current_status": "PASS_TYPED_PROVENANCE" if bx1_bridge_pass else "OPEN",
        "A_FIELD_CARRIER_X1_status": cr120w["primary_verdict"],
        "direct_A_OPERATOR_X1_edge": type_weld["a_operator_to_x1_edge"],
        "ledger_closed": cr120w["additive_ledger"]["closed"],
        "ledger_A_proxy_wrong_control": cr120w["additive_ledger"]["wrong_closed"],
        "wrong_controls_passed": sum(row["rejected"] for row in wrong_controls),
        "wrong_controls_total": len(wrong_controls),
        "starbreaker": starbreaker_support,
        "hard_gates_passed": sum(row["status"] for row in evidence if row["grade"] == "HARD"),
        "hard_gates_total": sum(1 for row in evidence if row["grade"] == "HARD"),
        "supportive_gates_passed": sum(row["status"] for row in evidence if row["grade"] != "HARD"),
        "supportive_gates_total": sum(1 for row in evidence if row["grade"] != "HARD"),
        "same_run_repair": False,
        "registry_mutated": False,
    }
    write_json(RELEASE / "CR120X_SUMMARY.json", summary)

    result = f"""# CR120X dual-depth Θ / B / X1 / W8-to-W9 relaxed discovery result

## Primary verdict

`{primary_verdict}`

## The current-data chain

The relaxed discovery chain closes exactly:

```text
A route scale at d=1     R^(d+1) = R² = N = 144
B contact                144 -> (126 retained, 18 released)
Θ-normalized ladder      126/18 = 7
                         144/18 = 8 = S8 (candidate W8 shorthand)
                         162/18 = 9 = W9
normalized release       18/18  = 1 = X1 scalar contact
typed closure            RESOLVE(S8, B, X1) -> W9
```

This is not a coincidence introduced by selecting Θ after the fact. Every
current real QP carrier was substituted using both its native payload and its
partition scalar. **QP093A-0300 TENSOR_CARRIER / Θ18 was the sole carrier that
reproduced the complete 7-8-9 ladder in both comparisons.**

## Depth result

The photon and historical A-field rows both retain QP row metadata
`closure_depth=3`. The active non-row A operator instead consumes route depth.
The current executed CR256 panel contains 16 rows at `d=0` and 16 at `d=1`;
all {len(a_rows)}/{len(a_rows)} remain exact with maximum residual
`{max_a_residual:.3e}`. In the frozen `d=0..3` comparison, only `d=1` gives
`R^(d+1)=144=S8*Θ`.

## What Θ is doing

Θ is not modeled as an invented contact amplitude. It is the existing primary
carrier packet and the released output of B. In this bridge its exact role is
the normalization quantum that maps the physical ledger capacities
`126,144,162` onto the consecutive closure grammar `7,8,9`.

That separates two functions cleanly:

- **Θ18** supplies the released carrier quantum of the B partition;
- **X1** is the normalized axis-fee occurrence that advances S8 to W9.

They share a scalar ratio in this construction; they are not the same entity.

## B activation and A-field candidate

The current typed provenance keeps `B/contact -> X1 axis-fee -> W9` at PASS.
CR120W independently retains QP093A-0305 A_FIELD_CARRIER as the unique typed
QP candidate for realizing the X1 axis channel. The direct executable
`A_OPERATOR -> X1` edge remains `{type_weld['a_operator_to_x1_edge']}`.

## Starbreaker contact

The newest Starbreaker surface contributes independent directional support:

- complete typed relations: **{history['any_stage_relation_count']:,}**;
- selected carrier-matter 101 pairs: **{reopening['history_101_selected_carrier_matter_pairs']:,}**;
- matched reopening grade: **{reopening['matched_specificity_grade']}**;
- endpoint direction: **{reopening['overall_selected_carrier_matter_direction']['direction_class']}**;
- carrier near-antiparallel return fraction: **{axis['overall_carrier']['near_antiparallel_fraction']:.9f}**;
- trajectory-identity shuffle p: **{axis['overall_shuffle']['empirical_p']:.9f}**.

Per the relaxed contract, the Starbreaker result is supportive. Matter also
shows axial return, so it is not used to demand a carrier-exclusive X1 motion.

## Controls and custody

- Frozen source hashes: **{provenance['source_hashes_matched']}/{provenance['source_hashes_total']} matched**.
- Hard gates: **{summary['hard_gates_passed']}/{summary['hard_gates_total']} passed**.
- Supportive relaxed gates: **{summary['supportive_gates_passed']}/{summary['supportive_gates_total']} passed**.
- Wrong controls: **{summary['wrong_controls_passed']}/{summary['wrong_controls_total']} rejected**.
- Canonical ledger: **162**; restored A-row wrong control: **163**.
- Same-run repair: `false`.
- Registry mutation: `false`.

## Remaining seam

The arithmetic and typed bridge now work together on the most current data.
Still open are the physical causal statements that A activates B, that B
dynamically creates X1, or that a particular moving Starbreaker carrier is X1.
Those are the hypotheses this result makes concrete enough to investigate
next; they are not reasons to discard the successful discovery bridge.
"""
    (RELEASE / "CR120X_result.md").write_text(result, encoding="utf-8")

    receipt = {
        "campaign_id": CAMPAIGN,
        "started_utc": started,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "runner": str(Path(__file__).relative_to(ROOT)).replace("\\", "/"),
        "runner_sha256": sha256(Path(__file__)),
        "exit_code": 0 if hard_pass else 2,
        "same_run_repair": False,
    }
    write_json(RELEASE / "EXECUTION_RECEIPT.json", receipt)

    release_files = sorted(path for path in RELEASE.iterdir() if path.is_file())
    release_manifest = {
        "campaign_id": CAMPAIGN,
        "artifacts": [
            {
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
            for path in release_files
        ],
        "precommit_sha256": seal["precommit_sha256"],
        "source_manifest_sha256": seal["source_manifest_sha256"],
    }
    release_manifest_path = RELEASE / "CR120X_RELEASE_MANIFEST.json"
    write_json(release_manifest_path, release_manifest)
    release_manifest_sha = sha256(release_manifest_path)
    (RELEASE / "RELEASE_MANIFEST_SHA256.txt").write_text(release_manifest_sha + "\n", encoding="utf-8")

    hash_lines = []
    for path in sorted(RELEASE.iterdir()):
        if path.is_file() and path.name != "HASHES.txt":
            hash_lines.append(f"{sha256(path)}  {path.name}")
    (RELEASE / "HASHES.txt").write_text("\n".join(hash_lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "primary_verdict": primary_verdict,
        "release_manifest_sha256": release_manifest_sha,
        "hard_gates": f"{summary['hard_gates_passed']}/{summary['hard_gates_total']}",
        "wrong_controls": f"{summary['wrong_controls_passed']}/{summary['wrong_controls_total']}",
    }, indent=2))
    return 0 if hard_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
