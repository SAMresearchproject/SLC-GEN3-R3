# QP017 - Private Stable Mode To Role Operator Bridge

## Verdict

`QP017_PRIVATE_STABLE_MODE_TO_ROLE_OPERATOR_BRIDGE_BUILT`

QP017 maps QP016's selected stable mode and boundary reorganization candidate
back into the QP004 phase role/operator lane.

Core rule:

```text
selected stable self-closure -> role anchor if it touches existing QP004 role neighborhoods
boundary candidate -> role bridge if it connects role/operator neighborhoods
transient tails -> no role promotion
```

## Main Read

```text
route-pair rows = 28
role-lane promotions = 2
stable role anchors = 1
boundary role bridges = 1
transient rejections = 26
free parameters introduced = 0
```

## Promoted Rows

| Rank | Pair | Bridge Class | Role Surface | Bridge Strength |
| ---: | --- | --- | --- | ---: |
| 1 | QUBIT-NL-001<->QUBIT-NL-001 | STABLE_ROLE_ANCHOR_PROMOTED | NEUTRAL_BINARY_MIXING_ROLE_OPERATOR | 0.929656778293 |
| 2 | QUBIT-NL-001<->QUBIT-UNK-001 | CROSS_ROLE_BOUNDARY_REORGANIZATION | anchor/cross-role | 0.0123297319472 |

## Top Bridge Rows

| Rank | Pair | QP016 Class | Role Bridge Class | Promote |
| ---: | --- | --- | --- | --- |
| 1 | QUBIT-NL-001<->QUBIT-NL-001 | STABLE_SELF_CLOSURE_MODE_SELECTED | STABLE_ROLE_ANCHOR_PROMOTED | True |
| 2 | QUBIT-NL-001<->QUBIT-UNK-001 | BOUNDARY_REORGANIZATION_CANDIDATE | CROSS_ROLE_BOUNDARY_REORGANIZATION | True |
| 3 | QUBIT-BN-001<->QUBIT-BN-001 | TRANSIENT_COMMIT_TAIL | TRANSIENT_SELF_CLOSURE_REJECTED | False |
| 4 | QUBIT-BN-001<->QUBIT-COLOR-001 | TRANSIENT_COMMIT_TAIL | TRANSIENT_ROLE_TAIL_REJECTED | False |
| 5 | QUBIT-BN-001<->QUBIT-TM-001 | TRANSIENT_COMMIT_TAIL | TRANSIENT_ROLE_TAIL_REJECTED | False |
| 6 | QUBIT-BN-001<->QUBIT-TP-001 | TRANSIENT_COMMIT_TAIL | TRANSIENT_ROLE_TAIL_REJECTED | False |
| 7 | QUBIT-CL-001<->QUBIT-BN-001 | TRANSIENT_COMMIT_TAIL | TRANSIENT_DIRECT_ROLE_CONTACT_REJECTED | False |
| 8 | QUBIT-CL-001<->QUBIT-CL-001 | TRANSIENT_COMMIT_TAIL | TRANSIENT_SELF_CLOSURE_REJECTED | False |
| 9 | QUBIT-CL-001<->QUBIT-COLOR-001 | TRANSIENT_COMMIT_TAIL | TRANSIENT_DIRECT_ROLE_CONTACT_REJECTED | False |
| 10 | QUBIT-CL-001<->QUBIT-TM-001 | TRANSIENT_COMMIT_TAIL | TRANSIENT_DIRECT_ROLE_CONTACT_REJECTED | False |

## Meaning

The stable mode promotes as a neutral identity anchor:

```text
QUBIT-NL-001<->QUBIT-NL-001
```

The boundary reorganization candidate bridges the neutral identity lane and the
unknown asymmetric lane:

```text
QUBIT-NL-001<->QUBIT-UNK-001
```

So QP017 preserves the split QP016 found:

```text
stable closure anchor
boundary/asymmetric reorganization bridge
transient tails rejected from role promotion
```

## Outputs

```text
qp017_stable_mode_role_operator_bridge.csv
qp017_role_operator_support_summary.csv
qp017_role_bridge_schema.csv
qp017_summary.json
qp017_next_frontier.csv
```

## Next Frontier

`QP018_PRIVATE_ROLE_BRIDGE_TO_PARTICLE_SLOT_SELECTOR`

QP018 should use the promoted stable anchor and boundary reorganization bridge
to select which particle slots are reachable without promoting transient tails.

Generated at UTC: `2026-06-07T16:35:25.660383+00:00`
