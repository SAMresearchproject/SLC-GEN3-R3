"""SOB126 Ledger — the full substrate order block as a substrate table.

Per Sean's spec: 32 columns, 126 rows. Three layers:
  Layer 1: 126-row native matter table  (Z → engine derivation)
  Layer 2: observed isotope comparison   (engine vs nature)
  Layer 3: binding and lane residuals    (B_smooth substrate kernel vs B_obs)

Outputs:
  SOB126_ledger.csv   — values, all 32 columns × 126 rows
  SOB126_ledger.xlsx  — live Excel formulas; change Z, watch everything recompute
"""
from __future__ import annotations

import csv
from fractions import Fraction
from math import gcd, sqrt
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

HERE = Path(__file__).parent
CR242 = HERE.parent / "CR242_SAM_BINDING_CURVATURE_DERIVATION" / "CR242_binding_dataset.csv"
OUT_CSV = HERE / "SOB126_ledger.csv"
OUT_XLSX = HERE / "SOB126_ledger.xlsx"

U_TO_MEV = 931.49410242
KAPPA = Fraction(7117, 768)
G_CONST = Fraction(1, 64)
MU_Q = Fraction(192, 7117)

# Observed-isotope lookup: Z → (symbol, name, observed_isotope_label, N_observed, m_obs_u)
# Z 1..118 use standard most-abundant stable isotope (or longest-lived for Tc, Pm, post-Bi).
# Z 119..126 are Sean's frontier predictions, no observed isotope.
# m_obs values are AME2020-class atomic masses; CR242 supplements where it has the row.
OBSERVED_DATA: dict[int, tuple[str, str, str, int, float | None]] = {
    1:  ("H",  "Hydrogen",       "H-1",     0,  1.00782503207),
    2:  ("He", "Helium",         "He-4",    2,  4.002603254),
    3:  ("Li", "Lithium",        "Li-7",    4,  7.016003434),
    4:  ("Be", "Beryllium",      "Be-9",    5,  9.012183065),
    5:  ("B",  "Boron",          "B-11",    6, 11.009305364),
    6:  ("C",  "Carbon",         "C-12",    6, 12.000000000),
    7:  ("N",  "Nitrogen",       "N-14",    7, 14.003074004),
    8:  ("O",  "Oxygen",         "O-16",    8, 15.994914620),
    9:  ("F",  "Fluorine",       "F-19",   10, 18.998403163),
    10: ("Ne", "Neon",           "Ne-20",  10, 19.992440176),
    11: ("Na", "Sodium",         "Na-23",  12, 22.989769282),
    12: ("Mg", "Magnesium",      "Mg-24",  12, 23.985041697),
    13: ("Al", "Aluminum",       "Al-27",  14, 26.981538531),
    14: ("Si", "Silicon",        "Si-28",  14, 27.976926535),
    15: ("P",  "Phosphorus",     "P-31",   16, 30.973761998),
    16: ("S",  "Sulfur",         "S-32",   16, 31.972071174),
    17: ("Cl", "Chlorine",       "Cl-35",  18, 34.968852682),
    18: ("Ar", "Argon",          "Ar-40",  22, 39.962383123),
    19: ("K",  "Potassium",      "K-39",   20, 38.963706679),
    20: ("Ca", "Calcium",        "Ca-40",  20, 39.962590866),
    21: ("Sc", "Scandium",       "Sc-45",  24, 44.955908275),
    22: ("Ti", "Titanium",       "Ti-48",  26, 47.947941980),
    23: ("V",  "Vanadium",       "V-51",   28, 50.943957009),
    24: ("Cr", "Chromium",       "Cr-52",  28, 51.940506231),
    25: ("Mn", "Manganese",      "Mn-55",  30, 54.938043191),
    26: ("Fe", "Iron",           "Fe-56",  30, 55.934936326),
    27: ("Co", "Cobalt",         "Co-59",  32, 58.933194288),
    28: ("Ni", "Nickel",         "Ni-58",  30, 57.935342414),
    29: ("Cu", "Copper",         "Cu-63",  34, 62.929597212),
    30: ("Zn", "Zinc",           "Zn-64",  34, 63.929142013),
    31: ("Ga", "Gallium",        "Ga-69",  38, 68.925573594),
    32: ("Ge", "Germanium",      "Ge-74",  42, 73.921177761),
    33: ("As", "Arsenic",        "As-75",  42, 74.921594562),
    34: ("Se", "Selenium",       "Se-80",  46, 79.916521776),
    35: ("Br", "Bromine",        "Br-79",  44, 78.918337601),
    36: ("Kr", "Krypton",        "Kr-84",  48, 83.911497728),
    37: ("Rb", "Rubidium",       "Rb-85",  48, 84.911789738),
    38: ("Sr", "Strontium",      "Sr-88",  50, 87.905612257),
    39: ("Y",  "Yttrium",        "Y-89",   50, 88.905838040),
    40: ("Zr", "Zirconium",      "Zr-90",  50, 89.904698755),
    41: ("Nb", "Niobium",        "Nb-93",  52, 92.906373013),
    42: ("Mo", "Molybdenum",     "Mo-98",  56, 97.905404482),
    43: ("Tc", "Technetium",     "Tc-98",  55, 97.907212),
    44: ("Ru", "Ruthenium",      "Ru-102", 58,101.904344096),
    45: ("Rh", "Rhodium",        "Rh-103", 58,102.905498401),
    46: ("Pd", "Palladium",      "Pd-106", 60,105.903480287),
    47: ("Ag", "Silver",         "Ag-107", 60,106.905091509),
    48: ("Cd", "Cadmium",        "Cd-114", 66,113.903365352),
    49: ("In", "Indium",         "In-115", 66,114.903878773),
    50: ("Sn", "Tin",            "Sn-120", 70,119.902201634),
    51: ("Sb", "Antimony",       "Sb-121", 70,120.903811966),
    52: ("Te", "Tellurium",      "Te-130", 78,129.906222748),
    53: ("I",  "Iodine",         "I-127",  74,126.904471838),
    54: ("Xe", "Xenon",          "Xe-132", 78,131.904155080),
    55: ("Cs", "Cesium",         "Cs-133", 78,132.905451961),
    56: ("Ba", "Barium",         "Ba-138", 82,137.905247237),
    57: ("La", "Lanthanum",      "La-139", 82,138.906356275),
    58: ("Ce", "Cerium",         "Ce-140", 82,139.905443127),
    59: ("Pr", "Praseodymium",   "Pr-141", 82,140.907657568),
    60: ("Nd", "Neodymium",      "Nd-142", 82,141.907728824),
    61: ("Pm", "Promethium",     "Pm-145", 84,144.912755748),
    62: ("Sm", "Samarium",       "Sm-152", 90,151.919739019),
    63: ("Eu", "Europium",       "Eu-153", 90,152.921237403),
    64: ("Gd", "Gadolinium",     "Gd-158", 94,157.924112349),
    65: ("Tb", "Terbium",        "Tb-159", 94,158.925354133),
    66: ("Dy", "Dysprosium",     "Dy-164", 98,163.929181874),
    67: ("Ho", "Holmium",        "Ho-165", 98,164.930328835),
    68: ("Er", "Erbium",         "Er-166", 98,165.930299323),
    69: ("Tm", "Thulium",        "Tm-169",100,168.934217954),
    70: ("Yb", "Ytterbium",      "Yb-174",104,173.938866437),
    71: ("Lu", "Lutetium",       "Lu-175",104,174.940775191),
    72: ("Hf", "Hafnium",        "Hf-180",108,179.946559544),
    73: ("Ta", "Tantalum",       "Ta-181",108,180.947995763),
    74: ("W",  "Tungsten",       "W-184", 110,183.950930929),
    75: ("Re", "Rhenium",        "Re-187",112,186.955750787),
    76: ("Os", "Osmium",         "Os-192",116,191.961477029),
    77: ("Ir", "Iridium",        "Ir-193",116,192.962921552),
    78: ("Pt", "Platinum",       "Pt-195",117,194.964791719),
    79: ("Au", "Gold",           "Au-197",118,196.966568795),
    80: ("Hg", "Mercury",        "Hg-202",122,201.970643011),
    81: ("Tl", "Thallium",       "Tl-205",124,204.974427801),
    82: ("Pb", "Lead",           "Pb-208",126,207.976652005),
    83: ("Bi", "Bismuth",        "Bi-209",126,208.980398734),
    84: ("Po", "Polonium",       "Po-209",125,208.982430420),
    85: ("At", "Astatine",       "At-210",125,209.987147423),
    86: ("Rn", "Radon",          "Rn-222",136,222.017577738),
    87: ("Fr", "Francium",       "Fr-223",136,223.019734241),
    88: ("Ra", "Radium",         "Ra-226",138,226.025409823),
    89: ("Ac", "Actinium",       "Ac-227",138,227.027750526),
    90: ("Th", "Thorium",        "Th-232",142,232.038055325),
    91: ("Pa", "Protactinium",   "Pa-231",140,231.035884000),
    92: ("U",  "Uranium",        "U-238", 146,238.050788268),
    93: ("Np", "Neptunium",      "Np-237",144,237.048173444),
    94: ("Pu", "Plutonium",      "Pu-244",150,244.064198000),
    95: ("Am", "Americium",      "Am-243",148,243.061380000),
    96: ("Cm", "Curium",         "Cm-247",151,247.070353000),
    97: ("Bk", "Berkelium",      "Bk-247",150,247.070307000),
    98: ("Cf", "Californium",    "Cf-251",153,251.079588000),
    99: ("Es", "Einsteinium",    "Es-252",153,252.082980000),
    100:("Fm", "Fermium",        "Fm-257",157,257.095106000),
    101:("Md", "Mendelevium",    "Md-258",157,258.098431000),
    102:("No", "Nobelium",       "No-259",157,259.101030000),
    103:("Lr", "Lawrencium",     "Lr-266",163,266.119830000),
    104:("Rf", "Rutherfordium",  "Rf-267",163,267.121790000),
    105:("Db", "Dubnium",        "Db-268",163,268.125670000),
    106:("Sg", "Seaborgium",     "Sg-269",163,269.128630000),
    107:("Bh", "Bohrium",        "Bh-270",163,270.133360000),
    108:("Hs", "Hassium",        "Hs-277",169,277.151990000),
    109:("Mt", "Meitnerium",     "Mt-278",169,278.156310000),
    110:("Ds", "Darmstadtium",   "Ds-281",171,281.164510000),
    111:("Rg", "Roentgenium",    "Rg-282",171,282.169120000),
    112:("Cn", "Copernicium",    "Cn-285",173,285.177120000),
    113:("Nh", "Nihonium",       "Nh-286",173,286.182210000),
    114:("Fl", "Flerovium",      "Fl-289",175,289.190420000),
    115:("Mc", "Moscovium",      "Mc-290",175,290.195980000),
    116:("Lv", "Livermorium",    "Lv-293",177,293.204490000),
    117:("Ts", "Tennessine",     "Ts-294",177,294.210460000),
    118:("Og", "Oganesson",      "Og-294",176,294.213920000),
    # Z 119..126: SAM frontier predictions, no observed isotope
    119:("Uue","Ununennium",     "",       0, None),
    120:("Ubn","Unbinilium",     "",       0, None),
    121:("Ubu","Unbiunium",      "",       0, None),
    122:("Ubb","Unbibium",       "",       0, None),
    123:("Ubt","Unbitrium",      "",       0, None),
    124:("Ubq","Unbiquadium",    "",       0, None),
    125:("Ubp","Unbipentium",    "",       0, None),
    126:("Ubh","Unbihexium",     "",       0, None),
}


