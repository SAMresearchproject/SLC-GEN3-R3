# CR222g PR Target Binding 3-Body Diamond Result

**Result class:** `CR222g_PASS_PR_TARGET_BINDING__3BODY_DIAMOND_TARGET_PLUS_SEALED_CARRIER_PACKET`

**Checks:** 14/14

**CR222g_3body_diamond_target_roster.csv SHA-256:** `86a410172d053d6fb7c1d7d85e5f7d96debd2301c50c0f6fa14f37552421fea2`

## Verdict

CR222g successfully binds the sealed carrier packet to 3-body matter targets:

```text
sealed carrier packet + 3-body target + protocol trigger
= targeted PR warning/write trial
```

The ledgers stay separated:

```text
carrier checksum = 162
carrier tensor witness = QP093A-0300=18
target family = GROUND_BARYON_3BODY
target qA/T/W comes from the matter row after G_matter=1
```

The roster contains 14 three-body targets, with 4 symmetric diamond anchors:

```text
1+1+1
2+2+2
4+4+4
8+8+8
```

The successful trial state is:

```text
TARGETED_PR_WARNING_BOUND -> TARGETED_EMITTED_WARNING_PACKET
```

Support inventory alone still cannot emit, and the 3-body target is not counted
inside the carrier checksum.
