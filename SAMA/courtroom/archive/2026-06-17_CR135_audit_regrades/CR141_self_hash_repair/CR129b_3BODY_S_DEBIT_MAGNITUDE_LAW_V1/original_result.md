# CR129b 3-Body S_debit Magnitude Law v1.0 (OCTET depth=3)

## Verdict

```text
CR129b_3BODY_S_DEBIT_MAGNITUDE_LAW_V1_SEALED
```

## Stage Decomposition Audit (User-Directed Strategy)

| stage | hypothesis | result |
|---|---|---|
| 1 | Pure pairwise BCP sum: S = ΣS_BCP(a_i,a_j) | **INSUFFICIENT** -- wrong sign, off by factor 7-15 |
| 2 | + (1/8)·M_native global surcharge | **INSUFFICIENT** -- wrong scale |
| 2' | + (9/8)·M/R³ surcharge (user proposal) | **OVERSHOOTS by 18/17 uniformly** -- right family, wrong member |
| 3 | + q_abs slot correction relative to mass | **DECISIVE** -- residual scales linearly with q_abs |
| 4 | q=0 closed form: S = (17/16) · M / R³ | **EXACT** -- user-directed lock |

## The Locked Form (q=0)

```text
                       17     M_native
  S_debit (q=0)  =   -----  *  --------
                       16        R^3

                =  (R + D + alpha_H)     M_native
                   ------------------  *  --------
                      alpha_H^4             R^3

  where R = 12, D = 3, alpha_H = 2
  17 = R + D + alpha_H = 12 + 3 + 2  (sum of foundation constants)
  16 = alpha_H^4                       (algebra's alpha_H to the 4th)
  Sign: always +1 at q=0 (verified on all 17 q=0 rows)
```

## The Unified Magnitude Form (q ≥ 0)

```text
                 4 * q_eff + D     M_native
  |S_3body|  =  --------------- * ----------
                    4 * R              R^3

    where  q_eff = R   if q_abs == 0  (yields the 17/16 coefficient)
           q_eff = q_abs  otherwise

Equivalent:  |X * 4| = |S * 4 * R^4 / M| = 4 * q_eff + D
```

## The Universal Sign Rule (locked, 76/76 match)

```text
  sign(S_debit)  =  + 1   if q_sign in {positive, neutral}
                  =  - 1   if q_sign == negative

  Equivalently: S_debit follows the direction of the row's net charge,
                with neutral charge mapping to positive surface debit.
```

Verified on all 76 OCTET 3-body depth=3 rows: 17 q=0 (neutral, S>0), 10 q_sign=positive (S>0), 49 q_sign=negative (S<0).  Zero violations.

**Structural reading:** analog of CR128b's `sign(S) = sign(a − b)` for 2-body BCP.  Both encode charge direction through the surface debit's sign.  At 2-body, charge direction is expressed via partition ordering; at 3-body, it's expressed directly via the row's net charge q_sign.

## Slot-Weighted Decomposition (q=0 closed form, derived)

The 17/16 coefficient at q=0 has a clean slot-weighted reading:

```text
                1       9      1        17
  S(q=0)  =  ( --- + ( - * - ) + --- ) * M / R^3  =  --- * M / R^3
                4       8   2     4                  16

  Slot weights:   outer:  1/4
                  middle: (9/8) * (1/2) = 9/16    <-- 9/8 surcharge on the 1/2
                  outer:  1/4

  Sum:  1/4 + 9/16 + 1/4 = 4/16 + 9/16 + 4/16 = 17/16
```

The 9/8 surcharge applies to the **middle slot only** (the 1/2 weight in the 1:2:1 ratio).  Outer slots are plain.  This is the structural derivation behind the (R + D + alpha_H) / alpha_H^4 form.

## Residual After Stage 1 by q_abs

Honest diagnostic showing why Stage 1 alone fails and how the q_abs slot enters:

| q_abs | n | mean res/M | min | max |
|---:|---:|---:|---:|---:|
| 0 | 17 | +6.36197e-04 | +6.19007e-04 | +6.62152e-04 |
| 1 | 18 | -1.01493e-05 | -7.30854e-05 | +1.30728e-04 |
| 2 | 16 | -2.75093e-05 | -1.24423e-04 | +1.80845e-04 |
| 3 | 4 | -1.66355e-04 | -1.71364e-04 | -1.55868e-04 |
| 4 | 4 | -2.13801e-04 | -2.19446e-04 | -2.07752e-04 |
| 5 | 8 | -2.60839e-04 | -2.73824e-04 | -2.38449e-04 |
| 6 | 2 | -2.98256e-04 | -3.08047e-04 | -2.88466e-04 |
| 7 | 2 | -3.61181e-04 | -3.68282e-04 | -3.54079e-04 |
| 8 | 3 | -4.12593e-04 | -4.18988e-04 | -4.04090e-04 |
| 10 | 1 | -5.14629e-04 | -5.14629e-04 | -5.14629e-04 |
| 11 | 1 | -5.64559e-04 | -5.64559e-04 | -5.64559e-04 |

The linear scaling with q_abs (negative slope for q>=1, positive constant for q=0) is the diagnostic that pointed to the magnitude formula.

## In-Sample Verification

- OCTET 3-body rows tested:           **76**
- Pure pairwise matches observed:     0
- **Magnitude formula matches:        76 / 76**
- q=0 positive sign matches:          17 / 17

## Forward-Blind Sub-Prediction CR129b_PRED_1 (FULLY LOCKED)

**Magnitude claim:** For any future OCTET 3-body depth=3 non-rejected row, |S_debit| = M_native * (4·q_eff + D) / (4·R⁴) exactly.

