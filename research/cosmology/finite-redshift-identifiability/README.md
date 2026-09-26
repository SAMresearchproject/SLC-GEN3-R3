# Finite-redshift identifiability of distance ratios

Reproducibility companion to Sean Brady’s **Finite-redshift identifiability of cosmological distance ratios**, expanded author-review manuscript dated 25 September 2026. The supplied PDF is preserved unchanged in [paper/](paper/). This addition was assembled and executed on 26 September 2026 at the author’s request.

**This is an independent, executable reconstruction and reproducibility audit, not the recovered original Supplemental Material.** The original simulation scripts, historical result files, figure sources, and reference-verification notes mentioned in the manuscript were not located. The author-supplied PDF and DOCX, manuscript-reported numbers, newly executed calculations, and inherited research records are distinguished throughout.

All statistical inputs here are **synthetic**. No supernova, BAO, gravitational-wave, or other observational catalogue was fitted or downloaded. No claim of detecting modified propagation or determining a model-independent infinite-redshift plateau follows from these experiments.

## Contents

| Path | Contents |
|---|---|
| [REPRODUCE.md](REPRODUCE.md) | Environment, commands, replay and verification |
| [RESULTS.md](RESULTS.md) | Reported versus independently computed results, including discrepancies |
| [CLAIM_MAP.md](CLAIM_MAP.md) | Paper claims mapped to equations, code, tests and artifacts |
| [PROVENANCE.md](PROVENANCE.md) | Source custody, assumptions and remaining gaps |
| [paper/](paper/) | Original PDF/DOCX, extracted text, transcribed historical numbers |
| [src/](src/) and [tests/](tests/) | Executable calculation, comparison, verification and 18 tests |
| [data/](data/) | Synthetic design, covariance matrices, 130,000 non-Gaussian catalogues and extended test statistics |
| [results/](results/) | Machine-readable independent outputs and covariance diagnostic |
| [figures/](figures/) | Five newly generated illustrations; not original figure files |
| [records/](records/) | Execution receipt, test log, environment, source inventory and replay verification |
| [related/](related/) | Two inherited distance-coordinate background records, explicitly separate from this paper’s evidence |
| [HASHES.sha256](HASHES.sha256) | Integrity manifest for every other published package file |

The main run follows the declared covariance in Eqs. (69)–(72). It reproduces the Table I noiseless fits and Table II Fisher uncertainties to reported precision. **The reported deterministic Fieller interval and binning exponent do not match that covariance.** A diagnostic covariance variant matches their published rounded values; this does not establish which original code was used. See [RESULTS.md](RESULTS.md).

The companion implements the stated synthetic experiments, algebra checks and diagnostics. It does not replace the manuscript, certify every proof, independently verify its bibliography, or supply an observational analysis pipeline. Numerical agreement is labelled numerical; symbolic checks are labelled symbolic.

Sean Brady originated and directed the research and authorized this public addition. ChatGPT assistance described in the manuscript belongs to the original work. This Codex session supplied the separate implementation, executed verification, provenance audit and packaging recorded here. The repository’s research-only license applies to the new code and documentation; inclusion does not relicense third-party works cited by the paper.
