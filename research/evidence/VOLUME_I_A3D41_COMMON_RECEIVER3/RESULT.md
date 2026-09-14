# Common reception identifies every declared native history

**The test result suggests strong contact with the concept.**

The completed common receiver reconstructs the exact Write order, phase path,
contact profile and native barrier for **98,304 of 98,304 histories**. The
independent implementation agrees on every observation and inverse. There are
zero ambiguous orders under the declared comparison conditions: initial native
phase, Write direction and J4 rho are fixed while all six orders are compared.

This completes the owner's requested construction. Both source maps remain
distinct channels, arise from the same source event, pass through a common
reception mechanism, and supply an executable inverse.

## One native event supplies both channels

The installed A3D41 readouts already give signed phase h and axis occupancy
|h|. The new common lift is their typed pair, formed at the same native event.
Both components pass through the same J4 response T:

    common source:       (h, |h|)
    common response:     diag(T, T)
    received frame:      (SIGNED_PHASE, AXIS_OCCUPANCY).

The source's phase evolves once. Under a unit Write, the signed component
rotates by its native quarter-turn while occupancy swaps its two axes. These
are the four-phase cycle and its two-phase quotient at one event. The common
action is detailed in the [extension map](PHYSICAL_EXTENSION_MAP.md).

Every received frame admits both lanes atomically. The receiver's local cache
holds only the current frame; the ordered observation record is retained
separately. The cache illustrates the current-state/history separation; it
does not assign the numerical frame to W8's physical coordinates. W8 retains
its updated current state without history. Native phase addresses, carrier
samples and eventual physical site coordinates have distinct meanings.

Projection onto either lane reproduces its original H000970 source map at all
8,192 state/rho combinations. The occupancy projection is applied at the
source, before combination. It is not the absolute value of the signed
received signal. No mixing weights or fitted parameters were introduced.

The common lift and direct-sum reception are Codex's discrete construction
from the owner's direction and the native source readouts. It executes in an
isolated campaign using the current native source engine. The moving-body
emission law and physical propagation/readout are the named next maps.

## An inverse that reads each change

The primary decoder begins with the declared initial phase and direction.
For each received increment, it considers every remaining legal next Write,
keeps all matches and advances the reconstructed phase. Its input contains
the observed channels and calibrated templates; source IDs, actual orders,
addresses, barriers and hashes are excluded. The native contact profile is
then calculated from the reconstructed phases.

The independent decoder uses a different route: Gaussian integer phase
arithmetic, all six law-generated words, and exact signal matching. Its
contact calculation uses the full incidence Gram. It imports none of the
primary or predecessor mathematical functions.

| Receiver information | Exact orders recovered | Native barriers recovered | Ambiguous orders |
|---|---:|---:|---:|
| Both channels, ordered observations | **98,304** | **98,304** | **0** |
| Signed channel alone | 73,728 | 77,824 | 24,576 |
| Occupancy channel alone | 49,152 | 65,536 | 49,152 |
| Both channels, endpoints alone | 0 | 6,144 | 98,304 |
| Signed plus its absolute value after reception | 73,728 | 77,824 | 24,576 |

All counts cover the same 16,384 fixed-condition families. The endpoint-only
barrier successes occur in families where all six orders already have the
same barrier. The original signed-only H000970 result retains its recorded
classification: **The test result suggests the concept is possible.**

## Why the inverse works

The exact template identity X_084=-X_006 is preserved. Let A=X_002 and B=X_006.
A nonzero complex minor certifies their independence at each of the 128
declared rho values. A Write on relation 0 is consequently distinguishable
from either of the other two.

For relations 1 and 2, equality of signed increments requires opposite phases,
which have the same phase parity. Equality of occupancy increments would
require opposite parities. These conditions cannot hold together. Thus every
possible next Write has a distinct two-channel increment. All 16,384
state/direction/rho cases satisfy that exact local certificate.

This gives an algebraic explanation as well as the completed census. With
known initial phase and Write directions, distinguishable consecutive single
Writes reconstruct inductively wherever those template conditions hold. The
executed roster remains the declared three-Write comparison. The
[derivation](DERIVATION.md) specifies the statement and its assumptions.

The motivating example now reconstructs directly. At initial phase (0,2,0),
positive Writes and rho=1, orders 012 and 021 have the same entire signed
history but different occupancy histories:

