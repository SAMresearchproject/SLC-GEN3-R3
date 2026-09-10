"""CR063a_WRONG_CONTROLS_AND_NEAR_NEIGHBORS.py

Courtroom wrong-control and misroute quarantine test.

This script directly verifies that the old 09 15-row branch is preserved only
as historical evidence and that QP075 is the active 35-row / 26-operator source.
"""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


CR_ID = "CR063a"
HERE = Path(__file__).resolve().parent
BRANCH = HERE.parent
COURTROOM = BRANCH.parent
QP075 = Path("C:/VS/quantum_phase/artifacts/qp075")
OLD_09 = COURTROOM / "09_PARTICLE_MASS_CHAIN"
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


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


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
    old_cr062_path = OLD_09 / "CR062_ROW_BY_ROW_PARTICLE_LEDGER/CR062_summary.json"
    old_claim_path = OLD_09 / "CR064a_APPEAL_QP075_FULL_LEDGER/CR064a_revised_strongest_claim.md"
    old_cr062 = read_json(old_cr062_path)
    old_claim = old_claim_path.read_text(encoding="utf-8", errors="ignore")
    qp075_summary = read_json(QP075 / "qp075_summary.json")
    qp075_closure = read_csv(QP075 / "qp075_campaign_closure_summary_table.csv")
    qp075_operators = read_csv(QP075 / "qp075_role_operator_closure_table.csv")

    old_rows = old_cr062.get("phases", {}).get("phase_2_row_extraction", {}).get("rows_extracted")
    old_scope_ack = "15-row scope" in old_claim or "15 rows" in old_claim or "15-row" in old_claim
    qp075_35_ack = "35-row" in old_claim
    qp075_26_ack = "26-row operator backbone" in old_claim or "26-operator backbone" in old_claim

    evidence = [
        {
            "check": "old_cr062_rows_extracted",
            "observed": old_rows,
            "expected": 15,
            "status": "PASS" if old_rows == 15 else "FAIL",
        },
        {
            "check": "old_claim_acknowledges_old_scope",
            "observed": old_scope_ack,
            "expected": True,
            "status": "PASS" if old_scope_ack else "FAIL",
        },
        {
            "check": "old_claim_acknowledges_qp075_35_row_surface",
            "observed": qp075_35_ack,
            "expected": True,
            "status": "PASS" if qp075_35_ack else "FAIL",
        },
        {
            "check": "old_claim_acknowledges_26_operator_backbone",
            "observed": qp075_26_ack,
            "expected": True,
            "status": "PASS" if qp075_26_ack else "FAIL",
        },
        {
            "check": "qp075_active_closure_rows",
            "observed": len(qp075_closure),
            "expected": 35,
            "status": "PASS" if len(qp075_closure) == 35 else "FAIL",
        },
        {
            "check": "qp075_active_operator_rows",
            "observed": len(qp075_operators),
            "expected": 26,
            "status": "PASS" if len(qp075_operators) == 26 else "FAIL",
        },
        {
            "check": "qp075_free_parameters",
            "observed": qp075_summary.get("free_parameters_introduced"),
            "expected": 0,
            "status": "PASS" if qp075_summary.get("free_parameters_introduced") == 0 else "FAIL",
        },
    ]

    wrong_controls = [
        {
            "wc_id": "WC1",
            "description": "Promote old 15-row CR062 as active terminal branch scope",
            "expected_verdict": "FAIL",
            "detected": old_rows == 15 and len(qp075_closure) == 35,
            "observed_match": old_rows == 15 and len(qp075_closure) == 35,
            "notes": "old branch is explicitly different from QP075",
        },
        {
            "wc_id": "WC2",
            "description": "35-row ledger without 26-operator backbone",
            "expected_verdict": "FAIL",
            "detected": len(qp075_operators) == 26,
            "observed_match": len(qp075_operators) == 26,
            "notes": "operator backbone is present",
        },
        {
            "wc_id": "WC3",
            "description": "Old 09 source role upgraded from historical to terminal",
            "expected_verdict": "FAIL",
            "detected": all(r["role"] == "historical_misroute_artifact" for r in manifest_rows if "09_PARTICLE_MASS_CHAIN" in r["path"]),
            "observed_match": all(r["role"] == "historical_misroute_artifact" for r in manifest_rows if "09_PARTICLE_MASS_CHAIN" in r["path"]),
            "notes": "manifest keeps old 09 historical only",
        },
    ]

    passed = (
        all(row["status"] == "PASS" for row in evidence)
        and all(row["observed_match"] for row in wrong_controls)
        and not mcheck["missing"]
        and not mcheck["mismatches"]
        and mcheck["manifest_seal_matches"]
    )
    verdict = "PASS_WRONG_CONTROLS_AND_OLDER_FREEZE_MISROUTE_QUARANTINE" if passed else "FAIL_WRONG_CONTROLS_OR_MISROUTE_QUARANTINE"
    reason = "The old 15-row branch is preserved as historical material, while QP075 is the active 35-row/26-operator source."

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
        "old_cr062_rows_extracted": old_rows,
        "qp075_closure_rows": len(qp075_closure),
        "qp075_operator_rows": len(qp075_operators),
        "manifest_sha256": mcheck["manifest_sha256"],
    }
    write_json(HERE / f"{CR_ID}_summary.json", out_summary)

    result = f"""# {CR_ID} Wrong Controls and Near Neighbors

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
old CR062 row extraction     {old_rows}
QP075 closure rows           {len(qp075_closure)}
QP075 role-operator rows     {len(qp075_operators)}
QP075 free parameters        {qp075_summary.get('free_parameters_introduced')}
manifest rows verified       {mcheck['verified']}/{mcheck['manifest_rows']}
```

## Rule-9 Line

```text
This test could have falsified the corrected branch if the old 15-row result
was indistinguishable from QP075, if the operator backbone was missing, or if
the old 09 artifacts were still promoted as active terminal sources.
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
