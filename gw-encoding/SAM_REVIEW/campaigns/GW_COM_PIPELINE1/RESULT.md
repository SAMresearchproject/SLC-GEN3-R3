# GW-COM five-layer GEN3 result

The first complete dimensionless C4 pipeline recovered the prime interval
message from both clean and noisy signed residuals after the declared carrier
and statistical controls passed. Three unmodulated/noise/drift controls were
blocked before decoding.

**The test result suggests the concept is possible.**

| Case | Selected carrier | Repeated packets | Permutation rank | Decoder |
|---|---|---:|---:|---|
| Prime, clean | Constant amplitude | 2 | 1/100 | `2,5,7,11,13,17` |
| Prime, bounded noise + gain 1/2 + DC offset | Amplitude + DC | 2 | 1/100 | `2,5,7,11,13,17` |
| Alternate message, gain 2 | Constant amplitude | 2 | 1/100 | `4,6,8,10,12,14` |
| Unmodulated, clean | Constant amplitude | 0 | 1 | Blocked |
| Unmodulated, bounded noise | Constant amplitude | 0 | 1 | Blocked |
| Unmodulated, amplitude drift + DC | Amplitude drift + DC | 0 | 1 | Blocked |

The source is two prescribed antipodal unit-weight bodies, with identical radial
perturbations carrying interval timing. GEN3 computes the signed quadrupole
second difference, fits three carrier alternatives to a declared quiet prefix,
and subtracts each prediction while retaining signs and sample order. The
validation window is separate from the fit window. It selects the simplest
carrier passing the recorded bounded-noise criterion; all alternatives remain.

Candidate symbolization retains signed marker samples, marker/sample spans,
all framing alternatives and an empirical timing alphabet. Information records
include marker-lag periodicity, exact symbol probabilities and derived Shannon
entropy, actual compression byte lengths, repetition and synchronization.
No parity/code model was defined, so error-correcting structure is explicitly
marked not implemented rather than inferred from repetition.

The recorded rank is `(1 + exceedances)/(1 + 99 permutations)`, counting ties.
There were no shuffled-gap outcomes with a repeat count at least two for the
three admitted signals. Each null preserves the detected gap multiset and
repeats the complete framing/max-repetition search. The value 1/100 is a
finite conditional permutation rank, not a probability that a physical signal
is accidental or intentional. The expected prime sequence does not enter
fitting, symbol selection, permutation testing or decoding.

The drift-only case is useful: the carrier fit absorbed the injected amplitude
drift, and its residual produced no repeated packet candidate. The noisy prime
case selected the DC-capable model; its repeated message survived both adequate
carrier alternatives. This records how source-model choice affects residuals
instead of compressing the outcome into one anomaly score.

## Execution and verification

- Current STARBREAKER / **SLC-GEN3-R4**, CE **SLC-GEN3-CEV1-R4**.
- **37 native calls**, **526,742 native graph nodes**; zero failed/incomplete
  session calls.
- **92 evidence records** checked for retained hashes and ancestry.
- **60,136 source/residual samples** reconstructed independently with exact
  rational arithmetic; **36 normal equations** checked.
- All six permutation-rank calculations and retained gap multisets checked.
- **9 decoder-gate tests** passed, including all nonpass statuses, incomplete
  stages, missing individual evidence, empty controls, changed bytes, mismatched
  candidates and attempts to override failed test values with PASS summaries.
- The final gate reproduced all six admissions and the three decoded outputs
  from saved evidence without repeating native calculations.

## Evidence

- [Run result and case lineage](run001/records/RUN_RESULT.json)
- [Clean prime admission](run001/records/prime_clean.admission.json)
- [Clean prime decoded hypothesis](run001/records/prime_clean.decoded.data.json)
- [Noisy prime information tests](run001/records/prime_noisy.information.data.json)
- [Drift-only blocked admission](run001/records/drift_only.admission.data.json)
- [Independent reconstruction](run001/VALIDATION.json)
- [Final gate checks](run001/gate_verification/VALIDATION.json)
- [Gate test output](run001/gate_verification/TEST_OUTPUT.txt)
- [Native session](run001/sessions/STARBREAKER_1516db9e14494ca0b24e1a646a2f29ce/SESSION.json)
- [Pre-run method snapshot](run001/METHOD.json)

The scope is the declared sampled carrier and idealized readout. Calibration
and validation windows are known quiet simulator intervals; framing is a known
protocol. Continuous orbital control, chirp/precession, additional polarizations,
SI strain, physical detector response and higher-prime strength encoding remain
successor work. Earlier interval-demo results are unchanged.

Sean Brady is originator and conceptual director of the communication concept,
five layers and retained-history requirement. OpenAI ChatGPT and Codex are AI
research collaborators; Codex supplied this bounded implementation and its
declared fit/test choices.
