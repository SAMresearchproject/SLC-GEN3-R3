"""SOB engine — compute the full substrate order block for every element Z=1..126.

Per v0.7 §9.6: one integer Z enters; the engine derives N, A, particle source address,
quark content, G_sub, Q_sub, Q_mass, m_0 baseline, χ channel ratio, and stability status.

This is forward derivation from substrate constants alone. No observed mass enters
the construction. B_u column is added afterwards from CR242 AME2020 m_observed when
available, computed as A·u − m_obs.

Outputs two CSVs:
  SOB_engine_output.csv    — pure substrate derivation per element (no observed)
  SOB_with_observed.csv    — same + m_obs + B_u where CR242 has data
"""
from __future__ import annotations

import csv
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 50

# Sealed substrate atoms (from CR238 / CR221 / CR240)
R = Fraction(12)
D = Fraction(3)
S = Fraction(8)
ALPHA_H = Fraction(2)
KAPPA = Fraction(7117, 768)
G = Fraction(1, 64)
MU_Q = Fraction(192, 7117)

U_TO_MEV = Decimal("931.49410242")

HERE = Path(__file__).parent
CR242 = HERE.parent / "CR242_SAM_BINDING_CURVATURE_DERIVATION" / "CR242_binding_dataset.csv"
ENGINE_CSV = HERE / "SOB_engine_output.csv"
COMBINED_CSV = HERE / "SOB_with_observed.csv"


# Element symbol table (Z=1..126)
ELEMENT_SYMBOLS = [
    "",  # Z=0 placeholder
    "H","He","Li","Be","B","C","N","O","F","Ne",
    "Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca",
    "Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn",
    "Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr",
    "Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn",
    "Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd",
    "Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb",
    "Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg",
    "Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th",
    "Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm",
    "Md","No","Lr","Rf","Db","Sg","Bh","Hs","Mt","Ds",
    "Rg","Cn","Nh","Fl","Mc","Lv","Ts","Og","Uue","Ubn",
    "Ubu","Ubb","Ubt","Ubq","Ubp","Ubh",
]


def derive_N(Z: int) -> int:
    """Engine neutron-count rule per v0.7 §9.6:

        radix_cycle = ((Z - 1) mod 12) + 1
        selected_depth = max(0, radix_cycle - 1)
        ΔN = floor(Z · selected_depth / 12)
        N = Z + ΔN

    Equivalently the SOB image formula N = Z + floor[(Z/R) · floor((Z-1)/R)].
    """
    radix_cycle = ((Z - 1) % 12) + 1
    selected_depth = max(0, radix_cycle - 1)
    delta_N = (Z * selected_depth) // 12
    return Z + delta_N


def derive_block(Z: int) -> dict:
    """Compute full SOB block for one element."""
    N = derive_N(Z)
    A = Z + N
    NmZ = N - Z

    # Particle source address
    u_count = 2 * Z + N      # up quarks
    d_count = Z + 2 * N      # down quarks
    e_count = Z              # electrons
    p_count = Z              # protons
    n_count = N              # neutrons

    # Substrate Q-charges (exact Fraction)
    G_sub = Fraction(Z) * KAPPA + Fraction(NmZ) * G          # Q-units
    Q_sub = S * G_sub                                          # = 8·G_sub
    Q_mass = Fraction(4 * A) * KAPPA                           # = 4Aκ

    # Channel ratio χ = Q_sub / Q_mass
    chi = Q_sub / Q_mass

    # Baseline mass m_0 = μ_Q · Q_mass = A · u (in atomic mass units, exactly A)
    m_0 = MU_Q * Q_mass  # equals Fraction(A) exactly

    # GR retained/released split per v0.7 §9.6
    GR = S * G_sub                  # = Q_sub
    retained_7G = Fraction(7) * G_sub
    released_G = G_sub               # = 1·G_sub

    # Stability (clock status)
    if Z > 83 or Z in {43, 61}:
        stability = "UNSTABLE"
    else:
        stability = "STABLE"

    # Radix cycle position
    radix_cycle = ((Z - 1) % 12) + 1
    selected_depth = max(0, radix_cycle - 1)

    return {
        "Z": Z,
        "Symbol": ELEMENT_SYMBOLS[Z] if Z < len(ELEMENT_SYMBOLS) else "?",
        "N": N,
        "A": A,
        "NmZ": NmZ,
        "anchor": f"{ELEMENT_SYMBOLS[Z] if Z < len(ELEMENT_SYMBOLS) else '?'}-{A}",
        "u_count": u_count,
        "d_count": d_count,
        "e_count": e_count,
        "p_count": p_count,
        "n_count": n_count,
        "G_sub_F": G_sub,
        "Q_sub_F": Q_sub,
        "Q_mass_F": Q_mass,
        "chi_F": chi,
        "m_0_F": m_0,           # equals Fraction(A) — atomic mass units, exact
        "GR_F": GR,
        "retained_7G_F": retained_7G,
        "released_G_F": released_G,
        "stability": stability,
        "radix_cycle": radix_cycle,
        "selected_depth": selected_depth,
    }


