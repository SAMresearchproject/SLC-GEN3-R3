# CR071 Superheavy Miss-Band Target Map - Precommit

```text
document_id:    CR071_PRECOMMIT
branch:         10_ISOTOPE_AND_PERIODIC_TABLE_VAULT
cr_slot:        CR071
sealed_before:  CR071 runner exists and CR071 result exists
seal_anchor:    SEALED_ISOTOPE_AND_PERIODIC_TABLE_VAULT_SCOPE_APPROACH_2026_06_13
                (sha256: 9ff6d79e8e5c63c614e70a6cce2affa0510cc77e7fbf8781fc0a55fe940688b5)
manifest:       10_ISOTOPE_AND_PERIODIC_TABLE_VAULT/SOURCE_MANIFEST.csv
                manifest sha256: cd7cf11094ae00cfcbdae7c0be5c4577da715c65d1463b187f9596021e8d60d2
date_local:     2026-06-13
```

## Rule

```text
Seal the Z=97..118 frontier band (38 sealed prediction rows, 0 IAEA
observed at retrieval) as a PRE-REGISTERED PREDICTION MAP.  CR071's
verdict is PERMANENT and never overwritten.  Future discoveries either
upgrade it (APPEAL_FRONTIER_HIT) or break it (APPEAL_FRONTIER_MISS) via
the M3 appeal channel.

Per the seal: this is the strongest courtroom move in the entire 10
branch.  Without CR071, the 0/38 Z=97..118 result is a 0/38 failure.
With CR071, it is a structured, sealed, falsifiable prediction.
```

## Question

```text
Are SAM's 38 predicted Z=97..118 ZNA rows pre-registered such that:
  (a) qp068 high_z_neutron_rich_island_prediction_table.csv is
      hash-locked,
  (b) qp068 nz_tier_structure_table.csv is hash-locked,
  (c) qp068 synthesis_inflection_table.csv is hash-locked,
  (d) the 38-row count matches qp061_band_summary Z_097_118 sealed_rows,
  (e) no row predicted by qp068 references an IAEA-observed value
      (the frontier prediction is forward-looking, not back-fit)?
```

## Declared Premises

```text
P1. QP068 frontier prediction artifacts (hash-locked):
      artifacts/qp068/qp068_high_z_neutron_rich_island_prediction_table.csv
      artifacts/qp068/qp068_nz_tier_structure_table.csv
      artifacts/qp068/qp068_synthesis_inflection_table.csv
      artifacts/qp068/qp068_summary.json
      artifacts/qp068/qp068_preflight.md

P2. Row count consistency:
      qp068 prediction table row count must be consistent with
      qp061_band_summary Z_097_118 sealed_rows = 38.

P3. QP068 self-disclosure (verified by CR066):
      external_data_used = false
      free_parameters_introduced = 0

P4. Pre-registration seal:
      CR071 produces a SHA256-sealed prediction record
      (CR071_pre_registered_frontier_map.json) that pins the per-Z
      ZNA coordinates AT CR071 EXECUTION TIME, before any new IAEA
      release post-2026-06-13.

P5. Permanent verdict statement:
      The verdict CR071_BOUNDARY_PRE_REGISTERED_PREDICTION is permanent.
      It is NEVER overwritten.  Future discoveries land as appeal CRs
      under M3 channel:
        APPEAL_FRONTIER_HIT  - a new IAEA observation matches a CR071-
                               predicted ZNA row
        APPEAL_FRONTIER_MISS - a new IAEA observation is in Z=97..118
                               but does NOT match any predicted row

P6. CR065 manifest seal intact.
```

## Outcome Taxonomy

```text
BOUNDARY_PRE_REGISTERED_PREDICTION:
  - All QP068 artifacts hash-locked.
  - Prediction table row count consistent with band_summary.
  - CR071 emits CR071_pre_registered_frontier_map.json with sealed
    SHA256.
  - This is the ONLY allowed "positive" outcome for CR071.
  - The verdict is permanent and never overwritten.

DIAGNOSTIC:
  - Manifest seal missing.
  - QP068 artifacts unreadable or missing.

FAIL:
  - Row count mismatch.
  - QP068 self-disclosure shows external_data_used=true
    (would break P3 - CR066 should have caught this).
```

## Rule-9 Line

```text
This test could have falsified the claim that SAM's Z=97..118 frontier
prediction is pre-registered, structured, hash-sealed before any
post-2026-06-13 IAEA observation, and consists of 38 specific ZNA
coordinates predicted from native structure rather than back-fit to
known absences.
```

## Expected Artifacts

```text
CR071_PRECOMMIT.md
CR071_SUPERHEAVY_MISS_BAND_TARGET_MAP.py
CR071_input_manifest.csv
CR071_qp068_artifact_check.csv
CR071_frontier_prediction_count_check.json
CR071_pre_registered_frontier_map.json   (THE SEALED PREDICTION RECORD)
CR071_pre_registered_frontier_map.sha256.txt
CR071_appeal_channel_documentation.md    (channel for future updates)
CR071_wrong_controls.csv
CR071_manifest_seal_check.json
CR071_summary.json
CR071_result.md
HASHES.txt
```

## Wrong Controls (declared in advance)

```text
WC1: simulate qp068 prediction table row count = 37 -> FAIL on P2
WC2: simulate qp068 external_data_used = true       -> FAIL on P3
WC3: simulate prediction map sha256 collision       -> not credible;
     wrong control wired to confirm sha256 is computed
WC4: corrupt CR065 manifest seal -> DIAGNOSTIC
WC5: simulate retrieval date post-2026-06-13 on IAEA roster
     (would imply backfit)       -> would FAIL upstream at CR065
WC6: simulate post-CR071 IAEA observation matching one prediction
     -> appeal channel produces APPEAL_FRONTIER_HIT; CR071 itself
     remains BOUNDARY_PRE_REGISTERED_PREDICTION permanently
```

## Sealed Premise Set

```text
P1-P6 sealed at CR071_PRECOMMIT write time.
```
