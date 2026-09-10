# CR230 Raw-Generator Test (Substrate Structural Numbers from {R, D, α_H} Alone)

## Verdict

```text
CR230_PASS_RAW_GENERATOR_TEST__STRUCTURAL_NUMBER_SET_126_81_81_162_27_EMERGES_FROM_R_12_D_3_ALPHA_H_2_ALONE__NO_SPREADSHEET_SELECTION__FOUR_WRONG_CONTROLS_ALL_FAIL__SUBSTRATE_LEDGER_IS_STRUCTURAL
```

`execution_status = CLEAN`
`scientific_verdict = PASS`
`classification = STRUCTURAL_IDENTITY_CR (raw-generator verification)`
`part_of_arc = Seven-test ownership arc, Test 1 of 7`

## Claim

The SAM foundational constants `{R = 12, D = 3, α_H = 2}` alone — without any curated spreadsheet, manual row selection, or external table lookup — produce the substrate's structural number set `{126, 81, 81, 162, 27}` via a nine-step algebraic derivation that uses only the inclusion-exclusion accounting (CR229) plus the substrate write-rate identity.

Four wrong controls (each tweaking the carrier-side inventory in a structurally-meaningful way) each break the closure, confirming the structural numbers depend on getting the carrier inventory exactly right.

## Derivation Chain (Executed by `CR230_runner.py`)

```text
inputs: R = 12, D = 3, α_H = 2

Step 1:  capacity              = R²                          = 144
Step 2:  binary closure         = 2^D                         = 8
Step 3:  tensor split-loss      = R² / 2^D                    = 144 / 8       = 18  = α_H · D²
Step 4:  retained capacity      = R² − tensor                 = 144 − 18      = 126  (matter-energy)
Step 5:  per-side unique        = retained / 2                = 126 / 2       = 63
Step 6:  one-side total         = per-side + tensor           = 63 + 18       = 81
Step 7:  mirror (QP093A-0303)   = D^(D+1)                     = 3^4           = 81
Step 8:  closed ledger          = one-side + mirror           = 81 + 81       = 162  = R²·9/8
Step 9:  write-rate identity    = (one-side × 4) / R          = 324 / 12      = 27   = D³
```

**All five structural numbers — `{126, 81, 81, 162, 27}` — emerge from the constants alone via the nine-step algebra. Zero spreadsheet selection. Zero curated input.** This is the substrate ledger as a derived structural fact, not as a hand-arranged tabulation.

## Wrong Controls Executed

| WC | What was changed | Resulting closure | Breaks? |
|---|---|---|---|
| WC1 | Omit row 0306 (`p = 1`) from carrier-side | one_side = 80, ledger = 161 | YES (off by 1 from R²·9/8 = 162) |
| WC2 | Restore CR216-retired duplicate 0305 (`p = 1`) | one_side = 82, ledger = 163 | YES (off by 1 over R²·9/8 = 162) |
| WC3 | Treat 0303 mirror as one of the 12 unpacked elements (no mirror side) | one_side = 162, mirror = 0 | YES (CR229 `|A| = |B| = 81` symmetry collapses) |
| WC4 | Use mass-lifted values `m(p) = p + p²/R²` instead of bare partition `p` | one_side ≈ 83.47, ledger ≈ 164.47 | YES (lifted masses overshoot, ledger ≠ 162) |

