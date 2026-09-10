# CR037C -- Parameter-Free CMB Shape on ACT DR4 -- RESULT

```text
verdict           : PASS
verdict_reason    : P1 PASS, P2 PASS, polarization not degraded
classification    : EXTERNAL_CATALOG_INDEPENDENCE_CR
execution_status  : CLEAN
sealed_utc        : 2026-06-29
precommit_hash    : 6ab6024c6e99ae35540ba93976cda79c3b2569bc4fffcd2371e36fd6ab4bd8ca
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
engine            : CAMB 1.6.6
free_parameters_introduced : 0
prior_CR_result_inputs     : false
Run_B_optimizer_used       : false
yp2_fitted                 : false
yp2_value                  : 1.0
act_data_sha256_verified   : true
forbidden_files_opened     : false
pyactlike_imported         : false
```

## Headline

The SAM-derived cosmology sealed in CR037B (densities + H_0 + perturbation
triplet, all from substrate atoms via FIRAS T_CMB + CODATA 2018 / SI
fixed constants) runs through CAMB at lmax=8000 and is convolved with
the ACT DR4 bandpower window functions. The model bandpower vector
X_model is compared to the published ACTPol cleaned-CMB likelihood
(Choi et al. 2020) using the full 260x260 covariance with yp2 fixed at
1.0 (no polarization-efficiency calibration fit).

Result:

```text
chi^2_TT   / dof_TT   = 1.2996  (chi^2 = 103.97, dof = 80)
chi^2_TE   / dof_TE   = 0.9495  (chi^2 = 85.46, dof = 90)
chi^2_EE   / dof_EE   = 1.0662  (chi^2 = 95.96, dof = 90)
chi^2_full / dof_full = 1.1218  (chi^2 = 291.67, dof = 260)
```

## SAM cosmology under test (zero free parameters)

| field | value | identity |
| --- | ---: | --- |
| Omega_m | 0.3183098862 | R*A_0 = 1/pi |
| Omega_b | 0.0492990113 | 2*A_0*(1-chi) |
| Omega_c | 0.2690108749 | Omega_m - Omega_b |
| H_0 (km/s/Mpc) | 67.250375195 | CR036 sealed |
| A_s | 2.111747e-09 | eta_SAM * sqrt(R)  (CR037A sealed) |
| n_s | 0.9646322349 | 1 - chi/2  (CR037A sealed) |
| tau | 0.0530516477 | 2 * A_0  (CR037A sealed) |
| yp2 | 1.0 | fixed (no polarization fit) |

## Gate-by-gate

| gate | claim | result |
| --- | --- | :---: |
| P1 | chi^2_TT/dof <= 2.0 | PASS |
| P2 | chi^2_full/dof <= 2.0 | PASS |
| P3 | TE/EE chi^2/dof <= 3.0 (polarization not degraded) | PASS |

## E1 per-patch reporting (not gated)

| patch | chi^2 | dof | chi^2/dof |
| --- | ---: | ---: | ---: |
| deep TT | 60.640 | 40 | 1.5160 |
| wide TT | 43.459 | 40 | 1.0865 |
| deep TE | 40.466 | 45 | 0.8992 |
| wide TE | 44.901 | 45 | 0.9978 |
| deep EE | 39.199 | 45 | 0.8711 |
| wide EE | 57.100 | 45 | 1.2689 |

## E4 yp2 sensitivity (reported)

| yp2 | chi^2_full/dof | TE/dof | EE/dof |
| ---: | ---: | ---: | ---: |
| 0.99 | 1.1605 | 1.0024 | 1.1682 |
| 1.00 | 1.1218 | 0.9495 | 1.0662 |
| 1.01 | 1.1309 | 0.9085 | 1.0730 |

## Verdict statement

CR037C verdict: **PASS** -- P1 PASS, P2 PASS, polarization not degraded

The CR037B parameter-free Planck PR3 result extends to an independent
ground-based instrument (ACT DR4, Choi et al. 2020) using the full
bandpower covariance and the published bandpower window functions, with
zero new free parameters and yp2 fixed at 1.0. This is the
external-catalog independence test placeholder named in CR037B's
"Connection to Future Work" section.

`CR037C_PASS_SAM_COSMOLOGY_ON_ACT_DR4_TT_chi2_over_dof_1.2996_FULL_chi2_over_dof_1.1218_ZERO_FREE_PARAMETERS_yp2_FIXED_AT_1.0_EXTERNAL_CATALOG_INDEPENDENCE_FROM_PLANCK_PR3`
