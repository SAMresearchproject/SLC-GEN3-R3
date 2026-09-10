# CR007 Strong-Field Landmark Selector

## Verdict

```text
CR007_BOUNDARY_STRONG_FIELD_LANDMARK_SELECTOR
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = BOUNDARY
triage_bin = C
claim_tier = STRUCTURAL_LANDMARK_ROOT
```

## Branch Claim Tested

```text
A(r) = r_s/r
horizon        r/r_s = 1   -> A = 1
photon sphere  r/r_s = 3/2 -> A = 2/3
ISCO           r/r_s = 3   -> A = 1/3
```

## Pass Conditions

| condition | pass |
|---|---:|
| no_older_test_outputs_used | true |
| sealed_scope_predates_test | true |
| free_parameters_introduced_zero | true |
| trace_ascii_clean | true |
| sam_landmark_tuple_exact | true |
| landmark_order_preserved | true |
| mass_scale_invariance | true |
| wrong_controls_do_not_match_full_packet | true |
| empirical_overclaim_rejected | true |

## SAM Landmark Rows

| landmark | r/r_s | candidate A | target A | absolute error |
|---|---:|---:|---:|---:|
| horizon | 1.000000000000 | 1.000000000000 | 1.000000000000 | 0.000e+00 |
| photon_sphere | 1.500000000000 | 0.666666666667 | 0.666666666667 | 0.000e+00 |
| isco | 3.000000000000 | 0.333333333333 | 0.333333333333 | 0.000e+00 |

## Mass-Scale Invariance

| quantity | spread |
|---|---:|
| horizon_A_spread | 0.000e+00 |
| photon_sphere_A_spread | 1.110e-16 |
| isco_A_spread | 5.551e-17 |

## Wrong Control Summary

```text
wrong_control_full_packet_count = 0
```

## Grade Reading

CR007 structurally succeeds as the 05-branch landmark root, but it remains
scientific_verdict=BOUNDARY by sealed design. The test does not claim broad
external strong-field closure. CR008-CR010 may later provide deferred support
through declared downstream tests.

## Rule-9 Line

```text
This test could have falsified the claim that SAM's strong-field root A(r)=r_s/r places the horizon, photon sphere, and ISCO at the ordered native A-values 1, 2/3, and 1/3 without a new parameter or a landmark-specific rule.
```
