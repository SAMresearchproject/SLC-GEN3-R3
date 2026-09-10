"""
CR254 — Compact Matter Charged-Row Law.

Tests qA = R^d * c_s * p * (1 + p/R^2) on 32 matter charged rows
from CR253's sealed 80-row promoted surface.

precommit : 23b94d10bba93c4622b03dead10b8bfb4759649bf1056d5ae489734d3f679c2f
input     : 59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b
"""

import csv
import hashlib
import itertools
import json
import os
import random
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
PRECOMMIT_PATH = os.path.join(HERE, "CR254_PRECOMMIT.md")
PRECOMMIT_HASH = "23b94d10bba93c4622b03dead10b8bfb4759649bf1056d5ae489734d3f679c2f"
INPUT_PATH = os.path.join(HERE, "..", "CR253_PARTICLE_PROMOTER_80_ROW",
                          "CR253_promoted_80_rows.csv")
INPUT_HASH = "59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b"

# Substrate atoms (locked)
R = 12
R2 = 144
ALPHA_H = 2

# Canonical constants
C_PLUS = Fraction(5, 4)   # 1 + 1/alpha_H^2
C_MINUS = Fraction(3, 2)  # 1 + 1/alpha_H

ABS_TOL = 1e-7

# Substrate-natural rational pool for W1
RATIONAL_POOL = [Fraction(1, 1), Fraction(5, 4), Fraction(4, 3),
                 Fraction(3, 2), Fraction(5, 3), Fraction(7, 4),
                 Fraction(2, 1)]


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
# Canonical law
# ----------------------------------------------------------------------

def matter_charged_qA(p, sign, d, c_plus=C_PLUS, c_minus=C_MINUS):
    c_s = c_plus if sign == "positive" else c_minus
    return Fraction(R) ** d * c_s * Fraction(p) * (Fraction(1) + Fraction(p, R2))


def count_matches(rows, predict_fn):
    n_match = 0
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
            n_match += 1
    return n_match


# ----------------------------------------------------------------------
# Wrong-control variants
# ----------------------------------------------------------------------

def w2_dim_exponent(variant):
    """variant: 'R_d_minus_1', 'R_d_plus_1', 'd_plus_1_pow_d'"""
    def predict(p, sign, d):
        c_s = C_PLUS if sign == "positive" else C_MINUS
        if variant == "R_d_minus_1":
            factor = Fraction(R) ** (d - 1)  # R^-1 at d=0
        elif variant == "R_d_plus_1":
            factor = Fraction(R) ** (d + 1)
        elif variant == "d_plus_1_pow_d":
            factor = Fraction(d + 1) ** d
        else:
            raise ValueError(variant)
        return factor * c_s * Fraction(p) * (Fraction(1) + Fraction(p, R2))
    return predict


def w3_surface_scale(variant):
    """variant: '1_plus_p_over_R', '1_plus_p_over_R3', '1_plus_p_sq_over_R2', '1_minus_p_over_R2'"""
    def predict(p, sign, d):
        c_s = C_PLUS if sign == "positive" else C_MINUS
        if variant == "1_plus_p_over_R":
            surf = Fraction(1) + Fraction(p, R)
        elif variant == "1_plus_p_over_R3":
            surf = Fraction(1) + Fraction(p, R ** 3)
        elif variant == "1_plus_p_sq_over_R2":
            surf = Fraction(1) + Fraction(p * p, R2)
        elif variant == "1_minus_p_over_R2":
            surf = Fraction(1) - Fraction(p, R2)
        else:
            raise ValueError(variant)
        return Fraction(R) ** d * c_s * Fraction(p) * surf
    return predict


