# CR127 Light-ALP / Dark-Scalar Coverage Map (10-1000 MeV)

## Verdict

```text
CR127_LIGHT_ALP_COVERAGE_MAP_SEALED
```

## What This CR Does

Walks the 150 SAM particle rows that fell in CR124's LIGHT_ALP_WINDOW (10 MeV - 1000 MeV), filters to 141 physically-allowed matter candidates, sub-classifies by mass band, attributes each row to active 2026 ALP-search experiments, identifies mass clusters, and ranks each row by test-readiness.

## Headline

- ALP-window rows: **150** (CR124-tagged)
- Physically allowed: **141** (after excluding 9)
- Structural clusters: **41** (88 rows clustered, 53 isolated)
- Priority: **HIGH=44**, MEDIUM=54, LOW=43

## Exclusions

| status | count | reason |
|---|---:|---|
| CARRIER_ONLY_NOT_MATTER | 2 | tensor / vector carrier; not a matter particle |
| HIDDEN_SUPPORT_NOT_MATTER | 1 | substrate support; not a matter particle |
| REJECTED_FAKE_CLOSURE | 6 | SAM's own stability filter rejects (CR126 lesson) |

## Mass Band Distribution

| band | range (MeV) | count | active 2026 experiments |
|---|---|---:|---|
| L0_10to100MeV | 10-100 | 49 | NA64, BaBar (legacy), BESIII, MEG II |
| L1_100to300MeV | 100-300 | 45 | NA62, NA64, BaBar (legacy), BESIII, FASER |
| L2_300to1000MeV | 300-1000 | 47 | KLOE-2, BESIII, BaBar (legacy), PADME, FASER |

## Operator Class Distribution

| class | count |
|---|---:|
| V4_1_SINGLE_WRITE | 58 |
| BOUND_COLOR_PAIR | 36 |
| OCTET_COMPOSITE | 32 |
| OUTER_BINARY_NEUTRAL | 11 |
| GROUND_BARYON_3BODY | 4 |

## Stability Status Distribution

| status | count |
|---|---:|
| BOUND_PAIR_CHARGED_CANDIDATE | 42 |
| STABLE_MATTER_CANDIDATE | 30 |
| ANTIMATTER_STABLE_CONJUGATE | 28 |
| UNSTABLE_PAIR_HEAVY_CANDIDATE | 10 |
| BOUND_COLOR_CLOSED_HEAVY_CANDIDATE | 9 |
| STABLE_NEUTRAL_CANDIDATE | 8 |
| BOUND_PAIR_NEUTRAL_CANDIDATE | 7 |
| BOUND_COLOR_CLOSED_STABLE_CANDIDATE | 4 |
| UNSTABLE_HEAVY_WRITE_CANDIDATE | 3 |

## Priority Manifest (Top 30)

