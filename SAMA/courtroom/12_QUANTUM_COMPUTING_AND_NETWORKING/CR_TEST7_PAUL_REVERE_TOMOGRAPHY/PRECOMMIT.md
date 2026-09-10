# TEST 7 — PAUL REVERE QUANTUM WARNING / TOMOGRAPHY TEST — PRECOMMIT

**Date:** 2026-06-22
**Classification:** PAUL_REVERE_TOMOGRAPHY (first QC technology contact)
**Permission status:** GRANTED_BY_USER: Sean Brady, 2026-06-22 (full Test 7 spec + strict addendum issued)
**Part of:** Seven-test ownership arc (Test 7 of 7)
**Status:** PRECOMMITTED before runner execution.

## Purpose

Build and run the first Paul Revere warning test.

The test question is:

```text
Can SAM define a quantum-warning threshold from the native substrate side-channel value
A_side = 1/24, detect that threshold from reconstructed density matrices, and show that
the warning fires before major decoherence damage?
```

The test must use density matrices, not population-only readout.

The central observable is:

```text
A_leak(t) = 1 - Tr(rho(t)^2)
```

The Paul Revere warning threshold is:

```text
A_side = 1 / (2 * R) = 1/24
```

The warning condition is:

```text
A_leak(t) >= A_side
```

Equivalently:

```text
Tr(rho(t)^2) <= 23/24
```

The Paul Revere warning time is:

```text
t_PR = inf { t : 1 - Tr(rho(t)^2) >= 1/24 }
```

## Directory Tree (Locked)

```text
CR_TEST7_PAUL_REVERE_TOMOGRAPHY/
├── PRECOMMIT.md
├── run_test7_pr_tomography.py
├── run_test7_pr_controls.py
├── inputs/
│   ├── density_matrices_template.csv
│   ├── tomography_counts_template.csv
│   └── README_INPUT_SCHEMA.md
├── outputs/
│   ├── test7_model_predictions.csv
│   ├── test7_density_matrix_reconstruction.csv
│   ├── test7_purity_leak_curve.csv
│   ├── test7_pr_warning_events.csv
│   ├── test7_control_comparison.csv
│   ├── test7_internal_checks.json
│   ├── test7_verdict.md
│   └── plots/
│       ├── purity_curve.png
│       ├── A_leak_curve.png
│       ├── threshold_crossing.png
│       └── control_comparison.png
├── controls/
│   ├── threshold_1_over_12.csv
│   ├── threshold_1_over_18.csv
│   ├── threshold_1_over_36.csv
│   ├── threshold_random.csv
│   ├── population_only_false_positive.csv
│   ├── shuffled_time_control.csv
│   └── scrambled_density_control.csv
├── hashes/
│   ├── PRECOMMIT_CURRENT_HASH.txt
│   ├── run_test7_pr_tomography_CURRENT_HASH.txt
│   ├── run_test7_pr_controls_CURRENT_HASH.txt
│   ├── model_predictions_CURRENT_HASH.txt
│   └── final_outputs_CURRENT_HASH.txt
└── HASHES.txt
```

## Hard Rule — Purity Loss Observable

Do not use population-only readout as the Paul Revere observable.

The valid observable is `A_leak = 1 - Tr(rho^2)`.

Population-only measurements are insufficient because two states can have identical populations but different coherence (e.g., the qutrit `(2|0> + 3|1> + 2|2>)/sqrt(17)` has purity 1, while diag(4/17, 9/17, 4/17) has purity 113/289 ≈ 0.391).

## Native SAM Threshold (Locked)

```text
A_SIDE = 1 / (2 * R) = 1/24 = 0.041666666666666664
PURITY_THRESHOLD = 1 - A_SIDE = 23/24 = 0.9583333333333334
```

Constants:

```text
ALPHA_H = 2
D = 3
R = 12
```

## Runner Modes

```bash
python run_test7_pr_tomography.py --mode simulate
python run_test7_pr_tomography.py --mode analyze --density-csv inputs/density_matrices.csv
python run_test7_pr_tomography.py --mode counts --counts-csv inputs/tomography_counts.csv
```

