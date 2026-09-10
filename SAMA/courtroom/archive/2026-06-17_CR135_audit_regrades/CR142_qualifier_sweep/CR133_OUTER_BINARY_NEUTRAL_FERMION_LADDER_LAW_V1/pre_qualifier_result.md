# CR133 OUTER_BINARY_NEUTRAL Neutral-Fermion Ladder Law v1.0

> **AUDIT-DRIVEN DEFECT CORRECTION — 2026-06-17 PER CR-141**
>
> The `CR133_law_lock_sha256` field in this file was corrected from `3adf93b8...f0f8cee` to `1e7e08d8...ddcf1e4` to match the actual SHA-256 of the lock JSON on disk. Root cause: runner self-reference artifact (hash computed before being embedded in the lock JSON). The defect was confined to the recorded self-citation; downstream CRs carried the correct value.
>
> The verdict `CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1_SEALED` is **unchanged**. The underlying claim, the in-sample row matches, the partition algebra, the forward-blind sub-prediction, and the wrong controls all stand verbatim.
>
> - Original archived at: `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1/original_result.md`
> - Original SHA-256: `8b02eb267930bd04ab7500ec54395dc26e50d060e8e20c43594152066c1861bf`
> - Replacement record: `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1/REPLACEMENT_RECORD.md`
> - Driving audit: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (verdict SHA-256 `2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661`)


## Verdict

```text
CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1_SEALED
```

## Answer to the Framing Question

**Do we get lucky with the same C1 = 1?**  NO -- we get lucky with the same *architecture* but K = 1/8, not C1 = 1.

OUTER_BINARY_NEUTRAL obeys the same formula shape as V4_1 (M = ladder_input · R^depth · K), but K = 1/8 = 2⁻ᴰ instead of (5/4 or 3/2).  Neutral fermions sit at the bare bounce factor with NO +1 inhomogeneity in the K coefficient.

## The Law (Locked)

```text
For operator_class == 'OUTER_BINARY_NEUTRAL':

                                   1                       partition * R^depth
  M_native  =  partition * R^depth * ---  =  partition * 2^-D * R^depth  =  -------------------
                                   8                              8

  where R = 12, D = 3, alpha_H = 2,  K = 1/alpha_H^3 = 1/8 = 2^-D
  Partition values: {1, 2, 3, 4, 6, 8, 9, 12}
  Closure depths observed: {0, 1, 2}
  S_debit = 0 universally
```

## Unified 1-Body Fermion Ladder Reading (CR131 + CR133)

Both fermion families obey `M = (charge-or-partition) · R^closure_depth · K`:

| class | K | structural | example |
|---|---|---|---|
| V4_1 matter positive | 5/4 | (α_H² + 1) / α_H² | q=1 d=0 → 1.25 |
| V4_1 matter negative | 3/2 | (α_H + 1) / α_H   | q=1 d=0 → 1.5 |
| V4_1 antimatter positive | 3/2 | sign-flipped twin | q=1 d=0 → 1.5 |
| V4_1 antimatter negative | 5/4 | sign-flipped twin | q=1 d=0 → 1.25 |
| **OUTER_BINARY_NEUTRAL** | **1/8** | **2⁻ᴰ = 1/α_H³** | **part=1 d=0 → 0.125** |

Three K-families cover all 114 (90 + 24) 1-body fermion_half_write rows.  Charged fermions take `(1 + 1/α_H^k)` for k = 1 or 2; neutral fermions take the bare `1/α_H³`.

## In-Sample Verification

- OUTER_BINARY_NEUTRAL rows tested:  **24**
- Formula matches:                    **24 / 24**
- S_debit = 0:                        **24 / 24**
- Violations:                         **0**
- Closure depths observed:            {0: 8, 1: 8, 2: 8}

## Sample Verification

| partition | depth | predicted M_native | observed M_native |
|---:|---:|---:|---:|
| 1 | 0 | 1/8 | 0.125 |
| 1 | 1 | 3/2 | 1.500 |
| 1 | 2 | 18 | 18.000 |
| 2 | 0 | 1/4 | 0.250 |
| 2 | 1 | 3 | 3.000 |
| 2 | 2 | 36 | 36.000 |
| 3 | 0 | 3/8 | 0.375 |
| 3 | 1 | 9/2 | 4.500 |
| 3 | 2 | 54 | 54.000 |
| 4 | 0 | 1/2 | 0.500 |
| 4 | 1 | 6 | 6.000 |
| 4 | 2 | 72 | 72.000 |
| 6 | 0 | 3/4 | 0.750 |
| 6 | 1 | 9 | 9.000 |
| 6 | 2 | 108 | 108.000 |
| 8 | 0 | 1 | 1.000 |
| 8 | 1 | 12 | 12.000 |
| 8 | 2 | 144 | 144.000 |
| 9 | 0 | 9/8 | 1.125 |
| 9 | 1 | 27/2 | 13.500 |

