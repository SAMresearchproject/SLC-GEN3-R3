"""Exploration v8 — corrected connector taxonomy.

Per Sean's PDF:
  F = 81 = half-ledger face shape (not a charged connector)
  Θ = 18 = α_H·D² = universal connector, NO FEE
  p ∈ {1, 2, 3, 4, 6, 8, 9, 12} = fee-bearing connector family
    L_p = p + p²/R²  (lifted connector value)
    f_p = p²/R²       (route-square surcharge / actual fee)

The per-lane residual ~6 MeV observed in v7 is NOT Θ/D = 6 (that would be dimension-
slicing the universal connector). The right candidates are:
  C_lane = p_6 = 6        (six-connector shape, exact)
  C_lane = L_6 = 25/4 = 6.25  (lifted six-connector)

Test: add this as a per-row connector-shape debit and see if MINUS-1 model RMS drops.

Multiple interpretations of "−6Λ" or "−25/4·Λ" to try:
  • Constant -6 per non-(1,1) lane row
  • -6 · λ (gcd-scaled)
  • -6 · √λ
  • -6 · (b-a) (lane unit)
  • -L_6 = -6.25 variants
"""
from __future__ import annotations

import csv
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
            a = Z // g if g else Z
            b = N // g if g else N
            rows.append({
                "iso": r["isotope"],
                "Z": Z, "N": N, "A": A, "NmZ": N - Z,
                "B_obs": B * U_TO_MEV,
                "lambda": g,
                "a": a, "b": b,
                "primitive": (a, b),
            })
    return rows


def delta_pair(Z, N):
    if Z % 2 == 0 and N % 2 == 0: return +1
    if Z % 2 == 1 and N % 2 == 1: return -1
    return 0


def predict_bw(row, c_V, c_S, c_C, c_A, c_P):
    Z, N, A = row["Z"], row["N"], row["A"]
    NmZ = N - Z
    vol = c_V * A
    surf = c_S * (A ** (2/3))
    coul = c_C * Z * (Z - 1) / (A ** (1/3)) if A > 0 else 0
    asym = c_A * NmZ * NmZ / A if A > 0 else 0
    pair = c_P * delta_pair(Z, N) / (A ** 0.5) if A > 0 else 0
    return vol - surf - coul - asym + pair


def evaluate_with_debit(rows, c_V, c_S, c_C, c_A, c_P, debit_fn, label):
    """debit_fn(row) returns the extra debit to subtract from B_pred for that row."""
    deltas = []
    for r in rows:
        pred = predict_bw(r, c_V, c_S, c_C, c_A, c_P)
        debit = debit_fn(r)
        pred_adj = pred - debit
        deltas.append(r["B_obs"] - pred_adj)
    n = len(rows)
    rms = (sum(d * d for d in deltas) / n) ** 0.5
    max_abs = max(abs(d) for d in deltas)
    return {"label": label, "rms": rms, "max_abs": max_abs, "deltas": deltas}


