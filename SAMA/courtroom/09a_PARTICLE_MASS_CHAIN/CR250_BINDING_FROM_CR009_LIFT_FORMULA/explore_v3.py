"""Exploration v3 — three-term search adding Coulomb-like term.

Builds on v2 finding:
  Best two-term: Z·per_link(647) + A^(2/3)·per_link(162)
    sign 100%, max|Δ| 53.25 MeV, RMS 28.47 MeV

Adds: -Z(Z-1)/A^(1/3)·per_link(q_Coul) term — searches q_Coul over substrate constants.
Also tests both signs (+/-) for the Coulomb term to let the search find the right direction.
"""
from __future__ import annotations

import csv
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 50

# Substrate atoms
R = Fraction(12)
D = Fraction(3)
S = Fraction(8)
ALPHA_H = Fraction(2)
THETA = Fraction(18)
F = Fraction(81)
V = Fraction(27)
M_CONST = Fraction(126)
L_CONST = Fraction(162)
KAPPA = Fraction(7117, 768)
G = Fraction(1, 64)
R4 = R ** 4
MU_Q = Fraction(192, 7117)

# CR245-derived asymmetry coefficient (per-link in Q-units = 7093²/(192·7117))
# The actual q value for asymmetry needs to be derived; here I expose it for search.

U_TO_MEV = Decimal("931.49410242")
DATASET = Path(__file__).parent.parent / "CR242_SAM_BINDING_CURVATURE_DERIVATION" / "CR242_binding_dataset.csv"


def frac_to_dec(f): return Decimal(f.numerator) / Decimal(f.denominator)
def u_to_mev(u): return u * U_TO_MEV


def per_link_u(q):
    return frac_to_dec((q + D) / R4 * MU_Q)


def load():
    rows = []
    with DATASET.open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                Z = int(float(r["Z"]))
                N = int(float(r["N"]))
                A = int(float(r["A"]))
                B_dec = Decimal(r["B_u"].strip())
            except (KeyError, ValueError):
                continue
            if N < Z:
                continue
            A_dec = Decimal(A)
            rows.append({
                "iso": r["isotope"],
                "Z": Z, "N": N, "A": A, "NmZ": N - Z,
                "B_obs_u": B_dec,
                "B_obs_MeV": B_dec * U_TO_MEV,
                "A_two_thirds": A_dec ** (Decimal(2) / Decimal(3)),
                "A_one_third": A_dec ** (Decimal(1) / Decimal(3)),
                "Z_term":       Decimal(Z),
                "Coul_count":   Decimal(Z * (Z - 1)) / (A_dec ** (Decimal(1) / Decimal(3))) if A > 0 else Decimal(0),
                "Asym_count":   Decimal((N - Z) ** 2) / A_dec if A > 0 else Decimal(0),
            })
    return rows


def sign_iron_peak_window(row):
    if row["A"] < 16: return Decimal(-1)
    if row["A"] >= 210: return Decimal(-1)
    return Decimal(1)


def predict_three_term(row, q_Z, q_A23, q_Coul, coul_sign):
    sign = sign_iron_peak_window(row)
    z_term = row["Z_term"] * per_link_u(q_Z)
    surf_term = row["A_two_thirds"] * per_link_u(q_A23)
    coul_term = coul_sign * row["Coul_count"] * per_link_u(q_Coul)
    return sign * (z_term + surf_term + coul_term)


def predict_four_term(row, q_Z, q_A23, q_Coul, coul_sign, q_Asym, asym_sign):
    sign = sign_iron_peak_window(row)
    z_term = row["Z_term"] * per_link_u(q_Z)
    surf_term = row["A_two_thirds"] * per_link_u(q_A23)
    coul_term = coul_sign * row["Coul_count"] * per_link_u(q_Coul)
    asym_term = asym_sign * row["Asym_count"] * per_link_u(q_Asym)
    return sign * (z_term + surf_term + coul_term + asym_term)


