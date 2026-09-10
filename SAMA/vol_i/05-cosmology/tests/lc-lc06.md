# Baryon And Matter Inventory Replay

[Back to tests](README.md)

Test identity: `LC:LC06`.

## Retest

Routes LC06 as the locked-stack replay of baryon and matter inventory, independent of CR281 and inclusive of the preserved CR023 boundary.

**Question:** Does the locked LC01 stack replay CR018 and CR019, preserve CR023 and recover every matter-row and wrong-control check?

**Calculation:** Recompute the baryon and matter ledgers from locked primitives, replay the direct CR rows and execute the matter/carrier wrong controls.

**Recorded outcome:** LC06 records LC06_PASS_BARYON_AND_MATTER_INVENTORY_REPLAY_FROM_LOCKED_PRIMITIVE_STACK with 58/58 checks, 10/10 wrong controls and 126/126 matter rows.

**Scope of this result:** LC06 replays and preserves the branch; it does not depend on CR281 and does not change CR023 BOUNDARY.

**Controls:**

- 58 replay checks and ten wrong controls.
- Complete 126-row matter ledger.

**Diagnostic comparisons:**

- Depend on CR281, which LC06 does not read.
- Count Theta18 or other carrier support as rest mass.

[Read the original test](../../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_result.md)

<details>
<summary>Exact source record</summary>

```json
{
  "alternate_source_paths": [],
  "approval": null,
  "description": "Baryon And Matter Inventory Replay",
  "family": "LC",
  "keywords": [
    "baryon",
    "Matter",
    "Inventory",
    "Replay"
  ],
  "qualified_test_id": "LC06",
  "record_key": "LC:LC06",
  "related_test_ids": [],
  "reviewed_and_approved": false,
  "source_basis": "LAST_CAMPAIGN_RESULT",
  "source_commit": "b5e914f71377e86ef4c67e199973d9300795cda1",
  "source_path": "16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_result.md",
  "source_repo": "The_Courtroom",
  "source_sha256": "81d5a92553e11c6b656ea4cb84d352a49600158eca5accf28d03b56abec1b2af",
  "source_status": null,
  "source_url": "../../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_result.md",
  "source_verdict": null,
  "test_id": "LC06",
  "volume_numbers": [
    "I",
    "II"
  ]
}
```

</details>



<!-- BEGIN FULL COURTROOM DATA -->
## Full Courtroom data

[Open the primary source record](../../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_result.md) · [All 10 package files](../../../tests/courtroom/16-the-last-campaign-lc06-baryon-matter-inventory-replay/README.md) · [Browse the source directory in CR](../../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY)

Package: `16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY`. This includes **0 code files** and **2 files categorized as results or reports**, plus all inputs, figures and other tracked files. The full inventory is unabridged.

### Wrong controls and comparison rows

- [LC06_wrong_controls.csv](../../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_wrong_controls.csv)

<details>
<summary>Results and reports</summary>

- [LC06_result.md](../../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_result.md) — [raw](../../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_result.md)
- [LC06_summary.json](../../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_summary.json) — [raw](../../../courtroom/16_THE_LAST_CAMPAIGN/LC06_BARYON_MATTER_INVENTORY_REPLAY/LC06_summary.json)

</details>

## Related Courtroom tests

- **retest of:** [07_BARYON_INVENTORY_AND_COSMOLOGY/CR018_A0_CHI_BARYON_INVENTORY_DERIVATION](../../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR018_A0_CHI_BARYON_INVENTORY_DERIVATION)
- **retest of:** [07_BARYON_INVENTORY_AND_COSMOLOGY/CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT](../../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT)
- **depends on:** [07_BARYON_INVENTORY_AND_COSMOLOGY/CR023_BARYON_COSMOLOGY_BRANCH_VERDICT](../../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR023_BARYON_COSMOLOGY_BRANCH_VERDICT)
- **depends on:** [16_THE_LAST_CAMPAIGN](../../../courtroom/16_THE_LAST_CAMPAIGN)
- **retest of:** [16_THE_LAST_CAMPAIGN](../../../courtroom/16_THE_LAST_CAMPAIGN)
- **retest of:** [16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY](../../../courtroom/16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY)

<details>
<summary>Other tests mentioned in the source package</summary>

These links record mentions, not an inferred dependency or supporting result. Where an identifier has several branch-qualified matches, their paths remain explicit.

