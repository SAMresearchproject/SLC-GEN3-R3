# CR116 SAM Halo Composition - Honest Correction

## Verdict

```text
CR116_SAM_HALO_COMPOSITION_CORRECTION_SEALED_PRIOR_READINGS_SUPERSEDED
```

## Provenance of the Catch

USER flagged the misread directly during governance review immediately after CR115 was committed.  The catch is recorded here in full transparency.

## What Was Misread

Three artifacts from THIS session carry an incorrect reading of SAM halo physics:

| Artifact | Where | What is wrong |
|---|---|---|
| CR110_PRED_2 | 14 branch | claims f_PBH ~ 0 |
| CR098a registry CR110_PRED_2 row | 13 branch | carries the same wrong reading |
| CR115 bridge | governance | concluded 'particle PBH insufficient' |

All three remain on the public record **immutable and unmodified**.  CR116 supersedes their readings; it does not edit them.

## Corrected Reading

```text
SAM galactic halo = cumulative nonzero A field + CLUSTERED BB-origin PBHs
```

**Critical distinction:** uniform / smooth-distribution PBHs ARE ruled out (CR026 uniform-control gap closed = 0.004 percent).  But that does NOT mean f_PBH = 0.  SAM's PBHs are **clustered** from Big Bang origin, and the clustered inventory is at **Omega_PBH ~ 0.265** (i.e. essentially all of Omega_DM).

## Evidence from Branch 08 (sealed prior to this session)

```text
CR023 omega_pbh (BB-origin trapped-A/PBH inventory) = 0.26446190430295646
CR026 primary candidate id                          = base12_outer_radius_over_12
CR026 primary clustered gap closed                  = 0.819138
CR026 uniform-distribution control gap closed       = 0.00003850  (REJECTED)
CR026 post-BB-window-only control gap closed        = 0.024485  (REJECTED)
CR027 first scaffold                                = BB-origin PBH/trapped-A clustered mass scaffold
CR027 selected route                                = bb_pbh_trapped_A_first_scaffold_plus_hydrogen_catchup
CR027 PBH/hydrogen mass ratio                       = 5.3644
CR025 clustered halo overdensity vs cosmic DM mean  = 79090x
CR025 chi^2 improvement over baryon-only            = 150.7662x
```

Branch 08 is unambiguous: BB-origin **clustered** PBHs + cumulative-A field carry the halo.

## Why Microlensing Envelopes Stay Compatible

CR109's microlensing envelope is dominantly a bound on **smooth/uniform** PBH spatial distributions.  Line-of-sight event statistics depend strongly on spatial geometry.  Clustered PBHs - which CR026 directly selects - evade smooth-distribution bounds.  The smooth-f_PBH envelope is therefore not a refutation of clustered PBH at f ~ Omega_DM.

**Honest open debt:** a clustered-PBH-aware microlensing analysis is the natural future test.  If that analysis tightens bounds below the CR023 clustered inventory, the SAM reading is in structural trouble.

## Corrected Forward-Blind Reading

**CR116_CORRECTED_PRED_2** (replaces the original CR110_PRED_2 framing):

> Galactic halo = cumulative nonzero A field + CLUSTERED BB-origin PBHs at > f_PBH ~ Omega_PBH / Omega_DM (CR023 omega_pbh ~ 0.265).  Compatible with CR109 > microlensing envelope BECAUSE the envelope constrains smooth distributions; clustered > PBHs evade these bounds.

Falsification criteria:

- a verified non-clustered (smooth/uniform) PBH detection at f_PBH ~ Omega_DM would falsify
- a clustered-PBH-aware microlensing envelope tightening below SAM clustered inventory would falsify
- any halo derivation that requires zero PBH inventory and also closes SPARC residual + scaffold + hydrogen catchup would falsify the BB-origin-PBH-first reading

## Cryptographic Chain