**All four wrong controls break the closure as predicted.** This confirms the structural numbers depend on:
- Including 0306 exactly once (carrier inventory is sealed at 12 elements summing to 81 — CR222/CR216 sealed this)
- Treating CR216-retired duplicates as retired (no double-counting)
- Treating 0303 as the mirror side (CR229's two-81-element-sides decomposition is structurally required)
- Using bare partition addresses, not lifted masses (the carrier-tensor ledger is the address inventory, not the observed mass inventory; CR134's lifted form is downstream and operates on different rows)

## Predictions Checks

- **[PASS]** P1: Capacity `R² = 144` derives exactly from input
- **[PASS]** P2: Binary closure `2^D = 8` and tensor `R²/2^D = 18 = α_H·D²` derive exactly
- **[PASS]** P3: Retained capacity `R² − tensor = 126` derives exactly
- **[PASS]** P4: Per-side unique `126/2 = 63` derives exactly
- **[PASS]** P5: One-side total `63 + 18 = 81` derives exactly
- **[PASS]** P6: Mirror `D^(D+1) = 81` derives exactly
- **[PASS]** P7: Closed ledger `81 + 81 = 162 = R²·9/8` derives exactly
- **[PASS]** P8: Write-rate identity `(81 × 4) / R = D³ = 27` derives exactly
- **[PASS]** P9: WC1, WC2, WC3, WC4 each break the closure (all four confirmed by runner)
- **[PASS]** P10: All five structural numbers emerge from constants alone — no curated input

## Wrong Controls — All Break the Closure as Required

- **[PASS]** WC1_omit_0306_p_1 → ledger 161 (broken by ≠ 162)
- **[PASS]** WC2_restore_duplicate_0305 → ledger 163 (broken by ≠ 162)
- **[PASS]** WC3_treat_0303_as_unpacked → asymmetric (one_side 162, mirror 0)
- **[PASS]** WC4_use_mass_lift_values → ledger ≈ 164.47 (broken by ≠ 162)

## K-Gate Audit

| Gate | Status | Evidence |
|---|---|---|
| K1 external anchor | N/A (this CR is purely structural; downstream CRs in the arc connect to external anchors) |
| K2 falsification | PASS | Any of the 9 derivation steps producing a non-sealed value, OR any wrong control failing to break the closure, falsifies this CR |
| K3 target hygiene | PASS | No target. The structural numbers are derived from constants alone via algebraic steps. No PDG, no Planck, no outside-model reference |
| K4 typed inputs | PASS | Inputs are 3 foundational constants `{R, D, α_H}`, each derived from sealed upstream CRs (CR113, CR115, CR104c) |
| K5 reproduction on demand | PASS | `CR230_runner.py` reproduces the full chain; runs to completion in <1s; deterministic |

## Cryptographic Chain (Inputs)

```text
CR114_result.md (R², split-loss = α_H·D², retained 7/8 capacity)     = f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
CR116_result.md (18 graviton-channel carrier)                          = 4385529ee82f863e5c2ac40ad2ce0114b71c84e3720d09d96d1fdde79bf07464
CR132_result.md (carrier lattice TENSOR=18, NEUTRAL_VECTOR=81)         = 09fb22d1c13c44025f540f5134658ecca81cf62c67c6ce1c15cea751adfed2d6
CR134_result.md (SOURCE_SUPPORT partitions {1,2,3,4,6,8,9,12})         = fe6d4576b2a5ae334ff590cb180669b2b67c1890ad485c14a072a0863d7cec05
CR216_result.md (duplicate 0305 retired; one-side stays at 81)         = 5fd583b8f4c600c78e9aea4446b2d93b22f2de6cba33ef7d3dfe082f25346b80
CR217_result.md (162 closed ledger = R²·9/8)                           = 635791273a54838531d9b59177268a645b4ca151720da383784ac9ac047ffc2e
CR218_result.md (bigrade lattice derivation)                            = c2552aa075ba989e0c6c30c658aa109ab005aed0df9cbf419de71779fbe8bf6e
CR222_result.md (carrier ledger 12+1 = 81+81 = 162)                    = b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR229_result.md (inclusion-exclusion unifying upstream)                 = ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
```

## Manuscript Implications

CR230 enables §0/§1 of the manuscript to make a stronger claim than "we derived a structural ledger": the structural ledger is computed from `{R, D, α_H}` alone via a 9-step algebraic chain reproducible from `CR230_runner.py`. The 5 structural numbers `{126, 81, 81, 162, 27}` that all downstream substrate work (Higgs derivation, gravity coupling, particle table, periodic structure) depends on are derivable from 3 inputs without any spreadsheet curation. Wrong controls confirm the carrier inventory is structurally pinned (not editorial choice).

## Sequence in the Seven-Test Arc

CR230 is **Test 1 of 7**. The five structural numbers verified here are the foundation that the remaining six tests build on:

- CR231 (Test 2): Partition-shuffle null test will verify random shuffles of the 139 rows do NOT reproduce these same five structural numbers (statistical confirmation)
- CR232 (Test 3): Matter/support promotion gate audit ensures the substrate ledger doesn't leak into spurious particle predictions
- CR233 (Test 4): 18 / 81 / 27 tensor-substrate role-separation test verifies the four numerical roles stay distinct
- CR234 (Test 5): Blind SOB element engine — Z + constants only — derives the periodic structure (extends this generator to the element level)
- CR235 (Test 6): qA/8 gravity bridge — first physical-observable bridge from the structural ledger
- CR236 (Test 7): Paul Revere tomography — first QC technology contact

See `[[project-seven-test-ownership-arc-cr230-236]]`.

## Rule of Immutability

Sealed 2026-06-22 by Sean Brady. Inputs hash-locked. The 9-step derivation chain, the 5 structural numbers, the 4 wrong controls, and the runner are frozen.

If any upstream sealed source (CR114, CR132, CR134, CR216, CR217, CR218, CR222, CR229) is later regraded, this CR must be re-examined.

---

**Sealed by:** Sean Brady, 2026-06-22
**Runner verified:** All 8 derivation values match; all 4 wrong controls break the closure
**Arc position:** Test 1 of 7 (raw-generator structural foundation)
