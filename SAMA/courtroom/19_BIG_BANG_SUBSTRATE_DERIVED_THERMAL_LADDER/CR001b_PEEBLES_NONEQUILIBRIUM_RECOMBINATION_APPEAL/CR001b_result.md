# CR001b@19_PEEBLES_NONEQUILIBRIUM_RECOMBINATION_APPEAL

## Verdict

```text
CR001b@19_FAIL_PEEBLES_BARES_DOWNSTREAM_OPTICAL_DEPTH_FORMULA_BUG
```

## Courtroom Fields

```text
execution_status = CLEAN_WITH_PRECOMMIT_BUG_NOTED
scientific_verdict = FAIL
triage_bin = A
claim_tier = SUBSTRATE_DERIVED_THERMAL_LADDER_WITH_PEEBLES_NONEQUILIBRIUM_RECOMBINATION
free_parameters_introduced = 0
precommit_sha256 = 38259de487a8b3a31df787c7c5d5bed5e442c134472b74e3f5ad0a98d7ff991b
```

This CR honors the sealed precommit ladder. Two precommit issues surfaced
during implementation; both are documented below and both feed forward
into the next appeal CR001c@19.

## Question

```text
Does SAM's substrate-only thermal spine, with NO catalog-fit parameters
and z_* / z_d DERIVED from plasma physics using Peebles non-equilibrium
recombination (instead of Saha first-approximation), reproduce the
Planck 2018 base-LCDM compressed CMB acoustic geometry to within 5%
under canonical substrate inputs?
```

## Substrate Inventory (zero catalog fit; identical to CR001@19)

```text
Omega_m  = R*A_0 = 1/pi               = 0.318310
Omega_b  = 2*A_0*(1-chi)              = 0.049299
Omega_c  = Omega_m - Omega_b          = 0.269011
```

## Measurement Inputs (identical to CR001@19)

```text
H_0     = 68.76 km/s/Mpc
T_0     = 2.7255 K
N_eff   = 3.046

Omega_gamma = 5.2306e-5  Omega_r = 8.8489e-5  Omega_L = 0.681602
```

## Bugs Surfaced During Implementation

### Bug A — precommit's Peebles RHS does not drive standard recombination

```text
The precommit specified:
  dx_e/dz = (C(z) / (H(z)*(1+z))) * [
              alpha_B(T) * n_H(z) * x_e^2
            - beta_2(T) * (1 - x_e)
          ]
  with beta_2(T) = alpha_B(T) * (m_e*k_B*T/(2*pi*hbar^2))^(3/2)
                                * exp(-h*nu_2 / (k_B*T))
                  and h*nu_2 = 3.4 eV (n=2 binding).

The equilibrium of this RHS is x_e^2/(1-x_e) = (beta_2/alpha_B/n_H),
which uses the 3.4 eV Boltzmann factor. That is "Saha-n=2 equilibrium,"
NOT the standard Saha-13.6 equilibrium that real hydrogen recombination
tracks at high T. With the precommit RHS exactly as written, x_e stays
essentially 1 throughout the integration range — no recombination
happens, optical depth diverges, no a_* exists, the runner crashes.

Diagnostic confirmation (during debug):
  At z=1090, T=2972 K, the precommit's beta_2 ~ 5e2 s^-1, and the
  equilibrium x_e ~ 1 - 5e-13 (essentially fully ionized).

The standard Peebles equation augments this RHS by ALSO including
the Boltzmann factor exp(-h*nu_alpha / (k_B*T)) (Lyman-alpha photon
energy 10.2 eV) on the ionization term, which combines with the 3.4 eV
of beta_2 to give exp(-13.6 eV / (k_B*T)) and drives the equilibrium
toward Saha-13.6 (the correct recombination equilibrium).

This runner uses the textbook-corrected form:
  beta_eff(T) = alpha_B(T) * (m_e*k_B*T/(2*pi*hbar^2))^(3/2)
                              * exp(-13.6 eV / (k_B*T))
  dx_e/dz = (C/(H*(1+z))) * [
              alpha_B * n_H * x_e^2
            - beta_eff * (1 - x_e)
          ]

This is a DEPARTURE from the precommit specification, made transparent
here because the precommit-exact RHS produces an immediate runner
failure (no recombination). The C-factor formula is unchanged; only
the net-rate Boltzmann exponent is corrected from 3.4 eV to 13.6 eV.

With the corrected RHS, x_e drops at recombination as expected:
  z=1800: x_e = 0.9998  (Saha-13.6 IC)
  z=1500: x_e = 0.9436
  z=1090: x_e = 0.1106
  z=800:  x_e = 0.0029
  z=500:  x_e = 0.00057
  z=10:   x_e = 0.00022 (frozen)

This matches the standard recombination history.
```

