# QN007 - Private Earth-A Deployment Surface

## Result

```text
QN007_EARTH_A_DEPLOYMENT_SURFACE_SELECTED
```

QN007 separates literal Earth gravitational A from engineered QN controls.

## Main Readout

```text
earth_surface_A = 1.390657777567e-09
earth_fraction_of_A_SIDE = 3.3375786661608004e-08
earth_fraction_of_A_SHARE = 1.6687893330804002e-08
control_surface_rows = 8
hardware_requirement_rows = 7
apparatus_required_controls = 7
check_passes = 6/6
wrong_control_passes = 5/5
external_quantum_network_data_used = False
free_parameters_introduced = 0
```

## Threshold Gap

| threshold | threshold_A | earth_surface_A | earth_fraction_of_threshold | literal_earth_A_reaches_threshold |
| --- | --- | --- | --- | --- |
| A_SIDE | 0.041666666666666664 | 1.390657777567e-09 | 3.3375786661608004e-08 | False |
| A_SHARE | 0.08333333333333333 | 1.390657777567e-09 | 1.6687893330804002e-08 | False |
| A_ALPHA_H_D | 0.5 | 1.390657777567e-09 | 2.781315555134e-09 | False |
| A_HORIZON | 1.0 | 1.390657777567e-09 | 1.390657777567e-09 | False |
| PRIVATE_CORE_CL_LANE_EARTH_SURFACE_EXPOSURE_RATE | 1e-05 | 1.390657777567e-09 | 0.0001390657777567 | False |

## Control Surface

| control_id | network_object_id | network_object_class | supplied_by | apparatus_required | control_role |
| --- | --- | --- | --- | --- | --- |
| QN007-CTRL-00 | EARTH_BACKGROUND | FIXED_A_FLOOR | EARTH_GRAVITATIONAL_A | False | fixed weak-field floor / clock-rate context |
| QN007-CTRL-01 | QN-CARRIER-001 | UNRESOLVED_CARRIER | APPARATUS_ENGINEERED_CONTROL | True | carrier isolation and no-write preservation |
| QN007-CTRL-02 | QN-ENVELOPE-001 | CONTROL_ENVELOPE | APPARATUS_ENGINEERED_CONTROL | True | controlled A-contact and timing envelope |
| QN007-CTRL-03 | QN-SENSOR-001 | BOUNDARY_SENSOR | APPARATUS_ENGINEERED_CONTROL | True | allowed stress/basin/timing letter readout |
| QN007-CTRL-04 | QN-LEDGERNODE-001 | LEDGER_NODE | APPARATUS_ENGINEERED_CONTROL | True | selected write endpoint and commit delay |
| QN007-CTRL-05 | QN-RELAY-001 | RELAY_REPEATER | APPARATUS_ENGINEERED_CONTROL | True | letter-safe relay with no-clone guard |
| QN007-CTRL-06 | QN-SUPPORT-001 | MATERIAL_SUPPORT | APPARATUS_ENGINEERED_CONTROL | True | support geometry and environmental conditioning |
| QN007-CTRL-99 | QN006_CORRECTION_LAYER | REAL_TIME_LETTER_CORRECTION | APPARATUS_PLUS_QN_PROTOCOL | True | real-time correction before A_SHARE closure |

## Hardware Requirements

| requirement_id | network_object_id | requirement_class | SAM_function |
| --- | --- | --- | --- |
| QN007-REQ-01 | QN-CARRIER-001 | REQUIRED_APPARATUS_CONTROL | carrier isolation and no-write preservation |
| QN007-REQ-02 | QN-ENVELOPE-001 | REQUIRED_APPARATUS_CONTROL | controlled A-contact and timing envelope |
| QN007-REQ-03 | QN-SENSOR-001 | REQUIRED_APPARATUS_CONTROL | allowed stress/basin/timing letter readout |
| QN007-REQ-04 | QN-LEDGERNODE-001 | REQUIRED_APPARATUS_CONTROL | selected write endpoint and commit delay |
| QN007-REQ-05 | QN-RELAY-001 | REQUIRED_APPARATUS_CONTROL | letter-safe relay with no-clone guard |
| QN007-REQ-06 | QN-SUPPORT-001 | REQUIRED_APPARATUS_CONTROL | support geometry and environmental conditioning |
| QN007-REQ-99 | QN006_CORRECTION_LAYER | REQUIRED_APPARATUS_CONTROL | real-time correction before A_SHARE closure |

## Checks

| check_id | check | pass | detail |
| --- | --- | --- | --- |
| QN007_CHECK_01 | literal Earth A is below A_SIDE | True | 3.3375786661608004e-08 |
| QN007_CHECK_02 | literal Earth A is below A_SHARE | True | 1.6687893330804002e-08 |
| QN007_CHECK_03 | active network controls are apparatus supplied | True | 7 |
| QN007_CHECK_04 | carrier, envelope, and sensor controls remain separated | True | BOUNDARY_SENSOR;CONTROL_ENVELOPE;FIXED_A_FLOOR;LEDGER_NODE;MATERIAL_SUPPORT;REAL_TIME_LETTER_CORRECTION;RELAY_REPEATER;UNRESOLVED_CARRIER |
| QN007_CHECK_05 | deployment decisions do not permit ledger commit | True | True |
| QN007_CHECK_06 | no external quantum-network hardware data is used | True | external=False;claims=False |

## Wrong Controls

| control_id | wrong_control | expected | actual | pass |
| --- | --- | --- | --- | --- |
| QN007_WC_01 | literal Earth A is treated as enough to reach A_SIDE | False | False | True |
| QN007_WC_02 | active QN controls are supplied by Earth gravity alone | False | False | True |
| QN007_WC_03 | control envelope is promoted to carrier role | False | False | True |
| QN007_WC_04 | external hardware benchmark data is used | False | False | True |
| QN007_WC_05 | deployment surface permits ledger commit | False | False | True |

## Interpretation

QN007 says the Earth lab starts with a real but weak A floor:

```text
Earth A is background context
carrier isolation is apparatus
control envelope is apparatus
boundary sensing is apparatus
ledger-safe relay logic is protocol/apparatus
closed windows remain closed
```

So the network does not wait for literal gravitational Earth A to create the
route-control condition. Earth A gives the background write-rate environment;
the live QN controls are engineered.

## Outputs

```text
artifacts/qn007/qn007_preflight.md
artifacts/qn007/qn007_input_manifest.csv
artifacts/qn007/earth_a_network_control_surface.csv
artifacts/qn007/carrier_envelope_hardware_requirements.csv
artifacts/qn007/earth_a_threshold_gap_table.csv
artifacts/qn007/earth_a_deployment_decision_surface.csv
artifacts/qn007/qn007_checks.csv
artifacts/qn007/qn007_wrong_controls.csv
artifacts/qn007/qn007_summary.json
artifacts/qn007/qn007_next_frontier.csv
```

## Next Frontier

```text
QN008_PRIVATE_SEALED_LAB_BENCHMARK_MANIFEST
```
