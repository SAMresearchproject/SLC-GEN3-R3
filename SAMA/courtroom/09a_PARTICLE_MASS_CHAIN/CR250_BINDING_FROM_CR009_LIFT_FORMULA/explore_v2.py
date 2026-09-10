"""Exploration v2 — exact Fraction arithmetic, CODATA MeV/u, two-term candidates.

Builds on v1 findings:
  - sign rule by A-window closes 92.5%
  - Z linear beats (N-Z) linear (RMS 29 vs 40 MeV)
  - magnitude residual has structured shape (mid-A undershoots, post-Au overshoots)
  - heavy region eff_q clusters near ℱ·S = 648

v2 tests Z + A^(2/3) two-term form and per-counting-rule back-solves.
Uses Decimal at 50 digits for A^(2/3) (irrational), Fraction everywhere else.
"""
from __future__ import annotations

import csv
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 50

# Substrate atoms — exact rationals
R = Fraction(12)
D = Fraction(3)
S = Fraction(8)
ALPHA_H = Fraction(2)
THETA = Fraction(18)
F = Fraction(81)         # ℱ
V = Fraction(27)
M_CONST = Fraction(126)
L_CONST = Fraction(162)
KAPPA = Fraction(7117, 768)
G = Fraction(1, 64)
R2 = R * R
R3 = R * R * R
R4 = R * R * R * R       # 20736
MU_Q = Fraction(192, 7117)

# CODATA 2018 — atomic mass unit in MeV/c²
U_TO_MEV = Decimal("931.49410242")

DATASET = Path(__file__).parent.parent / "CR242_SAM_BINDING_CURVATURE_DERIVATION" / "CR242_binding_dataset.csv"


def dec_from_str(s: str) -> Decimal:
    """Parse a high-precision string from the CSV into Decimal."""
    return Decimal(s.strip())


def u_to_mev(u: Decimal) -> Decimal:
    return u * U_TO_MEV


def mev_to_u(mev: Decimal) -> Decimal:
    return mev / U_TO_MEV


def frac_to_dec(f: Fraction) -> Decimal:
    return Decimal(f.numerator) / Decimal(f.denominator)


def load() -> list[dict]:
    """Load CR242 dataset, keep B_u at full Decimal precision."""
    rows = []
    with DATASET.open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                Z = int(float(r["Z"]))
                N = int(float(r["N"]))
                A = int(float(r["A"]))
                B_str = r["B_u"]
                B_dec = dec_from_str(B_str)
            except (KeyError, ValueError):
                continue
            if N < Z:
                continue
            rows.append({
                "iso": r["isotope"],
                "Z": Z, "N": N, "A": A, "NmZ": N - Z,
                "B_obs_u": B_dec,
                "B_obs_MeV": u_to_mev(B_dec),
                "A_two_thirds": Decimal(A) ** (Decimal(2) / Decimal(3)),
                "A_one_third": Decimal(A) ** (Decimal(1) / Decimal(3)),
            })
    return rows


# Sign rules ---------------------------------------------------------------
def sign_observed(row):
    return Decimal(1) if row["B_obs_u"] >= 0 else Decimal(-1)


def sign_naive_R1(row):
    return Decimal(1)


def sign_iron_peak_window(row):
    """A < 16 or A >= 210 → credit, else debit."""
    if row["A"] < 16:
        return Decimal(-1)
    if row["A"] >= 210:
        return Decimal(-1)
    return Decimal(1)


# Counting rules ----------------------------------------------------------
def count_NmZ(row):
    return Decimal(row["NmZ"])

def count_A(row):
    return Decimal(row["A"])

def count_Z(row):
    return Decimal(row["Z"])

def count_A_two_thirds(row):
    return row["A_two_thirds"]


# Single-term prediction --------------------------------------------------
def per_link_u(q: Fraction) -> Decimal:
    """(q + D) / R^4 * mu_Q in atomic mass units."""
    return frac_to_dec((q + D) / R4 * MU_Q)


