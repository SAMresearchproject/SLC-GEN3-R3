# REPLACEMENT_RECORD - CR212 -> CR212a

```text
original_test:   CR212_FANO_PLATES_OPEN_READINGS_PROMOTION_SCAN
original_result: CR212_PASS_SCOPED_PROMOTION_ELIGIBILITY_AUDIT__
                 OPEN_6_REPLAY_GRADE_BACKED__
                 OPEN_4_RETIRED_FALSIFIED__
                 OPEN_1_2_3_5_NOT_PROMOTABLE
regraded_to:     CR212a_PASS_SCOPED_PROMOTION_ELIGIBILITY_REGRADE__
                 SAM_SCAFFOLD_PLACEMENT_GRADE_RECOGNIZED
regrade_date_utc: 2026-06-19
regrade_authority: Sean Brady directive
```

## Reason for regrade

CR212 treated the four HH001 SIS columns
(MATTER / CLOCK / LIGHT / ACTION) as REFERENCE_NOT_COURTROOM_DATA
because their values are loaded from embedded lookup tables in
`HH001_build_sis_table.py`. That scoring missed the actual
construction of the table:

```text
the 126-row scaffold itself comes from CR119 SAM data:
  Z              <- CR119 atomic number  (SAM-derived)
  PARTICLE       <- proton_count + electron_count + neutron_count_primary
                    (CR119 columns; SAM-derived)
  ELEMENT        <- Z                    (SAM-derived)
  GRAVITY        <- qA_total_primary     (CR119 column; SAM-derived)
  (graviton)     <- qA_total_primary / 8 (CR119 column; SAM-derived)
the four observable columns sit on top of that scaffold per row.
```

The HH001 SIS table is therefore a **SAM-scaffolded** table, not an
external reference table. The columns MATTER / CLOCK / LIGHT / ACTION
are comparator observables aligned to the SAM-derived row scaffold,
with frontier Z=119-126 rows explicitly left as '-' so that no value
is fabricated outside the comparator range.

CR212's NOT_PROMOTABLE_FROM_EXISTING_DATA verdicts for OPEN_1, OPEN_2,
OPEN_3, OPEN_5 conflated "the column value comes from a lookup table"
with "the reading has no SAM tie". That conflation is corrected here.

## What changes

CR212a introduces a new verdict tier:

```text
SAM_SCAFFOLD_PLACEMENT_GRADE
    the column value is comparator-aligned per row,
    but the row scaffold itself (Z / PARTICLE / GRAVITY)
    is SAM-derived from CR119.
    Promotable as PLACEMENT grade with scoped boundary:
    the column is a per-row comparator on a SAM-derived scaffold,
    not a forward-blind SAM derivation of the column value.
```

OPEN_1 / OPEN_2 / OPEN_3 are regraded NOT_PROMOTABLE -> SAM_SCAFFOLD_PLACEMENT_GRADE.

OPEN_5 (seven-channel Fano position mapping) is regraded
NOT_PROMOTABLE -> SAM_SCAFFOLD_PLACEMENT_GRADE because the seven
positions are placed on the SAM-derived 18+126 Fano partition
(CR113/CR114/CR115/CR116) and on the SAM-derived row scaffold;
only the physical labeling of each position remains audit-pending,
not the existence of the scaffold.

OPEN_4 (ACTION = physical nuclear spin) remains RETIRED_FALSIFIED
at the physical-spin level (HH001 1/102 self-falsification), but
its column structure inherits the same SAM-scaffold backing for
placement purposes only.

OPEN_6 (126 GeV / Higgs reveal) remains REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND;
the LC02 CR120 target-visibility caveat is unchanged.

## What does not change

```text
- CR210 sealed verdict is preserved.
- CR211 sealed verdict is preserved.
- CR212 sealed verdict is preserved as the empirical-scan record.
- LC02 target-visibility caveat is preserved.
- HH001 1/102 ACTION-spin falsification is preserved.
- Address algebra CR113/114/115/116 closures are unchanged.
- No new theorem is sealed by CR212a.
- The seven-channel physical labeling remains audit-pending
  for a separate CR-class test (not opened here).
```

## Honored falsifiers

The CR212 NOT_PROMOTABLE verdicts for OPEN_1/2/3/5 are NOT erased.
They remain in `Fano_Plates/CR212_*` as the unmodified empirical-scan
record. The regrade adds a new verdict tier on top of that record;
it does not rewrite it. That is the difference between regrade and
suppression.
