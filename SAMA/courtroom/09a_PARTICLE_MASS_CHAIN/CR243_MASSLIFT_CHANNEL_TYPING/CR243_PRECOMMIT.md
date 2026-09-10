# CR243 Mass-Lift Channel Typing — Precommit

## Question

Is the substrate mass-lift fraction `Y = X/K` (per-row surface debit normalized
to native source) a **typed channel table** — a small set of CR238-substrate
expressions, one per channel class — rather than a single global formula
`Y = f(q)` with unstructured residual?

## Honest framing of K3 (target hygiene)

The five typed forms listed below were inferred by inspection of the source
table (`126part_with_carriers.xlsx`) before this precommit was sealed. This
precommit does **not** claim those forms were derived blindly. It tests:

1. Whether the forms match the clean classes exactly (within spreadsheet
   2-decimal storage precision of column `X`).
2. Whether substrate-constant perturbations `{R, D, S}` away from `{12, 3, 8}`
   each break the predicted values on the clean classes.
3. Whether a class-label shuffle degrades the per-class match rate (reported
   as informational, not verdict-blocking).
4. Whether the residual `Δ_unequal = Y_observed − Y_base` on the unequal-pair
   rows quantizes to the typed unit family
   `{1/R², 1/RS, 1/DS², 1/R, 1/M, 1/L}`. This piece is K3-clean — the unequal-
   pair residuals were not used to derive any of the precommitted forms.

## Locked substrate atoms (read-only from CR238)

```text
R = 12        D = 3        S = 8        alpha_H = 2
M = 126       L = 162      Theta = 18   V = 27
kappa = 7117/768            g = 1/64
```

## Locked typed forms

```text
Y_color_triad        = sign(q) * (|q| + D) / R
Y_equal_bound_pair   = (D + 2) / (R * (D + 1))                  = 5/48
Y_OCTET              = (D^2 + S) / (D * S^2)                    = 17/192
Y_zero_contact       = 0
Y_no_surface_depth   = 1
```

Channel-to-form binding:

| route_combination prefix          | surface_sign      | form                |
|-----------------------------------|-------------------|---------------------|
| `color_triad[...]`                | positive_debit / negative_credit | `Y_color_triad`      |
| `pair_write[a\|antib]`, a==b<9    | positive_debit    | `Y_equal_bound_pair` |
| `pair_write[9\|anti9]`            | positive_debit    | `Y_OCTET`            |
| `pair_write[a\|antib]`, a!=b      | pos / neg         | unequal-pair lane    |
| `plus_/minus_/neutral_single_write`| zero_contact     | `Y_zero_contact`     |
| `hidden_source_support[...]`, `carrier...` | no_surface_depth | `Y_no_surface_depth` |

## Unequal-pair residual structure

For each unequal pair row `(a != b)`, define:

```text
Y_base_unequal = 0                  (no precommitted base form)
Δ_unequal      = Y_observed - 0     = Y_observed
```

The K3-clean test is: do the 42 unequal-pair `Δ` values quantize to integer
multiples of any typed unit in the family `{1/R^2, 1/(R*S), 1/(D*S^2), 1/R,
1/M, 1/L}` within tolerance `1e-5`?

This precommit does NOT lock a typed form for unequal pairs. The result will
either find quantization (BOUNDARY-or-better) or not (no penalty beyond
reporting).

## Tolerance discipline

Column `X` in the source workbook is stored at 2-decimal precision. The
analytic value of `X` for a row is `K_native × Y_typed_form`, and the
spreadsheet stores `round(K_native × Y_typed_form, 2)`.

For each row, the comparison is:

```text
X_typed_predicted = K_native * Y_typed_form              (exact, Fraction)
Y_observed        = X_stored / K_native                  (limited by X precision)
match if |Y_observed - Y_typed_form| <= ceil_tol
where ceil_tol = max(1e-5, 0.005 / K_native)             (half-LSB of X column)
```

This tolerance band is the 2-decimal storage half-LSB of `X` scaled into `Y`.
Rows where `K_native` is small (single_write `K=1`, support `K~1-20`) get a
proportionally larger `Y` tolerance.

## Wrong controls

All wrong controls re-evaluate the typed forms with one substrate atom
perturbed; pass condition is **degrade**, not improvement. Each WC computes
the per-row match rate under perturbation and reports the count of clean-class
rows that still match the typed form.

```text
WC-R1   R = 10                              (D=3, S=8 fixed)
WC-R2   R = 11                              (D=3, S=8 fixed)
WC-R3   R = 13                              (D=3, S=8 fixed)
WC-D1   D = 2                               (R=12, S=8 fixed)
WC-D2   D = 4                               (R=12, S=8 fixed)
WC-S1   S = 7                               (R=12, D=3 fixed)
WC-S2   S = 9                               (R=12, D=3 fixed)
WC-O1   OCTET D=2,S=8        ((4+8)/(2*64) = 3/32 = 0.09375)
WC-O2   OCTET D=4,S=8        ((16+8)/(4*64) = 3/32 = 0.09375)
WC-O3   OCTET D=3,S=7        ((9+7)/(3*49) = 16/147 ~ 0.10884)
WC-O4   OCTET D=3,S=9        ((9+9)/(3*81) = 2/27 ~ 0.07407)
WC-O5   OCTET numerator substitution: |q|+S in place of D^2+S
        (arithmetic agrees on canonical OCTET row since |q|=9=D^2;
         flagged as weaker typing audit, not arithmetic break)
WC-CS   Class label shuffle (seed = 20260623)             [INFORMATIONAL]
```