def predict_single_term(row, sign_rule, count_rule, q):
    sign = sign_rule(row)
    n = count_rule(row)
    pl = per_link_u(q)
    return sign * n * pl


# Two-term prediction (Z + A^(2/3)) --------------------------------------
def predict_two_term(row, sign_rule, q_Z, q_A23):
    """B_pred = sign × [Z · per_link(q_Z) + A^(2/3) · per_link(q_A23)]"""
    sign = sign_rule(row)
    z_term = Decimal(row["Z"]) * per_link_u(q_Z)
    surf_term = row["A_two_thirds"] * per_link_u(q_A23)
    return sign * (z_term + surf_term)


# Evaluation ---------------------------------------------------------------
def evaluate(rows, predict_fn, label):
    deltas = []
    sign_hits = 0
    for r in rows:
        pred = predict_fn(r)
        obs = r["B_obs_u"]
        delta = obs - pred
        deltas.append((r, pred, delta))
        # sign check (treat 0 as positive)
        if (pred >= 0) == (obs >= 0):
            sign_hits += 1
    n = len(rows)
    abs_MeV = [abs(d) * U_TO_MEV for _, _, d in deltas]
    max_abs_MeV = max(abs_MeV)
    mean_abs_MeV = sum(abs_MeV) / Decimal(n)
    sum_sq = sum(d * d for _, _, d in deltas)
    rms_u = (sum_sq / Decimal(n)).sqrt()
    rms_MeV = rms_u * U_TO_MEV
    return {
        "label": label,
        "n": n,
        "sign_hits": sign_hits,
        "sign_acc": Decimal(sign_hits) / Decimal(n),
        "max_abs_MeV": max_abs_MeV,
        "mean_abs_MeV": mean_abs_MeV,
        "rms_MeV": rms_MeV,
        "deltas": deltas,
    }


def fmt(d: Decimal, places: int = 3) -> str:
    quant = Decimal("0." + "0" * places) if places > 0 else Decimal("1")
    return f"{d.quantize(quant)}"


# Back-solve q under a given (sign, count) rule --------------------------
def backsolve_q(rows, sign_rule, count_rule):
    """For each row: what q would close exactly?
    sign × n × (q + D)/R^4 × mu_Q = B_obs
    (q + D) = |B_obs| × R^4 / (n × mu_Q)
    """
    out = []
    for r in rows:
        n = count_rule(r)
        if n == 0:
            out.append((r, None, None))
            continue
        b_abs = abs(r["B_obs_u"])
        eff_qpD_dec = b_abs * frac_to_dec(R4) / (n * frac_to_dec(MU_Q))
        eff_q_dec = eff_qpD_dec - frac_to_dec(D)
        out.append((r, eff_qpD_dec, eff_q_dec))
    return out


