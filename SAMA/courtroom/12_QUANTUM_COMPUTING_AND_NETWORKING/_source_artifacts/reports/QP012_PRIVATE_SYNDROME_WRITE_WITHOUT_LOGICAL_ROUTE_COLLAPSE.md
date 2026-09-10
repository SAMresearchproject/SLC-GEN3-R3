# QP012 - Private Syndrome Write Without Logical Route Collapse

## Verdict

`QP012_PRIVATE_SYNDROME_WRITE_WITHOUT_LOGICAL_ROUTE_COLLAPSE_BUILT`

QP012 identifies the SAM side-channel used by quantum error correction:

```text
syndrome write = boundary damage information
logical collapse = route identity write
```

The loophole is real in the SAM accounting:

```text
boundary damage can be written while logical route identity remains hidden
```

## Core Rule

```text
allowed syndrome-only write:
  syndrome_probe = 1
  logical_probe = 0
  A_leak < A_SHARE
  share_survival > 0

collapse route:
  logical_probe = 1
  and write_pressure > 0 or A_leak >= A_SHARE
```

## Main Read

```text
syndrome-without-collapse rows = 35
logical-collapse rows = 42
too-late syndrome rows = 14
```

Top no-collapse window:

```text
QUBIT-NL-001
ticks = 2019874.9116810742
```

Fastest closing window:

```text
QUBIT-COLOR-001
ticks = 3.105021696626508
```

## Window Leaders

| Rank | Qubit | Exposure Family | syndrome/no-collapse window ticks |
| ---: | --- | --- | ---: |
| 1 | QUBIT-NL-001 | WEAK_CONTACT_LIMITED | 2019874.91168 |
| 2 | QUBIT-UNK-001 | PARTITION_OCCUPANCY_COUPLED | 53578.8461036 |
| 3 | QUBIT-CL-001 | EM_CONTACT_LIMITED | 18778.865045 |
| 4 | QUBIT-BN-001 | WEAK_CONTACT_LIMITED | 1421.22303376 |
| 5 | QUBIT-TM-001 | EM_CONTACT_LIMITED | 822.215994504 |

## Meaning

QP012 is the measurement loophole in SAM form:

```text
physical interaction can write boundary damage
without writing the protected route identity
```

That is why measurement-like operations can occur during error correction
without collapsing the logical route. The write is real, but it is typed:

```text
boundary syndrome write != logical route write
```

## Outputs

```text
qp012_readout_mode_table.csv
qp012_syndrome_logical_separation_table.csv
qp012_qec_window_table.csv
qp012_summary.json
qp012_next_frontier.csv
```

## Next Frontier

`QP013_PRIVATE_A_CONTACT_SUPPRESSION_TABLE`

QP013 should map cooling, vacuum, shielding, traps, photonics, and QEC to the
specific SAM leakage channels they suppress or control.

Generated at UTC: `2026-06-07T15:32:06.322941+00:00`