# ── Engine ────────────────────────────────────────────────────────────────────
def derive_N_sob(Z: int) -> int:
    """N = Z + floor[(Z/R) · floor((Z-1)/R)]  per the SOB image."""
    radix_cycle = ((Z - 1) % 12) + 1
    selected_depth = max(0, radix_cycle - 1)
    delta_N = (Z * selected_depth) // 12
    return Z + delta_N


def channel_role(chi: float) -> str:
    if chi < 1.0:  return "substrate-light / mass-heavy"
    if chi > 1.0:  return "substrate-heavy / mass-light"
    return "balanced"


def clock_role(Z: int) -> str:
    if Z <= 83 and Z not in {43, 61}:
        return "clock-stable"
    return "clock-boundary"


def delta_pair_value(Z: int, N: int) -> int:
    if Z % 2 == 0 and N % 2 == 0: return +1
    if Z % 2 == 1 and N % 2 == 1: return -1
    return 0


def smooth_kernel_MeV(Z: int, N: int) -> float:
    """B_u^(0) = 8A - 17A^(2/3) - (3/4)·Z(Z-1)/A^(1/3) - 22(N-Z)²/A + 7δ/√A - (25/4)·Λ"""
    A = Z + N
    NmZ = N - Z
    g = gcd(Z, N) if (Z > 0 and N > 0) else max(Z, N, 1)
    a = Z // g if g else Z
    b = N // g if g else N
    Lambda = 0 if (a, b) == (1, 1) else 1
    vol = 8 * A
    surf = 17 * (A ** (2/3))
    coul = (3/4) * Z * (Z - 1) / (A ** (1/3)) if A > 0 else 0
    asym = 22 * NmZ * NmZ / A if A > 0 else 0
    pair = 7 * delta_pair_value(Z, N) / (A ** 0.5) if A > 0 else 0
    lane = (25/4) * Lambda
    return vol - surf - coul - asym + pair - lane


