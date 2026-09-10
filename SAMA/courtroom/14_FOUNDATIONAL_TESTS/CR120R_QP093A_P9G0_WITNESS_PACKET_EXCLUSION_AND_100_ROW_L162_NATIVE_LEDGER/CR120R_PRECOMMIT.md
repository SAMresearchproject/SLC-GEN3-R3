# CR120R — QP093A p9,g0 Witness-Packet Exclusion and 100-Row L162 Native Ledger

record_id: `CR120R_QP093A_P9G0_WITNESS_PACKET_EXCLUSION_AND_100_ROW_L162_NATIVE_LEDGER`

task: `Execute the instructions in do this.pdf`

classification: `CONSTRUCTIVE_NEW_WORK`

## Controlling question

Does the frozen 105-row QP093A stable single-write surface consist of 21
complete five-role address packets obeying the documented row laws, with the
exact `[p=9,g=0]` packet the unique single packet whose exclusion leaves 100
payload rows, exact native sum 16200, and exact mean `L=162`?

This is the PDF's CR-A finding. It is a structural inventory/accounting test,
not a binding-energy test.

## Frozen arithmetic

Use exact rational arithmetic throughout.

```text
R = 12
u(p,g) = p * R^g

positive matter       M_native = (5/4)u
positive antimatter   M_native = (5/4)u
negative matter       M_native = (3/2)u
negative antimatter   M_native = (3/2)u
neutral               M_native = (1/8)u

complete packet = 2(5/4 u) + 2(3/2 u) + 1/8 u = 45/8 u
```

The exact permitted parent statement is only:

```text
[p=9,g=0,role] = [p=1,g=0,role] + [p=8,g=0,role]
```

for plus, minus, neutral, anti-plus, and anti-minus. No `g=1`, `g=2`,
composite, qA, or all-depth extension is admitted.

## Frozen selectors

The 105-row test lane is the full row set in `QP093A_105_OVERLAY`.
`p` and `g` are parsed only from the single-write `route_combination`. Each
address packet is the five rows sharing `(p,g)` across the five roles.

The candidate non-payload packet is frozen before execution as exactly:

```text
(p,g) = (9,0)
candidate_ids = QP093A-0019, QP093A-0020, QP093A-0021,
                QP093A-0085, QP093A-0086
```

No row is selected by a total, mean, or observed physical mass.

## Gates

- `G1_SOURCE_LOCK`: every manifest source exists at the frozen SHA-256 and byte count; the precommit hash matches `CR120R_PRECOMMIT.sha256.txt`.
- `G2_PACKET_COMPLETENESS`: exactly 105 unique rows form exactly 21 `(p,g)` packets of five roles each.
- `G3_ROW_LAWS`: all 105 stored `M_native` values equal the frozen charged/neutral row laws exactly.
- `G4_ADDRESS_LEDGER`: the 21 address values sum to 2889 and the full native inventory is `130005/8 = 16250.625`.
- `G5_P9_PARENT_IDENTITY`: the five frozen p9,g0 rows equal the same-role p1,g0 plus p8,g0 rows in exact `M_native` arithmetic.
- `G6_EXCLUSION_CLOSURE`: excluding only the p9,g0 packet leaves 100 rows, address sum 2880, native sum 16200, and mean 162.
- `G7_UNIQUENESS`: testing all 21 possible single-packet exclusions, p9,g0 is the only removal that leaves mean 162 (equivalently native sum 16200 for 100 rows).
- `G8_CURRENT_WORKBOOK_RECONCILIATION`: the derived 100 payload IDs and their exact `M_native` values match `CURRENT_ROSTER100` one-for-one.
- `G9_TYPED_CONTROLS`: same-scalar carrier/support objects are not treated as QP093A p9,g0 rows, and no source row is deleted or mutated.

## Predeclared wrong controls

1. Remove `[p=8,g=0]`.
2. Remove `[p=12,g=0]`.
3. Remove `[p=9,g=1]`.
4. Remove every row whose scalar or partition signature displays `9`.
5. Treat `QP093A-0302 weak_vector_support` (partition signature 9) as a p9 coordinate.
6. Treat `QP093A-0312 hidden_source_support[p=9]` as a native matter row.
7. Treat `W9_CLOSURE_WITNESS` as an additional payload row rather than a non-ledger witness.
8. Extend the p9 identity to g1, g2, composite routes, or qA.
9. Select a packet because its removal reaches 16200 rather than by the frozen p9,g0 typed identity.
10. Delete or mutate the five source rows instead of emitting a counted/not-counted overlay.

All controls must be detected or numerically rejected.

## Verdict grammar

```text
STRONG_STRUCTURAL_PASS
  iff G1 through G9 all pass and every wrong control is rejected.

FAIL
  otherwise.
```

A pass establishes the exact packet algebra, unique single-packet exclusion,
100-row sum 16200, and mean L162 inside this frozen lane. It does not establish
physical particle masses, a universal particle inventory, or a binding term.
The 16200 inventory is a conservation/accounting gate and must not be inserted
as a fitted coefficient or subtracted from nuclear mass.

## Required outputs

- `CR120R_packet_removal_scan.csv`
- `CR120R_payload_overlay.csv`
- `CR120R_wrong_controls.json`
- `CR120R_summary.json`
- `CR120R_result.md`
- `CR120R_VALIDATION_REPORT.json`
- `HASHES.txt`
