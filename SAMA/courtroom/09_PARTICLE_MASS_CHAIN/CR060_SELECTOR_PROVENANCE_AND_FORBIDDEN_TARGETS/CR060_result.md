# CR060 Selector Provenance and Forbidden Targets

## Verdict

```text
CR060_BOUNDARY_SELECTOR_PROVENANCE_AND_FORBIDDEN_TARGETS_VERIFIED
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = BOUNDARY
triage_bin = B
```

## Reason

```text
selector provenance and forbidden-targets boundary verified clean; no external anchor at this CR
```

## Phase Summary

```text
Phase 1 manifest seal + hash      seal_exists=True  sha_matches=True  verified=572
Phase 2 QP self-disclosure        clean=24/24  violations=0
Phase 3 provenance boards         boards=2  violations=0
Phase 4 hostile audit             files=15  verdicts={'PASS': 7, 'BOUNDARY': 8}
Phase 5 forbidden selector scan   engine_hits=0  doc_mentions=0  clean=4
Phase 6 wrong control injections  passed=6/6
```

## Rule-9 Line

```text
This test could have falsified: the claim that every selector in the
particle mass chain has a provenance trace independent of measured
particle masses, fitted Yukawa couplings, and post-observation
calibration loops, and that the hostile QP010-QP021 audit confirms
this independence.
```

## Courtroom Reading

CR060 is the selector-provenance gate for the 09 branch. A BOUNDARY
verdict is the expected default: the test structurally certifies that
selectors trace back to declared SAM-native quantities with no forbidden
construction pattern, and that the hostile audit confirms this. The K1
external anchor still belongs to CR062 row-by-row ledger.

## Artifacts

- `CR060_input_manifest.csv`
- `CR060_qp_self_disclosure_check.csv`
- `CR060_provenance_board_check.csv`
- `CR060_hostile_audit_replay_check.csv`
- `CR060_forbidden_selector_scan.csv`
- `CR060_manifest_seal_check.json`
- `CR060_wrong_controls.csv`
- `CR060_summary.json`
- `HASHES.txt`
