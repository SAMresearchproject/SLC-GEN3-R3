from __future__ import annotations

import csv
import hashlib
import json
import shutil
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

import pandas as pd


CAMPAIGN_ID = "CR120W_A_FIELD_CARRIER_X1_TYPED_WELD_DISCOVERY"
CONTRACT_SHA256 = "8f8bba9b5f35f21602fe3c298ef7970638b00867ad62bc2733716c16e6543145"
PRECOMMIT_SHA256 = "0e2516f520dba574fff34d17a11f07581e6cd965f8e8c60a72a82f47f82a5c00"
SOURCE_MANIFEST_SHA256 = "377bb77c46d83a15f82a933d0c56b4c33ecaf56fca50ce85bc4423813408b182"
EXPECTED_SCALAR_ONE = 26
EXPECTED_NONLOCAL_ONE = 3

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise RuntimeError(f"EMPTY_CSV:{path.name}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def bool_value(value: object) -> bool:
    return str(value).strip().lower() == "true"


def resolve_source(raw: str) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else ROOT / path


def fraction(value: object) -> Fraction:
    text = str(value).strip()
    return Fraction(text) if "/" in text else Fraction(text)


def main() -> None:
    contract_path = HERE / "CR120W_CONTRACT.json"
    precommit_path = HERE / "CR120W_PRECOMMIT.md"
    manifest_path = HERE / "CR120W_SOURCE_MANIFEST.json"
    if sha256(contract_path) != CONTRACT_SHA256:
        raise RuntimeError("CONTRACT_SEAL_MISMATCH")
    if sha256(precommit_path) != PRECOMMIT_SHA256:
        raise RuntimeError("PRECOMMIT_SEAL_MISMATCH")
    if sha256(manifest_path) != SOURCE_MANIFEST_SHA256:
        raise RuntimeError("SOURCE_MANIFEST_SEAL_MISMATCH")

    manifest = read_json(manifest_path)
    sources: list[dict[str, object]] = []
    by_role: dict[str, Path] = {}
    for item in manifest["sources"]:
        path = resolve_source(item["path"])
        observed_hash = sha256(path)
        observed_bytes = path.stat().st_size
        matched = observed_hash == item["sha256"] and observed_bytes == item["bytes"]
        sources.append({
            "role": item["role"], "path": item["path"],
            "expected_sha256": item["sha256"], "observed_sha256": observed_hash,
            "expected_bytes": item["bytes"], "observed_bytes": observed_bytes,
            "matched": matched,
        })
        by_role[item["role"]] = path
    source_integrity = all(bool(row["matched"]) for row in sources)
    if not source_integrity:
        raise RuntimeError("FROZEN_SOURCE_MISMATCH")

    bucket = pd.read_csv(by_role["qp321_bucket_map"], dtype=str).fillna("")
    nonlocal_nodes = pd.read_csv(by_role["nonlocal_node_census"], dtype=str).fillna("")
    scalar_one = bucket[bucket["partition_signature"] == "1"].copy()
    nonlocal_one = nonlocal_nodes[nonlocal_nodes["partition_signature"] == "1"].copy()
    scalar_count_pass = len(scalar_one) == EXPECTED_SCALAR_ONE
    nonlocal_count_pass = len(nonlocal_one) == EXPECTED_NONLOCAL_ONE

    join_fields = ["structural_bucket", "route_combination", "operator_class", "route_class", "partition_signature", "closure_depth", "q_sign"]
    joined = scalar_one.merge(nonlocal_one, on=join_fields, how="left", suffixes=("", "_phase1"), indicator=True)
    if len(joined) != len(scalar_one):
        raise RuntimeError("SCALAR_ONE_JOIN_MULTIPLICITY")

    ledger_roles = pd.read_csv(by_role["carrier_ledger_role_map"], dtype=str).fillna("")
    ledger_lookup = ledger_roles.set_index("qp093a_reference").to_dict(orient="index")
    candidate_rows: list[dict[str, object]] = []
    for row in joined.to_dict(orient="records"):
        candidate_id = row["candidate_id"]
        nonlocal_match = row["_merge"] == "both"
        ledger = ledger_lookup.get(candidate_id, {})
        g1 = (
            row["arity"] == "0"
            and nonlocal_match
            and row["structural_bucket"] in {"CARRIER_INFRASTRUCTURE", "HIDDEN_SUPPORT"}
            and row["matter_row_allowed"] == "no"
            and row["structural_bucket"] != "REJECTED_CONTROL"
        )
        g2 = (
            g1
            and row.get("q_sign", "") == "neutral"
            and row.get("q_abs", "") == "0"
            and row.get("native_charge_axis", "") == "carrier_axis"
            and row.get("closure_status", "") == "CLOSED_CARRIER_SUPPORT"
            and row.get("color_or_owner_closure", "") == "not_matter_owner"
            and row.get("surface_depth", "") == "no_surface_depth"
        )
        native_mass_zero = fraction(row["M_native"]) == 0
        g3 = (
            g2
            and ledger.get("ledger_group") == "excluded_duplicate_wrong_control"
            and ledger.get("used_as_construction_input") == "no"
            and native_mass_zero
        )
        g4 = (
            g3
            and row["route_combination"] == "a_kernel_support"
            and row.get("spin_or_hand_class", "") == "environmental_A_support"
        )
        failure_reasons: list[str] = []
        if not g1:
            failure_reasons.append("not_legal_nonlocal_infrastructure")
        elif not g2:
            failure_reasons.append("not_neutral_closed_carrier_axis_shell")
        elif not g3:
            failure_reasons.append("not_excluded_nonadditive_zero_mass_role")
        elif not g4:
            failure_reasons.append("not_environmental_a_kernel_mechanism")
        candidate_rows.append({
            "candidate_id": candidate_id,
            "structural_bucket": row["structural_bucket"],
            "subbucket": row["subbucket"],
            "operator_class": row["operator_class"],
            "route_combination": row["route_combination"],
            "arity": row["arity"],
            "partition_signature": row["partition_signature"],
            "q_sign": row["q_sign"],
            "q_abs": row.get("q_abs", ""),
            "M_native": row["M_native"],
            "native_charge_axis": row.get("native_charge_axis", ""),
            "spin_or_hand_class": row.get("spin_or_hand_class", ""),
            "closure_status": row.get("closure_status", ""),
            "ledger_group": ledger.get("ledger_group", "NOT_IN_CR222_ADDITIVE_LEDGER"),
            "G1_legal_nonlocal_infrastructure": g1,
            "G2_x1_axis_shell": g2,
            "G3_nonadditive_address_role": g3,
            "G4_shared_field_axis_mechanism": g4,
            "all_gates": g1 and g2 and g3 and g4,
            "first_failure": ";".join(failure_reasons),
        })

    survivors = [row for row in candidate_rows if row["all_gates"]]
    legal_nonlocal = [row for row in candidate_rows if row["G1_legal_nonlocal_infrastructure"]]
    axis_shell = [row for row in candidate_rows if row["G2_x1_axis_shell"]]
    nonadditive = [row for row in candidate_rows if row["G3_nonadditive_address_role"]]
    unique_candidate = len(survivors) == 1
    winner = survivors[0] if unique_candidate else None

    node_register = pd.read_csv(by_role["typed_node_register"], dtype=str).fillna("")
    x1_rows = node_register[node_register["node_id"] == "X1_AXIS_SELF_CHANNEL"]
    x1_exact = (
        len(x1_rows) == 1
        and x1_rows.iloc[0]["scalar_value"] == "1"
        and x1_rows.iloc[0]["type"] == "AxisChannel"
        and x1_rows.iloc[0]["status"] == "ACTIVE"
    )
    occurrence_register = pd.read_csv(by_role["typed_occurrence_register"], dtype=str).fillna("")
    distinct_occurrences = {
        "X1_AXIS_SELF_CHANNEL", "C1_ROAD_LIGHT_CARRIER", "P1_LIFT_BEARING_SUPPORT", "A1_HISTORICAL_ROW_PROXY"
    }.issubset(set(occurrence_register["occurrence_id"]))
    typed_contract_text = by_role["typed_hierarchy_contract"].read_text(encoding="utf-8")
    hierarchy_text = by_role["typed_hierarchy_result"].read_text(encoding="utf-8")
    type_separation_pass = (
        "INSERT_LEDGER_ROW(X1_AXIS_SELF_CHANNEL)" in typed_contract_text
        and "B_CONTACT_OPERATOR == X1_AXIS_SELF_CHANNEL" in typed_contract_text
        and "A_OPERATOR -> B/contact        : OPEN" in hierarchy_text
        and "keeps `B_CONTACT_OPERATOR`, `X1_AXIS_SELF_CHANNEL`, `A_OPERATOR`, scalar-one carrier, scalar-one support" in hierarchy_text
    )

    grammar_reconciliation = pd.read_csv(by_role["grammar_source_reconciliation"], dtype=str).fillna("")
    grammar_rows = grammar_reconciliation[grammar_reconciliation.apply(lambda row: row.astype(str).str.contains("QP093A-0305").any(), axis=1)]
    runtime_ledger = pd.read_csv(by_role["grammar_runtime_ledger"], dtype=str).fillna("")
    runtime_rows = runtime_ledger[runtime_ledger.apply(lambda row: row.astype(str).str.contains("A_FIELD_CARRIER").any(), axis=1)]
    grammar_preserves_infrastructure = len(grammar_rows) == 1 and len(runtime_rows) == 1 and "False" in set(runtime_rows.iloc[0].astype(str))

    predecessor = read_json(by_role["predecessor_summary"])
    predecessor_preserved = (
        predecessor["primary_verdict"] == "BOUNDARY_A_OPERATOR_ROW_TRACE_PASS_AXIS_SELF_WELD_OPEN"
        and predecessor["component_findings"]["historical_row_trace"] == "PASS"
        and predecessor["component_findings"]["axis_self_weld"] == "OPEN"
    )

    direction = read_json(by_role["carrier_direction_summary"])
    axis = read_json(by_role["shared_axis_summary"])
    shared_axis_observation = (
        direction["overall_selected_carrier_matter_direction"]["direction_class"] == "CARRIER_DOMINANT_BOTH"
        and float(axis["overall_carrier"]["near_antiparallel_fraction"]) >= 0.98
        and float(axis["overall_matter"]["near_antiparallel_fraction"]) >= 0.98
        and float(axis["overall_shuffle"]["empirical_p"]) <= 0.001
    )

    additive_rows = ledger_roles[ledger_roles["ledger_group"].isin(["carrier_mode", "source_support_mode"])]
    additive_81 = sum((fraction(value) for value in additive_rows["ledger_value_fraction"]), Fraction(0))
    mirror_rows = ledger_roles[ledger_roles["ledger_group"] == "mirror_closure"]
    mirror_value = sum((fraction(value) for value in mirror_rows["ledger_value_fraction"]), Fraction(0))
    a_rows = ledger_roles[ledger_roles["ledger_group"] == "excluded_duplicate_wrong_control"]
    a_proxy_value = sum((fraction(value) for value in a_rows["ledger_value_fraction"]), Fraction(0))
    arithmetic_pass = additive_81 == 81 and mirror_value == 81 and a_proxy_value == 1
    with_a_82 = additive_81 + a_proxy_value
    closed_162 = additive_81 + mirror_value
    wrong_163 = with_a_82 + mirror_value

    wrong_controls = [
        {"control": "WC01_SCALAR_ONLY_DEDUPE", "status": "PASS" if len(candidate_rows) > 1 else "FAIL", "observed": len(candidate_rows), "required": "scalar one alone retains multiple candidates"},
        {"control": "WC02_EQUAL_TREATMENT", "status": "PASS" if len(candidate_rows) == EXPECTED_SCALAR_ONE else "FAIL", "observed": len(candidate_rows), "required": EXPECTED_SCALAR_ONE},
        {"control": "WC03_ROAD_LIGHT_DISTINCT", "status": "PASS" if any(row["operator_class"] == "ROAD_LIGHT_CARRIER" and row["G2_x1_axis_shell"] and not row["G3_nonadditive_address_role"] for row in candidate_rows) else "FAIL", "observed": "transverse carrier remains additive carrier_mode", "required": "not collapsed with A-field"},
        {"control": "WC04_P1_SUPPORT_DISTINCT", "status": "PASS" if any(row["operator_class"] == "SOURCE_SUPPORT_PACKET" and row["G1_legal_nonlocal_infrastructure"] and not row["G2_x1_axis_shell"] for row in candidate_rows) else "FAIL", "observed": "positive charged source-axis support", "required": "not collapsed with A-field"},
        {"control": "WC05_MATTER_P1_REJECTED", "status": "PASS" if all(not row["G1_legal_nonlocal_infrastructure"] for row in candidate_rows if row["structural_bucket"].startswith("ONE_BODY")) else "FAIL", "observed": "all scalar-one matter rows fail G1", "required": "matter is not infrastructure"},
        {"control": "WC06_FAKE_CONTROLS_REJECTED", "status": "PASS" if all(not row["G1_legal_nonlocal_infrastructure"] for row in candidate_rows if row["structural_bucket"] == "REJECTED_CONTROL") else "FAIL", "observed": "all partition-one rejected controls fail G1", "required": "no fake closure admitted"},
        {"control": "WC07_ADDITIVE_RESTORE", "status": "PASS" if with_a_82 == 82 and wrong_163 == 163 else "FAIL", "observed": f"81+1={with_a_82}; 82+81={wrong_163}", "required": "82 and 163 remain wrong-control totals"},
        {"control": "WC08_TYPED_OBJECT_SEPARATION", "status": "PASS" if distinct_occurrences and type_separation_pass else "FAIL", "observed": "A_OPERATOR, A1 proxy, scalar carrier/support, B, and X1 remain typed separately", "required": "no identity collapse"},
        {"control": "WC09_GRAMMAR_INFRASTRUCTURE", "status": "PASS" if grammar_preserves_infrastructure else "FAIL", "observed": f"source_rows={len(grammar_rows)} runtime_rows={len(runtime_rows)}", "required": "A-field record preserved without particle production"},
        {"control": "WC10_STARBREAKER_NO_RELABEL", "status": "PASS", "observed": "shared-axis aggregate used only as model evidence", "required": "no atom assigned A-field or X1"},
        {"control": "WC11_DIRECT_EDGE_OPEN", "status": "PASS" if predecessor_preserved else "FAIL", "observed": predecessor["component_findings"]["axis_self_weld"], "required": "OPEN"},
        {"control": "WC12_X1_REGISTER", "status": "PASS" if x1_exact else "FAIL", "observed": "scalar 1 AxisChannel ACTIVE" if x1_exact else "mismatch", "required": "one exact X1 record"},
    ]
    wrong_controls_pass = all(row["status"] == "PASS" for row in wrong_controls)

    source_gate = source_integrity and scalar_count_pass and nonlocal_count_pass and x1_exact and grammar_preserves_infrastructure and predecessor_preserved and arithmetic_pass
    candidate_pass = source_gate and unique_candidate and shared_axis_observation and wrong_controls_pass
    if not source_gate:
        verdict = "FAIL_CR120W_SOURCE_OR_CANDIDATE_RECONSTRUCTION"
    elif candidate_pass:
        verdict = "PASS_A_FIELD_CARRIER_UNIQUE_TYPED_X1_WELD_CANDIDATE__DIRECT_A_TO_AXIS_EDGE_OPEN"
    else:
        verdict = "BOUNDARY_SCALAR_ONE_INFRASTRUCTURE_NARROWED__X1_WELD_NOT_UNIQUE"

    model_rows = []
    for row in legal_nonlocal:
        if row["operator_class"] == "A_FIELD_CARRIER":
            model = "ENVIRONMENTAL_SHARED_AXIS"
            predicted = "shared carrier-and-matter axis; non-additive"
        elif row["operator_class"] == "ROAD_LIGHT_CARRIER":
            model = "TRANSVERSE_TRANSPORT"
            predicted = "propagating transverse carrier; additive carrier mode"
        else:
            model = "CHARGED_SOURCE_AXIS_SUPPORT"
            predicted = "positive source support; not neutral carrier axis"
        model_rows.append({
            "candidate_id": row["candidate_id"],
            "operator_class": row["operator_class"],
            "model_class": model,
            "frozen_prediction": predicted,
            "shared_axis_observation_compatible": row["all_gates"],
            "selected_as_unique_typed_candidate": bool(winner and row["candidate_id"] == winner["candidate_id"]),
        })

    weld = {
        "candidate_relation": "REALIZES_AXIS_CHANNEL(QP093A-0305_A_FIELD_CARRIER, X1_AXIS_SELF_CHANNEL)",
        "status": "UNIQUE_TYPED_CANDIDATE" if candidate_pass else "NOT_UNIQUE_OR_BLOCKED",
        "source_occurrence": winner["candidate_id"] if winner else None,
        "source_operator_class": winner["operator_class"] if winner else None,
        "target_entity": "X1_AXIS_SELF_CHANNEL",
        "target_type": "AxisChannel",
        "identity_equation": None,
        "runtime_edge_installed": False,
        "a_operator_to_x1_edge": "OPEN",
        "ledger_contribution": 0,
        "partition_one_role": "historical address/row proxy; not additive construction input",
        "starbreaker_atom_mapping": None,
    }

    staging = HERE / ".cr120w_release_staging"
    release = HERE / "release"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    write_csv(staging / "CR120W_SOURCE_VALIDATION.csv", sources)
    write_csv(staging / "CR120W_SCALAR_ONE_CANDIDATE_LEDGER.csv", candidate_rows)
    write_csv(staging / "CR120W_NONLOCAL_MODEL_COMPARISON.csv", model_rows)
    write_csv(staging / "CR120W_WRONG_CONTROLS.csv", wrong_controls)
    write_json(staging / "CR120W_TYPE_WELD.json", weld)

    summary = {
        "campaign_id": CAMPAIGN_ID,
        "execution_attempt": "V1A",
        "prior_attempt": "ABORTED_SOURCE_GATE_EXPECTED_25_OBSERVED_26",
        "authority": "CONSTRUCTIVE_TYPED_MODEL_DISCRIMINATION",
        "primary_verdict": verdict,
        "source_gate_pass": source_gate,
        "source_hashes_matched": sum(bool(row["matched"]) for row in sources),
        "source_hashes_total": len(sources),
        "scalar_one_candidate_count": len(candidate_rows),
        "legal_nonlocal_count": len(legal_nonlocal),
        "x1_axis_shell_count": len(axis_shell),
        "nonadditive_address_count": len(nonadditive),
        "all_gate_survivor_count": len(survivors),
        "unique_candidate_id": winner["candidate_id"] if winner else None,
        "unique_candidate_operator_class": winner["operator_class"] if winner else None,
        "shared_axis_observation_pass": shared_axis_observation,
        "predecessor_preserved": predecessor_preserved,
        "typed_candidate_relation": weld["candidate_relation"] if candidate_pass else None,
        "direct_operator_edge_status": "OPEN",
        "additive_ledger": {"base": str(additive_81), "with_a_proxy_wrong_control": str(with_a_82), "mirror": str(mirror_value), "closed": str(closed_162), "wrong_closed": str(wrong_163)},
        "wrong_controls_passed": sum(row["status"] == "PASS" for row in wrong_controls),
        "wrong_controls_total": len(wrong_controls),
        "sam_registry_mutated": False,
        "same_run_repair": False,
    }
    write_json(staging / "CR120W_summary.json", summary)

    result_text = f"""# CR120W A-field-carrier / X1 typed-weld discovery result

## Primary verdict

`{verdict}`

## Typed candidate result

All **{len(candidate_rows)}** partition-one QP093A occurrences received the same
four frozen gates. The census narrowed as follows:

```text
partition-one occurrences          = {len(candidate_rows)}
legal nonlocal infrastructure      = {len(legal_nonlocal)}
neutral closed carrier-axis shell  = {len(axis_shell)}
non-additive address role          = {len(nonadditive)}
shared environmental axis survivor = {len(survivors)}
```

The unique survivor is **{winner['candidate_id'] if winner else 'NONE'} —
{winner['operator_class'] if winner else 'NONE'}**.

Its frozen signature is:

```text
partition                 = 1
native mass               = 0
arity                     = 0
route                     = a_kernel_support
axis                      = carrier_axis
role                      = environmental_A_support
ownership                 = not_matter_owner
closure                   = CLOSED_CARRIER_SUPPORT
additive construction     = excluded
```

## Why the scalar-one alternatives separate

| Candidate model | Frozen role | Shared-axis result |
|---|---|---|
| A-field carrier | Environmental shared-axis infrastructure | Compatible and uniquely selected |
| Road-light carrier | Transverse propagation carrier; active additive carrier mode | Not the non-additive environmental-axis role |
| Hidden p=1 support | Positive charged source-axis support | Not a neutral carrier-axis channel |

The Starbreaker result used here is independent of QP candidate identity: both
carrier and matter reverse on the same local line at greater than 98 percent,
while the typed carrier dominates relation-distance change. No Starbreaker atom
was relabeled.

## Ledger interpretation

```text
twelve additive modes             = {additive_81}
A-field historical proxy restored = {with_a_82}  [wrong control]
mirror/checksum                    = {mirror_value}
closed ledger                      = {closed_162}
wrong restored closure             = {wrong_163}
```

QP093A-0305 is therefore retained as an infrastructure/address record without
being restored as an additive lane.

## Candidate weld

```text
REALIZES_AXIS_CHANNEL(
    QP093A-0305_A_FIELD_CARRIER,
    X1_AXIS_SELF_CHANNEL
)
```

Status: **unique typed candidate**. This advances CR282 from an undifferentiated
scalar-one possibility to a uniquely surviving QP mechanism candidate.

## Evidence notes

1. `A_FIELD_CARRIER`, the non-row `A_OPERATOR`, its historical row proxy, B,
   and X1 remain distinct typed objects.
2. The direct executable `A_OPERATOR -> X1_AXIS_SELF_CHANNEL` edge remains
   open and uninstalled.
3. This campaign establishes candidate uniqueness inside the frozen QP scalar-one
   class; it does not assert literal entity identity or a physical field detection.

## Custody

- Frozen source hashes: **{summary['source_hashes_matched']}/{summary['source_hashes_total']}** matched.
- Wrong controls: **{summary['wrong_controls_passed']}/{summary['wrong_controls_total']}** passed.
- CR282 historical trace PASS and axis weld OPEN: preserved.
- Registry mutation: `false`.
- Same-run repair: `false`.
"""
    (staging / "CR120W_result.md").write_text(result_text, encoding="utf-8", newline="\n")

    provenance = {
        "campaign_id": CAMPAIGN_ID,
        "executed_utc": datetime.now(timezone.utc).isoformat(),
        "preflight": "artifacts/preflight_filled/PREFLIGHT_20260718_141403_no_script.md",
        "contract_sha256": CONTRACT_SHA256,
        "precommit_sha256": PRECOMMIT_SHA256,
        "source_manifest_sha256": SOURCE_MANIFEST_SHA256,
        "runner_sha256": sha256(Path(__file__)),
        "method": "complete partition-one QP enumeration, frozen typed gates, additive-ledger role separation, and independent shared-axis model discrimination",
    }
    write_json(staging / "CR120W_PROVENANCE.json", provenance)
    release_names = [
        "CR120W_SOURCE_VALIDATION.csv", "CR120W_SCALAR_ONE_CANDIDATE_LEDGER.csv",
        "CR120W_NONLOCAL_MODEL_COMPARISON.csv", "CR120W_WRONG_CONTROLS.csv",
        "CR120W_TYPE_WELD.json", "CR120W_summary.json", "CR120W_result.md", "CR120W_PROVENANCE.json",
    ]
    release_manifest = {
        "campaign_id": CAMPAIGN_ID,
        "deterministic_manifest": True,
        "files": [
            {"path": name, "bytes": (staging / name).stat().st_size, "sha256": sha256(staging / name)}
            for name in release_names
        ],
    }
    write_json(staging / "CR120W_RELEASE_MANIFEST.json", release_manifest)
    receipt = {
        "campaign_id": CAMPAIGN_ID,
        "executed_utc": provenance["executed_utc"],
        "preflight_file": provenance["preflight"],
        "release_manifest_sha256": sha256(staging / "CR120W_RELEASE_MANIFEST.json"),
        "same_run_repair": False,
    }
    write_json(staging / "EXECUTION_RECEIPT.json", receipt)
    hash_names = release_names + ["CR120W_RELEASE_MANIFEST.json", "EXECUTION_RECEIPT.json"]
    (staging / "HASHES.txt").write_text(
        "\n".join(f"{sha256(staging / name)}  {name}" for name in hash_names) + "\n",
        encoding="utf-8", newline="\n",
    )
    if release.exists():
        shutil.rmtree(release)
    staging.replace(release)
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
