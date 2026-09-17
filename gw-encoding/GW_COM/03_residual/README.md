# 3. Residual extractor

For each retained source fit, form the signed residual

`residual(t, channel) = observed_waveform(t, channel) - predicted_waveform(t, channel)`.

Input: the immutable raw record, source-fit identity, predicted waveform,
alignment/resampling operations and validity masks. Both operands must share
declared units, channel convention and time coordinates before subtraction.

Output: the full signed, time-ordered residual; the aligned operands; sample
maps back to the original data; uncertainty/noise assumptions; validity masks;
and the exact parent artifacts. Preserve each competing source-fit residual.

Whitening, filtering, envelopes, absolute values, spectra and compressed
representations are separately versioned derived products. Retain transforms,
phase/delay conventions and original signed samples so the source subtraction
can be reconstructed. Do not join separated valid intervals as if adjacent.

The unexplained component is a residual relative to a specified model. The
information layer investigates its structure while preserving physical-model
and processing explanations in the same lineage.

The [residual runtime](../runtime/residual.py) now executes exact native
prediction and signed subtraction for all three C4 fit alternatives, retaining
every sample and raw-index mapping. Independent checks reconstruct every
sample. The earlier demo's envelope analysis remains separately preserved.
