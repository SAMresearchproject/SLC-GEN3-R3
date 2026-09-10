# CR120P Precommit

## Record

- Test ID: `CR120P_P9_G0_UPDATED_SHEET_BINDING_IMPROVEMENT_POTENTIAL`
- Task: `Assess binding improvement potential of latest spreadsheets after p9 g0 value removal`
- Class: constructive new work
- Preflight: `artifacts/preflight_filled/PREFLIGHT_20260714_043602_no_script.md`
- Frozen source manifest: `CR120P_SOURCE_MANIFEST.csv`
- Frozen source-manifest SHA256: `b4d45761c1fc120f57c595184e25573158e53bdb49af1603f01c866f82b3c12d`

## Question

Do either of the two live updated spreadsheet assemblies have a source-backed mechanism with the potential to improve nuclear-binding construction when the values assigned to the `[p=9,g=0]` rows are removed?

This test discriminates **binding-improvement potential** from **already measured binding-fit improvement**. It does not refit a binding model and will not report a lower binding residual unless a future separately precommitted holdout test measures one.

## Frozen candidate

The only allowed `[p=9,g=0]` removal candidate is the executed five-row CR120K relation:

`[p=9,g=0] = [p=8,g=0] + [p=1,g=0]`

for exactly:

- `QP093A-0019`
- `QP093A-0020`
- `QP093A-0021`
- `QP093A-0085`
- `QP093A-0086`

The executed CR120K derivation must show exact `M_native` additivity, zero residual, passing type checks, and the prior W8/X1/W9 provenance for all five rows. No other partition, depth, row family, or selection rule may be removed under this candidate.

## Spreadsheet gates

All arithmetic is performed on `M_native` **sums**, not means.

### Assembly A: 100-row workbook

Pass the complete-removal gate only if the hash-matched current extraction:

1. has 100 unique rows;
2. has `sum(M_native) = 16200` exactly;
3. contains zero of the five CR120K `[p=9,g=0]` candidates; and
4. retains all ten declared `[p=8,g=0]` and `[p=1,g=0]` parent rows from the five executed derivations.

Its duplicate-prevention amount is the exact five-row sum `50.625`. A passing gate supports the statement that this assembly prevents the five W9 rows from being counted as independent linear `M_native` inventory in addition to their W8 and X1 parents.

### Assembly B: 81-row workbook

The current saved 81-row assembly is evaluated independently. Pass the same complete-removal gate only if it contains none of the five CR120K rows. If it retains any, report their exact IDs, sign counts, and `M_native` sum. Also compute the exact set contraction from the 100-row roster:

- 100-only removal packet: row count, `M_native` sum, and positive/negative/neutral counts and sums;
- 81-only insertion packet: the same quantities; and
- net sum change.

Charge/conjugacy balance is reported as a distinct signed-contraction fact and must not be relabeled as complete `[p=9,g=0]` removal.

## Binding-potential gates

The candidate has **binding-improvement potential** only if all of the following are true:

1. **Source-backed dependency:** all five CR120K rows pass exact additivity and type checks under the frozen W8/X1/W9 provenance.
2. **Complete live implementation:** at least one current spreadsheet assembly implements the complete five-row removal while retaining all declared parents.
3. **Double-count mechanism:** the implemented removal changes only independent linear-inventory accounting; the five source identities remain available through the frozen derivation/provenance record.
4. **Binding interface exists:** the frozen binding sources contain isotope-varying binding rows and a frozen train/holdout or observed-panel evaluation surface, while CR276 contains particle-role rows for all five candidate IDs.
5. **No automatic-fit claim:** the binding sources do not already contain a per-isotope occupancy/multiplicity map assigning the removed five rows to binding features. If that map is absent, measured improvement must be `NOT_YET_TESTED`.

Passing these gates yields `YES_POTENTIAL` for the qualifying assembly: removing a proven dependent linear contribution can prevent double counting and leaves a separately testable residual/interaction channel. It does not yield a measured residual improvement.

## Wrong controls

1. **Mean substitution:** replacing roster sums with means is forbidden and fails.
2. **Global-total predictor:** inserting `16200`, `12600`, `50.625`, or their difference as the same constant for every isotope is not an independent binding feature. CR242 must have an all-one intercept column; the runner must show the proposed global-total column is an exact scalar multiple of that intercept.
3. **Five-row deletion without parent retention:** fails the dependency implementation gate.
4. **Any-depth p9 deletion:** fails; only the five `[p=9,g=0]` candidates are admissible.
5. **Identity erasure:** fails; the candidate removes independent `M_native` value counting, not provenance or identity rows from the source record.
6. **Retrofitted fit claim:** fails; no binding coefficient, holdout partition, operator gate, isotope choice, or threshold may be tuned in this test.
7. **81-row relabeling:** if the current 81-row workbook retains any of the five rows, it cannot pass as the same complete `[p=9,g=0]` removal even if its separate signed-removal packet is balanced.

## Fixed outputs

- `CR120P_sheet_assessment.csv`
- `CR120P_p9_g0_rows.csv`
- `CR120P_roster_delta.csv`
- `CR120P_binding_interface.json`
- `CR120P_wrong_controls.json`
- `CR120P_summary.json`
- `CR120P_result.md`
- `HASHES.txt`

## Verdict grammar

- Assembly A: `YES_POTENTIAL`, `NO_POTENTIAL`, or `INVALID_SOURCE`
- Assembly B complete-removal mechanism: `YES_POTENTIAL`, `NO_SAME_MECHANISM_AS_SAVED`, or `INVALID_SOURCE`
- Measured binding improvement: `NOT_YET_TESTED` unless a future separately precommitted fit test supplies a holdout result
- Overall pass requires exact source integrity and a determinate classification for both assemblies; it does not require both assemblies to implement the same mechanism.

No runner result was consulted in freezing this precommit.
