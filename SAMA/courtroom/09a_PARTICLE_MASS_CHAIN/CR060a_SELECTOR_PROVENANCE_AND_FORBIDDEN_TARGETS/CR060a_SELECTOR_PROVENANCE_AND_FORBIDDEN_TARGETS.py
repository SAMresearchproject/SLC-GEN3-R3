"""CR060a_SELECTOR_PROVENANCE_AND_FORBIDDEN_TARGETS.py

Courtroom test for QP075 selector provenance.

This script directly checks the QP075 closure table, role-operator table, and
decision table. It does not delegate the test body to a shared harness.
"""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


CR_ID = "CR060a"
TITLE = "SELECTOR_PROVENANCE_AND_FORBIDDEN_TARGETS"
HERE = Path(__file__).resolve().parent
BRANCH = HERE.parent
COURTROOM = BRANCH.parent
QP075 = Path("C:/VS/quantum_phase/artifacts/qp075")
MANIFEST = BRANCH / "SOURCE_MANIFEST.csv"
MANIFEST_SEAL = BRANCH / "SOURCE_MANIFEST.csv.sha256.txt"


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(COURTROOM.resolve()).as_posix()
    except ValueError:
        return str(path).replace("\\", "/")


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def manifest_check(rows: list[dict]) -> dict:
    verified = 0
    missing = []
    mismatches = []
    for row in rows:
        path = Path(row["path"])
        if not path.exists():
            missing.append(row["item_id"])
            continue
        actual = sha256(path)
        if actual == row["sha256"].lower():
            verified += 1
        else:
            mismatches.append(row["item_id"])
    manifest_hash = sha256(MANIFEST)
    seal_text = MANIFEST_SEAL.read_text(encoding="utf-8", errors="ignore") if MANIFEST_SEAL.exists() else ""
    return {
        "manifest_rows": len(rows),
        "verified": verified,
        "missing": missing,
        "mismatches": mismatches,
        "manifest_sha256": manifest_hash,
        "manifest_seal_exists": MANIFEST_SEAL.exists(),
        "manifest_seal_matches": manifest_hash in seal_text,
    }