- [00_governance/CR114_COSMIC_BARYON_BRIDGE_REVEAL](../../../courtroom/00_governance/CR114_COSMIC_BARYON_BRIDGE_REVEAL)
- [00_governance/CR116_SAM_HALO_COMPOSITION_CORRECTION](../../../courtroom/00_governance/CR116_SAM_HALO_COMPOSITION_CORRECTION)
- [06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR018_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_TEST](../../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR018_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_TEST)
- [06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR018_candidate_workspace](../../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR018_candidate_workspace)
- [06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR019_SAM_ZERO_PARAMETER_CMB_COMPRESSED_GEOMETRY_TEST](../../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR019_SAM_ZERO_PARAMETER_CMB_COMPRESSED_GEOMETRY_TEST)
- [06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR019_candidate_workspace](../../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR019_candidate_workspace)
- [07_BARYON_INVENTORY_AND_COSMOLOGY/CR018_A0_CHI_BARYON_INVENTORY_DERIVATION](../../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR018_A0_CHI_BARYON_INVENTORY_DERIVATION)
- [07_BARYON_INVENTORY_AND_COSMOLOGY/CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT](../../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR019_EFFECTIVE_MATTER_INVENTORY_REFINEMENT)
- [07_BARYON_INVENTORY_AND_COSMOLOGY/CR020_CMB_BOUNDARY_AND_ACOUSTIC_CONCEPT_CHAIN](../../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR020_CMB_BOUNDARY_AND_ACOUSTIC_CONCEPT_CHAIN)
- [07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT](../../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT)
- [07_BARYON_INVENTORY_AND_COSMOLOGY/CR022_PRECISION_CMB_EXTENSION_FROM_sam_precision_cmb](../../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR022_PRECISION_CMB_EXTENSION_FROM_sam_precision_cmb)
- [07_BARYON_INVENTORY_AND_COSMOLOGY/CR023_BARYON_COSMOLOGY_BRANCH_VERDICT](../../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR023_BARYON_COSMOLOGY_BRANCH_VERDICT)
- [07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts](../../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts)
- [08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION](../../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION)
- [08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR023_BB_PBH_TRAPPED_A_INVENTORY](../../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR023_BB_PBH_TRAPPED_A_INVENTORY)
- [09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL](../../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL)
- [14_FOUNDATIONAL_TESTS/CR111_COSMIC_BARYON_OMEGA_B_CLOSURE_APPEAL](../../../courtroom/14_FOUNDATIONAL_TESTS/CR111_COSMIC_BARYON_OMEGA_B_CLOSURE_APPEAL)
- [14_FOUNDATIONAL_TESTS/CR114_BINARY_FACE_STATE_SPLIT_THEOREM](../../../courtroom/14_FOUNDATIONAL_TESTS/CR114_BINARY_FACE_STATE_SPLIT_THEOREM)
- [14_FOUNDATIONAL_TESTS/CR116_18_GRAVITON_CARRIER_THEOREM](../../../courtroom/14_FOUNDATIONAL_TESTS/CR116_18_GRAVITON_CARRIER_THEOREM)
- [14_FOUNDATIONAL_TESTS/CR119_TYPED_CLOSURE_HIERARCHY_PROMOTION_LADDER](../../../courtroom/14_FOUNDATIONAL_TESTS/CR119_TYPED_CLOSURE_HIERARCHY_PROMOTION_LADDER)
- [14_FOUNDATIONAL_TESTS/_scratch/QP093A_0299_FIXED_SINGLETON_A_MASS_RESPONSE](../../../courtroom/14_FOUNDATIONAL_TESTS/_scratch/QP093A_0299_FIXED_SINGLETON_A_MASS_RESPONSE)
- [16_THE_LAST_CAMPAIGN](../../../courtroom/16_THE_LAST_CAMPAIGN)
- [16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY](../../../courtroom/16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY)
- [16_THE_LAST_CAMPAIGN/LC05_PERIODIC_ISOTOPE_VAULT_REPLAY](../../../courtroom/16_THE_LAST_CAMPAIGN/LC05_PERIODIC_ISOTOPE_VAULT_REPLAY)
- [17_DISCOVERY_INTAKE/CR210_HH001_FANO_PLATES_126_INTAKE](../../../courtroom/17_DISCOVERY_INTAKE/CR210_HH001_FANO_PLATES_126_INTAKE)
- [Workbench-misc](../../../courtroom/Workbench-misc)
- [upstream_artifacts/qp092](../../../courtroom/upstream_artifacts/qp092)

</details>

<!-- END FULL COURTROOM DATA -->
