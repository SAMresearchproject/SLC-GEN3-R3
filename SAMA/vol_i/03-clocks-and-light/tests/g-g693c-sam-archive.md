# BAO Explicit c eff Native Distance Conversion

[Back to tests](README.md)

Test identity: `G:G693c@SAM-ARCHIVE`.

## Construction

Applies the declared coordinate conversion to BAO lanes and preserves the derivative-projection boundary.

**Question:** Does applying the explicit c_eff distance conversion to the declared BAO rows reduce the fixed row residuals, and does a speed-only anisotropic substitute fail where the derivative projection is required?

**Calculation:** Transform the declared BAO distance lanes by 1-A_los(z), calculate row residuals, and compare the applicable derivative-projected lane with the speed-only diagnostic lane.

**Recorded outcome:** The source result recorded mean absolute row residual changing from 29.990028% to 7.412127%; the speed-only anisotropic control remained insufficient and the declared derivative projection supplied the applicable lane.

**Scope of this result:** The record develops the BAO conversion and exposes its derivative boundary; it does not turn one distance factor into every BAO observable or close recombination physics.

**Controls:**

- Unmodified-row comparison.
- Exact application of the declared distance factor.
- Separate derivative projection for the anisotropic radial lane.

**Diagnostic comparisons:**

- Using only the common speed factor as a replacement for the anisotropic derivative projection.
- Reinterpreting the coordinate factor as local variable c.

## Construction

Routes BAO Explicit c eff Native Distance Conversion as a construction in the local/global road type boundary chain while preserving the source artifact and its historical status fields.

**Question:** For G:G693c@SAM-ARCHIVE: Does the evidence chain preserve local-source integration, global A_los construction, boundary values and native-distance conversion without one road replacing the other?

**Calculation:** Replay each road under its own construction and verify the exact bridge and boundary identities.

**Recorded outcome:** The permanent registry identifies G:G693c@SAM-ARCHIVE as ‘BAO Explicit c eff Native Distance Conversion’. The registry exposes no structured status or verdict, so the pinned source artifact remains the detailed outcome authority and this crosswalk adds no verdict.

**Scope of this result:** The route closes the distance-road types only; recombination, perturbations and polarization remain distinct.

**Controls:**

- z=0 and saturation limits.
- Typed dependency closure.

**Diagnostic comparisons:**

- Using host mass as the global road.
- Using the universal floor as a Euclidean local integrand.
- Speed-only replacement of a derivative projection.

The existing public index supplies a source locator and digest for this test, but no public source URL.

<details>
<summary>Exact source record</summary>

```json
{
  "alternate_source_paths": [
    "reference files_misc/archive/substrate_G_tests/G693c_BAO_EXPLICIT_C_EFF_NATIVE_DISTANCE_CONVERSION/G693c_BAO_EXPLICIT_C_EFF_NATIVE_DISTANCE_CONVERSION.py",
    "reference files_misc/archive/substrate_G_tests/G693c_BAO_EXPLICIT_C_EFF_NATIVE_DISTANCE_CONVERSION/G693c_PREFLIGHT.md"
  ],
  "approval": null,
  "description": "BAO Explicit c eff Native Distance Conversion",
  "family": "G",
  "keywords": [
    "BAO",
    "Explicit",
    "eff",
    "Native",
    "Distance",
    "Conversion"
  ],
  "qualified_test_id": "G693c@SAM-ARCHIVE",
  "record_key": "G:G693c@SAM-ARCHIVE",
  "related_test_ids": [],
  "reviewed_and_approved": false,
  "source_basis": "SAM_WORKSPACE_ARCHIVE_ARTIFACT",
  "source_commit": null,
  "source_path": "reference files_misc/archive/substrate_G_tests/G693c_BAO_EXPLICIT_C_EFF_NATIVE_DISTANCE_CONVERSION/G693c_RESULT.md",
  "source_repo": "SAM_Workspace_Archive",
  "source_sha256": "9f5fdf622826dec843a7fedf22890f4206024205eff5bee57308d9d4c0bb573a",
  "source_status": null,
  "source_url": null,
  "source_verdict": null,
  "test_id": "G693c",
  "volume_numbers": [
    "I"
  ]
}
```

</details>
