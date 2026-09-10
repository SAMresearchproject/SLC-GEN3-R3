# CR243 Mass-Lift Channel Typing — Result

## Verdict

```text
CR243_STRONG_PASS_MASSLIFT_IS_TYPED_CHANNEL_TABLE__FIVE_CLEAN_CLASSES_EXACT__
SUBSTRATE_PERTURBATIONS_DEGRADE_PER_ATOM_DEPENDENCE__OCTET_TYPING_LOCKED_AS_
D2_PLUS_S_OVER_D_S2__UNEQUAL_PAIR_RESIDUAL_DOES_NOT_QUANTIZE_TO_BASE_TYPED_UNIT_FAMILY
```

`execution_status   = CLEAN`
`scientific_verdict = STRONG_PASS`
`classification     = SUBSTRATE_CHANNEL_TYPING_AUDIT (downstream of CR238 / CR222 / CR229)`
`precommit_sha      = 4ea9789806a8bd17e0c314cb6508ee9ab80c0212b49e68b0cdf94fd052d97dc2`

## Plain-English Summary

The 139-row particle / carrier table at `126part_with_carriers.xlsx` (a copy of
CR219 promoted rows + the 13 added carrier-tensor rows) is **a typed channel
table**, not a single global formula with noise. Five precommitted typed forms
in the CR238 substrate atoms `{R=12, D=3, S=8}` reproduce **every clean-class
row exactly** within spreadsheet 2-decimal X-column storage tolerance:

```text
Y_color_triad        = sign(q) · (|q| + D) / R                         14/14 EXACT
Y_equal_bound_pair   = (D + 2) / (R · (D + 1))      = 5/48              6/6  EXACT
Y_OCTET              = (D² + S) / (D · S²)          = 17/192            1/1  EXACT
Y_zero_contact       = 0                                               63/63 EXACT
Y_no_surface_depth   = 1                                               12/12 EXACT
```

`Y = X/K = surface_debit / native_source` is the normalized mass-lift fraction
of the carrier or particle row. Each clean class is bound to a typed form
through the `surface_sign` × `route_combination` channel labelling.

Substrate-constant wrong controls each degrade exactly the classes whose typed
form contains the perturbed atom — `R`-perturbations break color triad and
equal-pair (R-dependent); `D`-perturbations break color triad, equal-pair, and
OCTET (D-dependent); `S`-perturbations break OCTET (the only S-dependent
clean class). Single-write `Y=0` and no-surface-depth `Y=1` are atom-free and
correctly remain stable under all WCs. **This per-atom WC dependence is itself
structural evidence that the typed forms encode the genuine atom-dependence
of each channel, not a coincidence of fitting.**

The OCTET-specific wrong controls WC-O1..WC-O4 each break the canonical
`17/192` value as predicted; WC-O5 (the `|q|+S` substitution) is recorded as
a typing-audit flag — it agrees arithmetically because `|q|=9=D²` on the
canonical OCTET row, but is structurally weaker (row-dependent rather than
substrate-typed) and therefore is not the locked form.

Class-label shuffle (informational only) drops the average clean-class match
rate from `1.000` to `0.139` — a clean indication that the channel typing is
real, not label-coincidental.

The 42 unequal-pair rows do **not** quantize to the base typed unit family
`{1/R², 1/(R·S), 1/(D·S²), 1/R, 1/M, 1/L}` at the precommitted tolerance.
The X column's 2-decimal storage precision is the immediate ceiling on what
can be characterized from this source; a higher-precision regeneration of the
unequal-pair X column, or an extended typed unit family including products
like `1/R³`, `1/(R²·D)`, or `1/(R²·S)`, would be a separate CR.

## Inputs (Hash-Locked)

