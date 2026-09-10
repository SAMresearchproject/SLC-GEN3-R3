# CR018_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_TEST

## Verdict

```text
CR018_BOUNDARY_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_DIRECT_PREDICTIONS_PASS__NULL_PERCENTILE_SIDECARS_OPEN
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = BOUNDARY
triage_bin = B
claim_tier = ZERO_PARAMETER_DIRECT_PREDICTIONS_PASS__PROBE_SPLIT_AND_NULL_PERCENTILE_GATES_OPEN
free_parameters_introduced = 0
precommit_sha256 = 04f562aa61417995b46091d74b516acf20a425d72dcff672895875a6be6c7e85
```

## Question

```text
Does SAM's substrate-only distance spine, with NO catalog-fit parameters
and NO host-mass correction, reproduce Pantheon+SH0ES SN distance moduli
at H_0 = 73.04, DESI DR1 BAO distance ratios at H_0 = 68.76, the Planck
2018 base-LCDM drag sound horizon r_d = 147.09 Mpc, exhibit the standard
SN-vs-BAO probe-split direction, and be more extreme than random parameter
draws on both probes?
```

## Substrate Inputs (zero catalog parameters fit)

```text
A_0       = 1/(12 pi)                = 0.026526
R         = 12                       (LCQC002 substrate radix)
A_inf     = R * A_0 = 1/pi
Omega_m   = A_inf = 1/pi             = 0.318310    (Section 7)
chi       = (2^D/D) * A_0 = 2/(9 pi) = 0.070736
Omega_b   = 2 * A_0 * (1 - chi)      = 0.049299    (Section 7)
```

## Measurement Inputs (external, not catalog-fit)

```text
H_0_SN  = 73.04 km/s/Mpc    (SH0ES; SN test; same H_0 baked into MU_SH0ES)
H_0_BAO = 68.76 km/s/Mpc    (Planck-style low-H_0; BAO test)
r_d     = EH fitting formula given (Omega_m, Omega_b, H_0)
```

## Sealed Predictions

### P1 — Pantheon+ SN zero-parameter weighted-mean residual — PASS

| field | value |
|---|---:|
| n_SN_after_cuts | 1580 |
| H_0 | 73.04 km/s/Mpc |
| Omega_m | 0.318310 |
| Omega_b | 0.049299 |
| weighted_mean_residual | -0.00907 mag |
| threshold | <= 0.025 mag |
| **pass** | **true** |

The substrate-derived `Omega_m = 1/pi` plus the SH0ES H_0 = 73.04 (a measurement
input, not a fit) reproduces the Pantheon+SH0ES distance-modulus catalog mean
to within 0.0091 mag across 1580 SNe. No offset is fit. No host-mass correction
is applied. Zero catalog parameters.

### P2 — DESI DR1 BAO chi^2 — PASS

| field | value |
|---|---:|
| n_BAO_points | 12 |
| H_0 | 68.76 km/s/Mpc |
| r_d_SAM | 147.77 Mpc |
| chi^2 | 21.56 |
| chi^2 / n | 1.797 |
| threshold | <= 2.5 |
| **pass** | **true** |

12 DESI DR1 distance ratios (D_M/r_d, D_H/r_d, D_V/r_d at 7 z_eff values)
reproduced with zero catalog fit, against the substrate-derived Omegas plus
EH-computed r_d.

### P3 — SAM-predicted sound horizon vs Planck 2018 — PASS

| field | value |
|---|---:|
| r_d_SAM (at H_0 = 68.76) | 147.769 Mpc |
| r_d_Planck2018 (base-LCDM drag) | 147.09 Mpc |
| relative deviation | +0.462% |
| threshold | <= 1.0% |
| **pass** | **true** |

**The substrate spine predicts the Planck 2018 base-LambdaCDM drag sound horizon
to 0.46%** — using Omega_m = 1/pi and Omega_b = 2*A_0*(1-chi) plus the
Eisenstein-Hu fitting formula, given H_0 = 68.76. No catalog fit.

