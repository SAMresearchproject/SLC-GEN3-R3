# CR201 Source-To-Field Simulator Bridge

## Verdict

```text
CR201_PASS_SOURCE_TO_FIELD_SIMULATOR_BRIDGE
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = SIMULATOR_SOURCE_TO_FIELD_BRIDGE
```

## Question

Can the source ledger feed field inventory without changing q_A grammar or adding a parameter?

## Pass Conditions

| condition | pass |
|---|---:|
| source_gate_pass | true |
| not_audit_or_retest | true |
| no_free_parameters | true |
| particle_rows_imported | true |
| qa_source_rows_emitted | true |
| qa_source_formula_exact | true |
| source_bridge_within_tolerance | true |
| composite_binding_within_tolerance | true |
| wrong_controls_passed | true |

## Evidence Rows

| key | value | note |
|---|---:|---|
| result_class | PASS_G750c_SOURCE_TO_FIELD_SIMULATOR_BRIDGE | source G-test result |
| particle_rows_imported | 26 | QP075 particle rows imported by G750c |
| source_rows_emitted | 7 | active q_A source rows |
| ratio_spread_fractional | 0.003286777770728273 | must be within declared tolerance |
| wrong_controls | 6/6 | all source-strength controls labeled |

## Rule-9 Line

```text
This test could have falsified the claim that q_A = m * (1 + r_bounce) can bridge particle source rows into field inventory rows with zero new parameters and with the declared wrong controls rejected.
```

## Notes

- Courtroom export reads frozen G750c artifacts and does not overwrite the G750c verdict.
