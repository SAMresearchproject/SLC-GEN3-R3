# CR235a Exact-Source Gravity Bridge Reaudit — Precommit

**Date:** 2026-06-22
**Classification:** AMENDMENT_EXACT_ARITHMETIC_REAUDIT (does not modify CR235)
**Permission status:** GRANTED_BY_USER: Sean Brady, 2026-06-22 (diagnosis + new spec for CR235a)
**Part of:** Seven-test ownership arc — Test 6 follow-up
**Status:** PRECOMMITTED before runner execution. CR235 result.md is preserved and not modified.

## Scope

CR235 produced a FAIL verdict that traced to two precommit-threshold choices, not to a broken bridge:

1. The CR235 precommit set matter-row identity tolerance at `1e-9`, but CR219 stores the qA / G / W columns at 6-9 decimal-place display precision (e.g., QP093A-0001: `8G = 1.258680552` vs stored `qA = 1.258680556`, residue `4e-9`). The bridge math is correct; the comparison used a tolerance below the source's precision.

2. The CR235 precommit fixed WC4 to a single shuffle seed with `|rho| < 0.10`. Observed shuffled `rho = -0.107520` — within Monte Carlo noise of the threshold. A single-seed binary threshold on a single-realization Spearman rho is brittle.

CR235a re-runs Test 6 with exact-source arithmetic (Fraction throughout) and a permutation-null WC4.

CR235 is not regraded. CR235's verdict and artifacts stay as the audit trail.

## Inputs (Hash-Locked at Execution)

```text
Matter rows source:  C:\VS\CR219_promoted_particle_rows_126.csv
Matter rows SHA:     45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f
SOB element source:  CR_TEST5_BLIND_SOB_ELEMENT_ENGINE/outputs/test5_no_name_predictions.csv
SOB element SHA:     0cd620be2f7ed1cd9ca03d4fb7222061ba990d258a04a7c99bbc7ff020b94616
Directional source:  CR_TEST5_BLIND_SOB_ELEMENT_ENGINE/reveal_reference.csv
Directional SHA:     fbfb17d82fbe7375690ae4b7c5ec0e473d0024284caf2dbd89d5404ded1b7b3a
Constants:           R = 12; gate denominator = 144 = R^2
Tolerance:           0 (exact Fraction arithmetic for all matter and SOB rows)
```

## Exact Source Reconstruction (Locked)

For each matter row (G_matter = 1):

```text
M_obs_exact     = Fraction(M_observed_candidate string).limit_denominator(10^12)
q_abs_exact     = integer parse of q_abs
qA_exact        = M_obs_exact * (R^2 + q_abs_exact) / R^2          # = M_obs * (1 + |q|/144)
G_exact         = qA_exact / 8
W_exact         = 7 * qA_exact / 8
```