```text
CR022 (08) kernel root              = d342cf25d4fa3dfd3496c1fab27ccb855eda100abc07931efb5960741f7292ec
CR023 (08) inventory chain          = a59d73dc2c0c40443c12976551f036dd9045474edf91d7b8f0b112e73cd4064d
CR024 (08) SPARC residual           = 9688c421c88f0adbf26478a54bbc35d6d81f40b3f875ef326f7ef101a30b3fad
CR025 (08) clustered profile        = 5387ad567c098862152dcfadb96881125eac45ef79378cac532c97d9fbe7920e
CR026 (08) seed-first clustering    = 0d9d072cdc1ce8dec7940085d51b87331c80edb2629cfc5609edf6ac055ae3c2
CR027 (08) hydrogen catchup         = dceb3afae107c12057acdedfb611b82ab37864f6a561617651e508c73fb4bc0f
CR030 (08) branch verdict           = ecb113a122f78965315e1c630efc16e93083b2194a161f3ee01111cd653385fc
CR109 (14) PBH anchor               = 8594e7025ffe9b92bd3592bf80195385347059b66973a51e3b6e128c760ace86
CR110 (14) three-mode appeal        = 6f85af05104c0ee7ec4ff6ecd1dd706d065f8942492eb0a8efdaeee6d84cce8b  (UNMODIFIED, contains incorrect PRED_2)
CR098a (13) registry CSV            = e867f2ba8e4e4aed27ed517dbe812d0cb0f9e72b3b6baaca73e876a5a1287986  (UNMODIFIED, contains incorrect PRED_2 entry)
CR115 (gov) galaxy/PBH bridge       = e193d8ec8179e6bc2c4fa88a4623bc28fe7e9e4e2c0162f096eac77c4f521b9c  (UNMODIFIED, contains misread PRED_2 verdict)
BLINDNESS_PROTOCOL.md               = 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
CR116 correction lock sha256        = d3f3204be9cbc5bbb9520664bdb937452981e494f38c6154266fffa95a04fd65
```

## Predictions

- **[PASS]** P1_misread_explicitly_documented
- **[PASS]** P2_branch_08_corrected_reading_supported_by_CR023_omega_pbh
- **[PASS]** P3_CR026_uniform_control_rejected_supports_clustered_reading
- **[PASS]** P4_CR026_post_bb_only_rejected_distinguishes_from_BB_origin
- **[PASS]** P5_CR026_clustered_primary_gap_closed_dominant
- **[PASS]** P6_CR027_BB_origin_PBH_clustered_scaffold_recorded
- **[PASS]** P7_microlensing_clustered_vs_smooth_distinction_documented
- **[PASS]** P8_corrected_forward_blind_reading_registered_with_falsifiers
- **[PASS]** P9_no_prior_artifact_modified
- **[PASS]** P10_correction_lock_sealed_with_sha256_sibling
- **[PASS]** P11_three_appeal_rows_written_separately_not_inline
- **[PASS]** P12_provenance_of_user_catch_recorded

## Wrong Controls

- **[PASS]** WC1_CR110_appeal_lock_unmodified
- **[PASS]** WC2_CR098a_registry_csv_unmodified
- **[PASS]** WC3_CR115_bridge_unmodified
- **[PASS]** WC4_no_free_parameter_introduced
- **[PASS]** WC5_no_silent_overwriting_of_prior_session_artifacts
- **[PASS]** WC6_correction_does_not_claim_branch_08_validates_clustered_PBH_at_full_DM_against_microlensing_quantitatively

## Immutability Preserved

CR110, CR098a, CR115 stay on the public record exactly as committed, with their incorrect readings intact.  CR116 supersedes them transparently - it does not edit them.  Future readers will see both: the original mistake and the honest correction.  The audit trail of human-caught error is itself a record of how the Courtroom works.

## Open Debts

```text
- Clustered-PBH-aware microlensing envelope analysis - natural next future CR to close CR116_CORRECTED_PRED_2 quantitatively
- Future CR098b (registry refresh) would import CR116_CORRECTED_PRED_2 cleanly
- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
```
