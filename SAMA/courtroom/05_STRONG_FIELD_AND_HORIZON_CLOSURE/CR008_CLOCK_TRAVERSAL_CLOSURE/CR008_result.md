# CR008 Clock Traversal Closure

## Verdict

```text
CR008_BOUNDARY_CLOCK_TRAVERSAL_CLOSURE
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = BOUNDARY
triage_bin = C
claim_tier = BOUNDARY_CLOCK_TRAVERSAL_CLOSURE
```

## Branch Claim Tested

```text
CR007 typed premise: A=1 horizon landmark
lapse(A) = sqrt(1 - A)
redshift(A) = 1/sqrt(1 - A) - 1
outside-ledger radial road: ct/r_s = integral dx/(1 - 1/x)
```

## Pass Conditions

| condition | pass |
|---|---:|
| no_older_test_outputs_used | true |
| sealed_scope_predates_test | true |
| cr007_typed_premise_present | true |
| free_parameters_introduced_zero | true |
| trace_ascii_clean | true |
| low_A_limit_matches_weak_clock | true |
| weak_clock_rejected_at_isco | true |
| redshift_diverges_as_A_to_1 | true |
| lapse_goes_to_zero_as_A_to_1 | true |
| outside_traversal_log_diverges | true |
| closure_at_A1_not_photon_or_isco | true |
| wrong_controls_do_not_match_full_packet | true |
| infalling_observer_overclaim_rejected | true |

## Landmark Clock Values

| landmark | A | exact redshift | weak A/2 |
|---|---:|---:|---:|
| ISCO | 0.333333333333 | 0.224744871392 | 0.166666666667 |
| photon_sphere | 0.666666666667 | 0.732050807569 | N/A |
| horizon | 1.000000000000 | Infinity | N/A |

## Near-Horizon Outside-Ledger Rows

| epsilon | A | lapse | redshift | ct/r_s to x=3 |
|---:|---:|---:|---:|---:|
| 1.0e-03 | 0.999000000000 | 3.162277660168e-02 | 3.062277660168e+01 | 9.599902459542 |
| 1.0e-06 | 0.999999000000 | 1.000000000014e-03 | 9.989999999856e+02 | 16.508656738606 |
| 1.0e-09 | 0.999999999000 | 3.162277615451e-05 | 3.162177704886e+04 | 23.416412933766 |
| 1.0e-12 | 0.999999999999 | 9.999889390788e-07 | 1.000010061044e+06 | 30.324079399857 |

## Wrong Control Summary

```text
wrong_control_full_packet_count = 0
```

## Grade Reading

CR008 structurally validates the outside-ledger clock/traversal closure
behavior at A=1, but remains scientific_verdict=BOUNDARY by sealed design.
It does not claim full infalling-observer physics or full strong-field
metric closure.

## Rule-9 Line

```text
This test could have falsified the claim that the CR007 A=1 horizon landmark is an operational clock/traversal closure boundary under the declared strong-field lane lapse(A)=sqrt(1-A), rather than a label that remains finite or shifts closure to the photon sphere or ISCO.
```
