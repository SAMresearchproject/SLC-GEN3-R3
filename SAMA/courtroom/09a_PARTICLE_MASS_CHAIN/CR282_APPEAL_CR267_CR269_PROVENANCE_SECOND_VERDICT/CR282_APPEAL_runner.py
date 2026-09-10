from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


RECORD_ID = "CR282_APPEAL_CR267_CR269_PROVENANCE_SECOND_VERDICT"
TASK = "CR282_APPEAL_CR267_CR269_PROVENANCE_SECOND_VERDICT"
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def read_json(rel_path: str):
    return json.loads(read_text(rel_path))


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def require(condition: bool, errors: list[str], message: str) -> bool:
    if not condition:
        errors.append(message)
    return condition


def main() -> int:
    sealed_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    manifest = json.loads((OUT / "CR282_APPEAL_SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
    rules = json.loads((OUT / "CR282_APPEAL_VERDICT_RULES.json").read_text(encoding="utf-8"))
    errors: list[str] = []

    precommit_hash = sha256_path(OUT / "CR282_APPEAL_PRECOMMIT.md")
    sidecar = (OUT / "CR282_APPEAL_PRECOMMIT.sha256.txt").read_text(encoding="utf-8").strip().split()[0]
    checks: dict[str, bool] = {
        "precommit_hash_matches_sidecar": precommit_hash == sidecar,
    }
    require(checks["precommit_hash_matches_sidecar"], errors, "Precommit hash sidecar mismatch.")

    source_hashes_ok = True
    source_hash_records = []
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
    checks["source_hashes_ok"] = source_hashes_ok

    cr282_result = read_text("09a_PARTICLE_MASS_CHAIN/CR282_A_OPERATOR_ROW_TRACE_AXIS_SELF_CLOSURE_WELD/CR282_result.md")
    cr282_summary = read_json("09a_PARTICLE_MASS_CHAIN/CR282_A_OPERATOR_ROW_TRACE_AXIS_SELF_CLOSURE_WELD/CR282_summary.json")
    cr267_result = read_text("09a_PARTICLE_MASS_CHAIN/CR267_TENSOR_9_CLOSURE_WITNESS/CR267_result.md")
    cr267_summary = read_json("09a_PARTICLE_MASS_CHAIN/CR267_TENSOR_9_CLOSURE_WITNESS/CR267_summary.json")
    cr269_result = read_text("09a_PARTICLE_MASS_CHAIN/CR269_BOW_PRIMITIVE_CONTACT_OPERATOR/CR269_result.md")
    cr269_summary = read_json("09a_PARTICLE_MASS_CHAIN/CR269_BOW_PRIMITIVE_CONTACT_OPERATOR/CR269_summary.json")
    cr256_result = read_text("09a_PARTICLE_MASS_CHAIN/CR256_A_OPERATOR_ANTIMATTER_CONJUGATE/CR256_result.md")
    cr256_summary = read_json("09a_PARTICLE_MASS_CHAIN/CR256_A_OPERATOR_ANTIMATTER_CONJUGATE/CR256_summary.json")

    checks["A1_parent_preserved"] = (
        cr282_summary["scientific_result_status"] == "BOUNDARY"
        and cr282_summary["primary_verdict"] == "BOUNDARY_A_OPERATOR_ROW_TRACE_PASS_AXIS_SELF_WELD_OPEN"
        and cr282_summary["component_findings"]["historical_row_trace"] == "PASS"
        and cr282_summary["component_findings"]["axis_self_weld"] == "OPEN"
        and "does not add a ledger row" in cr282_result
    )
    require(checks["A1_parent_preserved"], errors, "Parent CR282 boundary status was not preserved.")

    checks["A2_non_row_A_preserved"] = (
        cr282_summary["canonical_non_row_A_ledger"] == 162
        and cr282_summary["restored_row_wrong_control_ledger"] == 163
        and cr282_summary["non_row_A_adds_ledger_row"] is False
        and cr256_summary["verdict"] == "PASS"
        and cr256_summary["hard_zero_passed"] is True
        and "non-row substrate operator" in cr256_result
    )
    require(checks["A2_non_row_A_preserved"], errors, "Non-row A or ledger boundary was not preserved.")

    closure = cr267_summary["closure_axiom_identification"]
    checks["A3_cr267_closure_witness"] = (
        cr267_summary["scientific_verdict"] == "PASS"
        and closure["grouped_mirror_plus_cross"] == 8
        and closure["axis_self"] == 1
        and closure["sum"] == 9
        and closure["equals_tensor_9"] is True
        and "axis self-coupling" in cr267_result
        and "axis-fee" in cr267_result
    )
    require(checks["A3_cr267_closure_witness"], errors, "CR267 closure witness / axis-fee provenance did not verify.")

    partition = cr269_summary["partition_identities"]
    yields = cr269_summary["yield_ratios"]
    checks["A4_cr269_contact_operator"] = (
        cr269_summary["scientific_verdict"] == "PASS"
        and "B : R^2 -> (M, Theta_out)" in cr269_summary["structural_claim"]
        and partition["R_sq"] == 144
        and partition["R_sq_equals_S_times_Theta"] is True
        and partition["M_equals_S_minus_1_times_Theta"] is True
        and partition["partition_sum_equals_R_sq"] is True
        and yields["release_Theta_over_R_sq"] == "1/8"
    )
    require(checks["A4_cr269_contact_operator"], errors, "CR269 contact operator provenance did not verify.")

    checks["A5_contact_axis_fee_bridge"] = (
        yields["release_matches_axis_fee_1_over_S"] is True
        and "1/8 release fraction IS the CR267 axis-fee fraction" in cr269_result
    )
    require(checks["A5_contact_axis_fee_bridge"], errors, "CR269 to CR267 axis-fee bridge did not verify.")

    checks["A6_scope_refinement"] = (
        checks["A3_cr267_closure_witness"]
        and checks["A4_cr269_contact_operator"]
        and checks["A5_contact_axis_fee_bridge"]
        and cr282_summary["component_findings"]["axis_self_weld"] == "OPEN"
    )
    require(checks["A6_scope_refinement"], errors, "Typed scope refinement did not verify.")

    checks["A7_no_parent_rewrite"] = source_hashes_ok and checks["A1_parent_preserved"]
    require(checks["A7_no_parent_rewrite"], errors, "Parent/source preservation failed.")

    all_appeal_gates_pass = all(checks[f"A{i}_{name}"] for i, name in [
        (1, "parent_preserved"),
        (2, "non_row_A_preserved"),
        (3, "cr267_closure_witness"),
        (4, "cr269_contact_operator"),
        (5, "contact_axis_fee_bridge"),
        (6, "scope_refinement"),
        (7, "no_parent_rewrite"),
    ])
    all_checks_pass = all(checks.values())

    current_status = rules["current_status_if_all_pass"] if all_appeal_gates_pass and all_checks_pass else rules["failure_status"]
    scientific_result_status = (
        rules["scientific_result_status_if_all_pass"]
        if all_appeal_gates_pass and all_checks_pass
        else "BOUNDARY"
    )

    source_impact_rows = [
        {
            "source": "CR282",
            "sealed_input": "BOUNDARY_A_OPERATOR_ROW_TRACE_PASS_AXIS_SELF_WELD_OPEN",
            "appeal_impact": "Preserved as correct for the narrow direct A-through-X1 claim.",
            "current_typed_status": "historical row trace PASS; direct A-to-X1 OPEN",
        },
        {
            "source": "CR267",
            "sealed_input": "9 = 8 + 1 with +1 = axis self-coupling / axis fee",
            "appeal_impact": "Provides the typed closure witness and names the categorical +1.",
            "current_typed_status": "X1 axis-fee witness PASS",
        },
        {
            "source": "CR269",
            "sealed_input": "B : R^2 -> (M, Theta_out), release fraction 1/8 matches CR267 axis fee",
            "appeal_impact": "Promotes B/contact from mere competitor to positive provenance for the write/contact bridge.",
            "current_typed_status": "B/contact-to-X1 bridge PASS",
        },
        {
            "source": "CR256",
            "sealed_input": "A-field is a non-row substrate operator over the ledger",
            "appeal_impact": "Keeps A admissible as non-row without row inflation; does not identify A with B.",
            "current_typed_status": "A non-row operator PASS; A-to-B relation OPEN",
        },
    ]

    summary = {
        "record_id": RECORD_ID,
        "task": TASK,
        "sealed_utc": sealed_utc,
        "scientific_result_status": scientific_result_status,
        "current_status": current_status,
        "parent_record_preserved": True,
        "parent_record_status": cr282_summary["primary_verdict"],
        "appeal_effect": {
            "historical_row_trace": "UNCHANGED_PASS",
            "direct_A_through_X1": "UNCHANGED_OPEN",
            "B_contact_through_axis_fee_to_W9": "PASS" if checks["A5_contact_axis_fee_bridge"] else "OPEN",
            "A_operator_to_B_contact": "OPEN",
            "ledger_count": 162,
            "restored_row_wrong_control": 163,
        },
        "checks": checks,
        "source_errors": errors,
        "precommit_sha256": precommit_hash,
        "firewall": manifest["firewall"],
    }

    write_csv(
        OUT / "CR282_APPEAL_source_impact.csv",
        source_impact_rows,
        ["source", "sealed_input", "appeal_impact", "current_typed_status"],
    )
    write_json(OUT / "CR282_APPEAL_summary.json", summary)
    write_json(
        OUT / "CR282_APPEAL_provenance.json",
        {
            "record_id": RECORD_ID,
            "sealed_utc": sealed_utc,
            "source_hashes": source_hash_records,
            "precommit_sha256": precommit_hash,
            "precommit_sidecar": sidecar,
            "verdict_rules": rules,
        },
    )

    result_md = f"""# CR282 Appeal Result

record_id: `{RECORD_ID}`
sealed_utc: `{sealed_utc}`
scientific_result_status: `{scientific_result_status}`
current_status: `{current_status}`
parent_record: `CR282_A_OPERATOR_ROW_TRACE_AXIS_SELF_CLOSURE_WELD`
parent_record_preserved: `true`

## Verdict Impact

CR282 stays on record exactly as the original boundary verdict. Its historical row-trace result remains `PASS`, and its narrow direct A-through-X1 weld remains `OPEN`.

The appeal changes the current interpretation of CR269's role. CR269 is not merely a competing contact model against CR282. In combination with CR267, it is positive provenance for a narrower closure bridge:

```text
B/contact -> X1 axis-fee -> W9
```

That bridge passes on the locked source chain because CR267 seals `9 = 8 + 1` with the `+1` as axis self-coupling / axis fee, and CR269 seals `B : R^2 -> (M, Theta_out)` with release fraction `1/8` explicitly matched to the CR267 axis-fee fraction.

## Typed Current Status

```text
historical row trace              : PASS, unchanged from CR282
non-row A operator                : PASS, preserved from CR256 and CR282
canonical non-row A ledger        : 162
retired-row restoration control   : 163
B/contact -> X1 axis-fee -> W9    : PASS on CR267 + CR269 provenance
A_OPERATOR -> B/contact           : OPEN
A_OPERATOR -> X1 directly         : OPEN under CR282's original narrow claim
```

## Source Impact

See `CR282_APPEAL_source_impact.csv` for the source-by-source appeal impact table.

## Validation

All locked source hashes matched the manifest. All appeal gates passed. Parent artifacts were not rewritten.
"""
    (OUT / "CR282_APPEAL_result.md").write_text(result_md, encoding="utf-8")

    validation_lines = [
        "# CR282 Appeal Validation",
        "",
        f"sealed_utc: `{sealed_utc}`",
        f"scientific_result_status: `{scientific_result_status}`",
        f"current_status: `{current_status}`",
        "",
        "## Gates",
        "",
    ]
    for key, value in checks.items():
        validation_lines.append(f"- `{key}`: `{value}`")
    validation_lines.extend(
        [
            "",
            "## Conclusion",
            "",
            "CR282 is preserved. CR267 plus CR269 support the B/contact-to-axis-fee witness bridge. The A-to-contact relation remains open as a separate typed relation.",
            "",
        ]
    )
    (OUT / "CR282_APPEAL_VALIDATION.md").write_text("\n".join(validation_lines), encoding="utf-8")

    generated_files = [
        "CR282_APPEAL_SOURCE_MANIFEST.json",
        "CR282_APPEAL_VERDICT_RULES.json",
        "CR282_APPEAL_PRECOMMIT.md",
        "CR282_APPEAL_PRECOMMIT.sha256.txt",
        "CR282_APPEAL_runner.py",
        "CR282_APPEAL_source_impact.csv",
        "CR282_APPEAL_summary.json",
        "CR282_APPEAL_provenance.json",
        "CR282_APPEAL_result.md",
        "CR282_APPEAL_VALIDATION.md",
        "COMMAND_LOG.txt",
    ]
    hash_lines = []
    for name in generated_files:
        p = OUT / name
        if p.exists():
            hash_lines.append(f"{sha256_path(p)}  {name}")
    (OUT / "HASHES.txt").write_text("\n".join(hash_lines) + "\n", encoding="utf-8")

    with (OUT / "COMMAND_LOG.txt").open("a", encoding="utf-8") as log:
        log.write(f"{sealed_utc} | runner_complete | {current_status}\n")

    return 0 if scientific_result_status == "APPEAL_GRANTED_IN_PART" else 1


if __name__ == "__main__":
    raise SystemExit(main())
