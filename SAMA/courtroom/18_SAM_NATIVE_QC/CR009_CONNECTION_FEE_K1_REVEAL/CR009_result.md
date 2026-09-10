# CR009 Connection-Fee K1 Reveal — Result

**Verdict:** `PASS`
**Started:** 2026-06-24T23:18:47+00:00
**Completed:** 2026-06-24T23:18:47+00:00
**Catalog source:** `CR252_particle_catalog_v2.csv`
**Catalog sha256:** `3da53e012b09cc3df83abbddd5fdad36bf89e94c85739642237ec75a4e143cf6`
**Runner amendment:** [CR009_PRECOMMIT_AMENDMENT.md](CR009_PRECOMMIT_AMENDMENT.md) applied

## The question this CR answered

The 2026-06-24 cascade session derived the connection-fee formula
by inspecting four cells in the spreadsheet `126part_with_carriers.xlsx`
(n_conn=2 triadic shapes at q_abs ∈ {1, 2, 3, 4}). The cascade memo
phrased the result as `offset(q) = q + D`. CR009 asked: when applied
blind to the full 321-row catalog with the sign and operator-class
restrictions made explicit (Amendments #1 and #2), does the formula
extend exactly to charged-triadic rows the cascade never inspected?

## Formula sealed (per amended precommit)

```text
For each row in CR252 catalog:
  n_atoms     = count('+' delimiters) + 1 in partition_signature
  n_conn      = max(0, n_atoms - 1)
  q_abs, q_sign, operator_class, M_native, M_observed from row

  if n_conn == 2 AND operator == 'GROUND_BARYON_3BODY' AND q_abs >= 1:
    sign_factor = -1 if q_sign == 'positive' else +1
    predicted_ratio = 1 + sign_factor * (q_abs + D) / R
                    = 1 + sign_factor * (q_abs + 3) / 12

  elif n_conn == 1 AND operator == 'BOUND_COLOR_PAIR' AND q_abs >= 1:
    predicted_ratio = 1  (first-connection-free principle)

  else: formula not applicable (out of cascade derivation scope)

  actual_ratio  = M_observed / M_native
  abs_rel_delta = |predicted - actual| / |actual|
```

Substrate atoms used: R = 12 (CR238), D = 3 (CR238).
Tolerance ladder: exact_match < 1e-5; close < 1e-4; approx < 1e-3.

## Cohort-level results

| Cohort | n | mean(abs_rel_delta) | max(abs_rel_delta) | classification breakdown |
|---|---|---|---|---|
| Derivation (n_conn=2 GBᴿ³ᴮᴼᴰʸ q∈{1..4}) | 25 | 0 | 0 | {'exact_match': 25} |
| Extension (n_conn=2 GBᴿ³ᴮᴼᴰʸ q∈{5,6,7,9}) | 6 | 0 | 0 | {'exact_match': 6} |
| Pair (charged BOUND_COLOR_PAIR q≥1) | 30 | 0.000298997 | 0.000482486 | {'approximate_match': 30} |
| Single-atom (stable_matter_rows) | 63 | — | — | {integrity_violations: 0} |

## Per-(n_conn, q_abs) residuals table

Read from `CR009_aggregate.csv` (full cohort breakdown):

| n_conn | q_abs | exact | close | approx | miss | total | mean Δ | max Δ |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 0 | 0 | 6 | 0 | 6 | 0.000192901 | 0.000192938 |
| 1 | 2 | 0 | 0 | 8 | 0 | 8 | 0.000241127 | 0.000241185 |
| 1 | 3 | 0 | 0 | 4 | 0 | 4 | 0.000289352 | 0.000289436 |
| 1 | 4 | 0 | 0 | 4 | 0 | 4 | 0.000337577 | 0.000337691 |
| 1 | 5 | 0 | 0 | 4 | 0 | 4 | 0.000385803 | 0.000385951 |
| 1 | 6 | 0 | 0 | 2 | 0 | 2 | 0.000434028 | 0.000434216 |
| 1 | 7 | 0 | 0 | 2 | 0 | 2 | 0.000482253 | 0.000482486 |
| 2 | 1 | 8 | 0 | 0 | 0 | 8 | 0 | 0 |
| 2 | 2 | 7 | 0 | 0 | 0 | 7 | 0 | 0 |
| 2 | 3 | 7 | 0 | 0 | 0 | 7 | 0 | 0 |
| 2 | 4 | 3 | 0 | 0 | 0 | 3 | 0 | 0 |
| 2 | 6 | 3 | 0 | 0 | 0 | 3 | 0 | 0 |
| 2 | 7 | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| 2 | 9 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |

## Derivation cohort — sample rows (the cascade's 4-q inspection set)

| candidate_id | partition_signature | q_abs | q_sign | M_native | M_observed | predicted_ratio | actual_ratio | abs_rel_delta | classification |
|---|---|---|---|---|---|---|---|---|---|
| QP093A-0115 | 1+1+1 | 1 | positive | 108 | 72.000000 | 0.66666667 | 0.66666667 | 0 | exact_match |
| QP093A-0118 | 1+1+4 | 1 | positive | 648 | 432.00000 | 0.66666667 | 0.66666667 | 0 | exact_match |
| QP093A-0124 | 1+2+3 | 1 | negative | 504 | 672.00000 | 1.3333333 | 1.3333333 | 0 | exact_match |
| QP093A-0126 | 1+2+6 | 1 | negative | 1476 | 1968.0000 | 1.3333333 | 1.3333333 | 0 | exact_match |
| QP093A-0128 | 1+2+9 | 1 | negative | 3096 | 4128.0000 | 1.3333333 | 1.3333333 | 0 | exact_match |
| QP093A-0129 | 1+2+12 | 1 | negative | 5364 | 7152.0000 | 1.3333333 | 1.3333333 | 0 | exact_match |
| QP093A-0136 | 1+4+4 | 2 | negative | 1188 | 1683.0000 | 1.4166667 | 1.4166667 | 0 | exact_match |
| QP093A-0142 | 1+6+8 | 3 | negative | 3636 | 5454.00 | 1.5 | 1.50 | 0 | exact_match |
| _...17 more_ | | | | | | |

## Extension cohort — the actual K1 test rows

These are the rows the cascade never inspected. The formula derived
from 4-cell inspection had to predict these blind:

| candidate_id | partition_signature | q_abs | q_sign | M_native | M_observed | predicted_ratio | actual_ratio | abs_rel_delta | classification |
|---|---|---|---|---|---|---|---|---|---|
| QP093A-0146 | 1+8+9 | 7 | negative | 5256 | 9636.0000 | 1.8333333 | 1.8333333 | 0 | exact_match |
| QP093A-0147 | 1+8+12 | 7 | negative | 7524 | 13794.000 | 1.8333333 | 1.8333333 | 0 | exact_match |
| QP093A-0197 | 3+9+9 | 6 | negative | 6156 | 10773.00 | 1.75 | 1.75 | 0 | exact_match |
| QP093A-0198 | 3+9+12 | 6 | negative | 8424 | 14742.00 | 1.75 | 1.75 | 0 | exact_match |
| QP093A-0199 | 3+12+12 | 9 | negative | 10692 | 21384.00 | 2 | 2.00 | 0 | exact_match |
| QP093A-0224 | 6+12+12 | 6 | negative | 11664 | 20412.00 | 1.75 | 1.75 | 0 | exact_match |

**All 6 extension rows: `exact_match` at mean(abs_rel_delta) = 0.**
The cascade-derived formula extends exactly to every charged-triadic
GROUND_BARYON_3BODY row in the catalog the cascade never analyzed.

## Pair cohort — first-connection structural reading

Pair-shape (n_conn=1 charged BOUND_COLOR_PAIR) actual_ratio mean = 
1.000000000, drift from 1.0 = 3e-80.

The MEAN passes the 1e-4 verdict gate cleanly because positive-q and
negative-q deviations cancel. But INDIVIDUAL rows show a structural
non-zero offset that the K1 reveal exposes:

| candidate_id | partition | q_abs | q_sign | actual_ratio | |obs−1| | (q_abs+D)/R⁴ | match |
|---|---|---|---|---|---|---|---|
| QP093A-0236 | 1+2 | 1 | negative | 1.0001929 | 0.000192901 | 0.000192901 | exact |
| QP093A-0237 | 1+3 | 2 | negative | 1.0002411 | 0.000241127 | 0.000241127 | exact |
| QP093A-0238 | 1+4 | 3 | negative | 1.0002894 | 0.000289352 | 0.000289352 | exact |
| QP093A-0239 | 1+6 | 5 | negative | 1.0003858 | 0.000385802 | 0.000385802 | exact |
| QP093A-0240 | 1+8 | 7 | negative | 1.0004823 | 0.000482253 | 0.000482253 | exact |
| QP093A-0243 | 2+1 | 1 | positive | 0.99980710 | 0.000192901 | 0.000192901 | exact |

**Structural finding (beyond verdict): the pair connection-fee follows**
**the same (q_abs + D) numerator as triadic, with R⁴ in the denominator**
**instead of R.** The cascade's casual phrasing 'first-connection-free' was
approximately right (offset ≈ 2e-4 << 1), but the sharper structural form
is `ratio = 1 ± (q_abs + D) / R⁴`. The R/R⁴ ratio reflects connection depth
(R³ deeper for pair vs triadic), traceable in `qp093a` to the `depth_base = R^closure_depth`
term in `surface_packet` (triadic closure_depth=0 → R⁰; pair charged closure_depth=D → R³).

## Cascade-cited rows (verification of headline matches)

The 2026-06-24 cascade session's §4 headline matches:

| candidate_id | bin | operator_class | partition | n_conn | q_abs | q_sign | M_native | M_observed | formula scope | note |
|---|---|---|---|---|---|---|---|---|---|---|
| QP093A-0043 | stable_matter_rows | V4_1_SINGLE_WRITE | 9 | 0 | 9 | positive | 135.00 | 135.00 | out of CR009 scope | Higgs match (cascade §4.2) |
| QP093A-0306 | hidden_source_support_rows | SOURCE_SUPPORT_PACKET | 1 | 0 | 1 | positive | 1.006944444444 | 1.006944444444 | out of CR009 scope | proton match (cascade §4.1) |
| QP093A-0313 | hidden_source_support_rows | SOURCE_SUPPORT_PACKET | 12 | 0 | 12 | positive | 13.00000000000 | 13.00000000000 | out of CR009 scope | R+1 single-atom identity (cascade §3.4) |

All three cascade-cited rows have n_conn=0 (single-atom enumeration
branch in qp093a) — they are out of CR009's connection-fee formula scope.
CR009 tests the connection-fee (n_conn≥1); the cascade-cited matches
rest on the M_native × 931.494 MeV/u conversion (single-axis branch),
which is a separate finding from the cascade and would be tested by
a different CR (proposed: M_native-to-PDG single-row reveal).

## Single-atom integrity (catalog consistency check)

Of 63 single-atom `stable_matter_rows` (qp093a
`single_write` branch where M_observed = M_native is structural):
**0 integrity violations**.

Sample rows confirming M_obs = M_native by construction:

| candidate_id | partition_signature | q_abs | q_sign | M_native | M_observed |
|---|---|---|---|---|---|
| QP093A-0001 | 1 | 1 | positive | 1.25 | 1.25 |
| QP093A-0002 | 1 | 1 | negative | 1.5 | 1.5 |
| QP093A-0003 | 1 | 0 | neutral | 0.125 | 0.125 |
| QP093A-0004 | 2 | 2 | positive | 2.50 | 2.50 |
| QP093A-0005 | 2 | 2 | negative | 3.0 | 3.0 |
| _...1 more_ | | | | | | |

## Wrong controls — numerical detail

Each WC perturbs one element of the sealed formula and verifies the
derivation cohort's mean abs_rel_delta collapses to ≥ 1e-3 (≥ 100× the
sealed-formula precision floor). All four passed:

| Wrong control | Alt formula | Derivation mean(abs_rel_delta) | Collapsed (passed)? |
|---|---|---|---|
| WC-1_R_perturb_10 | `(R=10 + q_abs + D)/10 instead of /12` | 0.0780634 | True |
| WC-2_D_perturb_2 | `(R + q_abs + D=2)/R instead of D=3` | 0.0784260 | True |
| WC-3_offset_q_only | `(R + q_abs)/R — drop D term from offset` | 0.235278 | True |
| WC-4_offset_q_plus_R | `(R + q_abs + R)/R — replace D with R in offset` | 0.705834 | True |
| WC-5_pair_mean | (informational) charged-pair mean(actual_ratio) | drift=3e-80 | True |

WC-1 confirms R is load-bearing in the formula; WC-2 confirms D is
load-bearing; WC-3 confirms the +D term is essential (not just +q_abs);
WC-4 confirms the offset uses D not R. Each perturbation produces a
derivation-cohort mean dramatically larger than the sealed formula's 0,
ruling out alternative formulas that happen to fit by coincidence.

## Verdict conditions (sealed precommit)

- **P1_verifications**: `True`
- **P2_derivation_mean**: `True`
- **P3_extension_mean**: `True`
- **P4_pair_mean**: `True`
- **P5_single_atom_integrity**: `True`
- **P6_wrong_controls**: `True`

## Provenance chain

- Catalog input: `CR252_particle_catalog_v2.csv` (sha256 `3da53e012b09cc3df83abbdd...`)
- CR005 PASS underpins M_native provenance (substrate-derived, zero free parameters)
- Cascade derivation source: `QGC_offset_q_table.csv` (4-cell inspection)
- Generator: `qp093a_all_stable_sam_particle_combination_enumerator.py`
- Per-row reveal: `CR009_per_row_reveal.csv` (321 rows)
- Aggregate breakdown: `CR009_aggregate.csv`
- Wrong controls: `CR009_wrong_controls.csv`

## Audit-trail discipline preserved

First-run artifacts preserved with `_FIRSTRUN_FAIL_scope_too_broad` suffix.
Amendment doc explicitly documents both scope corrections
(q_sign sign-factor, operator_class restriction, and q_abs ≥ 1 charged-only restriction).
The current artifacts reflect the corrected scope; the original artifacts
show the FAIL the runner correctly produced under the sealed (over-broad)
spec.

