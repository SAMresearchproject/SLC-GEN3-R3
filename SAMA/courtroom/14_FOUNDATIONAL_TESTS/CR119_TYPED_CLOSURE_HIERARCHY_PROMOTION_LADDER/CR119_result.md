# CR119 Result

record_id: `CR119_TYPED_CLOSURE_HIERARCHY_PROMOTION_LADDER`
sealed_utc: `2026-07-12T09:02:06Z`
scientific_result_status: `PASS`
primary_verdict: `PASS_TYPED_CLOSURE_HIERARCHY_AND_PROMOTION_LADDER`

## Hierarchy

```text
h = 2
D = 3
R = 12
S = 8
X = 1
W = 9
Theta = 18
V = 27
F = 81
P = 80  [CR283 inherited status: STRUCTURAL_ONLY]
M = 126
N = 144
L = 162
```

All exact paths passed:

```text
X = D^(D-1) - S
W = S + X = D^2
Theta = h*W = R^2/S
V = D*W = D^3
F = D*V = W^2 = D^4
N = R^2 = S*Theta
M = N - Theta = (S-1)*Theta
L = h*F = W*Theta = N*(W/S)
P = F - X = S*(W+1) [conditional, inherited from CR283]
```

## Scope Preservation

CR282 is preserved exactly:

```text
B/contact -> X1 axis-fee -> W9 : PASS
A_OPERATOR -> B/contact        : OPEN
```

The hierarchy keeps `B_CONTACT_OPERATOR`, `X1_AXIS_SELF_CHANNEL`, `A_OPERATOR`, scalar-one carrier, scalar-one support, and repeated `8`, `9`, `12`, and `81` occurrences typed separately.

## Rejections

The runner rejected `S8 * D3 = 24` as volume promotion because unresolved `S8` is not a `ClosureWitness`. It also rejected operator insertion as a ledger row, `A == B`, `B == X1`, scalar-only deduplication, automatic promotion of the `80/81` edge, and Higgs input into the hierarchy.

## Handoff

Machine-readable outputs:

```text
CR119_typed_hierarchy.json
CR119_LANGUAGE_HANDOFF_CONTRACT.json
```

This CR imports prior results and is not eligible as a fresh SAM Language v0.3 holdout.
