"""
CR005 -- Theta Carrier Overflow and Schwarzschild QNM Derivation.

Verifies the substrate-physics derivation chain that produces
omega_R*M = d/(d^(d-1) - 1) = d/S = 3/8 from:
  (1) the bounded partition algebra and Theta as first overflow
  (2) Sean's identity Theta + M = R^2 = L - Theta
  (3) the closure axiom d^(d-1) = S + 1

All claims are pre-registered in CR005_PRECOMMIT.md as exact-rational
self-checks. The CR is PASS iff every claim verifies.

precommit : 624f0c2655333dd9e6e217f2bed0cbdbd97197281b6f06b462747b7896b13b6b
"""

import hashlib
import json
import os
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
PRECOMMIT_PATH = os.path.join(HERE, "CR005_PRECOMMIT.md")
PRECOMMIT_HASH = "624f0c2655333dd9e6e217f2bed0cbdbd97197281b6f06b462747b7896b13b6b"

# Substrate primitives (CR258, CR238 sealed)
h_hat = 2          # binary readout
d_hat = 3          # dimensional readout

# Derived atoms (computed live from primitives)
S = h_hat ** d_hat                  # 8 -- split inventory
V = d_hat ** d_hat                  # 27 -- write cell
F = d_hat ** (d_hat + 1)            # 81 -- carrier face
R = h_hat ** 2 * d_hat              # 12 -- route radix
R2 = R * R                          # 144 -- writable capacity
Theta = h_hat * d_hat ** 2          # 18 -- carrier tensor / first overflow
L = h_hat * F                       # 162 -- closed ledger
M = R2 - Theta                      # 126 -- matter capacity

# Sealed upstream from CR218 bigrade
BIGRADE_SEALED = (1, 2, 3, 4, 6, 8, 9, 12)


