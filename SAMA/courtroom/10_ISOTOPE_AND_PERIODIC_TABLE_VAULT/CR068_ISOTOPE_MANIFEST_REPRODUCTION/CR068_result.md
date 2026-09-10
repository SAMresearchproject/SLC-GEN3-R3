# CR068 Isotope Manifest Reproduction

## Verdict

```text
CR068_PASS_SCOPED_STRUCTURAL_ISOTOPE_MANIFEST_REPRODUCTION
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS_SCOPED_STRUCTURAL
triage_bin = A
```

## Reason

```text
QP055/QP058/QP059 hash-locked; QP060 pre-comparison state verified; 200 sealed prediction rows present
```

## Phase Summary

```text
Phase 1 manifest seal + hash      verified=155
Phase 2 QP artifacts              reproduction_verified=4/4
Phase 3 QP060 pre-comparison      status=pre_comparison_state_verified
Phase 4 prediction row count      found=200  expected=200  matches=True
Phase 5 wrong reproductions       passed=6/6
```

## QP060 Pre-Comparison Fields

```text
external_data_used           = False
prediction_manifest_sha256   = 19781d97b1008b3b1a1d030c64f37ab8ad7e55b7127cc75b72a0ab2792f697c3
hash_manifest_sha256         = 4461edd2fea795fa84ea20c1c230005f8eaae968ed11640196850f29bc28a273
```

## Rule-9 Line

```text
This test could have falsified: the claim that the QP isotope vault
manifest reproduces byte-equivalent across QP055 + QP058 + QP059 +
QP060 with exactly 200 sealed prediction rows pre-locked before the
QP061 external-comparison step.
```

## Artifacts

- `CR068_input_manifest.csv`
- `CR068_qp055_qp058_qp059_check.csv`
- `CR068_qp060_sealed_protocol_check.json`
- `CR068_prediction_row_count_check.json`
- `CR068_wrong_reproductions.csv`
- `CR068_manifest_seal_check.json`
- `CR068_summary.json`
- `HASHES.txt`
