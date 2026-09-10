# CR230 Raw-Generator Test — Precommit

**Date:** 2026-06-22
**Classification:** STRUCTURAL_IDENTITY_CR (raw-generator verification)
**Permission status:** GRANTED_BY_USER: Sean Brady, 2026-06-22 ("yes — I'll begin Test 1")
**Source:** `C:\Users\drwho\OneDrive\Desktop\Tests.docx` Test 1 ("Raw-generator test")
**Part of:** Seven-test ownership arc (CR230-CR236); see `[[project-seven-test-ownership-arc-cr230-236]]`

## Scope

Show that `{R = 12, D = 3, α_H = 2}` — the SAM foundational constants — regenerate the substrate's structural number set `{126, 81, 81, 162, 27}` step-by-step via the inclusion-exclusion identity (CR229@09a) plus the substrate write-rate identity (Sean's 6-phase observation). The test is structural-algebraic verification: no spreadsheet selection, no manual curation, no row lookup. Just the constants and the framework's accounting rules.

## What CR230 Tests

The raw generator takes `{R, D, α_H}` as input and produces:

```text
Step 1: capacity            =  R²                       = 144
Step 2: binary closure      =  2^D                       = 8
Step 3: tensor split-loss   =  R² / 2^D                  = 144 / 8         = 18  = α_H · D²
Step 4: retained capacity   =  R² − tensor                = 144 − 18        = 126 = matter-energy
Step 5: per-side unique     =  retained / 2               = 126 / 2         = 63
Step 6: one-side total      =  per-side + tensor          = 63 + 18         = 81
Step 7: mirror (0303)       =  D^(D+1)                    = 3^4              = 81
Step 8: closed ledger       =  one-side + mirror          = 81 + 81         = 162  = R² · 9/8
Step 9: write-rate identity =  (one-side × 4) / R         = 324 / 12        = 27   = D³
```

All five structural numbers (`126, 81, 81, 162, 27`) emerge from the constants alone via these nine algebraic steps. No row selection. No curated table.

## Pass Condition

```text
PASS  if and only if all five of {126, 81, 81, 162, 27} are produced
       by the algebraic steps above from inputs {R = 12, D = 3, α_H = 2}
       AND all four wrong controls below fail (i.e., they break the closure).
```

## Wrong Controls (each must fail — verified by inspection)

**WC1 — omit row 0306 (`p = 1`) ⇒ side sum = 80, ledger = 161 (off by 1):**
If 0306 (one of the bigrade lattice elements at `p = 1`) is omitted from the carrier-side count, the unpacked carrier sum becomes `81 − 1 = 80`, the closed ledger becomes `80 + 81 = 161 ≠ 162 = R²·9/8`. The CR217/CR222 sealed closed-ledger identity fails. Confirms the 0306 row is structurally required.

**WC2 — restore duplicate 0305 (`p = 1`) ⇒ side sum = 82, ledger = 163:**
If the CR216-retired duplicate 0305 row is restored to the carrier-side count, the unpacked carrier sum becomes `81 + 1 = 82`, the closed ledger becomes `82 + 81 = 163 ≠ 162`. Confirms the CR216 retirement was structurally required (validates the dedup discipline).

**WC3 — count 0303 mirror as an unpacked mode (rather than its own mirror side) ⇒ ledger structure breaks:**
If QP093A-0303 = 81 is treated as one of the 12 unpacked carrier elements rather than as the mirror side, the carrier side sum becomes `81 + 81 = 162`, the mirror side is empty (0), and the closed ledger reading `81 + 81 = 162` no longer reflects the inclusion-exclusion decomposition. CR229's `|A| = |B| = 81` symmetry fails. The substrate-as-two-sided-ledger interpretation collapses. Confirms 0303 is structurally distinct from the bigrade lattice elements.

