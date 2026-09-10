# CR212 - Fano Plates Open Readings Promotion Scan

Result: **CR212_PASS_SCOPED_PROMOTION_ELIGIBILITY_AUDIT__OPEN_6_REPLAY_GRADE_BACKED__OPEN_4_RETIRED_FALSIFIED__OPEN_1_2_3_5_NOT_PROMOTABLE**

Verdict: **PASS_SCOPED_AUDIT**.

CR212 is a scoped Courtroom audit. It scores each of the six OPEN
readings carried over from CR210 / CR211 against five candidate corpora
(priority-record G-tests, QP corpus, SUK gate lineage, QGA references,
Courtroom sealed closures). CR212 does **not** promote any reading on
its own. It identifies which OPEN readings have enough sealed backing
to be promoted to Courtroom-grade in a future test, and which do not.

## Question

Of the six OPEN HH001 / Fano-plate readings still untested at
Courtroom-grade, which can be promoted from existing data already sealed
inside the Courtroom or its upstream G / SUK / QGA / QP corpora?

## Per-reading verdicts

```text
OPEN_1  MATTER  (atomic weight 126 rows)        NOT_PROMOTABLE_FROM_EXISTING_DATA
OPEN_2  CLOCK   (stability flag 126 rows)        NOT_PROMOTABLE_FROM_EXISTING_DATA
OPEN_3  LIGHT   (wavelength 126 rows)            NOT_PROMOTABLE_FROM_EXISTING_DATA
OPEN_4  ACTION  (nuclear spin 126 rows)          RETIRED_FALSIFIED (1/102 upstream)
OPEN_5  seven-channel Fano position mapping     NOT_PROMOTABLE_FROM_EXISTING_DATA
OPEN_6  126 GeV conversion                      REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND
```

Verdict counts:

```text
COURTROOM_NATIVE_BACKED            0
REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND 1   (OPEN_6, backed by LC02 with LC01 lock)
NOT_PROMOTABLE_FROM_EXISTING_DATA   4   (OPEN_1, OPEN_2, OPEN_3, OPEN_5)
RETIRED_FALSIFIED                   1   (OPEN_4, HH001 1/102 self-falsified)
```

## Backed by Courtroom: OPEN_6 only (replay grade)

OPEN_6 (126 GeV conversion) is the single OPEN reading with a sealed
Courtroom backing:

```text
LC02 replays H_native = R^2 * (1 - 2^-D) = 144 * 7/8 = 126 from the
LC01-locked primitive stack {alpha_H, R, D, split fraction}. It further
replays H_reveal = H_native - D^2/R = 126 - 9/12 = 501/4 = 125.25.
LC02 rejects 13/13 wrong controls including D=2, D=4, R=10, R=24.

However, LC02 carries the CR120 target-visibility caveat: the Higgs
mass was known when the closure was authored. The reading is therefore
REPLAY-grade from locked primitives, not forward-blind.
```

Promotion eligibility for OPEN_6:

```text
- Numerically backed at Courtroom-grade (LC02 replay).
- Chronologically gated (CR120 target-visibility).
- Eligible for "replay-from-locked-primitives" promotion only.
- NOT eligible to be cited as a forward-blind prediction.
```

## Not promotable: OPEN_1, OPEN_2, OPEN_3, OPEN_5

For these four readings the audit's empirical corpus scan returned no
backing material in any of the five corpora:

```text
OPEN_1 MATTER:
  - Priority-record domain-specific term hits: 0
  - Operational memory hits: 0
  - QP corpus files-with-any-hit: 0 of 144
  - No SAM-native 126-row atomic-weight derivation anywhere.
  - LC05 uses IAEA roster as downstream comparator only.

OPEN_2 CLOCK:
  - Generic "stable" hits are abundant but not domain-specific.
  - No 126-row clock / stability law derivation.
  - LC05 K1 roster Z=1..96 with comparator-only flags; CR070 noted
    Tc/Pm holes per CR211.

OPEN_3 LIGHT:
  - QP corpus files-with-any-hit: 1 of 144 (single incidental match).
  - No SAM atomic-spectroscopy lane.

OPEN_5 seven-channel physical mapping:
  - Priority-record domain-specific term hits: 0
  - QP corpus files-with-any-hit: 0 of 144
  - Fano F_2^3 address algebra IS sealed (CR113/114/115/116), but the
    PARTICLE/MATTER/ELEMENT/GRAVITY/CLOCK/LIGHT/ACTION position
    assignment is a structural reading proposal, not a derived theorem.
```