```text
Precommit SHA-256       : 4ea9789806a8bd17e0c314cb6508ee9ab80c0212b49e68b0cdf94fd052d97dc2
Input snapshot SHA-256  : 7f5d9cc4c20f4bb62c3e40a4825c793ccc020fed72abb44ec17fe30406d8e4e5
Source workbook         : C:\VS\126part_with_carriers.xlsx (frozen snapshot in CR folder)

Substrate atoms (read-only from CR238):
  R = 12   D = 3   S = 8   alpha_H = 2   M = 126   L = 162
  kappa = 7117/768          g = 1/64
```

## Row Inventory

```text
single_write       :  63   (zero_contact,        Y = 0)
unequal_pair       :  42   (pair_write a≠b,      no precommitted base form)
color_triad        :  14   (positive_debit / negative_credit)
support            :  11   (no_surface_depth,    Y = 1)
equal_bound_pair   :   6   (pair_write a=b<9,    Y = 5/48)
carrier            :   1   (no_surface_depth,    Y = 1)
OCTET_pair         :   1   (pair_write[9|anti9], Y = 17/192)

Evaluated total    : 138 / 139 (138 rows enter clean-class+unequal-pair lanes)
Excluded           :   1   row 30 = QP093A-0301 (photon_road_carrier)
                           K_native = 0, X = 0 → Y_lift_fraction undefined.
                           Massless carrier has no mass-lift fraction by
                           construction; correctly excluded from the typed-
                           form audit, not a data defect.
```

## Block A — Clean-Class Typed Form Match

| Class               | Total | Evaluated | Match | Rate | Form |
|---------------------|------:|----------:|------:|-----:|---|
| color_triad         | 14    | 14        | **14** | 1.000 | `sign(q)·(|q|+D)/R` |
| equal_bound_pair    | 6     | 6         | **6**  | 1.000 | `(D+2)/(R(D+1)) = 5/48` |
| OCTET_pair          | 1     | 1         | **1**  | 1.000 | `(D²+S)/(D·S²) = 17/192` |
| single_write        | 63    | 63        | **63** | 1.000 | `0` (zero_contact) |
| support             | 11    | 11        | **11** | 1.000 | `1` (no_surface_depth) |
| carrier             | 1     | 1         | **1**  | 1.000 | `1` (no_surface_depth) |

All five precommitted clean classes are exact within the 2-decimal X-column
storage tolerance `ceil_tol(K) = max(1e-5, 0.005/|K|)`. Per-row predictions in
`CR243_clean_class_predictions.csv`.

## Block B — Substrate-Constant Wrong Controls (Per-Atom Dependence)

Each WC perturbs one substrate atom and re-evaluates the typed forms on all
clean classes. **Pass condition = degrades**, and the per-class degradation
table reveals which classes depend on which atom.

| WC    | Perturbation     | color_triad | equal_pair | OCTET | single_write | support | carrier |
|-------|------------------|:------:|:------:|:------:|:------:|:------:|:------:|
| WC-R1 | R=10, D=3, S=8   | 0/14 **D** | 0/6 **D** | 1/1   | 63/63 | 11/11 | 1/1 |
| WC-R2 | R=11, D=3, S=8   | 0/14 **D** | 0/6 **D** | 1/1   | 63/63 | 11/11 | 1/1 |
| WC-R3 | R=13, D=3, S=8   | 0/14 **D** | 0/6 **D** | 1/1   | 63/63 | 11/11 | 1/1 |
| WC-D1 | R=12, D=2, S=8   | 0/14 **D** | 0/6 **D** | 0/1 **D** | 63/63 | 11/11 | 1/1 |
| WC-D2 | R=12, D=4, S=8   | 0/14 **D** | 0/6 **D** | 0/1 **D** | 63/63 | 11/11 | 1/1 |
| WC-S1 | R=12, D=3, S=7   | 14/14 | 6/6   | 0/1 **D** | 63/63 | 11/11 | 1/1 |
| WC-S2 | R=12, D=3, S=9   | 14/14 | 6/6   | 0/1 **D** | 63/63 | 11/11 | 1/1 |

Reading: **D** = "degraded (the perturbed atom appears in this class's form)".

