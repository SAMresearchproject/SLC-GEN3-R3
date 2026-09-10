"""Quick residual-vs-A analysis for CR249 R1 results."""
import csv
from pathlib import Path

src = Path(r"c:\VS\The_Courtroom\09a_PARTICLE_MASS_CHAIN\CR249_BINDING_AS_CONNECTION_FEE\CR249_per_row_predictions.csv")

rows = []
with src.open("r", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["rule"] != "R1_per_excess_neutron":
            continue
        if not r["delta_MeV"]:
            continue
        rows.append({
            "iso": r["isotope"],
            "Z": int(float(r["Z"])),
            "N": int(float(r["N"])),
            "A": int(float(r["A"])),
            "B_obs": float(r["B_u_obs_u"]),
            "B_pred": float(r["B_u_pred_u"]),
            "delta_MeV": float(r["delta_MeV"]),
            "abs_delta_MeV": abs(float(r["delta_MeV"])),
        })

rows.sort(key=lambda x: x["A"])

print(f"{'iso':>8} {'A':>4} {'Z':>4} {'N':>4} {'B_obs(MeV)':>11} {'B_pred(MeV)':>11} {'delta_MeV':>10} {'|d|/A':>7} {'|d|/A^(2/3)':>12} {'|d|/Z2A^(-1/3)':>16}")
print("-" * 110)
for r in rows:
    A = r["A"]; Z = r["Z"]
    per_A = r["abs_delta_MeV"] / A
    per_A23 = r["abs_delta_MeV"] / (A ** (2/3))
    coulomb_scale = Z*(Z-1) / (A ** (1/3)) if A > 0 else 1
    per_coulomb = r["abs_delta_MeV"] / coulomb_scale if coulomb_scale > 0 else 0
    print(f"{r['iso']:>8} {A:4d} {Z:4d} {r['N']:4d} {r['B_obs']*931.494:11.3f} {r['B_pred']*931.494:11.3f} "
          f"{r['delta_MeV']:10.3f} {per_A:7.4f} {per_A23:12.4f} {per_coulomb:16.6f}")