These four readings remain in the Fano_Plates audit register as
NOT_PROMOTABLE_FROM_EXISTING_DATA, meaning: a future CR-class test
would need to derive (not import) the relevant data from SAM primitives
before promotion can be considered.

## Retired: OPEN_4

```text
OPEN_4 ACTION column (nuclear spin):
  - HH001 directly falsified ACTION-residual = physical nuclear spin
    at 1 of 102 matches (below chance).
  - CR210 and CR211 preserve the falsification.
  - No corpus rescues the reading.
  - Status: RETIRED_FALSIFIED.
```

## Corpora inventory (empirical)

```text
CORPUS_A   priority-record G-test token hits     1700+
CORPUS_B   QP corpus files                       144 (qp001..qp094)
CORPUS_C   SUK gate lineage files                qp071, qp073
CORPUS_D   QGA references                        searched in PR
CORPUS_E   Courtroom sealed closures             10 anchor closures
            (CR113, CR114, CR115, CR116, CR119,
             LC01, LC02, LC04, LC05, LC06)
```

Full per-reading per-corpus hit counts are in
`CR212_corpus_scan_per_reading.csv`.

## Wrong controls

8/8 rejected. Notable:

- WC1 (absence-of-evidence as derivation): rejected by explicit
  NOT_PROMOTABLE_FROM_EXISTING_DATA verdict vocabulary.
- WC2 (LC02 as forward-blind reveal): rejected by REPLAY_GRADE_ONLY
  on OPEN_6 with CR120 caveat preserved.
- WC6 (CR210/CR211 modified): rejected by branch write-isolation
  (Fano_Plates only).
- WC7 (new theorem sealed from scan): rejected by SCOPED_AUDIT
  claim-grade declaration.

## Checks

17/17 PASS.

## Boundary preserved

- CR210 verdict unchanged.
- CR211 verdict unchanged.
- LC01 primitive stack unchanged.
- LC02 Higgs replay unchanged.
- LC05 periodic vault replay unchanged.
- No new theorem sealed.
- No OPEN reading promoted by this test.

## Primary artifacts

- `Fano_Plates/CR212_FANO_PLATES_OPEN_READINGS_PROMOTION_SCAN/CR212_input_manifest.csv`
- `Fano_Plates/CR212_FANO_PLATES_OPEN_READINGS_PROMOTION_SCAN/CR212_open_readings.csv`
- `Fano_Plates/CR212_FANO_PLATES_OPEN_READINGS_PROMOTION_SCAN/CR212_corpus_inventory.csv`
- `Fano_Plates/CR212_FANO_PLATES_OPEN_READINGS_PROMOTION_SCAN/CR212_corpus_scan_per_reading.csv`
- `Fano_Plates/CR212_FANO_PLATES_OPEN_READINGS_PROMOTION_SCAN/CR212_promotion_scan.csv`
- `Fano_Plates/CR212_FANO_PLATES_OPEN_READINGS_PROMOTION_SCAN/CR212_wrong_controls.csv`
- `Fano_Plates/CR212_FANO_PLATES_OPEN_READINGS_PROMOTION_SCAN/CR212_checks.csv`
- `Fano_Plates/CR212_FANO_PLATES_OPEN_READINGS_PROMOTION_SCAN/CR212_summary.json`
- `Fano_Plates/CR212_FANO_PLATES_OPEN_READINGS_PROMOTION_SCAN/HASHES.txt`
