# SAM Phase 2 UI Campaign
## Natural-Language Scientific Interface with Phase 3 Website Readiness
### Sol Ultra Build and Validation Plan

**Primary build model:** Sol Ultra  
**Scientific engine:** frozen SAM Language v0.4.2 native runtime  
**Phase 2 target:** local desktop/web-style UI  
**Phase 3 target:** public website using the same contracts, components, and API surface  
**Opening prompt — preserve exactly:**

> **Shall we pay a game?**

The interface should evoke the spirit of *WarGames* without copying protected visual assets, branding, dialogue sequences, or character likenesses. The design should feel like a disciplined scientific terminal evolving into a modern research console.

---

# 1. Product Goal

Build a UI that lets a user ask SAM a plain-language scientific question without knowing:

- command-line syntax;
- entity IDs;
- operator names;
- Courtroom record numbers;
- packet names;
- branch paths;
- provenance formats;
- authority labels.

The user should be able to type:

```text
What altitude gives zero net clock adjustment around Earth?
```

or:

```text
What does SAM calculate for Au-197 binding?
```

or:

```text
What is the predicted distance to a supernova at zHD = 0.4?
```

The UI must translate the question into a constrained typed request, send that request to SAM Language, receive a validated scientific result, and explain the result without changing its authority or provenance.

---

# 2. Non-Negotiable Architecture

The language model may interpret the question.

The language model may not decide whether the requested science is valid.

```text
User question
    ↓
Natural-language planner
    ↓
Constrained typed execution plan
    ↓
SAM Language validation
    ↓
Scientific packet execution
    ↓
Typed result + authority + provenance
    ↓
Human-readable answer
```

The authority chain is:

```text
User asks
Sol Ultra interprets
SAM Language validates
Scientific packet executes
Sol Ultra explains
Courtroom provenance remains attached
```

The UI must never:

- invent an operator;
- invent an entity;
- upgrade `STRUCTURAL_ONLY`;
- convert `BOUNDARY` into `ACTIVE`;
- overwrite an appeal result;
- merge same-scalar entities;
- bypass type checking;
- execute raw generated Python;
- mutate the registry from a chat response;
- hide a residual;
- hide a failed control;
- answer around an `UnknownOperatorError`;
- answer around an `UnknownEntityError`.

---

# 3. Phase 2 Scope

Phase 2 is a functional research UI running against the frozen local SAM runtime.

It should include:

1. **Ask SAM**
2. **Scientific packet execution**
3. **Conversation follow-up**
4. **Mode control**
5. **Typed result cards**
6. **Expandable calculation trace**
7. **Expandable provenance**
8. **Boundary handling**
9. **Research-question handoff**
10. **Saved sessions**
11. **Export to Markdown and JSON**
12. **Packet browser**
13. **Test-drive gallery**
14. **Local API abstraction compatible with Phase 3**

Phase 2 does not require:

- public accounts;
- payments;
- public hosting;
- multi-tenant permissions;
- remote registry mutation;
- external scientific contract uploads;
- community editing;
- public leaderboards;
- mobile-native applications.

Those belong to Phase 3 or later.

---

# 4. Opening Experience

The first screen should be minimal.

```text
┌────────────────────────────────────────────────────────────┐
│ SAM                                                        │
│                                                            │
│ Shall we pay a game?                                       │
│                                                            │
│ Ask a scientific question...                               │
│                                                            │
│ [ Ask SAM ]                                                │
│                                                            │
│ Mode: Active                                               │
└────────────────────────────────────────────────────────────┘
```

Suggested rotating examples:

```text
Calculate the zero-net circular Earth orbit.
What does SAM predict for Au-197 binding?
Predict the distance modulus at zHD = 0.4.
Show the six-supernova distance panel.
Explain why S8 cannot promote directly to volume.
What is the difference between X1, C1, and P1?
```

The opening should feel inviting rather than theatrical. The phrase is a gateway to scientific exploration, not a claim that SAM is a game.

---

# 5. User Modes

## 5.1 Active Mode

Default mode.

Use only:

```text
ACTIVE
ACTIVE_IN_SOURCE_SCOPE
```

The result may include calibrated packets when those packets are registered for active execution.

Reject:

```text
STRUCTURAL_ONLY
BOUNDARY
OPEN
CONFLICT
SUPERSEDED
REJECTED
```

