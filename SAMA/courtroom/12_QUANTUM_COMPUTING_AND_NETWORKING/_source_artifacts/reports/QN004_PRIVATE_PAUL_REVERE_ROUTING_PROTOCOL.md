# QN004 - Private Paul Revere Routing Protocol

## Result

```text
QN004_PAUL_REVERE_ROUTING_PROTOCOL_SELECTED
```

QN004 builds the first SAM-native Paul Revere routing protocol.

## Main Readout

```text
protocol_steps = 5
decision_rows = 49
route_selected_samples = 5
closed_window_samples = 2
selected_route = QUBIT-NL-001
top_selected_routing_score = 0.003999561548899118
check_passes = 6/6
wrong_control_passes = 4/4
external_quantum_network_data_used = False
free_parameters_introduced = 0
```

## Formula

| term | formula | source |
| --- | --- | --- |
| valid_letter_gate | 1 if valid_pre_resolution_letter else 0 | QP013 |
| timing_headroom | pre_resolution_headroom_to_A_SHARE | QP013 |
| boundary_pressure | 1 - pre_resolution_headroom_to_A_SHARE | QP013 |
| route_link_viability | QN002 link_viability_score for route | QN002 |
| relay_viability | QN003 relay_viability_score | QN003 |
| routing_score | valid_letter_gate * route_link_viability * relay_viability * timing_headroom | QP013 + QN002 + QN003 |

## Protocol

| step | protocol_stage | operation | uses_fields | ledger_commit_allowed |
| --- | --- | --- | --- | --- |
| 1 | READ_ALLOWED_LETTER | read Paul Revere packet fields | route_family;boundary_stress;time_to_A_SIDE;time_to_A_SHARE;basin_bias;syndrome_signal | False |
| 2 | FILTER_WINDOW | require valid_pre_resolution_letter | time_to_A_SHARE;syndrome_signal | False |
| 3 | SCORE_ROUTE_PRESSURE | score candidate routes by timing headroom, link viability, and relay viability | route_family;boundary_stress;time_to_A_SHARE;basin_bias;syndrome_signal | False |
| 4 | SELECT_NEXT_HOP | choose highest open routing score | routing_score | False |
| 5 | RELAY_PACKET | send allowed packet over QN003 no-commit relay surface | route_family;boundary_stress;time_to_A_SIDE;time_to_A_SHARE;basin_bias;syndrome_signal | False |

## Sample Route Selection

| sample_id | route_decision | selected_route | selected_routing_score | routing_action |
| --- | --- | --- | --- | --- |
| ONE_T_SW | ROUTE_SELECTED | QUBIT-NL-001 | 0.003999561548899118 | PASSIVE_MONITOR_AND_PRESERVE |
| QUARTER_A_SIDE | ROUTE_SELECTED | QUBIT-NL-001 | 0.0034996180878782207 | PASSIVE_MONITOR_AND_PRESERVE |
| HALF_A_SIDE | ROUTE_SELECTED | QUBIT-NL-001 | 0.002999672646752761 | PASSIVE_MONITOR_AND_PRESERVE |
| A_SIDE_BOUNDARY | ROUTE_SELECTED | QUBIT-NL-001 | 0.0019997817645018407 | ACTIVE_ROUTE_AND_SUPPRESS |
| MID_A_SIDE_TO_A_SHARE | ROUTE_SELECTED | QUBIT-NL-001 | 0.0009998908822509206 | ACTIVE_ROUTE_AND_SUPPRESS |
| A_SHARE_BOUNDARY | NO_ROUTE_WINDOW_CLOSED |  | 0 | WINDOW_CLOSED_DO_NOT_ROUTE |
| WRITE_MIDPOINT | NO_ROUTE_WINDOW_CLOSED |  | 0 | WINDOW_CLOSED_DO_NOT_ROUTE |

## Checks

| check_id | check | pass | detail |
| --- | --- | --- | --- |
| QN004_CHECK_01 | packet fields exclude final outcome and logical route identity | True | basin_bias;boundary_stress;route_family;syndrome_signal;time_to_A_SHARE;time_to_A_SIDE |
| QN004_CHECK_02 | protocol steps do not use forbidden fields | True | False |
| QN004_CHECK_03 | decision rows do not use forbidden fields | True | False |
| QN004_CHECK_04 | open samples select protected carrier route | True | QUBIT-NL-001 |
| QN004_CHECK_05 | closed samples refuse routing | True | 2 |
| QN004_CHECK_06 | at least five pre-resolution route choices are made | True | 5 |

## Wrong Controls

| control_id | wrong_control | expected | actual | pass |
| --- | --- | --- | --- | --- |
| QN004_WC_01 | routing uses final outcome or logical route identity | False | False | True |
| QN004_WC_02 | closed A_SHARE/WRITE sample gets routed | False | False | True |
| QN004_WC_03 | charged envelope selected as main route | False | False | True |
| QN004_WC_04 | boundary sensor selected as main route | False | False | True |

## Interpretation

QN004 turns the Paul Revere letter into a routing protocol:

```text
read allowed pressure/timing fields
refuse closed windows
score open routes by link viability, relay viability, and time-to-A_SHARE headroom
select the protected neutral unresolved carrier as next hop
never use final ledger outcome or logical route identity
```

This is routing before resolution: the warning packet moves while the final
ledger result remains sealed.

## Outputs

```text
artifacts/qn004/qn004_preflight.md
artifacts/qn004/qn004_input_manifest.csv
artifacts/qn004/paul_revere_routing_protocol.csv
artifacts/qn004/route_pressure_decision_table.csv
artifacts/qn004/sample_route_selection_summary.csv
artifacts/qn004/routing_score_formula.csv
artifacts/qn004/qn004_checks.csv
artifacts/qn004/qn004_wrong_controls.csv
artifacts/qn004/qn004_summary.json
artifacts/qn004/qn004_next_frontier.csv
```

## Next Frontier

```text
QN005_PRIVATE_NETWORK_BORN_SURFACE
```
