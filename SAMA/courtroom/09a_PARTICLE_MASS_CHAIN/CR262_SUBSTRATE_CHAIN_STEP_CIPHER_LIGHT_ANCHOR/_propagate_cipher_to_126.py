"""Propagate CR262's carrier/container cipher across all 126 elements
in the SOB126 ledger. Identify (Z, N) → (u, d, e) substrate-atom hits.
Look for clean Gap-1 targets in surface/Coulomb/pairing residual structure.

Reads: SOB126_ledger.csv (CR250 sealed)
Outputs: tabulation + pattern grouping to stdout.
"""

import csv
from pathlib import Path
from collections import defaultdict

SOB126 = Path(r"c:\VS\The_Courtroom\09a_PARTICLE_MASS_CHAIN\CR250_BINDING_FROM_CR009_LIFT_FORMULA\SOB126_ledger.csv")

# Sealed substrate atoms and named compositions
ATOM_NAMES = {
    1:   "1 = identity",
    2:   "ĥ (primitive)",
    3:   "d̂ (primitive)",
    4:   "ĥ²",
    6:   "ĥ·d̂ = m₃ (chain k=1)",
    8:   "S = ĥ^d̂",
    9:   "D² = S+1 (closure witness)",
    12:  "R = ĥ²·d̂ (radix)",
    16:  "ĥ⁴",
    18:  "Θ = ĥ·d̂² (chain k=2)",
    24:  "ĥ³·d̂",
    27:  "V = d̂^d̂",
    32:  "ĥ⁵",
    36:  "(ĥ·d̂)² = m₃²",
    48:  "ĥ⁴·d̂",
    54:  "ĥ·V (chain k=3)",
    64:  "ĥ⁶",
    72:  "ĥ³·d̂²",
    81:  "F = d̂^(d̂+1)",
    108: "ĥ²·V",
    126: "M = R² − Θ (matter capacity)",
    144: "R²",
    162: "ℒ = ĥ·F (chain k=4 / closed ledger)",
    216: "ĥ³·V = (ĥ·d̂)³",
}

# Carrier (predict stable) / container (predict unstable) classifications
CARRIER = {6, 9, 18, 54}  # CR262 sealed: m₃, D², Θ, ĥV
CONTAINER = {12, 27, 81}   # CR262 sealed: R, V, F
CHAIN_K4 = {162}           # closed ledger; "chain ends" — no stable
MATTER_BOUNDARY = {126}    # M itself; structurally novel

# IUPAC-confirmed stable elements (rough check via Z range; will use SOB126 directly)
def classify_atom(n):
    if n in CARRIER:
        return "CARRIER"
    if n in CONTAINER:
        return "CONTAINER"
    if n in CHAIN_K4:
        return "CHAIN_END"
    if n in MATTER_BOUNDARY:
        return "M_BOUNDARY"
    if n in ATOM_NAMES:
        return "named-atom"
    return "off-atom"


