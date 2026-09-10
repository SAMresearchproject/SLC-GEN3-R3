# CR210a Precommit

## Record

```text
CR210a_OCTAHEDRAL_COMPLETE_LEDGER_ADDRESS_ADAPTER
```

Precommit sealed UTC:

```text
2026-07-15T03:19:23Z
```

Classification:

```text
CONSTRUCTIVE_NEW_WORK
```

Parent freeze:

```text
PSLI_DF_20260715T025638Z
```

The `CR210a` suffix is used because bare `CR211` is already assigned to the
Discovery Intake branch. This record extends the frozen Scale Bridge CR210
without creating a global identifier collision.

## Objective

Test the frozen structural address candidate only. Construct an outcome-blind
complete-ledger occurrence template from the hash-sealed Starbreaker modular
generator and compare:

```text
9 blocks * 18 occurrences = 162
6 (dimension,side) fibers * 27 occurrences = 162
two sides * 81 occurrences = 162
```

Build the candidate octahedral `W9 x K18` address system and the 27-node
octahedral face-poset cover graph. Reproduce the prior 32-link sidecar graph as
a control. Stop without opening Starbreaker outcomes, workbook membership,
F81 targets, isotope data, or binding residuals.

## Frozen source projection

For global complete-ledger index `ell` and local slot `s`:

```text
atom_id   = 162*ell + s
kind      = carrier for s=0..17
            matter for s=18..143
            shadow for s=144..161
route     = atom_id mod 12
dimension = atom_id mod 3
side      = atom_id mod 2
```

Because `162 mod 12 = 6`, route labels rotate by six between even and odd
ledgers. The canonical 162-row template must therefore retain both route
parities or the formula above. Dimension, side, kind, and slot reset exactly.

For `(dimension=d,side=h)`, the slot residue is:

```text
r = (4d + 3h) mod 6
s = r + 6k, k=0..26
```

## Candidate address definitions

### W9 block address

```text
block_index = floor(s/18)
block_slot  = s mod 18
```

Blocks `0..7` are mapped by their three binary digits to the eight oriented
face-address states. Block `8` is the closure/full-cell address. This is a
candidate address convention; it is not a physical face identity.

### K18 skeleton address

The frozen candidate split is:

```text
block_slot 0..11  -> E12 route-address lane
block_slot 12..17 -> V6 (dimension,side)-address lane
```

The candidate route-to-edge map for route `r` is:

```text
d = r mod 3
h = r mod 2
q = floor(r/6)
start = (d,h)
end   = ((d+1+q) mod 3, h XOR q)
```

The unordered `start/end` pair must enumerate all twelve octahedral edges once
and must contain the route's own `(dimension,side)` point. The map is an
address bijection, not a physical route-edge identity.

### H27 face-poset address set

```text
H27 = W9 disjoint-union K18
    = {1 full-cell + 8 faces} + {12 edges + 6 points}
```

The face-poset cover graph must contain:

```text
8  full-cell/face links
24 face/edge links
24 edge/point links
--
56 links total
```

This candidate is separate from both the six 27-occurrence fibers and the
prior sidecar's 27 six-atom cell templates.

## Frozen predictions and discriminants

P1. All 17 source files exist with exact precommit hashes and byte sizes.

P2. The canonical ledger template contains 162 distinct slots, nine complete
18-occurrence blocks, and exact kind blocks `1 carrier + 7 matter + 1 shadow`.

P3. In the declared first-12/last-6 split, every block and both ledger parities
contain all twelve routes exactly once in the first lane and all six
`(dimension,side)` pairs exactly once in the second lane.

P4. The declared split is admissible but not source-unique. Exhaustive
enumeration must find exactly 64 disjoint 12/6 partitions per block/parity that
preserve route-12 and point-6 coverage. Exactly seven are contiguous linear
12-slot windows. The runner must preserve this nonuniqueness boundary.

P5. The explicit route-to-edge address function enumerates all twelve
octahedral edges once and is incident to the route's own point. Arbitrary
route-edge bijections remain label conventions unless a later source action
selects one.

P6. Each of the six `(dimension,side)` fibers contains 27 slots with exact
kind counts `3 carrier + 21 matter + 3 shadow`. Each side contains
`9 carrier + 63 matter + 9 shadow = 81`.

P7. The centered base-three labeling of each ordered 27-set yields rank counts
`1/6/12/8`. It is a constructed combinatorial labeling, not independent
evidence that a fiber is one H27 face poset. Its frozen rank-by-kind matrix is:

```text
carrier: rank2=1, rank3=2
matter:  rank0=1, rank1=6, rank2=10, rank3=4
shadow:  rank2=1, rank3=2
```

