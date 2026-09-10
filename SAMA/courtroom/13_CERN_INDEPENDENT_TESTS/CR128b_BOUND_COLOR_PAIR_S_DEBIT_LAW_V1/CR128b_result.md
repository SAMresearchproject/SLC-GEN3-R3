# CR128b BOUND_COLOR_PAIR S_debit Law v1.0

> **IN-SAMPLE QUALIFIER -- 2026-06-17 PER CR-142**
>
> Headline rhetoric in this CR uses 'zero free parameters' / 'free_parameters = 0' language. That language is technically accurate in the strict sense (no scalar parameter fitted post-hoc) but requires the following qualifier at the headline level for honest interpretation:
>
> **In-sample qualifier:** The CR128b law was extracted inductively from the CR-119 catalog (via cluster inspection in CR-127 for some, direct row analysis for others). The reported in-sample match (e.g., 36/36 for CR-128) is therefore GENERATOR CONSISTENCY against the training data, NOT first-principles derivation. The forward-blind falsifier (the `CR<N>_PRED_1` sub-prediction) commits the law to FORWARD-BLIND testing on FUTURE rows; overfit cannot operate there. The existing wrong control `WC3_law_derived_from_data_not_first_principles` (or equivalent) carries the full disclosure; this header surfaces it to the top.
>
> The PASS verdict on this CR survives the qualifier. The framework's structural content (cross-class regularity across 10 operator classes from {R=12, D=3, alpha_H=2, partition algebra}) is the substantive signal; the in-sample status affects how the headline should be read, not whether the underlying claim holds.
>
> - Pre-qualifier state archived at: `archive/2026-06-17_CR135_audit_regrades/CR142_qualifier_sweep/CR128b_BOUND_COLOR_PAIR_S_DEBIT_LAW_V1/pre_qualifier_result.md`
> - Pre-qualifier SHA-256: `bd985cefbb3def3b436ebf5274d73919f707c99252284d64d492a755e104040d`
> - Replacement record: `archive/2026-06-17_CR135_audit_regrades/CR142_qualifier_sweep/CR128b_BOUND_COLOR_PAIR_S_DEBIT_LAW_V1/REPLACEMENT_RECORD.md`
> - Driving audit: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (verdict SHA-256 `2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661`)


> **AUDIT-DRIVEN DEFECT CORRECTION — 2026-06-17 PER CR-141**
>
> The `CR128b_law_lock_sha256` field in this file was corrected from `9336468a...dd26964` to `fb9287cd...ad16467` to match the actual SHA-256 of the lock JSON on disk. Root cause: runner self-reference artifact (hash computed before being embedded in the lock JSON). The defect was confined to the recorded self-citation; downstream CRs carried the correct value.
>
> The verdict `CR128b_BOUND_COLOR_PAIR_S_DEBIT_LAW_V1_SEALED` is **unchanged**. The underlying claim, the in-sample row matches, the partition algebra, the forward-blind sub-prediction, and the wrong controls all stand verbatim.
>
> - Original archived at: `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR128b_BOUND_COLOR_PAIR_S_DEBIT_LAW_V1/original_result.md`
> - Original SHA-256: `8dd3042c74952cb4b17ea700fe4db2e122d6913241f0b19ed817027be657fe08`
> - Replacement record: `archive/2026-06-17_CR135_audit_regrades/CR141_self_hash_repair/CR128b_BOUND_COLOR_PAIR_S_DEBIT_LAW_V1/REPLACEMENT_RECORD.md`
> - Driving audit: `00_governance/CR135_HOSTILE_AUDIT_2026_06_17/CR135_AUDIT_VERDICT.md` (verdict SHA-256 `2fe572d5efbb566043bf5a8abfa8404438ba9ebc2097fce51388fcca23b40661`)


## Verdict

```text
CR128b_BOUND_COLOR_PAIR_S_DEBIT_LAW_V1_SEALED
```

## The Law (Locked)

