# CR009 — Connection-Fee K1 Reveal

**Branch:** 18_SAM_NATIVE_QC
**Sealed by:** Sean Brady, 2026-06-24
**Input artifact:** [CR252_particle_catalog_v2.csv](../../09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_particle_catalog_v2.csv)
**Provenance backing:** [CR005 PASS](../CR005_M_NATIVE_PROVENANCE_AUDIT/CR005_result.md) (zero physics-fit inputs across upstream chain)

---

## Question

Does the substrate-derived connection-fee formula

```text
   M_observed / M_native  =  (R + offset(q)) / R
```

with

```text
   offset(q) = q_abs + D     for n_conn = 2  (triadic shapes; closure-priced)
   offset(q) = 0             for n_conn = 1  (pair shapes; first-connection-free)
   formula not applicable    for n_conn = 0  (single-atom; M_observed = M_native by construction)
```

correctly predict the M_observed / M_native ratio for the full
321-row CR252 particle catalog when applied **blind** to every row,
including q values and partition signatures that were NOT used in
the 2026-06-24 cascade-session derivation?

## K1 honest framing

The formula above was **derived during the 2026-06-24 cascade
session by inspecting four (n_conn=2, q_abs) cells** in the
`126part_with_carriers.xlsx` spreadsheet:

```text
   q_abs = 1   →   ratio = 16/12 = 4/3
   q_abs = 2   →   ratio = 17/12
   q_abs = 3   →   ratio = 18/12 = 3/2
   q_abs = 4   →   ratio = 19/12
```

These four cells produced the conjecture `offset(q) = q + D`. That's
4 data points — a small derivation set. **CR009 is not a from-scratch
blind K1**; the formula already exists. What CR009 IS:

1. **A formalization seal.** Lock the formula above the line as the
   substrate-derived prediction. No tuning, no refinement, no
   per-row adjustments allowed after this point.

2. **An extension test.** Apply the formula to **every row in the
   321-row catalog**, including:
   - n_conn=2 triadic rows with q_abs values OUTSIDE the derivation
     set {1, 2, 3, 4} (i.e., q_abs ∈ {0, 5, 6, 7, 8, 9, 10, 11, 12+})
   - n_conn=1 pair rows (the first-connection-free principle)
   - n_conn=0 single-atom rows (consistency check; should be M=N)

3. **A reveal against the actual catalog.** Compute predicted_ratio
   per the formula; compare to actual_ratio from CR252 catalog.
   Report match exactness, deviation distribution, and any
   systematic patterns.

The extension-test discipline: the formula was derived from a
4-point subset. If it extends cleanly to the entire 321-row catalog
(or to the n_conn-typed subset where the formula applies), that is
evidence the formula captures a structural identity rather than a
4-point coincidence. If it fits ONLY the derivation set and fails
elsewhere, the formula is a 4-point coincidence and the cascade-
session §3.3 claim must be downgraded accordingly.

## Locked formula (read-only above the line)

```text
   For every row in CR252_particle_catalog_v2.csv:

   n_atoms     = count of '+'-separated terms in partition_signature
   n_conn      = max(0, n_atoms - 1)
   q_abs       = absolute value of q from row
   M_native    = M_native value from row
   M_observed  = M_observed_candidate value from row
   actual_ratio    = M_observed / M_native   (if M_native > 0)

   predicted_ratio:
     if n_conn == 0:
       formula_applicable = False        (single-atom; identity by construction)
     elif n_conn == 1:
       predicted_ratio = 1                (first-connection-free principle)
     elif n_conn == 2:
       offset_q = q_abs + D              (with D = 3)
       predicted_ratio = (R + offset_q) / R    (with R = 12)
     elif n_conn >= 3:
       formula_applicable = False        (out of scope; not derived in cascade)

   delta = predicted_ratio − actual_ratio
   abs_rel_delta = |delta| / actual_ratio   (if actual_ratio > 0)
```

## Locked classification per row

CSV-precision-aware factor-of-10 ladder. The CR252 catalog stores
M_native and M_observed as decimal strings with finite precision; the
ratio precision floor is the catalog's decimal-place limit, not
machine epsilon.

```text
   For each row where formula_applicable is True:

   exact_match       : abs_rel_delta < 1e-5     (0.001% — CSV precision floor)
   close_match       : 1e-5 <= abs_rel_delta < 1e-4
   approximate_match : 1e-4 <= abs_rel_delta < 1e-3
   systematic_miss   : abs_rel_delta >= 1e-3    (≥ 0.1%)

   For rows where formula_applicable is False:
   not_applicable    : reported, not graded
```

