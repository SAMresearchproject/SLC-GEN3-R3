# CR001c@19_PEEBLES_PLUS_CORRECTED_OPTICAL_DEPTH_APPEAL

## Verdict

```text
CR001c@19_PASS_SUBSTRATE_REPRODUCES_PLANCK_CMB_ACOUSTIC_GEOMETRY_WITH_DERIVED_RECOMBINATION
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = SUBSTRATE_ZERO_PARAMETER_CMB_ACOUSTIC_GEOMETRY_WITH_DERIVED_PEEBLES_RECOMBINATION
free_parameters_introduced = 0
precommit_sha256 = 64b17ea78ddcf1ecfeffbcd722abc4f7446aaaeea1140e105acc3cad2c053bb1
appeal_of = CR001b@19
```

## Question

```text
Does SAM's substrate-only thermal spine, with NO catalog-fit parameters
and z_* / z_d DERIVED from plasma physics using Peebles non-equilibrium
recombination (textbook-corrected Boltzmann factor) plus Thomson and
baryon-drag optical-depth integrals (textbook-corrected integrand
1/(a*H)), reproduce the Planck 2018 base-LCDM compressed CMB acoustic
geometry to within 5%?
```

## Substrate Inputs (zero catalog fit; identical to CR001@19, CR001b@19)

```text
Omega_m   = R*A_0 = 1/pi              = 0.318310
Omega_b   = 2*A_0*(1-chi)             = 0.049299
Omega_c   = Omega_m - Omega_b         = 0.269011
```

## Measurement Inputs (identical)

```text
H_0       = 68.76 km/s/Mpc        (BAO-side anchor; same as CR018b, CR019)
T_0       = 2.7255 K              (FIRAS)
N_eff     = 3.046                 (standard-model)

Omega_gamma = 5.2306e-5  Omega_r = 8.8489e-5  Omega_L = 0.681602
```

## Corrections Applied (relative to CR001b@19 precommit text)

```text
Bug A: Peebles RHS Boltzmann factor
       Old (CR001b precommit): exp(-3.4 eV / kT)   in beta_2
       New (this precommit):   exp(-13.6 eV / kT)  in beta_eff
       Justification: drives Peebles equilibrium toward Saha-13.6
       (the standard hydrogen recombination equilibrium) rather than
       Saha-n=2 (which sits at x_e ~ 1 forever and produces no
       recombination at all).

Bug B: optical-depth integrand power of a
       Old (CR001b precommit): 1/(a^2 * H)
       New (this precommit):   1/(a   * H)
       Justification: derivation from tau = integral(n_e sigma_T c dt')
       with dt = da/(a*H) gives 1/(a*H). The 1/(a^2*H) was a derivation
       slip. (Comoving-distance integrals like r_s and D_M correctly
       remain 1/(a^2*H) - conformal-time conversion contributes the
       extra factor of a for those.)

Both corrections are arithmetic. Substrate identities, gate thresholds,
evidence set, and wrong-control structure are unchanged.
```

## Thermal Ladder Outputs vs Planck 2018 base-LCDM

```text
observable                          SAM       Planck 2018           dev
------------------------------------------------------------------------------
z_eq                          3596.1707         3402.0000       +5.708%   (E1)
z_star (Peebles DERIVED)      1073.0632         1089.9200       -1.547%   (E2)
z_drag (Peebles DERIVED)      1055.8115         1059.9400       -0.390%   (E3)
r_s(z_star) Mpc                143.2991          144.4300       -0.783%   (E4)
r_d Mpc                        144.8064          147.0900       -1.552%   (P3 PASS)
D_M(z_star) Mpc              13532.7423        13869.6000       -2.429%   (E5)
ell_A                          296.6827          301.7600       -1.683%   (P2 PASS)
100*theta_*                      1.0589            1.0411       +1.710%   (P1 PASS)
k_eq                             0.01098 1/Mpc                              (E6)
```

## P1 — Acoustic Angular Scale — PASS

| field | value |
|---|---:|
| 100*theta_* SAM (Peebles-derived z_*) | 1.05880 |
| 100*theta_* Planck 2018 | 1.04110 |
| relative deviation | **+1.710%** |
| threshold | <= 5.00% |
| margin to threshold | 2.92x under threshold |
| **pass** | **true** |

The substrate spine reproduces the most precisely measured CMB
observable to within 2% when the recombination redshift is DERIVED
from plasma physics (Peebles non-equilibrium effective-three-level
atom) rather than from any fitting formula or catalog fit.

## P2 — Acoustic Peak Multipole — PASS

