# The Courtroom

The Courtroom is the source-controlled grading, execution, and provenance repository for the **Substrate Accumulation Model (SAM)**.

Its purpose is simple:

```text
claim
-> provenance
-> declared premises
-> runner
-> result
-> hashes
```

The repository preserves the complete scientific record: successful tests, failed tests, wrong controls, superseded interpretations, implementation defects, and successor repairs. Nothing outranks the source artifacts.

For compression-safe agent onboarding, read [AGENTS.md](AGENTS.md) before editing or executing anything.

---

## 1. SAM in one sentence

SAM begins from one physical intuition:

> Matter displaces the substrate/space, and displacement accumulates.

The A-field, particle grammar, Starbreaker, SAM Language, the SLC runtime, cosmology, nuclear binding, and Courtroom campaigns are downstream formalizations and tests of that idea.

SAM has **not** replaced the Standard Model, general relativity, quantum mechanics, or nuclear theory. The repository distinguishes exact structural results, external contacts, calibrated models, working interpretations, and open physical bridges.

---

## 2. Core mathematical spine

Minimal basis:

```text
ĥ = 2
D  = 3
π  = geometric primitive
```

Derived structure:

```text
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

- Equal scalars do not imply equal typed entities.
- `P = 80` is a structural identity, not the current particle-row count.
- `X1` is one complete reciprocal information relay.
- The closure witness is the full transition:

```text
W8 --X1 activated by B--> W9
```

not `W9` in isolation.

---

## 3. A-field foundation

The basic field quantities are:

```text
A₀ = 1 / (12π) = 0.0265258238...
A(r) = r_s / r = 2GM / (c²r)
```

Working interpretation:

```text
A₀
    nonzero substrate floor

A(r)
    source-dependent accumulation lift

gradients
    local force/acceleration readouts

endpoint differences
    clock-rate comparisons

path accumulation
    photon-road and distance-road readouts
```

The repository keeps standard-result recovery separate from claims of new physical prediction.

---

## 4. Particle grammar

The complete QP source grammar contains **321 typed rows**.

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
321  complete source grammar
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
unary rows
    local entity/state candidates

ordered pairs
    oriented relations or formation steps

triads
    three-owner closure/face candidates

supports and carriers
    non-payload infrastructure

rejected rows
    forbidden constructions and controls
```

Current exact aggregates:

```text
100-row complete one-body payload
sum native = 16,200 = 100 × 162

81-row selected roster
sum native = 12,600 = 100 × 126
```

Use the distinctions below:

```text
321  complete grammar
100  one-body payload
81   selected retained-matter roster
80   structural P = F − X only
```

---

## 5. Starbreaker and matter formation

The intended architecture is:

```text
QP grammar
    defines legal productions

162-slot ledger
    provides address/capacity structure

Starbreaker
    generates formation trajectories, contacts, and remnants

terminal remnant
    retained result of the formation history

isotope cipher
    decodes remnant structure

binding calculation
    evaluates retained, escaped, surface, and closure accounts
```

Canonical complete-ledger composition:

```text
18 carrier + 126 matter + 18 shadow = 162
```

Starbreaker is not a static placement optimizer. Matter is treated as the stable remnant of a dynamical formation history.

Known open boundary:

- The fixed-inventory localized-versus-dispersed geometry result remains valid in its scoped form.
- The earlier A-dependent ledger-density allocation path did not execute the intended row-aligned A response.
- A corrected A-to-ledger replay remains required unless superseded by a later sealed record.
- `bounce_energy`, `stick_radius`, `cooling`, `fallback_scale`, and related controls remain normalized simulator quantities until a physical-units contract is sealed.

---

## 6. Binding and Be-8

Binding is treated as a property of the terminal remnant and its incidence network:

```text
formation
-> terminal remnant
-> isotope decoding
-> mass and binding readout
```

The current working binding surface covers 118 isotope rows and includes 20 sub-MeV residuals. Exact percentages, RMS values, and fitted-term counts must be quoted from the latest sealed result rather than conversational memory.

Be-8 structural result:

```text
u = d = R = 12
```

The current interpretation treats `R12` as a capacity/container boundary rather than a propagating closure element. This is a scoped structural result, not a replacement for the full nuclear dynamics of Be-8.

---

## 7. SAM Language and SLC

SAM Language must own the scientific semantics.

```text
UI or client
    input and presentation

SAM Language
    parser
    resolver
    type system
    operator registry
    program registry
    authority and provenance

SLC runtime
    12-lebit state
    scheduler
    executor
    execution ledger
    topology readout
```

Scientific logic must not be hidden in UI string matching or sidecar dispatch.

Bad:

```python
if "A_FIELD" in source_text:
    return hidden_python_calculation()
```

Correct architecture:

```python
compiled = sam_language.compile(program)
packet = slc_runtime.execute(compiled)
return packet
```

