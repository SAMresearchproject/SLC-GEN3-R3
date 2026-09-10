# CR004 Restore Record - 2026-07-03

Status: post-restoration documentation sidecar. This file is not part of the
original CR004 sealed artifact set and is not listed in the original
`HASHES.txt` ledger.

Preflight:

- `artifacts/preflight_filled/PREFLIGHT_20260703_134744_no_script.md`
- Task: `restore all CR004 files to original sealed hash-ledger state and document restoration`
- Classification: constructive new work

## Restoration Request

The requested action was to restore everything in
`18_SAM_NATIVE_QC/CR004_QGC_PHASE2_DISTANCE_COUPLING` to the original CR004
sealed hash-ledger state and document both the restoration and the discovered
changes.

## Source States

Original CR004 source state:

- Commit: `1929d0c`
- Commit label: `062426`
- Role: original CR004 state matching the CR004 `HASHES.txt` ledger.

Later changed state:

- Commit: `16cd7bd`
- Commit label: `062526`
- Role: later edit that changed three CR004 files but did not update
  `HASHES.txt`.

## Files Changed By 16cd7bd

The later `062526` commit touched exactly three CR004 files:

```text
CR004_PRECOMMIT.md    2-line diff surface
CR004_runner.py       8-line diff surface
CR004_summary.json    4-line diff surface
```

The changed content was limited to title/string metadata and UTF-8 BOM
introduction:

- `CR004_PRECOMMIT.md`
  - removed the original no-BOM opening byte state;
  - changed the H1 title from `QGC Phase 2` to `SLC Phase 2`.

- `CR004_runner.py`
  - removed the original no-BOM opening byte state;
  - changed the top docstring title from `QGC Phase 2` to `SLC Phase 2`;
  - changed the runtime print title from `QGC Phase 2` to `SLC Phase 2`;
  - changed the emitted summary title from `QGC Phase 2` to `SLC Phase 2`.

- `CR004_summary.json`
  - removed the original no-BOM opening byte state;
  - changed the JSON `title` value from `QGC Phase 2` to `SLC Phase 2`.

No evidence was found that the CR004 distance law, d_ref declaration, distance
sweep rows, wrong controls, or verdict were changed by `16cd7bd`.

The controlling d_ref lines remained part of the original CR004 precommit:

```text
where d_ref = unit spacing (chosen = 1)
d(X, Y) = distance between sites X and Y (in d_ref units)
d(X, X) = d_ref
```

## Restoration Performed

The CR004 directory was restored from the original `1929d0c` state.

Restoration detail:

- `CR004_PRECOMMIT.md` restored to the original no-BOM `QGC Phase 2` title
  state and hash-ledger byte form.
- `CR004_runner.py` restored to the original no-BOM `QGC Phase 2` title/string
  state and hash-ledger byte form.
- `CR004_summary.json` restored to the original `QGC Phase 2` title state and
  then line-ending matched to the hash-ledger byte form.
- Files that already matched the CR004 ledger remained matching.

Line-ending note:

- `CR004_PRECOMMIT.md` and `CR004_runner.py` match the ledger in LF/no-BOM byte
  form.
- `CR004_summary.json` matches the ledger in CRLF/no-BOM byte form.
- Future Git checkout or edit operations with automatic line-ending conversion
  can change these hashes again if the files are touched without preserving the
  ledger byte form.

## Verification After Restore

All CR004 `HASHES.txt` rows matched after restoration:

```text
CR004_distance_sweep.csv FD83413915FBC2ACD61D1DDD4AE657A1419681891A32A385C09CA80BB687F197 MATCH
CR004_per_step_trace.csv C0B3FCF1CFC9DFEF4F0AF72E662D43253E717B0069C0794060904F170A9FDBE5 MATCH
CR004_PRECOMMIT.md       5D565D113F6F8897D8173F99D54AEBEAF3E933655B85EE2D4F88F1AB3E6E833C MATCH
CR004_result.md          5D5D1153D8B1B9074B13274A474FABCA6AC14F57ABBFD445EB9B5B093F6DF33E MATCH
CR004_runner.py          3A25C2FFB8E5B47CCFEC4FCB9AB83FFED6D6BBA466BBA10C40DEFE435B825CBE MATCH
CR004_summary.json       50729C67EDECB00F646739513FE9F42E180487ACB1B49F5439F721A4BED30ADA MATCH
CR004_wrong_controls.csv 285A1317ED3C236BE3C9667E6F07F6970CB77818A36C5758956D701ABD4DC4E5 MATCH
```

No result-producing script was run for this restoration. This was a source
restore and hash-ledger hygiene action.

## Record Effect

CR004 is restored to its original sealed hash-ledger state for every file listed
in `HASHES.txt`.

The restored tracked diff against current `HEAD` is the inverse of the later
`062526` metadata edit: `SLC` title strings return to `QGC`, and the BOM added
by the later edit is removed.

This restoration does not create new CR004 result evidence. It restores the
original CR004 artifact bytes and documents that the later change was a metadata
and encoding drift, not a change to the d_ref source line or the tested kernel.