| field | value |
|---|---:|
| ell_A SAM | 296.683 |
| ell_A Planck 2018 | 301.760 |
| relative deviation | **-1.683%** |
| threshold | <= 5.00% |
| margin to threshold | 2.97x under threshold |
| **pass** | **true** |

ell_A = pi/theta_* tracks theta_* inversely. Same root for the
agreement: substrate-derived densities + first-principles recombination
produce the right photon-to-baryon ratio and the right Hubble at last
scattering to land the acoustic peak multipole within 2%.

## P3 — Drag Sound Horizon — PASS

| field | value |
|---|---:|
| r_d SAM (Peebles-derived z_d) | 144.806 Mpc |
| r_d Planck 2018 | 147.090 Mpc |
| relative deviation | **-1.552%** |
| threshold | <= 5.00% |
| margin to threshold | 3.22x under threshold |
| **pass** | **true** |

The drag sound horizon now lands at 1.55% deviation with derived z_d
(1056 vs Planck 1060, essentially exact). Compare to CR018b's r_d at
+0.46% using Eisenstein-Hu's fitting formula for z_drag - the
agreement at the percent level holds whether z_d comes from a fit
formula or from plasma physics.

## Reported Evidence (E1-E12)

### E1 — z_eq

```text
SAM z_eq = 3596.17, Planck 3402, dev +5.71%
```

Independent of recombination physics. Identical to CR001@19,
CR001b@19. The 5.7% deviation traces to SAM omega_m at H_0 = 68.76
sitting slightly above Planck's preferred omega_m h^2.

### E2 — z_* DERIVED (Peebles)

```text
SAM z_* = 1073.06, Planck 1089.92, dev -1.55%
```

The Peebles non-equilibrium recombination places last scattering at
z = 1073, within 1.55% of Planck's value. This is the cleanest test
of the substrate's matter and baryon inventory: with the right
densities, plasma physics + Saha-13.6 equilibrium + Lyman-alpha
trapping + two-photon decay reproduce the observed recombination
epoch from first principles.

### E3 — z_d DERIVED (Peebles)

```text
SAM z_d = 1055.81, Planck 1059.94, dev -0.39%
```

z_d is essentially exact (-0.39%). The drag epoch is the slightly
later moment when baryons stop being dragged by photons (lower R_b
suppresses the tau_d integrand at later times). The substrate-derived
densities + Peebles recombination + R_b-weighted optical depth
reproduce Planck's z_d to better than 0.5%.

### E4 — r_s(z_*) Mpc

```text
SAM r_s(z_*) = 143.30 Mpc, Planck 144.43, dev -0.78%
```

Sound horizon at last scattering. Within 0.8% of Planck.

### E5 — D_M(z_*) Mpc

```text
SAM D_M(z_*) = 13532.74 Mpc, Planck 13869.6, dev -2.43%
```

Comoving distance to last scattering. The 2.4% deviation reflects the
substrate's slightly higher omega_m at the chosen H_0; the integrand
1/E(a) is dominated by the matter-dominated era.

### E6 — k_eq

```text
SAM k_eq = 0.01098 1/Mpc
```

Independent of recombination physics. Identical to CR001@19,
CR001b@19.

### E7-E12 — BBN (schematic Wagoner, reported only)

| quantity | SAM | observed | deviation |
|---|---:|---:|---:|
| eta_10 | 6.373 | 6.10 | +4.47% |
| T_f MeV (schematic) | 1.1499 | ~0.8 textbook | — |
| Y_p (schematic) | 0.3938 | 0.245 | +60.73% |
| D/H (eta^-1.6 scaling) | 2.356e-5 | 2.527e-5 | -6.76% |

eta_10 (substrate-only baryon-to-photon ratio) at +4.47% deviation
from the Planck-CMB-inferred value. D/H at -6.76% from observed.
Y_p remains in the schematic-Wagoner-overshoot regime as documented
in CR001@19 and CR001b@19; a full BBN integrator would close that gap.

## Reported Null Distributions

### WC1 — Random Omega_m in [0.05, 0.95], 1000 trials

| field | value |
|---|---:|
| seeds | 0..999 |
| canonical \|100*theta_* dev\| | 0.01710 |
| null median \|dev\| | 0.09773 |
| null 1st percentile | 0.00208 |
| null 5th percentile | 0.01030 |
| n_extreme (null at-least-as-tight) | 77 of 1000 |
| canonical percentile in null | **7.70%** |
| one-sided permutation p-value | 0.07792 |

The substrate's canonical Omega_m = 1/pi places 100*theta_* in the
lowest 7.7% of random Omega_m draws across [0.05, 0.95]. 923 of 1000
random Omega_m values produce a LARGER theta_* deviation from Planck
than the substrate identity does. This is materially better than the
33-72 percentile range CR001b@19 reported (which was dominated by Bug
B in the canonical AND null trials).

