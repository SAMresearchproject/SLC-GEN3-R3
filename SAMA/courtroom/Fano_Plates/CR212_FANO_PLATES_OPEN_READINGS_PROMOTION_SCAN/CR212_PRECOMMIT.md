# CR212 Precommit

Task: scoped Courtroom audit. For each OPEN reading carried over from
CR210 / CR211, score whether any of the candidate Courtroom-side corpora
already contain backing sufficient to promote the reading to
Courtroom-grade.

This is a SCAN, not a promotion. CR212 emits an audit verdict per OPEN
reading. It does not seal any new theorem, and it does not modify any
existing sealed verdict.

## OPEN readings under audit (six)

```text
OPEN_1   MATTER column (atomic weight, 126 rows)
OPEN_2   CLOCK column (stable/radioactive flag, 126 rows)
OPEN_3   LIGHT column (atomic-spectrum wavelength, 126 rows)
OPEN_4   ACTION column (nuclear spin, 126 rows)  [HH001-falsified at 1/102]
OPEN_5   Seven-channel Fano position physical mapping
OPEN_6   126 GeV conversion (H_native = 126 -> Higgs mass)
```

## Candidate corpora (five)

```text
CORPUS_A   priority-record G-tests   (C:\VS\memory\PRIORITY_RECORD.md)
CORPUS_B   QP corpus                 (C:\VS\quantum_phase\src\qp*.py)
CORPUS_C   SUK gate lineage          (qp071 / qp073)
CORPUS_D   QGA references            (priority-record QGA grep)
CORPUS_E   Courtroom sealed closures (CR113/114/115/116, CR119, LC01-LC11)
```

## Pass condition

All of the following must hold for `PASS_SCOPED_PROMOTION_ELIGIBILITY_AUDIT`:

```text
- All input sources resolve and hash without error.
- Six OPEN readings replay verbatim from CR210/CR211 OPEN inventory.
- Five corpora are inventoried with explicit hit-counts for the per-reading
  search terms.
- Per-reading verdicts are emitted from the allowed verdict vocabulary:
  COURTROOM_NATIVE_BACKED
  REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND
  NOT_PROMOTABLE_FROM_EXISTING_DATA
  RETIRED_FALSIFIED
- Wrong controls are rejected.
- No OPEN reading is upgraded to Courtroom-grade inside this test.
```

## Wrong controls

```text
WC1  absence-of-evidence treated as derivation
WC2  LC02 H_native=126 used as forward-blind for Higgs reveal
WC3  HH001 builder embedded reference column treated as Courtroom-native
WC4  ACTION-residual-equals-spin used as supporting evidence after HH001 falsified it
WC5  seven-channel physical mapping declared closed based on Fano algebra alone
WC6  CR210/CR211 verdicts modified from this branch
WC7  any new theorem sealed from this scan
WC8  HH001 promotion claimed without explicit per-reading source citation
```

## Source citation rule

Any reading scored COURTROOM_NATIVE_BACKED or
REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND must cite the specific sealed
artifact path (test ID + file) that backs it. No corpus-level hand-waving.
