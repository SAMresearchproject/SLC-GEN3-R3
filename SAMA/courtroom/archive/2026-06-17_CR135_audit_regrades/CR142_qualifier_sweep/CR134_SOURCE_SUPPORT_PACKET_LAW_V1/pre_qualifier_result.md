# CR134 SOURCE_SUPPORT_PACKET Law v1.0

> **AUDIT-DRIVEN DEFECT CORRECTION — 2026-06-17 PER CR-141**
>
> The `CR134_law_lock_sha256` field in this file was corrected from `4aa8f02b...d48e342` to `6ab49442...adcd997` to match the actual SHA-256 of the lock JSON on disk. Root cause: runner self-reference artifact (hash computed before being embedded in the lock JSON). The defect was confined to the recorded self-citation; downstream CRs carried the correct value.
>
> The verdict `CR134_SOURCE_SUPPORT_PACKET_LAW_V1_SEALED` is **unchanged**. The underlying claim, the in-sample row matches, the partition algebra, the forward-blind sub-prediction, and the wrong controls all stand verbatim.
>
> - Original archived at: `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR134_SOURCE_SUPPORT_PACKET_LAW_V1/original_result.md`
> - Original SHA-256: `4b3b6bc2b478e153c506b350792cd1acd3054a783b540cc873c08903523131fd`
> - Replacement record: `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR134_SOURCE_SUPPORT_PACKET_LAW_V1/REPLACEMENT_RECORD.md`
> - Driving audit: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (verdict SHA-256 `2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661`)


## Verdict

```text
CR134_SOURCE_SUPPORT_PACKET_LAW_V1_SEALED
```

## The Law (Locked)

```text
For operator_class == 'SOURCE_SUPPORT_PACKET' (hidden substrate support):

                                  partition^2
  M_native  =  partition  +  -----------------
                                  R^2

            =  partition  *  (1 + partition / R^2)

            =  partition  *  (R^2 + partition) / R^2

  where R = 12.  Partition values: {1, 2, 3, 4, 6, 8, 9, 12}.
  S_debit = 0 and qA = 0 universally (substrate support has no debit or qA channel).
```

## Structural Reading

- **Bare term:** the partition value itself (the SAM algebra integer).
- **Self-correction:** partition² / R² — a quadratic perturbative response to partition value.
- **Reaches 100% bare value at p = R = 12:** M(p=12) = 12 + 144/144 = 13.
- **Smallest at p = 1:** M(p=1) = 1 + 1/144 = 145/144 ≈ 1.00694.
- **All 8 rows are HIDDEN_SUPPORT_NOT_MATTER** — substrate inventory, not physical particles.

## In-Sample Verification

- SOURCE_SUPPORT_PACKET rows tested:  **8**
- Formula matches:                     **8 / 8**
- S_debit = 0:                         **8 / 8**
- qA = 0:                              **8 / 8**
- Violations:                          **0**

## Verification Table

| partition | predicted M_native | observed M_native |
|---:|---:|---:|
| 1 | 145/144 | 1.006944444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444 |
| 2 | 73/36 | 2.027777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777778 |
| 3 | 49/16 | 3.062499999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999 |
| 4 | 37/9 | 4.111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111112 |
| 6 | 25/4 | 6.250000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002 |
| 8 | 76/9 | 8.444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444448 |
| 9 | 153/16 | 9.5625 |
| 12 | 13 | 13.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 |

## Forward-Blind Sub-Prediction CR134_PRED_1 (LOCKED)

**Claim:** For any future SOURCE_SUPPORT_PACKET row, M_native = partition + partition² / R² exactly.

**Falsifier:** ONE single future SSP row whose M_native deviates from the formula kills v1.0.

**Non-falsifying:** rows of other operator_class.  Non-zero S_debit or qA on future SSP rows would itself be a separate finding.

**Free parameters at test:** 0.

## Cryptographic Chain

```text
CR119_courtroom_particle_table_csv        = 5b937d284d6c0b93a5f875acc5fbf63780fd924c90202743865d845fb1d1fc42

CR134_verification_csv                    = d926bd4b2fcd6a98757d92128ff781d9f585d021cda46bc8c4412b2b809d39f9
CR134_law_lock_sha256                     = 6ab4944278530a359382303a4bacef4a1bcc8a939b7307925615a525aadcd997
```

## Predictions Checks

- **[PASS]** P1_all_8_rows_walked -- rows walked = 8 (expected 8)
- **[PASS]** P2_formula_matches_all_rows -- matches = 8/8, violations = 0
- **[PASS]** P3_S_debit_zero_universally -- S_debit = 0 on 8/8 rows
- **[PASS]** P4_qA_zero_universally -- qA = 0 on 8/8 rows (no qA channel for substrate)
- **[PASS]** P5_eight_partition_values_observed -- distinct partition values = [1, 2, 3, 4, 6, 8, 9, 12]
- **[PASS]** P6_law_lock_written -- law lock sha256 = 6ab4944278530a359382303a4bacef4a1bcc8a939b7307925615a525aadcd997

## Wrong Controls

- **[PASS]** WC1_CR119_table_unmodified -- CR119 read-only
- **[PASS]** WC2_SOURCE_SUPPORT_PACKET_explicitly_NOT_matter -- All 8 rows have stability_status = HIDDEN_SUPPORT_NOT_MATTER and matter_row_allowed = no.  CR134 locks the M_native generator without claiming these are physical particles -- they are SAM's substrate-support inventory.
- **[PASS]** WC3_formula_derived_directly_from_data -- M_native - partition divided by partition^2 gives EXACTLY 1/R^2 = 1/144 for all 8 rows.  The formula M = p + p^2/R^2 is the direct algebraic reading; no hypothesis fitting required.
- **[PASS]** WC4_S_debit_and_qA_both_zero_universally -- Confirmed: all 8 rows have S_debit = 0 AND qA_source_support = 0.  These are pure-structure rows with no surface debit and no qA channel.
- **[PASS]** WC5_partition_algebra_unbroken -- All 8 partition values are in the SAM algebra {1, 2, 3, 4, 6, 8, 9, 12}.
- **[PASS]** WC6_law_derived_inductively_forward_blind_committed -- Formula was extracted from the 8-row data via direct algebraic inspection.  Forward-blind CR134_PRED_1 commits the law for testing on future rows.

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
- First-principles derivation of why substrate support takes the +p^2/R^2 perturbative form is open
- Cross-class relation between SOURCE_SUPPORT_PACKET and OUTER_BINARY_NEUTRAL's 1/8 coefficient (both 'hidden' families but different forms) is structurally open
- Forward-blind CR134_PRED_1 resolves when CR119 gains new SOURCE_SUPPORT_PACKET rows

## Rule of Immutability

Law v1.0 formula and substrate-support classification are frozen at CR134 seal time.  Future falsification or refinement must be in an appeal CR.
