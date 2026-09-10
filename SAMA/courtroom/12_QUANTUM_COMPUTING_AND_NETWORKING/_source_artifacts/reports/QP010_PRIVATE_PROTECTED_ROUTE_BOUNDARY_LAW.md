# QP010 - Private Protected Route Boundary Law

## Verdict

`QP010_PRIVATE_PROTECTED_ROUTE_BOUNDARY_LAW_BUILT`

QP010 turns quantum-computing protection evidence into a SAM-native unresolved
route law:

```text
A_leak(N) = N * Gamma_leak
protected route: A_leak < A_SIDE = 1/24
write candidate: A_SIDE <= A_leak < A_SHARE = 1/12
resolution accessible: A_leak >= A_SHARE
```

## Main Read

The ledger-cell picture sharpens the quantum phase lane:

```text
qubit = protected unresolved route inside a ledger cell
decoherence = uncontrolled A leakage through the cell boundary
measurement = selected A-resolution
QEC syndrome = boundary damage write without logical route collapse
```

No free parameters were introduced. QP010 uses the existing route exposure
rates from the private phase-field table and the existing R=12 thresholds.

## Protection Leaders

| Rank | Qubit | Exposure Family | ticks to A_SIDE | Status |
| ---: | --- | --- | ---: | --- |
| 1 | QUBIT-NL-001 | WEAK_CONTACT_LIMITED | 1009937.45584 | PROTECTED_UNRESOLVED_ROUTE |
| 2 | QUBIT-UNK-001 | PARTITION_OCCUPANCY_COUPLED | 26789.4230518 | PROTECTED_UNRESOLVED_ROUTE |
| 3 | QUBIT-CL-001 | EM_CONTACT_LIMITED | 9389.43252248 | PROTECTED_UNRESOLVED_ROUTE |
| 4 | QUBIT-BN-001 | WEAK_CONTACT_LIMITED | 710.611516878 | PROTECTED_UNRESOLVED_ROUTE |
| 5 | QUBIT-TM-001 | EM_CONTACT_LIMITED | 411.107997252 | PROTECTED_UNRESOLVED_ROUTE |

## Modality Alignment

| Organization | Modality | SAM Fit | Score |
| --- | --- | --- | ---: |
| IBM Quantum | superconducting | ENGINEERED_MACRO_PHASE_CELL_FIT | 17 |
| Quantinuum | trapped ion | DIRECT_ROUTE_ISOLATION_FIT | 16 |
| Google Quantum AI | superconducting | ENGINEERED_MACRO_PHASE_CELL_FIT | 15 |
| Atom Computing / Microsoft neutral-atom lane | neutral atom | DIRECT_ROUTE_ISOLATION_FIT | 14 |
| QuEra | neutral atom | DIRECT_ROUTE_ISOLATION_FIT | 13 |

## Outputs

```text
qp010_contact_channel_table.csv
qp010_qubit_protection_table.csv
qp010_modality_alignment_table.csv
qp010_ledger_cell_mapping.csv
qp010_protected_route_boundary_summary.json
qp010_next_frontier.csv
```

## Next Frontier

`QP011_PRIVATE_DECOHERENCE_LEDGER_LEAKAGE_MODEL`

QP011 should turn this boundary law into a decoherence model:

```text
decoherence rate = uncontrolled ledger leakage rate
logical survival = protected route weight left before Gamma_res selection
```

Generated at UTC: `2026-06-07T15:14:31.235697+00:00`