The particle grammar belongs directly in the language/runtime.

The three components have independent version sequences:

```text
SAM Language
    0.7.0-candidate is the highest-version validated candidate found

SAM UI
    Phase 2 Candidate 004
    declares SAM Language runtime v0.4.2

SLC Dense Exact Solver
    v0.2.0
    SLC_DENSE_EXACT_V0_2
```

An `SLCX###` or `SLCV###` label identifies a campaign or revision, not a SAM
Language, SAM UI, or SLC component version. The authoritative component record
is [CURRENT_SLC_VERSION.md](SAM_LANGUAGE/CURRENT_SLC_VERSION.md).

---

## 8. Exact SLC density-of-states campaign

The current validated local dense solver is
`SLC_DENSE_EXACT_V0_2` (`v0.2.0`). It uses fused paired-branch exact NTT/CRT
variable elimination, a frozen finite graph-only order portfolio, and a root
batch rule bounded by `2^26` retained and `2^27` logical-union entries.

Its one-SLC calibration path was frozen before the N72 work:

```text
N24 -> N48 -> N60 calibration -> frozen rule -> N60 holdout
4/4 stages PASS
6/6 exact instances
62/62 checkpoints
```

The four-SLC software-cluster profile repeated that ladder successfully, then
executed two separately frozen N72 instances:

```text
N72 I00 — historical-vector validation
    instance = SLCX025_N72_I00
    verdict = PASS
    induced width = 22
    root batch = 16 × 2^22 = 2^26 retained entries
    checkpoints = 192/192
    four-node wave chains = 48/48
    represented count = 2^72
    full 871-coefficient historical-primary equality = true
    wall time = 1,398.647 s = 23 min 18.647 s
    peak sampled aggregate worker RSS = 8.171 GiB

N72 I01 — fresh prospective no-refit holdout
    instance = SLCV002C4_N72_I01
    verdict = PASS_NO_REFIT_EXACT_HOLDOUT
    selection = first structurally accepted graph
    width-22, DOS, and runtime screening = none
    induced width = 24
    root batch = 4 × 2^24 = 2^26 retained entries
    checkpoints = 768/768
    four-node wave chains = 192/192
    represented count = 2^72
    internal exact and independently derived raw-moment gates = PASS
    wall time = 2,825.225 s = 47 min 05.225 s
    peak sampled aggregate worker RSS = 7.276 GiB
    independent reference implementation = not run

combined N72 v0.2 evidence
    frozen instances = 2/2 PASS
    checkpoints = 960/960
    four-node wave chains = 240/240
    checkpoint reuse, retry, fallback, and same-run repair = none
```

The graph width and capacity exponent are different quantities. I00 retains
`16 × 2^22 = 2^26` entries per node task; I01 retains
`4 × 2^24 = 2^26`.

I00 establishes equality to the preserved historical primary vector, but does
not constitute a new independent implementation. I01 establishes prospective
no-refit internal exact closure under the unchanged v0.2 plan, but has no
independent coefficient vector. The combined result validates this local
four-SLC v0.2 software profile on two frozen N72 instances; it is not a generic
N72 guarantee, distributed-hardware result, repeated-physical-cell result, or
quantum-hardware claim.

Do not say the CPU literally enumerated `2^72` states. The defensible
description is:

> The SLC dense runtime reconstructed or aggregated an exact spectrum
> representing `2^72` configurations.

Authoritative result records:

- [Current SLC stack and version record](SAM_LANGUAGE/CURRENT_SLC_VERSION.md)
- [N72 I00 result](18_SAM_NATIVE_QC/SLCV002C4N72_FOUR_SLC_CLUSTER_EXACT_N72/release/SLCV002C4N72_RESULT.md)
- [N72 I01 fresh-holdout result](18_SAM_NATIVE_QC/SLCV002C4N72I01_FRESH_HOLDOUT/release/SLCV002C4N72I01_RESULT.md)
- [N72 I01 post-run audit](18_SAM_NATIVE_QC/SLCV002C4N72I01_FRESH_HOLDOUT/release/SLCV002C4N72I01_AUDIT.md)

---

## 9. Courtroom grading standard

Every test receives two independent classifications:

```text
execution_status
    CLEAN
    VIOLATED
    UNVERIFIABLE

scientific_verdict
    PASS
    BOUNDARY
    FAIL
    DIAGNOSTIC
    RETIRED
```

A scientific PASS requires:

```text
K1  external anchor
K2  explicit falsification statement
K3  target hygiene
K4  typed and traceable inputs
K5  reproduction on demand where ambiguity remains
```

Core artifact rule:

```text
No result exists unless the artifact exists.
No test passed unless the result file says it passed.
No citation counts unless the source path resolves.
No grade upgrade exists without branch-local hashes.
No agent summary outranks the files.
```

