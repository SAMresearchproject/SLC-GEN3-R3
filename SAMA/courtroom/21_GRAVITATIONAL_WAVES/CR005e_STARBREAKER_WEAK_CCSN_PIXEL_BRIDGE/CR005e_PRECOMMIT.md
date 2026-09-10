# CR005e Starbreaker / Weak-CCSN Pixel Bridge Precommit

## Classification

`CONSTRUCTIVE_EXTERNAL_WAVEFORM_MORPHOLOGY_BRIDGE`

This campaign is a new constructive bridge. It does not audit or overwrite
CR005d, the frozen Starbreaker trajectory surface, or any existing
gravitational-wave verdict.

## Question

Does the post-bounce, unit-carrier Starbreaker quadrupole source share stable
time-frequency pixel morphology with public three-dimensional core-collapse
supernova matter-strain waveforms when both are placed on one fixed,
amplitude-normalized event-phase grid?

## Why this comparison

The target is weak, single-collapse radiation rather than a compact-binary
chirp. The external files contain time, `hplus*distance`, and
`hcross*distance`. Starbreaker supplies a trace-free quadrupole and its second
phase derivative. These occupy the same quadrupole-source layer, but
Starbreaker still lacks physical carrier mass and seconds. Therefore the run
may compare morphology only.

## Locked source population

- ten Princeton 3D CCSN matter-strain waveforms from the downloaded archive;
- all 96 frozen Starbreaker scenarios;
- all 252 typed carrier occurrences in each scenario;
- thirteen fixed, predeclared observer directions;
- same-door matching only.

The CCSN doors are assigned before waveform inspection by sorting progenitor
mass and cycling `discovery, validation, final`.

## Locked pixel construction

1. Align both sources at post-bounce start.
2. Map each complete record linearly to normalized event phase `[0,1]`.
3. Resample to 2,049 points and trim three derivative-edge samples.
4. Demean each polarization.
5. Use 48 fixed Hann-window time frames of 256 samples.
6. Drop FFT DC and combine the other 128 frequencies into 64 adjacent-pair
   bins.
7. Add plus and cross power and normalize total pixel power to one.

There is no fitted shift, time stretching, dynamic time warping, truncation
search, frequency remapping, amplitude fit, or QNM convolution.

## Locked statistic

The primary pixel statistic is Hellinger affinity:

```text
A(P,Q) = sum sqrt(P_pixel * Q_pixel)
```

For each CCSN waveform, the reported match is the best same-door Starbreaker
scenario and fixed observer view. The full best-match selection is repeated
inside every null so that the template-bank look-elsewhere effect is retained.

## Locked controls

- 47 nonzero circular time-bin shifts;
- time reversal;
- frequency reversal;
- separable time-frequency marginal product;
- amplitude-normalization invariance;
- polarization-basis invariance;
- zero-source rejection;
- exact source hashes, archive membership, door membership, dimensions, and
  atomic release.

## Verdict ladder

- **Strong:** validation and final door median affinities exceed the 95th
  percentile of their time-shift nulls and beat all three chronology/texture
  controls.
- **Directional:** at least two of three doors exceed the 90th percentile of
  their time-shift nulls and beat time- and frequency-reversal controls.
- **Boundary:** the pixel bridge constructs cleanly but does not clear the
  directional morphology gate.
- **Fail:** a construction or stewardship gate fails.

## Claim boundary

This run cannot produce physical strain, luminosity, distance reach,
frequency in hertz, time in seconds, a detector forecast, or proof of a common
mechanism. It compares normalized source morphology only. The archive remains
internal source evidence unless its redistribution terms are separately
cleared.

Same-run repair is prohibited.
