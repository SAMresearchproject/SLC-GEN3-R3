# CR120U Discovery Report

## Constructive result

The QP093A three-body row is supported as a **cell/face-family template**, not
as one isolated literal face. A canonical signature `(a,b,c)` supplies three
axis labels. The CR117 binary sign operator generates eight oriented faces,
six signed-axis vertices, and twelve cross-axis edges.

```text
120 source triads -> 120 cell templates
vertex instances  -> 720
edge instances    -> 1440
face instances    -> 960
```

Every cell passes Euler closure, degree-four closure, three edges per face,
two faces per edge, connectedness, and exact rigidity rank 12.

## Why repeated labels matter

The source contains 56 all-distinct triads, 56 two-label triads, and 8
all-same triads. Equal scalar labels do not merge axis occurrences. The latter
64 templates still have six vertex instances because `x`, `y`, and `z` remain
distinct typed axes.

## Source weld

- Every signed vertex resolves to direct one-body plus/minus rows at all three
  available depths.
- Every edge resolves to a forward and reverse ordered-pair motif.
- Every face resolves to its source triad and one CR117 binary sign state.
- Every axis label resolves to its CR218 hidden-support row.
- The original 107 allowed / 13 surface-rejected triad gate is preserved.

## Independent 6/12/8 convergence

The geometry was not created by assigning the six carrier rows to vertices or
the eight hidden rows to faces. It was generated independently from three
signed axes:

```text
6 = 2*3 signed-axis vertices
12 = 4*C(3,2) cross-axis edges
8 = 2^3 sign-oriented faces
```

The carrier count 6 and hidden-support count 8 are therefore convergent type
counts, not circular incidence inputs. Their row-level assignment remains
open.

## Shape discrimination

The tetrahedron remains a valid possible geometry elsewhere in the grammar,
but it does not provide the same one-triad/one-cell operator. A tetrahedron
from one `(a,b,c)` needs an unsourced origin; a four-label tetrahedron needs
four triad motifs. The cube remains the frozen CR117 dual, with quadrilateral
rather than three-body faces.

## Binding boundary

No binding observation or 81-row selector was used. This run contributes the
topology-derived interface accounting `8C = exposed_faces + 2I` and the exact
motif multiplicities needed for a subsequent frozen binding campaign.
