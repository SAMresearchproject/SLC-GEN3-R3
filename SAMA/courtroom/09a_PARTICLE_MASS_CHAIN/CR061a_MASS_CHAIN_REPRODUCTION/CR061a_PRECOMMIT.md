# CR061a MASS_CHAIN_REPRODUCTION

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

Can the QP075 mass ledger be replayed from its frozen table and operator backbone without changing the source?

## Pass Conditions
- Residuals recompute from predicted and reference masses within rounding tolerance.
- 35 closure rows and 26 role operators are reproduced.
- All rows retain 0 free parameters.

## Wrong Controls
- Perturbing one mass residual must trip the replay.
- Dropping operator rows must trip the backbone count.
- Changing free_parameters_used from 0 must fail.

## Rule-9 Line

```text
This test could have falsified the corrected QP075 particle mass-chain branch if
the active source was not QP075, if forbidden target data entered construction,
if the row ledger failed residual replay, or if the older 12/15-row branch
remained the active terminal scope.
```
