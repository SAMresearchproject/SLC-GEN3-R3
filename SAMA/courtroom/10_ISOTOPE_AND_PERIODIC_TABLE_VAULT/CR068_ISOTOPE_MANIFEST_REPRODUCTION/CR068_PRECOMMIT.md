# CR068 Isotope Manifest Reproduction - Precommit

```text
document_id:    CR068_PRECOMMIT
branch:         10_ISOTOPE_AND_PERIODIC_TABLE_VAULT
cr_slot:        CR068
sealed_before:  CR068 runner exists and CR068 result exists
seal_anchor:    SEALED_ISOTOPE_AND_PERIODIC_TABLE_VAULT_SCOPE_APPROACH_2026_06_13
                (sha256: 9ff6d79e8e5c63c614e70a6cce2affa0510cc77e7fbf8781fc0a55fe940688b5)
manifest:       10_ISOTOPE_AND_PERIODIC_TABLE_VAULT/SOURCE_MANIFEST.csv
                manifest sha256: cd7cf11094ae00cfcbdae7c0be5c4577da715c65d1463b187f9596021e8d60d2
date_local:     2026-06-13
```

## Rule

```text
Verify byte-equivalent reproduction of the QP isotope vault manifest
across QP055 (Phase 5 isotope freeze), QP058 (pressure freeze), QP059
(visual package), and QP060 (sealed comparison protocol pre-comparison
state).  Verify the declared 200 sealed prediction rows are present
and hash-locked.  Do NOT contact the observed roster - roster contact
is reserved for CR069.
```

## Question

```text
Can the isotope vault manifest be shown to reproduce byte-equivalent
such that:
  (a) QP055 Phase 5 isotope freeze artifacts hash-match the manifest,
  (b) QP058 pressure freeze artifacts hash-match,
  (c) QP059 visual package byte-equivalent to sealed_results visual
      package (or QP059 artifacts hash-match if no sealed_results visual
      counterpart),
  (d) QP060 sealed comparison protocol pre-comparison state hash-matches,
  (e) the declared 200 sealed prediction rows exist in
      qp060_sealed_prediction_manifest.csv / phase5_sealed_prediction_manifest.csv
      and the count is exactly 200?
```

## Declared Premises

```text
P1. QP055 Phase 5 isotope freeze:
      qp055 summary and artifacts present and hash-locked.

P2. QP056 residual stability / decay pressure:
      Structural reading only - no roster contact.

P3. QP058 pressure freeze:
      qp058 artifacts present and hash-locked.

P4. QP059 visual package:
      qp059 artifacts present and hash-locked.

P5. QP060 sealed comparison protocol pre-comparison state:
      qp060 summary.json declares external_data_used=false,
      prediction_manifest_sha256, hash_manifest_sha256.
      The pre-comparison state predates QP061.

P6. Declared 200 sealed prediction rows:
      qp060_sealed_prediction_manifest.csv or
      phase4_tables/phase5_sealed_prediction_manifest.csv
      Must have exactly 200 prediction rows (one per sealed isotope row).

P7. No roster contact:
      No CR068 phase reads the IAEA local roster file.

P8. CR065 manifest seal intact.
```

## Outcome Taxonomy

```text
PASS_SCOPED_STRUCTURAL:
  - All manifest hashes verify.
  - QP055/QP058/QP059 artifacts present + hash-locked.
  - QP060 sealed_comparison_protocol pre-comparison fields verified.
  - 200 sealed prediction rows present.

BOUNDARY:
  - PASS conditions hold but with documented gaps (e.g., a visual
    artifact missing a sealed_results counterpart that wasn't required).

FAIL:
  - Hash mismatch on QP055/QP058/QP059.
  - QP060 sealed protocol fields contradict pre-comparison declaration.
  - Prediction row count != 200.

DIAGNOSTIC:
  - Manifest seal missing.
  - QP summary unreadable.
```

## Rule-9 Line

```text
This test could have falsified: the claim that the QP isotope vault
manifest reproduces byte-equivalent across QP055 + QP058 + QP059 +
QP060 with exactly 200 sealed prediction rows pre-locked before the
QP061 external-comparison step.
```

## Expected Artifacts

```text
CR068_PRECOMMIT.md
CR068_ISOTOPE_MANIFEST_REPRODUCTION.py
CR068_input_manifest.csv
CR068_qp055_qp058_qp059_check.csv
CR068_qp060_sealed_protocol_check.json
CR068_prediction_row_count_check.json
CR068_wrong_reproductions.csv
CR068_manifest_seal_check.json
CR068_summary.json
CR068_result.md
HASHES.txt
```

## Wrong Reproductions (declared in advance)

```text
WC1: simulate qp055 freeze hash mismatch -> FAIL
WC2: simulate qp058 pressure freeze hash mismatch -> FAIL
WC3: simulate prediction row count = 199 (off by one) -> FAIL
WC4: simulate qp060 external_data_used=true (pre-comparison violation) -> FAIL
WC5: corrupt CR065 manifest seal -> DIAGNOSTIC
WC6: simulate dropped binding-depth lane (qp051 missing) -> FAIL via chain break
```

## Sealed Premise Set

```text
P1-P8 sealed at CR068_PRECOMMIT write time.
```
