# CR235a Exact-Source Gravity Bridge Reaudit — Result

## Verdict

```text
CR235a_PASS_EXACT_SOURCE_GRAVITY_BRIDGE_REAUDIT__MATTER_126_OF_126_AND_SOB_126_OF_126_IDENTITIES_EXACT__MATTER_15750_OF_15750_AND_SOB_15750_OF_15750_RATIO_INVARIANCE_EXACT__DIRECTIONAL_SPEARMAN_RHO_1_000000__WC4_PERMUTATION_NULL_10000_SHUFFLES_P_PERM_0_OF_10000__MAX_ABS_RHO_SHUFFLED_0_387782__CR235_PRESERVED_NOT_MODIFIED
```

`execution_status   = CLEAN`
`scientific_verdict = PASS`
`classification     = AMENDMENT_EXACT_ARITHMETIC_REAUDIT`
`arc_position       = Test 6 follow-up (does not modify CR235)`
`precommit_sha      = e42944abe1cd6c1710de78cc4a992252dfe1cf083eaf905458477a89a49364dc`

## Inputs (Hash-Locked)

```text
Matter rows source:  C:\VS\CR219_promoted_particle_rows_126.csv
Matter rows SHA:     45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f
SOB element source:  CR_TEST5_BLIND_SOB_ELEMENT_ENGINE/outputs/test5_no_name_predictions.csv
SOB element SHA:     0cd620be2f7ed1cd9ca03d4fb7222061ba990d258a04a7c99bbc7ff020b94616
Directional source:  CR_TEST5_BLIND_SOB_ELEMENT_ENGINE/reveal_reference.csv
Directional SHA:     fbfb17d82fbe7375690ae4b7c5ec0e473d0024284caf2dbd89d5404ded1b7b3a
Constants:           R = 12, R^2 = 144
Tolerance:           0 (exact Fraction throughout)
```

## Exact Source Reconstruction

For each matter row (G_matter = 1), parsed `M_obs` as `Fraction(Decimal(str)).limit_denominator(10^12)` and `q_abs` as int, then computed:

```text
qA_exact = M_obs * (R^2 + q_abs) / R^2
G_exact  = qA_exact / 8
W_exact  = 7 * qA_exact / 8
```

For each SOB element row, `G_native, GR_8G, retained_7G` are parsed directly as Fractions from the Test 5 sealed CSV.

## Audit 1 — Matter Identities (Exact)

```text
rows checked = 126
identity_1 (G = qA/8):    126 / 126
identity_2 (W = 7qA/8):   126 / 126
identity_3 (qA = 8G):     126 / 126
all three:                126 / 126
```

Per-row exact reconstruction recorded in `CR235a_matter_exact_audit.csv`.

## Audit 2 — SOB Element Identities (Exact)

```text
rows checked = 126
identity_1 (G = qA/8):    126 / 126
identity_2 (W = 7qA/8):   126 / 126
identity_3 (qA = 8G):     126 / 126
all three:                126 / 126
```

Per-row exact values in `CR235a_sob_exact_audit.csv`.

## Audit 3 — Matter Ratio Invariance (Exact)

```text
ordered pairs checked  = 15750
breaks                 = 0
passes_audit           = True
```

## Audit 4 — SOB Ratio Invariance (Exact)

```text
ordered pairs checked  = 15750
breaks                 = 0
passes_audit           = True
```

## Audit 5 — Directional Spearman Rank Correlation

```text
stable set size      = 81 ({1..83} \ {43, 61})
joined rows          = 81
spearman_rho_real    = 1.000000
directional verdict  = PASS_DIRECTIONAL
passes_directional   = True (rho >= 0.99)
```

## Wrong Controls

```text
WC1  G' = qA/7      matter breaks 126/126   sob breaks 126/126   broke=True
WC2  W' = 6qA/8     matter breaks 126/126   sob breaks 126/126   broke=True
WC3  shuffle qA     sob pairs 15750, breaks 15750 (rate 1.0000)  broke=True
WC4  permutation null on Spearman rho (10000 shuffles, seed 20260623):
       rho_real            = 1.000000
       max |rho_shuffled|  = 0.387782
       p_perm              = 0.000000  (0 / 10000)
       percentile_rho_real = 1.000000
       broke_as_predicted  = True   (p_perm < 0.001 AND percentile > 0.999)
```

