"""Probe SOURCE_SUPPORT_PACKET cold."""
from __future__ import annotations

import csv
from decimal import Decimal
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
            if r["operator_class"] != "SOURCE_SUPPORT_PACKET":
                continue
            rows.append(r)

    print(f"Found {len(rows)} SOURCE_SUPPORT_PACKET rows\n")
    for r in rows:
        print(f"=== {r['candidate_id']} ===")
        print(f"  partition:         {r['partition_signature']}")
        print(f"  route_combination: {r['route_combination'][:60]}")
        print(f"  M_native:          {r['M_native']}")
        print(f"  M_obs:             {r['M_observed_candidate'][:30]}")
        print(f"  S_debit:           {r['S_debit_or_credit'][:25]}")
        print(f"  qA_support:        {r['qA_source_support'][:25]}")
        print(f"  tensor_carrier:    {r['tensor_carrier_support'][:25]}")
        print(f"  retained_write:    {r['retained_write_support'][:25]}")
        print(f"  q_abs={r['q_abs']}  q_sign={r['q_sign']}")
        print(f"  depth={r['closure_depth']}  bin={r['bin']}")
        print(f"  spin:              {r['spin_or_hand_class']}")
        print(f"  closure_status:    {r['closure_status']}")
        print(f"  stability:         {r['stability_status']}")
        print(f"  matter_row:        {r['matter_row_allowed']}")
        print()


if __name__ == "__main__":
    main()