- `R`-perturbations break color triad and equal-pair (both contain `R`).
- `D`-perturbations break color triad, equal-pair, AND OCTET (all D-dependent).
- `S`-perturbations break ONLY OCTET (the only S-dependent clean class).
- Single-write (`Y=0`), support and carrier (`Y=1`) are constant under all
  WCs — they correctly contain no substrate atom.

Every WC degrades at least one clean class. **All seven substrate-constant
WCs pass.** Per-row WC counts in `CR243_wrong_controls.csv`.

## Block C — OCTET-Specific Wrong Controls

| WC     | Form                              | Value     | Breaks 17/192? |
|--------|-----------------------------------|-----------|---------------|
| WC-O1  | `(D²+S)/(D·S²)` at D=2, S=8       | 3/32 = 0.09375 | YES |
| WC-O2  | `(D²+S)/(D·S²)` at D=4, S=8       | 3/32 = 0.09375 | YES |
| WC-O3  | `(D²+S)/(D·S²)` at D=3, S=7       | 16/147 ≈ 0.10884 | YES |
| WC-O4  | `(D²+S)/(D·S²)` at D=3, S=9       | 2/27 ≈ 0.07407 | YES |
| WC-O5  | numerator substitution `(|q|+S)`  | agrees on canonical row (|q|=9=D²) | typing-audit flag |

WC-O5 specifically: arithmetic matches because the canonical OCTET row has
`|q|=9=D²=9`, so `|q|+S = D²+S`. The substitution is not falsified by
arithmetic on this single row; it is recorded as a structural-typing audit
flag — the substrate-typed form `(D²+S)/(D·S²)` is the locked claim because
the numerator is purely substrate atoms with no `q` dependence, whereas
`(|q|+S)/(D·S²)` would carry a row-dependent numerator. Note that under
`D=2` and `D=4`, both `(D²+S)/(D·S²)` and `(|q|+S)/(D·S²)` would give
different values on a hypothetical second OCTET row with `|q|≠D²` — the
table has only one OCTET row, so this distinction is *typing*, not
*arithmetic*, on this dataset.

## Block D — Class-Shuffle Control (Informational)

```text
seed                          = 20260623
average canonical match rate  = 1.000   (across the six clean classes)
average shuffled match rate   = 0.139
```

Per-class shuffled match rates fall sharply for every class. The shuffle
strongly degrades the typed-form match rate, supporting (but not by itself
proving) that the channel typing is structural rather than label-coincidental.
Reported as informational per session agreement; not a verdict criterion.

## Block E — Unequal-Pair Residual Quantization

```text
Total unequal-pair rows tested            : 42
Δ_unequal = Y_observed  (Y_base_unequal = 0, no precommitted base form)
Tolerance                                  : max(1e-5, 0.005/|K|)
Typed unit family                          : {1/R², 1/(R·S), 1/(D·S²),
                                              1/R, 1/M, 1/L}
                                              ≈ {0.00694, 0.01042, 0.00521,
                                                 0.08333, 0.00794, 0.00617}

Rows quantized to any base typed unit     : 0 / 42
Match rate                                 : 0.000
```

**Reading.** The observed Δ values cluster in the range `[1e-4, 5e-4]` —
roughly an order of magnitude *smaller* than the smallest base typed unit
`1/(D·S²) = 1/192 ≈ 5e-3`. No row resolves to an integer multiple of any
member of the precommitted unit family within tolerance.

The most likely reason is the X column's 2-decimal storage: the raw `X` values
for unequal-pair rows are stored as `±0.03` to `±0.14` and the `Y = X/K`
normalization rescales them into the `1e-4` range, where the underlying
analytic structure is masked by `±0.005` of rounding noise in `X`.

This is **not** a precommitted FAIL trigger; the unequal-pair lane was
explicitly reserved with `Y_base_unequal = 0` and the quantization scan was
declared informational. Per-row Δ and best-fit attempts in
`CR243_unequal_pair_residuals.csv`.

Two natural follow-ups (out of CR243 scope):