def main():
    rows = load()
    n = len(rows)
    print(f"Loaded {n} N>=Z nuclei from CR242 (exact Decimal precision, 50 digits)\n")
    print(f"CODATA U_TO_MEV = {U_TO_MEV}")
    print(f"Per-link value at q=647 (Au cascade) = {fmt(per_link_u(Fraction(647)), 12)} u "
          f"= {fmt(per_link_u(Fraction(647)) * U_TO_MEV, 6)} MeV\n")

    print("=" * 100)
    print("PHASE A: Sign rule comparison (R1 magnitude, q=647, count=(N-Z))")
    print("=" * 100)
    for name, rule in [
        ("R1_naive_always_positive", sign_naive_R1),
        ("iron_peak_window", sign_iron_peak_window),
    ]:
        result = evaluate(rows,
                          lambda r, sr=rule: predict_single_term(r, sr, count_NmZ, Fraction(647)),
                          name)
        print(f"  {name:30s} sign_acc={fmt(result['sign_acc']*Decimal(100), 1)}%  "
              f"max|Δ|={fmt(result['max_abs_MeV'], 2):>8s} MeV  "
              f"RMS={fmt(result['rms_MeV'], 2):>7s} MeV")

    print()
    print("=" * 100)
    print("PHASE B: Counting rule comparison (perfect sign, q=647)")
    print("=" * 100)
    count_rules = [
        ("(N-Z) linear",     count_NmZ),
        ("Z linear",         count_Z),
        ("A linear",         count_A),
        ("A^(2/3) surface",  count_A_two_thirds),
    ]
    for name, rule in count_rules:
        result = evaluate(rows,
                          lambda r, cr=rule: predict_single_term(r, sign_observed, cr, Fraction(647)),
                          name)
        print(f"  {name:25s} max|Δ|={fmt(result['max_abs_MeV'], 2):>8s} MeV  "
              f"mean|Δ|={fmt(result['mean_abs_MeV'], 2):>7s} MeV  "
              f"RMS={fmt(result['rms_MeV'], 2):>7s} MeV")

    print()
    print("=" * 100)
    print("PHASE C: Single-term back-solve — what q does each row need?")
    print("         (sign=iron_peak_window; counting=(N-Z))")
    print("=" * 100)
    print("  Showing only heavy rows (A >= 50) for clean readout")
    print(f"  {'iso':>8} {'Z':>4} {'A':>4} {'N-Z':>4} {'B_obs MeV':>11} {'eff q+D':>11} {'eff q':>11} {'q/ℱ':>8} {'q/(ℱ·S)':>10}")
    print("-" * 100)
    bs = backsolve_q(rows, sign_iron_peak_window, count_NmZ)
    F_dec = frac_to_dec(F)
    FS_dec = frac_to_dec(F * S)
    for r, eff_qpD, eff_q in bs:
        if r["A"] < 50:
            continue
        if eff_q is None:
            continue
        print(f"  {r['iso']:>8} {r['Z']:4d} {r['A']:4d} {r['NmZ']:4d} "
              f"{fmt(r['B_obs_MeV'], 3):>11s} "
              f"{fmt(eff_qpD, 1):>11s} {fmt(eff_q, 1):>11s} "
              f"{fmt(eff_q/F_dec, 3):>8s} {fmt(eff_q/FS_dec, 4):>10s}")

    print()
    print("=" * 100)
    print("PHASE D: Back-solve under Z linear counting (heavy rows)")
    print("=" * 100)
    print(f"  {'iso':>8} {'Z':>4} {'A':>4} {'B_obs MeV':>11} {'eff q+D':>11} {'eff q':>11} {'q/D':>8} {'q/R':>8} {'q/ℱ':>8}")
    print("-" * 100)
    bs_Z = backsolve_q(rows, sign_iron_peak_window, count_Z)
    D_dec = frac_to_dec(D)
    R_dec = frac_to_dec(R)
    for r, eff_qpD, eff_q in bs_Z:
        if r["A"] < 50:
            continue
        if eff_q is None:
            continue
        print(f"  {r['iso']:>8} {r['Z']:4d} {r['A']:4d} "
              f"{fmt(r['B_obs_MeV'], 3):>11s} "
              f"{fmt(eff_qpD, 2):>11s} {fmt(eff_q, 2):>11s} "
              f"{fmt(eff_q/D_dec, 2):>8s} {fmt(eff_q/R_dec, 2):>8s} {fmt(eff_q/F_dec, 3):>8s}")

    print()
    print("=" * 100)
    print("PHASE E: Back-solve under A^(2/3) surface counting (all rows with positive B_obs)")
    print("=" * 100)
    print(f"  {'iso':>8} {'A':>4} {'A^(2/3)':>10} {'B_obs MeV':>11} {'eff q+D':>11} {'eff q':>11} {'q/D':>8} {'q/R':>8}")
    print("-" * 100)
    bs_surf = backsolve_q(rows, sign_iron_peak_window, count_A_two_thirds)
    for r, eff_qpD, eff_q in bs_surf:
        if r["B_obs_u"] < 0:
            continue
        if eff_q is None:
            continue
        print(f"  {r['iso']:>8} {r['A']:4d} "
              f"{fmt(r['A_two_thirds'], 4):>10s} "
              f"{fmt(r['B_obs_MeV'], 3):>11s} "
              f"{fmt(eff_qpD, 3):>11s} {fmt(eff_q, 3):>11s} "
              f"{fmt(eff_q/D_dec, 3):>8s} {fmt(eff_q/R_dec, 3):>8s}")

    print()
    print("=" * 100)
    print("PHASE F: Two-term (Z + A^(2/3)) search — try fixed q_Z and q_A23 combinations")
    print("=" * 100)
    print("  Tries combinations of substrate-named q values for both terms")
    print()
    q_candidates = [
        ("q=D", Fraction(3)),
        ("q=αH²", Fraction(4)),
        ("q=R/2", Fraction(6)),
        ("q=S-1", Fraction(7)),
        ("q=S", Fraction(8)),
        ("q=D²", Fraction(9)),
        ("q=R", Fraction(12)),
        ("q=Θ", Fraction(18)),
        ("q=V", Fraction(27)),
        ("q=ℱ", Fraction(81)),
        ("q=M", Fraction(126)),
        ("q=L", Fraction(162)),
        ("q=ℱ·S-1=647", Fraction(647)),
        ("q=ℱ·S=648", Fraction(648)),
    ]
    print(f"  Top 10 best (Z, A^(2/3)) combinations by RMS:")
    print()
    results = []
    for z_name, q_Z in q_candidates:
        for a_name, q_A in q_candidates:
            label = f"Z·({z_name}) + A^(2/3)·({a_name})"
            result = evaluate(rows,
                              lambda r, qz=q_Z, qa=q_A: predict_two_term(r, sign_iron_peak_window, qz, qa),
                              label)
            results.append(result)
    results.sort(key=lambda x: x["rms_MeV"])
    print(f"  {'rank':>4} {'label':<60s} {'sign%':>6} {'max|Δ| MeV':>10} {'RMS MeV':>8}")
    for i, r in enumerate(results[:10], 1):
        print(f"  {i:>4} {r['label']:<60s} "
              f"{fmt(r['sign_acc']*Decimal(100), 1):>6s} "
              f"{fmt(r['max_abs_MeV'], 2):>10s} "
              f"{fmt(r['rms_MeV'], 2):>8s}")

    print()
    print("  Bottom 5 (worst):")
    for i, r in enumerate(results[-5:], len(results)-4):
        print(f"  {i:>4} {r['label']:<60s} "
              f"{fmt(r['sign_acc']*Decimal(100), 1):>6s} "
              f"{fmt(r['max_abs_MeV'], 2):>10s} "
              f"{fmt(r['rms_MeV'], 2):>8s}")

    print()
    print("=" * 100)
    print("PHASE G: Detail on best two-term combo")
    print("=" * 100)
    best = results[0]
    print(f"  Best: {best['label']}")
    print(f"  Sign accuracy: {fmt(best['sign_acc']*Decimal(100), 1)}%  ({best['sign_hits']}/{best['n']})")
    print(f"  RMS: {fmt(best['rms_MeV'], 3)} MeV")
    print(f"  max |Δ|: {fmt(best['max_abs_MeV'], 3)} MeV")
    print()
    print(f"  {'iso':>8} {'A':>4} {'N-Z':>4} {'B_obs MeV':>11} {'B_pred MeV':>11} {'Δ MeV':>9}")
    print("-" * 80)
    for r, pred, delta in sorted(best["deltas"], key=lambda x: x[0]["A"]):
        print(f"  {r['iso']:>8} {r['A']:4d} {r['NmZ']:4d} "
              f"{fmt(r['B_obs_MeV'], 3):>11s} {fmt(pred*U_TO_MEV, 3):>11s} {fmt(delta*U_TO_MEV, 3):>9s}")


if __name__ == "__main__":
    main()
