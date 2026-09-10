# CR017 Distance-Road Typed Bridge Closure

## Verdict

```text
CR017_PASS_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = PASS_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE
```

## Closure Packet

```text
CR012 typed bridge
CR013 SN ledger
CR014 BAO ledger
CR015 independent SN/BAO lock
CR016 CMB acoustic ratio
CMB modal/polarization = OPEN_NOT_CLAIMED
```

## Pass Conditions

| condition | pass |
|---|---:|
| no_older_test_verdicts_used | true |
| free_parameters_introduced_zero | true |
| all_dependency_summaries_exist | true |
| all_dependencies_are_local_cr_tests | true |
| all_dependencies_pass | true |
| cmb_modal_polarization_left_open | true |
| wrong_controls_rejected | true |

## Rule-9 Line

```text
This closure test could have falsified the 06 branch if any local CR dependency failed, if a new parameter appeared, if CMB modal or polarization closure was smuggled into the branch, or if a dependency was replaced by an external G verdict instead of a local courtroom result.
```
