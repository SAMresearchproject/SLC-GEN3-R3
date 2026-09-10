"""
Phase 1: Verify scratchpad cipher across all 55 CR261 isotopes.

Cipher (from second-set-of-eyes scratchpad, verified 2026-07-01):
  G_p = 9.0625                    (proton carrier tensor support)
  G_e = 0.188802083333             (electron carrier tensor support)
  G_n = 0.015625 = 1/64            (neutron carrier tensor support)

For each neutral isotope:
  G(P) = Z·(G_p + G_e) + N·G_n
  Q_mass = 4·A·(7117/768)
  Q_sub  = 8·G(P)
  F_conn = Q_mass - Q_sub          (should equal (N-Z)·(7093/192))

Expected: F_conn_actual = F_conn_expected exactly for all rows.
If any deviates, the cipher needs adjustment.

References:
  - CR220 candidate rows QP093A-0115, QP093A-0003, QP093A-0002
  - CR245 asymmetry identity theorem-grade
  - CR269 bow 1/8 : 7/8 partition
  - CR261_bw_fit_per_row.csv fit data
"""

import csv
import math
import os
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
FIT_CSV = os.path.join(HERE, "CR261_bw_fit_per_row.csv")

# Cipher constants (from CR220 particle rows)
G_p = Fraction(145, 16)              # 9.0625 = 145/16
G_e = Fraction(145, 768)             # 0.188802083 = 145/768
G_n = Fraction(1, 64)                # 0.015625 = 1/64

# Substrate constants
KAPPA_NUM = 7117
KAPPA_DEN = 768
GAP_NUM = 7093
GAP_DEN = 192


def load_data():
    rows = []
    with open(FIT_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "set": row["set"],
                "isotope": row["isotope"],
                "Z": int(row["Z"]),
                "N": int(row["N"]),
                "A": int(row["A"]),
                "B_u_obs": float(row["B_u_obs_MeV"]),
                "B_u_pred_CR261": float(row["B_u_pred_MeV"]),
                "residual_CR261": float(row["residual_MeV"]),
            })
    return rows


def compute_cipher(Z, N, A):
    """Apply scratchpad cipher exactly using rational arithmetic."""
    # G(P) = Z·(G_p + G_e) + N·G_n
    G_P = Z * (G_p + G_e) + N * G_n
    # Q_mass = 4·A·(7117/768)
    Q_mass = Fraction(4 * A * KAPPA_NUM, KAPPA_DEN)
    # Q_sub = 8·G(P)
    Q_sub = 8 * G_P
    # F_conn actual
    F_conn_actual = Q_mass - Q_sub
    # F_conn expected = (N-Z)·(7093/192)
    F_conn_expected = Fraction((N - Z) * GAP_NUM, GAP_DEN)
    # Deviation
    deviation = F_conn_actual - F_conn_expected
    return dict(
        G_P=G_P,
        Q_mass=Q_mass,
        Q_sub=Q_sub,
        F_conn_actual=F_conn_actual,
        F_conn_expected=F_conn_expected,
        deviation=deviation,
    )


