"""Probe: OUTER_BINARY_NEUTRAL rows — try C1=1 first."""
from __future__ import annotations

import csv
from decimal import Decimal
from fractions import Fraction
from pathlib import Path


CR119 = Path(
    r"c:\VS\The_Courtroom\09a_PARTICLE_MASS_CHAIN"
    r"\CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
    r"\CR119_courtroom_particle_table.csv"
)

R = 12
D = 3
ALPHA_H = 2


def main():
    rows = []
    with open(CR119, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["operator_class"] != "OUTER_BINARY_NEUTRAL":
                continue
            rows.append({
                "id":     r["candidate_id"],
                "part":   r["partition_signature"],
                "Mn":     r["M_native"],
                "Mo":     r["M_observed_candidate"][:15],
                "S":      r["S_debit_or_credit"][:15],
                "qA":     r["qA_source_support"][:15],
                "q_abs":  int(r["q_abs"]),
                "q_sign": r["q_sign"],
                "depth":  int(r["closure_depth"]),
                "stab":   r["stability_status"][:25],
                "spin":   r["spin_or_hand_class"],
                "closure": r["closure_status"][:25],
            })

    print(f"Found {len(rows)} OUTER_BINARY_NEUTRAL rows\n")
    print(f"{'part':6} {'Mn':10} {'Mo':16} {'S':16} {'q_abs':5} {'q_sign':10} {'depth':5} {'stab':25}")
    print("-" * 110)
    for r in sorted(rows, key=lambda x: (int(x["part"]) if x["part"].isdigit() else 0,
                                         x["depth"],
                                         x["q_abs"])):
        print(f"{r['part']:6} {r['Mn']:10} {r['Mo']:16} {r['S']:16} "
              f"{r['q_abs']:5} {r['q_sign']:10} {r['depth']:5} {r['stab']:25}")

    # Now test: M_native = partition_value? (C1=1)
    matches_C1_1 = 0
    for r in rows:
        try:
            p = int(r["part"])
            m = Decimal(r["Mn"])
            if abs(m - Decimal(p)) < Decimal("1e-50"):
                matches_C1_1 += 1
        except (ValueError, KeyError):
            pass
    print(f"\nC1=1 test (M_native == partition_value): {matches_C1_1}/{len(rows)}")

    # Test M = partition * something
    print(f"\nM_native / partition_value:")
    seen = set()
    for r in rows:
        try:
            p = int(r["part"])
            m = Decimal(r["Mn"])
            ratio = m / Decimal(p) if p else Decimal(0)
            key = (p, str(ratio), r["q_abs"], r["q_sign"], r["depth"])
            if key in seen:
                continue
            seen.add(key)
            print(f"  partition={p:3} Mn={m:10} q_abs={r['q_abs']} q_sign={r['q_sign']:9} "
                  f"depth={r['depth']} -> ratio = {ratio}")
        except (ValueError, KeyError):
            pass


if __name__ == "__main__":
    main()
