# QC004 - Paul Revere Readout Protocol

## Result

```text
QC004_PAUL_REVERE_READOUT_PROTOCOL_SELECTED
```

## Main Readout

```text
protocol_rows = 5
allowed_pre_write_observables = 6
blocked_pre_write_observables = 8
check_passes = 8/8
wrong_control_passes = 6/6
free_parameters_introduced = 0
```

## Protocol

| protocol_step | native_gate | readout_target | allowed_pre_write_readout | post_write_join_rule | protocol_status |
| --- | --- | --- | --- | --- | --- |
| 1 | shielded_no_write_wait | window-open flag | boundary stress / basin pressure / timing / syndrome only | no final join at this gate | SELECTED |
| 2 | letter_preserving_drift_gate | phase drift;polarization drift | boundary stress / basin pressure / timing / syndrome only | no final join at this gate | SELECTED |
| 3 | basin_bias_steering_gate | syndrome_signal;basin_bias;boundary_stress | boundary stress / basin pressure / timing / syndrome only | no final join at this gate | SELECTED |
| 4 | controlled_A_contact_gate | window-open flag;phase drift;polarization drift;timing headroom | boundary stress / basin pressure / timing / syndrome only | no final join at this gate | SELECTED |
| 5 | delayed_resolution_read_gate | timing headroom | boundary stress / basin pressure / timing / syndrome only | hash freeze required | SELECTED |

## Observable Split

| observable | timing | readout_status |
| --- | --- | --- |
| route_family | pre-write | ALLOWED_PRE_WRITE |
| boundary_stress | pre-write | ALLOWED_PRE_WRITE |
| time_to_A_SIDE | pre-write | ALLOWED_PRE_WRITE |
| time_to_A_SHARE | pre-write | ALLOWED_PRE_WRITE |
| basin_bias | pre-write | ALLOWED_PRE_WRITE |
| syndrome_signal | pre-write | ALLOWED_PRE_WRITE |
| clone_final_outcome | pre-write | SAM_BLOCKER |
| copy_logical_route_identity | pre-write | SAM_BLOCKER |
| final_ledger_outcome | pre-write | SAM_BLOCKER |
| force_pre_resolution_route_after_A_SHARE | pre-write | SAM_BLOCKER |
| ledger_commit_result | pre-write | SAM_BLOCKER |
| logical_route_identity | pre-write | SAM_BLOCKER |
| premature_selected_write | pre-write | SAM_BLOCKER |
| selected_final_result | pre-write | SAM_BLOCKER |
| selected_final_result | post-write only | ALLOWED_ONLY_AFTER_SELECTED_WRITE_AND_HASH_FREEZE |

## Checks

| check_id | check | pass | detail |
| --- | --- | --- | --- |
| QC004_CHECK_01 | QC003 dependency is selected | True | QC003_PARTICLE_INFORMED_NATIVE_GATE_CATALOG_SELECTED |
| QC004_CHECK_02 | all QC003 native gates receive readout protocol rows | True | 5 |
| QC004_CHECK_03 | allowed pre-write observable set has six SAM letter fields | True | 6 |
| QC004_CHECK_04 | forbidden final payload fields map to SAM_BLOCKER | True | 8 |
| QC004_CHECK_05 | delayed read gate carries hash freeze rule | True | delayed_resolution_read_gate |
| QC004_CHECK_06 | sample clean events pass | True | 5 |
| QC004_CHECK_07 | sample leakage event blocks | True | QC004-EVT-BLOCK |
| QC004_CHECK_08 | carrier lane is protected in every protocol row | True | QUBIT-NL-001 |

## Wrong Controls

| control_id | wrong_control | expected | actual | pass |
| --- | --- | --- | --- | --- |
| QC004_WC_01 | final payload pre-write is treated as allowed | False | False | True |
| QC004_WC_02 | readout protocol omits protected carrier | False | False | True |
| QC004_WC_03 | readout protocol omits control lane | False | False | True |
| QC004_WC_04 | readout protocol omits sensor lane | False | False | True |
| QC004_WC_05 | delayed read lacks hash-freeze rule | False | False | True |
| QC004_WC_06 | unsupported protocol status appears | False | False | True |

## Next Frontier

```text
QC005_PRIVATE_MATERIAL_ISOTOPE_SUPPORT_FILTER
```
