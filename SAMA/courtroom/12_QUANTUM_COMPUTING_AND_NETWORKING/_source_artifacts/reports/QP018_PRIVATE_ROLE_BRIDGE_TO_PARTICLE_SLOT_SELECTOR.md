# QP018 - Private Role Bridge To Particle Slot Selector

## Verdict

`QP018_PRIVATE_ROLE_BRIDGE_TO_PARTICLE_SLOT_SELECTOR_BUILT`

QP018 applies QP017's promoted role surfaces to the existing private particle
slot tables from QP006 and QP008.

Core rule:

```text
stable role anchor + QP008 selected slot -> stable particle-slot promotion
boundary role bridge + QP008 selected slot -> reorganization particle-slot promotion
reachable role family + no QP008 selection -> held open
selected slot outside QP017 bridge -> preserved outside this gate
```

## Main Read

```text
slot rows = 12
qp017 reachable role-family slots = 6
particle slot promotions = 2
stable anchor slot promotions = 1
boundary reorganization slot promotions = 1
held-open reachable slots = 4
free parameters introduced = 0
```

## Promoted Particle Slots

| Rank | Pair | Role | Selector Class | Score |
| --- | --- | --- | --- | --- |
| 1 | b<->s | NEUTRAL_BINARY_MIXING_ROLE_OPERATOR | STABLE_ANCHOR_SLOT_SELECTED | 0.0789833727906 |
| 2 | c<->s | TRANSITION_COLOR_COUPLED_ROLE_OPERATOR | BOUNDARY_REORGANIZATION_SLOT_SELECTED | 0.00311292426395 |

## Top Selector Rows

| Rank | Pair | Role | QP017 Surface | Selector Class | Promote |
| --- | --- | --- | --- | --- | --- |
| 1 | b<->s | NEUTRAL_BINARY_MIXING_ROLE_OPERATOR | STABLE_ROLE_ANCHOR | STABLE_ANCHOR_SLOT_SELECTED | True |
| 2 | c<->s | TRANSITION_COLOR_COUPLED_ROLE_OPERATOR | BOUNDARY_ROLE_BRIDGE | BOUNDARY_REORGANIZATION_SLOT_SELECTED | True |
| 3 | c<->t | NEUTRAL_BINARY_MIXING_ROLE_OPERATOR | STABLE_ROLE_ANCHOR | ROLE_FAMILY_REACHABLE_HELD_OPEN | False |
| 4 | c<->u | NEUTRAL_BINARY_MIXING_ROLE_OPERATOR | STABLE_ROLE_ANCHOR | ROLE_FAMILY_REACHABLE_HELD_OPEN | False |
| 5 | b<->d | NEUTRAL_BINARY_MIXING_ROLE_OPERATOR | STABLE_ROLE_ANCHOR | ROLE_FAMILY_REACHABLE_HELD_OPEN | False |
| 6 | t<->u | NEUTRAL_BINARY_MIXING_ROLE_OPERATOR | STABLE_ROLE_ANCHOR | ROLE_FAMILY_REACHABLE_HELD_OPEN | False |
| 7 | b<->c | DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR | OUTSIDE_QP017_PROMOTED_SURFACE | QP008_SELECTED_OUTSIDE_QP017_BRIDGE | False |
| 8 | b<->t | DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR | OUTSIDE_QP017_PROMOTED_SURFACE | QP008_SELECTED_OUTSIDE_QP017_BRIDGE | False |
| 9 | b<->u | DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR | OUTSIDE_QP017_PROMOTED_SURFACE | NOT_REACHED_BY_QP017_BRIDGE | False |
| 10 | c<->d | DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR | OUTSIDE_QP017_PROMOTED_SURFACE | NOT_REACHED_BY_QP017_BRIDGE | False |

## Role Family Summary

| Role | QP017 Surface | Slots | Promoted | Top Slot |
| --- | --- | --- | --- | --- |
| DUAL_POLARITY_CHARGED_HEAVY_ROLE_OPERATOR | OUTSIDE_QP017_PROMOTED_SURFACE | 6 | 0 | b<->c |
| NEUTRAL_BINARY_MIXING_ROLE_OPERATOR | STABLE_ROLE_ANCHOR | 5 | 1 | b<->s |
| TRANSITION_COLOR_COUPLED_ROLE_OPERATOR | BOUNDARY_ROLE_BRIDGE | 1 | 1 | c<->s |

## Meaning

QP018 turns the QP017 bridge into a particle-slot selector.

The first stable anchor slot is:

```text
b<->s
```

The boundary/reorganization slot is:

```text
c<->s
```

This gives QP018 a clean next surface:

```text
stable neutral anchor slot
asymmetric transition/reorganization slot
reachable but held-open role families
selected charged slots preserved outside the QP017 bridge
```

## Outputs

```text
qp018_role_bridge_particle_slot_selector.csv
qp018_slot_family_summary.csv
qp018_schema.csv
qp018_summary.json
qp018_next_frontier.csv
```

## Next Frontier

`QP019_PRIVATE_PARTICLE_SLOT_TO_NATIVE_MASS_SURFACE_BRIDGE`

QP019 should use the QP018 selected slot pair to connect the stable anchor and
boundary/reorganization slot to native mass-surface readouts.

Generated at UTC: `2026-06-07T16:41:54.418731+00:00`
