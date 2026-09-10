# CR059a Particle Engine Allowed Inputs

## Verdict

```text
CR059a_PASS_QP075_ALLOWED_INPUTS_AND_LATEST_SOURCE_LOCK
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS_QP075_ALLOWED_INPUTS_AND_LATEST_SOURCE_LOCK
triage_bin = A
```

## Reason

```text
QP075 is source-locked as the corrected terminal particle surface; old 09 is quarantined as historical misroute only.
```

## Phase Summary

```text
QP075 files checked        7
manifest rows verified    21/21
closure rows              35
role-operator rows        26
free parameters           0
old 09 role               historical_misroute_artifact only
```

## Rule-9 Line

```text
This test could have falsified the corrected branch if QP075 was not the
active terminal source, if any terminal file failed hash lock, if QP075 did not
declare 35 rows / 26 operators / 0 free parameters, or if old 09 was still
treated as the active terminal scope.
```
