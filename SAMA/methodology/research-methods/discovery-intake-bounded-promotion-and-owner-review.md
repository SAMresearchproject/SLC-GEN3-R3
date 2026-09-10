[SAM](../../README.md) · [Research methodology](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Discovery Intake, Bounded Promotion and Owner Review

## Conceptual abstract

Discovery and promotion are different research activities. Discovery asks what
new structure may be present. Promotion asks whether a precisely bounded piece
of that structure has acquired enough provenance, technical definition and
evidence to move into a named project surface. A valuable discovery may remain
exploratory; a promotion may carry only one narrow identity from a much larger
idea.

SAM treats promotion as a sequence of explicit state transitions. No passing
runner automatically updates current authority, no current result automatically
becomes an approved SAMA document, and no approved internal document
automatically becomes public. This separation permits fast exploration and
exact custody at the same time.

## 1. The lifecycle state machine

The complete documented route is

```text
DISCOVERY
→ SOURCE_INTAKE
→ CLAIM_AND_TYPE_TRIAGE
→ TECHNICAL_MAP
→ DECLARED_CAMPAIGN
→ EXECUTION
→ PRESERVED_OUTCOME
→ BOUNDED_CANDIDATE
→ ATOMIC_INSTALLATION
→ DOCUMENT_REVISION
→ OWNER_REVIEW
→ LIVE_PROMOTION, if authorized
→ PUBLIC_RELEASE, if authorized
```

These are states, not mandatory bureaucratic delays. A small exact identity can
move through several of them in one focused work session, provided each
transition remains visible. A large established-reference campaign may require
separate freezes, runners, independent checks and handoffs.

## 2. Discovery

### 2.1 What enters discovery

Discovery may begin from an owner association, a collaborator-derived identity,
an anomalous residual, a failed control, a cross-volume resemblance, a new
finite enumeration or an external source. The entry is allowed to be
incomplete. Its first obligation is to preserve what was actually noticed.

### 2.2 Discovery artifact

A useful discovery artifact records:

- the conceptual objects and observed association;
- its origin and date;
- the source or execution that exposed it;
- the smallest exact examples available;
- known counterexamples or open pieces; and
- what must not yet be inferred.

The artifact can be real and valuable without becoming a closed claim.

## 3. Source and provenance intake

The Courtroom discovery-intake model makes the transition explicit:

```text
exploratory artifact
→ source/provenance intake
→ claim triage
→ scoped CR test
```

The preserved Haunted House intake is a concrete illustration. It did not make
an entire PDF theorem-grade. It verified a narrow address partition and its
source bridge while retaining forbidden overclaims and open sub-readings.

### 3.1 Intake packet

For each source, record:

\[
I_s=(\text{origin},\text{path},\text{revision},\text{hash},
\text{relevant section},\text{permitted role}).
\]

The permitted role matters. A raw author note can establish conceptual origin;
it need not supply a proof. A structure-only manuscript can guide layout while
its stale claims remain barred. A result JSON can establish numbers while the
live document supplies current interpretation.

### 3.2 Intake is not validation of everything nearby

The intake question is bounded to the dependency needed for the candidate.
It does not authorize a repository-wide audit, replay of every predecessor or
promotion of adjacent claims.

## 4. Claim and type triage

Separate the discovery into atomic propositions. A useful triage table is:

| Candidate component | Type | Evidence available | Next action |
|---|---|---|---|
| exact finite identity | identity | derivation plus finite replay | register/test directly |
| proposed physical interpretation | interpretation | conceptual source only | keep open or design comparison |
| bridge between unlike types | open relation | partial route | formalize missing operator |
| external numerical contact | established-reference result | independent comparator required | freeze and test |
| implementation acceleration | computational result | same-work equality and timing | benchmark without altering model |

Triage prevents an evidence-rich narrow identity from carrying an evidence-poor
neighbor into promotion.

## 5. Technical map and campaign declaration

Apply the campaign tuple from `SAMA-D000049`:

\[
\mathcal M=(C_o,T_o,D,E,C_t,R_b,P).
\]

Then select the testing mode. A declaration or preflight should include only
what the campaign needs:

- exact scope and non-scope;
- source freeze or current-source list;
- technical definitions and derivation;
- executable question;
- controls and holdouts;
- preservation/correction rule;
- result boundary and stop point; and
- destination identity if promotion succeeds.

Clear owner direction authorizes in-scope execution. The declaration is a
technical alignment surface, not a second approval token.

## 6. Preflight as a bounded contract

The preserved three-record promotion preflight demonstrates a precise campaign
contract. It identified:

- exactly three new destination records;
- the source repositories and frozen manifest;
- pre-existing dirty-worktree material to preserve and exclude;
- non-colliding record numbers;
- explicit non-scope, including no full repository reanalysis and no source
  mutation;
- precommit/hash-before-runner requirements; and
- preserved boundaries and failures.

The important derivation is:

```text
candidate pieces already exist
→ choose exact promotion units
→ freeze only their permitted sources
→ declare destination and non-scope
→ precommit each executable predicate
→ run and preserve
```

The campaign did not treat promotion as “copy the latest attractive prose.” It
rebuilt a source-bound test route for each atomic unit.

## 7. Execution and preservation gate

At execution, every material branch is retained:

\[
E\to
\begin{cases}
Y_{\rm concept}, & \text{predicate evaluated},\\
Y_{\rm implementation}, & \text{implementation fault},\\
Y_{\rm unresolved}, & \text{resource or dependency limit}.
\end{cases}
\]

The applicable branch determines the successor action. The CR281 lookup repair
is a preserved implementation correction. A failed mathematical candidate
would require a changed route or result boundary and therefore a separately
named successor.

## 8. Bounded candidate promotion

A candidate is promotion-ready when the active campaign's own gate is met. A
general form is

\[
G_{\rm campaign}
=G_{\rm source}
\land G_{\rm type}
\land G_{\rm execution}
\land G_{\rm controls}
\land G_{\rm preservation}
\land G_{\rm boundary}.
\]

The meaning of each (G) is campaign-specific. An exploratory identity may
need exact symbolic reduction and counterexample search. An observational
holdout may need a source freeze, no-fit declaration and comparator audit. A
performance claim may need same-work equality before timing.

There is no universal numerical threshold and no automatic requirement that a
prior campaign's independent lane be reproduced for an unrelated exploratory
question.

### 8.1 Promotion unit

Promote the smallest unit justified by the evidence. If an intake artifact
contains one exact address identity and five untested interpretations, promote
the identity and preserve the interpretations as open. This creates a strong
foundation for later work without shrinking the successful result.

### 8.2 Promotion result

The three-record campaign completed all three bounded records and validated
its precommits, runners, JSON artifacts, hashes and source freeze. It also
retained named open items. Those opens are part of the promoted boundary, not
defects to be removed from the report.

## 9. Atomic installation before prose

SAMA uses record-first installation:

```text
promoted candidate statement
→ one or more atomic SAMA records
→ registered document structure
→ standard document prose
→ parent manuscript synthesis
```

An atomic record states one definition, identity, route, result, failure or open
relation and cites its exact sources. The document catalog then resolves which
records and tests belong to each chapter. This order prevents polished prose
from becoming the only place where a claim exists.

## 10. Mechanical validation

Builders can establish:

- JSON/schema validity;
- unique IDs and graph integrity;
- resolvable source-record and test keys;
- deterministic content hashes;
- document hierarchy consistency;
- exact approval-field consistency; and
- generated index reproducibility.

Let

\[
V_m\in\{0,1\}
\]

denote mechanical validity. A value \(V_m=1\) means the artifact satisfies its
machine contract. It does not set the owner-review state.

## 11. Owner review

Only Sean Brady may set `reviewed_and_approved: true` for an exact SAMA record
or document revision. Review binds to a content hash:

\[
A_o=(\text{Sean Brady},\text{date},\operatorname{SHA256}(F)).
\]

Therefore

\[
V_m=1\not\Rightarrow A_o,
\qquad
A_o(F)\not\Rightarrow A_o(F'),\quad F'\ne F.
\]

A revised approved document becomes a new unapproved revision until explicitly
reviewed. This preserves the meaning of owner approval without slowing internal
drafting or mechanical validation.

## 12. Current-authority and publication transitions

After owner review, two further transitions may or may not occur:

1. **Live promotion:** create the numbered history entry and replace the
   affected present-tense live statement when authorized.
2. **Public release:** export or publish the authorized exact content when
   separately authorized.

Neither transition is implied by a passing campaign. Internal research can be
complete and preserved while live/public state remains unchanged.

## 13. Promotion failure and return routes

If a gate fails, route the candidate according to the failure:

| Failed gate | Return route |
|---|---|
| Source | recover provenance or keep the claim open |
| Type | refine the technical map; do not invent a bridge |
| Execution | repair implementation or record resource limit |
| Control | strengthen discriminator or narrow the claim |
| Preservation | reconstruct custody before promotion |
| Boundary | split the candidate into supported and open units |

The candidate returns to discovery or technical development with its evidence
intact. Promotion failure is not deletion.

## 14. Current boundaries

This methodology does not automatically promote the present four volumes.
They remain `reviewed_and_approved: false` through construction, validation and
handoff. Their source spines and Courtroom repository remain immutable. Any
later approval, live installation or public export requires its own explicit
transition.

## 15. Related SAMA documents

`SAMA-D000048` selects testing mode. `SAMA-D000049` supplies the technical map.
`SAMA-D000050` and `SAMA-D000051` govern controls and preservation.
`SAMA-D000052` supplies result language. `SAMA-D000054` carries an exact
candidate through retrieval, compaction, handoff and publication boundaries.

## Test and result index

| Test record key | Role | Source result/status | Result artifact | Test folder |
|---|---|---|---|---|
| [`LC:LC00`](../../tests/courtroom/16-the-last-campaign/README.md) | Example of a campaign-specific locked-replay charter | Charter; no scientific verdict assigned | [LC00 charter](../../courtroom/16_THE_LAST_CAMPAIGN/LC00_THE_LAST_CAMPAIGN_CHARTER.md) | [Last Campaign folder](../../courtroom/16_THE_LAST_CAMPAIGN) |
| [`LC:LC01`](../../tests/courtroom/16-the-last-campaign/README.md) | Primitive/source/control lock that begins the replay rather than pre-assigning downstream outcomes | Historical lock result | [LC01 result](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_result.md) | [Last Campaign folder](../../courtroom/16_THE_LAST_CAMPAIGN) |

## Atomic SAMA source records

| Record ID | Role in this document |
|---|---|
| `SAMA-C000018-R001` | Full discovery-to-promotion lifecycle. |
| `SAMA-C000019-R001` | Separation of mechanical validation and owner approval. |
| `SAMA-C000024-R001` | Campaign-specific promotion gates. |
| `SAMA-C000025-R001` | Separation of internal result, revision, approval, live authority and publication. |

## External references

- [Pinned discovery-intake branch](../../courtroom/17_DISCOVERY_INTAKE/README.md)
- [Pinned three-record preflight](../../courtroom/SAM_THREE_CR_PROMOTION_PREFLIGHT.md)
- [Pinned three-record result](../../courtroom/SAM_THREE_CR_PROMOTION_RESULT.md)
- [SAMA Constitution](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/ATLAS_CONSTITUTION.md)

## Revision and approval

This exact revision has `reviewed_and_approved: false` until Sean Brady
explicitly approves it.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`LC:LC00`](../../tests/courtroom/16-the-last-campaign/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign/README.md) | [All files](../../tests/courtroom/16-the-last-campaign/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign/README.md) | [All 164 files](../../tests/courtroom/16-the-last-campaign/README.md) |
| [`LC:LC01`](../../tests/courtroom/16-the-last-campaign/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign/README.md) | [LC01_primitive_stack_lock_runner.py](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_primitive_stack_lock_runner.py) | [LC01_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_wrong_controls.csv)<br>[LC01_wrong_controls.csv.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_wrong_controls.csv.sha256.txt) | [LC01_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_result.md)<br>[LC01_result.md.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_result.md.sha256.txt)<br>[LC01_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_summary.json)<br>[LC01_summary.json.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_summary.json.sha256.txt) | [All 164 files](../../tests/courtroom/16-the-last-campaign/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000053`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/DISCOVERY_INTAKE_BOUNDED_PROMOTION_AND_OWNER_REVIEW.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I–II–III–IV | SAMA-D000053 | Research Methodology | Discovery Intake, Bounded Promotion and Owner Review |

| Document field | Value |
|---|---|
| Purpose | Develop the full lifecycle from exploratory discovery through source intake, scoped testing, candidate promotion, atomic/document installation, explicit owner review and separately authorized current/public transitions. |
| Prerequisite documents | `SAMA-D000052` |
| Used by | `SAMA-D000054`, every campaign handoff, and the four-volume assembly process |

</details>
