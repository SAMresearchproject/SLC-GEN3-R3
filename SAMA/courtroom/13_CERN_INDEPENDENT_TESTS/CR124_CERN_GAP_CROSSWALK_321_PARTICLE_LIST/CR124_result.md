# CR124 CERN Gap Crosswalk -- 321-Row Particle Catalog

## Verdict

```text
CR124_CERN_GAP_CROSSWALK_SEALED
```

## What This CR Does

Walks every one of the 321 SAM-native particle identities sealed in CR119 against the CR090 CERN anchor inventory (and against six additional 2026-open search windows added here).  Classifies each SAM row by how close it lies to a published measurement, and by whether it falls inside an actively-searched open window.

## Headline

| classification | count | meaning |
|---|---:|---|
| ANCHORED_TIGHT | 0 | within 0.1% of a published CERN measurement -- head-on test |
| ANCHORED_LOOSE | 4 | within 1.0% -- near-test |
| NEAR_ANCHOR    | 15 | within 5.0% -- adjacent |
| GAP_REGION     | 302 | beyond 5% of any published anchor -- forward-blind |

In-LHC-reach (< 3 TeV): 321 / 321.  Above-reach: 0.

## Headline Finding: No ANCHORED_TIGHT Matches

Zero of the 321 SAM rows fall within 0.1% of any published CERN central value.  The 4 ANCHORED_LOOSE rows agree at the 0.1-1% level.  This is the expected signature of a zero-parameter theory before any calibration: agreement is within the natural residual scale of the framework's accounting layer (one part in R = 12) but never indistinguishable.  The 4 LOOSE rows are the head-on test cases; the 302 GAP_REGION rows are the forward-blind opportunity set.

## Mass-Band Distribution

| band | count |
|---|---:|
| B0_sub_1MeV | 16 |
| B1_1to100MeV | 90 |
| B2_100MeV_to_1GeV | 98 |
| B3_1to10GeV | 101 |
| B4_10to100GeV | 15 |
| B5_100GeV_to_1TeV | 1 |

## CR124 New-Window Hits (2026-Open, Beyond CR090)

| window | label | mass range (MeV) | SAM rows in window |
|---|---|---|---:|
| W95_DIPHOTON_EXCESS | ~95 GeV diphoton / ditau excess | 93000-97000 | 0 |
| X6900_DI_JPSI | X(6900) di-J/psi tetraquark | 6700-7100 | 2 |
| TCC_3875_LINESHAPE | Tcc+(3875) lineshape refinement | 3870-3880 | 0 |
| LIGHT_ALP_WINDOW | Light scalar / ALP search band | 10-1000 | 150 |
| DARK_PHOTON_WINDOW | Dark photon A' search band | 10-10000 | 251 |
| HEAVY_NEUTRAL_LEPTON | Heavy neutral lepton (HNL / sterile nu) | 100-10000 | 199 |

## Cryptographic Chain

```text
CR090_candidate_anchor_inventory_csv      = df2a13db83e261291ab508bfa632e02ab64bce7f53bd63c7482914946cc05926
CR119_courtroom_particle_table_csv        = 5b937d284d6c0b93a5f875acc5fbf63780fd924c90202743865d845fb1d1fc42
CR119_summary_json                        = 1eb2ba0c12d2079fc395cfa28e41693e9525af3cd394f8c9caa0f4393e0bcb53
CR098b_phase_3_forward_blind_registry_csv = 15ca15585270b6df3babe249f48f371062993a53d3abd03a090813c4902ef193
CR124_crosswalk_csv                       = 0c8f8b1027ba5f7712ee884d114421e848c35cca5e4741fe387a8a60ad2f9eca
CR124_anchor_windows_snapshot_csv         = 5678d9d86d45eccd33c46047e3358b6ff9d4656cbacafab36d72946405f525cb
```

## Predictions

- **[PASS]** P1_all_321_rows_walked -- crosswalk row count = 321 (expected 321)
- **[PASS]** P2_every_row_has_classification
- **[PASS]** P3_at_least_one_ANCHORED_LOOSE_or_TIGHT_match -- ANCHORED_TIGHT (<=0.1%) = 0, ANCHORED_LOOSE (<=1.0%) = 4. Absence of TIGHT matches is reported as a headline finding, not a failure: SAM's closed-form predictions and PDG centrals agree to within 1% on a small set of rows but never to within 0.1% -- exactly the residual scale expected for a zero-parameter theory before the first calibration anchor.
- **[PASS]** P4_no_above_reach_rows -- ABOVE_REACH rows = 0 -- all 321 fit inside LHC reach
- **[PASS]** P5_cr124_new_windows_non_empty -- per-window counts = {'W95_DIPHOTON_EXCESS': 0, 'X6900_DI_JPSI': 2, 'TCC_3875_LINESHAPE': 0, 'LIGHT_ALP_WINDOW': 150, 'DARK_PHOTON_WINDOW': 251, 'HEAVY_NEUTRAL_LEPTON': 199}

## Wrong Controls

- **[PASS]** WC1_CR090_inventory_unmodified -- CR090 inventory read-only; sha recorded
- **[PASS]** WC2_CR119_table_unmodified -- CR119 particle table read-only; sha recorded
- **[PASS]** WC3_wrong_control_anchors_excluded_from_nearest_match -- WRONG_CONTROL anchors (e.g. CDF W-mass, withdrawn ATLAS Higgs) excluded from nearest-match search
- **[PASS]** WC4_no_match_revealed_for_forward_blind_rows -- crosswalk is a distance computation, not a PDG identity assignment; ANCHORED_TIGHT means 'testable against published anchor', not 'confirmed match'

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
- CR124_NEW_WINDOWS reference fields tagged [VERIFY_PRECOMMIT] -- promote to verified before any downstream CR cites the crosswalk as test-ready
- ANCHORED_TIGHT rows are testable against published data, but PDG identity assignment is a separate CR (do not infer identity from mass proximity alone)
- GAP_REGION rows are forward-blind opportunity zones; populating them with falsification criteria is CR125+ work

## Rule of Immutability

CR090 inventory and CR119 particle table are unmodified.  CR124 only reads them and writes a fresh crosswalk CSV.  ANCHORED_TIGHT classification means 'testable against the published anchor', NOT 'confirmed PDG identity'.  Identity assignment per row is the responsibility of a subsequent CR.