def evaluate(rows, predict_fn, label):
    deltas = []
    sign_hits = 0
    for r in rows:
        pred = predict_fn(r)
        obs = r["B_obs_u"]
        delta = obs - pred
        deltas.append((r, pred, delta))
        if (pred >= 0) == (obs >= 0):
            sign_hits += 1
    n = len(rows)
    abs_MeV = [abs(d) * U_TO_MEV for _, _, d in deltas]
    sum_sq = sum(d * d for _, _, d in deltas)
    rms_u = (sum_sq / Decimal(n)).sqrt()
    return {
        "label": label,
        "n": n,
        "sign_hits": sign_hits,
        "sign_acc": Decimal(sign_hits) / Decimal(n),
        "max_abs_MeV": max(abs_MeV),
        "mean_abs_MeV": sum(abs_MeV) / Decimal(n),
        "rms_MeV": rms_u * U_TO_MEV,
        "deltas": deltas,
    }


def fmt(d, places=3):
    q = Decimal("0." + "0" * places) if places > 0 else Decimal("1")
    return f"{d.quantize(q)}"


def main():
    rows = load()
    print(f"Loaded {len(rows)} N>=Z nuclei (Decimal precision 50, CODATA U_TO_MEV)\n")

    q_list = [
        ("D=3", Fraction(3)),
        ("αH²=4", Fraction(4)),
        ("R/2=6", Fraction(6)),
        ("S-1=7", Fraction(7)),
        ("S=8", Fraction(8)),
        ("D²=9", Fraction(9)),
        ("R=12", Fraction(12)),
        ("Θ=18", Fraction(18)),
        ("V=27", Fraction(27)),
        ("ℱ=81", Fraction(81)),
        ("M=126", Fraction(126)),
        ("L=162", Fraction(162)),
        ("ℱ·S-1=647", Fraction(647)),
        ("ℱ·S=648", Fraction(648)),
    ]

    print("=" * 100)
    print("PHASE H: 3-term search (Z + A^(2/3) + Z(Z-1)/A^(1/3))")
    print("         q_Z and q_A23 locked from v2 best (647, 162)")
    print("         Search q_Coul over substrate-named values, both signs")
    print("=" * 100)
    results = []
    for c_name, q_C in q_list:
        for coul_sign, sign_name in [(Decimal(-1), "-"), (Decimal(1), "+")]:
            label = f"Z·647 + A^(2/3)·162 {sign_name} Z(Z-1)/A^(1/3)·({c_name})"
            result = evaluate(rows,
                              lambda r, qc=q_C, cs=coul_sign:
                                  predict_three_term(r, Fraction(647), Fraction(162), qc, cs),
                              label)
            results.append(result)
    results.sort(key=lambda x: x["rms_MeV"])
    print(f"  {'rank':>4} {'label':<55s} {'sign%':>6} {'max|Δ| MeV':>10} {'RMS MeV':>8}")
    for i, r in enumerate(results[:10], 1):
        print(f"  {i:>4} {r['label']:<55s} "
              f"{fmt(r['sign_acc']*Decimal(100), 1):>6s} "
              f"{fmt(r['max_abs_MeV'], 2):>10s} "
              f"{fmt(r['rms_MeV'], 2):>8s}")

    print()
    print("=" * 100)
    print("PHASE I: 3-term search — also vary q_Z and q_A23")
    print("=" * 100)
    print("  Restricted to top substrate constants for tractability")
    print()
    q_short = [
        ("S-1=7", Fraction(7)),
        ("Θ=18", Fraction(18)),
        ("V=27", Fraction(27)),
        ("ℱ=81", Fraction(81)),
        ("M=126", Fraction(126)),
        ("L=162", Fraction(162)),
        ("ℱ·S-1=647", Fraction(647)),
        ("ℱ·S=648", Fraction(648)),
    ]
    results_3t = []
    for z_name, q_Z in q_short:
        for a_name, q_A in q_short:
            for c_name, q_C in q_short:
                for coul_sign in [Decimal(-1), Decimal(1)]:
                    sn = "-" if coul_sign < 0 else "+"
                    label = f"Z·({z_name}) + A^(2/3)·({a_name}) {sn} Z(Z-1)/A^(1/3)·({c_name})"
                    result = evaluate(rows,
                                      lambda r, qz=q_Z, qa=q_A, qc=q_C, cs=coul_sign:
                                          predict_three_term(r, qz, qa, qc, cs),
                                      label)
                    results_3t.append(result)
    results_3t.sort(key=lambda x: x["rms_MeV"])
    print(f"  Top 15 from 3-term search ({len(results_3t)} combinations):")
    print(f"  {'rank':>4} {'label':<75s} {'sign%':>6} {'max|Δ|':>8} {'RMS':>7}")
    for i, r in enumerate(results_3t[:15], 1):
        print(f"  {i:>4} {r['label']:<75s} "
              f"{fmt(r['sign_acc']*Decimal(100), 1):>6s} "
              f"{fmt(r['max_abs_MeV'], 2):>8s} "
              f"{fmt(r['rms_MeV'], 2):>7s}")

    print()
    print("=" * 100)
    print("PHASE J: 4-term search — add (N-Z)²/A asymmetry term")
    print("         Lock q_Z and q_A23 to v2/v3 best; search q_Coul + q_Asym")
    print("=" * 100)
    results_4t = []
    for c_name, q_C in q_list:
        for coul_sign in [Decimal(-1), Decimal(1)]:
            for as_name, q_As in q_list:
                for asym_sign in [Decimal(-1), Decimal(1)]:
                    cs = "-" if coul_sign < 0 else "+"
                    ass = "-" if asym_sign < 0 else "+"
                    label = f"Z·647 + A^(2/3)·162 {cs}Coul·({c_name}) {ass}Asym·({as_name})"
                    result = evaluate(rows,
                                      lambda r, qc=q_C, cs2=coul_sign, qa2=q_As, as2=asym_sign:
                                          predict_four_term(r, Fraction(647), Fraction(162), qc, cs2, qa2, as2),
                                      label)
                    results_4t.append(result)
    results_4t.sort(key=lambda x: x["rms_MeV"])
    print(f"  Top 10 from 4-term search ({len(results_4t)} combinations):")
    print(f"  {'rank':>4} {'label':<70s} {'sign%':>6} {'max|Δ|':>8} {'RMS':>7}")
    for i, r in enumerate(results_4t[:10], 1):
        print(f"  {i:>4} {r['label']:<70s} "
              f"{fmt(r['sign_acc']*Decimal(100), 1):>6s} "
              f"{fmt(r['max_abs_MeV'], 2):>8s} "
              f"{fmt(r['rms_MeV'], 2):>7s}")

    print()
    print("=" * 100)
    print("PHASE K: Per-row detail for best 4-term combo")
    print("=" * 100)
    best = results_4t[0]
    print(f"  {best['label']}")
    print(f"  sign={fmt(best['sign_acc']*Decimal(100),1)}%  max|Δ|={fmt(best['max_abs_MeV'],3)} MeV  RMS={fmt(best['rms_MeV'],3)} MeV")
    print()
    print(f"  {'iso':>8} {'A':>4} {'N-Z':>4} {'B_obs MeV':>11} {'B_pred MeV':>11} {'Δ MeV':>9}")
    print("-" * 80)
    for r, pred, delta in sorted(best["deltas"], key=lambda x: x[0]["A"]):
        print(f"  {r['iso']:>8} {r['A']:4d} {r['NmZ']:4d} "
              f"{fmt(r['B_obs_MeV'], 3):>11s} "
              f"{fmt(pred * U_TO_MEV, 3):>11s} "
              f"{fmt(delta * U_TO_MEV, 3):>9s}")


if __name__ == "__main__":
    main()
