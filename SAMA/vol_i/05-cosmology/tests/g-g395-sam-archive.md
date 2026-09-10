# H0 Density Closure Selector

[Back to tests](README.md)

Test identity: `G:G395@SAM-ARCHIVE`.

## Premise

Routes G395 as the earlier CMB-data-conditioned density-closure inversion, not as an eta/K derivation and not as a dependency of CR036.

**Question:** Do the baryon- and matter-density inversions select a common H0 near 67.4, separate from the raw predecessor and reject H0=73.04 at the declared density offsets?

**Calculation:** Compute H0,b=100 sqrt(omega_b/Omega_b) and H0,m=100 sqrt(omega_m/Omega_m), then form the declared consensus and spread.

**Recorded outcome:** G395 records 9/9 checks and G395_PASS_H0_67P4_DENSITY_CLOSURE_SELECTOR_CANDIDATE__EXACT_NATIVE_SELECTOR_OPEN. Its primary consensus is H0=67.43595381087943 with spread 0.14824438582543564; the G383 neighbor gives 67.3931995510815.

**Scope of this result:** This is a CMB-data-conditioned selector candidate. It consumes neither eta nor FIRAS/CODATA conversion K and does not supply the exact native CR036 route.

**Controls:**

- Compare the primary selector with the G383 near-neighbor and raw G262 lane.

**Diagnostic comparisons:**

- H0=73.04 density closure, which displaces omega_b and omega_m by 17.5693% and 17.0535%.

The existing public index supplies a source locator and digest for this test, but no public source URL.

<details>
<summary>Exact source record</summary>

```json
{
  "alternate_source_paths": [
    "reference files_misc/archive/substrate_G_tests/G395_H0_DENSITY_CLOSURE_SELECTOR/G395_H0_DENSITY_CLOSURE_SELECTOR.py",
    "reference files_misc/archive/substrate_G_tests/G395_H0_DENSITY_CLOSURE_SELECTOR/G395_checks.csv",
    "reference files_misc/archive/substrate_G_tests/G395_H0_DENSITY_CLOSURE_SELECTOR/G395_output.txt",
    "reference files_misc/archive/substrate_G_tests/G395_H0_DENSITY_CLOSURE_SELECTOR/G395_selector_board.csv"
  ],
  "approval": null,
  "description": "H0 Density Closure Selector",
  "family": "G",
  "keywords": [
    "Density",
    "Closure",
    "Selector"
  ],
  "qualified_test_id": "G395@SAM-ARCHIVE",
  "record_key": "G:G395@SAM-ARCHIVE",
  "related_test_ids": [],
  "reviewed_and_approved": false,
  "source_basis": "SAM_WORKSPACE_ARCHIVE_ARTIFACT",
  "source_commit": null,
  "source_path": "reference files_misc/archive/substrate_G_tests/G395_H0_DENSITY_CLOSURE_SELECTOR/G395_output.json",
  "source_repo": "SAM_Workspace_Archive",
  "source_sha256": "1b2322aac8250a414e17b8f7be38715202f85dad06f6a4b15ad46ca0a11edf8a",
  "source_status": null,
  "source_url": null,
  "source_verdict": "G395_PASS_H0_67P4_DENSITY_CLOSURE_SELECTOR_CANDIDATE__EXACT_NATIVE_SELECTOR_OPEN",
  "test_id": "G395",
  "volume_numbers": [
    "I"
  ]
}
```

</details>
