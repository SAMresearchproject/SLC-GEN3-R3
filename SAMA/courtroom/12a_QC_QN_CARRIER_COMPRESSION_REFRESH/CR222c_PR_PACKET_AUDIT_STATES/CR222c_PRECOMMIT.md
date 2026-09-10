# CR222c PRECOMMIT - Paul Revere Packet Audit States

## Scope

Define the packet state machine around CR222b. This is an audit/transition
layer only; it does not regenerate or discover physics rows.

## State Chain

```text
DRAFT_PACKET -> SEALED_PACKET -> VALID_PR_WARNING_PACKET
DRAFT_PACKET/SEALED_PACKET -> CORRUPT_PACKET
```

## Sealed Packet Requirements

```text
CR222a hash = 0b18cd65bcf366364c66f1ea0aabe50f2e085794448713342bce6c69670aed0b
CR222b packet hash = 79d5c3bb6384910d54f61df519d6f4cc005f5fd6b30952a1d78440be02e1a009
carrier subtotal = 36
source subtotal = 45
unpacked total = 81
mirror total = 81
full checksum = 162
```

## Warning Gate

```text
VALID_PR_WARNING_PACKET =
  SEALED_PACKET
  + tensor witness present
  + route present
  + warning threshold reached
  + checksum intact

A_side = 1/24
warning threshold: A_leak >= A_side
t_fire = T2*(-1/2*ln(23/24))
```

## Pre-run Hash

Expected `CR222c_state_machine.csv` hash:

```text
7644f9ca376ec2bac1e41c214aa782976d10d2ba067e19322431872bd9aac186
```
