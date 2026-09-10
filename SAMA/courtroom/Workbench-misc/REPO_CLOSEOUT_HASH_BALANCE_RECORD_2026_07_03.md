# REPO CLOSEOUT HASH BALANCE RECORD - 2026-07-03

## Preflight

Task:

`repo closeout balance repair efforts against test result integrity and apply minimal closeout fixes`

Preflight artifacts:

- `artifacts/preflight_filled/PREFLIGHT_20260703_140941_no_script.md`
- `artifacts/preflight_filled/PREFLIGHT_20260703_140941_no_script.json`

Preflight class: `CONSTRUCTIVE_NEW_WORK`

Approval status: not required by the preflight classification.

## Closeout Principle

The correct closeout balance is result integrity first, operating hash discipline second, and stale-document cleanup only where it protects those two things.

For this closeout, that means:

1. Repair the live root operating hash spine when the current file bytes are the controlling state.
2. Restore sealed result artifacts to their original ledger bytes when a later process changed them without rehashing.
3. Preserve the audit and repair records that document the failure chain and the recovery.
4. Do not chase stale, historical, first-run, reference, external-path, or living-document rows unless they threaten the controlling result chain.
5. Do not run new SAM result-producing scripts as part of closeout hygiene.

This record does not erase the prior operational failures. It documents the balance chosen after repair: fix the controlling integrity chain, preserve the failure audits, and avoid over-mutating the repository during closeout.

## Repairs Applied

### Root Operating Hash Spine

Root `HASHES.txt` was updated for five live operating files whose current bytes are the accepted current state:

- `./SAM_NATIVE_ACTION_ENGINE_V4_2.md`
- `./SAM_NATIVE_MASTER_FORMULA_V4_2.md`
- `./SAM_TESTING_RULES.md`
- `./SAM_TEST_PREFLIGHT.md`
- `./tools/run_sam_test.py`

The following root rows already matched and were left unchanged:

- `./INSTALL_V4_2_PREFLIGHT_LOCK.md`
- `./STEWARDSHIP_DECLARATION.md`
- `./docs/RESULT_SCRIPT_GUARD_SNIPPET.py`

Verification after the edit: root `HASHES.txt` is `8/8 OK`.

### Sealed Branch 18 Result Artifacts

The QGC-to-SLC rename had been applied to sealed files without rehashing. That was not compatible with the sealed-artifact concept.

The affected sealed files in these Branch 18 CR folders were restored to the pre-rename byte state required by their local ledgers:

- `18_SAM_NATIVE_QC/CR001_QGC_PHASE1_SUBSTRATE_GATE_INVOLUTION`
- `18_SAM_NATIVE_QC/CR002_T2_PRESCREENING_AND_K1_ENVELOPE`
- `18_SAM_NATIVE_QC/CR003_QGC_PHASE2_JOINT_FIGURE_CORRELATION`
- `18_SAM_NATIVE_QC/CR004_QGC_PHASE2_DISTANCE_COUPLING`
- `18_SAM_NATIVE_QC/CR005_M_NATIVE_PROVENANCE_AUDIT`
- `18_SAM_NATIVE_QC/CR009_CONNECTION_FEE_K1_REVEAL`

Where local ledgers required CRLF/no-BOM byte form for summary JSON files, that byte form was restored as part of the repair.

Verification after the restore:

| Folder | Rows | Bad | Missing | Status |
| --- | ---: | ---: | ---: | --- |
| `CR001_QGC_PHASE1_SUBSTRATE_GATE_INVOLUTION` | 6 | 0 | 0 | OK |
| `CR002_T2_PRESCREENING_AND_K1_ENVELOPE` | 5 | 0 | 0 | OK |
| `CR003_QGC_PHASE2_JOINT_FIGURE_CORRELATION` | 6 | 0 | 0 | OK |
| `CR004_QGC_PHASE2_DISTANCE_COUPLING` | 7 | 0 | 0 | OK |
| `CR005_M_NATIVE_PROVENANCE_AUDIT` | 9 | 0 | 0 | OK |
| `CR009_CONNECTION_FEE_K1_REVEAL` | 7 | 0 | 0 | OK |

## Repo-Wide Sweep Interpretation

The read-only repo sweep found:

- Ledgers scanned: `432`
- Parsed rows: `2621`
- OK rows: `2408`
- Mismatches: `34`
- Missing rows: `179`

The closeout interpretation is:

- Root operating mismatches were repaired.
- Sealed Branch 18 result mismatches caused by the QGC-to-SLC cleanroom rename were repaired by restoration, not rehashing.
- Remaining mismatches are treated as non-closeout-blocking unless later tied to a controlling result chain.

Known remaining non-blocking classes include:

- Stale reference or README ledgers.
- Historical first-run or failure ledgers.
- Living/reference documents whose current bytes no longer match old local rows.
- CR013 W5 expectations affected by the CR004 restoration.
- Prior verifier/template rows that are not the controlling current result chain.
- Missing rows from moved, external, or legacy path references.

## Grade

Sealed test-result integrity: `A- / GREEN`.

Reason: the damaged sealed Branch 18 CR folders were restored to ledger-matching byte state; no new result-producing SAM scripts were run as part of this repair. The minus is for the prior unauthorized mutation history, not for the current restored state.

Root operating hash spine: `A / GREEN`.

Reason: root `HASHES.txt` now verifies `8/8 OK` against current root operating files.

Line-ending caution: Git reports that `HASHES.txt` currently has LF line endings in the working copy and may be converted to CRLF the next time Git touches it. This is not a current hash-row failure, but future hash-sensitive edits should use byte-preserving handling, such as `core.autocrlf=false`, where sealed or sidecar hashes are involved.

Closeout hash hygiene outside root files and sealed test results: `B- / YELLOW`.

Reason: stale, historic, moved, and reference-document rows still exist, but they are not currently controlling the result chain. Chasing all of them during closeout would create more mutation risk than value.

Overall closeout posture: `B+ / CLOSEOUT-ADEQUATE`.

Reason: the controlling result chain and root operating spine are repaired and documented. Remaining drift should be treated as archival/reference hygiene, not as a reason to reopen or downgrade the sealed test-result corpus.

## Non-Goals Preserved

This closeout record did not:

- Rehash sealed result files to bless changed text.
- Convert cleanroom edits into accepted historical substitutions.
- Rerun SAM result-producing scripts.
- Downgrade CR004 or `d_ref_norm=1` on the basis of the malformed CR013 cleanroom package.
- Chase every stale ledger row in the repository.

## Closeout Statement

The balanced repair position is:

The restored sealed CR files, root hash spine repair, and documented failure audits are enough to close the integrity emergency. Further cleanup should be handled only as targeted archival hygiene, not as another broad mutation process.
