# CR244 Unequal-Pair Typed Forms — Result

## Verdict

```text
CR244_STRONG_PASS_UNEQUAL_PAIR_TYPED_FORMS_CLOSED__
ORDINARY_30_OF_30_AND_OCTET_12_OF_12_EXACT_AT_2DEC_X_STORAGE__
R4_DENOMINATOR_LOCKED__D2_OVER_R_OCTET_CORRECTION_LOCKED__
ALL_WRONG_CONTROLS_DEGRADE_AS_PREDICTED
```

`execution_status   = CLEAN`
`scientific_verdict = STRONG_PASS`
`classification     = UNEQUAL_PAIR_LANE_TYPING (downstream of CR238 / CR243)`
`precommit_sha      = 1c1bd7c69ce8edf88cd8c1c164f822eefeee431adf0532ae8b141b610f9b6182`

## Plain-English Summary

CR243 confirmed five clean-class typed forms but reported `0/42` on
unequal-pair quantization against the precommit unit family
`{1/R², 1/(R·S), 1/(D·S²), 1/R, 1/M, 1/L}`. CR243 explicitly noted that
the X-column 2-decimal storage masks structure smaller than ~5e-3, and that
the unit family did not include `1/R⁴`.

CR244 locks two unequal-pair lane forms — both proposed by Sean after the
CR243 BOUNDARY readout — and tests them on all 42 unequal-pair rows under
the same 2-decimal storage tolerance discipline plus nine wrong controls.

```text
ORDINARY (neither a nor b = 9):
    Y = sign(a - b) · (|a - b| + D)     / R⁴       30/30 EXACT

OCTET-involved (a = 9 or b = 9):
    Y = sign(a - b) · (|a - b| + D²/R) / R⁴       12/12 EXACT
```

Match on the X-round criterion: `round(K_native · Y_typed_form, 2) == X_stored`
for every row. The lane forms close the unequal-pair channel of the substrate
mass-lift table with **zero new primitives** — all atoms `{R, D}` are read
from CR238, and the trigger condition (one of `{a, b} = 9`) is the same
OCTET-charge identifier already established by the equal-pair OCTET row at
`(D² + S) / (D · S²)`.

All nine wrong controls degrade at least one lane, with the magnitude
WC-A1 (`R³` denominator) breaking both lanes completely (0/0 match): the
denominator is structurally `R⁴`, not `R³`.

## What This Closes

Combined with CR243's five clean-class typed forms, **the full mass-lift
fraction `Y(P) = X(P) / K_native(P)` is now closed in CR238 substrate atoms
for every row of the 138-row substrate ledger** (the photon at row 30 has
`K_native = 0` and is correctly off-table by construction).

```text
class                    surface_depth  Y(row)
─────────────────────────────────────────────────────────────────────────
color_triad              depth=0        sign(q) · (|q| + D) / R
equal_bound_pair         depth=1        (D + 2) / (R · (D + 1))           = 5/48
OCTET_pair (equal)       depth=1        (D² + S) / (D · S²)               = 17/192
single_write             route_contact  0
support / carrier        no_surface_depth   1
unequal_pair ordinary    depth=3        sign(a-b) · (|a-b| + D) / R⁴
unequal_pair OCTET       depth=3        sign(a-b) · (|a-b| + D²/R) / R⁴
```

The typed channel table is now structurally complete on this dataset.

## Inputs (Hash-Locked)

```text
Precommit SHA-256       : 1c1bd7c69ce8edf88cd8c1c164f822eefeee431adf0532ae8b141b610f9b6182
Input snapshot SHA-256  : 7f5d9cc4c20f4bb62c3e40a4825c793ccc020fed72abb44ec17fe30406d8e4e5
Input snapshot          : CR244_input_snapshot.xlsx (copy of the CR243 snapshot,
                          itself a frozen copy of C:\VS\126part_with_carriers.xlsx)

Substrate atoms (read-only from CR238):
  R = 12   D = 3   S = 8   alpha_H = 2   M = 126
  R^4 = 20736
```

## Row Inventory (Unequal Pairs Only)

```text
ORDINARY (neither a nor b = 9)   :  30
OCTET-involved (a = 9 or b = 9)  :  12
TOTAL unequal-pair rows           :  42
```

The 12 OCTET-involved rows are 6 negative_credit `pair_write[a|anti9]` rows
(a ∈ {1, 2, 3, 4, 6, 8}) and 6 positive_debit `pair_write[9|antib]` rows
(b ∈ {1, 2, 3, 4, 6, 8}). The 30 ordinary rows are all remaining `a != b`
combinations.

## Block A — Canonical Match

| Lane | Rows | X-round Match | Y-tolerance Match |
|---|---:|---:|---:|
| ORDINARY      | 30 | **30 / 30** | 30 / 30 |
| OCTET-involved | 12 | **12 / 12** | 12 / 12 |
| **TOTAL**     | 42 | **42 / 42** | 42 / 42 |

