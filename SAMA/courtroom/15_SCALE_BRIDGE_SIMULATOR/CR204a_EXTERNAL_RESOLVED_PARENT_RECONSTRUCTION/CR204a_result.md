# CR204a External Resolved Parent Reconstruction

## Verdict

```text
CR204a_PASS_EXTERNAL_RESOLVED_PARENT_RECONSTRUCTION
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = EXTERNAL_RESOLVED_PARENT_RECONSTRUCTION_APPEAL
```

## Question

Can CR204's resolved-SW grammar touch a real H -> ZZ* -> 4l parent/daughter/final-state target without changing CR204?

## Pass Conditions

| condition | pass |
|---|---:|
| original_cr204_remains_boundary | true |
| original_cr204_conditions_remain_true | true |
| metadata_manifest_exact_allowed_imports | true |
| external_hzz4l_topology_envelope_present | true |
| external_hzz4l_parent_rows_present | true |
| diphoton_only_row_excluded_as_topology_anchor | true |
| external_z_daughter_row_present | true |
| external_parent_rows_within_declared_band | true |
| external_topology_requires_offshell_daughter | true |
| two_intermediate_branches_present | true |
| four_visible_final_state_grammar_present | true |
| sam_vector_reconstruction_closed | true |
| hidden_budget_separate | true |
| partial_channels_do_not_fake_closure | true |
| no_free_parameters | true |

## Evidence Rows

| key | value | note |
|---|---:|---|
| original_cr204_verdict | BOUNDARY | frozen boundary preserved |
| allowed_import_file_count | 5 | from CR204a metadata manifest |
| external_hzz4l_parent_rows | 2 | CR092 rows accepted by topology envelope |
| excluded_parent_context_rows | 1 | diphoton-only context excluded as HZZ4l topology anchor |
| external_z_daughter_mass_MeV | 91187.6 | CR091 on-shell Z row |
| offshell_Zstar_min_MeV | 33902.399999999994 | external H - external Z |
| offshell_Zstar_max_MeV | 33922.399999999994 | external H - external Z |
| sam_route_event | G753_EVT_B_SCALAR_FOUR_WRITE_ZZSTAR_4L | G753 route selected for HZZ*->4l grammar |
| intermediate_branches | Z_on_shell_branch|Zstar_off_shell_branch | two branch topology |
| final_state_grammar_rows | 2 | 4l/terminal-lepton controls present |
| sam_visible_parent_MeV | 125219.0 | visible invariant parent from CR204 |
| hidden_source_budget_MeV | 125419.11694535677 | tracked separately, not added to visible parent |
| z_precision_debt_status | AGREEMENT_OUTSIDE_DECLARED_BAND | kept separate from parent/daughter topology appeal |

## Rule-9 Line

```text
This test could have falsified the claim that visible resolved-SW parent closure can be externally supported by the Higgs/ZZ*->4l reconstruction topology while preserving CR204's hidden-budget separation and boundary status.
```

## Notes

- CR204 is not relabeled; this is a separate promotion appeal artifact.
- Mass is supporting context; topology closure plus wrong-control rejection is the promotion target.
- The CR091 Z precision residual remains a separate debt and is not hidden by this appeal.
- The CR092 CMS diphoton-only row is retained as parent-mass context but excluded as a direct HZZ4l topology anchor.
- CR092 is a provisional CERN comparison artifact; this appeal inherits that citation state.
