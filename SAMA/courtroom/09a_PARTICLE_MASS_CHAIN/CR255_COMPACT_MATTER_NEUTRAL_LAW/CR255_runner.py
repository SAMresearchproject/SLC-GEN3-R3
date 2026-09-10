"""
CR255 — Compact Matter Neutral-Row Law.

Tests qA = (p/8) * R^d on 16 matter neutral rows from CR253's sealed
80-row promoted surface. The divisor 1/8 = Theta/R^2 = 2^(-D) is
substrate-derived; zero free parameters.

precommit : 567e4683112c245f065205ac98695bc15a03db0b7730782c59c8e6e4c214752a
input     : 59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b
"""

import csv
import hashlib
import json
import os
import random
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
PRECOMMIT_PATH = os.path.join(HERE, "CR255_PRECOMMIT.md")
PRECOMMIT_HASH = "567e4683112c245f065205ac98695bc15a03db0b7730782c59c8e6e4c214752a"
INPUT_PATH = os.path.join(HERE, "..", "CR253_PARTICLE_PROMOTER_80_ROW",
                          "CR253_promoted_80_rows.csv")
INPUT_HASH = "59647b850b7a1a99f6e992cf8644dfce99a394d2774b736f2cf92ab4a6e84f8b"

R = 12
R2 = 144
D = 3
ALPHA_H = 2
THETA = 18
F = 81

# Canonical divisor
CANONICAL_DIVISOR = Fraction(8)  # = 2^D, also = R^2 / Theta = 144 / 18

ABS_TOL = 1e-7

# Substrate-derivable divisor pool (W1) — excludes canonical 1/8
WRONG_DIVISOR_POOL = [
    Fraction(2), Fraction(3), Fraction(4), Fraction(6),
    Fraction(9), Fraction(12), Fraction(18), Fraction(24),
    Fraction(27), Fraction(36), Fraction(81), Fraction(144),
]


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

def neutral_qA(p, d, divisor=CANONICAL_DIVISOR):
    return Fraction(p, 1) / divisor * Fraction(R) ** d


def count_matches(rows, predict_fn):
    n_match = 0
    for r in rows:
        p = int(r["partition_signature"])
        d = int(r["closure_depth"])
        actual = float(r["qA_source_support"])
        try:
            pred = float(predict_fn(p, d))
        except (ZeroDivisionError, ValueError):
            continue
        if abs(actual - pred) < ABS_TOL:
            n_match += 1
    return n_match


# ----------------------------------------------------------------------
# Wrong-control variants
# ----------------------------------------------------------------------

def w2_dim_exponent(variant):
    def predict(p, d):
        if variant == "R_d_minus_1":
            factor = Fraction(R) ** (d - 1)
        elif variant == "R_d_plus_1":
            factor = Fraction(R) ** (d + 1)
        elif variant == "R_2d":
            factor = Fraction(R) ** (2 * d)
        elif variant == "d_plus_1_pow_d":
            factor = Fraction(d + 1) ** d
        else:
            raise ValueError(variant)
        return Fraction(p, 1) / CANONICAL_DIVISOR * factor
    return predict


