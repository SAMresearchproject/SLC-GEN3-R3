# CR208 Wrong-Control Zipper And Branch Verdict

## Verdict

```text
CR208_PASS_SCALE_BRIDGE_SIMULATOR_WRONG_CONTROL_ZIPPER
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = SIMULATOR_BRANCH_VERDICT
```

## Question

Does the scale bridge survive the full wrong-control zipper without overwriting individual gate verdicts?

## Pass Conditions

| condition | pass |
|---|---:|
| zipper_gate_pass | true |
| not_audit_or_retest | true |
| no_courtroom_export_performed_upstream | true |
| no_free_parameters | true |
| all_controls_passed | true |
| controls_fire_or_degrade | true |
| honest_diagnostic_preserved | true |
| failed_controls_zero | true |
| families_complete | true |
| claim_file_contains_scale_bridge | true |
| honest_negatives_file_present | true |

## Evidence Rows

| key | value | note |
|---|---:|---|
| result_class | PASS_G757c_FULL_SCALE_BRIDGE_WRONG_CONTROLS_ZIPPER | source G-test result |
| total_controls | 43 | wrong-control zipper size |
| controls_passed | 43 | all controls passed |
| controls_fired_or_degraded | 42 | controls actually broke/degraded the wrong route |
| honest_diagnostics | 1 | diagnostic retained, not hidden |
| failed_controls | 0 | must be zero |

## Rule-9 Line

```text
This test could have falsified the claim that the scale bridge survived a full wrong-control zipper with 43/43 controls passed, no failed controls, and individual gate verdicts preserved.
```

## Notes

- CR204 and CR207 remain BOUNDARY by design while CR208 records the branch-level wrong-control PASS.
- The branch strongest claim is imported from G757c and hash-anchored here.
