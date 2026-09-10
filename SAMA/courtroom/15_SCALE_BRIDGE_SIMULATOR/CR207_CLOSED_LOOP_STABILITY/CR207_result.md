# CR207 Closed-Loop Stability

## Verdict

```text
CR207_BOUNDARY_CLOSED_LOOP_STABILITY
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = BOUNDARY
triage_bin = C
claim_tier = SIMULATOR_CLOSED_LOOP_STABILITY
```

## Question

Can the simulator replay the scale bridge without unexpected type violations?

## Pass Conditions

| condition | pass |
|---|---:|
| engineering_gate_pass | true |
| scientific_boundary_expected | true |
| not_audit_or_retest | true |
| no_courtroom_sources_opened | true |
| no_free_parameters | true |
| unexpected_type_violations_zero | true |
| expected_controls_fire | true |
| all_run_traces_hashed | true |
| type_report_records_zero_unexpected | true |

## Evidence Rows

| key | value | note |
|---|---:|---|
| result_class | PASS_ENGINEERING_G756c_SIMULATOR_CLOSED_LOOP_STABILITY_BOUNDARY_SCIENCE | source G-test result |
| unexpected_type_violations | 0 | closed-loop replay |
| expected_control_breaks | 3 | controls fired by design |
| trace_hash_count | 5 | all run traces hashed |
| run_steps | 5,4,4,4,3 | A through E loop sizes |

## Rule-9 Line

```text
This test could have falsified the claim that the scale bridge can be replayed as a closed loop with all run traces hashed and no unexpected type violations.
```

## Notes

- Boundary is preserved: closed-loop stability is internal simulator discipline, not standalone external validation.
