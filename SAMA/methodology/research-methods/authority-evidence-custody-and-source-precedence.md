[SAM](../../README.md) · [Research methodology](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Authority Layers, Evidence Custody and Source Precedence

## Current research connections — 14 September 2026

The global execution authority is SLC-GEN3-R3 / SLC-GEN3-CEV1-R3. The September 2026 research includes exact retained-history computation, RH arithmetic compensation, native Mersenne work, Starbreaker signed reception and ATOM3D contact/grammar. The research index connects the retained derivations to the latest code, results and current domain assignments.

[Current derivations, code and results](../../../docs/RESEARCH.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

SAM does not ask one file to perform every evidential role. Present-tense
authority, immutable history, direct result artifacts, test folders, hashes,
atomic records and manuscripts form a layered evidence system. The layers
cooperate, but they are not interchangeable.

The key methodological distinction is between meaning and custody. A live
document identifies the current authorized interpretation. A numbered history
entry preserves how that interpretation changed. A result artifact records
what an execution produced. A hash fixes byte identity. A SAMA document makes
the conceptual and technical chain readable. Treating any one of those as a
substitute for all the others breaks provenance.

## 1. The authority stack

For present work, the bounded reading order is:

```text
repository rules and controlling declaration
→ global live authority hub
→ one relevant live domain document
→ directly cited history entry or result artifact, when needed
→ focused SAMA atomic record and manuscript synthesis
```

The order is a routing rule, not a ranking of intellectual importance. It
prevents an old handoff or a later-looking paragraph in a historical file from
silently displacing the live pointer.

### 1.1 Live authority

`SAM_LIVE/*.md` holds bounded present-tense interpretive authority. When the
current state changes, the affected section is replaced in place. A live file
is therefore a compact answer to “what is current now?” rather than a diary.

### 1.2 Immutable history

`SAM_HISTORY/entries/HNNNNNN_*.md` preserves the transition. A meaningful
authority change receives a new numbered entry that records its sources, prior
state, exact new statement and preserved boundaries. Finalized history is not
edited to make later developments appear inevitable.

### 1.3 Executable numerical authority

The result artifact is the numerical authority for its own execution. It
records inputs, computed values, checks, verdict/status fields and named opens.
The live narrative may interpret that artifact, but it does not replace its
numbers.

### 1.4 SAMA atomic and document layers

An atomic SAMA record binds one concept, identity, route, result or boundary to
specific sources. A SAMA standard document then develops several such atoms
into a readable start-to-finish explanation. Parent manuscripts integrate the
documents. Until explicit owner review, each remains unapproved even when all
references and hashes validate.

## 2. Courtroom evidence custody

A Courtroom evidence chain is ordered as

\[
\text{claim}
\rightarrow \text{provenance}
\rightarrow \text{declared premises}
\rightarrow \text{runner}
\rightarrow \text{result}
\rightarrow \text{hashes}.
\]

Each arrow answers a distinct question:

| Stage | Question answered |
|---|---|
| Claim | What exact proposition or bounded contact is being tested? |
| Provenance | Where did its objects, constants and target values originate? |
| Declared premises | What was fixed before execution, and what was excluded? |
| Runner | What deterministic operation was actually performed? |
| Result | What happened, including failures and named boundaries? |
| Hashes | Which exact input and output bytes belong to this record? |

The chain is intentionally directional. A hash can establish that a result
file has not changed; it cannot establish that the physical interpretation in
that file is correct. A precommit can establish that a formula was frozen before a
comparison; it cannot replace the resulting execution. An agent summary can
make the chain legible; it cannot supersede the result artifact.

## 3. Source identity as a technical object

For an artifact (F), define the custody descriptor

\[
\mathcal C(F)=(P, K, B, H_F, L),
\]

where (P) is repository identity, (K) is commit or frozen source state,
(B) is the path, (H_F=\operatorname{SHA256}(F)), and (L) is the precise
section or locator used. Two prose references that omit different coordinates
of this tuple may point to materially different evidence.

The SAMA registry therefore stores path, source commit and SHA-256 where the
source type supports them. The document catalog separately stores the hash of
the exact manuscript content. This produces two independent questions:

1. Does the manuscript point to the intended evidence?
2. Is this the exact manuscript revision that was reviewed or handed off?

Both can be answered without confusing evidence validity with owner approval.

## 4. Resolving disagreements

When two layers disagree, SAM preserves the disagreement and follows the
direct-source precedence route:

```text
direct source/result artifact
> precommit, manifest or hash summary
> branch summary
> handoff narrative
> conversational memory
```

The `>` symbol here means “controls the disputed source fact,” not “is always a
better explanation.” A manuscript can explain a result more clearly than a JSON
file, but it may not change the JSON file's value.

### 4.1 Resolution procedure

1. State the exact disputed field or proposition.
2. Identify the artifacts that disagree; do not generalize the conflict.
3. Resolve each artifact's custody descriptor.
4. Read the direct result or source artifact for the disputed fact.
5. Preserve the earlier summary as historical evidence of what was written.
6. Correct the current interpretive layer through a new history entry if the
   disagreement changes current authority.
7. Link the correction to the source that settled it.

This procedure avoids two equal and opposite losses: overwriting the past, and
allowing stale prose to remain current merely because it was once authoritative.

## 5. Example: implementation correction without result erasure

In the preserved three-record promotion campaign, the first CR281 execution
looked for `free_parameters_total` in the wrong JSON file. The declared source
containing the field was a different precommitted artifact. The runner lookup
was corrected without changing the verdict tree, and the final result records
the failed first execution and the correction.

This one event exercises the whole stack:

- source freeze establishes which JSON files were admissible;
- the first run supplies a real implementation-fault artifact;
- the corrected runner is a separately identifiable technical state;
- the result records both the correction and final output; and
- hashes fix the resulting custody.

The correction does not turn the first run into a scientific falsification,
and the passing corrected run does not make the first event disappear.

## 6. Current boundaries

Evidence custody answers what was run and where the result came from. It does
not itself assign a SAM result classification, establish a general theorem from a
finite computation, or authorize promotion. Those transitions require the
specific result boundary in `SAMA-D000052` and the lifecycle in
`SAMA-D000053`.

## 7. Related SAMA documents

`SAMA-D000046` supplies attribution. `SAMA-D000051` develops failure and
correction preservation. `SAMA-D000054` applies the bounded authority stack to
context recovery and handoff.

## Test and result index

This document describes the evidence contract rather than asserting a result
from one indexed test. Campaign examples are cited as fixed methodology
sources through the atomic records below.

## Atomic SAMA source records

| Record ID | Role in this document |
|---|---|
| `SAMA-C000012-R001` | Separation of present-tense live authority and immutable history. |
| `SAMA-C000021-R001` | Claim-to-hash Courtroom evidence chain. |
| `SAMA-C000023-R001` | Source precedence and disagreement-preservation rule. |

## External references

- [SAM current authority](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/SAM_LIVE/00_CURRENT.md)
- [SAM history protocol](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/SAM_HISTORY/README.md)
- [Pinned Courtroom README](../../courtroom/README.md)
- [Pinned Courtroom rules](../../courtroom/AGENTS.md)

## Revision and approval

This exact revision has `reviewed_and_approved: false` until Sean Brady
explicitly approves it.

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000047`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/AUTHORITY_EVIDENCE_CUSTODY_AND_SOURCE_PRECEDENCE.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I–II–III–IV | SAMA-D000047 | Research Methodology | Authority, Evidence Custody and Source Precedence |

| Document field | Value |
|---|---|
| Purpose | Explain how SAM separates current interpretation, immutable provenance, executable evidence and narrative synthesis, then resolve disagreements without erasing the record. |
| Prerequisite documents | `SAMA-D000046` |
| Used by | `SAMA-D000048`–`SAMA-D000054` and every evidence-bearing SAMA document |

</details>