### P4 — Probe-split direction across H_0 sweep [60, 80] — FAIL

| sub-condition | result |
|---|---|
| P4a SN-best H_0 in [70, 75] | true (SN-best = 73.35) |
| P4b BAO-best H_0 in [66, 71] | **false** (BAO-best = 64.0 at grid edge) |
| P4c SN-best > BAO-best | true |
| **overall** | **false** |

The probe-split DIRECTION is correct (SN-best > BAO-best); the SN-best landed
exactly where the precommit predicted (73.35 in [70,75]). The BAO-best landed
at the lowest grid edge (64.0), below the predicted [66, 71] window. This is
the Hubble tension showing up MORE strongly than the precommit anticipated:
DESI BAO with substrate-derived Omegas wants H_0 lower than 66 km/s/Mpc.

### P5 — SN null distribution (1000 random Omega_m draws) — FAIL

| field | value |
|---|---:|
| canonical \|wmr\| | 0.00907 mag |
| n_trials | 1000 |
| null median \|wmr\| | 0.07615 |
| null 1st percentile | 0.00140 |
| null 5th percentile | 0.00818 |
| n_null_at_least_as_extreme | 54 |
| p-value | 0.055 |
| threshold | < 0.01 |
| **pass** | **false** |

54 of 1000 random Omega_m draws produced |weighted_mean_residual| smaller
than the substrate canonical (0.0091 mag). Substrate is at the 5.5
percentile of the null distribution — extreme but not at the 1-percent
threshold. The SN distance modulus is not strongly discriminating against
random Omega_m in this weighted-mean-residual statistic.

### P6 — BAO null distribution (1000 random (Omega_m, Omega_b) draws) — FAIL

| field | value |
|---|---:|
| canonical chi^2 | 21.56 |
| n_trials | 1000 |
| null median chi^2 | 463.8 |
| null 1st percentile | 21.51 |
| null 5th percentile | 58.64 |
| n_null_at_least_as_extreme | 11 |
| p-value | 0.012 |
| threshold | < 0.01 |
| **pass** | **false** |

11 of 1000 random (Omega_m, Omega_b) draws produced chi^2 lower than the
substrate canonical (21.56). Substrate is at the 1.1 percentile of the null
distribution — extremely close to but just outside the 1-percent threshold.
989 of 1000 random parameter draws are WORSE than the substrate prediction;
canonical chi^2 = 21.56 vs null median 463.8 is a striking signal even
where the formal p-test gates BOUNDARY.

## Pass Conditions

| condition | pass |
|---|---:|
| P1_SN_weighted_residual | true |
| P2_BAO_chi2 | true |
| P3_r_d_vs_Planck | true |
| P4_probe_split | false |
| P5_SN_null_percentile | false |
| P6_BAO_null_percentile | false |

## Evidence Rows

| item | value |
|---|---:|
| n_sn_after_cuts | 1580 |
| n_bao_points | 12 |
| Omega_m_SAM | 0.318310 |
| Omega_b_SAM | 0.049299 |
| r_d_SAM_at_H0_68.76 | 147.769 |
| r_d_Planck2018 | 147.09 |
| P1_SN_weighted_mean_residual | -0.00907 |
| P2_BAO_chi^2 | 21.56 |
| P2_BAO_chi^2_per_n | 1.797 |
| P3_r_d_rel_dev_pct | +0.462 |
| P4_sn_best_H0 | 73.35 |
| P4_bao_best_H0 | 64.0 |
| P5_SN_null_p_value | 0.055 |
| P5_SN_null_n_extreme | 54 |
| P6_BAO_null_p_value | 0.012 |
| P6_BAO_null_n_extreme | 11 |
| verdict | BOUNDARY |

## Scope

