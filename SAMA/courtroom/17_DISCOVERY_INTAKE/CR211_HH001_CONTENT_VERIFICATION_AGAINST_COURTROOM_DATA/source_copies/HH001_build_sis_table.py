"""HH001 supporting: build the 126 x 7 SIS table.

Reads C:/VS/The_Courtroom/.../CR119_courtroom_periodic_table.csv for the
columns that already exist in SAM (PARTICLE, ELEMENT, GRAVITY via qA).
Adds the four remaining SIS channels (MATTER, CLOCK, LIGHT, ACTION) from
embedded standard-physics reference data.

Column meaning (placement-grade per HOUSE_RULES):
  cell_id   : SIS-NNN sequential index over the 126 rows
  Z         : atomic number (from CR119)
  symbol    : element symbol (CR119 known_symbol or 'frontier-Z')
  name      : element name (CR119 known_name or 'SAM frontier')

  PARTICLE  : total atomic particle count = 2Z + N
              (protons + electrons + neutrons in the neutral atom)
              from CR119 proton_count, electron_count, neutron_count_primary
  MATTER    : atomic weight in amu (standard reference)
  ELEMENT   : Z (atomic number, the binding identity)
  GRAVITY   : qA_total_primary from CR119 (SAM-native A-source value)
  CLOCK     : stability classification of the primary isotope
              ('stable' / 'radioactive' / '-' for SAM frontier)
  LIGHT     : principal emission-line wavelength (nm) of the dominant
              visible / nearest-visible transition. '-' where not clean.
  ACTION    : nuclear spin I of the most common stable isotope
              (or principal isotope if no stable form exists).
              '-' for SAM frontier rows.

Frontier Z=119-126 rows are populated only for the columns CR119 supplies
(PARTICLE, ELEMENT, GRAVITY). MATTER/CLOCK/LIGHT/ACTION are '-' because
SAM forward-blind discipline forbids fabricating those values.
"""

import csv
from pathlib import Path

CR119_CSV = Path(
    r"C:/VS/The_Courtroom/09a_PARTICLE_MASS_CHAIN/"
    r"CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/"
    r"CR119_courtroom_periodic_table.csv"
)
OUTPUT_CSV = Path(r"C:/VS/Haunted_House/explorations/HH001_SIS_126x7_table.csv")

# ---------------------------------------------------------------------------
# Standard atomic weights (amu) for Z = 1..118
# Values follow IUPAC 2021 standard atomic weights, rounded to 4-5 sig figs.
# For synthetic elements where no stable isotope exists, the mass number
# of the longest-lived known isotope is given.
ATOMIC_MASS = {
    1: 1.008,    2: 4.0026,  3: 6.94,     4: 9.0122,  5: 10.81,    6: 12.011,
    7: 14.007,   8: 15.999,  9: 18.998,   10: 20.180, 11: 22.990,  12: 24.305,
    13: 26.982,  14: 28.085, 15: 30.974,  16: 32.06,  17: 35.45,   18: 39.948,
    19: 39.098,  20: 40.078, 21: 44.956,  22: 47.867, 23: 50.942,  24: 51.996,
    25: 54.938,  26: 55.845, 27: 58.933,  28: 58.693, 29: 63.546,  30: 65.38,
    31: 69.723,  32: 72.630, 33: 74.922,  34: 78.971, 35: 79.904,  36: 83.798,
    37: 85.468,  38: 87.62,  39: 88.906,  40: 91.224, 41: 92.906,  42: 95.95,
    43: 98.0,    44: 101.07, 45: 102.91,  46: 106.42, 47: 107.87,  48: 112.41,
    49: 114.82,  50: 118.71, 51: 121.76,  52: 127.60, 53: 126.90,  54: 131.29,
    55: 132.91,  56: 137.33, 57: 138.91,  58: 140.12, 59: 140.91,  60: 144.24,
    61: 145.0,   62: 150.36, 63: 151.96,  64: 157.25, 65: 158.93,  66: 162.50,
    67: 164.93,  68: 167.26, 69: 168.93,  70: 173.05, 71: 174.97,  72: 178.49,
    73: 180.95,  74: 183.84, 75: 186.21,  76: 190.23, 77: 192.22,  78: 195.08,
    79: 196.97,  80: 200.59, 81: 204.38,  82: 207.2,  83: 208.98,  84: 209.0,
    85: 210.0,   86: 222.0,  87: 223.0,   88: 226.0,  89: 227.0,   90: 232.04,
    91: 231.04,  92: 238.03, 93: 237.0,   94: 244.0,  95: 243.0,   96: 247.0,
    97: 247.0,   98: 251.0,  99: 252.0,   100: 257.0, 101: 258.0,  102: 259.0,
    103: 266.0,  104: 267.0, 105: 268.0,  106: 269.0, 107: 270.0,  108: 277.0,
    109: 278.0,  110: 281.0, 111: 282.0,  112: 285.0, 113: 286.0,  114: 289.0,
    115: 290.0,  116: 293.0, 117: 294.0,  118: 294.0,
}

