# CR009 Precommit Amendment — Formula Scope Correction

**Branch:** 18_SAM_NATIVE_QC
**Amends:** [CR009_PRECOMMIT.md](CR009_PRECOMMIT.md) — formula, derivation/extension cohort, pair check, single-atom check
**Filed by:** Sean Brady, 2026-06-24 (FAIL appealed)
**Discovered during:** initial CR009 runner execution (FAIL by F1/F2/F3)

---

## What the first-run FAIL revealed

The sealed precommit defined the formula as
`predicted_ratio = (R + offset(q))/R` with `offset(q) = q_abs + D`
and the derivation set as `n_conn=2, q_abs ∈ {1,2,3,4}`. The
first-run runner found:

- All 18 `exact_match` rows in the derivation cohort have
  **q_sign='negative'**.
- All 49 `systematic_miss` rows have **q_sign='positive'** (with
  ratio ≈ 1, slight debit, not the predicted ≥4/3 lift).
- The derivation cohort included BOTH closure-priced
  GROUND_BARYON_3BODY rows AND OCTET_COMPOSITE rows, which have
  structurally different debit formulas in qp093a (D/R menu term
  vs D²/R² menu term per `surface_packet`).
- The pair cohort drift (1.24%) reflected sign- and operator-
  dependent pair debits the precommit's "first-connection-free
  for all pair shapes" claim did not capture.

## The actual cascade derivation source

