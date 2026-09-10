# QP006 - Private Heavy Composite Slot Priority Table

Location: `D:\quantum_phase`

## Verdict

`QP006_PRIVATE_HEAVY_COMPOSITE_SLOT_PRIORITY_TABLE_BUILT`

QP006 turns the QP005 native strength law into a private priority table for
heavy q/anti-q scaffold slots. It reads the public SUK055 and QGA075 outputs
from the private side and does not use observed composite masses.

## Main Read

The first role-lock target is `b<->c`
(`bc_meson-;bc_meson+`), with native strength
`0.717139946489`.

Rows at P1/P2 are the slots that clear A-share scale or better before any
external comparison.

## Priority Table

| Rank | Pair | Oriented symbols | Priority | Native strength |
| ---: | --- | --- | --- | ---: |
| 1 | b<->c | bc_meson-;bc_meson+ | P1_ROLE_LOCK_FIRST | 0.717139946489 |
| 2 | c<->s | cs_meson+;cs_meson- | P2_A_SHARE_ROLE_CANDIDATE | 0.252472987837 |
| 3 | b<->t | bt_meson-;bt_meson+ | P2_A_SHARE_ROLE_CANDIDATE | 0.0923016101689 |
| 4 | b<->s | bs_meson0;bs_meson0 | P2_A_SHARE_ROLE_CANDIDATE | 0.0849597126971 |
| 5 | c<->t | ct_meson0;ct_meson0 | P3_SCAFFOLD_HELD_OPEN | 0.0291578696086 |
| 6 | c<->d | cd_meson+;cd_meson- | P3_SCAFFOLD_HELD_OPEN | 0.0144409361727 |
| 7 | c<->u | cu_meson0;cu_meson0 | P3_SCAFFOLD_HELD_OPEN | 0.00669113159829 |
| 8 | b<->d | bd_meson0;bd_meson0 | P3_SCAFFOLD_HELD_OPEN | 0.00443564972461 |
| 9 | s<->t | st_meson-;st_meson+ | P3_SCAFFOLD_HELD_OPEN | 0.00214652742778 |
| 10 | b<->u | bu_meson-;bu_meson+ | P3_SCAFFOLD_HELD_OPEN | 0.0020496727624 |
| 11 | d<->t | dt_meson-;dt_meson+ | P3_SCAFFOLD_HELD_OPEN | 0.000107602567305 |
| 12 | t<->u | tu_meson0;tu_meson0 | P3_SCAFFOLD_HELD_OPEN | 4.96641640597e-05 |

## Counts

```text
priority rows = 12
priority class counts = {'P1_ROLE_LOCK_FIRST': 1, 'P2_A_SHARE_ROLE_CANDIDATE': 3, 'P3_SCAFFOLD_HELD_OPEN': 8}
A-share or better rows = 4
```

## Next Frontier

`QP007_PRIVATE_ROLE_OPERATOR_MASS_CLOSURE_TRIAL`

QP007 should attempt a private mass-closure readout for the P1/P2 rows using
only constituent sum, interaction mass coordinate, and SAM-native role class.

Generated at UTC: `2026-06-07T02:37:24.557218+00:00`
