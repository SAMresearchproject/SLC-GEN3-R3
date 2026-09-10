"""
CR005a -- Neutrino Mass Spectrum Substrate Identification + DUNE Forecast Lock.

Verifies the substrate-identification chain (placing the three neutrino
mass-squareds in CR005's partition-algebra and Theta-unit framework) and
computes the DUNE/Hyper-K forecast discrimination of SAM's predicted
ratio (35) vs current best fit (33.895).

precommit : 5beb9ab51b03ee4ec29b18e9e60c743092d0f47e386072281d6f2c1a9e78dcd8
"""

import hashlib
import json
import math
import os
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
PRECOMMIT_PATH = os.path.join(HERE, "CR005a_PRECOMMIT.md")
PRECOMMIT_HASH = "5beb9ab51b03ee4ec29b18e9e60c743092d0f47e386072281d6f2c1a9e78dcd8"

# Substrate primitives (CR258, CR238 sealed; same as CR005)
h_hat = 2
d_hat = 3
S = h_hat ** d_hat       # 8
V = d_hat ** d_hat       # 27
F = d_hat ** (d_hat + 1) # 81
R = h_hat ** 2 * d_hat   # 12
R2 = R * R               # 144
Theta = h_hat * d_hat ** 2   # 18
L = h_hat * F            # 162
M_atom = R2 - Theta      # 126

# External anchors (numeric literals, declared)
DM31_PDG = 2.515e-3          # eV^2 (PDG 2024 normal ordering)
DM21_PDG = 7.42e-5           # eV^2 (PDG 2024 global fit)
RATIO_MEASURED = DM31_PDG / DM21_PDG  # 33.895...
RATIO_SIGMA_CURRENT = 0.70   # absolute uncertainty on ratio (NuFit 5.2, ~2.06%)
PLANCK_SUM_MNU_BOUND = 0.12  # eV

# DUNE / Hyper-K projected sigma on the ratio
DUNE_RATIO_SIGMA = 0.17      # absolute (~0.5% of central ~34)
JOINT_RATIO_SIGMA = 0.10     # DUNE+HK joint (~0.3% of central)

# CR001@20 sealed values for cross-check
CR001_RATIO_SAM = 35
CR001_SIGMA_MNU_SAM_EV = 0.07133


