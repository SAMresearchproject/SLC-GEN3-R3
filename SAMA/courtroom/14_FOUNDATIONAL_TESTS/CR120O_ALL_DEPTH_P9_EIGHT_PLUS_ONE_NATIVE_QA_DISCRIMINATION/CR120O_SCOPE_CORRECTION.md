# CR120O Scope Correction - p9,g0 Only

correction_status: `CONTROLLING_FOR_CR120O_INTERPRETATION`

corrected_utc_date: `2026-07-14`

task: `Correct CR120O scope to p9 g0 equals p1 g0 plus p8 g0 only`

preflight: `artifacts/preflight_filled/PREFLIGHT_20260714_041939_no_script.md`

preflight_sha256: `36de8fdfcb76452b1e95bb12d01367c7706c954e305d61fb8d419556dd61d987`

## User correction

The only authorized relation is:

```text
[p=9, g=0] = [p=1, g=0] + [p=8, g=0]
```

It applies only to the five same-role `g=0` QP093A triples below:

| role | p=1 parent | p=8 parent | p=9 row |
|---|---|---|---|
| plus | QP093A-0001 | QP093A-0016 | QP093A-0019 |
| minus | QP093A-0002 | QP093A-0017 | QP093A-0020 |
| neutral | QP093A-0003 | QP093A-0018 | QP093A-0021 |
| anti-plus | QP093A-0073 | QP093A-0083 | QP093A-0085 |
| anti-minus | QP093A-0074 | QP093A-0084 | QP093A-0086 |

For each row, the permitted numerical statement is exactly:

```text
M_native(p=9, g=0, role)
  = M_native(p=1, g=0, role) + M_native(p=8, g=0, role)
```

## CR120O status

CR120O over-scoped the intended task by applying an `8+1` interpretation to
`g=1`, testing `g=2`, examining composite p9 occurrences, and drawing an
all-depth model comparison. Those extensions were not authorized by the user.

The sealed CR120O files and hashes remain unchanged as a historical execution
record, but CR120O is `NONCONTROLLING_FOR_THE_INTENDED_CLAIM` except for the
five `g=0` rows listed above.

## Prohibited carry-forward

This correction forbids using CR120O to claim any of the following:

- `[p=9,g=1] = [p=1,g=1] + [p=8,g=1]` as part of the intended relation;
- a `g=2` extension;
- a composite-route extension;
- an all-depth eight-plus-one model;
- rejection of a base-depth-only scope;
- a universal qA law across generations;
- deletion or merger of p9 identities;
- identification of QP093A p9 with W9;
- identification of any normalized scalar with L162;
- a binding-energy, particle-ontology, or physical-inventory conclusion.

The current spreadsheet values remain sums. No mean is introduced by this
correction.

## Prior artifact boundary

CR120K may be consulted only for its exact five-row `g=0` parent matrix. Its
additional W9/independent-inventory interpretation is not imported into this
correction.

No workbook, QP093A artifact, registry, prior result, or CR120O sealed file was
modified.
