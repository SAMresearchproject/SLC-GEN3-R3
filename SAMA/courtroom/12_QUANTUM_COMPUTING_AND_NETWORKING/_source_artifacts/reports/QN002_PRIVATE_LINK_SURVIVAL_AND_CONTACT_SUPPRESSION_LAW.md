# QN002 - Private Link Survival And Contact Suppression Law

## Result

```text
QN002_LINK_SURVIVAL_AND_CONTACT_SUPPRESSION_LAW_SELECTED
```

QN002 builds the first SAM-native quantum-network link survival score.

## Main Readout

```text
scored_link_rows = 3
selected_link_object = QN-CARRIER-001
selected_link_route = QUBIT-NL-001
selected_link_viability_score = 0.06559092722191634
selected_segment_survival_score = 0.06802717720543114
selected_route_capacity_prior = 0.9641871075120799
check_passes = 5/5
wrong_control_passes = 5/5
external_quantum_network_data_used = False
free_parameters_introduced = 0
```

## Formula

| term | formula | source |
| --- | --- | --- |
| valid_letter_fraction | valid_pre_resolution_letter_rows / total_contact_rows | QP013 contact suppression table |
| active_suppression_fraction | active_suppression_rows / total_contact_rows | QP013 contact suppression table |
| headroom_factor | max_pre_resolution_headroom_to_A_SHARE | QP013 route control window table |
| suppression_margin_to_A_SIDE | 1 - max_required_suppression_to_restore_A_SIDE / native_theoretical_ceiling_before_A_SHARE | QP013 route control window table |
| segment_survival_score | valid_letter_fraction * active_suppression_fraction * headroom_factor * suppression_margin_to_A_SIDE * ledger_safety_guard | QN001 + QP013 |
| link_viability_score | segment_survival_score * route_capacity_prior | QN001 + QP013 + QP014 |

## Link Viability Ranking

| rank | network_object_id | selected_route | segment_survival_score | route_capacity_prior | link_viability_score | selected_top_link |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | QN-CARRIER-001 | QUBIT-NL-001 | 0.06802717720543114 | 0.9641871075120799 | 0.06559092722191634 | True |
| 2 | QN-SENSOR-001 | QUBIT-UNK-001 | 0.06802594121888259 | 0.025575392682963508 | 0.0017397901593011154 | False |
| 3 | QN-ENVELOPE-001 | QUBIT-CL-001 | 0.06802358834322994 | 0.008963616628858815 | 0.0006097373676280225 | False |

## Survival Table

| network_object_id | object_class | selected_route | route_present_in_qp013_qp014 | segment_survival_score | link_viability_score | selector_class |
| --- | --- | --- | --- | --- | --- | --- |
| QN-CARRIER-001 | UNRESOLVED_CARRIER | QUBIT-NL-001 | True | 0.06802717720543114 | 0.06559092722191634 | SELECTED_PROTECTED_LINK_CARRIER |
| QN-ENVELOPE-001 | CONTROL_ENVELOPE | QUBIT-CL-001 | True | 0.06802358834322994 | 0.0006097373676280225 | CONTROL_ENVELOPE_SIDE_BAND_NOT_PRIMARY_LINK |
| QN-SENSOR-001 | BOUNDARY_SENSOR | QUBIT-UNK-001 | True | 0.06802594121888259 | 0.0017397901593011154 | BOUNDARY_SENSOR_SIDE_BAND |
| QN-LEDGERNODE-001 | LEDGER_NODE | LOCAL_NODE_COMPOSITE | False | 0.0 | 0.0 | NOT_LINK_SURVIVAL_CANDIDATE |
| QN-RELAY-001 | RELAY_REPEATER | CARRIER_PLUS_ENVELOPE_HANDOFF | False | 0.0 | 0.0 | NOT_LINK_SURVIVAL_CANDIDATE |
| QN-SUPPORT-001 | MATERIAL_SUPPORT | triadic/color/support lanes | False | 0.0 | 0.0 | NOT_LINK_SURVIVAL_CANDIDATE |

## Checks

| check_id | check | pass | detail |
| --- | --- | --- | --- |
| QN002_CHECK_01 | protected carrier is top scored link | True | QN-CARRIER-001 |
| QN002_CHECK_02 | carrier has positive no-write segment survival | True | 0.06802717720543114 |
| QN002_CHECK_03 | at least three route-backed network objects are scored | True | 3 |
| QN002_CHECK_04 | selected top link keeps ledger safety guard | True | 1 |
| QN002_CHECK_05 | no survival row permits final outcome as pre-resolution content | True | True |

## Wrong Controls

| control_id | wrong_control | expected | actual | pass |
| --- | --- | --- | --- | --- |
| QN002_WC_01 | charged control envelope outranks protected carrier as link carrier | False | False | True |
| QN002_WC_02 | material support becomes primary link carrier | False | False | True |
| QN002_WC_03 | carrier link has zero survival score | False | False | True |
| QN002_WC_04 | envelope score exceeds carrier score | False | False | True |
| QN002_WC_05 | support object receives route-backed link score | False | False | True |

## Interpretation

The protected network link is not chosen by name. It wins because the neutral
unresolved carrier combines:

```text
high route capacity prior
positive pre-resolution letter window
positive active A-contact suppression window
large no-write headroom to A_SHARE
ledger safety guard = 1
```

The charged lane remains a control envelope, and the boundary route remains a
stress sensor. Both are useful, but neither outranks the protected carrier as
the main unresolved network link.

## Outputs

```text
artifacts/qn002/qn002_preflight.md
artifacts/qn002/qn002_input_manifest.csv
artifacts/qn002/sam_link_survival_table.csv
artifacts/qn002/sam_link_viability_score.csv
artifacts/qn002/sam_link_score_formula.csv
artifacts/qn002/qn002_checks.csv
artifacts/qn002/qn002_wrong_controls.csv
artifacts/qn002/qn002_summary.json
artifacts/qn002/qn002_next_frontier.csv
```

## Next Frontier

```text
QN003_PRIVATE_LEDGER_SAFE_RELAY_REPEATER_LAW
```
