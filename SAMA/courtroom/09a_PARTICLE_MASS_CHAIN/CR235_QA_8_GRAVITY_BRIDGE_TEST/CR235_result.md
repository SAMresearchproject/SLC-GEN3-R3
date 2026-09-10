# CR235 qA/8 Gravity Bridge Test — Result

## Verdict

```text
CR235_FAIL_QA_8_GRAVITY_BRIDGE_TEST__MATTER_ROW_IDENTITY_76_OF_126_AT_1E_NEG_9__MATTER_RATIO_BREAKS_8842_OF_15750__SOB_IDENTITY_126_OF_126_EXACT__SOB_RATIO_15750_OF_15750_EXACT__DIRECTIONAL_SPEARMAN_RHO_1_000000__WC4_SHUFFLED_RHO_0_107520_DID_NOT_FALL_BELOW_0_10
```

`execution_status   = CLEAN`
`scientific_verdict = FAIL`
`classification     = PROPORTIONAL_SOURCE_BRIDGE`
`arc_position       = Test 6 of 7 in the Seven-Test Ownership Arc`
`precommit_sha      = 0e91dd6759200d3cf2b8b361632631805a71cf5b311a6c465cc8a8457265538e`

## Inputs (Hash-Locked)

```text
Matter rows source:  C:\VS\CR219_promoted_particle_rows_126.csv
Matter rows SHA:     45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f
SOB element source:  CR_TEST5_BLIND_SOB_ELEMENT_ENGINE/outputs/test5_no_name_predictions.csv
SOB element SHA:     0cd620be2f7ed1cd9ca03d4fb7222061ba990d258a04a7c99bbc7ff020b94616
Directional source:  CR_TEST5_BLIND_SOB_ELEMENT_ENGINE/reveal_reference.csv
Directional SHA:     fbfb17d82fbe7375690ae4b7c5ec0e473d0024284caf2dbd89d5404ded1b7b3a
Constants:           R = 12
Tolerance (matter):  1e-9
Tolerance (SOB):     0 (exact Fraction arithmetic)
```

## Audit 1 — Matter Row Identities

For each of 126 matter rows, verify the three bridge identities within `1e-9`:

```text
rows checked        = 126
identity_1 (G = qA/8):    99 / 126
identity_2 (W = 7qA/8):   82 / 126
identity_3 (qA = 8G):     82 / 126
all three:                76 / 126
```

Per-row residues recorded in `CR235_matter_identity_audit.csv`.

## Audit 2 — SOB Element Row Identities

For each of 126 SOB element rows, verify the three bridge identities exactly (Fraction arithmetic):

```text
rows checked        = 126
identity_1 (G = qA/8):    126 / 126
identity_2 (W = 7qA/8):   126 / 126
identity_3 (qA = 8G):     126 / 126
all three:                126 / 126
```

Per-row results in `CR235_sob_identity_audit.csv`.

## Audit 3 — Matter Ratio Invariance

For each of 15750 ordered pairs `(P_i, P_j)` from the 126 matter rows, verify
`|G(P_i)·qA(P_j) − G(P_j)·qA(P_i)| ≤ 1e-9`:

```text
ordered pairs checked      = 15750
ratio invariance breaks    = 8842
ratio invariance passes    = 6908
largest residue            = 0.000579975
passes_audit               = False
```

## Audit 4 — SOB Ratio Invariance

For each of 15750 ordered pairs from the 126 SOB rows, verify
`G(P_i)·qA(P_j) − G(P_j)·qA(P_i) == 0` exactly:

```text
ordered pairs checked      = 15750
ratio invariance breaks    = 0
ratio invariance passes    = 15750
passes_audit               = True
```

## Audit 5 — Directional Rank Correlation

Spearman rank correlation between predicted `G(P)` and external `external_anchor_A` over the 81-row stable Z set `{1..83} \ {43, 61}`:

```text
stable set size           = 81
joined rows               = 81
Spearman rho              = 1.000000
directional verdict       = PASS_DIRECTIONAL
passes_directional        = True (rho >= 0.99)
```

