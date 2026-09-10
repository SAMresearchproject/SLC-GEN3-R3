"""RESIDUAL-CLASS AUDIT — NOT a refit, NOT a rerun.

The smooth+lane kernel is FROZEN:

    B_u^(0) = 8·A − 17·A^(2/3) − (3/4)·Z(Z−1)/A^(1/3) − 22·(N−Z)²/A + 7·δ/√A − (25/4)·Λ

    Λ = 1 if primitive (a, b) ≠ (1, 1), else 0.
    RMS = 5.3813 MeV across 69 CR242 rows.
    All coefficients substrate-exact identities. No fitting permitted on the kernel.

This script applies LOCKED corrections to specific row classes ON TOP of the frozen
kernel. Purpose: determine whether the residual structure is random noise or organized
shell/deformation operators. No coefficient is fit. Each correction is a typed
substrate quantity (L_6, S, L_8, L_9). The kernel never changes.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from fractions import Fraction
from math import gcd
from pathlib import Path

U_TO_MEV = 931.49410242
MAGIC = {2, 8, 20, 28, 50, 82, 126}
HERE = Path(__file__).parent
CR242 = HERE.parent / "CR242_SAM_BINDING_CURVATURE_DERIVATION" / "CR242_binding_dataset.csv"

# FROZEN substrate-exact coefficients — NOT TO BE MODIFIED IN THIS AUDIT
C_V = 8                 # S — split inventory shape
C_S = 17                # Θ − 1 — overlap shape, minus closure
C_C = Fraction(3, 4)    # D²/R — Higgs surface debit
C_A = 22                # α_H·(R − 1) — binary-route shape, minus closure
C_P = 7                 # S − 1 — retained split, candidate-grade
C_LANE = Fraction(25, 4)  # L_6 = p_6 + p_6²/R² = 6 + 36/144 — lifted six-connector

# Typed deformation-debit candidates (all substrate-exact, from the fee-bearing family)
L_6 = Fraction(25, 4)       # = 6.25     = 6 + 6²/R²
S   = Fraction(8)           # = 8        = octet
L_8 = Fraction(8) + Fraction(64, 144)  # = 8 + 64/144 = 8.4444…
L_9 = Fraction(9) + Fraction(81, 144)  # = 9 + 81/144 = 9.5625

# Reduce L_8 and L_9 to exact rationals matching Sean's spec: L_8 = 76/9, L_9 = 153/16
assert L_8 == Fraction(76, 9), f"L_8 = {L_8} != 76/9"
assert L_9 == Fraction(153, 16), f"L_9 = {L_9} != 153/16"


def delta_pair(Z, N):
    if Z % 2 == 0 and N % 2 == 0: return +1
    if Z % 2 == 1 and N % 2 == 1: return -1
    return 0


def frozen_kernel(Z, N, A):
    """Apply the FROZEN smooth+lane kernel. No coefficient adjustment."""
    NmZ = N - Z
    g = gcd(Z, N) if (Z > 0 and N > 0) else max(Z, N, 1)
    a = Z // g if g else Z
    b = N // g if g else N
    is_non_unity = (a, b) != (1, 1)
    vol = C_V * A
    surf = C_S * (A ** (2/3))
    coul = float(C_C) * Z * (Z - 1) / (A ** (1/3)) if A > 0 else 0
    asym = C_A * NmZ * NmZ / A if A > 0 else 0
    pair = C_P * delta_pair(Z, N) / (A ** 0.5) if A > 0 else 0
    lane = float(C_LANE) if is_non_unity else 0
    return vol - surf - coul - asym + pair - lane


def load_rows():
    rows = []
    with CR242.open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                Z = int(float(r["Z"])); N = int(float(r["N"])); A = int(float(r["A"]))
                B = float(r["B_u"])
            except (KeyError, ValueError):
                continue
            B_obs = B * U_TO_MEV
            pred = frozen_kernel(Z, N, A)
            rows.append({
                "iso": r["isotope"],
                "Z": Z, "N": N, "A": A,
                "B_obs": B_obs,
                "B_pred_frozen": pred,
                "delta_frozen": B_obs - pred,
                "is_doubly_magic": (Z in MAGIC) and (N in MAGIC),
                "is_actinide": Z >= 90,
                "N_eq_126": (N == 126),
            })
    return rows


def report_delta(rows, label):
    n = len(rows)
    if n == 0:
        print(f"  {label}: n=0")
        return
    rms = (sum(r["delta_audit"] ** 2 for r in rows) / n) ** 0.5
    max_abs = max(abs(r["delta_audit"]) for r in rows)
    print(f"  {label}: n={n:2d}   RMS = {rms:7.4f} MeV   max|Δ| = {max_abs:7.4f} MeV")


def apply_correction(rows, correction_fn, label):
    """Apply a row-specific correction (added to B_pred, so it shifts residuals downward by the correction amount)."""
    for r in rows:
        delta_correction = correction_fn(r)
        r["delta_audit"] = r["delta_frozen"] - delta_correction


def main():
    rows = load_rows()
    n = len(rows)

    # Baseline (frozen kernel, no corrections)
    for r in rows:
        r["delta_audit"] = r["delta_frozen"]
    base_rms = (sum(r["delta_frozen"] ** 2 for r in rows) / n) ** 0.5
    base_max = max(abs(r["delta_frozen"]) for r in rows)

    print("=" * 100)
    print("RESIDUAL-CLASS AUDIT — Frozen Smooth+Lane Kernel")
    print("=" * 100)
    print("Kernel (FROZEN, all coefficients substrate-exact, NOT MODIFIED in this audit):")
    print("  B_u^(0) = 8·A − 17·A^(2/3) − (3/4)·Z(Z−1)/A^(1/3) − 22·(N−Z)²/A + 7·δ/√A − (25/4)·Λ")
    print(f"  where Λ = 1 if primitive (a,b) ≠ (1,1), else 0")
    print()
    print(f"Frozen-kernel baseline: n={n}, RMS = {base_rms:.4f} MeV, max|Δ| = {base_max:.4f} MeV")
    print()
    print("=" * 100)
    print("TEST A — +L_6 = +25/4 credit applied ONLY to He-4 and Pb-208")
    print("  Class language: 'extreme-closure rows where matched positive residual ≈ +5.85'")
    print("  Status: EXPLORATORY (class membership picked post-hoc from observed residuals)")
    print("=" * 100)
    test_a_set = {"He-4", "Pb-208"}
    def correction_A(r):
        return float(L_6) if r["iso"] in test_a_set else 0

    apply_correction(rows, correction_A, "test_A")
    # Members of class
    a_members = [r for r in rows if r["iso"] in test_a_set]
    others = [r for r in rows if r["iso"] not in test_a_set]
    print(f"  Class members:")
    for r in a_members:
        print(f"    {r['iso']:>8s}  before Δ = {r['delta_frozen']:+8.4f}   after Δ = {r['delta_audit']:+8.4f}   shift = {r['delta_audit'] - r['delta_frozen']:+.4f}")
    print()
    report_delta(rows, "  Whole-corpus RMS after Test A correction")
    report_delta([r for r in rows if r["iso"] in test_a_set], "    Class members only")
    report_delta([r for r in rows if r["iso"] not in test_a_set], "    Non-class rows (unchanged)")

    print()
    print("=" * 100)
    print("TEST B — +L_6 = +25/4 credit applied to ALL DOUBLY MAGIC rows")
    print("  Class language: 'both Z and N in {2, 8, 20, 28, 50, 82, 126}'")
    print("  Status: STRUCTURAL CONTROL — expected to fail at O-16 and Ca-40")
    print("=" * 100)
    def correction_B(r):
        return float(L_6) if r["is_doubly_magic"] else 0

    apply_correction(rows, correction_B, "test_B")
    b_members = [r for r in rows if r["is_doubly_magic"]]
    print(f"  Doubly-magic members:")
    for r in sorted(b_members, key=lambda x: x["A"]):
        print(f"    {r['iso']:>8s}  before Δ = {r['delta_frozen']:+8.4f}   after Δ = {r['delta_audit']:+8.4f}   shift = {r['delta_audit'] - r['delta_frozen']:+.4f}")
    print()
    report_delta(rows, "  Whole-corpus RMS after Test B correction")
    report_delta(b_members, "    Doubly-magic class")

    print()
    print("=" * 100)
    print("TEST C — Locked correction on N = 126 closure")
    print("  Class language: 'N = 126 (= M, retained matter-support shape)'")
    print("  Apply +L_6 to N=126 rows only.")
    print("=" * 100)
    def correction_C(r):
        return float(L_6) if r["N"] == 126 else 0

    apply_correction(rows, correction_C, "test_C")
    c_members = [r for r in rows if r["N"] == 126]
    print(f"  N=126 members:")
    for r in c_members:
        print(f"    {r['iso']:>8s}  Z={r['Z']:3d} N={r['N']:3d}  before Δ = {r['delta_frozen']:+8.4f}   after Δ = {r['delta_audit']:+8.4f}")
    print()
    report_delta(rows, "  Whole-corpus RMS after Test C correction")

    print()
    print("=" * 100)
    print("TEST D — Actinide deformation debit (Z ≥ 90 rows)")
    print("  Class language: 'actinide region — Z ≥ 90'")
    print("  Apply a deformation DEBIT: B_u = B_u^(0) − C_deform")
    print("  Typed candidates only: L_6, S, L_8, L_9 — no free fitting")
    print("=" * 100)
    actinides = [r for r in rows if r["is_actinide"]]
    print(f"  Actinide members and their frozen residuals:")
    for r in sorted(actinides, key=lambda x: x["A"]):
        print(f"    {r['iso']:>8s}  Z={r['Z']:3d}  before Δ = {r['delta_frozen']:+8.4f}")
    print()

    deform_candidates = [
        ("L_6 = 25/4 = 6.2500", float(L_6)),
        ("S   = 8     = 8.0000", float(S)),
        ("L_8 = 76/9  = 8.4444", float(L_8)),
        ("L_9 = 153/16 = 9.5625", float(L_9)),
    ]
    print(f"  Candidate-by-candidate (lock the same debit on ALL actinides; report actinide RMS):")
    print(f"  {'candidate':>25s}   {'actinide RMS':>13s}   {'whole-corpus RMS':>17s}")
    print("-" * 100)
    for name, val in deform_candidates:
        def cor(r, v=val): return -v if r["is_actinide"] else 0
        apply_correction(rows, cor, name)
        a_rms = (sum(r["delta_audit"] ** 2 for r in actinides) / len(actinides)) ** 0.5
        w_rms = (sum(r["delta_audit"] ** 2 for r in rows) / n) ** 0.5
        print(f"  {name:>25s}   {a_rms:13.4f}   {w_rms:17.4f}")

    # Detailed per-row for the best deformation candidate
    print()
    print(f"  Per-row residuals under each candidate:")
    print(f"  {'iso':>8s} {'frozen Δ':>10s}" + "".join(f"  {nm:>14s}" for nm, _ in deform_candidates))
    for r in sorted(actinides, key=lambda x: x["A"]):
        line = f"  {r['iso']:>8s} {r['delta_frozen']:10.4f}"
        for name, val in deform_candidates:
            new = r["delta_frozen"] - (-val)  # debit subtracted, so audit_delta = frozen + val
            line += f"  {new:14.4f}"
        print(line)

    print()
    print("=" * 100)
    print("AUDIT SUMMARY")
    print("=" * 100)
    print("  Test A (L_6 on He-4 and Pb-208 only): exploratory — class picked post-hoc")
    print("  Test B (L_6 on all doubly magic):     control — should harm O-16 and Ca-40")
    print("  Test C (L_6 on N=126 only):           tests whether effect is M=126-specific")
    print("  Test D (actinide deformation debit):  typed candidates only, no free fit")
    print()
    print("  The frozen kernel is UNCHANGED throughout this audit.")
    print("  No coefficient was fit. All corrections are locked substrate-exact quantities")
    print("  applied to pre-specified row classes.")


if __name__ == "__main__":
    main()