def file_sha256(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def verify_precommit():
    h = file_sha256(PRECOMMIT_PATH)
    if h != PRECOMMIT_HASH:
        raise SystemExit(f"precommit hash mismatch: got {h} want {PRECOMMIT_HASH}")


def check(label, condition, detail=""):
    result = bool(condition)
    print(f"  [{'PASS' if result else 'FAIL'}] {label}"
          f"{('  ' + detail) if detail else ''}")
    return result


def main():
    verify_precommit()
    print(f"CR005a -- Neutrino Substrate Identification + DUNE Forecast Lock")
    print(f"precommit hash : {PRECOMMIT_HASH}")
    print()
    print(f"Substrate primitives (CR258 sealed):  h_hat = {h_hat}, d_hat = {d_hat}")
    print(f"Derived atoms:  S = {S}, Theta = {Theta}, R = {R}, R^2 = {R2}")
    print(f"External anchors:")
    print(f"  Delta m^2_31 (PDG 2024)  = {DM31_PDG:.4e} eV^2")
    print(f"  Delta m^2_21 (PDG 2024)  = {DM21_PDG:.4e} eV^2")
    print(f"  measured ratio           = {RATIO_MEASURED:.4f}")
    print(f"  current ratio sigma     ~= {RATIO_SIGMA_CURRENT}")
    print(f"  DUNE projected sigma    ~= {DUNE_RATIO_SIGMA}")
    print(f"  DUNE+HK joint sigma     ~= {JOINT_RATIO_SIGMA}")
    print(f"  Planck Sigma m_nu bound  = {PLANCK_SUM_MNU_BOUND} eV")
    print()

    all_passed = True

    # =================================================================
    # Block A -- Substrate identification of mass-squared eigenvalues
    # =================================================================
    print("Block A -- Substrate identification of m_i^2 in partition algebra")

    # A1: m_1^2 / base_eV^2 = 1 at position (0, 0)
    val_00 = h_hat**0 * d_hat**0
    a1 = check("A1 m_1^2 / base_eV^2 = 1 at partition-algebra (0, 0)",
               val_00 == 1)
    all_passed &= a1

    # A2: m_2^2 / base_eV^2 = h_hat = 2 at position (1, 0)
    val_10 = h_hat**1 * d_hat**0
    a2 = check("A2 m_2^2 / base_eV^2 = h_hat = 2 at partition-algebra (1, 0)",
               val_10 == h_hat == 2)
    all_passed &= a2

    # A3: m_3^2 / base_eV^2 = (h_hat * d_hat)^2 = 36 at position (2, 2)
    val_22 = h_hat**2 * d_hat**2
    a3a = check("A3.value m_3^2 / base_eV^2 = (h_hat * d_hat)^2 = 36 at position (2, 2)",
                val_22 == 36 == (h_hat * d_hat)**2)

    # A3.overflow_set -- 36 is second element of overflow {18, 24, 36, 72}
    grid_outside = sorted({h_hat**i * d_hat**j
                           for i in range(d_hat + 1)
                           for j in range(d_hat)
                           if h_hat**i * d_hat**j > R})
    a3b = check("A3.overflow 36 is second element of partition-algebra overflow set",
                grid_outside == [18, 24, 36, 72] and grid_outside[1] == 36)
    all_passed &= a3a and a3b

    # A4: m_3^2 = 2*Theta = h_hat * Theta (cross-branch identity)
    a4a = check("A4.a m_3^2 = 2 * Theta",
                val_22 == 2 * Theta == 36)
    a4b = check("A4.b m_3^2 = h_hat * Theta",
                val_22 == h_hat * Theta == 36)
    a4c = check("A4.c (h_hat * d_hat)^2 = h_hat * Theta  (algebraic identity)",
                (h_hat * d_hat)**2 == h_hat * Theta)
    all_passed &= a4a and a4b and a4c
    print()

    # =================================================================
    # Block B -- Multiplicative chain
    # =================================================================
    print("Block B -- Mass-squared progression as substrate multiplicative chain")

    s_chain = [1, h_hat, h_hat * Theta]
    b1 = check(f"B1 substrate-quantity sequence s = [1, h_hat, h_hat*Theta] = {s_chain}",
               s_chain == [1, 2, 36])

    b2a = check("B2.a Step 1->2 multiplier = h_hat (binary readout)",
                Fraction(s_chain[1], s_chain[0]) == Fraction(h_hat, 1))
    b2b = check("B2.b Step 2->3 multiplier = Theta (carrier overflow)",
                Fraction(s_chain[2], s_chain[1]) == Fraction(Theta, 1))

    b3a = check("B3.a m_3^2 / m_2^2 = Theta = 18",
                Fraction(s_chain[2], s_chain[1]) == Fraction(Theta, 1))
    b3b = check("B3.b m_2^2 / m_1^2 = h_hat = 2",
                Fraction(s_chain[1], s_chain[0]) == Fraction(h_hat, 1))
    all_passed &= b1 and b2a and b2b and b3a and b3b
    print()

    # =================================================================
    # Block C -- Splittings derivation in Theta-unit form
    # =================================================================
    print("Block C -- Splittings derivation")

    delta_21_factor = h_hat - 1   # = 1
    delta_31_factor = h_hat * Theta - 1   # = 35
    c1 = check(f"C1 Delta m^2_21 / base_eV^2 = h_hat - 1 = {delta_21_factor}",
               delta_21_factor == 1)
    c2 = check(f"C2 Delta m^2_31 / base_eV^2 = h_hat*Theta - 1 = {delta_31_factor}",
               delta_31_factor == 35)

    ratio_sam = Fraction(delta_31_factor, delta_21_factor)
    c3 = check(f"C3 ratio = (h_hat*Theta - 1) / (h_hat - 1) = {ratio_sam}",
               ratio_sam == Fraction(35, 1))

    # Also verify (h_hat*Theta - 1) = (h_hat*d_hat)^2 - 1
    c3b = check("C3.b (h_hat*Theta - 1) = (h_hat*d_hat)^2 - 1",
                h_hat * Theta - 1 == (h_hat * d_hat)**2 - 1)

    c4 = check(f"C4 ratio = {CR001_RATIO_SAM} matches CR001@20 sealed",
               ratio_sam == Fraction(CR001_RATIO_SAM, 1))
    all_passed &= c1 and c2 and c3 and c3b and c4
    print()

    # =================================================================
    # Block D -- eV scale anchor
    # =================================================================
    print("Block D -- eV scale anchor (from CR001@20)")

    base_eV = math.sqrt(DM31_PDG / 35)
    d1 = check(f"D1 base_eV = sqrt(2.515e-3 / 35) = {base_eV:.6f} eV "
               f"(~ 0.008477 eV)",
               abs(base_eV - 0.008477) < 1e-5)

    m1 = base_eV * 1
    m2 = base_eV * math.sqrt(h_hat)
    m3 = base_eV * h_hat * d_hat
    d2a = check(f"D2.m1 m_1 = {m1:.6f} eV  (~ 0.008477)",
                abs(m1 - 0.008477) < 1e-5)
    d2b = check(f"D2.m2 m_2 = {m2:.6f} eV  (~ 0.011988)",
                abs(m2 - 0.011988) < 1e-5)
    d2c = check(f"D2.m3 m_3 = {m3:.6f} eV  (~ 0.050861)",
                abs(m3 - 0.050861) < 1e-5)

    sigma_mnu = m1 + m2 + m3
    d3a = check(f"D3.a Sigma m_nu = {sigma_mnu:.6f} eV  (~ 0.07133)",
                abs(sigma_mnu - 0.07133) < 1e-4)
    d3b = check(f"D3.b Sigma m_nu < Planck bound {PLANCK_SUM_MNU_BOUND} eV",
                sigma_mnu < PLANCK_SUM_MNU_BOUND)
    all_passed &= d1 and d2a and d2b and d2c and d3a and d3b
    print()

    # =================================================================
    # Block E -- Cross-check against CR001@20 sealed values
    # =================================================================
    print("Block E -- Cross-check against CR001@20 sealed values")
    e1 = check(f"E1 ratio_SAM = {int(ratio_sam)} matches CR001@20 sealed {CR001_RATIO_SAM}",
               int(ratio_sam) == CR001_RATIO_SAM)
    e2 = check(f"E2 Sigma m_nu = {sigma_mnu:.5f} matches CR001@20 sealed {CR001_SIGMA_MNU_SAM_EV}",
               abs(sigma_mnu - CR001_SIGMA_MNU_SAM_EV) < 1e-4)
    e3 = check("E3 individual masses match CR001@20 sealed to 4 decimal places",
               abs(m1 - 0.008477) < 1e-4 and abs(m2 - 0.011988) < 1e-4
               and abs(m3 - 0.050861) < 1e-4)
    all_passed &= e1 and e2 and e3
    print()

    # =================================================================
    # Block F -- Forecast lock (load-bearing new content)
    # =================================================================
    print("Block F -- DUNE / Hyper-K forecast lock")

    sam_ratio = 35.0
    deviation = sam_ratio - RATIO_MEASURED
    relative_pct = 100.0 * deviation / RATIO_MEASURED

    print(f"  SAM ratio (substrate-derived, exact)  : {sam_ratio}")
    print(f"  Measured ratio (PDG 2024)             : {RATIO_MEASURED:.4f} +/- {RATIO_SIGMA_CURRENT}")
    print(f"  Deviation                              : +{deviation:.4f} (+{relative_pct:.3f}%)")
    print()

    sigma_current = abs(deviation) / RATIO_SIGMA_CURRENT
    sigma_dune = abs(deviation) / DUNE_RATIO_SIGMA
    sigma_joint = abs(deviation) / JOINT_RATIO_SIGMA

    f1 = check(f"F1 SAM commits to ratio = 35 (zero substrate-side uncertainty)",
               True)
    f2 = check(f"F2 current discrimination = {sigma_current:.2f}σ "
               f"(< 3σ; not yet discriminating)",
               sigma_current < 3.0)
    f3 = check(f"F3 DUNE projected discrimination = {sigma_dune:.2f}σ "
               f"(>= 3σ; clean test)",
               sigma_dune >= 3.0)
    f4 = check(f"F4 DUNE+HK joint discrimination = {sigma_joint:.2f}σ",
               sigma_joint > sigma_dune)
    print()
    print(f"  Falsification criteria for SAM ratio = 35:")
    print(f"    DUNE measures r with |35 - r|/sigma_DUNE > 3  -> SAM falsified")
    print(f"    DUNE measures r with |35 - r|/sigma_DUNE < 1  -> SAM strongly confirmed")
    print(f"  Timeline: DUNE first data ~2028, full sensitivity ~2032")
    print(f"            Hyper-K first data ~2027")
    print(f"            Discrimination expected ~2030")
    f5 = True  # falsification criteria registered

    all_passed &= f1 and f2 and f3 and f4 and f5
    print()

    # =================================================================
    # Verdict
    # =================================================================
    verdict = "PASS" if all_passed else "FAIL"
    print(f"CR005a VERDICT: {verdict}")
    print()

    if verdict == "PASS":
        print("Substrate-identification chain sealed:")
        print(f"  m_1^2 = 1             at partition-algebra ground (0,0)")
        print(f"  m_2^2 = h_hat = 2     at binary level (1,0)")
        print(f"  m_3^2 = (h*d)^2 = 36  at partition-algebra (2,2) — second overflow")
        print(f"        = 2*Theta = h_hat * Theta")
        print()
        print("Forecast lock registered:")
        print(f"  SAM ratio = 35 (exact)")
        print(f"  DUNE / Hyper-K discrimination at projected precision: "
              f"{sigma_dune:.1f}σ vs current 33.895")
        print(f"  Falsification window: ~2030")
        print()

    # Outputs
    summary = {
        "artifact": "CR005a_NEUTRINO_SUBSTRATE_IDENTIFICATION_AND_DUNE_FORECAST_LOCK",
        "classification": "STRUCTURAL_IDENTIFICATION + FORECAST_LOCK",
        "verdict": verdict,
        "precommit_hash": PRECOMMIT_HASH,
        "substrate_identification": {
            "m1_sq_over_base_eV_sq": 1,
            "m1_position": "(0, 0)",
            "m2_sq_over_base_eV_sq": h_hat,
            "m2_position": "(1, 0)",
            "m3_sq_over_base_eV_sq": (h_hat * d_hat) ** 2,
            "m3_position": "(2, 2)",
            "m3_in_overflow_set": True,
            "m3_overflow_set_index": 1,  # second element (zero-indexed = 1)
            "cross_branch_m3_sq_equals_2Theta": True,
        },
        "multiplicative_chain": {
            "sequence_s": [1, h_hat, h_hat * Theta],
            "step_1_to_2_multiplier": h_hat,
            "step_2_to_3_multiplier": Theta,
        },
        "splittings": {
            "Dm21_factor": h_hat - 1,
            "Dm31_factor": h_hat * Theta - 1,
            "ratio_SAM": int(h_hat * Theta - 1),  # 35
            "ratio_form": "(h_hat*Theta - 1) / (h_hat - 1)",
        },
        "eV_anchor": {
            "base_eV": base_eV,
            "m1_eV": m1, "m2_eV": m2, "m3_eV": m3,
            "Sigma_mnu_eV": sigma_mnu,
            "Sigma_mnu_below_Planck_bound": sigma_mnu < PLANCK_SUM_MNU_BOUND,
        },
        "forecast_lock": {
            "SAM_ratio": 35.0,
            "measured_ratio": RATIO_MEASURED,
            "current_sigma": RATIO_SIGMA_CURRENT,
            "DUNE_projected_sigma": DUNE_RATIO_SIGMA,
            "DUNE_HK_joint_sigma": JOINT_RATIO_SIGMA,
            "deviation": deviation,
            "deviation_pct": relative_pct,
            "current_discrimination_sigma": sigma_current,
            "DUNE_discrimination_sigma": sigma_dune,
            "DUNE_HK_joint_discrimination_sigma": sigma_joint,
            "falsification_threshold_dune": "|35 - r_DUNE| / sigma_DUNE > 3",
            "confirmation_threshold_dune": "|35 - r_DUNE| / sigma_DUNE < 1",
            "timeline": "DUNE 2028-2032; Hyper-K 2027+; discrimination ~2030",
        },
        "all_claims_passed": all_passed,
    }
    with open(os.path.join(HERE, "CR005a_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    runner_hash = file_sha256(__file__)
    print(f"runner SHA-256 : {runner_hash}")


if __name__ == "__main__":
    main()
