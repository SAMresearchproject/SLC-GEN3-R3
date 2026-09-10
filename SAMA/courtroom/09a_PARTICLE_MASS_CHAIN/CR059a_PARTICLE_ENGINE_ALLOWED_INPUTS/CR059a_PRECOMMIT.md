# CR059a PARTICLE_ENGINE_ALLOWED_INPUTS

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

Does the corrected 09a branch lock QP075 as the active terminal input and exclude the older 12/15-row table as terminal scope?

## Pass Conditions
- QP075 summary/table/operator/decision/preflight/schema files exist and hash-lock.
- QP075 reports 35 closure rows, 26 role operators, and 0 free parameters.
- The source manifest contains QP075 as terminal source and old 09 only as historical misroute evidence.

## Wrong Controls
- Old 12/15-row table treated as terminal source must fail.
- Missing QP075 file must fail.
- Nonzero free-parameter source must fail.

## Rule-9 Line

```text
This test could have falsified the corrected QP075 particle mass-chain branch if
the active source was not QP075, if forbidden target data entered construction,
if the row ledger failed residual replay, or if the older 12/15-row branch
remained the active terminal scope.
```
