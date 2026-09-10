# CR205 Scalar/Gauge/Fermion Lane Separation

## Verdict

```text
CR205_PASS_SCALAR_GAUGE_FERMION_LANE_SEPARATION
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = SIMULATOR_TYPED_LANE_SEPARATION
```

## Question

Can scalar 9/16 stay lane-specific rather than becoming a universal particle multiplier?

## Pass Conditions

| condition | pass |
|---|---:|
| lane_gate_pass | true |
| not_audit_or_retest | true |
| no_free_parameters | true |
| scalar_half_is_9_16 | true |
| scalar_expression_is_D3 | true |
| fermions_degrade_under_forced_9_16 | true |
| fermions_degrade_under_forced_16_9 | true |
| gauge_rows_held | true |
| higgs_scalar_owner_confirmed | true |
| wrong_controls_passed | true |

## Evidence Rows

| key | value | note |
|---|---:|---|
| result_class | PASS_G754c_SCALAR_GAUGE_FERMION_LANE_SEPARATION | source G-test result |
| derived_scalar_half | 0.5625 | D=3 scalar lane |
| fermion_rows_checked | 6 | fermion controls degrade under scalar multipliers |
| gauge_rows_held | 2 | gauge owners separated |
| wrong_controls | 8/8 | all lane-separation controls passed |

## Rule-9 Line

```text
This test could have falsified the claim that 9/16 is a D=3 scalar-lane structure and not a universal multiplier for fermion or gauge rows.
```

## Notes

- This is a scoped lane-separation result, not a new particle-mass fit.
