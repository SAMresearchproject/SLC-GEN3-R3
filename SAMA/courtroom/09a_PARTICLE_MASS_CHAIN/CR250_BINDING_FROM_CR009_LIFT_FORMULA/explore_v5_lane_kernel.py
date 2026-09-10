"""Exploration v5 — lane-scaling audit + full BW A-kernel in lane variables.

Per Sean's PDF:
  For every row: λ = gcd(Z, N), (a, b) = (Z/λ, N/λ), ρ = (N-Z)/A, χ = 1 - 7093/7117·ρ
  Group by primitive (a, b), test 6 normalizations.
  Then fit the full kernel in lane variables and look for substrate-named coefficients.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from decimal import Decimal, getcontext
from fractions import Fraction
from math import gcd
from pathlib import Path

import numpy as np

getcontext().prec = 50

U_TO_MEV = Decimal("931.49410242")
U_TO_MEV_F = float(U_TO_MEV)

HERE = Path(__file__).parent
CR242 = HERE.parent / "CR242_SAM_BINDING_CURVATURE_DERIVATION" / "CR242_binding_dataset.csv"

# Sealed substrate rationals
SUBSTRATE_RATIONALS = {
    "1":         Fraction(1),
    "α_H=2":     Fraction(2),
    "D=3":       Fraction(3),
    "α_H²=4":    Fraction(4),
    "R/2=6":     Fraction(6),
    "S-1=7":     Fraction(7),
    "S=8":       Fraction(8),
    "D²=9":      Fraction(9),
    "R=12":      Fraction(12),
    "Θ=18":      Fraction(18),
    "V=27":      Fraction(27),
    "ℱ=81":      Fraction(81),
    "M=126":     Fraction(126),
    "L=162":     Fraction(162),
    "ℱ·S-1=647": Fraction(647),
    "ℱ·S=648":   Fraction(648),
    "κ":         Fraction(7117, 768),
    "g":         Fraction(1, 64),
    "μ_Q":       Fraction(192, 7117),
    "1/R":       Fraction(1, 12),
    "D/R":       Fraction(1, 4),
    "D²/R":      Fraction(3, 4),
    "1/R²":      Fraction(1, 144),
    "1/R⁴":      Fraction(1, 20736),
    "7093/192":  Fraction(7093, 192),
    "7093/7117": Fraction(7093, 7117),
    "7093²/(192·7117)": Fraction(7093 * 7093, 192 * 7117),
    "8κ":        Fraction(8) * Fraction(7117, 768),
    "4κ":        Fraction(4) * Fraction(7117, 768),
}


def load_all():
    rows = []
    with CR242.open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                Z = int(float(r["Z"]))
                N = int(float(r["N"]))
                A = int(float(r["A"]))
                B = float(r["B_u"])
            except (KeyError, ValueError):
                continue
            NmZ = N - Z
            g = gcd(Z, N) if (Z > 0 and N > 0) else max(Z, N, 1)
            a = Z // g if g > 0 else Z
            b = N // g if g > 0 else N
            rho = NmZ / A if A else 0.0
            chi = 1.0 - (7093.0 / 7117.0) * rho
            rows.append({
                "iso": r["isotope"],
                "Z": Z, "N": N, "A": A, "NmZ": NmZ,
                "B_obs_u": B,
                "B_obs_MeV": B * U_TO_MEV_F,
                "lambda": g,
                "a": a, "b": b,
                "rho": rho,
                "chi": chi,
                "primitive": (a, b),
                "ratio_NmZ_A": Fraction(NmZ, A) if A else Fraction(0),
            })
    return rows


def match_substrate(value, tol=0.02):
    """Find substrate-named rationals near `value` (relative tolerance)."""
    matches = []
    for name, frac in SUBSTRATE_RATIONALS.items():
        f_val = float(frac)
        if f_val == 0:
            continue
        rel = abs(value - f_val) / abs(f_val)
        if rel < tol:
            matches.append((name, f_val, rel))
    # also check 1/value
    if value != 0:
        inv = 1.0 / value
        for name, frac in SUBSTRATE_RATIONALS.items():
            f_val = float(frac)
            if f_val == 0:
                continue
            rel = abs(inv - f_val) / abs(f_val)
            if rel < tol:
                matches.append((f"1/({name})", 1.0 / f_val, rel))
    return matches


def main():
    rows = load_all()
    print(f"Loaded {len(rows)} CR242 rows (all)\n")

    # Group by primitive
    by_prim = defaultdict(list)
    for r in rows:
        by_prim[r["primitive"]].append(r)
    multi_lanes = {p: m for p, m in by_prim.items() if len(m) >= 2}
    print(f"Multi-member primitive lanes: {len(multi_lanes)}")

    # Test normalizations within each multi-member lane
    print()
    print("=" * 100)
    print("LANE-SCALING AUDIT — test which B_u/X is most constant within each primitive lane")
    print("=" * 100)
    print("  Method: for each lane, compute B_u/X for all members, then report std/|mean|")
    print("  Smaller std/|mean| means X is a better lane-invariant normalizer.")
    print()

    normalizations = [
        ("B_u/A",                lambda r: r["B_obs_MeV"] / r["A"]),
        ("B_u/λ",                lambda r: r["B_obs_MeV"] / r["lambda"]),
        ("B_u/λ²",               lambda r: r["B_obs_MeV"] / (r["lambda"] ** 2)),
        ("B_u/A^(2/3)",          lambda r: r["B_obs_MeV"] / (r["A"] ** (2/3))),
        ("B_u/[Z(Z-1)/A^(1/3)]", lambda r: r["B_obs_MeV"] / (r["Z"] * (r["Z"] - 1) / (r["A"] ** (1/3))) if r["Z"] > 1 else None),
        ("B_u/((N-Z)²/A)",       lambda r: r["B_obs_MeV"] / ((r["NmZ"] ** 2) / r["A"]) if r["NmZ"] != 0 else None),
    ]
    print(f"  {'normalization':>24s} | per-lane (std/|mean|), and mean value")
    print("-" * 100)
    for prim, members in sorted(multi_lanes.items(), key=lambda kv: (kv[0][1] - kv[0][0], kv[0][0])):
        if len(members) < 2:
            continue
        print(f"\n  LANE primitive {prim} ({len(members)} members):")
        for name, fn in normalizations:
            vals = [fn(r) for r in members]
            vals = [v for v in vals if v is not None]
            if len(vals) < 2:
                continue
            mean = sum(vals) / len(vals)
            var = sum((v - mean) ** 2 for v in vals) / len(vals)
            std = var ** 0.5
            cv = std / abs(mean) if mean != 0 else float('inf')
            print(f"    {name:>30s}  mean = {mean:>12.4f}  std/|mean| = {cv:>7.3f}")

    # Full BW kernel fit in lane variables
    print()
    print("=" * 100)
    print("FULL BW KERNEL FIT — B_u = c_V·A + c_S·A^(2/3) + c_C·Z(Z-1)/A^(1/3) + c_A·(N-Z)²/A + c_P·δ")
    print("  (Conventional sign convention: c_V > 0, c_S < 0, c_C < 0, c_A < 0, c_P signed)")
    print("=" * 100)

    A = np.array([r["A"] for r in rows], dtype=float)
    Z = np.array([r["Z"] for r in rows], dtype=float)
    N = np.array([r["N"] for r in rows], dtype=float)
    NmZ = N - Z
    B_obs_MeV = np.array([r["B_obs_MeV"] for r in rows], dtype=float)

    # Build design matrix
    f_V = A
    f_S = A ** (2/3)
    f_C = Z * (Z - 1) / (A ** (1/3))
    f_A = (NmZ ** 2) / A
    # Pairing: delta = +1 even-even, -1 odd-odd, 0 odd-A
    # Standard BW uses delta / A^(1/2)
    delta_sign = []
    for r in rows:
        if r["Z"] % 2 == 0 and r["N"] % 2 == 0:
            delta_sign.append(+1)
        elif r["Z"] % 2 == 1 and r["N"] % 2 == 1:
            delta_sign.append(-1)
        else:
            delta_sign.append(0)
    f_P = np.array(delta_sign, dtype=float) / np.sqrt(A)

    # Fit B_obs_MeV ≈ c_V·f_V + c_S·f_S + c_C·f_C + c_A·f_A + c_P·f_P
    # (Note: CR242 B_u = A·u - m_obs, not conventional binding energy. Sign may differ.)
    X = np.column_stack([f_V, f_S, f_C, f_A, f_P])
    coeffs, residuals, rank, sv = np.linalg.lstsq(X, B_obs_MeV, rcond=None)

    c_V, c_S, c_C, c_A, c_P = coeffs
    predicted = X @ coeffs
    delta_pred = B_obs_MeV - predicted
    rms = (delta_pred ** 2).mean() ** 0.5
    max_abs = abs(delta_pred).max()

    print(f"\n  Fitted coefficients (MeV):")
    print(f"    c_V (volume)      = {c_V:+10.4f} MeV")
    print(f"    c_S (surface)     = {c_S:+10.4f} MeV")
    print(f"    c_C (Coulomb)     = {c_C:+10.4f} MeV")
    print(f"    c_A (asymmetry)   = {c_A:+10.4f} MeV")
    print(f"    c_P (pairing)     = {c_P:+10.4f} MeV")
    print(f"\n  Fit quality:")
    print(f"    RMS residual      = {rms:>10.4f} MeV")
    print(f"    max |residual|    = {max_abs:>10.4f} MeV")

    # Check each coefficient against substrate-named rationals
    print(f"\n  Substrate-constant matches (within 2% relative tolerance):")
    for name, val in [("c_V", c_V), ("c_S", c_S), ("c_C", c_C), ("c_A", c_A), ("c_P", c_P)]:
        matches = match_substrate(abs(val), tol=0.02)
        match_str = ", ".join(f"{m[0]} ({m[1]:.4f}, rel={m[2]:.4f})" for m in matches) if matches else "(none within 2%)"
        print(f"    {name} = {val:+8.4f}  →  {match_str}")

    # Also try with looser tolerance
    print(f"\n  Substrate-constant matches (within 10% relative tolerance):")
    for name, val in [("c_V", c_V), ("c_S", c_S), ("c_C", c_C), ("c_A", c_A), ("c_P", c_P)]:
        matches = match_substrate(abs(val), tol=0.10)
        match_str = ", ".join(f"{m[0]}({m[1]:.2f},rel={m[2]:.3f})" for m in matches) if matches else "(none within 10%)"
        print(f"    {name:>4} = {val:+8.4f}  →  {match_str}")

    # Per-row residuals
    print()
    print("=" * 100)
    print("PER-ROW RESIDUALS AFTER FIT (sorted by A)")
    print("=" * 100)
    print(f"  {'iso':>8} {'Z':>3} {'N':>3} {'A':>4} {'λ':>4} {'(a,b)':>10} {'B_obs MeV':>11} {'B_pred MeV':>11} {'Δ MeV':>9}")
    for i, r in enumerate(sorted(rows, key=lambda x: x["A"])):
        idx = rows.index(r)
        pred = predicted[idx]
        delta = B_obs_MeV[idx] - pred
        prim_str = f"({r['a']},{r['b']})"
        print(f"  {r['iso']:>8} {r['Z']:3d} {r['N']:3d} {r['A']:4d} {r['lambda']:4d} {prim_str:>10s} "
              f"{r['B_obs_MeV']:11.4f} {pred:11.4f} {delta:9.4f}")

    # Also test the consecutive primitive (k, k+1) simplified form
    print()
    print("=" * 100)
    print("CONSECUTIVE PRIMITIVE LANES (a, b)=(k, k+1) — sample fit check")
    print("=" * 100)
    consec_rows = [r for r in rows if r["b"] - r["a"] == 1]
    print(f"  {len(consec_rows)} rows have (b - a) = 1 (consecutive primitive lanes)")
    for r in sorted(consec_rows, key=lambda x: (x["a"], x["lambda"])):
        k = r["a"]
        lam = r["lambda"]
        print(f"  {r['iso']:>8} k={k:2d} λ={lam:3d} A={r['A']:4d}  B_obs={r['B_obs_MeV']:9.3f} MeV  "
              f"χ={r['chi']:.6f}")


if __name__ == "__main__":
    main()
