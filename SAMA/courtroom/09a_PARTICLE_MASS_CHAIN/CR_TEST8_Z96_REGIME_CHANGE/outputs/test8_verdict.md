# Test 8 Verdict

**Verdict:** `BOUNDARY_TEST8_Z96_MIXED_SIGNAL`

- Test name: Z=96 Regime-Change / N-Z Stability Collapse
- Input source: inputs/external_nuclide_table.csv
- Input SHA-256: 48cc66a72c278db405fc2b7c7a1ef0b82c321c54dba68c1415218ac9c33ca073
- SAM constants: alpha_H=2, D=3, R=12, SPLIT=8, Z_break=96
- Primary pre-window:  Z = 85..96  (count = 12)
- Primary post-window: Z = 97..108  (count = 12)
- J_96 = 9.5
- C_96 = 0.5833333333333334
- K_96 = 1.0
- p_random_boundary = 0.608048  (N_random = 10000, seed = 20260621, n_valid = 9268)
- Control degradation count: 7 / 7
- SAM boundary rank by J (in scan b=84..112): 15
- Best b by J: b=108, J=12.0

## Internal Checks

- [PASS] constants_locked: True
- [PASS] Z_break_equals_96: True
- [PASS] first_post_boundary_Z_equals_97: True
- [PASS] SAM_prediction_rows_equal_126: True
- [PASS] audit_Z84_passed: True
- [PASS] audit_Z96_passed: True
- [PASS] audit_Z97_passed: True
- [PASS] audit_Z108_passed: True
- [PASS] audit_Z118_passed: True
- [PASS] audit_Z119_passed: True
- [PASS] audit_Z120_passed: True
- [PASS] audit_Z121_passed: True
- [PASS] external_table_loaded: True
- [PASS] external_anchor_rows_created: True
- [PASS] primary_pre_window_count_at_least_10: True
- [PASS] primary_post_window_count_at_least_10: True
- [PASS] random_boundary_controls_completed: True
- [PASS] changepoint_scan_completed: True
- [PASS] wrong_controls_completed: True
- [PASS] no_boundary_relocation: True
- [PASS] no_post_reveal_tuning: True

## Allowed Claim

> The Z=96 boundary remains structurally interesting but is not yet externally confirmed by this scoring lane.

## Disallowed (Per Precommit)

- The boundary was NOT moved if another b scored better.
- No tuning of R, D, 2^D, or Z_break after seeing external data.
- No alternate anchor chosen to improve the result.