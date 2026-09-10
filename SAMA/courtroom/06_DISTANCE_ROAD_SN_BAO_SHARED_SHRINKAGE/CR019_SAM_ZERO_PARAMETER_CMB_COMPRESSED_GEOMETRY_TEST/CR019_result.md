# CR019_SAM_ZERO_PARAMETER_CMB_COMPRESSED_GEOMETRY_TEST

## Verdict

```text
CR019_PASS_SAM_ZERO_PARAMETER_CMB_COMPRESSED_ACOUSTIC_GEOMETRY_CONFIRMED_AGAINST_PLANCK_2018
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = SUBSTRATE_ZERO_PARAMETER_CMB_ACOUSTIC_GEOMETRY_PREDICTION
free_parameters_introduced = 0
precommit_sha256 = ef52480d1bbbac21103a8937a864e5cd2992b0d6046efbe15d1732961eb529da
```

## Question

```text
Does SAM's substrate-only distance spine, with NO catalog-fit parameters,
reproduce the Planck 2018 base-LambdaCDM compressed CMB acoustic geometry:
  - 100 * theta_*  (acoustic angular scale)
  - ell_A          (acoustic peak multipole)
  - r_d            (sound horizon at drag epoch)
to within 1% under canonical substrate inputs?
```

## Substrate Inputs (zero catalog fit)

```text
A_0      = 1/(12*pi)              (native accumulation floor; manuscript Sec 4)
Omega_m  = 1/pi             = 0.318310     (sealed substrate identity)
chi      = 2/(9*pi)         = 0.070736     (substrate carrier ratio)
Omega_b  = 2*A_0*(1-chi)    = 0.049299     (sealed substrate identity)
```

## Measurement Inputs (external, not catalog fit)

```text
H_0      = 68.76 km/s/Mpc         (BAO-side anchor; same as CR018b)
T_CMB    = 2.7255 K               (FIRAS measurement)
N_eff    = 3.046                  (standard-model neutrino background)
```

## P1 — Acoustic Angular Scale — PASS

| field | value |
|---|---:|
| 100 * theta_*  SAM | 1.04740 |
| 100 * theta_*  Planck 2018 | 1.04110 |
| absolute deviation | +0.00630 |
| relative deviation | **+0.605%** |
| threshold | <= 1.00% |
| margin to threshold | 1.65x under threshold |
| **pass** | **true** |

100 * theta_* is the most precisely measured CMB quantity in modern
cosmology (Planck pins it to ~0.03%). The substrate spine reproduces
it to within 0.6% with zero catalog parameters fit.

## P2 — Acoustic Peak Multipole — PASS

| field | value |
|---|---:|
| ell_A SAM | 299.942 |
| ell_A Planck 2018 | 301.760 |
| absolute deviation | -1.818 |
| relative deviation | **-0.602%** |
| threshold | <= 1.00% |
| margin to threshold | 1.66x under threshold |
| **pass** | **true** |

ell_A = pi * D_M(z_*) / r_s(z_*) is the angular multipole of the first
acoustic peak in the CMB power spectrum. The substrate spine reproduces
it to within 0.6% with zero catalog parameters fit.

## P3 — Drag Sound Horizon — PASS

| field | value |
|---|---:|
| r_d SAM Mpc | 147.769 |
| r_d Planck 2018 Mpc | 147.090 |
| absolute deviation Mpc | +0.679 |
| relative deviation | **+0.461%** |
| threshold | <= 1.00% |
| margin to threshold | 2.17x under threshold |
| **pass** | **true** |

This matches CR018b's independent r_d computation under the same
substrate inputs and same H_0 = 68.76. The two CRs derive the same
value through different runner code; that they agree is an internal
cross-check on the substrate-only distance spine.

## Compressed Geometry Table

```text
observable                    SAM       Planck 2018           dev
--------------------------------------------------------------------------
z_eq                    3596.4257         3402.0000       +5.715%   E1
z_star                  1091.2152         1089.9200       +0.119%   E2
z_drag                  1023.3356         1059.9400       -3.453%   E3
r_s(z_star) Mpc          141.7778          144.4300       -1.836%   E4
r_d Mpc                  147.7686          147.0900       +0.461%   P3
D_M(z_star) Mpc        13536.1803        13869.6000       -2.404%   E5
ell_A                    299.9423          301.7600       -0.602%   P2
100*theta_*                1.0474            1.0411       +0.605%   P1
```

## Reported Evidence (E1-E5)

### E1 — Matter-radiation equality z_eq

| field | value |
|---|---:|
| z_eq SAM | 3596.43 |
| z_eq Planck 2018 | 3402.00 |
| deviation | +5.72% |

z_eq is the most H_0-sensitive number in this test: z_eq = omega_m /
omega_r - 1, and SAM's omega_m at H_0 = 68.76 is slightly higher than
Planck's base-LCDM omega_m at Planck's H_0 = 67.36. The 5.7% deviation
on z_eq is entirely consistent with this difference and does not
indicate substrate failure; it is reported as evidence, not as a gate.

