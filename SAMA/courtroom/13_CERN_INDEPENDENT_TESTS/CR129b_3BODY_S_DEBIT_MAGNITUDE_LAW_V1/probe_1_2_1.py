"""Probe: 1:2:1 slot weighting for qA + 9/8 coefficient test.

Several interpretations of (1/4, 1/2, 1/4) slot weights tested:
  A) qA_i = w_i * qA_total           with w = (1/4, 1/2, 1/4) normalized
  B) qA_i = w_i * M                  with w = (1/4, 1/2, 1/4)
  C) qA_i = w_i * a_i * scale        slot weight times partition element
  D) qA_i = w_i * a_i^2 * scale      slot weight times slot's M contribution
"""
from __future__ import annotations

import csv
from decimal import Decimal, getcontext
from pathlib import Path


getcontext().prec = 100


CR119 = Path(
    r"c:\VS\The_Courtroom\09a_PARTICLE_MASS_CHAIN"
    r"\CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
    r"\CR119_courtroom_particle_table.csv"
)

R = 12
D = 3
W = (Decimal(1)/Decimal(4), Decimal(1)/Decimal(2), Decimal(1)/Decimal(4))
COEF_9_8 = Decimal(9) / Decimal(8)


def sum_sq_diff(qa, qb, qc):
    return (qa - qb) ** 2 + (qb - qc) ** 2 + (qa - qc) ** 2


def main():
    rows = []
    with open(CR119, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["operator_class"] != "OCTET_COMPOSITE":
                continue
            try:
                parts = [int(x) for x in r["partition_signature"].split("+")]
            except ValueError:
                continue
            if len(parts) != 3:
                continue
            if int(r["q_abs"]) != 0:  # restrict to q=0 first for clean test
                continue
            a, b, c = parts
            M = int(float(r["M_native"]))
            S_obs = Decimal(r["S_debit_or_credit"])
            qA_tot = Decimal(r["qA_source_support"])
            # A: w_i * qA_total
            qA_A = (W[0]*qA_tot, W[1]*qA_tot, W[2]*qA_tot)
            sumA = sum_sq_diff(*qA_A)
            S_predA_half = sumA / Decimal(2)
            S_predA_98 = COEF_9_8 * sumA / Decimal(2)
            # B: w_i * M
            qA_B = (W[0]*Decimal(M), W[1]*Decimal(M), W[2]*Decimal(M))
            sumB = sum_sq_diff(*qA_B)
            S_predB_half = sumB / Decimal(2)
            S_predB_98 = COEF_9_8 * sumB / Decimal(2)
            # C: w_i * a_i (no extra scale)
            qA_C = (W[0]*Decimal(a), W[1]*Decimal(b), W[2]*Decimal(c))
            sumC = sum_sq_diff(*qA_C)
            S_predC_half = sumC / Decimal(2)
            S_predC_98 = COEF_9_8 * sumC / Decimal(2)
            # D: w_i * a_i^2  (slot's contribution to M_native)
            qA_D = (W[0]*Decimal(a*a), W[1]*Decimal(b*b), W[2]*Decimal(c*c))
            sumD = sum_sq_diff(*qA_D)
            S_predD_half = sumD / Decimal(2)
            S_predD_98 = COEF_9_8 * sumD / Decimal(2)
            # E: per-slot qA = a_i (no weight, just slot values as masses)
            qA_E = (Decimal(a), Decimal(b), Decimal(c))
            sumE = sum_sq_diff(*qA_E)
            S_predE_half = sumE / Decimal(2)
            rows.append({
                "abc":   f"({a},{b},{c})",
                "M":     M,
                "S_obs": float(S_obs),
                "A_half":  float(S_predA_half),
                "A_98":    float(S_predA_98),
                "B_half":  float(S_predB_half),
                "B_98":    float(S_predB_98),
                "C_half":  float(S_predC_half),
                "C_98":    float(S_predC_98),
                "D_half":  float(S_predD_half),
                "D_98":    float(S_predD_98),
                "E_half":  float(S_predE_half),
                "ratio_obs_C_98": float(S_obs / S_predC_98) if S_predC_98 != 0 else 0,
                "ratio_obs_D_98": float(S_obs / S_predD_98) if S_predD_98 != 0 else 0,
                "ratio_obs_E_half": float(S_obs / S_predE_half) if S_predE_half != 0 else 0,
            })

    print("Testing 1:2:1 slot weighting (1/4 | 1/2 | 1/4) combined with 9/8 coefficient")
    print("for all OCTET 3-body q=0 rows (Q = qA_source_support).\n")
    print(f"{'abc':10} {'M':6} {'S_obs':10} "
          f"{'C_98':10} {'D_98':10} {'E_half':10} "
          f"{'obs/C_98':10} {'obs/D_98':10} {'obs/E_half':10}")
    print("-" * 110)
    for r in rows[:20]:
        print(f"{r['abc']:10} {r['M']:6} {r['S_obs']:+10.5f} "
              f"{r['C_98']:+10.5f} {r['D_98']:+10.5f} {r['E_half']:+10.4f} "
              f"{r['ratio_obs_C_98']:+10.5f} {r['ratio_obs_D_98']:+10.6f} {r['ratio_obs_E_half']:+10.6f}")


if __name__ == "__main__":
    main()
