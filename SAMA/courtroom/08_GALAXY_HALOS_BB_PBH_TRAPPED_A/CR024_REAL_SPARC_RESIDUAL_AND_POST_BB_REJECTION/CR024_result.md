# CR024_REAL_SPARC_RESIDUAL_AND_POST_BB_REJECTION

## Verdict

```text
CR024_PASS_REAL_SPARC_RESIDUAL_POST_BB_ONLY_REJECTED
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = PASS_REAL_DATA_HALO_RESIDUAL_AND_CONTROL_REJECTION
```

## Question

```text
Does real SPARC data show a large outer halo residual while the post-BB-only PBH envelope remains far too small to be the full halo source?
```

## Pass Conditions

| condition | pass |
|---|---:|
| real_sparc_external_anchor_present | true |
| large_real_sparc_sample_loaded | true |
| outer_dark_residual_detected | true |
| post_bb_only_control_rejected_as_full_halo | true |
| wrong_controls_rejected_upstream | true |
| free_parameters_introduced_zero | true |

## Evidence Rows

| item | value | pass |
|---|---:|---:|
| sparc_galaxies | 175 | true |
| sparc_points | 3391 | true |
| median_outer_dark_fraction_v2 | 0.760699023482704 | true |
| post_bb_envelope_supplied_pct_dark_residual | 2.576714268055339 | true |
| missing_after_pbh_envelope_pct_dark_residual | 97.42328573194466 | true |

## Wrong Controls

```text
wrong_control_full_packet_count = 0
```

## Scope

CR024 is a real-data contact test. It does not close the full radial halo law; it locks the SPARC residual and rejects the post-BB-only control as a full-halo explanation.

## Rule-9 Line

```text
This test could have falsified: the claim that SPARC rotation data leaves a large halo residual and that the bounded post-BB/window PBH envelope is insufficient as the complete source.
```
