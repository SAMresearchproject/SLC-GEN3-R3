# CR037A_SAM_PERTURBATION_SELECTOR

## Verdict

```text
CR037A_PASS_SAM_PERTURBATION_TRIPLET_WITHIN_1SIGMA_PLANCK_POSTERIOR
```

## Courtroom Fields

```text
execution_status             = CLEAN
scientific_verdict           = PASS
triage_bin                   = A
free_parameters_introduced   = 0
prior_CR_result_inputs       = false
CMB_spectrum_inputs          = false
posterior_table_inputs       = false
forbidden_files_opened       = false
opened_paths_count           = 0
precommit_sha256             = 1b7da85b860825d7e9b0a8e7d231aef92ec980b020341800da81a09f48ba5d78
```

## Substrate Identities Under Test

| parameter | identity | SAM value |
|---|---|---:|
| A_s | η_SAM · √R = 7·√R / (4·(12π)⁶) | 2.1117473568e-09 |
| n_s | 1 − χ/2 = 1 − 1/(9π) | 0.9646322349 |
| τ | 2·A_0 = 1/(6π) | 0.0530516477 |

η_SAM verified from substrate atoms (Path A vs Path B agree to 1.70e-16).

## Frozen Planck References (in-code; NOT file-read)

| field | value |
|---|---:|
| A_s_reference | 2.100e-09 ± 3.000e-11 |
| n_s_reference | 0.9649 ± 0.0042 |
| τ_reference | 0.0544 ± 0.0073 |

## P1, P2, P3 — Selector Gates

| param | SAM value | σ_dev | band | STRONG_CONTACT |
|---|---:|---:|---|---:|
| **A_s** (P1) | 2.1117473568e-09 | **+0.3916** | **PASS** | True |
| **n_s** (P2) | 0.9646322349 | **-0.0638** | **PASS** | True |
| **τ** (P3) | 0.0530516477 | **-0.1847** | **PASS** | True |

Bands: PASS ≤ 1.0σ; BOUNDARY (1.0σ, 2.0σ]; FAIL > 2.0σ.
STRONG_CONTACT_X: |σ_dev| ≤ 0.5.

## E1 — Wrong-Control Comparators for A_s

| comparator | value | σ_dev vs A_s_ref |
|---|---:|---:|
| eta_SAM (bare) | 6.0961e-10 | -49.6797 |
| eta * sqrt(R) [chosen]  ← canonical | 2.1117e-09 | +0.3916 |
| eta * sqrt(S) | 1.7242e-09 | -12.5255 |
| eta * sqrt(R/2) | 1.4932e-09 | -20.2256 |
| eta * sqrt(Theta) | 2.5864e-09 | +16.2117 |
| eta * D | 1.8288e-09 | -9.0391 |
| eta * pi | 1.9151e-09 | -6.1619 |

The canonical A_s_SAM = η·√R earns its place if its |σ_dev| is the
smallest of the set (or tied for smallest). Reported as evidence.

## E2 — Self-Lifted τ Alternative (reported only)

```text
tau_alt = 2 * A_0 * (1 + A_0) = 0.054458886359
sigma_dev_tau_alt = +0.0081
```

Canonical CR037A τ is 2·A_0 = 1/(6π); the self-lifted form is reported
for completeness and is NOT used in the P3 gate.

## E3 — Algebraic Two-Path Checks (machine precision)

| identity | Path A − Path B (relative) |
|---|---:|
| η_SAM | 1.696e-16 |
| n_s,SAM | 0.000e+00 |
| A_s,SAM | 1.959e-16 |
| τ_SAM | 0.000e+00 |

## Chronology

```text
CR037A is the selector test for the SAM perturbation triplet. It does
NOT consult any CMB spectrum, likelihood, chain, or posterior table at
runtime. It computes three closed-form substrate values and compares
them to frozen Planck 2018 posterior centroids declared as numeric
constants in the precommit. If CR037A PASSes, CR037B follows: the
CR036B pipeline with these three SAM values replacing the Planck-
centroid perturbation inputs.

The runner did not open any CR036, CR036B, CR035A, or CR035A2 file at
runtime; the forbidden-file guard did not trip (opened_paths_count =
0; forbidden_files_opened = false).
```

## Provenance Chain

```text
Stewardship    = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Precommit      = 1b7da85b860825d7e9b0a8e7d231aef92ec980b020341800da81a09f48ba5d78
eta_SAM source = CR036 sealed PASS (precommit 345a1a8d...; eta_SAM verified in CR037A runner from atoms)
```

---

**Sealed by:** CR037A runner, 2026-06-27.