**WC4 — use mass-lift values (`m(p) = p + p²/R²`) instead of bare partition values `p`:**
If the carrier-side sum is computed using lifted masses (the `p + p²/R²` form from CR134's SOURCE_SUPPORT_PACKET law) rather than bare partition values, the side sum becomes `≠ 81` (mass-lifted values are each slightly above their bare counterparts). The closed ledger `162 = R²·9/8` identity breaks. Confirms the structural ledger uses bare partition addresses, not lifted masses.

## Precommitted Verdict (target)

```text
CR230_PASS_RAW_GENERATOR_TEST__STRUCTURAL_NUMBER_SET_126_81_81_162_27_EMERGES_FROM_R_12_D_3_ALPHA_H_2_ALONE__NO_SPREADSHEET_SELECTION__FOUR_WRONG_CONTROLS_ALL_FAIL__SUBSTRATE_LEDGER_IS_STRUCTURAL
```

## Precommitted Predictions (P1–P10)

- P1: From `{R = 12, D = 3, α_H = 2}`, capacity `R² = 144` derives exactly
- P2: Binary closure `2^D = 8`, tensor split-loss `R²/2^D = 18 = α_H · D²` derives exactly
- P3: Retained capacity `R² − tensor = 126` derives exactly
- P4: Per-side unique `126 / 2 = 63` derives exactly
- P5: One-side total `63 + 18 = 81` derives exactly
- P6: Mirror `D^(D+1) = 81` derives exactly
- P7: Closed ledger `81 + 81 = 162 = R²·9/8` derives exactly
- P8: Write-rate identity `(one-side × 4) / R = D³ = 27` derives exactly
- P9: WC1, WC2, WC3, WC4 each break the closure (each must fail)
- P10: All five structural numbers emerge from constants alone — no curated input

## Upstream Sources (Hash-Locked, Read-Only)

```text
CR114_result.md (R², split-loss = α_H·D², retained 7/8 capacity)   = f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
CR116_result.md (18 graviton-channel carrier)                       = 4385529ee82f863e5c2ac40ad2ce0114b71c84e3720d09d96d1fdde79bf07464
CR132_result.md (carrier lattice positions including TENSOR=18)     = 09fb22d1c13c44025f540f5134658ecca81cf62c67c6ce1c15cea751adfed2d6
CR134_result.md (SOURCE_SUPPORT_PACKET partitions {1,2,3,4,6,8,9,12}) = 46c77cd912b932125228c8923e4705c4d36d0c1e2df14294f44d086d37856aff
CR216_result.md (carrier duplicate retirement, 0305 retired)         = 5fd583b8f4c600c78e9aea4446b2d93b22f2de6cba33ef7d3dfe082f25346b80
CR217_result.md (162 closed ledger = R²·9/8)                         = 635791273a54838531d9b59177268a645b4ca151720da383784ac9ac047ffc2e
CR218_result.md (bigrade lattice derivation)                         = c2552aa075ba989e0c6c30c658aa109ab005aed0df9cbf419de71779fbe8bf6e
CR222_result.md (carrier ledger 12 + 1 = 81 + 81 = 162)              = b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR229_result.md (inclusion-exclusion identity unifying upstream)     = ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
```

## Falsifier

If any of the nine algebraic steps fails to produce its sealed value from the inputs `{R = 12, D = 3, α_H = 2}`, OR if any of the four wrong controls is found NOT to break the closure, this CR's verdict falsifies.

## Reversibility Clause

If upstream CR114, CR132, CR134, CR216, CR217, CR218, CR222, or CR229 are later regraded, this CR must be re-examined. The arithmetic is unconditional; the structural-meaning interpretation depends on those upstream sealings.

## What This CR Does NOT Do

- Does NOT execute a full particle-table generator (CR119 / CR227 already do that).
- Does NOT verify the 320-particle table row-by-row (that's separate, sealed in CR119 + CR214-CR228).
- Does NOT compare to PDG, Planck, or any outside-model target.
- Does NOT extend the structural-number set beyond {126, 81, 81, 162, 27}.
- Does NOT depend on the actual physical Higgs mass; this test is purely structural-algebraic.

## Sequence in the Seven-Test Arc

CR230 (this CR) is Test 1 of 7. Once sealed, the arc continues:

- **CR231@09a (Test 2):** Partition-shuffle null test (Monte Carlo against random shuffles)
- **CR232@09a (Test 3):** Matter/support promotion gate audit
- **CR233@09a (Test 4):** 18 / 81 / 27 tensor-substrate role-separation test
- **CR234@09a or @10 (Test 5):** Blind SOB element engine (Z-only input)
- **CR235 (Test 6):** qA/8 gravity bridge
- **CR236@12a (Test 7):** Paul Revere tomography (real density-matrix)

See `[[project-seven-test-ownership-arc-cr230-236]]` for full arc.
