# CR210d Full Fresh Octahedral Complete-Ledger Adapter Precommit

## Record policy

`record_id = CR210d_OCTAHEDRAL_COMPLETE_LEDGER_BOUNDARY_CLOSURE_APPEAL`

`classification = CONSTRUCTIVE_NEW_WORK`

`parent_freeze = PSLI_DF_20260715T025638Z`

`historical_record = CR210c_OCTAHEDRAL_COMPLETE_LEDGER_ADDRESS_ADAPTER`

CR210c remains an immutable historical FAIL at 15/17. Its artifacts are lineage and regression context only. **No CR210c PASS gate is counted as a CR210d PASS.** CR210d must execute all seventeen structural gates freshly from the frozen sources using a standalone runner that neither imports nor transforms any prior runner.

The generated prose in prior result files is not scientific input. Historical status is read only from sealed checks, validation, adjudication, and hash zippers.

## Closed lanes

Starbreaker outcomes, density/permutation runs, workbooks, F81 membership, PDG data, particle labels, particle masses, isotope data, and binding residuals remain closed. No target value, fitted parameter, promoted roster, semantic particle label, or downstream outcome field may enter construction or evaluation.

## Exact source-native premises

For ledger `ell` and slot `s`:

```text
L = 162
Theta = 18
M = 126
N = 144

atom_id = 162*ell + s
route = (s + 6*ell) mod 12
dimension = s mod 3
side = s mod 2
```

Source kind boundaries:

```text
s = 0..17     carrier
s = 18..143   matter
s = 144..161  ledger_shadow
```

## Frozen structural constructions

### W9 x K18 inventory

Divide the canonical 162-slot ledger into nine consecutive 18-slot blocks. Blocks 0..7 receive the eight declared binary face-sign addresses; block 8 receives the closure/full-cell address. The declared representative uses block offsets 0..11 for route-edge addresses and 12..17 for dimension-side point addresses.

The representative split is not source-unique and may not be promoted as unique.

### Route-edge candidate

For route `r`:

```text
d = r mod 3
s = r mod 2
h = floor(r/6)

v1 = (d,s)
v2 = ((d+1+h) mod 3, s XOR h)
edge(r) = unordered(v1,v2)
```

### Six source-native fibers

For dimension `d` and side `h`:

```text
rho = (4*d + 3*h) mod 6
slot = rho + 6*j, j=0..26
```

Centered base-three coordinates assigned by `j` are a constructed audit label, not source dynamical topology.

### H27 face-poset candidate

Use all 27 coordinates in `{-1,0,1}^3`:

```text
rank0: 1 cell
rank1: 6 points
rank2: 12 edges
rank3: 8 faces
```

Add 8 cell-face, 24 sign-compatible face-edge, and 24 sign-compatible edge-point links.

### Boundary maps

The boundary universe is:

```text
B = {0,...,17} union {144,...,161}
|B| = 36
```

Decode `x in B` as:

```text
b = floor(x/18) in {0,8}
t = x mod 18
q = floor(t/6) in {0,1,2}
r = t mod 6 in {0,...,5}
```

Freeze both maps:

```text
phi_cross(b,q,r) = (8-b, q, (r+3) mod 6)
phi_same(b,q,r)  = (b,   q, (r+3) mod 6)
```

The cross-kind map is tested for admissibility. The same-kind map is a neutral comparator. Counts may not select between them.

## Fresh seventeen-gate predictions

### C00 — precommit seal

The 25-source manifest, premises, and this precommit are hash-sealed before the standalone runner exists. The historical records remain unmodified.

### C01 — source contract and lineage

All 25 declared sources match exact hashes and byte counts. The PSLI, CR210c execution, and CR210c outer hash zippers have zero missing or mismatched entries. Revalidation of every source in the CR210c source manifest has zero errors.

### C02 — source-native formulas

The frozen Starbreaker source contains the exact `L=162`, `Theta=18`, `M_native=126`, kind boundaries, and route/dimension/side formulas used by the runner.

### C03 — source kind totals

