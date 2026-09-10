# CR063a WRONG_CONTROLS_AND_NEAR_NEIGHBORS

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

Does the corrected branch quarantine the old 09 misroute and reject near-neighbor or wrong-control substitutions?

## Pass Conditions
- Old CR062 is recognized as 15-row historical scope only.
- Old CR064a appeal note is recognized as evidence of the QP075 correction need.
- Wrong controls for old terminal source, nonzero free parameters, and missing operator backbone trip.

## Wrong Controls
- Older frozen table promoted as active terminal source must fail.
- A 35-row ledger without the 26-operator backbone must fail.
- A lattice row reclassified as PDG without declaration must fail.

## Rule-9 Line

```text
This test could have falsified the corrected QP075 particle mass-chain branch if
the active source was not QP075, if forbidden target data entered construction,
if the row ledger failed residual replay, or if the older 12/15-row branch
remained the active terminal scope.
```
