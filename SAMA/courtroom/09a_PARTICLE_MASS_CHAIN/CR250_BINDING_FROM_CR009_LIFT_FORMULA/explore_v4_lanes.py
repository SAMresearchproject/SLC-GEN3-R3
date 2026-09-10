"""Exploration v4 — group every row by exact (N-Z)/A, reduce (Z,N) to primitive
vectors via gcd, and look for structural lane patterns.

Per Sean's hint: same (N-Z)/A ratio → same lane. Same primitive (Z,N) → same
substrate direction in the lattice. B_u behavior within a lane may reveal the
structural classifier we've been missing.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from decimal import Decimal, getcontext
from fractions import Fraction
from math import gcd
from pathlib import Path

getcontext().prec = 50

U_TO_MEV = Decimal("931.49410242")

HERE = Path(__file__).parent
CR242 = HERE.parent / "CR242_SAM_BINDING_CURVATURE_DERIVATION" / "CR242_binding_dataset.csv"


def load_all() -> list[dict]:
    """Load ALL CR242 rows including N<Z."""
    rows = []
    with CR242.open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                Z = int(float(r["Z"]))
                N = int(float(r["N"]))
                A = int(float(r["A"]))
                B = Decimal(r["B_u"].strip())
            except (KeyError, ValueError):
                continue
            NmZ = N - Z
            ratio = Fraction(NmZ, A) if A else Fraction(0)
            g = gcd(Z, N) if (Z > 0 and N > 0) else max(Z, N, 1)
            prim = (Z // g, N // g) if g else (Z, N)
            rows.append({
                "iso": r["isotope"],
                "Z": Z, "N": N, "A": A, "NmZ": NmZ,
                "B_obs_u": B,
                "B_obs_MeV": B * U_TO_MEV,
                "ratio": ratio,
                "ratio_dec": float(ratio),
                "gcd": g,
                "primitive": prim,
            })
    return rows


def main():
    rows = load_all()
    print(f"Loaded {len(rows)} rows from CR242 (all, including N<Z)\n")

    # Group by (N-Z)/A ratio
    by_ratio: dict[Fraction, list[dict]] = defaultdict(list)
    for r in rows:
        by_ratio[r["ratio"]].append(r)

    print("=" * 100)
    print(f"LANES BY (N-Z)/A RATIO — {len(by_ratio)} distinct ratios across {len(rows)} rows")
    print("=" * 100)
    print(f"  {'ratio':>10s} {'decimal':>10s} {'n_rows':>6s}  members (Z,N,iso)")
    print("-" * 100)
    for ratio in sorted(by_ratio.keys(), key=lambda x: float(x)):
        members = by_ratio[ratio]
        if len(members) >= 2:
            isos = ", ".join(f"{m['iso']}({m['Z']},{m['N']})" for m in sorted(members, key=lambda x: x["A"]))
            print(f"  {str(ratio):>10s} {float(ratio):>10.6f} {len(members):>6d}  {isos}")
    print()
    print("  (Singleton lanes — only one member at that ratio):")
    singletons = sum(1 for r, m in by_ratio.items() if len(m) == 1)
    print(f"  {singletons} ratios appear in only one row")

    # Group by primitive vector
    by_prim: dict[tuple[int, int], list[dict]] = defaultdict(list)
    for r in rows:
        by_prim[r["primitive"]].append(r)

    print()
    print("=" * 100)
    print(f"LANES BY PRIMITIVE (Z,N) — {len(by_prim)} distinct primitives across {len(rows)} rows")
    print("=" * 100)
    print(f"  {'primitive':>12s} {'ratio':>10s} {'n':>3s}  members (multiplier shown)")
    print("-" * 100)
    for prim in sorted(by_prim.keys(), key=lambda x: x[0] + x[1]):
        members = by_prim[prim]
        if len(members) >= 2:
            isos = ", ".join(f"{m['iso']}(×{m['gcd']})" for m in sorted(members, key=lambda x: x["gcd"]))
            ratio = members[0]["ratio"]
            print(f"  {str(prim):>12s} {str(ratio):>10s} {len(members):>3d}  {isos}")
    print()

    # Within each multi-member lane, look at B_u and B_u/A
    print()
    print("=" * 100)
    print("WITHIN-LANE B_u STRUCTURE — multi-member (N-Z)/A ratios sorted by ratio")
    print("=" * 100)
    print("  Lane: members showing (Z, N, A, B_u MeV, B_u/A keV)")
    print("-" * 100)
    for ratio in sorted(by_ratio.keys(), key=lambda x: float(x)):
        members = by_ratio[ratio]
        if len(members) < 2:
            continue
        print(f"\n  RATIO (N-Z)/A = {ratio} = {float(ratio):.6f}  [{len(members)} members]")
        print(f"  {'iso':>8} {'Z':>3} {'N':>3} {'A':>4} {'B_u MeV':>10} {'B_u/A keV':>12} {'B_u/(N-Z) MeV':>15}")
        for m in sorted(members, key=lambda x: x["A"]):
            B_per_A = (m["B_obs_MeV"] * Decimal(1000)) / Decimal(m["A"])
            if m["NmZ"] != 0:
                B_per_NmZ = m["B_obs_MeV"] / Decimal(m["NmZ"])
                B_per_NmZ_str = f"{B_per_NmZ:.4f}"
            else:
                B_per_NmZ_str = "(N=Z)"
            print(f"  {m['iso']:>8} {m['Z']:3d} {m['N']:3d} {m['A']:4d} "
                  f"{float(m['B_obs_MeV']):10.4f} {float(B_per_A):12.4f} {B_per_NmZ_str:>15s}")

    # Specific deep-dive: the N=Z lane (ratio=0)
    print()
    print("=" * 100)
    print("DEEP DIVE — N=Z LANE (ratio = 0): primitive (1,1) ×k for various k")
    print("=" * 100)
    n_eq_z = sorted([r for r in rows if r["NmZ"] == 0], key=lambda x: x["Z"])
    print(f"  {'iso':>8} {'Z=N':>3} {'A':>4} {'primitive':>12} {'k=gcd':>6} {'B_u MeV':>10} {'B_u/Z MeV':>11} {'B_u/A keV':>10}")
    for r in n_eq_z:
        B_per_Z = r["B_obs_MeV"] / Decimal(r["Z"]) if r["Z"] else Decimal(0)
        B_per_A = r["B_obs_MeV"] * Decimal(1000) / Decimal(r["A"])
        print(f"  {r['iso']:>8} {r['Z']:3d} {r['A']:4d} {str(r['primitive']):>12s} {r['gcd']:6d} "
              f"{float(r['B_obs_MeV']):10.4f} {float(B_per_Z):11.4f} {float(B_per_A):10.4f}")

    # Ratio histogram for context
    print()
    print("=" * 100)
    print("RATIO HISTOGRAM (top 15 most-populated lanes)")
    print("=" * 100)
    by_pop = sorted(by_ratio.items(), key=lambda kv: -len(kv[1]))
    for ratio, mems in by_pop[:15]:
        print(f"  ratio={str(ratio):>10s} = {float(ratio):.6f}  count={len(mems)}")


if __name__ == "__main__":
    main()
