# CR120U Precommit

Record:

```text
CR120U_QP093A_TYPED_MOTIF_OCTAHEDRAL_INCIDENCE_DISCOVERY
```

Precommit sealed UTC:

```text
2026-07-14T21:37:36Z
```

Classification:

```text
CONSTRUCTIVE_NEW_WORK
```

## Objective

Construct a new instance-level incidence operator from the frozen QP093A
one-body, ordered-pair, and unordered-triad grammar.

The operator under test is:

```text
one unordered QP triad signature (a,b,c)
    -> one three-axis cell template
    -> vertices {+x_a,-x_a,+y_b,-y_b,+z_c,-z_c}
    -> edges between vertices on different axes
    -> faces formed by one signed vertex from each axis
```

This produces the CR117 octahedral incidence counts without using the six
carrier rows, eight hidden-support rows, or twelve matter-side-lane count as
construction inputs:

```text
V = 2D = 6
E = 4*C(D,2) = 12
F = 2^D = 8
V - E + F = 2
```

The candidate is a typed grammar operator. It is not a claim that a particle
row is literally a polyhedron, that all physical substrate cells are proven
octahedra, or that a numeric QP row value is already a binding fee.

## Frozen Inputs

The runner may open only the source files enumerated in
`CR120U_SOURCE_MANIFEST.json` plus its own precommit and preflight metadata.
It must not open any observed binding-energy table, CR274/CR277 prediction
table, isotope residual, or the current 81-row membership field as a selector.

The QP093A map is an annotation layer over the exact original 321 source rows.
The original table is included only for source reconciliation. The map remains
the operative grammar source.

## Candidate Incidence Operator

For every unordered triad row with canonical signature `a+b+c`, where
`a <= b <= c` and each value belongs to the CR218 alphabet
`P={1,2,3,4,6,8,9,12}`:

1. Assign `a,b,c` to distinct axis instances `x,y,z` in sorted order.
2. Create two signed vertex instances on every axis.
3. Connect every pair of vertices from different axes; opposite same-axis
   vertices are non-edges.
4. Create one triangular face for every binary sign triple.
5. Preserve axis instance identity when two or three partition labels are
   equal. Scalar label equality must not merge occurrences.
6. Map each signed vertex to the matching QP direct one-body plus/minus family
   at every available depth.
7. Map each geometric edge to the matching QP ordered-pair motif and retain the
   reverse ordered motif as a distinct catalog occurrence.
8. Map every oriented face back to the same source triad motif. A triad row is
   therefore a cell/face-family template, not one isolated face occurrence.
9. Map each distinct axis label to its CR218 hidden-support row. Hidden support
   supplies the admissible coordinate alphabet; it is not assigned to a face
   merely because both counts equal eight.

## Frozen Predictions

P1. The 321-row source reconciliation is exact on all shared source columns.

P2. The grammar counts are exactly `114 one-body`, `64 ordered pairs`,
`120 unordered triads`, `1 scalar`, `14 carrier/support`, and `8 explicit
controls`.

P3. The triad set is exactly the multiset-combination library
`C(8+3-1,3)=120` over the CR218 alphabet.

P4. The runner constructs exactly 120 cell templates, 720 vertex instances,
1,440 edge instances, and 960 face instances.

P5. Every cell has `(V,E,F)=(6,12,8)`, Euler characteristic 2, vertex degree
4, three edges per face, two faces per edge, and one connected component.

P6. Every cell has exact 3D skeletal rigidity rank `3V-6=12` at coordinates
`(+/-a,0,0)`, `(0,+/-b,0)`, `(0,0,+/-c)`.

P7. All 720 vertex instances have complete direct one-body plus/minus source
coverage at `g=0,1,2`.

P8. All 1,440 edge instances resolve to an ordered-pair source motif; reverse
motifs remain separately addressable. Repeated labels do not collapse edges.

P9. All 960 faces resolve to their cell's single source triad row and to one
of the eight frozen CR117 binary sign states.

P10. The 64 repeated-label triads remain full six-vertex cells through axis
instance identity: 56 two-label signatures plus 8 one-label signatures.

P11. Every axis label resolves to exactly one hidden-support row and reproduces
`L_p = p + p^2/144` to source precision.

P12. The source triad gate is preserved: 107 cells are matter-allowed and 13
are retained as rejected surface controls. Geometry construction does not
override the source gate.

P13. The independent geometric derivation yields `6/12/8` without treating
the overlapping infrastructure-row counts as incidence.

