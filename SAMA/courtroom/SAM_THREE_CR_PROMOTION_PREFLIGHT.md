# SAM Three-CR Promotion Preflight

generated_utc: 2026-07-11T08:20:00Z
campaign: SAM_COURTROOM_THREE_RECORD_PROMOTION_CAMPAIGN_5_5_XHIGH
preflight_gate: artifacts/preflight_filled/PREFLIGHT_20260711_031606_no_script.md
preflight_classification: CONSTRUCTIVE_NEW_WORK
permission_required: false

## Scope

This preflight is for the bounded three-record promotion campaign only.
It creates new Courtroom records and campaign-level handoff artifacts.
It does not modify existing G tests, existing CR folders, existing appeals,
source documents, SAM Language v0.2 artifacts, or SAM Language source.

## Working Roots

| root | status |
| --- | --- |
| C:/VS/The_Courtroom | exists |
| C:/VS/Stam_model-A-v1.0/tests/Substrate | exists |
| C:/VS/quantum_phase | exists |

## Git Status Snapshot

The working tree had unrelated pre-existing modifications and untracked files
before this campaign. They are preserved and excluded from this campaign.

Tracked modified before campaign:

```text
16_THE_LAST_CAMPAIGN/LC10_QUANTUM_INFORMATION_THRESHOLDS_REPLAY/HASHES.txt
16_THE_LAST_CAMPAIGN/LC10_QUANTUM_INFORMATION_THRESHOLDS_REPLAY/LC10_sources_hashes.csv
16_THE_LAST_CAMPAIGN/LC10_QUANTUM_INFORMATION_THRESHOLDS_REPLAY/LC10_summary.json
TEST_INDEX.csv
```

Relevant untracked before campaign included SAM Language v0.2 work,
diagnostic folders, prior preflight outputs, and the campaign brief itself.
Those existing files are not modified by this campaign.

## Destination Selection

The branch/index scan found maximum existing Courtroom CR number 278 under
09a_PARTICLE_MASS_CHAIN. New non-colliding records are assigned sequentially:

| record | destination | reason |
| --- | --- | --- |
| Higgs direct-weld promotion | 13_CERN_INDEPENDENT_TESTS/CR279_HIGGS_DIRECT_WELD_PROMOTION | Higgs/CERN promotion from G748c and CR120 |
| CR253 semantic clarification | 09a_PARTICLE_MASS_CHAIN/CR280_CR253_STABLE_MATTER_SURFACE_SEMANTIC_CLARIFICATION | Sibling clarification of live 09a CR253 surface |
| Cosmic-budget typed readout | 07_BARYON_INVENTORY_AND_COSMOLOGY/CR281_COSMIC_BUDGET_TYPED_READOUT_PROMOTION | Structural inventory spine lives in branch 07; CR036@19 is a dependency |

No destination folder existed at preflight selection time.

## Source Freeze

Primary source hashes and metadata are recorded in
SAM_THREE_CR_SOURCE_MANIFEST.json. The manifest lists the permitted source set
used for the three records and the campaign-level source freeze.

## Boundary Commitments

- No full repository reanalysis.
- No old result rerun or audit target.
- No source artifact mutation.
- No SAM Language v0.3 generation.
- No forecast generation.
- No bridge invention if a source chain is incomplete.
- Precommit and hash before runner for each record.
- Exact arithmetic and symbolic formulas are preserved where possible.
- Boundaries and failures are preserved.
