# QN010 - Private Approved External Benchmark Comparison

## Result

```text
QN010_EXTERNAL_BENCHMARK_COMPARISON_SELECTED
```

QN010 is the first SAM quantum-network gate that admits external platform
facts after the QN009 comparator schema freeze.

## Main Readout

```text
candidate_platforms = 5
external_sources_used = 8
comparison_rows = 40
strongest_candidate = Qunnect_Cisco_metro_photonic_entanglement_swap
strongest_candidate_match_count = 4
strongest_candidate_partial_count = 4
check_passes = 7/7
wrong_control_passes = 5/5
external_quantum_network_data_used = True
free_parameters_introduced = 0
```

## Candidate Alignment Summary

| candidate_id | candidate_platform | match_count | partial_count | blocker_count | not_reported_count | alignment_class |
| --- | --- | --- | --- | --- | --- | --- |
| QN010-CAND-001 | Qunnect_Cisco_metro_photonic_entanglement_swap | 4 | 4 | 0 | 0 | STRONGEST_QN010_ALIGNMENT |
| QN010-CAND-002 | NIST_trapped_ion_photonic_repeater_node | 3 | 3 | 0 | 2 | PROMISING_PARTIAL_ALIGNMENT |
| QN010-CAND-005 | AWS_memory_repeater_architecture | 1 | 6 | 0 | 1 | ARCHITECTURE_DIRECTION_ALIGNMENT |
| QN010-CAND-003 | QuTech_multi_node_quantum_internet_stack | 1 | 5 | 0 | 2 | ARCHITECTURE_DIRECTION_ALIGNMENT |
| QN010-CAND-004 | IonQ_trapped_ion_photonic_interconnect | 1 | 3 | 0 | 4 | LOW_REPORTED_ALIGNMENT |

## Checks

| check_id | check | pass | detail |
| --- | --- | --- | --- |
| QN010_CHECK_01 | QN009 comparator schema is frozen before external comparison | True | QN009_BENCHMARK_COMPARATOR_SCHEMA_FROZEN |
| QN010_CHECK_02 | every candidate covers every sealed benchmark row | True | 40 rows |
| QN010_CHECK_03 | every comparison row cites known external source IDs | True | 8 sources |
| QN010_CHECK_04 | only frozen QN009 status vocabulary is used | True | NOT_REPORTED;SAM_BLOCKER;SAM_MATCH;SAM_MISS;SAM_PARTIAL |
| QN010_CHECK_05 | no fitted ranking weights or platform scores are introduced | True | count statuses only |
| QN010_CHECK_06 | forbidden leakage screen remains active in external comparison | True | 10 leakage rows |
| QN010_CHECK_07 | at least one candidate reaches strongest alignment without blockers | True | QN010-CAND-001 |

## Wrong Controls

| control_id | wrong_control | expected | actual | pass |
| --- | --- | --- | --- | --- |
| QN010_WC_01 | external platform data entered before QN009 freeze | False | False | True |
| QN010_WC_02 | external source lacks URL provenance | False | False | True |
| QN010_WC_03 | SAM_MATCH status is assigned without external source support | False | False | True |
| QN010_WC_04 | leakage blocker does not force SAM_BLOCKER | False | False | True |
| QN010_WC_05 | fitted numerical platform score is introduced | False | False | True |

## Interpretation

The first external comparison lands where SAM expected:

```text
best current alignment is photonic entanglement over fiber with separated
apparatus controls, relay/orchestration behavior, and no-cloning/measurement
discipline.
```

Qunnect/Cisco-style deployed photonic entanglement swapping is the strongest
QN010 alignment because it simultaneously supplies a flying photonic carrier,
deployed fiber, entanglement swapping, active stabilization, and apparatus
orchestration. Trapped-ion photonic nodes and memory-assisted repeater
architectures are strong supporting lanes because they supply the stationary
node/repeater side of the same SAM network picture.

## Outputs

```text
artifacts/qn010/qn010_preflight.md
artifacts/qn010/qn010_input_manifest.csv
artifacts/qn010/external_quantum_network_source_manifest.csv
artifacts/qn010/candidate_platform_fact_table.csv
artifacts/qn010/candidate_benchmark_comparison.csv
artifacts/qn010/candidate_alignment_summary.csv
artifacts/qn010/qn010_checks.csv
artifacts/qn010/qn010_wrong_controls.csv
artifacts/qn010/qn010_summary.json
artifacts/qn010/qn010_next_frontier.csv
```

## Next Frontier

```text
QN011_PRIVATE_PLATFORM_REQUIREMENT_TO_EXPERIMENTAL_PROTOCOL_TRANSLATION
```
