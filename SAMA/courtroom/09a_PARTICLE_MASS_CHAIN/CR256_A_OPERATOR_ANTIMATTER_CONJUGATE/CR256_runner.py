"""
CR256 — A-Operator Antimatter Conjugate Transform.

Tests qA_anti = qA_matter * A_conjugate(sign, p, d) on 32 antimatter
charged rows from CR253's sealed 80-row promoted surface, with the
A_conjugate route-scale correction at R^(d+1) and the load-bearing
single-row hard-zero prediction at QP093A-0088 (p=12, d=0, pos) -> qA=0.

precommit : 25654e6e3f1e3863f096e997326eaf3036cd5c9b2cb0436ed83f651c37a0b382
input     : 59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b
"""

import csv
import hashlib
import json
import os
import random
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
PRECOMMIT_PATH = os.path.join(HERE, "CR256_PRECOMMIT.md")
PRECOMMIT_HASH = "25654e6e3f1e3863f096e997326eaf3036cd5c9b2cb0436ed83f651c37a0b382"
INPUT_PATH = os.path.join(HERE, "..", "CR253_PARTICLE_PROMOTER_80_ROW",
                          "CR253_promoted_80_rows.csv")
INPUT_HASH = "59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b"

# Substrate atoms (locked)
R = 12
R2 = 144

# Matter law constants (from CR254)
C_PLUS = Fraction(5, 4)
C_MINUS = Fraction(3, 2)

# A-operator route coefficients (canonical)
A_NEG_COEF = Fraction(5, 6)
A_POS_COEF = Fraction(6, 5)

ABS_TOL = 1e-7
HARD_ZERO_TOL = 1e-9
HARD_ZERO_ROW_ID = "QP093A-0088"


