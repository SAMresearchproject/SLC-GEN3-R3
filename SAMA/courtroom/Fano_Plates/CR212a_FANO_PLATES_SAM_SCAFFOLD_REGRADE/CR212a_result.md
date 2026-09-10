# CR212a - Fano Plates SAM Scaffold Regrade

Result: **CR212a_PASS_SCOPED_PROMOTION_ELIGIBILITY_REGRADE__SAM_SCAFFOLD_PLACEMENT_GRADE_RECOGNIZED__CR212_EMPIRICAL_SCAN_PRESERVED__OPEN_4_RETIRED_FALSIFIED__OPEN_6_REPLAY_GRADE_ONLY**

Verdict: **PASS_SCOPED_REGRADE**.

## What this regrade does

CR212a corrects a scoring error in CR212. CR212 treated the four HH001
SIS columns MATTER / CLOCK / LIGHT / ACTION as
`NOT_PROMOTABLE_FROM_EXISTING_DATA` because their values come from
embedded lookup tables. That scoring missed that the HH001 builder
constructs each row directly from CR119's 126-row SAM-derived
periodic table:

```text
HH001_build_sis_table.py:235-279
  for el in CR119 rows:
      Z         = int(el["Z"])                              # SAM
      protons   = int(el["proton_count"])                   # SAM
      electrons = int(el["electron_count"])                 # SAM
      neutrons  = int(el["neutron_count_primary"])          # SAM
      qA        = float(el["qA_total_primary"])             # SAM

      PARTICLE  = protons + electrons + neutrons            # SAM identity
      ELEMENT   = Z                                         # SAM identity
      GRAVITY   = qA                                        # SAM identity

      MATTER    = ATOMIC_MASS.get(Z, "-")                   # comparator on SAM Z
      CLOCK     = clock_value(Z)                            # rule on SAM Z
      LIGHT     = LIGHT_NM.get(Z, "-")                      # comparator on SAM Z
      ACTION    = NUCLEAR_SPIN.get(Z, "-")                  # comparator on SAM Z

      (frontier Z=119..126 emit "-" for the four comparators)
```

That is **SAM scaffold + per-row comparator**, not external reference
data. CR212a introduces a new verdict tier `SAM_SCAFFOLD_PLACEMENT_GRADE`
to capture this distinction, applies it to the four columns that ride
the CR119 scaffold, and preserves CR212's empirical scan unmodified.

## Regraded verdicts

```text
OPEN_1  MATTER  (atomic weight 126 rows)
        CR212  : NOT_PROMOTABLE_FROM_EXISTING_DATA
        CR212a : SAM_SCAFFOLD_PLACEMENT_GRADE
        why    : ATOMIC_MASS[Z] lookup rides CR119 SAM row scaffold;
                 frontier Z=119-126 dash'ed; PLACEMENT-grade promotion only.

OPEN_2  CLOCK   (stable/radioactive flag 126 rows)
        CR212  : NOT_PROMOTABLE_FROM_EXISTING_DATA
        CR212a : SAM_SCAFFOLD_PLACEMENT_GRADE
        why    : clock_value(Z) rule on SAM-derived Z; PLACEMENT-grade only.

OPEN_3  LIGHT   (atomic wavelength 126 rows)
        CR212  : NOT_PROMOTABLE_FROM_EXISTING_DATA
        CR212a : SAM_SCAFFOLD_PLACEMENT_GRADE
        why    : LIGHT_NM[Z] lookup on SAM scaffold; limited-data rows dashed.

OPEN_4  ACTION  (nuclear spin 126 rows)
        CR212  : RETIRED_FALSIFIED
        CR212a : RETIRED_FALSIFIED   (unchanged)
        why    : HH001 1/102 self-falsification of action-residual = spin;
                 SAM-scaffold tie is placement context only, not rescue.

OPEN_5  seven-channel Fano position mapping
        CR212  : NOT_PROMOTABLE_FROM_EXISTING_DATA
        CR212a : SAM_SCAFFOLD_PLACEMENT_GRADE
        why    : F_2^3 partition sealed by CR113/114/115/116; placement on
                 the SAM scaffold; physical-meaning derivation remains open.

OPEN_6  126 GeV conversion
        CR212  : REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND
        CR212a : REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND   (unchanged)
        why    : LC02 replay from LC01-lock; CR120 target-visibility caveat.
```

