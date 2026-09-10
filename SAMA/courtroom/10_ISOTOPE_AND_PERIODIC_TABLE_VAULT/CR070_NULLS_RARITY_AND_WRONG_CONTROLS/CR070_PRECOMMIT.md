# CR070 Nulls, Rarity, and Wrong Controls - Precommit

```text
document_id:    CR070_PRECOMMIT
branch:         10_ISOTOPE_AND_PERIODIC_TABLE_VAULT
cr_slot:        CR070
sealed_before:  CR070 runner exists and CR070 result exists
seal_anchor:    SEALED_ISOTOPE_AND_PERIODIC_TABLE_VAULT_SCOPE_APPROACH_2026_06_13
                (sha256: 9ff6d79e8e5c63c614e70a6cce2affa0510cc77e7fbf8781fc0a55fe940688b5)
manifest:       10_ISOTOPE_AND_PERIODIC_TABLE_VAULT/SOURCE_MANIFEST.csv
                manifest sha256: cd7cf11094ae00cfcbdae7c0be5c4577da715c65d1463b187f9596021e8d60d2
date_local:     2026-06-13
```

## Rule

```text
Verify three INDEPENDENT sub-lanes per the seal:

  Sub-lane A (Nulls):
    Known periodic-table holes (Tc Z=43, Pm Z=61) must be either
    pre-derived by the vault or explicitly flagged as debts with a
    boundary note.

  Sub-lane B (Rarity):
    The engine's internal pressure ordering (QP056/QP058) must
    correlate with natural-abundance / stability ranking beyond chance,
    declared via qp061_summary pressure_alignment_counts.

  Sub-lane C (Wrong controls):
    Perturbed QP049-QP060 chains and near-neighbor unselected ZNA
    triples must fail the CR069 anchor.

Per the seal: each sub-lane has its OWN Rule-9 line and pass criterion.
Branch verdict can only cite sub-lanes that individually passed.
A single aggregate PASS is forbidden language.
```

## Sub-Lane A - Nulls: Rule-9

```text
This test could have falsified the claim that the vault's structural
lane predicts known table holes (Tc Z=43, Pm Z=61) rather than being
fit to them.
```

## Sub-Lane B - Rarity: Rule-9

```text
This test could have falsified the claim that internal pressure
ordering (from QP056/QP058) correlates with natural-abundance ranking
beyond chance, rejecting permutation controls.
```

## Sub-Lane C - Wrong controls: Rule-9

```text
This test could have falsified the claim that the vault's 162/162 hit
rate at Z=1..96 is not reproducible by a perturbed engine (dropped
binding-depth lane, swapped Phase 5 freeze, perturbed pressure freeze).
```

## Declared Premises

```text
P1. Sub-lane A check (table holes):
      Tc (Z=43): no stable isotope known.
      Pm (Z=61): no stable isotope known.
      Verify these Z values appear in qp061_sealed_row_comparison.csv
      with appropriate handling (either pre-derived as boundaries or
      flagged in qp061_summary as named debts).

P2. Sub-lane B check (rarity / pressure alignment):
      qp061_summary.json field pressure_alignment_counts has shape:
        { "MATCH": N_match, "MISMATCH": N_miss, "NO_OBSERVED_ROW": N_no }
      Sub-lane PASS criterion:
        N_match / (N_match + N_miss) > 0.5
        (i.e., engine's pressure ordering correlates better than chance)

P3. Sub-lane C check (wrong-controls):
      QP049-QP060 source code .py files exist and each has at least
      one *_wrong_controls* / *_consistency_controls* sibling artifact.

P4. Aggregate verdict per seal:
      CR070_verdict = list of sub-lane verdicts, NOT a single PASS.

P5. CR065 manifest seal intact, hashes verified.
```

## Outcome Taxonomy

```text
PASS_SUB_LANE_A_NULLS:
  - Z=43 (Tc) and Z=61 (Pm) handled correctly per P1.

PASS_SUB_LANE_B_RARITY:
  - pressure_alignment_counts MATCH/MISMATCH ratio > 0.5.

PASS_SUB_LANE_C_WRONG_CONTROLS:
  - QP049-QP060 wrong-control siblings all present with rows.

BOUNDARY_SUB_LANE_X:
  - Sub-lane has partial evidence (e.g., one of two table holes
    flagged, one missing).

FAIL_SUB_LANE_X:
  - Sub-lane fails its declared criterion.

CR070 composite verdict is a tuple of (verdict_A, verdict_B, verdict_C).
The result.md must report all three explicitly with their own Rule-9
lines, per seal rule.
```

## Expected Artifacts

```text
CR070_PRECOMMIT.md
CR070_NULLS_RARITY_AND_WRONG_CONTROLS.py
CR070_input_manifest.csv
CR070_sublane_A_nulls_table_holes.json
CR070_sublane_B_rarity_pressure_alignment.json
CR070_sublane_C_wrong_controls_inventory.csv
CR070_wrong_controls_meta.csv     (meta-wrong-controls)
CR070_manifest_seal_check.json
CR070_summary.json
CR070_result.md
HASHES.txt
```

## Meta Wrong Controls (declared in advance)

```text
WC1: simulate Tc (Z=43) row missing from sealed_row_comparison.csv
     -> Sub-lane A FAIL detection
WC2: simulate pressure_alignment_counts with MISMATCH > MATCH
     -> Sub-lane B FAIL detection
WC3: simulate QP049 source code with NO wrong_controls sibling
     -> Sub-lane C FAIL detection
WC4: corrupt CR065 manifest seal -> DIAGNOSTIC
WC5: simulate qp061_summary missing pressure_alignment_counts field
     -> Sub-lane B DIAGNOSTIC
WC6: simulate Pm (Z=61) row missing -> Sub-lane A FAIL
```

## Sealed Premise Set

```text
P1-P5 sealed at CR070_PRECOMMIT write time.
```