If counts mode is not implemented, the runner must print `COUNTS_MODE_NOT_IMPLEMENTED` and leave that mode for a later amendment.

## Allowed Libraries (Locked)

```text
numpy, pandas, json, math, argparse, pathlib, hashlib, matplotlib
```

Forbidden: `scipy, sklearn, qutip, tensorflow, pytorch, curve_fit, optimization routines`.

## Analytic Crossing Values (Locked)

### Qubit dephasing

```text
rho(0) = 0.5 * [[1, 1], [1, 1]]
rho(t) = [[0.5, 0.5*exp(-t/T2)], [0.5*exp(-t/T2), 0.5]]
P(t)   = (1 + exp(-2t/T2)) / 2
t_PR / T2 = -0.5 * ln(11/12) = 0.043505688494814905
```

### Qutrit dephasing — fixed populations

```text
|psi> = (2|0> + 3|1> + 2|2>) / sqrt(17)
populations (4/17, 9/17, 4/17); sum p_i^2 = 113/289; 2*sum_{i<j} p_i p_j = 176/289
P(t)   = 113/289 + (176/289) * exp(-2t/T2)
t_PR / T2 = -0.5 * ln((23/24 - 113/289) / (176/289)) = 0.03543583226729687
```

The runner must compute these values directly (no hard-coded decimals).

## Simulation Time Grid

```text
T2 = 1.0
time_start = 0.000
time_end   = 0.200
time_step  = 0.001
```

## Density Matrix Validation (Locked)

```text
Hermiticity tolerance:   1e-8
Trace tolerance:         1e-8
Eigenvalue floor:       -1e-8
Purity allowed range:    [-1e-8, 1 + 1e-8]
```

Validation errors (do not silently repair):

```text
NON_HERMITIAN
TRACE_NOT_ONE
NEGATIVE_EIGENVALUE
BAD_FLAT_LENGTH
BAD_DIMENSION
PARSE_ERROR
```

## Density Matrix Input Schema

Required columns:

```text
run_id, platform, dimension, time, time_unit, rho_real_flat, rho_imag_flat, T1, T2, notes
```

Row-major flat order. For 2x2: `rho00|rho01|rho10|rho11`. For 3x3: 9 entries.
Real and imaginary lengths must equal `dimension^2`.

## Core Calculation

```text
P(t) = Re[Tr(rho(t) * rho(t))]
A_leak(t) = 1 - P(t)
if A_leak < 1/24:  PR_state = PR_CLEAR
if A_leak >= 1/24: PR_state = PR_WARNING
```

First crossing = smallest t where `A_leak >= 1/24`. If none, `NO_CROSSING`.

## Linear Interpolation Rule

```text
t_PR_interp = t_i + (t_{i+1} - t_i) * (A_side - A_i) / (A_{i+1} - A_i)
```

Linear only. No curve fitting, no smoothing, no optimization.

## Required Output Columns

`outputs/test7_purity_leak_curve.csv`:

```text
run_id, platform, dimension, time, time_unit, purity, A_leak, A_side, purity_threshold,
PR_state, is_first_crossing, T1, T2, t_over_T2, matrix_valid, matrix_validation_error
```

`outputs/test7_pr_warning_events.csv`:

```text
run_id, platform, dimension, first_crossing_found, t_PR_discrete, t_PR_interpolated,
t_PR_over_T2_discrete, t_PR_over_T2_interpolated, A_side, purity_threshold, verdict
```

## Simulation Pass Condition

```text
qubit interpolated crossing within 1e-5 of 0.043505688494814905
qutrit interpolated crossing within 1e-5 of 0.03543583226729687
```

If either fails, do not proceed to real-data claims.

## Controls (Locked)

- **A** — threshold `1/12` (expect later crossing)
- **B** — threshold `1/18` (expect later than `1/24`, earlier than `1/12`)
- **C** — threshold `1/36` (expect earlier crossing)
- **D** — random threshold in `[0.01, 0.20]`, seed `20260621`
- **E** — population-only false positive: coherent `(2|0>+3|1>+2|2>)/sqrt(17)` vs diag(4/17, 9/17, 4/17) — populations identical, purities 1 and 113/289 (verdict `PASS_POPULATION_ONLY_REJECTED`)
- **F** — shuffled time labels (seed `20260621`); verdict `PASS_SHUFFLED_TIME_REJECTED` if time_monotonic flagged false
- **G** — scrambled density (off-diagonals zeroed); population curve unchanged, purity curve changes (`PASS_SCRAMBLED_DENSITY_CHANGES_PURITY`)

