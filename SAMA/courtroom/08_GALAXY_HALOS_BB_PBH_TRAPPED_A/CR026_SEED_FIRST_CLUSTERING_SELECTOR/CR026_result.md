# CR026_SEED_FIRST_CLUSTERING_SELECTOR

## Verdict

```text
CR026_PASS_SEED_FIRST_CLUSTERING_SELECTOR_CANDIDATE
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = PASS_SEED_FIRST_PROFILE_BEHAVIOR_CANDIDATE
```

## Question

```text
Does the seed-first clustering test select a native base-12 BB-PBH scaffold behavior while rejecting uniform-cosmic and post-BB-only controls?
```

## Pass Conditions

| condition | pass |
|---|---:|
| seed_first_primary_candidate_native_base12 | true |
| seed_first_closes_most_baryon_to_profile_gap | true |
| uniform_control_rejected | true |
| post_bb_window_only_control_rejected | true |
| comparison_candidate_recorded_not_selected_by_target | true |
| wrong_controls_rejected_upstream | true |
| open_mass_normalization_and_native_law_preserved | true |
| free_parameters_introduced_zero | true |

## Evidence Rows

| item | value | pass |
|---|---:|---:|
| primary_candidate_id | base12_outer_radius_over_12 | true |
| primary_gap_closed | 0.8191375474184742 | true |
| uniform_gap_closed | 3.8495994978147876e-05 | true |
| post_bb_gap_closed | 0.02448481593940179 | true |
| best_candidate_gap_closed | 0.8625828787369356 | true |

## Wrong Controls

```text
wrong_control_full_packet_count = 0
```

## Scope

CR026 is a profile-behavior candidate test. It supports PBH-first clustering but does not derive the native mass function, abundance normalization, or concentration law.

## Rule-9 Line

```text
This test could have falsified: the claim that BB-origin PBH/trapped-A seed-first clustering explains most of the baryon-to-clustered-halo gap while wrong controls fail.
```
