"""Exploration — not CR work. Try multiple sign and counting rules against
the CR242 dataset and see what closes.

Loads CR242 binding dataset, applies several candidate (sign × counting × q)
combinations, and reports per-row residuals plus aggregate statistics.
Nothing is sealed; this is search-mode.
"""
from __future__ import annotations

import csv
from fractions import Fraction
from pathlib import Path

# Substrate atoms (all sealed upstream)
R = Fraction(12)
D = Fraction(3)
S = Fraction(8)
KAPPA = Fraction(7117, 768)
G = Fraction(1, 64)
ALPHA_H = Fraction(2)
THETA = Fraction(18)
F_PARTITION = Fraction(81)
V_PARTITION = Fraction(27)
R4 = R ** 4
MU_Q = Fraction(192, 7117)
MEV_PER_U = 931.494

# CR009-sealed lift values
Q_AU = Fraction(647)        # ℱ·S − 1 (Au-197 cascade)
Q_PLUS_D = lambda q: q + D
PAIR_LIFT_U = lambda q: float((Q_PLUS_D(q) / R4) * MU_Q)  # per-link in atomic mass units

# Dataset path
DATASET = Path(__file__).parent.parent / "CR242_SAM_BINDING_CURVATURE_DERIVATION" / "CR242_binding_dataset.csv"


def load() -> list[dict]:
    rows = []
    with DATASET.open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                Z = int(float(r["Z"]))
                N = int(float(r["N"]))
                A = int(float(r["A"]))
                B = float(r["B_u"])
            except (KeyError, ValueError):
                continue
            if N < Z:
                continue
            rows.append({
                "iso": r["isotope"],
                "Z": Z, "N": N, "A": A, "NmZ": N - Z,
                "B_obs_u": B,
                "B_obs_MeV": B * MEV_PER_U,
            })
    return rows


def sign_observed(row):
    """The actual observed sign — for measuring how well rules match."""
    return 1 if row["B_obs_u"] >= 0 else -1


def sign_rule_R1_naive(row):
    """Current R1: always +1."""
    return 1


def sign_rule_iron_peak_window(row):
    """Heuristic: positive for mid-A range, negative outside.
    Light (A < threshold_lo): negative_credit (matches qp091v anchor for deuteron/alpha).
    Mid (threshold_lo <= A < threshold_hi): positive_debit (iron peak region).
    Heavy actinides (A >= threshold_hi): negative_credit again.

    Thresholds picked from substrate constants:
      lo = R + D = 15  (just above N-15 boundary in observed data)
      hi = R^2 + Θ + R = 144 + 18 + 12 = 174  (just before Pt at A=190+)
    """
    if row["A"] < 16:
        return -1
    if row["A"] >= 210:  # actinides
        return -1
    return 1


def sign_rule_by_NmZ_over_A(row):
    """Sign based on neutron-excess ratio. Heuristic: high (N-Z)/A → credit.
    Threshold from Θ/R² = 18/144 = 1/8.
    """
    A = row["A"]
    if A == 0:
        return 1
    ratio = row["NmZ"] / A
    if ratio > Fraction(1, 8):  # threshold 0.125
        return -1
    if A < 16:
        return -1  # light nuclei also credit
    return 1


def count_NmZ(row):
    return row["NmZ"]


def count_A(row):
    return row["A"]


def count_Z(row):
    return row["Z"]


def count_pairs_ZN(row):
    return row["Z"] * row["N"]


def count_pairs_A_squared(row):
    A = row["A"]
    return A * (A - 1) // 2


def count_A_surface(row):
    """A^(2/3) surface count, rounded down."""
    A = row["A"]
    return int(round(A ** (2/3)))


def count_NmZ_squared_over_A(row):
    if row["A"] == 0:
        return 0
    return row["NmZ"] ** 2 / row["A"]


def predict(row, sign_rule, count_rule, q):
    per_link = PAIR_LIFT_U(q)
    n = count_rule(row)
    if not isinstance(n, (int, float)):
        n = float(n)
    magnitude_u = n * per_link
    sign = sign_rule(row)
    return sign * magnitude_u


def evaluate(rows, sign_rule, count_rule, q, label):
    deltas_u = []
    sign_hits = 0
    for r in rows:
        pred = predict(r, sign_rule, count_rule, q)
        obs = r["B_obs_u"]
        delta = obs - pred
        deltas_u.append(delta)
        if (pred >= 0) == (obs >= 0):
            sign_hits += 1
    n = len(rows)
    abs_MeV = [abs(d) * MEV_PER_U for d in deltas_u]
    return {
        "label": label,
        "n": n,
        "sign_hits": sign_hits,
        "sign_acc": sign_hits / n,
        "max_abs_MeV": max(abs_MeV),
        "mean_abs_MeV": sum(abs_MeV) / n,
        "rms_MeV": (sum(d * d for d in deltas_u) / n) ** 0.5 * MEV_PER_U,
    }


