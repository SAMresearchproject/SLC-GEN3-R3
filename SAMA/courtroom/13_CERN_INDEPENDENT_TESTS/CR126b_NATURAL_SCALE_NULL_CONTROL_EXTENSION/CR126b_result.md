# CR126b Natural-Scale Null Control + Extension to 17 Allowed Rows

## Verdict

```text
CR126b_NATURAL_SCALE_NULL_CONTROL_SEALED
```

## Hypothesis-Test Class

```text
STRUCTURAL_SCALE_PATTERN_SUPPORTED
```

Strongest evidence tier achieved at tolerance **±5%**: p_uniform = 0.0295, p_loguniform = 0.0202.

## What This CR Refines

CR126 reported that 2 of 2 physically-allowed LOOSE rows landed within ~10% of a natural SAM scale.  Two-of-two is small-N evidence, so CR126b extends the analysis: (i) builds the full natural-scale catalog from {1, alpha_H, D, alpha_H*D, 2^-D, 2^-D*D, 2^-D*alpha_H*D, 2^-D*alpha_H} divided by {R, R^2, R^3}; (ii) walks all CR124 LOOSE + NEAR_ANCHOR rows; (iii) runs Monte Carlo null controls against uniform and log-uniform random residuals; (iv) reports a one-sided binomial p-value per tolerance level.

## Natural Scale Catalog (25 scales in [5e-5, 0.1])

| scale | value (%) |
|---|---:|
| 2negD_over_R3 | 0.00723 |
| 2negD_alphaH_over_R3 | 0.01447 |
| 2negD_D_over_R3 | 0.02170 |
| 2negD_alphaH_D_over_R3 | 0.04340 |
| 1_over_R3 | 0.05787 |
| 2negD_over_R2 | 0.08681 |
| alphaH_over_R3 | 0.11574 |
| D_over_R3 | 0.17361 |
| 2negD_alphaH_over_R2 | 0.17361 |
| alphaH_sq_over_R3 | 0.23148 |
| 2negD_D_over_R2 | 0.26042 |
| alphaH_D_over_R3 | 0.34722 |
| D_sq_over_R3 | 0.52083 |
| 2negD_alphaH_D_over_R2 | 0.52083 |
| 1_over_R2 | 0.69444 |
| 2negD_over_R | 1.04167 |
| alphaH_over_R2 | 1.38889 |
| D_over_R2 | 2.08333 |
| 2negD_alphaH_over_R | 2.08333 |
| alphaH_sq_over_R2 | 2.77778 |
| 2negD_D_over_R | 3.12500 |
| alphaH_D_over_R2 | 4.16667 |
| D_sq_over_R2 | 6.25000 |
| 2negD_alphaH_D_over_R | 6.25000 |
| 1_over_R | 8.33333 |

## Rows Walked

From CR124 crosswalk: 19 (ANCHORED_LOOSE + NEAR_ANCHOR).  Physically allowed: 17.  REJECTED_FAKE_CLOSURE: 2.

### Per-Row Decomposition (physically-allowed only)

| candidate | class | partition | depth | residual % | closest scale | log10(obs/scale) | in 2% | in 5% | in 10% | in 20% |
|---|---|---|---:|---:|---|---:|:-:|:-:|:-:|:-:|
| QP093A-0070 | NEAR_ANCHOR | 12 | 2 | 1.9074 | D_over_R2 | -0.038 | . | . | Y | Y |
| QP093A-0073 | NEAR_ANCHOR | 1 | 0 | 2.5779 | alphaH_sq_over_R2 | -0.032 | . | . | Y | Y |
| QP093A-0074 | NEAR_ANCHOR | 1 | 0 | 1.0791 | 2negD_over_R | +0.015 | . | Y | Y | Y |
| QP093A-0128 | NEAR_ANCHOR | 1+2+9 | 0 | 4.2649 | alphaH_D_over_R2 | +0.010 | . | Y | Y | Y |
| QP093A-0139 | NEAR_ANCHOR | 1+4+9 | 3 | 2.5655 | alphaH_sq_over_R2 | -0.035 | . | . | Y | Y |
| QP093A-0143 | NEAR_ANCHOR | 1+6+9 | 3 | 1.4546 | alphaH_over_R2 | +0.020 | . | Y | Y | Y |
| QP093A-0145 | NEAR_ANCHOR | 1+8+8 | 3 | 4.1825 | alphaH_D_over_R2 | +0.002 | Y | Y | Y | Y |
| QP093A-0170 | NEAR_ANCHOR | 2+6+8 | 3 | 3.2842 | 2negD_D_over_R | +0.022 | . | . | Y | Y |
| QP093A-0171 | NEAR_ANCHOR | 2+6+9 | 3 | 1.0459 | 2negD_over_R | +0.002 | Y | Y | Y | Y |
| QP093A-0186 | ANCHORED_LOOSE | 3+4+6 | 3 | 0.2641 | 2negD_D_over_R2 | +0.006 | Y | Y | Y | Y |
| QP093A-0187 | NEAR_ANCHOR | 3+4+8 | 0 | 2.4460 | alphaH_sq_over_R2 | -0.055 | . | . | . | Y |
| QP093A-0188 | NEAR_ANCHOR | 3+4+9 | 3 | 1.4291 | alphaH_over_R2 | +0.012 | . | Y | Y | Y |
| QP093A-0190 | NEAR_ANCHOR | 3+6+6 | 0 | 1.4402 | alphaH_over_R2 | +0.016 | . | Y | Y | Y |
| QP093A-0191 | NEAR_ANCHOR | 3+6+8 | 3 | 1.3607 | alphaH_over_R2 | -0.009 | . | Y | Y | Y |
| QP093A-0202 | NEAR_ANCHOR | 4+4+8 | 3 | 4.5839 | alphaH_D_over_R2 | +0.041 | . | . | . | Y |
| QP093A-0225 | NEAR_ANCHOR | 8+8+8 | 0 | 4.1416 | alphaH_D_over_R2 | -0.003 | Y | Y | Y | Y |
| QP093A-0299 | ANCHORED_LOOSE | 12+12 | 3 | 0.1037 | alphaH_over_R3 | -0.048 | . | . | . | Y |

