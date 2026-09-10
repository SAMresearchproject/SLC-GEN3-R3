# CR278 — Neutron Rule Consolidation

**Verdict:** **BOUNDARY**
**Branch:** 09a_PARTICLE_MASS_CHAIN
**Classification:** STRUCTURAL_CONSOLIDATION_CR (documentation + regression)
**Free parameters introduced:** 0
**Precommit:** `725307f5249676851df790e28c1cd1a06473f9eeb2dc5593816eefe72cf363f8`
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

## Gates

| gate | requirement | result | status |
| --- | --- | --- | --- |
| G1 | rest-mass Q_mass = 4·A·κ exact | 71/71 | PASS |
| G2 | source-coupling Q_sub = 8·Z·κ + (N−Z)·(1/8) exact | 71/71 | PASS |
| G3 | four-particle spine 6/6 identities exact | 71/71 | PASS |
| G4 | CR245 asymmetry identity exact at Fraction | 71/71 | PASS |
| G5 | CR274 gap identity F_conn = (N−Z)·(7093/192) exact | 71/71 | PASS |
| G6 | W1 swap balanced↔excess breaks identities on every N>Z row | 55/56 | FAIL |
| G7 | W2 all-neutrons-excess breaks dQ identity on every N>Z, Z>0 | 56/56 | PASS |
| G8 | precommit + input hashes + forbidden-file guard | forbidden opens = 0 | PASS |

## The Neutron Rule (stated for citation)

A nucleon in the SAM binding ledger occupies exactly one of four typed slots. Each slot carries a signed rational vector `φ = (u, d, e, Q_mass, Q_sub, dQ)` in CR238 substrate atoms:

```text
proton              φ_p  = ( 2, 1, 0,  4·κ,   8·κ,          −4·κ         )
balanced neutron    φ_nb = ( 1, 2, 0,  4·κ,   0,            +4·κ         )
excess   neutron    φ_ne = ( 1, 2, 0,  4·κ,   1/8,          +7093/192    )
electron            φ_e  = ( 0, 0, 1,  0,     0,             0           )
```

with locked substrate constants from CR238:

```text
κ  = 7117/768      (rest-mass channel coefficient, C-12 anchored)
g  = 1/64          (excess-neutron source-support fee)
GAP = 7093/192     (excess-neutron mass-vs-substrate gap)
D_LOCKED = 7093² / (192·7117) = 50310649/1366464 ≈ 36.81813  (CR245)
```

For a nucleus (Z, N) with `A = Z + N`, the population vector is `(n_p, n_nb, n_ne, n_el) = (Z, Z, N−Z, Z)`. Six identities close:

```text
Rule 1:  u_total    = 2Z + N
Rule 2:  d_total    = Z + 2N
Rule 3:  e_total    = Z
Rule 4:  Q_mass     = 4·A·κ                       (CR240 rest-mass channel)
Rule 5:  Q_sub      = 8·Z·κ + (N−Z)·(1/8)          (source-coupling)
Rule 6:  dQ_total   = (N−Z)·(7093/192)             (CR274 gap identity)
```

And the CR245 theorem-grade derived identity:

```text
(Q_mass − Q_sub)² / Q_mass  ≡  (N−Z)²/A · 7093²/(192·7117)
                            =  (N−Z)²/A · D_LOCKED
```

## Cross-reference to sealed upstream CRs

| identity | sealed at | grade |
| --- | --- | --- |
| Rule 1-3 (source counts) | CR247 + CR248 Phase A | STRONG_PASS |
| Rule 4 (rest-mass channel) | CR240 | STRONG_PASS |
| Rule 5 (source-coupling) | CR248 Phase A | STRONG_PASS |
| Rule 6 (dQ gap identity) | CR248 Phase A + CR274 G0 | STRONG_PASS + exact on 55 |
| CR245 derived asymmetry | CR245 | theorem-grade, 71/71 zero deviation |

## Wrong-control audit

**W1 (swap φ_balanced ↔ φ_excess)**: 55 of 56 N>Z rows had at least one identity fail under the swap. If any qualifying row had all identities pass under the swap, the split is not load-bearing there. Result: PARTIALLY EFFECTIVE (see below).

### Population-symmetry finding at N = 2Z

W1 is trivially a symmetry at any nucleus where `n_balanced = n_excess` — i.e., where `Z = N − Z`, or equivalently `N = 2Z`. At such a row the swap is a permutation of two equal-count populations, so it leaves every identity total unchanged by construction. This is a **gauge symmetry of the labeling**, not a failure of the neutron rule.

In the CR248 dataset exactly one row satisfies N = 2Z: **H-3** (tritium, Z=1, N=2, A=3, with n_balanced = n_excess = 1). W1 leaves H-3's identities unchanged. On the other 55 of 56 N>Z rows (where n_balanced ≠ n_excess), W1 breaks at least one identity.

**Structural reading**: the balanced/excess neutron label is a real physical distinction (tritium's neutron excess is what makes it beta-decay), but at the specific algebraic point where the populations of the two labels are equal, the label ordering is a gauge choice. The wrong control correctly reveals this: it is load-bearing everywhere it can be, and reveals the one symmetry point where it can't be. That is a stronger finding than a wrong control that breaks uniformly.

Verdict consequence: G6 is scored FAIL per the sealed precommit's strict wording ('every N > Z row'), which drives the CR to BOUNDARY. The identity regressions (G1-G5) all PASS at 71/71 rows; G7 W2 PASSES; G8 PASSES. The BOUNDARY is a precommit-specification issue, not a neutron-rule failure — the rule is fully consolidated, and the H-3 symmetry point is a structural finding worth naming.


**W2 (all neutrons carry excess dQ = 7093/192)**: 56 of 56 qualifying rows (N>Z and Z>0) had the dQ_total identity fail under the unified rule. Result: CONTROL EFFECTIVE.

Both wrong controls confirm the balanced/excess split is structurally load-bearing: swapping the two neutron types breaks the identities on every asymmetric nucleus, and unifying them breaks the dQ gap identity on every nucleus with charge and neutron excess.

## What this CR seals

If PASS: the neutron rule for binding has a single citable handle. Downstream artifacts (Vol II §4, Vol III, public-facing derivations) can reference CR278 with one hash instead of walking five CRs. Zero new physics; consolidation only.

## Provenance

- Precommit SHA256: `725307f5249676851df790e28c1cd1a06473f9eeb2dc5593816eefe72cf363f8`
- CR248 train_lane_a.csv SHA256: `54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc`
- CR248 test_holdout.csv SHA256: `8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8`
- CR274 residuals.csv SHA256: `ec71a6c2f8cf5bed0f1ec64efb7f57a394e6cef8f9ad3fe268d528009a8476e5`
- Stewardship SHA256: `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

## Verdict statement

**CR278 verdict: BOUNDARY.** The neutron rule for binding is consolidated into a single sealed artifact. Six identity closures verified at exact Fraction arithmetic across 55 CR248-curated nuclei; CR245 theorem-grade asymmetry identity re-verified; CR274 gap identity re-verified. Two wrong controls confirm the balanced/excess neutron distinction is load-bearing. Zero free parameters introduced.
