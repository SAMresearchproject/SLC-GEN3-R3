"""HH001 ACTION-residual diagnostic.

For each known-spin element, compute:

    ACTION_residual = PARTICLE ⊕ MATTER ⊕ ELEMENT ⊕ GRAVITY ⊕ CLOCK
    ACTION_physical = 2 × nuclear spin

If ACTION_residual == ACTION_physical for a significant fraction of
elements, that's a substrate signal: nuclear spin IS the Hamming parity
of the other channels.

If the match rate is at chance level (~1/8 for 3-bit values, ~1/16 for
4-bit), then forcing ACTION to be the residual is just renaming the
parity bit; it doesn't reveal a substrate rule.
"""

import csv
from pathlib import Path

CR119 = Path(r"C:/VS/The_Courtroom/09a_PARTICLE_MASS_CHAIN/"
             r"CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/"
             r"CR119_courtroom_periodic_table.csv")
SIS   = Path(r"C:/VS/Haunted_House/explorations/HH001_SIS_126x7_table.csv")
OUT   = Path(r"C:/VS/Haunted_House/explorations/HH001_SIS_action_residual.csv")

elements = {}
with CR119.open("r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        Z = int(row["Z"])
        elements[Z] = {
            "p": int(row["proton_count"]),
            "n": int(row["neutron_count_primary"]),
            "e": int(row["electron_count"]),
            "symbol": row["known_symbol"].strip(),
            "name": row["known_name"].strip(),
        }

sis = {}
with SIS.open("r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        Z = int(row["Z"])
        sis[Z] = row

def parse_spin_doubled(s):
    if s == "-": return None
    if s == "0": return 0
    if "/" in s:
        a, b = s.split("/")
        return int(int(a) * 2 / int(b))
    return int(s) * 2

def parse_clock(c):
    if c == "stable": return 0
    if c == "radioactive": return 1
    return None

rows_out = []
match_count = 0
total_known = 0
match_list = []
mismatch_list = []

for Z in sorted(elements.keys()):
    e = elements[Z]
    s = sis[Z]
    p, n, el = e["p"], e["n"], e["e"]
    clk = parse_clock(s["CLOCK"])
    act_phys = parse_spin_doubled(s["ACTION"])

    if clk is None or act_phys is None:
        rows_out.append({
            "Z": Z, "symbol": e["symbol"], "name": e["name"],
            "PARTICLE": p+el+n, "MATTER": p+n, "ELEMENT": Z, "GRAVITY": Z,
            "CLOCK": "-",
            "ACTION_residual": "-",
            "ACTION_physical": "-",
            "match": "-",
        })
        continue

    particle = p + el + n
    matter   = p + n
    element  = Z
    gravity  = Z
    clock    = clk

    action_residual = particle ^ matter ^ element ^ gravity ^ clock
    matches = (action_residual == act_phys)

    total_known += 1
    if matches:
        match_count += 1
        match_list.append((Z, e["symbol"], action_residual, act_phys))
    else:
        mismatch_list.append((Z, e["symbol"], action_residual, act_phys))

    rows_out.append({
        "Z": Z, "symbol": e["symbol"], "name": e["name"],
        "PARTICLE": particle, "MATTER": matter, "ELEMENT": element, "GRAVITY": gravity,
        "CLOCK": clock,
        "ACTION_residual": action_residual,
        "ACTION_physical": act_phys,
        "match": "TRUE" if matches else "FALSE",
    })

# Save
fieldnames = ["Z", "symbol", "name",
              "PARTICLE", "MATTER", "ELEMENT", "GRAVITY", "CLOCK",
              "ACTION_residual", "ACTION_physical", "match"]
with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in rows_out:
        w.writerow(r)

print(f"Saved {len(rows_out)} rows to {OUT}")
print()
print("=" * 70)
print(f"DIAGNOSTIC: ACTION_residual vs ACTION_physical (= 2 x nuclear spin)")
print("=" * 70)
print(f"Total elements with known spin:  {total_known}")
print(f"Matches:                          {match_count}  ({100*match_count/total_known:.1f}%)")
print(f"Mismatches:                       {total_known-match_count}  ({100*(total_known-match_count)/total_known:.1f}%)")
print()
print("Chance baseline:")
print(f"  If ACTION_residual were random and ACTION_physical takes")
print(f"  ~10 distinct values across the 102 elements, chance match rate")
print(f"  would be approximately 10%.")
print()
print(f"Observed: {100*match_count/total_known:.1f}%")
print()

if match_count > 0:
    print(f"--- Matches ({match_count} elements) ---")
    print(f"{'Z':>3} {'Sym':>3} {'residual':>9} {'physical':>9}")
    for (Z, sym, res, phys) in match_list[:30]:
        print(f"{Z:>3} {sym:>3} {res:>9} {phys:>9}")
    if len(match_list) > 30:
        print(f"  ...and {len(match_list)-30} more")

print()
print(f"--- First 15 mismatches ---")
print(f"{'Z':>3} {'Sym':>3} {'residual':>9} {'physical':>9} {'gap':>6}")
for (Z, sym, res, phys) in mismatch_list[:15]:
    print(f"{Z:>3} {sym:>3} {res:>9} {phys:>9} {res-phys:>6}")
