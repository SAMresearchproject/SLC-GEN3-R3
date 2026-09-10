# QN006 - Private Error Correction As Letter Management

## Result

```text
QN006_LETTER_SAFE_ERROR_CORRECTION_SELECTED
```

QN006 restates network error correction as management of allowed
pre-resolution letters.

## Main Readout

```text
syndrome_rows = 49
correction_rules = 7
correction_decision_rows = 49
open_correction_samples = 5
closed_correction_samples = 2
correction_classes = BOUNDARY_SENSOR_LETTER_READ;CARRIER_ACTIVE_SUPPRESSION;CARRIER_PASSIVE_PRESERVATION;CONTROL_ENVELOPE_ADJUSTMENT;SUPPORT_OUTSIDE_NETWORK_DENOMINATOR;WINDOW_CLOSED_STOP_CORRECTION
check_passes = 6/6
wrong_control_passes = 5/5
external_quantum_network_data_used = False
free_parameters_introduced = 0
```

## Correction Rules

| rule_id | correction_stage | operation | ledger_commit_allowed | pass |
| --- | --- | --- | --- | --- |
| QN006-CORR-01 | READ_LETTER | read syndrome and route-pressure letter | False | True |
| QN006-CORR-02 | PRESERVE_PROBABILITY | preserve QN005 normalized unresolved probability surface | False | True |
| QN006-CORR-03 | CARRIER_CONTROL | preserve carrier and apply active suppression when boundary pressure rises | False | True |
| QN006-CORR-04 | SENSOR_READ | read boundary sensor as damage letter only | False | True |
| QN006-CORR-05 | ENVELOPE_ADJUST | adjust charged envelope without promoting it to carrier | False | True |
| QN006-CORR-06 | NO_CLONE_GUARD | apply QN003 no-clone guard to every correction packet | False | True |
| QN006-CORR-07 | WINDOW_CLOSE | stop pre-resolution correction when the surface closes | False | True |

## Sample Correction Summary

| sample_id | correction_surface_state | open_correction_routes | corrected_probability_sum | probability_mass_preserved |
| --- | --- | --- | --- | --- |
| ONE_T_SW | LETTER_SAFE_CORRECTION_OPEN | 3 | 1.0 | True |
| QUARTER_A_SIDE | LETTER_SAFE_CORRECTION_OPEN | 3 | 1.0 | True |
| HALF_A_SIDE | LETTER_SAFE_CORRECTION_OPEN | 3 | 1.0 | True |
| A_SIDE_BOUNDARY | LETTER_SAFE_CORRECTION_OPEN | 3 | 1.0 | True |
| MID_A_SIDE_TO_A_SHARE | LETTER_SAFE_CORRECTION_OPEN | 3 | 1.0 | True |
| A_SHARE_BOUNDARY | CORRECTION_WINDOW_CLOSED | 0 | 0.0 | True |
| WRITE_MIDPOINT | CORRECTION_WINDOW_CLOSED | 0 | 0.0 | True |

## Checks

| check_id | check | pass | detail |
| --- | --- | --- | --- |
| QN006_CHECK_01 | correction rules use allowed letter fields only | True | 7 |
| QN006_CHECK_02 | letter-safe correction preserves open probability mass | True | ONE_T_SW:1.0;QUARTER_A_SIDE:1.0;HALF_A_SIDE:1.0;A_SIDE_BOUNDARY:1.0;MID_A_SIDE_TO_A_SHARE:1.0 |
| QN006_CHECK_03 | closed windows remain closed under correction | True | A_SHARE_BOUNDARY:0.0;WRITE_MIDPOINT:0.0 |
| QN006_CHECK_04 | correction never permits ledger commit | True | False |
| QN006_CHECK_05 | forbidden final ledger fields are not used | True | False |
| QN006_CHECK_06 | active correction classes exist for carrier, sensor, and envelope | True | BOUNDARY_SENSOR_LETTER_READ;CARRIER_ACTIVE_SUPPRESSION;CARRIER_PASSIVE_PRESERVATION;CONTROL_ENVELOPE_ADJUSTMENT;SUPPORT_OUTSIDE_NETWORK_DENOMINATOR;WINDOW_CLOSED_STOP_CORRECTION |

## Wrong Controls

| control_id | wrong_control | expected | actual | pass |
| --- | --- | --- | --- | --- |
| QN006_WC_01 | correction reads final outcome or logical route identity | False | False | True |
| QN006_WC_02 | closed A_SHARE/WRITE windows are corrected back open | False | False | True |
| QN006_WC_03 | support-only routes become correction carriers | False | False | True |
| QN006_WC_04 | control envelope is promoted to unresolved carrier | False | False | True |
| QN006_WC_05 | letter correction changes normalized probability mass | False | False | True |

## Interpretation

QN006 gives the network a SAM-native error-correction primitive:

```text
read syndrome, stress, basin, and timing letters
preserve the QN005 unresolved probability surface
act through carrier isolation, boundary sensor readout, and envelope adjustment
refuse correction when A_SHARE/write windows have closed
never read or copy the final ledger result
```

The correction object is the letter and its allowed control response, not a
classical copy of the final answer.

## Outputs

```text
artifacts/qn006/qn006_preflight.md
artifacts/qn006/qn006_input_manifest.csv
artifacts/qn006/sam_network_error_syndrome_table.csv
artifacts/qn006/letter_safe_correction_rules.csv
artifacts/qn006/letter_safe_correction_decision_surface.csv
artifacts/qn006/letter_safe_correction_sample_summary.csv
artifacts/qn006/qn006_checks.csv
artifacts/qn006/qn006_wrong_controls.csv
artifacts/qn006/qn006_summary.json
artifacts/qn006/qn006_next_frontier.csv
```

## Next Frontier

```text
QN007_PRIVATE_EARTH_A_DEPLOYMENT_SURFACE
```