(full 24-row verification in `CR133_verification.csv`)

## Forward-Blind Sub-Prediction CR133_PRED_1 (LOCKED)

**Claim:** For any future OUTER_BINARY_NEUTRAL row, M_native = partition · R^depth / 8 exactly.

**Falsifier:** ONE future OUTER_BINARY_NEUTRAL row whose M_native deviates from the formula kills v1.0.

**Non-falsifying:** rows outside the OUTER_BINARY_NEUTRAL class; charged OUTER_BINARY rows (q_abs ≥ 1) would warrant extension.

**Free parameters at test:** 0.

## Cryptographic Chain

```text
CR119_courtroom_particle_table_csv        = 5b937d284d6c0b93a5f875acc5fbf63780fd924c90202743865d845fb1d1fc42
CR131_law_lock_json                       = 2aef1403da7f764a7e0666d12ea9ba974b09719154ce8f1f5da5d3fd456caceb

CR133_verification_csv                    = 22f44bf8d682f45f7716c4e02a687d2ee7bce34f686613800ae64feac483da25
CR133_law_lock_sha256                     = 1e7e08d8764ebdfeb4c4756495c78fb94236f63eea277f9d970db2ad3ddcf1e4
```

## Predictions Checks

- **[PASS]** P1_all_24_rows_walked -- rows walked = 24 (expected 24)
- **[PASS]** P2_formula_matches_all_rows -- matches = 24/24, violations = 0
- **[PASS]** P3_S_debit_zero_universally -- S_debit = 0 on 24/24 rows
- **[PASS]** P4_three_closure_depths_observed -- depths = {0: 8, 1: 8, 2: 8}
- **[PASS]** P5_eight_partition_values_observed -- distinct partition values = [1, 2, 3, 4, 6, 8, 9, 12]
- **[PASS]** P6_law_lock_written -- law lock sha256 = 1e7e08d8764ebdfeb4c4756495c78fb94236f63eea277f9d970db2ad3ddcf1e4

## Wrong Controls

- **[PASS]** WC1_CR119_table_unmodified -- CR119 read-only
- **[PASS]** WC2_CR131_law_lock_unmodified -- CR131 V4_1 law lock referenced but not modified
- **[PASS]** WC3_C1_equals_1_8_NOT_1_or_9_8 -- User asked: 'do we get lucky with the same C1=1?'  Answer: NO -- the OUTER_BINARY_NEUTRAL K = 1/8 = 2^-D, not C1 = 1 (which would have given M = partition * R^depth).  Same FORMULA SHAPE as V4_1 (M = ladder_input * R^depth * K) but different K.  Honest report: we got lucky with the architecture, not with the C1 value.
- **[PASS]** WC4_neutral_fermion_K_is_bare_bounce_factor -- Charged fermions (V4_1) take K = (1 + 1/alpha_H^k) with k = 1 or 2 (CR131).  Neutral fermions take K = 1/alpha_H^3 = 2^-D = 1/8.  The neutral case carries the bare bounce factor with NO +1 inhomogeneity term.
- **[PASS]** WC5_law_derived_inductively_forward_blind_committed -- Formula was derived from the 24-row ratio table (M_native/partition = 1/8, 3/2, 18 for depths 0, 1, 2; successive ratios = R).  Forward-blind CR133_PRED_1 commits the law for testing on future rows.
- **[PASS]** WC6_partition_value_used_as_ladder_input_NOT_q_abs -- Unlike V4_1 where q_abs = partition_value and both work as the ladder input, OUTER_BINARY_NEUTRAL has q_abs = 0 universally.  The ladder uses partition_value (the integer label) as the input.  This distinction is documented.

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
- Unification CR could combine CR131 + CR133 into a single 'universal 1-body fermion ladder law' if curator desires
- First-principles derivation of why neutral takes K = 2^-D vs charged takes K = (1 + 1/alpha_H^k) is open
- CR133b: M_observed structure if S_debit becomes non-zero on future OUTER_BINARY rows (currently always 0)
- Forward-blind CR133_PRED_1 resolves when CR119 gains new OUTER_BINARY_NEUTRAL rows

## Rule of Immutability

Law v1.0 formula and unified ladder reading are frozen at CR133 seal time.  Future falsification or refinement must be in an appeal CR.
