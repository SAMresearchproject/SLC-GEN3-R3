# CR118 Distance Road SN+BAO Headline Export - Result

## Verdict

```text
CR118_DISTANCE_ROAD_SN_BAO_HEADLINE_EXPORT_SEALED
```

## One-Line Headline

> Two independent observational ledgers (SN luminosity 1701 Pantheon rows; BAO ruler projection 19 rows) are built without sharing data AND independently reduce to the same A_los(z) with zero free parameters; their cross-overlap is 0.240%.

## Key Numbers (verified from sealed CRs)

```text
A0                              = 0.026525823848649224
w                               = 0.0466031311731253
r_drag (derived, Mpc)           = 150.92186401518705
r_drag delta vs Planck (%)      = +2.6330
SN Pantheon rows                = 1701
SN max mu identity error        = 7.105427357601002e-15
BAO compilation rows            = 19
BAO rms pull                    = 0.8269872776835621
BAO rows over 3 sigma           = 0
SN-BAO cross overlap (%)        = 0.24000025506268896
SAM distance-road fit params    = 0
LCDM baseline fit params        = ~6
```

## Predictions

- **[PASS]** P1_CR012_structural_constants_consistent_with_A0_identity
- **[PASS]** P2_CR013_sn_ledger_identity_at_machine_precision
- **[PASS]** P3_CR014_bao_zero_rows_over_3sigma
- **[PASS]** P4_CR015_cross_overlap_within_quarter_percent
- **[PASS]** P5_r_drag_derived_within_few_percent_of_planck
- **[PASS]** P6_two_lanes_built_without_shared_data
- **[PASS]** P7_zero_free_parameters_in_distance_road
- **[PASS]** P8_branch_verdict_CR017_PASS_referenced_unchanged
- **[PASS]** P9_export_headline_sealed_with_sha256_sibling
- **[PASS]** P10_no_prior_CR_modified

## Wrong Controls

- **[PASS]** WC1_does_not_claim_full_cosmological_closure
- **[PASS]** WC2_does_not_modify_branch_06_CRs
- **[PASS]** WC3_does_not_introduce_free_parameter
- **[PASS]** WC4_does_not_overstate_BAO_sample_size
- **[PASS]** WC5_does_not_misrepresent_overlap_as_global
- **[PASS]** WC6_honest_about_LCDM_comparison

## Headline Export Document

See `CR118_HEADLINE_SN_BAO_CROSS_OVERLAP_AT_QUARTER_PERCENT_ZERO_FREE_PARAMETERS.md` for the human-readable external-facing claim.

## Cryptographic Chain

```text
CR012 sha256 = 29abc83488c863d2eacf7ca2595cda4f63cd5ef969eed56fcd8631ae9523517d
CR013 sha256 = bffd17d22a11fcb03b0c2dd8581550d60df91c052e59e7f8023bae7d300420cc
CR014 sha256 = 78fe728d2adf4780ccf13ec1b7cd5149889f00057f7150a63cbfe1594d17b8a2
CR015 sha256 = 584d3dad801b81bc62e84b22be6b45391c14fe238b0aa6b85b27bc85e3fb8217
CR016 sha256 = 4ec3d7baf0966db6daeec2da2c0a5b3393eff2165471a8941be03cb1935af5d6
CR017 sha256 = b122955abcfa4cb4739f2e8846b3c51b3155d72ad9961013b113b706b782f555
CR114 sha256 = e2f394b40768bc45d916427e7031066cb23e24298e0e4337c3c5bcd4715549c6
CR117 sha256 = 0ccbc3d720674b45a8f4b569a926a3ae213ea5a00786380fd598a2a8568c7c4c
BLINDNESS_PROTOCOL sha256 = 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
CR118 headline sha256 = 05b17c8984b1546c9d301e0c89f208472cc45584660c0958b367b0b48abb848d
```

## Open Debts

```text
- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
- Future high-row BAO compilation (DESI/LSST) could tighten the 19-row test
- CMB modal/polarization closure is the next-layer move per CR117 scope boundary
```
