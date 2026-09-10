"""Exploration v7 — shape-substitution audit.

Per Sean's PDF: the numbers are scalar shadows of substrate shapes. Test by swapping
the SHAPES themselves and seeing if the substrate-locked formula degrades.

Five shape wrong controls:
  1. A^(2/3) → A^(1/2)       (surface shape)
  2. A^(-1/3) → A^(-1/2) or A^(-2/3)  (Coulomb road depth)
  3. (N-Z)²/A → |N-Z| or (N-Z)²/A^(2/3)  (asymmetry lane curvature)
  4. δ → random parity or shuffled  (pairing closure)
  5. Group residuals by primitive lane (a,b) and scale λ — if shape, residuals organize.

Also test: re-fit each shape substitution to see if a wrong shape can match RMS by
adjusting only the scalar coefficient. If the substrate shape is right, no scalar
re-fit of a wrong shape can match the original shape's RMS.
"""
from __future__ import annotations

import csv
import random
from collections import defaultdict
from math import gcd, sqrt
from pathlib import Path

import numpy as np

U_TO_MEV = 931.49410242
HERE = Path(__file__).parent
CR242 = HERE.parent / "CR242_SAM_BINDING_CURVATURE_DERIVATION" / "CR242_binding_dataset.csv"


def load():
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
            g = gcd(Z, N) if (Z > 0 and N > 0) else max(Z, N, 1)
            rows.append({
                "iso": r["isotope"],
                "Z": Z, "N": N, "A": A, "NmZ": N - Z,
                "B_obs": B * U_TO_MEV,
                "lambda": g,
                "primitive": (Z // g if g else Z, N // g if g else N),
            })
    return rows


def delta_pair(Z, N):
    if Z % 2 == 0 and N % 2 == 0: return +1
    if Z % 2 == 1 and N % 2 == 1: return -1
    return 0


def predict_shape(row, coeffs, surface_pow, coul_pow, asym_form, pair_array=None, pair_idx=None):
    """Generic prediction with swappable shapes.
    coeffs = (c_V, c_S, c_C, c_A, c_P)
    surface_pow: exponent on A for surface term (default 2/3)
    coul_pow: exponent on A for Coulomb denominator (default 1/3) — passed positive, used as A^(-coul_pow)
    asym_form: function (Z, N, A) → asymmetry shape value
    """
    Z, N, A = row["Z"], row["N"], row["A"]
    NmZ = N - Z
    cV, cS, cC, cA, cP = coeffs
    vol = cV * A
    surf = cS * (A ** surface_pow)
    coul = cC * Z * (Z - 1) * (A ** (-coul_pow)) if A > 0 else 0.0
    asym = cA * asym_form(Z, N, A) if A > 0 else 0.0
    if pair_array is not None:
        # shuffled pairing
        d_p = pair_array[pair_idx]
    else:
        d_p = delta_pair(Z, N)
    pair = cP * d_p / (A ** 0.5) if A > 0 else 0.0
    return vol - surf - coul - asym + pair


def rms_max(rows, predict_fn):
    preds = [predict_fn(r, idx) for idx, r in enumerate(rows)]
    deltas = [r["B_obs"] - p for r, p in zip(rows, preds)]
    n = len(rows)
    rms = (sum(d * d for d in deltas) / n) ** 0.5
    max_abs = max(abs(d) for d in deltas)
    return rms, max_abs, deltas, preds


# Asymmetry shape candidates
def asym_native(Z, N, A): return (N - Z) ** 2 / A
def asym_abs(Z, N, A): return abs(N - Z)
def asym_A23_denom(Z, N, A): return (N - Z) ** 2 / (A ** (2/3))
def asym_no_square(Z, N, A): return (N - Z) / A


def main():
    rows = load()
    n = len(rows)
    print(f"Loaded {n} CR242 rows\n")

    # Coefficient sets
    LOCKED = (8, 18, 3/4, 24, 7)
    MINUS1 = (8, 17, 3/4, 22, 7)
    BEST   = (8, 17, 3/4, 23, 7)

    # Free-fit baseline (for comparison)
    print("=" * 100)
    print("BASELINE — substrate-native shapes (surf=A^2/3, coul=Z(Z-1)/A^(1/3), asym=(N-Z)²/A, δ=parity)")
    print("=" * 100)
    for label, coeffs in [
        ("LOCKED (8, 18, 3/4, 24, 7)", LOCKED),
        ("MINUS-1 (8, 17, 3/4, 22, 7)", MINUS1),
        ("BEST   (8, 17, 3/4, 23, 7)", BEST),
    ]:
        def pf(r, idx, c=coeffs): return predict_shape(r, c, 2/3, 1/3, asym_native)
        rms, mx, _, _ = rms_max(rows, pf)
        print(f"  {label:35s}  RMS = {rms:7.4f} MeV   max|Δ| = {mx:7.4f} MeV")

    # ─────────────────────────────────────────────────────────────────────────
    print()
    print("=" * 100)
    print("SHAPE WRONG CONTROL #1 — surface power: A^(2/3) ↔ A^(1/2)")
    print("  If A^(2/3) is the real surface shape, swap to A^(1/2) should degrade.")
    print("=" * 100)
    for label, coeffs in [("LOCKED", LOCKED), ("MINUS-1", MINUS1), ("BEST", BEST)]:
        # Native (A^2/3)
        def p1(r, idx, c=coeffs): return predict_shape(r, c, 2/3, 1/3, asym_native)
        rms_native, _, _, _ = rms_max(rows, p1)
        # Wrong shape A^1/2
        def p2(r, idx, c=coeffs): return predict_shape(r, c, 1/2, 1/3, asym_native)
        rms_swap, _, _, _ = rms_max(rows, p2)
        # Refit c_S with wrong shape (best-case scalar adjustment)
        A_arr = np.array([r["A"] for r in rows])
        Z_arr = np.array([r["Z"] for r in rows])
        NmZ_arr = np.array([r["N"] - r["Z"] for r in rows])
        B_arr = np.array([r["B_obs"] for r in rows])
        pair_arr = np.array([delta_pair(r["Z"], r["N"]) for r in rows]) / np.sqrt(A_arr)
        cV, cS, cC, cA, cP = coeffs
        # Residual after locking everything but c_S: B - (cV·A - cC·...) = cS·shape_swap - cA·asym + cP·pair
        fixed_part = cV * A_arr - cC * Z_arr * (Z_arr - 1) / (A_arr ** (1/3)) - cA * (NmZ_arr ** 2) / A_arr + cP * pair_arr
        target = B_arr - fixed_part   # = -cS·shape_swap
        wrong_shape_vals = A_arr ** 0.5
        cS_refit = -target.dot(wrong_shape_vals) / wrong_shape_vals.dot(wrong_shape_vals)
        # Apply refitted
        def p3(r, idx, cs=cS_refit, c=coeffs): return predict_shape(r, (c[0], cs, c[2], c[3], c[4]), 1/2, 1/3, asym_native)
        rms_refit, _, _, _ = rms_max(rows, p3)
        print(f"  {label:8s}  native RMS = {rms_native:7.3f}   wrong A^(1/2) RMS = {rms_swap:7.3f}   "
              f"refit c_S = {cS_refit:.3f} → RMS = {rms_refit:7.3f}")

    # ─────────────────────────────────────────────────────────────────────────
    print()
    print("=" * 100)
    print("SHAPE WRONG CONTROL #2 — Coulomb road depth: A^(-1/3) ↔ A^(-1/2) or A^(-2/3)")
    print("=" * 100)
    for label, coeffs in [("LOCKED", LOCKED), ("MINUS-1", MINUS1), ("BEST", BEST)]:
        def p1(r, idx, c=coeffs): return predict_shape(r, c, 2/3, 1/3, asym_native)
        def p2(r, idx, c=coeffs): return predict_shape(r, c, 2/3, 1/2, asym_native)
        def p3(r, idx, c=coeffs): return predict_shape(r, c, 2/3, 2/3, asym_native)
        rms_n, _, _, _ = rms_max(rows, p1)
        rms_h, _, _, _ = rms_max(rows, p2)
        rms_t, _, _, _ = rms_max(rows, p3)
        print(f"  {label:8s}  native A^(-1/3) RMS = {rms_n:7.3f}   "
              f"swap A^(-1/2) RMS = {rms_h:7.3f}   swap A^(-2/3) RMS = {rms_t:7.3f}")

    # ─────────────────────────────────────────────────────────────────────────
    print()
    print("=" * 100)
    print("SHAPE WRONG CONTROL #3 — asymmetry shape: (N-Z)²/A ↔ |N-Z| or (N-Z)²/A^(2/3)")
    print("=" * 100)
    for label, coeffs in [("LOCKED", LOCKED), ("MINUS-1", MINUS1), ("BEST", BEST)]:
        def p1(r, idx, c=coeffs): return predict_shape(r, c, 2/3, 1/3, asym_native)
        def p2(r, idx, c=coeffs): return predict_shape(r, c, 2/3, 1/3, asym_abs)
        def p3(r, idx, c=coeffs): return predict_shape(r, c, 2/3, 1/3, asym_A23_denom)
        def p4(r, idx, c=coeffs): return predict_shape(r, c, 2/3, 1/3, asym_no_square)
        rms_n, _, _, _ = rms_max(rows, p1)
        rms_abs, _, _, _ = rms_max(rows, p2)
        rms_a23, _, _, _ = rms_max(rows, p3)
        rms_nosq, _, _, _ = rms_max(rows, p4)
        print(f"  {label:8s}  native (N-Z)²/A RMS = {rms_n:7.3f}")
        print(f"            wrong |N-Z|        RMS = {rms_abs:7.3f}")
        print(f"            wrong (N-Z)²/A^(2/3) RMS = {rms_a23:7.3f}")
        print(f"            wrong (N-Z)/A      RMS = {rms_nosq:7.3f}")

    # ─────────────────────────────────────────────────────────────────────────
    print()
    print("=" * 100)
    print("SHAPE WRONG CONTROL #4 — pairing δ: parity ↔ shuffled or random")
    print("=" * 100)
    for label, coeffs in [("LOCKED", LOCKED), ("MINUS-1", MINUS1), ("BEST", BEST)]:
        def p1(r, idx, c=coeffs): return predict_shape(r, c, 2/3, 1/3, asym_native)
        rms_n, _, _, _ = rms_max(rows, p1)
        # Shuffled pairing (deterministic seed)
        rng = random.Random(42)
        native_pair = [delta_pair(r["Z"], r["N"]) for r in rows]
        shuffled = list(native_pair)
        rng.shuffle(shuffled)
        def p2(r, idx, c=coeffs, sp=shuffled): return predict_shape(r, c, 2/3, 1/3, asym_native, pair_array=sp, pair_idx=idx)
        rms_shuf, _, _, _ = rms_max(rows, p2)
        # All zero pairing
        zero_pair = [0] * len(rows)
        def p3(r, idx, c=coeffs, zp=zero_pair): return predict_shape(r, c, 2/3, 1/3, asym_native, pair_array=zp, pair_idx=idx)
        rms_zero, _, _, _ = rms_max(rows, p3)
        # Reversed pairing (flip sign)
        rev_pair = [-x for x in native_pair]
        def p4(r, idx, c=coeffs, rp=rev_pair): return predict_shape(r, c, 2/3, 1/3, asym_native, pair_array=rp, pair_idx=idx)
        rms_rev, _, _, _ = rms_max(rows, p4)
        print(f"  {label:8s}  native parity    RMS = {rms_n:7.3f}")
        print(f"            shuffled parity  RMS = {rms_shuf:7.3f}")
        print(f"            all zero parity  RMS = {rms_zero:7.3f}")
        print(f"            flipped sign     RMS = {rms_rev:7.3f}")

    # ─────────────────────────────────────────────────────────────────────────
    print()
    print("=" * 100)
    print("SHAPE PROBE #5 — residuals grouped by primitive lane (a, b)")
    print("  If lane is real, residuals should organize by primitive, not random isotope.")
    print("=" * 100)
    coeffs = MINUS1  # use MINUS-1 model
    def pf(r, idx, c=coeffs): return predict_shape(r, c, 2/3, 1/3, asym_native)
    rms, mx, deltas, preds = rms_max(rows, pf)
    print(f"  Model: MINUS-1 (8, 17, 3/4, 22, 7), RMS = {rms:.4f} MeV")
    print()
    by_prim = defaultdict(list)
    for r, d in zip(rows, deltas):
        by_prim[r["primitive"]].append((r, d))
    print(f"  Multi-member primitive lanes (n >= 2):")
    print(f"  {'primitive':>12s} {'n':>3s} {'residual range MeV':>22s} {'mean':>9s} {'std':>9s}")
    for prim in sorted(by_prim.keys(), key=lambda p: -len(by_prim[p])):
        members = by_prim[prim]
        if len(members) < 2:
            continue
        dvals = [d for _, d in members]
        rng = (min(dvals), max(dvals))
        mean = sum(dvals) / len(dvals)
        std = (sum((d - mean) ** 2 for d in dvals) / len(dvals)) ** 0.5
        print(f"  {str(prim):>12s} {len(members):3d} {rng[0]:>8.2f} .. {rng[1]:>8.2f}  {mean:9.3f} {std:9.3f}")
    print()
    print("  Singleton lanes — residuals listed with primitive vector and λ:")
    print(f"  {'iso':>8} {'(a,b)':>10} {'λ':>4} {'Δ MeV':>9}")
    singletons = [(prim, members[0]) for prim, members in by_prim.items() if len(members) == 1]
    # Sort by |residual| descending
    singletons.sort(key=lambda x: -abs(x[1][1]))
    for prim, (r, d) in singletons[:15]:
        print(f"  {r['iso']:>8} {str(prim):>10s} {r['lambda']:4d} {d:9.3f}")

    # Overall summary
    print()
    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print("  Shape substitutions test whether the BW form is geometric, not algebraic.")
    print("  If a swap (e.g. A^(2/3) → A^(1/2)) degrades sharply AND no scalar re-fit recovers it,")
    print("  then the original shape is structural — a substrate shadow, not a fitting choice.")


if __name__ == "__main__":
    main()
