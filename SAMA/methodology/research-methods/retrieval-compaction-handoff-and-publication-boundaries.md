[SAM](../../README.md) · [Research methodology](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Retrieval, Compaction, Handoff and Publication Boundaries

## Conceptual abstract

Large research programs lose reliability when context recovery becomes either
guesswork or an unbounded re-audit. SAM uses bounded retrieval: recover the
controlling declaration, global live hub, one relevant live domain and only the
direct sources required by the task. If a material dependency remains absent,
request a compact source packet rather than reconstructing the entire
repository.

The same boundedness governs handoff and publication. A handoff identifies exact
content, hashes, current open items and the next authorized action. It does not
silently approve, promote or publish the work. These separations let successive
agents continue one research chain without treating every context boundary as a
new investigation.

## 1. The continuity problem

A continuation agent must answer two questions:

1. What is the present authorized state relevant to this task?
2. Which exact sources are needed to continue the unfinished derivation?

Reading too little risks stale assumptions. Reading everything risks replacing
the immediate task with a new audit and gives historical prose accidental
authority. The recovery rule is therefore an ordered stopping algorithm.

## 2. Bounded recovery algorithm

At a substantial task start or after compaction:

```text
1. Read repository rules and the controlling declaration.
2. Read SAM_LIVE/00_CURRENT.md.
3. Read exactly one relevant live domain document.
4. Follow only the directly cited history/result sources needed by the task.
5. Stop when the dependency is resolved.
```

Formally, let \(S_0\) be the required authority set and \(q\) the unresolved
task dependency. Define successive source sets \(S_1,S_2,\ldots\) only while

\[
q\notin\operatorname{closure}(S_i)
\]

and the next source is directly routed by current authority. Once (q) is
resolved, expansion stops. This is not a mathematical closure proof; it is an
operational rule against uncontrolled context growth.

## 3. Retrieval firewall

The following are not automatically authorized by missing context:

- repository-wide grep campaigns;
- full branch reconstruction;
- hash audits of completed sources;
- rerunning historical tests;
- mathematical revalidation of current live statements; or
- opening unrelated campaign families.

Completed artifacts are project inputs. They are reopened only for a concrete
dependency or a task-relevant contradiction.

## 4. SAM retrieval request

If bounded authority does not contain the needed fact, issue a focused request:

```text
SAM RETRIEVAL REQUEST
Question: <exact missing information>
Why needed: <current task dependency>
Concept anchors: <memorable terms, equations, branches or associations>
Current authority already read: <live documents or entry IDs>
Desired return: compact source directory/index with current authority,
                direct paths, relevant sections and read order
Do not do: mathematical revalidation, new tests or unrelated repo audit
```

The request asks for provenance recovery, not for the owner to reconstruct
technical paths from memory. When a numbered retrieval packet returns, read its
index and only the sources it identifies.

## 5. Compaction continuity

Context compaction should preserve a live work state rather than a narrative of
everything ever read. A high-quality continuation summary includes:

- current user objective and exact stop condition;
- negative-drift and owner-disclosure obligations;
- current plan with completed/in-progress/pending steps;
- files created or edited and their roles;
- validation results and exact unresolved failures;
- immutable sources and user-owned dirty-worktree boundaries;
- active agent ownership; and
- the next concrete action.

It should not instruct the next agent to restart completed validation or infer
that an unfinished artifact is complete.

## 6. Exact handoff packet

A terminal internal handoff for a volume or campaign should contain:

| Handoff field | Required content |
|---|---|
| Objective | Exact campaign or manuscript burden completed |
| Content manifest | Paths, revisions, byte counts and SHA-256 values |
| Source custody | Source repository state, paths, hashes and immutable boundaries |
| Evidence map | Atomic records and exact qualified test keys reached by each document |
| Validation | Commands, versions, pass/fail outputs and preserved failures |
| Current state | Approved/unapproved, live/non-live, public/non-public |
| Named opens | Specific unresolved relations or missing evidence routes |
| Next authority | What action requires owner direction |

The handoff itself should be hashable. If content changes after handoff, issue a
new manifest instead of claiming the prior receipt still covers it.

## 7. Current, review and publication as distinct states

For an artifact (F), define the state vector

\[
\Sigma(F)=(I,C,A,L,P),
\]

where

- (I): internally complete;
- (C): cataloged/installed in SAMA;
- (A): explicitly owner-approved;
- (L): installed as current live authority; and
- (P): publicly released.

These bits do not imply one another except through an explicit authorized
transition. A typical new manuscript can be

\[
\Sigma(F)=(1,1,0,0,0),
\]

meaning complete and cataloged, but unapproved, non-live and non-public. This
is a valid terminal internal state.

### 7.1 Approval transition

Approval binds Sean Brady's explicit review to an exact content hash. It does
not follow from polish, length, source completeness or builder success.

### 7.2 Live-authority transition

When authorized, create the next immutable history entry, replace the affected
live section, update the history index and validate the graph. Do not append a
chronological stream to a live document.

### 7.3 Publication transition

Publication requires an explicitly selected public surface and exact content.
Internal source paths, open research artifacts and unapproved drafts are not
silently exported merely because they are linked by SAMA.

## 8. Source immutability across handoff

The new volumes are successors assembled from immutable technical spines and
Courtroom evidence. Their construction must not edit those sources. Baseline
and final custody hashes make this check executable:

\[
H_{\rm before}(S)=H_{\rm after}(S)
\]

for every source artifact (S) declared immutable. New prose and registries
live in successor SAMA paths and carry their own hashes.

## 9. Dirty-worktree custody

Pre-existing modifications belong to the owner unless the task says otherwise.
A handoff records the starting dirty set and isolates campaign-owned changes.
It does not revert unrelated files or claim them as new work. If a required file
overlaps owner work, the conflict is surfaced narrowly.

## 10. Publication-ready does not mean approved

A document may be technically publication-ready—complete prose, citations,
indexes, hashes and deterministic builders—while `reviewed_and_approved` remains
false. This wording is precise: readiness describes artifact quality; approval
describes an owner action. The handoff should state both.

## 11. Current boundaries

This document does not authorize any remote import, push, live-pointer change
or public release. It specifies how those transitions are recorded when they
are separately authorized. The present four-volume build terminates at an
unapproved exact-hash handoff.

## 12. Related SAMA documents

`SAMA-D000047` supplies authority and source precedence. `SAMA-D000053` supplies
the discovery/promotion state machine. `SAMA-D000046` ensures contributor
attribution survives compaction and handoff.

## Test and result index

No scientific test defines the bounded recovery and handoff protocol. Its
authority is carried by repository contracts and the atomic records below.

## Atomic SAMA source records

| Record ID | Role in this document |
|---|---|
| `SAMA-C000012-R001` | Live/history distinction used during recovery and installation. |
| `SAMA-C000020-R001` | Bounded recovery and retrieval-request route. |
| `SAMA-C000023-R001` | Source precedence when recovered layers disagree. |
| `SAMA-C000025-R001` | Separate internal, revision, approval, live and publication transitions. |

## External references

- [Repository recovery and retrieval rules](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/AGENTS.md)
- [SAM retrieval system](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/SAM_RETRIEVAL/README.md)
- [SAMA document contract](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/DOCUMENT_SYSTEM.md)
- [SAMA Constitution](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/ATLAS_CONSTITUTION.md)

## Revision and approval

This exact revision has `reviewed_and_approved: false` until Sean Brady
explicitly approves it.

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000054`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/RETRIEVAL_COMPACTION_HANDOFF_AND_PUBLICATION_BOUNDARIES.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I–II–III–IV | SAMA-D000054 | Research Methodology | Retrieval, Compaction, Handoff and Publication Boundaries |

| Document field | Value |
|---|---|
| Purpose | Preserve conceptual and technical continuity through bounded source recovery, context compaction and exact-hash handoff while keeping internal work, current authority, approval and publication separate. |
| Prerequisite documents | `SAMA-D000053` |
| Used by | All parent manuscripts, continuation agents, owner-review packets and any future publication assembly |

</details>