unless the requested action is inspection rather than execution.

## 5.2 Research Mode

Allows controlled execution of:

```text
STRUCTURAL_ONLY
```

Every result must visibly retain its status.

Example:

```text
STRUCTURAL RESULT
Research mode
No particle row or physical law was promoted
```

Research mode must not authorize:

```text
OPEN
CONFLICT
SUPERSEDED
REJECTED
```

## 5.3 Audit Mode

Shows:

- typed execution plan;
- resolved entities;
- operator signatures;
- authority decisions;
- branch-qualified sources;
- artifact hashes;
- exact formulas;
- wrong controls;
- appeal/supersession chain;
- residual calculations;
- packet version;
- runtime version;
- deterministic result hash.

Audit mode is for reviewers, developers, and Courtroom work.

---

# 6. Natural-Language Planner

The planner must emit a restricted intermediate request.

Example:

```json
{
  "request_type": "scientific_packet",
  "domain": "clocks",
  "packet": "EARTH_ORBIT_CLOCK",
  "operation": "SOLVE_ZERO_NET_CLOCK",
  "inputs": {
    "central_body": "EARTH",
    "orbit_type": "CIRCULAR",
    "reference_clock": "EARTH_SURFACE"
  },
  "mode": "ACTIVE"
}
```

Binding example:

```json
{
  "request_type": "scientific_packet",
  "domain": "nuclear_binding",
  "packet": "BINDING_BU_PACKET",
  "operation": "CALCULATE_ISOTOPE_BINDING",
  "inputs": {
    "element": "Au",
    "Z": 79,
    "N": 118,
    "A": 197
  },
  "mode": "ACTIVE"
}
```

Supernova example:

```json
{
  "request_type": "scientific_packet",
  "domain": "cosmology_distance",
  "packet": "SN_ZHD_DISTANCE",
  "operation": "PREDICT_DISTANCE",
  "inputs": {
    "zHD": 0.4
  },
  "mode": "ACTIVE"
}
```

The planner output must be schema-validated before it reaches SAM Language.

---

# 7. Planner Rules

The planner may:

- infer the domain;
- resolve common scientific names;
- identify units;
- recognize isotope notation;
- recognize follow-up context;
- ask one focused clarification;
- choose among already registered packets;
- prepare an inspection request;
- prepare a research-mode request when explicitly authorized.

The planner may not:

- create a packet;
- install a packet;
- create an operator;
- create an entity;
- choose a stronger authority status;
- reinterpret an appeal;
- use observed output to select a favorable case;
- change scientific constants;
- fill a missing physical law with prose;
- silently switch from active to research mode.

---

# 8. Follow-Up Conversation

The UI should preserve conversational context without weakening execution discipline.

Example:

```text
User:
What altitude gives zero clock adjustment?

SAM:
3,189,068.20 m above the reference Earth radius.

User:
What about the normal GPS orbit?

SAM:
[Reuses domain, Earth, circular-orbit context]
[Runs a new validated packet]
[Returns nonzero GPS correction]
```

Conversation state may retain:

```text
domain
packet family
central body
isotope
selected dataset
units
display preferences
last result ID
```

Conversation state may not retain a result as authority for a new scientific claim unless the new execution plan explicitly references a sealed source or frozen packet output.

---

# 9. Result Card Standard

Every scientific answer should have five layers.

## 9.1 Direct Answer

Answer the user’s actual question.

## 9.2 Numeric Result

Display values with units and sensible precision.

## 9.3 Scientific Status

Examples:

```text
ACTIVE
ACTIVE CALIBRATED PACKET
STRUCTURAL_ONLY
BOUNDARY
OPEN
```

## 9.4 Interpretation

Explain what the result means.

## 9.5 Evidence

Expandable:

- formulas;
- execution trace;
- data inputs;
- uncertainty;
- residual;
- source records;
- hashes;
- wrong controls;
- packet version;
- language version.

---

# 10. Example Result: Zero-Net Earth Orbit

```text
Zero-Net Circular Earth Orbit

Radius
9,567,205.1979 m

Altitude
3,189,068.1979 m

Orbital speed
6,454.7042 m/s

Gravitational clock gain
+20.026035 μs/day

Special-relativistic loss
−20.026035 μs/day

Net adjustment
0.000000 μs/day

Status
ACTIVE SCIENTIFIC PACKET
```