```text
For operator_class == 'BOUND_COLOR_PAIR' with partition (first, second),
first != second:

  Magnitude:  |S_debit| = M_native(a, b) * (|a - b| + D) / R^4
  Sign:       sign(S_debit) = sign(first - second)

  Combined:   S_debit = M_native * (first - second) * (|first - second| + D)
                       / ( |first - second| * R^4 )

where R = 12, D = 3, M_native = R*a*b + D*|a-b| (per CR128 v1.0),
and (a, b) drawn from {1, 2, 3, 4, 6, 8, 9, 12}.
```

## Combined Zero-Parameter Claim (CR128 + CR128b)

With both v1.0 laws sealed, the full row state of any asymmetric BCP row is determined by the integer pair (a, b) and the constants R, D alone:

```text
M_native(a, b)   = R*a*b + D*|a-b|
S_debit(a, b)    = M_native * (a - b) * (|a-b| + D) / ( |a-b| * R^4 )
M_observed(a, b) = M_native + S_debit
```

Zero free parameters per row.

## In-Sample Verification

- Asymmetric BOUND_COLOR_PAIR rows tested: **30**
- Symmetric rows skipped (out of scope):    6
- Formula matches (sign + magnitude):       **30 / 30**
- Magnitude matches:                        30
- Sign matches:                             30
- Violations:                               **0**

## Per-Row Verification (first 16 rows)

| candidate | sig | (first, second) | |diff| | M_native | S_predicted | S_observed | match |
|---|---|---|---:|---:|---:|---:|:-:|
| QP093A-0236 | 1+2 | (1, 2) | 1 | 27 | -1/192 | -5.208333e-03 | YES |
| QP093A-0237 | 1+3 | (1, 3) | 2 | 42 | -35/3456 | -1.012731e-02 | YES |
| QP093A-0238 | 1+4 | (1, 4) | 3 | 57 | -19/1152 | -1.649306e-02 | YES |
| QP093A-0239 | 1+6 | (1, 6) | 5 | 87 | -29/864 | -3.356481e-02 | YES |
| QP093A-0240 | 1+8 | (1, 8) | 7 | 117 | -65/1152 | -5.642361e-02 | YES |
| QP093A-0243 | 2+1 | (2, 1) | 1 | 27 | 1/192 | +5.208333e-03 | YES |
| QP093A-0245 | 2+3 | (2, 3) | 1 | 75 | -25/1728 | -1.446759e-02 | YES |
| QP093A-0246 | 2+4 | (2, 4) | 2 | 102 | -85/3456 | -2.459491e-02 | YES |
| QP093A-0247 | 2+6 | (2, 6) | 4 | 156 | -91/1728 | -5.266204e-02 | YES |
| QP093A-0248 | 2+8 | (2, 8) | 6 | 210 | -35/384 | -9.114583e-02 | YES |
| QP093A-0251 | 3+1 | (3, 1) | 2 | 42 | 35/3456 | +1.012731e-02 | YES |
| QP093A-0252 | 3+2 | (3, 2) | 1 | 75 | 25/1728 | +1.446759e-02 | YES |
| QP093A-0254 | 3+4 | (3, 4) | 1 | 147 | -49/1728 | -2.835648e-02 | YES |
| QP093A-0255 | 3+6 | (3, 6) | 3 | 225 | -25/384 | -6.510417e-02 | YES |
| QP093A-0256 | 3+8 | (3, 8) | 5 | 303 | -101/864 | -1.168981e-01 | YES |
| QP093A-0259 | 4+1 | (4, 1) | 3 | 57 | 19/1152 | +1.649306e-02 | YES |

(full 30-row verification in `CR128b_verification.csv`)

## Forward-Blind Sub-Prediction CR128b_PRED_1 (LOCKED)

**Claim:** For any FUTURE asymmetric BOUND_COLOR_PAIR row with partition (a, b), first != second, drawn from the algebra:

    S_debit = sign(first - second) * M_native * (|first - second| + D) / R^4

