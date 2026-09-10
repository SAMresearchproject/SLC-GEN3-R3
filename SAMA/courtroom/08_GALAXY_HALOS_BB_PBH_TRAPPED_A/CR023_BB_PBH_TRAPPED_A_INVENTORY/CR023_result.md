# CR023_BB_PBH_TRAPPED_A_INVENTORY

## Verdict

```text
CR023_BOUNDARY_BB_PBH_TRAPPED_A_INVENTORY_CHAIN
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = BOUNDARY
triage_bin = B
claim_tier = INVENTORY_CHAIN_SUPPORT_FOR_HALO_BRANCH
```

## Question

```text
Does the current source chain preserve BB-origin PBH/trapped-A as the dark halo inventory lane while rejecting post-BB-only PBH as the full halo source?
```

## Pass Conditions

| condition | pass |
|---|---:|
| inventory_sums_to_one | true |
| bb_pbh_inventory_matches_halo_lane | true |
| bb_pbh_inventory_dominates_hydrogen_arrival | true |
| post_bb_window_not_enough_for_full_halo | true |
| halo_inventory_reading_declared | true |
| free_parameters_introduced_zero | true |

## Evidence Rows

| item | value | pass |
|---|---:|---:|
| total_inventory | 1.0 | true |
| omega_pbh_matches_g394 | 0.26446190430295646 | true |
| omega_pbh_exceeds_hydrogen | 5.364446416084761 | true |
| post_bb_subchannel_small | 0.02576714268055339 | true |
| pbh_halo_reading | BB-origin PBH/trapped-A is the dark halo inventory lane | true |

## Wrong Controls

```text
wrong_control_full_packet_count = 0
```

## Scope

CR023 is an inventory-chain support test. It preserves the distinction between BB-origin trapped-A inventory and the smaller post-BB/window PBH subchannel.

## Rule-9 Line

```text
This test could have falsified: the claim that BB-origin PBH/trapped-A, not the bounded post-BB PBH window alone, is the current SAM halo inventory lane.
```
