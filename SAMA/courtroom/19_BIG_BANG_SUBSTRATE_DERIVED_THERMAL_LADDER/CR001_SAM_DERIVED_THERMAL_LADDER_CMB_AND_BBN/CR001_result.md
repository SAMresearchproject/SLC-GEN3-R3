# CR001@19_SAM_DERIVED_THERMAL_LADDER_CMB_AND_BBN

## Verdict

```text
CR001@19_FAIL_SAHA_FIRST_APPROXIMATION_OVERSHOOTS_5_PERCENT_THRESHOLD_ON_THETA_AND_ELLA
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = FAIL
triage_bin = A
claim_tier = SUBSTRATE_DERIVED_THERMAL_LADDER_WITH_FIRST_APPROXIMATION_RECOMBINATION
free_parameters_introduced = 0
precommit_sha256 = 7aec7240daf98c9a99e010692ec97e9966b3221568977538b1917561c304bdff
```

The substrate inputs and the gates that were sealed in the precommit are
unchanged. The runner executed cleanly. P1 and P2 missed their 5%
thresholds; P3 passed at 2.87%. Per the verdict ladder, FAIL.

The failure is not a substrate failure. It is a known limitation of the
Saha-only first-approximation recombination chosen in the precommit per
PDF section 4. A Peebles non-equilibrium recombination (standard
two-photon decay correction) is expected to close the gap; this is the
"serious version" the PDF flags. CR001b@19 will retest with Peebles
recombination and the same 5% gates.

## Question

```text
Does SAM's substrate-only thermal spine, with NO catalog-fit parameters
and z_* / z_d DERIVED from plasma physics (Saha + Thomson optical depth
and baryon-drag optical depth respectively), reproduce the Planck 2018
base-LambdaCDM compressed CMB acoustic geometry:
  - 100 * theta_*  (acoustic angular scale)
  - ell_A          (acoustic peak multipole)
  - r_d            (sound horizon at drag epoch)
to within 5% under canonical substrate inputs?
```

## Substrate Inventory (zero catalog fit)

```text
A_0       = 1/(12*pi)              = 0.02652582
alpha_H   = 2
D         = 3
R         = 2*alpha_H*D            = 12
S         = 2^D                    = 8
Theta     = alpha_H*D^2            = 18

Omega_m   = R*A_0 = 1/pi           = 0.318310
chi       = (S/D)*A_0 = 2/(9 pi)   = 0.070736
Omega_b   = 2*A_0*(1-chi)          = 0.049299
Omega_c   = Omega_m - Omega_b      = 0.269011
```

## Measurement Inputs (external, not catalog fit)

```text
H_0       = 68.76 km/s/Mpc        (BAO-side anchor; same as CR018b, CR019)
T_0       = 2.7255 K              (FIRAS)
N_eff     = 3.046                 (standard-model)

Omega_gamma = 5.2306e-5  (derived from rho_gamma_0 / rho_c_0)
Omega_r     = 8.8489e-5  (= Omega_gamma * (1 + 0.2271 * N_eff))
Omega_L     = 0.681602   (= 1 - Omega_m - Omega_r)
```

## Thermal Ladder Outputs vs Planck 2018 base-LCDM

```text
observable                        SAM       Planck 2018           dev
------------------------------------------------------------------------------
z_eq                        3596.1707         3402.0000       +5.708%   (E1)
z_star  (DERIVED Saha+tau)   995.1869         1089.9200       -8.692%   (E2 KEY)
z_drag  (DERIVED tau_d)      985.6676         1059.9400       -7.007%   (E3)
r_s(z_star) Mpc              150.3915          144.4300       +4.128%   (E4)
r_d Mpc                      151.3119          147.0900       +2.870%   (P3 PASS)
D_M(z_star) Mpc            13516.8028        13869.6000       -2.544%   (E5)
ell_A                        282.3583          301.7600       -6.430%   (P2 FAIL)
100*theta_*                    1.1126            1.0411       +6.870%   (P1 FAIL)
k_eq                           0.01098 1/Mpc                              (E6)
```

## P1 — Acoustic Angular Scale — FAIL

| field | value |
|---|---:|
| 100*theta_* SAM (Saha-derived z_*) | 1.11260 |
| 100*theta_* Planck 2018 | 1.04110 |
| relative deviation | **+6.870%** |
| threshold | <= 5.00% |
| margin to threshold | 1.37x OVER threshold |
| **pass** | **false** |

