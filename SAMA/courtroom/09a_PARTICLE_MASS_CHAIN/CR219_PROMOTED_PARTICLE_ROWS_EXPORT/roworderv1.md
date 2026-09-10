# Row Order V1

## Status

This is a working row-order interpretation note for the CR219 promoted particle
surface and the user-organized overlay at:

`C:\Users\drwho\OneDrive\Desktop\CR219_promoted_particle_rows_126.csv`

It is not a replacement for the sealed CR219 export. The sealed 126-row
promoted particle surface remains:

`09a_PARTICLE_MASS_CHAIN/CR219_PROMOTED_PARTICLE_ROWS_EXPORT/CR219_promoted_particle_rows_126.csv`

The Desktop overlay intentionally adds support/carrier rows and `.1` visual
markers so row-order structure can be inspected.

## Source Boundary

- CR119: `321 particle / 126 matter / 126 periodic` vault reveal.
- CR219: formal 126 promoted particle export from the CR119 matter table.
- CR216/CR217: deduped support/carrier shelf, including five active carriers
  and eight hidden-source support rows.
- Desktop overlay: visual row-order layout built from the promoted rows plus
  support/carrier rows.

## Overlay Count

The organized overlay has:

- `126` promoted matter rows from CR219.
- `5` active carrier rows.
- `8` hidden-source support rows.
- `139` rows total.

The 126 promoted rows still split exactly:

- `63 stable_matter_rows`
- `63 bound_composite_rows`

The added support rows split:

- `5 carrier_only_rows`
- `8 hidden_source_support_rows`

## Address Skeleton

The stable single-write matter rows and hidden-source support rows share the
same partition address set:

```text
P = {1, 2, 3, 4, 6, 8, 9, 12}
sum(P) = 45
```

This is one of the strongest visible patterns in the row order. The support
rows do not behave like promoted matter rows; they mark the same address
skeleton that the stable matter ladder uses.

## Stable Single-Particle Sector

The `stable_matter_rows` form exact neutral / positive / negative triplets by
`partition_signature` and `closure_depth`.

For every stable `(p, d)` group:

```text
neutral, positive, negative
```

No stable triplet group is broken in the organized table.

Depth coverage:

```text
p = 1, 2, 3, 4, 6  -> depths 0, 1, 2
p = 8, 9, 12       -> depths 0, 1
```

This gives:

```text
5 low partitions * 3 depths * 3 charges = 45 rows
3 high partitions * 2 depths * 3 charges = 18 rows
45 + 18 = 63 stable rows
```

The missing high-depth triplets for `p = 8, 9, 12` at `d = 2` exist in the
particle catalog, but they are rejected into the complement as
`UNSTABLE_HEAVY_WRITE_CANDIDATE` / `UNSTABLE_RESONANCE_COMPLEMENT`.

### Stable Mass Rule

All 63 stable rows obey:

```text
M_native = p * 12^d * k
```

with:

```text
neutral  k = 1/8
positive k = 5/4
negative k = 3/2
```

Example for `p = 1`:

```text
neutral:  0.125 -> 1.5 -> 18
positive: 1.25  -> 15  -> 180
negative: 1.5   -> 18  -> 216
```

Each depth step multiplies by `12`.

## Composite Sector

The `bound_composite_rows` split into:

```text
49 boson_integer_write rows
14 fermion_baryon_half_write rows
```

Operator split:

```text
36 BOUND_COLOR_PAIR
13 OCTET_COMPOSITE
14 GROUND_BARYON_3BODY
```

Charge balance:

```text
28 positive
28 negative
7 neutral
```

The `7` neutral rows are the self-pair line:

```text
1+1, 2+2, 3+3, 4+4, 6+6, 8+8, 9+9
```

### Pair Rule

All 49 two-body pair rows obey:

```text
M_native = 12ab + 3|a-b|
```

for partition signature:

```text
a+b
```

The neutral self-pair case reduces to:

```text
M_native = 12p^2
```

The `H = 10` row band is a clean mirror display:

```text
1+9 / 9+1 -> M_native 132 / 132
2+8 / 8+2 -> M_native 210 / 210
4+6 / 6+4 -> M_native 294 / 294
```

