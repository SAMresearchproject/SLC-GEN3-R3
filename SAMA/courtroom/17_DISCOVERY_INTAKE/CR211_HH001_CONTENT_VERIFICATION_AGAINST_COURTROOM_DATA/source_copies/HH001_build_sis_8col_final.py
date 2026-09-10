"""HH001 SIS final table - 7 channels + graviton (the 8th).

Combines the original 7-column SIS table with the GRAVITON column
(= qA / 8 = the 1/8 carrier emission per closure cycle = row 18 per
element).

8 substrate value columns per element:
  PARTICLE   total atomic particle count (p + e + n)
  MATTER     atomic mass (amu)
  ELEMENT    atomic number (Z)
  GRAVITY    qA total = substrate-write source-strength
  CLOCK      stable / radioactive
  LIGHT      principal emission line (nm); '-' if no clean data
  ACTION     nuclear spin (fraction); '-' if no data
  GRAVITON   carrier emission per cycle = qA / 8 (the 8th row,
             the closure address, the substrate's commit target)

Plus identifiers: cell_id, Z, symbol, name.
"""

import csv
from pathlib import Path

CR119 = Path(r"C:/VS/The_Courtroom/09a_PARTICLE_MASS_CHAIN/"
             r"CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/"
             r"CR119_courtroom_periodic_table.csv")
SIS = Path(r"C:/VS/Haunted_House/explorations/HH001_SIS_126x7_table.csv")
OUT = Path(r"C:/VS/Haunted_House/explorations/HH001_SIS_8col_final.csv")

cr119_data = {}
with CR119.open("r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        Z = int(row["Z"])
        cr119_data[Z] = {
            "qA_carrier": float(row["tensor_carrier_support_primary"]),
        }

rows_out = []
with SIS.open("r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        Z = int(row["Z"])
        graviton = f"{cr119_data[Z]['qA_carrier']:.6f}"

        rows_out.append({
            "cell_id":  row["cell_id"],
            "Z":        Z,
            "symbol":   row["symbol"],
            "name":     row["name"],
            "PARTICLE": row["PARTICLE"],
            "MATTER":   row["MATTER"],
            "ELEMENT":  row["ELEMENT"],
            "GRAVITY":  row["GRAVITY"],
            "CLOCK":    row["CLOCK"],
            "LIGHT":    row["LIGHT"],
            "ACTION":   row["ACTION"],
            "GRAVITON": graviton,
        })

fieldnames = ["cell_id", "Z", "symbol", "name",
              "PARTICLE", "MATTER", "ELEMENT",
              "GRAVITY", "CLOCK", "LIGHT", "ACTION",
              "GRAVITON"]
with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in rows_out:
        w.writerow(r)

print(f"Wrote {len(rows_out)} rows to {OUT}")
print()
print("First 15 rows:")
hdr = f"{'ID':<8}{'Sy':>3}{'Name':<13}{'PART':>5}{'MASS':>9}{'Z':>4}{'GRAVITY':>13}{'CLK':>6}{'LGT':>5}{'ACT':>5}{'GRAVITON':>13}"
print(hdr)
for r in rows_out[:15]:
    name = r['name'] if r['name'] != 'SAM frontier' else 'frontier'
    print(f"{r['cell_id']:<8}{r['symbol']:>3}{name:<13}{r['PARTICLE']:>5}{r['MATTER']:>9}{r['Z']:>4}{r['GRAVITY']:>13}{r['CLOCK']:>6}{str(r['LIGHT']):>5}{r['ACTION']:>5}{r['GRAVITON']:>13}")

print()
print("Frontier rows (Z=119-126):")
for r in rows_out[-8:]:
    name = r['name'] if r['name'] != 'SAM frontier' else 'frontier'
    print(f"{r['cell_id']:<8}{r['symbol']:>3}{name:<13}{r['PARTICLE']:>5}{r['MATTER']:>9}{r['Z']:>4}{r['GRAVITY']:>13}{r['CLOCK']:>6}{str(r['LIGHT']):>5}{r['ACTION']:>5}{r['GRAVITON']:>13}")