def w4_functional_form(variant):
    """variant: 'additive', 'no_p'"""
    def predict(p, sign, d):
        c_s = C_PLUS if sign == "positive" else C_MINUS
        if variant == "additive":
            return Fraction(R) ** d + c_s * Fraction(p) * (Fraction(1) + Fraction(p, R2))
        elif variant == "no_p":
            return Fraction(R) ** d * c_s * (Fraction(1) + Fraction(p, R2))
        else:
            raise ValueError(variant)
    return predict


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():
    verify_inputs()
    print(f"CR254 — Compact Matter Charged-Row Law")
    print(f"precommit  hash : {PRECOMMIT_HASH}")
    print(f"CR253 input hash: {INPUT_HASH}")
    print()

    rows = list(csv.DictReader(open(INPUT_PATH, "r", encoding="utf-8")))
    matter_charged = [r for r in rows
                      if r["bin"] == "stable_matter_rows" and r["q_abs"] != "0"]
    n = len(matter_charged)
    print(f"Loaded {len(rows)} rows from CR253; matter charged subset = {n} "
          f"(expected 32)")
    print()

    # ===== Canonical PASS check =====
    print("Canonical law qA = R^d * c_s * p * (1 + p/R^2):")
    print(f"  c_+ = {C_PLUS} (= 1 + 1/alpha_H^2 = 5/4)")
    print(f"  c_- = {C_MINUS} (= 1 + 1/alpha_H = 3/2)")
    print()
    canonical_matches = count_matches(matter_charged, matter_charged_qA)
    print(f"Canonical matches: {canonical_matches}/{n}")

    # Per-row table
    print(f"\n  {'row_id':>13s} {'p':>3s} {'sign':>9s} {'d':>2s} "
          f"{'actual':>14s} {'predicted':>14s} match")
    residuals = []
    for r in matter_charged:
        p = int(r["partition_signature"])
        sign = r["q_sign"]
        d = int(r["closure_depth"])
        actual = float(r["qA_source_support"])
        pred = float(matter_charged_qA(p, sign, d))
        residuals.append(abs(actual - pred))
        match = "OK" if abs(actual - pred) < ABS_TOL else "MISS"
        print(f"  {r['row_id']:>13s} {p:>3d} {sign:>9s} {d:>2d} "
              f"{actual:>14.7f} {pred:>14.7f} {match}")
    cond_1 = (canonical_matches == n)
    print(f"\n  max residual: {max(residuals):.2e}")
    print(f"  (1) all 32 rows match to abs_tol {ABS_TOL}: "
          f"{'PASS' if cond_1 else 'FAIL'}\n")

    # ===== W1: Rational pool (c_+, c_-) sweep =====
    print(f"W1: rational-pool (c_+, c_-) pair sweep")
    print(f"  pool = {[str(x) for x in RATIONAL_POOL]}")
    w1_pairs = []
    for cp in RATIONAL_POOL:
        for cm in RATIONAL_POOL:
            matches = count_matches(matter_charged,
                lambda p, s, d, cp=cp, cm=cm: matter_charged_qA(p, s, d, cp, cm))
            w1_pairs.append((cp, cm, matches))
    w1_full_match = [(cp, cm) for cp, cm, m in w1_pairs if m == n]
    w1_canonical_only = (len(w1_full_match) == 1
                        and w1_full_match[0] == (C_PLUS, C_MINUS))
    print(f"  pairs achieving 32/32: {len(w1_full_match)}")
    for cp, cm in w1_full_match:
        is_canon = "CANONICAL" if (cp, cm) == (C_PLUS, C_MINUS) else "OTHER"
        print(f"    (c_+={cp}, c_-={cm}) — {is_canon}")
    # Top-5 highest match counts among non-canonical
    non_canon = [(cp, cm, m) for cp, cm, m in w1_pairs
                 if (cp, cm) != (C_PLUS, C_MINUS)]
    non_canon.sort(key=lambda x: -x[2])
    print(f"  top 3 non-canonical pairs by match count:")
    for cp, cm, m in non_canon[:3]:
        print(f"    (c_+={cp}, c_-={cm}): {m}/{n}")
    cond_2 = w1_canonical_only
    print(f"  (2) W1: only canonical (5/4, 3/2) achieves 32/32: "
          f"{'PASS' if cond_2 else 'FAIL'}\n")

    # ===== W2: dimensional exponent variants =====
    print(f"W2: dimensional exponent variants")
    w2_results = {}
    for v in ["R_d_minus_1", "R_d_plus_1", "d_plus_1_pow_d"]:
        m = count_matches(matter_charged, w2_dim_exponent(v))
        w2_results[v] = m
        print(f"  {v}: {m}/{n}")
    cond_3 = all(m <= 16 for m in w2_results.values())
    print(f"  (3) W2: every variant <= 16/32: {'PASS' if cond_3 else 'FAIL'}\n")

    # ===== W3: surface scale variants =====
    print(f"W3: surface scale variants")
    w3_results = {}
    for v in ["1_plus_p_over_R", "1_plus_p_over_R3",
              "1_plus_p_sq_over_R2", "1_minus_p_over_R2"]:
        m = count_matches(matter_charged, w3_surface_scale(v))
        w3_results[v] = m
        print(f"  {v}: {m}/{n}")
    cond_4 = all(m <= 16 for m in w3_results.values())
    print(f"  (4) W3: every variant <= 16/32: {'PASS' if cond_4 else 'FAIL'}\n")

    # ===== W4: functional form variants =====
    print(f"W4: functional form variants")
    w4_results = {}
    for v in ["additive", "no_p"]:
        m = count_matches(matter_charged, w4_functional_form(v))
        w4_results[v] = m
        print(f"  {v}: {m}/{n}")
    cond_5 = all(m <= 4 for m in w4_results.values())
    print(f"  (5) W4: every variant <= 4/32: {'PASS' if cond_5 else 'FAIL'}\n")

    # ===== W5: continuous c_s null distribution =====
    print(f"W5: continuous random (c_+, c_-) from [1,2]^2, 1000 draws")
    rng = random.Random(20260628)
    n_full = 0
    n_max_match = 0
    for _ in range(1000):
        cp_r = rng.uniform(1.0, 2.0)
        cm_r = rng.uniform(1.0, 2.0)
        def predict(p, sign, d, cp=cp_r, cm=cm_r):
            c = cp if sign == "positive" else cm
            return R ** d * c * p * (1 + p / R2)
        m = sum(1 for r in matter_charged
                if abs(float(r["qA_source_support"]) -
                       predict(int(r["partition_signature"]),
                               r["q_sign"], int(r["closure_depth"]))) < 1e-6)
        if m == n:
            n_full += 1
        if m > n_max_match:
            n_max_match = m
    print(f"  draws achieving 32/32 matches: {n_full}/1000")
    print(f"  best random draw match count: {n_max_match}/32")
    cond_6 = (n_full == 0)
    print(f"  (6) W5: zero random draws reproduce 32/32: "
          f"{'PASS' if cond_6 else 'FAIL'}\n")

    # ===== Verdict =====
    all_pass = cond_1 and cond_2 and cond_3 and cond_4 and cond_5 and cond_6
    misses = n - canonical_matches
    if all_pass:
        verdict = "PASS"
    elif misses <= 2 and cond_1 is False and all([cond_2, cond_3, cond_4, cond_5, cond_6]):
        verdict = "BOUNDARY"
    elif misses <= 2 and cond_1:
        # cond_1 passes but a wrong-control gate barely missed
        verdict = "BOUNDARY"
    else:
        verdict = "FAIL"

    print(f"Verdict conditions:")
    print(f"  (1) canonical 32/32 exact:           {'PASS' if cond_1 else 'FAIL'}")
    print(f"  (2) W1 only canonical achieves 32/32: {'PASS' if cond_2 else 'FAIL'}")
    print(f"  (3) W2 each variant <= 16/32:         {'PASS' if cond_3 else 'FAIL'}")
    print(f"  (4) W3 each variant <= 16/32:         {'PASS' if cond_4 else 'FAIL'}")
    print(f"  (5) W4 each variant <= 4/32:          {'PASS' if cond_5 else 'FAIL'}")
    print(f"  (6) W5 0/1000 random reproduce 32/32: {'PASS' if cond_6 else 'FAIL'}")
    print()
    print(f"CR254 VERDICT: {verdict}")
    print()

    # ===== Emit outputs =====
    per_row_csv = os.path.join(HERE, "CR254_per_row_predictions.csv")
    with open(per_row_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["row_id", "p", "sign", "d", "qA_actual", "qA_predicted",
                    "residual", "match"])
        for r in matter_charged:
            p = int(r["partition_signature"])
            sign = r["q_sign"]
            d = int(r["closure_depth"])
            actual = float(r["qA_source_support"])
            pred = float(matter_charged_qA(p, sign, d))
            resid = abs(actual - pred)
            w.writerow([r["row_id"], p, sign, d, actual, pred, resid,
                        "OK" if resid < ABS_TOL else "MISS"])

    wc_csv = os.path.join(HERE, "CR254_wrong_controls.csv")
    with open(wc_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["control", "variant", "matches_out_of_32", "sensitive"])
        for cp, cm, m in w1_pairs:
            is_canon = (cp, cm) == (C_PLUS, C_MINUS)
            w.writerow(["W1", f"(c_+={cp}, c_-={cm}){' [CANON]' if is_canon else ''}",
                        m, "n/a"])
        for v, m in w2_results.items():
            w.writerow(["W2", v, m, m <= 16])
        for v, m in w3_results.items():
            w.writerow(["W3", v, m, m <= 16])
        for v, m in w4_results.items():
            w.writerow(["W4", v, m, m <= 4])
        w.writerow(["W5", "continuous [1,2]^2 random, 1000 draws",
                    f"{n_full}/1000 full, max={n_max_match}", n_full == 0])

    summary = {
        "artifact": "CR254_COMPACT_MATTER_CHARGED_LAW",
        "verdict": verdict,
        "precommit_hash": PRECOMMIT_HASH,
        "input_hash": INPUT_HASH,
        "n_matter_charged": n,
        "canonical_matches": canonical_matches,
        "max_residual": max(residuals),
        "wrong_controls": {
            "W1_rational_pool_pairs_full_match":
                [(str(cp), str(cm)) for cp, cm in w1_full_match],
            "W2_dim_exponent": w2_results,
            "W3_surface_scale": w3_results,
            "W4_functional_form": w4_results,
            "W5_continuous_full_matches": n_full,
            "W5_continuous_best_match_count": n_max_match,
        },
        "verdict_conditions": {
            "canonical_32_32": cond_1,
            "W1_canonical_unique": cond_2,
            "W2_all_le_16": cond_3,
            "W3_all_le_16": cond_4,
            "W4_all_le_4": cond_5,
            "W5_zero_full_match": cond_6,
        },
    }
    with open(os.path.join(HERE, "CR254_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    runner_hash = file_sha256(__file__)
    print(f"runner SHA-256 : {runner_hash}")


if __name__ == "__main__":
    main()
