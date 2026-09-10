# Current SLC stack and SAM dependencies

Recorded: 2026-07-23

## Product boundary

SAM Language, the SAM UI, and the SLC are separate components:

```text
SAM UI
    presentation and interaction
        |
        v
SAM Language
    parser, types, operators, programs, authority, and provenance
        |
        v
SLC
    separate execution/scaling system that uses SAM Language
```

The SLC does not inherit the SAM Language or SAM UI version number. Each
component must be versioned independently.

## SAM Language

The highest-version validated SAM Language candidate found in the repository is
`0.7.0-candidate`. It is an additive SAM Language successor that exposes the
formal SLC C1 reflective interface:

```text
SAM Language candidate:
    SAM_LANGUAGE_V0_7_0_SLC_C1_REFLECTIVE_TAPE_INTERPRETER_CANDIDATE
SAM Language version:
    0.7.0-candidate
Formal interface profile:
    SLC_C1_REFLECTIVE_FORMAL
Formal register contract:
    12 sites, 4,096 basis addresses
Validation:
    SLCX006 PASS, 12/12 gates
Release status:
    validated candidate; no final non-candidate release is declared
```

This is a SAM Language version. It is not an SLC system version.

## SAM UI

The current authoritative SAM UI manifest declares:

```text
SAM UI:
    Phase 2 Candidate 004
SAM UI API:
    v1
SAM Language runtime used by that UI:
    0.4.2
```

The SAM UI is not the SLC. Its UI manifest is authoritative over the currently
stale `Candidate 003` title in `SAM_UI_PHASE_2/README.md`.

## SLC

Explicit SLC component versioning begins with the dense exact solver:

```text
SLC component:
    Dense Exact Solver
Current version:
    v0.2.0
Version label:
    SLC_DENSE_EXACT_V0_2
Algorithm:
    fused paired-branch exact NTT/CRT variable elimination
Order policy:
    frozen finite graph-only portfolio
Root batch policy:
    largest power of two satisfying retained 2^26 and logical-union 2^27 entry ceilings
Checkpoint policy:
    immutable self-sealed record after every root batch
Validation:
    SLCV002 N24 -> N48 -> N60 calibration -> frozen rule -> N60 holdout
    4/4 stages PASS; 6/6 exact instances; 62/62 checkpoints
N72 validation:
    2/2 frozen instances PASS under the same v0.2 capacity-26 rule
    I00: width 22; 192/192 checkpoints; 48/48 wave chains
         exact 2^72 count; full 871-coefficient historical-primary equality
    I01: prospectively generated with no width-22, DOS, or runtime filter
         width 24; 768/768 checkpoints; 192/192 wave chains
         exact 2^72 count; all internal exact and raw-moment gates PASS
         no independent implementation comparison was run for I01
```

This v0.2 label belongs to the SLC dense solver. It does not belong to SAM
Language, the SAM UI, or the SLCX038 supervisor.

The validated local execution profiles now include:

```text
Execution profile:
    four-SLC root-domain software cluster
Cluster validation:
    N24 -> N48 -> N60 calibration -> frozen rule -> N60 holdout
Exact result:
    4/4 stages; 6/6 instances; 72/72 node checkpoints; 18/18 wave chains
Meaningful N48/N60 speed ratio:
    2.39x combined versus the sealed one-SLC v0.2 controls
Maximum sampled aggregate worker RSS:
    8.465 GiB
N72:
    I00 separate SLCV002C4N72 successor PASS
        width 22; 16 roots/node task; retained batch 16 x 2^22 = 2^26
        192/192 node checkpoints; 48/48 four-node wave chains
        1,398.647 s = 23 min 18.647 s
        8.171 GiB peak sampled aggregate worker RSS
        all 871 coefficients equal the post-candidate historical primary
    I01 separate fresh no-refit holdout PASS
        first structurally accepted graph; no width-22/DOS/runtime screening
        width 24; 4 roots/node task; retained batch 4 x 2^24 = 2^26
        768/768 node checkpoints; 192/192 four-node wave chains
        2,825.225 s = 47 min 05.225 s
        7.276 GiB peak sampled aggregate worker RSS
        all internal exact and independent raw-moment gates PASS
        no independent reference implementation completed
    N72 total: 2/2 instances; 960/960 checkpoints; 240/240 chains
Historical fused-primary wall ratio:
    6.107x descriptive combined profile ratio
    not a pure four-node scaling ratio because v0.2 batching also changed
```

This is an execution profile of v0.2, not a new solver version. Its
hash-linked four-node receipt chain concerns clustered root evaluation; it is
distinct from the repeated-physical-cell transfer construction in
SLCX032/SLCX035.

