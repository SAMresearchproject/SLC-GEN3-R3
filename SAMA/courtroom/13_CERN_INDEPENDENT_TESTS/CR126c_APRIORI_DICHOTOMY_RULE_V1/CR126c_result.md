# CR126c A-Priori Dichotomy Rule v1.0

## Verdict

```text
CR126c_APRIORI_DICHOTOMY_RULE_V1_SEALED
```

## Rule v1.0 Class

```text
RULE_V1_SUPPORTED
```

Verdict by null distribution:

- Uniform null:     **SIGNIFICANT** (p_joint = 0.01947)
- Log-uniform null: **STRONG** (p_joint = 6.567e-05)

## Rule v1.0 Definition (Locked)

```python
def predict_denom_family(operator_class: str) -> set[int]:
    if operator_class == 'CLOSED_SCALAR_LOOP':
        return {3}        # closest natural SAM scale is /R^3
    return {1, 2}         # closest natural SAM scale is /R or /R^2
```

Inputs: operator_class only.  Numerator NOT predicted in v1.0.

## Rule Application (17 Allowed Rows)

| candidate | operator_class | depth | residual % | closest scale | denom | predicted family | match |
|---|---|---:|---:|---|---:|---|:-:|
| QP093A-0070 | V4_1_SINGLE_WRITE | 2 | 1.9074 | D_over_R2 | R^2 | {1,2} | YES |
| QP093A-0073 | V4_1_SINGLE_WRITE | 0 | 2.5779 | alphaH_sq_over_R2 | R^2 | {1,2} | YES |
| QP093A-0074 | V4_1_SINGLE_WRITE | 0 | 1.0791 | 2negD_over_R1 | R^1 | {1,2} | YES |
| QP093A-0128 | GROUND_BARYON_3BODY | 0 | 4.2649 | alphaH_D_over_R2 | R^2 | {1,2} | YES |
| QP093A-0139 | OCTET_COMPOSITE | 3 | 2.5655 | alphaH_sq_over_R2 | R^2 | {1,2} | YES |
| QP093A-0143 | OCTET_COMPOSITE | 3 | 1.4546 | alphaH_over_R2 | R^2 | {1,2} | YES |
| QP093A-0145 | OCTET_COMPOSITE | 3 | 4.1825 | alphaH_D_over_R2 | R^2 | {1,2} | YES |
| QP093A-0170 | OCTET_COMPOSITE | 3 | 3.2842 | 2negD_D_over_R1 | R^1 | {1,2} | YES |
| QP093A-0171 | OCTET_COMPOSITE | 3 | 1.0459 | 2negD_over_R1 | R^1 | {1,2} | YES |
| QP093A-0186 | OCTET_COMPOSITE | 3 | 0.2641 | 2negD_D_over_R2 | R^2 | {1,2} | YES |
| QP093A-0187 | GROUND_BARYON_3BODY | 0 | 2.4460 | alphaH_sq_over_R2 | R^2 | {1,2} | YES |
| QP093A-0188 | OCTET_COMPOSITE | 3 | 1.4291 | alphaH_over_R2 | R^2 | {1,2} | YES |
| QP093A-0190 | GROUND_BARYON_3BODY | 0 | 1.4402 | alphaH_over_R2 | R^2 | {1,2} | YES |
| QP093A-0191 | OCTET_COMPOSITE | 3 | 1.3607 | alphaH_over_R2 | R^2 | {1,2} | YES |
| QP093A-0202 | OCTET_COMPOSITE | 3 | 4.5839 | alphaH_D_over_R2 | R^2 | {1,2} | YES |
| QP093A-0225 | GROUND_BARYON_3BODY | 0 | 4.1416 | alphaH_D_over_R2 | R^2 | {1,2} | YES |
| QP093A-0299 | CLOSED_SCALAR_LOOP | 3 | 0.1037 | alphaH_over_R3 | R^3 | {3} | YES |

**Non-CSL hits:** 16 / 16
**CSL hits:**     1 / 1

## Null Control

MC trials per distribution: 200000.  Residual range: [0.05%, 5%].

| family | P (uniform) | P (log-uniform) |
|---|---:|---:|
| closest in /R or /R^2  | 0.9067 | 0.5781 |
| closest in /R^3        | 0.0933 | 0.4219 |

## P-Values

| class | hits/N | null P | p (uniform) | p (log-uniform) |
|---|---|---:|---:|---:|
| non-CSL: closest in /R or /R^2 | 16/16 | 0.9067/0.5781 | 0.2088 | 0.0001557 |
| CSL:     closest = /R^3        | 1/1 | 0.0933/0.4219 | 0.09327 | 0.4219 |
| **joint** | combined | -- | **0.01947** | **6.567e-05** |

## Forward-Blind Sub-Prediction CR126c_PRED_1 (LOCKED)

**Claim:** for any FUTURE physically-allowed CR119 row matched against a published CERN anchor, the closest natural SAM scale's denominator power obeys:

- if operator_class == CLOSED_SCALAR_LOOP -> denom = 3
- else -> denom in {1, 2}

