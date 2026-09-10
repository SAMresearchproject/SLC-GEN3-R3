"""Dry-run: does the ĥ·d̂^k chain actually pick the local BE/A maxima?
Uses AME2020 masses from CR248 hash-locked train+test files.
"""
import csv
from pathlib import Path

BASE = Path(r"c:\VS\The_Courtroom\09a_PARTICLE_MASS_CHAIN\CR248_SOB_MICRO_CHANNEL_DEBIT_OCCUPANCY")
TRAIN = BASE / "CR248_train_lane_a.csv"
TEST = BASE / "CR248_test_holdout.csv"

# Atomic masses for hydrogen, neutron (CODATA / AME2020)
M_H_atomic = 1.00782503207   # H-1 atomic mass
M_N = 1.00866491588          # free neutron mass
U_TO_MEV = 931.49410242

def load_rows(p):
    rows = []
    with open(p, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append((r["isotope"], int(r["Z"]), int(r["N"]),
                         int(r["A"]), float(r["atomic_mass_u"])))
    return rows

rows = load_rows(TRAIN) + load_rows(TEST)
# Z = N stable nuclei
zn = [(iso, Z, N, A, m) for (iso, Z, N, A, m) in rows if Z == N and Z >= 1]
zn.sort(key=lambda r: r[1])

print(f"{'iso':8s} {'Z':>3s} {'A':>4s}  "
      f"{'u_count':>8s} {'on chain?':>12s}  "
      f"{'BE_total':>10s} {'BE/A':>8s}  {'tag':s}")
print("-" * 90)

chain_steps = {2: "ĥ", 6: "ĥ·d̂ = m₃", 18: "Θ", 54: "ĥ·V",
               162: "ℒ", 9: "(D² — closure witness; not chain)",
               12: "(R — not chain)", 27: "(V — not chain)",
               81: "(F — not chain)", 24: "(off-chain)", 36: "((ĥd̂)²)",
               15: "(off-atom)", 21: "(off-atom)", 30: "(off-atom)",
               39: "(off-atom)", 45: "(bigrade_sum)",
               48: "(off-atom)", 57: "(off-atom)", 60: "(off-atom)",
               63: "(D²·(S-1))", 66: "(off-atom)", 69: "(off-atom)",
               72: "(ĥ³·d̂²)", 75: "(off-atom)", 78: "(off-atom)"}

for (iso, Z, N, A, m) in zn:
    u_count = 2 * Z + N
    BE_u = (Z * M_H_atomic + N * M_N - m)
    BE_MeV = BE_u * U_TO_MEV
    BE_per_A = BE_MeV / A
    tag = chain_steps.get(u_count, "")
    on_chain = u_count in (6, 18, 54, 162)
    print(f"{iso:8s} {Z:>3d} {A:>4d}  "
          f"{u_count:>8d} {'CHAIN' if on_chain else '':>12s}  "
          f"{BE_MeV:>10.3f} {BE_per_A:>8.4f}  {tag:s}")

print()
print("Chain-step anchors and their immediate Z=N neighbors:")
print()

for target_Z, label in [(2, "He-4"), (6, "C-12"), (18, "Ar-36")]:
    print(f"--- Chain step at Z={target_Z} ({label}) ---")
    for (iso, Z, N, A, m) in zn:
        if abs(Z - target_Z) <= 2:
            u_count = 2 * Z + N
            BE_u = (Z * M_H_atomic + N * M_N - m)
            BE_MeV = BE_u * U_TO_MEV
            BE_per_A = BE_MeV / A
            marker = "  ← chain" if u_count in (6, 18, 54) else ""
            print(f"  {iso:8s} Z={Z}  A={A}  BE/A={BE_per_A:.4f} MeV{marker}")
    print()
