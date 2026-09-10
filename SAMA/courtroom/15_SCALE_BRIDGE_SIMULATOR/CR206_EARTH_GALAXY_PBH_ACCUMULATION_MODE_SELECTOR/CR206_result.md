# CR206 Earth/Galaxy/PBH Accumulation Mode Selector

## Verdict

```text
CR206_PASS_EARTH_GALAXY_PBH_ACCUMULATION_MODE_SELECTOR
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = SIMULATOR_ACCUMULATION_MODE_SELECTOR
```

## Question

Can local Earth A, galaxy many-nonzero A, clustered BB-PBH scaffold, and PBH cumulative nonzeros remain typed?

## Pass Conditions

| condition | pass |
|---|---:|
| accumulation_gate_pass | true |
| not_audit_or_retest | true |
| no_courtroom_sources_opened | true |
| no_free_parameters | true |
| earth_local_A_forward_present | true |
| baryon_many_nonzero_cumulative_present | true |
| clustered_BB_PBH_scaffold_present | true |
| pbh_many_nonzero_present | true |
| galaxy_statuses_complete | true |
| mode_report_present | true |
| wrong_controls_passed | true |

## Evidence Rows

| key | value | note |
|---|---:|---|
| result_class | PASS_G755c_EARTH_GALAXY_PBH_ACCUMULATION_MODE_SELECTOR | source G-test result |
| earth_A_local_forward | 0.026530964987239263 | local compact lane |
| baryon_many_nonzero_A_cumulative | 1.914163e-07 | many stellar nonzeros |
| Omega_BB_PBH_trapped | 0.26446190430295646 | clustered BB-PBH/trapped-A inventory |
| pbh_cumulative_nonzero_proxy_median | 0.2039506172839506 | PBH many-nonzero lane |
| wrong_controls | 8/8 | uniform/PBH-only/baryon-only controls rejected |

## Rule-9 Line

```text
This test could have falsified the claim that galaxy halo support is typed as baryon many-nonzero A plus clustered BB-PBH/trapped-A scaffold plus PBH many-nonzero accumulation, distinct from Earth local A.
```

## Notes

- This explicitly includes cumulative nonzero A from PBH as requested.