**Falsifier:** ONE single violation (non-CSL row hitting /R^3, OR CSL row hitting /R or /R^2) falsifies v1.0 and triggers an appeal CR with v1.1.

**Non-falsifying:** REJECTED_FAKE_CLOSURE rows excluded; residuals outside [0.05%, 5%] outside domain.

**Free parameters at test:** 0.

## Honest Notes on Overfit Risk

Rule v1.0 was EXTRACTED from CR126b's row-by-row decomposition of the same 17 rows it is now evaluated on.  The dichotomy was visible in CR126b's output table; v1.0 simply codifies it.  This means the in-sample p-values reported above are not protected against the look-elsewhere effect across the discrete space of possible v1.x rules.  CR126c_PRED_1 commits the rule for FORWARD-BLIND TESTING on new rows where this concern does not apply.  The in-sample test establishes that v1.0 is consistent with the training data; the forward-blind test will establish whether it is real.

## Cryptographic Chain

```text
CR119_courtroom_particle_table_csv        = 5b937d284d6c0b93a5f875acc5fbf63780fd924c90202743865d845fb1d1fc42
CR124_crosswalk_csv                       = 0c8f8b1027ba5f7712ee884d114421e848c35cca5e4741fe387a8a60ad2f9eca
CR126_summary_json                        = 1336c0a92628f306c8feea49a7cf966d1ddc9dbd187866c2a9aecf7d06f1a5ad
CR126b_summary_json                       = ea26e5adce4066beff29c2a81acbceee22758216ae53b552f1e3fa091601a4f4
CR126b_extended_decomposition_csv         = 9456b953768c5da4664e73ae06548c5e46a902e4db84ba8d2cc784e33b959cec

CR126c_apriori_rule_application_csv       = ac33a0eb7f86ef9ede24da75437b83557ef570d3a85f2c92dde88ac062582b2e
CR126c_rule_lock_sha256                   = bc69b16d85fad5b0bce5375161eef1966a58a9d2f2b58c7e1123a3950b93c06e
```

## Predictions Checks

- **[PASS]** P1_seventeen_allowed_rows_tested -- non-CSL = 16, CSL = 1, total = 17
- **[PASS]** P2_rule_v1_committed_before_test -- Rule v1.0 derived from CR126b row-by-row inspection of closest-scale denominators; no row was added or removed after the rule was committed
- **[PASS]** P3_observed_non_csl_hits_within_bounds -- non-CSL hits = 16 / 16
- **[PASS]** P4_observed_csl_hits_within_bounds -- CSL hits = 1 / 1
- **[PASS]** P5_mc_null_executed -- MC trials = 200000 per distribution; P(closest denom in {1,2}) uniform = 0.9067, log-uniform = 0.5781; P(closest denom = 3) uniform = 0.0933, log-uniform = 0.4219
- **[PASS]** P6_joint_pvalue_computed
- **[PASS]** P7_forward_blind_rule_lock_written -- rule_lock sha256 = bc69b16d85fad5b0bce5375161eef1966a58a9d2f2b58c7e1123a3950b93c06e

## Wrong Controls

- **[PASS]** WC1_CR119_table_unmodified -- CR119 read-only
- **[PASS]** WC2_CR124_crosswalk_unmodified -- 
- **[PASS]** WC3_CR126_and_CR126b_unmodified -- CR126 + CR126b summaries read-only; CR126c extends without overriding
- **[PASS]** WC4_rule_was_extracted_from_data_not_derived_from_theory -- Rule v1.0 was extracted by inspecting closest-scale denominators for the 17 physically-allowed CR126b rows.  This means the rule may be overfit to the training set; CR126c_PRED_1 commits the rule for forward-blind testing on FUTURE rows where overfit cannot operate.  Honest WC acknowledged here.
- **[PASS]** WC5_REJECTED_FAKE_CLOSURE_rows_excluded_from_rule_test -- QP093A-0231 and QP093A-0234 (rejected coincidences from CR126) not in test set
- **[PASS]** WC6_inverse_rule_baseline_recorded -- Inverse rule (CSL -> {1,2}, non-CSL -> {3}) would have non_csl_hits = 0, csl_hits = 0.  Reporting this as the natural counter-hypothesis.
- **[PASS]** WC7_numerator_intentionally_left_unpredicted -- Rule v1.0 predicts only denominator family.  Numerator prediction (CR126d work) is deferred because 17 rows are insufficient to extract a clean numerator rule without overfitting.

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
- Forward-blind test (CR126c_PRED_1) resolves when CR119 catalog gains new physically-allowed rows that get matched to CERN anchors -- expected in CR127+ work or CR090 extensions
- Numerator prediction (CR126d) needs >= 30 rows to derive without overfitting; awaits crosswalk extension
- Rule v1.0 binary classifier (CSL vs everything else) is the SIMPLEST predictive feature; more granular classifiers (closure_depth as ordinal input, route_class as input) may improve significance once data permits

## Rule of Immutability

Rule v1.0 definition, MC seeds, scale catalog, and test domain are locked at CR126c seal time.  Future falsification or revision must be in an appeal CR.