## Wrong Controls

```text
WC1  G' = qA/7      matter_breaks=126  sob_breaks=126   broke_as_predicted=True
WC2  W' = 6qA/8     matter_breaks=126  sob_breaks=126   broke_as_predicted=True
WC3  shuffle qA     pairs=15750  breaks=15750 (1.0000) broke_as_predicted=True
WC4  shuffle G      shuffled_rho=-0.107520            broke_as_predicted=False
```

## Predictions vs. Observed

| ID | Predicted | Observed | Pass |
|---|---|---|---|
| P1 | 126 matter + 126 SOB rows | 126 + 126 | YES |
| P2 | Identity 1 holds for all 126+126 | matter 99/126; SOB 126/126 | NO |
| P3 | Identity 2 holds for all 126+126 | matter 82/126; SOB 126/126 | NO |
| P4 | Identity 3 holds for all 126+126 | matter 82/126; SOB 126/126 | NO |
| P5 | Ratio invariance passes all 31500 pairs | matter 6908/15750; SOB 15750/15750 | NO |
| P6 | Spearman rho ≥ 0.99 | rho = 1.000000 | YES |
| P7 | WC1 breaks on all nonzero | 126/126 (matter) + 126/126 (SOB) | YES |
| P8 | WC2 breaks on all nonzero | 126/126 (matter) + 126/126 (SOB) | YES |
| P9 | WC3 ratio breaks > 50% pairs | 15750/15750 (100%) | YES |
| P10 | WC4 shuffled rho falls below 0.10 | -0.107520 (|rho| = 0.107520) | NO |

## K-Gate Audit

| Gate | Status | Evidence |
|---|---|---|
| K1 external anchor | PASS | Directional rank vs external_anchor_A; no unit conversion |
| K2 falsification | PASS | Pre-stated falsifiers triggered: matter identity at 1e-9, ratio invariance at 1e-9, and WC4 rho threshold not met |
| K3 target hygiene | PASS | Identities, tolerance values (1e-9, 0), Spearman threshold (0.99 / 0.95), and WC4 rho threshold (0.10) locked in precommit before runner ran |
| K4 typed inputs | PASS | Two SHA-locked source CSVs; reveal CSV used only for directional rank |
| K5 reproduction on demand | PASS | Deterministic; seeded WC3=20260622, WC4=20260623 |

## Cryptographic Chain

```text
CR235_PRECOMMIT.md   = 0e91dd6759200d3cf2b8b361632631805a71cf5b311a6c465cc8a8457265538e
CR219 matter CSV     = 45a8e7d20117b5aad62933d3858faf892cd3a3620c2ea8671f05904b10f1142f
Test 5 SOB CSV       = 0cd620be2f7ed1cd9ca03d4fb7222061ba990d258a04a7c99bbc7ff020b94616
Test 5 reveal CSV    = fbfb17d82fbe7375690ae4b7c5ec0e473d0024284caf2dbd89d5404ded1b7b3a
CR230_result.md      = 3c1fd16c860a09a3b92fe61de008eb3b5f943e797a63327c47110af51b9829b7
CR229_result.md      = ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
CR222_result.md      = b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR114_result.md      = f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
```

## Sequence in the Seven-Test Arc

CR235 is **Test 6 of 7**. Test 7 (CR236@12a Paul Revere tomography) remains.

See `[[project-seven-test-ownership-arc-cr230-236]]`.

## Rule of Immutability

Sealed 2026-06-22 by Sean Brady. Precommit (sha `0e91dd67…`), runner, and per-row audit CSVs frozen. Verdict FAIL recorded as produced.

---

**Sealed by:** Sean Brady, 2026-06-22
**Runner verified:** matter 76/126 identity, 6908/15750 ratio pairs; SOB 126/126 identity, 15750/15750 ratio pairs; directional Spearman rho = 1.000000; WC1-WC3 broke, WC4 did not
**Arc position:** Test 6 of 7 — FAIL as precommitted
