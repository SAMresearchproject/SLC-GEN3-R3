# SLC-GEN3-R3 distribution scope

This repository preserves the September 10 R3 computational runtime, native GEN2
components, exact logarithmic accounts, acquired relation/observation seeds,
and local durable checkpoint storage. Its required Q3/Q2/Q1 and sealed V6/ICF1
foundation components remain included with their source identities.

The exported portable release is SLC-GEN3-R3, build
`GEN3-UNIFIED-EXECUTION1-20260910`, generation
`GEN3-UNIFIED-EXECUTION1-20260910-G2`. The portable entry point has release binding
`SLC-GEN3-R3-RESEARCH-20260910-1`. `CURRENT_REVISION/runtime.py` verifies the export
manifest and loads `gen3_runtime.py`; `slc_gen3_r3` supplies the portable CLI and
receipt wrapper. `slc_gen2_r4` forwards to that same R3 runtime.

The mathematical implementations are copied from their sources. Portable binding,
CLI and scope checks are identified distribution code. The included source set
has its own implementation digest; local checkpoints belong to that source set.

## Included routes

Native execution and acquired source support; complete forward/inverse histories;
exact signed arithmetic and logarithmic U/D/V/net/M accounts; account append and
composition; actual observation encounters; acquired seeds; local authenticated
checkpoints; inherited motion, construction, readout, boundary and encounter calls.

## Separate deployments

| Operation or entry point | Required deployment |
|---|---|
| GEN3_REPLICATE | Configured remote replication service; portable wrapper reports this explicitly. |
| GEN2_SOURCE_BATCH | Original multi-host CPU/GPU/T500 application. |
| GEN2_TAU_ASSIGNMENT, GEN2_TAU_REPLAY, GEN2_TAU_FEATURE_CATALOG | Separately installed tau application and model. |
| GEN2_DENSE_N72 | Preserved Linux affinity/compiler/NumPy hardware attachment. The quick start does not launch it. |
| CE domains and managed project launchers | Separate RH, MP, ATOM3D, Starbreaker and project installations. |

The upstream host-specific GEN3 launcher, resource profile and replication
scripts are excluded from this portable export. The portable CLI executes
locally. Linux is required by the durable store's file locking and fsync calls.
NumPy is required by the inherited foundation. Optional python-flint accelerates
exact ratios when installed; the standard Fraction backend retains exact values.

## Provenance and project information

[SOURCE_MANIFEST.json](../provenance/SOURCE_MANIFEST.json) authenticates included
source files. [Export validation](../provenance/EXPORT_VALIDATION.json) records
checks run on this distribution. The former R4 source manifest remains in
[GEN2_R4_SOURCE_MANIFEST.json](../provenance/GEN2_R4_SOURCE_MANIFEST.json).
Files under `docs/upstream/` retain historical source specifications and statuses;
they describe their originating installation. This page and the root README
describe the public distribution.

[SAMA](../SAMA/README.md) is the project's supporting research collection. Its
four-volume reading structure, source identities, tests and original licences
remain preserved. [Project status](PROJECT_STATUS.md) records current information.

## Installed R4 source supplement — 16 September 2026

The current upstream installation is SLC-GEN3-R4, generation
GEN3-SOURCEOPERATORS1-20260916-G1. Its [capability supplement](../research/gen3-r4/README.md)
contains exact source copies, contracts and retained qualification records.
It requires the upstream unified store and CE/DomainSession adapters; the
portable R3 CLI above does not gain those operations from this publication.
The [isotope source adapters](../research/atom3d/source) have the same upstream
application dependencies. The roster CSV/HTML and template dataset are available
for direct inspection without running those adapters.