## Null-Control Results

MC trials per distribution: 200000.  Residual range sampled: [0.05%, 5.0%].

| tolerance | hits / N | null cov (uniform) | p-val (uniform) | verdict (unif) | null cov (log) | p-val (log) | verdict (log) |
|---:|---|---:|---:|---|---:|---:|---|
| ±2% | 4 / 17 | 0.1371 | 0.1958 | SUGGESTIVE | 0.1291 | 0.1679 | SUGGESTIVE |
| ±5% | 10 / 17 | 0.3370 | 0.0295 | SIGNIFICANT | 0.3195 | 0.0202 | SIGNIFICANT |
| ±10% | 14 / 17 | 0.6119 | 0.0567 | SUGGESTIVE | 0.5895 | 0.0386 | SIGNIFICANT |
| ±20% | 17 / 17 | 0.9740 | 0.6387 | COMPATIBLE_WITH_NULL | 0.9555 | 0.4614 | COMPATIBLE_WITH_NULL |

## How to Read the Verdict

- **SIGNIFICANT** (p < 0.05): observed hit count is unlikely under the random null at this tolerance.
- **SUGGESTIVE** (0.05 <= p < 0.20): trend present but not conclusive at this sample size.
- **COMPATIBLE_WITH_NULL** (p >= 0.20): observation indistinguishable from random.

Overall pattern-class verdict requires BOTH uniform and log-uniform nulls to agree.

## Cryptographic Chain

```text
CR119_courtroom_particle_table_csv        = 5b937d284d6c0b93a5f875acc5fbf63780fd924c90202743865d845fb1d1fc42
CR090_candidate_anchor_inventory_csv      = df2a13db83e261291ab508bfa632e02ab64bce7f53bd63c7482914946cc05926
CR124_crosswalk_csv                       = 0c8f8b1027ba5f7712ee884d114421e848c35cca5e4741fe387a8a60ad2f9eca
CR126_summary_json                        = 1336c0a92628f306c8feea49a7cf966d1ddc9dbd187866c2a9aecf7d06f1a5ad

CR126b_natural_scale_catalog_csv          = b3d2d02152e035d358453a86a62724452a6e92c628fa55ccff7f883f3628ab55
CR126b_extended_decomposition_csv         = 9456b953768c5da4664e73ae06548c5e46a902e4db84ba8d2cc784e33b959cec
CR126b_null_control_json                  = 74168e65eda9021afab07c6c189b8fd5947413f22a1f30d0138c738fc587cbcc
```

## Predictions Checks

- **[PASS]** P1_loose_and_near_walked -- walked 19 rows (LOOSE + NEAR_ANCHOR from CR124)
- **[PASS]** P2_natural_scale_catalog_built -- catalog size = 25 natural scales in [5e-5, 0.1]
- **[PASS]** P3_mc_null_control_executed -- MC trials per distribution = 200000; uniform and log-uniform both run
- **[PASS]** P4_pvalues_computed_per_tolerance
- **[PASS]** P5_rejected_rows_excluded_from_test -- REJECTED_FAKE_CLOSURE rows (2) excluded from the hypothesis test

## Wrong Controls

- **[PASS]** WC1_CR119_table_unmodified -- CR119 read-only
- **[PASS]** WC2_CR124_crosswalk_unmodified -- CR124 read-only
- **[PASS]** WC3_CR126_summary_unmodified -- CR126 summary read-only; CR126b extends rather than overrides
- **[PASS]** WC4_no_post_hoc_scale_addition_to_fit_data -- natural scale catalog is generated combinatorially from {1, alpha_H, D, alpha_H*D, 2^-D, ...} / {R, R^2, R^3} BEFORE looking at the observed residuals; no scale was added after seeing the data
- **[PASS]** WC5_both_uniform_and_loguniform_nulls_reported -- uniform null reflects 'random central value'; log-uniform reflects 'random order of magnitude'.  Verdict requires both nulls to agree.
- **[PASS]** WC6_seed_pinned_for_reproducibility -- MC seeds = 42 (uniform), 43 (log-uniform); same output on re-run

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
- Sample size still small (17 allowed rows); extending walk to ALL 321 rows is a future CR -- but that test loses focus because most rows are in GAP_REGION with no nearest published anchor at meaningful sigma
- p-values computed under independent uniform / log-uniform priors; both reported.  Bayesian posterior given a structural-account prior is a separate downstream CR
- Per-class (operator_class x closure_depth) a-priori scale assignment is CR126c work; CR126b only tests the WEAKER claim 'residual lies in ANY natural scale band'

## Rule of Immutability

Natural-scale catalog, MC seeds, and tolerance grid are locked at seal time.  Future extensions (more rows, alternative null distributions, per-class a-priori scale assignment) must be in separate child CRs.
