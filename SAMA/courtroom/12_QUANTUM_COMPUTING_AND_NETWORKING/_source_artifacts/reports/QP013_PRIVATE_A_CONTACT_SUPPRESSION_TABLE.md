# QP013 - Private A-Contact Suppression Table

## Verdict

`QP013_PRIVATE_A_CONTACT_SUPPRESSION_TABLE_BUILT`

QP013 converts the pre-resolution syndrome letter into a contact-control law:

```text
required suppression to restore A_SIDE = 1 - A_SIDE / A_leak
```

The letter does not need the final logical outcome. It needs to report enough
boundary pressure to say:

```text
this route is approaching uncontrolled write access
reduce contact before A_SHARE
```

## Main Read

```text
contact rows = 49
active suppression rows = 14
passive monitor rows = 21
too-late rows = 14
max sampled required suppression = 0.33333333333333337
native ceiling before A_SHARE = 0.5
```

Control-class counts:

```text
ACTIVE_A_CONTACT_SUPPRESSION_WINDOW = 14
NO_COLLAPSE_WINDOW_CLOSED = 14
PASSIVE_SYNDROME_MONITORING = 21
```

## Control Leaders

| Rank | Qubit | Exposure Family | active rows | max required suppression | max letter lead |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | QUBIT-NL-001 | WEAK_CONTACT_LIMITED | 2 | 0.333333333333 | 2019873.91168 |
| 2 | QUBIT-UNK-001 | PARTITION_OCCUPANCY_COUPLED | 2 | 0.333333333333 | 53577.8461036 |
| 3 | QUBIT-CL-001 | EM_CONTACT_LIMITED | 2 | 0.333333333333 | 18777.865045 |
| 4 | QUBIT-BN-001 | WEAK_CONTACT_LIMITED | 2 | 0.333333333333 | 1420.22303376 |
| 5 | QUBIT-TM-001 | EM_CONTACT_LIMITED | 2 | 0.333333333333 | 821.215994504 |
| 6 | QUBIT-TP-001 | EM_CONTACT_LIMITED | 2 | 0.333333333333 | 424.499750375 |
| 7 | QUBIT-COLOR-001 | SUPPORT_COUPLED | 2 | 0.333333333333 | 2.71689398455 |

## Meaning

Cooling, vacuum, shielding, traps, isolation, and syndrome-only QEC all point to
the same SAM action:

```text
reduce uncontrolled A-contact
preserve the unresolved route
delay logical route identity write until selected resolution
```

QP013 sharpens the loophole:

```text
the system can receive a warning letter before collapse
and use it to suppress the contact channel that would cause collapse
```

## Outputs

```text
qp013_contact_suppression_table.csv
qp013_route_control_window_table.csv
qp013_suppression_strategy_table.csv
qp013_summary.json
qp013_next_frontier.csv
```

## Next Frontier

`QP014_PRIVATE_BORN_RULE_ROUTE_WEIGHT_BRIDGE`

QP014 should use the protected route window, suppression-adjusted contact, and
Gamma_res access to turn unresolved route strength into normalized route
weights.

Generated at UTC: `2026-06-07T16:01:27.715212+00:00`