The separate remote stack reported in the attached 2026-07-23 snapshot was:

```text
SLC campaign/safety supervisor:
    SLCX038
Problem/lane:
    N72 / REFERENCE_MATERIALIZED_WIDTH23
Borrowed worker:
    SLCX031 slcx031_worker.py
Exact engine lineage:
    SLCX023A sealed full-materialization NTT variable elimination
Frozen instance:
    SLCX025_N72_I00
SLC dense solver version:
    SLC_DENSE_EXACT_V0_1
SAM Language version executed by this numerical stack:
    not declared by the SLCX038 contract
Subsequent status:
    interrupted by a Windows update/restart; no completion result reported
```

In plain language, **SLCX038 was a remote N72 reference campaign**, and
**SLC Dense Exact v0.1 was the solver version used by that run**. Its
interruption does not retroactively change the solver version it used, and the
local v0.2 promotion does not claim that SLCX038 ran v0.2. SLCX038 used the
SLCX031 worker and SLCX023A exact engine lineage. Architecturally, the SLC uses
SAM Language, but this numerical campaign does not claim that it executed the
SAM Language v0.7 reflective interface.

SLCX031 separately records a completed N72 fused primary lane and an incomplete
reference lane. That boundary result is historical N72 evidence, not v0.2
validation by itself. SLCV002C4N72 subsequently opened the required separate
v0.2 successor, sealed its candidate before parsing the historical primary,
and passed full fixed-domain coefficient equality. The later
SLCV002C4N72I01 campaign then generated a fresh graph prospectively, accepted
its frozen width-24 outcome without filtering for width 22, and passed the
unchanged v0.2 plan with no refit. Together these validate the local v0.2
four-SLC profile on two frozen N72 instances. I00 has historical full-vector
equality; I01 has prospective no-refit internal exact closure, including
independently recomputed raw moments, but no second implementation comparison.
Neither result completes the timed-out independent SLCX031 reference lane.

The I01 source manifest pinned the preceding structured version record
(`CURRENT_SLC_VERSION_V5`, SHA-256
`97c0b7ff4b8697ad43255204bb5412baa2b1a2859861da0a60db83a717826e4b`)
before execution. Git commit `a9050754` preserves that exact pre-execution
context, and commit `1eeebb9b` preserves the verified result tree before this
documentation advanced to `CURRENT_SLC_VERSION_V6`. This is a documentation
update after the sealed result, not a solver refit or a new SLC version.

`SLCX###` identifiers are campaign/revision identifiers, not SAM Language or
SAM UI semantic versions, and they are no longer used as the dense solver
version.

## Authoritative sources

- SAM Language v0.7 interface contract:
  `SAM_LANGUAGE/SAM_LANGUAGE_V0_7_0_SLC_C1_REFLECTIVE_TAPE_INTERPRETER_CANDIDATE/V0_7_REFLECTIVE_CONTRACT.json`
  - SHA-256: `4e45955616daea253c85a656c010d10ab59bf08e9c2f878bc4565aa39b7e7171`
- SAM Language v0.7 validation:
  `18_SAM_NATIVE_QC/SLCX006_MINIMAL_REFLECTIVE_SAM_TAPE_INTERPRETER_COMMUTATION_DISCOVERY/release/SLCX006_RESULT.md`
  - SHA-256: `1ff12d4dcded5982edd2e45436e9d2ab09000d3698d3de4748a65cb5be182210`
- SAM UI:
  `SAM_UI_PHASE_2/PHASE_2_UI_MANIFEST.json`
  - SHA-256: `cc1cec12d38fc36dd6f64b80a5650810bfc9262f1a587a620635c7990a07afdd`
- SLC stack:
  `18_SAM_NATIVE_QC/SLCX038_PROCESS_TREE_BOUND_DENSE_N72_WIDTH23_24H/SLCX038_CONTRACT.json`
  - SHA-256: `e5516daa9c8793ee28f715fd98bd53a0539ec29dbc0334598b1d8a3e9fff81f2`
- SLC Dense Exact v0.1:
  `18_SAM_NATIVE_QC/SLCV001R1_NUMPY_ENVIRONMENT_CORRECTED_N24_REPLAY/SLC_DENSE_EXACT_V0_1.json`
  - SHA-256: `12e9763051820172a02c39e639d3a9610348dc9c5432d6022fe10ccc1eaf31d6`