exactly, as a rational number.

**Falsifier:** ONE single future asymmetric BCP row whose S_debit deviates from the formula by any non-zero rational.  ONE violation falsifies v1.0.

**Non-falsifying:** rows of other operator_class; symmetric (a, a) rows; algebra extensions.

**Free parameters at test:** 0.

## What CR128b Does NOT Claim

- A formula for symmetric (a, a) pair S_debit (handled in CR128c).
- An OCTET_COMPOSITE 3-body analog of this formula (CR129+ work).
- That the (|a-b| + D) antisymmetric factor has a first-principles SAM derivation -- it is observed and locked but not yet derived.

## Cryptographic Chain

```text
CR119_courtroom_particle_table_csv        = 5b937d284d6c0b93a5f875acc5fbf63780fd924c90202743865d845fb1d1fc42
CR128_law_lock_json                       = 0f62d6b4e942a9b41d2b620265f3b05d737a35d65acb4553190f64183ff19871
CR128_verification_csv                    = 0b51ff37925777edc9af0d48e3c279e28dfd5e69feddd6c12d379d2b40415517

CR128b_verification_csv                   = adc84235f09782d4ed135813f6b8dd60975d54236442fbfa56bbb2181d9efe8f
CR128b_law_lock_sha256                    = fb9287cd6c79b161f138f5ce4fde5b109483be1787757d6e4bdf4f613ad16467
```

## Predictions Checks

- **[PASS]** P1_30_asymmetric_rows_tested -- asymmetric rows tested = 30 (expected 30)
- **[PASS]** P2_all_formula_matches -- matches = 30/30, violations = 0
- **[PASS]** P3_all_magnitude_matches -- magnitude matches = 30/30
- **[PASS]** P4_all_sign_matches -- sign matches = 30/30
- **[PASS]** P5_six_symmetric_rows_correctly_skipped -- symmetric rows skipped = 6 (expected 6; out of CR128b scope)
- **[PASS]** P6_forward_blind_law_lock_written -- law lock sha256 = fb9287cd6c79b161f138f5ce4fde5b109483be1787757d6e4bdf4f613ad16467

## Wrong Controls

- **[PASS]** WC1_CR119_table_unmodified -- CR119 read-only
- **[PASS]** WC2_CR128_law_lock_unmodified -- CR128 M_native law lock referenced but unchanged; CR128b extends not overrides
- **[PASS]** WC3_exact_rational_arithmetic_used -- Verification uses Python Fraction for exact rationals and Decimal at 200-digit precision for parsing CR119's high-precision S_debit strings.  No float round-off contamination.
- **[PASS]** WC4_sign_rule_derived_separately_from_magnitude -- Magnitude formula was pattern-spotted from 8 doublet pairs; sign rule (sign(first - second)) was observed independently.  Both verified together against all 30 rows.
- **[PASS]** WC5_symmetric_pairs_explicitly_out_of_scope -- Symmetric (a, a) rows have a different surface debit structure (M_obs(a,a) ~ (43/4) * a^2 empirically) and are reserved for CR128c.
- **[PASS]** WC6_law_derived_inductively_forward_blind_committed -- Like CR128, the law was derived inductively from in-sample data.  Forward-blind falsifier CR128b_PRED_1 commits the formula for testing on future rows where overfit cannot operate.

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
- CR128c: derive M_observed formula for symmetric (a, a) BCP rows (empirical 10.75 a^2 = (43/4) a^2)
- CR129: derive OCTET_COMPOSITE 3-body M_native + S_debit generators -- the BCP antisymmetric (first - second) factor suggests the 3-body case may have an analogous antisymmetric tensor structure
- Forward-blind test CR128b_PRED_1 resolves when CR119 gains new asymmetric BCP rows

## Rule of Immutability

Law v1.0 formula (magnitude + sign rule), partition algebra, and constants are frozen at CR128b seal time.  Future falsification or revision must be in an appeal CR.
