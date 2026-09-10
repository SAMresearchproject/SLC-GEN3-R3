# QP016 - Private Ledger Commit To Stable Mode Selector

## Verdict

`QP016_PRIVATE_LEDGER_COMMIT_TO_STABLE_MODE_SELECTOR_BUILT`

QP016 asks which committed ledger intersections survive as stable modes.

Selector law:

```text
stable selected mode:
  self-pair
  latest P_commit >= A_SHARE
  persistence across structured commit rows >= A_SIDE

boundary reorganization candidate:
  latest P_commit >= A_SIDE
  persistence across structured commit rows >= A_SIDE
  but not selected self-closure

transient commit tail:
  latest P_commit < A_SIDE
```

No new thresholds are introduced:

```text
A_SIDE = 0.041666666666666664
A_SHARE = 0.08333333333333333
```

## Main Read

```text
route pairs = 28
stable selected modes = 1
boundary reorganization candidates = 1
transient commit tails = 26
top stable mode = QUBIT-NL-001<->QUBIT-NL-001
top stable mode probability = 0.9296567782925111
free parameters introduced = 0
```

## Selected Stable Mode

```text
QUBIT-NL-001<->QUBIT-NL-001  P_commit=0.929656778293
```

## Boundary Reorganization Candidates

```text
QUBIT-NL-001<->QUBIT-UNK-001  P_commit=0.0493189277889
```

## Top Selector Rows

| Rank | Pair | Selector Class | latest P_commit | native persistence | stability index |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | QUBIT-NL-001<->QUBIT-NL-001 | STABLE_SELF_CLOSURE_MODE_SELECTED | 0.929656778293 | 1 | 0.929656778293 |
| 2 | QUBIT-NL-001<->QUBIT-UNK-001 | BOUNDARY_REORGANIZATION_CANDIDATE | 0.0493189277889 | 1 | 0.0246594638945 |
| 3 | QUBIT-BN-001<->QUBIT-BN-001 | TRANSIENT_COMMIT_TAIL | 4.59607623934e-07 | 0 | 0 |
| 4 | QUBIT-BN-001<->QUBIT-COLOR-001 | TRANSIENT_COMMIT_TAIL | 1.75846350755e-09 | 0 | 0 |
| 5 | QUBIT-BN-001<->QUBIT-TM-001 | TRANSIENT_COMMIT_TAIL | 5.31518110887e-07 | 0 | 0 |
| 6 | QUBIT-BN-001<->QUBIT-TP-001 | TRANSIENT_COMMIT_TAIL | 2.74750256816e-07 | 0 | 0 |
| 7 | QUBIT-CL-001<->QUBIT-BN-001 | TRANSIENT_COMMIT_TAIL | 1.21536543638e-05 | 0 | 0 |
| 8 | QUBIT-CL-001<->QUBIT-CL-001 | TRANSIENT_COMMIT_TAIL | 8.03464230692e-05 | 0 | 0 |
| 9 | QUBIT-CL-001<->QUBIT-COLOR-001 | TRANSIENT_COMMIT_TAIL | 2.32500034476e-08 | 0 | 0 |
| 10 | QUBIT-CL-001<->QUBIT-TM-001 | TRANSIENT_COMMIT_TAIL | 7.0276112399e-06 | 0 | 0 |

## Meaning

QP015 said a ledger intersection can be committed. QP016 adds the next filter:

```text
commit is not enough
stable mode requires self-closure plus native-strength persistence
```

That produces a clean split:

```text
stable closure mode
boundary/asymmetric reorganization candidate
transient commit tail
```

## Outputs

```text
qp016_stable_mode_selector_table.csv
qp016_mode_family_summary.csv
qp016_stability_selector_schema.csv
qp016_summary.json
qp016_next_frontier.csv
```

## Next Frontier

`QP017_PRIVATE_STABLE_MODE_TO_ROLE_OPERATOR_BRIDGE`

QP017 should connect selected stable modes and boundary reorganization
candidates back to the phase role/operator lane.

Generated at UTC: `2026-06-07T16:25:03.265201+00:00`
