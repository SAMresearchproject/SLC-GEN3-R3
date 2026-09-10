# CR220 PRECOMMIT - Native 63 Generator

## Scope

Generate `Tier1_Native63.csv` from SAM constants only:

```text
alpha_H = 2
D = 3
R = 12
Pi = (1, 2, 3, 4, 6, 8, 9, 12)
charges = neutral, positive, negative
```

## Generator

Depths 0 and 1 admit all eight partition modes. Depth 2 admits only
`1, 2, 3, 4, 6`. For every allowed `(p,d)`, emit the neutral, positive,
negative triplet.

Native mass:

```text
M_native = p * R^d * k
neutral  k = 1/8
positive k = 5/4
negative k = 3/2
```

Charged source support uses the first carrier lift:

```text
source_support(charged) = M_native * (R^2 + 1) / R^2
source_support(neutral) = M_native
tensor_support          = source_support / 2^D
retained_support        = source_support - tensor_support
```

## Source Boundary

`CR219_promoted_particle_rows_126.csv` is read only after generation as a
downstream validation surface. It supplies no candidate IDs, names, labels, or
rows to the construction step.

## Pre-run Hash

Expected generated CSV hash after deterministic construction:

```text
7b047416848c282ad3c5ea4b6a86a964623d64e9e7ab8baad93ddc2656e0ed3a
```
