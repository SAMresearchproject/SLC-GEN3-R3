# CR202 Typed Readout Reproduction

## Verdict

```text
CR202_PASS_TYPED_READOUT_REPRODUCTION
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = SIMULATOR_TYPED_READOUT
```

## Question

Can field readouts stay typed across mass ledger, q_A direct, force, and clock lanes?

## Pass Conditions

| condition | pass |
|---|---:|
| readout_gate_pass | true |
| not_audit_or_retest | true |
| no_free_parameters | true |
| readout_rows_present | true |
| all_recompute_errors_zero | true |
| typed_lanes_separated | true |
| species_mix_spread_within_tolerance | true |
| wrong_controls_passed | true |

## Evidence Rows

| key | value | note |
|---|---:|---|
| result_class | PASS_G751c_TYPED_READOUT_REPRODUCTION_FROM_QA_SOURCES | source G-test result |
| readout_rows | 6 | typed readout rows |
| max_recompute_error | 0.0 | mass/q_A/force/clock recomputation |
| typed_lane_status_rows | 6 | rows explicitly reporting separated lanes |
| wrong_controls | 5/5 | all lane-mixing controls passed |

## Rule-9 Line

```text
This test could have falsified the claim that typed field readouts reproduce mass-ledger A, q_A-direct A, force, and clock lanes without lane mixing or species retuning.
```

## Notes

- Courtroom export reads frozen G751c artifacts and does not tune by species.