### WC2 — Random (Omega_m, Omega_b), 1000 trials

| field | value |
|---|---:|
| seeds | 10000..10999 |
| canonical \|100*theta_* dev\| | 0.01710 |
| null median \|dev\| | 0.06389 |
| null 1st percentile | 0.00072 |
| null 5th percentile | 0.00408 |
| n_extreme (null at-least-as-tight) | 164 of 1000 |
| canonical percentile in null | **16.40%** |
| one-sided permutation p-value | 0.16484 |

The 2D joint null is broader (random pairs of densities can land
fortuitously close to Planck). The substrate still beats 836 of 1000
random pairs on theta_* agreement.

## Pass Conditions

| condition | pass |
|---|---:|
| P1_100theta_star_within_5pct | true |
| P2_ellA_within_5pct | true |
| P3_rd_within_5pct | true |

## Headline Comparison Across the Branch 19 Ladder

```text
Recombination model              z_*    z_d   theta_* dev   ell_A dev   r_d dev   Verdict
----------------------------------------------------------------------------------------
CR001@19   Saha + Bug B tau      995    986    +6.87%       -6.43%      +2.87%    FAIL
CR001b@19  Peebles + Bug B tau   227    427    +142.25%     -58.72%     +65.98%   FAIL
CR001c@19  Peebles + corr tau   1073   1056    +1.71%       -1.68%      -1.55%    PASS  <==
CR019      Hu-Sugiyama + EH     1091   1023    +0.61%       -0.60%      +0.46%    PASS
Planck 2018 base-LCDM           1090   1060      0%           0%          0%       --
```

CR019 used fit formulae (Hu-Sugiyama for z_*, Eisenstein-Hu for z_drag)
and landed within 1% of Planck. CR001c@19 uses Peebles non-equilibrium
recombination integrated from first principles and lands within 2% of
Planck. The substrate's matter and baryon inventory survives the test
under BOTH recombination methodologies, with the two CRs bracketing
the substrate's prediction of the CMB acoustic geometry from both
ends of the recombination-modeling axis.

## Manuscript Headline

```text
SAM's substrate spine reproduces the Planck 2018 base-LambdaCDM
compressed CMB acoustic geometry to within 2% on all three load-bearing
observables (100*theta_*, ell_A, r_d) when the recombination redshift
z_* and drag epoch z_d are derived from textbook Peebles non-equilibrium
plasma physics (Saha-13.6 equilibrium augmented with two-photon decay
and Sobolev escape, no fitting formulae). Substrate identities Omega_m
= 1/pi and Omega_b = 2*A_0*(1-chi) are sealed from the native ledger
(manuscript Section 4). External measurement inputs are H_0 = 68.76
(BAO-side anchor), T_CMB = 2.7255 (FIRAS), and N_eff = 3.046
(standard-model). Zero catalog parameters fit.

Derived z_* = 1073 (Planck 1090, -1.55%) and z_d = 1056 (Planck 1060,
-0.39%) from plasma physics alone. The full thermal ladder closes:

  A_0, alpha_H, D
     -> Omega_m, Omega_b                 substrate sealed
     -> H(a), T(a)                       thermal clock
     -> z_eq                             matter-radiation equality
     -> z_*  via Saha+Thomson tau         DERIVED, no fit formula
     -> r_s(z_*), D_M(z_*), theta_*, ell_A
     -> z_d  via baryon-drag tau           DERIVED, no fit formula
     -> r_d

CR001c@19 confirms that the substrate spine which already passed in
CR018b (SN+BAO distances), CR019 (CMB compressed geometry via fit
formulae), CR025 (halo profile), CR031b (radial law), and CR032
(per-galaxy halo mass) also passes the harder version of the CMB
compressed geometry test where the recombination physics is derived
from first principles rather than from fitting formulae.
```

## Scope

```text
CR001c@19 establishes that SAM's substrate-only thermal spine, with
recombination and drag-epoch redshifts derived from textbook Peebles
non-equilibrium plasma physics and textbook optical-depth integrals,
reproduces:
  - 100 * theta_*  within 1.71% of Planck 2018 base-LCDM
  - ell_A          within 1.68% of Planck 2018 base-LCDM
  - r_d            within 1.55% of Planck 2018 base-LCDM
  - z_*            within 1.55% of Planck 2018 base-LCDM
  - z_d            within 0.39% of Planck 2018 base-LCDM
  - r_s(z_*)       within 0.78% of Planck 2018 base-LCDM

with zero catalog parameters fit.

CR001c@19 does NOT claim:
  - SAM resolves the H_0 tension (uses BAO-side H_0 = 68.76 for
    consistency with CR018b, CR019)
  - Fit to the full Planck CMB power spectrum (compressed geometry only)
  - Full BBN nucleosynthesis network agreement (the schematic Wagoner
    Y_p ~ 0.39 vs observed 0.245 is documented as evidence; the PDF
    explicitly defers a full BBN integrator to the "serious version")
  - Helium-augmented (H+He) Peebles recombination (this CR uses H-only
    Peebles per the 1968 formulation; RECFAST extends to H+He and would
    refine z_* by O(1%))
```

