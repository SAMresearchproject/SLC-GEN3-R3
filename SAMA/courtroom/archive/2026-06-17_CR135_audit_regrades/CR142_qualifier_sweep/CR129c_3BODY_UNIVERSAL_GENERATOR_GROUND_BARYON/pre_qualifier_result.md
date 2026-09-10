# CR129c 3-Body Universal Generator (GROUND_BARYON_3BODY Extension)

> **AUDIT-DRIVEN DEFECT CORRECTION — 2026-06-17 PER CR-141**
>
> The `CR129c_universal_lock_sha256` field in this file was corrected from `d823faba...8263d34` to `bfd5ab8c...1bd8090` to match the actual SHA-256 of the lock JSON on disk. Root cause: runner self-reference artifact (hash computed before being embedded in the lock JSON). The defect was confined to the recorded self-citation; downstream CRs carried the correct value.
>
> The verdict `CR129c_3BODY_UNIVERSAL_GENERATOR_SEALED` is **unchanged**. The underlying claim, the in-sample row matches, the partition algebra, the forward-blind sub-prediction, and the wrong controls all stand verbatim.
>
> - Original archived at: `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR129c_3BODY_UNIVERSAL_GENERATOR_GROUND_BARYON/original_result.md`
> - Original SHA-256: `b37cb070b8880de7c8fb511e8106279dd4a1f365039262cd61592152bce80929`
> - Replacement record: `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR129c_3BODY_UNIVERSAL_GENERATOR_GROUND_BARYON/REPLACEMENT_RECORD.md`
> - Driving audit: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (verdict SHA-256 `2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661`)


## Verdict

```text
CR129c_3BODY_UNIVERSAL_GENERATOR_SEALED
```

## Promotion

CR129 locked the formula M = R*D*(a^2+b^2+c^2) for OCTET_COMPOSITE 3-body rows (76 rows).  CR129c tests the same formula on GROUND_BARYON_3BODY rows (44 rows, including 13 REJECTED_FAKE_CLOSURE).  Result: 44/44 match.  The formula is now promoted from operator-class-specific to **UNIVERSAL 3-BODY**.

```text
Universal 3-body M_native generator:

    M_native(a, b, c)  =  R * D * (a^2 + b^2 + c^2)
                       =  36 * (a^2 + b^2 + c^2)

for ANY 3-element partition (a, b, c) from the SAM partition algebra,
REGARDLESS of operator_class or stability_status.
```

## Combined Coverage (CR129 + CR129c)

| operator_class | rows | matches | violations |
|---|---:|---:|---:|
| OCTET_COMPOSITE (3-body)  | 76 | 76 | 0 |
| GROUND_BARYON_3BODY       | 44 | 44 | 0 |
| **combined 3-body**       | **120** | **120** | **0** |
| total 3-body in CR119     | 120 | -- | -- |

Coverage: **120/120** = 100%.

## Key Finding: REJECTED_FAKE_CLOSURE Rows ALSO Match

| stability_status | matches | violations |
|---|---:|---:|
| BOUND_COLOR_CLOSED_HEAVY_CANDIDATE | 17 | 0 |
| BOUND_COLOR_CLOSED_STABLE_CANDIDATE | 14 | 0 |
| REJECTED_FAKE_CLOSURE | 13 | 0 |

13 of 13 REJECTED_FAKE_CLOSURE rows in GROUND_BARYON_3BODY match the formula.  This is the structural reveal: **SAM's M_native formula GENERATES every candidate row from the partition algebra.  The stability_status filter (qA support, color closure, write retention) is DOWNSTREAM** -- it decides which generated candidates are physically real, but it does not affect the M_native value itself.

Interpretation:

- **Generator** (M_native formula): produces every (a, b, c) with mass R*D*(a^2+b^2+c^2)
- **Filter** (stability_status): rejects generated rows that fail physicality (qA = 0, no color closure, no write retention)

