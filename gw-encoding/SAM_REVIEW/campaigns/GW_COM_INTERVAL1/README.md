# GW-COM: first interval experiment

Sean Brady's proposal is to manipulate two orbiting objects to transmit the
interval sequence **2, 5, 7, 11, 13, 17**. A later layer may encode larger
primes in wave strength. This campaign implements the interval layer only.

## Source-to-operation mapping

This isolated successor uses H000733's dimensionless antipodal C4 orbit and
trace-free quadrupole, Q = sum(x x^T - r^2 I/3). Its wave observable is the
signed second difference of Qxx-Qyy. Positions advance by quarter turns on
each discrete tick. Both unit-weight bodies have opposite positions.

At each marker, the prescribed radius changes by the same nine-sample profile
`[0,1,3,6,8,6,3,1,0]/128`, a maximum 6.25% excursion. The frame begins with
four markers one reference unit apart. Six subsequent gaps carry the message;
one unit is 16 source ticks. Two complete packets are sent, separated by a
23-unit guard interval. The decoder knows the frame format, not the message,
source timestamps, reference unit, delay or channel gain.

`run.py` is the campaign-local source adapter. Python constructs the prescribed
positions and compiles their unique three-position stencils. A current
STARBREAKER DomainSession executes all quadrupole and wave arithmetic through
`GEN2_SIGNED_LOG`; exact repeated stencils are reused when assembling the trace.
The source is not a hand-inserted waveform pulse. Independent Python Fraction
arithmetic checks the wave contraction against each native result.

`receiver.py` reads only wave samples. It finds peaks in deviations of absolute
wave amplitude from the median carrier amplitude, identifies the synchronization
markers, estimates the time unit, and rounds the six subsequent interval ratios.
It never tests whether decoded integers are prime. Marker shape/separation,
threshold and packet format are protocol assumptions. Quiet baseline occupies
most samples. Timing resolution is one sample, and the orbit is a discrete model.

The first channel is an ideal delayed, scaled scalar readout. Twenty seeded
trials add Gaussian noise with sigma 0.04 before gain (0.5% of the baseline
absolute wave value of 8). Controls are the unmodulated orbit and a separately
generated even-integer message `[4,6,8,10,12,14]`.

This models prescribed motion, not an integrated force-controlled binary.
Actuator force/energy, continuous orbital dynamics, SI strain, detector response,
physical propagation and the strength-message layer remain future work.

## Run

From the repository root:

```bash
.venv-r3/bin/python CURRENT_REVISION/engines/SLC/gen3/resources.py run -- \
  .venv-r3/bin/python SAM_REVIEW/campaigns/GW_COM_INTERVAL1/run.py
```

The runner creates a new `release/` and refuses to overwrite an existing result.
Receipts are compressed under `sessions/`. The receiver inputs are separate from
the transmitter schedule. The source CSV contains exact rational samples.

Originator / conceptual director: Sean Brady. AI research collaborators:
OpenAI ChatGPT and Codex. Framing, radial profile and receiver implementation
are Codex's proposed first technical realization of the owner's concept.
