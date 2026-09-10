# CR069 Observed Roster Comparison - Precommit

```text
document_id:    CR069_PRECOMMIT
branch:         10_ISOTOPE_AND_PERIODIC_TABLE_VAULT
cr_slot:        CR069
sealed_before:  CR069 runner exists and CR069 result exists
seal_anchor:    SEALED_ISOTOPE_AND_PERIODIC_TABLE_VAULT_SCOPE_APPROACH_2026_06_13
                (sha256: 9ff6d79e8e5c63c614e70a6cce2affa0510cc77e7fbf8781fc0a55fe940688b5)
manifest:       10_ISOTOPE_AND_PERIODIC_TABLE_VAULT/SOURCE_MANIFEST.csv
                manifest sha256: cd7cf11094ae00cfcbdae7c0be5c4577da715c65d1463b187f9596021e8d60d2
date_local:     2026-06-13
```

## Rule

```text
Verify per-row contact between QP061's sealed prediction manifest (200
rows) and the IAEA LiveChart of Nuclides ground-state roster, within
the declared Z bands:

  Z = 1..96   :  162 / 162 exact ZNA matches required for K1 PASS
  Z = 97..118 :  0   / 38  observed at retrieval (frontier band,
                            deferred to CR071 for structured map)
  Z = 1..118  :  162 / 200 total

Per the seal: the Z=97..118 band is a STRUCTURED MISS, not a
scattered failure.  It is recorded but not scored here; CR071 freezes
it as a pre-registered prediction map.
```

## Question

```text
Does QP061's sealed prediction manifest contact the IAEA LiveChart
ground-state roster such that:
  (a) Z=1..96 band achieves 162/162 exact ZNA matches (100%),
  (b) Z=1..82 sub-band achieves 136/136 (100%),
  (c) Z=83..96 sub-band achieves 26/26 (100%),
  (d) Z=97..118 frontier band is reported as 0/38 (a structured miss
      to be sealed at CR071, NOT scored as FAIL here),
  (e) per-element coverage rate matches qp061_summary.json's declared
      element_exact_coverage_rate (96/118 = 0.8136)?
```

## Declared Premises

```text
P1. QP061 hash-locked artifacts in scope:
      artifacts/qp061/qp061_summary.json
      artifacts/qp061/qp061_band_summary.csv
      artifacts/qp061/qp061_sealed_row_comparison.csv
      artifacts/qp061/qp061_observed_roster_normalized.csv
      artifacts/qp061/qp061_element_coverage_summary.csv
      artifacts/qp061/external/iaea_livechart_ground_states_all_qp061.csv

P2. IAEA local roster sha256 must equal the QP061-declared value:
      8aee5dc431af1e35fcb49746387b83e927b3c300e7787defbda621a08212c795
      (already verified by CR065 Phase 3).

P3. Band partition (from qp061_band_summary.csv):
      Z_001_082, Z_083_096, Z_001_096 (combined), Z_097_118, Z_001_118.

P4. K1 PASS criterion (Z=1..96):
      sealed_rows = 162, exact_ZNA_matches = 162, exact_match_rate = 1.0.

P5. Z=97..118 deferral:
      This band is recorded as STRUCTURED MISS BAND (sealed at CR071).
      0/38 hit rate is NOT a CR069 FAIL.

P6. Cross-check with qp061_summary.json:
      exact_ZNA_matches = 162 must match band_summary's Z_001_096 row.

P7. CR065 manifest seal intact.

P8. No CR069 phase modifies any QP061 artifact or the IAEA roster.
```

## Outcome Taxonomy

```text
PASS_SCOPED_K1_ROSTER_LEVEL:
  - All hashes verify.
  - Z=1..96 = 162/162 exact ZNA matches.
  - Z=1..82 = 136/136 sub-band.
  - Z=83..96 = 26/26 sub-band.
  - qp061_summary.json cross-check matches band_summary.
  - Z=97..118 = 0/38 reported but not scored (deferred to CR071).

BOUNDARY:
  - All structural conditions hold but per-element coverage rate is
    indeterminate or partial (e.g., element_exact_coverage_rate field
    missing from summary).

FAIL:
  - Z=1..96 hit rate < 162/162.
  - Hash mismatch on any QP061 artifact.
  - band_summary.csv contradicts qp061_summary.json.

DIAGNOSTIC:
  - Manifest seal missing.
  - QP061 artifact unreadable.
  - IAEA local file missing or sha mismatch (rolled forward from CR065).
```

## Rule-9 Line

```text
This test could have falsified: the claim that SAM's sealed-hash-guarded
QP061 isotope prediction manifest contacts the IAEA LiveChart ground-
state roster exactly 162/162 times across Z=1..96, with 0/38 in the
Z=97..118 frontier band reserved as a structured miss to be sealed
at CR071.
```

## Expected Artifacts

```text
CR069_PRECOMMIT.md
CR069_OBSERVED_ROSTER_COMPARISON.py
CR069_input_manifest.csv
CR069_qp061_artifact_check.csv
CR069_band_partition_verification.csv
CR069_z_001_096_pass_summary.json
CR069_z_097_118_deferred_summary.json
CR069_element_coverage_check.json
CR069_iaea_anchor_roll_forward.json
CR069_wrong_controls.csv
CR069_manifest_seal_check.json
CR069_summary.json
CR069_result.md
HASHES.txt
```

## Wrong Controls (declared in advance)

```text
WC1: simulate Z=1..96 hit rate = 161/162 -> FAIL
WC2: simulate Z=1..82 sub-band miss -> FAIL
WC3: simulate IAEA local sha mismatch -> DIAGNOSTIC
WC4: simulate band_summary inconsistent with qp061_summary -> FAIL
WC5: corrupt CR065 manifest seal -> DIAGNOSTIC
WC6: simulate Z=97..118 hit rate change (e.g., 1/38 vs 0/38)
     -> recorded but does NOT change CR069 verdict (deferred to CR071)
```

## Sealed Premise Set

```text
P1-P8 sealed at CR069_PRECOMMIT write time.
```
