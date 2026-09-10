# CR027_HYDROGEN_CATCHUP_FIRST_STAR_SCAFFOLD

## Verdict

```text
CR027_PASS_HYDROGEN_CATCHUP_FIRST_STAR_SCAFFOLD
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = PASS_SCOPED_HYDROGEN_CATCHUP_SCAFFOLD
```

## Question

```text
Does the source chain select hydrogen/normal baryons as catch-up material inside a BB-PBH/trapped-A first scaffold?
```

## Pass Conditions

| condition | pass |
|---|---:|
| hydrogen_arrival_selected | true |
| pbh_first_hydrogen_catchup_selected | true |
| pbh_inventory_exceeds_hydrogen_inventory | true |
| seed_first_support_imported | true |
| prediction_rows_complete | true |
| wrong_controls_complete | true |
| full_sfh_overclaim_rejected | true |
| free_parameters_introduced_zero | true |

## Evidence Rows

| item | value | pass |
|---|---:|---:|
| terminal_arrival | neutral_hydrogen_protium | true |
| hot_arrival | proton_electron_plasma | true |
| who_catches_up | hydrogen/normal baryonic matter | true |
| catching_up_to | BB-origin PBH/trapped-A clustered mass scaffold | true |
| g682_selected_route | bb_pbh_trapped_A_first_scaffold_plus_hydrogen_catchup | true |
| pbh_to_hydrogen_ratio | 5.364446416084761 | true |
| g677_gap_closed | 0.8191375474184742 | true |

## Wrong Controls

```text
wrong_control_full_packet_count = 0
```

## Scope

CR027 is a scoped route selector. It says hydrogen catches up inside PBH/trapped-A wells; it does not claim a full star-formation history.

## Rule-9 Line

```text
This test could have falsified: the claim that the current SAM source chain selects BB-origin PBH/trapped-A as first scaffold and hydrogen/normal baryons as catch-up material.
```
