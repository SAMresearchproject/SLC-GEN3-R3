# QP015 - Private Interference To Ledger Commit Bridge

## Verdict

`QP015_PRIVATE_INTERFERENCE_TO_LEDGER_COMMIT_BRIDGE_BUILT`

QP015 connects QP014 route probabilities to QP003 interference/bounce kernels:

```text
P_ij = P_i^2              for self-pairs
P_ij = 2 * P_i * P_j      for mixed pairs
commit_weight_ij = P_ij * bounce_kernel_ij * ledger_kernel_ij
P_commit_ij = commit_weight_ij / sum(commit_weight_all_pairs)
```

## Main Read

```text
bridge rows = 1176
sample summary rows = 42
normalization failures = 0
top latest-open commit pair = QUBIT-NL-001<->QUBIT-NL-001
top latest-open commit probability = 0.9296567782925111
free parameters introduced = 0
```

## Commit Surface

| QP014 sample | top commit pair through N_A_SHARE | top commit P | P sum |
| --- | --- | ---: | ---: |
| A_SIDE_BOUNDARY | QUBIT-NL-001<->QUBIT-NL-001 | 0.929656778293 | 1 |
| MID_A_SIDE_TO_A_SHARE | QUBIT-NL-001<->QUBIT-NL-001 | 0.929656778293 | 1 |

## Latest Open N_A_SHARE Commit Rows

| QP014 sample | pair | commit P | commit weight |
| --- | --- | ---: | ---: |
| MID_A_SIDE_TO_A_SHARE | QUBIT-NL-001<->QUBIT-NL-001 | 0.929656778293 | 0.929656778293 |
| MID_A_SIDE_TO_A_SHARE | QUBIT-NL-001<->QUBIT-UNK-001 | 0.0493189277889 | 0.0493189277889 |
| MID_A_SIDE_TO_A_SHARE | QUBIT-NL-001<->QUBIT-CL-001 | 0.0172852071805 | 0.0172852071805 |
| MID_A_SIDE_TO_A_SHARE | QUBIT-NL-001<->QUBIT-BN-001 | 0.0013073290985 | 0.0013073290985 |
| MID_A_SIDE_TO_A_SHARE | QUBIT-NL-001<->QUBIT-TM-001 | 0.000755937300163 | 0.000755937300163 |
| MID_A_SIDE_TO_A_SHARE | QUBIT-UNK-001<->QUBIT-UNK-001 | 0.000654100710888 | 0.000654100710888 |
| MID_A_SIDE_TO_A_SHARE | QUBIT-UNK-001<->QUBIT-CL-001 | 0.000458496030285 | 0.000458496030285 |

## Meaning

QP014 supplied the unresolved route probability surface. QP003 supplied the
interference, bounce, and ledger kernels. QP015 shows how those combine into a
ledger-intersection probability:

```text
unresolved probability
-> pair probability
-> bounce response
-> committed ledger intersection candidate
```

The probability surface exists before commit. The bounce/ledger kernel decides
when that surface can become a written intersection.

## Outputs

```text
qp015_interference_commit_bridge_table.csv
qp015_sample_commit_summary.csv
qp015_commit_bridge_schema.csv
qp015_summary.json
qp015_next_frontier.csv
```

## Next Frontier

`QP016_PRIVATE_LEDGER_COMMIT_TO_STABLE_MODE_SELECTOR`

QP016 should ask which committed intersections become stable matter-like modes
rather than transient writes.

Generated at UTC: `2026-06-07T16:15:01.587801+00:00`
