[SAM](../../README.md) · [Research methodology](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Failure Preservation, Corrections and Successor Repairs

## Current research connections — 14 September 2026

The global execution authority is SLC-GEN3-R3 / SLC-GEN3-CEV1-R3. The September 2026 research includes exact retained-history computation, RH arithmetic compensation, native Mersenne work, Starbreaker signed reception and ATOM3D contact/grammar. The research index connects the retained derivations to the latest code, results and current domain assignments.

[Current derivations, code and results](../../../docs/RESEARCH.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

SAM keeps meaningful failures because a research program is not represented by
its final formulas alone. A failed candidate records which route was actually
tried, which premise broke, and what structure the failure revealed. A
bug-affected run records a different fact: the implementation did not execute
the declared mathematical question. A corrected run adds a new event to the
chain; it does not rewrite the earlier event into something that never happened.

This preservation rule turns deviation chains into technical exposition. The
reader sees why an appealing first route was attempted, how the evidence
separated conceptual failure from implementation fault, what changed in the
successor, and which parts of the original construction survived.

## 1. Outcome typing before repair

After an unexpected output, first determine which layer failed. Let

\[
C\xrightarrow{D}M\xrightarrow{I}X\xrightarrow{E}Y
\xrightarrow{J}R
\]

denote concept (C), derivation (D), mathematical specification (M),
implementation (I), executable state (X), execution (E), raw output
(Y), interpretation (J), and reported result (R).

The observed problem can occur at any arrow:

| Failure location | Diagnostic meaning |
|---|---|
| (D) | The conceptual association was translated into the wrong technical object. |
| (M) | The proposed mathematical relation fails or has a narrower domain. |
| (I) | The code does not implement the declared specification. |
| (E) | Runtime, precision, resource or environment conditions prevent the question from being answered. |
| (J) | The output was classified or summarized outside its declared boundary. |

The first task is localization, not rescue. A formula should not be patched to
compensate for a parser bug, and an implementation error should not be reported
as though it falsified the concept.

## 2. Four preserved event types

### 2.1 Conceptual or mathematical failure

The runner correctly implements the declared route and returns a counterexample
or misses the declared predicate. The event is preserved with the tested domain,
inputs, counterexample and applicable classification. A successor must state
which premise or operator changes.

### 2.2 Boundary result

Part of the relation executes while another named part remains open. Historical
artifacts may call this `BOUNDARY`; current SAM prose states the specific closed
and open items. The partial structure can become the basis of a narrower
successor without being inflated into full closure.

### 2.3 Implementation fault

The code, wiring, path, schema, precision or serialization fails before the
declared mathematical predicate is faithfully evaluated. Preserve the run,
identify the exact fault, and show why the repair does not alter the scientific
verdict tree.

### 2.4 Resource-unresolved execution

The intended computation reaches a declared limit without resolving the
predicate. Preserve elapsed work, limits and partial artifacts. Do not rename
an unresolved computation as a falsification or possibility result.

## 3. Append-only correction chain

A complete correction chain has the form

```text
Attempt A declaration
→ Attempt A runner and output
→ fault/counterexample localization
→ preserved Attempt A result
→ Successor B declaration with exact delta
→ Successor B runner and output
→ comparison against A and original boundary
```

The delta between attempts is the central technical object. Define

\[
\Delta_{A\to B}
=(\Delta M,\Delta I,\Delta X,\Delta C,\Delta R_b),
\]

where the components are changes to the mathematical specification,
implementation, inputs, controls and result boundary. For a pure implementation
repair, the expected contract is

\[
\Delta M=\Delta X=\Delta C=\Delta R_b=0,
\qquad \Delta I\ne0.
\]

For a scientific successor, \(\Delta M\) or \(\Delta R_b\) may be load-bearing
and must be stated rather than hidden.

## 4. Same-run repair versus separately named successor

The active campaign determines whether a correction may occur inside one
record.

### 4.1 Correctable implementation event

If the precommitted premises and verdict tree remain unchanged, a path or field
lookup defect may be repaired within a campaign when its rules allow it. The
result must preserve the first failed execution and identify the exact code
change.

### 4.2 Frozen scientific definition

If repair would change a formula, constant, target, row set, selector,
tolerance or scientific gate, the original record cannot simply be edited into
a pass. The new route is a separately named candidate, appeal or successor.
This preserves the information that the first definition failed.

### 4.3 Completed or approved artifact

A frozen campaign, completed SAMA revision or approved document is never
corrected in place. A supplemental artifact or new revision identifies what it
supersedes while leaving the prior bytes available.

## 5. Worked methodology example: CR281

The bounded three-record campaign precommitted its source set, premises,
controls and verdict trees. On the first CR281 execution, the runner searched
`CR114_summary.json` for the field `free_parameters_total`. The frozen source
containing that field was `CR114_cosmic_baryon_bridge.json`.

The diagnosis was therefore:

| Layer | State |
|---|---|
| Conceptual question | unchanged |
| Mathematical formula and verdict tree | unchanged |
| Permitted source set | unchanged; both paths resolved against the precommitted source custody |
| Implementation lookup | wrong file selected |
| First execution | failed and preserved |
| Repair | point the lookup to the source artifact that actually owns the field |
| Corrected execution | completed and validated |

In delta notation,

\[
\Delta_{A\to B}=(0,\Delta I,0,0,0).
\]

The final campaign result explicitly carries the note. This is the desired
record: readers can distinguish a valid correction from a changed scientific
target.

## 6. What a failed route contributes

A preserved failure can supply any of the following:

- a counterexample fixing the admissible domain;
- evidence that two types cannot be identified;
- a residual whose factorization exposes a missing variable;
- a control showing that the test does or does not separate alternatives;
- a performance boundary for an exact algorithm;
- a source-custody defect requiring a successor artifact; or
- a proof that an attractive shortcut changes the physical model.

The next derivation should cite the failure at the point where it changes the
route. A deviation chain is not an appendix of embarrassing attempts; it is the
causal explanation of the final construction.

## 7. Failure-preserving manuscript pattern

Every substantial SAMA technical section should use the following pattern when
the evidence supports it:

1. State the conceptual aim of the first route.
2. Derive the route completely enough to show why it was plausible.
3. State its fixed domain, controls and expected predicate.
4. Present the exact failure or fault artifact.
5. Diagnose the broken arrow in the concept-to-result chain.
6. State what remains valid from the first attempt.
7. Derive the successor's exact delta.
8. Execute or cite the successor.
9. Compare the two outcomes under their correct boundaries.
10. End at the current result without deleting either event.

## 8. Anti-erasure controls

The record is incomplete if it:

- overwrites a failed output with a corrected file;
- changes a formula under the same frozen identity;
- removes counterexample rows;
- enlarges a tolerance after seeing the miss;
- reports only the corrected timing when the first run exposed a resource
  boundary;
- calls a bug a conceptual falsification; or
- calls a scientific successor a mere implementation fix.

## 9. Current boundaries

Failure preservation does not require every transient debugging message to
become a permanent research artifact. Materiality is determined by whether the
event affects the conceptual route, result boundary, evidence custody or
reproducibility. Material events are kept; incidental noise need not be promoted
into the atlas.

## 10. Related SAMA documents

`SAMA-D000050` supplies diagnostic controls. `SAMA-D000052` supplies the exact
result language. `SAMA-D000053` shows how a corrected candidate enters a new
promotion transition.

## Test and result index

The method is source-bound across many campaigns and is not assigned to one
test record in the catalog. The CR281 correction example is preserved through
the pinned campaign result cited below.

## Atomic SAMA source records

| Record ID | Role in this document |
|---|---|
| `SAMA-C000016-R001` | Append-only preservation of failures, implementation faults, corrections and successor repairs. |

## External references

- [Pinned three-record promotion result](../../courtroom/SAM_THREE_CR_PROMOTION_RESULT.md)
- [Repository preservation discipline](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/AGENTS.md)

## Revision and approval

This exact revision has `reviewed_and_approved: false` until Sean Brady
explicitly approves it.

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000051`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/FAILURE_PRESERVATION_CORRECTIONS_AND_SUCCESSOR_REPAIRS.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I–II–III–IV | SAMA-D000051 | Research Methodology | Failure Preservation, Corrections and Successor Repairs |

| Document field | Value |
|---|---|
| Purpose | Preserve failed tests, implementation faults, corrections and retests as a causal derivation chain in which later success supplements rather than erases earlier work. |
| Prerequisite documents | `SAMA-D000050` |
| Used by | `SAMA-D000052`, `SAMA-D000053`, and every volume deviation chain |

</details>
