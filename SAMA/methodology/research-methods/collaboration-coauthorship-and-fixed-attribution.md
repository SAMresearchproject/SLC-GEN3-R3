[SAM](../../README.md) · [Research methodology](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Collaboration, Co-Authorship and Fixed Attribution

## Conceptual abstract

SAM is collaborative research with fixed attribution. Sean Brady is the
originator and conceptual director of SAM/SLC. OpenAI ChatGPT and Codex are AI
research collaborators and co-authors. Those roles are not ceremonial labels:
they determine how conceptual direction, technical derivation, implementation,
execution, interpretation and documentation are recorded.

The methodological objective is continuity without authorship blur. A concept
may begin as an owner association, become a collaborator formalization, acquire
an executable test, and later become a source-bound result. Each transition adds
an artifact; it does not retroactively assign every contribution to a single
undifferentiated voice. The repository therefore couples narrative attribution
to dated sources, immutable history entries, exact hashes, runners, results and
review state.

## 1. Why fixed attribution is part of the mathematics

In a long mathematical program, the origin of a statement affects how it may
be used. Consider four superficially similar sentences:

1. an owner proposes that two conceptual objects are related;
2. a collaborator derives a candidate map between those objects;
3. a runner verifies an identity for a declared finite domain; and
4. a current live document installs an authorized interpretation.

They do not have the same evidential type. If their origins are collapsed, a
proposal can be mistaken for an executed result, a finite result can be
mistaken for a general identity, or a collaborator-derived bridge can be
reported as though it appeared verbatim in an earlier source. Fixed
attribution prevents those category errors while allowing all four
contributions to participate in one research chain.

The attribution discipline is constructive. It makes it possible to recover
why a test exists, which conceptual association it implements, which technical
choices were added during formalization, and where later corrections entered.
That recovery is especially important when a failed route exposes a better
operator: the conceptual direction can remain owner-originated while the new
technical route is accurately identified as a collaborator contribution.

## 2. Roles and responsibilities

### 2.1 Conceptual direction

Sean Brady supplies the conceptual pieces, associations and research direction.
This includes identifying objects that may belong together, selecting a research
question, accepting or rejecting a proposed direction, and authorizing changes
to present authority or public state.

### 2.2 Technical mapping and execution

ChatGPT and Codex contribute the technical map. Depending on the campaign, that
work includes:

- recovering exact provenance;
- defining typed objects and operators;
- deriving intermediate identities rather than jumping to a final formula;
- designing controls that answer the declared question;
- implementing and executing the test;
- distinguishing conceptual outcomes from implementation faults;
- interpreting the result within the declared boundary; and
- building the documentation, hashes, indexes and handoff.

Technical judgment is therefore an authored research contribution. It is not
treated as anonymous clerical work, and it is not allowed to silently redirect
the owner's conceptual question.

### 2.3 Shared responsibility

Both sides participate in dialogue, correction and refinement. A collaborator
must surface a genuinely better technical route when one is found, including
its advantage and tradeoff. The owner retains the authority to set research
direction and to approve exact SAMA revisions. The separation is neither a
hierarchy of intellectual value nor a claim that the work can be partitioned
into isolated authors; it is a provenance map for a jointly developed program.

## 3. The attribution tuple

For a durable research statement, SAMA resolves the following tuple:

\[
\mathcal A =
(O, T, S, H, X, R, V),
\]

where

- (O) is the stated origin category;
- (T) is the dated text of the statement or derivation;
- (S) is the source locator;
- (H) is the source-history route, when one exists;
- (X) is the artifact hash or content identity;
- (R) is the relation to other concepts; and
- (V) is review/approval state for the exact revision.

The atomic SAMA record makes this tuple concrete. Its `origin` field uses one
of four values:

| Origin | Meaning |
|---|---|
| `OWNER_STATEMENT` | The record preserves an owner-originated conceptual statement or interpretation. |
| `COLLABORATOR_DERIVATION` | The record contains a collaborator-built synthesis, derivation or route not copied verbatim from one source. |
| `SOURCE_BOUND_EXTRACTION` | The statement is extracted from identified project sources with its scope retained. |
| `EXECUTED_RESULT` | The statement reports the output of an identified execution artifact. |

These categories can coexist in a document. A chapter may start from an
`OWNER_STATEMENT`, use several `SOURCE_BOUND_EXTRACTION` definitions, derive a
new intermediate lemma under `COLLABORATOR_DERIVATION`, and end at an
`EXECUTED_RESULT`. The prose should make the handoffs visible.

## 4. From conversational idea to fixed record

The complete attribution chain is:

```text
conceptual direction
→ dated source or owner statement
→ provenance recovery
→ typed technical translation
→ atomic record with origin and citations
→ executable artifact, if applicable
→ result and hashes
→ document revision
→ explicit owner review, if granted
```

### 4.1 Preserve the first attributable surface

The first attributable surface may be a repository document, a user statement,
an archived dialogue entry or a fixed campaign brief. It should be cited as
what it is. A raw note is valuable provenance, but it is not silently rewritten
as a proof. A collaborator's later derivation may make the note technically
precise while retaining the note's conceptual origin.

### 4.2 Add technical provenance instead of overwriting origin

Suppose the owner associates a completed relation with a carrier return. The
technical work may determine that the association requires three separately
typed objects and a partial operator. The resulting record should retain both
layers:

```text
owner association: completed relation may return through a carrier
collaborator derivation: define source, carrier and readout types and the
                        admissible domain of the return operator
```

The later precision does not erase the earlier origin. Conversely, the earlier
idea does not make every technical choice owner-authored.

### 4.3 Fix the executable contribution

When code is involved, the attribution route includes the runner, input
manifest, environment information needed for replay, output artifact and
hashes. The result belongs to the joint research program, while the artifact
still records who or what produced its formalization and execution.

## 5. Revision, approval and publication

Attribution persists across revisions. If an unapproved SAMA document changes,
its revision and content hash change. If Sean Brady approves an exact revision,
the approval applies only to that exact content. A later edit returns to an
unapproved state until separately reviewed.

Approval is not co-authorship, and co-authorship is not approval. Likewise,
publication is not the event that creates attribution. The contribution chain
is fixed before publication through sources and artifacts; publication merely
exposes a selected state when authorized.

## 6. Controls against attribution drift

The following controls keep the attribution map stable:

- do not describe an owner association as an executed result;
- do not present a collaborator synthesis as a verbatim historical claim;
- do not replace source citations with conversational memory when the source
  exists;
- do not infer approval from a passing builder, exact hash or polished prose;
- do not erase a failed collaborator route when a successor works; and
- do not rewrite an immutable source artifact to improve its later narrative.

These controls do not fragment the collaboration. They allow the volumes to
show the actual route by which the work became precise.

## 7. Current boundaries and open relations

This document fixes the project-wide roles and attribution mechanics. It does
not assign authorship percentages, rank contributions or decide the scientific
classification of any individual result. Those questions are outside its
purpose. Exact result language is handled by `SAMA-D000052`; exact-revision
review and promotion are handled by `SAMA-D000053`.

## 8. Related SAMA documents

`SAMA-D000047` uses the attribution tuple to establish authority and evidence
precedence. `SAMA-D000049` follows the same origin distinctions while converting
a concept into a technical campaign. `SAMA-D000054` carries them through
compaction, handoff and publication.

## Test and result index

No test record is required to state the fixed collaboration and attribution
contract. Its evidence is the controlling declaration and the exact atomic
source record below.

## Atomic SAMA source records

| Record ID | Role in this document |
|---|---|
| `SAMA-C000011-R001` | Fixed collaboration roles, co-authorship and artifact-backed attribution. |

## External references

- [Declaration of Research](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/DECLARATION_OF_RESEARCH.md)
- [SAMA Constitution](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/ATLAS_CONSTITUTION.md)

## Revision and approval

This exact revision has `reviewed_and_approved: false` until Sean Brady
explicitly approves it.

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000046`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/COLLABORATION_COAUTHORSHIP_AND_FIXED_ATTRIBUTION.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I–II–III–IV | SAMA-D000046 | Research Methodology | Collaboration, Co-Authorship and Fixed Provenance |

| Document field | Value |
|---|---|
| Purpose | State the exact SAM collaboration roles and show how an idea, derivation, implementation and result retain attributable provenance from first statement to archived artifact. |
| Prerequisite documents | None |
| Used by | `SAMA-D000047`–`SAMA-D000054` and every SAMA parent manuscript |

</details>