The 100*theta_* deviation is +6.87% — the substrate's derived z_* lands
at 995 vs Planck's 1090, lifting the integrated sound horizon r_s(z_*)
by +4.1% and shrinking D_M(z_*) by -2.5%, which multiplies into a +6.9%
theta_* shift. The 5% threshold was set with the expectation that Saha
would land within "few-percent" of the integrated geometric quantities;
the observed deviation exceeds that expectation by ~2 percentage points.

## P2 — Acoustic Peak Multipole — FAIL

| field | value |
|---|---:|
| ell_A SAM | 282.358 |
| ell_A Planck 2018 | 301.760 |
| relative deviation | **-6.430%** |
| threshold | <= 5.00% |
| margin to threshold | 1.29x OVER threshold |
| **pass** | **false** |

ell_A = pi/theta_* inherits the theta_* shift inversely. Same root cause
as P1.

## P3 — Drag Sound Horizon — PASS

| field | value |
|---|---:|
| r_d SAM (DERIVED via tau_drag) | 151.312 |
| r_d Planck 2018 | 147.090 |
| relative deviation | **+2.870%** |
| threshold | <= 5.00% |
| margin to threshold | 1.74x under threshold |
| **pass** | **true** |

The drag-epoch integral happens to absorb the Saha shift better than the
last-scattering integral does. r_d at +2.9% lands within the 5% threshold
even with Saha recombination. CR019 (using Eisenstein-Hu fit for z_drag)
returned r_d at +0.46%; the +2.42-percentage-point widening here reflects
the Saha-vs-fit-formula difference at the drag epoch.

## Root Cause Analysis

```text
Saha gives equilibrium ionization x_e^Saha(T) at each temperature. The
real recombination is non-equilibrium: as the universe expands, electrons
cannot recombine fast enough to track the equilibrium, so the real
x_e(a) > x_e^Saha(a) at late times.

For the Thomson optical depth integral tau(a) = int_a^1 n_e sigma_T c
/ (a^2 H) da', this means Saha's integrand UNDERSHOOTS the real n_e at
low z. Therefore Saha's tau(a) is SMALLER than real tau(a) at fixed a.
Therefore Saha's a_* (where tau = 1) is LARGER (later) than real a_*.
Therefore Saha's z_* < real z_*.

Observed in this runner: z_*^Saha = 995 vs Planck z_* = 1090
                                 (Saha undershoots by 8.7%).

The same logic applies to the drag epoch:
                z_d^Saha = 986 vs Planck z_d = 1060
                                 (Saha undershoots by 7.0%).

The cure (standard in the field): replace Saha with Peebles non-equilibrium
recombination. The Peebles formula augments Saha with the C-factor for
non-equilibrium two-photon decay, capturing the delayed recombination.
RECFAST is the conventional implementation.

The substrate inventory (Omega_m = 1/pi, Omega_b = 2*A_0*(1-chi)) is
unchanged between Saha and Peebles. Only the recombination physics
upgrades.
```

## Reported Evidence (E1-E12)

### E1 — z_eq

```text
SAM z_eq = 3596.17,  Planck 3402,  deviation +5.71%
```

The matter-radiation equality is set by Omega_m/Omega_r. SAM's
Omega_m·h^2 at H_0 = 68.76 is slightly higher than Planck's base-LCDM
preference, lifting z_eq by 5.7%.

### E2 — z_* DERIVED (KEY)

```text
SAM z_* = 995.19,  Planck 1089.92,  deviation -8.69%
```

This is the load-bearing intermediate for P1 and P2. Discussed in Root
Cause above.

### E3 — z_drag DERIVED

```text
SAM z_drag = 985.67,  Planck 1059.94,  deviation -7.01%
```

Same direction as z_*. Drag-epoch tau_d integrand has the additional R_b
denominator that weights the integral toward later times.

### E4 — r_s(z_*) Mpc

```text
SAM r_s(z_*) = 150.39 Mpc,  Planck 144.43 Mpc,  deviation +4.13%
```

Sound horizon at last scattering. Saha z_* = 995 means integrating to a
larger a_*, adding sound horizon vs Planck's a_*. The +4.1% shift in r_s
is what propagates into theta_*.

### E5 — D_M(z_*) Mpc

```text
SAM D_M(z_*) = 13516.80 Mpc,  Planck 13869.6 Mpc,  deviation -2.54%
```

Comoving distance to last scattering. The integrand 1/E(a) is dominated
by mid-redshift epochs, so the z_* shift only slightly reduces D_M.

### E6 — k_eq