| rank | candidate | M (MeV) | band | operator | status | score | priority |
|---:|---|---:|---|---|---|---:|---|
| 1 | QP093A-0235 | 10.75 | L0 | BOUND_COLOR_PAIR | BOUND_PAIR_NEUTRAL_CANDIDATE | 8 | HIGH |
| 2 | QP093A-0042 | 12.00 | L0 | OUTER_BINARY_NEUTRAL | STABLE_NEUTRAL_CANDIDATE | 8 | HIGH |
| 3 | QP093A-0045 | 13.50 | L0 | OUTER_BINARY_NEUTRAL | STABLE_NEUTRAL_CANDIDATE | 8 | HIGH |
| 4 | QP093A-0054 | 36.00 | L0 | OUTER_BINARY_NEUTRAL | STABLE_NEUTRAL_CANDIDATE | 8 | HIGH |
| 5 | QP093A-0244 | 43.00 | L0 | BOUND_COLOR_PAIR | BOUND_PAIR_NEUTRAL_CANDIDATE | 8 | HIGH |
| 6 | QP093A-0057 | 54.00 | L0 | OUTER_BINARY_NEUTRAL | STABLE_NEUTRAL_CANDIDATE | 8 | HIGH |
| 7 | QP093A-0060 | 72.00 | L0 | OUTER_BINARY_NEUTRAL | STABLE_NEUTRAL_CANDIDATE | 8 | HIGH |
| 8 | QP093A-0115 | 72.00 | L0 | GROUND_BARYON_3BODY | BOUND_COLOR_CLOSED_STABLE_CANDIDATE | 8 | HIGH |
| 9 | QP093A-0253 | 96.75 | L0 | BOUND_COLOR_PAIR | BOUND_PAIR_NEUTRAL_CANDIDATE | 8 | HIGH |
| 10 | QP093A-0063 | 108.00 | L1 | OUTER_BINARY_NEUTRAL | STABLE_NEUTRAL_CANDIDATE | 8 | HIGH |
| 11 | QP093A-0262 | 172.00 | L1 | BOUND_COLOR_PAIR | BOUND_PAIR_NEUTRAL_CANDIDATE | 8 | HIGH |
| 12 | QP093A-0151 | 252.00 | L1 | GROUND_BARYON_3BODY | BOUND_COLOR_CLOSED_STABLE_CANDIDATE | 8 | HIGH |
| 13 | QP093A-0048 | 18.00 | L0 | OUTER_BINARY_NEUTRAL | STABLE_NEUTRAL_CANDIDATE | 7 | HIGH |
| 14 | QP093A-0051 | 18.00 | L0 | OUTER_BINARY_NEUTRAL | STABLE_NEUTRAL_CANDIDATE | 7 | HIGH |
| 15 | QP093A-0016 | 10.00 | L0 | V4_1_SINGLE_WRITE | STABLE_MATTER_CANDIDATE | 6 | HIGH |
| 16 | QP093A-0017 | 12.00 | L0 | V4_1_SINGLE_WRITE | STABLE_MATTER_CANDIDATE | 6 | HIGH |
| 17 | QP093A-0020 | 13.50 | L0 | V4_1_SINGLE_WRITE | STABLE_MATTER_CANDIDATE | 6 | HIGH |
| 18 | QP093A-0083 | 16.67 | L0 | V4_1_SINGLE_WRITE | ANTIMATTER_STABLE_CONJUGATE | 6 | HIGH |
| 19 | QP093A-0085 | 19.69 | L0 | V4_1_SINGLE_WRITE | ANTIMATTER_STABLE_CONJUGATE | 6 | HIGH |
| 20 | QP093A-0091 | 30.42 | L0 | V4_1_SINGLE_WRITE | ANTIMATTER_STABLE_CONJUGATE | 6 | HIGH |
| 21 | QP093A-0092 | 35.50 | L0 | V4_1_SINGLE_WRITE | ANTIMATTER_STABLE_CONJUGATE | 6 | HIGH |
| 22 | QP093A-0029 | 36.00 | L0 | V4_1_SINGLE_WRITE | STABLE_MATTER_CANDIDATE | 6 | HIGH |
| 23 | QP093A-0031 | 45.00 | L0 | V4_1_SINGLE_WRITE | STABLE_MATTER_CANDIDATE | 6 | HIGH |
| 24 | QP093A-0093 | 45.94 | L0 | V4_1_SINGLE_WRITE | ANTIMATTER_STABLE_CONJUGATE | 6 | HIGH |
| 25 | QP093A-0094 | 52.88 | L0 | V4_1_SINGLE_WRITE | ANTIMATTER_STABLE_CONJUGATE | 6 | HIGH |
| 26 | QP093A-0032 | 54.00 | L0 | V4_1_SINGLE_WRITE | STABLE_MATTER_CANDIDATE | 6 | HIGH |
| 27 | QP093A-0034 | 60.00 | L0 | V4_1_SINGLE_WRITE | STABLE_MATTER_CANDIDATE | 6 | HIGH |
| 28 | QP093A-0095 | 61.67 | L0 | V4_1_SINGLE_WRITE | ANTIMATTER_STABLE_CONJUGATE | 6 | HIGH |
| 29 | QP093A-0096 | 70.00 | L0 | V4_1_SINGLE_WRITE | ANTIMATTER_STABLE_CONJUGATE | 6 | HIGH |
| 30 | QP093A-0035 | 72.00 | L0 | V4_1_SINGLE_WRITE | STABLE_MATTER_CANDIDATE | 6 | HIGH |

Full priority-ranked inventory (141 rows) in `CR127_alp_window_inventory.csv`.  Top 30 in `CR127_priority_manifest.csv`.

## Structural Clusters (>=2 rows from same operator_class within 1%)

Total clusters: **41**.  Members:

