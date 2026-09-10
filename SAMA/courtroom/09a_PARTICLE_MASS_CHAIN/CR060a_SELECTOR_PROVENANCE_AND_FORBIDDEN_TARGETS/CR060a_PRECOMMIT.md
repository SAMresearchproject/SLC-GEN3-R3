# CR060a SELECTOR_PROVENANCE_AND_FORBIDDEN_TARGETS

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

Do the QP075 rows and operators expose selector provenance without using observed masses as construction inputs?

## Pass Conditions
- Every closure row has a role operator or V4.1 ladder, k expression, k class, structural reading, and 0 free parameters.
- Every role-operator row has integer k, shift, q, and N fields.
- QP075 decision table records observed mass use as REVEAL_ONLY_RESIDUAL_COLUMN.

## Wrong Controls
- Observed masses used as selector inputs must fail.
- Missing role operator or structural reading must fail.
- Non-integer operator tuple must fail.

## Rule-9 Line

```text
This test could have falsified the corrected QP075 particle mass-chain branch if
the active source was not QP075, if forbidden target data entered construction,
if the row ledger failed residual replay, or if the older 12/15-row branch
remained the active terminal scope.
```