- SLC Dense Exact v0.1 N24 validation:
  `18_SAM_NATIVE_QC/SLCV001R1_NUMPY_ENVIRONMENT_CORRECTED_N24_REPLAY/release/SLCV001R1_RESULT.json`
  - SHA-256: `7e7ceeea3a85fbc4649bf165ea5e1eafa41df5e4cbc7d96441c3e2432507f7b7`
- SLC Dense Exact v0.2 immutable candidate contract:
  `18_SAM_NATIVE_QC/SLCV002_CAPACITY26_RESTARTABLE_SCALING_LADDER/SLC_DENSE_EXACT_V0_2_CANDIDATE.json`
  - SHA-256: `4ea05bec4caa791d1e9cd36d100e86f2bd4141812c3f1b33b908d7b020de4d1c`
- SLC Dense Exact v0.2 validation:
  `18_SAM_NATIVE_QC/SLCV002_CAPACITY26_RESTARTABLE_SCALING_LADDER/release/SLCV002_RESULT.json`
  - File SHA-256: `a3578910fc3f3771d4c655e62d622bb829a6ecce3caa4b08f1e5d7ac75712816`
  - Result self-seal: `5f0f46f8f32d21c597440c99fdf4ff231eb717c7960232762e5335d36d271c8c`
- SLC Dense Exact v0.2 promotion:
  `18_SAM_NATIVE_QC/SLCV002_CAPACITY26_RESTARTABLE_SCALING_LADDER/release/SLCV002_PROMOTION.json`
  - File SHA-256: `572e6f1cdce672b5fe64dbe753bcf65c95d176797b2c7c3ece5a39afb0e242de`
  - Promotion self-seal: `5fc8db2cf89dca8847ddc420784d608cd977f161245bc551b626b3fc18d0b6b4`
- SLC Dense Exact v0.2 four-SLC execution profile:
  `18_SAM_NATIVE_QC/SLCV002C4_FOUR_SLC_CLUSTER_SCALING_LADDER/release/SLCV002C4_RESULT.json`
  - File SHA-256: `37a16d8f861a5d75ef7baabafa48a3133584023e9c51937a7487db40cb0b7c72`
  - Result self-seal: `76a41f4f1d3224f6dfadebbb29db9a78c55e97ac975dded57fe6d1e766be7ced`
- SLC Dense Exact v0.2 four-SLC N72 successor:
  `18_SAM_NATIVE_QC/SLCV002C4N72_FOUR_SLC_CLUSTER_EXACT_N72/release/SLCV002C4N72_RESULT.json`
  - File SHA-256: `b3ab2e98a4deafbc81fb2fbab956958f0ed5df7a801dbeee8de9b64b45fb4bde`
  - Result self-seal: `52458abc4d95b90b9fb0431f7a23f76770a7810abc6eef94eae4218d2b91f076`
  - Executable seal: `e3b4d7522c3ff9645bfa8d8fec60a1206bfeab84711fff1a9391c0f734fc358e`
- SLC Dense Exact v0.2 four-SLC fresh N72 I01 holdout:
  `18_SAM_NATIVE_QC/SLCV002C4N72I01_FRESH_HOLDOUT/release/SLCV002C4N72I01_RESULT.json`
  - File SHA-256: `6823607b07a9d36e9303e3c797c428be65b6913a7d72f8913e598d0e55875c43`
  - Result self-seal: `ecd396f0b2fdfdb93e1a062ad0d385e04acc09de0a29dfa59711d7cb0eb7ee48`
  - Executable seal: `6b921439cf43b76cde54bdb5ad62796d7676e9b849630763d3ded6d62a2dd668`
  - Post-run audit:
    `18_SAM_NATIVE_QC/SLCV002C4N72I01_FRESH_HOLDOUT/release/SLCV002C4N72I01_AUDIT.json`
- Historical SLCX031 N72 boundary:
  `18_SAM_NATIVE_QC/SLCX031_DENSE_N72_EXACT_DOS_WIDTH22_FUSED_INDEPENDENT_REFERENCE/release/SLCX031_RESULT.md`
  - SHA-256: `5cb577aa522557634ae86244c3a58be19ce46f4ef9ba1dc97ac340e511284689`

## Required campaign declaration

Every new SLC or SLCX contract/result should record these identities separately:

```text
sam_language_version_used:
sam_language_candidate_id:
sam_ui_version_used:
slc_component:
slc_component_version:
slc_system_revision:
slc_execution_usage:
slc_address_model:
slcx_campaign_id:
numerical_engine_lineage:
version_context_as_of:
```

Use `slc_execution_usage: NOT_EXECUTED` when a campaign only borrows SLC
naming, addressing, or decomposition. Do not describe such a sidecar as an SLC
system or SAM Language runtime benchmark.
