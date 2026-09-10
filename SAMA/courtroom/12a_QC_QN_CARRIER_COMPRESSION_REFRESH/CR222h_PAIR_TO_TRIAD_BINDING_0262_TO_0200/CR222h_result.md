# CR222h Pair-to-Triad Binding Result

**Result class:** `CR222h_PASS_PAIR_TO_TRIAD_BINDING__QP093A_0262_TO_QP093A_0200_WITH_SEALED_PR_CARRIER`

**Checks:** 21/21

**CR222h_pair_triad_roster.csv SHA-256:** `02b89ffe270a25067acfdb7b1b79fbac8de67f74ee336d6f629e2baef8be3d68`

## Verdict

CR222h binds the neutral pair-face precursor to the original 3-body diamond
target under the sealed PR carrier:

```text
QP093A-0262 4+4 -> QP093A-0200 4+4+4
```

The successful trial state is:

```text
PAIR_TO_TRIAD_BRIDGE_BOUND -> TARGETED_EMITTED_WARNING_PACKET
```

The bridge keeps the ledgers separated:

```text
carrier checksum = 162
carrier tensor witness = QP093A-0300=18
protocol_event_qA = 1/24
pair qA/T/W = 172 / 21.5 / 150.5
triad qA/T/W = 1160 / 145 / 1015
```

QP093A-0262 is not carrier support and is not the final three-body target. It
acts as the valid two-owner `4+4` face that points into the `4+4+4` diamond
target.
