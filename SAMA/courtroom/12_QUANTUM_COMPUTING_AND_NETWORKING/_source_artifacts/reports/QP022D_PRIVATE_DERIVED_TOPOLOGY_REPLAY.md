# QP022D - Private Derived-Topology Replay

## Result

```text
QP022D_DERIVED_TOPOLOGY_REPLAY_MATCHES_QP017B
```

QP022D uses QP016 stable/boundary commit classes plus the QP022B/QP022C
derived topology. It does not use QP004 role labels as selector input.

## Replay

| lane | selected pairs | expected replay pairs | matches expected |
| --- | --- | --- | --- |
| stable | QUBIT-NL-001<->QUBIT-NL-001 | QUBIT-NL-001<->QUBIT-NL-001 | True |
| boundary | QUBIT-NL-001<->QUBIT-UNK-001 | QUBIT-NL-001<->QUBIT-UNK-001 | True |
| charged_carrier | QUBIT-CL-001<->QUBIT-TM-001;QUBIT-CL-001<->QUBIT-TP-001 | QUBIT-CL-001<->QUBIT-TM-001;QUBIT-CL-001<->QUBIT-TP-001 | True |

## Key Fields

```text
selected_hub_route = QUBIT-CL-001
selector_used_qp004_labels = False
free_parameters_introduced = 0
stable_replay_matches = True
boundary_replay_matches = True
charged_replay_matches = True
full_replay_matches = True
```

## Interpretation

The Phase 2 topology chain now reaches the old QP017B endpoint without importing
QP004 topology as the selector. CL is selected as hub by QP022B, lanes are
separated by QP022C, and QP022D replays the stable anchor, boundary bridge, and
charged transient-carrier separation from those derived pieces.

## Next Frontier

```text
QP023_PRIVATE_DERIVED_ROLE_TO_PARTICLE_TABLE_FREEZE
```