# Clock channel: 'stable' if a stable isotope exists, else 'radioactive'.
# All Z = 43 (Tc) and 61 (Pm), plus everything Z >= 84 is radioactive only.
def clock_value(Z):
    if Z in (43, 61):
        return "radioactive"
    if Z >= 84:
        return "radioactive"
    if 1 <= Z <= 118:
        return "stable"
    return "-"

# Nuclear spin I of the most common stable isotope (or principal isotope).
# Standard reference values. '-' where data is unclear or frontier.
NUCLEAR_SPIN = {
    1: "1/2",  2: "0",    3: "3/2",  4: "3/2",  5: "3/2",  6: "0",
    7: "1",    8: "0",    9: "1/2",  10: "0",   11: "3/2", 12: "0",
    13: "5/2", 14: "0",   15: "1/2", 16: "0",   17: "3/2", 18: "0",
    19: "3/2", 20: "0",   21: "7/2", 22: "0",   23: "7/2", 24: "0",
    25: "5/2", 26: "0",   27: "7/2", 28: "0",   29: "3/2", 30: "0",
    31: "3/2", 32: "0",   33: "3/2", 34: "0",   35: "3/2", 36: "0",
    37: "5/2", 38: "0",   39: "1/2", 40: "0",   41: "9/2", 42: "0",
    43: "9/2", 44: "5/2", 45: "1/2", 46: "0",   47: "1/2", 48: "1/2",
    49: "9/2", 50: "0",   51: "5/2", 52: "0",   53: "5/2", 54: "0",
    55: "7/2", 56: "3/2", 57: "7/2", 58: "0",   59: "5/2", 60: "0",
    61: "5/2", 62: "0",   63: "5/2", 64: "0",   65: "3/2", 66: "0",
    67: "7/2", 68: "0",   69: "1/2", 70: "0",   71: "7/2", 72: "0",
    73: "7/2", 74: "0",   75: "5/2", 76: "0",   77: "3/2", 78: "1/2",
    79: "3/2", 80: "1/2", 81: "1/2", 82: "0",   83: "9/2", 84: "0",
    85: "9/2", 86: "0",   87: "1/2", 88: "0",   89: "3/2", 90: "0",
    91: "3/2", 92: "0",   93: "5/2", 94: "0",   95: "5/2", 96: "0",
    97: "3/2", 98: "0",   99: "7/2", 100: "0",  101: "9/2", 102: "0",
    103: "-",  104: "-",  105: "-",  106: "-",  107: "-",   108: "-",
    109: "-",  110: "-",  111: "-",  112: "-",  113: "-",   114: "-",
    115: "-",  116: "-",  117: "-",  118: "-",
}