The two are structurally separable.  A REJECTED row at M = 8748 MeV (e.g. (9,9,9) GROUND_BARYON) is not a 'wrong prediction' -- it is a structurally-valid mass value that the framework declines to promote to a physical state.

## Sample Verification (first 20 rows)

| candidate | (a,b,c) | a²+b²+c² | predicted | observed | stability | match |
|---|---|---:|---:|---:|---|:-:|
| QP093A-0115 | (1,1,1) | 3 | 108 | 108 | BOUND_COLOR_CLOSED_STABLE_CANDIDATE | YES |
| QP093A-0118 | (1,1,4) | 18 | 648 | 648 | BOUND_COLOR_CLOSED_STABLE_CANDIDATE | YES |
| QP093A-0124 | (1,2,3) | 14 | 504 | 504 | BOUND_COLOR_CLOSED_STABLE_CANDIDATE | YES |
| QP093A-0126 | (1,2,6) | 41 | 1476 | 1476 | BOUND_COLOR_CLOSED_STABLE_CANDIDATE | YES |
| QP093A-0128 | (1,2,9) | 86 | 3096 | 3096 | BOUND_COLOR_CLOSED_HEAVY_CANDIDATE | YES |
| QP093A-0129 | (1,2,12) | 149 | 5364 | 5364 | BOUND_COLOR_CLOSED_HEAVY_CANDIDATE | YES |
| QP093A-0133 | (1,3,8) | 74 | 2664 | 2664 | REJECTED_FAKE_CLOSURE | YES |
| QP093A-0136 | (1,4,4) | 33 | 1188 | 1188 | BOUND_COLOR_CLOSED_STABLE_CANDIDATE | YES |
| QP093A-0142 | (1,6,8) | 101 | 3636 | 3636 | BOUND_COLOR_CLOSED_STABLE_CANDIDATE | YES |
| QP093A-0146 | (1,8,9) | 146 | 5256 | 5256 | BOUND_COLOR_CLOSED_HEAVY_CANDIDATE | YES |
| QP093A-0147 | (1,8,12) | 209 | 7524 | 7524 | BOUND_COLOR_CLOSED_HEAVY_CANDIDATE | YES |
| QP093A-0151 | (2,2,2) | 12 | 432 | 432 | BOUND_COLOR_CLOSED_STABLE_CANDIDATE | YES |
| QP093A-0155 | (2,2,8) | 72 | 2592 | 2592 | BOUND_COLOR_CLOSED_STABLE_CANDIDATE | YES |
| QP093A-0159 | (2,3,4) | 29 | 1044 | 1044 | REJECTED_FAKE_CLOSURE | YES |
| QP093A-0165 | (2,4,6) | 56 | 2016 | 2016 | BOUND_COLOR_CLOSED_STABLE_CANDIDATE | YES |
| QP093A-0167 | (2,4,9) | 101 | 3636 | 3636 | BOUND_COLOR_CLOSED_HEAVY_CANDIDATE | YES |
| QP093A-0168 | (2,4,12) | 164 | 5904 | 5904 | BOUND_COLOR_CLOSED_HEAVY_CANDIDATE | YES |
| QP093A-0173 | (2,8,8) | 132 | 4752 | 4752 | BOUND_COLOR_CLOSED_STABLE_CANDIDATE | YES |
| QP093A-0179 | (3,3,3) | 27 | 972 | 972 | REJECTED_FAKE_CLOSURE | YES |
| QP093A-0181 | (3,3,6) | 54 | 1944 | 1944 | REJECTED_FAKE_CLOSURE | YES |

(full 44-row verification in `CR129c_verification.csv`)

## Forward-Blind Sub-Prediction CR129c_PRED_1 (LOCKED)

**Claim:** For any FUTURE 3-element partition (a, b, c) from the algebra, regardless of operator_class or stability_status, M_native = R*D*(a^2+b^2+c^2) = 36*(a^2+b^2+c^2) exactly.

