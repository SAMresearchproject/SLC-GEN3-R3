# QN009 - Private Benchmark Comparator Schema

## Result

```text
QN009_BENCHMARK_COMPARATOR_SCHEMA_FROZEN
```

QN009 freezes the SAM quantum-network comparator grammar before candidate
hardware or protocol data enters the branch.

## Main Readout

```text
benchmark_rows_imported = 8
scoring_rule_rows = 8
candidate_role_template_rows = 7
candidate_evidence_template_rows = 8
forbidden_leakage_screen_rows = 10
status_vocabulary_rows = 5
check_passes = 7/7
wrong_control_passes = 5/5
external_quantum_network_data_used = False
free_parameters_introduced = 0
```

## Comparator Rule Surface

| benchmark_id | sealed_object | required_candidate_fields | sam_match_condition | sam_blocker_condition |
| --- | --- | --- | --- | --- |
| QN-BENCH-001 | network_object_grammar | carrier_role;control_envelope_role;boundary_sensor_role | candidate maps distinct mechanisms to carrier=QUBIT-NL-001, envelope=QUBIT-CL-001, sensor=QUBIT-UNK-001 | candidate collapses carrier, final outcome, and control readout into one early ledger read |
| QN-BENCH-002 | link_survival_and_viability | carrier_isolation;active_suppression;timing_headroom;route_capacity_evidence | candidate reports protected carrier transport with active contact suppression and timing headroom | candidate requires reading final route identity to maintain link |
| QN-BENCH-003 | ledger_safe_relay | relay_packet_fields;no_clone_guard;no_commit_support_surface | candidate relays allowed syndrome/pressure letters without copying final outcome or route identity | candidate copies final outcome, clones route identity, or commits during relay |
| QN-BENCH-004 | paul_revere_routing | pre_resolution_letter;timing_lead;closed_window_stop_rule | candidate routes warning letters before write closure and stops once the window closes | candidate transmits selected final result before physical resolution |
| QN-BENCH-005 | network_born_surface | route_stability_surface;carrier_topology;open_closed_window_behavior | candidate route stability favors protected unresolved carrier and normalizes only over open routes | candidate normalizes by peeking at final ledger outcome |
| QN-BENCH-006 | letter_safe_error_correction | allowed_syndrome_fields;correction_latency;probability_preservation;forbidden_field_guard | candidate corrects allowed letters in real time while preserving unresolved probability surface | candidate error correction reads logical route identity or ledger commit result |
| QN-BENCH-007 | earth_a_deployment_surface | apparatus_controls;shielding;cooling;timing;geometry_support | candidate supplies apparatus controls rather than relying on literal Earth A | candidate claims literal Earth gravitational A is sufficient control engine |
| QN-BENCH-008 | forbidden_leakage_invariant | final_outcome_access_policy;logical_route_identity_policy;pre_write_commit_policy | candidate explicitly forbids final outcome and logical route identity before selected write | candidate permits final ledger outcome or logical route identity before selected write |

## Forbidden Leakage Screen

| screen_id | forbidden_item | source | comparator_status_if_triggered |
| --- | --- | --- | --- |
| QN009-LEAK-01 | act_as_primary_unresolved_carrier | QN001_NETWORK_OBJECT_GRAMMAR | SAM_BLOCKER |
| QN009-LEAK-02 | clone_final_outcome | QN001_NETWORK_OBJECT_GRAMMAR | SAM_BLOCKER |
| QN009-LEAK-03 | copy_final_outcome | QN006_LETTER_SAFE_CORRECTION | SAM_BLOCKER |
| QN009-LEAK-04 | copy_logical_route_identity | QN001_NETWORK_OBJECT_GRAMMAR | SAM_BLOCKER |
| QN009-LEAK-05 | final_ledger_outcome | QN001_NETWORK_OBJECT_GRAMMAR | SAM_BLOCKER |
| QN009-LEAK-06 | force_pre_resolution_route_after_A_SHARE | QN006_LETTER_SAFE_CORRECTION | SAM_BLOCKER |
| QN009-LEAK-07 | ledger_commit_result | QN006_LETTER_SAFE_CORRECTION | SAM_BLOCKER |
| QN009-LEAK-08 | logical_route_identity | QN001_NETWORK_OBJECT_GRAMMAR | SAM_BLOCKER |
| QN009-LEAK-09 | premature_ledger_commit | QN001_NETWORK_OBJECT_GRAMMAR | SAM_BLOCKER |
| QN009-LEAK-10 | premature_selected_write | QN008_FORBIDDEN_LEAKAGE_INVARIANT | SAM_BLOCKER |

## Checks

| check_id | check | pass | detail |
| --- | --- | --- | --- |
| QN009_CHECK_01 | QN008 package is frozen before comparator schema | True | QN008_SEALED_LAB_BENCHMARK_MANIFEST_FROZEN |
| QN009_CHECK_02 | all QN008 benchmark rows are covered by scoring rules | True | 8/8 |
| QN009_CHECK_03 | candidate templates contain placeholders only | True | 15 |
| QN009_CHECK_04 | comparator introduces no ranking weights or fitted scores | True | NONE_REQUIRED_BINARY_BLOCKER |
| QN009_CHECK_05 | forbidden leakage screen includes final ledger outcome | True | 10 |
| QN009_CHECK_06 | status vocabulary is closed before external comparison | True | SAM_MATCH;SAM_PARTIAL;SAM_MISS;SAM_BLOCKER;NOT_REPORTED |
| QN009_CHECK_07 | no external hardware data is admitted in QN009 schema | True | templates_only |

## Wrong Controls

| control_id | wrong_control | expected | actual | pass |
| --- | --- | --- | --- | --- |
| QN009_WC_01 | real candidate hardware data enters QN009 | False | False | True |
| QN009_WC_02 | weighted ranking score is introduced before external comparison | False | False | True |
| QN009_WC_03 | final ledger outcome can pass leakage screen | False | False | True |
| QN009_WC_04 | scoring schema omits blocker state | False | False | True |
| QN009_WC_05 | candidate evidence template already declares comparator outputs | False | False | True |

## Interpretation

QN009 turns the sealed QN008 package into a comparison interface:

```text
candidate roles are mapped to sealed SAM network objects
candidate evidence is collected per sealed benchmark object
comparison status is closed before external data enters
forbidden leakage is a blocker, not a soft penalty
no ranking weights or fitted platform scores are introduced
```

The result is a ready shell for QN010 approved external comparison.

## Outputs

```text
artifacts/qn009/qn009_preflight.md
artifacts/qn009/qn009_input_manifest.csv
artifacts/qn009/candidate_hardware_role_map_template.csv
artifacts/qn009/candidate_benchmark_evidence_template.csv
artifacts/qn009/sam_qn_benchmark_scoring_rules.csv
artifacts/qn009/forbidden_leakage_screen.csv
artifacts/qn009/sam_qn_comparator_output_schema.csv
artifacts/qn009/qn009_checks.csv
artifacts/qn009/qn009_wrong_controls.csv
artifacts/qn009/qn009_summary.json
artifacts/qn009/qn009_next_frontier.csv
```

## Next Frontier

```text
QN010_PRIVATE_APPROVED_EXTERNAL_BENCHMARK_COMPARISON_REQUIRES_PREFLIGHT
```
