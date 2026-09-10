# CR120U Result

record_id: `CR120U_QP093A_TYPED_MOTIF_OCTAHEDRAL_INCIDENCE_DISCOVERY`
sealed_utc: `2026-07-14T21:47:29Z`
scientific_result_status: `PASS`
primary_verdict: `PASS_QP093A_TRIAD_TO_OCTAHEDRAL_CELL_INCIDENCE_OPERATOR`

## Result

QP093A's complete unordered-triad library supports a source-complete
three-axis octahedral incidence operator:

```text
one triad motif (a,b,c)
-> one cell template
-> 6 signed-axis vertices
-> 12 cross-axis edges
-> 8 sign-oriented triangular faces
```

All 120 triad templates construct. All
720 vertex, 1440 edge, and
960 face instances resolve to their frozen QP/CR117 source
motifs. All 15 predictions pass and all 12 wrong
controls are rejected as precommitted.

## Strongest new meaning

A QP triad row is not one literal geometric face. It is a reusable
three-axis cell/face-family template whose eight orientations are supplied by
the already-sealed S8 binary sign states. Pair rows are reusable connection
motifs and one-body rows supply signed vertex-state families.

## Binding handoff

The new topology-derived count is:

```text
8C = exposed_faces + 2I
```

for `C` cells with `I` face-sharing interfaces. No binding formula or observed
binding target was run.

## Boundaries

- Physical octahedral ontology remains a candidate realization.
- Tetrahedral geometry is not globally excluded.
- Carrier-to-vertex and hidden-row-to-face assignments remain unresolved.
- M2/M3 per-instance versus compressed-budget roles remain unresolved.
- The 81-row projection did not select the geometry.
