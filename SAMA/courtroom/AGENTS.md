# AGENTS.md — SAM / SLC Repository Operating Guide

This file is the compression-safe starting point for coding and research agents working in the SAM repositories. Read it before editing, executing, grading, or summarizing anything.

## 1. Project identity

**SAM** is the Substrate Accumulation Model.

The project is idea-first. Its central physical intuition is:

> Matter displaces the substrate/space, and displacement accumulates.

The equations, particle grammar, Courtroom tests, Starbreaker, SAM Language, and SLC are downstream formalizations and tests of that idea. Do not reverse the genealogy and present a later numerical identity as the origin of the model.

The repository is not a conventional polished codebase. It is an auditable scientific record. Failed runs, superseded interpretations, wrong controls, and implementation defects are preserved rather than erased.

## 2. Agent mission

An agent working here should do four things well:

1. Recover the exact current state from source artifacts.
2. Preserve typed distinctions and claim boundaries.
3. Make the smallest correct change that advances the requested task.
4. Leave a compression-safe record so the next agent can continue without reconstructing the project from scratch.

Do not substitute confidence, skepticism, or general scientific commentary for source inspection and executable work.

## 3. Canonical mathematical spine

Current core primitives and derived quantities:

```text
ĥ = 2
D  = 3
π  = geometric primitive

R  = ĥ²D = 12
S  = ĥᴰ = 8
X  = D^(D−1) − S = 1
W  = S + X = D² = 9
Θ  = ĥW = R²/S = 18
V  = DW = D³ = 27
F  = DV = W² = D⁴ = 81
N  = R² = SΘ = 144
M  = N − Θ = (S−1)Θ = 126
L  = ĥF = WΘ = 162
P  = F − X = 80
```

Typed hierarchy:

```text
S8 --B/contact activates X1--> W9 -> V27 -> F81 -> L162
```

Important:

- Equal numbers do not imply equal entities.
- Repeated `1`, `8`, `9`, `12`, and `81` roles must remain separately typed.
- `P = 80` is a structural identity. It is **not** the current particle-row count.

## 4. The current W8–X1–W9 interpretation

Use this wording unless a newer sealed artifact supersedes it:

```text
W8:
    unresolved eight-position octahedral shell/state

B:
    contact or activation operator

X1:
    one complete reciprocal information relay

W9:
    terminal resolved state/write
```

The closure witness is the complete transition:

```text
W8 --X1 activated by B--> W9
```

Do **not** say:

```text
B contributes 1/2 and X contributes 1/2
X1 is two independent half-operators
W9 alone is the full closure witness
```

Directional endpoint views may be represented, but they are two orientations of one shared relational event:

```text
state A changes
connecting route changes
state B changes
one shared relay/write event completes
```

`Θ18` is presently the strongest moving-carrier candidate. `X1` is the relay/operator, not automatically the moving object. The A-field is a macro accumulation/readout account, not automatically identical to either carrier.

## 5. A-field basics

The basic field quantities are:

```text
A₀ = 1 / (12π) = 0.0265258238...
A(r) = r_s / r = 2GM / (c²r)
```

Working interpretation:

- `A₀` is the nonzero substrate floor.
- `A(r)` is the source-dependent lift above the floor.
- Local gradients, endpoint differences, and path accumulation must remain distinct readouts.
- Recovering a standard weak-field result does not by itself establish a new physical prediction.

Do not write `A₀ = 1(12/π)`. The exact expression is `1/(12π)`.

## 6. QP particle grammar

The complete source grammar contains **321 typed rows**, not 321 independent particles.

Exact census:

```text
72   direct unary
42   conjugate unary
64   ordered pairs
120  unordered triad candidates
8    hidden supports
6    carrier infrastructure rows
1    global scalar parent
8    explicit controls
--------------------------------
321  complete typed source grammar
```

Equivalent typed partition:

```text
285 legal local templates
    114 unary
     64 ordered pairs
    107 admitted triads

14 infrastructure
     8 hidden supports
     6 carriers

1 global parent

21 rejected
    13 rejected triads
     8 explicit controls
```

Interpretation:

```text
unary rows:
    local entity/state candidates

ordered pairs:
    oriented relations or formation steps

triads:
    three-owner closure/face candidates

hidden supports and carriers:
    non-payload infrastructure

rejected rows:
    forbidden constructions or controls; preserve them
```

Current exact aggregates:

```text
100-row complete one-body payload
sum native = 16,200 = 100 × L

81-row selected roster
sum native = 12,600 = 100 × M
```

The observation-blind rule selecting the 81-row roster remains open unless a newer sealed result closes it.

Never revert to “the 80-row particle table.” Use:

