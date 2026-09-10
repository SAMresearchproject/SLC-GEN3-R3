# CR013 Existing-Document Mutation Audit

Date: 2026-07-03

Status: audit sidecar. This document records observed in-place modification of
existing documents around the CR013 cleanroom/d_ref chain. It does not run a new
SAM result and does not alter any sealed result artifact.

Preflight:

- `artifacts/preflight_filled/PREFLIGHT_20260703_135211_no_script.md`
- Task: `audit cleanroom process for modifications to existing CR documents`
- Preflight result: blocked pending audit approval
- Approval: user approved same-task audit

## Executive Finding

The CR013 cleanroom package itself mostly added new files, including redacted
copies under `INPUTS_REDACTED/`. Those redacted copies are modified derivatives
by design, but they are new files, not in-place edits to the original source
files.

Post-audit repair update: after this audit was written, the outstanding
`16cd7bd` QGC-to-SLC sealed-file mutations were restored to their original
local hash-ledger states and documented in:

```text
18_SAM_NATIVE_QC/QGC_TO_SLC_SEALED_FILE_RESTORE_RECORD_2026_07_03.md
```

The "Current Hash-Ledger Failures Outside Restored CR004" section below records
the audit-time state before that repair, not the current post-restore state.

However, the wider d_ref / SLC / cleanroom chain did rely on existing CR
documents that had already been modified in place. The key example is CR004:
CR013 recorded W5 source as the later changed `CR004_PRECOMMIT.md` hash
`b7edd0e9...`, not the original CR004 ledger hash `5d565d11...`.

The larger mutation surface is the `062526` commit (`16cd7bd`), which edited
multiple existing Branch 18 CR files in place after their original hash ledgers
were written. Those edits were mostly QGC-to-SLC title/path/string changes and
UTF-8 BOM introduction, but they still broke the core CR rule: sealed artifacts
should not be modified in place. If a naming/status correction is needed, it
should be a sidecar, continuation, correction note, or supersession, not a
mutation of the original sealed artifact bytes.

## Source Classes

This audit separates four classes:

1. Original source files modified in place.
2. New redacted derivative files created by CR013.
3. New same-commit source files used by CR013.
4. Collateral living/reference documents modified during the same July 3 chain.

Only class 1 is a direct violation of immutable sealed-CR artifact discipline.
Class 2 can be valid if clearly marked as derivative. Class 3 weakens cleanroom
source independence. Class 4 may be acceptable for living documents, but not for
sealed CR artifacts.

## CR013 Source Inputs

CR013 declared six source inputs:

```text
W1  CR010_PRECOMMIT.md
W2  CR266_PRECOMMIT.md
W3  CR268_PRECOMMIT.md
W4  CR001_PRECOMMIT.md
W5  CR004_PRECOMMIT.md
W6  SAM_ON_EARTH_v1.md
```

Current source-hash check against CR013 `HASHES.txt`:

```text
W1  CR010_PRECOMMIT.md  expected 3fafa02ce39f85e8f89790c4cf85db2ce5103e9bf21d4c1501a604c271498d05  actual 3fafa02ce39f85e8f89790c4cf85db2ce5103e9bf21d4c1501a604c271498d05  MATCH
W2  CR266_PRECOMMIT.md  expected 2967eec865f95c0b73a966ed5da8b011d0515eccef027fdd2db82862dc7096a2  actual 2967eec865f95c0b73a966ed5da8b011d0515eccef027fdd2db82862dc7096a2  MATCH
W3  CR268_PRECOMMIT.md  expected bbc3c5b863aa6be12d0d7502c59db6834f6c6ea5a0edc7dbc86b648929028423  actual bbc3c5b863aa6be12d0d7502c59db6834f6c6ea5a0edc7dbc86b648929028423  MATCH
W4  CR001_PRECOMMIT.md  expected 8e6cb1975cd7d2084ffbbf2c215472d2ef8042fae18b68e76b74b94dc4281c77  actual 8e6cb1975cd7d2084ffbbf2c215472d2ef8042fae18b68e76b74b94dc4281c77  MATCH
W5  CR004_PRECOMMIT.md  expected b7edd0e934b8e0fc9441df9b1ed13295d4a8073a1c4b1c732cd890ac4b47a350  actual 5d565d113f6f8897d8173f99d54aebeaf3e933655b85ee2d4f88f1ab3e6e833c  MISMATCH AFTER RESTORE
W6  SAM_ON_EARTH_v1.md  expected 7b0f225821e2aea55e02b0868997fa2acd4ee88b4711ab1b1fb161366e1c5137  actual 7b0f225821e2aea55e02b0868997fa2acd4ee88b4711ab1b1fb161366e1c5137  MATCH
```

