"""
CR257b -- A Meets Theta at d=1, W4 correction re-run.

Identical to CR257 v1 except:
  - W4 power variant is strictly scoped to the negative side at d=1
    (CR257 v1's runner extended it to both signs, which made power=1
    trivially equal canonical on the positive side and produced an
    8/16 W4 hit that downgraded the verdict to BOUNDARY)
  - E, A, D, W3 are bit-identical to v1

precommit : 3a3b301d45d4573845f6744f315ff4ef6278e9ece0ccf314724f109ee41c9fe7
input     : 59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b
"""

import csv
import hashlib
import json
import os
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
PRECOMMIT_PATH = os.path.join(HERE, "CR257b_PRECOMMIT.md")
PRECOMMIT_HASH = "3a3b301d45d4573845f6744f315ff4ef6278e9ece0ccf314724f109ee41c9fe7"
INPUT_PATH = os.path.join(HERE, "..", "CR253_PARTICLE_PROMOTER_80_ROW",
                          "CR253_promoted_80_rows.csv")
INPUT_HASH = "59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b"

R = 12
R2 = 144

C_PLUS = Fraction(5, 4)
C_MINUS = Fraction(3, 2)
A_NEG_COEF = Fraction(5, 6)
A_POS_COEF = Fraction(6, 5)

ABS_TOL = 1e-7