WC-CS is informational only per discussion — it reports the per-class match
rate after shuffling class labels, but its result does not block the verdict.

## Verdict gates

```text
STRONG_PASS conditions (all required):
  S1  Color triad:      14/14 match within ceil_tol
  S2  Equal bound pair: all (a=b<9) rows match Y=5/48 within ceil_tol
  S3  OCTET:            pair_write[9|anti9] matches Y=17/192 within ceil_tol
  S4  Single write:     all zero_contact rows match Y=0 exactly
  S5  No-surface-depth: all support/carrier rows match Y=1 within ceil_tol
  S6  WC-R1..R3:        each degrades color triad match count
  S7  WC-D1..D2:        each degrades color triad match count
  S8  WC-S1..S2:        each degrades OCTET match
  S9  WC-O1..O4:        each breaks OCTET against canonical 17/192
  S10 No clean-class match falls below precommit count under any constant WC

BOUNDARY conditions:
  B1  All S1..S5 satisfied
  B2  Some constant-WC subset does not degrade (e.g. symmetric WC-D1/WC-D2
      pair giving same value 3/32 — recorded as a symmetry, not a degrade)
  B3  Unequal-pair residual quantization to typed unit family inconclusive

FAIL conditions (any one is sufficient):
  F1  Any clean-class typed form fails on at least one row outside ceil_tol
  F2  Any constant WC (R, D, S) does NOT degrade the clean-class match count
      (excluding the WC-D1/WC-D2 symmetry which is documented in advance)
  F3  Class shuffle (WC-CS) preserves per-class match rate >= 90% of canonical
      (reported but informational only; does not by itself trigger FAIL)
```

Verdict precedence: `STRONG_PASS > BOUNDARY > FAIL`. F3 is reported but does
not trigger FAIL by itself (per session agreement to keep the shuffle fair
rather than verdict-blocking).

## Unequal-pair residual readout (no verdict claim)

The 42 unequal-pair rows are reported as a separate readout block:

```text
For each unequal-pair row:
  - Δ = Y_observed (since Y_base_unequal = 0)
  - quantization_unit  = best-fit typed unit from family {1/R^2, 1/(R*S),
    1/(D*S^2), 1/R, 1/M, 1/L} that gives integer-multiple match within 1e-5
  - quantization_multiplier_n = round(Δ / quantization_unit)
  - quantization_residual = Δ - n * quantization_unit
  - quantized_match = (|quantization_residual| < 1e-5)
```

Counts of rows with `quantized_match = True` are reported. The 2-decimal
precision of `X` in the source workbook is a known precision limit; the
quantization readout is not a verdict criterion.

## Outputs (locked file shape)

```text
CR243_summary.json              — full readout, verdict, WC degradation table
CR243_clean_class_predictions.csv — per-row prediction & match for clean classes
CR243_unequal_pair_residuals.csv  — per-row Δ + best-fit quantization
CR243_wrong_controls.csv         — per-WC match counts and degradation
CR243_input_manifest.csv         — input SHA + row count + class inventory
HASHES.txt                       — all input and output file SHA-256
```

## Cryptographic chain (inputs)

```text
CR238_result.md (substrate spine compaction; F=81, S=8 + alpha_H + mu_Q + D=3 forced)
  = 7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef
CR222_result.md (carrier ledger)
  = b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR229_result.md (inclusion-exclusion identity 144 = 126 + 18)
  = ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
CR238_PRECOMMIT.md (substrate spine compaction)
  = 5e916199fb185db80a2b2346d3e0a9c59f9418c5e8d96b7453ffc716e8c46293
CR243_input_snapshot.xlsx (frozen snapshot of C:\VS\126part_with_carriers.xlsx)
  = 7f5d9cc4c20f4bb62c3e40a4825c793ccc020fed72abb44ec17fe30406d8e4e5
```

## Falsifiers

```text
F1   Any of S1-S5 fails: the typed form claim is wrong for that channel.
F2   Any of S6-S9 fails: the substrate constant the WC perturbed is not
     actually doing the structural work the typed form ascribed to it.
F3*  Class-shuffle WC-CS preserves match rate: the channel-typing claim is
     weak (informational only; does not trigger FAIL by itself).
F4   The OCTET row matches Y=5/48 within ceil_tol AND fails Y=17/192:
     OCTET is not a distinct channel from equal-bound-pair.
F5   The single-write or no-surface-depth class produces nonzero typed-form
     values inconsistent with Y=0 / Y=1: the surface_sign categorization is
     not the right binding to these channels.
```

## Sealed

Sean Brady, 2026-06-23. Substrate atoms, typed forms, WCs, tolerance
discipline, verdict gates, falsifiers all locked above the line.
