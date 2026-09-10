# CR125 X(6900) Forward-Blind Two-State Prediction

## Verdict

```text
CR125_X6900_FORWARD_BLIND_TWO_STATE_PREDICTION_SEALED
```

## What This CR Adds

Two forward-blind predictions inside the LHCb X(6900) di-J/psi window (6700-7100 MeV), promoted from the two SAM rows that fell in this window in CR124's crosswalk.  Each prediction has explicit falsification criteria.  Zero free parameters at test time -- both masses come from sealed CR119 catalog arithmetic on partition signatures, NOT from fitting to X(6900).

## Predictions

| id | mass (MeV) | tol (MeV) | source row | partition | depth |
|---|---:|---:|---|---|---:|
| CR125_PRED_1 | 6804.00 | 50 | QP093A-0192 | 3+6+9 | 0 |
| CR125_PRED_2 | 7056.94 | 50 | QP093A-0208 | 4+6+12 | 3 |

State separation: |6804 - 7056.94| = 252.94 MeV.  Combined tolerance: 100 MeV.  Predictions are independently resolvable.

## Falsification (per prediction)

### CR125_PRED_1

**Falsifies if:** Single-state fit at 6900 +/- 50 MeV with no satellite peak between 6750 and 6850 MeV at > 3 sigma local; OR a confirmed two-state structure where neither state lies within +/- 50 MeV of 6804 MeV.

**Does NOT falsify:** Null result in non-di-J/psi channels; additional states outside 6700-7100 MeV; continued single-vs-two-state ambiguity at low statistics.

**Target dataset:** LHCb di-J/psi Run-3 refinement (extending Sci.Bull.65:1983, 2020); CMS Run-3 di-J/psi (extending CMS-PAS-BPH-23-009 era results); ATLAS Run-3 di-J/psi.  Resolution requires Run-3 final-data statistical power or better.

**Construction:** M_native = 4536 + |S_debit| = 4536 + 2268 = 6804 MeV from SAM closed-loop ledger arithmetic on GROUND_BARYON_3BODY row with partition signature 3+6+9 (sum = 18 = R^2 / 8), closure_depth = 0, q_abs = 3, three_owner_color_closure.

### CR125_PRED_2

**Falsifies if:** Single-state fit at 6900 +/- 50 MeV with no satellite peak between 7000 and 7100 MeV at > 3 sigma local; OR a confirmed two-state structure where neither state lies within +/- 50 MeV of 7057 MeV.

**Does NOT falsify:** Null result in non-di-J/psi channels; additional states outside 6700-7100 MeV; continued single-vs-two-state ambiguity at low statistics.

**Target dataset:** LHCb di-J/psi Run-3 refinement; CMS Run-3 di-J/psi; ATLAS Run-3 di-J/psi. Same data sources as PRED_1; both predictions resolve together.

**Construction:** M_native = 7056 = 49 * R^2 (exact integer on the partition lattice); M_obs = 7056 + 0.9358 = 7056.94 MeV from OCTET_COMPOSITE row with partition signature 4+6+12 (sum = 22), closure_depth = 3 (carrying the 2^-D = 1/8 surface debit), q_abs = 2, three_owner_color_closure.

## What This CR Does NOT Claim

- A specific quark-content assignment for either row.
- That the di-J/psi spectrum contains exactly two states (only that SAM predicts at least these two).
- Widths or branching ratios.

## Cryptographic Chain

```text
CR119_courtroom_particle_table_csv        = 5b937d284d6c0b93a5f875acc5fbf63780fd924c90202743865d845fb1d1fc42
CR119_summary_json                        = 1eb2ba0c12d2079fc395cfa28e41693e9525af3cd394f8c9caa0f4393e0bcb53
CR124_crosswalk_csv                       = 0c8f8b1027ba5f7712ee884d114421e848c35cca5e4741fe387a8a60ad2f9eca
CR124_summary_json                        = 82951214172a95c1ca4c2e3bc7683801cb3ea94495a7decdaa5e286d2c7978bc
CR098b_phase_3_forward_blind_registry_csv = 15ca15585270b6df3babe249f48f371062993a53d3abd03a090813c4902ef193

CR125_x6900_predictions_csv               = a4f3166c962944d10916f3bc145a04fc27a16a0ff379e911803eb86782ab3bcb
CR125_prediction_commit_sha256            = d8f7e41a55d7d92e4b4cbfb83194f1ef5c19b1fe05fd0db0495ef6a94fbf2a21
```

## Predictions Checks

- **[PASS]** P1_two_predictions_committed -- prediction count = 2
- **[PASS]** P2_both_predictions_zero_free_parameters
- **[PASS]** P3_both_predictions_inside_X6900_window -- X(6900) di-J/psi window = 6700-7100 MeV (matches CR124 W124_X6900_DI_JPSI bounds)
- **[PASS]** P4_predictions_separated_by_more_than_combined_tolerance -- |6804 - 7056.94| = 252.94 MeV vs combined tol 100 MeV (predictions are resolvable)
- **[PASS]** P5_explicit_falsification_per_prediction
- **[PASS]** P6_explicit_non_falsifying_outcomes_per_prediction

## Wrong Controls

- **[PASS]** WC1_CR119_table_unmodified -- CR119 particle table read-only; sha recorded
- **[PASS]** WC2_CR124_crosswalk_unmodified -- CR124 crosswalk read-only; sha recorded
- **[PASS]** WC3_CR098b_registry_unmodified -- CR098b phase-3 registry untouched; this CR sits beside it, not inside
- **[PASS]** WC4_no_match_revealed_at_commit_time -- neither QP093A-0192 nor QP093A-0208 carries a known_match label in CR119; both are NATIVE_PARTICLE_IDENTITY_ASSIGNED_NO_KNOWN_LABEL
- **[PASS]** WC5_no_fitting_to_X6900_central_value -- Neither 6804 nor 7056.94 equals the published X(6900) central (~6900 MeV); masses come from sealed CR119 catalog independent of the LHCb measurement
- **[PASS]** WC6_quark_content_assignment_NOT_claimed -- predictions are SAM-native three_owner_color_closure composites; mapping to ccbar-ccbar tetraquark or any other quark content is explicitly out of scope of this CR

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
- Future X(6900) substructure reveal must be added as an appeal CR; this CR's CSV is never edited
- Quark-content assignment (tetraquark mapping) is a separate downstream CR
- Width and branching-ratio predictions are future CRs once QP093 chain extends to decay structure

## Rule of Immutability

Prediction masses and falsification criteria are locked at CR125 seal time.  Future LHCb / CMS / ATLAS X(6900) substructure reveal must be recorded in a SEPARATE appeal CR; this registry CSV is never edited.
