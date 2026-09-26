# Provenance and limits

## Preserved sources

1. Author-supplied `Finite_Redshift_Identifiability_Distance_Ratios.pdf`, recovered from the local SAM PAPER folder. Copied byte-for-byte; it remains the manuscript authority for this package.
2. Same-named DOCX recovered from Downloads. Preserved as a companion source document; PDF and DOCX are not asserted to be text-identical. No embedded original code or result archive was found in the DOCX.
3. `paper/manuscript.txt` is a `pdftotext -layout` extraction. Two-column layout and equations can render imperfectly; consult the PDF for interpretation.
4. `paper/reported_results.json` transcribes selected manuscript numbers, including page locations. These are historical reported values, not recovered historical output files.
5. `related/DISTANCE_METHOD.md` and `related/VIBE2_DISTANCE_LOCAL_RETURN.json` are unchanged copies from the earlier `GEN4/vol_i_branch_expansion2` campaign. Original relative paths and byte hashes appear in `records/related_sources.json`.

No original Supplementary Material scripts, numerical result files, figure sources or reference-verification notes were recovered in targeted searches of the manuscript folders and relevant local research branches. An earlier draft was identified but is not treated as the authority for the expanded manuscript. The present package does not invent original execution receipts or attribute its new runs to the historical paper. The paper’s acknowledgement that its original simulations were not new Codex/GEN4 executions remains intact.

## New work and evidence types

- `src/model.py`, `src/reproduce.py`, `src/compare.py`, `src/verify.py`, tests and companion documentation are new independent work in this publication task.
- `data/`, `results/` and `figures/` are outputs of the new independent implementation, except explicitly labelled historical transcriptions in `paper/` and archived background in `related/`.
- Symbolic identities are checked with SymPy. Floating-point identities and simulations are numerical checks; no Arb enclosures or exact-arithmetic certification are claimed.
- The original PCG generator/draw order was not supplied, so the historical seed is insufficient for bitwise replication. The new generator and ordering are now recorded completely.
- The original extended experiment’s covariance is unresolved: the paper says it uses the same covariance, but reported deterministic Fieller/binning values match an alternative. Both matrices and the diagnostic are published without silently revising the paper.
- Historical Hankel grids, the 72 original test parameters and some illustrative figure parameters are underspecified. New choices are explicit and are not represented as recovered choices.

## Related research: what transfers

The inherited branch studies `q(u)=1−1/pi+(1/pi)u^−3` as a particular distance-coordinate response. Its admissible transfer here is **representation and covariance technique**: a constant-plus-power function, preservation of response history, and transforming the covariance when transforming coordinates. The 18-test suite includes an independent two-channel covariance-invariance check.

Its cosmological normalization, physical interpretation, Arb bounds, thermal background and source-packet numbers are **not** imported as evidence for the paper’s free `(Xi0,n,C)` statistical model. Its JSON contains original execution paths and historical owner-state fields as archival context, not current authority. The full old campaign is not rerun or claimed self-contained in this package; only the two identified background records are preserved. Neither is needed by the standalone paper replay.

## Scope and custody

This publication adds one isolated package and an index link. It does not alter original research sources, global selectors, production implementations, RH campaigns or prior scientific verdicts. No unrelated job or cloud pod was used. New calculations ran locally on the author’s machine, and the package is self-contained for its stated statistical checks.

Beginning negative-drift check: CLEAR — compile this paper’s reproducibility evidence, preserve original sources, label new calculations, and avoid importing unrelated physical claims.

Completion negative-drift check: CLEAR — original documents and historical records preserved; simulation and symbolic/numerical statuses distinguished; missing sources and failed numerical reproduction retained; no observational or asymptotic claim promoted from finite synthetic evidence.
