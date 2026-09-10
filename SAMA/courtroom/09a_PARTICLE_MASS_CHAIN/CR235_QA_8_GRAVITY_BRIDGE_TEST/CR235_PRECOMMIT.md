# CR235 qA/8 Gravity Bridge Test — Precommit

**Date:** 2026-06-22
**Classification:** PROPORTIONAL_SOURCE_BRIDGE (first physics bridge — ratios first, no unit jump)
**Permission status:** GRANTED_BY_USER: Sean Brady, 2026-06-22 ("proceed with Test 6")
**Source:** `C:\Users\drwho\OneDrive\Desktop\Tests.docx` Test 6 ("qA/8 gravity bridge test")
**Part of:** Seven-test ownership arc (Test 6 of 7)
**Status:** PRECOMMITTED before runner execution.

## Scope

Test the proportional source bridge from the substrate ledger to physical gravity, on both row populations the bridge applies to:

1. **Every promoted matter row** of the canonical CR219 table (126 matter rows; the 13 blocked rows are excluded by the gate).
2. **Every SOB element row** of Test 5's sealed no-name engine (126 rows, E001..E126).

The bridge identities under audit (locked):

```text
G(P)   = qA(P) / 8
W(P)   = 7 · qA(P) / 8
qA(P)  = 8 · G(P)
```

And the proportional / ratio identity:

```text
G(P_1) / G(P_2)  =  qA(P_1) / qA(P_2)     for any two rows
```

Plus the externally-directional comparison: for the SOB elements, the predicted G(P) ordering across Z should be monotonic with the conventional atomic mass number (external_anchor_A) over the stable Z range. No absolute-unit conversion; direction only.

## Inputs (Hash-Locked at Execution)

```text
Matter rows source:  C:\VS\CR219_promoted_particle_rows_126.csv
Matter rows SHA:     45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f
SOB element source:  CR_TEST5_BLIND_SOB_ELEMENT_ENGINE/outputs/test5_no_name_predictions.csv
SOB element SHA:     0cd620be2f7ed1cd9ca03d4fb7222061ba990d258a04a7c99bbc7ff020b94616
Directional source:  CR_TEST5_BLIND_SOB_ELEMENT_ENGINE/reveal_reference.csv (external_anchor_A column)
Directional SHA:     fbfb17d82fbe7375690ae4b7c5ec0e473d0024284caf2dbd89d5404ded1b7b3a
Constants:           R = 12, eighth = 8, seven = 7
Tolerance (identity): 1e-9 (matter rows in Decimal precision); 0 (SOB rows in Fraction precision)
```

## Identity Audit (Locked)

For each matter row (G_matter = 1 only):

```text
G_observed(P)   = tensor_carrier_support
qA_observed(P)  = qA_source_support
W_observed(P)   = retained_write_support

Identity 1:  | G_observed  - qA_observed / 8        | <= 1e-9
Identity 2:  | W_observed  - 7 * qA_observed / 8    | <= 1e-9
Identity 3:  | qA_observed - 8 * G_observed         | <= 1e-9
```

For each SOB element row:

```text
G_observed(P)   = G_native
qA_observed(P)  = GR_8G
W_observed(P)   = retained_7G

Identity 1:  G_observed  == qA_observed / 8
Identity 2:  W_observed  == 7 * qA_observed / 8
Identity 3:  qA_observed == 8 * G_observed
```

SOB rows use exact Fraction arithmetic — identities must hold with zero error.

## Ratio Invariance Audit (Locked)

For each row population, verify that the proportional identity holds across every ordered pair (i, j):

```text
G(P_i) / G(P_j)  =  qA(P_i) / qA(P_j)        for all valid i, j (qA(P_j) != 0)
```

Implemented via the cross-product check:

```text
| G(P_i) * qA(P_j) - G(P_j) * qA(P_i) |  <= 1e-9     (matter rows)
G(P_i) * qA(P_j) - G(P_j) * qA(P_i)  ==  0          (SOB rows, exact)
```

For matter rows: every ordered pair from the 126 matter rows.
For SOB element rows: every ordered pair from E001..E126.

## Directional / Externally-Meaningful Audit (Locked)

For the 126 SOB element rows, compute the per-row predicted `G(P)` and join against the external reveal reference's `external_anchor_A` column (joined on Z, source-locked by SHA).

