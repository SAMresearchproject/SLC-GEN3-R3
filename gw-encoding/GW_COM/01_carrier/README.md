# 1. GW carrier model

Own the physical binary/orbital source and its predicted observation: phase
evolution, amplitude, polarization, chirp and precession. Separate source
coordinates from propagation, detector projection and measurement noise.

Input: immutable raw waveform and acquisition/simulation metadata; a versioned
source-model family, fit criterion, parameter domain and noise/readout model.

Output: fitted parameters and uncertainties, predicted signed waveform on a
specified time grid, fit diagnostics, selected-model criterion, alternative
fits, and model/configuration/code/native-receipt identities. Mark unsupported
effects explicitly rather than silently setting them to zero.

The selected fit is "best" only under its recorded criterion and admitted
model family. Preserve model uncertainty and alternatives for residual/control
analysis. The expected prime message is not a fit objective. Training and
evaluation windows and any data-dependent model selection remain recorded.

Current asset: the dimensionless prescribed antipodal C4 source in
[GW_COM_INTERVAL1](../../SAM_REVIEW/campaigns/GW_COM_INTERVAL1/README.md).
It is a toy forward source, not a fitted physical chirping/precessing binary.
The [carrier runtime](../runtime/carrier.py) now fits three C4 models: amplitude,
amplitude + DC, and linear amplitude drift + DC. Exact least squares uses a
declared quiet calibration prefix; a separate quiet holdout checks the
bounded-noise criterion. The simplest adequate model is selected and all fits
are retained. Full physical binary fitting remains future work.
