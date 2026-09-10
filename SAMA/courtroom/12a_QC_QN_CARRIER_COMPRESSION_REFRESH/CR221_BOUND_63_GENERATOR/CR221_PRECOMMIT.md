# CR221 PRECOMMIT - Bound 63 Generator

## Scope

Generate `Tier1_Bound63.csv` from SAM constants and closure selectors only:

```text
alpha_H = 2
D = 3
R = 12
Pi = (1, 2, 3, 4, 6, 8, 9, 12)
Omega = (1, 2, 3, 4, 6, 8, 9)
```

## Pair Generator

Ordered two-owner closures use:

```text
Omega x Omega = 7^2 = 49
M_pair(a,b) = R*a*b + D*abs(a-b)
q = a - b
```

This decomposes into 7 equal neutral pairs and 42 oriented charged pairs.
Pair rows with owner 9 are classified as `OCTET_COMPOSITE`; rows whose owners
remain at or below 8 are classified as `BOUND_COLOR_PAIR`.

## Three-Owner Generator

Three-owner color closures are generated from combinations with replacement
over `Pi`, then selected by the native stable charged closure predicate:

```text
sum(a,b,c) mod D = 0
max(a,b,c) <= 8
q = (a - b) + (c mod D)
q != 0
M_triad(a,b,c) = R*D*(a^2+b^2+c^2)
```

This selects 14 `GROUND_BARYON_3BODY` rows.

## Source Boundary

`CR219_promoted_particle_rows_126.csv` is read only after generation as a
downstream validation surface. It supplies no candidate IDs, names, labels, or
rows to the construction step.

## Pre-run Hash

Expected generated CSV hash after deterministic construction:

```text
1a774001e30a322aaff3811c7ab376672744a2f7bfcba1b534a515dabb391713
```
