# CR218 Hidden Source Bigrade Derivation

Result: **CR218_PASS_HIDDEN_SOURCE_SET_DERIVED_FROM_BIGRADE_LATTICE_BOUNDED_BY_R__8_OF_8_OBSERVED_EQUALS_PREDICTED__WC1_WC2_WC3_ALL_FAIL_AS_REQUIRED**

## Direct Answer

The sealed 8-row hidden_source_support_rows partition set
`{1, 2, 3, 4, 6, 8, 9, 12}` is **exactly** reproduced by:

```
enumerate p = alpha_H^a * D^b for a, b in {0, 1, 2, ...}
include p iff p <= R
```

with `alpha_H = 2`, `D = 3`, `R = 12`. No extras, no omissions.

Equivalent algebraic statement: the set is exactly the bigrade-lattice
elements where the CR217 lift `p^2 / R^2 <= 1`. The hidden_source set
boundary **is** the lift unity line.

## What Changed

Before CR218, the set `{1, 2, 3, 4, 6, 8, 9, 12}` sat in CR214's
`hidden_source_support_rows` bin as an enumerator output we accepted as
given. CR217 verified the lift formula `m(p) = p + p^2/R^2` held on each
row but didn't explain the set membership.

After CR218, the set is **derived** from two sealed primitives and one
bound rule. The hypothesis was sharp, falsifiable, and now sealed.

## Input Verification

All four sealed inputs re-hashed at runtime, all matches confirmed:

| Input | Sealed sha256 head | Match |
|---|---|---|
| `CR214_particle_complement_195.csv`           | `e41016b5...` | yes |
| `CR216_particle_complement_194_active.csv`    | `01e780c0...` | yes |
| `CR217_summary.json`                          | `375e458b...` | yes |
| `02_A_KERNEL_WEAK_FIELD/README.md`            | `317081ed...` | yes |

## Sealed Primitives Carried In

- `alpha_H = 2` — sealed in `02_A_KERNEL_WEAK_FIELD/README.md` at derivation
  grade, propagated through G219, G305, G312 generator outputs and the
  CR142 row-gen qualifier sweep. Not derived here.
- `D = 3` — closure_depth on every carrier and hidden_source row.
- `R = 12`, `R^2 = 144` — sealed in SAMs_TOE glossary and used in CR213,
  CR214, CR217.

## The 8 Hidden Source Rows, Each Derived

| p | (a, b) | form | lift = p²/R² | row in CR214 |
|---:|---|---|---:|---|
| 1  | (0, 0) | `2^0 * 3^0` | 1/144 | QP093A-0306 |
| 2  | (1, 0) | `2^1 * 3^0` | 4/144 | QP093A-0307 |
| 3  | (0, 1) | `2^0 * 3^1` | 9/144 | QP093A-0308 |
| 4  | (2, 0) | `2^2 * 3^0` | 16/144 | QP093A-0309 |
| 6  | (1, 1) | `2^1 * 3^1` | 36/144 | QP093A-0310 |
| 8  | (3, 0) | `2^3 * 3^0` | 64/144 | QP093A-0311 |
| 9  | (0, 2) | `2^0 * 3^2` | 81/144 | QP093A-0312 |
| 12 | (2, 1) | `2^2 * 3^1` | **144/144 = 1** | QP093A-0313 |

The last row sits exactly on the lift unity line (`p = R`, `lift = 1`).
Every smaller bigrade element falls inside the lift-bounded region;
every larger bigrade element falls outside. The set boundary is the
lift-unity line.

## Set Comparison

| p | predicted by main rule | observed in CR214 | agreement |
|---:|:---:|:---:|---|
| 1, 2, 3, 4, 6, 8, 9, 12 | yes | yes | **MATCH** (all 8) |

- main extras (predicted minus observed): `{}` empty
- main omissions (observed minus predicted): `{}` empty
- `predicted_set == observed_set` → **true**

## Wrong Controls (all required to FAIL set-equality, all did)

### WC1 — relax bound to `p ≤ R² = 144`

Adds: `{16, 18, 24, 27, 32, 36, 48, 54, 64, 72, 81, 96, 108, 128, 144}`
→ 23 total elements. WC1 set ≠ observed set. **WC1 distinct as required.**

### WC2 — drop bigrade constraint, use `p ≤ R` alone

Adds: `{5, 7, 10, 11}` (integers in `[1, 12]` that are not `2^a · 3^b`)
→ 12 total elements. WC2 set ≠ observed set. **WC2 distinct as required.**