| Order | Recovered contact profile | Recovered barrier | Occupancy at prefix 2, first forward sample |
|---|---|---:|---|
| 012 | 2,4,6,2 | 4 | (8,376, -32,984) |
| 021 | 2,4,4,2 | 2 | (15,960, -49,144) |

The signed sample is (4,088, -44,856) for both. The complete extracted records
are in [the motivating-pair readback](MOTIVATING_PAIR_READBACK.json).

## Execution and evidence custody

The design was sealed before science, with the earlier joint partition result
explicitly declared as prior knowledge. The executor was separately sealed
after eight synthetic fixture groups passed. The design contains 18 hashed
files; the executor contains eight. Both full implementations verified them.

Attempt `run001` stopped before any native word or receiver census because
the managed current CE reported `current CE runtime differs`. Its failure and
manifest are preserved without scientific classification. The installed CE
binding subsequently resolved under its H000971 authority. The recorded
[launch recovery](LAUNCH_RECOVERY_001.json) verifies matching expected/actual
runtime hashes. This campaign changed neither engine code nor bindings.
The same sealed executor then completed `run002`.

Primary execution ran from `2026-09-06T20:02:15.180996+00:00` to
`2026-09-06T20:02:40.852881+00:00`. Independent reconstruction ran from
`2026-09-06T20:03:06.701237+00:00` to
`2026-09-06T20:03:31.764052+00:00`. Both exited zero.

The managed `CURRENT_REVISION.open_domain("ATOM3D")` entry executed 768 native
words, comprising 2,304 Writes. Every trajectory reproduced the inherited
installed A3D41 source trajectory. Native contact ground truth comes from the
completed hardware source. The new receiver arithmetic ran locally and emitted
393,216 common reception frames containing 12,582,912 exact scalar values.
Every scalar, inverse, control candidate, source receipt, per-rho metric and
injectivity certificate matched the independent calculation.

The synthetic checks cover source/readout sign-erasure distinction, atomic
admission, unchanged state after rejection, current-state-only storage,
immutable frames, exact recovery, all ties for a blind receiver, inconsistent
signals and metadata exclusion. Full reversed native words reconstruct in all
98,304 cases. The declared cyclic occupancy-misalignment control is rejected
in all 98,304 cases. Its initial frame already violates the known initial
condition; it demonstrates that particular inconsistency detection, not a
general ability to identify arbitrary channel timing errors.

Evidence:

- [Precommitment](PRECOMMIT.md), [contract](EXPERIMENT_CONTRACT.json),
  [source register](SOURCE_REGISTER.json), [design seal](DESIGN_SEAL.json).
- [Executor specification](executors/v1/EXECUTION_SPEC.md),
  [code seal](executors/v1/CODE_SEAL.json),
  [fixture results](executors/v1/FIXTURE_CHECKS_001.json).
- [Primary summary](runs/run002/SUMMARY.json),
  [all observations and inverses](runs/run002/RECEPTION_INVERSE.jsonl.gz),
  [per-rho results](runs/run002/PER_RHO.json),
  [injectivity certificates](runs/run002/INJECTIVITY_CERTIFICATE.json).
- [Current native binding](runs/run002/NATIVE_BINDING.json),
  [native word receipts](runs/run002/NATIVE_WORD_RECEIPTS.jsonl.gz),
  [independent verification](runs/run002/independent/VERIFICATION.json).
- [Preserved launch failure](runs/run001/FAILURE.json) and
  [completion record](COMPLETION.json).

## Owner disclosure and the next construction

The useful additional finding is local injectivity: the receiver identifies
each next Write from its two-channel change. It supplies a constructive reason
for recovery and a route to longer ordered histories under the same source
conditions.

The source study's next steps are now mapped in
[PHYSICAL_EXTENSION_MAP.md](PHYSICAL_EXTENSION_MAP.md): moving-body source,
fixed-site encounter geometry, then physical propagation/readout. The first
proposed campaign carries SO1's separately retained orbital and spin sources
into this common packet law. The site map then locates actual encounters as
information moves across stationary support. The physical map supplies the
particular measured response and its source-derived units.

NEGATIVE DRIFT CHECK — COMPLETION: CLEAR.