def file_sha256(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def verify_inputs():
    for path, locked in [(PRECOMMIT_PATH, PRECOMMIT_HASH),
                         (INPUT_PATH, INPUT_HASH)]:
        h = file_sha256(path)
        if h != locked:
            raise SystemExit(f"hash mismatch on {path}: got {h} want {locked}")


# ----------------------------------------------------------------------
# Law forms (bit-identical to CR257 v1 for E / A / D / W3)
# ----------------------------------------------------------------------

def matter_charged_qA(p, sign, d):
    c_s = C_PLUS if sign == "positive" else C_MINUS
    return Fraction(R) ** d * c_s * Fraction(p) * (Fraction(1) + Fraction(p, R2))


def anti_general(p, sign, d):
    """CR256 general A-operator form, evaluable at any depth."""
    qA_m = matter_charged_qA(p, sign, d)
    if sign == "negative":
        route = A_NEG_COEF * (Fraction(1) + Fraction(p, R ** (d + 1)))
    else:
        route = A_POS_COEF * (Fraction(1) - Fraction(p, R ** (d + 1)))
    return qA_m * route


def anti_d1_compact(p, sign, d):
    """d=1 substrate-natural compact forms (A meets Theta at R^2).
    Evaluable at ANY depth in the same algebraic form -- but the algebraic
    DERIVATION is valid only at d=1. Applying this at d != 1 is the
    depth-uniqueness wrong-control."""
    if sign == "negative":
        # R . (5/4) . p . (1 + p/R^2)^2
        return Fraction(R) * C_PLUS * Fraction(p) * (Fraction(1) + Fraction(p, R2)) ** 2
    else:
        # R . (3/2) . p . (1 - p^2/R^4)
        return Fraction(R) * C_MINUS * Fraction(p) * (
            Fraction(1) - Fraction(p * p, R2 * R2)
        )


def anti_d1_compact_sign_swap(p, sign, d):
    """W3: sign-swapped compact forms (neg gets diff-of-squares, pos gets squared)."""
    if sign == "negative":
        return Fraction(R) * C_PLUS * Fraction(p) * (
            Fraction(1) - Fraction(p * p, R2 * R2)
        )
    else:
        return Fraction(R) * C_MINUS * Fraction(p) * (Fraction(1) + Fraction(p, R2)) ** 2


# ----------------------------------------------------------------------
# W4 (CORRECTED): scope strictly to negative side at d=1
# ----------------------------------------------------------------------

def anti_d1_neg_power_variant(p, sign, d, power):
    """W4 corrected: power variant on the negative-side (1 + p/R^2) factor only.
    Returns None on positive side so the caller excludes positive rows from
    the count -- avoiding the CR257 v1 bug where the positive canonical form
    was unmodified and trivially matched at power=1."""
    if sign != "negative":
        return None
    return Fraction(R) * C_PLUS * Fraction(p) * (Fraction(1) + Fraction(p, R2)) ** power


def count_matches(rows, predict_fn):
    n = 0
    for r in rows:
        p = int(r["partition_signature"])
        sign = r["q_sign"]
        d = int(r["closure_depth"])
        actual = float(r["qA_source_support"])
        try:
            pred_val = predict_fn(p, sign, d)
        except (ZeroDivisionError, ValueError):
            continue
        if pred_val is None:
            continue  # row excluded from this control's scope
        pred = float(pred_val)
        if abs(actual - pred) < ABS_TOL:
            n += 1
    return n


def count_in_scope(rows, predict_fn):
    """Count how many rows the predict_fn does NOT return None for."""
    n = 0
    for r in rows:
        p = int(r["partition_signature"])
        sign = r["q_sign"]
        d = int(r["closure_depth"])
        try:
            v = predict_fn(p, sign, d)
        except (ZeroDivisionError, ValueError):
            continue
        if v is not None:
            n += 1
    return n


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():
    verify_inputs()
    print(f"CR257b -- A Meets Theta at d=1 (W4 correction re-run)")
    print(f"precommit  hash : {PRECOMMIT_HASH}")
    print(f"CR253 input hash: {INPUT_HASH}")
    print()

    rows = list(csv.DictReader(open(INPUT_PATH, "r", encoding="utf-8")))
    anti_charged = [r for r in rows
                    if r["bin"] == "antimatter_conjugate_rows"
                    and r["q_abs"] != "0"]
    anti_d1 = [r for r in anti_charged if r["closure_depth"] == "1"]
    anti_d0 = [r for r in anti_charged if r["closure_depth"] == "0"]

    print(f"Loaded {len(rows)} rows from CR253")
    print(f"  anti charged d=1: {len(anti_d1)} (expected 16)")
    print(f"  anti charged d=0: {len(anti_d0)} (expected 16) [used for D gate]")
    print()

    # ===== E gate: empirical match at d=1 =====
    print(f"E gate: compact forms vs catalog at d=1")
    print(f"  qA_anti(neg, p, 1) = R . (5/4) . p . (1 + p/R^2)^2")
    print(f"  qA_anti(pos, p, 1) = R . (3/2) . p . (1 - p^2/R^4)")
    print()
    print(f"  {'row_id':>13s} {'p':>3s} {'sign':>9s} "
          f"{'actual':>14s} {'compact':>14s} match")
    e_matches = 0
    residuals = []
    for r in anti_d1:
        p = int(r["partition_signature"])
        sign = r["q_sign"]
        d = int(r["closure_depth"])
        actual = float(r["qA_source_support"])
        pred = float(anti_d1_compact(p, sign, d))
        resid = abs(actual - pred)
        residuals.append(resid)
        match = "OK" if resid < ABS_TOL else "MISS"
        if resid < ABS_TOL:
            e_matches += 1
        print(f"  {r['row_id']:>13s} {p:>3d} {sign:>9s} "
              f"{actual:>14.7f} {pred:>14.7f} {match}")
    cond_E = (e_matches == len(anti_d1))
    print(f"\n  matches: {e_matches}/{len(anti_d1)}, "
          f"max residual: {max(residuals):.2e}")
    print(f"  (1) E gate: {'PASS' if cond_E else 'FAIL'}\n")

    # ===== A gate: algebraic equality of compact and general forms at d=1 =====
    print(f"A gate: Fraction-equality compact vs general form at d=1")
    a_equal = 0
    a_disagree = []
    for r in anti_d1:
        p = int(r["partition_signature"])
        sign = r["q_sign"]
        d = int(r["closure_depth"])
        gen = anti_general(p, sign, d)  # Fraction
        cmp = anti_d1_compact(p, sign, d)  # Fraction
        if gen == cmp:
            a_equal += 1
        else:
            a_disagree.append((r["row_id"], p, sign, str(gen), str(cmp)))
    cond_A = (a_equal == len(anti_d1))
    print(f"  bit-equivalent Fraction pairs: {a_equal}/{len(anti_d1)}")
    if a_disagree:
        for row_id, p, sign, g, c in a_disagree[:5]:
            print(f"    DISAGREE: {row_id} p={p} sign={sign} gen={g} cmp={c}")
    print(f"  (2) A gate: {'PASS' if cond_A else 'FAIL'}\n")

    # ===== D gate: compact forms FAIL at d=0 =====
    print(f"D gate: compact forms applied to d=0 antimatter rows must NOT match")
    d0_neg = [r for r in anti_d0 if r["q_sign"] == "negative"]
    d0_pos = [r for r in anti_d0 if r["q_sign"] == "positive"]
    d0_neg_matches = count_matches(d0_neg, anti_d1_compact)
    d0_pos_matches = count_matches(d0_pos, anti_d1_compact)
    print(f"  compact (neg) applied to d=0 neg rows: {d0_neg_matches}/{len(d0_neg)}")
    print(f"  compact (pos) applied to d=0 pos rows: {d0_pos_matches}/{len(d0_pos)}")
    cond_D = (d0_neg_matches == 0 and d0_pos_matches == 0)
    print(f"  (3) D gate: {'PASS' if cond_D else 'FAIL'}\n")

    # ===== W3: sign-swap of compact forms =====
    print(f"W3: sign-swap of compact forms at d=1")
    w3_matches = count_matches(anti_d1, anti_d1_compact_sign_swap)
    print(f"  sign-swap matches: {w3_matches}/{len(anti_d1)}")
    cond_W3 = (w3_matches <= 4)
    print(f"  (4) W3 <= 4/16: {'PASS' if cond_W3 else 'FAIL'}\n")

    # ===== W4 (CORRECTED): power variants on neg side at d=1 only =====
    print(f"W4: power variants on the neg-side squared factor (neg side only, per spec)")
    w4_results = {}
    neg_d1 = [r for r in anti_d1 if r["q_sign"] == "negative"]
    print(f"  scope: {len(neg_d1)} negative d=1 rows")
    for power in [1, 3]:
        m = count_matches(neg_d1,
                          lambda p, s, d, pw=power: anti_d1_neg_power_variant(p, s, d, pw))
        w4_results[f"power={power}"] = f"{m}/{len(neg_d1)}"
        print(f"  power={power}: {m}/{len(neg_d1)}")
    cond_W4 = all(int(v.split("/")[0]) == 0 for v in w4_results.values())
    print(f"  (5) W4 each variant = 0/{len(neg_d1)}: {'PASS' if cond_W4 else 'FAIL'}\n")

    # ===== Verdict =====
    all_pass = cond_E and cond_A and cond_D and cond_W3 and cond_W4
    if all_pass:
        verdict = "PASS"
    elif not cond_E:
        if e_matches >= len(anti_d1) - 2:
            verdict = "BOUNDARY"
        else:
            verdict = "FAIL"
    elif not cond_A:
        verdict = "FAIL"
    else:
        verdict = "BOUNDARY"

    print(f"Verdict conditions:")
    print(f"  (1) E gate empirical 16/16 at d=1:        {'PASS' if cond_E else 'FAIL'}")
    print(f"  (2) A gate Fraction equality at d=1:       {'PASS' if cond_A else 'FAIL'}")
    print(f"  (3) D gate compact forms FAIL at d=0:      {'PASS' if cond_D else 'FAIL'}")
    print(f"  (4) W3 sign-swap <= 4/16:                  {'PASS' if cond_W3 else 'FAIL'}")
    print(f"  (5) W4 neg-side power variants 0/8:        {'PASS' if cond_W4 else 'FAIL'}")
    print()
    print(f"CR257b VERDICT: {verdict}")
    print()

    # ===== Emit outputs =====
    per_row_csv = os.path.join(HERE, "CR257b_d1_predictions.csv")
    with open(per_row_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["row_id", "p", "sign", "d", "qA_actual", "qA_compact_form",
                    "qA_general_form", "compact_matches_actual",
                    "compact_equals_general_fraction"])
        for r in anti_d1:
            p = int(r["partition_signature"])
            sign = r["q_sign"]
            d = int(r["closure_depth"])
            actual = float(r["qA_source_support"])
            compact = anti_d1_compact(p, sign, d)
            general = anti_general(p, sign, d)
            w.writerow([r["row_id"], p, sign, d, actual,
                        float(compact), float(general),
                        abs(actual - float(compact)) < ABS_TOL,
                        compact == general])

    wc_csv = os.path.join(HERE, "CR257b_wrong_controls.csv")
    with open(wc_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["control", "variant", "matches", "of_N", "sensitive"])
        w.writerow(["D-neg", "compact_neg at d=0",
                    d0_neg_matches, len(d0_neg), d0_neg_matches == 0])
        w.writerow(["D-pos", "compact_pos at d=0",
                    d0_pos_matches, len(d0_pos), d0_pos_matches == 0])
        w.writerow(["W3", "sign-swap of compact forms at d=1",
                    w3_matches, len(anti_d1), w3_matches <= 4])
        for v, m_str in w4_results.items():
            m, n = m_str.split("/")
            w.writerow(["W4-neg-only", v, int(m), int(n), int(m) == 0])

    summary = {
        "artifact": "CR257b_A_MEETS_THETA_AT_D_1_W4_CORRECTION",
        "supersedes": "CR257_A_MEETS_THETA_AT_D_1 (W4 runner bug; BOUNDARY)",
        "verdict": verdict,
        "precommit_hash": PRECOMMIT_HASH,
        "input_hash": INPUT_HASH,
        "n_anti_d1": len(anti_d1),
        "n_anti_d0": len(anti_d0),
        "n_anti_d1_neg": len(neg_d1),
        "E_gate_matches": f"{e_matches}/{len(anti_d1)}",
        "E_gate_max_residual": max(residuals) if residuals else None,
        "A_gate_fraction_equal": f"{a_equal}/{len(anti_d1)}",
        "D_gate_d0_compact_matches": {
            "neg": f"{d0_neg_matches}/{len(d0_neg)}",
            "pos": f"{d0_pos_matches}/{len(d0_pos)}",
        },
        "wrong_controls": {
            "W3_sign_swap": f"{w3_matches}/{len(anti_d1)}",
            "W4_neg_side_power_variants": w4_results,
        },
        "verdict_conditions": {
            "E_empirical_16_16": cond_E,
            "A_algebraic_fraction_equality": cond_A,
            "D_depth_uniqueness": cond_D,
            "W3_sign_swap_le_4": cond_W3,
            "W4_neg_power_variants_zero": cond_W4,
        },
    }
    with open(os.path.join(HERE, "CR257b_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    runner_hash = file_sha256(__file__)
    print(f"runner SHA-256 : {runner_hash}")


if __name__ == "__main__":
    main()
