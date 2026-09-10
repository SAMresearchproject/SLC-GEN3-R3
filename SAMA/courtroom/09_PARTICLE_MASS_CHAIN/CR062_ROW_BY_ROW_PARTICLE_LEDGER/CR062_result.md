# CR062 Row-by-Row Particle Ledger (K1 Anchor)

## Verdict

```text
CR062_PASS_SCOPED_K1_ROW_LEVEL_ROW_BY_ROW_PARTICLE_LEDGER
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS_SCOPED_K1_ROW_LEVEL
triage_bin = A
```

## Reason

```text
all 10 strict rows contact PDG within 1.0% tolerance; 2 audit rows within 2.0% band; 3/3 neutrinos within PDG upper bound
```

## Phase Summary

```text
Phase 1 manifest seal + frozen table   sha_matches=True  frozen_table_sha_match=True  verified=572
Phase 2-4 row extraction + verdicts    rows_extracted=15
Phase 5 strict-grade aggregate         10/10 PASS_SCOPED_ROW_LEVEL  max_residual=0.801%
Phase 6 audit-grade aggregate          2/2 BOUNDARY_ROW_LEVEL  max_residual=0.478%
Phase 7 boundary-grade (neutrino)      3/3 within PDG upper bound
Phase 8 wrong control injections       passed=6/6
```

## Row-by-Row Results

| Symbol | Predicted (MeV) | Observed (MeV) | Residual % | Grade | Verdict |
|---|---:|---:|---:|---|---|
| H | 125077 | 125250.0 | 0.138 | strict | PASS_SCOPED_ROW_LEVEL |
| e | 0.512349 | 0.51099895 | 0.264 | strict | PASS_SCOPED_ROW_LEVEL |
| mu | 106.504 | 105.6583755 | 0.801 | strict | PASS_SCOPED_ROW_LEVEL |
| tau | 1770.68 | 1776.86 | 0.348 | strict | PASS_SCOPED_ROW_LEVEL |
| nu_e | 1.91971e-08 | <= 2e-06 | - | boundary | BOUNDARY_ROW_LEVEL_WITHIN_PDG_UPPER_BOUND |
| nu_mu | 3.99058e-06 | <= 0.19 | - | boundary | BOUNDARY_ROW_LEVEL_WITHIN_PDG_UPPER_BOUND |
| nu_tau | 6.6345e-05 | <= 18.2 | - | boundary | BOUNDARY_ROW_LEVEL_WITHIN_PDG_UPPER_BOUND |
| u | 2.14509 | 2.16 | 0.690 | strict | PASS_SCOPED_ROW_LEVEL |
| d | 4.64769 | 4.67 | 0.478 | audit | BOUNDARY_ROW_LEVEL_WITHIN_AUDIT_BAND |
| s | 92.8098 | 93.4 | 0.632 | strict | PASS_SCOPED_ROW_LEVEL |
| c | 1278.05 | 1273.0 | 0.397 | strict | PASS_SCOPED_ROW_LEVEL |
| b | 4181.91 | 4183.0 | 0.026 | strict | PASS_SCOPED_ROW_LEVEL |
| t | 172763 | 172690.0 | 0.042 | audit | BOUNDARY_ROW_LEVEL_WITHIN_AUDIT_BAND |
| W | 80365.1 | 80369.2 | 0.005 | strict | PASS_SCOPED_ROW_LEVEL |
| Z | 91161.5 | 91187.6 | 0.029 | strict | PASS_SCOPED_ROW_LEVEL |


## Rule-9 Line

```text
This test could have falsified: the claim that SAM's parameter-free
particle predictions contact the PDG 2024 observed masses within
1.0% for strict-grade rows, within 2.0% for audit-grade rows, and
at-or-below the PDG upper bound for neutrino rows, derived from the
same engine that produced the Phase4 frozen tables under zero free
parameters.
```

## Courtroom Reading

CR062 is the K1 external anchor slot for the 09 branch.
PASS_SCOPED_K1_ROW_LEVEL means every strict row contacts PDG within
1.0%, every audit row within 2.0%, and every neutrino row sits at or
below the documented PDG upper bound.  PDG 2024 values are pinned in
CR062_pdg_2024_typed_inputs.json and become hash-locked input to this
CR.

Per the seal: residuals are recorded as fields, not verdict criteria.
The verdict is whether a row satisfies its grade tolerance.

## Artifacts

- `CR062_input_manifest.csv`
- `CR062_pdg_2024_typed_inputs.json`
- `CR062_row_by_row_ledger.csv`
- `CR062_strict_grade_summary.json`
- `CR062_audit_grade_summary.json`
- `CR062_boundary_grade_summary.json`
- `CR062_wrong_controls.csv`
- `CR062_manifest_seal_check.json`
- `CR062_summary.json`
- `HASHES.txt`
