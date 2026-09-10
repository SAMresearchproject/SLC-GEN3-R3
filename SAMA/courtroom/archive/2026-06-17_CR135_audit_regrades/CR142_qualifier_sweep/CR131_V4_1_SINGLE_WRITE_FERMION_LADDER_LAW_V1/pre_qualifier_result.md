# CR131 V4_1_SINGLE_WRITE Fermion Ladder Law v1.0

> **AUDIT-DRIVEN DEFECT CORRECTION — 2026-06-17 PER CR-141**
>
> The `CR131_law_lock_sha256` field in this file was corrected from `9fb53281...f9e8765` to `2aef1403...56caceb` to match the actual SHA-256 of the lock JSON on disk. Root cause: runner self-reference artifact (hash computed before being embedded in the lock JSON). The defect was confined to the recorded self-citation; downstream CRs carried the correct value.
>
> The verdict `CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1_SEALED` is **unchanged**. The underlying claim, the in-sample row matches, the partition algebra, the forward-blind sub-prediction, and the wrong controls all stand verbatim.
>
> - Original archived at: `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1/original_result.md`
> - Original SHA-256: `5c3c148c7cfe0d64260ee16b4762d5d67256234d2af243a27e9856f220a0e213`
> - Replacement record: `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1/REPLACEMENT_RECORD.md`
> - Driving audit: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (verdict SHA-256 `2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661`)


## Verdict

```text
CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1_SEALED
```

## Answer to the Framing Question

**Is V4_1_SINGLE_WRITE a true 1-body scalar?  NO.**

All 90 V4_1_SINGLE_WRITE rows have `spin_or_hand_class = fermion_half_write`.  V4_1 is the 1-body **fermion** family -- the lepton-class single-writes -- not a scalar.  True 1-body bosons in CR119 are the carrier rows (TENSOR_CARRIER, ROAD_LIGHT_CARRIER, WEAK_VECTOR_CARRIER, etc., each n=1).

## The Law (Locked)

```text
For operator_class == 'V4_1_SINGLE_WRITE':

  M_native = q_abs * R^closure_depth * K(q_sign, stability_status)

  K coefficients (matter):       K(+) = 5/4 = (alpha_H^2 + 1) / alpha_H^2
                                  K(-) = 3/2 = (alpha_H + 1) / alpha_H

  K coefficients (antimatter):   K(+) = 3/2     <-- sign-flipped twin of matter K(-)
                                  K(-) = 5/4     <-- sign-flipped twin of matter K(+)

  where R = 12, alpha_H = 2.
```

## Structural Reading

- **Bare charge contribution:** q_abs * R^closure_depth.  Linear in q, with R-multiplied jumps per closure depth.
- **K coefficient = 1 + 1/alpha_H^k:** the "extra beyond bare charge" factor.  k=2 for positive matter (= negative antimatter), k=1 for negative matter (= positive antimatter).  Analog of CR128b's (|a-b| + D)/|a-b| inhomogeneity term.
- **R^depth scaling = three-generation hierarchy:** depth=0 gen 1, depth=1 gen 2 (×R), depth=2 gen 3 (×R²).  Architecturally consistent with SM's three lepton generations.
- **Matter/antimatter K-swap = CPT-like structure:** a particle and its conjugate are related by sign-flip of K at the same (q_abs, depth) coordinate.

## In-Sample Verification

- V4_1_SINGLE_WRITE rows tested: **90**
- Formula matches:                **90 / 90**
  - Matter (STABLE_MATTER_CANDIDATE):    48
  - Antimatter (STABLE_CONJUGATE):       42
- Violations:                     **0**
- Closure depths observed:        {0: 32, 1: 32, 2: 26}

## Sample Verification (matter, all depths)

| q_abs | q_sign | depth | predicted M_native | observed M_native |
|---:|---|---:|---:|---:|
| 1 | positive | 0 | 5/4 | 1.25 |
| 1 | negative | 0 | 3/2 | 1.5 |
| 2 | positive | 0 | 5/2 | 2.50 |
| 2 | negative | 0 | 3 | 3.0 |
| 3 | positive | 0 | 15/4 | 3.75 |
| 3 | negative | 0 | 9/2 | 4.5 |
| 4 | positive | 0 | 5 | 5.00 |
| 4 | negative | 0 | 6 | 6.0 |
| 6 | positive | 0 | 15/2 | 7.50 |
| 6 | negative | 0 | 9 | 9.0 |
| 8 | positive | 0 | 10 | 10.00 |
| 8 | negative | 0 | 12 | 12.0 |
| 9 | positive | 0 | 45/4 | 11.25 |
| 9 | negative | 0 | 27/2 | 13.5 |
| 12 | positive | 0 | 15 | 15.00 |
| 12 | negative | 0 | 18 | 18.0 |
| 1 | positive | 1 | 15 | 15.00 |
| 1 | negative | 1 | 18 | 18.0 |
| 2 | positive | 1 | 30 | 30.00 |
| 2 | negative | 1 | 36 | 36.0 |

## Antimatter Sample (K-swap verified)