# Light channel: principal emission-line wavelength (nm) of a representative
# strong neutral-atom line. Sources: NIST atomic spectra, standard
# spectroscopy references. Values rounded to nearest nm.
# These are placement-grade; refinement requires NIST-direct retrieval.
LIGHT_NM = {
    1: 656,    # H-alpha
    2: 587,    # He I yellow D3
    3: 670,    # Li I red
    4: 234,    # Be I UV
    5: 250,    # B I UV
    6: 248,    # C I UV
    7: 500,    # N I (one of many in visible)
    8: 777,    # O I red triplet
    9: 685,    # F I red
    10: 585,   # Ne I orange (signage)
    11: 589,   # Na D line
    12: 285,   # Mg I UV/violet
    13: 396,   # Al I violet
    14: 251,   # Si I UV
    15: 213,   # P I UV
    16: 469,   # S I blue
    17: 542,   # Cl I green
    18: 696,   # Ar I red
    19: 766,   # K I red
    20: 423,   # Ca I violet
    21: 391,   # Sc I violet
    22: 365,   # Ti I near-UV
    23: 437,   # V I violet
    24: 425,   # Cr I violet
    25: 403,   # Mn I violet
    26: 372,   # Fe I near-UV/violet
    27: 345,   # Co I UV
    28: 352,   # Ni I UV/violet
    29: 325,   # Cu I UV
    30: 214,   # Zn I UV
    31: 417,   # Ga I violet
    32: 265,   # Ge I UV
    33: 235,   # As I UV
    34: 207,   # Se I UV
    35: 478,   # Br I blue
    36: 557,   # Kr I yellow-green
    37: 780,   # Rb I red
    38: 461,   # Sr I blue (flame)
    39: 410,   # Y I violet
    40: 360,   # Zr I near-UV
    41: 405,   # Nb I violet
    42: 313,   # Mo I UV
    43: 363,   # Tc I near-UV
    44: 349,   # Ru I UV
    45: 343,   # Rh I UV
    46: 247,   # Pd I UV
    47: 328,   # Ag I UV
    48: 326,   # Cd I UV/violet
    49: 451,   # In I blue
    50: 286,   # Sn I UV
    51: 252,   # Sb I UV
    52: 238,   # Te I UV
    53: 206,   # I I UV
    54: 467,   # Xe I blue
    55: 852,   # Cs I near-IR D
    56: 553,   # Ba I green
    57: 550,   # La I yellow-green
    58: 569,   # Ce I yellow
    59: 422,   # Pr I violet
    60: 463,   # Nd I blue
    61: 467,   # Pm I blue
    62: 488,   # Sm I blue
    63: 459,   # Eu I blue
    64: 363,   # Gd I UV
    65: 432,   # Tb I violet
    66: 421,   # Dy I violet
    67: 410,   # Ho I violet
    68: 386,   # Er I near-UV
    69: 372,   # Tm I near-UV
    70: 399,   # Yb I violet
    71: 452,   # Lu I blue
    72: 286,   # Hf I UV
    73: 271,   # Ta I UV
    74: 401,   # W I violet
    75: 346,   # Re I near-UV
    76: 290,   # Os I UV
    77: 380,   # Ir I near-UV
    78: 266,   # Pt I UV
    79: 268,   # Au I UV (242 nm is also prominent)
    80: 254,   # Hg I (famous 253.7 nm UV)
    81: 535,   # Tl I green
    82: 405,   # Pb I violet
    83: 306,   # Bi I UV
    84: 255,   # Po I UV
    85: "-",   # At, limited data
    86: 705,   # Rn I red
    87: "-",   # Fr, limited data
    88: 482,   # Ra I blue
    89: "-",   # Ac, limited data
    90: 401,   # Th I violet
    91: "-",   # Pa, limited data
    92: 386,   # U I near-UV
    93: 392,   # Np I violet
    94: 414,   # Pu I violet
    95: 408,   # Am I violet
    96: "-",   # Cm, limited data
    97: "-",   # Bk, limited data
    98: "-",   # Cf
    99: "-",   # Es
    100: "-",  # Fm
    101: "-",  # Md
    102: "-",  # No
    103: "-",  # Lr
    104: "-",  # Rf
    105: "-",  # Db
    106: "-",  # Sg
    107: "-",  # Bh
    108: "-",  # Hs
    109: "-",  # Mt
    110: "-",  # Ds
    111: "-",  # Rg
    112: "-",  # Cn
    113: "-",  # Nh
    114: "-",  # Fl
    115: "-",  # Mc
    116: "-",  # Lv
    117: "-",  # Ts
    118: "-",  # Og
}