def main():
    rows = load()
    print(f"Loaded {len(rows)} CR242 rows\n")

    # MINUS-1 baseline coefficients (substrate-derived with -1 closure)
    cV, cS, cC, cA, cP = 8, 17, 3/4, 22, 7

    print("=" * 100)
    print("BASELINE — MINUS-1 model (8, 17, 3/4, 22, 7), no extra debit")
    print("=" * 100)
    baseline = evaluate_with_debit(rows, cV, cS, cC, cA, cP, lambda r: 0, "baseline")
    print(f"  RMS = {baseline['rms']:.4f} MeV  max|Δ| = {baseline['max_abs']:.4f} MeV")
    print()

    # Show the per-lane residual structure
    by_prim = defaultdict(list)
    for r, d in zip(rows, baseline["deltas"]):
        by_prim[r["primitive"]].append((r, d))

    print("=" * 100)
    print("PER-LANE RESIDUAL OFFSET — MINUS-1 baseline")
    print("=" * 100)
    print(f"  {'primitive':>12s} {'n':>3s} {'mean residual':>14s} {'lane (b-a)':>10}")
    for prim in sorted(by_prim.keys(), key=lambda p: -len(by_prim[p])):
        members = by_prim[prim]
        mean_d = sum(d for _, d in members) / len(members)
        if len(members) >= 2:
            print(f"  {str(prim):>12s} {len(members):3d} {mean_d:14.3f}     {prim[1] - prim[0]:5d}")

    print()
    print("=" * 100)
    print("DEBIT CANDIDATE TESTS — applied only to non-(1,1) lanes (per Sean's PDF)")
    print("  Apply C_lane debit to each row; check RMS drop and per-lane mean.")
    print("=" * 100)

    def non_unity(r): return r["primitive"] != (1, 1)

    candidates = [
        # Sean's two named candidates: -6 and -6.25 (p_6 and L_6)
        ("DEBIT 0 (baseline)",              lambda r: 0),
        ("DEBIT -6 (p_6) constant non-(1,1)",       lambda r: -6 if non_unity(r) else 0),
        ("DEBIT -6.25 (L_6) constant non-(1,1)",    lambda r: -6.25 if non_unity(r) else 0),
        ("DEBIT -6·λ non-(1,1)",                    lambda r: -6 * r["lambda"] if non_unity(r) else 0),
        ("DEBIT -6·sqrt(λ) non-(1,1)",              lambda r: -6 * sqrt(r["lambda"]) if non_unity(r) else 0),
        ("DEBIT -6·(b-a) non-(1,1)",                lambda r: -6 * (r["b"] - r["a"]) if non_unity(r) else 0),
        ("DEBIT -6·A^(1/3) non-(1,1)",              lambda r: -6 * (r["A"] ** (1/3)) if non_unity(r) else 0),
        ("DEBIT -6.25·sqrt(λ) non-(1,1)",           lambda r: -6.25 * sqrt(r["lambda"]) if non_unity(r) else 0),
        # Wrong controls — should degrade if shape is real
        ("WRONG: -6 ALL rows (including (1,1))",    lambda r: -6),
        ("WRONG: -8 constant non-(1,1)",            lambda r: -8 if non_unity(r) else 0),
        ("WRONG: -10 constant non-(1,1)",           lambda r: -10 if non_unity(r) else 0),
        ("WRONG: +6 (sign flip) non-(1,1)",         lambda r: +6 if non_unity(r) else 0),
    ]

    print(f"  {'candidate':>50s}  {'RMS MeV':>8s}  {'max|Δ| MeV':>10s}  {'Δ from baseline':>16s}")
    print("-" * 100)
    base_rms = baseline["rms"]
    for label, fn in candidates:
        result = evaluate_with_debit(rows, cV, cS, cC, cA, cP, fn, label)
        delta_rms = result["rms"] - base_rms
        sign = "✓ better" if delta_rms < -0.1 else ("≈ same" if abs(delta_rms) < 0.1 else "✗ worse")
        print(f"  {label:>50s}  {result['rms']:8.4f}  {result['max_abs']:10.4f}  {delta_rms:+16.3f}  {sign}")

    # Now the best — apply -6 constant non-(1,1) and show per-lane structure
    print()
    print("=" * 100)
    print("WITH BEST DEBIT — show per-lane residuals after correction")
    print("=" * 100)
    # Determine best constant-non-(1,1) debit by sweep
    print(f"\n  Best-debit sweep: -X non-(1,1), X ∈ {{4, 5, 5.5, 6, 6.25, 6.5, 7, 8}}:")
    print(f"  {'debit':>10s} {'RMS MeV':>8s}")
    best_rms = 1e9; best_debit = 0
    for X in [4, 5, 5.5, 6, 6.25, 6.5, 7, 8]:
        result = evaluate_with_debit(rows, cV, cS, cC, cA, cP,
                                     lambda r, x=X: -x if non_unity(r) else 0, f"-{X}")
        print(f"  {-X:10.3f} {result['rms']:8.4f}")
        if result["rms"] < best_rms:
            best_rms = result["rms"]; best_debit = -X

    # Apply best, show per-lane
    print(f"\n  Best constant non-(1,1) debit: {best_debit} MeV → RMS {best_rms:.4f} MeV")
    result = evaluate_with_debit(rows, cV, cS, cC, cA, cP,
                                 lambda r, x=best_debit: x if non_unity(r) else 0, f"best")
    by_prim_after = defaultdict(list)
    for r, d in zip(rows, result["deltas"]):
        by_prim_after[r["primitive"]].append((r, d))
    print(f"\n  Per-lane mean residual AFTER best constant debit:")
    print(f"  {'primitive':>12s} {'n':>3s} {'before mean':>12s} {'after mean':>12s}")
    for prim in sorted(by_prim.keys(), key=lambda p: -len(by_prim[p])):
        before = sum(d for _, d in by_prim[prim]) / len(by_prim[prim])
        after = sum(d for _, d in by_prim_after[prim]) / len(by_prim_after[prim])
        if len(by_prim[prim]) >= 2:
            print(f"  {str(prim):>12s} {len(by_prim[prim]):3d} {before:12.3f} {after:12.3f}")

    # Now also test the corrected MODEL (no Θ as surface, use a fee-bearing connector instead)
    print()
    print("=" * 100)
    print("CORRECTED SURFACE COEFFICIENT — try fee-bearing p-family for c_S")
    print("  If Θ=18 is the no-fee universal connector, c_S = Θ-1 was wrong typing.")
    print("  Try c_S as a fee-bearing connector p ∈ {12, L_12, 9+8, ...}")
    print("=" * 100)
    print(f"  {'c_S candidate':>30s} {'RMS MeV':>8s}  {'max|Δ| MeV':>10s}")
    surface_candidates = [
        ("17 (Θ-1, original MINUS-1)", 17),
        ("18 (Θ, locked)",              18),
        ("12 (p_12 = R)",               12),
        ("12.25 (L_12 = R + R²/R²)",   12 + 144/144),  # = 13
        ("8 (p_8 = S)",                 8),
        ("8.44 (L_8 = 8 + 64/144)",    8 + 64/144),
        ("9 (p_9 = D²)",                9),
        ("9.5625 (L_9 = 9 + 81/144)", 9 + 81/144),
        ("16 (S + S = 2·S)",            16),
        ("R+S = 20",                    20),
        ("L_12 = 13 exactly (R+1)",    13),
    ]
    for name, cs_val in surface_candidates:
        result = evaluate_with_debit(rows, cV, cs_val, cC, cA, cP, lambda r: 0, name)
        print(f"  {name:>30s} {result['rms']:8.4f}  {result['max_abs']:10.4f}")

    # And c_A: search the fee-bearing family for asymmetry
    print()
    print("=" * 100)
    print("CORRECTED ASYMMETRY COEFFICIENT — try fee-bearing connectors for c_A")
    print("  c_A near 22-23 was found; check substrate-named alternatives in p-family.")
    print("=" * 100)
    print(f"  {'c_A candidate':>40s} {'RMS MeV':>8s}  {'max|Δ| MeV':>10s}")
    asym_candidates = [
        ("22 (2·(R-1), MINUS-1)",       22),
        ("23 (α_H·R-1, BEST)",          23),
        ("24 (α_H·R)",                   24),
        ("12+12 = 2R",                  24),
        ("L_12+L_12 = 26",              26),
        ("L_9 + L_12 = 22.5625",       9 + 81/144 + 13),
        ("p_12 + p_8 + p_2 = 22",       22),
        ("Θ + α_H² = 22",               22),
        ("Θ + S = 26",                  26),
        ("p_6 + p_6 + p_6 + p_6 = 24", 24),
    ]
    for name, ca_val in asym_candidates:
        result = evaluate_with_debit(rows, cV, cS, cC, ca_val, cP, lambda r: 0, name)
        print(f"  {name:>40s} {result['rms']:8.4f}  {result['max_abs']:10.4f}")


if __name__ == "__main__":
    main()
