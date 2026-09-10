# CR204 Resolved-SW Parent Reconstruction

## Verdict

```text
CR204_BOUNDARY_RESOLVED_SW_PARENT_RECONSTRUCTION
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = BOUNDARY
triage_bin = C
claim_tier = SIMULATOR_RESOLVED_SW_PARENT_RECONSTRUCTION
```

## Question

Can resolved daughter-write closure reconstruct a parent while keeping full SW/source budget hidden?

## Pass Conditions

| condition | pass |
|---|---:|
| engineering_gate_pass | true |
| scientific_boundary_expected | true |
| not_audit_or_retest | true |
| no_free_parameters | true |
| hidden_budget_separate | true |
| multiple_scalar_channels_same_parent | true |
| partial_channels_do_not_fake_closure | true |
| closed_rows_zero_residual | true |
| wrong_controls_passed | true |

## Evidence Rows

| key | value | note |
|---|---:|---|
| result_class | PASS_ENGINEERING_G753c_RESOLVED_SW_PARENT_RECONSTRUCTION_BOUNDARY_SCIENCE | source G-test result |
| visible_parent_MeV | 125219.0 | visible invariant parent |
| hidden_source_budget_MeV | 125419.11694535677 | tracked separately |
| closed_rows | 3 | zero-residual visible closures |
| wrong_controls | 7/7 | full-SW/direct-hidden controls rejected |

## Rule-9 Line

```text
This test could have falsified the claim that visible resolved-SW parent closure is reconstructed from daughter-write lanes while hidden/source bounce budget remains separate from visible invariant mass.
```

## Notes

- Boundary is preserved intentionally: this is structural reconstruction, not standalone external discovery.
