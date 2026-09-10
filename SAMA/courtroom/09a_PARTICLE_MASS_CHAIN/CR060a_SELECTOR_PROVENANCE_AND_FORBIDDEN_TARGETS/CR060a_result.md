# CR060a Selector Provenance and Forbidden Targets

## Verdict

```text
CR060a_PASS_QP075_SELECTOR_PROVENANCE_AND_FORBIDDEN_TARGETS
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS_QP075_SELECTOR_PROVENANCE_AND_FORBIDDEN_TARGETS
triage_bin = A
```

## Reason

```text
QP075 exposes selector/role provenance and keeps observed masses in reveal-only residual columns.
```

## Phase Summary

```text
closure rows checked        35
role-operator rows checked  26
observed mass use           REVEAL_ONLY_RESIDUAL_COLUMN
manifest rows verified      21/21
```

## Rule-9 Line

```text
This test could have falsified selector provenance if any QP075 row lacked a
role/lane, k expression, k class, structural reading, integer operator tuple,
or if observed masses were used anywhere except the reveal-only residual
column.
```
