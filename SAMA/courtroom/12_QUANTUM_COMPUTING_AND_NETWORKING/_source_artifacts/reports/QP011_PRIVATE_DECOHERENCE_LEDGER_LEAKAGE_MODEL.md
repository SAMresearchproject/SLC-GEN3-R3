# QP011 - Private Decoherence Ledger Leakage Model

## Verdict

`QP011_PRIVATE_DECOHERENCE_LEDGER_LEAKAGE_MODEL_BUILT`

QP011 turns QP010's protected-route law into a decoherence model:

```text
A_leak(N) = N * Gamma_leak
protected_cell_survival = clamp(1 - A_leak/A_SIDE, 0, 1)
share_survival = clamp(1 - A_leak/A_SHARE, 0, 1)
decoherence_pressure = clamp(A_leak/A_SIDE, 0, 1)
write_pressure = clamp((A_leak - A_SIDE)/(A_SHARE - A_SIDE), 0, 1)
```

## Main Read

Decoherence is uncontrolled ledger leakage through the route cell boundary.
It does not require human observation, and it begins before selected write.

```text
A_SIDE = 0.041666666666666664
A_SHARE = 0.08333333333333333
WRITE midpoint = 0.5
```

The strongest protected route remains:

```text
QUBIT-NL-001
ticks to A_SIDE = 1009937.4558405371
ticks to A_SHARE = 2019874.9116810742
```

Fastest leakage route:

```text
QUBIT-COLOR-001
ticks to A_SIDE = 1.552510848313254
```

## Protection Leaders

| Rank | Qubit | Exposure Family | ticks to A_SIDE | one-tick survival |
| ---: | --- | --- | ---: | ---: |
| 1 | QUBIT-NL-001 | WEAK_CONTACT_LIMITED | 1009937.45584 | 0.99999900984 |
| 2 | QUBIT-UNK-001 | PARTITION_OCCUPANCY_COUPLED | 26789.4230518 | 0.999962671835 |
| 3 | QUBIT-CL-001 | EM_CONTACT_LIMITED | 9389.43252248 | 0.999893497291 |
| 4 | QUBIT-BN-001 | WEAK_CONTACT_LIMITED | 710.611516878 | 0.998592761338 |
| 5 | QUBIT-TM-001 | EM_CONTACT_LIMITED | 411.107997252 | 0.997567549144 |

## Meaning

QP011 separates three things that often get blurred:

```text
leakage = uncontrolled A contact through the cell boundary
decoherence = loss of protected unresolved-route survival
measurement = selected Gamma_res write access
```

So decoherence can happen without measurement:

```text
environment contact -> A_leak accumulates -> protected route survival drops
```

## Outputs

```text
qp011_route_leakage_windows.csv
qp011_decoherence_survival_table.csv
qp011_decoherence_class_table.csv
qp011_summary.json
qp011_next_frontier.csv
```

## Next Frontier

`QP012_PRIVATE_SYNDROME_WRITE_WITHOUT_LOGICAL_ROUTE_COLLAPSE`

QP012 should use the leakage model to show how a syndrome write can record
boundary damage while the protected logical route identity remains unresolved.

Generated at UTC: `2026-06-07T15:25:54.334122+00:00`
