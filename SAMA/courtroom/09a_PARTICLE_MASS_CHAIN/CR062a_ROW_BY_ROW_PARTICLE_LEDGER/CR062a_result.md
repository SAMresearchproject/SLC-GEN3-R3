# CR062a Row-by-Row Particle Ledger

## Verdict

```text
CR062a_PASS_QP075_ROW_BY_ROW_PARTICLE_LEDGER_35_ROWS
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS_QP075_ROW_BY_ROW_PARTICLE_LEDGER_35_ROWS
triage_bin = A
```

## Reason

```text
QP075 provides a 35-row ledger: 32 PDG-anchored rows and 3 lattice-anchored rows under declared tolerances.
```

## Phase Summary

```text
ledger rows              35
PDG-anchored rows        32
lattice-anchored rows    3
PDG residual range       -0.3974% to 0.0708%
lattice residual range   -1.7715% to 4.1534%
observed mass use        REVEAL_ONLY_RESIDUAL_COLUMN
```

## Rule-9 Line

```text
This test could have falsified the row ledger if QP075 did not contain 35 rows,
if PDG/lattice anchors were mistyped, if residuals failed replay, or if any row
exceeded its declared tolerance.
```