```text
321  complete grammar
100  one-body payload
81   selected retained-matter roster
80   structural P = F − X only
```

## 7. Starbreaker

Starbreaker is the proposed dynamical formation engine.

Correct architecture:

```text
QP grammar:
    defines legal productions

162-slot ledger:
    address/capacity structure

Starbreaker:
    generates actual formation trajectories and contacts

terminal remnant:
    retained result of the formation history

isotope cipher:
    decodes remnant structure

binding calculation:
    evaluates retained/escaped/closure account
```

Do not describe matter as if an optimizer places pre-existing pieces with tweezers. The intended claim is that stable matter is the remnant of a dynamical formation process.

Canonical complete-ledger composition:

```text
18 carrier + 126 matter + 18 shadow = 162 total
```

Earlier Starbreaker work found exact-composition residues, later refined by lineage into true single-source ledgers and mixed-source lookalikes. Preserve lineage distinctions.

Known implementation boundary:

- The fixed-inventory localized-versus-dispersed geometry result is valid in its own scope.
- The A-dependent ledger-density response was not correctly executed in the earlier allocation path.
- A corrected row-aligned A-to-ledger replay remains required unless superseded.
- Simulator controls such as `bounce_energy`, `stick_radius`, `cooling`, and `fallback_scale` are normalized controls until a physical-units contract is sealed.

Do not silently turn normalized simulator coordinates into MeV, meters, velocity, impulse, tension, or physical capture energy.

## 8. Binding and Be-8

Binding is a property of the terminal remnant/incidence network, not a primitive property of an isolated QP row.

Keep this order:

```text
formation
-> terminal remnant
-> isotope decoding
-> mass/binding readout
```

The existing calibrated binding baseline should be finished and preserved before any new refit campaign. Do not reopen it casually.

Latest working reports include:

- 118-isotope evaluation surface.
- 20 sub-MeV residual rows.
- A high fraction within 5 MeV in the latest working baseline.

Always read the current sealed result before quoting exact percentages or RMS values.

Be-8 structural result:

```text
u = d = R = 12
```

The current SAM interpretation treats `R12` as a capacity/container boundary rather than a propagating closure element. State this as the scoped structural result; do not claim that one identity replaces all nuclear dynamics.

## 9. SAM Language and SLC

SAM Language must own the scientific semantics. A UI or Python transport layer must not secretly implement calculations by string matching.

Required architecture:

```text
UI / client
    input and presentation only

SAM Language
    parser
    resolver
    type system
    operator registry
    program registry
    authority/provenance

SLC runtime
    12-lebit state
    scheduler
    executor
    execution ledger
    topology readout
```

Forbidden architecture:

```python
if "A_FIELD" in source_text:
    return hidden_python_calculation()
```

Acceptable transport:

```python
compiled = sam_language.compile(program)
packet = slc_runtime.execute(compiled)
return packet
```

The particle grammar should be integrated directly into the language/runtime, not exposed only through a sidecar UI.

Version note:

- The direct particle-grammar runtime was initially framed as the v0.5 target.
- SAM Language, the SAM UI, and the SLC are separate components. The SLC uses
  SAM Language; it does not inherit the SAM Language or UI version number.
- The highest-version validated SAM Language candidate is `0.7.0-candidate`,
  with a formal 12-site / 4,096-address SLC C1 interface.
- The current SAM UI manifest is Phase 2 Candidate 004 and declares SAM
  Language runtime v0.4.2.
- SLC components use their own version sequence. The current dense exact solver
  is `SLC_DENSE_EXACT_V0_2` (`v0.2.0`). Its capacity-26 rule was frozen through
  N24, N48, and N60 before the N72 validations.
- SLCX038 is a historical remote N72 reference campaign that used dense solver
  v0.1 and was interrupted by a Windows restart. It is not the current solver
  version, and its incomplete reference lane is not repaired by the later v0.2
  results.
- `SLCX###` and `SLCV###` names identify campaigns or revisions; they do not
  replace the independent SAM Language, SAM UI, or SLC component versions.
- Read `SAM_LANGUAGE/CURRENT_SLC_VERSION.md` and its cited component artifacts
  before editing version labels.

## 10. Current exact SLC density-of-states campaign

Current validated local state:

```text
SLC Dense Exact v0.2:
    N24 -> N48 -> N60 calibration -> frozen rule -> N60 holdout
    4/4 stages PASS
    6/6 exact instances
    62/62 checkpoints

four-SLC v0.2 execution profile:
    N24 -> N48 -> N60 calibration -> frozen rule -> N60 holdout
    4/4 stages PASS
    6/6 exact instances
    72/72 node checkpoints
    18/18 four-node wave chains

N72 I00:
    instance = SLCX025_N72_I00
    PASS
    induced width = 22
    root batch = 16 × 2^22 = 2^26 retained entries
    192/192 node checkpoints
    48/48 four-node wave chains
    exact represented count = 2^72
    all 871 coefficients equal the preserved historical primary
    runtime = 1,398.647 s = 23 min 18.647 s
    peak sampled aggregate worker RSS = 8.171 GiB

N72 I01 fresh holdout:
    instance = SLCV002C4_N72_I01
    PASS_NO_REFIT_EXACT_HOLDOUT
    first structurally accepted prospective graph
    no width-22, DOS, or runtime screening
    unchanged v0.2 portfolio selected induced width 24
    root batch = 4 × 2^24 = 2^26 retained entries
    768/768 node checkpoints
    192/192 four-node wave chains
    exact represented count = 2^72
    all internal exact and independently derived raw-moment gates PASS
    runtime = 2,825.225 s = 47 min 05.225 s
    peak sampled aggregate worker RSS = 7.276 GiB
    independent reference implementation = not run

combined N72 v0.2 evidence:
    2/2 frozen instances PASS
    960/960 node checkpoints
    240/240 four-node wave chains
    reused checkpoints = 0
    fallback = none
    retry = none
```

Keep the evidence types separate. I00 provides equality to a preserved
historical primary coefficient vector; it is not a new independent
implementation. I01 provides a prospective, unchanged-plan, no-refit internal
exact closure; no independent implementation produced an I01 coefficient
vector. Together they validate the local four-SLC v0.2 software profile on two
frozen N72 instances, not generic N72 performance, distributed hardware,
repeated physical cells, or quantum hardware.

Do not say the CPU literally enumerated `2^72` configurations. The defensible
statement is that the exact represented state space was
reconstructed/aggregated under the SLC dense runtime.

Do not rerun or modify the frozen I00 or I01 single-execution records. Any
additional generalization instance must be a separately precommitted successor,
for example I02, under an explicitly declared solver version.

The strongest remaining external comparison is:

```text
fresh frozen instance
same hardware
same exact coefficient vector
SLC Dense Exact v0.2 versus the strongest independent reference implementation
```

A faster second run is only evidence of learning if persisted state is audited and the speedup generalizes to a fresh hidden instance. Same-instance cache reuse is not sufficient.

## 11. Courtroom standard

The Courtroom chain is:

```text
claim
-> provenance
-> declared premises
-> runner
-> result
-> hashes
```

Two independent fields are required:

```text
execution_status:
    CLEAN | VIOLATED | UNVERIFIABLE

scientific_verdict:
    PASS | BOUNDARY | FAIL | DIAGNOSTIC | RETIRED
```

Core rules:

1. No result exists unless the artifact exists.
2. No PASS exists unless the result file says PASS.
3. No citation counts unless the source path resolves.
4. No grade upgrade exists without branch-local hashes.
5. No agent summary outranks source files.
6. A failed or buggy run remains preserved.
7. No same-run repair when the precommit forbids it.
8. A corrected attempt requires a separately named successor record.
9. Hashes prove process integrity, not physical truth.
10. `BOUNDARY` is a productive frontier, not a shame label.

Before making a strong claim, locate:

```text
precommit
declared premises
runner
result
summary
input/source manifest
HASHES.txt
```

## 12. Claim discipline

Every important statement must be classified mentally as one of:

```text
SEALED:
    directly supported by an immutable result artifact

EXECUTED BUT SCOPED:
    run completed, but promotion ceiling limits interpretation

WORKING RESULT:
    current development result not yet released

INTERPRETATION:
    conceptual reading of existing structure

CANDIDATE:
    proposed operator, bridge, or physical meaning

OPEN:
    absent, unexecuted, unstable, or not observation-blind

RETIRED:
    preserved historical statement no longer active
```

Use the strongest honest formulation, not the strongest imaginable formulation.

## 13. Common prohibited conflations

Do not conflate:

```text
321 grammar rows
with 321 physical particles

P = 80
with an 80-row particle table

100-row payload
with the 81-row selected roster

W9
with the complete W8 -> X1 -> W9 closure witness

X1
with two half-operators

Theta carrier
with X1 relay
with the A-field account

exact state total
with coefficient-for-coefficient proof

first four moments
with a mathematical proof of every coefficient

state-equivalent rate
with literal state enumeration

typed SLC
with a physical quantum computer

simulator protocol
with hardware demonstration

same-instance warm-cache speedup
with generalized learning

a hash chain
with empirical validation
```

## 14. Repository orientation

The principal Courtroom branches commonly include:

