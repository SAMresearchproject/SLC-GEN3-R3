# CR063a Wrong Controls and Near Neighbors

## Verdict

```text
CR063a_PASS_WRONG_CONTROLS_AND_OLDER_FREEZE_MISROUTE_QUARANTINE
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS_WRONG_CONTROLS_AND_OLDER_FREEZE_MISROUTE_QUARANTINE
triage_bin = A
```

## Reason

```text
The old 15-row branch is preserved as historical material, while QP075 is the active 35-row/26-operator source.
```

## Phase Summary

```text
old CR062 row extraction     15
QP075 closure rows           35
QP075 role-operator rows     26
QP075 free parameters        0
manifest rows verified       21/21
```

## Rule-9 Line

```text
This test could have falsified the corrected branch if the old 15-row result
was indistinguishable from QP075, if the operator backbone was missing, or if
the old 09 artifacts were still promoted as active terminal sources.
```
