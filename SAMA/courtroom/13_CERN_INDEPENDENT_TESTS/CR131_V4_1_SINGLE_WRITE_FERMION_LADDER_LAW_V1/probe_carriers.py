"""Probe: pull mass and properties of the 6 carrier rows.

Test C1 = 9/8 candidate against carrier masses.
"""
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


CARRIER_CLASSES = (
    "TENSOR_CARRIER",
    "ROAD_LIGHT_CARRIER",
    "WEAK_VECTOR_CARRIER",
    "NEUTRAL_VECTOR_CARRIER",
    "COLOR_OWNER_CARRIER",
    "A_FIELD_CARRIER",
)


def main():
    rows = []
    with open(CR119, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["operator_class"] not in CARRIER_CLASSES:
                continue
            rows.append({
                "op":         r["operator_class"],
                "partition":  r["partition_signature"],
                "M_native":   r["M_native"],
                "M_obs":      r["M_observed_candidate"][:25],
                "S_debit":    r["S_debit_or_credit"][:25],
                "qA":         r["qA_source_support"][:25],
                "q_abs":      r["q_abs"],
                "q_sign":     r["q_sign"],
                "depth":      r["closure_depth"],
                "spin":       r["spin_or_hand_class"],
                "closure":    r["closure_status"],
                "stab":       r["stability_status"],
                "route":      r["route_class"],
                "surf_addr":  r["surface_packet_address"][:30],
                "known":      r["known_match"][:30],
            })

    print(f"Found {len(rows)} carrier rows")
    print()
    for r in rows:
        print(f"=== {r['op']} ===")
        print(f"  partition:      {r['partition']}")
        print(f"  M_native:       {r['M_native']}")
        print(f"  M_obs:          {r['M_obs']}")
        print(f"  S_debit:        {r['S_debit']}")
        print(f"  qA_support:     {r['qA']}")
        print(f"  q_abs={r['q_abs']}, q_sign={r['q_sign']}, depth={r['depth']}")
        print(f"  spin:           {r['spin']}")
        print(f"  closure_status: {r['closure']}")
        print(f"  stability:      {r['stab']}")
        print(f"  route_class:    {r['route']}")
        print(f"  surface_addr:   {r['surf_addr']}")
        print(f"  known_match:    {r['known']}")
        # Test C1 = 9/8 against M_native
        try:
            M = Decimal(r["M_native"])
            print(f"  M / (9/8):      {M / (Decimal(9)/Decimal(8))}")
            print(f"  M * (8/9):      {M * Decimal(8) / Decimal(9)}")
        except Exception:
            pass
        print()


if __name__ == "__main__":
    main()
