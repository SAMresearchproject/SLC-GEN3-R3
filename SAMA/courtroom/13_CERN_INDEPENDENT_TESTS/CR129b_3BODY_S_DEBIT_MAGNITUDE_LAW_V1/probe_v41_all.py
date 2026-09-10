"""Probe: verify V4_1 mass formula on all 90 rows."""
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
ALPHA_H = 2


def K(q_sign, stab):
    is_antimatter = "ANTIMATTER" in stab
    # antimatter swaps the K factor
    if q_sign == "positive":
        return Fraction(3, 2) if is_antimatter else Fraction(5, 4)
    if q_sign == "negative":
        return Fraction(5, 4) if is_antimatter else Fraction(3, 2)
    return None


def main():
    rows = []
    violations = []
    matches = 0
    with open(CR119, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["operator_class"] != "V4_1_SINGLE_WRITE":
                continue
            q_abs = int(r["q_abs"])
            q_sign = r["q_sign"]
            depth = int(r["closure_depth"])
            stab = r["stability_status"]
            M_native = Decimal(r["M_native"])
            k = K(q_sign, stab)
            if k is None:
                violations.append({"id": r["candidate_id"], "reason": f"unexpected q_sign={q_sign}"})
                continue
            pred = Fraction(q_abs * R ** depth) * k
            pred_dec = Decimal(pred.numerator) / Decimal(pred.denominator)
            diff = M_native - pred_dec
            ok = abs(diff) < Decimal("1e-50")
            if ok:
                matches += 1
            else:
                violations.append({
                    "id":       r["candidate_id"],
                    "partition": r["partition_signature"],
                    "q_abs":    q_abs,
                    "q_sign":   q_sign,
                    "depth":    depth,
                    "stab":     stab,
                    "M_native_obs": float(M_native),
                    "M_native_pred": float(pred_dec),
                    "diff":     float(diff),
                })

    print(f"V4_1_SINGLE_WRITE rows: 90 expected")
    print(f"Formula matches: {matches}")
    print(f"Violations: {len(violations)}")
    if violations:
        print("\nViolators:")
        for v in violations[:30]:
            print(f"  {v}")


if __name__ == "__main__":
    main()