def main():
    elements = []
    with CR119_CSV.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            elements.append(row)

    if len(elements) != 126:
        print(f"WARNING: expected 126 rows in CR119 periodic table, got {len(elements)}")

    sis_rows = []
    for el in elements:
        Z = int(el["Z"])
        protons = int(el["proton_count"])
        electrons = int(el["electron_count"])
        neutrons = int(el["neutron_count_primary"])
        symbol = el["known_symbol"].strip() if el["known_symbol"].strip() else f"Z{Z}"
        name = el["known_name"].strip() if el["known_name"].strip() else "SAM frontier"
        qA = float(el["qA_total_primary"])

        particle = protons + electrons + neutrons  # total particle count
        element = Z

        if Z <= 118:
            matter = ATOMIC_MASS.get(Z, "-")
            clock = clock_value(Z)
            light = LIGHT_NM.get(Z, "-")
            action = NUCLEAR_SPIN.get(Z, "-")
        else:
            matter = "-"
            clock = "-"
            light = "-"
            action = "-"

        sis_rows.append({
            "cell_id":  f"SIS-{Z:03d}",
            "Z":         Z,
            "symbol":    symbol,
            "name":      name,
            "PARTICLE":  particle,
            "MATTER":    matter,
            "ELEMENT":   element,
            "GRAVITY":   f"{qA:.6f}",
            "CLOCK":     clock,
            "LIGHT":     light,
            "ACTION":    action,
        })

    fieldnames = [
        "cell_id", "Z", "symbol", "name",
        "PARTICLE", "MATTER", "ELEMENT", "GRAVITY",
        "CLOCK", "LIGHT", "ACTION",
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in sis_rows:
            writer.writerow(r)

    print(f"Wrote {len(sis_rows)} SIS rows to {OUTPUT_CSV}")
    print()
    print("First 10 rows:")
    print(f"{'cell_id':<10}{'sym':<5}{'name':<14}{'PART':>5}{'MATTER':>9}{'ELEM':>5}{'GRAVITY':>14}{'CLOCK':>14}{'LIGHT':>7}{'ACT':>6}")
    for r in sis_rows[:10]:
        print(f"{r['cell_id']:<10}{r['symbol']:<5}{r['name']:<14}{r['PARTICLE']:>5}{str(r['MATTER']):>9}{r['ELEMENT']:>5}{r['GRAVITY']:>14}{r['CLOCK']:>14}{str(r['LIGHT']):>7}{r['ACTION']:>6}")
    print()
    print("Frontier rows (Z=119-126):")
    print(f"{'cell_id':<10}{'sym':<5}{'name':<14}{'PART':>5}{'MATTER':>9}{'ELEM':>5}{'GRAVITY':>14}{'CLOCK':>14}{'LIGHT':>7}{'ACT':>6}")
    for r in sis_rows[-8:]:
        print(f"{r['cell_id']:<10}{r['symbol']:<5}{r['name']:<14}{r['PARTICLE']:>5}{str(r['MATTER']):>9}{r['ELEMENT']:>5}{r['GRAVITY']:>14}{r['CLOCK']:>14}{str(r['LIGHT']):>7}{r['ACTION']:>6}")


if __name__ == "__main__":
    main()