def main():
    rows = load()
    print(f"Loaded {len(rows)} N>=Z nuclei from CR242 dataset\n")
    print("="*100)
    print("PHASE 1: Sign-rule diagnostics with R1 magnitude (q=647, (N-Z) counting)")
    print("="*100)

    sign_rules = [
        ("R1_naive_always_positive", sign_rule_R1_naive),
        ("iron_peak_window", sign_rule_iron_peak_window),
        ("NmZ_over_A_threshold", sign_rule_by_NmZ_over_A),
    ]
    for name, rule in sign_rules:
        result = evaluate(rows, rule, count_NmZ, Q_AU, name)
        print(f"  {name:35s} sign_acc={result['sign_acc']:.3f}  max|Δ|={result['max_abs_MeV']:7.2f} MeV  RMS={result['rms_MeV']:6.2f} MeV")

    print()
    print("="*100)
    print("PHASE 2: Counting-rule diagnostics with sign=observed (perfect sign), q=647")
    print("="*100)
    print("  (Tests which counting rule best matches magnitude when sign is known)")

    count_rules = [
        ("NmZ_linear",          count_NmZ),
        ("A_linear",            count_A),
        ("Z_linear",            count_Z),
        ("Z_times_N_pairs",     count_pairs_ZN),
        ("A_squared_pairs",     count_pairs_A_squared),
        ("A_to_two_thirds",     count_A_surface),
        ("NmZ_squared_over_A",  count_NmZ_squared_over_A),
    ]
    for name, rule in count_rules:
        result = evaluate(rows, sign_observed, rule, Q_AU, name)
        print(f"  {name:25s} max|Δ|={result['max_abs_MeV']:7.2f} MeV  mean|Δ|={result['mean_abs_MeV']:6.2f} MeV  RMS={result['rms_MeV']:6.2f} MeV")

    print()
    print("="*100)
    print("PHASE 3: Per-row detail with iron-peak-window sign + linear (N-Z) count")
    print("="*100)
    print(f"  {'iso':>8} {'Z':>4} {'N':>4} {'A':>4} {'N-Z':>4} {'B_obs MeV':>11} {'B_pred MeV':>11} {'Δ MeV':>9} {'sign?':>6}")
    print("-"*100)
    for r in sorted(rows, key=lambda x: x["A"]):
        pred_u = predict(r, sign_rule_iron_peak_window, count_NmZ, Q_AU)
        delta_u = r["B_obs_u"] - pred_u
        sign_match = "✓" if (pred_u >= 0) == (r["B_obs_u"] >= 0) else "✗"
        print(f"  {r['iso']:>8} {r['Z']:4d} {r['N']:4d} {r['A']:4d} {r['NmZ']:4d} "
              f"{r['B_obs_MeV']:11.3f} {pred_u*MEV_PER_U:11.3f} {delta_u*MEV_PER_U:9.3f} {sign_match:>6}")

    print()
    print("="*100)
    print("PHASE 4: Back-solve per-row effective q under linear-(N-Z) with iron-peak sign")
    print("="*100)
    print("  (Asks: what q would each row need to close perfectly? Look for substrate constants.)")
    print(f"  {'iso':>8} {'A':>4} {'N-Z':>4} {'B_obs MeV':>11} {'eff q+D':>9} {'eff q':>8} {'q÷ℱ':>8} {'q÷R²':>8} {'q÷Θ':>8}")
    print("-"*100)
    for r in sorted(rows, key=lambda x: x["A"]):
        if r["NmZ"] == 0:
            continue
        sign = sign_rule_iron_peak_window(r)
        # B_obs = sign * NmZ * (eff_q+D)/R^4 * mu_Q
        # eff_q = abs(B_obs) * R^4 / (NmZ * mu_Q) - D
        signed_b_u = sign * r["B_obs_u"]
        eff_qpD = abs(r["B_obs_u"]) * float(R4) / (r["NmZ"] * float(MU_Q))
        eff_q = eff_qpD - float(D)
        F_ratio = eff_q / float(F_PARTITION)
        R2_ratio = eff_q / float(R * R)
        Theta_ratio = eff_q / float(THETA)
        print(f"  {r['iso']:>8} {r['A']:4d} {r['NmZ']:4d} {r['B_obs_MeV']:11.3f} {eff_qpD:9.1f} {eff_q:8.1f} {F_ratio:8.3f} {R2_ratio:8.3f} {Theta_ratio:8.3f}")


if __name__ == "__main__":
    main()
