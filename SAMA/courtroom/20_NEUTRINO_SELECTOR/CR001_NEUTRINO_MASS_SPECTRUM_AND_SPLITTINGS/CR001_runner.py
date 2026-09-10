"""
CR001@20_NEUTRINO_MASS_SPECTRUM_AND_SPLITTINGS runner.

Implements the test specified in CR001_PRECOMMIT.md (SHA-256
8e6cb1975cd7d2084ffbbf2c215472d2ef8042fae18b68e76b74b94dc4281c77).

Substrate derivation rule (locked):
  m_1 = base_eV * 1
  m_2 = base_eV * sqrt(alpha_H)            with alpha_H = 2
  m_3 = base_eV * (alpha_H * D)            with D = 3

  base_eV = sqrt(Delta_m2_31_observed / 35)

Outputs:
  CR001_summary.json
  CR001_evidence_rows.csv
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
import math

# ============================================================================
# Sealed substrate atoms (Volume I)
# ============================================================================
ALPHA_H = 2
D = 3

# ============================================================================
# External measurement anchors
# ============================================================================
DELTA_M2_31_OBS_EV2 = 2.515e-3      # eV^2, PDG 2024 normal ordering (anchor)
DELTA_M2_21_OBS_EV2 = 7.42e-5       # eV^2, PDG 2024 (comparison target)
SIGMA_M_NU_PLANCK_BOUND_EV = 0.12   # Planck 2018 + BAO, 95% CL
KATRIN_M_BETA_BOUND_EV = 0.45       # KATRIN 2024 tritium beta-decay endpoint

# PDG 2024 mixing (for E5 only)
SIN2_THETA_12 = 0.307
SIN2_THETA_13 = 0.0220
SIN2_THETA_23 = 0.451

# Gates
P1_THRESHOLD_REL = 0.10   # splittings ratio within 10% of observed
P2_THRESHOLD_EV = 0.12    # Sigma m_nu below Planck bound


def deviation(a, b):
    return (a - b) / b


def main():
    out_dir = Path(__file__).parent

    print("=" * 78)
    print("CR001@20 -- Neutrino mass spectrum and splittings")
    print("=" * 78)

    # ============================================================
    # Substrate derivation
    # ============================================================
    print(f"\nSealed substrate atoms:")
    print(f"  alpha_H = {ALPHA_H}")
    print(f"  D       = {D}")

    # Structural ratios (substrate-derived, no anchor)
    r1 = 1.0
    r2 = math.sqrt(ALPHA_H)
    r3 = ALPHA_H * D

    # Substrate-derived splittings ratio (closed form, no anchor)
    ratio_sam = (r3**2 - r1**2) / (r2**2 - r1**2)
    ratio_obs = DELTA_M2_31_OBS_EV2 / DELTA_M2_21_OBS_EV2

    print(f"\nStructural mass ratios:")
    print(f"  m_1 / base = 1                       = {r1:.10f}")
    print(f"  m_2 / base = sqrt(alpha_H) = sqrt(2) = {r2:.10f}")
    print(f"  m_3 / base = alpha_H * D = 6         = {r3:.10f}")

    print(f"\nSubstrate-derived splittings ratio:")
    print(f"  Delta m^2_31 / Delta m^2_21 (SAM)    = ((alpha_H*D)^2 - 1) / (alpha_H - 1)")
    print(f"                                       = (36 - 1) / (2 - 1)")
    print(f"                                       = {ratio_sam:.4f}")
    print(f"  Delta m^2_31 / Delta m^2_21 (obs)    = {DELTA_M2_31_OBS_EV2:.3e} / {DELTA_M2_21_OBS_EV2:.3e}")
    print(f"                                       = {ratio_obs:.4f}")

    # eV anchor from larger splitting
    base_eV = math.sqrt(DELTA_M2_31_OBS_EV2 / ratio_sam)
    print(f"\neV anchor:")
    print(f"  base_eV = sqrt(Delta m^2_31 / 35)")
    print(f"          = sqrt({DELTA_M2_31_OBS_EV2:.3e} / {ratio_sam})")
    print(f"          = {base_eV:.10f} eV")

    # Three mass eigenstates
    m1 = base_eV * r1
    m2 = base_eV * r2
    m3 = base_eV * r3
    sigma_m_nu = m1 + m2 + m3

    print(f"\nThree neutrino mass eigenstates:")
    print(f"  m_1 = {m1*1000:.4f} meV  = {m1:.10f} eV")
    print(f"  m_2 = {m2*1000:.4f} meV  = {m2:.10f} eV")
    print(f"  m_3 = {m3*1000:.4f} meV  = {m3:.10f} eV")
    print(f"  Sigma m_nu = {sigma_m_nu*1000:.4f} meV = {sigma_m_nu:.10f} eV")
    print(f"  Ordering = normal (m_3 > m_2 > m_1 by construction)")

    # ============================================================
    # Gates
    # ============================================================
    dev_p1 = deviation(ratio_sam, ratio_obs)
    p1_passed = abs(dev_p1) <= P1_THRESHOLD_REL

    p2_passed = sigma_m_nu < P2_THRESHOLD_EV

    p3_passed = m1 > 0 and m2 > 0 and m3 > 0

    print("\n" + "=" * 78)
    print("Load-bearing gates")
    print("=" * 78)
    print(f"  P1  splittings ratio SAM vs observed:")
    print(f"      SAM = {ratio_sam:.4f},  observed = {ratio_obs:.4f}")
    print(f"      relative deviation = {dev_p1*100:+.3f}%")
    print(f"      threshold = +/- {P1_THRESHOLD_REL*100:.1f}%")
    print(f"      P1: {'PASS' if p1_passed else 'FAIL'}")

    print(f"\n  P2  Sigma m_nu vs Planck bound:")
    print(f"      Sigma m_nu = {sigma_m_nu:.6f} eV")
    print(f"      Planck bound = {P2_THRESHOLD_EV} eV")
    print(f"      margin to bound = {(P2_THRESHOLD_EV - sigma_m_nu)/P2_THRESHOLD_EV*100:.2f}% below")
    print(f"      P2: {'PASS' if p2_passed else 'FAIL'}")

    print(f"\n  P3  Three positive mass eigenstates:")
    print(f"      m_1 > 0: {m1 > 0}")
    print(f"      m_2 > 0: {m2 > 0}")
    print(f"      m_3 > 0: {m3 > 0}")
    print(f"      P3: {'PASS' if p3_passed else 'FAIL'}")

    # ============================================================
    # Reported evidence
    # ============================================================
    # E1: Predicted Delta m^2_21
    delta_m2_21_sam = base_eV**2 * (r2**2 - r1**2)
    dev_e1 = deviation(delta_m2_21_sam, DELTA_M2_21_OBS_EV2)

    # E5: m_beta
    U_e1_sq = (1 - SIN2_THETA_13) * (1 - SIN2_THETA_12)
    U_e2_sq = (1 - SIN2_THETA_13) * SIN2_THETA_12
    U_e3_sq = SIN2_THETA_13
    m_beta_sq = U_e1_sq * m1**2 + U_e2_sq * m2**2 + U_e3_sq * m3**2
    m_beta = math.sqrt(m_beta_sq)

    print("\n" + "=" * 78)
    print("Reported evidence")
    print("=" * 78)
    print(f"  E1  Delta m^2_21 from substrate anchor:")
    print(f"      SAM = {delta_m2_21_sam:.6e} eV^2")
    print(f"      observed = {DELTA_M2_21_OBS_EV2:.6e} eV^2")
    print(f"      deviation = {dev_e1*100:+.3f}%")
    print(f"  E2  Individual masses:")
    print(f"      m_1 = {m1*1000:.4f} meV")
    print(f"      m_2 = {m2*1000:.4f} meV")
    print(f"      m_3 = {m3*1000:.4f} meV")
    print(f"  E3  Ordering: normal (by substrate construction)")
    print(f"  E4  Lightest mass: m_1 = {m1*1000:.4f} meV")
    print(f"  E5  Effective beta-decay mass:")
    print(f"      |U_e1|^2 = {U_e1_sq:.4f}")
    print(f"      |U_e2|^2 = {U_e2_sq:.4f}")
    print(f"      |U_e3|^2 = {U_e3_sq:.4f}")
    print(f"      m_beta = {m_beta*1000:.4f} meV")
    print(f"      KATRIN bound = {KATRIN_M_BETA_BOUND_EV*1000} meV (SAM is factor {KATRIN_M_BETA_BOUND_EV/m_beta:.1f} below)")
    print(f"  E6  DESI+CMB tighter bound ~0.072 eV:")
    print(f"      SAM Sigma m_nu = {sigma_m_nu:.4f} eV — {'inside' if sigma_m_nu < 0.072 else 'just outside'} tighter bound")

    # ============================================================
    # Verdict
    # ============================================================
    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    all_pass = p1_passed and p2_passed and p3_passed
    if all_pass:
        verdict = "PASS"
        verdict_reason = (
            "P1, P2, P3 all hold under canonical substrate inputs. "
            "Substrate-derived splittings ratio 35 matches observed 33.9 within 3.3%; "
            "Sigma m_nu = 0.071 eV is 40% below the Planck cosmological bound; "
            "all three mass eigenstates are positive."
        )
    else:
        verdict = "FAIL"
        failed = [k for k, v in [("P1", p1_passed), ("P2", p2_passed), ("P3", p3_passed)] if not v]
        verdict_reason = f"failed: {failed}"
    print(f"  P1: {'PASS' if p1_passed else 'FAIL'}    "
          f"P2: {'PASS' if p2_passed else 'FAIL'}    "
          f"P3: {'PASS' if p3_passed else 'FAIL'}")
    print(f"\n  CR001@20 verdict: {verdict}")
    print(f"\n  Headline: m_1 : m_2 : m_3 = 1 : sqrt(2) : 6")
    print(f"            Delta m^2_31 / Delta m^2_21 = 35 (SAM) vs 33.9 (obs)")
    print(f"            Sigma m_nu = {sigma_m_nu*1000:.2f} meV < 120 meV Planck bound")

    # ============================================================
    # Write outputs
    # ============================================================
    summary = dict(
        precommit_sha256="8e6cb1975cd7d2084ffbbf2c215472d2ef8042fae18b68e76b74b94dc4281c77",
        substrate=dict(alpha_H=ALPHA_H, D=D),
        derivation_rule=dict(
            description="m_i = base_eV * substrate_ratio_i",
            ratios=dict(r1=r1, r2=r2, r3=r3),
            ratio_formula="(1, sqrt(alpha_H), alpha_H * D) = (1, sqrt(2), 6)",
            eV_anchor="base_eV = sqrt(Delta m^2_31 / 35)",
        ),
        substrate_derived_splittings_ratio=ratio_sam,
        observed_splittings_ratio=ratio_obs,
        base_eV=base_eV,
        masses_eV=dict(m_1=m1, m_2=m2, m_3=m3),
        Sigma_m_nu_eV=sigma_m_nu,
        ordering="normal",
        external_anchors=dict(
            Delta_m2_31_eV2=DELTA_M2_31_OBS_EV2,
            Delta_m2_21_eV2=DELTA_M2_21_OBS_EV2,
            Sigma_m_nu_Planck_bound_eV=SIGMA_M_NU_PLANCK_BOUND_EV,
            KATRIN_m_beta_bound_eV=KATRIN_M_BETA_BOUND_EV,
        ),
        P1=dict(
            name="Splittings ratio SAM vs observed",
            SAM=ratio_sam,
            observed=ratio_obs,
            deviation=dev_p1,
            threshold=P1_THRESHOLD_REL,
            passed=p1_passed,
        ),
        P2=dict(
            name="Sigma m_nu vs Planck cosmological bound",
            Sigma_m_nu=sigma_m_nu,
            bound=P2_THRESHOLD_EV,
            margin_below_pct=(P2_THRESHOLD_EV - sigma_m_nu)/P2_THRESHOLD_EV*100,
            passed=p2_passed,
        ),
        P3=dict(
            name="Three positive mass eigenstates",
            m_1=m1, m_2=m2, m_3=m3,
            passed=p3_passed,
        ),
        evidence=dict(
            E1_Delta_m2_21_SAM=delta_m2_21_sam,
            E1_Delta_m2_21_observed=DELTA_M2_21_OBS_EV2,
            E1_deviation=dev_e1,
            E5_m_beta=m_beta,
            E5_m_beta_meV=m_beta*1000,
            E5_KATRIN_factor_below=KATRIN_M_BETA_BOUND_EV/m_beta,
        ),
        verdict=verdict,
        verdict_reason=verdict_reason,
    )
    (out_dir / "CR001_summary.json").write_text(json.dumps(summary, indent=2, default=str))

    evidence = [
        dict(item="alpha_H", value=ALPHA_H, passes=True),
        dict(item="D", value=D, passes=True),
        dict(item="m_1_eV", value=m1, passes=True),
        dict(item="m_2_eV", value=m2, passes=True),
        dict(item="m_3_eV", value=m3, passes=True),
        dict(item="Sigma_m_nu_eV", value=sigma_m_nu, passes=p2_passed),
        dict(item="splittings_ratio_SAM", value=ratio_sam, passes=True),
        dict(item="splittings_ratio_observed", value=ratio_obs, passes=True),
        dict(item="splittings_ratio_deviation_pct", value=dev_p1*100, passes=p1_passed),
        dict(item="Delta_m2_21_SAM_eV2", value=delta_m2_21_sam, passes=True),
        dict(item="Delta_m2_21_observed_eV2", value=DELTA_M2_21_OBS_EV2, passes=True),
        dict(item="Delta_m2_21_deviation_pct", value=dev_e1*100, passes=True),
        dict(item="m_beta_eV", value=m_beta, passes=True),
        dict(item="ordering", value="normal", passes=True),
        dict(item="P1_passed", value=p1_passed, passes=p1_passed),
        dict(item="P2_passed", value=p2_passed, passes=p2_passed),
        dict(item="P3_passed", value=p3_passed, passes=p3_passed),
        dict(item="verdict", value=verdict, passes=(verdict == "PASS")),
    ]
    with (out_dir / "CR001_evidence_rows.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["item", "value", "pass"])
        w.writeheader()
        for e in evidence:
            w.writerow({"item": e["item"], "value": e["value"], "pass": e["passes"]})


if __name__ == "__main__":
    main()
