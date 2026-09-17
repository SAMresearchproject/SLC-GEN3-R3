---
entry_id: H001492
entry_date: 2026-09-17
entry_type: ARCHITECTURE / AUTHORITY_CHANGE
status: IMMUTABLE_HISTORY
supersedes: NONE
prior_entry: H001491
affects_live:
  - SAM_LIVE/03_STARBREAKER_GW_CURRENT.md
---

# GW-COM five-layer architecture and retained evidence

Sean Brady directs the `gw-com` branch to use five layers:

1. GW carrier model: binary/orbital source, expected phase evolution,
   amplitude, polarization, chirp and precession.
2. Intentional modulation: phase, frequency, amplitude, timing, polarization
   and pulse trains.
3. Residual extraction: subtract the best physical source model and retain
   the unexplained signed, time-ordered residual.
4. Information tests: periodicity, entropy, compression, symbol alphabets,
   repetition, synchronization and error-correcting structure.
5. Decoder: only after a candidate survives physical and statistical controls.

The owner requires the retained chain **raw waveform → source fit → residual
history → candidate symbolization → decoded hypothesis** rather than reduction
to one anomaly score. This architecture is owner-originated; Codex implements
its repository organization and contracts.

Prior live state linked only H001491's completed interval experiment. The new
current entry point is [GW_COM/README.md](../../GW_COM/README.md), with five
numbered layer directories, scoped working instructions, a hash-linked
[program inventory](../../GW_COM/PROGRAM.json), and the
[evidence contract](../../GW_COM/EVIDENCE_CONTRACT.md). Each stage preserves
parents, samples or sample support, methods, alternatives and execution refs.
Physical and statistical dispositions are separately retained; absent,
incomplete, failed or mismatched controls do not admit candidate decoding.
Specific test criteria belong to future experiment contracts, with no new
universal threshold imposed by this organization.

H001491 and all original interval-demo artifacts remain unchanged. The
inventory explicitly distinguishes its known-protocol decoder output from
an admitted hypothesis in the new candidate pipeline. Its signed waveform
is retained; it did not implement best-source fitting or signed fitted
residual extraction. Missing stages are recorded as absent, not fabricated.

This change defines architecture and interfaces. It does not install a full
physical carrier, information-test engine or candidate runtime gate, and it
makes no new measurement or scientific classification. The first successor
will implement carrier fitting and signed residual history before candidate
information tests and admission. Current native computation rules, source
authority, prior classifications and unrelated domain states are preserved.

Verification for this organizational change checks local documentation links,
the five-layer program inventory, referenced artifact hashes, unchanged demo
manifest contents and the repository live/history contract.