### WC3 — strict `p < R` (lift `<` 1, not `≤` 1)

Drops: `{12}` (the row where lift hits 1 exactly)
→ 7 total elements. WC3 set ≠ observed set. **WC3 distinct as required.**

All three wrong controls fire correctly, with the exact element-level
extras/omissions predicted in `CR218_declared_premises.json`. The
discrimination between the main rule and each variant is sharp: every
WC differs from the main rule by a specifically named, predicted set.

## Pass Conditions

11 of 11 checks passed. Execution status: CLEAN.

| Check | Result |
|---|---|
| all_inputs_verified | PASS |
| observed_set_equals_expected_8_rows | PASS |
| observed_set_size_is_8 | PASS |
| predicted_set_equals_expected | PASS |
| predicted_set_size_is_8 | PASS |
| predicted_set_equals_observed_set | PASS |
| no_extras_in_predicted_vs_observed | PASS |
| no_omissions_in_predicted_vs_observed | PASS |
| WC1_distinct_from_observed_and_size_23 | PASS |
| WC2_distinct_from_observed_and_size_12 | PASS |
| WC3_distinct_from_observed_and_size_7 | PASS |

## What is BACKED, what remains OPEN, what is NOT CLAIMED

### BACKED

- The set `{1, 2, 3, 4, 6, 8, 9, 12}` is exactly the bigrade-lattice
  elements `2^a · 3^b` bounded by `p ≤ R = 12`.
- Equivalently, the set boundary coincides with the CR217 lift unity
  line `p^2 / R^2 = 1`.
- The discriminating power of the rule is sharp: relaxing the bound
  (WC1), dropping the bigrade structure (WC2), or strict-inequality on
  the bound (WC3) each produces a clearly distinguishable set, with the
  specific extras/omissions named at PRECOMMIT time and observed at
  runtime.

### OPEN

- *Why* the upstream enumerator (CR119 / LC04 generator suite) selected
  the bigrade lattice `2^a · 3^b` as the hidden_source structural form.
  CR218 verifies the match; it does not derive the lattice choice.
- *Why* the bound is `p ≤ R` rather than some other functional of R.
  CR218 shows the bound matches the lift unity line; the deeper question
  of why the unity line is the structural boundary is a follow-up.

### NOT CLAIMED

- That `lift bound causes the set boundary` in a mechanistic sense. CR218
  records the two coincide on the sealed data. Causality between the
  lift formula and the lattice-cutoff is a separate question.
- That this derivation generalizes to other bins. CR217 already showed
  the lift formula is bin-locked to hidden_source. Whether other bins
  have analogous lattice-bound derivations is open (a CR219-grade
  question).

## Implications (not promoted in this CR)

The 8-row hidden_source set is no longer an enumerator artifact. It is
the answer to a single combinatorial question: *what is the bigrade
lattice generated by `alpha_H = 2` and `D = 3` inside the lift-stable
region?* The answer has exactly 8 elements, matches the courtroom-sealed
set element-by-element, and the largest element sits on the lift unity
line.

The Seanbrady identity from CR217 reads:

```
99 + 45 = 144 = R^2
162 = R^2 * (9/8)
163.4652778 = 162 + 211/144
```

Combined with CR218, the hidden_source contribution `45 = 1+2+3+4+6+8+9+12`
and the bigrade-squared contribution `355 = 1+4+9+16+36+64+81+144` are
themselves derived sums over the bigrade lattice bounded by R. The
identity is now built from two primitives (`alpha_H, D`) and one bound
rule (`lift <= 1`), nothing else, on the hidden-source side.

## Chain of Custody

CR119 (sealed) → CR214 (sealed) → CR215 (identified duplicate) → CR216
(retired QP093A-0305) → CR217 (verified closed-form lift identity) →
**CR218** (derived the hidden_source set from `alpha_H, D, R` and the
lift bound).

Every step hash-linked. No sealed artifact modified anywhere.

## Artifacts

- `CR218_PRECOMMIT.md`
- `CR218_declared_premises.json`
- `CR218_runner.py`
- `CR218_input_manifest.csv`
- `CR218_bigrade_enumeration.csv`     *(full a,b → p table up to R²)*
- `CR218_set_comparison.csv`          *(P_main vs P_obs side by side)*
- `CR218_wrong_controls.csv`          *(WC1, WC2, WC3 with pass/fail)*
- `CR218_summary.json`
- `HASHES.txt`
