[SAM](../../README.md) · [Volume III](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# SAM Language and Exact Program Semantics

## SLC-GEN3-R3: current computation — 14 September 2026

SLC-GEN3-R3 and SLC-GEN3-CEV1-R3 are the sole current global runtime and CE, generation GEN3-UNIFIED-EXECUTION1-20260910-G2. Exact execution, acquired support, complete ordered history and exact U/D/V/net/M logarithmic accumulation share one durable machine. Installation records 617 core and 191 memory-admission checks; adoption records 75 checks and 49 managed receipts. Native hosts agree on 8,123,904 exact values. GEN3-RXT-R7.1 adds the C++/CUDA/GMP joint research implementation.

[Current derivations, code and results](../../../docs/ARCHITECTURE.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

SAM Language is the semantic boundary between a mathematical grammar and an
execution. It owns the parser, resolver, checker, type system, operator
definitions, program registry and evaluator. A UI, wrapper or orchestration
layer may transport a program, but it cannot acquire authority to recognize a
phrase and run hidden scientific logic. Exact program meaning belongs to one
declared language path.

That path carries more than a final state. It carries immutable source and
program custody, the typed current state, a separately typed accumulated
history, deterministic receipts and predecessor hashes. Two programs may end
at the same exact state while retaining different route histories. A rejected
operation must be atomic, and a tampered receipt must fail custody rather than
be silently reinterpreted.

The evidence has three time layers that must remain distinct. SAM Language
v0.6 is the preserved formal-simulator campaign whose G01–G16 records test the
semantic and custody surfaces in detail. SAM Language v0.7 is the later typed
12-site reflective-tape candidate. Neither is the SLC version or the current
SLC release. The live repository authority is `SLCQ2-RZ`; historical language
and SLC labels remain source lineage, not current-pointer aliases.

## 1. Opening question and conceptual picture

The governing question is:

> How does a source grammar become one exact, reproducible computation without
> allowing interfaces, profiles, mutable tapes or hidden dispatch paths to
> change its scientific meaning?

The required architecture is

```text
source text or immutable instruction tape
  -> parser
  -> resolver
  -> checker and type system
  -> operator/program registry
  -> evaluator
  -> typed current state + typed history + custody receipt
```

The forbidden alternative is semantic branching outside the language:

```text
UI or wrapper recognizes a phrase
  -> runs an unrelated calculation
  -> returns a value as if the language produced it
```

The first architecture makes source, meaning and result traceable. The second
creates two semantic authorities and breaks provenance even if the returned
number happens to match.

## 2. Version and authority firewall

### 2.1 v0.6: preserved formal-simulator evidence

The v0.6 campaign supplies the focused evidence in this document. It tests one
semantic path, formal-profile isolation, the complete 12-site basis, frozen B
and X1 operators, ordered-pair schedules, native decompositions, state/history
separation, deterministic interfaces, atomic rejection, packaging and 23
wrong controls.

Its source statuses are `PASS` across G01–G16. Those statuses belong to the
sealed v0.6 test surface. They are not an authorized SAMA result
classification and do not make v0.6 the current language or SLC revision.

### 2.2 v0.7: typed reflective-tape candidate

The Volume III source spine records v0.7 as a later typed, source-linked
reflective SLC C1 tape candidate over twelve sites and 4,096 basis addresses.
Its first-class types include

```text
SLCInstructionTape
SLCTape12
SLCTapeInspection
```

Six declared operations create an immutable zero-origin tape, append
B/request/response records, execute it and inspect custody. The executor
validates the zero-origin hash chain, dispatches through inherited exact state
transitions and returns the same `SLCState12` dossier as the corresponding
direct program.

The candidate remains bounded to a straight-line 12-site tape. It has no
self-hosted parser, recursive source generation or general
SAM-Language-to-Dense-Exact adapter. Tape custody and executed state remain
different types.

### 2.3 Current SLC: `SLCQ2-RZ`

The immutable Volume III spine contains historical SLC-current wording from
its creation time. The live authority now controls: `SLCQ2-RZ` is the sole
frozen/default SLC, with its delegated arithmetic/application base separately
typed. SAM Language, the SAM UI and SLC each have their own version lineage.

Accordingly:

```text
SAM Language v0.6  = preserved formal-simulator evidence
SAM Language v0.7  = later typed reflective-tape candidate
SLCQ2-RZ           = sole current/default SLC authority
```

No row in this document promotes one identity into another.

## 3. Definitions and type boundaries

### 3.1 Source, tape, state and history

| Object | Mutability | Semantic role |
|---|---|---|
| source text | fixed for a declared execution | human-readable program origin |
| instruction tape | immutable append/custody object | ordered typed program records and predecessor chain |
| current state | transformed by accepted operators | exact endpoint dossier |
| accumulated history | append-only typed receipt | ordered route, including distinctions erased at the endpoint |
| inspection | read-only | custody and semantic trace readback |

Endpoint equality means

\[
s_{final}^{(1)}=s_{final}^{(2)}.
\]

It does not imply

\[
h^{(1)}=h^{(2)}.
\]

That distinction later supports Complete Exact Write and reciprocal history.

### 3.2 The twelve-site address domain

Let a basis state be a twelve-bit vector

\[
b=(b_0,\ldots,b_{11}),\qquad b_i\in\{0,1\}.
\]

Its canonical integer address is

\[
a(b)=\sum_{i=0}^{11}b_i2^i,
\]

so

\[
0\le a<2^{12}=4{,}096.
\]

The finite address surface permits exhaustive basis, arity, range and site-ID
checks.

### 3.3 Operators and profiles

An operator is resolved by identifier through the registry, checked against a
typed signature, and executed only after the profile admits it. The formal
evidence profile is `FORMAL_CANDIDATE`; normal and research profiles are
rejected in G03. This prevents an application mode from injecting semantics
into a formal campaign.

### 3.4 Exact receipt

A receipt binds at least the declared program, predecessor lineage, exact
state, history and operator trace. The relevant invariants are byte-stable
serialization, deterministic ordering and exact coefficients. Recomputing a
hash for a mutated object does not authorize it; predecessor custody is part
of the chain.

## 4. From source custody to one semantic path

### 4.1 G01 — seal the parent and candidate delta

Before executing semantics, G01 inventories:

```text
parent files                 92
frozen-source files         150
candidate executable files   97
```

Every declared hash matches, no mismatch is reported and the parent remains
unchanged. The candidate delta is therefore distinguishable from inherited
source. Filename equality or an unsealed working tree would not provide the
same custody.

### 4.2 G02 — traverse the only authority path

G02 checks that parser, checker, evaluator, type system and registry exports
resolve to one authority. A representative mixed program emits the trace

```text
RESOLVE
QP_ORDERED_PAIR
SLC_ZERO_REGISTER
SLC_PREPARE_REQUEST
```

Operator digits resolve through the registry. No legacy sidecar or source-text
dispatch is present. The trace matters because a matching endpoint produced
through a hidden path would not be the same semantic result.

### 4.3 G03 — isolate the formal profile

The same path is then invoked under three profiles. `FORMAL_CANDIDATE` is
accepted; normal and research profiles are rejected. Thus the formal evidence
does not borrow undeclared application or exploratory behavior.

## 5. Build and exhaust the formal state surface

### 5.1 G04 — complete basis construction

G04 enumerates all `2^12=4,096` addresses. It verifies the exact dimension,
site-ID order and binary range, then rejects wrong arity, out-of-range values,
wrong register size and unknown/reordered site identifiers.

This establishes a finite formal address space. It does not identify the
twelve sites with physical hardware or assign coupling magnitudes.

### 5.2 G05 — exact canonical-state invariant

The evaluator returns an exact sparse state. G05 checks:

- canonical sparse-key order;
- integer coefficients;
- the engine contract hash; and
- exact norm.

Reordering terms before hashing, converting coefficients to floats or using an
undeclared norm would change the contract even if a display looked similar.

### 5.3 G06 — freeze B request and X1 response

G06 installs B prepare/request and X1 response as differently typed operators.
For every declared basis column it verifies frozen hashes, matrix shapes,
prepare columns, response mapping and involution. B contains a binary flip but
is not identical to the flip; request and response cannot be exchanged.

This is the formal premise used by D39. It defines executable operators inside
the candidate without assigning a physical B-to-X1 causal weld.

## 6. Complete reciprocal and decomposition schedules

### 6.1 G07 — ordered-pair lift

Twelve sites produce

\[
12\cdot11=132
\]

ordered non-self placements. Each placement acts on all 4,096 basis states in
both directions:

\[
132\cdot4{,}096=540{,}672
\]

forward cases and the same number in reverse. Therefore

\[
2\cdot132\cdot4{,}096=1{,}081{,}344.
\]

G07 closes all 1,081,344 classicalized schedule cases. Using unordered pairs,
one direction or a sample would be a different schedule.

### 6.2 G08 — request sign and gauge diagnostics

The four frozen real request candidates `REQ02`, `REQ08`, `REQ09` and `REQ15`
are each tested on all 132 placements:

\[
4\cdot132=528.
\]

All 528 placement cases pass, leaving four surviving gauges under the
installed positive-first-row convention. The diagnostic therefore preserves
ambiguity among the four real gauges instead of selecting one from a desired
downstream result.

### 6.3 G09 — every declared native decomposition

The grammar generates five factor-shape families with exact assignment counts:

| Shape | Assignments |
|---|---:|
| `1×12` | 1 |
| `3×4` | 5,775 |
| `4×3` | 15,400 |
| `6×2` | 10,395 |
| `12×1` | 1 |

Their sum is

\[
1+5{,}775+15{,}400+10{,}395+1=31{,}572.
\]

All 66 rooted-forest parent cases also pass, and the two induction modes
agree. The decomposition is native to the declared grammar rather than an
external factorization imported after execution.

### 6.4 G10 — peel and restore the extra edge

G10 executes 204 exact controls:

```text
1×12 : 132 cases
3×4  :  36 cases
4×3  :  24 cases
6×2  :  12 cases
total: 204 cases
```

For each case, the declared extra edge is peeled, the exposed native
decomposition is evaluated, the same edge is restored, and the original
terminal state returns exactly. Restoring a different edge or accepting graph
isomorphism without exact state equality would weaken the control.

### 6.5 G11 — frozen classical-limit boundary

G11 checks all eight forward/reverse two-bit rows in the frozen classical
limit. Every row matches. The result is deliberately bounded: a complete
classical table is not evidence that complex-phase or general quantum
semantics have been installed.

## 7. State, history and interface custody

### 7.1 G12 — same endpoint, different route

Chain and star programs produce the same exact coefficients and the same
terminal-state hash, but their history hashes differ. In symbols,

\[
s_{chain}=s_{star},
\qquad
\operatorname{hash}(h_{chain})\ne\operatorname{hash}(h_{star}).
\]

The component partition is not used to erase the route. This is the formal
reason an endpoint-returning computation can retain a nontrivial receipt.

### 7.2 G13 — deterministic API and CLI receipts

The same declared program is executed repeatedly through API and CLI. Both
interfaces are byte-deterministic, their receipts match each other, the CLI
exits successfully and no traceback occurs. Interface adapters therefore do
not introduce independent semantics or serialization defaults.

### 7.3 G14 — atomic rejection and tamper detection

G14 mutates coefficient, exponent, operator argument, predecessor hash and
receipt content. Every mutation is detected. Invalid operations reject
atomically, leaving no accepted prefix or partially changed state.

This is a semantic property as well as a custody property: malformed input
does not acquire meaning merely because its first tokens were valid.

### 7.4 G15 — inherited and new replay on a clean wheel

The candidate suite contains

\[
154\text{ inherited}+29\text{ new}=183\text{ tests}.
\]

All 183 pass. The clean wheel contains 37 members, and 13 CLI cases pass with
API/CLI parity, no sidecar or UI dependency, no repository-path dependency and
no traceback. This retest establishes that the candidate package preserves the
parent while carrying the new semantics outside the source checkout.

### 7.5 G16 — keep the wrong controls and open boundaries

All 23 declared wrong controls produce their diagnostic outcomes. The release
also retains five open domains:

1. complex-phase semantics;
2. measurement and publication semantics;
3. physical connectivity;
4. coupling magnitude and cost; and
5. hardware realization.

A passing formal candidate remains scoped because these boundaries remain in
the artifact rather than being erased after the regression run.

## 8. The v0.7 reflective-tape semantics

The v0.7 candidate makes the instruction sequence itself typed data. A typical
execution can be understood as:

1. create a zero-origin `SLCTape12` and record its origin hash;
2. append a typed B/request record whose predecessor is the current tape tip;
3. append a typed X1/response record under the same custody law;
4. seal the straight-line tape;
5. validate the complete predecessor chain;
6. dispatch each record through the inherited exact transition;
7. return `SLCState12` and a separate `SLCTapeInspection`.

If the direct program and tape program contain the same declared operations,
their current-state dossiers match. Their custody still arrives through
different source objects, so the tape is not replaced by the endpoint.

This reflective layer prepares exact program composition and history without
making the language self-hosting. Recursive source generation, a general
parser inside the tape and a complete typed-IR-to-Dense-Exact adapter remain
open.

## 9. Source-native N100-to-F81 compiler boundary

G1 asks a different question from G01–G16: whether the exact language and N100
source rows already carry a complete elementwise semantic map to F81. The
audit finds:

```text
100/100 typed QP source keys
72/100 Shared72 aggregate connector-incidence rows
162 CR211 address rows
0 CR211 QP elementwise assignments
81 F81 semantic sites
10 F81 contact classes
0 N100 rows with a complete elementwise F81 map
```

The missing relation is

```text
QP candidate/template
  -> F81 semantic site or source-native F81 address class.
```

No outcome or residual selects a map. The contact lane is not executed and the
status remains `PARTIAL_DOMAIN__ELEMENTWISE_F81_JOIN_OPEN`.

The boundary shows why formal determinism and semantic completeness are
different. The language can parse, type, execute and receipt a program while
a particular source-to-target scientific join remains absent.

## 10. Controls, deviations and promotion discipline

The full chain prevents several distinct deviations:

| Deviation | Detecting evidence | Preserved correction or boundary |
|---|---|---|
| parent source changes under the candidate | G01 hashes and inventories | parent remains sealed; candidate delta stays explicit |
| hidden semantic dispatch | G02 path and trace | one parser/checker/evaluator/registry path |
| profile leakage | G03 | formal candidate accepts only its declared profile |
| malformed address gains meaning | G04 | range, arity, size and ID rejection |
| request and response collapse | G06 | frozen hashes, shapes and typed mappings |
| sampled schedule called complete | G07 | all 1,081,344 cases executed |
| preferred gauge selected after outcome | G08 | all four survivors preserved |
| endpoint equality erases history | G12 | equal state hash, unequal history hash |
| interface changes semantics | G13 | byte-identical API/CLI receipts |
| partial mutation survives rejection | G14 | atomic rollback and tamper detection |
| source-tree dependency hidden by tests | G15 | clean-wheel replay |
| open physical domains disappear after PASS | G16 | 23 wrong controls and five boundaries retained |
| aggregate incidence becomes elementwise mapping | G1 | zero assignments and unexecuted contact lane preserved |

Passing validation is not promotion. v0.6 stays a preserved formal-simulator
surface, v0.7 stays a reflective-tape candidate, and SLC current authority is
resolved through the live `SLCQ2-RZ` pointer rather than a historical filename.

## 11. Established result and current boundaries

The source-bound language result is:

1. one declared parser/resolver/checker/type/registry/evaluator path owns exact
   program semantics;
2. twelve sites give a complete 4,096-address finite basis;
3. B request and X1 response are frozen, differently typed operators;
4. all 1,081,344 ordered-pair schedule cases and all 31,572 declared native
   decompositions close under their respective tests;
5. current state, immutable source tape and accumulated history remain
   separate;
6. API and CLI produce deterministic identical receipts;
7. malformed operations reject atomically and declared tampering is detected;
8. 154 inherited plus 29 new tests pass in the clean candidate wheel;
9. 23 wrong controls pass while complex phase, measurement/publication,
   physical connectivity, coupling/cost and hardware realization stay open;
10. v0.7 supplies a later typed reflective tape but not general Dense-Exact
    integration; and
11. the N100-to-F81 elementwise semantic join remains open and unexecuted.

The focused G artifacts carry source status `PASS` or the explicit partial
G1 status. The registered atomic records assign no authorized project result
classification to D35, so this revision does not create one.

## 12. Connections and forward handoff

| Document | Connection |
|---|---|
| `SAMA-D000034` | Supplies the N100 source grammar and exact structure-first certificates that language must serialize. |
| `SAMA-D000038` | Receives immutable programs, signed `Z4^9` operations, separate state/history and exact readback for Complete Exact Write. |
| `SAMA-D000039` | Uses the typed B request, X1 response and W9 resolution route. |
| `SAMA-D000042` | Receives the separate history receipt for directional event-reel computation. |
| `SAMA-P000006` | Uses the language as the computation interface for particle grammar, Starbreaker and binding. |

The forward handoff is to Complete Exact Write: compile a declared signed
program to its exact group action, apply it without mutating the tape, and
retain a reconstructible history even when the endpoint returns.

## Test and result index

| Test record key | Role in this document | Source status | Result artifact | Test folder |
|---|---|---|---|---|
| [`G:G01@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | Parent custody and sealed source | `PASS` | [result](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G01_PARENT_CUSTODY_AND_SEALED_SOURCE/PRECOMMIT_LINEAGE.json) | [folder](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G01_PARENT_CUSTODY_AND_SEALED_SOURCE) |
| [`G:G02@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | Single semantic authority path | `PASS` | [result](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G02_SINGLE_PARSER_CHECKER_EVALUATOR_TYPE_SYSTEM_AND_REGISTRY_PATH.json) | [folder](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports) |
| [`G:G03@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | Formal-profile isolation | `PASS` | [result](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G03_FORMAL_PROFILE_ISOLATION.json) | [folder](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports) |
| [`G:G04@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | Twelve-site/4,096-address construction | `PASS` | [result](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G04_TWELVE_SITES_AND_4096_BASIS_ADDRESSES.json) | [folder](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports) |
| [`G:G05@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | Exact canonical-state invariant | `PASS` | [result](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G05_EXACT_CANONICAL_STATE_INVARIANT.json) | [folder](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports) |
| [`G:G06@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | Frozen B request and X1 response operators | `PASS` | [result](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G06_FROZEN_B_PREPARE_REQUEST_AND_X1_RESPONSE_OPERATORS.json) | [folder](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports) |
| [`G:G07@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | Complete ordered-pair lift | `PASS` | [result](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G07_COMPLETE_ORDERED-PAIR_LIFT.json) | [folder](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports) |
| [`G:G08@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | Four request sign/gauge diagnostics | `PASS` | [result](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G08_FOUR_REAL_REQUEST_SIGN-GAUGE_DIAGNOSTICS.json) | [folder](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports) |
| [`G:G09@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | Rooted forests and native decompositions | `PASS` | [result](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G09_ROOTED_FORESTS_AND_ALL_NATIVE_DECOMPOSITIONS.json) | [folder](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports) |
| [`G:G10@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | Extra-edge peel and restore | `PASS` | [result](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G10_EXTRA-EDGE_PEEL_AND_RESTORE.json) | [folder](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports) |
| [`G:G11@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | Frozen classical-limit boundary | `PASS` | [result](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G11_FROZEN_CLASSICAL_LIMIT.json) | [folder](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports) |
| [`G:G12@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | State/history separation | `PASS` | [result](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G12_STATE/HISTORY_SEPARATION.json) | [folder](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G12_STATE) |
| [`G:G13@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | Deterministic API/CLI receipts | `PASS` | [result](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G13_DETERMINISTIC_API_AND_CLI_RECEIPTS.json) | [folder](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports) |
| [`G:G14@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | Atomic rejection and tamper detection | `PASS` | [result](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G14_ATOMIC_REJECTION_AND_TAMPER_DETECTION.json) | [folder](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports) |
| [`G:G15@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | Inherited/new regression and clean-wheel replay | `PASS` | [result](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G15_INHERITED/NEW_REGRESSIONS_AND_CLEAN_WHEEL.json) | [folder](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G15_INHERITED) |
| [`G:G16@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | Boundary and 23 wrong-control preservation | `PASS` | [result](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G16_BOUNDARY_AND_WRONG-CONTROL_PRESERVATION.json) | [folder](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports) |
| `G:G1@SAM-RESEARCH` | Open N100-to-F81 elementwise compiler join | `PARTIAL_DOMAIN__ELEMENTWISE_F81_JOIN_OPEN` | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/2b45b6edf1fb80b70c0193f63e3d32dd218967d6/SLC/SAM_LANGUAGE/SAM_LANGUAGE_CONTACT_NATIVE_SUCCESSOR_DESIGN/SLC_H14F_EXACT_N100_PARTICLE_SPIN_G1_V1/G1_SOURCE_NATIVE_COMPILER_AUDIT.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/tree/2b45b6edf1fb80b70c0193f63e3d32dd218967d6/SLC/SAM_LANGUAGE/SAM_LANGUAGE_CONTACT_NATIVE_SUCCESSOR_DESIGN/SLC_H14F_EXACT_N100_PARTICLE_SPIN_G1_V1) |

## Atomic SAMA source records

| Record ID | Role in this document |
|---|---|
| `SAMA-C000008-R001` | Complete Exact Write computation surface receiving language state/history. |
| `SAMA-C000194-R001` | SAM Language v0.7 typed reflective-tape candidate. |
| `SAMA-C000195-R001` | Single parser-to-evaluator semantic authority path. |
| `SAMA-C000196-R001` | Immutable tape, current state and accumulated-history distinction. |
| `SAMA-C000197-R001` | v0.6/v0.7/current-SLC lineage and wrong-control boundary. |

## External references

None. This chapter is supported by the internal language artifacts, current
SLC authority and permanent test registry.

## Revision and approval

This exact revision has `reviewed_and_approved: false`. Mechanical validation,
source fidelity and complete test routing do not imply approval. The document
changes no language version, current SLC pointer, test record, atomic record or
result classification.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`G:G01@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [V0_6_SLC_C1_CONTRACT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_CONTRACT.json)<br>[V0_6_SLC_C1_PRECOMMIT.md](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_PRECOMMIT.md)<br>[V0_6_SLC_C1_PRECOMMIT_SEAL.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_PRECOMMIT_SEAL.json)<br>[QP_GRAMMAR_CONTRACT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/registry/QP_GRAMMAR_CONTRACT.json)<br>[PRECOMMIT_LINEAGE.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G01_PARENT_CUSTODY_AND_SEALED_SOURCE/PRECOMMIT_LINEAGE.json)<br>[QP_GRAMMAR_CONTRACT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/data/QP_GRAMMAR_CONTRACT.json) | [build_v06_slc_c1_precommit.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/build_v06_slc_c1_precommit.py)<br>[cr005_gps_calibration.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/cr005_gps_calibration.sam)<br>[declared_42164km_circular_orbit.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/declared_42164km_circular_orbit.sam)<br>[invalid_deep_conjugate.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_deep_conjugate.sam)<br>[invalid_neutral_conjugate.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_neutral_conjugate.sam)<br>[invalid_physical_mass.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_physical_mass.sam)<br>[invalid_relation_as_constituent.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_relation_as_constituent.sam)<br>[invalid_starbreaker_transition.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_starbreaker_transition.sam)<br>[invalid_static_slot_placement.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_static_slot_placement.sam)<br>[invalid_unresolved_volume.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_unresolved_volume.sam)<br>[mixed_core_qp.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/mixed_core_qp.sam)<br>[qp_admitted_triad.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_admitted_triad.sam)<br>[qp_carrier.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_carrier.sam)<br>[qp_hidden_support.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_hidden_support.sam)<br>[qp_native_signature.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_native_signature.sam)<br>[qp_ordered_pair.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_ordered_pair.sam)<br>[qp_rejected_triad.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_rejected_triad.sam)<br>[qp_scalar_parent.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_scalar_parent.sam)<br>[qp_triad.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_triad.sam)<br>[qp_unary.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_unary.sam)<br>[slc_bell.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_bell.sam)<br>[slc_ghz12_chain.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_ghz12_chain.sam)<br>[slc_ghz12_star.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_ghz12_star.sam)<br>[slc_peel_restore.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_peel_restore.sam)<br>[structural_only_research.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/structural_only_research.sam)<br>[valid_closure.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/valid_closure.sam)<br>[__init__.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/__init__.py)<br>[cli.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/cli.py)<br>[diagnostic_probe_map.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/diagnostic_probe_map.py)<br>[errors.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/errors.py)<br>[evaluator.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/evaluator.py)<br>[kernels.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/kernels.py)<br>[model.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/model.py)<br>[parser.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/parser.py)<br>[provenance.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/provenance.py)<br>[qp_grammar.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/qp_grammar.py)<br>[qp_native.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/qp_native.py)<br>[registry.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry.py)<br>[registry_core.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry_core.py)<br>[registry_qp.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry_qp.py)<br>[registry_slc.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry_slc.py)<br>[runtime.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/runtime.py)<br>[slc_state.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/slc_state.py)<br>[type_system.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/type_system.py)<br>[__init__.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/__init__.py)<br>[test_v03_probe_regression_map.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v03_probe_regression_map.py)<br>[test_v042_clock_kernel.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v042_clock_kernel.py)<br>[test_v04_runtime.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v04_runtime.py)<br>[test_v05_direct_integration.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_direct_integration.py)<br>[test_v05_grammar_exhaustive.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_grammar_exhaustive.py)<br>[test_v05_negative_boundaries.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_negative_boundaries.py)<br>[test_v05_source_tamper.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_source_tamper.py)<br>[test_v05_theorem_regression.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_theorem_regression.py)<br>[test_v06_slc_c1.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v06_slc_c1.py)<br>[clean_wheel_probe.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/clean_wheel_probe.py)<br>[development_clean_wheel.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/development_clean_wheel.py)<br>[development_static_check.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/development_static_check.py)<br>[reference_qp_enumerator.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/reference_qp_enumerator.py)<br>[run_internal_tests.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/run_internal_tests.py)<br>[run_v06_slc_c1_acceptance.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/run_v06_slc_c1_acceptance.py)<br>[seal_v06_slc_c1_executable.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/seal_v06_slc_c1_executable.py) | [G16_BOUNDARY_AND_WRONG-CONTROL_PRESERVATION.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G16_BOUNDARY_AND_WRONG-CONTROL_PRESERVATION.json) | [V0_6_SLC_C1_ACCEPTANCE_RESULT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_ACCEPTANCE_RESULT.json)<br>[V0_6_SLC_C1_ACCEPTANCE_RESULT.md](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_ACCEPTANCE_RESULT.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |
| [`G:G02@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |
| [`G:G03@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |
| [`G:G04@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |
| [`G:G05@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |
| [`G:G06@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |
| [`G:G07@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |
| [`G:G08@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |
| [`G:G09@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |
| [`G:G10@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |
| [`G:G11@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |
| [`G:G12@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [V0_6_SLC_C1_CONTRACT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_CONTRACT.json)<br>[V0_6_SLC_C1_PRECOMMIT.md](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_PRECOMMIT.md)<br>[V0_6_SLC_C1_PRECOMMIT_SEAL.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_PRECOMMIT_SEAL.json)<br>[QP_GRAMMAR_CONTRACT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/registry/QP_GRAMMAR_CONTRACT.json)<br>[PRECOMMIT_LINEAGE.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G01_PARENT_CUSTODY_AND_SEALED_SOURCE/PRECOMMIT_LINEAGE.json)<br>[QP_GRAMMAR_CONTRACT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/data/QP_GRAMMAR_CONTRACT.json) | [build_v06_slc_c1_precommit.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/build_v06_slc_c1_precommit.py)<br>[cr005_gps_calibration.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/cr005_gps_calibration.sam)<br>[declared_42164km_circular_orbit.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/declared_42164km_circular_orbit.sam)<br>[invalid_deep_conjugate.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_deep_conjugate.sam)<br>[invalid_neutral_conjugate.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_neutral_conjugate.sam)<br>[invalid_physical_mass.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_physical_mass.sam)<br>[invalid_relation_as_constituent.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_relation_as_constituent.sam)<br>[invalid_starbreaker_transition.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_starbreaker_transition.sam)<br>[invalid_static_slot_placement.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_static_slot_placement.sam)<br>[invalid_unresolved_volume.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_unresolved_volume.sam)<br>[mixed_core_qp.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/mixed_core_qp.sam)<br>[qp_admitted_triad.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_admitted_triad.sam)<br>[qp_carrier.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_carrier.sam)<br>[qp_hidden_support.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_hidden_support.sam)<br>[qp_native_signature.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_native_signature.sam)<br>[qp_ordered_pair.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_ordered_pair.sam)<br>[qp_rejected_triad.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_rejected_triad.sam)<br>[qp_scalar_parent.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_scalar_parent.sam)<br>[qp_triad.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_triad.sam)<br>[qp_unary.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_unary.sam)<br>[slc_bell.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_bell.sam)<br>[slc_ghz12_chain.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_ghz12_chain.sam)<br>[slc_ghz12_star.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_ghz12_star.sam)<br>[slc_peel_restore.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_peel_restore.sam)<br>[structural_only_research.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/structural_only_research.sam)<br>[valid_closure.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/valid_closure.sam)<br>[__init__.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/__init__.py)<br>[cli.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/cli.py)<br>[diagnostic_probe_map.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/diagnostic_probe_map.py)<br>[errors.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/errors.py)<br>[evaluator.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/evaluator.py)<br>[kernels.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/kernels.py)<br>[model.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/model.py)<br>[parser.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/parser.py)<br>[provenance.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/provenance.py)<br>[qp_grammar.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/qp_grammar.py)<br>[qp_native.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/qp_native.py)<br>[registry.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry.py)<br>[registry_core.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry_core.py)<br>[registry_qp.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry_qp.py)<br>[registry_slc.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry_slc.py)<br>[runtime.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/runtime.py)<br>[slc_state.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/slc_state.py)<br>[type_system.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/type_system.py)<br>[__init__.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/__init__.py)<br>[test_v03_probe_regression_map.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v03_probe_regression_map.py)<br>[test_v042_clock_kernel.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v042_clock_kernel.py)<br>[test_v04_runtime.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v04_runtime.py)<br>[test_v05_direct_integration.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_direct_integration.py)<br>[test_v05_grammar_exhaustive.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_grammar_exhaustive.py)<br>[test_v05_negative_boundaries.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_negative_boundaries.py)<br>[test_v05_source_tamper.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_source_tamper.py)<br>[test_v05_theorem_regression.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_theorem_regression.py)<br>[test_v06_slc_c1.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v06_slc_c1.py)<br>[clean_wheel_probe.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/clean_wheel_probe.py)<br>[development_clean_wheel.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/development_clean_wheel.py)<br>[development_static_check.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/development_static_check.py)<br>[reference_qp_enumerator.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/reference_qp_enumerator.py)<br>[run_internal_tests.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/run_internal_tests.py)<br>[run_v06_slc_c1_acceptance.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/run_v06_slc_c1_acceptance.py)<br>[seal_v06_slc_c1_executable.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/seal_v06_slc_c1_executable.py) | [G16_BOUNDARY_AND_WRONG-CONTROL_PRESERVATION.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G16_BOUNDARY_AND_WRONG-CONTROL_PRESERVATION.json) | [V0_6_SLC_C1_ACCEPTANCE_RESULT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_ACCEPTANCE_RESULT.json)<br>[V0_6_SLC_C1_ACCEPTANCE_RESULT.md](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_ACCEPTANCE_RESULT.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |
| [`G:G13@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |
| [`G:G14@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |
| [`G:G15@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [V0_6_SLC_C1_CONTRACT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_CONTRACT.json)<br>[V0_6_SLC_C1_PRECOMMIT.md](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_PRECOMMIT.md)<br>[V0_6_SLC_C1_PRECOMMIT_SEAL.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_PRECOMMIT_SEAL.json)<br>[QP_GRAMMAR_CONTRACT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/registry/QP_GRAMMAR_CONTRACT.json)<br>[PRECOMMIT_LINEAGE.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G01_PARENT_CUSTODY_AND_SEALED_SOURCE/PRECOMMIT_LINEAGE.json)<br>[QP_GRAMMAR_CONTRACT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/data/QP_GRAMMAR_CONTRACT.json) | [build_v06_slc_c1_precommit.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/build_v06_slc_c1_precommit.py)<br>[cr005_gps_calibration.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/cr005_gps_calibration.sam)<br>[declared_42164km_circular_orbit.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/declared_42164km_circular_orbit.sam)<br>[invalid_deep_conjugate.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_deep_conjugate.sam)<br>[invalid_neutral_conjugate.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_neutral_conjugate.sam)<br>[invalid_physical_mass.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_physical_mass.sam)<br>[invalid_relation_as_constituent.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_relation_as_constituent.sam)<br>[invalid_starbreaker_transition.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_starbreaker_transition.sam)<br>[invalid_static_slot_placement.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_static_slot_placement.sam)<br>[invalid_unresolved_volume.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_unresolved_volume.sam)<br>[mixed_core_qp.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/mixed_core_qp.sam)<br>[qp_admitted_triad.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_admitted_triad.sam)<br>[qp_carrier.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_carrier.sam)<br>[qp_hidden_support.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_hidden_support.sam)<br>[qp_native_signature.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_native_signature.sam)<br>[qp_ordered_pair.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_ordered_pair.sam)<br>[qp_rejected_triad.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_rejected_triad.sam)<br>[qp_scalar_parent.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_scalar_parent.sam)<br>[qp_triad.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_triad.sam)<br>[qp_unary.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_unary.sam)<br>[slc_bell.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_bell.sam)<br>[slc_ghz12_chain.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_ghz12_chain.sam)<br>[slc_ghz12_star.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_ghz12_star.sam)<br>[slc_peel_restore.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_peel_restore.sam)<br>[structural_only_research.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/structural_only_research.sam)<br>[valid_closure.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/valid_closure.sam)<br>[__init__.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/__init__.py)<br>[cli.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/cli.py)<br>[diagnostic_probe_map.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/diagnostic_probe_map.py)<br>[errors.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/errors.py)<br>[evaluator.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/evaluator.py)<br>[kernels.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/kernels.py)<br>[model.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/model.py)<br>[parser.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/parser.py)<br>[provenance.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/provenance.py)<br>[qp_grammar.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/qp_grammar.py)<br>[qp_native.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/qp_native.py)<br>[registry.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry.py)<br>[registry_core.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry_core.py)<br>[registry_qp.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry_qp.py)<br>[registry_slc.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry_slc.py)<br>[runtime.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/runtime.py)<br>[slc_state.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/slc_state.py)<br>[type_system.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/type_system.py)<br>[__init__.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/__init__.py)<br>[test_v03_probe_regression_map.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v03_probe_regression_map.py)<br>[test_v042_clock_kernel.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v042_clock_kernel.py)<br>[test_v04_runtime.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v04_runtime.py)<br>[test_v05_direct_integration.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_direct_integration.py)<br>[test_v05_grammar_exhaustive.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_grammar_exhaustive.py)<br>[test_v05_negative_boundaries.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_negative_boundaries.py)<br>[test_v05_source_tamper.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_source_tamper.py)<br>[test_v05_theorem_regression.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_theorem_regression.py)<br>[test_v06_slc_c1.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v06_slc_c1.py)<br>[clean_wheel_probe.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/clean_wheel_probe.py)<br>[development_clean_wheel.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/development_clean_wheel.py)<br>[development_static_check.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/development_static_check.py)<br>[reference_qp_enumerator.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/reference_qp_enumerator.py)<br>[run_internal_tests.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/run_internal_tests.py)<br>[run_v06_slc_c1_acceptance.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/run_v06_slc_c1_acceptance.py)<br>[seal_v06_slc_c1_executable.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/seal_v06_slc_c1_executable.py) | [G16_BOUNDARY_AND_WRONG-CONTROL_PRESERVATION.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G16_BOUNDARY_AND_WRONG-CONTROL_PRESERVATION.json) | [V0_6_SLC_C1_ACCEPTANCE_RESULT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_ACCEPTANCE_RESULT.json)<br>[V0_6_SLC_C1_ACCEPTANCE_RESULT.md](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_ACCEPTANCE_RESULT.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |
| [`G:G16@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [G16_BOUNDARY_AND_WRONG-CONTROL_PRESERVATION.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G16_BOUNDARY_AND_WRONG-CONTROL_PRESERVATION.json) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000035`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/SAM_LANGUAGE_AND_EXACT_PROGRAM_SEMANTICS.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol III | SAMA-D000035 | SAM Language | Typed Program Semantics, Custody and State-History Separation |

| Document field | Value |
|---|---|
| Purpose | Present the typed grammar, parser-to-evaluator authority path, immutable program custody, state/history separation and v0.6-to-v0.7/current-SLC boundaries owned by SAM Language. |
| Prerequisite documents | `SAMA-D000034` |
| Used by | `SAMA-D000038` |
| Revision state | Unapproved revision 1; no language, SLC, registry or result classification is promoted. |

</details>
