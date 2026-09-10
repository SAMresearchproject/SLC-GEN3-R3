# CR061a Mass Chain Reproduction

## Verdict

```text
CR061a_PASS_QP075_MASS_CHAIN_REPRODUCTION
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS_QP075_MASS_CHAIN_REPRODUCTION
triage_bin = A
```

## Reason

```text
QP075 residuals replay from frozen predicted/reference masses across 35 rows with 26 role operators and zero free parameters.
```

## Phase Summary

```text
closure rows replayed       35
role-operator rows checked  26
failed replay rows          0
free parameters introduced  0
manifest rows verified      21/21
```

## Rule-9 Line

```text
This test could have falsified QP075 reproduction if any row residual failed
to recompute from predicted/reference mass, if the 35-row surface or 26-row
operator backbone was absent, or if any free-parameter field was nonzero.
```
