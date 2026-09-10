# CR075 Unresolved Path and Ledger Write

## Verdict
```text
CR075_PASS_SCOPED_STRUCTURAL_LEDGER_WRITE_CHAIN
```

## Reason
```text
protected_route+syndrome+ledger_commit+stable_mode all present; qp010+qp016 zero free params; 5/5 public bridges; engine clean
```

## Phase Summary
```text
P1 seal+hash       verified=242
P2 protected_route hits=6
P3 syndrome        hits=6
P4 ledger_commit   hits=10
P5 stable_mode     hits=8
P6 qp010           zero_free_params
P7 qp016           zero_free_params
P8 fit-scan        fail=0
P9 public_bridges  5/5 present
P10 wrong controls 6/6
```

## Rule-9
```text
This test could have falsified the claim that SAM reproduces the
unresolved-to-resolved ledger-write chain with zero free parameters
and no engine-surface fit loop.
```

## Artifacts
- `CR075_input_manifest.csv`
- `CR075_protected_route_check.json`
- `CR075_syndrome_boundary_check.json`
- `CR075_ledger_commit_check.json`
- `CR075_stable_mode_selector_check.json`
- `CR075_qp_disclosure_check.json`
- `CR075_engine_surface_fit_scan.csv`
- `CR075_public_bridge_cite_check.csv`
- `CR075_manifest_seal_check.json`
- `CR075_wrong_controls.csv`
- `CR075_summary.json`
- `HASHES.txt`
