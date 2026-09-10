"""Exploration v6 — locked substrate-exact BW kernel test.

Per Sean's PDF:
  Lock c_V, c_S, c_C, c_A, c_P = 8, 18, 3/4, 24, 7 (all exact substrate constants).
  Test against 69 CR242 rows, compare RMS to fitted model.
  Verify residuals localize to: H-1 edge case, Pb-208 magic closure, actinide deformation.
  Wrong controls: S=7,9; Θ=17,19; D²/R=2/3,1; c_A=21,22,25; pairing=6,8.

The four-way overdetermined identity for c_A = 24:
  24 = α_H · R   = 2 · 12
  24 = D · S     = 3 · 8
  24 = (α_H²/D) · Θ = (4/3) · 18
  24 = 2 · R
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

U_TO_MEV = float(Decimal("931.49410242"))

HERE = Path(__file__).parent
CR242 = HERE.parent / "CR242_SAM_BINDING_CURVATURE_DERIVATION" / "CR242_binding_dataset.csv"


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
            rows.append({
                "iso": r["isotope"],
                "Z": Z, "N": N, "A": A, "NmZ": N - Z,
                "B_obs_u": B,
                "B_obs_MeV": B * U_TO_MEV,
            })
    return rows


def delta_pairing(Z, N):
    """+1 even-even, -1 odd-odd, 0 odd-A. Standard BW; divided by sqrt(A) in the kernel."""
    if Z % 2 == 0 and N % 2 == 0:
        return +1
    if Z % 2 == 1 and N % 2 == 1:
        return -1
    return 0


def predict_kernel(rows, c_V, c_S, c_C, c_A, c_P):
    """B_pred = c_V·A - c_S·A^(2/3) - c_C·Z(Z-1)/A^(1/3) - c_A·(N-Z)²/A + c_P·δ/sqrt(A)

    Sign convention: c_V positive (volume binds), others subtract from binding,
    c_P adds for even-even, subtracts for odd-odd.
    """
    out = []
    for r in rows:
        Z, N, A = r["Z"], r["N"], r["A"]
        NmZ = N - Z
        vol = c_V * A
        surf = c_S * (A ** (2/3))
        coul = c_C * Z * (Z - 1) / (A ** (1/3)) if A > 0 else 0.0
        asym = c_A * (NmZ ** 2) / A if A > 0 else 0.0
        pair = c_P * delta_pairing(Z, N) / (A ** 0.5) if A > 0 else 0.0
        pred_MeV = vol - surf - coul - asym + pair
        out.append(pred_MeV)
    return out


def evaluate(rows, c_V, c_S, c_C, c_A, c_P, label):
    preds = predict_kernel(rows, c_V, c_S, c_C, c_A, c_P)
    deltas = [r["B_obs_MeV"] - p for r, p in zip(rows, preds)]
    abs_d = [abs(d) for d in deltas]
    n = len(rows)
    rms = (sum(d * d for d in deltas) / n) ** 0.5
    return {
        "label": label,
        "n": n,
        "rms": rms,
        "max_abs": max(abs_d),
        "mean_abs": sum(abs_d) / n,
        "preds": preds,
        "deltas": deltas,
    }


def main():
    rows = load_all()
    print(f"Loaded {len(rows)} CR242 rows\n")
    print(f"U_TO_MEV = {U_TO_MEV}\n")

    print("=" * 100)
    print("EXACT SUBSTRATE-LOCKED KERNEL TEST")
    print("  B_u = 8·A − 18·A^(2/3) − (3/4)·Z(Z−1)/A^(1/3) − 24·(N−Z)²/A + 7·δ/√A")
    print("  Identities for c_A = 24:")
    print("    24 = α_H·R = 2·12")
    print("    24 = D·S = 3·8")
    print("    24 = (α_H²/D)·Θ = (4/3)·18")
    print("    24 = 2·R")
    print("=" * 100)

    locked = evaluate(rows, 8, 18, 3/4, 24, 7, "LOCKED (8, 18, 3/4, 24, 7)")
    print(f"\n  LOCKED MODEL")
    print(f"    RMS      = {locked['rms']:8.4f} MeV")
    print(f"    mean|Δ|  = {locked['mean_abs']:8.4f} MeV")
    print(f"    max|Δ|   = {locked['max_abs']:8.4f} MeV")

    # Reference: re-fit for comparison
    A = np.array([r["A"] for r in rows], dtype=float)
    Z = np.array([r["Z"] for r in rows], dtype=float)
    N = np.array([r["N"] for r in rows], dtype=float)
    NmZ = N - Z
    B_obs = np.array([r["B_obs_MeV"] for r in rows], dtype=float)
    deltas_pair = np.array([delta_pairing(r["Z"], r["N"]) for r in rows], dtype=float)

    X = np.column_stack([A, -(A ** (2/3)), -Z * (Z - 1) / (A ** (1/3)),
                          -(NmZ ** 2) / A, deltas_pair / np.sqrt(A)])
    coeffs, _, _, _ = np.linalg.lstsq(X, B_obs, rcond=None)
    cV_fit, cS_fit, cC_fit, cA_fit, cP_fit = coeffs
    fit_pred = X @ coeffs
    fit_delta = B_obs - fit_pred
    fit_rms = float((fit_delta ** 2).mean() ** 0.5)
    fit_max = float(abs(fit_delta).max())

    print(f"\n  FREE-FIT REFERENCE")
    print(f"    c_V (fitted) = {cV_fit:+8.4f}  (locked: +8.0000)")
    print(f"    c_S (fitted) = {cS_fit:+8.4f}  (locked: +18.0000)")
    print(f"    c_C (fitted) = {cC_fit:+8.4f}  (locked: +0.7500)")
    print(f"    c_A (fitted) = {cA_fit:+8.4f}  (locked: +24.0000)")
    print(f"    c_P (fitted) = {cP_fit:+8.4f}  (locked: +7.0000)")
    print(f"    RMS          = {fit_rms:8.4f} MeV  (locked: {locked['rms']:.4f} MeV)")
    print(f"    max|Δ|       = {fit_max:8.4f} MeV  (locked: {locked['max_abs']:.4f} MeV)")
    print(f"    RMS degradation locked vs fitted: {locked['rms'] - fit_rms:+.4f} MeV")

    print()
    print("=" * 100)
    print("WRONG CONTROLS — perturb each substrate constant, check RMS inflates")
    print("=" * 100)
    print(f"  Reference (locked): RMS = {locked['rms']:.4f} MeV")
    print()
    print(f"  {'control':>30s} {'RMS MeV':>10s} {'max|Δ|':>10s} {'RMS ratio':>10s}")
    print("-" * 100)
    controls = [
        ("S=7  (c_V=7)",          7,    18,   3/4,  24, 7),
        ("S=9  (c_V=9)",          9,    18,   3/4,  24, 7),
        ("Θ=17 (c_S=17)",         8,    17,   3/4,  24, 7),
        ("Θ=19 (c_S=19)",         8,    19,   3/4,  24, 7),
        ("D²/R=2/3 (c_C=0.667)",  8,    18,   2/3,  24, 7),
        ("D²/R=1   (c_C=1.0)",    8,    18,   1.0,  24, 7),
        ("c_A=21",                8,    18,   3/4,  21, 7),
        ("c_A=22",                8,    18,   3/4,  22, 7),
        ("c_A=25",                8,    18,   3/4,  25, 7),
        ("pairing=6 (c_P=6)",     8,    18,   3/4,  24, 6),
        ("pairing=8 (c_P=8)",     8,    18,   3/4,  24, 8),
    ]
    for name, cv, cs, cc, ca, cp in controls:
        r = evaluate(rows, cv, cs, cc, ca, cp, name)
        ratio = r["rms"] / locked["rms"]
        print(f"  {name:>30s} {r['rms']:10.4f} {r['max_abs']:10.4f} {ratio:10.3f}×")

    print()
    print("=" * 100)
    print("PER-ROW RESIDUALS WITH LOCKED KERNEL")
    print("  (Sorted by |Δ| descending — looking for concentration at H-1, Pb-208, actinides)")
    print("=" * 100)
    annotated = []
    for r, pred, delta in zip(rows, locked["preds"], locked["deltas"]):
        category = ""
        if r["iso"] == "H-1":
            category = "← edge case (N=0)"
        elif r["iso"] == "Pb-208":
            category = "← doubly magic Z=82, N=126"
        elif r["Z"] >= 90:
            category = "← actinide"
        elif r["Z"] == 82:
            category = "← Pb magic Z"
        elif r["Z"] == 50:
            category = "← Sn magic Z"
        elif r["N"] == 126:
            category = "← N=126 magic"
        elif r["N"] == 82:
            category = "← N=82 magic"
        elif r["N"] == 50:
            category = "← N=50 magic"
        elif r["N"] == 28 or r["Z"] == 28:
            category = "← magic 28"
        elif r["N"] == 20 or r["Z"] == 20:
            category = "← magic 20"
        annotated.append({
            "iso": r["iso"], "Z": r["Z"], "N": r["N"], "A": r["A"],
            "B_obs": r["B_obs_MeV"], "B_pred": pred, "delta": delta,
            "category": category,
        })
    annotated.sort(key=lambda x: -abs(x["delta"]))

    print(f"  {'iso':>8} {'Z':>3} {'N':>3} {'A':>4} {'B_obs MeV':>11} {'B_pred MeV':>11} {'Δ MeV':>9}  category")
    for r in annotated:
        print(f"  {r['iso']:>8} {r['Z']:3d} {r['N']:3d} {r['A']:4d} "
              f"{r['B_obs']:11.4f} {r['B_pred']:11.4f} {r['delta']:+9.4f}  {r['category']}")

    print()
    print("=" * 100)
    print("RESIDUAL CONCENTRATION CHECK")
    print("=" * 100)
    # Group residuals: predicted lanes (H-1, Pb-208, actinides) vs everything else
    predicted_lanes = []
    others = []
    for r in annotated:
        if r["iso"] == "H-1" or r["iso"] == "Pb-208" or r["Z"] >= 90:
            predicted_lanes.append(r)
        else:
            others.append(r)
    pl_rms = (sum(r["delta"] ** 2 for r in predicted_lanes) / len(predicted_lanes)) ** 0.5
    other_rms = (sum(r["delta"] ** 2 for r in others) / len(others)) ** 0.5
    pl_max = max(abs(r["delta"]) for r in predicted_lanes)
    other_max = max(abs(r["delta"]) for r in others)
    print(f"  Predicted-concentration rows (H-1, Pb-208, actinides): n={len(predicted_lanes)}")
    print(f"    RMS = {pl_rms:.4f} MeV   max|Δ| = {pl_max:.4f} MeV")
    print(f"  All other rows:                                        n={len(others)}")
    print(f"    RMS = {other_rms:.4f} MeV   max|Δ| = {other_max:.4f} MeV")
    print(f"  Concentration ratio (pred_RMS / other_RMS): {pl_rms/other_rms:.3f}×")
    print()
    print(f"  If concentration is real, predicted-lane RMS >> other RMS,")
    print(f"  AND removing predicted lanes drops the overall RMS sharply.")
    rest = [r for r in annotated if r not in predicted_lanes]
    rest_rms = (sum(r["delta"] ** 2 for r in rest) / len(rest)) ** 0.5
    print(f"  Locked RMS excluding predicted-concentration rows: {rest_rms:.4f} MeV")
    print(f"    (vs full {locked['rms']:.4f} MeV)")


if __name__ == "__main__":
    main()
