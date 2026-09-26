# Independent results and reproduction audit

All results below are from the new local execution unless marked “paper”. The frozen numerical outputs, original reported values and covariance diagnostic are in `results/`, `paper/reported_results.json` and `results/comparison.json` respectively.

## Main findings

The declared model and covariance reproduce the Table I noiseless fits and all four Table II Fisher uncertainties to the manuscript’s displayed precision. Eighteen tests pass. The exact polynomial identities pass symbolic simplification; the 72-case inverse has maximum parameter error 6.67e-14, and the overlapping four-point exponent error is 2.79e-13. The contrast/GLS statistic differs by 5.0e-14 in the recorded deterministic control.

The declared 30,000-catalogue non-Gaussian calibration yields critical values **34.14664 / 32.95055**, versus the manuscript’s **34.1599 / 32.8542**. These are independently generated calibrations, not recovered historical files.

| Input (20,000 catalogues each) | Paper fixed / profile rejection | New fixed / profile rejection | New noiseless n / Xi0 |
|---|---|---|---|
| Single power C=1.04 | 5.09% / 5.06% | 5.200% / 5.025% | 3.00000 / 0.90000 |
| Same shape C=0.96 | 4.97% / 5.15% | 4.920% / 4.950% | 3.00000 / 0.90000 |
| Second power | 5.20% / 5.20% | 5.100% / 4.960% | 2.57760 / 0.91611 |
| Calibration drift | 4.97% / 5.03% | 4.875% / 4.825% | 3.34482 / 0.90972 |
| Localized departure | 6.20% / 5.87% | 6.285% / 5.920% | 2.95009 / 0.90775 |

At a 5% rate, an individual 20,000-catalogue evaluation has conditional Monte Carlo standard error about 0.154 percentage points. Calibration uncertainty also matters, and all rows share their thresholds. These comparisons support the same finite-experiment interpretation, not equality of historical random draws. Smooth alternatives have little power at this precision while their fitted plateau can move appreciably. The localized departure is only weakly distinguished.

The fiducial fixed-n Xi estimator has mean 0.900421 and standard deviation 0.021445 (paper 0.90073 / 0.02150). Forcing C=1 gives Xi=0.9503406 and noncentrality 6.37717, reproducing the reported 0.95034 / 6.38.

## Deterministic covariance discrepancy retained

The manuscript says the extended checks use the same 24-point covariance. Eqs. (69)–(72) give a correlated core with `fcore=sqrt(f²−ell²)`, plus independent tail variance. A second matrix, using `f` directly in the correlated covariance with no separate tail, produces the manuscript’s rounded Fieller and binning numbers instead.

| Quantity | Paper | Declared covariance rerun | Diagnostic alternative |
|---|---|---|---|
| sigma(C) | 0.01595 | 0.01583967 | 0.01595145 |
| Noiseless Fieller interval | [0.85863, 0.94365] | [0.85897736, 0.94326754] | [0.85862629, 0.94365069] |
| Point-center bin-fit exponent | 3.01539 | 3.01540890 | 3.01538954 |
| Bin-fit noncentrality | 1.94e-6 | 1.967203e-6 | 1.944764e-6 |

Both matrices have identical marginal variances; their **off-diagonal correlations differ**. These are deterministic differences, so Monte Carlo variation does not explain them. The alternative’s numerical agreement suggests a historical covariance mismatch, but original scripts are needed to establish provenance. No manuscript text or declared model has been silently corrected. The main run uses the declared equations; the diagnostic alternative is separately archived and reproducible with `src/compare.py`.

The window-aware fixed-n fit recovers Xi=0.9 and C=1.04 to floating-point precision under the declared covariance. The bin-centering lesson survives this numerical discrepancy.

## Extended checks

- Fieller coverage: **95.085% of 100,000** Gaussian catalogues (paper 95.017%). This validates the fixed-n Gaussian pivot in the declared independent experiment; it is not a non-Gaussian or profiled confidence guarantee.
- Constant-null scan: independently calibrated cutoff **4.71922**, rejection **5.395%**; using a single-exponent chi-square cutoff rejects **8.715%**. Paper: 4.81599, 5.08%, 8.93%. Both calibration and evaluation have 20,000 draws. The difference in calibration streams and the unresolved historical covariance preclude a bitwise or exact-threshold reproduction claim.
- Correlated held-out test: mean **8.01079**, rejection **5.157%**, 100,000 Gaussian catalogues and eight held-out degrees of freedom. Paper: 8.00894 / 5.005%. The rejection is about 2.28 binomial standard errors above 5%; it is retained without reseeding. A separate deterministic full-linear-map test verifies the predictive covariance.
- Hankel bias: theory **−0.0018**; new first-contrast empirical bias **−0.00179906**, corrected mean **9.38e-7**. Theory / empirical overlap correlation **−0.15973 / −0.15593** on the explicitly declared new five-point grid. The paper reports −0.20587 / −0.20501 on an unspecified historical grid, so those correlation values are **not directly reproduced or contradicted** here.
- Fisher sigma(n), low / broad / high / three-band: **10.81027 / 2.04982 / 21.84091 / 1.90631**. Corresponding sigma(Xi): **0.20500 / 0.02174 / 1.20322 / 0.01883**. All agree with Table II rounding.

## What is and is not established

This package supplies a complete replay of the new implementation and a clear audit of historical reproducibility gaps. The recovered background confirms prior constant-plus-power and matched-covariance work, but imports no physical identification into the paper. No observational conclusion, new propagation detection, universal proof from simulations, or replacement of prior scientific authority is claimed.

To close the historical gaps, recover the original supplement, identify the covariance used for its extended checks, and identify its Hankel/test grids and RNG draw order. These are provenance questions, not reasons to obscure or discard the independent results.
