# CR287 Signed-Axis Boundary Mapping

## Domain

The CR286 primary envelope uses six abstract signed-axis ports. A CR285
directed gate divides the same six octahedral vertices into a three-vertex
entry face and its three-vertex complementary exit face.

## Normalization

For a gate vertex ID ending in one of `_+x`, `_-x`, `_+y`, `_-y`, `_+z`, or
`_-z`, retain only the signed-axis suffix. Sort labels in this fixed order:

```text
-x, +x, -y, +y, -z, +z
```

The direction of traversal changes which labels occur at entry and exit. It
does not change the union of available signed-axis boundary ports.

## Mapping

Map each CR286 primary envelope port to the gate port with the identical
signed-axis label. Preserve the chemical-core nodes, chemical-core edges,
frame-membership edges, and envelope-support edges without edits.

This gives the coefficient-free vector `K=(0,0,0,0)` only when all six labels
are unique and present on both sides.

## Non-Mappings

The tetrahedral controls are face-state constructions with bit labels. Those
labels are not silently converted into signed-axis vertices. The core-only
control has no envelope boundary. Both are inadmissible under the CR285 typed
validity gate and are reported outside the ranking set.

## Claim Boundary

Label equality tests graph incidence only. It does not establish pore scale,
steric fit, hydration stability, wall interaction, transport barrier,
permeability, rejection, or physical selectivity.