def w3_p_dependence(variant):
    def predict(p, d):
        if variant == "p_squared":
            base = Fraction(p * p, 1)
        elif variant == "p_times_D":
            base = Fraction(p * D, 1)
        elif variant == "constant_p_mean":
            # Mean of {1,2,3,4,6,8,9,12} = 45/8 = 5.625
            base = Fraction(45, 8)
        elif variant == "sqrt_p_times_sqrt_p":
            # Trivially equal to p — sanity check
            base = Fraction(p, 1)
        else:
            raise ValueError(variant)
        return base / CANONICAL_DIVISOR * Fraction(R) ** d
    return predict


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():
    verify_inputs()
    print(f"CR255 — Compact Matter Neutral-Row Law")
    print(f"precommit  hash : {PRECOMMIT_HASH}")
    print(f"CR253 input hash: {INPUT_HASH}")
    print()

    rows = list(csv.DictReader(open(INPUT_PATH, "r", encoding="utf-8")))
    matter_neutral = [r for r in rows
                      if r["bin"] == "stable_matter_rows" and r["q_abs"] == "0"]
    n = len(matter_neutral)
    print(f"Loaded {len(rows)} rows from CR253; matter neutral subset = {n} "
          f"(expected 16)")
    print()

    # ===== Canonical PASS check =====
    print("Canonical law qA = (p / 8) * R^d:")
    print(f"  divisor 8 = 2^D = Theta/R^2 inverse = R^2/Theta = {R2 // THETA}")
    print(f"  tensor share 1/8 derives from Section 9.1 (zero free parameters)")
    print()
    canonical_matches = count_matches(matter_neutral, neutral_qA)
    print(f"Canonical matches: {canonical_matches}/{n}")
    print(f"\n  {'row_id':>13s} {'p':>3s} {'d':>2s} "
          f"{'actual':>10s} {'predicted':>10s} match")
    residuals = []
    for r in matter_neutral:
        p = int(r["partition_signature"])
        d = int(r["closure_depth"])
        actual = float(r["qA_source_support"])
        pred = float(neutral_qA(p, d))
        residuals.append(abs(actual - pred))
        match = "OK" if abs(actual - pred) < ABS_TOL else "MISS"
        print(f"  {r['row_id']:>13s} {p:>3d} {d:>2d} "
              f"{actual:>10.6f} {pred:>10.6f} {match}")
    cond_1 = (canonical_matches == n)
    print(f"\n  max residual: {max(residuals):.2e}")
    print(f"  (1) all 16 rows match to abs_tol {ABS_TOL}: "
          f"{'PASS' if cond_1 else 'FAIL'}\n")

    # ===== W1: divisor pool sweep =====
    print(f"W1: substrate-derivable wrong-divisor pool sweep")
    print(f"  pool (canonical 8 NOT in this set): "
          f"{[str(x) for x in WRONG_DIVISOR_POOL]}")
    w1_results = []
    for div in WRONG_DIVISOR_POOL:
        m = count_matches(matter_neutral,
                          lambda p, d, div=div: neutral_qA(p, d, divisor=div))
        w1_results.append((div, m))
    w1_full_match = [d for d, m in w1_results if m == n]
    print(f"  divisors achieving 16/16: {len(w1_full_match)}")
    for d in w1_full_match:
        print(f"    divisor = {d}")
    w1_top = sorted(w1_results, key=lambda x: -x[1])[:3]
    print(f"  top 3 wrong divisors by match count:")
    for div, m in w1_top:
        print(f"    divisor = {div}: {m}/{n}")
    cond_2 = (len(w1_full_match) == 0)
    print(f"  (2) W1: zero non-canonical divisors achieve 16/16: "
          f"{'PASS' if cond_2 else 'FAIL'}\n")

    # ===== W2: dimensional exponent variants =====
    print(f"W2: dimensional exponent variants")
    w2_results = {}
    for v in ["R_d_minus_1", "R_d_plus_1", "R_2d", "d_plus_1_pow_d"]:
        m = count_matches(matter_neutral, w2_dim_exponent(v))
        w2_results[v] = m
        print(f"  {v}: {m}/{n}")
    cond_3 = all(m <= 8 for m in w2_results.values())
    print(f"  (3) W2: every variant <= 8/16: {'PASS' if cond_3 else 'FAIL'}\n")

    # ===== W3: p-dependence variants =====
    print(f"W3: p-dependence variants")
    w3_results = {}
    for v in ["p_squared", "p_times_D", "constant_p_mean", "sqrt_p_times_sqrt_p"]:
        m = count_matches(matter_neutral, w3_p_dependence(v))
        w3_results[v] = m
        print(f"  {v}: {m}/{n}")
    # sqrt_p_times_sqrt_p is trivially canonical — expected 16/16, exempt
    sqrt_p_count = w3_results["sqrt_p_times_sqrt_p"]
    non_sanity = {k: v for k, v in w3_results.items() if k != "sqrt_p_times_sqrt_p"}
    cond_4 = all(m <= 8 for m in non_sanity.values())
    print(f"  (sqrt_p variant is trivially canonical; exempt from gate)")
    print(f"  (4) W3: non-sanity variants each <= 8/16: "
          f"{'PASS' if cond_4 else 'FAIL'}\n")

    # ===== W4: continuous random divisor =====
    print(f"W4: continuous random divisor from Uniform(2, 50), 1000 draws")
    rng = random.Random(20260628)
    n_full = 0
    n_max_match = 0
    for _ in range(1000):
        delta = rng.uniform(2.0, 50.0)
        def predict(p, d, delta=delta):
            return p / delta * R ** d
        m = sum(1 for r in matter_neutral
                if abs(float(r["qA_source_support"]) -
                       predict(int(r["partition_signature"]),
                               int(r["closure_depth"]))) < 1e-6)
        if m == n:
            n_full += 1
        if m > n_max_match:
            n_max_match = m
    print(f"  draws achieving 16/16 matches: {n_full}/1000")
    print(f"  best random draw match count: {n_max_match}/16")
    cond_5 = (n_full == 0)
    print(f"  (5) W4: zero random draws reproduce 16/16: "
          f"{'PASS' if cond_5 else 'FAIL'}\n")

    # ===== Verdict =====
    all_pass = cond_1 and cond_2 and cond_3 and cond_4 and cond_5
    misses = n - canonical_matches
    if all_pass:
        verdict = "PASS"
    elif misses <= 2 and cond_2 and cond_3 and cond_4 and cond_5:
        verdict = "BOUNDARY"
    else:
        verdict = "FAIL"

    print(f"Verdict conditions:")
    print(f"  (1) canonical 16/16 exact:           {'PASS' if cond_1 else 'FAIL'}")
    print(f"  (2) W1 zero non-canon full matches:  {'PASS' if cond_2 else 'FAIL'}")
    print(f"  (3) W2 each variant <= 8/16:         {'PASS' if cond_3 else 'FAIL'}")
    print(f"  (4) W3 non-sanity each <= 8/16:      {'PASS' if cond_4 else 'FAIL'}")
    print(f"  (5) W4 0/1000 random reproduce 16/16:{'PASS' if cond_5 else 'FAIL'}")
    print()
    print(f"CR255 VERDICT: {verdict}")
    print()

    # ===== Emit outputs =====
    per_row_csv = os.path.join(HERE, "CR255_per_row_predictions.csv")
    with open(per_row_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["row_id", "p", "d", "qA_actual", "qA_predicted",
                    "residual", "match"])
        for r in matter_neutral:
            p = int(r["partition_signature"])
            d = int(r["closure_depth"])
            actual = float(r["qA_source_support"])
            pred = float(neutral_qA(p, d))
            resid = abs(actual - pred)
            w.writerow([r["row_id"], p, d, actual, pred, resid,
                        "OK" if resid < ABS_TOL else "MISS"])

    wc_csv = os.path.join(HERE, "CR255_wrong_controls.csv")
    with open(wc_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["control", "variant", "matches_out_of_16", "sensitive"])
        for div, m in w1_results:
            w.writerow(["W1", f"divisor={div}", m, m < n])
        for v, m in w2_results.items():
            w.writerow(["W2", v, m, m <= 8])
        for v, m in w3_results.items():
            w.writerow(["W3", v, m, m <= 8 or v == "sqrt_p_times_sqrt_p"])
        w.writerow(["W4", "continuous random divisor (Uniform[2,50], 1000 draws)",
                    f"{n_full}/1000 full, max={n_max_match}", n_full == 0])

    summary = {
        "artifact": "CR255_COMPACT_MATTER_NEUTRAL_LAW",
        "verdict": verdict,
        "precommit_hash": PRECOMMIT_HASH,
        "input_hash": INPUT_HASH,
        "n_matter_neutral": n,
        "canonical_matches": canonical_matches,
        "max_residual": max(residuals),
        "wrong_controls": {
            "W1_divisor_pool_full_matches": [str(d) for d in w1_full_match],
            "W2_dim_exponent": w2_results,
            "W3_p_dependence": w3_results,
            "W4_continuous_full_matches": n_full,
            "W4_continuous_best_match_count": n_max_match,
        },
        "verdict_conditions": {
            "canonical_16_16": cond_1,
            "W1_no_non_canon_full_match": cond_2,
            "W2_all_le_8": cond_3,
            "W3_non_sanity_le_8": cond_4,
            "W4_zero_full_match": cond_5,
        },
    }
    with open(os.path.join(HERE, "CR255_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    runner_hash = file_sha256(__file__)
    print(f"runner SHA-256 : {runner_hash}")


if __name__ == "__main__":
    main()