The canonical template is exactly:

```text
18 carrier + 126 matter + 18 ledger_shadow = 162
```

### C04 — W9 x K18 factorization

There are exactly nine 18-slot blocks with block kind pattern `1 carrier / 7 matter / 1 ledger_shadow`. Every block has 12 declared edge-channel and 6 declared point-channel offsets at both ledger route parities.

### C05 — partition nonuniqueness

Exhaustive enumeration finds exactly 64 disjoint 12/6 partitions per block and ledger parity that preserve full route-12 and point-6 coverage. The declared representative has 63 alternatives; exactly seven valid partitions are contiguous linear 12-slot windows.

### C06 — route-edge candidate

The explicit map gives 12 distinct octahedral edges over six points. Every point has degree four, every route's own dimension-side point is incident, and the map contains no self-edge or same-axis edge.

### C07 — six fibers

There are six exact fibers, each:

```text
3 carrier + 21 matter + 3 shadow = 27
```

Each side is exactly `9 + 63 + 9 = 81`.

### C08 — constructed ternary audit

Each fiber has constructed centered-ternary ranks `1/6/12/8` and kind-rank matrix:

```text
carrier: [0,0,1,2]
matter:  [1,6,10,4]
shadow:  [0,0,1,2]
```

This label must remain distinct from the H27 ontology.

### C09 — H27 graph

The candidate graph has 27 nodes and 56 links:

```text
8 cell-face
24 face-edge
24 edge-point
```

It is connected with degree histogram `{4:26,8:1}`.

### C10 — prior selector control

The safe prior sidecar reproduces 32 links for each of 14 ledgers, component sizes `9+6+6+6`, and degree histogram `{1:8,2:12,4:6,8:1}`.

### C11 — graph replacement, not addition

Prior/H27 intersection is 8, prior-only is 24, H27-only is 48, union is 80, and Jaccard is 0.1. The prior-only 24 are support-complement anti-incidences. H27 with its face-edge layer removed has 32 links but components `18+9`.

### C12 — octahedral automorphisms

All 48 signed-axis transformations preserve the H27 node and edge sets. Axis names and global orientation are not selected.

### C13 — side reversal

Each side has `9 carrier + 63 matter + 9 shadow = 81`, and global side reversal preserves the structural graph.

### C14 — complete modulo-6 boundary quotient

Apply `phi_cross` independently to all 36 directed boundary occurrences before canonicalizing pairs. All of the following must hold:

```text
domain = B
image = B
domain size = image size = 36
each image multiplicity = 1
fixed points = 0
round-trip mismatches = 0
unordered pair classes = 18
carrier-shadow pair classes = 18
q changes = 0
dimension changes = 0
side-flip failures = 0
K18-channel changes = 0
out-of-boundary outputs = 0
out-of-ledger outputs = 0
```

The exact canonical pair roster is:

```text
0-147, 1-148, 2-149, 3-144, 4-145, 5-146
6-153, 7-154, 8-155, 9-150, 10-151, 11-152
12-159, 13-160, 14-161, 15-156, 16-157, 17-158
```

Under each ledger route parity, all 36 directed mappings preserve route hemisphere and map point and route-edge addresses antipodally. The route-parity audit therefore has 72 rows with 72 point-antipode and 72 edge-antipode passes.

The quotient is exactly:

```text
side A = 81
side B = 81
intersection = 18 = Theta
union = 144 = N
symmetric difference = 126 = M
occurrence sum = 162 = L
```

The same-kind comparator also yields 18 pairs over all 36 boundary occurrences and the same cardinality ladder. Boundary orientation therefore remains open.

### C15 — controls and conditional uniqueness

Enumerate all `6! = 720` residue permutations while block flip and `q` preservation are frozen:

```text
dimension-preserving permutations = 8
side-flipping permutations = 36
both dimension-preserving and side-flipping = 1
unique joint map = [3,4,5,0,1,2]
```

This is uniqueness only under the declared typed constraints; it is not physical orientation selection.

Required controls:

