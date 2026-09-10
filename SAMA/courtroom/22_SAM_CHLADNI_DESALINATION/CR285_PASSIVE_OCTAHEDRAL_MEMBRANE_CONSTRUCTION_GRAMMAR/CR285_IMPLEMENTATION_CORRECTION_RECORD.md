# CR285 Implementation Correction Record

## Initial Run

The first Courtroom execution on `2026-07-15T03:19:30Z` returned:

```text
CR285_FAIL_PASSIVE_MEMBRANE_CONSTRUCTION_GRAMMAR
checks = 34/35
sources = 17/17
directed gates = 960
undirected pairs = 480
```

The only failed check was `C23`, which preserves CR120U's source-level split
between 107 matter-row-allowed templates and 13 surface-rejected templates.

## Cause

`CR120U_CELL_TEMPLATES.csv` encodes `source_matter_row_allowed` as `yes/no`.
The CR285 runner expected `true/false`, so it misreported the already-loaded
120 templates as `0/120` even though every source row and hash was correct.

## Correction

The parser now reads the source's exact `yes/no` vocabulary. No source,
precommit, topology, gate pairing, compatibility rule, acoustic shelf rule,
wrong control, physical boundary, or expected verdict was changed.

## Status Meaning

This was an implementation schema defect, not a failed passive topology and
not a scientific appeal. The original failure is preserved here rather than
silently overwritten by the corrected execution.