Expandable trace:

```text
EARTH_ORBIT_CLOCK
-> evaluate gravitational contribution
-> evaluate circular-orbit velocity contribution
-> solve equality
-> return zero-net radius
```

---

# 11. Example Result: Au-197 Binding

```text
Au-197 Binding Packet

Z / N / A
79 / 118 / 197

Atomic mass
196.96657010300 u

Observed B_u
31.139752 MeV

SAM base
27.421477 MeV

Operator debit
0.000000 MeV

SAM final
27.421477 MeV

Residual
+3.718275 MeV

Cross-lock
CR274 and CR277 agree within 0.000023 MeV

Status
ACTIVE CALIBRATED PACKET
```

The UI must not hide that the final prediction is below the observed value.

---

# 12. Example Result: Six-Supernova Panel

## Frozen packet result

**Verdict:**

```text
PASS_NATIVE_V4_2_SN_PANEL_ZHD_DISTANCE_PACKET_EXECUTED
```

The six targets were precommitted before residuals were computed.

| Target zHD | CID | Selected zHD | Residual (mag) | Pull |
|---:|---|---:|---:|---:|
| 0.05 | PS15asb | 0.04989000 | -0.164429 | -0.886269 σ |
| 0.10 | 010010 | 0.09950000 | +0.229387 | +1.178079 σ |
| 0.20 | 560150 | 0.19970000 | +0.042048 | +0.245107 σ |
| 0.40 | 05D4ff | 0.40050000 | -0.092250 | -0.582609 σ |
| 0.80 | 03D1fq | 0.79863000 | +0.048126 | +0.167022 σ |
| 1.20 | SCP06H5 | 1.23225000 | -0.221655 | -0.363074 σ |

Summary:

```text
N              = 6
mean bias      = -0.026462 mag
RMSE           = 0.153504 mag
mean pull      = -0.040291 sigma
pull RMSE      = 0.674855 sigma
within 1 sigma = 5/6
within 2 sigma = 6/6
```

The UI should present this as a reproducible scientific packet, not as a claim that six points settle the full cosmology question.

---

# 13. Boundary Handling

When the user asks for unsourced science, the UI should not return a vague failure.

Example question:

```text
How does closure propagate into the next substrate site?
```

Expected answer:

```text
The existing closure hierarchy executed successfully.

The requested local-propagation step is not yet registered.

Missing scientific contracts:
- PROPAGATE_CLOSURE
- LEDGER_SITE
- ADJACENT
- ADJACENT_LEDGER_STATE

Current status:
CR120 boundary — locality and adjacency remain unsourced.

No propagation law was invented.
```

Available actions:

```text
[Show current hierarchy]
[Open research question]
[Show CR120]
[Export CR proposal]
```

---

# 14. Research-Question Generator

When execution stops at a missing scientific edge, the UI may generate a proposed Courtroom question.

It must clearly separate:

```text
what passed
where execution stopped
what entity/operator is missing
what source would be required
what controls should be tested
```

It may not automatically write the missing operator into the runtime.

Example output:

```text
Candidate research question:

Can a completed ledger transfer one Theta closure difference
to a source-defined adjacent native closure site while preserving
the total ledger account?

Status:
PROPOSED CR QUESTION
NOT AN ACTIVE OPERATOR
```

---

# 15. Phase 2 Interface Layout

## 15.1 Main Workspace

```text
┌────────────────────────────────────────────────────────────┐
│ SAM                                                        │
│ Shall we pay a game?                                       │
├────────────────────────────────────────────────────────────┤
│ Conversation                                               │
│                                                            │
│ User question                                              │
│ SAM answer                                                 │
│ Result cards                                               │
│                                                            │
├────────────────────────────────────────────────────────────┤
│ [Ask] [Research] [Audit]                                   │
│ [New Session] [Export] [Packets] [Sources]                 │
└────────────────────────────────────────────────────────────┘
```

## 15.2 Right-Side Inspector

Optional collapsible panel:

```text
Execution
Entities
Operators
Authority
Sources
Hashes
Residuals
Wrong controls
```

## 15.3 Packet Browser

Categories:

```text
Foundational hierarchy
Clocks and GPS
Cosmological distance
Supernova panels
Galaxy halos
Nuclear binding
Particle rows
Cosmic budget
Research boundaries
```

---

