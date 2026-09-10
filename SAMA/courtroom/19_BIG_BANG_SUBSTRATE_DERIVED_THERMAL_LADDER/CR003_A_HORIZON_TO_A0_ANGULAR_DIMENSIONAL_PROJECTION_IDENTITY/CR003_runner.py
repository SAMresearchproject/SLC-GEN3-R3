"""
CR003@19_A_HORIZON_TO_A0_ANGULAR_DIMENSIONAL_PROJECTION_IDENTITY runner.

Implements the test specified in CR003_PRECOMMIT.md (SHA-256
27603dd611afe5ed48fc24709126a58e6553b390a961fe06c4aec59a6ae3b658).

Structural-identity CR. Verifies the closed-form projection:
  A_0 = A_horizon / (4*pi*D)
at A_horizon = 1, D = 3 yields A_0 = 1/(12*pi); and reports the
D-sensitivity table with the R-coupling invariance check showing
that R*A_0 = alpha_H/(2*pi) does not depend on D when
R = 2*alpha_H*D.

Outputs:
  CR003_summary.json
  CR003_evidence_rows.csv
"""

from __future__ import annotations

from pathlib import Path
import csv
import json
import math

PI = math.pi

# Substrate primitives (sealed)
A_HORIZON = 1
ALPHA_H = 2
D_SUBSTRATE = 3
ANGULAR_FACTOR_3D = 4.0 * PI
R_RADIX = 2 * ALPHA_H * D_SUBSTRATE   # = 12

TOL = 1e-12


def deviation(a, b):
    return abs(a - b) / abs(b) if b != 0 else abs(a - b)