# ── Build a row ──────────────────────────────────────────────────────────────
def build_row(Z: int) -> dict:
    symbol, name, obs_iso, N_obs, m_obs_u = OBSERVED_DATA[Z]
    N_sob = derive_N_sob(Z)
    A_sob = Z + N_sob
    A_obs = (Z + N_obs) if obs_iso else 0  # check label, not N_obs (N=0 is valid for H-1)

    delta_N = N_sob - N_obs if obs_iso else None
    delta_A = A_sob - A_obs if obs_iso else None

    g_lattice = gcd(Z, N_sob) if (Z > 0 and N_sob > 0) else max(Z, N_sob, 1)
    prim_Z = Z // g_lattice if g_lattice else Z
    prim_N = N_sob // g_lattice if g_lattice else N_sob
    lane_ratio = Fraction(N_sob - Z, A_sob) if A_sob else Fraction(0)

    G_sub = float(Fraction(Z) * KAPPA + Fraction(N_sob - Z) * G_CONST)
    Q_sub = 8 * G_sub
    Q_mass = float(Fraction(4 * A_sob) * KAPPA)
    delta_Q = Q_mass - Q_sub
    chi = Q_sub / Q_mass if Q_mass else 0

    p_count = Z
    n_count = N_sob
    e_count = Z
    u_count = 2 * Z + N_sob
    d_count = Z + 2 * N_sob

    if m_obs_u is not None:
        B_u_u = A_obs - m_obs_u
        B_u_MeV = B_u_u * U_TO_MEV
        B_smooth_MeV = smooth_kernel_MeV(Z, N_obs)  # smooth kernel evaluated at OBSERVED (Z,N)
        residual_MeV = B_u_MeV - B_smooth_MeV
    else:
        B_u_u = None
        B_u_MeV = None
        B_smooth_MeV = smooth_kernel_MeV(Z, N_sob)   # for predictions, evaluate at engine (Z,N)
        residual_MeV = None

    # Row status notes
    if not obs_iso:
        row_status = "frontier_prediction"
        notes = f"SAM frontier (Z=119..126), no observed isotope; engine output Z={Z}, N={N_sob}, A={A_sob}"
    elif N_sob == N_obs:
        row_status = "engine_matches_observed"
        notes = ""
    else:
        row_status = "engine_diff_from_observed"
        notes = f"engine anchor {symbol}-{A_sob} differs from observed most-abundant {obs_iso}"

    return {
        "Z": Z,
        "symbol": symbol,
        "name": name,
        "N_sob": N_sob,
        "A_sob": A_sob,
        "observed_isotope": obs_iso,
        "N_observed": N_obs if obs_iso else "",
        "A_observed": A_obs if obs_iso else "",
        "delta_N": delta_N if delta_N is not None else "",
        "delta_A": delta_A if delta_A is not None else "",
        "lambda_gcd": g_lattice,
        "primitive_Z": prim_Z,
        "primitive_N": prim_N,
        "primitive_lane": f"({prim_Z},{prim_N})",
        "lane_ratio_NmZ_over_A": float(lane_ratio),
        "chi": chi,
        "p_count": p_count,
        "n_count": n_count,
        "e_count": e_count,
        "u_count": u_count,
        "d_count": d_count,
        "Q_sub": Q_sub,
        "Q_mass": Q_mass,
        "delta_Q": delta_Q,
        "channel_role": channel_role(chi),
        "B_u_u": B_u_u if B_u_u is not None else "",
        "B_u_MeV": B_u_MeV if B_u_MeV is not None else "",
        "B_smooth_MeV": B_smooth_MeV,
        "binding_residual_MeV": residual_MeV if residual_MeV is not None else "",
        "clock_role": clock_role(Z),
        "row_status": row_status,
        "notes": notes,
    }