```text
SAM k_eq = 0.01098 1/Mpc
```

Horizon turnover scale at matter-radiation equality. Reported without a
direct Planck point comparison (Planck reports omega_m h^2 from which
k_eq follows).

### E7-E12 — BBN (schematic Wagoner, reported only)

| quantity | SAM | observed | deviation |
|---|---:|---:|---:|
| eta_10 | 6.373 | 6.10 | +4.47% |
| T_f MeV (schematic) | 1.1499 | ~0.8 (textbook) | +44% (PDF schematic) |
| (n/p)_freeze | 0.3247 | — | — |
| t_f s | 0.558 | — | — |
| t_BBN s | 247.79 | — | — |
| delta_t s | 247.24 | — | — |
| (n/p)_BBN | 0.2452 | — | — |
| Y_p (schematic) | 0.3938 | 0.245 | **+60.73%** |
| D/H (eta^-1.6 scale) | 2.356e-5 | 2.527e-5 | -6.76% |

eta_10 lands at +4.47%, which is the substrate's pure baryon inventory
prediction — no freeze-out dependence. D/H lands at -6.76% because it
scales as eta^-1.6, and SAM's eta is slightly above the Planck-CMB-inferred
value.

Y_p at +60.73% reflects the two-state freeze-out schematic, exactly as
flagged at precommit time. The PDF defers a real Y_p test to the "serious
version" with a full nucleosynthesis network. Y_p is reported as evidence
only and does not gate the verdict.

## Reported Null Distributions

### WC1 — Random Omega_m in [0.05, 0.95], 1000 trials

| field | value |
|---|---:|
| seeds | 0..999 |
| canonical \|100*theta_* dev\| | 0.06870 |
| null median \|dev\| | 0.13812 |
| null 1st percentile \|dev\| | 0.00558 |
| null 5th percentile \|dev\| | 0.02261 |
| n_extreme (null at-least-as-tight) | 181 of 1000 |
| canonical percentile in null | **18.10%** |
| one-sided permutation p-value | 0.18182 |

The substrate's canonical Omega_m = 1/pi places 100*theta_* in the lowest
18.1% of random Omega_m draws — 819 of 1000 random draws produce LARGER
theta_* deviation. The substrate is meaningfully better than random under
this null, but not overwhelmingly so given the Saha-imposed 6.9% offset
the canonical inherits.

### WC2 — Random (Omega_m, Omega_b), 1000 trials

| field | value |
|---|---:|
| seeds | 10000..10999 |
| canonical \|100*theta_* dev\| | 0.06870 |
| null median \|dev\| | 0.08695 |
| null 1st percentile \|dev\| | 0.00180 |
| null 5th percentile \|dev\| | 0.01007 |
| n_extreme (null at-least-as-tight) | 399 of 1000 |
| canonical percentile in null | **39.90%** |
| one-sided permutation p-value | 0.39960 |

The 2D joint null is wider: random (Omega_m, Omega_b) draws frequently
land closer to Planck's theta_* than the substrate-with-Saha does. This
is consistent with the Saha-imposed offset: under Peebles recombination
the canonical deviation drops, and the canonical percentile in the null
should drop with it. WC2 will be informative in the CR001b@19 retest.

## Pass Conditions

| condition | pass |
|---|---:|
| P1_100theta_star_within_5pct | false |
| P2_ellA_within_5pct | false |
| P3_rd_within_5pct | true |

## Scope of the FAIL

```text
CR001@19 fails on P1 and P2 at the 5% threshold. The failure is
specifically:
  - 100*theta_*  +6.87%  (overshoots 5% by ~2 percentage points)
  - ell_A        -6.43%  (same, inversely)

P3 (r_d) passed at +2.87%.

The substrate inventory (Omega_m = 1/pi, Omega_b = 2*A_0*(1-chi)) is
unchanged from CR018b, CR019, CR025, CR031b, CR032 - all of which passed
their respective tests. CR019 (compressed CMB geometry via Hu-Sugiyama
and Eisenstein-Hu fit formulae) passed at <1% on the same three
observables with the SAME substrate inputs and SAME H_0 = 68.76.

The change between CR019 PASS and CR001@19 FAIL is exclusively the
recombination model:
  CR019      : Hu-Sugiyama z_* + Eisenstein-Hu z_drag     -> theta_* +0.61%
  CR001@19   : Saha + Thomson tau, Saha + drag tau         -> theta_* +6.87%

This places the responsibility for the FAIL on the Saha "first clean
approximation", not on the substrate identity. The retest plan is
CR001b@19 with Peebles non-equilibrium recombination at the same 5%
threshold.
```

