# QP093A 321-Row Structural Bucket Map

## Main finding

The 321-row catalog is not a flat list of 321 proposed particles. It is an exact generated grammar over the eight-value partition alphabet:

```text
P = {1, 2, 3, 4, 6, 8, 9, 12}
```

The complete row count closes as:

```text
72  direct one-body writes
42  antimatter-conjugate one-body writes
120 complete unordered three-body color multisets
64  complete ordered two-body pair matrix
1   closed scalar-loop parent
6   carrier-only infrastructure rows
8   hidden support rows
8   explicit rejected controls
---
321 total
```

Equivalently:

```text
321 = 114 one-body rows
    + 184 raw composite rows
    +   1 scalar parent
    +  14 carrier/support rows
    +   8 explicit fake controls
```

The 184 composite rows split into 171 accepted composites and 13 surface-gate rejections:

```text
120 triads - 13 rejected triads = 107 allowed triads
107 allowed triads + 64 pair rows = 171 allowed composites
13 rejected triads + 8 fake controls = 21 total rejections
```

So the catalog also closes as:

```text
321 = 300 non-rejected rows + 21 rejected rows
300 = 286 matter-eligible rows + 14 carrier/support rows
286 = 114 one-body rows + 171 composites + 1 scalar parent
```

## Exact generator families

### One-body direct rows

There are:

```text
8 partition values x 3 depths x 3 route modes = 72 rows
```

For `u = p * 12^g`:

```text
M_plus    = (5/4) u
M_minus   = (3/2) u
M_neutral = (1/8) u
```

The formula is exact on all 72 rows.

### Antimatter conjugates

There are 42 conjugate rows:

```text
21 stable (p,g) addresses x 2 charged modes = 42
```

The three deep packets `(p,g) = (8,2), (9,2), (12,2)` have no conjugate rows in the source catalog.

### Three-body color sector

There are exactly:

```text
C(8+3-1,3) = C(10,3) = 120
```

unordered triples with repetition from the eight-value alphabet.

Every row obeys:

```text
M3(a,b,c) = 36 * (a^2 + b^2 + c^2)
```

Thirteen neutral ground-baryon rows fail the observed-surface gate; the other 107 survive.

### Two-body pair sector

There are exactly:

```text
8 x 8 = 64
```

ordered pair rows.

Every row obeys:

```text
M2(a,b) = 12ab + 3|a-b|
```

The order controls the charge sign. Equal pairs are neutral. Every pair containing `12` is placed in the resonance bin, but remains matter-row allowed in the source table.

### Hidden support

The eight hidden support rows obey:

```text
Lp = p + p^2/144
```

They are lift-bearing source packets and are explicitly not promoted as matter rows.

## Why the 105, 100, and 81 surfaces are related

### 105-row surface

The 105-row surface is a projection of the 114-row one-body sector:

```text
63 direct stable rows + 42 conjugates = 105
```

It excludes the nine deepest direct resonance rows.

### 100-row L162 projection

Removing the five role occurrences at `(p=9,g=0)` gives:

```text
105 - 5 = 100 rows
sum M_native = 16,200 = 100 * 162 = 100L
```

This is a full-ledger normalization of the one-body payload after the W9 packet is excluded.

### 81-row M126 projection

The explicit 81-row sheet contains:

```text
30 matter rows
30 matched antimatter rows
16 neutral rows
5 unpaired reclassified resonance rows
---
81 rows
```

Its depth structure is:

```text
g=0: 39 rows
g=1: 35 rows
g=2: 7 rows
```

and:

```text
sum M_native = 12,600 = 100 * 126 = 100M
```

The sheet excludes the neutral `p=9` occurrence at every depth while retaining charged `p=9` occurrences. That is evidence for a role-sensitive witness interpretation, not a rule that every scalar nine must be removed.

The exact selector for the 81-row projection is still not independently derived.

## A newly visible cross-sector checksum

The entire ordered pair sector has:

```text
sum M_native over 64 pair rows = 25,074
```

and:

```text
25,074 = 199 * 126 = 199M
```

The number 199 is also the count:

```text
120 triads
+ 64 pairs
+ 14 carrier/support rows
+ 1 scalar parent
= 199
```

This is an exact cross-sector identity. It is not yet a physical law, but it is strong enough to deserve a precommitted checksum test.

The triad sector also closes exactly as:

```text
sum M_native over 120 triads = 575,100 = 3,550 * 162 = 3,550L
```

## The support-layer count and the octahedral lead

The raw infrastructure layer contains:

```text
6 carrier-only rows
8 hidden support rows
```

Removing the A-field row leaves 13 active carrier/support lanes. Removing the Z/81 structural singleton leaves 12 matter-side lanes.

That produces the count sequence:

```text
6 carrier roles
8 hidden-support roles
12 matter-side lanes
```

This matches the octahedral count signature `(6 vertices, 8 faces, 12 edges)` at the level of counts.

It is a serious test lead, but the sets overlap: the twelve lanes are derived from the fourteen carrier/support rows. It must not be presented as a geometric proof without an incidence rule.

## What the catalog most likely is

The strongest current interpretation is:

```text
one-body rows        = constituent/address states
two-body rows        = pair-link motifs
three-body rows      = color/three-owner closure motifs
hidden supports      = lift-bearing connector packets
carrier-only rows    = non-payload transport or ledger roles
scalar parent        = global closed-loop reveal
rejected rows        = forbidden constructions and explicit controls
```

In other words, QP093A looks more like a finite construction grammar than a list of independent particles.

## Binding implication

The binding model should not sum all 321 rows and should not turn 126, 144, 162, 12,600, or 16,200 into new coefficients.

The useful route is:

1. Use one-body rows for the native constituent account.
2. Use pair rows as the exact library of two-body connection motifs.
3. Use triad rows as the exact library of three-body/color closure motifs.
4. Use hidden supports for lift fees.
5. Exclude carrier-only and witness-only rows from matter payload.
6. Treat the scalar loop as a global reveal, not a repeated isotope constituent.
7. Determine motif counts from isotope geometry and neutron excess before looking at observed binding.
8. Compare the frozen assembly rule on held-out nuclei.

This would change binding from:

```text
fit coefficients to A, Z, and N
```

toward:

```text
solve a constrained assembly problem over an exact finite motif grammar
```

That is the important possibility exposed by the full 321-row catalog.

## Required next validation

The next Courtroom record should freeze and test:

- the complete 321-row combinatorial generation;
- the nested `300/286/171/114/21/14` bucket accounting;
- the `100L`, `100M`, `199M`, and `3550L` checksums;
- neutral-W9 versus charged-nine role separation;
- the 6/8/12 octahedral count lead;
- an isotope assembly algorithm that uses one-, two-, and three-body motifs without binding-target leakage.
