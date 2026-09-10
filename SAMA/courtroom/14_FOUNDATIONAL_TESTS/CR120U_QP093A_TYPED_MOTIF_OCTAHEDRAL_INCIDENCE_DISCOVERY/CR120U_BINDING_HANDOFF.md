# CR120U Binding Handoff

## Frozen geometry operator

`PASS_QP093A_TRIAD_TO_OCTAHEDRAL_CELL_INCIDENCE_OPERATOR`

For one QP three-axis cell:

```text
vertex degree within one octahedral cell = 4
vertices = 6
edges = 12
triangular faces = 8
maximum face-sharing slots per isolated cell = 8
```

For `C` cells joined across `I` complete face-sharing interfaces:

```text
face inventory = 8C
shared face occurrences = 2I
exposed faces = 8C - 2I
8C = exposed_faces + 2I
```

These are geometry-derived integer features. They are the permitted inputs to
the next binding discovery. No observed binding value was opened here.

## Source motif multiplicities

For a cell signature `(a,b,c)`:

```text
signed vertex instances: 2 per axis
edge instances: 4 for each axis pair (a,b), (a,c), (b,c)
face instances: 8 sign orientations of the same unordered triad motif
hidden support lookup: L_a, L_b, L_c
```

`CR120U_CELL_TEMPLATES.csv` reports both the once-per-row values and the
geometry-repeated candidate totals. This CR does not select between:

```text
M2 as a per-edge motif versus an already-compressed pair budget
M3 as a per-face motif versus an already-compressed cell budget
```

That role discrimination must be frozen before held-out binding rows are
opened. The values `126`, `144`, `162`, `12,600`, and `16,200` remain forbidden
as fitted coefficients.

## Remaining typed assignments

- Carrier-row-to-signed-vertex assignment is unresolved.
- Hidden-row-to-oriented-face assignment is unresolved and was not assumed.
- Tetrahedral geometry is not globally excluded; it failed the single-triad
  source-complete operator, not geometry in general.