| cluster_id | operator_class | size | mass range (MeV) | candidate IDs |
|---:|---|---:|---|---|
| 1 | BOUND_COLOR_PAIR | 2 | 26.99-27.01 | QP093A-0243, QP093A-0236 |
| 2 | BOUND_COLOR_PAIR | 2 | 41.99-42.01 | QP093A-0251, QP093A-0237 |
| 3 | BOUND_COLOR_PAIR | 2 | 56.98-57.02 | QP093A-0259, QP093A-0238 |
| 4 | BOUND_COLOR_PAIR | 2 | 74.99-75.01 | QP093A-0252, QP093A-0245 |
| 5 | BOUND_COLOR_PAIR | 2 | 86.97-87.03 | QP093A-0267, QP093A-0239 |
| 6 | BOUND_COLOR_PAIR | 2 | 101.98-102.02 | QP093A-0260, QP093A-0246 |
| 7 | BOUND_COLOR_PAIR | 2 | 116.94-117.06 | QP093A-0275, QP093A-0240 |
| 8 | BOUND_COLOR_PAIR | 2 | 146.97-147.03 | QP093A-0261, QP093A-0254 |
| 9 | BOUND_COLOR_PAIR | 2 | 155.95-156.05 | QP093A-0268, QP093A-0247 |
| 10 | BOUND_COLOR_PAIR | 2 | 209.91-210.09 | QP093A-0276, QP093A-0248 |
| 11 | BOUND_COLOR_PAIR | 2 | 224.93-225.07 | QP093A-0269, QP093A-0255 |
| 12 | BOUND_COLOR_PAIR | 2 | 293.93-294.07 | QP093A-0270, QP093A-0263 |
| 13 | BOUND_COLOR_PAIR | 2 | 302.88-303.12 | QP093A-0277, QP093A-0256 |
| 14 | BOUND_COLOR_PAIR | 2 | 395.87-396.13 | QP093A-0278, QP093A-0264 |
| 15 | BOUND_COLOR_PAIR | 2 | 581.86-582.14 | QP093A-0279, QP093A-0272 |
| 16 | OCTET_COMPOSITE | 2 | 131.94-132.06 | QP093A-0283, QP093A-0241 |
| 17 | OCTET_COMPOSITE | 2 | 176.90-177.10 | QP093A-0291, QP093A-0242 |
| 18 | OCTET_COMPOSITE | 2 | 236.91-237.09 | QP093A-0284, QP093A-0249 |
| 19 | OCTET_COMPOSITE | 2 | 317.84-318.16 | QP093A-0292, QP093A-0250 |
| 20 | OCTET_COMPOSITE | 2 | 341.89-342.11 | QP093A-0285, QP093A-0257 |
| 21 | OCTET_COMPOSITE | 2 | 446.88-447.12 | QP093A-0286, QP093A-0265 |
| 22 | OCTET_COMPOSITE | 2 | 458.78-459.22 | QP093A-0293, QP093A-0258 |
| 23 | OCTET_COMPOSITE | 2 | 599.75-600.25 | QP093A-0294, QP093A-0266 |
| 24 | OCTET_COMPOSITE | 2 | 656.88-657.12 | QP093A-0287, QP093A-0273 |
| 25 | OCTET_COMPOSITE | 3 | 863.93-867.07 | QP093A-0153, QP093A-0288, QP093A-0281 |
| 26 | OCTET_COMPOSITE | 3 | 881.71-885.94 | QP093A-0295, QP093A-0274, QP093A-0289 |
| 27 | OUTER_BINARY_NEUTRAL | 2 | 18.00-18.00 | QP093A-0048, QP093A-0051 |
| 28 | V4_1_SINGLE_WRITE | 2 | 11.25-11.25 | QP093A-0019, QP093A-0081 |
| 29 | V4_1_SINGLE_WRITE | 3 | 15.00-15.10 | QP093A-0022, QP093A-0025, QP093A-0089 |
| 30 | V4_1_SINGLE_WRITE | 3 | 17.88-18.00 | QP093A-0090, QP093A-0023, QP093A-0026 |
| 31 | V4_1_SINGLE_WRITE | 2 | 30.00-30.00 | QP093A-0028, QP093A-0087 |
| 32 | V4_1_SINGLE_WRITE | 2 | 135.00-136.00 | QP093A-0043, QP093A-0100 |
| 33 | V4_1_SINGLE_WRITE | 2 | 143.44-144.00 | QP093A-0101, QP093A-0041 |
| 34 | V4_1_SINGLE_WRITE | 3 | 180.00-180.10 | QP093A-0046, QP093A-0049, QP093A-0105 |
| 35 | V4_1_SINGLE_WRITE | 3 | 215.88-216.00 | QP093A-0106, QP093A-0047, QP093A-0050 |
| 36 | V4_1_SINGLE_WRITE | 2 | 360.00-360.42 | QP093A-0052, QP093A-0107 |
| 37 | V4_1_SINGLE_WRITE | 2 | 431.50-432.00 | QP093A-0108, QP093A-0053 |
| 38 | V4_1_SINGLE_WRITE | 2 | 540.00-540.94 | QP093A-0055, QP093A-0109 |
| 39 | V4_1_SINGLE_WRITE | 2 | 646.88-648.00 | QP093A-0110, QP093A-0056 |
| 40 | V4_1_SINGLE_WRITE | 2 | 720.00-721.67 | QP093A-0058, QP093A-0111 |
| 41 | V4_1_SINGLE_WRITE | 2 | 862.00-864.00 | QP093A-0112, QP093A-0059 |

