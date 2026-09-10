# CR014 BAO Ruler Projection Ledger Shrinkage

## Verdict

```text
CR014_PASS_BAO_RULER_PROJECTION_LEDGER_SHRINKAGE
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = PASS_BAO_RULER_PROJECTION_LEDGER
```

## BAO Packet

```text
rows = 19
w = 0.0466031311731253
max_prediction_error = 0.000e+00
rms_pull = 0.826987277684
rows_over_3sigma = 0
```

## Pass Conditions

| condition | pass |
|---|---:|
| no_older_test_verdicts_used | true |
| free_parameters_introduced_zero | true |
| bao_source_rows_present | true |
| sn_inputs_not_loaded | true |
| window_values_follow_declared_symbols | true |
| bao_windowed_prediction_identity | true |
| f_ap_derived_from_dm_dh_rows | true |
| all_primary_rows_under_3sigma | true |
| wrong_controls_do_not_match_packet | true |

## Rule-9 Line

```text
This test could have falsified the BAO ledger claim if the BAO rows did not recompute from their local ruler/projection window packet, if F_AP was not derived from recomputed DM/DH rows, if SN rows were needed, or if wrong controls matched the packet.
```