# 16. Visual Direction

The aesthetic should combine:

- dark terminal atmosphere;
- modern scientific dashboard;
- restrained phosphor-inspired accents;
- monospaced data where appropriate;
- readable proportional type for explanations;
- sharp status labels;
- subtle grid/ledger motifs;
- animated cursor only on opening;
- no excessive neon;
- no fake “hacking” effects;
- no imitation of the original *WarGames* interface.

Suggested opening behavior:

```text
SAM initializes
cursor blinks once
“Shall we pay a game?” appears
input becomes active
```

Accessibility requirements:

- high contrast;
- keyboard navigation;
- screen-reader labels;
- reduced-motion mode;
- no status communicated only by color;
- adjustable font size;
- copyable numeric output;
- responsive layout.

---

# 17. Phase 3 Website Readiness

Phase 2 must not be built as a dead-end desktop script.

The UI should communicate with SAM through a versioned service boundary:

```text
POST /api/v1/ask
POST /api/v1/plan
POST /api/v1/execute
POST /api/v1/research
GET  /api/v1/entities/{id}
GET  /api/v1/operators/{id}
GET  /api/v1/packets
GET  /api/v1/results/{id}
GET  /api/v1/sources/{id}
```

Phase 2 may use an in-process adapter that implements the same interface.

Phase 3 can replace the adapter with a hosted API without rewriting the UI.

---

# 18. Phase 3 Security Preparation

Build these boundaries now:

```text
UI cannot write to registry
planner cannot execute Python
runtime receives schema-validated plans only
results are immutable
source hashes are returned with results
server chooses installed packet versions
client cannot upgrade authority status
research mode is explicit
audit logs are append-only
```

Phase 3 will additionally require:

- authentication;
- rate limiting;
- session isolation;
- server-side secrets;
- signed result IDs;
- public/private project separation;
- abuse controls;
- database-backed session storage;
- deployment monitoring;
- privacy policy;
- terms of use;
- scientific disclaimer;
- accessibility review;
- browser compatibility testing.

---

# 19. Front-End Technology Guidance

Keep the stack portable.

Recommended:

```text
React or Next.js
TypeScript
component-based result cards
JSON-schema-generated forms
streaming answer renderer
local mock API
versioned API client
```

Alternative local-first implementation:

```text
Python backend
FastAPI service
React/TypeScript frontend
local process launcher
```

Do not tightly couple the UI directly to Python classes.

Use API contracts and JSON schemas.

---

# 20. Back-End Interface

A result object should resemble:

```json
{
  "result_id": "immutable-id",
  "question": "What does SAM calculate for Au-197 binding?",
  "mode": "ACTIVE",
  "plan": {
    "domain": "nuclear_binding",
    "packet": "BINDING_BU_PACKET",
    "operation": "CALCULATE_ISOTOPE_BINDING"
  },
  "result": {
    "entity": "AU197_BINDING_BU_RESULT",
    "authority": "ACTIVE_CALIBRATED_PACKET",
    "values": {
      "observed_Bu_MeV": 31.139752,
      "base_Bu_MeV": 27.421477,
      "operator_debit_MeV": 0.0,
      "final_Bu_MeV": 27.421477,
      "residual_MeV": 3.718275
    }
  },
  "trace": [],
  "sources": [],
  "warnings": []
}
```

---

# 21. Error Contract

Errors should be typed and readable.

```json
{
  "status": "FAIL",
  "error": "UnknownOperatorError",
  "message": "No registered operator named PROPAGATE_CLOSURE",
  "scientific_boundary": {
    "passed_prefix": "S8 -> W9 -> V27 -> F81 -> L162",
    "missing": [
      "PROPAGATE_CLOSURE",
      "LEDGER_SITE",
      "ADJACENT",
      "ADJACENT_LEDGER_STATE"
    ]
  }
}
```

The UI must never expose a raw Python traceback.

---

# 22. Saved Sessions

A saved session should contain:

```text
questions
typed plans
result IDs
packet versions
runtime version
source hashes
mode
display preferences
```

A saved session should not silently rerun against a newer runtime.

When reopened:

```text
This result was generated with SAM Language v0.4.2.
[View frozen result]
[Re-run with current version]
```

---

# 23. Export

Support:

```text
Markdown report
JSON result packet
CSV table
Courtroom-ready evidence bundle
shareable Phase 3 result URL [future]
```

