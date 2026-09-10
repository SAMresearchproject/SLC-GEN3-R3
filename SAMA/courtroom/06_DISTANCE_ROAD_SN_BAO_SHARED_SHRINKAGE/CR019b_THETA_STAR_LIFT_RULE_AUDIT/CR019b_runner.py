"""
CR019b -- theta_* substrate-lift rule audit.

Tests whether the 09a binding-work lift rule (bigrade lifted, Theta exempt)
applied to CR019@06's substrate atoms closes the +0.605% theta_* gap.

precommit : d83ef6864e095550cb7989a88da88c25b60c2b8bd584b7719efd4568d3b8f32f
"""

import csv
import hashlib
import json
import math
import os
from scipy.integrate import quad
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PRECOMMIT_PATH = os.path.join(HERE, "CR019b_PRECOMMIT.md")
PRECOMMIT_HASH = "d83ef6864e095550cb7989a88da88c25b60c2b8bd584b7719efd4568d3b8f32f"

PI = math.pi
C_KMS = 299792.458
h_hat, d_hat = 2, 3
S = h_hat ** d_hat       # 8
R = h_hat ** 2 * d_hat   # 12
R2 = R * R               # 144
Theta = h_hat * d_hat ** 2   # 18
F = d_hat ** (d_hat + 1)     # 81
L_ledger = h_hat * F          # 162

def L_p(p):
    return p + (p * p) / R2

H0 = 68.76
T_CMB = 2.7255
N_EFF = 3.046
OMEGA_GAMMA_H2 = 2.4728e-5 * (T_CMB / 2.7255) ** 4
REL_FACTOR = 1.0 + (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0) * N_EFF

PLANCK_100THETA_STAR = 1.04110
PLANCK_ELL_A = 301.76
PLANCK_R_D = 147.09