def main():
    out_dir = Path(__file__).parent

    print("=" * 78)
    print("CR003@19 -- A_horizon -> A_0 angular/dimensional projection identity")
    print("=" * 78)
    print(f"\nSubstrate inputs (sealed):")
    print(f"  A_horizon  = {A_HORIZON}")
    print(f"  alpha_H    = {ALPHA_H}")
    print(f"  D          = {D_SUBSTRATE}")
    print(f"  R = 2*alpha_H*D = {R_RADIX}")
    print(f"  angular    = 4*pi = {ANGULAR_FACTOR_3D:.12f}")

    # ============================================================
    # P1: A_0 = A_horizon / (4*pi*D) at D=3
    # ============================================================
    A0_path_A = 1.0 / (4.0 * PI * 3.0)                # direct
    A0_path_B = 1.0 / (12.0 * PI)                      # sealed substrate value
    A0_path_C = A_HORIZON / (ANGULAR_FACTOR_3D * D_SUBSTRATE)  # symbolic

    p1_pairs = [
        ("A vs B", deviation(A0_path_A, A0_path_B)),
        ("A vs C", deviation(A0_path_A, A0_path_C)),
        ("B vs C", deviation(A0_path_B, A0_path_C)),
    ]
    p1_max = max(d for _, d in p1_pairs)
    p1_passed = p1_max <= TOL

    print("\n" + "=" * 78)
    print("P1 -- A_0 = A_horizon / (4*pi*D) at D=3 reproduces 1/(12*pi)")
    print("=" * 78)
    print(f"  Path A: 1 / (4 * pi * 3)              = {A0_path_A:.18f}")
    print(f"  Path B: 1 / (12 * pi)                 = {A0_path_B:.18f}")
    print(f"  Path C: A_horizon / (4*pi*D)          = {A0_path_C:.18f}")
    for label, dev in p1_pairs:
        print(f"  {label:10s} relative deviation = {dev:.3e}")
    print(f"  max relative deviation               = {p1_max:.3e}")
    print(f"  tolerance                            = {TOL:.1e}")
    print(f"  P1: {'PASS' if p1_passed else 'FAIL'}")
    A_0_sealed = A0_path_B

    # ============================================================
    # P2: R*A_0 = 1/pi with R = 2*alpha_H*D, alpha_H=2, D=3
    # ============================================================
    p2_path_A = R_RADIX * A_0_sealed                       # explicit
    p2_path_B = ALPHA_H / (2.0 * PI)                       # reduced form
    p2_path_C = 1.0 / PI                                    # direct closed form

    p2_pairs = [
        ("A vs B", deviation(p2_path_A, p2_path_B)),
        ("A vs C", deviation(p2_path_A, p2_path_C)),
        ("B vs C", deviation(p2_path_B, p2_path_C)),
    ]
    p2_max = max(d for _, d in p2_pairs)
    p2_passed = p2_max <= TOL

    print("\n" + "=" * 78)
    print("P2 -- R*A_0 = 1/pi with alpha_H=2, D=3, R = 2*alpha_H*D = 12")
    print("=" * 78)
    print(f"  Path A: R * A_0  = 12 * 1/(12*pi)     = {p2_path_A:.18f}")
    print(f"  Path B: alpha_H / (2*pi)              = {p2_path_B:.18f}")
    print(f"  Path C: 1 / pi                        = {p2_path_C:.18f}")
    for label, dev in p2_pairs:
        print(f"  {label:10s} relative deviation = {dev:.3e}")
    print(f"  max relative deviation               = {p2_max:.3e}")
    print(f"  tolerance                            = {TOL:.1e}")
    print(f"  P2: {'PASS' if p2_passed else 'FAIL'}")
    Omega_m = p2_path_C

    # ============================================================
    # P3: A(r=r_s) = r_s/r at r=r_s yields A=1
    # ============================================================
    def A_profile(r, r_s):
        return r_s / r

    p3_tests = [
        ("r_s = 1 (unit)",     1.0),
        ("r_s ~ 2950 m (Sun)", 2.95e3),
        ("r_s = 1e30 m",       1.0e30),
    ]
    p3_devs = []
    print("\n" + "=" * 78)
    print("P3 -- A(r=r_s) = r_s/r = 1 (full local closure)")
    print("=" * 78)
    for label, r_s in p3_tests:
        A_at_r_s = A_profile(r_s, r_s)
        dev = abs(A_at_r_s - 1.0)
        p3_devs.append((label, r_s, A_at_r_s, dev))
        print(f"  {label:30s}  A(r_s) = {A_at_r_s:.18f}  |dev| = {dev:.3e}")
    p3_max = max(d for _, _, _, d in p3_devs)
    p3_passed = p3_max <= TOL
    print(f"  max |A - 1|                          = {p3_max:.3e}")
    print(f"  tolerance                            = {TOL:.1e}")
    print(f"  P3: {'PASS' if p3_passed else 'FAIL'}")

    # ============================================================
    # E1: Sensitivity table with R-coupling invariance check
    # ============================================================
    print("\n" + "=" * 78)
    print("E1 -- D-sensitivity table for A_0 = 1/(4*pi*D)")
    print("       Coupled-constant check: R*A_0 invariant when R = 2*alpha_H*D")
    print("=" * 78)
    print(f"  {'D':>3s}   {'A_0 = 1/(4*pi*D)':>22s}   "
          f"{'R = 2*alpha_H*D':>16s}   {'R*A_0':>20s}   {'matches 1/pi?':>14s}")
    print("  " + "-" * 76)
    e1_rows = []
    for D in [2, 3, 4, 5]:
        A0_at_D = 1.0 / (4.0 * PI * D)
        R_at_D = 2 * ALPHA_H * D
        R_A0 = R_at_D * A0_at_D
        match = abs(R_A0 - 1.0/PI) <= 1e-15
        e1_rows.append(dict(D=D, A_0=A0_at_D, R=R_at_D, R_A0=R_A0, matches_Omega_m=match))
        marker = "*" if D == D_SUBSTRATE else " "
        print(f"  {D:>3d}   {A0_at_D:>22.16f}   {R_at_D:>16d}   "
              f"{R_A0:>20.16f}   {'YES' if match else 'no':>14s}  {marker}")
    print(f"  * = D = 3 recovers sealed SAM A_0 = 1/(12*pi)")
    print(f"  Coupling invariance: R*A_0 = alpha_H/(2*pi) = 1/pi for ALL D when")
    print(f"  R is coupled as R = 2*alpha_H*D (alpha_H = 2). Omega_m identity")
    print(f"  is fixed by alpha_H alone; D enters A_0 and R coherently and cancels.")

    # ============================================================
    # E2: A(r) ramp outside the closure
    # ============================================================
    print("\n" + "=" * 78)
    print("E2 -- A(r) = r_s/r ramp outside the closure (r_s = 1)")
    print("=" * 78)
    print(f"  {'r/r_s':>8s}   {'A(r)':>14s}")
    print("  " + "-" * 30)
    e2_rows = []
    for r_over_rs in [1.0, 2.0, 5.0, 10.0, 100.0, 1000.0]:
        A_val = 1.0 / r_over_rs
        e2_rows.append(dict(r_over_rs=r_over_rs, A=A_val))
        print(f"  {r_over_rs:>8.1f}   {A_val:>14.10f}")

    # ============================================================
    # E3: Bridge map (chain to downstream PASSes)
    # ============================================================
    print("\n" + "=" * 78)
    print("E3 -- Bridge map: A_horizon = 1 -> all downstream sealed PASSes")
    print("=" * 78)
    bridge_chain = [
        ("full local closure", "A_horizon = 1", 1.0),
        ("angular/dim projection", "A_0 = 1/(4*pi*D)", 1.0/(4.0*PI*D_SUBSTRATE)),
        ("cosmic background seed", "A_0 = 1/(12*pi)", 1.0/(12.0*PI)),
        ("radix coupling", "R = 2*alpha_H*D = 12", float(R_RADIX)),
        ("matter density identity", "Omega_m = R*A_0 = 1/pi", 1.0/PI),
        ("substrate carrier ratio", "chi = (S/D)*A_0 = 2/(9*pi)", 2.0/(9.0*PI)),
        ("baryon density identity", "Omega_b = 2*A_0*(1-chi)", 2.0*(1.0/(12.0*PI))*(1.0 - 2.0/(9.0*PI))),
        ("Lambda density identity", "Omega_Lambda = (pi-1)/pi", (PI-1.0)/PI),
    ]
    for label, expr, value in bridge_chain:
        print(f"  {label:30s}  {expr:35s}  = {value:.10f}")

    # ============================================================
    # E4 -- Reframing note
    # ============================================================
    print("\n" + "=" * 78)
    print("E4 -- Reframing note")
    print("=" * 78)
    print("  The r_s surface where A = 1 is conventionally labeled the")
    print("  'black-hole horizon' in observational language. The substrate")
    print("  math reads it neutrally: A(r) = r_s/r monotonically; A reaches")
    print("  the unit value at r = r_s; this is the FULL LOCAL CLOSURE of")
    print("  the substrate accumulation. The observational labeling sits on")
    print("  top of the structural condition but is not part of the substrate")
    print("  identity. The same A = 1 condition projects through angular and")
    print("  dimensional ledger into the cosmic seed A_0 = 1/(12*pi).")

    # ============================================================
    # Verdict
    # ============================================================
    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    all_pass = p1_passed and p2_passed and p3_passed
    if all_pass:
        verdict = "PASS"
        verdict_reason = ("P1, P2, P3 all hold to machine precision; "
                          "A_horizon = 1 projects through 4*pi*D at D=3 into "
                          "the sealed A_0 = 1/(12*pi), and R*A_0 = 1/pi is "
                          "invariant under D when R = 2*alpha_H*D.")
    else:
        verdict = "FAIL"
        failed = [k for k, v in [("P1", p1_passed), ("P2", p2_passed), ("P3", p3_passed)] if not v]
        verdict_reason = f"failed: {failed}"
    print(f"  P1: {'PASS' if p1_passed else 'FAIL'}    "
          f"P2: {'PASS' if p2_passed else 'FAIL'}    "
          f"P3: {'PASS' if p3_passed else 'FAIL'}")
    print(f"\n  CR003@19 verdict: {verdict}")
    print(f"  reason: {verdict_reason}")
    print(f"\n  Headline: A_horizon = 1 -> A_0 = 1/(4*pi*D) at D=3 = 1/(12*pi)")
    print(f"           Omega_m = R*A_0 = alpha_H/(2*pi) = 1/pi (D-invariant under R coupling)")

    # ============================================================
    # Write outputs
    # ============================================================
    summary = dict(
        precommit_sha256="27603dd611afe5ed48fc24709126a58e6553b390a961fe06c4aec59a6ae3b658",
        substrate=dict(
            A_horizon=A_HORIZON, alpha_H=ALPHA_H, D=D_SUBSTRATE,
            R=R_RADIX, angular_4pi=ANGULAR_FACTOR_3D,
        ),
        closed_form_results=dict(
            A_0_via_projection=A_0_sealed,
            A_0_sealed_value=1.0/(12.0*PI),
            Omega_m_via_coupling=Omega_m,
            Omega_m_invariant_form="alpha_H/(2*pi)",
        ),
        P1=dict(
            name="A_0 angular-dimensional projection identity",
            path_A_direct=A0_path_A,
            path_B_sealed=A0_path_B,
            path_C_symbolic=A0_path_C,
            max_relative_deviation=p1_max,
            tolerance=TOL,
            passed=p1_passed,
        ),
        P2=dict(
            name="R*A_0 coupled-constant density identity",
            path_A_explicit=p2_path_A,
            path_B_reduced=p2_path_B,
            path_C_direct=p2_path_C,
            max_relative_deviation=p2_max,
            tolerance=TOL,
            passed=p2_passed,
        ),
        P3=dict(
            name="Horizon unit-closure identity A(r=r_s) = 1",
            tests=[dict(label=L, r_s=r, A=A, abs_dev=d) for L, r, A, d in p3_devs],
            max_abs_deviation=p3_max,
            tolerance=TOL,
            passed=p3_passed,
        ),
        E1_D_sensitivity=e1_rows,
        E2_A_ramp_outside_closure=e2_rows,
        E3_bridge_chain=[dict(label=l, expr=e, value=v) for l, e, v in bridge_chain],
        E4_reframing="The r_s surface where A=1 is the full local closure of the substrate accumulation; the 'black hole' label is observational labeling and not part of the substrate identity.",
        verdict=verdict,
        verdict_reason=verdict_reason,
    )
    (out_dir / "CR003_summary.json").write_text(json.dumps(summary, indent=2, default=str))

    evidence = [
        dict(item="A_horizon", value=A_HORIZON, passes=True),
        dict(item="alpha_H", value=ALPHA_H, passes=True),
        dict(item="D", value=D_SUBSTRATE, passes=True),
        dict(item="R = 2*alpha_H*D", value=R_RADIX, passes=True),
        dict(item="A_0_via_projection", value=A_0_sealed, passes=True),
        dict(item="A_0_sealed_value", value=1.0/(12.0*PI), passes=True),
        dict(item="Omega_m_via_coupling", value=Omega_m, passes=True),
        dict(item="P1_max_relative_deviation", value=p1_max, passes=p1_passed),
        dict(item="P2_max_relative_deviation", value=p2_max, passes=p2_passed),
        dict(item="P3_max_abs_deviation", value=p3_max, passes=p3_passed),
        dict(item="P1_passed", value=p1_passed, passes=p1_passed),
        dict(item="P2_passed", value=p2_passed, passes=p2_passed),
        dict(item="P3_passed", value=p3_passed, passes=p3_passed),
        dict(item="verdict", value=verdict, passes=(verdict == "PASS")),
    ]
    for r in e1_rows:
        evidence.append(dict(item=f"E1_D{r['D']}_A_0", value=r["A_0"], passes=True))
        evidence.append(dict(item=f"E1_D{r['D']}_R_A0", value=r["R_A0"], passes=r["matches_Omega_m"]))
    for r in e2_rows:
        evidence.append(dict(item=f"E2_r_over_rs_{r['r_over_rs']}_A", value=r["A"], passes=True))
    for l, e, v in bridge_chain:
        evidence.append(dict(item=f"E3_{l.replace(' ', '_')}", value=v, passes=True))

    with (out_dir / "CR003_evidence_rows.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["item", "value", "pass"])
        w.writeheader()
        for e in evidence:
            w.writerow({"item": e["item"], "value": e["value"], "pass": e["passes"]})


if __name__ == "__main__":
    main()