Required ordering: `t_{1/36} < t_{1/24} < t_{1/18} < t_{1/12}`.

## Internal Checks (test7_internal_checks.json)

```text
A_side_equals_1_over_24
purity_threshold_equals_23_over_24
qubit_analytic_value_correct
qutrit_analytic_value_correct
qubit_sim_crossing_matches_analytic
qutrit_sim_crossing_matches_analytic
density_matrices_valid_or_flagged
purity_in_allowed_range
A_leak_in_allowed_range
first_crossing_detected_if_present
population_only_control_rejected
wrong_threshold_ordering_passed
shuffled_time_control_rejected
scrambled_density_control_changes_purity
```

All must be true for simulation pass.

## Allowed Verdicts

```text
PASS_TEST7_PR_TOMOGRAPHY_SIMULATION
PASS_TEST7_PR_TOMOGRAPHY_REAL_DENSITY_DATA
PASS_TEST7_PR_TOMOGRAPHY_COUNTS_RECONSTRUCTION
PASS_TEST7_PR_WARNING_PLUS_CONTROL_ADVANTAGE
```

Failure verdicts:

```text
FAIL_TEST7_THRESHOLD_NOT_LOCKED
FAIL_TEST7_POPULATION_ONLY_USED
FAIL_TEST7_DENSITY_MATRIX_INVALID
FAIL_TEST7_ANALYTIC_SIM_MISMATCH
FAIL_TEST7_NO_PR_CROSSING
FAIL_TEST7_CONTROLS_NOT_DEGRADED
FAIL_TEST7_TIME_AXIS_INVALID
FAIL_TEST7_INPUT_SCHEMA
FAIL_TEST7_DATA_LEAKAGE
FAIL_TEST7_UNIVERSAL_TIME_CLAIM
```

## Universality Rules

```text
The universal SAM object is:     A_leak = 1 - Tr(rho^2)
The universal SAM threshold is:  A_side = 1/24
```

The crossing time is NOT universal. It depends on state, dimension, channel, platform, T1, T2, tomography quality.

A report of "Paul Revere time = 0.04351 T2" (or similar) without specifying the state and channel is `FAIL_TEST7_UNIVERSAL_TIME_CLAIM`.

## Allowed Claims by Verdict

- `PASS_TEST7_PR_TOMOGRAPHY_SIMULATION`: SAM's PR observable was implemented correctly in controlled qubit and qutrit dephasing models.
- `PASS_TEST7_PR_TOMOGRAPHY_REAL_DENSITY_DATA`: PR threshold was detected from reconstructed density matrices without population-only readout.
- `PASS_TEST7_PR_WARNING_PLUS_CONTROL_ADVANTAGE`: PR-triggered correction outperformed specified control correction policies in the tested platform/model.

## K-Gate Audit (Plan)

| Gate | Statement | Plan |
|---|---|---|
| K1 | External anchor | Simulation-only K1 = N/A; real-density mode introduces external platform data as the anchor |
| K2 | Falsification | Any internal check or simulation crossing within-1e-5 failing falsifies |
| K3 | Target hygiene | Threshold `A_side = 1/(2R) = 1/24` locked; analytic values locked; controls locked; libraries locked; verdict labels locked — all in this PRECOMMIT before runner ran |
| K4 | Typed inputs | Substrate constants `{R=12, D=3, alpha_H=2}` only for threshold; T2=1, time grid locked for simulation; analyze mode requires SHA-locked input CSV |
| K5 | Reproduction on demand | Deterministic + seeded controls (D, F: seed 20260621) |

## Sequence in the Seven-Test Arc

Test 7 of 7 — the final arc test. After this, the seven-test ownership arc is complete.

See `[[project-seven-test-ownership-arc-cr230-236]]`.