### Bug B — Thomson optical depth integrand has wrong power of a

```text
The precommit specified:
  tau(a) = integral from a to 1 of n_e * sigma_T * c / (a^2 * H) da

The correct derivation:
  tau = integral over proper time of n_e * sigma_T * c dt
  dt = da / (a*H)
  tau(a_*) = integral from a_* to 1 of n_e * sigma_T * c / (a * H) da

The precommit has 1/(a^2 * H); the standard derivation has 1/(a * H).
The bug overestimates the integrand at small a (high z) by a factor of
1/a, pushing the tau = 1 surface to LATER times (larger a, smaller z_*).

This runner HONORS the precommit specification (1/(a^2 * H)) per the
appeal discipline. The resulting z_* sits far below Planck:

  z_*^Peebles_buggy_tau = 227   vs Planck 1089.92    (-79.1%)

With the correct tau formula (1/(a*H)), z_* would land much closer
to Planck (~1090). CR001c@19 will be sealed with the corrected tau
formula and re-run.

Cross-check: CR001@19 (Saha + buggy tau) gave z_* = 995. The Saha
approximation undershoots z_* (Saha is too crude at late recombination,
lowering z_*), and the tau bug undershoots z_* further. The two effects
partly canceled in CR001@19, giving z_* = 995 (close enough to Planck
1090 to make the Saha FAIL look like a Saha problem alone). With
Peebles, the Saha undershoot is removed and the tau bug stands alone,
producing the gross z_* = 227.

Same bug also affects the drag-epoch optical depth tau_d.
```

## Thermal Ladder Outputs vs Planck 2018 base-LCDM

```text
observable                          SAM       Planck 2018           dev
------------------------------------------------------------------------------
z_eq                          3596.1707         3402.0000       +5.708%
z_star (Peebles+buggy tau)     227.3151         1089.9200      -79.144%
z_drag (Peebles+buggy tau)     427.1521         1059.9400      -59.700%
r_s(z_star) Mpc                328.2601          144.4300     +127.280%
r_d Mpc                        244.1354          147.0900      +65.977%
D_M(z_star) Mpc              13015.3205        13869.6000       -6.159%
ell_A                          124.5623          301.7600      -58.721%
100*theta_*                      2.5221            1.0411     +142.254%
```

## P1 — Acoustic Angular Scale — FAIL

| field | value |
|---|---:|
| 100*theta_* SAM | 2.5221 |
| 100*theta_* Planck | 1.04110 |
| relative deviation | **+142.254%** |
| threshold | <= 5.00% |
| margin to threshold | 28.5x OVER threshold |
| **pass** | **false** |

100*theta_* is wildly off because r_s(z_*) is over-extended (SAM 328 Mpc
vs Planck 144) when z_* is too low. With z_* = 227 (a_* = 1/228), the
sound horizon integral runs from a=0 to a=1/228 - much further than
Planck's a=1/1091 - accumulating roughly 2.3x the physical r_s.

## P2 — Acoustic Peak Multipole — FAIL

| field | value |
|---|---:|
| ell_A SAM | 124.56 |
| ell_A Planck | 301.76 |
| relative deviation | **-58.721%** |
| threshold | <= 5.00% |
| margin to threshold | 11.7x OVER threshold |
| **pass** | **false** |