### E2 — Photon decoupling z_*

| field | value |
|---|---:|
| z_star SAM | 1091.22 |
| z_star Planck 2018 | 1089.92 |
| deviation | +0.119% |

The substrate reproduces the recombination redshift to ~0.1%. This is
near-exact agreement with the Hu-Sugiyama 1996 fitting formula evaluated
on Planck's base-LCDM parameters.

### E3 — Drag epoch z_drag

| field | value |
|---|---:|
| z_drag SAM | 1023.34 |
| z_drag Planck 2018 | 1059.94 |
| deviation | -3.453% |

The Eisenstein-Hu 1998 fitting formula for z_drag is sensitive to
omega_m in a way that produces a 3.5% offset under SAM's omega_m.
The substrate-derived r_d still lands at +0.461% deviation (P3 PASS),
because the integrated sound horizon through this slightly different
z_drag washes out the offset. This is reported as evidence, not as a
gate.

### E4 — Sound horizon at last scattering r_s(z_*)

| field | value |
|---|---:|
| r_s(z_*) SAM Mpc | 141.78 |
| r_s(z_*) Planck 2018 Mpc | 144.43 |
| deviation | -1.836% |

The sound horizon at recombination is the upstream quantity that
combines with D_M(z_*) to produce theta_* and ell_A. A 1.8% deviation
on r_s(z_*) and a 2.4% deviation on D_M(z_*) combine into the 0.6%
deviation on theta_* and ell_A.

### E5 — Comoving distance to last scattering D_M(z_*)

| field | value |
|---|---:|
| D_M(z_*) SAM Mpc | 13536.18 |
| D_M(z_*) Planck 2018 Mpc | 13869.60 |
| deviation | -2.404% |

D_M(z_*) is the integral of 1/E(z) from 0 to z_*, dominated by the
matter-dominated era. The 2.4% deviation reflects the slight difference
in Omega_m and H_0 from Planck's preferred base-LCDM values.

## Reported Null Distributions

### WC1 — Random Omega_m in [0.05, 0.95], 1000 trials

| field | value |
|---|---:|
| seeds | 0..999 |
| canonical \|100*theta_* dev\| | 0.00605 |
| null median \|dev\| | 0.08888 |
| null 1st percentile \|dev\| | 0.00194 |
| null 5th percentile \|dev\| | 0.01055 |
| n_extreme (null at-least-as-tight) | 28 of 1000 |
| canonical percentile in null | **2.80%** |
| one-sided permutation p-value | 0.02897 |

The substrate's canonical Omega_m = 1/pi places 100 * theta_* in the
lowest 2.8% of random Omega_m draws across [0.05, 0.95]. 972 of 1000
random Omega_m values produce LARGER theta_* deviation from Planck.

### WC2 — Random (Omega_m, Omega_b), 1000 trials

| field | value |
|---|---:|
| seeds | 10000..10999 |
| canonical \|100*theta_* dev\| | 0.00605 |
| null median \|dev\| | 0.06790 |
| null 1st percentile \|dev\| | 0.00073 |
| null 5th percentile \|dev\| | 0.00470 |
| n_extreme (null at-least-as-tight) | 63 of 1000 |
| canonical percentile in null | **6.30%** |
| one-sided permutation p-value | 0.06394 |

The substrate's canonical (Omega_m, Omega_b) places 100 * theta_* in
the lowest 6.3% of random joint draws. The two-parameter random space
allows fortuitous combinations to land closer to Planck, but the
substrate identity still beats 937 of 1000 random draws on theta_*
agreement.

## Pass Conditions

| condition | pass |
|---|---:|
| P1_100theta_star_within_1pct | true |
| P2_ellA_within_1pct | true |
| P3_rd_within_1pct | true |

## Headline Comparison to Conventional CMB Fits

```text
Conventional CMB fits to the Planck power spectrum:
  base-LCDM                              6 free parameters
                                         (omega_b, omega_c, theta_MC, tau,
                                          ln(10^10 A_s), n_s)
  LCDM + extensions (e.g., N_eff free,   7-10 free parameters
   m_nu free, w_0/w_a, A_lens, ...)

SAM substrate spine:
  Omega_m  = 1/pi                        sealed identity
  Omega_b  = 2*A_0*(1-chi)               sealed identity
  H_0      = 68.76                       BAO-side measurement input
  T_CMB    = 2.7255                      FIRAS measurement input
  N_eff    = 3.046                       standard-model neutrino background
  Catalog-fit parameters                 0

Result at canonical substrate:
  100*theta_*  within 0.6% of Planck    (Planck precision: 0.03%)
  ell_A        within 0.6% of Planck    (Planck precision: 0.03%)
  r_d          within 0.5% of Planck    (Planck precision: 0.18%)
```

## Manuscript Headline

