# Standalone R4 distribution scope

This export preserves the installed SLC-GEN2-R4 computational source and its
required Q3/Q2/Q1 and sealed V6/ICF1 foundation components. Their historical
directory names are retained because the authenticated imports use those paths.

The new portable files are CURRENT_REVISION/__init__.py,
CURRENT_REVISION/runtime.py and slc_gen2_r4/*.py. They resolve the local release,
verify the export inventory and provide a CLI/receipt wrapper. They do not
rewrite the upstream mathematical implementations. The portable release has
its own generation string, `SLC-GEN2-R4-RESEARCH-20260907-1`; the upstream
generation is retained separately in the source manifest.

## Included computational routes

Native source compilation, forward programs and inverse DAGs; reconstructive
custody; exact HD/formal-log operations; typed signed arithmetic; history
summaries, append and composition; inverse sessions and observation planning;
adaptive policy planning/apply/resume; construction, site/cycle and readout
operations; linked boundary information; encounter operations; automatic sphere
and golden motion; retained T18_WORD; and reuse telemetry.

The preserved interface catalogue is
CURRENT_REVISION/engines/SLC/INTERFACE.json. Use docs/USAGE.md for the portable
entry point. The complete upstream qualification fixture covers 35 integration
cases; tests/test_release.py compares its exact outputs in this export.

## Separate deployments

| Operation group | Distribution boundary |
|---|---|
| GEN2_TAU_ASSIGNMENT, GEN2_TAU_REPLAY, GEN2_TAU_FEATURE_CATALOG | Require the separately installed PILOT3 application and model binding. Source is preserved; the portable wrapper reports the missing application explicitly. |
| GEN2_SOURCE_BATCH | Uses the original multi-host CPU/GPU/T500 infrastructure and remote paths. Source is preserved; the portable wrapper does not launch that deployment. |
| GEN2_DENSE_N72 | Exact source attachment and declared dependencies are included. It retains its original Linux affinity list, C compiler, NumPy and output-custody requirements. The core release tests do not rerun this hardware workload. |
| CE domain programs | RH, MP, ATOM3D and Starbreaker project deployments are separate from this engine repository. No active research services or trained application checkpoints are exported. |

The default examples and release tests run locally and require no SAM account,
remote host, API key, GPU, T500 disk or research workspace. NumPy is required
by the preserved foundation. Optional hardware sources are not portable promises
about an arbitrary machine's CPU layout or OpenCL devices.

## Evidence and source custody

SOURCE_MANIFEST.json binds every copied file. The large upstream installation
fixture is gzip-compressed; its manifest records both the compressed digest and
the digest of the original bytes. Decompression is lossless. The V6 source ZIP
is unchanged and its original importer verifies every member before use.

docs/upstream contains original source specifications and installation narrative.
Their historical statuses, hardware evidence and source-relative links belong
to the originating workspace. docs/USAGE.md and this document describe this
standalone distribution. Upstream test counts are not represented as new
independent runs; provenance/EXPORT_VALIDATION.json records the export checks.

Sealed source components must not be silently edited. A research modification
should identify its new source version, update applicable binding contracts and
retain the predecessor and its evidence. The research licence permits such
private work; it does not make changed bytes an authenticated original release.