W5 mismatch is expected after the 2026-07-03 CR004 restoration. CR004 has been
restored to its original sealed hash-ledger state. CR013's W5 source hash now
documents the fact that CR013 consumed the later modified CR004 precommit, not
the original CR004 precommit.

## Directly Observed Existing-CR Mutations

Commit `16cd7bd` (`062526`) modified existing Branch 18 CR files in place:

```text
CR001_QGC_PHASE1_SUBSTRATE_GATE_INVOLUTION/CR001_PRECOMMIT.md
CR001_QGC_PHASE1_SUBSTRATE_GATE_INVOLUTION/CR001_runner.py
CR001_QGC_PHASE1_SUBSTRATE_GATE_INVOLUTION/CR001_summary.json
CR002_T2_PRESCREENING_AND_K1_ENVELOPE/CR002_PRECOMMIT.md
CR002_T2_PRESCREENING_AND_K1_ENVELOPE/CR002_runner.py
CR002_T2_PRESCREENING_AND_K1_ENVELOPE/CR002_summary.json
CR003_QGC_PHASE2_JOINT_FIGURE_CORRELATION/CR003_PRECOMMIT.md
CR003_QGC_PHASE2_JOINT_FIGURE_CORRELATION/CR003_runner.py
CR003_QGC_PHASE2_JOINT_FIGURE_CORRELATION/CR003_summary.json
CR004_QGC_PHASE2_DISTANCE_COUPLING/CR004_PRECOMMIT.md
CR004_QGC_PHASE2_DISTANCE_COUPLING/CR004_runner.py
CR004_QGC_PHASE2_DISTANCE_COUPLING/CR004_summary.json
CR005_M_NATIVE_PROVENANCE_AUDIT/CR005_PRECOMMIT.md
CR009_CONNECTION_FEE_K1_REVEAL/CR009_PRECOMMIT.md
CR009_CONNECTION_FEE_K1_REVEAL/CR009_PRECOMMIT_AMENDMENT.md
CR009_CONNECTION_FEE_K1_REVEAL/CR009_runner.py
```

The diff pattern was not numerical retesting. It was mostly:

- adding a UTF-8 BOM at file start;
- changing `QGC` text/title strings to `SLC`;
- changing references from `QGC_*` files to `SLC_*` files;
- changing emitted runner/summary title strings from `QGC` to `SLC`.

Even though these are metadata/string edits, they are still in-place changes to
sealed CR artifacts. They also broke local hash-ledger verification.

## Current Hash-Ledger Failures Outside Restored CR004

After the 2026-07-03 CR004 restoration, CR004 now verifies against its original
ledger. The following 062526-touched files still fail their local ledgers:

```text
18_SAM_NATIVE_QC/CR001_QGC_PHASE1_SUBSTRATE_GATE_INVOLUTION/CR001_PRECOMMIT.md
  expected 11E6277F58C2E5C24326F21B29EAA434165C57BE4D046CFEC09D29EEF0B2B7F7
  actual   45C2A61093DED568D3A83533D43875A140637019BD0DB98ECDAB61EEBA496171

18_SAM_NATIVE_QC/CR001_QGC_PHASE1_SUBSTRATE_GATE_INVOLUTION/CR001_runner.py
  expected 5F52AA5657185466019A4131B9CE6C8397EB826F10F8231A2C499BDC0418B365
  actual   5D51E772E97FEECE46564B1A70ADD9E441B02D4F27ACB76FF232677626299B7B

18_SAM_NATIVE_QC/CR001_QGC_PHASE1_SUBSTRATE_GATE_INVOLUTION/CR001_summary.json
  expected DF12C779834798DB74A349FF691528CD856A2DE40B7F68F5232849219C2EBEEB
  actual   F5C75C89D826C3E8437A6AE5B94C70E5273C3E2D9F6C4C6C0E77FF1DAECB1C1D

18_SAM_NATIVE_QC/CR002_T2_PRESCREENING_AND_K1_ENVELOPE/CR002_PRECOMMIT.md
  expected 68DC093EEC97B26C03875B9C99791DAD6B0122767936518CCB36934DA11E215B
  actual   4EB855E8C6C782DD01E02327AA19780341302AAC61A2CB35C90672A3727216B5

18_SAM_NATIVE_QC/CR002_T2_PRESCREENING_AND_K1_ENVELOPE/CR002_runner.py
  expected 13185958C9EDCB176ACFE34B64198ECCFFCF28B6DCC1D9F91683CC94B3B495B9
  actual   F03DA7C45BCDAF0624704E6E388D2DD59EDFF54C79037AF3907FA7313229184A

18_SAM_NATIVE_QC/CR002_T2_PRESCREENING_AND_K1_ENVELOPE/CR002_summary.json
  expected 5367A9C4F4B3B78C255E2817CE698017F1EC5B4B2B6664F85DDF68034EF36DEB
  actual   107BC86CFD5E3A2EF39BE7E0A6F441C45DEDB0553D25909369392FD5DD0E6CB5

18_SAM_NATIVE_QC/CR003_QGC_PHASE2_JOINT_FIGURE_CORRELATION/CR003_PRECOMMIT.md
  expected F4FBF4022425D719A9994DA46A98EEC5D89085809BB9CCD3C9D5E6ACCC56CC28
  actual   5AB9640A3A10960929149BCFF50A68284406DAE65B6BBC0B1C9A67836A93EF72

18_SAM_NATIVE_QC/CR003_QGC_PHASE2_JOINT_FIGURE_CORRELATION/CR003_runner.py
  expected C67996DCB8117D4D7D6ABE9206A90ECF44BCD8D7F401F40034D5D176373C8FC1
  actual   2EB59B4BBC62F8809816119C4779AE63C062E41ED070A01AFB21D6C66C8B54DB

18_SAM_NATIVE_QC/CR003_QGC_PHASE2_JOINT_FIGURE_CORRELATION/CR003_summary.json
  expected 352224CA0FAE2E3A4271743885AD22E2659F7AEF8BD16CB032E7D96C836A3FE6
  actual   56D3C9DD661D9D01EC4C03B5F3D8C6F6FA83EF20892856D26736858240A8510D

18_SAM_NATIVE_QC/CR005_M_NATIVE_PROVENANCE_AUDIT/CR005_PRECOMMIT.md
  expected A4D03264484E16B470FDE9FA205E83D9B3D438E3612888112DA540C2D6CB1BBD
  actual   4B1452D75E4AA301A06D43FBF532FE58A1760C074F6436977B40193920456844

18_SAM_NATIVE_QC/CR009_CONNECTION_FEE_K1_REVEAL/CR009_PRECOMMIT.md
  expected 4A7FCCF97D310B782F7AD63F4E8915B62C93675ABE482449017C1641A29BE3E9
  actual   3806729AD73471368B4E50B68CCB0BA9EC96D76B5B54D496C7C7936075775CBF

18_SAM_NATIVE_QC/CR009_CONNECTION_FEE_K1_REVEAL/CR009_runner.py
  expected 6B2491CFEFF2177584D8C3DF63752839F01434A5C2A4595E3CBD9CB776F6E59B
  actual   EE4AF1F9B3E58EDC6B3C70ECD7C4483FF2FFC51411D36C3BA1FD93CE59A6A175
```

`CR009_PRECOMMIT_AMENDMENT.md` was also modified in `16cd7bd`; it was not found
in its local `HASHES.txt`, so no local-ledger expected hash was available in
this pass.