## Locked derivation-set partition

```text
   derivation_set:
     n_conn == 2 AND q_abs in {1, 2, 3, 4}

   extension_set:
     formula_applicable is True
     AND not in derivation_set

   The verdict primarily rests on the extension_set behavior.
   Derivation_set matches are sanity checks (expected by construction).
```

## Locked verifications

Verdict is **cohort-mean-based**, not single-row-based. A single
outlier (e.g., one row with a 1e-6 CSV-precision artifact) does
NOT deny a cohort verdict. Systematic drift across a cohort (mean
shifted) does.

```text
V-1   Formula applied to every row in CR252 catalog (321 rows);
      classification computed for each; results written to
      CR009_per_row_reveal.csv (diagnostic per-row detail)

V-2   Derivation_set (n_conn=2, q_abs ∈ {1,2,3,4}):
      mean(abs_rel_delta) across cohort is < 1e-5.
      If derivation-set mean exceeds 1e-5, the formula's lockdown
      reading is itself drifted at the catalog-precision level.

V-3   Extension_set classification breakdown reported:
      per (n_conn, q_abs) cohort, count of exact_match / close_match
      / approximate_match / systematic_miss, plus mean(abs_rel_delta)
      per cohort

V-4   Pair-shape (n_conn=1) cohort: report mean(actual_ratio).
      First-connection-free principle predicts mean = 1.0.

V-5   Single-atom (n_conn=0) cohort: confirm M_observed = M_native
      for all. This is BY CONSTRUCTION in qp093a (route_class
      single_write / outer_binary_neutral force zero surface debit)
      and serves as a catalog-integrity check, not a precision
      claim.

V-6   Per-row CSV includes: candidate_id, partition_signature,
      n_atoms, n_conn, q_abs, q_sign, M_native, M_observed,
      actual_ratio, predicted_ratio, abs_rel_delta, classification,
      derivation_or_extension_set

V-7   Aggregate counts written to CR009_aggregate.csv: per
      n_conn × derivation/extension × classification, plus
      mean(abs_rel_delta) per cohort
```

## Locked wrong controls

```text
WC-1  (R perturbation) Recompute predicted_ratio with R=10 instead
      of R=12. Verify derivation-set mean(abs_rel_delta) ≥ 1e-3
      (≥ 100× the sealed-formula precision floor). Confirms R is
      load-bearing.

WC-2  (D perturbation) Recompute with D=2 instead of D=3. Verify
      derivation-set mean(abs_rel_delta) ≥ 1e-3. Confirms D is
      load-bearing.

WC-3  (offset alternative — no D term) Recompute with
      offset(q) = q_abs (no +D). Verify derivation set mean
      ≥ 1e-3 (predicted becomes (12+q)/12 not (15+q)/12).

WC-4  (offset alternative — wrong scale) Recompute with
      offset(q) = q_abs + R (instead of q_abs + D). Verify
      derivation set mean ≥ 1e-3.

WC-5  (pair-shape mean) Pair-shape (n_conn=1) cohort:
      report mean(actual_ratio). Used as verification for P4
      (first-connection-free principle).
```

## Locked verdict gates

All cohort metrics are **means**, not medians. Single-row outliers
do not move the verdict; systematic cohort-wide drift does.

```text
PASS conditions (all required):
  P1  V-1 through V-7 hold
  P2  Derivation set (n_conn=2, q_abs ∈ {1,2,3,4}):
      mean(abs_rel_delta) < 1e-5 (within CSV precision floor)
  P3  Extension set (n_conn=2, q_abs NOT in derivation set):
      mean(abs_rel_delta) < 1e-4
      (10× looser than derivation — extension is the real test)
  P4  Pair-shape (n_conn=1) cohort:
      |mean(actual_ratio) − 1.0| < 1e-4
      (first-connection-free principle holds at CSV precision)
  P5  Single-atom (n_conn=0) cohort: M_observed = M_native
      for all rows (qp093a construction; catalog-integrity check)
  P6  WC-1 through WC-4 all confirm formula sensitivity to
      R/D/offset structure (each perturbation produces mean
      abs_rel_delta ≥ 1e-3 — at least 1000× worse than the
      sealed formula)

BOUNDARY conditions:
  B1  P1, P2, P5, P6 hold; extension-set mean(abs_rel_delta)
      is in [1e-4, 1e-3]. Formula extends partially; documented
      as "formula structural for derivation set; extension shows
      systematic drift at the 0.01%–0.1% level."
  B2  P1, P2, P5, P6 hold; |mean(pair actual_ratio) − 1.0|
      in [1e-4, 1e-3]. First-connection-free principle
      approximate, not exact at CSV precision.

FAIL conditions:
  F1  V-2 fails: derivation set mean(abs_rel_delta) ≥ 1e-5.
      The formula's lockdown reading is drifted at the catalog-
      precision level — formula is wrong even on its derivation.
  F2  Extension set mean(abs_rel_delta) ≥ 1e-3.
      Formula fits derivation set but does NOT extend; it was
      a 4-point coincidence at best.
  F3  Pair-shape cohort: |mean(actual_ratio) − 1.0| ≥ 1e-3.
      First-connection-free principle false at the structural
      level.
  F4  Single-atom rows fail V-5: catalog has rows where qp093a's
      single_write construction did not produce M_observed = M_native.
      Would contradict CR252 PASS.
  F5  WC-1 or WC-2 unexpectedly succeed: any perturbation produces
      mean abs_rel_delta < 1e-4 (formula not sensitive to R or D).
      Would conflict with CR005 audit.
  F6  Runner crashes or audit incomplete.
```

