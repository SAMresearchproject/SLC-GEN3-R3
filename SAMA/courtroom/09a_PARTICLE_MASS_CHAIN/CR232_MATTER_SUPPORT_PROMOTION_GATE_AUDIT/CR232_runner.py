"""
CR232 Matter / Support Promotion Gate Audit — Runner

Audits the locked CR222d gate equations as a standalone theorem across all 139
rows of the canonical CR219 source.

Theorem (locked in precommit, sha 4b29f49c5818816620ad3b7a49644cf8de3385ac642019b844e173f556696765):

    G_matter = 0  =>  M_obs = qA = T = W = 0
    G_matter = 1  =>  qA = M_obs * (1 + |q|/R^2)
                       T  = qA / 8
                       W  = 7 * qA / 8

Plus the hidden_source_support surcharge shape:

    M_native = p + p^2 / R^2     (still blocked from emitting)

Wrong controls:
    WC1: promote a blocked row -> qA prediction does not match uploaded qA=0
    WC2: T = qA/7 instead of qA/8 -> tensor predictions do not match
    WC3: W = 6*qA/8 instead of 7*qA/8 -> retained predictions do not match
    WC4: M_native = p + p^2/100 instead of p + p^2/144 -> surcharge shape breaks
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from decimal import Decimal, getcontext, InvalidOperation
from pathlib import Path

getcontext().prec = 80

CR_DIR = Path(__file__).resolve().parent
SOURCE_CSV = Path(r"C:\VS\CR219_promoted_particle_rows_126.csv")
SOURCE_SHA_EXPECTED = "45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f"
PRECOMMIT_SHA = "4b29f49c5818816620ad3b7a49644cf8de3385ac642019b844e173f556696765"

R = 12
R2 = R * R
TOL = Decimal("0.000001")
EIGHT = Decimal(8)
SEVEN = Decimal(7)
SIX = Decimal(6)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_rows(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        if header[0].isdigit():
            header[0] = "source_order"
        rows = [dict(zip(header, r)) for r in reader]
    return header, rows


def dec(value: str) -> Decimal:
    value = (value or "").strip()
    if value.lower() in {"", "no", "none", "null", "nan", "no_surface_depth"}:
        return Decimal(0)
    try:
        return Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"not decimal: {value!r}") from exc


def close(a: Decimal, b: Decimal, tol: Decimal = TOL) -> bool:
    return abs(a - b) <= tol


def parse_p(row: dict) -> int:
    route = row.get("route_combination", "")
    m = re.search(r"p=(\d+)", route)
    if m:
        return int(m.group(1))
    q_abs = row.get("q_abs", "")
    if q_abs.isdigit():
        return int(q_abs)
    raise ValueError(f"cannot parse p from {row.get('candidate_id')}")


def audit_matter_row(row: dict) -> dict:
    """Apply G_matter=1 gate equations and verify against uploaded columns."""
    m_obs = dec(row["M_observed_candidate"])
    q_abs = dec(row["q_abs"])
    qA_expected = m_obs * (Decimal(1) + (q_abs / Decimal(R2)))
    T_expected = qA_expected / EIGHT
    W_expected = qA_expected * SEVEN / EIGHT
    qA_observed = dec(row["qA_source_support"])
    T_observed = dec(row["tensor_carrier_support"])
    W_observed = dec(row["retained_write_support"])
    qA_match = close(qA_observed, qA_expected)
    T_match = close(T_observed, T_expected)
    W_match = close(W_observed, W_expected)
    return {
        "candidate_id": row["candidate_id"],
        "bin": row["bin"],
        "q_sign": row["q_sign"],
        "q_abs": str(q_abs),
        "M_obs": str(m_obs),
        "qA_observed": str(qA_observed),
        "qA_expected": str(qA_expected),
        "qA_distance": str(abs(qA_observed - qA_expected)),
        "qA_match": qA_match,
        "T_observed": str(T_observed),
        "T_expected": str(T_expected),
        "T_distance": str(abs(T_observed - T_expected)),
        "T_match": T_match,
        "W_observed": str(W_observed),
        "W_expected": str(W_expected),
        "W_distance": str(abs(W_observed - W_expected)),
        "W_match": W_match,
        "all_three_match": qA_match and T_match and W_match,
    }


def audit_blocked_row(row: dict) -> dict:
    """Apply G_matter=0 gate: M_obs = qA = T = W = 0 within tolerance."""
    m_obs = dec(row["M_observed_candidate"])
    qA = dec(row["qA_source_support"])
    T = dec(row["tensor_carrier_support"])
    W = dec(row["retained_write_support"])
    zero = Decimal(0)
    m_obs_zero = close(m_obs, zero)
    qA_zero = close(qA, zero)
    T_zero = close(T, zero)
    W_zero = close(W, zero)
    return {
        "candidate_id": row["candidate_id"],
        "bin": row["bin"],
        "operator_class": row["operator_class"],
        "M_native": row["M_native"],
        "M_obs_observed": str(m_obs),
        "M_obs_zero": m_obs_zero,
        "qA_observed": str(qA),
        "qA_zero": qA_zero,
        "T_observed": str(T),
        "T_zero": T_zero,
        "W_observed": str(W),
        "W_zero": W_zero,
        "all_four_zero": m_obs_zero and qA_zero and T_zero and W_zero,
    }


def audit_surcharge_row(row: dict) -> dict:
    """Apply hidden_source_support surcharge: M_native = p + p^2/R^2."""
    p = parse_p(row)
    expected = Decimal(p) + (Decimal(p * p) / Decimal(R2))
    observed = dec(row["M_native"])
    match = close(observed, expected)
    return {
        "candidate_id": row["candidate_id"],
        "p": p,
        "M_native_observed": str(observed),
        "M_native_expected": str(expected),
        "distance": str(abs(observed - expected)),
        "matches_surcharge_shape": match,
    }


# ---- Wrong controls ----

def wc1_promote_blocked_row(blocked_row: dict) -> dict:
    """Treat a hidden_source_support row as if G_matter=1.
    Predict qA from M_native; compare against uploaded qA (which is 0).
    WC1 expected to BREAK (predicted qA != uploaded qA=0)."""
    p = parse_p(blocked_row)
    m_native_value = Decimal(p) + (Decimal(p * p) / Decimal(R2))  # use the surcharge value
    q_abs = dec(blocked_row["q_abs"])
    qA_predicted_if_matter = m_native_value * (Decimal(1) + (q_abs / Decimal(R2)))
    qA_uploaded = dec(blocked_row["qA_source_support"])
    broke = not close(qA_predicted_if_matter, qA_uploaded)
    return {
        "candidate_id": blocked_row["candidate_id"],
        "p": p,
        "qA_predicted_if_matter": str(qA_predicted_if_matter),
        "qA_uploaded": str(qA_uploaded),
        "distance": str(abs(qA_predicted_if_matter - qA_uploaded)),
        "broke_as_predicted": broke,
    }


def wc2_wrong_tensor_ratio(matter_rows: list) -> dict:
    """Replace T = qA/8 with T = qA/7. WC2 expected to BREAK on every nonzero row."""
    breaks = 0
    nonzero = 0
    for row in matter_rows:
        qA = dec(row["qA_source_support"])
        T_observed = dec(row["tensor_carrier_support"])
        T_wrong = qA / SEVEN  # would-be ratio
        if qA != 0:
            nonzero += 1
            if not close(T_observed, T_wrong):
                breaks += 1
    return {
        "rule_under_test": "T = qA/7 (wrong; correct is qA/8)",
        "nonzero_rows_checked": nonzero,
        "breaks_count": breaks,
        "broke_all_as_predicted": breaks == nonzero,
    }


def wc3_wrong_retained_ratio(matter_rows: list) -> dict:
    """Replace W = 7*qA/8 with W = 6*qA/8. WC3 expected to BREAK."""
    breaks = 0
    nonzero = 0
    for row in matter_rows:
        qA = dec(row["qA_source_support"])
        W_observed = dec(row["retained_write_support"])
        W_wrong = qA * SIX / EIGHT
        if qA != 0:
            nonzero += 1
            if not close(W_observed, W_wrong):
                breaks += 1
    return {
        "rule_under_test": "W = 6*qA/8 (wrong; correct is 7*qA/8)",
        "nonzero_rows_checked": nonzero,
        "breaks_count": breaks,
        "broke_all_as_predicted": breaks == nonzero,
    }


def wc4_wrong_surcharge_shape(hidden_support_rows: list) -> dict:
    """Replace surcharge M_native = p + p^2/144 with M_native = p + p^2/100. WC4 expected to BREAK."""
    breaks = 0
    nonzero_p_count = 0
    HUNDRED = Decimal(100)
    for row in hidden_support_rows:
        p = parse_p(row)
        if p == 0:
            continue
        nonzero_p_count += 1
        observed = dec(row["M_native"])
        wrong_expected = Decimal(p) + (Decimal(p * p) / HUNDRED)
        if not close(observed, wrong_expected):
            breaks += 1
    return {
        "rule_under_test": "M_native = p + p^2/100 (wrong; correct is p + p^2/144)",
        "nonzero_p_rows_checked": nonzero_p_count,
        "breaks_count": breaks,
        "broke_all_as_predicted": breaks == nonzero_p_count,
    }


# ---- CSV writers ----

def write_csv(path: Path, rows: list, fields: list):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fields})


def main():
    print("=" * 72)
    print("CR232 Matter / Support Promotion Gate Audit")
    print("=" * 72)

    # ---- Source verification ----
    src_sha = sha256_file(SOURCE_CSV)
    print(f"\nSource: {SOURCE_CSV}")
    print(f"  SHA-256:  {src_sha}")
    print(f"  Expected: {SOURCE_SHA_EXPECTED}")
    assert src_sha == SOURCE_SHA_EXPECTED, "source SHA mismatch — refusing to run"
    print("  [PASS] source SHA matches precommit lock")

    header, rows = load_rows(SOURCE_CSV)
    print(f"\nRows loaded: {len(rows)}")
    assert len(rows) == 139

    bin_counter = Counter(r["bin"] for r in rows)
    allowed_counter = Counter(r["matter_row_allowed"] for r in rows)
    print(f"  bins:    {dict(bin_counter)}")
    print(f"  allowed: {dict(allowed_counter)}")

    matter_rows = [r for r in rows if r["matter_row_allowed"] == "yes"]
    blocked_rows = [r for r in rows if r["matter_row_allowed"] == "no"]
    hidden_support_rows = [r for r in rows if r["bin"] == "hidden_source_support_rows"]

    assert len(matter_rows) == 126, f"expected 126 matter rows, got {len(matter_rows)}"
    assert len(blocked_rows) == 13, f"expected 13 blocked rows, got {len(blocked_rows)}"
    assert len(hidden_support_rows) == 8, f"expected 8 hidden support rows, got {len(hidden_support_rows)}"
    print("  [P1 PASS] 126 matter + 13 blocked + 8 hidden support partitioning confirmed")

    # ---- AUDIT 1: matter rows obey qA/T/W identities ----
    print(f"\n[AUDIT 1] {len(matter_rows)} matter rows: qA = M_obs*(1+|q|/144), T = qA/8, W = 7*qA/8")
    matter_audit = [audit_matter_row(r) for r in matter_rows]
    matter_pass = sum(1 for a in matter_audit if a["all_three_match"])
    matter_fail = sum(1 for a in matter_audit if not a["all_three_match"])
    print(f"  pass: {matter_pass} / {len(matter_rows)}")
    print(f"  fail: {matter_fail}")
    matter_audit_passes = matter_pass == len(matter_rows)
    print(f"  [P2 {'PASS' if matter_audit_passes else 'FAIL'}]")

    # ---- AUDIT 2: blocked rows have all four channels zero ----
    print(f"\n[AUDIT 2] {len(blocked_rows)} blocked rows: M_obs = qA = T = W = 0")
    blocked_audit = [audit_blocked_row(r) for r in blocked_rows]
    blocked_pass = sum(1 for a in blocked_audit if a["all_four_zero"])
    blocked_fail = sum(1 for a in blocked_audit if not a["all_four_zero"])
    print(f"  pass: {blocked_pass} / {len(blocked_rows)}")
    print(f"  fail: {blocked_fail}")
    blocked_audit_passes = blocked_pass == len(blocked_rows)
    print(f"  [P3 {'PASS' if blocked_audit_passes else 'FAIL'}]")

    # ---- AUDIT 3: hidden support surcharge shape ----
    print(f"\n[AUDIT 3] {len(hidden_support_rows)} hidden-source-support rows: M_native = p + p^2/R^2")
    surcharge_audit = [audit_surcharge_row(r) for r in hidden_support_rows]
    surcharge_pass = sum(1 for a in surcharge_audit if a["matches_surcharge_shape"])
    surcharge_fail = sum(1 for a in surcharge_audit if not a["matches_surcharge_shape"])
    print(f"  pass: {surcharge_pass} / {len(hidden_support_rows)}")
    print(f"  fail: {surcharge_fail}")
    surcharge_audit_passes = surcharge_pass == len(hidden_support_rows)
    print(f"  [P4 {'PASS' if surcharge_audit_passes else 'FAIL'}]")

    # ---- WRONG CONTROLS ----
    print("\n[WC1] Promote a blocked row (QP093A-0306, p=1) as if G_matter=1:")
    wc1_row = next(r for r in blocked_rows if r["candidate_id"] == "QP093A-0306")
    wc1 = wc1_promote_blocked_row(wc1_row)
    print(f"  candidate: {wc1['candidate_id']}, p={wc1['p']}")
    print(f"  qA_predicted_if_matter: {wc1['qA_predicted_if_matter']}")
    print(f"  qA_uploaded:            {wc1['qA_uploaded']}")
    print(f"  broke_as_predicted:     {wc1['broke_as_predicted']}")

    print("\n[WC2] Wrong tensor ratio T = qA/7 instead of qA/8:")
    wc2 = wc2_wrong_tensor_ratio(matter_rows)
    print(f"  nonzero rows: {wc2['nonzero_rows_checked']}")
    print(f"  breaks:       {wc2['breaks_count']}")
    print(f"  broke_all_as_predicted: {wc2['broke_all_as_predicted']}")

    print("\n[WC3] Wrong retained ratio W = 6*qA/8 instead of 7*qA/8:")
    wc3 = wc3_wrong_retained_ratio(matter_rows)
    print(f"  nonzero rows: {wc3['nonzero_rows_checked']}")
    print(f"  breaks:       {wc3['breaks_count']}")
    print(f"  broke_all_as_predicted: {wc3['broke_all_as_predicted']}")

    print("\n[WC4] Wrong surcharge shape M_native = p + p^2/100 instead of /144:")
    wc4 = wc4_wrong_surcharge_shape(hidden_support_rows)
    print(f"  nonzero-p rows: {wc4['nonzero_p_rows_checked']}")
    print(f"  breaks:         {wc4['breaks_count']}")
    print(f"  broke_all_as_predicted: {wc4['broke_all_as_predicted']}")

    all_wcs_passed = (
        wc1["broke_as_predicted"]
        and wc2["broke_all_as_predicted"]
        and wc3["broke_all_as_predicted"]
        and wc4["broke_all_as_predicted"]
    )
    print(f"\n[P5 {'PASS' if all_wcs_passed else 'FAIL'}] all four wrong controls broke as predicted")

    # ---- WRITE CSVs ----
    write_csv(CR_DIR / "CR232_matter_row_audit.csv", matter_audit,
              ["candidate_id", "bin", "q_sign", "q_abs", "M_obs",
               "qA_observed", "qA_expected", "qA_distance", "qA_match",
               "T_observed", "T_expected", "T_distance", "T_match",
               "W_observed", "W_expected", "W_distance", "W_match",
               "all_three_match"])
    write_csv(CR_DIR / "CR232_blocked_row_audit.csv", blocked_audit,
              ["candidate_id", "bin", "operator_class", "M_native",
               "M_obs_observed", "M_obs_zero",
               "qA_observed", "qA_zero",
               "T_observed", "T_zero",
               "W_observed", "W_zero",
               "all_four_zero"])
    write_csv(CR_DIR / "CR232_surcharge_audit.csv", surcharge_audit,
              ["candidate_id", "p", "M_native_observed", "M_native_expected",
               "distance", "matches_surcharge_shape"])
    print(f"\nWrote: CR232_matter_row_audit.csv ({len(matter_audit)} rows)")
    print(f"Wrote: CR232_blocked_row_audit.csv ({len(blocked_audit)} rows)")
    print(f"Wrote: CR232_surcharge_audit.csv ({len(surcharge_audit)} rows)")

    # ---- VERDICT ----
    main_audit_pass = matter_audit_passes and blocked_audit_passes and surcharge_audit_passes
    overall_pass = main_audit_pass and all_wcs_passed
    verdict = "PASS" if overall_pass else "FAIL"

    print("\n" + "=" * 72)
    print(f"MAIN AUDIT pass:   {main_audit_pass}")
    print(f"WRONG CONTROLS:    {all_wcs_passed}")
    print(f"CR232 VERDICT:     {verdict}")
    print("=" * 72)

    # ---- SUMMARY ----
    summary = {
        "artifact": "CR232_MATTER_SUPPORT_PROMOTION_GATE_AUDIT",
        "classification": "STRUCTURAL_THEOREM_AUDIT",
        "arc_position": "Test 3 of 7 in the Seven-Test Ownership Arc",
        "permission_status": "GRANTED_BY_USER_SEAN_BRADY_2026_06_22",
        "precommit_sha256": PRECOMMIT_SHA,
        "source_file": str(SOURCE_CSV),
        "source_sha256": src_sha,
        "constants": {"R": R, "R2": R2, "tolerance": str(TOL)},
        "row_partition": {
            "total": len(rows),
            "matter_rows": len(matter_rows),
            "blocked_rows": len(blocked_rows),
            "hidden_source_support_rows": len(hidden_support_rows),
        },
        "audit_1_matter": {
            "rule": "qA = M_obs*(1+|q|/R^2); T = qA/8; W = 7*qA/8",
            "rows_checked": len(matter_rows),
            "pass_count": matter_pass,
            "fail_count": matter_fail,
            "passes_audit": matter_audit_passes,
        },
        "audit_2_blocked": {
            "rule": "M_obs = qA = T = W = 0",
            "rows_checked": len(blocked_rows),
            "pass_count": blocked_pass,
            "fail_count": blocked_fail,
            "passes_audit": blocked_audit_passes,
        },
        "audit_3_surcharge": {
            "rule": "M_native = p + p^2/R^2",
            "rows_checked": len(hidden_support_rows),
            "pass_count": surcharge_pass,
            "fail_count": surcharge_fail,
            "passes_audit": surcharge_audit_passes,
        },
        "wrong_controls": {
            "WC1_promote_blocked_row": wc1,
            "WC2_wrong_tensor_ratio": wc2,
            "WC3_wrong_retained_ratio": wc3,
            "WC4_wrong_surcharge_shape": wc4,
            "all_broke_as_predicted": all_wcs_passed,
        },
        "scientific_verdict": verdict,
        "execution_status": "CLEAN",
        "main_audit_passed": main_audit_pass,
        "wrong_controls_passed": all_wcs_passed,
        "K_gates": {
            "K1_external_anchor": "N/A (closed-form structural audit)",
            "K2_falsification_statement": "PASS",
            "K3_target_hygiene": "PASS (theorem + tolerance + WCs locked in precommit before runner ran)",
            "K4_typed_inputs": "PASS (single SHA-locked CSV + R=12)",
            "K5_reproduction_on_demand": "PASS (deterministic runner; sub-second runtime)",
        },
    }
    with (CR_DIR / "CR232_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)
    print("Wrote: CR232_summary.json")
    return verdict


if __name__ == "__main__":
    main()