rows = []
with open(SOB126, "r", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        try:
            Z = int(r["Z"])
            A_sob = int(r["A_sob"])
            N = A_sob - Z
            u = 2*Z + N
            d = Z + 2*N
            e = Z
            asym = N - Z
            binding_resid = r.get("binding_residual_MeV", "")
            try:
                resid = float(binding_resid) if binding_resid else None
            except ValueError:
                resid = None
            B_u_MeV = r.get("B_u_MeV", "")
            try:
                bu = float(B_u_MeV) if B_u_MeV else None
            except ValueError:
                bu = None
            row_status = r.get("row_status", "")
            rows.append(dict(
                Z=Z, symbol=r.get("symbol", ""), name=r.get("name", ""),
                A=A_sob, N=N,
                u=u, d=d, e=e,
                asym=asym,
                u_atom=ATOM_NAMES.get(u, ""),
                d_atom=ATOM_NAMES.get(d, ""),
                e_atom=ATOM_NAMES.get(e, ""),
                u_class=classify_atom(u),
                d_class=classify_atom(d),
                e_class=classify_atom(e),
                binding_resid_MeV=resid,
                B_u_MeV=bu,
                row_status=row_status,
            ))
        except (ValueError, KeyError):
            continue

print(f"Loaded {len(rows)} elements from SOB126 ledger.\n")
print("=" * 110)
print(f"{'Z':>3s} {'sym':>4s}  {'A':>3s} {'N':>3s}  "
      f"{'u':>4s} {'d':>4s} {'e':>3s}  "
      f"{'u atom':<30s} {'d atom':<30s} {'class summary':<20s}  "
      f"{'resid MeV':>10s}")
print("=" * 110)

class_summary_counts = defaultdict(int)
for row in rows:
    cls_summary = []
    if row["u_class"] == "CARRIER":
        cls_summary.append("u=CARRIER")
    elif row["u_class"] == "CONTAINER":
        cls_summary.append("u=CONTAINER")
    elif row["u_class"] == "CHAIN_END":
        cls_summary.append("u=CHAIN_END")
    elif row["u_class"] == "M_BOUNDARY":
        cls_summary.append("u=M")
    elif row["u_class"] == "named-atom":
        cls_summary.append("u=named")
    if row["d_class"] == "CARRIER":
        cls_summary.append("d=CARRIER")
    elif row["d_class"] == "CONTAINER":
        cls_summary.append("d=CONTAINER")
    elif row["d_class"] == "CHAIN_END":
        cls_summary.append("d=CHAIN_END")
    elif row["d_class"] == "M_BOUNDARY":
        cls_summary.append("d=M")
    elif row["d_class"] == "named-atom":
        cls_summary.append("d=named")
    summary = "; ".join(cls_summary) if cls_summary else "off-atom"
    class_summary_counts[summary] += 1

    resid_str = f"{row['binding_resid_MeV']:+.3f}" if row['binding_resid_MeV'] is not None else "—"
    print(f"{row['Z']:>3d} {row['symbol']:>4s}  "
          f"{row['A']:>3d} {row['N']:>3d}  "
          f"{row['u']:>4d} {row['d']:>4d} {row['e']:>3d}  "
          f"{row['u_atom'][:30]:<30s} {row['d_atom'][:30]:<30s} {summary[:20]:<20s}  "
          f"{resid_str:>10s}")

print()
print("=" * 110)
print("Class-summary counts across 126 elements:")
print("=" * 110)
for s, c in sorted(class_summary_counts.items(), key=lambda x: -x[1]):
    print(f"  {s:50s} {c} elements")
print()

# Specifically look for elements with substrate-atom hits AND residuals
print("=" * 110)
print("Elements where u OR d lands on a sealed substrate atom (CR262 cipher candidates):")
print("=" * 110)
for row in rows:
    u_hit = row["u_class"] in ("CARRIER", "CONTAINER", "CHAIN_END", "M_BOUNDARY", "named-atom")
    d_hit = row["d_class"] in ("CARRIER", "CONTAINER", "CHAIN_END", "M_BOUNDARY", "named-atom")
    if u_hit or d_hit:
        resid_str = f"{row['binding_resid_MeV']:+.3f}" if row['binding_resid_MeV'] is not None else "—"
        print(f"  Z={row['Z']:>3d} {row['symbol']:>4s} (A={row['A']}, N={row['N']}): "
              f"u={row['u']} {'[' + row['u_atom'] + ']' if u_hit else '':<35s} "
              f"d={row['d']} {'[' + row['d_atom'] + ']' if d_hit else '':<35s} "
              f"resid={resid_str} MeV  {row['row_status']}")
print()

# Look at residual patterns by substrate class
print("=" * 110)
print("Mean residual by u-class (where data available):")
print("=" * 110)
by_class = defaultdict(list)
for row in rows:
    if row['binding_resid_MeV'] is not None and row['Z'] <= 118:
        by_class[row['u_class']].append(row['binding_resid_MeV'])
for cls, lst in by_class.items():
    if lst:
        mean = sum(lst) / len(lst)
        rms = (sum(r**2 for r in lst) / len(lst)) ** 0.5
        print(f"  u_class={cls:15s}  n={len(lst):3d}  mean={mean:+.3f} MeV  RMS={rms:.3f} MeV")
print()

# Look at frontier predictions (Z >= 119)
print("=" * 110)
print("Jerroldium frontier (Z=119–126) — substrate readings:")
print("=" * 110)
for row in rows:
    if row['Z'] < 119:
        continue
    summary_parts = []
    if row["u_class"] != "off-atom":
        summary_parts.append(f"u({row['u']})={row['u_atom']}")
    if row["d_class"] != "off-atom":
        summary_parts.append(f"d({row['d']})={row['d_atom']}")
    print(f"  Z={row['Z']:>3d} {row['symbol']:>4s} (A={row['A']}, N={row['N']}): "
          f"u={row['u']}, d={row['d']}, e={row['e']}")
    if summary_parts:
        for p in summary_parts:
            print(f"      {p}")
