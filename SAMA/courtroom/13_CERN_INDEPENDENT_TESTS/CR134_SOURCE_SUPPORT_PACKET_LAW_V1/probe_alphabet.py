"""Probe: tier the CR-119 catalog by body count and promotion status for the Paul Revere alphabet."""
from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path


CR119 = Path(
    r"c:\VS\The_Courtroom\09a_PARTICLE_MASS_CHAIN"
    r"\CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL"
    r"\CR119_courtroom_particle_table.csv"
)


def tier_for(op_class: str, partition_sig: str) -> str:
    n_elements = len(partition_sig.split("+"))
    if op_class in {"TENSOR_CARRIER", "ROAD_LIGHT_CARRIER", "WEAK_VECTOR_CARRIER",
                    "NEUTRAL_VECTOR_CARRIER", "COLOR_OWNER_CARRIER", "A_FIELD_CARRIER"}:
        return "1body_carrier"
    if op_class == "SOURCE_SUPPORT_PACKET":
        return "substrate_echo"
    if op_class in {"DIRECT_QA_AS_MASS", "PROMOTE_TENSOR_CARRIER", "SKIP_LEDGER_COMPRESSION",
                    "RANDOM_ROUTE_CLOSURE", "NEAREST_KNOWN_PARTICLE_MATCH", "OPEN_COLOR_NO_OWNER",
                    "SURFACE_STACK_DISABLED", "FAKE_PARENT_NO_CLOSED_LOOP"}:
        return "null_control"
    if n_elements == 1:
        return "1body_fermion"  # V4_1 or OUTER_BINARY_NEUTRAL
    if n_elements == 2:
        return "2body_short"
    if n_elements == 3:
        return "3body_standard"
    return f"{n_elements}body_other"


def main():
    tier_promoted = defaultdict(int)
    tier_rejected = defaultdict(int)
    tier_total = defaultdict(int)
    rejected_status = "REJECTED_FAKE_CLOSURE"
    total = 0
    with open(CR119, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            total += 1
            tier = tier_for(r["operator_class"], r["partition_signature"])
            stab = r["stability_status"]
            tier_total[tier] += 1
            if stab == rejected_status:
                tier_rejected[tier] += 1
            elif tier == "null_control":
                pass  # null controls neither promoted nor rejected
            else:
                tier_promoted[tier] += 1

    print(f"Total CR119 rows: {total}")
    print()
    print(f"{'tier':22} {'total':>7} {'promoted':>10} {'rejected':>10} {'log2(promoted)':>16}")
    print("-" * 80)
    sum_promoted = 0
    sum_rejected = 0
    for tier in sorted(tier_total.keys()):
        t = tier_total[tier]
        p = tier_promoted[tier]
        rj = tier_rejected[tier]
        sum_promoted += p
        sum_rejected += rj
        bits = math.log2(p) if p > 0 else 0
        print(f"{tier:22} {t:>7} {p:>10} {rj:>10} {bits:>16.4f}")
    print("-" * 80)
    bits_total = math.log2(sum_promoted) if sum_promoted > 0 else 0
    bits_per_packet = sum(math.log2(tier_promoted[t]) for t in tier_promoted if tier_promoted[t] > 0)
    print(f"{'TOTAL':22} {total:>7} {sum_promoted:>10} {sum_rejected:>10} {bits_total:>16.4f}")
    print()
    print(f"Information capacity per tier (sum of log2(promoted) per tier): {bits_per_packet:.4f} bits per mixed-tier packet")


if __name__ == "__main__":
    main()