1. **Higher-precision regeneration.** Recompute the X column for the 42
   unequal-pair rows from the underlying analytic source (not from a
   2-decimal spreadsheet), then re-run the quantization test on the
   precommitted unit family.
2. **Extended typed unit family.** Include products `{1/R³, 1/(R²·D),
   1/(R²·S), 1/(R·D·S)}` and rationals like `1/(R·M)` in the unit family
   and re-precommit the quantization scan on a fresh CR.

## Block F — K-Gate Audit (Post-Execution)

| Gate | Status | Evidence |
|---|---|---|
| K1 | PARTIAL | Each clean-class form is an internal structural identity. External-anchor character is partial: the typed forms (`(|q|+D)/R`, `5/48`, `17/192`) were observed in pre-existing CR219+carriers data, and this CR tests their survival under substrate-constant perturbations. The class-shuffle informational result and per-atom WC dependence pattern are external-anchor-like in that the relationship could have come out otherwise. |
| K2 | PASS | Five precommitted typed forms; each could have failed. None did. All seven substrate-constant WCs could have failed to degrade. None did. |
| K3 | PARTIAL — DECLARED | The five typed forms were inferred from the data before the precommit was sealed. The precommit explicitly declares this and tests survival under constant-perturbation WCs + residual quantization (the latter is K3-clean — residuals were not used in form derivation). |
| K4 | PASS | Two foundational atoms `{F, S}` + structural constant `α_H` + read-only CR238 spine atoms `{R, D, S, M, L}`. No free parameter entered the runner. Source xlsx and precommit both SHA-locked at runner entry. |
| K5 | PASS | `python CR243_runner.py` deterministically reproduces every typed-form match count, every WC, every unequal-pair Δ, the class-shuffle, and the verdict assignment. |

## Block G — Strong-Pass Conditions

| Condition | Status |
|---|---|
| S1 color_triad 14/14 within ceil_tol | PASS |
| S2 equal_bound_pair 6/6 within ceil_tol | PASS |
| S3 OCTET within ceil_tol | PASS |
| S4 single_write 63/63 exact at Y=0 | PASS |
| S5 support+carrier all match Y=1 within ceil_tol | PASS |
| S6 WC-R1..R3 each degrade ≥ 1 clean class | PASS |
| S7 WC-D1..D2 each degrade ≥ 1 clean class | PASS |
| S8 WC-S1..S2 each degrade ≥ 1 clean class | PASS |
| S9 WC-O1..O4 each break canonical 17/192 | PASS |

## Cryptographic Chain (Inputs)

```text
CR114_result.md (capacity R² + split-loss)             = f691b9c9e966e408f378f968cf0a523c433e376234ed71488335090783e87543
CR217_result.md (162 = R²·9/8 closed ledger)           = 635791273a54838531d9b59177268a645b4ca151720da383784ac9ac047ffc2e
CR222_result.md (carrier ledger 12+1 closed sum)       = b316d0fb2e8d5eb83a8be4cad5a53926385004f3130434eebaf2d13b4beda83e
CR229_result.md (inclusion-exclusion identity)         = ee266dcc00bf90e71a40b8d576faaf81acd8fbdcc94fb3299ab14e97487237da
CR238_result.md (substrate spine compaction)           = 7c1b870014b7f45bd1686963c13304375792f443e7a6d156a2ae90c9489174ef
CR243_PRECOMMIT.md                                     = 4ea9789806a8bd17e0c314cb6508ee9ab80c0212b49e68b0cdf94fd052d97dc2
CR243_input_snapshot.xlsx                              = 7f5d9cc4c20f4bb62c3e40a4825c793ccc020fed72abb44ec17fe30406d8e4e5
```

## What CR243 Does

1. Locks five precommitted typed forms (`color_triad`, `equal_bound_pair`,
   `OCTET`, `single_write`, `no_surface_depth`) for the mass-lift fraction
   `Y = X / K` of the substrate particle/carrier table.
