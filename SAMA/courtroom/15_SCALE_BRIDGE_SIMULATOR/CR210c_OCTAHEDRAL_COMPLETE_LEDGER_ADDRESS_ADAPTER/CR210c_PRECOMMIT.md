# CR210c Octahedral Complete-Ledger Address Adapter Precommit

## Record and immutable lineage

`record_id = CR210c_OCTAHEDRAL_COMPLETE_LEDGER_ADDRESS_ADAPTER`

`parent_freeze = PSLI_DF_20260715T025638Z`

`successor_of = CR210b_FAIL_PRECOMMITTED_STRUCTURAL_CHECK`

CR210a remains frozen as a pre-verdict serializer failure. CR210b remains frozen at 15/17 with C14 and dependent C15 failed. Neither record is rerun or rewritten.

CR210c inherits the scientific algorithm base at SHA-256 `094d39be033db8dfe7bd1b78c845abf8839dbba1f36b31987af3d3bfb7616d1a`. It carries forward CR210b's deterministic set-safe check-display serializer and corrects one mismatch between the frozen formula and its enumerator:

```text
frozen cross-kind domain: r = 0..5
CR210b implemented domain: r = 0..2
CR210c implemented domain: r = 0..5 for cross-kind; r = 0..2 per boundary block for same-kind
```

No candidate formula, expected value, threshold, control, firewall, or verdict ceiling changes.

## Closed lanes

Starbreaker outcomes, density/permutation runs, workbook membership, QP093A 81-roster membership, F81 targets, isotope data, binding fields, and binding residuals remain closed. Fitted parameter count is zero.

## Exact source premises

```text
L = 162
Theta = 18
M = 126
N = 144
V = 6
E = 12
F = 8

atom_id = 162*ell + slot
route = (slot + 6*ell) mod 12
dimension = slot mod 3
side = slot mod 2
```

Source kinds remain carrier 0..17, matter 18..143, ledger-shadow 144..161.

## Frozen candidate

1. Divide the ledger into nine consecutive 18-slot blocks: one carrier block, seven matter blocks, one closure/shadow block.
2. Use the declared representative 12-route/6-point split within each block while explicitly preserving its nonuniqueness.
3. Map route `r` to the unordered edge:

```text
d = r mod 3
s = r mod 2
h = floor(r/6)
v1 = (d,s)
v2 = ((d+1+h) mod 3, s XOR h)
```

4. Audit the orthogonal six fibers using `rho=(4d+3h) mod6`, `slot=rho+6j`, `j=0..26`.
5. Construct H27 on `{-1,0,1}^3` with 8 cell-face, 24 face-edge, and 24 edge-point links.
6. Compare the two frozen boundary maps:

```text
cross-kind: phi(b,q,r) = (8-b, q, (r+3) mod6), b=0, r=0..5
same-kind:  phi(b,q,r) = (b,   q, (r+3) mod6), b in {0,8}, representatives r=0..2
```

The constructions are address candidates, not physical identities.

## Frozen predictions

P1. All 20 declared sources match exact hashes and byte counts.

P2. Source typing is exactly `18 + 126 + 18 = 162`.

P3. There are nine 18-slot blocks with kind pattern 1/7/1 and representative 12+6 coverage at both route parities.

P4. Every block/parity has exactly 64 valid route-point partitions, 63 alternatives, and seven contiguous 12-slot windows.

P5. The route-edge map gives 12 distinct edges over six points, point degree four, and 12/12 incident route anchors.

P6. Six fibers each contain `3 + 21 + 3 = 27`; each side is `9 + 63 + 9 = 81`.

P7. The declared constructed ternary label gives per-fiber rank `1/6/12/8` and kind-rank matrix carrier `[0,0,1,2]`, matter `[1,6,10,4]`, shadow `[0,0,1,2]`.

P8. H27 has 27 nodes, 56 links, one component, degree histogram `{4:26,8:1}`, and all 48 signed-axis automorphisms.

P9. The prior sidecar has 32 links for each of 14 ledgers, components `9+6+6+6`, degrees `{1:8,2:12,4:6,8:1}`.

P10. Prior/H27 intersection is 8, prior-only 24, H27-only 48, union 80, Jaccard 0.1. H27 without face-edge links has 32 links and components 18+9.

P11. Each boundary map produces exactly 18 pairs using all 36 boundary occurrences once, with no fixed points, dimension/microcycle preservation, side flip, point/edge antipodes, and accounting `81+81-18=144`, symmetric difference 126, occurrence sum 162.

P12. All 16 frozen wrong controls behave as declared.

P13. No forbidden path or field is opened; outcomes, F81, workbooks, and binding remain closed.

## Wrong controls

Preserve the old disconnected 32-link selector, H27 with face-edge layer deleted, 63 alternate valid splits, missing-axis route map, K12-only, K6-only, wrong E10 radix, cube/dual swap, padded tetrahedron, no pairing, many-to-one pairing, adjacent-r pairing, same-kind antipodal comparator, global side reversal, all 48 signed-axis automorphisms, and centered-ternary identity rejection.

## Verdict ceiling and stop

Maximum PASS:

```text
CR210c_PASS_EXACT_SOURCE_NATIVE_W9_BY_K18_ADDRESS_FACTORIZATION__SLOT_PARTITION_ROUTE_EDGE_OVERLAP_ORIENTATION_AND_PHYSICAL_INCIDENCE_OPEN
```

Even on PASS, Starbreaker dynamical adjacency, physical route-edge identity, carrier/shadow identity, F81 membership, particle assembly, isotope transport, and binding remain open.

No same-run repair is permitted. Stop after one wrapper-mediated structural execution and freeze its artifacts.