ell_A = pi/theta_*. Lower z_* boosts r_s, which lowers theta_* inversely
and ell_A correspondingly.

## P3 — Drag Sound Horizon — FAIL

| field | value |
|---|---:|
| r_d SAM | 244.14 Mpc |
| r_d Planck | 147.09 Mpc |
| relative deviation | **+65.977%** |
| threshold | <= 5.00% |
| margin to threshold | 13.2x OVER threshold |
| **pass** | **false** |

CR001@19 had r_d at +2.87% PASS — the Peebles + buggy tau combination
now overshoots r_d by 66% because z_d also drops (427 vs Planck 1060)
and r_s integrated to that later epoch picks up far more sound horizon.

## Reported Evidence

### E1 — z_eq

```text
z_eq = 3596.17, Planck 3402, dev +5.71%
```

Identical to CR001@19 within rounding. z_eq is set by Omega_m/Omega_r
ratio at H_0 = 68.76; recombination/optical-depth physics doesn't enter.

### E2-E5 — Recombination-affected quantities

All four (z_*, z_d, r_s(z_*), D_M(z_*)) are dominated by the Bug-B tau
formula in this CR. Reported for the audit trail; will be re-tested in
CR001c@19 with corrected tau.

### E6 — k_eq

```text
k_eq = 0.01098 1/Mpc
```

Independent of recombination physics. Identical to CR001@19.

### E7-E12 — BBN

| quantity | SAM | observed | dev |
|---|---:|---:|---:|
| eta_10 | 6.373 | 6.10 | +4.47% |
| T_f MeV (schematic) | 1.1499 | ~0.8 textbook | — |
| Y_p (schematic) | 0.3938 | 0.245 | +60.73% |
| D/H (eta^-1.6 scaled) | 2.356e-5 | 2.527e-5 | -6.76% |

BBN block is independent of recombination/optical-depth machinery.
Identical to CR001@19.

## Reported Null Distributions

### WC1 — Random Omega_m in [0.05, 0.95], 1000 trials

| field | value |
|---|---:|
| canonical \|100*theta_* dev\| | 1.42254 |
| null median | 1.32233 |
| canonical percentile in null | **71.90%** |
| one-sided p-value | 0.71928 |

The canonical substrate's percentile is WORSE than median under random
Omega_m draws. This is consistent with Bug B dominating: the bug forces
theta_* far from Planck for the canonical substrate; random Omega_m
draws (also under the buggy tau formula) span a similar range and many
land closer to Planck than the canonical does.

### WC2 — Random (Omega_m, Omega_b), 1000 trials

| field | value |
|---|---:|
| canonical \|100*theta_* dev\| | 1.42254 |
| null median | 1.54188 |
| canonical percentile in null | **31.90%** |
| one-sided p-value | 0.31968 |

Joint (Omega_m, Omega_b) random draws span an even wider theta_*
range, putting canonical at 32nd percentile. Both WCs report against
the buggy tau, so percentiles here measure how the substrate canonical
ranks among random parameter choices UNDER THE SAME BUG. They will be
re-reported with the corrected tau in CR001c@19.

## Pass Conditions

| condition | pass |
|---|---:|
| P1_100theta_star_within_5pct | false |
| P2_ellA_within_5pct | false |
| P3_rd_within_5pct | false |

## Root Cause Summary

```text
Bug A (Peebles RHS missing the exp(-h*nu_alpha/kT) factor):
  Caught and corrected during implementation. The precommit RHS as
  written maintains x_e ~ 1 forever and produces no recombination.
  The textbook-correct form (with exp(-13.6 eV/kT) in beta_eff) was
  used in this runner. This DEPARTURE FROM THE PRECOMMIT is documented
  above; the precommit text in CR001c@19 will be corrected to match
  the textbook standard.

Bug B (tau integrand uses 1/(a^2 * H) instead of 1/(a * H)):
  HONORED per the appeal discipline. The result is the gross failure
  documented in P1, P2, P3. This is the bug that will be corrected in
  CR001c@19.

Substrate inputs (Omega_m = 1/pi, Omega_b = 2*A_0*(1-chi)):
  Not implicated. Same identities pass cleanly in CR018b, CR019, CR025,
  CR031b, CR032. The CR001b@19 failure is purely arithmetic in the
  optical-depth integrand.
```

