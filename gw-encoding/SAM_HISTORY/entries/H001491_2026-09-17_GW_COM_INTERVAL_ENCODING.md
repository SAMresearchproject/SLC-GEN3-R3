---
entry_id: H001491
entry_date: 2026-09-17
entry_type: RESULT / APPLICATION
status: IMMUTABLE_HISTORY
supersedes: NONE
prior_entry: H001490
affects_live:
  - SAM_LIVE/03_STARBREAKER_GW_CURRENT.md
---

# GW-COM first interval encoding

Sean Brady opened `gw-com` to manipulate two orbiting objects so their wave
encodes `2,5,7,11,13,17`, starting with intervals and reserving larger primes
in wave strength as a later layer. This is a new communication application of
the established dimensionless orbit-wave source; it does not replace H000733
or the completed Starbreaker receiver results.

The isolated [GW_COM_INTERVAL1 result](../../SAM_REVIEW/campaigns/GW_COM_INTERVAL1/RESULT.md)
uses the antipodal C4 source, equal prescribed radial marker profiles and its
trace-free quadrupole second-difference projection. Current STARBREAKER /
SLC-GEN3-R4 native arithmetic evaluates 13 unique stencils in 470 nodes through
a recorded `GEN2_SIGNED_LOG` call; exact stencil reuse assembles the wave.

The receiver gets wave samples and a frame format only. It reconstructs both
prime packets exactly, plus both packets in all20 mild Gaussian-noise trials
with varied delay/gain. An unmodulated orbit returns no packets. A separate
even-integer message is correctly decoded. All13 native stencils and2,285
saved-wave interior stencils match independent exact arithmetic; three
fresh-process receiver checks and nine custody hashes pass.

**The test result suggests the concept is possible.**

Prior live state carried orbit-wave and receiver groundwork without this
communication application. New live statement: GW-COM has completed its first
dimensionless interval-only communication experiment with exact recovery of
the specified sequence and the stated controls.

Preserved boundaries: prescribed sampled motion, ideal delayed/scaled scalar
channel, known frame format and marker assumptions. Continuous controlled
dynamics, actuation energy, SI strain, physical propagation, detector response,
false-alarm probability and higher-prime strength encoding are not assigned.
There is no global engine replacement or change to unrelated domain pauses.

Source mapping, artifacts, session receipt, run instructions and authorship
are recorded in the campaign result and README. Sean Brady is originator and
conceptual director; OpenAI ChatGPT and Codex are AI research collaborators.