The sign flips across the mirror while native mass remains paired.

### Three-Body Rule

All 14 `GROUND_BARYON_3BODY` rows obey:

```text
M_native = 36(a^2 + b^2 + c^2)
```

for partition signature:

```text
a+b+c
```

This makes the baryon-like rows a separate square-sum lattice rather than a
loose residue of the pair sector.

## Carrier And Support Anchors

The overlay places carrier/support rows as address anchors:

```text
photon / ROAD_LIGHT_CARRIER      -> 0
hidden support p=1              -> 1.1
hidden support p=2              -> 2.1
hidden support p=3              -> 3.1
hidden support p=4              -> 4.1
hidden support p=6              -> 6.1
gluon / COLOR_OWNER_CARRIER      -> 8.1
hidden support p=8              -> 8.1
weak / WEAK_VECTOR_CARRIER       -> 9.1
hidden support p=9              -> 9.1
hidden support p=12             -> 12.1
tensor / TENSOR_CARRIER          -> 18
neutral vector / NEUTRAL_VECTOR  -> 81
```

The `.1` values are visual row-order markers in the Desktop overlay. They are
not sealed CR219 matter values.

## Band Structure

The row order is organized by an integer/address band `H_value_or_integer_sum`.

The strongest population bands are:

```text
H = 6   -> 15 rows
H = 12  -> 14 rows
H = 3   -> 12 rows
H = 4   -> 12 rows
H = 9   -> 12 rows
H = 2   -> 10 rows
H = 1   -> 9 rows
H = 8   -> 9 rows
```

The visible band sequence is:

```text
0, 1, 1.1, 2, 2.1, 3, 3.1, 4, 4.1, 5, 6, 6.1,
7, 8, 8.1, 9, 9.1, 10, 11, 12, 12.1, 13, 14,
15, 16, 17, 18, 24, 81
```

## Interpretation

The organized row order exposes a generated spectrum:

1. Carrier/support anchors define the address skeleton.
2. Stable single-write matter fills neutral/positive/negative triplets.
3. Heavy high-depth single-write rows cross the stability selector and move to
   the complement.
4. Two-body composites fill a pair lattice with mirror symmetry.
5. Three-body composites fill a baryon-like square-sum lattice.

This is stronger than raw arithmetic. It is a grammar of allowed matter rows,
support rows, and rejected heavy rows.

## Periodic-Table Derivation Use

This row-order grammar can help further derive the periodic table, but it does
not by itself complete that derivation.

The useful bridge is:

```text
particle row-order grammar
-> stable address skeleton P
-> support/carrier anchors
-> stability cutoff
-> composite closure families
-> candidate element-family shell/address generator
```

Reasons it may help:

- CR119 already exposes a parallel count: `126 matter rows` and `126 periodic
  rows`, while keeping the periodic layer separate.
- The stable/support address set has sum `45`, and CR217 independently records
  the same hidden-source partition sum.
- CR217 records `carrier_incl_graviton = 117`, `hidden_source = 45`, and
  `total_partition = 162 = R^2 * 9/8` on sealed inputs.
- The high-depth cutoff for `p = 8, 9, 12` gives a concrete selector boundary,
  not just a count.
- The composite sector gives closed two-body and three-body mass rules that can
  be tested against element-family shell occupancy and closure families.

The immediate next Courtroom-safe derivation target should be a row-level bridge
test, not a declaration that the periodic table has been derived from this row
order.

Suggested next test:

```text
Build a CR220-style bridge from ROWORDERV1 bands to CR119 periodic rows.
For each periodic row, test whether its shell/family placement can be assigned
from the P skeleton, support anchors, carrier anchors, and composite closure
rules without using downstream known element names as construction inputs.
```

The key success condition would be a row-level mapping into the 126 periodic
rows, including the `Z119-Z126` frontier, while preserving the CR119 rule that
known labels are downstream reveal labels only.

## Boundary

This note records backed row-order observations and a proposed derivation path.
It does not promote the periodic-table derivation to a completed Courtroom
result.
