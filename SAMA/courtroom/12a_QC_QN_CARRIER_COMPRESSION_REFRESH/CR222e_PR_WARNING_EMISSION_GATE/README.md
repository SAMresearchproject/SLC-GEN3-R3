# CR222e Paul Revere Warning Emission Gate

CR222e defines the emission state machine:

```text
DRAFT_PACKET -> SEALED_PACKET -> VALID_WARNING_PACKET -> EMITTED_WARNING_PACKET
DRAFT_PACKET/SEALED_PACKET -> CORRUPT_PACKET
```

It protects the distinction:

```text
support inventory != promoted matter != emitted tensor/write
```
