# QP021 - Private Charged Lane Bridge

## Verdict

`QP021_PRIVATE_CHARGED_LANE_BRIDGE_BUILT`

Charged lane status:

```text
SUCCESS_CHARGED_PARALLEL_CARRIER_BRIDGE
```

QP021 tests the open charged role/operator lane left by QP020.

Core rule:

```text
charged lane requires paired transient direct role contacts:
  QUBIT-CL-001<->QUBIT-TM-001
  QUBIT-CL-001<->QUBIT-TP-001

and selected charged mass surfaces:
  b<->c
  b<->t
```

## Main Read

```text
required charged route contacts = 2
supported charged route contacts = 2
selected charged mass surfaces = 2
charged lane success = True
private freeze recommended = True
free parameters introduced = 0
```

## Route Support

| Required Pair | QP017 Class | Carrier Contact |
| --- | --- | --- |
| QUBIT-CL-001<->QUBIT-TM-001 | TRANSIENT_DIRECT_ROLE_CONTACT_REJECTED | True |
| QUBIT-CL-001<->QUBIT-TP-001 | TRANSIENT_DIRECT_ROLE_CONTACT_REJECTED | True |

## Selected Charged Mass Surfaces

| Pair | Surface | Readout MeV | Status |
| --- | --- | --- | --- |
| b<->c | INTERACTION_COORDINATE_SURFACE | 3950.10153486 | CHARGED_SELECTED_MASS_SURFACE_AVAILABLE |
| b<->t | INTERACTION_COORDINATE_SURFACE | 15800.4061394 | CHARGED_SELECTED_MASS_SURFACE_AVAILABLE |

## Meaning

QP021 succeeds as a charged parallel-carrier bridge.

The charged lane is not promoted by the neutral stable anchor or the
NL/UNK boundary bridge. It travels through a paired transient direct-contact
carrier:

```text
CL<->TM
CL<->TP
```

That carrier links to selected charged mass surfaces already present in QP019:

```text
b<->c -> 3950.10153486 MeV
b<->t -> 15800.4061394 MeV
```

## Freeze Decision

```text
private package: freeze after QP021
phase 2: optional, not required before freeze
public posture: hold private
```

Generated at UTC: `2026-06-07T18:21:59.316285+00:00`