Compute the Spearman rank correlation between predicted `G(P)` and external `external_anchor_A` over the stable Z range:

```text
stable_set = {Z : 1 <= Z <= 83 and Z not in {43, 61}}    (81 rows)
```

Pass conditions:

```text
PASS_DIRECTIONAL      iff  Spearman rho >= 0.99 on the 81-row stable set
PARTIAL_DIRECTIONAL   iff  0.95 <= rho < 0.99
FAIL_DIRECTIONAL      iff  rho < 0.95
```

The directional audit asks: does heavier conventional mass correspond to larger native G under the bridge, monotonically? Yes/no on direction; NO absolute-unit scaling is performed.

## Wrong Controls (Precommitted)

- **WC1 — Wrong tensor ratio G' = qA/7:** Compute `G' = qA/7` for every row, compare to observed G. Expected: BREAK on every nonzero row.
- **WC2 — Wrong retained ratio W' = 6·qA/8:** Compare against observed W. Expected: BREAK on every nonzero row.
- **WC3 — Shuffle qA across rows (seed 20260622):** Recompute ratio cross-product `G(P_i)·qA'(P_j) - G(P_j)·qA'(P_i)` and verify the ratio invariance breaks. Expected: BREAK on the majority of pairs.
- **WC4 — Shuffle SOB G(P) labels across Z (seed 20260623):** Recompute Spearman rho against external_anchor_A. Expected: rho falls below 0.10 (no direction preserved).

## Pass Condition (Precommitted)

```text
PASS  iff  ALL of:
  (1)  Every matter row passes the three identities within 1e-9
  (2)  Every SOB element row passes the three identities exactly
  (3)  Every matter-row ordered pair passes the ratio invariance within 1e-9
  (4)  Every SOB-element ordered pair passes the ratio invariance exactly
  (5)  Spearman rho >= 0.99 for SOB-element directional audit
  (6)  All four wrong controls break as predicted
```

## Precommitted Predictions

- **P1:** 126 matter rows; 126 SOB element rows.
- **P2:** Identity 1 (G = qA/8) holds for all 126 matter and all 126 SOB rows.
- **P3:** Identity 2 (W = 7qA/8) holds for all 126 matter and all 126 SOB rows.
- **P4:** Identity 3 (qA = 8G) holds for all 126 matter and all 126 SOB rows.
- **P5:** Ratio invariance: 126·125 = 15750 ordered pairs per population; all pass.
- **P6:** Spearman rho (G_SOB vs external_anchor_A, stable set n=81) >= 0.99.
- **P7:** WC1 breaks on all nonzero rows.
- **P8:** WC2 breaks on all nonzero rows.
- **P9:** WC3 ratio invariance breaks on >50% of pairs.
- **P10:** WC4 Spearman rho falls below 0.10 under shuffle.

## K-Gate Audit (Plan)

| Gate | Statement | Plan |
|---|---|---|
| K1 | External anchor | Directional audit compares to external_anchor_A AFTER the bridge identity is verified internally; ratios only, no unit conversion |
| K2 | Falsification | Any identity row failing within tolerance, OR ratio invariance breaking, OR rho < 0.99, OR any WC failing to break, falsifies |
| K3 | Target hygiene | Identities, tolerance, ratio test, directional pass threshold, and WCs locked here BEFORE the runner ran |
| K4 | Typed inputs | Two SHA-locked CSVs (matter + SOB); R = 12; no measured-mass values enter the engine |
| K5 | Reproduction on demand | Deterministic + seeded controls (WC3 seed 20260622; WC4 seed 20260623) |

## Falsifier

If any of P2-P10 fails, CR235 fails. The bridge is allowed to claim only:

```text
The proportional source bridge G = qA/8 is internally exact across both the matter-row
and SOB-element-row populations, and its predicted G(P) ranks monotonically with the
external atomic mass number across the 81 stable elements (rho >= 0.99).
```

CR235 may NOT claim that SAM derived gravitational acceleration in m/s², or atomic mass in u. Those require a separate native-to-physical unit conversion, sealed in a different CR.

## Sequence in the Seven-Test Arc

Test 6 of 7. Test 7 (CR236@12a Paul Revere tomography) remains.

See `[[project-seven-test-ownership-arc-cr230-236]]`.