Every row's typed-form `Y` produces an `X = K_native · Y` that rounds (at
2-decimal precision) to exactly the stored `X` value in the source workbook.
Per-row detail in `CR244_unequal_pair_predictions.csv`.

Representative rows:

| Row | Route                    | a | b | \|a-b\| | K     | X stored | X typed-form | Match |
|----:|--------------------------|--:|--:|------:|------:|---------:|-------------:|:---:|
|   9 | `pair_write[6\|anti8]`   | 6 | 8 |     2 |   582 |   -0.14  |  -0.140336   | ✓ |
|  10 | `pair_write[4\|anti8]`   | 4 | 8 |     4 |   396 |   -0.13  |  -0.133681   | ✓ |
|  11 | `pair_write[3\|anti8]`   | 3 | 8 |     5 |   303 |   -0.12  |  -0.116898   | ✓ |
|  12 | `pair_write[4\|anti9]`   | 4 | 9 |     5 |   447 |   -0.12  |  -0.123951   | ✓ |
|  19 | `pair_write[8\|anti9]`   | 8 | 9 |     1 |   867 |   -0.07  |  -0.073170   | ✓ |
| 106 | `pair_write[9\|anti8]`   | 9 | 8 |     1 |   867 |   +0.07  |  +0.073170   | ✓ |

## Block B — Wrong Controls

| WC    | Description                                       | ORDINARY (canon→pert) | OCTET (canon→pert) |
|-------|---------------------------------------------------|----------------------:|-------------------:|
| WC-R1 | R = 10, D = 3                                     | 30 → **2**            | 12 → **0**          |
| WC-R2 | R = 11, D = 3                                     | 30 → **6**            | 12 → **0**          |
| WC-R3 | R = 13, D = 3                                     | 30 → **6**            | 12 → **0**          |
| WC-D1 | R = 12, D = 2                                     | 30 → **10**           | 12 → **0**          |
| WC-D2 | R = 12, D = 4                                     | 30 → **8**            | 12 → **2**          |
| WC-T1 | Trigger swap (ORDINARY ↔ OCTET)                   | 30 → **4**            | 12 → **0**          |
| WC-A1 | Alternate denominator R³ = 1728                   | 30 → **0**            | 12 → **0**          |
| WC-A2 | Alternate denominator R²·M = 18144                | 30 → **12**           | 12 → **2**          |
| WC-A3 | ORDINARY numerator `(\|a-b\| + D²)` instead of `+D`  | 30 → **2**            | 12 → **12** (unaffected) |

Each WC degrades at least one lane; the R-perturbations and the trigger swap
degrade both lanes; the alternate-denominator `R³` (WC-A1) breaks all 42
rows to zero matches (off by a factor of 12); WC-A3 leaves the OCTET lane
unaffected because the perturbation is locked to ORDINARY only — that's
correct behaviour, not a falsifier.

WC counts in `CR244_wrong_controls.csv`.

## Block C — K-Gate Audit

| Gate | Status | Evidence |
|---|---|---|
| K1 | PARTIAL | Internal substrate-typing audit. The structure-of-substrate could have come out otherwise (e.g., `R³` denominator, no OCTET-correction term). WC-A1 specifically discriminates `R⁴` vs `R³`; WC-T1 discriminates whether the OCTET-trigger is real. Both pass. |
| K2 | PASS | Pre-stated falsifiers F1-F5 — none fired. WC-A1 specifically falsified an alternate denominator that the precommit said would break both lanes; it did. |
| K3 | PARTIAL — DECLARED | Lane forms proposed by inspection of the 42 rows after CR243 BOUNDARY readout. Precommit explicitly declares this. Tested under nine wrong controls including trigger swap and alternate denominators. |
| K4 | PASS | Two CR238 atoms `{R, D}` only — no free parameter entered the runner. SHA-locked input and precommit verified at runner entry. |
| K5 | PASS | `python CR244_runner.py` deterministically reproduces all per-row predictions, all WC results, and the verdict. |

## Block D — Strong-Pass Conditions

| Condition | Status | Detail |
|---|:---:|---|
| S1 ORDINARY 30/30 X-round match | PASS | 30/30 |
| S2 OCTET 12/12 X-round match    | PASS | 12/12 |
| S3 WC-R1..R3 degrade both lanes | PASS | both lanes degrade for all three R values |
| S4 WC-D1..D2 degrade at least one lane | PASS | both D-WCs degrade both lanes |
| S5 WC-T1 trigger swap degrades both lanes | PASS | ORD 30→4, OCT 12→0 |
| S6 WC-A1..A3 degrade at least one lane | PASS | all three alternate-form WCs degrade |

## Cryptographic Chain (Inputs)

