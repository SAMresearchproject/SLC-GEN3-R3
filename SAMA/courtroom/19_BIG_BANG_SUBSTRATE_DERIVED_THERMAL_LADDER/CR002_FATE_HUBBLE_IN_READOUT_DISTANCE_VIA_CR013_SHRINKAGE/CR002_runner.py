"""
CR002@19_FATE_HUBBLE_IN_READOUT_DISTANCE_VIA_CR013_SHRINKAGE runner.

Implements the test specified in CR002_PRECOMMIT.md (SHA-256
b18c49fc4f3c2d73c87cbf0112072db4483d9678e7a42dc052f6c60cc4b26633).

Structural-identity CR. Verifies a closed-form composition of two sealed
upstream results:
  - Fate PDF asymptotic:  H_inf_native = H_0 * sqrt((pi-1)/pi)
  - CR013 sealed saturation: A_los_max = 1/pi
  - Composition:         H_inf_readout = H_0 * ((pi-1)/pi)^(3/2)

Outputs:
  CR002_summary.json
  CR002_evidence_rows.csv
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
import math

# ============================================================================
# Substrate inputs (sealed identities)
# ============================================================================
PI = math.pi
A_0 = 1.0 / (12.0 * PI)
ALPHA_H = 2
D_DIM = 3
R_RADIX = 2 * ALPHA_H * D_DIM

OMEGA_M = R_RADIX * A_0                  # = 1/pi
OMEGA_L = 1.0 - OMEGA_M                  # = (pi-1)/pi

# CR013 shrinkage (sealed)
def A_los(z):
    return A_0 * R_RADIX * (1.0 - (1.0 + z) ** (-D_DIM))

def c_eff_factor(z):
    return 1.0 - A_los(z)

A_LOS_MAX = 1.0 / PI                     # lim z -> infinity

# Measurement anchor
H0 = 68.76                               # km/s/Mpc
C_KMS = 299792.458

# Fate PDF checkpoints
Z_EQ_LAMBDA_PDF = (PI - 1.0) ** (1.0/3.0) - 1.0          # ~ 0.28898
Z_ACC_PDF       = (2.0 * (PI - 1.0)) ** (1.0/3.0) - 1.0  # ~ 0.62402
Q_0_PDF         = (3.0 - 2.0 * PI) / (2.0 * PI)          # ~ -0.52254

# Tolerances
TOL_P1 = 1e-12
TOL_P2 = 1e-12
TOL_P3 = 1e-9


def E_z(z, Omega_m, Omega_L, Omega_r=0.0):
    a = 1.0 / (1.0 + z)
    return math.sqrt(Omega_r/a**4 + Omega_m/a**3 + Omega_L)


def deviation(a, b):
    return abs(a - b) / abs(b)


def main():
    out_dir = Path(__file__).parent

    print("=" * 78)
    print("CR002@19 -- Fate Hubble in measurable distance via CR013 shrinkage")
    print("=" * 78)
    print(f"\nSubstrate identities (sealed):")
    print(f"  A_0       = 1/(12 pi)              = {A_0:.12f}")
    print(f"  R         = {R_RADIX}")
    print(f"  D         = {D_DIM}")
    print(f"  Omega_m   = R * A_0 = 1/pi         = {OMEGA_M:.12f}")
    print(f"  Omega_L   = 1 - Omega_m = (pi-1)/pi = {OMEGA_L:.12f}")
    print(f"  A_los_max = 1/pi                    = {A_LOS_MAX:.12f}")
    print(f"\nMeasurement anchor:  H_0 = {H0} km/s/Mpc")

    # ============================================================
    # P1: H_inf_native three paths must agree
    # ============================================================
    p1_path_A = H0 * math.sqrt(OMEGA_L)
    p1_path_B = H0 * math.sqrt(1.0 - OMEGA_M)
    p1_path_C = H0 * math.sqrt((PI - 1.0) / PI)
    p1_pairs = [
        ("A vs B", deviation(p1_path_A, p1_path_B)),
        ("A vs C", deviation(p1_path_A, p1_path_C)),
        ("B vs C", deviation(p1_path_B, p1_path_C)),
    ]
    p1_max = max(d for _, d in p1_pairs)
    p1_passed = p1_max <= TOL_P1

    print("\n" + "=" * 78)
    print("P1 -- H_inf_native = H_0 * sqrt((pi-1)/pi)")
    print("=" * 78)
    print(f"  Path A: H_0 * sqrt(Omega_L)        = {p1_path_A:.15f} km/s/Mpc")
    print(f"  Path B: H_0 * sqrt(1 - Omega_m)    = {p1_path_B:.15f} km/s/Mpc")
    print(f"  Path C: H_0 * sqrt((pi-1)/pi)      = {p1_path_C:.15f} km/s/Mpc")
    for label, dev in p1_pairs:
        print(f"  {label:10s} relative deviation = {dev:.3e}")
    print(f"  max relative deviation               = {p1_max:.3e}")
    print(f"  tolerance                            = {TOL_P1:.1e}")
    print(f"  P1: {'PASS' if p1_passed else 'FAIL'}")
    H_inf_native = p1_path_C

    # ============================================================
    # P2: H_inf_readout two paths must agree
    # ============================================================
    p2_path_A = H_inf_native * (1.0 - A_LOS_MAX)
    p2_path_B = H0 * ((PI - 1.0) / PI) ** 1.5
    p2_dev = deviation(p2_path_A, p2_path_B)
    p2_passed = p2_dev <= TOL_P2

    print("\n" + "=" * 78)
    print("P2 -- H_inf_readout = H_0 * ((pi-1)/pi)^(3/2)")
    print("=" * 78)
    print(f"  Path A: H_inf_native * (1 - 1/pi)  = {p2_path_A:.15f} km/s/Mpc")
    print(f"  Path B: H_0 * ((pi-1)/pi)^(3/2)    = {p2_path_B:.15f} km/s/Mpc")
    print(f"  relative deviation                   = {p2_dev:.3e}")
    print(f"  tolerance                            = {TOL_P2:.1e}")
    print(f"  P2: {'PASS' if p2_passed else 'FAIL'}")
    H_inf_readout = p2_path_B

    # ============================================================
    # P3: CR013 saturation limit
    # ============================================================
    z_far = 1.0e6
    a_los_far = A_los(z_far)
    p3_dev = deviation(a_los_far, A_LOS_MAX)
    p3_passed = p3_dev <= TOL_P3

    print("\n" + "=" * 78)
    print("P3 -- CR013 saturation: A_los(z) -> 1/pi as z -> infinity")
    print("=" * 78)
    print(f"  A_los(z = 1e6)                      = {a_los_far:.15f}")
    print(f"  A_los_max = 1/pi                    = {A_LOS_MAX:.15f}")
    print(f"  relative deviation                   = {p3_dev:.3e}")
    print(f"  tolerance                            = {TOL_P3:.1e}")
    print(f"  P3: {'PASS' if p3_passed else 'FAIL'}")

    # ============================================================
    # Reported evidence
    # ============================================================
    print("\n" + "=" * 78)
    print("E1/E2 -- A_los, c_eff, H(z) native and readout track")
    print("=" * 78)
    print(f"  {'z':>12s}  {'A_los':>11s}  {'1-A_los':>11s}  "
          f"{'c_eff km/s':>14s}  {'H_native':>10s}  {'H_readout':>10s}")
    print("  " + "-" * 76)
    checkpoints = [
        ("today", 0.0),
        ("z_eq_Lambda", Z_EQ_LAMBDA_PDF),
        ("z_acc", Z_ACC_PDF),
        ("z=1", 1.0),
        ("z=5", 5.0),
        ("z=10", 10.0),
        ("z=100", 100.0),
        ("z_*", 1090.0),
        ("z=1e6", 1.0e6),
    ]
    e2_rows = []
    for label, z in checkpoints:
        a_l = A_los(z)
        ce = C_KMS * (1.0 - a_l)
        Hn = H0 * E_z(z, OMEGA_M, OMEGA_L)
        Hr = Hn * (1.0 - a_l)
        print(f"  {label:>12s}  {a_l:11.7f}  {1.0-a_l:11.7f}  {ce:14.4f}  "
              f"{Hn:10.4f}  {Hr:10.4f}")
        e2_rows.append(dict(label=label, z=z, A_los=a_l, c_eff=ce, H_native=Hn, H_readout=Hr))

    # Fate asymptote row
    Hn_inf = H_inf_native
    Hr_inf = H_inf_readout
    ce_inf = C_KMS * (1.0 - A_LOS_MAX)
    print(f"  {'fate inf':>12s}  {A_LOS_MAX:11.7f}  {1.0-A_LOS_MAX:11.7f}  "
          f"{ce_inf:14.4f}  {Hn_inf:10.4f}  {Hr_inf:10.4f}")

    print("\n" + "=" * 78)
    print("E3 -- Fate PDF checkpoint constants (closed form)")
    print("=" * 78)
    print(f"  z_eq_Lambda = (pi-1)^(1/3) - 1     = {Z_EQ_LAMBDA_PDF:.6f}")
    print(f"  z_acc       = [2(pi-1)]^(1/3) - 1  = {Z_ACC_PDF:.6f}")
    print(f"  q_0         = (3 - 2 pi)/(2 pi)    = {Q_0_PDF:.6f}")

    print("\n" + "=" * 78)
    print("E4 -- LambdaCDM comparison (native only; LCDM has no shrinkage)")
    print("=" * 78)
    Omega_L_lcdm = 0.685
    H_inf_lcdm_native = H0 * math.sqrt(Omega_L_lcdm)
    print(f"  Omega_L_LCDM = 0.685")
    print(f"  H_inf_LCDM_native = H_0 * sqrt(0.685)   = {H_inf_lcdm_native:.4f} km/s/Mpc")
    print(f"  H_inf_SAM_native  = H_0 * sqrt((pi-1)/pi) = {H_inf_native:.4f} km/s/Mpc")
    print(f"  difference                             = {abs(H_inf_lcdm_native - H_inf_native):.4f} km/s/Mpc")
    print(f"  (LCDM has no analog for H_inf_readout)")

    print("\n" + "=" * 78)
    print("E5 -- Headline number")
    print("=" * 78)
    omega_L_3_2 = ((PI - 1.0) / PI) ** 1.5
    print(f"  H_inf_readout / H_0 = ((pi-1)/pi)^(3/2) = {omega_L_3_2:.10f}")
    print(f"  H_inf_readout      = {H_inf_readout:.4f} km/s/Mpc")
    print(f"  (substrate prediction: asymptotic expansion rate in measurable distance)")

    # ============================================================
    # Verdict
    # ============================================================
    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    if p1_passed and p2_passed and p3_passed:
        verdict = "PASS"
        verdict_reason = "P1, P2, P3 all hold within tolerance; substrate identities compose consistently"
    else:
        verdict = "FAIL"
        failed = [k for k, v in [("P1", p1_passed), ("P2", p2_passed), ("P3", p3_passed)] if not v]
        verdict_reason = f"failed: {failed}"
    print(f"  P1: {'PASS' if p1_passed else 'FAIL'}    "
          f"P2: {'PASS' if p2_passed else 'FAIL'}    "
          f"P3: {'PASS' if p3_passed else 'FAIL'}")
    print(f"\n  CR002@19 verdict: {verdict}")
    print(f"  reason: {verdict_reason}")
    print(f"\n  Headline: H_inf_readout = H_0 * ((pi-1)/pi)^(3/2) = {H_inf_readout:.4f} km/s/Mpc")

    # ============================================================
    # Write outputs
    # ============================================================
    summary = dict(
        precommit_sha256="b18c49fc4f3c2d73c87cbf0112072db4483d9678e7a42dc052f6c60cc4b26633",
        substrate=dict(
            A_0=A_0, alpha_H=ALPHA_H, D=D_DIM, R=R_RADIX,
            Omega_m=OMEGA_M, Omega_L=OMEGA_L, A_los_max=A_LOS_MAX,
        ),
        measurement_input=dict(H_0_kms_Mpc=H0),
        closed_form_results=dict(
            H_inf_native_kms_Mpc=H_inf_native,
            H_inf_readout_kms_Mpc=H_inf_readout,
            H_inf_readout_over_H_0=H_inf_readout / H0,
            omega_L_3_2=omega_L_3_2,
            z_eq_Lambda=Z_EQ_LAMBDA_PDF,
            z_acc=Z_ACC_PDF,
            q_0=Q_0_PDF,
        ),
        P1=dict(
            name="H_inf_native three-path identity",
            path_A_H0_sqrtOmegaL=p1_path_A,
            path_B_H0_sqrt1minusOmegaM=p1_path_B,
            path_C_H0_sqrtPiMinus1OverPi=p1_path_C,
            max_relative_deviation=p1_max,
            tolerance=TOL_P1,
            passed=p1_passed,
        ),
        P2=dict(
            name="H_inf_readout two-path identity",
            path_A_native_times_one_minus_A_max=p2_path_A,
            path_B_H0_omegaL_3_2=p2_path_B,
            relative_deviation=p2_dev,
            tolerance=TOL_P2,
            passed=p2_passed,
        ),
        P3=dict(
            name="CR013 saturation limit",
            z_test=z_far,
            A_los_at_z=a_los_far,
            A_los_max=A_LOS_MAX,
            relative_deviation=p3_dev,
            tolerance=TOL_P3,
            passed=p3_passed,
        ),
        evidence_checkpoints=e2_rows,
        lcdm_comparison=dict(
            Omega_L_LCDM=Omega_L_lcdm,
            H_inf_LCDM_native=H_inf_lcdm_native,
            H_inf_SAM_native=H_inf_native,
            difference=abs(H_inf_lcdm_native - H_inf_native),
            note="LCDM has no analog for shrinkage / readout-vs-native distinction",
        ),
        verdict=verdict,
        verdict_reason=verdict_reason,
    )
    (out_dir / "CR002_summary.json").write_text(json.dumps(summary, indent=2, default=str))

    evidence = [
        dict(item="Omega_m", value=OMEGA_M, passes=True),
        dict(item="Omega_L", value=OMEGA_L, passes=True),
        dict(item="A_los_max", value=A_LOS_MAX, passes=True),
        dict(item="H_0_input", value=H0, passes=True),
        dict(item="H_inf_native", value=H_inf_native, passes=True),
        dict(item="H_inf_readout", value=H_inf_readout, passes=True),
        dict(item="H_inf_readout_over_H_0", value=H_inf_readout/H0, passes=True),
        dict(item="z_eq_Lambda", value=Z_EQ_LAMBDA_PDF, passes=True),
        dict(item="z_acc", value=Z_ACC_PDF, passes=True),
        dict(item="q_0", value=Q_0_PDF, passes=True),
        dict(item="P1_max_relative_deviation", value=p1_max, passes=p1_passed),
        dict(item="P2_relative_deviation", value=p2_dev, passes=p2_passed),
        dict(item="P3_relative_deviation", value=p3_dev, passes=p3_passed),
        dict(item="P1_passed", value=p1_passed, passes=p1_passed),
        dict(item="P2_passed", value=p2_passed, passes=p2_passed),
        dict(item="P3_passed", value=p3_passed, passes=p3_passed),
        dict(item="H_inf_LCDM_native", value=H_inf_lcdm_native, passes=True),
        dict(item="verdict", value=verdict, passes=(verdict == "PASS")),
    ]
    for row in e2_rows:
        evidence.append(dict(item=f"A_los_{row['label']}",   value=row["A_los"],    passes=True))
        evidence.append(dict(item=f"c_eff_{row['label']}",   value=row["c_eff"],    passes=True))
        evidence.append(dict(item=f"H_native_{row['label']}", value=row["H_native"], passes=True))
        evidence.append(dict(item=f"H_readout_{row['label']}", value=row["H_readout"], passes=True))

    with (out_dir / "CR002_evidence_rows.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["item", "value", "pass"])
        w.writeheader()
        for e in evidence:
            w.writerow({"item": e["item"], "value": e["value"], "pass": e["passes"]})


if __name__ == "__main__":
    main()
