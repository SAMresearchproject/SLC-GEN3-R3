"""Probe pure pairwise BCP debit sum vs observed S_3body, then test 1/8 surcharge."""
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


def S_BCP(a: int, b: int) -> Fraction:
    """BCP 2-body S_debit per CR128b: sign(a-b) * (R*a*b + D*|a-b|) * (|a-b|+D) / (|a-b| * R^4)."""
    if a == b:
        return Fraction(0)
    M = R * a * b + D * abs(a - b)
    sign = 1 if a > b else -1
    return Fraction(sign * M * (abs(a - b) + D), abs(a - b) * (R ** 4))


def parse_partition(sig):
    try:
        return tuple(int(p) for p in sig.strip().split("+"))
    except ValueError:
        return None


def main():
    rows = []
    with open(CR119, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["operator_class"] != "OCTET_COMPOSITE":
                continue
            parsed = parse_partition(r["partition_signature"])
            if parsed is None or len(parsed) != 3:
                continue
            a, b, c = parsed  # PRESERVE ORDER from the partition string
            M_native = int(float(r["M_native"]))
            S_obs = Decimal(r["S_debit_or_credit"])
            q_abs = int(r["q_abs"])
            depth = int(r["closure_depth"])
            # Stage 1: pure pairwise from ordered partition string
            s_ab = S_BCP(a, b)
            s_bc = S_BCP(b, c)
            s_ac = S_BCP(a, c)
            pairwise = s_ab + s_bc + s_ac
            pairwise_dec = Decimal(pairwise.numerator) / Decimal(pairwise.denominator)
            residual = S_obs - pairwise_dec
            # Stage 2: 1/8 surcharge candidates
            #  S = pairwise + (1/8) * M_native ?
            cand_1_8_M = pairwise_dec + Decimal(M_native) / Decimal(8)
            res_minus_1_8_M = S_obs - cand_1_8_M
            # S = pairwise + (1/8) * (pairwise) ?
            cand_1_8_pair = pairwise_dec * Decimal("1.125")
            res_minus_1_8_pair = S_obs - cand_1_8_pair
            # ratio residual / M
            ratio_res_M = residual / Decimal(M_native) if M_native else Decimal(0)
            ratio_res_pair = (residual / pairwise_dec) if pairwise_dec else Decimal("nan")
            rows.append({
                "sig": r["partition_signature"],
                "order_abc": f"({a},{b},{c})",
                "q": q_abs,
                "d": depth,
                "M": M_native,
                "S_obs": float(S_obs),
                "pairwise": float(pairwise_dec),
                "residual": float(residual),
                "res/M": float(ratio_res_M),
                "res/pair": float(ratio_res_pair) if pairwise_dec else float("nan"),
            })

    rows.sort(key=lambda x: (x["q"], x["order_abc"]))
    print(f"{'sig':12} {'order':12} {'q':3} {'M':6} "
          f"{'S_obs':12} {'pairwise':12} {'residual':12} {'res/M':12} {'res/pair':10}")
    print("-" * 110)
    for r in rows[:30]:
        print(f"{r['sig']:12} {r['order_abc']:12} {r['q']:3} {r['M']:6} "
              f"{r['S_obs']:+12.6f} {r['pairwise']:+12.6f} {r['residual']:+12.6f} "
              f"{r['res/M']:+12.7f} {r['res/pair']:+10.4f}")

    # Aggregate: what is the average res/M by q_abs?
    print("\nAggregates by q_abs:")
    from collections import defaultdict
    by_q = defaultdict(list)
    for r in rows:
        by_q[r["q"]].append(r["res/M"])
    for q in sorted(by_q.keys()):
        vals = by_q[q]
        # unique values?
        unique = sorted(set(round(v, 8) for v in vals))
        print(f"  q={q}: n={len(vals)}, unique res/M = {unique[:6]}")


if __name__ == "__main__":
    main()