## CR004 Status

CR004 was restored separately on 2026-07-03 and documented in:

- `18_SAM_NATIVE_QC/CR004_QGC_PHASE2_DISTANCE_COUPLING/CR004_RESTORE_RECORD_2026_07_03.md`

After restore, every original CR004 `HASHES.txt` row verifies. CR004 is no
longer part of the outstanding hash-failure set, but its prior mutation remains
historically relevant because CR013 W5 recorded the later modified `b7edd0e9...`
source hash.

## July 3 CR013 Commits

Commit `923f1aa` (`070326`) created the CR013 cleanroom package and related
chain. Its source-control status shows:

- CR013 cleanroom files: added.
- CR013 redacted inputs W1-W6: added.
- CR010 and `docs/SAM_ON_EARTH_v1.md`: added in the same commit as CR013.
- W2/W3/W4 source files existed from earlier commits and were not modified in
  this commit.
- Existing collateral documents modified in this commit:
  - `09a_PARTICLE_MASS_CHAIN/MATTER_BRANCH_CLOSEOUT.md`
  - `09a_PARTICLE_MASS_CHAIN/MATTER_INDEX.md`
  - `09a_PARTICLE_MASS_CHAIN/MATTER_INDEX_SHA256.txt`
  - `18_SAM_NATIVE_QC/SLC_PATENT_APPLICATION_DRAFT.md`
  - `18_SAM_NATIVE_QC/SLC_PATENT_CLAIM_STRUCTURE.md`

The patent-document edits were substantive downgrade/claim edits tied to
CR-NSC-01 / d_ref non-derivation framing. They are living/reference patent
documents rather than sealed CR result files, but they were still edited in
place rather than preserved as separate amendment sidecars.

Commit `b6a3bc5` (`070326`) added appeal/repair files and preflight artifacts.
No existing source documents were modified by that commit in the checked scope.

## Cleanroom Redacted Copies

The redacted files under `CR013_CLEANROOM_DREF_REDERIVATION/INPUTS_REDACTED/`
are new derivative files. They are not source-file in-place edits.

However, the W5 derivative is materially important because it changed the CR004
d_ref statement from explicit normalized unit convention into a target for the
DERIVER to identify. That is documented separately in:

- `CR013_CHAIN_OF_EVENTS_AND_MELTDOWN_REPORT.md`

This audit treats W5 redaction as a defective derivative, not as an in-place
modification of original CR004. The in-place CR004 mutation came earlier, in
`16cd7bd`.

## Conclusions

1. The cleanroom process did not merely operate on immutable existing files; it
   relied on at least one already-mutated source file, CR004_PRECOMMIT.md.
2. A broader earlier Branch 18 rewrite pass (`16cd7bd`) changed multiple sealed
   CR artifacts in place and left their local hash ledgers stale.
3. CR004 has now been restored to its original ledger state, but CR001, CR002,
   CR003, CR005, and CR009 still show hash-ledger failures for files touched by
   `16cd7bd`.
4. CR013's redacted copies were new files, but W5 redaction altered load-bearing
   meaning and should not be treated as a faithful source-preserving copy.
5. CR013's W1 and W6 source inputs were introduced in the same commit as CR013,
   which weakens the cleanroom claim of being anchored only on independent,
   pre-existing sealed sources.
6. The operating principle should be restored: existing sealed CR documents are
   not edited in place. Corrections should be sidecars, continuation files,
   correction notes, appeal records, or supersession artifacts.

## Recommended Next Actions

1. Restore the remaining `16cd7bd`-modified sealed CR files to their original
   local hash-ledger state, as was already done for CR004.
2. Add per-CR restore records for CR001, CR002, CR003, CR005, and CR009, or one
   branch-level restore ledger that lists every file and hash.
3. Preserve the later QGC-to-SLC naming intent as a sidecar/supersession layer,
   not as mutation of original CR bytes.
4. Mark CR013 W5 source hash as historically pointing at the mutated CR004 state
   and no longer matching current restored CR004.
5. Treat the cleanroom package as context-limited until the source mutation
   chain is fully repaired.
