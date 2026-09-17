# GW-COM interval result

The first dimensionless orbit-wave experiment recovered Sean Brady's message
**2, 5, 7, 11, 13, 17** exactly from both repeated packets. The receiver was
given wave samples and the framing protocol, without the message, emission
schedule, time unit, delay or gain.

**The test result suggests the concept is possible.**

| Check | Observed result |
|---|---|
| Two clean packets | Both recovered exactly; inferred unit 16 samples |
| Twenty seeded mild-noise trials with varied delay/gain | Both packets recovered in 20/20 trials |
| Unmodulated orbit | No decoded packets |
| Separate even-integer message | Both `[4,6,8,10,12,14]` packets recovered exactly |
| Native quadrupole arithmetic | 13 distinct source stencils, 470 native graph nodes; every stencil matches independent exact arithmetic |
| Independent saved-wave reconstruction | 2,285 interior stencils match exactly |
| Fresh-process receiver isolation | All three saved wave cases reproduce the recorded decoding |
| Artifact custody | All 9 manifest hashes match; native session status reports 1 returned call, 0 failed or incomplete calls |

Identical radius perturbations, each with peak excursion 1/16 of the baseline
radius, generate the markers. The two unit-weight bodies stay antipodal on the
prescribed sampled C4 orbit. The channel observable is the signed second
difference of the trace-free quadrupole projection Qxx-Qyy, following H000733.
The current STARBREAKER DomainSession executes this calculation through
`GEN2_SIGNED_LOG`; the adapter reuses exact results for identical stencils.

The decoder estimates its carrier baseline, detects marker peaks, uses four
equally spaced opening markers to recover the reference interval, and reads
six data gaps. It has no primality test or expected-message comparison.
The evaluator compares the independently decoded output with the input afterward.

The noise trials use Gaussian sigma 0.04 before gain, 0.5% of the absolute
baseline wave value 8. Gains are 0.25, 1 and 4; delays range from 7 to 64 samples.
This is a bounded mild-noise check, not a measured false-alarm probability.
The even-integer control establishes that the receiver is recovering timing
values rather than returning a fixed prime sequence.

The physical work still to model is the force and energy needed to produce the
prescribed orbit changes, continuous dynamics, propagation and detector response.
The current signal is dimensionless and sampled; no SI strain or communication
range is assigned. The higher-prime strength layer is reserved for a successor.

## Evidence

- [Machine result and trial records](release/RESULT.json)
- [Exact source and waveform samples](release/source_wave.csv)
- [Wave-only receiver input](release/prime_receiver_input.json)
- [Transmitter schedule](release/transmitter.json)
- [Independent verification](verification/VALIDATION.json)
- [Native calculation receipt](sessions/STARBREAKER_dfc32b1af0ab4b7eb5b18c2aee83ba9c/calls/41423cdca70944f8b60d63d98f1a71c6/RECEIPT.json)
- [Protocol, source mapping and execution instructions](README.md)

Sean Brady supplied the orbit-manipulation communication concept, prime interval
sequence and proposed higher-prime strength layer. Codex supplied this initial
framing, radial marker profile, source adapter, receiver and checks.