P8. The H27 octahedral face-poset graph has 27 nodes, 56 links, one connected
component, one degree-8 full-cell node, and 26 degree-4 nodes. All 48 signed
axis permutations preserve its edge set.

P9. The prior sidecar graph reproduces for all 14 recorded ledgers: 27 nodes,
32 links, components `9+6+6+6`, and degree histogram
`degree1:8, degree2:12, degree4:6, degree8:1`.

P10. Only eight prior links overlap H27, all full-cell/face links. Its 24
rank1/rank2 links are support-complement anti-incidences, not octahedral
point/edge incidences. The 56-link candidate replaces those 24 and adds the
missing 24 face/edge links; it is not `old32 + 24`.

P11. Two explicit boundary pairing candidates each produce 18 two-member
boundary equivalence classes, a 144-class union, and a 126-occurrence symmetric
difference:

```text
A: same-kind antipodal pairing
B: cross-kind carrier/shadow antipodal pairing
```

Candidate B implements the leading mirrored-Theta address hypothesis; A is the
neutral comparator. Counts alone must not choose between them.

P12. Tetrahedral, cube/dual-swap, route-only, point-only, and wrong-radix
factorizations fail the full `126/144/162` ladder at fixed rules.

P13. No forbidden outcome, binding, workbook membership, target count, target
sum, or candidate whitelist source is opened. No parameter is fitted.

## Required wrong controls

WC1. Prior 32-link disconnected body-diagonal selector.

WC2. Support-complement route-to-edge anti-incidence map.

WC3. Tetrahedron `(V,E,F)=(4,6,4)`.

WC4. Cube/point-face swap `(V,E,F)=(8,12,6)`.

WC5. Route-only `K=12` and point-only `K=6` ladders.

WC6. Wrong radix edge count `E=10` with `V=6,F=8`.

WC7. Same-kind versus cross-kind antipodal boundary pairings. Both are valid
count controls; neither may be selected by the target ladder.

WC8. Adjacent-slot, many-to-one, and non-side-flipping boundary maps.

WC9. Global side reversal. Structural results must be invariant.

WC10. All 48 signed-axis automorphisms. Graph predictions must be invariant.

WC11. Centered ternary labeling treated as an observed physical object type.
It must be rejected as a constructed labeling.

WC12. Route identity treated as physical edge identity. It must remain open.

WC13. Any outcome, binding, F81, workbook-81, target-count, or target-sum
selector. This is a firewall failure, not a candidate.

## Verdict policy

If the exact source-native factorizations, candidate bijections, graph checks,
controls, firewall, and hashes pass while the predicted nonuniqueness remains,
the ceiling is:

```text
CR210a_PASS_EXACT_SOURCE_NATIVE_W9_BY_K18_ADDRESS_FACTORIZATION
__SLOT_PARTITION_ROUTE_EDGE_OVERLAP_ORIENTATION_AND_PHYSICAL_INCIDENCE_OPEN
```

Do not issue the stronger physical-adapter PASS while multiple exact slot
partitions and boundary orientations survive.

If any exact source count, graph incidence, source hash, or firewall gate fails,
the record fails. No same-run repair is permitted.

## Required artifacts

```text
CR210a_SOURCE_MANIFEST.json
CR210a_OPENED_FILE_MANIFEST.json
CR210a_FORBIDDEN_FIELD_FIREWALL.json
CR210a_SLOT_TEMPLATE.csv
CR210a_BLOCK_AUDIT.csv
CR210a_ROUTE_POINT_PARTITION_AUDIT.csv
CR210a_ROUTE_EDGE_MAP.csv
CR210a_POINT_FIBER_AUDIT.csv
CR210a_TERNARY_RANK_AUDIT.csv
CR210a_H27_NODE_REGISTER.csv
CR210a_H27_FACE_POSET_EDGES.csv
CR210a_PRIOR_SELECTOR_AUDIT.csv
CR210a_GRAPH_COMPARISON.json
CR210a_AUTOMORPHISM_AUDIT.csv
CR210a_SIDE_AUDIT.csv
CR210a_BOUNDARY_PAIRINGS.csv
CR210a_QUOTIENT_AUDIT.json
CR210a_WRONG_CONTROLS.csv
CR210a_CHECKS.csv
CR210a_PROVENANCE.json
CR210a_result.md
CR210a_summary.json
CR210a_VALIDATION.json
COMMAND_LOG.txt
HASHES.txt
```

Stop after this single structural comparison. Do not open Starbreaker outcomes
or begin packet transport, F81, isotope, or binding work in this campaign.

