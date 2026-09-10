# CR066 Allowed Inputs and Forbidden Targets

## Verdict

```text
CR066_BOUNDARY_VAULT_INPUT_BOUNDARY_VERIFIED
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = BOUNDARY
triage_bin = B
```

## Reason

```text
vault input boundary verified clean; K1 external anchor reserved for CR069
```

## Phase Summary

```text
Phase 1 manifest seal + hash       seal=True  sha_matches=True  verified=155
Phase 2 vault construction chain   clean=12/12  violations=0
Phase 3 qp060 boundary             status=boundary_correctly_declared
Phase 4 qp061 comparator role      status=comparator_role_confirmed
Phase 5 qp068 self-disclosure      status=clean_disclosure
Phase 6 forbidden input scan       engine_hits=0  doc_mentions=0  clean=4
Phase 7 wrong controls             passed=6/6
```

## QP061 Comparator-Role Confirmation

```text
external_data_used               = True
sealed_hash_guard_pass           = True
prediction_manifest_mutated      = False
free_parameters_introduced       = 0
external_data_sha256             = 8aee5dc431af1e35fcb49746387b83e927b3c300e7787defbda621a08212c795
```

## QP060 Boundary Declaration

```text
next_frontier_names_qp061           = True
next_frontier_declares_external_data = True
next_frontier_text                  = QP061_PRIVATE_APPROVED_SEALED_ISOTOPE_COMPARISON_REQUIRES_EXTERNAL_DATA_PREFLIGHT
```

## Rule-9 Line

```text
This test could have falsified: the claim that the QP isotope vault
construction chain (QP049-QP060 + QP068) consumes no externally
measured isotope value, no external authority roster value, and no
post-observation calibration source as a construction input, and that
the only point of external-data admission is QP061 as a post-
construction comparator.
```

## Courtroom Reading

CR066 is the input-boundary gate for the 10 branch. A BOUNDARY verdict
is the expected default: the test certifies that the vault construction
chain consumes no external data and that QP061 cleanly admits IAEA data
only as a sealed-hash-guarded post-construction comparator. The K1
external anchor is at CR069 observed roster comparison.

## Artifacts

- `CR066_input_manifest.csv`
- `CR066_qp_self_disclosure_check.csv`
- `CR066_qp060_boundary_check.json`
- `CR066_qp061_comparator_role_check.json`
- `CR066_forbidden_input_scan.csv`
- `CR066_manifest_seal_check.json`
- `CR066_wrong_controls.csv`
- `CR066_summary.json`
- `HASHES.txt`