# ── CSV writer ───────────────────────────────────────────────────────────────
COLUMNS = [
    "Z", "symbol", "name",
    "N_sob", "A_sob",
    "observed_isotope", "N_observed", "A_observed",
    "delta_N", "delta_A",
    "lambda_gcd", "primitive_Z", "primitive_N", "primitive_lane", "lane_ratio_NmZ_over_A",
    "chi",
    "p_count", "n_count", "e_count", "u_count", "d_count",
    "Q_sub", "Q_mass", "delta_Q", "channel_role",
    "B_u_u", "B_u_MeV", "B_smooth_MeV", "binding_residual_MeV",
    "clock_role", "row_status", "notes",
]


def write_csv(rows: list[dict]) -> None:
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow(r)


# ── XLSX writer with live formulas ───────────────────────────────────────────
def write_xlsx(rows: list[dict]) -> None:
    """Write XLSX where every derived quantity is an Excel formula referencing Z.

    Sheet "SOB126" — the main table with formulas.
    Sheet "Constants" — substrate constants (R, D, S, κ, g, μ_Q).
    Sheet "Observed" — lookup table of observed-isotope info per Z.
    """
    wb = openpyxl.Workbook()

    # ─── Constants sheet ───
    consts_ws = wb.active
    consts_ws.title = "Constants"
    consts_data = [
        ("name", "value", "meaning"),
        ("R", 12, "radix (substrate route shape)"),
        ("D", 3, "substrate dimension"),
        ("S", 8, "split inventory shape (octet)"),
        ("alpha_H", 2, "partition algebra generator"),
        ("Theta", 18, "overlap shape (alpha_H * D^2)"),
        ("F", 81, "face shape (D^4)"),
        ("M", 126, "retained matter-support shape"),
        ("L", 162, "closed carrier ledger"),
        ("kappa_num", 7117, "kappa numerator (7117/768)"),
        ("kappa_den", 768, "kappa denominator"),
        ("g_num", 1, "g numerator (1/64)"),
        ("g_den", 64, "g denominator"),
        ("mu_Q_num", 192, "mu_Q numerator (192/7117)"),
        ("mu_Q_den", 7117, "mu_Q denominator"),
        ("U_TO_MEV", U_TO_MEV, "CODATA atomic mass unit in MeV"),
    ]
    for r in consts_data:
        consts_ws.append(r)
    for cell in consts_ws[1]:
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor="DDDDDD")

    # ─── Observed lookup sheet ───
    obs_ws = wb.create_sheet("Observed_Lookup")
    obs_ws.append(["Z", "symbol", "name", "observed_isotope", "N_observed", "A_observed", "m_obs_u"])
    for Z in range(1, 127):
        sym, nm, iso, Nobs, mobs = OBSERVED_DATA[Z]
        Aobs = (Z + Nobs) if iso else ""
        obs_ws.append([Z, sym, nm, iso, Nobs if iso else "", Aobs, mobs if mobs is not None else ""])
    for cell in obs_ws[1]:
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor="DDDDDD")

    # ─── Main SOB126 sheet ───
    ws = wb.create_sheet("SOB126", 0)  # insert at index 0 so it's first
    ws.append(COLUMNS)
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor="DDDDDD")

    # Column letter map
    col = {name: get_column_letter(i + 1) for i, name in enumerate(COLUMNS)}

    for row_i, Z in enumerate(range(1, 127), start=2):  # row 2 onwards
        # Direct inputs
        ws.cell(row=row_i, column=1, value=Z)  # Z
        sym, nm, iso, Nobs, mobs = OBSERVED_DATA[Z]
        ws.cell(row=row_i, column=2, value=sym)
        ws.cell(row=row_i, column=3, value=nm)

        # N_sob (engine formula)
        # N = Z + INT(Z * INT((Z-1)/12) / 12)
        cZ = f"{col['Z']}{row_i}"
        n_formula = f"={cZ} + INT({cZ} * INT(({cZ}-1)/12) / 12)"
        ws.cell(row=row_i, column=4, value=n_formula)

        cN = f"{col['N_sob']}{row_i}"
        ws.cell(row=row_i, column=5, value=f"={cZ}+{cN}")  # A_sob

        # Observed lookup (using VLOOKUP from Observed_Lookup)
        ws.cell(row=row_i, column=6, value=f"=VLOOKUP({cZ}, Observed_Lookup!A:G, 4, FALSE)")  # observed_isotope
        ws.cell(row=row_i, column=7, value=f"=VLOOKUP({cZ}, Observed_Lookup!A:G, 5, FALSE)")  # N_observed
        ws.cell(row=row_i, column=8, value=f"=VLOOKUP({cZ}, Observed_Lookup!A:G, 6, FALSE)")  # A_observed

        cNobs = f"{col['N_observed']}{row_i}"
        cAobs = f"{col['A_observed']}{row_i}"
        cAsob = f"{col['A_sob']}{row_i}"
        cObsIso = f"{col['observed_isotope']}{row_i}"

        # delta_N, delta_A (only if observed_isotope is non-empty)
        ws.cell(row=row_i, column=9, value=f'=IF({cObsIso}="","",{cN}-{cNobs})')
        ws.cell(row=row_i, column=10, value=f'=IF({cObsIso}="","",{cAsob}-{cAobs})')

        # lambda_gcd, primitive_Z, primitive_N
        ws.cell(row=row_i, column=11, value=f"=GCD({cZ},{cN})")  # lambda_gcd
        cLam = f"{col['lambda_gcd']}{row_i}"
        ws.cell(row=row_i, column=12, value=f"={cZ}/{cLam}")  # primitive_Z
        ws.cell(row=row_i, column=13, value=f"={cN}/{cLam}")  # primitive_N
        cPrimZ = f"{col['primitive_Z']}{row_i}"
        cPrimN = f"{col['primitive_N']}{row_i}"
        ws.cell(row=row_i, column=14, value=f'="("&{cPrimZ}&","&{cPrimN}&")"')  # primitive_lane

        ws.cell(row=row_i, column=15, value=f"=({cN}-{cZ})/{cAsob}")  # lane_ratio

        # Substrate (G_sub = Z*κ + (N-Z)*g; Q_sub = 8*G_sub; Q_mass = 4*A*κ)
        kappa = "(7117/768)"
        g_const = "(1/64)"
        ws.cell(row=row_i, column=22, value=f"=8*({cZ}*{kappa}+({cN}-{cZ})*{g_const})")  # Q_sub
        ws.cell(row=row_i, column=23, value=f"=4*{cAsob}*{kappa}")  # Q_mass
        cQsub = f"{col['Q_sub']}{row_i}"
        cQmass = f"{col['Q_mass']}{row_i}"
        ws.cell(row=row_i, column=24, value=f"={cQmass}-{cQsub}")  # delta_Q
        ws.cell(row=row_i, column=16, value=f"={cQsub}/{cQmass}")  # chi
        cChi = f"{col['chi']}{row_i}"

        # Counts
        ws.cell(row=row_i, column=17, value=f"={cZ}")  # p_count
        ws.cell(row=row_i, column=18, value=f"={cN}")  # n_count
        ws.cell(row=row_i, column=19, value=f"={cZ}")  # e_count
        ws.cell(row=row_i, column=20, value=f"=2*{cZ}+{cN}")  # u_count
        ws.cell(row=row_i, column=21, value=f"={cZ}+2*{cN}")  # d_count

        # channel_role (text classifier)
        ws.cell(row=row_i, column=25, value=(
            f'=IF({cChi}<1,"substrate-light / mass-heavy",'
            f'IF({cChi}>1,"substrate-heavy / mass-light","balanced"))'
        ))

        # B_u (only if observed): use observed mass via VLOOKUP
        obs_mass_lookup = f'IFERROR(VLOOKUP({cZ}, Observed_Lookup!A:G, 7, FALSE),"")'
        ws.cell(row=row_i, column=26, value=f'=IF({cObsIso}="","",{cAobs}-{obs_mass_lookup})')  # B_u_u
        cBuU = f"{col['B_u_u']}{row_i}"
        ws.cell(row=row_i, column=27, value=f'=IF({cBuU}="","",{cBuU}*{U_TO_MEV})')  # B_u_MeV

        # B_smooth_MeV: evaluate kernel at (Z, N_used) where N_used = N_observed if available else N_sob
        # delta_pair logic
        n_for_kernel = f'IF({cObsIso}="",{cN},{cNobs})'
        # Z_for_kernel is just cZ
        # A for kernel = Z + N_used
        a_for_kernel = f'({cZ}+{n_for_kernel})'
        delta_p = (
            f'IF(AND(MOD({cZ},2)=0,MOD({n_for_kernel},2)=0),1,'
            f'IF(AND(MOD({cZ},2)=1,MOD({n_for_kernel},2)=1),-1,0))'
        )
        nmz = f'({n_for_kernel}-{cZ})'
        # Lambda based on primitive of (Z, N_used)
        gcd_used = f'GCD({cZ},{n_for_kernel})'
        a_prim = f'({cZ}/{gcd_used})'
        b_prim = f'({n_for_kernel}/{gcd_used})'
        Lambda = f'IF(AND({a_prim}=1,{b_prim}=1),0,1)'
        b_smooth = (
            f'=8*{a_for_kernel}'
            f'-17*{a_for_kernel}^(2/3)'
            f'-(3/4)*{cZ}*({cZ}-1)/{a_for_kernel}^(1/3)'
            f'-22*{nmz}^2/{a_for_kernel}'
            f'+7*{delta_p}/SQRT({a_for_kernel})'
            f'-(25/4)*{Lambda}'
        )
        ws.cell(row=row_i, column=28, value=b_smooth)
        cBsmooth = f"{col['B_smooth_MeV']}{row_i}"

        # binding_residual_MeV = B_u_MeV - B_smooth_MeV (only if observed)
        cBuMeV = f"{col['B_u_MeV']}{row_i}"
        ws.cell(row=row_i, column=29, value=f'=IF({cBuMeV}="","",{cBuMeV}-{cBsmooth})')

        # clock_role
        ws.cell(row=row_i, column=30, value=(
            f'=IF(AND({cZ}<=83,{cZ}<>43,{cZ}<>61),"clock-stable","clock-boundary")'
        ))

        # row_status, notes — static text, set after we have all values
        row_data = build_row(Z)
        ws.cell(row=row_i, column=31, value=row_data["row_status"])
        ws.cell(row=row_i, column=32, value=row_data["notes"])

    # Column widths
    widths = {
        "Z": 5, "symbol": 7, "name": 14, "N_sob": 7, "A_sob": 7,
        "observed_isotope": 16, "N_observed": 11, "A_observed": 11,
        "delta_N": 8, "delta_A": 8,
        "lambda_gcd": 11, "primitive_Z": 11, "primitive_N": 11, "primitive_lane": 14,
        "lane_ratio_NmZ_over_A": 18,
        "chi": 10,
        "p_count": 8, "n_count": 8, "e_count": 8, "u_count": 8, "d_count": 8,
        "Q_sub": 14, "Q_mass": 14, "delta_Q": 12, "channel_role": 32,
        "B_u_u": 12, "B_u_MeV": 12, "B_smooth_MeV": 13, "binding_residual_MeV": 19,
        "clock_role": 16, "row_status": 25, "notes": 60,
    }
    for name, w in widths.items():
        ws.column_dimensions[col[name]].width = w
    ws.freeze_panes = "D2"

    wb.save(OUT_XLSX)


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    rows = [build_row(Z) for Z in range(1, 127)]
    write_csv(rows)
    write_xlsx(rows)

    print(f"Wrote {len(rows)} rows.")
    print(f"CSV : {OUT_CSV}")
    print(f"XLSX: {OUT_XLSX} (open in Excel — formulas live, change Z and watch row recompute)")
    print()

    # Spot-check the Au-197 row against the gold image
    au = next(r for r in rows if r["Z"] == 79)
    print("Au-197 spot-check (should match SOB79 gold image):")
    print(f"  Z = {au['Z']}, N_sob = {au['N_sob']}, A_sob = {au['A_sob']}")
    print(f"  G_sub (Q-units) = {au['Q_sub']/8:.6f}  (image: 732.696615)")
    print(f"  Q_sub  = {au['Q_sub']:.6f}  (image: 5861.572917)")
    print(f"  Q_mass = {au['Q_mass']:.6f}  (image: 7302.338542)")
    print(f"  chi    = {au['chi']:.6f}  (image: 0.802698)")
    print(f"  B_u (observed, u) = {au['B_u_u']:.6f}  (image: 0.033)")
    print(f"  B_smooth_MeV (substrate kernel) = {au['B_smooth_MeV']:.4f}")
    print(f"  residual MeV = {au['binding_residual_MeV']:.4f}")
    print(f"  clock_role = {au['clock_role']}, channel_role = {au['channel_role']}")
    print(f"  primitive_lane = {au['primitive_lane']}, lambda = {au['lambda_gcd']}")
    print(f"  source quarks: u={au['u_count']}, d={au['d_count']}, e={au['e_count']}")

    # Summary
    print()
    n_match = sum(1 for r in rows if r["row_status"] == "engine_matches_observed")
    n_diff = sum(1 for r in rows if r["row_status"] == "engine_diff_from_observed")
    n_pred = sum(1 for r in rows if r["row_status"] == "frontier_prediction")
    n_with_residual = sum(1 for r in rows if isinstance(r["binding_residual_MeV"], (int, float)))
    print(f"Status counts: engine_matches_observed={n_match}, engine_diff={n_diff}, frontier_prediction={n_pred}")
    print(f"Rows with binding residual computable (B_u observed available): {n_with_residual}")


if __name__ == "__main__":
    main()