```text
CR114_result.md (capacity R² + split-loss)             = f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
CR217_result.md (162 = R²·9/8 closed ledger)           = 635791273a54838531d9b59177268a645b4ca151720da383784ac9ac047ffc2e
CR222_result.md (carrier ledger 12+1 closed sum)       = b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR229_result.md (inclusion-exclusion identity)         = ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
CR238_result.md (substrate spine compaction)           = 7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef
CR243_PRECOMMIT.md (clean-class channel typing)        = 4ea9789806a8bd17e0c314cb6508ee9ab80c0212b49e68b0cdf94fd052d97dc2
CR243_result.md (clean-class STRONG_PASS, unequal-pair BOUNDARY)
                                                       = 4884fe84f5d89ff363317b52608d3cc6913299e626e4131adfedaa0723d24bf1
CR244_PRECOMMIT.md                                     = 1c1bd7c69ce8edf88cd8c1c164f822eefeee431adf0532ae8b141b610f9b6182
CR244_input_snapshot.xlsx                              = 7f5d9cc4c20f4bb62c3e40a4825c793ccc020fed72abb44ec17fe30406d8e4e5
```

## What CR244 Does

1. Locks two typed forms for the unequal-pair lane of the substrate mass-lift
   table:
   - ORDINARY: `Y = sign(a-b) · (|a-b| + D) / R⁴`
   - OCTET-involved: `Y = sign(a-b) · (|a-b| + D²/R) / R⁴`
2. Tests all 42 unequal-pair rows under the same 2-decimal X-column storage
   tolerance discipline as CR243.
3. Achieves 30/30 ORDINARY + 12/12 OCTET = 42/42 exact X-round match.
4. Runs nine wrong controls (three R-perturbations, two D-perturbations, one
   trigger swap, three alternate-form perturbations) and confirms each
   degrades at least one lane.
5. Locks the trigger rule (`a == 9 or b == 9`) by demonstrating that swapping
   it breaks ORDINARY from 30 → 4 and OCTET from 12 → 0.
6. Locks the `R⁴` denominator by demonstrating that the alternate `R³`
   denominator breaks both lanes to zero matches.

## What CR244 Does NOT Do

- Does NOT modify CR243. CR243 BOUNDARY on unequal-pair quantization
  remains as audit trail — the original precommit unit family did not include
  `1/R⁴`, and that is the honest record of why the quantization scan returned
  zero matches. CR244 supplies the missing form; CR243 is preserved.
- Does NOT modify any upstream sealed CR. CR114, CR217, CR222, CR229, CR238
  remain frozen.
- Does NOT claim the lane forms were derived blindly. K3 is declared
  PARTIAL — Sean proposed both forms after inspection. The pass condition
  is survival under nine wrong controls, not blind discovery.
- Does NOT close the binding-curvature derivation. With the mass-lift
  formula now complete in CR238 atoms, the binding-from-closure-geometry
  derivation that follows is a separate CR.

## Manuscript Implications

CR243 + CR244 jointly close the substrate mass-lift fraction in CR238 atoms
for every row of the substrate ledger:

```text
Y(P) = X_debit(P) / K_native(P)
     = F_channel(R, D, S; row data)

where F_channel is one of seven typed expressions, selected by the row's
{route_combination, surface_sign, OCTET-charge involvement} triple.
```

This is the **typed channel table** reading of the substrate that masslift.pdf
proposed and that CR243 began to test. With CR244 the unequal-pair lane is
now part of the closed table rather than the open residual it was at CR243
seal.

The next CR can build the binding surface `B_u = A · u - m_measured` from
the now-typed mass-lift, returning to the question that CR242 left at
BOUNDARY ("BW shape reproducible from SAM-typed basis but was not derived
from it at zero free parameters") with a fully typed substrate underneath it.

## Rule of Immutability

Sealed 2026-06-23 by Sean Brady. Inputs, precommit, runner, two lane forms,
OCTET-trigger rule, tolerance discipline, wrong controls, verdict gates,
falsifiers all frozen.

If any sealed upstream CR (CR114, CR217, CR222, CR229, CR238) is later
regraded such that its frozen numerical value or structural identity
changes, CR244 must be re-examined and the lane forms re-verified.

If a higher-precision (>2 decimal) regeneration of the X column becomes
available, CR244 should re-run with the tighter tolerance to confirm both
lanes still close exactly. The forms are predicted to remain exact since
the typed expressions evaluate to exact `Fraction` values.

---

**Sealed by:** Sean Brady, 2026-06-23
**Runner verified:** ORDINARY 30/30 X-round match; OCTET 12/12 X-round match;
WC-R1..R3 + WC-T1 each degrade both lanes; WC-D1..D2 each degrade at least
one lane; WC-A1 (R³ denominator) breaks all 42 rows; WC-A2 (R²·M)
degrades; WC-A3 (numerator D² in place of D) breaks ORDINARY without
affecting OCTET (correct behaviour, scope is locked to ORDINARY).
**Verdict driver:** all six strong-pass conditions satisfied; the lane
forms close the unequal-pair channel of the substrate mass-lift table.
**Open follow-up:** binding-curvature derivation from the now-closed
typed channel table (CR245 candidate; returns to CR242 BOUNDARY with a
fully typed substrate).