## What CR127 Does NOT Claim

- Per-row falsifiable forward-blind predictions (mass-only is not sufficient; coupling and decay channel must be specified)
- That every HIGH-priority row is testable in 2026 (a HIGH score means STRUCTURALLY test-ready, but the actual experimental analysis must still be performed)
- That clusters represent physical multiplets (could also be SAM-internal degeneracies between similar partition signatures); cluster interpretation is downstream work

## Cryptographic Chain

```text
CR119_courtroom_particle_table_csv        = 5b937d284d6c0b93a5f875acc5fbf63780fd924c90202743865d845fb1d1fc42
CR124_crosswalk_csv                       = 0c8f8b1027ba5f7712ee884d114421e848c35cca5e4741fe387a8a60ad2f9eca

CR127_alp_window_inventory_csv            = 3ae9752151c84aa2c805ee12a235583e8d5c0c47e498ce2a5fba7c87db839879
CR127_priority_manifest_csv               = e62ba3816afaedc97c0f4751992a9bb7e455a443f15556d6e49e6e8e7458552e
CR127_experimental_window_map_json        = 6d13c8f41216a16c74ae97b628956b1962a955b778c867bc913d50213d4c6487
```

## Predictions Checks

- **[PASS]** P1_150_rows_pulled_from_cr124 -- CR124 LIGHT_ALP_WINDOW row count = 150
- **[PASS]** P2_excluded_classes_documented -- excluded statuses = ['CARRIER_ONLY_NOT_MATTER', 'HIDDEN_SUPPORT_NOT_MATTER', 'REJECTED_FAKE_CLOSURE']
- **[PASS]** P3_inventory_size_consistent -- inventory=141, excluded=9, sum=150
- **[PASS]** P4_three_mass_bands_populated -- band counts = {'L0_10to100MeV': 49, 'L1_100to300MeV': 45, 'L2_300to1000MeV': 47}
- **[PASS]** P5_priority_classes_populated -- HIGH=44, MEDIUM=54, LOW=43
- **[PASS]** P6_experimental_window_map_has_active_experiments

## Wrong Controls

- **[PASS]** WC1_CR119_table_unmodified -- CR119 read-only
- **[PASS]** WC2_CR124_crosswalk_unmodified -- 
- **[PASS]** WC3_no_falsifiable_per_row_predictions_committed -- CR127 is a COVERAGE / PRIORITY manifest, not a forward-blind registry.  Mass-only predictions without coupling and channel specification would overpromise.  Per-row forward-blind registry CRs (CR128+) will pick from this manifest and add coupling assumptions + decay-channel commitments before declaring falsifiers.
- **[PASS]** WC4_rejected_fake_closure_filtered -- REJECTED_FAKE_CLOSURE rows (6) excluded from manifest
- **[PASS]** WC5_carrier_rows_filtered -- CARRIER_ONLY_NOT_MATTER and HIDDEN_SUPPORT_NOT_MATTER rows are not matter particles per CR119; excluding them keeps the manifest focused on testable particle candidates
- **[PASS]** WC6_priority_score_documented -- score = +3 (band L0/L1) + 2 (>=3 active expts) + 2 (clean neutral status) + 1 (isolated) - 1 (cluster >= 3); HIGH if >=6, MEDIUM 4-5, LOW <=3
- **[PASS]** WC7_experimental_references_tagged_for_verification -- all experiment references tagged [VERIFY_PRECOMMIT]; promote to verified before any downstream CR cites the manifest as test-ready

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
- Per-row forward-blind registry CRs (CR128+) will pick from this manifest and add coupling/channel commitments
- Experimental reference fields tagged [VERIFY_PRECOMMIT] -- promote to verified before any downstream CR cites the manifest as test-ready
- Structural-cluster interpretation (multiplet vs duplicate) is a separate analysis CR

## Rule of Immutability

Inventory snapshot and priority scoring are locked at CR127 seal time.  Future experimental updates, new reference papers, or refined scoring rules go in a separate child CR.
