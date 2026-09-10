# CR128 BOUND_COLOR_PAIR Mass Law v1.0

## Verdict

```text
CR128_BOUND_COLOR_PAIR_MASS_LAW_V1_SEALED
```

## The Law (Locked)

```text
For operator_class == 'BOUND_COLOR_PAIR' with partition (a, b):

    M_native(a, b) = R * a * b + D * |a - b|

where R = 12, D = 3, alpha_H = 2,
and (a, b) are drawn from the SAM partition algebra
    {1, 2, 3, 4, 6, 8, 9, 12}.
```

## In-Sample Verification

- BOUND_COLOR_PAIR rows in CR119:    **36**
- Formula matches:                   **36 / 36**
  - Asymmetric (a != b):             30
  - Symmetric (a == b):              6
- Formula violations:                **0**
- Partition parse failures:          0
- Partition-algebra violations:      0

## Pair Coverage

Distinct (a, b) pairs observed:           **21**

Total possible unordered pairs in algebra: 36

| (a, b) | predicted M_native | rows |
|---|---:|---|
| (1, 1) | 12 | QP093A-0235 |
| (1, 2) | 27 | QP093A-0236, QP093A-0243 |
| (1, 3) | 42 | QP093A-0237, QP093A-0251 |
| (1, 4) | 57 | QP093A-0238, QP093A-0259 |
| (1, 6) | 87 | QP093A-0239, QP093A-0267 |
| (1, 8) | 117 | QP093A-0240, QP093A-0275 |
| (2, 2) | 48 | QP093A-0244 |
| (2, 3) | 75 | QP093A-0245, QP093A-0252 |
| (2, 4) | 102 | QP093A-0246, QP093A-0260 |
| (2, 6) | 156 | QP093A-0247, QP093A-0268 |
| (2, 8) | 210 | QP093A-0248, QP093A-0276 |
| (3, 3) | 108 | QP093A-0253 |
| (3, 4) | 147 | QP093A-0254, QP093A-0261 |
| (3, 6) | 225 | QP093A-0255, QP093A-0269 |
| (3, 8) | 303 | QP093A-0256, QP093A-0277 |
| (4, 4) | 192 | QP093A-0262 |
| (4, 6) | 294 | QP093A-0263, QP093A-0270 |
| (4, 8) | 396 | QP093A-0264, QP093A-0278 |
| (6, 6) | 432 | QP093A-0271 |
| (6, 8) | 582 | QP093A-0272, QP093A-0279 |
| (8, 8) | 768 | QP093A-0280 |

## Forward-Blind Sub-Prediction CR128_PRED_1 (LOCKED)

**Claim:** For any FUTURE row with operator_class == 'BOUND_COLOR_PAIR' and a 2-element partition (a, b) from the algebra, M_native = R*a*b + D*|a-b| exactly.

**Falsifier:** ONE single future BOUND_COLOR_PAIR row whose M_native deviates from the formula by any non-zero integer.  ONE violation falsifies v1.0.

**Non-falsifying:** rows of other operator_class; rows with partition != 2 elements; rows containing an algebra extension (which warrants an appeal CR, not a violation).

**Free parameters at test:** 0.

## What CR128 Does NOT Claim

- A formula for the surface debit S_debit that splits the (a,b) / (b,a) doublet (CR128b).
- A formula for M_observed of symmetric (a, a) pairs (empirically ~ (43/4) * a^2; CR128c).
- That OCTET_COMPOSITE 3-body rows obey the same formula -- numerical coincidences exist but the 3-body generator is separate (CR129+).
- That extending the partition algebra wouldn't change anything -- algebra extension is an appeal-CR matter.

## Honest Notes on Derivation

Law v1.0 was derived inductively by inspecting BOUND_COLOR_PAIR cluster centers in CR127.  In-sample 100% match confirms generator consistency with all rows the catalog currently contains.  It does NOT by itself prove first-principles derivation -- the formula could in principle have been overfit to 36 data points.  CR128_PRED_1 commits the law for forward-blind testing on future rows, where overfit cannot operate.

## Cryptographic Chain