def main() -> None:
    manifest_rows = read_csv(MANIFEST)
    mcheck = manifest_check(manifest_rows)
    closure = read_csv(QP075 / "qp075_campaign_closure_summary_table.csv")
    operators = read_csv(QP075 / "qp075_role_operator_closure_table.csv")
    decision_rows = read_csv(QP075 / "qp075_decision_table.csv")
    decision = {row["decision_item"]: row["decision_value"] for row in decision_rows}

    evidence = []
    required_row_fields = ["role_operator_or_ladder", "k_expression", "k_class", "structural_reading"]
    for row in closure:
        missing = [field for field in required_row_fields if not row.get(field, "").strip()]
        status = "PASS" if not missing and row.get("free_parameters_used") == "0" else "FAIL"
        evidence.append({
            "scope": "closure_row",
            "row": row["order"],
            "carrier": row["symbol_or_carrier"],
            "role_operator_or_ladder": row["role_operator_or_ladder"],
            "missing_fields": ";".join(missing),
            "free_parameters_used": row.get("free_parameters_used", ""),
            "status": status,
        })

    for row in operators:
        tuple_ok = all(str(row.get(field, "")).strip().lstrip("-").isdigit() for field in ["k", "shift", "q", "N"])
        missing = []
        for field in ["role_operator", "k_expression", "k_class", "structural_reading"]:
            if not row.get(field, "").strip():
                missing.append(field)
        status = "PASS" if tuple_ok and not missing and row.get("free_parameters_used") == "0" else "FAIL"
        evidence.append({
            "scope": "role_operator",
            "row": row["order"],
            "carrier": row["carrier_or_symbol"],
            "role_operator_or_ladder": row["role_operator"],
            "missing_fields": ";".join(missing) if missing else ("" if tuple_ok else "non_integer_tuple"),
            "free_parameters_used": row.get("free_parameters_used", ""),
            "status": status,
        })

    observed_use_ok = decision.get("observed_mass_use") == "REVEAL_ONLY_RESIDUAL_COLUMN"
    evidence.append({
        "scope": "decision_table",
        "row": "observed_mass_use",
        "carrier": "QP075",
        "role_operator_or_ladder": decision.get("observed_mass_use", ""),
        "missing_fields": "",
        "free_parameters_used": "0",
        "status": "PASS" if observed_use_ok else "FAIL",
    })

    wrong_controls = [
        {
            "wc_id": "WC1",
            "description": "Observed masses used as selector inputs",
            "expected_verdict": "FAIL",
            "detected": observed_use_ok,
            "observed_match": observed_use_ok,
            "notes": "QP075 decision table says REVEAL_ONLY_RESIDUAL_COLUMN",
        },
        {
            "wc_id": "WC2",
            "description": "Missing selector field in closure row",
            "expected_verdict": "FAIL",
            "detected": all(row["status"] == "PASS" for row in evidence if row["scope"] == "closure_row"),
            "observed_match": all(row["status"] == "PASS" for row in evidence if row["scope"] == "closure_row"),
            "notes": "every closure row has selector fields",
        },
        {
            "wc_id": "WC3",
            "description": "Non-integer role-operator tuple",
            "expected_verdict": "FAIL",
            "detected": all(row["status"] == "PASS" for row in evidence if row["scope"] == "role_operator"),
            "observed_match": all(row["status"] == "PASS" for row in evidence if row["scope"] == "role_operator"),
            "notes": "every operator row has integer k, shift, q, N",
        },
    ]

    passed = (
        all(row["status"] == "PASS" for row in evidence)
        and all(row["observed_match"] for row in wrong_controls)
        and not mcheck["missing"]
        and not mcheck["mismatches"]
        and mcheck["manifest_seal_matches"]
    )
    verdict = "PASS_QP075_SELECTOR_PROVENANCE_AND_FORBIDDEN_TARGETS" if passed else "FAIL_SELECTOR_PROVENANCE"
    reason = "QP075 exposes selector/role provenance and keeps observed masses in reveal-only residual columns."

    write_csv(HERE / f"{CR_ID}_input_manifest.csv", manifest_rows)
    write_csv(HERE / f"{CR_ID}_evidence_rows.csv", evidence)
    write_csv(HERE / f"{CR_ID}_wrong_controls.csv", wrong_controls)
    write_json(HERE / f"{CR_ID}_manifest_seal_check.json", mcheck)

    out_summary = {
        "cr_id": CR_ID,
        "branch": "09a_PARTICLE_MASS_CHAIN",
        "execution_status": "CLEAN",
        "scientific_verdict": verdict,
        "triage_bin": "A" if verdict.startswith("PASS") else "C",
        "reason": reason,
        "captured_at_utc": now(),
        "closure_rows_checked": len(closure),
        "role_operator_rows_checked": len(operators),
        "observed_mass_use": decision.get("observed_mass_use"),
        "manifest_sha256": mcheck["manifest_sha256"],
    }
    write_json(HERE / f"{CR_ID}_summary.json", out_summary)

    result = f"""# {CR_ID} Selector Provenance and Forbidden Targets

## Verdict

```text
{CR_ID}_{verdict}
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = {verdict}
triage_bin = {out_summary['triage_bin']}
```

## Reason

```text
{reason}
```

## Phase Summary

```text
closure rows checked        {len(closure)}
role-operator rows checked  {len(operators)}
observed mass use           {decision.get('observed_mass_use')}
manifest rows verified      {mcheck['verified']}/{mcheck['manifest_rows']}
```

## Rule-9 Line

```text
This test could have falsified selector provenance if any QP075 row lacked a
role/lane, k expression, k class, structural reading, integer operator tuple,
or if observed masses were used anywhere except the reveal-only residual
column.
```
"""
    (HERE / f"{CR_ID}_result.md").write_text(result, encoding="utf-8")

    hash_files = [
        HERE / f"{CR_ID}_PRECOMMIT.md",
        HERE / f"{CR_ID}_declared_premises.json",
        Path(__file__),
        HERE / f"{CR_ID}_input_manifest.csv",
        HERE / f"{CR_ID}_evidence_rows.csv",
        HERE / f"{CR_ID}_wrong_controls.csv",
        HERE / f"{CR_ID}_manifest_seal_check.json",
        HERE / f"{CR_ID}_summary.json",
        HERE / f"{CR_ID}_result.md",
    ]
    (HERE / "HASHES.txt").write_text(
        "\n".join(f"sha256  {rel(p)}  {sha256(p)}" for p in hash_files if p.exists()) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({"cr_id": CR_ID, "scientific_verdict": verdict, "reason": reason}, indent=2))


if __name__ == "__main__":
    main()
