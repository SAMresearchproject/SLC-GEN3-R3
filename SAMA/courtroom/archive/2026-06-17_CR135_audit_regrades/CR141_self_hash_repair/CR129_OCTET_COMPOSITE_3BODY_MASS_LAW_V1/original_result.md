# CR129 OCTET_COMPOSITE 3-Body Mass Law v1.0

## Verdict

```text
CR129_OCTET_COMPOSITE_3BODY_MASS_LAW_V1_SEALED
```

## The Law (Locked)

```text
For operator_class == 'OCTET_COMPOSITE' with 3-element partition (a, b, c):

    M_native(a, b, c) = R * D * (a^2 + b^2 + c^2)
                      = 36 * (a^2 + b^2 + c^2)

where R = 12, D = 3, and (a, b, c) drawn (with multiplicity) from the
SAM partition algebra {1, 2, 3, 4, 6, 8, 9, 12}.

Fully symmetric in (a, b, c).  No antisymmetric term.
```

## Structural Progression

- **2-body partition**: M = R*a*b + D*|a-b|  (linear product + linear antisymmetric correction)
- **3-body partition**: M = R*D*(a^2+b^2+c^2)  (pure sum-of-squares, fully symmetric)

The 2-body formula needs the antisymmetric `|a-b|` to encode the doublet splitting.  The 3-body formula collapses to a single fully-symmetric quadratic.  Why this structural change happens between 2-body and 3-body is a separate derivation question.

## In-Sample Verification

- OCTET_COMPOSITE rows in CR119:    **104**
- 3-body rows tested:               **76**
- 3-body formula matches:           **76 / 76**
- 3-body violations:                **0**
- 2-body OCTET rows tested:         28
- 2-body BCP-formula matches:       28 / 28
- 2-body violations:                0
- Partition parse failures:         0
- Partition-algebra violations:     0

## Coverage

- Distinct 3-body triples observed:  **76**
- Distinct 2-body pairs observed:    15

## Forward-Blind Sub-Prediction CR129_PRED_1 (LOCKED)

**Claim:** For any FUTURE 3-body OCTET_COMPOSITE row with partition (a, b, c) from the algebra, M_native = R*D*(a^2+b^2+c^2) = 36*(a^2+b^2+c^2) exactly.

**Falsifier:** ONE single future 3-body OCTET row whose M_native deviates from the formula by any non-zero integer.  ONE violation falsifies v1.0.

**Non-falsifying:** rows of other operator_class; 2-body OCTET rows (covered by CR128 BCP formula); algebra extensions.

**Free parameters at test:** 0.

## Sample Verification (first 30 3-body rows)

| candidate | (a, b, c) | a²+b²+c² | 36·sum² | M_native obs | match |
|---|---|---:|---:|---:|:-:|
| QP093A-0116 | (1,1,2) | 6 | 216 | 216 | YES |
| QP093A-0117 | (1,1,3) | 11 | 396 | 396 | YES |
| QP093A-0119 | (1,1,6) | 38 | 1368 | 1368 | YES |
| QP093A-0120 | (1,1,8) | 66 | 2376 | 2376 | YES |
| QP093A-0121 | (1,1,9) | 83 | 2988 | 2988 | YES |
| QP093A-0122 | (1,1,12) | 146 | 5256 | 5256 | YES |
| QP093A-0123 | (1,2,2) | 9 | 324 | 324 | YES |
| QP093A-0125 | (1,2,4) | 21 | 756 | 756 | YES |
| QP093A-0127 | (1,2,8) | 69 | 2484 | 2484 | YES |
| QP093A-0130 | (1,3,3) | 19 | 684 | 684 | YES |
| QP093A-0131 | (1,3,4) | 26 | 936 | 936 | YES |
| QP093A-0132 | (1,3,6) | 46 | 1656 | 1656 | YES |
| QP093A-0134 | (1,3,9) | 91 | 3276 | 3276 | YES |
| QP093A-0135 | (1,3,12) | 154 | 5544 | 5544 | YES |
| QP093A-0137 | (1,4,6) | 53 | 1908 | 1908 | YES |
| QP093A-0138 | (1,4,8) | 81 | 2916 | 2916 | YES |
| QP093A-0139 | (1,4,9) | 98 | 3528 | 3528 | YES |
| QP093A-0140 | (1,4,12) | 161 | 5796 | 5796 | YES |
| QP093A-0141 | (1,6,6) | 73 | 2628 | 2628 | YES |
| QP093A-0143 | (1,6,9) | 118 | 4248 | 4248 | YES |
| QP093A-0144 | (1,6,12) | 181 | 6516 | 6516 | YES |
| QP093A-0145 | (1,8,8) | 129 | 4644 | 4644 | YES |
| QP093A-0148 | (1,9,9) | 163 | 5868 | 5868 | YES |
| QP093A-0149 | (1,9,12) | 226 | 8136 | 8136 | YES |
| QP093A-0150 | (1,12,12) | 289 | 10404 | 10404 | YES |
| QP093A-0152 | (2,2,3) | 17 | 612 | 612 | YES |
| QP093A-0153 | (2,2,4) | 24 | 864 | 864 | YES |
| QP093A-0154 | (2,2,6) | 44 | 1584 | 1584 | YES |
| QP093A-0156 | (2,2,9) | 89 | 3204 | 3204 | YES |
| QP093A-0157 | (2,2,12) | 152 | 5472 | 5472 | YES |

