# Reproduce and verify

Run from this directory. The published full run used CPython 3.12.3 on Linux x86_64, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0 and Matplotlib 3.10.7. The manuscript reports Python 3.13.5; this is a disclosed environment difference. [records/environment-lock.txt](records/environment-lock.txt) captures the tested dependency versions. No GPU, cloud pod, licensed data or external research service is required.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/verify.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python src/reproduce.py --output /tmp/finite-redshift-replay
.venv/bin/python src/compare.py --run /tmp/finite-redshift-replay
.venv/bin/python src/verify.py --replay /tmp/finite-redshift-replay
```

Choose a new, empty output directory. The generator refuses to overwrite completed output. For an inexpensive smoke run add `--quick`; it intentionally changes sample counts and random-stream positions and must not be compared to full-run artifacts. The full run took about three seconds of computation in the recorded environment, excluding environment installation; hardware and startup costs vary. Allow about 150 MB for artifacts plus working memory (under 1 GB here). No privileged commands are needed once Python and its venv support are available.

`src/verify.py` first checks the published SHA-256 inventory. With `--replay` it also compares every stored NPZ array and result JSON value against a fresh full run. Floating results allow rtol=1e-7, atol=1e-10 for ordinary platform/library differences. This is a comparison tolerance, not a confidence interval or mathematical error enclosure. Records with timestamps and rendered PNG/PDF metadata are not replay-compared. The integrity manifest still checks their archived bytes. If an environment changes rank decisions at thresholds, investigate rather than silently increasing tolerance.

## Exact generation contract

- Table I: `default_rng(20260927)` / PCG64; 30,000 null calibration catalogues, then 20,000 catalogues for each of five cases in table order. Each draw call generates the full correlated Gaussian matrix before the full centered-lognormal matrix. The covariance always uses the fiducial mean, including the C=0.96 case.
- Exponent search: 311 equally spaced values, n=0.25 through 8, spacing 0.025. Fixed-n uses n=3. The profile statistic selects the maximum squared projection on this finite grid. Noiseless best fits instead use continuous bounded minimization, as explicitly recorded in the code.
- Empirical thresholds use NumPy’s default linear 95th-percentile quantile and strict `>` rejection. The constant-null experiment additionally stores finite-Monte-Carlo rank p-values.
- Extended Gaussian checks use a separate `default_rng(20260926)` stream, sequentially: 100,000 Fieller catalogues; 20,000 calibration and 20,000 evaluation standard-normal whitened vectors; 100,000 held-out catalogues; 200,000 five-point Hankel catalogues. Gaussian exact pivot statements apply to this part, not automatically to the asymmetric Table I noise.
- The Hankel experiment uses five equally spaced log-redshifts between z=0.03 and 2. This independently selected grid is recorded because the historical grid is missing. The 72-case inverse grid is likewise declared explicitly in the implementation.
- Thread counts are set to one before numerical-library import in the generation and comparison entry points.

`src/compare.py` regenerates the comparison and the two covariance diagnostic CSVs. It preserves the declared covariance as the primary experiment; the diagnostic alternative does not replace it. All random matrices needed for the Table I statistics are archived. Extended runs archive sufficient per-catalogue statistics and regenerate their raw random draws from the complete contract above.

## Data dictionary

`design.csv`: redshift z, log-redshift s, fiducial mean, total fractional standard deviation and lognormal-component fractional RMS. `design.npz` additionally contains core/total covariance and the exponent grid. Units are dimensionless.

`calibration_catalogs.npz`: `(30000,24)` catalogue array and fixed/profile statistics. Each `*_catalogs.npz`: `(20000,24)` catalogue array, noiseless mean, two test-statistic vectors and fixed-n Xi estimates. `extended_statistics.npz`: Fieller pivot, calibration/evaluation scan maxima, rank p-values, held-out chi-square statistic, and raw/corrected two-column Hankel determinants. Load with `numpy.load(path, allow_pickle=False)`.

Covariance CSVs have 24 rows and columns in `design.csv` order. The `diagnostic_...` covariance is deliberately an alternative, not observational data. Result JSONs contain counts, rates, fitted parameters and analytical/empirical quantities. Figure filenames correspond to manuscript topics, not pixel-identical reproductions.
