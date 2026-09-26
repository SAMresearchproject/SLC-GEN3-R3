# Claim-to-artifact map

The PDF supplies the proofs and scope. This index identifies the companion’s executable coverage; it is not a claim that a finite test proves the theorems.

| Manuscript component | Implementation / check | Archived evidence |
|---|---|---|
| Theorems 1–2, finite-window endpoint obstructions | `test_slow_mode_bound`, `test_fast_mode_bound`; declared illustrative parameters in `reproduce.py` | Figure 1; manuscript proofs |
| Known-exponent and equal-grid recovery | SymPy tests `test_known_exponent_two_point_symbolic`, `test_equal_grid_inverse_symbolic` | Test log |
| Irregular triplet and four-point reconstruction | `model.recover`; 72 declared cases and shared-exponent check | `results/deterministic_checks.json` |
| Two-mode Hankel factorization | SymPy exact polynomial expansion | Test log and deterministic checks |
| Overlapping contrast / GLS equivalence, Eqs. (48)–(51) | `model.contrasts`, `Likelihood.fit`, correlated-data equivalence test | Deterministic checks and tests |
| Fixed-n Fieller confidence set, Eq. (53) | Gaussian pivot and quadratic inversion in `reproduce.py` | `results/extended.json`, pivot array; covariance discrepancy in `comparison.json` |
| Constant-null finite-grid scan and Monte Carlo p-value | Whitened `Likelihood.Q`, maximum projection and rank p-value | Calibration/evaluation arrays, Figure 4 |
| Finite-bin design, Eqs. (62), (76) | Exact top-hat integral, independent quadrature test | `results/binning.json`, covariance diagnostic |
| Hankel bias and joint covariance | Quadratic-form trace formulas, 200,000 Gaussian draws | Raw/corrected determinant arrays, theory/empirical covariance |
| Correlated held-out statistic, Eqs. (63)–(67) | Training first 16, testing final 8; independent full linear-map covariance check | Held-out statistics and test log |
| Eq. (69)–(72) error specification | `model.design`, `model.noise`; diagonal-variance test | CSV/NPZ designs, covariance matrices |
| Table I / smooth versus localized alternatives | Five explicit means, 30,000 calibration + 100,000 evaluation catalogues | `results/table_i.json`, full catalogues, Figure 3 |
| Table II / Fisher information | Analytical derivative matrix, four specified designs | `results/table_ii.json`, Figure 5 |
| Calibration constraint C=1 | One-parameter fixed-n GLS | Table I JSON: Xi=0.9503406, noncentrality=6.37717 |
| Common-gain covariance | Contrast annihilation and exact model-column nullspace | Deterministic checks, tests |
| Earlier source/receiver work | Archived distance-method / local-return record, separate covariance-invariance control | `related/`, source hashes; background only |

The observational-application discussion, bibliography verification, full historical source recovery and arbitrary physical propagation models are outside this executable coverage. Conditional spectral bounds remain analytical statements in the preserved manuscript; selected endpoint examples are not a proof audit of all possible measures.