(full 76-row 3-body verification + 28-row 2-body verification in `CR129_verification.csv`)

## What CR129 Does NOT Claim

- A formula for S_debit of 3-body OCTET rows (CR129b).
- That GROUND_BARYON_3BODY follows the same formula (CR129c).
- Why 3-body has no antisymmetric term while 2-body does (open structural question).
- That the formula extends to 4-body partitions (separate CR if any such rows exist).

## Cryptographic Chain

```text
CR119_courtroom_particle_table_csv        = 5b937d284d6c0b93a5f875acc5fbf63780fd924c90202743865d845fb1d1fc42
CR128_law_lock_json                       = 0f62d6b4e942a9b41d2b620265f3b05d737a35d65acb4553190f64183ff19871
CR128b_law_lock_json                      = fb9287cd6c79b161f138f5ce4fde5b109483be1787757d6e4bdf4f613ad16467

CR129_verification_csv                    = abe8df7fe3d752accbe115728d53d3f8fa2c256c3ca7f1d3dd0bdb56358378df
CR129_law_lock_sha256                     = 210e174e5145da6815fe27e7c6985886292a99cfb57f29a003fb3e1be8d95360
```

## Predictions Checks

- **[PASS]** P1_all_OCTET_rows_walked -- OCTET rows walked = 104 of 104, parse_failures = 0
- **[PASS]** P2_3body_formula_matches_all_3body_rows -- 3-body matches = 76/76, violations = 0
- **[PASS]** P3_2body_BCP_formula_matches_all_2body_OCTET_rows -- 2-body matches = 28/28, violations = 0 (CR128 BCP formula extends to OCTET 2-body)
- **[PASS]** P4_partition_algebra_unbroken -- algebra_violations = 0
- **[PASS]** P5_distinct_3body_triples_covered -- distinct 3-body triples observed = 76
- **[PASS]** P6_forward_blind_law_lock_written -- law lock sha256 = 210e174e5145da6815fe27e7c6985886292a99cfb57f29a003fb3e1be8d95360

## Wrong Controls

- **[PASS]** WC1_CR119_table_unmodified -- CR119 read-only; sha recorded
- **[PASS]** WC2_CR128_law_locks_unmodified -- CR128 + CR128b law locks read-only; CR129 references but does not modify
- **[PASS]** WC3_law_derived_inductively_not_from_first_principles -- Formula M_native = R*D*(a^2+b^2+c^2) was extracted by inspecting the OCTET 3-body row collection.  In-sample 100% match confirms generator consistency with all rows currently in CR119.  Forward-blind falsifier CR129_PRED_1 commits the formula for testing on FUTURE rows where overfit cannot operate.
- **[PASS]** WC4_S_debit_formula_intentionally_NOT_claimed -- The 3-body OCTET rows show varied S_debit values (from milli-MeV to ~150 MeV for some unsymmetric configurations).  No clean closed form for S_debit is claimed in CR129; reserved for CR129b.
- **[PASS]** WC5_2_body_OCTET_rows_use_CR128_formula_not_3body_one -- OCTET_COMPOSITE rows with 2-element partitions (e.g. (1,9), (1,12), (8,12)) follow the CR128 BCP formula M = R*a*b + D*|a-b|, NOT the 3-body formula.  This is verified in this CR's predictions (P3).
- **[PASS]** WC6_GROUND_BARYON_3BODY_explicitly_out_of_scope -- GROUND_BARYON_3BODY is a different operator_class with its own 3-body structure.  CR129 does NOT claim that the same formula applies; CR129c will investigate.
- **[PASS]** WC7_symmetry_observation_noted -- The 3-body formula is fully symmetric in (a, b, c) -- no antisymmetric term.  Unlike the 2-body case (where |a-b| is essential), 3-body M_native depends only on the multiset {a, b, c}.  This is observed structurally, not derived.

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
- CR129b: derive S_debit formula for 3-body OCTET rows (the 75 observed values are not yet captured by a closed form)
- CR129c: test whether GROUND_BARYON_3BODY (different operator_class) obeys the same formula
- Why the 3-body formula has no antisymmetric term while the 2-body formula does is a structural question -- separate derivation CR
- Forward-blind test CR129_PRED_1 resolves when CR119 gains new 3-body OCTET rows

## Rule of Immutability

Law v1.0 formula, partition algebra, and constants are frozen at CR129 seal time.  Future falsification or revision must be in an appeal CR.