Failed and buggy runs remain preserved. If a precommit forbids same-run repair, a corrected execution requires a newly named successor record.

Hashes prove process integrity. They do not prove physical truth.

---

## 10. Claim classes

Use these classes when reading or writing repository documentation:

```text
SEALED
    supported by an immutable result artifact

EXECUTED BUT SCOPED
    completed run with an explicit promotion ceiling

WORKING RESULT
    current development result not yet released

INTERPRETATION
    conceptual reading of existing structure

CANDIDATE
    proposed operator, bridge, or physical meaning

OPEN
    absent, unstable, observation-dependent, or unexecuted

RETIRED
    preserved historical statement no longer active
```

Common prohibited conflations:

```text
321 grammar rows
!= 321 physical particles

P = 80
!= an 80-row particle table

100-row payload
!= 81-row selected roster

W9
!= the full closure witness

X1
!= two half-operators

Theta carrier
!= X1 relay
!= A-field account

exact state total
!= coefficient-for-coefficient proof

raw moments 1–4
!= proof of every coefficient

state-equivalent rate
!= literal state enumeration

typed SLC
!= demonstrated physical quantum computer

same-instance warm-cache speedup
!= generalized learning
```

---

## 11. Repository orientation

Principal branches commonly include:

```text
00_governance
02_A_KERNEL_WEAK_FIELD
03_CLOCKS_AND_GPS
04_PHOTON_ROAD_SHAPIRO_DELAY
06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE
07_BARYON_INVENTORY_AND_COSMOLOGY
08_GALAXY_HALOS_BB_PBH_TRAPPED_A
09a_PARTICLE_MASS_CHAIN
12_QUANTUM_COMPUTING_AND_NETWORKING
14_FOUNDATIONAL_TESTS
15_SCALE_BRIDGE_SIMULATOR
19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER
```

Names and locations evolve. Search the repository rather than relying on remembered paths.

Recommended startup order:

1. Read this file.
2. Read [AGENTS.md](AGENTS.md).
3. Read the target branch `README.md`.
4. Read the latest relevant result and precommit.
5. Read the local manifest and `HASHES.txt`.
6. Inspect the actual runner/runtime/compiler source.
7. Read any active campaign or handoff packet.

---

## 12. Standard branch shape

A typical Courtroom record contains:

```text
NN_BRANCH_NAME/
    README.md

    CR###_TEST_NAME/
        CR###_PRECOMMIT.md
        CR###_declared_premises.json
        CR###_runner.py
        CR###_result.md
        CR###_summary.json
        CR###_input_manifest.csv
        HASHES.txt
```

Actual names vary, but the provenance chain must remain resolvable.

---

## 13. Stewardship

Commercial value received by SAM Research Project LC from SAM-derived work is governed by the binding stewardship declaration sealed on 2026-06-25.

Headline commitment:

> No less than 90% of net proceeds flows to the SAM Foundation for housing, recovery, food security, clean water, medical access, education, and other community public-good purposes.

Authoritative files:

```text
STEWARDSHIP_DECLARATION.md
STEWARDSHIP_DECLARATION_HASH.txt
STEWARDSHIP.md
```

Current declaration SHA-256 recorded by the repository:

```text
d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

---

## 14. Current high-priority frontiers

Unless superseded by newer sealed artifacts:

```text
1. Preserve the frozen SLC Dense Exact v0.2 calibration, I00, and I01 records.
2. Use a new prospective successor such as I02 for more N72 generalization evidence.
3. Obtain a fresh independent full coefficient-vector comparison.
4. Audit persistent learning before claiming rerun improvement.
5. Preserve direct SAM Language ownership of the SLC runtime.
6. Complete the corrected A-to-ledger allocation replay.
7. Keep Starbreaker formation/remnant decoding separate from binding refits.
8. Stabilize a physical mass operator before validation and holdout promotion.
9. Translate normalized Starbreaker controls into a units/semantics contract.
10. Keep physical-SLC and quantum claims explicitly experimental.
```

---

## 15. Contributing and agent behavior

Before changing a scientific artifact:

```text
1. Identify the authoritative source.
2. Read the current verdict and promotion ceiling.
3. Identify typed entities that must remain distinct.
4. Determine whether the work is:
       source intake
       audit
       constructive new work
       successor repair
       documentation
       UI/runtime implementation
       sealed execution
5. Confirm prohibited actions.
6. Make the smallest correct change.
7. Execute the declared tests.
8. Preserve all results and hashes.
9. Stop at the precommitted boundary.
```

For compression-safe task recovery, follow the handoff format in [AGENTS.md](AGENTS.md).

---

## 16. Authority order

When repository artifacts disagree:

```text
source artifact
> result file
> precommit
> manifest or hash record
> branch README
> agent handoff
> conversational memory
```

Do not erase disagreements. Surface them, identify the authoritative artifact, and preserve the history.
