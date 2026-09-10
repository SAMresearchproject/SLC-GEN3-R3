"""HH001 6-channel signature uniqueness test.

For each of 126 elements, compute the substrate signature using
6 channels (no LIGHT, no graviton-as-channel). Test under both
XOR and arithmetic addition. Check uniqueness across all 126.

6-channel encoding (from CR119 + SIS table):
  PARTICLE = p + e + n
  MATTER   = p + n (mass number A)
  ELEMENT  = Z
  GRAVITY  = Z (carries known duplicate with ELEMENT)
  CLOCK    = 0 (stable) / 1 (radioactive)
  ACTION   = 2 x nuclear spin (integer); 0 if unknown

Frontier elements (Z=119-126) have missing ACTION data; treated as 0.

The signature IS the value at the center (row 18 / graviton position)
for that element - what the substrate writes when this element closes.

If we get 126 distinct signatures under either operation, the substrate's
per-element identity is unambiguously encoded.
"""

import csv
from pathlib import Path
from collections import Counter

CR119 = Path(r"C:/VS/The_Courtroom/09a_PARTICLE_MASS_CHAIN/"
             r"CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/"
             r"CR119_courtroom_periodic_table.csv")
SIS = Path(r"C:/VS/Haunted_House/explorations/HH001_SIS_126x7_table.csv")
OUT = Path(r"C:/VS/Haunted_House/explorations/HH001_6channel_signatures.csv")

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
    if s == "-" or s == "":
        return 0
    if s == "0":
        return 0
    if "/" in s:
        a, b = s.split("/")
        return int(int(a) * 2 / int(b))
    return int(s) * 2

def parse_clock(c):
    if c == "stable":
        return 0
    if c == "radioactive":
        return 1
    return 0  # frontier default

results = []
for Z in sorted(elements.keys()):
    e = elements[Z]
    s = sis[Z]
    p, n, el = e["p"], e["n"], e["e"]

    particle = p + el + n
    matter   = p + n
    element  = Z
    gravity  = Z
    clock    = parse_clock(s["CLOCK"])
    action   = parse_spin_doubled(s["ACTION"])

    sig_xor = particle ^ matter ^ element ^ gravity ^ clock ^ action
    sig_sum = particle + matter + element + gravity + clock + action

    results.append({
        "Z": Z, "symbol": e["symbol"], "name": e["name"],
        "PARTICLE": particle, "MATTER": matter, "ELEMENT": element,
        "GRAVITY": gravity, "CLOCK": clock, "ACTION": action,
        "XOR_signature": sig_xor,
        "SUM_signature": sig_sum,
    })

xor_values = [r["XOR_signature"] for r in results]
sum_values = [r["SUM_signature"] for r in results]

xor_counter = Counter(xor_values)
sum_counter = Counter(sum_values)

print("=" * 65)
print(f"126 elements - 6-channel signature uniqueness test")
print("=" * 65)
print(f"XOR signatures:  {len(set(xor_values))}/126 distinct ({100*len(set(xor_values))/126:.1f}%)")
print(f"SUM signatures:  {len(set(sum_values))}/126 distinct ({100*len(set(sum_values))/126:.1f}%)")
print()

print("XOR collisions:")
xor_collisions = [(v, c) for v, c in xor_counter.items() if c > 1]
if not xor_collisions:
    print("  none - 126 distinct values")
else:
    for val, count in sorted(xor_collisions):
        cols = [r for r in results if r["XOR_signature"] == val]
        names = [f"{r['Z']}{r['symbol']}" for r in cols]
        print(f"  XOR={val:>3}: {count} elements: {names}")

print()
print("SUM collisions:")
sum_collisions = [(v, c) for v, c in sum_counter.items() if c > 1]
if not sum_collisions:
    print("  NONE - 126 DISTINCT VALUES")
else:
    for val, count in sorted(sum_collisions):
        cols = [r for r in results if r["SUM_signature"] == val]
        names = [f"{r['Z']}{r['symbol']}" for r in cols]
        print(f"  SUM={val:>4}: {count} elements: {names}")

print()
print(f"SUM range: {min(sum_values)} to {max(sum_values)}")
print(f"XOR range: {min(xor_values)} to {max(xor_values)}")

fieldnames = ["Z","symbol","name","PARTICLE","MATTER","ELEMENT",
              "GRAVITY","CLOCK","ACTION","XOR_signature","SUM_signature"]
with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in results:
        w.writerow(r)

print(f"\nSaved 126 rows to {OUT}")
