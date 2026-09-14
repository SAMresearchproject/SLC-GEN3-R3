[SAM](../../README.md) · [Research methodology](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Result Language and Historical Status Typing

## Current research connections — 14 September 2026

The global execution authority is SLC-GEN3-R3 / SLC-GEN3-CEV1-R3. The September 2026 research includes exact retained-history computation, RH arithmetic compensation, native Mersenne work, Starbreaker signed reception and ATOM3D contact/grammar. The research index connects the retained derivations to the latest code, results and current domain assignments.

[Current derivations, code and results](../../../docs/RESEARCH.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

SAM result language has exactly three authorized classifications. Courtroom and
other historical artifacts also contain fields such as `PASS`, `FAIL`,
`BOUNDARY`, `DIAGNOSTIC`, `RETIRED`, execution status, validation status and
campaign verdict. These fields remain valuable provenance, but they do not form
additional SAM result grades.

The methodological task is to retain both layers without mistranslation. A test
index copies the source status or verdict so the reader can find the original
record. The manuscript states the current SAM classification only when the
scoped evidence supports one. If no classification has been assigned, the
outcome remains explicitly unclassified.

## 1. The exact classification contract

Only the following strings are used for current SAM result reporting:

1. **The test falsifies the concept.**
2. **The test result suggests the concept is possible.**
3. **The test result suggests strong contact with the concept.**

They are not a numerical scale, probability distribution or invitation to add
adjectives. The manuscript does not weaken them with personal qualifiers or
strengthen them beyond their exact wording.

## 2. Four independent status axes

A single artifact can carry four separate kinds of status:

\[
\mathcal S=(S_e,S_h,S_c,S_a),
\]

where

- \(S_e\) is execution state: did the runner complete and emit usable output?
- \(S_h\) is historical artifact status/verdict: what token did that campaign
  assign under its own contract?
- \(S_c\) is current SAM result classification, if any; and
- \(S_a\) is review/approval state for the exact SAMA revision.

Example:

```text
execution_state: completed
historical_verdict: PASS_SOME_SCOPED_IDENTITY
SAM_classification: The test result suggests strong contact with the concept.
reviewed_and_approved: false
```

No contradiction is present. The first two fields describe the source campaign,
the third gives the authorized current result language, and the fourth says the
atlas document has not yet received owner approval.

## 3. Execution status is not scientific meaning

A runner may finish successfully while the candidate predicate fails. It may
crash before evaluating the predicate. It may hit a resource limit without an
answer. Therefore

\[
S_e\not\Rightarrow S_c.
\]

`completed` means the computational process reached its defined output state.
It does not mean the concept survived. Conversely, an implementation failure
does not mean the concept was falsified.

## 4. Historical verdicts remain source metadata

Courtroom folders were created under several historical contracts. A `PASS`
token can mean that a bounded predicate passed its precommitted gates. A
`BOUNDARY` token can retain partial contact and named opens. A `FAIL` can refer
to a candidate route, a wrong control or a scientific predicate depending on
the record.

The source token is copied verbatim into the bottom test index because changing
it would damage provenance. In narrative prose, its meaning is explained from
the actual result artifact. SAMA does not create an automatic map such as

```text
historical PASS → strong contact
historical BOUNDARY → possible
historical FAIL → falsifies
```

Such a map would ignore scope. The current classification is assigned from the
tested concept and evidence, not from string matching.

## 5. Classification from a declared boundary

Let \(C\) be the concept under test, \(D_t\) the tested domain, \(P\) the
predeclared predicate and \(Y\) the preserved output. Classification begins
from the quadruple

\[
(C,D_t,P,Y).
\]

### 5.1 Falsification

Use **The test falsifies the concept.** when the correctly executed scoped test
contradicts the declared concept. State the counterexample or failed predicate
and preserve the exact domain.

### 5.2 Possibility

Use **The test result suggests the concept is possible.** when the scoped
construction survives the applicable test and establishes the stated
possibility boundary without reaching the program's strong-contact condition.
The document should say what was constructed or retained and what exact item
remains unresolved.

### 5.3 Strong contact

Use **The test result suggests strong contact with the concept.** when the
active project result assigns that classification to the scoped evidence. State
the exact contact—identities, holdouts, transfers, controls or convergent
structure—that carries it.

### 5.4 Unassigned outcomes

If execution is incomplete, the comparator is unresolved, the active authority
has not classified the event, or the artifact is methodological rather than
scientific, keep `result_classification: null`. Name the precise unresolved item
instead of inventing a fourth label.

## 6. Result statements must retain scope

The classification sentence should be adjacent to its scoped claim. A useful
pattern is:

```text
State the declared domain, operator, exact observed result and controls.
Reproduce exactly one of the three authorized classification sentences.
State any remaining specifically named boundary in a separate sentence.
```

This protects the classification without weakening it. Scope is not a skeptical
qualifier; it identifies which concept the test actually addressed.

## 7. Corrections and changing classifications

A later successor can change current understanding without rewriting the prior
artifact. Record:

```text
Attempt A: source verdict and applicable SAM classification under boundary A
Successor B: changed route or corrected implementation under boundary B
Current authority: exact installed interpretation with both artifacts linked
```

If an earlier classification is superseded, the new history entry identifies
that transition. The old result remains part of the derivation chain.

## 8. Approval is a separate field

`reviewed_and_approved` applies to an exact SAMA record or document revision.
It does not certify the universe, replace the result classification or follow
automatically from a builder. Only Sean Brady may set it true for exact content.

Thus a source-bound manuscript can accurately report a strong-contact result
while the manuscript itself remains unapproved. This is the state of the new
volumes until owner review.

## 9. Current boundaries

This document governs result wording, not the scientific criteria of every
campaign. Those criteria are declared by the campaign and preserved in its
artifacts. SAMA does not retroactively standardize all historical verdict trees.

## 10. Related SAMA documents

`SAMA-D000051` distinguishes conceptual failure from implementation fault.
`SAMA-D000053` separates classification from promotion and approval.
`SAMA-D000047` supplies the source precedence needed when historical summaries
disagree.

## Test and result index

No single test defines the project-wide result-language contract. Individual
volume documents carry their exact classified evidence and historical source
statuses in their bottom indexes.

## Atomic SAMA source records

| Record ID | Role in this document |
|---|---|
| `SAMA-C000017-R001` | Exact three-class SAM result-language contract. |
| `SAMA-C000022-R001` | Separation of historical Courtroom fields from current SAM classifications. |

## External references

- [Declaration of Research](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/DECLARATION_OF_RESEARCH.md)
- [Pinned Courtroom rules](../../courtroom/AGENTS.md)

## Revision and approval

This exact revision has `reviewed_and_approved: false` until Sean Brady
explicitly approves it.

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000052`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/RESULT_LANGUAGE_AND_HISTORICAL_STATUS_TYPING.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I–II–III–IV | SAMA-D000052 | Research Methodology | Result Language and Historical Status Typing |

| Document field | Value |
|---|---|
| Purpose | Keep current SAM classifications distinct from historical execution, verdict, custody and review fields while preserving every source artifact exactly. |
| Prerequisite documents | `SAMA-D000051` |
| Used by | `SAMA-D000053`, all result-bearing standard documents and all parent manuscripts |

</details>
