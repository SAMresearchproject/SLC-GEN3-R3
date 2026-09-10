# CR222c Paul Revere Packet Audit States

This artifact defines the state machine around the CR222b Paul Revere packet:

```text
DRAFT_PACKET -> SEALED_PACKET -> VALID_PR_WARNING_PACKET
DRAFT_PACKET/SEALED_PACKET -> CORRUPT_PACKET
```

Primary product:

```text
CR222c_state_machine.csv
```
