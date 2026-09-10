# Test 7 Verdict

**Verdict:** `PASS_TEST7_PR_TOMOGRAPHY_SIMULATION`

## Internal Checks

- [PASS] A_side_equals_1_over_24: True
- [PASS] purity_threshold_equals_23_over_24: True
- [PASS] qubit_analytic_value_correct: True
- [PASS] qutrit_analytic_value_correct: True
- [PASS] qubit_sim_crossing_matches_analytic: True
- [PASS] qutrit_sim_crossing_matches_analytic: True
- [PASS] density_matrices_valid_or_flagged: True
- [PASS] purity_in_allowed_range: True
- [PASS] A_leak_in_allowed_range: True
- [PASS] first_crossing_detected_if_present: True
- [PASS] population_only_control_rejected: True
- [PASS] wrong_threshold_ordering_passed: True
- [PASS] shuffled_time_control_rejected: True
- [PASS] scrambled_density_control_changes_purity: True

## Constants Locked

- `A_SIDE = 1 / (2 * R) = 1/24 = 0.041666666666666664`
- `PURITY_THRESHOLD = 23/24 = 0.9583333333333334`
- `R = 12, D = 3, alpha_H = 2`

## Simulation Crossings (Discrete + Interpolated)

- qubit interpolated `t_PR / T2 = 0.04350593846148717` (analytic `0.043505688494814905`; |diff| = 2.5e-07)
- qutrit interpolated `t_PR / T2 = 0.0354360781602973` (analytic `0.03543583226729687`; |diff| = 2.46e-07)

## Controls (All Pass)

- A (1/12) / B (1/18) / 1/24 reference / C (1/36) — ordering `t_{1/36} < t_{1/24} < t_{1/18} < t_{1/12}` confirmed on both qubit and qutrit runs
- D random threshold (seed 20260621): sampled threshold 0.109656; crossings reported honestly
- E population-only: coherent P=1.0 vs diag P=113/289 with identical populations — `PASS_POPULATION_ONLY_REJECTED`
- F shuffled time (seed 20260621): `PASS_SHUFFLED_TIME_REJECTED`
- G scrambled density (off-diagonals zeroed): populations preserved, purity changed — `PASS_SCRAMBLED_DENSITY_CHANGES_PURITY`

## Allowed Claim

```text
SAM's Paul Revere warning observable was implemented correctly:
A_leak = 1 - Tr(rho^2), with threshold A_side = 1/24, and the runner
detects the expected crossing in controlled qubit and qutrit dephasing models.
```

## Not Claimed

- Real-data PR pass — `--mode analyze` available but no real density-matrix data ingested in this run.
- Counts reconstruction — `COUNTS_MODE_NOT_IMPLEMENTED` reserved for amendment.
- Correction advantage — extension not run.
- Universal `t_PR / T2` — crossing time is model-specific (qubit and qutrit differ by design).