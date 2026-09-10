"""Probe: test qA_source_support relative to M as slot correction."""
from __future__ import annotations

import csv
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path


getcontext().prec = 200


CR119 = Path(
    r"c:\VS\The_Courtroom\09a_PARTICLE_MASS_CHAIN"
    r"\CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
    r"\CR119_courtroom_particle_table.csv"
)

R = 12
D = 3


def S_BCP(a, b):
    if a == b:
        return Fraction(0)
    M = R * a * b + D * abs(a - b)
    sign = 1 if a > b else -1
    return Fraction(sign * M * (abs(a - b) + D), abs(a - b) * (R ** 4))


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
            a, b, c = parts
            M = int(float(r["M_native"]))
            S_obs = Decimal(r["S_debit_or_credit"])
            qA = Decimal(r["qA_source_support"])
            q_abs = int(r["q_abs"])
            depth = int(r["closure_depth"])
            # pure pairwise
            spw = S_BCP(a, b) + S_BCP(b, c) + S_BCP(a, c)
            spw_dec = Decimal(spw.numerator) / Decimal(spw.denominator)
            # qA relative to M
            qA_over_M = qA / Decimal(M) if M else Decimal(0)
            # Test: is qA / M a clean structural ratio?
            #   Hypothesis: qA = M + S * something  (since qA_source_support is the "support" mass at the qA channel)
            #   Or: qA = M + S * R^k
            # Try: qA - M  vs  S * scale
            qA_minus_M = qA - Decimal(M)
            # ratio (qA - M) / S
            ratio_qAm_S = (qA_minus_M / S_obs) if S_obs != 0 else Decimal("nan")
            # Try: residual after pure pairwise vs (qA - M)
            residual = S_obs - spw_dec
            ratio_res_qAm = (residual / qA_minus_M) if qA_minus_M != 0 else Decimal("nan")
            # Stage-2 candidate: 1/8 * (qA - M) ?
            cand_18_qAm = spw_dec + qA_minus_M / Decimal(8)
            err_18_qAm = S_obs - cand_18_qAm
            rows.append({
                "sig":     r["partition_signature"],
                "abc":     f"({a},{b},{c})",
                "q":       q_abs,
                "d":       depth,
                "M":       M,
                "qA":      float(qA),
                "qA-M":    float(qA_minus_M),
                "S_obs":   float(S_obs),
                "pairwise": float(spw_dec),
                "residual": float(residual),
                "qA/M":    float(qA_over_M),
                "(qA-M)/S": float(ratio_qAm_S),
                "res/(qA-M)": float(ratio_res_qAm),
                "S - (pair + (qA-M)/8)": float(err_18_qAm),
            })

    rows.sort(key=lambda x: (x["q"], x["abc"]))
    print(f"{'sig':12} {'abc':10} {'q':3} {'M':6} {'qA':10} {'qA-M':10} "
          f"{'S_obs':10} {'pairwise':10} {'residual':10} {'(qA-M)/S':10} {'res/(qA-M)':10}")
    print("-" * 130)
    for r in rows[:30]:
        print(f"{r['sig']:12} {r['abc']:10} {r['q']:3} {r['M']:6} "
              f"{r['qA']:10.3f} {r['qA-M']:10.3f} "
              f"{r['S_obs']:+10.6f} {r['pairwise']:+10.6f} {r['residual']:+10.6f} "
              f"{r['(qA-M)/S']:+10.4f} {r['res/(qA-M)']:+10.5f}")

    # Test if (qA - M) == S * constant, or (qA-M) == S * R^k for some k
    print("\nAggregates: is (qA - M)/S constant across rows?")
    from collections import defaultdict
    by_q = defaultdict(list)
    for r in rows:
        by_q[r["q"]].append(r["(qA-M)/S"])
    for q in sorted(by_q.keys()):
        vals = by_q[q]
        if not vals or any(abs(v) > 1e15 for v in vals):
            continue
        unique = sorted(set(round(v, 4) for v in vals))
        print(f"  q={q}: n={len(vals)}, unique (qA-M)/S = {unique[:6]}")


if __name__ == "__main__":
    main()
