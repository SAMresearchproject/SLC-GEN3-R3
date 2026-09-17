# 4. Information tests

Own candidate discovery and structured assessment before candidate decoding.

| Family | Retain |
|---|---|
| Periodicity | Period/phase hypotheses, scan range, windowing and stability |
| Entropy | Estimator, sample counts, binning/alphabet, scale and comparison distributions |
| Compression | Actual compressor/encoding, headers, byte lengths and matched baselines |
| Symbol alphabets | Every admitted boundary/cluster map, ambiguous assignments and sample support |
| Repetition | Repeated segments, alignment alternatives and mismatch histories |
| Synchronization | Marker candidates, clock estimates, framing alternatives and search scope |
| Error-correcting structure | Candidate code/parity relations, constraints tested and mismatches |

Inputs are signed residual histories and declared derived views, with their
source-fit and modulation-family identities. Each candidate symbolization
retains the original sample intervals, polarity, timing, uncertainty and
alternative assignments. Searching or selecting an alphabet is part of the
recorded search, not evidence that a message has already been decoded.

Each campaign states its physical and statistical controls and decision rules
before using their outcomes for decoder admission. Relevant physical controls
can include competing source/readout fits, unmodulated sources and injection
recovery through the complete fit/subtraction path. Relevant statistical
controls can include matched noise/surrogates, held-out data, search accounting
and calibrated accidental-pattern rates. The actual set and thresholds belong
to the campaign contract; this document does not impose a universal roster.

Preserve every control's inputs, method, parameters, seed where applicable,
observed result, decision rule and status. Preserve search multiplicity and
data reuse, so selecting an appealing period/alphabet cannot disappear from
the record. Shuffles must state which temporal/noise structures they destroy.

Output is a structured record with candidate alternatives and separate physical
and statistical control dispositions. No composite anomaly score replaces the
evidence. An incomplete or failed disposition leaves the decoder unavailable;
the candidate and its results remain retained.

The [information runtime](../runtime/information.py) now retains signed marker
support, all framing alternatives, interval alphabets, lag histograms, symbol
probabilities/entropy, compression lengths and repetition. It searches every
framing start again in each of99 shuffled-gap controls. Native exact ratios
support the statistical decision. Error-correcting-code search remains
unimplemented. The conditional interval-order null is not a universal physical
noise calibration. The first demo remains separately preserved.
