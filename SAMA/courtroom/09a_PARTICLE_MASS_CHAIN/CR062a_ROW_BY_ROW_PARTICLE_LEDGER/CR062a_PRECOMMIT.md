# CR062a ROW_BY_ROW_PARTICLE_LEDGER

## Test Class

```text
FORWARD_COURTROOM_RERUN_CORRECTED_QP075_SOURCE
```

## Preflight

```text
This is not an audit, retest, or double-check of the old 09 result.
It is the same 09 courtroom test spine with an `a` suffix, rerun from
QP075 as the corrected active terminal source.
```

## Question

Does QP075 provide the row-by-row external contact ledger for the corrected branch?

## Pass Conditions
- 35 rows are ledgered.
- 32 PDG rows pass the branch tolerance and 3 lattice rows remain typed as lattice anchors.
- Residual replay remains consistent with QP075 frozen values.

## Wrong Controls
- PDG row outside 0.5 percent tolerance must fail.
- Lattice row outside 5 percent tolerance must fail.
- Missing row comparator must fail.

## Rule-9 Line

```text
This test could have falsified the corrected QP075 particle mass-chain branch if
the active source was not QP075, if forbidden target data entered construction,
if the row ledger failed residual replay, or if the older 12/15-row branch
remained the active terminal scope.
```
