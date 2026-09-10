"""Standalone exploration script: compute S_debit structure for 3-body rows."""
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


def parse_partition(sig):
    parts = sig.strip().split("+")
    try:
        return tuple(int(p) for p in parts)
    except ValueError:
        return None


def main():
    rows = []
    with open(CR119, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            op = r["operator_class"]
            if op not in ("OCTET_COMPOSITE", "GROUND_BARYON_3BODY"):
                continue
            sig = r["partition_signature"]
            parsed = parse_partition(sig)
            if parsed is None or len(parsed) != 3:
                continue
            a, b, c = parsed
            m_native = int(float(r["M_native"]))
            s_str = r["S_debit_or_credit"]
            s_dec = Decimal(s_str)
            # S * R^4 as exact rational
            s_R4 = s_dec * Decimal(R ** 4)
            # X = S * R^4 / M
            X = s_R4 / Decimal(m_native) if m_native else Decimal(0)
            X_4 = X * Decimal(4)
            # Sort canonical
            sorted_abc = tuple(sorted(parsed))
            form = ("aab" if sorted_abc[0] == sorted_abc[1] and sorted_abc[1] != sorted_abc[2]
                    else "abb" if sorted_abc[1] == sorted_abc[2] and sorted_abc[0] != sorted_abc[1]
                    else "aaa" if sorted_abc[0] == sorted_abc[2]
                    else "abc")
            rows.append({
                "id":      r["candidate_id"],
                "op":      op,
                "sig":     sig,
                "sorted":  f"({sorted_abc[0]},{sorted_abc[1]},{sorted_abc[2]})",
                "M":       m_native,
                "S_str":   s_str[:25],
                "X_4":     float(X_4),
                "form":    form,
                "q_abs":   r["q_abs"],
                "depth":   r["closure_depth"],
                "stab":    r["stability_status"][:25],
            })

    # print sorted by form then by sorted_abc
    rows.sort(key=lambda x: (x["form"], x["sorted"]))
    print(f"{'sig':16} {'sort':12} {'form':4} {'M':6} {'X*4':12} {'q':3} {'d':3} {'op':22} {'stab':25}")
    print("-" * 130)
    for r in rows:
        print(f"{r['sig']:16} {r['sorted']:12} {r['form']:4} {r['M']:6} {r['X_4']:12.4f} "
              f"{r['q_abs']:3} {r['depth']:3} {r['op']:22} {r['stab']:25}")


if __name__ == "__main__":
    main()
