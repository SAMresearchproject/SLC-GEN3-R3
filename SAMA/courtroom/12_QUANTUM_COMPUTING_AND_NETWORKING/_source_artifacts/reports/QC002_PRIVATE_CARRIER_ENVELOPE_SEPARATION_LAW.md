# QC002 - Private Carrier / Envelope Separation Law

## Result

```text
QC002_CARRIER_ENVELOPE_SEPARATION_LAW_SELECTED
```

QC002 freezes the first quantum-computing gate primitive law after QC001.

## Main Readout

```text
carrier_route = QUBIT-NL-001
control_envelope_route = QUBIT-CL-001
boundary_sensor_route = QUBIT-UNK-001
carrier_to_envelope_lead_ratio = 107.56674983263241
gate_primitives = 5
check_passes = 9/9
wrong_control_passes = 6/6
free_parameters_introduced = 0
```

## Separation Law

| law_id | law | selected_route | allowed_role | forbidden_role | status |
| --- | --- | --- | --- | --- | --- |
| QC002-LAW-01 | protected carrier identity | QUBIT-NL-001 | carry unresolved route and Paul Revere letter | act as final ledger readout before write | PASS |
| QC002-LAW-02 | control envelope identity | QUBIT-CL-001 | adjust charged envelope without promoting it to carrier | act as primary unresolved carrier | PASS |
| QC002-LAW-03 | boundary stress sensor identity | QUBIT-UNK-001 | report basin/reorganization pressure before final identity resolves | read final ledger outcome | PASS |
| QC002-LAW-04 | carrier-envelope lead separation | QUBIT-NL-001>QUBIT-CL-001 | carrier lead/envelope lead = 107.566749833 | collapse separation by using charged lane as carrier | PASS |
| QC002-LAW-05 | pre-write leakage firewall | all QC002 gates | route_family;boundary_stress;time_to_A_SIDE;time_to_A_SHARE;basin_bias;syndrome_signal | final_ledger_outcome;logical_route_identity;selected_final_result | PASS |
| QC002-LAW-06 | post-write join boundary | final read gate only | join final result only after pre-resolution hash freeze | post-write join before hash freeze | PASS |

## Gate Primitive Catalog

| gate_id | gate_name | allowed_letter | envelope_operation | carrier_state_after_operation | separation_status |
| --- | --- | --- | --- | --- | --- |
| QC002-GATE-01 | shielded_no_write_wait | window-open flag | hold carrier inside open no-write window | UNRESOLVED_PRESERVED | PASS |
| QC002-GATE-02 | phase_drift_envelope_correction | phase drift | adjust charged control envelope without selecting final route | UNRESOLVED_STEERED | PASS |
| QC002-GATE-03 | polarization_drift_envelope_correction | polarization drift | update apparatus orientation while carrier remains unresolved | UNRESOLVED_STEERED | PASS |
| QC002-GATE-04 | basin_stress_boundary_sensor_gate | syndrome_signal | apply letter-safe correction from sensor stress | UNRESOLVED_CORRECTED | PASS |
| QC002-GATE-05 | delayed_resolution_read_gate | timing headroom | allow final read only after selected write and hash boundary | RESOLVED_ONLY_AFTER_SELECTED_WRITE | PASS |

## Checks

| check_id | check | pass | detail |
| --- | --- | --- | --- |
| QC002_CHECK_01 | QC001 primary neutral carrier exists | True | QUBIT-NL-001 |
| QC002_CHECK_02 | QC001 charged route is envelope, not primary carrier | True | QUBIT-CL-001 |
| QC002_CHECK_03 | boundary stress sensor remains separate from carrier and envelope | True | QUBIT-UNK-001 |
| QC002_CHECK_04 | carrier lead exceeds charged envelope lead | True | 107.566749833 |
| QC002_CHECK_05 | QN006 envelope adjust forbids promoting envelope to carrier | True | adjust charged envelope without promoting it to carrier |
| QC002_CHECK_06 | QN013 final-content leak remains a hard blocker | True | QN013-VAL-03 |
| QC002_CHECK_07 | QN013 post-write join boundary remains a hard blocker | True | QN013-VAL-06 |
| QC002_CHECK_08 | all QC002 gate primitives preserve carrier before write | True | 5 |
| QC002_CHECK_09 | all law rows pass | True | 6 |

## Wrong Controls

| control_id | wrong_control | expected | actual | pass |
| --- | --- | --- | --- | --- |
| QC002_WC_01 | charged envelope is promoted to primary unresolved carrier | False | False | True |
| QC002_WC_02 | final ledger outcome is allowed in pre-write packet | False | False | True |
| QC002_WC_03 | post-write join may happen before pre-resolution hash freeze | False | False | True |
| QC002_WC_04 | gate catalog allows pre-write commit | False | False | True |
| QC002_WC_05 | gate catalog allows pre-write final payload | False | False | True |
| QC002_WC_06 | unsupported gate separation status appears | False | False | True |

## Interpretation

QC002 makes the QC slide concrete:

```text
neutral unresolved lane -> protected carrier
charged lane            -> control/readout envelope
8/4 boundary route      -> basin and reorganization stress sensor
QN013 firewall          -> no final-answer leakage before selected write
```

This is the point where the Paul Revere letter stops being only a diagnostic.
It becomes a gate-control primitive: the letter may adjust the envelope while
the carrier remains unresolved.

## Outputs

```text
artifacts/qc002/qc002_carrier_envelope_separation_law.csv
artifacts/qc002/qc002_gate_primitive_catalog.csv
artifacts/qc002/qc002_gate_boundary_conditions.csv
artifacts/qc002/qc002_pre_write_leakage_firewall.csv
artifacts/qc002/qc002_summary.json
```

## Next Frontier

```text
QC003_PRIVATE_PARTICLE_INFORMED_NATIVE_GATE_CATALOG
```