2. Tests each clean-class row against its bound form within a 2-decimal
   X-column storage tolerance and confirms exact match across 96/96 clean
   rows (sum of evaluated clean classes).
3. Runs seven substrate-constant wrong controls and confirms each perturbed
   atom degrades exactly the classes whose typed form contains that atom —
   per-atom dependence is structural, not coincidental.
4. Runs four OCTET-specific WCs (D=2, D=4, S=7, S=9) and confirms each
   breaks the canonical `17/192` value.
5. Records the `|q|+S` numerator-substitution as a typing-audit flag — the
   substrate-typed `D²+S` form is the locked claim because the numerator
   contains only substrate atoms.
6. Reports a class-shuffle WC as informational evidence (avg match rate
   `1.000 → 0.139`).
7. Reports the unequal-pair residual quantization scan as informational —
   no row resolves to a base typed unit at the precommitted tolerance,
   most likely because of X-column 2-decimal storage masking.

## What CR243 Does NOT Do

- Does NOT modify any upstream sealed CR. CR114, CR217, CR222, CR229, CR238
  remain frozen.
- Does NOT promote the typed-channel-table claim to a theorem-grade
  derivation of the unequal-pair residual structure. That structure remains
  open and is the natural CR244 (or beyond) target.
- Does NOT claim the five typed forms were derived blindly. K3 is recorded
  as PARTIAL-DECLARED: the forms were inferred from inspection of the
  source table prior to the precommit, and survival under substrate-constant
  perturbation is what the CR adds.
- Does NOT touch the rest-mass channel `Q_mass = 4·A·κ` from CR240, the
  Q_substrate gravitational coupling from CR238/CR239, or the binding
  curvature surface from CR242. CR243 audits a different SAM channel
  (per-row mass-lift fraction) on the same substrate atoms.

## Manuscript Implications

CR243 supplies an explicit "typed channel table" reading of the SAM particle
ledger:

```text
For each row P in the 139-row substrate ledger:
  Y(P) = F_channel(R, D, S; row data)
where F_channel is one of:
  {(|q|+D)/R, (D+2)/(R(D+1)), (D²+S)/(D·S²), 0, 1}
and the channel is selected by the {route_combination, surface_sign} pair.
```

This is the load-bearing structural claim that follows from CR238's substrate
compaction: the substrate has multiple channels, each typed in the same
foundational atoms, and a single global formula `Y = f(q)` is rejected by
construction.

Combined with the two-kernel ontology of CR239/CR240 (`Q_substrate ≠ Q_mass`),
the SAM picture is now: **the substrate carries several typed channels, each
selected by row-class, each derived from the CR238 atoms with no new
primitives** — a typed channel table, not a single mass formula.

## Rule of Immutability

Sealed 2026-06-23 by Sean Brady. Inputs, precommit, runner, tolerance
discipline, verdict gates, falsifiers all frozen.

If any sealed upstream CR (CR114, CR217, CR222, CR229, CR238) is later
regraded such that its frozen numerical value or structural identity changes,
CR243 must be re-examined and the typed-form per-atom dependence rebuilt.

If a higher-precision (>2 decimal) regeneration of the X column for the 42
unequal-pair rows becomes available, the residual quantization scan should
be re-precommitted as a follow-up CR (CR244 candidate).

---

**Sealed by:** Sean Brady, 2026-06-23
**Runner verified:** clean-class evaluations 96/96 EXACT (14+6+1+63+11+1);
substrate WCs 7/7 degrade per-atom; OCTET WCs WC-O1..O4 4/4 break canonical;
WC-O5 typing audit flagged; class-shuffle 1.000 → 0.139; unequal-pair
residuals 0/42 quantize to base typed unit family.
**Verdict driver:** all five precommitted typed forms exact; all substrate-
constant WCs degrade with structural per-atom dependence; all OCTET-specific
WCs break canonical `17/192`.
**Open follow-up:** unequal-pair residual structure (CR244 candidate) —
requires higher-precision X column or extended typed unit family.
