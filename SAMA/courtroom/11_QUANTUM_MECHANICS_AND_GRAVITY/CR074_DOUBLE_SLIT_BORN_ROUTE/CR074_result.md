# CR074 Double Slit / Born Route

## Verdict
```text
CR074_PASS_SCOPED_STRUCTURAL_BORN_ROUTE
```

## Reason
```text
Born+route_weight identities present (b=2, rw=9); qp014 0 free params; G421 present; engine clean
```

## Phase Summary
```text
Phase 1 seal + hash    verified=242
Phase 2 Born identity  born_present hits=2
Phase 3 route weight   route_weight_present hits=9
Phase 4 qp014 disclos  zero_free_parameters_verified
Phase 5 fit-scan       fail=0
Phase 6 G421 bridge    present
Phase 7 wrong controls passed=6/6
```

## Rule-9 Line
```text
This test could have falsified the claim that SAM reproduces the Born
rule as route weighting over unresolved exposure without an external
probability postulate or fit-to-observation loop.
```

## Artifacts
- `CR074_input_manifest.csv`
- `CR074_born_identity_check.json`
- `CR074_route_weight_check.json`
- `CR074_qp014_disclosure_check.json`
- `CR074_engine_surface_fit_scan.csv`
- `CR074_public_bridge_cite_check.csv`
- `CR074_manifest_seal_check.json`
- `CR074_wrong_controls.csv`
- `CR074_summary.json`
- `HASHES.txt`