**Falsifier:** ONE future 3-body row whose M_native differs from the formula by any non-zero integer.  ONE violation falsifies the universal claim.

**Non-falsifying:** rows with partition size != 3; algebra extensions.

**Free parameters at test:** 0.

## Cryptographic Chain

```text
CR119_courtroom_particle_table_csv        = 5b937d284d6c0b93a5f875acc5fbf63780fd924c90202743865d845fb1d1fc42
CR129_law_lock_json                       = 041a487c30a8ee3d96dbf347e26e110c2808741b325769a910217d8bcfbeb710
CR129_verification_csv                    = abe8df7fe3d752accbe115728d53d3f8fa2c256c3ca7f1d3dd0bdb56358378df

CR129c_verification_csv                   = ad7ea656ef3da66863c7f0c7e6a6005f9cc58dfac9bf707f3259128e5d0fb53c
CR129c_universal_lock_sha256              = bfd5ab8c325656ffd3c34c88ab90bb0d1c486046241cf6a07c07506441bd8090
```

## Predictions Checks

- **[PASS]** P1_all_44_GROUND_BARYON_rows_walked -- verifications = 44, parse_failures = 0
- **[PASS]** P2_all_GROUND_BARYON_rows_match_formula -- matches = 44/44, violations = 0
- **[PASS]** P3_REJECTED_FAKE_CLOSURE_rows_also_match -- REJECTED_FAKE_CLOSURE: 13 matches, 0 violations
- **[PASS]** P4_combined_3body_coverage_complete -- OCTET 3-body (CR129): 76 rows.  GROUND_BARYON_3BODY (CR129c): 44 rows.  Combined: 120 of 120 3-body rows in CR119.  Combined violations: 0.
- **[PASS]** P5_partition_algebra_unbroken -- algebra_violations = 0
- **[PASS]** P6_universal_lock_written -- universal lock sha256 = bfd5ab8c325656ffd3c34c88ab90bb0d1c486046241cf6a07c07506441bd8090

## Wrong Controls

- **[PASS]** WC1_CR119_table_unmodified -- CR119 read-only
- **[PASS]** WC2_CR129_law_lock_unmodified -- CR129 law lock referenced but not modified; CR129c promotes without overriding
- **[PASS]** WC3_REJECTED_rows_explicitly_included_in_test -- 13 REJECTED_FAKE_CLOSURE rows in GROUND_BARYON_3BODY are INCLUDED in this test (not filtered out).  Their matching the formula is the key finding -- it shows M_native generation is upstream of stability filtering.
- **[PASS]** WC4_formula_NOT_promoted_to_other_body_counts -- Universal claim is restricted to 3-body partitions.  CR128 BCP 2-body (M = R*ab + D*|a-b|) remains the 2-body law.  CR130 documents the structural break at n=2 vs n>=3.  CR129c does NOT extend the formula to 1-body, 2-body, or 4-body rows.
- **[PASS]** WC5_law_derived_from_data_not_first_principles -- The universal 3-body claim is derived from 120 in-sample rows.  CR129c_PRED_1 commits the law for forward-blind testing on FUTURE 3-body rows where overfit cannot operate.
- **[PASS]** WC6_other_3body_operator_classes_open -- If any future operator_class with 3-element partitions is added (e.g. a new exotic-state class), the universal claim predicts it will also obey the formula.  One violation triggers an appeal CR; absence of such classes does not falsify.

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
- S_debit formula for GROUND_BARYON_3BODY rows is open (S_debit values vary substantially across rows; CR129b would address this)
- Why M_native generates valid mass values even on REJECTED_FAKE_CLOSURE rows is a structural question -- the generator/filter separation is observed but not derived
- Forward-blind CR129c_PRED_1 resolves when CR119 gains new 3-body rows in any operator class

## Rule of Immutability

Universal 3-body M_native formula is frozen at CR129c seal time.  Future falsification or refinement must be in an appeal CR.