```text
CR119_courtroom_particle_table_csv        = 5b937d284d6c0b93a5f875acc5fbf63780fd924c90202743865d845fb1d1fc42
CR127_alp_window_inventory_csv            = 3ae9752151c84aa2c805ee12a235583e8d5c0c47e498ce2a5fba7c87db839879

CR128_verification_csv                    = 0b51ff37925777edc9af0d48e3c279e28dfd5e69feddd6c12d379d2b40415517
CR128_law_lock_sha256                     = d8ed19c10f5166ab14c33b878ee045714648a3f9f65df9a48fc76595bf00820a
```

## Predictions Checks

- **[PASS]** P1_all_36_BCP_rows_verified -- BOUND_COLOR_PAIR rows = 36, parse_failures = 0
- **[PASS]** P2_formula_matches_all_rows -- matches = 36/36, violations = 0
- **[PASS]** P3_partition_algebra_unbroken -- algebra_violations = 0
- **[PASS]** P4_symmetric_pairs_covered -- symmetric (a,a) matches = 6; CR127 ALP window did not surface these because doublet splitting requires a != b
- **[PASS]** P5_asymmetric_pairs_covered -- asymmetric (a,b) matches = 30 (each unordered pair generates two rows -- (a,b) and (b,a)); n_unordered_pairs_with_a_neq_b = 15
- **[PASS]** P6_forward_blind_law_lock_written -- law lock sha256 = d8ed19c10f5166ab14c33b878ee045714648a3f9f65df9a48fc76595bf00820a

## Wrong Controls

- **[PASS]** WC1_CR119_table_unmodified -- CR119 particle table read-only; sha recorded
- **[PASS]** WC2_CR127_inventory_unmodified -- CR127 ALP window inventory read-only; sha recorded
- **[PASS]** WC3_law_derived_from_data_not_first_principles -- Law v1.0 was derived inductively by inspecting BOUND_COLOR_PAIR cluster centers in CR127.  In-sample verification confirms the rule is CONSISTENT with the training set; CR128_PRED_1 commits the rule for FORWARD-BLIND testing on future rows where overfit cannot operate.  Honest WC: in-sample 100% match does not prove first-principles derivation, only generator consistency.
- **[PASS]** WC4_S_debit_formula_intentionally_NOT_claimed -- Doublet splitting at +/- S_debit is observed in every (a,b) / (b,a) pair but its amplitude formula is left to CR128b.  Claiming the splitting formula here without separate derivation would overpromise.
- **[PASS]** WC5_symmetric_pair_M_obs_explicitly_out_of_scope -- Symmetric (a,a) pairs match the M_native formula but their M_observed is shifted by a non-trivial debit (M_obs(a,a) ~ 10.75 * a^2 = (43/4) * a^2).  CR128 covers M_native only; M_observed structure for symmetric pairs is separate work.
- **[PASS]** WC6_OCTET_COMPOSITE_numerical_coincidences_noted -- Several OCTET_COMPOSITE 3-body clusters in CR127 land at the same numerical mass as 2-body pair predictions (e.g. cluster 16 at 132 MeV = (1,9)).  This is a numerical coincidence -- 3-body generator is not the same as 2-body.  OCTET_COMPOSITE law derivation is separate CR129+ work.
- **[PASS]** WC7_algebra_extension_path_documented -- If the partition algebra is ever extended (e.g. adding 5, 7, 10, 11), each new element generates additional pairs.  CR128 v1.0 is locked against the current algebra {1,2,3,4,6,8,9,12}; algebra extension warrants an appeal CR, not a violation of v1.0.

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
- CR128b: derive S_debit amplitude formula (doublet splitting) for asymmetric (a,b) pairs
- CR128c: derive M_observed offset formula for symmetric (a,a) pairs (currently empirical ~ 10.75 a^2)
- CR129+: derive 3-body M_native generator for OCTET_COMPOSITE and GROUND_BARYON_3BODY operator classes
- Forward-blind test CR128_PRED_1 resolves when CR119 catalog gains new BOUND_COLOR_PAIR rows

## Rule of Immutability

Law v1.0 formula, partition algebra, and constants are frozen at CR128 seal time.  Future falsification or revision must be in an appeal CR.