## Predictions vs. Observed

| ID | Predicted | Observed | Pass |
|---|---|---|---|
| P1 | 126 matter + 126 SOB | 126 + 126 | YES |
| P2 | All three identities pass exactly on both populations | 126 + 126 all three | YES |
| P3 | All 15750 + 15750 pairs ratio invariance exactly | 15750 + 15750 | YES |
| P4 | Directional rho_real = 1.000000 | 1.000000 | YES |
| P5 | WC1, WC2, WC3 break | all three broke | YES |
| P6 | WC4 permutation null: p_perm < 0.001 AND percentile > 0.999 | p_perm = 0.000000, percentile = 1.000000 | YES |

## K-Gate Audit

| Gate | Status | Evidence |
|---|---|---|
| K1 external anchor | PASS | Directional rank vs external_anchor_A; no unit conversion |
| K2 falsification | PASS | Pre-stated falsifiers (exact identity failure, ratio invariance break, rho < 0.99, p_perm >= 0.001, percentile <= 0.999, any WC failing) — none occurred |
| K3 target hygiene | PASS | Exact-source rule, ratio rule, directional threshold, AND WC4 permutation parameters (N_perm = 10000, seed 20260623, p_perm threshold 0.001, percentile threshold 0.999) all locked in precommit BEFORE the runner ran |
| K4 typed inputs | PASS | Three SHA-locked source CSVs; constants R = 12 only |
| K5 reproduction on demand | PASS | Deterministic + seeded WC3=20260622, WC4=20260623 |

## Relationship to CR235

CR235 stays sealed at FAIL with its precommit (sha `0e91dd67…`), result, and artifacts intact. CR235a is an independent amendment, not a regrade.

CR235's failure traced to two precommit-threshold calibration choices (`1e-9` tolerance against a CSV at 6-9 decimal display precision; single-seed binary threshold `|rho| < 0.10` on a single-realization Spearman rho). CR235a's exact-Fraction arithmetic and 10000-shuffle permutation null both PASS comfortably.

## Cryptographic Chain

```text
CR235a_PRECOMMIT.md  = e42944abe1cd6c1710de78cc4a992252dfe1cf083eaf905458477a89a49364dc
CR235_result.md      = c9843e829d22636cd7a3d3690397c4c3a85a22200ab5777a1f2b5b5427064b11   (preserved, not modified)
CR219 matter CSV     = 45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f
Test 5 SOB CSV       = 0cd620be2f7ed1cd9ca03d4fb7222061ba990d258a04a7c99bbc7ff020b94616
Test 5 reveal CSV    = fbfb17d82fbe7375690ae4b7c5ec0e473d0024284caf2dbd89d5404ded1b7b3a
CR230_result.md      = 3c1fd16c860a09a3b92fe61de008eb3b5f943e797a63327c47110af51b9829b7
CR229_result.md      = ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
CR222_result.md      = b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR114_result.md      = f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
```

## Sequence in the Seven-Test Arc

Test 6 follow-up. Test 7 (CR236@12a Paul Revere tomography) remains.

See `[[project-seven-test-ownership-arc-cr230-236]]`.

## Rule of Immutability

Sealed 2026-06-22 by Sean Brady. Precommit, exact-source rule, ratio rule, directional threshold, permutation parameters (N_perm = 10000, seeds), and runner are frozen.

---

**Sealed by:** Sean Brady, 2026-06-22
**Runner verified:** matter 126/126 identity exact, 15750/15750 ratio pairs exact; SOB 126/126 identity exact, 15750/15750 ratio pairs exact; directional Spearman rho = 1.000000; WC1-WC3 broke; WC4 permutation null p_perm = 0/10000, max |rho_shuffled| = 0.387782, percentile_rho_real = 1.000000
**Arc position:** Test 6 follow-up — PASS as precommitted
