# CR115 Galaxy/PBH Bridge - PARTIAL Reveal Result

## Verdict

```text
CR115_GALAXY_PBH_BRIDGE_PARTIAL_REVEAL_SEALED
```

## Honest Scope

This bridge is **PARTIAL** by design.  Branch 08 CR022-CR030 was sealed BEFORE CR110 was registered in this session.  CR115 documents what is bridged and what explicitly remains open.

## Naming Disambiguation (Critical)

Branch 08 uses **'BB-origin PBH/trapped-A'** as a SAM-native label for the cumulative trapped-A field at primordial scale.  This is **NOT** the same object class as CR109 particle PBHs (compact objects probed by EROS/OGLE/HSC microlensing).  CR023's omega_pbh ~ 0.265 refers to the SAM-native trapped-A inventory, not to particle PBHs.

## CR110_PRED_2 - Particle PBH Envelope Consistent with f_PBH ~ 0

```text
CR023 post-BB particle subchannel = 0.025767
CR024 post-BB envelope supplies   = 2.5767% of dark residual
CR024 missing after particle PBH  = 97.4233% of dark residual
implied f_PBH(particle) upper bound from CR024 = 0.0258
```

**Status: BRIDGED_PARTICLE_PBH_INSUFFICIENT_CONSISTENT_WITH_CUMULATIVE_A_READING**

Particle PBHs supply at most ~2.58% of the SPARC dark residual.  Cumulative-A interpretation carries the remaining ~97% as trapped-A field, not particle DM.

## CR110_PRED_1 - Rotation Curves Follow G732c Native R12 Cored Law

```text
CR024 SPARC galaxies              = 175
CR024 SPARC points                = 3391
CR024 median outer dark fraction  = 0.7607
CR025 galaxies fit                = 175
CR025 median baryon RMS km/s      = 40.9524
CR025 median halo RMS km/s        = 3.6254
CR025 chi^2 improvement vs baryon = 150.7662x
CR025 halo overdensity vs cosmic  = 79090x cosmic DM mean
CR025 native radial law           = native radial organization law / mass function / concentration relation
```

**Status: BRIDGED_PARTIALLY_RESIDUAL_AND_CLUSTERED_PROFILE_CLOSED_NATIVE_RADIAL_LAW_OPEN**

**Bridged:** real SPARC residual confirmed; clustered profile fits 175 galaxies zero-free-parameter with 150x chi^2 improvement and 79,090x cosmic overdensity.

**Open:** the specific G732c r_c = R_outer/12 functional form was not the profile CR025 tested.  Per-galaxy r_c extraction vs R_outer/12 prediction is a useful future CR.

## Cryptographic Chain

```text
CR022 kernel root (08)              = d342cf25d4fa3dfd3496c1fab27ccb855eda100abc07931efb5960741f7292ec
CR023 inventory chain (08)          = a59d73dc2c0c40443c12976551f036dd9045474edf91d7b8f0b112e73cd4064d
CR024 SPARC residual (08)           = 9688c421c88f0adbf26478a54bbc35d6d81f40b3f875ef326f7ef101a30b3fad
CR025 clustered profile (08)        = 5387ad567c098862152dcfadb96881125eac45ef79378cac532c97d9fbe7920e
CR030 branch verdict (08)           = ecb113a122f78965315e1c630efc16e93083b2194a161f3ee01111cd653385fc
CR107 SPARC anchor (14)             = 937ee99e4605dff30ee0fac1ef12ad2e3bfd2091e4ca296c83a1afa77259388c
CR109 PBH anchor (14)               = 8594e7025ffe9b92bd3592bf80195385347059b66973a51e3b6e128c760ace86
CR110 three-mode appeal (14)        = 6f85af05104c0ee7ec4ff6ecd1dd706d065f8942492eb0a8efdaeee6d84cce8b
CR098a registry (13)                = e867f2ba8e4e4aed27ed517dbe812d0cb0f9e72b3b6baaca73e876a5a1287986
CR113 cross-branch certificate      = 5023841154959148aab6574358be3bd24eeab58f585736b2c28cc387e1cb2f35
CR114 cosmic baryon bridge          = e2f394b40768bc45d916427e7031066cb23e24298e0e4337c3c5bcd4715549c6
BLINDNESS_PROTOCOL.md               = 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
CR115 bridge JSON sha256            = e193d8ec8179e6bc2c4fa88a4623bc28fe7e9e4e2c0162f096eac77c4f521b9c
```

## Predictions

- **[PASS]** P1_branch_08_summaries_present
- **[PASS]** P2_cr110_appeal_present
- **[PASS]** P3_cr107_sparc_anchor_present
- **[PASS]** P4_cr109_pbh_anchor_present
- **[PASS]** P5_cr024_real_sparc_175_galaxies_loaded
- **[PASS]** P6_cr024_post_bb_particle_pbh_insufficient_as_full_halo
- **[PASS]** P7_cr025_clustered_profile_chi2_improvement_over_100x
- **[PASS]** P8_cr025_radial_law_explicitly_recorded_as_open
- **[PASS]** P9_naming_disambiguation_documented
- **[PASS]** P10_both_appeal_rows_written_to_separate_csv
- **[PASS]** P11_bridge_file_sealed_with_sha256_sibling
- **[PASS]** P12_blindness_protocol_present

## Wrong Controls

- **[PASS]** WC1_no_branch_08_CR_modified
- **[PASS]** WC2_no_cr110_appeal_modified
- **[PASS]** WC3_cr098a_registry_csv_not_modified
- **[PASS]** WC4_no_free_parameter_introduced
- **[PASS]** WC5_no_full_closure_claimed_radial_law_explicitly_marked_open
- **[PASS]** WC6_trapped_a_vs_particle_pbh_not_conflated
- **[PASS]** WC7_no_forward_blind_claim_made

## Immutability

CR022, CR023, CR024, CR025, CR030, CR107, CR109, CR110, CR098a, CR113, CR114 all unmodified.  Both appeal rows live in `CR115_appeal_rows_for_CR098a_CR110_PRED_1_and_2.csv` inside this CR's dir, per the CR098a rule that match reveals are added in a NEW CR.

## Open Debts

```text
- G732c r_c = R_outer/12 specific functional form vs SPARC per-galaxy r_c is the natural next reveal CR
- CR110_PRED_3 (Earth-mode K(A_H) continued improvement) - no direct bridge in 08; bridges to 13/14 EP tests
- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
```