For each SOB element row: parse `G_native, GR_8G, retained_7G` columns from Test 5 as Fractions (they are already exact in the CSV per Test 5's Fraction-output formatter).

## Identity Audit (Exact)

For each row in each population, verify:

```text
Identity 1:  G_exact      == qA_exact / 8
Identity 2:  W_exact      == 7 * qA_exact / 8
Identity 3:  qA_exact     == 8 * G_exact
```

All comparisons exact (Fraction). Zero residue required.

## Ratio Invariance Audit (Exact)

For every ordered pair `(i, j)` in each population, verify:

```text
G_exact(P_i) * qA_exact(P_j)  ==  G_exact(P_j) * qA_exact(P_i)
```

Exact equality. 126 · 125 = 15750 pairs per population.

## Directional Audit (Same as CR235)

Spearman rank correlation between predicted `G(P)` and external `external_anchor_A` over the 81-row stable Z set `{1..83} \ {43, 61}`.

Pass conditions:

```text
PASS_DIRECTIONAL      iff  rho >= 0.99
PARTIAL_DIRECTIONAL   iff  0.95 <= rho < 0.99
FAIL_DIRECTIONAL      iff  rho < 0.95
```

## Wrong Controls

WC1, WC2, WC3 unchanged from CR235.

WC4 — **PERMUTATION NULL TEST**:

```text
Run N_perm = 10000 random permutations of the G(P) labels across Z.
For each permutation, compute Spearman rho_shuffle vs external_anchor_A.
Record the distribution of |rho_shuffle|.
Compute:
  p_perm = (#shuffles with |rho_shuffle| >= |rho_real|) / N_perm
  percentile_rho_real = (#shuffles with |rho_shuffle| < |rho_real|) / N_perm

Pass conditions (WC4 must satisfy BOTH):
  (a) p_perm < 0.001
  (b) percentile_rho_real > 0.999

Seed: 20260623 (same as CR235's WC4 master seed; full distribution sampled).
```

## Pass Condition (Precommitted)

```text
PASS  iff  ALL of:
  (1)  Every matter row passes the three exact identities (trivially by construction)
  (2)  Every SOB element row passes the three exact identities
  (3)  Every matter-row ordered pair passes the ratio invariance exactly
  (4)  Every SOB-element ordered pair passes the ratio invariance exactly
  (5)  Spearman rho_real >= 0.99
  (6)  WC1, WC2, WC3 break as predicted
  (7)  WC4 permutation null: p_perm < 0.001 AND percentile_rho_real > 0.999
```

## Note on Pass Condition (1)

Identity (1) is satisfied by construction because G_exact is DEFINED as qA_exact/8 in the recomputation. This is not testing the SAM bridge — it is testing that the exact computation pipeline is internally consistent and reproducible. The substantive empirical content of CR235a is in conditions (4), (5), and (7).

## Precommitted Predictions

- **P1:** 126 matter rows + 126 SOB element rows after exact reconstruction.
- **P2:** All three identities pass exactly on both populations (by construction for matter; by Test 5 engine math for SOB).
- **P3:** All 15750 + 15750 ordered pairs pass ratio invariance exactly.
- **P4:** Directional rho_real = 1.000000 (same as CR235 because the SOB G values feeding the rank correlation are unchanged from Test 5's sealed CSV).
- **P5:** WC1, WC2, WC3 all break as predicted.
- **P6:** WC4 permutation null: rho_real = 1.000000 is unreachable by any shuffle of 81 ranks against 81 distinct values, so `p_perm = 0` (or very close) and `percentile_rho_real > 0.999`.

## K-Gate Audit (Plan)

| Gate | Statement | Plan |
|---|---|---|
| K1 | External anchor | Same as CR235 — directional rank only, no unit conversion |
| K2 | Falsification | Any identity / ratio / directional / WC condition failing as precommitted falsifies |
| K3 | Target hygiene | Exact-source rule, ratio rule, directional threshold, AND WC4 permutation parameters (N_perm = 10000, seed 20260623, thresholds p_perm < 0.001 AND percentile > 0.999) locked here BEFORE the runner ran |
| K4 | Typed inputs | Same SHA-locked CSVs as CR235 |
| K5 | Reproduction on demand | Deterministic + single seed for WC4 (sample the full 10000-shuffle distribution from one seed) |

## Falsifier

If any of P2-P6 fails under exact arithmetic and 10000-shuffle permutation, CR235a fails.

## Relationship to CR235

CR235 stays sealed at FAIL. CR235a is an independent amendment that audits the same bridge under exact-source arithmetic and a permutation null. Neither modifies the other.

If CR235a PASSES, the manuscript may cite CR235a as the operative test of the qA/8 bridge, while preserving CR235 as the audit trail showing the tolerance-calibration failure.

## Sequence in the Seven-Test Arc

Test 6 follow-up. Test 7 (CR236@12a Paul Revere tomography) still pending.

See `[[project-seven-test-ownership-arc-cr230-236]]`.
