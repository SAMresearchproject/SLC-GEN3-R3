# 2. Intentional modulation model

Own the proposed source control: phase, frequency, amplitude, timing,
polarization and pulse trains. A model specifies what is changed in the source,
how the change produces a waveform, and which receiver observable can retain it.

Input: carrier model identity and a versioned modulation contract containing
control variables, time law, units, permitted magnitudes, marker profile,
framing and the intended forward mapping. Preserve relationships between phase
and frequency rather than treating linked parameters as independent controls.

Output: source control history and resulting wave prediction, including
baseline/modulated comparisons. Retain force/energy and dynamical assumptions,
including when motion is prescribed rather than produced by integrated dynamics.

Interval-first design: equal source-control profiles separated by
`2,3,5,7,11,13,17` reference units. Larger primes in a strength layer remain a
separate future modulation hypothesis. Equal source-control amplitude does not
by itself establish equal observed amplitude under an evolving carrier.

Synthetic transmitter truth is retained for evaluation in a separate artifact.
Candidate searches receive only their declared model family and observation
data; they do not receive hidden message labels. Known framing assumptions must
be stated, while searched framing alternatives count as part of the search.

The [modulation runtime](../runtime/modulation.py) implements equal radial
excursions and known framing through a native quadrupole source, with explicit
gain, offset, bounded noise and amplitude-drift readout inputs.
Continuous actuation, other modulation families and coupled-layer transmission
are not implemented yet.
