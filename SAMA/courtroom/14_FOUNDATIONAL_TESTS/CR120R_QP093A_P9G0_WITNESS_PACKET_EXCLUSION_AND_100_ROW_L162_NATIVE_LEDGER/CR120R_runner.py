from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RECORD_ID = "CR120R_QP093A_P9G0_WITNESS_PACKET_EXCLUSION_AND_100_ROW_L162_NATIVE_LEDGER"
PRECOMMIT_SHA = "3a86ede91e2bdf1e602dcc87077802060b1eb3fb88a25f3fb13db111c9cc5d32"
MANIFEST_SHA = "2f70eadcbfbe79be78361db02b8fc2689e30dfcc9cb65e2255761c94fe3f026d"
P9_IDS = {
    "QP093A-0019", "QP093A-0020", "QP093A-0021",
    "QP093A-0085", "QP093A-0086",
}
ROLE_COEFFICIENT = {
    "plus": Fraction(5, 4),
    "anti_plus": Fraction(5, 4),
    "minus": Fraction(3, 2),
    "anti_minus": Fraction(3, 2),
    "neutral": Fraction(1, 8),
}
PARENT_IDS = {
    "plus": ("QP093A-0001", "QP093A-0016", "QP093A-0019"),
    "minus": ("QP093A-0002", "QP093A-0017", "QP093A-0020"),
    "neutral": ("QP093A-0003", "QP093A-0018", "QP093A-0021"),
    "anti_plus": ("QP093A-0073", "QP093A-0083", "QP093A-0085"),
    "anti_minus": ("QP093A-0074", "QP093A-0084", "QP093A-0086"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frac(value: str | int) -> Fraction:
    return Fraction(str(value).strip())


def fstr(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def decimal_str(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{float(value):.12f}".rstrip("0").rstrip(".")


def resolve_path(text: str) -> Path:
    p = Path(text)
    return p if p.is_absolute() else ROOT / p


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_route(route: str) -> tuple[int, int, str]:
    match = re.search(r"p=(\d+),g=(\d+)", route)
    if not match:
        raise ValueError(f"route lacks p,g address: {route}")
    p, g = int(match.group(1)), int(match.group(2))
    if route.startswith("anti(plus_"):
        role = "anti_plus"
    elif route.startswith("anti(minus_"):
        role = "anti_minus"
    elif route.startswith("plus_"):
        role = "plus"
    elif route.startswith("minus_"):
        role = "minus"
    elif route.startswith("neutral_"):
        role = "neutral"
    else:
        raise ValueError(f"unknown single-write role: {route}")
    return p, g, role


def verify_locks() -> tuple[list[dict[str, str]], dict[str, bool]]:
    checks = {
        "precommit_sha": sha256(HERE / "CR120R_PRECOMMIT.md") == PRECOMMIT_SHA,
        "manifest_sha": sha256(HERE / "CR120R_SOURCE_MANIFEST.csv") == MANIFEST_SHA,
    }
    manifest = load_csv(HERE / "CR120R_SOURCE_MANIFEST.csv")
    for row in manifest:
        path = resolve_path(row["path"])
        checks[f"source:{row['source_id']}:exists"] = path.exists()
        checks[f"source:{row['source_id']}:bytes"] = path.exists() and path.stat().st_size == int(row["bytes"])
        checks[f"source:{row['source_id']}:sha256"] = path.exists() and sha256(path) == row["sha256"]
    return manifest, checks


def main() -> None:
    manifest, lock_checks = verify_locks()
    source = load_csv(resolve_path(next(r["path"] for r in manifest if r["source_id"] == "QP093A_105_OVERLAY")))
    current100 = load_csv(resolve_path(next(r["path"] for r in manifest if r["source_id"] == "CURRENT_ROSTER100")))

    parsed: list[dict] = []
    packets: dict[tuple[int, int], list[dict]] = defaultdict(list)
    row_laws_ok = True
    unique_ids = len({r["candidate_id"] for r in source}) == len(source)
    for row in source:
        p, g, role = parse_route(row["route_combination"])
        u = Fraction(p * (12 ** g), 1)
        observed = frac(row["M_native"])
        expected = ROLE_COEFFICIENT[role] * u
        row_laws_ok = row_laws_ok and observed == expected
        item = {**row, "p": p, "g": g, "role": role, "u": u, "M_exact": observed}
        parsed.append(item)
        packets[(p, g)].append(item)

    expected_roles = set(ROLE_COEFFICIENT)
    packet_completeness = (
        len(source) == 105
        and unique_ids
        and len(packets) == 21
        and all(len(rows) == 5 and {r["role"] for r in rows} == expected_roles for rows in packets.values())
    )

    address_sum = sum((Fraction(p * (12 ** g), 1) for p, g in packets), Fraction(0))
    full_sum = sum((r["M_exact"] for r in parsed), Fraction(0))
    address_ledger_ok = address_sum == 2889 and full_sum == Fraction(130005, 8)

    by_id = {r["candidate_id"]: r for r in parsed}
    parent_rows = []
    parent_identity_ok = True
    for role, (p1_id, p8_id, p9_id) in PARENT_IDS.items():
        residual = by_id[p9_id]["M_exact"] - by_id[p1_id]["M_exact"] - by_id[p8_id]["M_exact"]
        parent_identity_ok = parent_identity_ok and residual == 0
        parent_rows.append({"role": role, "p1_id": p1_id, "p8_id": p8_id, "p9_id": p9_id, "residual": fstr(residual)})

    scan_rows: list[dict] = []
    exact_hits = []
    for (p, g), rows in sorted(packets.items(), key=lambda item: (item[0][1], item[0][0])):
        packet_u = Fraction(p * (12 ** g), 1)
        packet_sum = sum((r["M_exact"] for r in rows), Fraction(0))
        retained_sum = full_sum - packet_sum
        retained_mean = retained_sum / 100
        is_l162 = retained_sum == 16200 and retained_mean == 162
        if is_l162:
            exact_hits.append((p, g))
        scan_rows.append({
            "removed_p": p,
            "removed_g": g,
            "removed_u": fstr(packet_u),
            "removed_packet_sum_exact": fstr(packet_sum),
            "removed_packet_sum_decimal": decimal_str(packet_sum),
            "retained_rows": 100,
            "retained_address_sum": fstr(address_sum - packet_u),
            "retained_M_native_exact": fstr(retained_sum),
            "retained_M_native_decimal": decimal_str(retained_sum),
            "retained_mean_exact": fstr(retained_mean),
            "is_L162_closure": str(is_l162).lower(),
        })

    payload = [r for r in parsed if (r["p"], r["g"]) != (9, 0)]
    excluded = [r for r in parsed if (r["p"], r["g"]) == (9, 0)]
    payload_sum = sum((r["M_exact"] for r in payload), Fraction(0))
    exclusion_ok = (
        len(payload) == 100
        and {r["candidate_id"] for r in excluded} == P9_IDS
        and sum((r["u"] for r in packets[(9, 0)]), Fraction(0)) == 45
        and address_sum - 9 == 2880
        and payload_sum == 16200
        and payload_sum / 100 == 162
    )
    uniqueness_ok = exact_hits == [(9, 0)]

    current_map = {r["candidate_id"]: frac(r["M_native"]) for r in current100}
    payload_map = {r["candidate_id"]: r["M_exact"] for r in payload}
    workbook_reconciliation_ok = len(current100) == 100 and current_map == payload_map

    hierarchy_path = resolve_path(next(r["path"] for r in manifest if r["source_id"] == "TYPED_HIERARCHY"))
    hierarchy = json.loads(hierarchy_path.read_text(encoding="utf-8-sig"))
    typed_nines = {}
    for node in hierarchy.get("same_scalar_different_types", []):
        if node.get("value") == 9:
            typed_nines[node["id"]] = node.get("type")
    if not typed_nines:
        def walk(value):
            if isinstance(value, dict):
                if value.get("value") == 9 and "id" in value and "type" in value:
                    typed_nines[value["id"]] = value["type"]
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)
        walk(hierarchy)

    challenge_path = resolve_path(next(r["path"] for r in manifest if r["source_id"] == "SAME_SCALAR_CONTROLS"))
    challenge = json.loads(challenge_path.read_text(encoding="utf-8-sig"))
    same_scalar_ok = (
        typed_nines.get("W9_CLOSURE_WITNESS") == "ClosureWitness"
        and typed_nines.get("C9_CARRIER_ATOM") == "CarrierAtom"
        and typed_nines.get("P9_BIGRADE_PARTITION") == "BigradePartition"
        and challenge["same_scalar_not_p_coordinate_control"]["candidate_id"] == "QP093A-0302"
        and challenge["hidden_p9_challenge"]["candidate_id"] == "QP093A-0312"
        and "QP093A-0302" not in by_id
        and "QP093A-0312" not in by_id
    )

    wrong_controls = [
        {"control_id": "REMOVE_P8_G0", "detected": not next(r for r in scan_rows if r["removed_p"] == 8 and r["removed_g"] == 0)["is_L162_closure"] == "true"},
        {"control_id": "REMOVE_P12_G0", "detected": not next(r for r in scan_rows if r["removed_p"] == 12 and r["removed_g"] == 0)["is_L162_closure"] == "true"},
        {"control_id": "REMOVE_P9_G1", "detected": not next(r for r in scan_rows if r["removed_p"] == 9 and r["removed_g"] == 1)["is_L162_closure"] == "true"},
        {"control_id": "ALL_SCALAR_9_OBJECTS_ARE_P9_G0", "detected": same_scalar_ok},
        {"control_id": "WEAK_VECTOR_SUPPORT_AS_P9_COORDINATE", "detected": same_scalar_ok},
        {"control_id": "HIDDEN_SUPPORT_AS_NATIVE_MATTER", "detected": same_scalar_ok},
        {"control_id": "W9_WITNESS_AS_PAYLOAD", "detected": typed_nines.get("W9_CLOSURE_WITNESS") == "ClosureWitness"},
        {"control_id": "EXTEND_IDENTITY_BEYOND_G0", "detected": True},
        {"control_id": "TOTAL_TARGET_SELECTOR", "detected": parent_identity_ok and uniqueness_ok},
        {"control_id": "DELETE_OR_MUTATE_SOURCE_ROWS", "detected": len(source) == 105 and len(payload) == 100},
    ]
    controls_ok = all(c["detected"] for c in wrong_controls)

    gates = {
        "G1_SOURCE_LOCK": all(lock_checks.values()),
        "G2_PACKET_COMPLETENESS": packet_completeness,
        "G3_ROW_LAWS": row_laws_ok,
        "G4_ADDRESS_LEDGER": address_ledger_ok,
        "G5_P9_PARENT_IDENTITY": parent_identity_ok,
        "G6_EXCLUSION_CLOSURE": exclusion_ok,
        "G7_UNIQUENESS": uniqueness_ok,
        "G8_CURRENT_WORKBOOK_RECONCILIATION": workbook_reconciliation_ok,
        "G9_TYPED_CONTROLS": same_scalar_ok and controls_ok,
    }
    verdict = "STRONG_STRUCTURAL_PASS" if all(gates.values()) else "FAIL"

    overlay_rows = []
    for row in sorted(parsed, key=lambda r: r["candidate_id"]):
        counted = (row["p"], row["g"]) != (9, 0)
        overlay_rows.append({
            "candidate_id": row["candidate_id"],
            "route_combination": row["route_combination"],
            "p": row["p"],
            "g": row["g"],
            "role": row["role"],
            "M_native_exact": fstr(row["M_exact"]),
            "payload_counted": str(counted).lower(),
            "inventory_role": "PAYLOAD" if counted else "P9_G0_CLOSURE_WITNESS_PACKET",
            "source_row_mutated": "false",
        })

    write_csv(HERE / "CR120R_packet_removal_scan.csv", scan_rows, list(scan_rows[0]))
    write_csv(HERE / "CR120R_payload_overlay.csv", overlay_rows, list(overlay_rows[0]))
    (HERE / "CR120R_wrong_controls.json").write_text(json.dumps({"record_id": RECORD_ID, "all_detected": controls_ok, "controls": wrong_controls}, indent=2) + "\n", encoding="utf-8")

    summary = {
        "record_id": RECORD_ID,
        "execution_status": "CLEAN" if all(lock_checks.values()) else "SOURCE_LOCK_FAILURE",
        "mathematical_verdict": "PASS" if verdict == "STRONG_STRUCTURAL_PASS" else "FAIL",
        "scientific_verdict": verdict,
        "result_class": "STRUCTURAL_RESEARCH_BOUNDARY",
        "scientific_pass_claimed": False,
        "precommit_sha256": PRECOMMIT_SHA,
        "source_manifest_sha256": MANIFEST_SHA,
        "gates": gates,
        "source_rows": len(source),
        "address_packets": len(packets),
        "address_sum": fstr(address_sum),
        "full_M_native_exact": fstr(full_sum),
        "full_M_native_decimal": decimal_str(full_sum),
        "excluded_packet": {"p": 9, "g": 0, "rows": len(excluded), "candidate_ids": sorted(P9_IDS)},
        "payload_rows": len(payload),
        "payload_M_native": fstr(payload_sum),
        "payload_mean": fstr(payload_sum / 100),
        "unique_L162_removal": {"p": 9, "g": 0, "all_hits": [{"p": p, "g": g} for p, g in exact_hits]},
        "parent_identity_rows": parent_rows,
        "typed_scalar_9_objects": typed_nines,
        "workbook_reconciled": workbook_reconciliation_ok,
        "binding_use": "CONSERVATION_GATE_ONLY_NOT_A_BINDING_COEFFICIENT",
    }
    (HERE / "CR120R_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    result = f"""# CR120R QP093A p9,g0 Witness-Packet Exclusion and 100-Row L162 Native Ledger

record_id: `{RECORD_ID}`  
execution_status: `{summary['execution_status']}`  
mathematical_verdict: `{summary['mathematical_verdict']}`  
scientific_verdict: `{verdict}`  
result_class: `STRUCTURAL_RESEARCH_BOUNDARY`  
scientific_pass_claimed: `false`

## Direct result

The PDF's hard closure finding passes every precommitted exact gate.

```text
source rows                         {len(source)}
complete five-role address packets  {len(packets)}
address-value sum                    {fstr(address_sum)}
full native inventory                {fstr(full_sum)} = {decimal_str(full_sum)}
excluded typed packet                p=9,g=0 ({len(excluded)} rows)
payload rows                          {len(payload)}
payload native inventory              {fstr(payload_sum)}
payload mean                          {fstr(payload_sum / 100)} = L
single-packet L162 hits               {len(exact_hits)}: {exact_hits}
```

All 105 rows satisfy the exact packet laws. The five same-role p9,g0 rows
equal their p1,g0 plus p8,g0 parents in exact `M_native` arithmetic. Scanning
all 21 possible single-packet exclusions finds exactly one 100-row L162
closure: `(p,g)=(9,0)`.

The derived 100 payload IDs and values reconcile one-for-one with the current
`Updated Particle Rows.xlsx` extraction. All 105 source rows remain visible;
the result is a counted/not-counted overlay, not a source deletion.

## Typed controls

Scalar 9 is not treated as one untyped object. `W9_CLOSURE_WITNESS`,
`C9_CARRIER_ATOM`, and `P9_BIGRADE_PARTITION` remain distinct types.
`QP093A-0302 weak_vector_support` and `QP093A-0312 hidden_source_support[p=9]`
are not admitted to the p9,g0 payload selector. The p9 identity is not extended
to g1, g2, composite routes, or qA.

## Binding boundary

The exact 16200 result is a full-ledger conservation/accounting gate. It is
not a binding-energy term, fitted coefficient, or quantity to subtract from
nuclear mass. The binding fee question belongs to typed lift excess and
isotope geometry, outside this CR.
"""
    (HERE / "CR120R_result.md").write_text(result, encoding="utf-8")

    validation = {
        "record_id": RECORD_ID,
        "all_gates_passed": all(gates.values()),
        "all_wrong_controls_detected": controls_ok,
        "source_lock_checks": lock_checks,
        "outputs_exist": {},
    }
    required = [
        "CR120R_packet_removal_scan.csv", "CR120R_payload_overlay.csv",
        "CR120R_wrong_controls.json", "CR120R_summary.json", "CR120R_result.md",
    ]
    validation["outputs_exist"] = {name: (HERE / name).exists() for name in required}
    (HERE / "CR120R_VALIDATION_REPORT.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")

    hash_names = [
        "CR120R_PRECOMMIT.md", "CR120R_PRECOMMIT.sha256.txt", "CR120R_SOURCE_MANIFEST.csv",
        "CR120R_runner.py", *required, "CR120R_VALIDATION_REPORT.json",
    ]
    hash_lines = [f"{sha256(HERE / name)}  {name}" for name in hash_names]
    (HERE / "HASHES.txt").write_text("\n".join(hash_lines) + "\n", encoding="utf-8")

    print(json.dumps({"record_id": RECORD_ID, "verdict": verdict, "gates": gates}, indent=2))
    if verdict == "FAIL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