The Markdown export should include:

- question;
- answer;
- values;
- units;
- status;
- interpretation;
- trace;
- sources;
- hashes;
- warnings;
- runtime version.

---

# 24. UI Acceptance Tests

## 24.1 Natural-Language Routing

Require correct plan generation for:

```text
zero-net clock orbit
GPS correction
Au-197 binding
single-SN distance
six-SN panel
closure hierarchy
same-scalar entity explanation
unknown propagation request
```

## 24.2 Authority Preservation

Require:

```text
ACTIVE executes
STRUCTURAL_ONLY requires research mode
OPEN does not execute
CONFLICT does not execute
SUPERSEDED remains historical
REJECTED does not execute
appealed claim uses effective scoped authority
```

## 24.3 Same-Scalar Preservation

Require the UI to distinguish:

```text
X1 axis channel
C1 carrier
P1 support
A1 historical proxy
```

even though all have scalar address 1 where applicable.

## 24.4 Scientific Packet Accuracy

Require exact reproduction of frozen packet outputs:

```text
zero-net Earth orbit
Au-197 B_u packet
single-SN CID 010010
six-SN panel summary
```

## 24.5 Boundary Behavior

Require the propagation question to stop cleanly at the missing contract.

## 24.6 Provenance

Require branch-qualified sources and hashes in audit mode.

## 24.7 Conversation

Require follow-up questions to preserve context without bypassing a new execution.

## 24.8 UX

Require:

```text
no raw traceback
copyable values
working keyboard navigation
responsive layout
reduced motion
clear units
clear status
clear residuals
```

---

# 25. Phase 2 Deliverables

Create:

```text
SAM_UI_PHASE_2/
    README.md
    ARCHITECTURE.md
    API_CONTRACT.md
    DESIGN_SYSTEM.md
    PACKET_CATALOG.md
    SECURITY_BOUNDARIES.md
    PHASE_3_WEB_HANDOFF.md
    frontend/
    backend/
    schemas/
    fixtures/
    tests/
```

Required artifacts:

```text
PHASE_2_UI_MANIFEST.json
PHASE_2_ROUTE_REGISTRY.json
PHASE_2_PACKET_REGISTRY.json
PHASE_2_RESULT_SCHEMA.json
PHASE_2_ERROR_SCHEMA.json
PHASE_2_ACCEPTANCE_REPORT.md
PHASE_2_TEST_RESULTS.json
PHASE_2_PHASE3_COMPATIBILITY_REPORT.md
COMMAND_LOG.txt
HASHES.txt
```

---

# 26. Build Phases

## Phase 2A — Skeleton

- opening screen;
- chat input;
- mode selector;
- result card shell;
- inspector shell;
- local API adapter.

## Phase 2B — Planner

- constrained plan schema;
- Sol Ultra routing prompt;
- entity resolution;
- unit handling;
- clarification behavior.

## Phase 2C — Runtime Integration

- submit typed plan;
- receive typed result;
- handle errors;
- preserve authority;
- render provenance.

## Phase 2D — Scientific Packets

Add and test:

```text
closure hierarchy
Earth orbit clocks
Au-197 binding
single-SN distance
six-SN panel
```

Then add additional frozen packets:

```text
GPS operational orbit
halo calculations
cosmic budget
particle lookup
```

only when their packet contracts are available.

## Phase 2E — Conversation and Export

- follow-up state;
- saved sessions;
- Markdown export;
- JSON export;
- audit bundle.

## Phase 2F — Phase 3 Preparation

- versioned API client;
- environment configuration;
- deployment-neutral routing;
- website handoff report;
- component documentation.

---

# 27. Completion Gate

Phase 2 passes when:

```text
a user can ask a plain-language question
the planner emits a valid constrained plan
SAM Language validates the plan
a registered packet executes
the UI renders values, units, authority, and provenance
follow-up questions work
unsourced science stops cleanly
research mode preserves STRUCTURAL_ONLY
saved results remain reproducible
exports work
Phase 3 can replace the local adapter with a web API
```

Primary verdict:

```text
PASS_SAM_PHASE_2_NATURAL_LANGUAGE_UI
```

Boundary verdict:

```text
BOUNDARY_UI_CORE_PASS_PHASE3_API_HANDOFF_INCOMPLETE
```

Fail verdict:

