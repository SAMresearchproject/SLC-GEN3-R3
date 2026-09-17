# GW-COM first five-layer GEN3 run

This is the executable successor to the interval demonstration, scoped to the
dimensionless prescribed C4 orbit. It implements source fitting, modulation,
signed residuals, structured information tests and candidate-gated decoding.
It preserves the complete waveform → fit → residual → symbols → hypothesis
chain, all three fit alternatives and every null permutation.

[RESULT.md](RESULT.md) records the completed outcome. [CONTRACT.json](CONTRACT.json)
declares the fit family, known quiet calibration/holdout windows, marker and
framing assumptions, physical/model controls and statistical criteria. A copy
of the contract and implementation was saved before the run in
[run001/code](run001/code).

The C4 source and readout are synthetic and dimensionless. The carrier family
is constant amplitude, amplitude plus DC, and linear amplitude drift plus DC.
It does not implement continuous binary dynamics, chirp, precession, multiple
polarizations, calibrated detector strain or an error-correcting-code search.

## Execute a successor

From the repository root, use a new run name:

```bash
.venv-r3/bin/python CURRENT_REVISION/engines/SLC/gen3/resources.py run -- \
  .venv-r3/bin/python SAM_REVIEW/campaigns/GW_COM_PIPELINE1/run.py --run run002
```

Each run directory is created exclusively. Existing evidence is never
overwritten. Changes to the scientific contract should be made in an isolated
successor campaign; saved snapshots preserve the original run semantics.

For a new run, substitute its name in these commands:

```bash
.venv-r3/bin/python SAM_REVIEW/campaigns/GW_COM_PIPELINE1/verify.py run002
.venv-r3/bin/python SAM_REVIEW/campaigns/GW_COM_PIPELINE1/verify_gate.py run002
.venv-r3/bin/python -m unittest discover -s GW_COM/tests -v
```

Both verification scripts preserve their reports exclusively. To inspect an
existing verified run, read the saved reports rather than overwrite them.

## Runtime and numerical roles

The modules under [GW_COM/runtime](../../../GW_COM/runtime) implement the five
layers. Current STARBREAKER DomainSession calls execute source quadrupoles,
readout arithmetic, exact least-squares fitting, all predicted/signed-residual
samples and exact statistical ratios on SLC-GEN3-R4. Session inputs/outputs are
retained as compressed, authenticated receipts.

Python compiles graphs, constructs prescribed source and measurement-noise
inputs, enumerates candidate frames and permutations, runs standard zlib
compression, renders the derived Shannon diagnostic from native probabilities,
and independently reconstructs exact source/fit/residual relationships. The
receiver contains no prime test or expected-message input.

Carrier selection uses the simplest model compatible with the declared
held-out bounded-noise criterion. All other predictions and residuals remain.
Physical controls are relative to this C4 carrier/readout family. They include
the clean/noisy unmodulated and drift-only cases and preservation of a repeated
candidate under every adequate fit. Statistical admission requires two disjoint
repeated packets and a permutation rank at most 1/20 against 99 shuffled-gap
orders, with the same complete framing search applied to every permutation.

The decoder checks exact lineage, artifact hashes, complete stage records and
nonempty individual physical/statistical control evidence. It checks the
retained repetition/rank criterion again before interpreting timing bins as
integer hypotheses. Rejected cases have no decoded-hypothesis artifact.
Expected messages enter only the separate post-decode evaluation.

The supplemental gate verification retains the final checks against the saved
run, including explicit missing-evidence and incomplete-stage rejection. It
does not refit the data or replace the original run's code snapshot.