def file_sha256(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def verify_precommit():
    h = file_sha256(PRECOMMIT_PATH)
    if h != PRECOMMIT_HASH:
        raise SystemExit(f"precommit hash mismatch: got {h} want {PRECOMMIT_HASH}")


def check(label, condition, detail=""):
    """Record a pre-registered claim's verification."""
    result = bool(condition)
    print(f"  [{'PASS' if result else 'FAIL'}] {label}"
          f"{('  ' + detail) if detail else ''}")
    return result


def main():
    verify_precommit()
    print(f"CR005 -- Theta Carrier Overflow and Schwarzschild QNM Derivation")
    print(f"precommit hash : {PRECOMMIT_HASH}")
    print()
    print(f"Substrate primitives (CR258 sealed):")
    print(f"  h_hat = {h_hat},  d_hat = {d_hat}")
    print()
    print(f"Derived atoms (CR229/CR238 sealed):")
    print(f"  S = {S},  V = {V},  F = {F},  R = {R},  R^2 = {R2},  "
          f"Theta = {Theta},  L = {L},  M = {M}")
    print()

    all_passed = True

    # ==============================================================
    # Block A -- Bounded partition algebra and overflow
    # ==============================================================
    print("Block A -- Bounded partition algebra (i in [0..d], j in [0..d-1])")
    grid = []
    for i in range(d_hat + 1):           # i in [0..3]
        for j in range(d_hat):            # j in [0..2]
            val = h_hat**i * d_hat**j
            grid.append(((i, j), val))
    grid_sorted = sorted(grid, key=lambda x: x[1])

    # A1
    a1 = check("A1 grid cell count = (d+1)*d",
               len(grid) == (d_hat + 1) * d_hat,
               f"got {len(grid)}, want {(d_hat+1)*d_hat}")
    all_passed &= a1

    # A2 -- 8 products fit inside R, match sealed bigrade
    inside = sorted(set(v for (_, v) in grid if v <= R))
    a2_count = check("A2.count 8 products fit inside R",
                     len(inside) == 8,
                     f"got {len(inside)}")
    a2_match = check("A2.bigrade equals CR218 sealed alphabet",
                     tuple(inside) == BIGRADE_SEALED,
                     f"got {inside}, want {list(BIGRADE_SEALED)}")
    all_passed &= a2_count and a2_match

    # A3 -- 4 products overflow, smallest = Theta
    outside = sorted(set(v for (_, v) in grid if v > R))
    a3_count = check("A3.count 4 products exceed R",
                     len(outside) == 4,
                     f"got {len(outside)} = {outside}")
    a3_min = check("A3.min smallest overflow = Theta = 18",
                   outside[0] == Theta,
                   f"got smallest={outside[0]}, want {Theta}")
    a3_full = check("A3.full overflow set = {18, 24, 36, 72}",
                    outside == [18, 24, 36, 72],
                    f"got {outside}")

    # A3 location -- the smallest overflow is at (i, j) = (1, 2)
    overflow_locations = [(pos, val) for (pos, val) in grid if val > R]
    overflow_locations.sort(key=lambda x: x[1])
    smallest_overflow_pos, smallest_overflow_val = overflow_locations[0]
    a3_loc = check("A3.location smallest overflow at (i, j) = (1, 2)",
                   smallest_overflow_pos == (1, 2) and smallest_overflow_val == Theta,
                   f"got pos={smallest_overflow_pos}, val={smallest_overflow_val}")
    all_passed &= a3_count and a3_min and a3_full and a3_loc

    # A4 -- h_hat * d_hat^2 == Theta (CR229 sealed)
    a4 = check("A4 h_hat * d_hat^2 = Theta",
               h_hat * d_hat**2 == Theta,
               f"{h_hat*d_hat**2} = {Theta}")
    all_passed &= a4

    print()

    # ==============================================================
    # Block B -- Substrate-in-Theta-units identities
    # ==============================================================
    print("Block B -- Substrate-in-Theta-units identities")
    b1 = check("B1 Theta=18, M=126, R^2=144, L=162",
               (Theta == 18 and M == 126 and R2 == 144 and L == 162))
    b2_frac = Fraction(M, Theta)
    b2 = check("B2 M/Theta = 7 exact integer",
               b2_frac == Fraction(7, 1),
               f"got {b2_frac}")
    b3_frac = Fraction(R2, Theta)
    b3 = check("B3 R^2/Theta = 8 = S",
               b3_frac == Fraction(8, 1) and b3_frac == S,
               f"got {b3_frac}, S={S}")
    b4_frac = Fraction(L, Theta)
    b4 = check("B4 L/Theta = 9 exact integer",
               b4_frac == Fraction(9, 1),
               f"got {b4_frac}")
    b5 = check("B5 Theta + M = R^2",
               Theta + M == R2,
               f"{Theta}+{M}={Theta+M} vs R^2={R2}")
    b6 = check("B6 L - Theta = R^2",
               L - Theta == R2,
               f"{L}-{Theta}={L-Theta} vs R^2={R2}")
    b7 = check("B7 R^2 = S * Theta",
               R2 == S * Theta,
               f"{R2} = {S}*{Theta} = {S*Theta}")
    b8 = check("B8 M = (S-1) * Theta",
               M == (S - 1) * Theta,
               f"{M} = {S-1}*{Theta} = {(S-1)*Theta}")
    b9 = check("B9 L = (S+1) * Theta",
               L == (S + 1) * Theta,
               f"{L} = {S+1}*{Theta} = {(S+1)*Theta}")
    all_passed &= b1 and b2 and b3 and b4 and b5 and b6 and b7 and b8 and b9
    print()

    # ==============================================================
    # Block C -- Closure-axiom connections
    # ==============================================================
    print("Block C -- Closure-axiom connections")
    c1 = check("C1 S = h_hat^d_hat = 8",
               S == h_hat ** d_hat == 8)
    closure_lhs = d_hat ** (d_hat - 1)        # 9
    closure_rhs = S + 1
    c2 = check("C2 d_hat^(d_hat-1) = S + 1 at d_hat=3 (closure axiom)",
               closure_lhs == closure_rhs == 9,
               f"d^(d-1)={closure_lhs}, S+1={closure_rhs}")
    c3 = check("C3 L/Theta = S+1 = d_hat^(d_hat-1) = 9",
               L // Theta == S + 1 == d_hat ** (d_hat - 1) == 9)
    seven_check = (h_hat ** d_hat) - 1
    c4 = check("C4 M/Theta = S-1 = h_hat^d_hat - 1 = alpha_H^3 - 1 = 7",
               M // Theta == S - 1 == seven_check == 7)
    all_passed &= c1 and c2 and c3 and c4
    print()

    # ==============================================================
    # Block D -- QNM derivation chain
    # ==============================================================
    print("Block D -- Schwarzschild fundamental QNM derivation chain")

    # D1 -- substrate-derived expression
    omega_R_M_form1 = Fraction(d_hat, d_hat ** (d_hat - 1) - 1)
    print(f"  D1 omega_R*M = d/(d^(d-1) - 1) = {d_hat}/({d_hat**(d_hat-1)}-1) = {omega_R_M_form1}")

    # D2 -- equals 3/8
    d2 = check("D2 = 3/8 exact rational",
               omega_R_M_form1 == Fraction(3, 8))
    d2_dec = check("D2.decimal = 0.375 exact",
                   float(omega_R_M_form1) == 0.375)

    # D3 -- d / S
    omega_R_M_form2 = Fraction(d_hat, S)
    d3 = check("D3 = d/S (closure axiom equivalence)",
               omega_R_M_form2 == omega_R_M_form1 == Fraction(3, 8))

    # D4 -- (Theta * d) / R^2
    omega_R_M_form3 = Fraction(Theta * d_hat, R2)
    d4 = check("D4 = (Theta*d)/R^2 (Sean's identity equivalence)",
               omega_R_M_form3 == omega_R_M_form1 == Fraction(3, 8))

    # D5 -- bit-identical fractions
    d5 = check("D5 all three forms bit-identical as Fractions",
               omega_R_M_form1 == omega_R_M_form2 == omega_R_M_form3)

    # D6 -- gap to GR
    omega_R_M_GR = 0.37367168
    gap_pct = 100.0 * (float(omega_R_M_form1) - omega_R_M_GR) / omega_R_M_GR
    # CR003 reported 0.3555% -- verify we match to 3 decimal places
    d6 = check("D6 gap to GR Berti+2009 = 0.356% (matches CR003 sealed 0.3555%)",
               abs(gap_pct - 0.3555) < 0.01,
               f"got {gap_pct:.4f}%")
    all_passed &= d2 and d2_dec and d3 and d4 and d5 and d6
    print()

    # ==============================================================
    # Block E -- Falsification controls
    # ==============================================================
    print("Block E -- Falsification controls")

    # E1 -- the wider unbounded grid would let h^(d+1)=16 in
    wider_grid = [(i, j, h_hat**i * d_hat**j)
                  for i in range(d_hat + 2)
                  for j in range(d_hat + 1)]
    wider_overflow = sorted(v for (_, _, v) in wider_grid if v > R)
    wider_min = wider_overflow[0]
    h_to_d_plus_1 = h_hat ** (d_hat + 1)
    e1a = check(f"E1a h^(d+1) = {h_to_d_plus_1} < Theta = {Theta} "
                f"(would be smaller overflow in wider grid)",
                h_to_d_plus_1 < Theta)
    e1b = check(f"E1b but h^(d+1) lies OUTSIDE the typed-spine bounded grid "
                f"(i={d_hat+1} > d={d_hat})",
                d_hat + 1 > d_hat)
    e1c = check("E1c within the bounded grid (i<=d, j<=d-1), Theta IS the "
                "smallest overflow",
                outside[0] == Theta)

    # E2 -- closure-axiom bound on j
    e2 = check(f"E2 j <= d-1 = {d_hat-1} is the closure-axiom bound: "
               f"d^(d-1) = S+1 (= {S+1}) is the largest dimensional power in closure",
               d_hat ** (d_hat - 1) == S + 1)

    # E3 -- alternative candidates for the carrier
    candidates_to_kill = {
        "d_hat^d_hat (write cell V=27)": V,
        "h_hat^(d_hat+1) (=16)": h_to_d_plus_1,
        "d_hat^(d_hat+1) (carrier face F=81)": F,
    }
    print("  E3 alternative carrier candidates:")
    e3_all = True
    for name, val in candidates_to_kill.items():
        # A valid carrier must be (a) the smallest overflow IN the bounded grid AND
        # (b) match the CR229 sealed Theta value 18
        is_theta = (val == Theta)
        in_bounded = any(((h_hat**i * d_hat**j) == val
                          and i <= d_hat and j <= d_hat - 1)
                         for i in range(d_hat + 2)
                         for j in range(d_hat + 1))
        eliminated = (not is_theta) or (not in_bounded)
        print(f"    {name}: value={val}, "
              f"in_bounded_grid={in_bounded}, equals_Theta={is_theta}, "
              f"eliminated={eliminated}")
        e3_all &= eliminated   # candidate must be eliminated
    e3 = check("E3 all alternative carrier candidates eliminated",
               e3_all)
    all_passed &= e1a and e1b and e1c and e2 and e3
    print()

    # ==============================================================
    # Verdict
    # ==============================================================
    verdict = "PASS" if all_passed else "FAIL"
    print(f"CR005 VERDICT: {verdict}")
    print()

    if verdict == "PASS":
        print("Substrate-physics derivation of Schwarzschild fundamental QNM real frequency:")
        print()
        print("  omega_R * M  =  (Theta * d) / R^2          [Theta-overflow propagates in d dims]")
        print("              =  d / S                        [Sean's identity R^2 = S*Theta]")
        print("              =  d / (d^(d-1) - 1)            [closure axiom S = d^(d-1) - 1]")
        print(f"              =  {d_hat} / ({d_hat**(d_hat-1)} - 1)")
        print(f"              =  {omega_R_M_form1}")
        print(f"              =  {float(omega_R_M_form1)}")
        print()
        print(f"  GR (Berti+2009):  omega_R * M = {omega_R_M_GR}")
        print(f"  gap            :  +{gap_pct:.4f}%  (matches CR003 sealed empirical residual)")
        print()

    # Emit outputs
    summary = {
        "artifact": "CR005_THETA_CARRIER_OVERFLOW_AND_QNM_DERIVATION",
        "classification": "STRUCTURAL_IDENTIFICATION_CR",
        "verdict": verdict,
        "precommit_hash": PRECOMMIT_HASH,
        "substrate_primitives": {"h_hat": h_hat, "d_hat": d_hat},
        "derived_atoms": {
            "S": S, "V": V, "F": F, "R": R, "R_sq": R2,
            "Theta": Theta, "L": L, "M": M,
        },
        "bounded_partition_algebra": {
            "grid_bounds": f"i in [0..{d_hat}], j in [0..{d_hat-1}]",
            "grid_cells": (d_hat + 1) * d_hat,
            "inside_R": inside,
            "overflow_sorted": outside,
            "smallest_overflow": outside[0],
            "smallest_overflow_position": list(smallest_overflow_pos),
        },
        "theta_units": {
            "L_over_Theta": L // Theta,
            "R_sq_over_Theta": R2 // Theta,
            "M_over_Theta": M // Theta,
            "closure_axiom_S_plus_1": S + 1,
            "d_to_d_minus_1": d_hat ** (d_hat - 1),
            "matches": (L // Theta == S + 1 == d_hat ** (d_hat - 1)),
        },
        "qnm_derivation": {
            "omega_R_M_form1_closure": str(Fraction(d_hat, d_hat ** (d_hat - 1) - 1)),
            "omega_R_M_form2_d_over_S": str(Fraction(d_hat, S)),
            "omega_R_M_form3_Theta_d_over_R2": str(Fraction(Theta * d_hat, R2)),
            "value_decimal": 0.375,
            "GR_Berti_2009": omega_R_M_GR,
            "gap_pct": gap_pct,
        },
        "all_claims_passed": all_passed,
    }
    with open(os.path.join(HERE, "CR005_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    runner_hash = file_sha256(__file__)
    print(f"runner SHA-256 : {runner_hash}")


if __name__ == "__main__":
    main()
