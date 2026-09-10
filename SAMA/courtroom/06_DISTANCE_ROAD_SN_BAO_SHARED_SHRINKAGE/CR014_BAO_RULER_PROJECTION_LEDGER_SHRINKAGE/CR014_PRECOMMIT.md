# CR014 Precommit

## Test ID

```text
CR014_BAO_RULER_PROJECTION_LEDGER_SHRINKAGE
```

## Test Type

```text
Fresh Courtroom branch test.
Not a pointer to a G-test verdict.
The G717c row artifact is used as source data rows, not as a pass verdict.
```

## Question

```text
Does the BAO ruler/projection route recompute from its own window packet and
derive F_AP from DM/DH rows without SN inputs?
```

## Frozen Formula Set

```text
w = (D/R)*(Omega_b/Omega_BB_PBH_trapped)
non-F_AP rows: prediction = base_predicted*(1+window_value)
F_AP rows: prediction = recomputed_DM_over_rd/recomputed_DH_over_rd
```

## Wrong Controls

```text
no_window
half_window
sign_flipped_window
all_minus_w
phi_power_window
```

## Pass Conditions

```text
no_older_test_verdicts_used = true
free_parameters_introduced_zero = true
bao_source_rows_present = true
sn_inputs_not_loaded = true
window_values_follow_declared_symbols = true
bao_windowed_prediction_identity = true
f_ap_derived_from_dm_dh_rows = true
all_primary_rows_under_3sigma = true
wrong_controls_do_not_match_packet = true
```

## Rule-9 Line

```text
This test could have falsified: the BAO ledger claim if the BAO rows did not
recompute from their local ruler/projection window packet, if F_AP was not
derived from recomputed DM/DH rows, if SN rows were needed, or if wrong controls
matched the packet.
```