```text
FAIL_SAM_PHASE_2_TYPED_UI_INTEGRATION
```

---

# 28. Sol Ultra Master Prompt

```text
Execute SAM_PHASE_2_UI_CAMPAIGN_SOL_ULTRA.md exactly as written.

Use Sol Ultra.

Build a Phase 2 natural-language UI for the frozen SAM Language runtime.

The opening prompt must be preserved exactly as:

    Shall we pay a game?

The design may evoke a restrained scientific-terminal atmosphere inspired by
the user's affection for WarGames, but it must not copy protected visual assets,
branding, dialogue sequences, or character likenesses.

The user must be able to ask a scientific question in ordinary language.

Architecture:

    user question
    -> constrained intent planner
    -> typed SAM execution plan
    -> SAM Language validation
    -> scientific packet execution
    -> readable answer
    -> expandable trace and provenance

The model interprets.
SAM Language authorizes and executes.

Do not allow the UI agent to:

    invent operators
    invent entities
    upgrade authority
    merge same-scalar entities
    bypass type checking
    execute generated Python
    mutate the registry
    hide residuals
    answer around runtime rejection

Support three modes:

    Active
    Research
    Audit

Active mode executes only active authority.

Research mode may execute STRUCTURAL_ONLY relations while visibly preserving
their status.

Audit mode shows typed plans, entity resolution, operators, authority,
sources, hashes, residuals, wrong controls, and appeals.

Implement first-class packets and frozen fixtures for:

    full closure hierarchy
    zero-net circular Earth-orbit clock packet
    Au-197 binding B_u packet
    single-SN zHD distance packet
    six-SN precommitted panel

The six-SN panel fixture is:

    target 0.05, CID PS15asb, zHD 0.04989000,
        residual -0.164429 mag, pull -0.886269 sigma

    target 0.10, CID 010010, zHD 0.09950000,
        residual +0.229387 mag, pull +1.178079 sigma

    target 0.20, CID 560150, zHD 0.19970000,
        residual +0.042048 mag, pull +0.245107 sigma

    target 0.40, CID 05D4ff, zHD 0.40050000,
        residual -0.092250 mag, pull -0.582609 sigma

    target 0.80, CID 03D1fq, zHD 0.79863000,
        residual +0.048126 mag, pull +0.167022 sigma

    target 1.20, CID SCP06H5, zHD 1.23225000,
        residual -0.221655 mag, pull -0.363074 sigma

Summary:

    N = 6
    mean bias = -0.026462 mag
    RMSE = 0.153504 mag
    mean pull = -0.040291 sigma
    pull RMSE = 0.674855 sigma
    within 1 sigma = 5/6
    within 2 sigma = 6/6

When the user asks about local closure propagation, preserve the CR120 frontier:

    existing hierarchy PASS
    PROPAGATE_CLOSURE missing
    LEDGER_SITE missing
    ADJACENT missing
    ADJACENT_LEDGER_STATE missing

Do not invent the missing science.

Build Phase 2 with Phase 3 website migration in mind.

Use a versioned service boundary:

    POST /api/v1/ask
    POST /api/v1/plan
    POST /api/v1/execute
    POST /api/v1/research
    GET /api/v1/entities/{id}
    GET /api/v1/operators/{id}
    GET /api/v1/packets
    GET /api/v1/results/{id}
    GET /api/v1/sources/{id}

Phase 2 may use an in-process local adapter that implements the same interface.
Phase 3 will replace it with a hosted API without rewriting the UI.

Use a component-based TypeScript front end and a clean JSON API boundary.
Do not tightly couple the UI to Python implementation classes.

Create all required source, schemas, fixtures, tests, documentation, manifests,
hashes, command logs, acceptance reports, and Phase 3 handoff records.

Acceptance requires:

    plain-language questions route correctly
    typed plans are schema-valid
    SAM Language remains the authority gate
    scientific packets reproduce frozen outputs
    same-scalar entities remain distinct
    STRUCTURAL_ONLY remains visible
    unsourced science stops cleanly
    no raw traceback reaches the user
    follow-up questions work
    Markdown and JSON export work
    the local API adapter can be replaced by a Phase 3 web API

Stop after one validated Phase 2 candidate.

Return:

    candidate hash
    test result
    supported packet list
    known boundaries
    Phase 3 readiness status
    launch recommendation
```