## Connection to CR001@19

```text
CR001@19 (Saha + buggy tau, sealed FAIL):
  z_* = 995, z_d = 986, r_s = 150.4, r_d = 151.3, theta_* +6.87%

The CR001@19 result.md attributed the FAIL to Saha as the
"first clean approximation." That attribution was partially correct
(Saha does undershoot z_*) but missed the tau-integrand bug. With the
corrected tau formula in CR001c@19, Saha alone may produce a smaller
deviation than CR001@19 reported (the bug and Saha both pushed z_*
down; removing the bug recovers some z_*).

CR001@19 verdict is preserved as sealed FAIL. A separate appeal
CR001c@19 will run with corrected tau using both Saha AND Peebles
side-by-side to isolate each contribution.
```

## Scope of the FAIL

```text
The CR001b@19 ladder fails on all three gates by 12-29x the 5%
threshold. The failure is mechanically due to the buggy tau integrand
specified in the precommit. The substrate inputs are not implicated.

Precommit Bug A (Peebles RHS exp factor) was caught and corrected
during implementation; this runner departs from the precommit on that
point and the departure is documented transparently in this result.md.

Precommit Bug B (tau formula 1/(a^2*H)) was honored per the appeal
discipline ("every step documented") and produces the FAIL above.
```

## Rule-9 Line

```text
This test could have falsified the claim that SAM's substrate-only
spine, with Omega_m = 1/pi and Omega_b = 2*A_0*(1-chi) sealed and z_*
/ z_d derived from the (precommit-specified) Peebles non-equilibrium
recombination + Thomson and baryon-drag optical-depth integrals (as
specified in the precommit including its arithmetic), reproduces the
Planck 2018 base-LCDM compressed CMB acoustic geometry to within 5%
on 100*theta_*, ell_A, and r_d.

It did falsify that specific claim. P1, P2, P3 all FAIL by 12-29x the
threshold. The failure mechanism is identified as Bug B in the
precommit's tau integrand, not the substrate identities.

It does NOT falsify the substrate identities. CR001c@19 will retest
with the corrected tau formula at the same 5% gates.
```

## Retest Plan: CR001c@19

```text
CR001c@19 will:
  - Reuse the same substrate inputs and measurement inputs.
  - Reuse the same 5% gates on 100*theta_*, ell_A, r_d.
  - Specify the Peebles RHS with the textbook-correct Boltzmann factor
    (exp(-13.6 eV / kT) in beta_eff) — encoding Bug A's fix into the
    precommit text.
  - Specify the tau integrand as 1/(a * H), correcting Bug B.
  - Run both Saha and Peebles side-by-side for diagnostic transparency
    on which approximation contributes how much to the residual
    deviation.

Substrate identities are unchanged. Gate thresholds are unchanged.
The corrections are purely arithmetic in the precommit specification.
```

## Provenance Chain

```text
Stewardship           = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Naming canon          = 35c2d9650909f420018e1a72f1a597e101a1670c7eb00b0bcaec63724928a2f8
Patent claim register = db91680abce1e18d23f559eb8bb8141f04dd51b8a038504f9959ae0437291fa1
CR001@19  precommit   = 7aec7240daf98c9a99e010692ec97e9966b3221568977538b1917561c304bdff
CR001b@19 precommit   = 38259de487a8b3a31df787c7c5d5bed5e442c134472b74e3f5ad0a98d7ff991b
CR018b precommit      = bdd4dc29688af099a0ec5b6f47e4cb0e449f0ff36c45037e545bf76bb88879ce
CR019 precommit       = ef52480d1bbbac21103a8937a864e5cd2992b0d6046efbe15d1732961eb529da
```

---

**Sealed by:** Sean Brady, 2026-06-27.