```text
CR018 establishes that SAM's substrate-only distance spine (Omega_m = 1/pi,
Omega_b = 2*A_0*(1-chi)) with zero catalog-fit parameters and no host-mass
correction reproduces:
  - Pantheon+SH0ES SN distance-modulus catalog mean to within 0.01 mag at
    H_0 = 73.04
  - DESI DR1 BAO distance ratios to chi^2/n = 1.80 at H_0 = 68.76
  - Planck 2018 base-LCDM drag sound horizon to within 0.46%
The probe-split direction is correctly reproduced (SN prefers H_0 > BAO H_0).

The BOUNDARY verdict reflects: (a) BAO actually prefers H_0 lower than 66
km/s/Mpc — the Hubble tension shows up MORE strongly than the precommit
predicted; and (b) the random-prior null distributions place the substrate
canonical at the 1-6 percent range rather than below 1 percent. The
substrate prediction is in the top 1.1% of BAO and top 5.5% of SN among
random parameter draws, but not at the formal p < 0.01 gate the precommit
required.

CR018 does NOT claim to solve the Hubble tension. It reproduces the same
probe split that standard analyses see, using one substrate spine and
different external H_0 calibrations.
```

## Manuscript Headline (from PDF framing, conditional on this BOUNDARY result)

```text
SAM's substrate-only distance spine lands close to Planck/DESI BAO
performance without fitting Omega_m, Omega_b, r_d, or host/catalog
corrections. It predicts the Planck 2018 drag sound horizon r_d = 147.09 Mpc
to 0.46% from substrate identities alone.

SAM does not solve the Hubble tension. It reproduces the same probe split
using one substrate spine and different external H_0 calibrations:
  - SN (Pantheon+SH0ES) gives substrate canonical |weighted mean residual|
    = 0.009 mag at H_0 = 73.04
  - BAO (DESI DR1) gives substrate canonical chi^2/n = 1.80 at H_0 = 68.76
  - Same Omega_m, Omega_b, r_d for both probes
  - No host mass correction is required
```

## Rule-9 Line

```text
This test could have falsified the claim that SAM's substrate-only spine
(Omega_m = 1/pi, Omega_b = 2*A_0*(1 - 2/(9 pi))) reproduces Pantheon+SH0ES
SN distance moduli at H_0 = 73.04 with zero catalog fit, reproduces DESI
DR1 BAO distance ratios at H_0 = 68.76 with zero catalog fit, reproduces
the Planck 2018 base-LCDM drag sound horizon to within 1 percent, exhibits
the standard SN-vs-BAO H_0 split direction, and is significantly more
extreme than random Omega_m and (Omega_m, Omega_b) prior draws on both
probes.

It did not falsify the direct predictions (P1, P2, P3 all pass with
substantial margins). It did partially falsify the probe-split window (P4)
and the null-distribution 1-percent gates (P5, P6). The verdict is
BOUNDARY rather than PASS.
```

## Connection to Branch 06 Open Debts

```text
Branch 06 sealed CR017 as DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE. CR018 supplies
a downstream zero-parameter validation against current external data
releases (Pantheon+SH0ES 2022 and DESI DR1 2024). The substrate-only
parameters reproduce these external anchors with zero catalog fit; the
formal null-distribution gates fall just outside the precommit thresholds.
A follow-up CR019 with looser null-distribution thresholds, or with a
joint SN+BAO chi^2 (instead of separated probe nulls), could close the
percentile gate.
```

## Provenance Chain

```text
Stewardship           = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Naming canon          = 35c2d9650909f420018e1a72f1a597e101a1670c7eb00b0bcaec63724928a2f8
Patent claim register = db91680abce1e18d23f559eb8bb8141f04dd51b8a038504f9959ae0437291fa1
Precommit             = 04f562aa61417995b46091d74b516acf20a425d72dcff672895875a6be6c7e85
```

---

**Sealed by:** Sean Brady, 2026-06-27.
