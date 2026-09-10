"""Probe: is V4_1_SINGLE_WRITE actually a 1-body scalar, or a single-write fermion?"""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path


CR119 = Path(
    r"c:\VS\The_Courtroom\09a_PARTICLE_MASS_CHAIN"
    r"\CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
    r"\CR119_courtroom_particle_table.csv"
)


def main():
    by_class_spin = Counter()
    v41_rows = []
    closed_loop_rows = []
    other_1body = []
    with open(CR119, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            parts = r["partition_signature"].split("+")
            if len(parts) != 1:
                continue
            op = r["operator_class"]
            spin = r["spin_or_hand_class"]
            by_class_spin[(op, spin)] += 1
            row_info = {
                "id": r["candidate_id"],
                "partition": r["partition_signature"],
                "M_native": r["M_native"],
                "M_obs": r["M_observed_candidate"][:20],
                "q_abs": r["q_abs"],
                "q_sign": r["q_sign"],
                "depth": r["closure_depth"],
                "spin": spin,
                "closure": r["closure_status"][:20],
                "stab": r["stability_status"][:25],
                "op": op,
            }
            if op == "V4_1_SINGLE_WRITE":
                v41_rows.append(row_info)
            elif "CLOSED_SCALAR_LOOP" in op:
                closed_loop_rows.append(row_info)
            else:
                other_1body.append(row_info)

    print("\n1-body row breakdown by (operator_class, spin_or_hand_class):")
    for (op, spin), n in sorted(by_class_spin.items(), key=lambda kv: -kv[1]):
        print(f"  {op:30}  spin={spin:30}  n={n}")

    print(f"\nV4_1_SINGLE_WRITE rows: {len(v41_rows)}")
    print(f"Sample V4_1 rows (showing M_native variation):")
    print(f"{'partition':10} {'M_native':10} {'q_abs':5} {'q_sign':10} {'depth':5} {'spin':28} {'stab':25}")
    print("-" * 110)
    # Show diverse M_native values
    seen_M = set()
    for r in v41_rows:
        m = r["M_native"][:10]
        if m not in seen_M and len(seen_M) < 20:
            seen_M.add(m)
            print(f"{r['partition']:10} {m:10} {r['q_abs']:5} {r['q_sign']:10} {r['depth']:5} {r['spin']:28} {r['stab']:25}")


if __name__ == "__main__":
    main()