def main():
    print("=" * 78)
    print("Phase 1: Scratchpad cipher verification across CR261 isotopes")
    print("=" * 78)
    print(f"G_p = {G_p} = {float(G_p):.10f}")
    print(f"G_e = {G_e} = {float(G_e):.10f}")
    print(f"G_n = {G_n} = {float(G_n):.10f}")
    print(f"kappa = {KAPPA_NUM}/{KAPPA_DEN} = {KAPPA_NUM/KAPPA_DEN:.10f}")
    print(f"gap unit = {GAP_NUM}/{GAP_DEN} = {GAP_NUM/GAP_DEN:.10f}")
    print()

    rows = load_data()
    print(f"Loaded {len(rows)} isotopes from CR261 fit data\n")

    # First check the four scratchpad anchors: extend to include H-1
    print("Anchor cross-check (from scratchpad):")
    print(f"{'isotope':10s} {'Z':>3s} {'N':>4s} {'A':>4s} "
          f"{'G(P)':>16s} {'Q_mass':>16s} {'Q_sub':>16s} {'F_conn':>16s}")
    for label, Z, N, A in [("H-1", 1, 0, 1), ("He-4", 2, 2, 4),
                            ("C-12", 6, 6, 12), ("Au-197", 79, 118, 197)]:
        c = compute_cipher(Z, N, A)
        print(f"{label:10s} {Z:>3d} {N:>4d} {A:>4d} "
              f"{float(c['G_P']):>16.10f} {float(c['Q_mass']):>16.10f} "
              f"{float(c['Q_sub']):>16.10f} {float(c['F_conn_actual']):>16.10f}")
    print()

    # Now verify on all CR261 rows
    print("Verification across all CR261 isotopes:")
    print(f"{'set':>5s} {'isotope':>8s} {'Z':>3s} {'N':>3s} {'A':>3s} "
          f"{'F_conn_actual':>15s} {'F_conn_expected':>17s} "
          f"{'deviation':>12s} {'match?':>7s}")
    print("-" * 100)

    all_match = True
    max_deviation = Fraction(0)
    mismatches = []

    for row in rows:
        c = compute_cipher(row["Z"], row["N"], row["A"])
        matches = c["deviation"] == 0
        if not matches:
            all_match = False
            mismatches.append({
                "isotope": row["isotope"],
                "Z": row["Z"],
                "N": row["N"],
                "actual": float(c["F_conn_actual"]),
                "expected": float(c["F_conn_expected"]),
                "deviation": float(c["deviation"]),
            })
        if abs(c["deviation"]) > abs(max_deviation):
            max_deviation = c["deviation"]

        print(f"{row['set']:>5s} {row['isotope']:>8s} "
              f"{row['Z']:>3d} {row['N']:>3d} {row['A']:>3d} "
              f"{float(c['F_conn_actual']):>15.6f} "
              f"{float(c['F_conn_expected']):>17.6f} "
              f"{float(c['deviation']):>12.9f} "
              f"{'YES' if matches else 'NO':>7s}")

    print()
    print("=" * 78)
    print("VERIFICATION SUMMARY")
    print("=" * 78)
    if all_match:
        print(f"[PASS] F_conn = (N-Z)·(7093/192) holds EXACTLY on all "
              f"{len(rows)} isotopes")
    else:
        print(f"[FAIL] {len(mismatches)} isotopes deviate from expected formula")
        for m in mismatches:
            print(f"  {m['isotope']}: actual={m['actual']:.6f}, "
                  f"expected={m['expected']:.6f}, deviation={m['deviation']:.9f}")
    print(f"Max |deviation| = {abs(max_deviation)} = {float(abs(max_deviation)):.12e}")
    print()

    # Also verify the CR245 quadratic identity
    print("=" * 78)
    print("CR245 quadratic identity check: (F_conn)^2 / Q_mass = d·(N-Z)²/A")
    print("=" * 78)
    d_theorem = Fraction(GAP_NUM * GAP_NUM, GAP_DEN * KAPPA_NUM)  # 7093²/(192·7117)
    print(f"d = 7093²/(192·7117) = {d_theorem} ≈ {float(d_theorem):.6f}")
    print()
    print(f"{'isotope':>8s} {'F²/Q_mass':>18s} {'d·(N-Z)²/A':>18s} "
          f"{'match?':>8s}")
    print("-" * 60)
    sample = [("H-1", 1, 0, 1), ("He-4", 2, 2, 4), ("C-12", 6, 6, 12),
              ("Au-197", 79, 118, 197)]
    for label, Z, N, A in sample:
        c = compute_cipher(Z, N, A)
        lhs = c["F_conn_actual"] ** 2 / c["Q_mass"]
        rhs = d_theorem * Fraction((N - Z) ** 2, A)
        match = "YES" if lhs == rhs else "NO"
        print(f"{label:>8s} {float(lhs):>18.10f} {float(rhs):>18.10f} "
              f"{match:>8s}")


if __name__ == "__main__":
    main()
