# QN008 - Private Sealed Lab Benchmark Manifest

## Result

```text
QN008_SEALED_LAB_BENCHMARK_MANIFEST_FROZEN
```

QN008 seals the QN001-QN007 quantum-network package before external comparison.

## Main Readout

```text
gates_sealed = 7
benchmark_manifest_rows = 8
formula_freeze_rows = 7
sealed_hash_rows = 14
gate_check_passes = 40/40
gate_wrong_control_passes = 32/32
check_passes = 7/7
wrong_control_passes = 4/4
external_quantum_network_data_used = False
free_parameters_introduced = 0
```

## Benchmark Manifest

| benchmark_id | sealed_object | sealed_value | source_gate |
| --- | --- | --- | --- |
| QN-BENCH-001 | network_object_grammar | carrier=QUBIT-NL-001; envelope=QUBIT-CL-001; sensor=QUBIT-UNK-001 | QN001 |
| QN-BENCH-002 | link_survival_and_viability | link=QN-CARRIER-001; route=QUBIT-NL-001; score=0.06559092722191634 | QN002 |
| QN-BENCH-003 | ledger_safe_relay | surface=ONE_T_SW:N0; relay_score=0.060977389684884344 | QN003 |
| QN-BENCH-004 | paul_revere_routing | route=QUBIT-NL-001; top_score=0.003999561548899118; closed=2 | QN004 |
| QN-BENCH-005 | network_born_surface | top_route=QUBIT-NL-001; top_probability=0.9654196547077734; open=5; closed=2 | QN005 |
| QN-BENCH-006 | letter_safe_error_correction | rules=7; open=5; closed=2 | QN006 |
| QN-BENCH-007 | earth_a_deployment_surface | earth_A=1.390657777567e-09; A_SIDE_fraction=3.3375786661608004e-08; apparatus_controls=7 | QN007 |
| QN-BENCH-008 | forbidden_leakage_invariant | final_ledger_outcome/logical_route_identity forbidden before selected write | QN001-QN007 |

## Checks

| check_id | check | pass | detail |
| --- | --- | --- | --- |
| QN008_CHECK_01 | all QN001-QN007 gates report no external quantum-network data | True | 0 |
| QN008_CHECK_02 | all QN001-QN007 gates report zero free parameters | True | 0 |
| QN008_CHECK_03 | all internal gate checks passed before freeze | True | 40/40 |
| QN008_CHECK_04 | all wrong controls passed before freeze | True | 32/32 |
| QN008_CHECK_05 | benchmark rows exclude external data before manifest | True | 8 |
| QN008_CHECK_06 | formula/rule freeze excludes external data before manifest | True | 7 |
| QN008_CHECK_07 | sealed source hashes are present | True | 14 |

## Wrong Controls

| control_id | wrong_control | expected | actual | pass |
| --- | --- | --- | --- | --- |
| QN008_WC_01 | external benchmark data entered before freeze | False | False | True |
| QN008_WC_02 | free deployment/probability parameters were introduced | False | False | True |
| QN008_WC_03 | forbidden leakage invariant is absent from benchmark manifest | False | False | True |
| QN008_WC_04 | manifest freezes hardware-rate/commercial performance claim | False | False | True |

## Interpretation

QN008 freezes the quantum-network phase-1 package:

```text
QN001 object grammar
QN002 link survival
QN003 ledger-safe relay
QN004 Paul Revere routing
QN005 network Born surface
QN006 real-time letter-safe correction
QN007 Earth-A deployment split
```

The package is now sealed for later external benchmark comparison.

## Outputs

```text
artifacts/qn008/qn008_preflight.md
artifacts/qn008/qn008_input_manifest.csv
artifacts/qn008/sealed_quantum_network_benchmark_manifest.csv
artifacts/qn008/sealed_quantum_network_formula_freeze.csv
artifacts/qn008/sealed_qn_artifact_hash_manifest.csv
artifacts/qn008/external_comparison_exclusion_record.md
artifacts/qn008/qn008_checks.csv
artifacts/qn008/qn008_wrong_controls.csv
artifacts/qn008/qn008_summary.json
artifacts/qn008/qn008_next_frontier.csv
```

## Next Frontier

```text
QN_PHASE1_PRIVATE_PACKAGE_READY_FOR_EXTERNAL_BENCHMARK_REVIEW
```
