# CR210b Octahedral Complete-Ledger Address Adapter Precommit

## Record and lineage

`record_id = CR210b_OCTAHEDRAL_COMPLETE_LEDGER_ADDRESS_ADAPTER`

`parent_freeze = PSLI_DF_20260715T025638Z`

`successor_of = CR210a_EXECUTION_FAILURE_BEFORE_STRUCTURAL_VERDICT`

`classification = CONSTRUCTIVE_NEW_WORK`

CR210a is immutable and is not rerun. Its single execution stopped before a structural verdict because its check-display serializer could not encode a Python set. CR210b inherits the exact CR210a scientific algorithm body at SHA-256 `094d39be033db8dfe7bd1b78c845abf8839dbba1f36b31987af3d3bfb7616d1a`.

The only permitted executable changes are:

1. successor record/file/task identity;
2. source-count and local sealed-hash administration for this successor;
3. recursive, deterministic conversion of sets and tuples to JSON-safe display arrays before check values are serialized.

No candidate map, formula, prediction, threshold, wrong control, firewall, or verdict ceiling may change.

## Closed lanes

Starbreaker outcomes, density runs, permutation runs, workbook membership, QP093A 81-roster membership, F81 targets, isotope data, binding fields, and binding residuals remain closed. No fitted parameter is allowed.

## Exact premises

```text
L = 162
Theta = 18
M = 126
N = 144
V = 6
E = 12
F = 8
```

For ledger `ell` and slot `s`:

```text
atom_id = 162*ell + s
route = (s + 6*ell) mod 12
dimension = s mod 3
side = s mod 2
```

Source kinds are carrier slots 0..17, matter slots 18..143, and ledger-shadow slots 144..161.

## Frozen candidate constructions

### W9 x K18 inventory

Partition the 162-slot template into nine consecutive 18-slot blocks. Blocks 0..7 receive the eight declared binary face-sign addresses; block 8 receives the closure/full-cell address. Within each block the declared representative convention uses offsets 0..11 for route-edge addresses and offsets 12..17 for dimension-side point addresses.

This is an address convention, not a physical identity claim.

### Route-edge address function

For route `r`:

```text
d = r mod 3
s = r mod 2
h = floor(r/6)
v1 = (d,s)
v2 = ((d+1+h) mod 3, s XOR h)
```

The unordered pair `(v1,v2)` is the candidate edge address.

### Six source-native fibers

For dimension `d` and side `h`:

```text
rho = (4*d + 3*h) mod 6
slot = rho + 6*j, j=0..26
```

Centered base-three coordinates assigned by `j` are a constructed audit label, not an independently source-native topology.

### H27 candidate face-poset graph

Use all 27 coordinates in `{-1,0,1}^3`:

- rank 0: one cell;
- rank 1: six points;
- rank 2: twelve edges;
- rank 3: eight faces.

Add 8 cell-face, 24 sign-compatible face-edge, and 24 sign-compatible edge-point links.

### Boundary candidates

For boundary blocks `b in {0,8}`, microcycle `q`, and residue `r`:

```text
cross-kind: phi(b,q,r) = (8-b, q, (r+3) mod 6)
same-kind:  phi(b,q,r) = (b,   q, (r+3) mod 6)
```

Both remain frozen candidates; counts alone may not choose between them.

## Frozen predictions

P1. All 20 declared sources match exact bytes and hashes.

P2. The source-native kind total is `18 + 126 + 18 = 162`.

P3. The ledger has exactly nine 18-slot blocks with block kinds `1 carrier / 7 matter / 1 shadow`, and every declared representative split is 12+6 at both route parities.

P4. Exhaustive enumeration finds exactly 64 valid 12/6 route-point partitions per block and parity, 63 alternatives to the representative, and exactly seven contiguous linear windows.

P5. The route-edge candidate gives 12 distinct edges over six points, degree four at every point, with each route's own dimension-side point incident.

P6. There are six exact 27-slot fibers, each `3 carrier + 21 matter + 3 shadow`; each side is `9 + 63 + 9 = 81`.

P7. Under the declared constructed base-three labeling, each fiber has rank counts `1/6/12/8` and kind-rank matrix:

```text
carrier: rank2=1, rank3=2
matter: rank0=1, rank1=6, rank2=10, rank3=4
shadow: rank2=1, rank3=2
```

P8. The H27 graph has 27 nodes, 56 links, one connected component, degree histogram `{4:26, 8:1}`, and is preserved by all 48 signed-axis automorphisms.

P9. The safe prior sidecar reproduces 32 links for each of 14 ledgers, components `9+6+6+6`, and degree histogram `{1:8,2:12,4:6,8:1}`.

P10. Exactly eight prior links overlap H27. The prior-only 24 are support-complement anti-incidences; H27-only is 48, union is 80, Jaccard is 0.1. Removing H27's face-edge layer gives 32 links but components `18+9`.

P11. Each frozen boundary map gives 18 pairs using all 36 boundary occurrences once, preserves dimension and microcycle, flips side, maps points and edges antipodally, and closes `81+81-18=144`, symmetric difference 126, occurrence sum 162.

P12. Every frozen wrong control behaves as declared.

P13. No forbidden path, field, outcome, roster, F81, or binding input is opened or used.

## Wrong controls

The runner must include the prior 32-link selector, H27 without face-edge links, all 63 split alternatives, missing-axis route map, route-only K12, point-only K6, wrong E10 radix, cube/dual swap, padded tetrahedron, no boundary pairing, many-to-one collapse, adjacent-r pairing, same-kind antipodal comparator, global side reversal, all 48 signed-axis automorphisms, and rejection of centered-ternary physical promotion.

## Verdict policy

If every precommitted check passes, the maximum verdict is:

```text
CR210b_PASS_EXACT_SOURCE_NATIVE_W9_BY_K18_ADDRESS_FACTORIZATION__SLOT_PARTITION_ROUTE_EDGE_OVERLAP_ORIENTATION_AND_PHYSICAL_INCIDENCE_OPEN
```

Even on PASS, route-edge physical identity, Starbreaker dynamical adjacency, carrier/shadow physical identity, F81 membership, particle construction, isotope transport, and binding remain open.

If execution fails or any exact source, arithmetic, graph, control, or firewall gate fails, freeze the record without repair. No same-run repair is permitted.

Stop after one wrapper-mediated execution and its structural artifacts. Do not open outcomes or begin binding.
