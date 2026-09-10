# CR222c Paul Revere Packet Audit States Result

**Result class:** `CR222c_PASS_PR_PACKET_AUDIT_STATES__DRAFT_SEALED_CORRUPT_VALID_WARNING`

**Checks:** 12/12

**CR222c_state_machine.csv SHA-256:** `7644f9ca376ec2bac1e41c214aa782976d10d2ba067e19322431872bd9aac186`

## Verdict

The Paul Revere packet now has an audit state machine:

```text
DRAFT_PACKET -> SEALED_PACKET -> VALID_PR_WARNING_PACKET
DRAFT_PACKET/SEALED_PACKET -> CORRUPT_PACKET
```

A packet is sealed only when the CR222a and CR222b hashes match and the packet
checksum remains intact:

```text
36 + 45 = 81
0303 = 81
81 + 81 = 162
```

A valid warning packet is stronger than a sealed packet:

```text
VALID_PR_WARNING_PACKET =
  SEALED_PACKET
  + route present
  + tensor witness present
  + A_leak >= A_side
  + checksum intact
```

with:

```text
A_side = 1/24
t_fire = T2*(-1/2*ln(23/24))
```

The tensor carrier remains witness/floor only. It does not become payload or
matter.