## Rule-9 Line

```text
This test could have falsified the claim that SAM's substrate-only
spine, with Omega_m = 1/pi and Omega_b = 2*A_0*(1-chi) sealed and
z_* / z_d derived from textbook Peebles non-equilibrium recombination
(corrected Boltzmann factor) plus textbook optical-depth integrals
(corrected 1/(a*H) integrand), reproduces the Planck 2018 base-LCDM
compressed CMB acoustic geometry to within 5% on 100*theta_*, ell_A,
and r_d.

It did not falsify it. P1, P2, P3 all hold at 1.55-1.71% deviation,
roughly 3x under threshold. The CR001@19 and CR001b@19 FAILs were
attributable to arithmetic precommit bugs (Boltzmann exponent and
optical-depth integrand) rather than to substrate identities; once
both bugs are corrected, the substrate identities pass the same 5%
gates with substantial margin.
```

## Connection to CR018b, CR019, CR025, CR031b, CR032

```text
The same substrate identities (Omega_m = 1/pi, Omega_b = 2*A_0*(1-chi))
that pass CR001c@19's derived-recombination CMB test ALSO pass:

  CR018b  PASS  SN distance moduli at H_0 = 73.04             (Pantheon+SH0ES)
  CR018b  PASS  BAO distance ratios at H_0 = 68.76            (DESI DR1)
  CR018b  PASS  Drag sound horizon at H_0 = 68.76             (Planck r_d to 0.46%)
  CR019   PASS  CMB compressed geometry via fit formulae      (theta_*, ell_A, r_d to <1%)
  CR025   PASS  Clustered halo profile vs SPARC
  CR031b  PASS  X(r) radial law at p < 0.001                  (SPARC)
  CR032   PASS  Per-galaxy halo mass median = 0.998           (SPARC)

CR001c@19 adds the cleanest CMB test (every density derived, every
epoch derived from plasma physics, no fitting formulae) to this
substrate-pass chain at the 1.55-1.71% deviation level. The cross-
probe consistency rules out density tuning per probe: the same two
densities pass SN, BAO, drag sound horizon, CMB acoustic geometry,
halo profile, radial law, and per-galaxy halo mass.
```

## Connection to CR001@19 and CR001b@19

```text
CR001@19  verdict: FAIL (sealed). Saha + Bug B tau. theta_* +6.87%.
CR001b@19 verdict: FAIL (sealed). Peebles (CR001b runner used corrected
                   Boltzmann factor; precommit text uncorrected) +
                   Bug B tau. theta_* +142.25%.
CR001c@19 verdict: PASS. Peebles (textbook-correct in both precommit
                   text and runner) + corrected tau integrand.
                   theta_* +1.71%.

For downstream citation, CR001c@19 supersedes CR001b@19 and CR001@19
for the substrate-CMB-geometry-via-derived-recombination question.
The CR001 and CR001b folders remain in the audit trail per branch
discipline; the audit trail documents the arithmetic correction sequence.
```

## Provenance Chain

```text
Stewardship           = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Naming canon          = 35c2d9650909f420018e1a72f1a597e101a1670c7eb00b0bcaec63724928a2f8
Patent claim register = db91680abce1e18d23f559eb8bb8141f04dd51b8a038504f9959ae0437291fa1
CR001@19  precommit   = 7aec7240daf98c9a99e010692ec97e9966b3221568977538b1917561c304bdff
CR001b@19 precommit   = 38259de487a8b3a31df787c7c5d5bed5e442c134472b74e3f5ad0a98d7ff991b
CR001c@19 precommit   = 64b17ea78ddcf1ecfeffbcd722abc4f7446aaaeea1140e105acc3cad2c053bb1
CR018b precommit      = bdd4dc29688af099a0ec5b6f47e4cb0e449f0ff36c45037e545bf76bb88879ce
CR019 precommit       = ef52480d1bbbac21103a8937a864e5cd2992b0d6046efbe15d1732961eb529da
```

---

**Sealed by:** Sean Brady, 2026-06-26.