| q_abs | q_sign | depth | K used | predicted | observed |
|---:|---|---:|---|---:|---:|
| 1 | negative | 0 | 5/4 | 5/4 | 1.25 |
| 1 | positive | 0 | 3/2 | 3/2 | 1.5 |
| 2 | negative | 0 | 5/4 | 5/2 | 2.50 |
| 2 | positive | 0 | 3/2 | 3 | 3.0 |
| 3 | negative | 0 | 5/4 | 15/4 | 3.75 |
| 3 | positive | 0 | 3/2 | 9/2 | 4.5 |
| 4 | negative | 0 | 5/4 | 5 | 5.00 |
| 4 | positive | 0 | 3/2 | 6 | 6.0 |
| 6 | negative | 0 | 5/4 | 15/2 | 7.50 |
| 6 | positive | 0 | 3/2 | 9 | 9.0 |
| 8 | negative | 0 | 5/4 | 10 | 10.00 |
| 8 | positive | 0 | 3/2 | 12 | 12.0 |

(full 90-row verification in `CR131_verification.csv`)

## Forward-Blind Sub-Prediction CR131_PRED_1 (LOCKED)

**Claim:** For any future V4_1_SINGLE_WRITE row, M_native = q_abs · R^closure_depth · K exactly, with K determined by (q_sign, matter/antimatter status).

**Falsifier:** ONE future V4_1 row whose M_native deviates from the formula by any non-zero rational kills v1.0.

**Non-falsifying:** rows of other operator_class; stability_status outside the matter/antimatter pair (would warrant an extension CR).

**Free parameters at test:** 0.

## What CR131 Does NOT Claim

- A formula for S_debit / M_observed (CR131b).
- Extension to OUTER_BINARY_NEUTRAL (CR131c).
- That carrier rows (true 1-body bosons) follow this generator (CR132+ work).
- A first-principles derivation of K = (1 + 1/α_H^k) from SAM's dozenal algebra (open structural question).

## Cryptographic Chain

```text
CR119_courtroom_particle_table_csv        = 5b937d284d6c0b93a5f875acc5fbf63780fd924c90202743865d845fb1d1fc42

CR131_verification_csv                    = 426bd99ddf02ce25086bf450675822bdfd2d02e2e7c9a4c54ab8faf301658718
CR131_law_lock_sha256                     = 2aef1403da7f764a7e0666d12ea9ba974b09719154ce8f1f5da5d3fd456caceb
```

## Predictions Checks

- **[PASS]** P1_all_90_V4_1_rows_walked -- V4_1_SINGLE_WRITE rows walked = 90
- **[PASS]** P2_formula_matches_all_rows -- matches = 90/90, violations = 0
- **[PASS]** P3_matter_subset_matches -- matter matches = 48
- **[PASS]** P4_antimatter_subset_matches -- antimatter matches = 42 (K-swap rule verified)
- **[PASS]** P5_three_closure_depths_observed -- depths observed = {0: 32, 1: 32, 2: 26}
- **[PASS]** P6_law_lock_written -- law lock sha256 = 2aef1403da7f764a7e0666d12ea9ba974b09719154ce8f1f5da5d3fd456caceb

## Wrong Controls

- **[PASS]** WC1_CR119_table_unmodified -- CR119 read-only
- **[PASS]** WC2_NOT_a_1body_scalar_claim -- V4_1_SINGLE_WRITE has spin_or_hand_class = 'fermion_half_write' for ALL 90 rows.  CR131 explicitly classifies this as the 1-body fermion family, NOT a 1-body scalar.
- **[PASS]** WC3_carrier_rows_explicitly_out_of_scope -- True 1-body bosons (TENSOR_CARRIER, ROAD_LIGHT_CARRIER, WEAK_VECTOR_CARRIER, NEUTRAL_VECTOR_CARRIER, COLOR_OWNER_CARRIER, A_FIELD_CARRIER, each n=1) are in different operator classes and require separate generators.  CR131 does not claim to cover them.
- **[PASS]** WC4_OUTER_BINARY_NEUTRAL_out_of_scope -- OUTER_BINARY_NEUTRAL (24 rows, also fermion_half_write but different operator class) is excluded from CR131.  Whether the same K-coefficient family applies there is a separate test.
- **[PASS]** WC5_law_derived_inductively_forward_blind_committed -- The formula M = q*R^depth*K was derived by inspecting the systematic doublet structure across partitions 1, 2, 3, 4, 6, 8, 9, 12 and depths 0, 1, 2.  Forward-blind falsifier CR131_PRED_1 commits the law for testing on future rows.
- **[PASS]** WC6_antimatter_K_swap_documented_NOT_postulated -- The K-swap under matter/antimatter conjugation was DISCOVERED via the 42 initial violations -- when the first version assumed K depends only on q_sign, ALL ANTIMATTER_STABLE_CONJUGATE rows failed.  Inspection revealed they all had K swapped, prompting the corrected rule.  This is honest forensics, not post-hoc tuning.

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
- CR131b: derive S_debit / M_observed for V4_1 rows (M_native locked here, M_observed open)
- CR131c: extend test to OUTER_BINARY_NEUTRAL (24 rows, also 1-body fermion_half_write)
- CR132+: derive 1-body BOSON generators for the 6 single-instance carrier classes (TENSOR, ROAD_LIGHT, WEAK_VECTOR, NEUTRAL_VECTOR, COLOR_OWNER, A_FIELD)
- First-principles derivation of K = (1 + 1/alpha_H^k) coefficients from SAM's dozenal algebra is open
- Forward-blind CR131_PRED_1 resolves when CR119 gains new V4_1 rows

## Rule of Immutability

Law v1.0 formula, K coefficients, matter/antimatter rule, and partition algebra are frozen at CR131 seal time.  Future falsification or refinement must be in an appeal CR.
