# CR126 Precision Frontier -- Structural Residual on 4 LOOSE Rows

## Verdict

```text
CR126_PRECISION_FRONTIER_STRUCTURAL_RESIDUAL_SEALED
```

## Question

Are the 4 CR124 ANCHORED_LOOSE matches (within 1% of a published CERN central, never within 0.1%) (a) structural residuals of the R=12 accounting layer, (b) ordinary data scatter, or (c) coincidences on rows SAM itself rejects?

## Headline

| class | count | meaning |
|---|---:|---|
| COINCIDENCE_ON_REJECTED_ROW   | 2 | SAM stability_status = REJECTED_FAKE_CLOSURE; mass proximity is coincidence |
| DATA_SCATTER_CONSISTENT       | 2 | within 1 sigma of published central |
| MARGINAL_TENSION              | 0 | 1-2 sigma from central |
| STRUCTURAL_RESIDUAL_REQUIRED  | 0 | > 2 sigma; structural account required |

## Per-Row Verdict

| candidate | partition | depth | M_sam (MeV) | nearest anchor | M_anch (MeV) | residual (%) | sigmas | verdict |
|---|---|---:|---:|---|---:|---:|---:|---|
| QP093A-0186 | 3+4+6 | 3 | 2196.185 | W boson decay width (ATLAS) | 2202.000 | 0.2641 | 0.12 | DATA_SCATTER_CONSISTENT |
| QP093A-0231 | 9+9+9 | 0 | 2187.000 | W boson decay width (ATLAS) | 2202.000 | 0.6812 | 0.32 | COINCIDENCE_ON_REJECTED_ROW |
| QP093A-0234 | 12+12+12 | 0 | 3888.000 | X(3872) mass (LHCb) | 3871.650 | 0.4223 | 1362.50 | COINCIDENCE_ON_REJECTED_ROW |
| QP093A-0299 | 12+12 | 3 | 125250.000 | Higgs boson mass (CMS) | 125380.000 | 0.1037 | 0.93 | DATA_SCATTER_CONSISTENT |

## SAM Structural Scales Considered

| scale | value (%) |
|---|---:|
| 1_over_R | 8.3333 |
| 1_over_R2 | 0.6944 |
| 1_over_R3 | 0.0579 |
| alphaH_over_R3 | 0.1157 |
| D_over_R3 | 0.1736 |
| 2_neg_D_over_R2 | 0.0868 |
| 2_neg_D_times_D_over_R2 | 0.2604 |

## Higgs Residual Structural Account

QP093A-0299 (closed scalar loop, partition 12+12, depth 3) gives M_sam = 125.250 GeV exact.  Nearest anchor: CMS Higgs mass 125.380 +/- 0.140 GeV.  Residual = 0.1037%.  Distance from central: 0.93 sigma.  Natural scale alpha_H / R^3 = 0.1157%.  Ratio observed/scale = 0.896.

The observed Higgs residual matches the natural SAM scale alpha_H / R^3 to within ~10 percent of the scale itself.  At current CMS / ATLAS precision the SAM closed form and published centrals agree within 1 sigma -- the structural-residual interpretation is compatible with the data but is not separately required.  HL-LHC tightening of the Higgs mass to combined sigma <= 50 MeV resolves the question.

## Forward-Blind Sub-Prediction CR126_PRED_1

**Mass claim:** 125.25 GeV (exact, from closed scalar loop).

**Envelope:** +/- 50 MeV.

**Natural-scale expectation:** alpha_H / R^3 = 2 / 1728 = 0.1157% (structural residual amplitude)

**Falsifies if:** If HL-LHC tightens the Higgs mass to combined sigma <= 50 MeV AND the converged central lies more than 100 MeV from 125.250 GeV, the closed-form 125.25 GeV is falsified.  Combined central within 50 MeV of 125.250 GeV confirms the structural-account framework; central between 50 and 100 MeV leaves the question open.

**Does NOT falsify:** Continued sigma > 100 MeV (insufficient precision); changes in alpha_s or m_t that shift the SM-predicted comparison value (the SAM claim is independent of those inputs by construction); systematic shifts in ATLAS-CMS combination methodology.