## Falsifiers

```text
F-NON-EXTENSION   Formula matches derivation set (q ∈ {1,2,3,4})
                  exactly but fails extension set systematically:
                  the 4-point derivation was coincidence, not a
                  structural identity.

F-PAIR-NON-UNITY  Pair-shape (n_conn=1) cohort shows median
                  ratio ≠ 1.0: the first-connection-free
                  principle is wrong; pair shapes also carry a
                  connection fee.

F-WRONG-D-OR-R    WC-1/WC-2 perturbations succeed without
                  collapsing exact_match rate: R and D are not
                  load-bearing in the formula, contradicting
                  the substrate-atom basis claim.

F-CATALOG-BROKEN  Single-atom rows violate M_observed = M_native:
                  the catalog itself has inconsistencies that
                  invalidate the entire reveal. Would also
                  invalidate CR252.
```

## Outputs

```text
   CR009_PRECOMMIT.md           this file
   CR009_runner.py              Python K1 reveal engine
   CR009_per_row_reveal.csv     per-row formula application + classification
   CR009_aggregate.csv          per-cohort breakdown
   CR009_wrong_controls.csv     WC-1 through WC-5 results
   CR009_summary.json           verdict + V-1..V-7 + per-cohort summary
   CR009_result.md              verdict markdown
   HASHES.txt                   SHA-256 of all CR009 artifacts
```

## Cryptographic chain (inputs)

```text
   Catalog source:
   c:\VS\The_Courtroom\09a_PARTICLE_MASS_CHAIN\
     CR252_PARTICLE_CATALOG_SPINE_REFRESH\CR252_particle_catalog_v2.csv
     sha256 = 3da53e012b09cc3df83abbddd5fdad36bf89e94c85739642237ec75a4e143cf6

   Provenance backing:
   c:\VS\The_Courtroom\18_SAM_NATIVE_QC\CR005_M_NATIVE_PROVENANCE_AUDIT\
     CR005_summary.json (PASS verdict)

   Substrate atoms used in the locked formula (read-only):
   R = 12 (CR238 atom)
   D = 3 (CR238 atom)

   Derivation reference (the 4-point cascade derivation that
   produced the formula):
   c:\VS\The_Courtroom\18_SAM_NATIVE_QC\QGC_SESSION_MEMO_2026_06_24.md §3.3
   c:\VS\The_Courtroom\18_SAM_NATIVE_QC\QGC_offset_q_table.csv
```

## Sealed

Sean Brady, 2026-06-24. The formula, the classification taxonomy,
the derivation-vs-extension set partition, V-1 through V-7,
wrong controls WC-1 through WC-5, verdict gates P/B/F, and
falsifiers are locked above the line. The runner's per-row
reveal across the full 321-row catalog is the test. The verdict
is what the catalog says, not what was hoped for.

**Pre-runner tolerance refinement (2026-06-24):** Initial draft
used 1e-9 exact threshold and 100% derivation-set match requirement
with median pair-cohort metric. Sean flagged that 1e-9 is below the
CSV's decimal-string precision floor (test rigged to fail), and
that median ignores distribution shape. Refined to: factor-of-10
ladder (exact 1e-5, close 1e-4, approximate 1e-3, miss ≥ 1e-3),
mean-based cohort verdicts (not single-row), and 10×-looser
extension tolerance (1e-4) vs derivation (1e-5). Pre-runner
refinement; no measurements taken under prior thresholds.
