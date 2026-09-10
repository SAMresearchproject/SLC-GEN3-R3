# CR212a Precommit

Task: regrade the CR212 audit verdicts for OPEN_1, OPEN_2, OPEN_3, OPEN_4,
OPEN_5, OPEN_6 against the actual construction of the HH001 SIS table.

The HH001 builder (`HH001_build_sis_table.py` lines 235-280) iterates
over CR119's 126-row periodic table and computes:

```text
PARTICLE = proton_count + electron_count + neutron_count_primary    (SAM)
ELEMENT  = Z                                                        (SAM)
GRAVITY  = qA_total_primary                                         (SAM)
MATTER   = ATOMIC_MASS[Z] lookup or '-' for frontier                (comparator)
CLOCK    = clock_value(Z) rule or '-' for frontier                  (comparator)
LIGHT    = LIGHT_NM[Z] lookup or '-' for frontier                   (comparator)
ACTION   = NUCLEAR_SPIN[Z] lookup or '-' for frontier               (comparator)
```

Frontier Z=119-126 explicitly emit '-' for the four comparator columns,
so no value is fabricated outside the comparator range.

The scaffold is SAM-derived. The comparator columns sit on top of that
SAM-derived scaffold. CR212's "REFERENCE_NOT_COURTROOM_DATA" scoring
missed this distinction. CR212a corrects it by introducing a new
verdict tier `SAM_SCAFFOLD_PLACEMENT_GRADE` and applying it where
appropriate.

## Pass condition

```text
- REPLACEMENT_RECORD references the original CR212 verdict verbatim.
- CR212 artifacts remain unmodified on disk and re-hash to the values
  sealed in HASHES.txt of CR212.
- The HH001 builder script is hashed and the SAM-scaffold path is
  reproduced verbatim in the regrade table.
- Every regraded verdict comes from the expanded vocabulary:
    COURTROOM_NATIVE_BACKED
    REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND
    SAM_SCAFFOLD_PLACEMENT_GRADE        (new in CR212a)
    NOT_PROMOTABLE_FROM_EXISTING_DATA
    RETIRED_FALSIFIED
- The four CR212 sealed wrong controls relevant to this regrade
  remain rejected.
- No new theorem is sealed by this test.
- 17_HAUNTED_HOUSE_INTAKE artifacts remain read-only.
```

## Wrong controls (regrade-specific)

```text
WC1a  treating SAM_SCAFFOLD_PLACEMENT_GRADE as forward-blind derivation
WC2a  rewriting CR212 verdicts in place (rather than recording a regrade)
WC3a  promoting OPEN_4 ACTION-spin above RETIRED_FALSIFIED
WC4a  collapsing the comparator distinction (lookup-value vs derived-value)
WC5a  treating the seven-channel labeling as closed because the scaffold is SAM
WC6a  inheriting CR212's NOT_PROMOTABLE for OPEN_1/2/3 after the SAM-scaffold
       construction has been documented
```

## Source citation rule

The regrade must cite, for each regraded reading, the specific HH001
builder line range that shows the SAM-scaffold construction PLUS the
specific CR119 column it reads from. No corpus-level hand-waving.
