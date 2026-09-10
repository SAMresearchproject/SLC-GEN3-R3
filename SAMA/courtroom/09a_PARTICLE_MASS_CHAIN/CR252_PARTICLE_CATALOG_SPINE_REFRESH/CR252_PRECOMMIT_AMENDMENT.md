# CR252 Precommit Amendment — V-3 Specification Correction

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Amends:** [CR252_PRECOMMIT.md](CR252_PRECOMMIT.md) V-3, F2
**Filed by:** Sean Brady, 2026-06-24
**Discovered during:** initial CR252 runner execution (first-run FAIL by F2)

---

## What was wrong with the sealed precommit

The sealed precommit's V-3 stated:

> V-3   Matter promotion audit: regen produces exactly 126 rows with
>       matter_row_allowed=yes (the CR119 matter table boundary)

This conflated **two distinct filters**:

1. **qp093a's `matter_row_allowed` column.** Set to `"yes"` at row-construction
   time for stable_matter_rows, antimatter_conjugate_rows, the Higgs
   resonance row, and bound_composite_rows. The 2026-06-15 baseline
   has **286 rows** with `matter_row_allowed=yes`.

2. **CR119's matter table boundary (126 rows).** Produced by a
   **downstream gating layer** (`export_latest_particle_matter_periodic_tables.py`
   in `quantum_phase/src/`) that applies further filtering (matter-gate
   classification + QP093B null-conjugate override + bin restriction)
   on top of qp093a's catalog. CR119 reads this gated 126-row table
   directly; qp093a does not produce it.

These are different counts. The 126 is a downstream artifact; qp093a's
`matter_row_allowed` count is 286. V-3 was wrong to use `=126` as the
expected value against qp093a's column.

## Why this is a precommit error, not a runner / regen failure

The runner's actual regen produced output **bit-identical to the
2026-06-15 baseline** (sha256 `3da53e012b09cc3df83abbddd5fdad36bf89e94c85739642237ec75a4e143cf6`).
Every one of the 321 rows is in `change_class = unchanged`. All key
rows (QP093A-0306 proton, QP093A-0043 Higgs, QP093A-0313 R+1) are
present and structurally identical. WC-1 (determinism), WC-2 (R
load-bearing), WC-3 (key-row stability), WC-4 (carrier non-promotion)
all pass.

The first-run FAIL classification was triggered solely by F2
(`matter_count_v2 != 126`), which depended on a V-3 specification that
asked the wrong question. The regen itself succeeded against the
question CR252 was supposed to answer: did the catalog change since
2026-06-15? No — bit-identical.

## Corrected V-3 and F2

**V-3 (amended):**

> V-3   Matter-allowed count stability: regen produces the same number
>       of rows with `matter_row_allowed=yes` as the 2026-06-15 baseline.
>       This is automatically satisfied if every row is in
>       `change_class = unchanged` (which is the stronger condition the
>       row-by-row diff already verifies). V-3 is therefore a redundant
>       cross-check derived from the row-delta; an explicit baseline
>       count comparison is reported.

**F2 (amended):**

> F2  Matter-allowed count drifts from baseline: if the regen's
>     `matter_row_allowed=yes` count differs from the baseline's
>     count, V-3 fails. (The pre-amendment "≠126" expectation is
>     withdrawn; baseline is 286.)

## What the CR252 scope does NOT include

Re-execution of CR119's downstream gating (`export_latest_particle_matter_periodic_tables.py`)
to confirm the **CR119 matter table** still produces 126 rows after
the qp093a regen is **a separate CR's scope**. CR252's bit-identical
regen result implies CR119's gating, being deterministic, will also
reproduce 126 — but CR252 does not execute that downstream gate. If a
downstream verification CR is needed (e.g., to confirm CR119's intake
also regenerates clean), that's CR253 territory, not CR252.

## Discipline preserved

Per [feedback_old_tests_proof_of_process]: the first-run FAIL artifacts
(`CR252_summary.json` with `verdict_class: "FAIL"`, the row_delta CSV
showing all 321 unchanged, the wrong_controls CSV with all WCs
passing) are **preserved unmodified** by this amendment. The
amendment authorizes the runner re-execution with the corrected V-3
check; the new summary.json supersedes the prior with a pointer back
to the original for audit-trail continuity.

The original sealed precommit's V-3 stays in
[CR252_PRECOMMIT.md](CR252_PRECOMMIT.md) as the recorded spec error.
This amendment is the named correction.

## Authorization

Sean Brady authorized the appeal-as-retest path on 2026-06-24,
explicitly leaving the regrade-vs-retest call to the agent. The
retest path was chosen because:

1. The precommit's own appeal block specifies "A FAIL is not
   appealable — F1-F8 conditions are structural failures that
   require diagnostic work before re-running." Honoring this clause
   means a sealed FAIL stays FAIL; the corrected re-run produces a
   separate verdict on the corrected spec.

2. Stamping the first-run FAIL with a regrade would dilute the
   discipline (any future FAIL becomes appealable for "precommit
   error" reasons). Re-running on a corrected precommit preserves
   the FAIL category as structural.

3. The audit trail is stronger this way: anyone reading the CR252
   directory sees both verdicts and the amendment that bridges them,
   rather than a single regraded FAIL that hides the spec error.

## Sealed

Sean Brady (authorization) + agent (drafting), 2026-06-24.
The V-3 and F2 corrections are locked above the line. The runner
is updated to honor the amended V-3; re-execution proceeds.