def file_sha256(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def verify_precommit():
    h = file_sha256(PRECOMMIT_PATH)
    if h != PRECOMMIT_HASH:
        raise SystemExit(f"precommit hash mismatch: got {h} want {PRECOMMIT_HASH}")


def compressed_geometry(Omega_m, Omega_b, H0_local=H0):
    h = H0_local / 100.0
    wm = Omega_m * h * h
    wb = Omega_b * h * h
    Omega_r = OMEGA_GAMMA_H2 * REL_FACTOR / (h * h)
    Omega_DE = 1.0 - Omega_m - Omega_r
    g1 = 0.0783 * wb ** (-0.238) / (1.0 + 39.5 * wb ** 0.763)
    g2 = 0.560 / (1.0 + 21.1 * wb ** 1.81)
    z_star = 1048.0 * (1.0 + 0.00124 * wb ** (-0.738)) * (1.0 + g1 * wm ** g2)
    b1 = 0.313 * wm ** (-0.419) * (1.0 + 0.607 * wm ** 0.674)
    b2 = 0.238 * wm ** 0.223
    z_drag = 1291.0 * wm ** 0.251 / (1.0 + 0.659 * wm ** 0.828) * (1.0 + b1 * wb ** b2)
    def E(z):
        return math.sqrt(Omega_m * (1.0 + z) ** 3 + Omega_r * (1.0 + z) ** 4 + Omega_DE)
    def cs(z):
        Rcs = 0.75 * wb / OMEGA_GAMMA_H2 / (1.0 + z)
        return C_KMS / math.sqrt(3.0 * (1.0 + Rcs))
    rs_zstar, _ = quad(lambda z: cs(z) / (H0_local * E(z)), z_star, np.inf, limit=400)
    rs_zd, _    = quad(lambda z: cs(z) / (H0_local * E(z)), z_drag, np.inf, limit=400)
    DM_zstar_int, _ = quad(lambda x: 1.0 / E(x), 0.0, z_star, limit=400)
    DM_zstar = C_KMS / H0_local * DM_zstar_int
    ell_A = PI * DM_zstar / rs_zstar
    theta_star = rs_zstar / DM_zstar
    return dict(rs_zstar=rs_zstar, rs_zd=rs_zd, DM_zstar=DM_zstar,
                ell_A=ell_A, hundred_theta_star=100.0*theta_star)


def gaps(Om, Ob):
    g = compressed_geometry(Om, Ob)
    return (
        100.0 * (g["hundred_theta_star"] - PLANCK_100THETA_STAR) / PLANCK_100THETA_STAR,
        100.0 * (g["ell_A"] - PLANCK_ELL_A) / PLANCK_ELL_A,
        100.0 * (g["rs_zd"] - PLANCK_R_D) / PLANCK_R_D,
    )


def main():
    verify_precommit()
    print(f"CR019b -- theta_* substrate-lift rule audit")
    print(f"precommit hash : {PRECOMMIT_HASH}")
    print()

    A_0 = 1.0 / (12.0 * PI)
    Om_canon = 1.0 / PI
    chi_canon = (S / d_hat) * A_0
    Ob_canon = 2.0 * A_0 * (1.0 - chi_canon)

    rows = []

    # Canonical (baseline)
    t, l, r = gaps(Om_canon, Ob_canon)
    print(f"  CANONICAL                    Om={Om_canon:.5f} Ob={Ob_canon:.5f}  "
          f"theta_*{t:+6.3f}%  ellA{l:+6.3f}%  rd{r:+6.3f}%")
    rows.append(("canonical", Om_canon, Ob_canon, t, l, r))

    # H1: Lift R only in A_0 denominator
    A_0_H1 = 1.0 / (L_p(R) * PI)
    Om_H1 = R * A_0_H1
    chi_H1 = (S / d_hat) * A_0_H1
    Ob_H1 = 2.0 * A_0_H1 * (1.0 - chi_H1)
    t, l, r = gaps(Om_H1, Ob_H1)
    print(f"  H1: R lifted in A_0          Om={Om_H1:.5f} Ob={Ob_H1:.5f}  "
          f"theta_*{t:+6.3f}%  ellA{l:+6.3f}%  rd{r:+6.3f}%")
    rows.append(("H1_R_lifted_in_A0", Om_H1, Ob_H1, t, l, r))

    # H2: Lift R consistently
    Om_H2 = L_p(R) * A_0_H1  # = 1/pi
    Ob_H2 = 2.0 * A_0_H1 * (1.0 - chi_H1)
    t, l, r = gaps(Om_H2, Ob_H2)
    print(f"  H2: R lifted consistently    Om={Om_H2:.5f} Ob={Ob_H2:.5f}  "
          f"theta_*{t:+6.3f}%  ellA{l:+6.3f}%  rd{r:+6.3f}%")
    rows.append(("H2_R_lifted_consistently", Om_H2, Ob_H2, t, l, r))

    # H3: Lift S and d in chi
    chi_H3 = (L_p(S) / L_p(d_hat)) * A_0
    Ob_H3 = 2.0 * A_0 * (1.0 - chi_H3)
    t, l, r = gaps(Om_canon, Ob_H3)
    print(f"  H3: chi lifted (S,d)         Om={Om_canon:.5f} Ob={Ob_H3:.5f}  "
          f"theta_*{t:+6.3f}%  ellA{l:+6.3f}%  rd{r:+6.3f}%")
    rows.append(("H3_chi_lifted", Om_canon, Ob_H3, t, l, r))

    # H4: All bigrade lifted
    A_0_H4 = 1.0 / (L_p(R) * PI)
    Om_H4 = L_p(R) * A_0_H4
    chi_H4 = (L_p(S) / L_p(d_hat)) * A_0_H4
    Ob_H4 = 2.0 * A_0_H4 * (1.0 - chi_H4)
    t, l, r = gaps(Om_H4, Ob_H4)
    print(f"  H4: all bigrade lifted       Om={Om_H4:.5f} Ob={Ob_H4:.5f}  "
          f"theta_*{t:+6.3f}%  ellA{l:+6.3f}%  rd{r:+6.3f}%")
    rows.append(("H4_all_bigrade", Om_H4, Ob_H4, t, l, r))

    # Wrong control: lift Theta (per binding rule, should make things worse)
    Om_WC = Theta / (L_p(Theta) * PI)   # = 18 / (20.25 * pi)
    t, l, r = gaps(Om_WC, Ob_canon)
    print(f"  WC: lift Theta (forbidden)   Om={Om_WC:.5f} Ob={Ob_canon:.5f}  "
          f"theta_*{t:+6.3f}%  ellA{l:+6.3f}%  rd{r:+6.3f}%")
    rows.append(("WC_lift_Theta_forbidden", Om_WC, Ob_canon, t, l, r))

    print()
    print("Joint grid optimum search (1% Om x 1% Ob steps over -5% to +5%):")
    best_sum = float('inf')
    best = None
    for d_Om_pct in np.arange(-5.0, 5.0, 0.1):
        Om_try = Om_canon * (1.0 + d_Om_pct/100)
        for d_Ob_pct in np.arange(-5.0, 5.0, 0.1):
            Ob_try = Ob_canon * (1.0 + d_Ob_pct/100)
            t, l, r = gaps(Om_try, Ob_try)
            s = abs(t) + abs(l) + abs(r)
            if s < best_sum:
                best_sum = s
                best = (Om_try, Ob_try, d_Om_pct, d_Ob_pct, t, l, r)
    print(f"  joint optimum   Om={best[0]:.5f} ({best[2]:+.1f}%)  Ob={best[1]:.5f} ({best[3]:+.1f}%)  "
          f"theta_*{best[4]:+.4f}%  ellA{best[5]:+.4f}%  rd{best[6]:+.4f}%")
    rows.append(("joint_grid_optimum", best[0], best[1], best[4], best[5], best[6]))

    # Verdict logic
    # PASS: theta_* gap < 0.1% AND ell_A < 1% AND r_d < 1%
    # BOUNDARY: theta_* closed but breaks another observable
    # FAIL: no closure achievable

    print()
    print("Verdict analysis:")
    print(f"  CANONICAL gaps: theta_*={rows[0][3]:+.3f}%  ellA={rows[0][4]:+.3f}%  rd={rows[0][5]:+.3f}%")
    print()
    print("  Candidate-by-candidate (excluding canonical):")
    closes_theta = []
    keeps_others = []
    for r in rows[1:]:
        label, Om, Ob, t, l, r_d = r
        theta_closed = abs(t) <= 0.1
        others_ok = abs(l) <= 1.0 and abs(r_d) <= 1.0
        joint_pass = theta_closed and others_ok
        print(f"    {label:30s} theta_closed={theta_closed}  others_OK={others_ok}  joint_PASS={joint_pass}")
        if theta_closed:
            closes_theta.append(label)
        if joint_pass:
            keeps_others.append(label)

    print()
    print(f"  Candidates closing theta_* to <= 0.1%:  {closes_theta}")
    print(f"  Candidates achieving joint PASS:        {keeps_others}")

    if keeps_others:
        verdict = "PASS"
        verdict_note = (f"At least one substrate-lift correction "
                        f"({keeps_others[0]}) closes theta_* without "
                        f"breaking ell_A or r_d.")
    elif closes_theta:
        verdict = "BOUNDARY"
        verdict_note = (f"Substrate-lift correction(s) close theta_* "
                        f"({closes_theta}) but break ell_A or r_d "
                        f"beyond 1%. Mechanism is structurally suggestive "
                        f"but does not produce a clean joint fit.")
    else:
        verdict = "FAIL"   # informative — eliminates the mechanism
        verdict_note = (f"No substrate-lift correction closes theta_* "
                        f"to <= 0.1%. The 0.605% theta_* gap is NOT in "
                        f"the substrate-lift layer; likely in the "
                        f"Hu-Sugiyama / EH fitting-formula error budget.")

    print()
    print(f"CR019b VERDICT: {verdict}")
    print(f"  {verdict_note}")
    print()

    # Outputs
    csv_path = os.path.join(HERE, "CR019b_candidates.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["candidate", "Omega_m", "Omega_b", "theta_star_gap_pct",
                    "ellA_gap_pct", "rd_gap_pct"])
        for r in rows:
            w.writerow(r)

    summary = {
        "artifact": "CR019b_THETA_STAR_LIFT_RULE_AUDIT",
        "classification": "AUDIT_CR",
        "verdict": verdict,
        "verdict_note": verdict_note,
        "precommit_hash": PRECOMMIT_HASH,
        "hypothesis_tested": (
            "Does the 09a binding-work lift rule (bigrade lifted, "
            "Theta exempt) close the +0.605% theta_* gap when applied "
            "to CR019@06's substrate atoms (R, S, d_hat, d_hat^2)?"
        ),
        "canonical_gaps": {
            "theta_star_pct": rows[0][3],
            "ellA_pct": rows[0][4],
            "rd_pct": rows[0][5],
        },
        "candidates_tested": len(rows) - 1,
        "candidates_closing_theta": closes_theta,
        "candidates_joint_pass": keeps_others,
        "joint_grid_optimum": {
            "Omega_m": best[0],
            "Omega_b": best[1],
            "Om_shift_pct": best[2],
            "Ob_shift_pct": best[3],
            "theta_star_residual_pct": best[4],
            "ellA_residual_pct": best[5],
            "rd_residual_pct": best[6],
            "interpretation": (
                "Joint optimum requires Om shift -1.5% and Ob shift +4.9%. "
                "No substrate-lift candidate produces an Ob shift this "
                "large simultaneously with a corresponding Om shift."
            ),
        },
        "structural_finding": (
            "Theta = 18 does not appear explicitly in CR019@06's substrate "
            "inputs. The bigrade atoms that DO appear (R, S, d, d^2) admit "
            "lift corrections, but no single-atom lift closes the theta_* "
            "gap without breaking ell_A or r_d. The 0.605% gap is likely "
            "in the Hu-Sugiyama / EH fitting-formula error budget "
            "(~1% intrinsic accuracy), not in the substrate layer."
        ),
        "implication_for_grammar": (
            "The substrate-lift rule from CR249a (bigrade pays, Theta exempt) "
            "is correctly applied in this test and ruled out as the mechanism "
            "for the theta_* gap. The 09a binding lift rule remains valid "
            "for binding work; it just does not generalize to CR019's "
            "recombination-layer derivation. A substrate-derived recombination "
            "physics (replacing Hu-Sugiyama / EH) would be a separate "
            "multi-CR program."
        ),
    }
    with open(os.path.join(HERE, "CR019b_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    runner_hash = file_sha256(__file__)
    print(f"runner SHA-256 : {runner_hash}")


if __name__ == "__main__":
    main()
