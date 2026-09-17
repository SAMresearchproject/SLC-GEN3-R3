# GW-COM retained-evidence contract

Status: implemented for the dimensionless C4 successor in
[runtime](runtime), with [gate tests](tests/test_decoder_gate.py). The first
[run and verification](../SAM_REVIEW/campaigns/GW_COM_PIPELINE1/RESULT.md)
retain this chain. Additional physical models must preserve the same contract.

## Common envelope

Every stage record retains `record_id`, `kind`, `schema_version`, `created_utc`,
`campaign_id`, `parent_refs`, `artifact_refs`, `method_ref`, `parameters`,
`units_and_conventions`, `execution_refs` and `status`. A reference names a
repository-relative artifact and its SHA-256. Parents identify exact immutable
versions, not moving "latest" names. Execution references identify real native
calculation receipts when a stage performs research computations.

Records retain content at the referenced paths; a digest alone is not a data
archive. Original numerical precision and exact rational samples are retained
when supplied. New fits, processing choices or corrections create new records.

## Stage records

| Kind | Required evidence beyond the common envelope |
|---|---|
| `raw_waveform` | Signed samples; sample times/order; channels; acquisition or simulation identity; time/phase/polarization conventions; units; gaps and validity masks; calibration/noise metadata |
| `source_fit` | Raw parent; carrier family; fit criterion; parameters/uncertainty; predicted signed samples; fitting/evaluation windows; alternative fits and selection history |
| `modulation_model` | Versioned source-control hypothesis; modulation family; parameter meaning/units; source-to-wave mapping; known versus searched protocol assumptions |
| `residual_history` | Raw and fit parents; aligned observed/predicted samples; signed difference; raw-sample correspondence; masks; transform history and alternatives |
| `candidate_symbolization` | Residual and modulation parents; alphabet definition; symbol/time/polarity sequence; raw/residual sample spans for each symbol; uncertainties and competing assignments |
| `information_tests` | Symbolization and residual parents; complete test configurations/results; search inventory; physical/statistical control evidence; comparisons and declared criteria |
| `decoder_admission` | Exact fit/residual/symbolization/test references; physical and statistical dispositions; missing/failed controls; eligibility and rationale |
| `decoded_hypothesis` | Admitted parent; grammar; decoded sequence and alternatives; symbol-to-sample mapping; correction history; unresolved content and outcome |

The canonical chain is raw → fit → residual → symbolization → hypothesis.
Modulation models, test histories and admission records are additional linked
records, not replacements for any chain element. A scalar statistic may appear
inside a test result but cannot stand in for a stage or its history.

## Decoder admission

Each candidate has distinct `physical_controls` and `statistical_controls`.
Each stores the declared contract reference, individual result references and
a disposition in `NOT_RUN`, `INCOMPLETE`, `FAIL`, `PASS`. Empty result sets do
not count as PASS. Dispositions are operational control statuses, not new
scientific result classifications.

`eligible = physical_controls == PASS and statistical_controls == PASS`

Eligibility additionally requires complete, matching, readable artifact
references through the raw/fit/residual/symbolization/test chain. It is scoped
to that candidate and those versions. A changed fit, residual, alphabet or
search requires a new corresponding control/admission record; earlier outcomes
remain intact. There is no inference of PASS from a low entropy value, high
compression ratio, compelling prime sequence or aggregate anomaly score.

A noneligible candidate retains its analysis artifacts with no candidate
`decoded_hypothesis`. Explicit synthetic protocol demonstrations are cataloged
separately as `CONTROLLED_DEMONSTRATION`; their known-message evaluations never
populate a candidate's admission record automatically.

## Current inventory

`PROGRAM.json` records the preserved demonstration, historical and corrected C4 pipelines, the continuous-source run with its separately retained numerical refinement, and the three fixed follow-up experiments (noise, physical scaling, natural-carrier false positives).
The demonstration retains its missing pipeline stages explicitly.
Its waveform references, transmitter truth, source calculations and demo
decoder outputs remain at the original frozen campaign paths. No source-fit,
residual, information-test or candidate-admission result is fabricated to make
that demonstration appear to be a completed five-layer analysis.