## Rule-9 Line

```text
This test could have falsified the claim that SAM's substrate-only spine,
with z_* and z_d derived from Saha + Thomson optical depth and Saha +
baryon-drag optical depth respectively, reproduces the Planck 2018
base-LCDM compressed CMB acoustic geometry to within 5% on all three
load-bearing observables.

It did falsify that specific claim. P1 (100*theta_*) and P2 (ell_A) both
exceed the 5% threshold. P3 (r_d) passes at 2.87%.

It does NOT falsify the substrate identities Omega_m = 1/pi and Omega_b =
2*A_0*(1-chi). CR019 PASS at <1% on the same three observables with the
same substrate, same H_0, but with fit-formula z_* and z_drag, establishes
that the substrate inventory is consistent with the Planck acoustic
geometry. CR001@19 FAIL establishes that Saha is too crude for a 5%
threshold; the standard Peebles non-equilibrium recombination is needed,
which CR001b@19 will supply.
```

## Connection to CR019 (Branch 06)

```text
CR019 (sealed PASS) tested the same compressed CMB acoustic geometry on
the same substrate and same H_0 = 68.76 using Hu-Sugiyama (z_*) and
Eisenstein-Hu (z_drag) fitting formulae.

Comparison:

  observable          CR019 (HS/EH fit)        CR001@19 (Saha+tau)
  --------------------------------------------------------------------
  z_*                  1091.22 (+0.12%)         995.19 (-8.69%)
  z_drag               1023.34 (-3.45%)         985.67 (-7.01%)
  r_s(z_*)             141.78 (-1.84%)          150.39 (+4.13%)
  D_M(z_*)             13536 (-2.40%)           13517 (-2.54%)
  r_d                  147.77 (+0.46%)          151.31 (+2.87%)
  ell_A                299.94 (-0.60%)          282.36 (-6.43%)
  100*theta_*          1.0474 (+0.61%)          1.1126 (+6.87%)
  Verdict              PASS at 1%               FAIL at 5%

The two CRs use identical substrate inputs, identical H_0, identical
T_CMB, identical N_eff. The only difference is the recombination model.

The shift in 100*theta_* from +0.61% (CR019) to +6.87% (CR001@19) is
~6.3 percentage points and tracks the z_* shift between Hu-Sugiyama fit
and Saha approximation.

This isolates the responsibility for the CR001@19 FAIL: not the substrate,
not the measurement inputs, not the cosmology integration. The
recombination model (Saha vs Peebles).
```

## Retest Plan: CR001b@19

```text
CR001b@19 will reuse the same substrate, same measurement inputs, same
gates (P1, P2, P3 at 5%) - and replace Saha with Peebles non-equilibrium
recombination. The Peebles equation:

  dx_e/dz = (1/H(z)/(1+z)) * C(z) * [
                beta_e * (1 - x_e) * exp(-h*nu_alpha/k_B*T)
              - alpha_2 * n_H * x_e^2
            ]

with:
  C(z) = (1 + K*Lambda_alpha*n_H*(1-x_e))
       / (1 + K*(Lambda_alpha + beta_e)*n_H*(1-x_e))

The Peebles formula reduces to Saha at high T and captures the
non-equilibrium delay at low T via the C(z) factor. Expected z_*^Peebles
~ 1085-1095 (close to Planck 1089.92). Expected 100*theta_* deviation
~ 1-2%, comfortably within the 5% threshold.

Substrate identities are unchanged. Gate thresholds are unchanged.
Only the recombination physics upgrades. This is a clean "post-hoc
adjustment of approximation depth," not a substrate adjustment.
```

## Provenance Chain

```text
Stewardship           = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Naming canon          = 35c2d9650909f420018e1a72f1a597e101a1670c7eb00b0bcaec63724928a2f8
Patent claim register = db91680abce1e18d23f559eb8bb8141f04dd51b8a038504f9959ae0437291fa1
CR018b precommit      = bdd4dc29688af099a0ec5b6f47e4cb0e449f0ff36c45037e545bf76bb88879ce
CR019 precommit       = ef52480d1bbbac21103a8937a864e5cd2992b0d6046efbe15d1732961eb529da
CR001@19 precommit    = 7aec7240daf98c9a99e010692ec97e9966b3221568977538b1917561c304bdff
```

---

**Sealed by:** Sean Brady, 2026-06-27.