def file_sha256(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def verify_inputs():
    for path, locked in [(PRECOMMIT_PATH, PRECOMMIT_HASH),
                         (INPUT_PATH, INPUT_HASH)]:
        h = file_sha256(path)
        if h != locked:
            raise SystemExit(f"hash mismatch on {path}:\n  got    {h}\n  locked {locked}")


# ----------------------------------------------------------------------
# Canonical laws
# ----------------------------------------------------------------------

def matter_charged_qA(p, sign, d):
    c_s = C_PLUS if sign == "positive" else C_MINUS
    return Fraction(R) ** d * c_s * Fraction(p) * (Fraction(1) + Fraction(p, R2))


def anti_qA(p, sign, d, R_exp_d=None, neg_coef=A_NEG_COEF, pos_coef=A_POS_COEF):
    """qA_anti = qA_matter * A_conjugate(sign, p, d)
    A_conjugate(neg) = neg_coef * (1 + p / R_exp_d)
    A_conjugate(pos) = pos_coef * (1 - p / R_exp_d)
    R_exp_d defaults to R^(d+1) (canonical).
    """
    qA_m = matter_charged_qA(p, sign, d)
    if R_exp_d is None:
        R_exp_d = R ** (d + 1)
    if sign == "negative":
        route = neg_coef * (Fraction(1) + Fraction(p, R_exp_d))
    else:
        route = pos_coef * (Fraction(1) - Fraction(p, R_exp_d))
    return qA_m * route


def count_matches(rows, predict_fn):
    n = 0
    for r in rows:
        p = int(r["partition_signature"])
        sign = r["q_sign"]
        d = int(r["closure_depth"])
        actual = float(r["qA_source_support"])
        try:
            pred = float(predict_fn(p, sign, d))
        except (ZeroDivisionError, ValueError):
            continue
        if abs(actual - pred) < ABS_TOL:
            n += 1
    return n


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():
    verify_inputs()
    print(f"CR256 - A-Operator Antimatter Conjugate Transform")
    print(f"precommit  hash : {PRECOMMIT_HASH}")
    print(f"CR253 input hash: {INPUT_HASH}")
    print()

    rows = list(csv.DictReader(open(INPUT_PATH, "r", encoding="utf-8")))
    anti_charged = [r for r in rows
                    if r["bin"] == "antimatter_conjugate_rows" and r["q_abs"] != "0"]
    n = len(anti_charged)
    print(f"Loaded {len(rows)} rows from CR253; anti charged subset = {n} "
          f"(expected 32)")
    print()

    # ===== Canonical law =====
    print(f"Canonical A-operator law:")
    print(f"  qA_anti = qA_matter(p, sign, d) * A_conjugate(sign, p, d)")
    print(f"  A_conjugate(neg, p, d) = (5/6)(1 + p/R^(d+1))")
    print(f"  A_conjugate(pos, p, d) = (6/5)(1 - p/R^(d+1))")
    print(f"  At d=0: R^(d+1) = R   = 12")
    print(f"  At d=1: R^(d+1) = R^2 = 144")
    print()

    canonical_matches = count_matches(anti_charged, anti_qA)
    print(f"Canonical matches: {canonical_matches}/{n}")
    print(f"\n  {'row_id':>13s} {'p':>3s} {'sign':>9s} {'d':>2s} "
          f"{'actual':>14s} {'predicted':>14s} match")
    residuals = []
    for r in anti_charged:
        p = int(r["partition_signature"])
        sign = r["q_sign"]
        d = int(r["closure_depth"])
        actual = float(r["qA_source_support"])
        pred = float(anti_qA(p, sign, d))
        resid = abs(actual - pred)
        residuals.append(resid)
        match = "OK" if resid < ABS_TOL else "MISS"
        print(f"  {r['row_id']:>13s} {p:>3d} {sign:>9s} {d:>2d} "
              f"{actual:>14.7f} {pred:>14.7f} {match}")
    cond_1 = (canonical_matches == n)
    print(f"\n  max residual: {max(residuals):.2e}")
    print(f"  (1) all 32 rows match to abs_tol {ABS_TOL}: "
          f"{'PASS' if cond_1 else 'FAIL'}\n")

    # ===== HARD-ZERO SUB-GATE =====
    print(f"HARD-ZERO SUB-GATE: {HARD_ZERO_ROW_ID} expected qA = 0.0 exactly")
    hard_zero_row = next((r for r in anti_charged
                         if r["row_id"] == HARD_ZERO_ROW_ID), None)
    if hard_zero_row is None:
        print(f"  *** {HARD_ZERO_ROW_ID} NOT FOUND in anti charged subset ***")
        cond_2 = False
    else:
        actual_qA = float(hard_zero_row["qA_source_support"])
        print(f"  row found: p={hard_zero_row['partition_signature']}, "
              f"d={hard_zero_row['closure_depth']}, "
              f"sign={hard_zero_row['q_sign']}")
        print(f"  actual qA = {actual_qA}")
        print(f"  hard-zero pass tol = {HARD_ZERO_TOL}")
        cond_2 = abs(actual_qA - 0.0) < HARD_ZERO_TOL
        print(f"  (2) HARD-ZERO sub-gate: {'PASS' if cond_2 else 'FAIL'}")
    print()

    # ===== W1: wrong R^(d+1) exponent =====
    print(f"W1: wrong R^(d+1) exponent variants")
    w1_results = {}
    for variant_name, exp_fn in [
        ("R^d (depth-independent)", lambda d: R ** d),
        ("R^(d+2)", lambda d: R ** (d + 2)),
        # R^(d-1): only well-defined for d >= 1; for d=0 use 1 (limit)
        ("R^(d-1) clamped", lambda d: R ** max(d - 1, 0)),
    ]:
        def predict_factory(exp_fn=exp_fn):
            return lambda p, sign, d: anti_qA(p, sign, d, R_exp_d=exp_fn(d))
        m = count_matches(anti_charged, predict_factory())
        w1_results[variant_name] = m
        print(f"  {variant_name}: {m}/{n}")
    cond_3 = all(m <= 16 for m in w1_results.values())
    print(f"  (3) W1: every variant <= 16/32: {'PASS' if cond_3 else 'FAIL'}\n")

    # ===== W2: wrong route coefficient pair =====
    print(f"W2: wrong route coefficient pair variants")
    w2_results = {}
    for variant_name, (nc, pc) in [
        ("(1, 1) no conjugation", (Fraction(1), Fraction(1))),
        ("(6/5, 5/6) swapped", (Fraction(6, 5), Fraction(5, 6))),
        ("(7/8, 8/7) off-substrate", (Fraction(7, 8), Fraction(8, 7))),
    ]:
        def predict_factory(nc=nc, pc=pc):
            return lambda p, sign, d: anti_qA(p, sign, d,
                                              neg_coef=nc, pos_coef=pc)
        m = count_matches(anti_charged, predict_factory())
        w2_results[variant_name] = m
        print(f"  {variant_name}: {m}/{n}")
    cond_4 = all(m <= 16 for m in w2_results.values())
    print(f"  (4) W2: every variant <= 16/32: {'PASS' if cond_4 else 'FAIL'}\n")

    # ===== W3: sign-swap convention =====
    print(f"W3: sign-swap convention "
          f"(neg uses (1 - p/R^(d+1)), pos uses (1 + p/R^(d+1)))")
    def sign_swap_predict(p, sign, d):
        qA_m = matter_charged_qA(p, sign, d)
        R_exp_d = R ** (d + 1)
        if sign == "negative":
            route = A_NEG_COEF * (Fraction(1) - Fraction(p, R_exp_d))
        else:
            route = A_POS_COEF * (Fraction(1) + Fraction(p, R_exp_d))
        return qA_m * route
    w3_matches = count_matches(anti_charged, sign_swap_predict)
    print(f"  sign-swap variant: {w3_matches}/{n}")
    # Hard-zero check under sign swap: should NOT be zero
    if hard_zero_row is not None:
        p_hz = int(hard_zero_row["partition_signature"])
        d_hz = int(hard_zero_row["closure_depth"])
        sign_hz = hard_zero_row["q_sign"]
        actual_hz = float(hard_zero_row["qA_source_support"])
        pred_hz_swap = float(sign_swap_predict(p_hz, sign_hz, d_hz))
        print(f"  under sign-swap, hard-zero row predicted = {pred_hz_swap}")
        print(f"    (canonical predicts 0; swap gives non-zero)")
        sign_swap_kills_zero = abs(pred_hz_swap) > 1e-3
    else:
        sign_swap_kills_zero = False
    cond_5 = (w3_matches <= 16 and sign_swap_kills_zero)
    print(f"  (5) W3: sign-swap <= 16/32 AND kills hard-zero: "
          f"{'PASS' if cond_5 else 'FAIL'}\n")

    # ===== W4: continuous random draws =====
    print(f"W4: continuous random (c_neg, c_pos, R_exp) draws, 1000 trials")
    rng = random.Random(20260628)
    n_full = 0
    n_max_match = 0
    for _ in range(1000):
        c_neg_r = rng.uniform(0.5, 1.5)
        c_pos_r = rng.uniform(0.5, 2.0)
        R_choice = rng.choice([12, 144, 1728])  # R, R^2, R^3
        def predict_random(p, sign, d, cn=c_neg_r, cp=c_pos_r, Re=R_choice):
            qA_m = R ** d * (5/4 if sign == "positive" else 3/2) * p * (1 + p/R2)
            if sign == "negative":
                route = cn * (1 + p / Re)
            else:
                route = cp * (1 - p / Re)
            return qA_m * route
        m = sum(1 for r in anti_charged
                if abs(float(r["qA_source_support"]) -
                       predict_random(int(r["partition_signature"]),
                                      r["q_sign"],
                                      int(r["closure_depth"]))) < 1e-6)
        if m == n:
            n_full += 1
        if m > n_max_match:
            n_max_match = m
    print(f"  draws achieving 32/32 matches: {n_full}/1000")
    print(f"  best random draw match count: {n_max_match}/32")
    cond_6 = (n_full == 0)
    print(f"  (6) W4: zero random draws reproduce 32/32: "
          f"{'PASS' if cond_6 else 'FAIL'}\n")

    # ===== Verdict =====
    all_pass = (cond_1 and cond_2 and cond_3 and cond_4 and cond_5 and cond_6)
    misses = n - canonical_matches
    if all_pass:
        verdict = "PASS"
    elif not cond_2:
        # Hard-zero failure is a single-row falsification per precommit
        verdict = "FAIL"
    elif cond_1 and not all_pass and misses == 0:
        verdict = "BOUNDARY"
    elif misses <= 2:
        verdict = "BOUNDARY"
    else:
        verdict = "FAIL"

    print(f"Verdict conditions:")
    print(f"  (1) canonical 32/32 exact:           {'PASS' if cond_1 else 'FAIL'}")
    print(f"  (2) HARD-ZERO sub-gate:              {'PASS' if cond_2 else 'FAIL'}")
    print(f"  (3) W1 wrong-exponent <= 16/32:      {'PASS' if cond_3 else 'FAIL'}")
    print(f"  (4) W2 wrong-coefs <= 16/32:         {'PASS' if cond_4 else 'FAIL'}")
    print(f"  (5) W3 sign-swap <= 16 + kills zero: {'PASS' if cond_5 else 'FAIL'}")
    print(f"  (6) W4 0/1000 random full match:     {'PASS' if cond_6 else 'FAIL'}")
    print()
    print(f"CR256 VERDICT: {verdict}")
    print()

    # ===== Emit outputs =====
    per_row_csv = os.path.join(HERE, "CR256_per_row_predictions.csv")
    with open(per_row_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["row_id", "p", "sign", "d", "qA_actual", "qA_predicted",
                    "residual", "match", "is_hard_zero_row"])
        for r in anti_charged:
            p = int(r["partition_signature"])
            sign = r["q_sign"]
            d = int(r["closure_depth"])
            actual = float(r["qA_source_support"])
            pred = float(anti_qA(p, sign, d))
            resid = abs(actual - pred)
            w.writerow([r["row_id"], p, sign, d, actual, pred, resid,
                        "OK" if resid < ABS_TOL else "MISS",
                        r["row_id"] == HARD_ZERO_ROW_ID])

    wc_csv = os.path.join(HERE, "CR256_wrong_controls.csv")
    with open(wc_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["control", "variant", "matches_out_of_32", "sensitive"])
        for v, m in w1_results.items():
            w.writerow(["W1", v, m, m <= 16])
        for v, m in w2_results.items():
            w.writerow(["W2", v, m, m <= 16])
        w.writerow(["W3", "sign-swap convention", w3_matches, w3_matches <= 16])
        w.writerow(["W3-hz", "sign-swap predicts hard-zero row as non-zero",
                    pred_hz_swap if hard_zero_row else "n/a",
                    sign_swap_kills_zero])
        w.writerow(["W4", "continuous random (c_neg, c_pos, R_exp), 1000 draws",
                    f"{n_full}/1000 full, max={n_max_match}", n_full == 0])

    summary = {
        "artifact": "CR256_A_OPERATOR_ANTIMATTER_CONJUGATE",
        "verdict": verdict,
        "precommit_hash": PRECOMMIT_HASH,
        "input_hash": INPUT_HASH,
        "n_anti_charged": n,
        "canonical_matches": canonical_matches,
        "max_residual": max(residuals),
        "hard_zero_row": HARD_ZERO_ROW_ID,
        "hard_zero_actual_qA": (float(hard_zero_row["qA_source_support"])
                                 if hard_zero_row else None),
        "hard_zero_passed": cond_2,
        "wrong_controls": {
            "W1_wrong_exponent": w1_results,
            "W2_wrong_coefs": w2_results,
            "W3_sign_swap_matches": w3_matches,
            "W3_sign_swap_predicts_hard_zero_as": (pred_hz_swap if hard_zero_row else None),
            "W4_continuous_full_matches": n_full,
            "W4_continuous_best_match_count": n_max_match,
        },
        "verdict_conditions": {
            "canonical_32_32": cond_1,
            "hard_zero_sub_gate": cond_2,
            "W1_le_16": cond_3,
            "W2_le_16": cond_4,
            "W3_le_16_and_kills_zero": cond_5,
            "W4_zero_full_match": cond_6,
        },
    }
    with open(os.path.join(HERE, "CR256_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    runner_hash = file_sha256(__file__)
    print(f"runner SHA-256 : {runner_hash}")


if __name__ == "__main__":
    main()