```text
00_governance
09a_PARTICLE_MASS_CHAIN
12_QUANTUM_COMPUTING_AND_NETWORKING
14_FOUNDATIONAL_TESTS
15_SCALE_BRIDGE_SIMULATOR
19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER
```

Names and locations evolve. Search the repository rather than assuming a remembered path is current.

At startup, inspect in this order:

1. Root `README.md`.
2. This `AGENTS.md`.
3. The target branch `README.md`.
4. The latest relevant result and precommit.
5. The local `HASHES.txt` and manifest.
6. The actual runtime/compiler source files.
7. Any current campaign or handoff packet.

Do not begin from an old public PDF when newer Courtroom artifacts exist.

## 15. Startup protocol — first 90 seconds

When beginning a task:

```text
A. State the exact requested outcome.
B. Identify the authoritative branch and files.
C. Read the current verdict and promotion ceiling.
D. List typed entities that must not be merged.
E. Check whether the task is:
       source intake
       audit
       constructive new work
       successor repair
       documentation
       UI/runtime implementation
       sealed execution
F. Identify what is explicitly unopened or prohibited.
G. Only then edit or execute.
```

For repo work, provide a short internal plan:

```text
sources
current state
change
tests
artifacts
stop condition
```

## 16. Coding rules

- Prefer exact `Fraction`, integer, or `Decimal` arithmetic where the source contract requires exactness.
- Never convert exact counts to float.
- Preserve deterministic ordering before hashing.
- Record CPU, thread count, memory, OS, runtime version, and wall time for performance claims.
- Scientific logic belongs in SAM Language/runtime operators, not UI code.
- Add wrong controls whenever a false-positive path is plausible.
- Do not optimize away auditability without preserving equivalent receipts or hashes.
- Do not change parameters after seeing a result unless the run is closed and a new successor is precommitted.
- Do not rerun a frozen single-execution record.
- Treat generated IDs, row order, and canonical serialization as part of the contract.
- Keep development probes separate from official executable results.

## 17. Agent communication style

Sean often begins with a physical picture and reaches mathematics through structure. Preserve the idea while making the equations exact.

Preferred response order:

```text
1. What the source/result shows.
2. The exact numbers or equations.
3. What remains open.
4. The next executable move.
```

Avoid:

- generic warnings unrelated to the request;
- repeatedly telling Sean what not to say;
- treating lack of credentials as a scientific argument;
- burying a strong numerical result under pages of disclaimers;
- agreeing with claims that artifacts do not support.

Be direct. Distinguish source fact, inference, and speculation.

## 18. Compression-safe handoff

Before ending a long task or before context compression, write a handoff containing exactly:

```text
TASK
    one-sentence objective

AUTHORITATIVE SOURCES
    exact paths and hashes/SHAs when available

CURRENT SEALED STATE
    verdicts and immutable results

CURRENT WORKING STATE
    unsealed development results

CHANGES MADE
    files created or modified

LAST CLEAN COMMAND
    exact command and exit code

LAST RESULT
    exact numerical/output summary

OPEN QUESTIONS
    no more than seven

DO NOT DO
    prohibited reruns, repairs, refits, or claim promotions

NEXT ACTION
    one concrete step
```

Do not write a narrative biography of the entire project into every handoff. Point back to this file for stable context and record only the task-specific delta.

## 19. Minimal post-compression recovery prompt

An agent recovering after compression should begin with:

```text
Read AGENTS.md, the target branch README, the latest local result,
precommit, manifest, and HASHES.txt. Report:

1. exact current task;
2. strongest sealed result;
3. active working result;
4. open gates;
5. prohibited actions;
6. next command or edit.

Do not execute until those six items are grounded in files.
```

## 20. Current high-priority frontiers

Unless superseded by newer artifacts:

```text
1. Preserve the frozen SLC Dense Exact v0.2 calibration, I00, and I01 records.
2. Use a new prospective successor such as I02 for more N72 generalization evidence.
3. Obtain a fresh independent full coefficient-vector comparison.
4. Audit persisted learning before claiming second-run improvement.
5. Preserve the direct SAM Language ownership of the SLC runtime.
6. Complete the corrected A-to-ledger allocation replay.
7. Keep Starbreaker formation/remnant decoding separate from binding refits.
8. Stabilize a physical mass operator before validation/holdout promotion.
9. Translate normalized Starbreaker controls into a sourced units/semantics contract.
10. Keep physical SLC and quantum claims explicitly experimental.
```

## 21. Final rule

When memory, summaries, and source files disagree:

```text
source artifact > result file > precommit > manifest/hash record
> branch README > agent handoff > conversational memory
```

Do not erase the disagreement. Surface it, identify the authoritative artifact, and preserve the historical record.