- the exact CR210c regression `r+3` without modulo, evaluated over all 36 directed occurrences: 18 `q` changes, 6 outputs outside `B`, and 3 outputs outside `0..161`;
- half-domain enumeration: 9 pair classes and only 18 used boundary occurrences;
- `r+1 mod6`: side flips but dimension and involution gates fail;
- residue identity: not side-flipping and not antipodal;
- `q -> q+1`: locality and involution fail;
- no pairing: union and symmetric difference remain 162;
- many-to-one: bijection and class-count failure;
- same-kind antipodal comparator: expected count success, not a failed control;
- global side reversal: expected invariant.

C15 must be computed independently of C14's aggregate Boolean so a failed cross-kind candidate cannot falsely mark the same-kind comparator itself as failed.

### C16 — firewall

The fresh run opens no outcome, density/permutation result, workbook, F81 membership, PDG target, mass, isotope, or binding source; uses no forbidden field; and fits no parameter.

## Verdict policy

If and only if all seventeen fresh gates pass, CR210d may issue:

```text
CR210d_PASS_EXACT_SOURCE_NATIVE_W9_BY_K18_ADDRESS_FACTORIZATION__SLOT_PARTITION_ROUTE_EDGE_OVERLAP_ORIENTATION_AND_PHYSICAL_INCIDENCE_OPEN
```

That verdict establishes a full fresh structural adapter PASS with an admissible modulo-6 cross-kind boundary map. It does not establish:

- that cross-kind orientation is uniquely preferred over the same-kind comparator;
- Starbreaker dynamical adjacency;
- physical particle geometry;
- carrier/shadow physical identity;
- F81 projection or row membership;
- any PDG identity, mass relation, or binding improvement.

CR210c remains historically FAIL and is not rewritten. Any source, lineage, arithmetic, topology, boundary, control, or firewall failure yields a fresh CR210d FAIL. No same-run repair is permitted.

## Required fresh artifacts and row counts

```text
CR210d_SOURCE_VALIDATION.csv                 25 rows
CR210d_LINEAGE_INTEGRITY.csv                one row per hash-zipper entry
CR210d_SLOT_TEMPLATE.csv                    162 rows
CR210d_BLOCK_AUDIT.csv                       9 rows
CR210d_PARTITION_AUDIT.csv                  18 rows
CR210d_ROUTE_EDGE_MAP.csv                   12 rows
CR210d_FIBER_AUDIT.csv                       6 rows
CR210d_TERNARY_RANK_AUDIT.csv               72 rows
CR210d_H27_NODES.csv                        27 rows
CR210d_H27_LINKS.csv                        56 rows
CR210d_PRIOR_SELECTOR_AUDIT.csv             14 rows
CR210d_GRAPH_COMPARISON.csv                  metric rows
CR210d_AUTOMORPHISM_AUDIT.csv               48 rows
CR210d_SIDE_AUDIT.csv                        2 rows
CR210d_BOUNDARY_DIRECTED_AUDIT.csv          36 rows
CR210d_CROSS_KIND_PAIR_CLASSES.csv          18 rows
CR210d_ROUTE_PARITY_AUDIT.csv               72 rows
CR210d_SAME_KIND_COMPARATOR.csv             18 rows
CR210d_BOUNDARY_QUOTIENT_AUDIT.csv           2 rows
CR210d_RESIDUE_PERMUTATION_UNIQUENESS.csv  720 rows
CR210d_WRONG_CONTROLS.csv                   control rows
CR210d_CHECKS.csv                           17 rows
CR210d_FORBIDDEN_FIELD_FIREWALL.json
CR210d_CURRENT_STATUS.json
CR210d_result.md
CR210d_SUMMARY.json
CR210d_PROVENANCE.json
CR210d_COMMAND_LOG.json
CR210d_VALIDATION.json
CR210d_EXECUTION_HASHES.txt
```

The runner must be standalone and execute once only through `tools/run_sam_test.py`. Stop after the structural packet, validate it, and hard-freeze it. Do not begin the PDG campaign inside CR210d.