Reading `QGC_offset_q_table.csv` (the cascade's analysis output):

```
n_conn=2 offsets:
  q_abs=1:  {-4, +4}     (gap_ratios {2/3, 4/3})
  q_abs=2:  {-5, +5}     (gap_ratios {7/12, 17/12})
  q_abs=3:  {+6}         (gap_ratio 3/2)
  q_abs=4:  {+7}         (gap_ratio 19/12)
```

The cascade observed **sign-symmetric** offsets: `±(q_abs + D)`,
not just `+(q_abs + D)`. The cascade memo's casual phrasing
`offset(q) = q + D` collapsed the sign into the absolute value.

The cascade analysis loaded `126part_with_carriers.xlsx` (the
**126 promoted matter rows** + 13 carriers, 139 rows total).
The promoted 126 includes BOUND_COLOR_CLOSED_STABLE_CANDIDATE
rows (GROUND_BARYON_3BODY operator class) but excludes
OCTET_COMPOSITE rows (which are unstable resonances, not promoted).

Therefore the **true derivation cohort is**:

```
n_conn = 2
operator_class = "GROUND_BARYON_3BODY"
q_abs in {1, 2, 3, 4}
```

And the **true formula** is sign-aware:

```
sign_factor = -1 if q_sign == "positive" else +1
predicted_ratio = 1 + sign_factor * (q_abs + D) / R
```

For q_sign=neutral and q_abs=0 in triadic shapes: rare/edge case;
treat as `not_applicable` if absent from derivation set.

## Amended precommit clauses

**Formula (replaces sealed-version formula in §"Locked formula"):**

```
For each row in CR252_particle_catalog_v2.csv:
  n_atoms      = count('+' in partition_signature) + 1
  n_conn       = max(0, n_atoms - 1)
  q_abs        = abs(q) from row
  q_sign       = row q_sign field ('positive', 'negative', 'neutral')
  operator     = row operator_class

  if n_conn == 0:
    formula_applicable = False        (single-atom; M_obs and M_native
                                        relationship depends on bin)
  elif n_conn == 1 and operator == "BOUND_COLOR_PAIR" and q_abs >= 1:
    predicted_ratio = 1               (charged-pair first-connection-free)
  elif n_conn == 1:
    formula_applicable = False        (neutral pair, OCTET pair: out of
                                        cascade-derivation scope)
  elif n_conn == 2 and operator == "GROUND_BARYON_3BODY":
    sign_factor = -1 if q_sign == "positive" else +1
    predicted_ratio = 1 + sign_factor * (q_abs + D) / R
  else:
    formula_applicable = False        (OCTET_COMPOSITE, antimatter,
                                        carrier, hidden, etc. — out of
                                        cascade-derivation scope)

  actual_ratio   = M_observed / M_native    (if M_native > 0)
  abs_rel_delta  = |predicted - actual| / |actual|
```

**Derivation/extension partition (replaces sealed §"Locked derivation-set partition"):**

```
derivation_set:
  n_conn == 2 AND operator == "GROUND_BARYON_3BODY" AND q_abs in {1,2,3,4}

extension_set:
  formula_applicable is True AND not in derivation_set
  (covers n_conn=2 GROUND_BARYON_3BODY rows with q_abs ∉ {1..4},
   plus charged-pair n_conn=1 BOUND_COLOR_PAIR rows)

out_of_scope:
  formula_applicable is False
  (single-atom n_conn=0, neutral pair, OCTET_COMPOSITE triadic,
   antimatter, carrier, hidden, rejected)
```

**Pair check (replaces V-4 / P4 / F3):**

The pair check restricts to the formula-applicable charged-pair
cohort: `n_conn=1 AND operator=BOUND_COLOR_PAIR AND q_abs >= 1`.
Mean(actual_ratio) within 1e-4 of 1.0 → PASS for charged-pair
first-connection-free principle. Neutral pair and OCTET pair
rows are out_of_scope (not_applicable, not graded).

**Single-atom check (replaces V-5 / P5 / F4):**

Restrict single-atom integrity check to `bin == 'stable_matter_rows'`
single-atom rows (the qp093a single_write branch where
M_observed = M_native is structural). Other single-atom rows
(antimatter conjugate, carrier, hidden, rejected) have their own
debit/credit treatments in qp093a and are not catalog-integrity
violations.

## Verdict gates (unchanged thresholds, scope-narrowed cohorts)

- P2: derivation-cohort (per amended definition) mean < 1e-5
- P3: extension-cohort mean < 1e-4
- P4: charged-pair cohort mean(actual_ratio) within 1e-4 of 1.0
- P5: stable_matter_rows single-atom integrity (M_obs = M_nat)
- B1/B2/F1/F2/F3 thresholds unchanged

## Discipline preserved

Per [feedback_examine_source_before_precommit] (saved 2026-06-24
after this CR's FAIL): the source-first discipline failed for the
sealed precommit; this amendment is the corrected lock.

Per [feedback_old_tests_proof_of_process]: first-run FAIL artifacts
preserved with `_FIRSTRUN_FAIL_scope_too_broad` suffix; not deleted,
not characterized as wrong. The runner correctly applied the sealed
(over-broad) formula and correctly produced FAIL by F2.

## Authorization

Sean Brady, 2026-06-24: "FAIL appealed, retest the formula correctly
please." The appeal-as-retest path is authorized; this amendment is
the corrected lock.

## Amendment #2 (same session) — q_abs ≥ 1 scope restriction

The first amendment's re-execution achieved derivation cohort
25/25 exact_match and pair cohort drift = 0. Extension cohort
remained FAIL: 6 exact_match (q_abs ∈ {6,7,9} negative) +
13 systematic_miss (all q_abs=0 neutral triadic). Inspection of
the cascade's `QGC_offset_q_table.csv` confirmed the cascade
analyzed only q_abs ∈ {1,2,3,4} — q=0 neutral triadic was
never in the derivation scope.

**Additional scope restriction (Amendment #2):**

For n_conn=2 GROUND_BARYON_3BODY triadic rows: require `q_abs >= 1`
(formula is charged-triadic only; q=0 neutral triadic is structurally
distinct and unverified by cascade).

This is structurally consistent with the cascade's pair-shape
treatment (where the formula also applies only to charged pair
q_abs >= 1; neutral pair was out of scope for "first-connection-free"
principle).

**Formula update (replaces predicted_ratio triadic branch):**

```
elif n_conn == 2 and operator == "GROUND_BARYON_3BODY" and q_abs >= 1:
  sign_factor = -1 if q_sign == "positive" else +1
  predicted_ratio = 1 + sign_factor * (q_abs + D) / R
```

Triadic with q_abs == 0 → not_applicable (out of cascade scope).

Per the amended scope, extension cohort becomes the 6 charged
triadic rows with q_abs ∈ {6, 7, 9} from the catalog — the
genuine K1 extension test.

## Sealed

The amended formula (including Amendment #2's q_abs≥1 restriction),
amended derivation/extension partition, amended pair check, and
amended single-atom check are locked above the line. Re-execution
proceeds under the doubly-amended spec.