def load_cr242_observed() -> dict[tuple[int, int], dict]:
    """Load observed masses keyed by (Z, N) from CR242."""
    out = {}
    with CR242.open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                Z = int(float(r["Z"]))
                N = int(float(r["N"]))
                A = int(float(r["A"]))
                m_obs_str = r["m_measured_u"]
                B_u_str = r["B_u"]
            except (KeyError, ValueError):
                continue
            out[(Z, N)] = {
                "isotope": r["isotope"],
                "m_obs_u": Decimal(m_obs_str.strip()),
                "B_obs_u": Decimal(B_u_str.strip()),
            }
    return out


def frac_to_dec_str(f: Fraction, places: int = 8) -> str:
    d = Decimal(f.numerator) / Decimal(f.denominator)
    return f"{d.quantize(Decimal('1.' + '0' * places))}"


def main():
    observed = load_cr242_observed()
    rows = [derive_block(Z) for Z in range(1, 127)]

    # Write engine-only CSV (no observed)
    with ENGINE_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "Z", "Symbol", "N", "A", "anchor",
            "p", "n", "e", "u", "d",
            "G_sub", "Q_sub", "Q_mass", "chi",
            "m_0_baseline_u", "GR", "retained_7G", "released_G",
            "stability", "radix_cycle", "selected_depth",
        ])
        for r in rows:
            w.writerow([
                r["Z"], r["Symbol"], r["N"], r["A"], r["anchor"],
                r["p_count"], r["n_count"], r["e_count"], r["u_count"], r["d_count"],
                frac_to_dec_str(r["G_sub_F"], 8),
                frac_to_dec_str(r["Q_sub_F"], 8),
                frac_to_dec_str(r["Q_mass_F"], 8),
                frac_to_dec_str(r["chi_F"], 8),
                frac_to_dec_str(r["m_0_F"], 4),
                frac_to_dec_str(r["GR_F"], 6),
                frac_to_dec_str(r["retained_7G_F"], 6),
                frac_to_dec_str(r["released_G_F"], 6),
                r["stability"], r["radix_cycle"], r["selected_depth"],
            ])

    # Write combined CSV with observed and B_u
    matches = 0
    discrepancies = []  # engine N doesn't match any observed N at that Z
    with COMBINED_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "Z", "Symbol", "engine_N", "engine_A", "engine_anchor",
            "G_sub", "Q_sub", "Q_mass", "chi", "m_0_baseline_u",
            "obs_isotope", "obs_m_u", "obs_B_u", "obs_B_MeV",
            "engine_matches_obs", "stability",
        ])
        for r in rows:
            key = (r["Z"], r["N"])
            obs = observed.get(key)
            obs_match = obs is not None
            # If exact (Z,N) not in observed, see if ANY (Z,*) is observed
            alt_obs = None
            if not obs_match:
                for (zk, nk), v in observed.items():
                    if zk == r["Z"]:
                        alt_obs = v
                        break
            row_obs = obs if obs else alt_obs
            if obs_match:
                matches += 1
            elif alt_obs is not None:
                discrepancies.append((r["Z"], r["Symbol"], r["anchor"], alt_obs["isotope"]))

            w.writerow([
                r["Z"], r["Symbol"], r["N"], r["A"], r["anchor"],
                frac_to_dec_str(r["G_sub_F"], 8),
                frac_to_dec_str(r["Q_sub_F"], 8),
                frac_to_dec_str(r["Q_mass_F"], 8),
                frac_to_dec_str(r["chi_F"], 8),
                frac_to_dec_str(r["m_0_F"], 4),
                row_obs["isotope"] if row_obs else "",
                f"{row_obs['m_obs_u']:.9f}" if row_obs else "",
                f"{row_obs['B_obs_u']:.9f}" if row_obs else "",
                f"{(row_obs['B_obs_u'] * U_TO_MEV):.4f}" if row_obs else "",
                "EXACT" if obs_match else ("ALT_Z" if alt_obs else ""),
                r["stability"],
            ])

    # Console summary
    print(f"SOB engine output: {len(rows)} elements Z=1..126")
    print(f"Engine output CSV: {ENGINE_CSV.name}")
    print(f"Combined CSV:      {COMBINED_CSV.name}")
    print(f"")
    print(f"Exact engine-(Z,N) matches in CR242 dataset: {matches}")
    print(f"Engine N differs from observed anchor for {len(discrepancies)} elements where CR242 has alt-Z data:")
    print()
    if discrepancies:
        print(f"  {'Z':>3} {'Sym':>4} {'engine':>10} {'CR242_obs':>10}")
        for Z, sym, engine, obs in discrepancies:
            print(f"  {Z:3d} {sym:>4} {engine:>10} {obs:>10}")
    print()

    print("=" * 100)
    print("SOB BLOCK SAMPLE — every 6th element + key anchors")
    print("=" * 100)
    sample_Zs = [1, 2, 6, 8, 12, 18, 20, 26, 28, 36, 40, 50, 56, 60, 79, 82, 92, 100, 118, 126]
    print(f"  {'Z':>3} {'Sym':>4} {'N':>4} {'A':>4} {'G_sub':>12} {'Q_sub':>12} {'Q_mass':>12} {'chi':>10} {'cyc':>3} {'stab':>9}")
    for Z in sample_Zs:
        r = next(x for x in rows if x["Z"] == Z)
        print(f"  {r['Z']:3d} {r['Symbol']:>4} {r['N']:4d} {r['A']:4d} "
              f"{frac_to_dec_str(r['G_sub_F'], 4):>12} "
              f"{frac_to_dec_str(r['Q_sub_F'], 4):>12} "
              f"{frac_to_dec_str(r['Q_mass_F'], 4):>12} "
              f"{frac_to_dec_str(r['chi_F'], 6):>10} "
              f"{r['radix_cycle']:3d} {r['stability']:>9}")

    # Per-element particle source addresses (sample)
    print()
    print("=" * 100)
    print("PARTICLE SOURCE ADDRESS sample")
    print("=" * 100)
    for Z in sample_Zs:
        r = next(x for x in rows if x["Z"] == Z)
        print(f"  {r['Symbol']}-{r['A']} (Z={r['Z']}, N={r['N']}): "
              f"P = {r['p_count']}p + {r['n_count']}n + {r['e_count']}e  =  "
              f"{r['u_count']}u + {r['d_count']}d + {r['e_count']}e")

    # 8 = 7+1 split sample (gravitational coupling)
    print()
    print("=" * 100)
    print("8·G(P) = 7·G(P) + 1·G(P) split — retained mass + released carrier")
    print("=" * 100)
    print(f"  {'Z':>3} {'Sym':>4} {'A':>4} {'G_sub':>12} {'8·G (Q_sub)':>14} {'7·G retained':>14} {'1·G released':>14}")
    for Z in sample_Zs:
        r = next(x for x in rows if x["Z"] == Z)
        print(f"  {r['Z']:3d} {r['Symbol']:>4} {r['A']:4d} "
              f"{frac_to_dec_str(r['G_sub_F'], 4):>12} "
              f"{frac_to_dec_str(r['GR_F'], 4):>14} "
              f"{frac_to_dec_str(r['retained_7G_F'], 4):>14} "
              f"{frac_to_dec_str(r['released_G_F'], 4):>14}")


if __name__ == "__main__":
    main()
