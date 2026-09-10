# QN003 - Private Ledger-Safe Relay / Repeater Law

## Result

```text
QN003_LEDGER_SAFE_RELAY_REPEATER_LAW_SELECTED
```

QN003 defines the first SAM-native relay/repeater law.

## Main Readout

```text
allowed_packet_fields = 6
no_clone_guards = 6
selected_relay_surface = ONE_T_SW:N0
selected_surface_commit_probability_sum = 0.0
selected_surface_interference_probability = 0.9296619558155835
relay_viability_score = 0.060977389684884344
check_passes = 6/6
wrong_control_passes = 5/5
external_quantum_network_data_used = False
free_parameters_introduced = 0
```

## Relay Rules

| rule_id | relay_stage | operation | allowed | guard |
| --- | --- | --- | --- | --- |
| QN003-RELAY-01 | ACCEPT | accept protected carrier letter | True | carrier remains unresolved |
| QN003-RELAY-02 | TRANSFER | transfer route pressure and syndrome packet | True | packet fields restricted to QP012B/QN001 allowed letter fields |
| QN003-RELAY-03 | SURFACE | use no-commit support/interference surface | True | commit_probability_sum == 0 |
| QN003-RELAY-04 | ENVELOPE | refresh timing/contact envelope without becoming carrier | True | envelope does not carry final route identity |
| QN003-RELAY-05 | DELAY | delay ledger commit until selected endpoint write | True | no premature ledger commit inside relay |
| QN003-RELAY-06 | FORBID | copy final ledger outcome or logical route identity | False | no-clone guard |

## Transfer Packet

| packet_field | relay_permission | copy_mode | may_trigger_ledger_commit |
| --- | --- | --- | --- |
| route_family | TRANSFER_ALLOWED | STRUCTURE_OR_PRESSURE_ONLY | False |
| boundary_stress | TRANSFER_ALLOWED | STRUCTURE_OR_PRESSURE_ONLY | False |
| time_to_A_SIDE | TRANSFER_ALLOWED | STRUCTURE_OR_PRESSURE_ONLY | False |
| time_to_A_SHARE | TRANSFER_ALLOWED | STRUCTURE_OR_PRESSURE_ONLY | False |
| basin_bias | TRANSFER_ALLOWED | STRUCTURE_OR_PRESSURE_ONLY | False |
| syndrome_signal | TRANSFER_ALLOWED | STRUCTURE_OR_PRESSURE_ONLY | False |

## No-Clone Guard

| guard_id | forbidden_operation | guard_condition | pass |
| --- | --- | --- | --- |
| QN003-NOCLONE-01 | copy_final_ledger_outcome | field_must_not_be_present_in_relay_packet | True |
| QN003-NOCLONE-02 | copy_logical_route_identity | field_must_not_be_present_in_relay_packet | True |
| QN003-NOCLONE-03 | copy_repeater_copy | field_must_not_be_present_in_relay_packet | True |
| QN003-NOCLONE-04 | copy_ledger_commit | field_must_not_be_present_in_relay_packet | True |
| QN003-NOCLONE-05 | clone_final_outcome | relay_must_preserve_letter_not_clone_final_state | True |
| QN003-NOCLONE-06 | copy_logical_route_identity | relay_must_preserve_letter_not_clone_final_state | True |

## Selected Surface

```text
surface = ONE_T_SW:N0
top_interference_pair = QUBIT-NL-001<->QUBIT-NL-001
top_interference_probability = 0.9296619558155835
commit_probability_sum = 0.0
support_probability_sum = 1.0
```

## Relay Viability Terms

| term | value | source |
| --- | --- | --- |
| selected_link_viability_score | 0.06559092722191634 | QN002 |
| selected_no_commit_surface_weight | 0.9296619558155835 | QP015 |
| packet_guard | 1 | QN001/QN003 |
| no_clone_guard | 1 | QN001/QN003 |
| no_commit_guard | 1 | QP015/QN003 |
| relay_viability_score | 0.060977389684884344 | QN002 * QP015 * QN003 guards |

## Checks

| check_id | check | pass | detail |
| --- | --- | --- | --- |
| QN003_CHECK_01 | six allowed packet fields transferred | True | 6 |
| QN003_CHECK_02 | final outcome and logical route identity absent from packet | True | basin_bias;boundary_stress;route_family;syndrome_signal;time_to_A_SHARE;time_to_A_SIDE |
| QN003_CHECK_03 | selected relay surface has no ledger commit | True | 0.0 |
| QN003_CHECK_04 | no-clone guards all pass | True | 6 |
| QN003_CHECK_05 | relay law contains an explicit forbid rule | True | FORBID |
| QN003_CHECK_06 | relay viability score is positive | True | 0.060977389684884344 |

## Wrong Controls

| control_id | wrong_control | expected | actual | pass |
| --- | --- | --- | --- | --- |
| QN003_WC_01 | relay packet transports final ledger outcome | False | False | True |
| QN003_WC_02 | relay packet transports logical route identity | False | False | True |
| QN003_WC_03 | relay selected a commit-open surface | False | False | True |
| QN003_WC_04 | relay selected boundary commit pair as transfer carrier | False | False | True |
| QN003_WC_05 | forbid rule is missing from relay law | False | False | True |

## Interpretation

The relay is not a classical amplifier. It transfers the allowed Paul Revere
letter packet:

```text
route family
boundary stress
time to A_SIDE
time to A_SHARE
basin bias
syndrome signal
```

It does not transfer:

```text
final ledger outcome
logical route identity
ledger commit
```

The selected relay surface is a no-commit support/interference surface. That is
the narrow bridge between useful network handoff and forbidden outcome copying.

## Outputs

```text
artifacts/qn003/qn003_preflight.md
artifacts/qn003/qn003_input_manifest.csv
artifacts/qn003/ledger_safe_relay_rules.csv
artifacts/qn003/repeater_no_clone_guard.csv
artifacts/qn003/relay_transfer_packet_schema.csv
artifacts/qn003/relay_surface_selector.csv
artifacts/qn003/relay_viability_score.csv
artifacts/qn003/qn003_checks.csv
artifacts/qn003/qn003_wrong_controls.csv
artifacts/qn003/qn003_summary.json
artifacts/qn003/qn003_next_frontier.csv
```

## Next Frontier

```text
QN004_PRIVATE_PAUL_REVERE_ROUTING_PROTOCOL
```