P14. The pair and triad catalog fingerprints reproduce:

```text
sum(pair M_native)  = 25,074 = 199*126
sum(triad M_native) = 575,100 = 3,550*162
```

These remain grammar checksums, not fitted coefficients.

P15. No observed binding target or 81-roster membership is used by the
incidence operator.

## Wrong Controls

WC1. **Tetrahedron from one triad plus an origin.** This has `(4,6,4)` and
requires a new `p=0` vertex absent from the QP alphabet. It is a valid
polyhedron but fails the single-triad source-complete SAM mapping.

WC2. **Four-label tetrahedron.** It is catalog-compatible only by using four
independent labels and four triad motifs. It must fail the one-triad/one-cell
operator while remaining recorded as a non-global exclusion boundary.

WC3. **Cube.** It has `(8,12,6)` and quadrilateral faces. It remains the CR117
dual but fails the triangular three-body-face operator.

WC4. **Count-preserving scrambled 6/12/8 incidence.** Preserve V/E/F while
removing three non-edges that do not form a perfect matching. It must fail the
degree and/or edge-face incidence conditions.

WC5. **Collapse equal scalar labels.** Merge repeated-label axis instances.
Exactly the 64 repeated-label triads must lose six-vertex closure.

WC6. **Treat all 64 ordered pair rows as one cell's geometric edges.** This
must fail `E=12` and the degree-four condition.

WC7. **Treat each triad row as one literal face.** This must fail `F=8` for all
120 cell templates.

WC8. **Assign the eight hidden rows directly to the eight faces by row order.**
This must be rejected as an untyped permutation: no source incidence maps
hidden partition value to CR117 sign state.

WC9. **Assign the six carrier rows directly to the six vertices by row order.**
This must be rejected as count-only: no frozen opposite-pair or axis-sign map
is present.

WC10. **Wrong radix R=10.** The cross-polytope still has 12 edges while the
wrong radix has 10; the bounded bigrade alphabet falls from 8 to 7 and the
triad library from 120 to 84.

WC11. **Use 81-row projection membership to select geometry.** This is
forbidden and must be reported as leakage.

WC12. **Use observed binding residuals to rank shapes.** This is forbidden in
this discovery and must be reported as leakage.

## Binding Handoff Boundary

This CR may derive topology-only binding inputs but must not fit or validate a
binding formula. Permitted handoff features are:

```text
cell coordination number = 4
faces per isolated cell = 8
edges per isolated cell = 12
for C cells and I face-sharing interfaces:
    face inventory = 8C
    exposed faces = 8C - 2I
    8C = exposed_faces + 2I
```

The runner may also report source motif multiplicities and support-row lookup
values. It must not decide whether `M2` or `M3` is a per-instance cost or an
already-compressed cell budget. Both accounting interpretations remain open
for the next frozen binding campaign.

## Acceptance And Verdicts

Primary PASS requires P1-P15 and rejection of WC1-WC12:

```text
PASS_QP093A_TRIAD_TO_OCTAHEDRAL_CELL_INCIDENCE_OPERATOR
```

If the topology constructs but source motif coverage is incomplete:

```text
PARTIAL_OCTAHEDRAL_TOPOLOGY_SOURCE_WELD_INCOMPLETE
```

If the octahedral operator does not construct:

```text
FAIL_QP093A_TYPED_INCIDENCE_OPERATOR
```

Allowed PASS boundary:

```text
PHYSICAL_OCTAHEDRAL_ONTOLOGY_REMAINS_CANDIDATE
CARRIER_TO_VERTEX_AND_HIDDEN_TO_FACE_ROW_ASSIGNMENTS_UNRESOLVED
TETRAHEDRAL_GEOMETRY_NOT_GLOBALLY_EXCLUDED
BINDING_FORMULA_NOT_RUN
```

## Required Artifacts

```text
CR120U_SOURCE_MANIFEST.json
CR120U_PRECOMMIT.sha256.txt
CR120U_runner.py
CR120U_CELL_TEMPLATES.csv
CR120U_VERTEX_INSTANCES.csv
CR120U_EDGE_INSTANCES.csv
CR120U_FACE_INSTANCES.csv
CR120U_INCIDENCE_CHECKS.csv
CR120U_WRONG_CONTROLS.csv
CR120U_GEOMETRY_CONTRACT.json
CR120U_BINDING_HANDOFF.md
CR120U_DISCOVERY_REPORT.md
CR120U_summary.json
CR120U_result.md
COMMAND_LOG.txt
HASHES.txt
```
