"""Frozen kernel residual table — clean reprint for THIS exact model only:

  B_u^(0) = 8·A − 17·A^(2/3) − (3/4)·Z(Z−1)/A^(1/3) − 22·(N−Z)²/A + 7·δ/√A − (25/4)·Λ

  Λ = 1 if primitive (a, b) ≠ (1, 1), else 0.
  Sort by |Δ| descending so the dominant residuals show first.
  Annotate magic Z or N from {2, 8, 20, 28, 50, 82, 126}.
"""
from __future__ import annotations

import csv
from math import gcd
from pathlib import Path

U_TO_MEV = 931.49410242
MAGIC = {2, 8, 20, 28, 50, 82, 126}
HERE = Path(__file__).parent
CR242 = HERE.parent / "CR242_SAM_BINDING_CURVATURE_DERIVATION" / "CR242_binding_dataset.csv"


def delta_pair(Z, N):
    if Z % 2 == 0 and N % 2 == 0: return +1
    if Z % 2 == 1 and N % 2 == 1: return -1
    return 0


def predict(Z, N, A):
    NmZ = N - Z
    g = gcd(Z, N) if (Z > 0 and N > 0) else max(Z, N, 1)
    a = Z // g if g else Z
    b = N // g if g else N
    is_non_unity = (a, b) != (1, 1)
    vol = 8 * A
    surf = 17 * (A ** (2/3))
    coul = (3/4) * Z * (Z - 1) / (A ** (1/3)) if A > 0 else 0
    asym = 22 * NmZ * NmZ / A if A > 0 else 0
    pair = 7 * delta_pair(Z, N) / (A ** 0.5) if A > 0 else 0
    lane = (25/4) if is_non_unity else 0
    return vol - surf - coul - asym + pair - lane


def main():
    rows = []
    with CR242.open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                Z = int(float(r["Z"])); N = int(float(r["N"])); A = int(float(r["A"]))
                B = float(r["B_u"])
            except (KeyError, ValueError):
                continue
            B_obs_MeV = B * U_TO_MEV
            pred_MeV = predict(Z, N, A)
            delta = B_obs_MeV - pred_MeV
            g = gcd(Z, N) if (Z > 0 and N > 0) else max(Z, N, 1)
            a = Z // g if g else Z
            b = N // g if g else N
            magic = []
            if Z in MAGIC: magic.append(f"Z={Z}")
            if N in MAGIC: magic.append(f"N={N}")
            magic_str = " ".join(magic) if magic else ""
            rows.append({
                "iso": r["isotope"],
                "Z": Z, "N": N, "A": A, "NmZ": N - Z,
                "primitive": (a, b),
                "lambda": g,
                "B_obs": B_obs_MeV,
                "B_pred": pred_MeV,
                "delta": delta,
                "abs_delta": abs(delta),
                "magic": magic_str,
            })

    n = len(rows)
    sum_sq = sum(r["delta"] ** 2 for r in rows)
    rms = (sum_sq / n) ** 0.5
    mean_abs = sum(r["abs_delta"] for r in rows) / n
    max_abs = max(r["abs_delta"] for r in rows)

    print("=" * 100)
    print("FROZEN MODEL: B_u^(0) = 8·A − 17·A^(2/3) − (3/4)·Z(Z−1)/A^(1/3) − 22·(N−Z)²/A + 7·δ/√A − (25/4)·Λ")
    print(f"All coefficients substrate-exact. Λ = 1 if primitive ≠ (1,1), else 0.")
    print("=" * 100)
    print(f"n = {n}   RMS = {rms:.4f} MeV   mean|Δ| = {mean_abs:.4f} MeV   max|Δ| = {max_abs:.4f} MeV")
    print()
    print("=" * 100)
    print("PER-ROW RESIDUALS, SORTED BY |Δ| DESCENDING")
    print("=" * 100)
    print(f"  {'iso':>8} {'Z':>3} {'N':>3} {'A':>4} {'(a,b)':>10} {'λ':>3} "
          f"{'B_obs MeV':>11} {'B_pred MeV':>11} {'Δ MeV':>9}  magic")
    print("-" * 100)
    for r in sorted(rows, key=lambda x: -x["abs_delta"]):
        prim_str = f"({r['primitive'][0]},{r['primitive'][1]})"
        print(f"  {r['iso']:>8} {r['Z']:3d} {r['N']:3d} {r['A']:4d} {prim_str:>10s} {r['lambda']:3d} "
              f"{r['B_obs']:11.3f} {r['B_pred']:11.3f} {r['delta']:+9.3f}  {r['magic']}")

    print()
    print("=" * 100)
    print("RESIDUAL CONCENTRATION AT MAGIC NUMBERS {2, 8, 20, 28, 50, 82, 126}")
    print("=" * 100)
    magic_rows = [r for r in rows if r["magic"]]
    non_magic = [r for r in rows if not r["magic"]]
    if magic_rows:
        m_rms = (sum(r["delta"] ** 2 for r in magic_rows) / len(magic_rows)) ** 0.5
        nm_rms = (sum(r["delta"] ** 2 for r in non_magic) / len(non_magic)) ** 0.5
        m_mean = sum(r["delta"] for r in magic_rows) / len(magic_rows)
        nm_mean = sum(r["delta"] for r in non_magic) / len(non_magic)
        print(f"  Rows touching magic Z or N (n={len(magic_rows)}):  RMS = {m_rms:7.3f} MeV   mean Δ = {m_mean:+7.3f} MeV")
        print(f"  Rows without magic (n={len(non_magic)}):           RMS = {nm_rms:7.3f} MeV   mean Δ = {nm_mean:+7.3f} MeV")
        ratio = m_rms / nm_rms if nm_rms > 0 else float("inf")
        print(f"  Concentration ratio (magic / non-magic): {ratio:.3f}×")

    print()
    print("=" * 100)
    print("DOUBLY MAGIC AND NEAR-MAGIC CASES")
    print("=" * 100)
    double_magic = [r for r in rows if r["Z"] in MAGIC and r["N"] in MAGIC]
    near_dm = [r for r in rows if (r["Z"] in MAGIC and abs(r["N"] - min(MAGIC, key=lambda m: abs(m - r["N"]))) <= 2)
                                or (r["N"] in MAGIC and abs(r["Z"] - min(MAGIC, key=lambda m: abs(m - r["Z"]))) <= 2)]
    print(f"  Doubly magic (both Z and N in {{2,8,20,28,50,82,126}}):")
    for r in sorted(double_magic, key=lambda x: -x["abs_delta"]):
        print(f"    {r['iso']:>8} Z={r['Z']:3d} N={r['N']:3d}  Δ = {r['delta']:+8.3f} MeV")
    print(f"\n  Near-magic (one axis magic, other within ±2 of magic):")
    for r in sorted([x for x in near_dm if x not in double_magic], key=lambda x: -x["abs_delta"])[:15]:
        print(f"    {r['iso']:>8} Z={r['Z']:3d} N={r['N']:3d}  Δ = {r['delta']:+8.3f} MeV  ({r['magic']})")


if __name__ == "__main__":
    main()