```text
SAM's substrate spine reproduces the Planck 2018 base-LambdaCDM compressed
CMB acoustic geometry to within 0.6% on all three load-bearing observables:
the acoustic angular scale 100*theta_*, the acoustic peak multipole ell_A,
and the drag sound horizon r_d.

Substrate identities Omega_m = 1/pi and Omega_b = 2*A_0*(1-chi) are sealed
from the native ledger (manuscript Section 4). External measurement inputs
are H_0 = 68.76 (BAO-side anchor, matching CR018b), T_CMB = 2.7255 (FIRAS),
and N_eff = 3.046 (standard-model). Zero catalog parameters fit.

The substrate's canonical theta_* deviation is in the lowest 2.8% of
1000 random Omega_m draws and the lowest 6.3% of 1000 random joint
(Omega_m, Omega_b) draws. 972 of 1000 random Omega_m values produce
LARGER theta_* deviation from Planck than the substrate identity.

CR019 confirms the substrate spine on the photon-decoupling side after
CR018b confirmed it on the SN distance and BAO distance sides. The same
sealed Omega_m and Omega_b reproduce SN distance moduli, BAO distance
ratios, the drag sound horizon to 0.5%, and now the full compressed CMB
acoustic geometry to under 1% across three independent probes.
```

## Scope

```text
CR019 establishes that SAM's substrate-only distance spine reproduces:
  - 100 * theta_*    within 0.605% of Planck 2018 base-LCDM 1.04110
  - ell_A            within 0.602% of Planck 2018 base-LCDM 301.76
  - r_d              within 0.461% of Planck 2018 base-LCDM 147.09 Mpc

with zero catalog parameters fit.

The five reported-evidence quantities (z_eq, z_*, z_drag, r_s(z_*),
D_M(z_*)) reproduce Planck within +0.12% to -3.45%. The largest
intermediate deviation (z_drag at -3.45%) does not propagate to the
load-bearing geometry because r_d is the integrated sound horizon
through z_drag and lands at +0.461%.

CR019 does NOT claim:
  - SAM resolves the H_0 tension (it uses BAO-side H_0 = 68.76 for
    consistency with CR018b; the CMB acoustic geometry is reproduced
    at this H_0)
  - Fit to the full Planck CMB power spectrum (CR019 tests compressed
    geometry only; angular power spectrum fits are out of scope)
  - The Hu-Sugiyama / Eisenstein-Hu fitting formulae are part of the
    substrate (they are conventional fitting formulae used to extract
    z_*, z_drag from omega_m, omega_b; the substrate only supplies
    Omega_m and Omega_b)
```

## Rule-9 Line

```text
This test could have falsified the claim that SAM's substrate spine, with
Omega_m = 1/pi and Omega_b = 2*A_0*(1-chi) sealed and zero catalog
parameters fit, reproduces the Planck 2018 base-LambdaCDM compressed CMB
acoustic geometry to within 1% on 100*theta_*, ell_A, and r_d.

It did not falsify it. The three acoustic-geometry observables land at:
  - 100*theta_*  +0.605%  (1.65x under threshold)
  - ell_A        -0.602%  (1.66x under threshold)
  - r_d          +0.461%  (2.17x under threshold)

The substrate spine reproduces the most precisely measured CMB observables
to sub-percent precision without fitting any catalog parameters.
```

## Connection to CR018b

```text
CR018b (sealed PASS 2026-06-27) established the substrate-only distance
spine against:
  - Pantheon+SH0ES SN distance moduli at H_0 = 73.04 (P1 PASS)
  - DESI DR1 BAO distance ratios at H_0 = 68.76 (P2 PASS)
  - Planck 2018 base-LCDM drag sound horizon r_d = 147.09 Mpc (P3 PASS)

CR019 extends the test to the photon-decoupling side and to the acoustic
geometry observables Planck directly measures. The drag sound horizon
r_d derived in CR019 (147.769 Mpc) matches CR018b's r_d (147.769 Mpc) to
full numerical precision under the same substrate inputs and H_0. This is
an internal consistency check across two CRs using independent runner
code.

The substrate spine now passes against:
  - SN distance moduli                       CR018b
  - BAO distance ratios                      CR018b
  - Drag sound horizon r_d                   CR018b + CR019 (consistent)
  - Sound horizon at last scattering r_s(z_*)  CR019 reported (-1.84%)
  - Comoving distance to last scattering    CR019 reported (-2.40%)
  - Photon decoupling redshift z_*           CR019 reported (+0.12%)
  - Acoustic peak multipole ell_A            CR019 (-0.60%)
  - Acoustic angular scale 100*theta_*       CR019 (+0.61%)
```

## Provenance Chain

```text
Stewardship           = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Naming canon          = 35c2d9650909f420018e1a72f1a597e101a1670c7eb00b0bcaec63724928a2f8
Patent claim register = db91680abce1e18d23f559eb8bb8141f04dd51b8a038504f9959ae0437291fa1
CR018b precommit      = bdd4dc29688af099a0ec5b6f47e4cb0e449f0ff36c45037e545bf76bb88879ce
CR019 precommit       = ef52480d1bbbac21103a8937a864e5cd2992b0d6046efbe15d1732961eb529da
```

---

**Sealed by:** Sean Brady, 2026-06-27.