Regrade verdict counts:

```text
SAM_SCAFFOLD_PLACEMENT_GRADE        4   (OPEN_1, OPEN_2, OPEN_3, OPEN_5)
RETIRED_FALSIFIED                   1   (OPEN_4)
REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND 1   (OPEN_6)
COURTROOM_NATIVE_BACKED             0
NOT_PROMOTABLE_FROM_EXISTING_DATA   0   (after regrade)
```

## What stays sealed

CR212 sealed-artifact hashes all match (`CR212a_cr212_seal_check.csv`,
0 mismatches over the full CR212 file set). CR212a does not modify
CR212. The empirical-scan record stands as written.

```text
CR210 sealed verdict       preserved
CR211 sealed verdict       preserved
CR212 sealed verdict       preserved
CR113/114/115/116 sealed   preserved
CR119 sealed               preserved
LC01 / LC02 / LC05 sealed  preserved
HH001 1/102 falsification  preserved
```

## What does NOT change

- No new theorem is sealed by CR212a.
- The seven-channel physical labeling is **not** declared closed; only
  its placement on the SAM scaffold is recognized.
- OPEN_6 (126 GeV) stays at REPLAY-grade. The CR120 target-visibility
  caveat is preserved verbatim.
- ACTION-spin (OPEN_4) stays RETIRED_FALSIFIED at the physical-spin
  level.
- The four PLACEMENT-grade columns are **not** asserted as forward-blind
  SAM derivations of their column values.

## Verdict-tier vocabulary after CR212a

```text
COURTROOM_NATIVE_BACKED              backed by a sealed SAM-native derivation
REPLAY_GRADE_ONLY_NOT_FORWARD_BLIND  backed via locked-stack replay; target-visible
SAM_SCAFFOLD_PLACEMENT_GRADE         comparator on SAM-derived row scaffold (new)
NOT_PROMOTABLE_FROM_EXISTING_DATA    no candidate corpus or scaffold backs the reading
RETIRED_FALSIFIED                    already falsified upstream
```

## Wrong controls

6/6 rejected. Including:

- WC2a (CR212 modified in place): rejected via re-hash check, 0 mismatches.
- WC3a (OPEN_4 promoted above RETIRED_FALSIFIED): rejected; OPEN_4 stays retired.
- WC5a (seven-channel labeling declared closed): rejected; OPEN_5 boundary
  field explicitly says physical-meaning derivation remains open.

## Checks

15/15 PASS.

## Primary artifacts

- `Fano_Plates/CR212a_FANO_PLATES_SAM_SCAFFOLD_REGRADE/REPLACEMENT_RECORD.md`
- `Fano_Plates/CR212a_FANO_PLATES_SAM_SCAFFOLD_REGRADE/CR212a_PRECOMMIT.md`
- `Fano_Plates/CR212a_FANO_PLATES_SAM_SCAFFOLD_REGRADE/CR212a_input_manifest.csv`
- `Fano_Plates/CR212a_FANO_PLATES_SAM_SCAFFOLD_REGRADE/CR212a_cr212_seal_check.csv`
- `Fano_Plates/CR212a_FANO_PLATES_SAM_SCAFFOLD_REGRADE/CR212a_regrade_table.csv`
- `Fano_Plates/CR212a_FANO_PLATES_SAM_SCAFFOLD_REGRADE/CR212a_sam_scaffold_evidence.csv`
- `Fano_Plates/CR212a_FANO_PLATES_SAM_SCAFFOLD_REGRADE/CR212a_wrong_controls.csv`
- `Fano_Plates/CR212a_FANO_PLATES_SAM_SCAFFOLD_REGRADE/CR212a_checks.csv`
- `Fano_Plates/CR212a_FANO_PLATES_SAM_SCAFFOLD_REGRADE/CR212a_summary.json`
- `Fano_Plates/CR212a_FANO_PLATES_SAM_SCAFFOLD_REGRADE/HASHES.txt`