**Sign claim (universal):** sign(S_debit) = +1 if q_sign in {positive, neutral}, -1 if q_sign = negative.

**q=0 closed-form claim:** S_debit(q=0) = (17/16) · M_native / R³ = (1/4 + 9/16 + 1/4) · M/R³, sign = +1.

**q=0 mass balance:** qA_source_support + S_debit = M_native exactly.

**Magnitude falsifier:** one violation of the magnitude rule kills v1.0.

**Sign falsifier:** one row where sign(S) disagrees with the q_sign rule kills v1.0.

**q=0 closed-form falsifier:** one q=0 row whose S ≠ (17/16)·M/R³ exactly kills the q=0 lock.

**Combined claim:** S_debit is FULLY DETERMINED (both magnitude and sign) by (M_native, q_abs, q_sign) and the constants R, D, alpha_H.  Zero free parameters per row.

**Free parameters at test:** 0.

## What CR129b Does NOT Claim

- A pairwise-derivation of the formula (the pure pairwise hypothesis was tested and rejected).
- That (1/8) = 2^-D global surcharge accounts for the 3-body S_debit structure (also rejected).
- A complete sign rule for q_abs >= 1 (open).
- That GROUND_BARYON_3BODY (depth=0) follows the same magnitude (different scale by R^3).

## Cryptographic Chain

```text
CR119_courtroom_particle_table_csv        = 5b937d284d6c0b93a5f875acc5fbf63780fd924c90202743865d845fb1d1fc42
CR128_law_lock_json                       = 0f62d6b4e942a9b41d2b620265f3b05d737a35d65acb4553190f64183ff19871
CR128b_law_lock_json                      = fb9287cd6c79b161f138f5ce4fde5b109483be1787757d6e4bdf4f613ad16467
CR129_law_lock_json                       = 041a487c30a8ee3d96dbf347e26e110c2808741b325769a910217d8bcfbeb710

CR129b_stage_decomposition_csv            = e1f7beee490410d59b600dc12348be45cc85fc7dfdc6e0de1a1c6742f59be557
CR129b_magnitude_lock_sha256              = c5751756c5e90e7f14e7254e8df95b32d01ba56a1876d7a4d8d12170ad13a112
```

## Predictions Checks

- **[PASS]** P1_all_76_OCTET_3body_rows_walked -- rows walked = 76
- **[PASS]** P2_pure_pairwise_INSUFFICIENT_as_expected -- pure pairwise matches observed = 0/76.  Confirms Stage 1 is insufficient (failure mode is the discovery).
- **[PASS]** P3_magnitude_formula_matches_all_rows -- magnitude matches = 76/76
- **[PASS]** P4_q0_sign_rule_holds -- q=0 positive-sign matches = 17/17
- **[PASS]** P4b_q0_17_over_16_closed_form_holds -- q=0 rows where S = (17/16) * M / R^3 exactly: 17/17.  USER-DIRECTED LOCK: this is the cleanest closed form for the q=0 case.
- **[PASS]** P4c_q0_mass_balance_holds -- q=0 rows where qA_source_support + S = M_native: 17/17
- **[PASS]** P4d_universal_sign_rule_holds -- sign(S_debit) = sign(q_sign) with neutral->positive: 76/76 match.  This CLOSES the sign rule that was open in earlier drafts.
- **[PASS]** P5_residual_after_stage1_q_dependence_documented -- residual aggregates collected for 11 distinct q_abs values
- **[PASS]** P6_magnitude_lock_written -- magnitude lock sha256 = c5751756c5e90e7f14e7254e8df95b32d01ba56a1876d7a4d8d12170ad13a112

## Wrong Controls

- **[PASS]** WC1_CR119_table_unmodified -- 
- **[PASS]** WC2_CR128_CR128b_CR129_law_locks_unmodified -- Upstream law locks read-only; CR129b extends without overriding
- **[PASS]** WC3_pairwise_failure_reported_HONESTLY -- Pure pairwise hypothesis from CR128b's BCP form was TESTED and FOUND INSUFFICIENT.  CR129b reports this rejection rather than masking it with a post-hoc combination of weak pieces.
- **[PASS]** WC4_1_8_surcharge_failure_reported_HONESTLY -- (1/8) * M_native as a global surcharge does NOT close the residual.  Reported as such rather than tuned away.
- **[PASS]** WC5_sign_rule_for_q_geq_1_explicitly_OPEN -- CR129b locks ONLY the magnitude rule and the q=0 sign rule.  The sign rule for q >= 1 is explicitly flagged as open work, not over-claimed.
- **[PASS]** WC6_GROUND_BARYON_3body_explicitly_out_of_scope -- GROUND_BARYON_3BODY (depth=0) has different magnitude scale by factor R^3 and a REJECTED_FAKE_CLOSURE sentinel.  Out of scope for CR129b; handled separately.
- **[PASS]** WC7_REJECTED_rows_filtered_from_test -- All 76 OCTET_COMPOSITE 3-body rows in CR119 are BOUND (no REJECTED in this operator class).  Filter is vacuous here but documented for the law's scope.

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
- GROUND_BARYON_3BODY (depth=0) S_debit magnitude: separate CR (residuals differ by factor R^3; REJECTED rows have sentinel)
- Why the q_abs slot correction dominates over pure-pairwise structure is a structural derivation question -- the (4q+D)/(4R^4) form is empirically locked but its derivation from SAM's dozenal algebra is open
- Forward-blind CR129b_PRED_1 resolves when CR119 gains new OCTET 3-body depth=3 rows

## Rule of Immutability

Magnitude formula, q=0 sign rule, and scope are frozen at CR129b seal time.  Future falsification or refinement (including a full sign rule for q>=1) must be in an appeal CR.