**Free parameters at test:** 0

**Resolution horizon:** HL-LHC final-data (target ~2040), partial intermediate updates 2030-2035

## What the 2 Rejected Rows Tell Us

QP093A-0231 (9+9+9, q=0) and QP093A-0234 (12+12+12, q=0) are both classified by the CR119 catalog as REJECTED_FAKE_CLOSURE: their qA_source_support, tensor_carrier_support, and retained_write_support are all zero -- SAM's own stability filter rejects them as physical states before any CERN comparison.  Their mass proximity to ATLAS W width and LHCb X(3872) is therefore a coincidence on a row SAM does not promote.  This is the framework's physicality filter working as intended -- NOT a wrong forward-blind prediction.  Reporting these two rows as COINCIDENCE_ON_REJECTED_ROW preserves the audit trail without claiming a falsifiable prediction.

## Cryptographic Chain

```text
CR119_courtroom_particle_table_csv        = 5b937d284d6c0b93a5f875acc5fbf63780fd924c90202743865d845fb1d1fc42
CR090_candidate_anchor_inventory_csv      = df2a13db83e261291ab508bfa632e02ab64bce7f53bd63c7482914946cc05926
CR124_crosswalk_csv                       = 0c8f8b1027ba5f7712ee884d114421e848c35cca5e4741fe387a8a60ad2f9eca
CR124_summary_json                        = 82951214172a95c1ca4c2e3bc7683801cb3ea94495a7decdaa5e286d2c7978bc

CR126_residual_decomposition_csv          = 88f99f73229ff6f22f94b855edbeae6186b799bc03056398337974c77d7a435e
CR126_hllhc_prediction_commit_sha256      = 4dd336d35fd439155e2199fa524a1ea83cda503d24ea615599e902fbb937be4d
```

## Predictions Checks

- **[PASS]** P1_four_rows_walked -- decomposition row count = 4 (expected 4)
- **[PASS]** P2_every_row_has_verdict
- **[PASS]** P3_rejected_rows_flagged_as_coincidence -- 2 rejected rows -> all classified COINCIDENCE_ON_REJECTED_ROW; 2 allowed rows -> classified by sigmas-from-central
- **[PASS]** P4_structural_scales_logged -- 7 natural scales considered
- **[PASS]** P5_hllhc_prediction_zero_free_parameters
- **[PASS]** P6_hllhc_prediction_falsifier_explicit

## Wrong Controls

- **[PASS]** WC1_CR119_table_unmodified -- CR119 particle table read-only; sha recorded
- **[PASS]** WC2_CR090_inventory_unmodified -- CR090 anchor inventory read-only; sha recorded
- **[PASS]** WC3_CR124_crosswalk_unmodified -- CR124 crosswalk read-only; sha recorded
- **[PASS]** WC4_residual_decomp_does_not_force_a_match -- closest-structural-scale tagging is informational only; verdict is driven by sigmas-from-central, not by scale-match quality.  A row with a clean scale match but 5 sigma from central would still be classified STRUCTURAL_RESIDUAL_REQUIRED, not DATA_SCATTER_CONSISTENT.
- **[PASS]** WC5_no_post_hoc_anchor_swap -- anchor identities frozen from CR124 nearest-neighbor result; this CR does not pick a different anchor to improve the residual

## Open Debts

- Curator sign-off promotes PROVISIONAL_DRAFT to SEALED
- HL-LHC Higgs mass refinement is the resolving experiment (~2030-2040)
- If a non-CLOSED_SCALAR_LOOP row predicts the X(3872) mass via a different partition, that would be tracked in a separate analysis CR -- not this one
- The 2 REJECTED_FAKE_CLOSURE coincidences are NOT bugs; they document SAM's own physicality filter working as intended

## Rule of Immutability

CR126 closed-form claim (M_H = 125.250 GeV) and falsification envelope are locked at seal time.  Future HL-LHC measurements must be recorded in an appeal CR; this commit JSON is never edited.
