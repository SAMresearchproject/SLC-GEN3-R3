"""Probe: does sign(S_debit) follow q_sign for OCTET 3-body rows?

Hypothesis: sign(S_debit) = +1 if q_sign in {positive, neutral}, -1 if q_sign == 'negative'.
"""
from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path
from collections import Counter


CR119 = Path(
    r"c:\VS\The_Courtroom\09a_PARTICLE_MASS_CHAIN"
    r"\CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
    r"\CR119_courtroom_particle_table.csv"
)


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
            S = Decimal(r["S_debit_or_credit"])
            q_sign = r["q_sign"]
            q_abs = int(r["q_abs"])
            S_sign = "positive" if S > 0 else "negative" if S < 0 else "zero"
            # Hypothesis A: S sign = q_sign (positive/negative/neutral)
            # Hypothesis B: S sign = q_sign with neutral mapped to positive
            hyp_A_match = (
                (q_sign == "positive" and S > 0) or
                (q_sign == "negative" and S < 0) or
                (q_sign == "neutral" and S > 0)  # q=0 always positive
            )
            rows.append({
                "sig":     r["partition_signature"],
                "abc":     f"({parts[0]},{parts[1]},{parts[2]})",
                "q_abs":   q_abs,
                "q_sign":  q_sign,
                "S_sign":  S_sign,
                "hyp_A":   hyp_A_match,
            })

    # tabulate
    by_q_sign = Counter((r["q_sign"], r["S_sign"]) for r in rows)
    print("Tabulation: (q_sign, S_sign) -> count")
    for (qs, ss), n in sorted(by_q_sign.items()):
        print(f"  q_sign={qs:10} S_sign={ss:10}  n={n}")
    n_match = sum(1 for r in rows if r["hyp_A"])
    n_total = len(rows)
    print(f"\nHypothesis A (sign(S) = q_sign with neutral->positive): {n_match}/{n_total} match")
    print("\nViolators (if any):")
    for r in rows:
        if not r["hyp_A"]:
            print(f"  {r['sig']:10}  q_sign={r['q_sign']:9}  S_sign={r['S_sign']:9}  q_abs={r['q_abs']}")


if __name__ == "__main__":
    main()
