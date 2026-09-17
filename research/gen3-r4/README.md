# Installed GEN3-R4 research sources

Snapshot: 16 September 2026. Global runtime **SLC-GEN3-R4**, CE **SLC-GEN3-CEV1-R4**,
generation **GEN3-SOURCEOPERATORS1-20260916-G1** (H001469).

This directory publishes the installed capability source and contracts, with
recorded qualification and research data. It is a source/evidence export; the
root `python -m slc_gen3_r3` quick start still runs the preserved portable R3
release. The R4 adapters require the upstream unified store, DomainSession and
CE installation; copying them over the portable runtime is not an installation.

- [Certified logarithmic contracts](contracts/CERTIFIED_LOG.md): exact signed
  source moments, scalar and spectral logarithms, certified error intervals,
  refinement and retained export. Scalar log(1+Q) and source-weighted spectral
  log are distinct operations.
- [Source-operator contracts](contracts/SOURCE_OPERATORS.md): exact words,
  subspaces, native pair-root relations, block recurrence, spectral creation,
  exchange checks, terminal action and authenticated export.
- [C++ native source](capabilities/native) and [Python admission adapters](capabilities).
- [Certified-log qualification](../evidence/GEN3_R4_CERTIFIED_LOG1/RESULT.md):
  5,791 integrated checks and 4,032 independent native assertions; installed
  adoption has 57 checks, with their scopes recorded separately.
- [Source-operator installation](../evidence/GEN3_R4_SOURCE_OPERATORS1/RESULT.md):
  50 candidate checks and 157 installed-adoption checks, with all five CE domains.
- [ATOM3D research](../atom3d/README.md): Li-6 dressed-source exchange, isotope
  construction and learned source-template generation.
- [Numbered source history](history) and [exact export hashes](../../provenance/RESEARCH_UPDATE_20260916.json).

Copied result documents preserve their source-era paths and statements. Paths
into the original project denote upstream dependencies; this guide and the
manifest identify the artifacts available in this public checkout. Qualification
counts here report retained upstream runs, not new executions by this export.
Original runtime/model identities, source histories and research classifications
are preserved. No checkpoint authentication keys or host credentials are included.
