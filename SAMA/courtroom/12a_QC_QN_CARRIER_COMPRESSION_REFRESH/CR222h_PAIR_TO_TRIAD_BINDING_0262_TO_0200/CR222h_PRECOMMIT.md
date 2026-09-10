# CR222h PRECOMMIT - Pair-to-Triad Binding 0262 -> 0200

## Scope

Trial a narrow pair-to-triad bridge:

```text
sealed carrier packet + QP093A-0262 pair face + QP093A-0200 triad target
+ protocol trigger
```

## Protected Distinctions

```text
carrier checksum = 162
carrier tensor witness = QP093A-0300=18
pair face = QP093A-0262, 4+4, qA=172, T=21.5, W=150.5
triad target = QP093A-0200, 4+4+4, qA=1160, T=145, W=1015
protocol_event_qA = 1/24
```

## Pre-run Hash

Expected `CR222h_pair_triad_roster.csv` hash:

```text
02b89ffe270a25067acfdb7b1b79fbac8de67f74ee336d6f629e2baef8be3d68
```
