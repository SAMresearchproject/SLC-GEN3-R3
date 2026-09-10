[SAM](../../README.md) · [Research methodology](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Concept-to-Technical Campaign Translation

## Conceptual abstract

A concept is not made technical by attaching a formula to it. The technical map
must identify the objects, their types, admissible operators, executable
question, controls, evidence surface and result boundary. Each stage should be
explained as it is built so that a reader can see why the eventual formula or
runner answers the original conceptual question.

This method is the bridge between Sean Brady's conceptual direction and the
formal, computational and documentary work contributed by the collaborators.
It gives the research room to discover new operators while preventing prompt
shorthand, implementation convenience or familiar external formulas from
silently changing the intended object.

## 1. The campaign map

For a bounded campaign define

\[
\mathcal M=(C_o,T_o,D,E,C_t,R_b,P),
\]

where

- \(C_o\): conceptual objects and their intended relation;
- \(T_o\): technical objects and types;
- \(D\): derivation from \(C_o\) to \(T_o\);
- \(E\): executable question and finite or symbolic domain;
- \(C_t\): controls and diagnostic alternatives;
- \(R_b\): result boundary and classification rule; and
- \(P\): provenance, artifacts and preservation route.

The tuple is not an approval form. It is a shared technical map used whenever
making the objects explicit improves the work.

## 2. Stage 1 — recover the conceptual objects

Begin with the owner's immediate objective and the current authority for the
relevant domain. Extract the nouns and relations before choosing equations.
For example:

```text
conceptual nouns: source, carrier, completed write, readout
conceptual relation: a completed write returns through a carrier to a readout
```

At this stage, do not collapse the four nouns into one scalar merely because a
candidate source happens to give them numerical values. The conceptual map is
the first type firewall.

Record:

- what each object means in the project;
- which relations are asserted, suggested or still open;
- which earlier source or owner statement establishes that meaning; and
- which neighboring concepts are explicitly outside the campaign.

## 3. Stage 2 — translate objects into mathematical types

Assign each conceptual object a technical type. A minimal type table might be:

| Concept | Technical type | Domain | Codomain or output |
|---|---|---|---|
| source | finite ledger or field source | source rows | source strength |
| carrier | typed transport object | closed writes | compressed support |
| readout | operator | field or ledger | observable scalar/tensor |
| completed write | state transition plus receipt | admissible state | new state and immutable receipt |

The type assignment determines which compositions are legal. If
\(K:W\to S\) is a carrier compression and \(A:S\to F\) is an accumulation
lift, then \(A\circ K:W\to F\) is meaningful. The expression \(K+A\) is not
automatically meaningful because its terms have different domains and roles.

This is where many useful deviations are found. A failed direct bridge may not
mean the concepts are unrelated; it may show that the missing intermediate
type is load-bearing.

## 4. Stage 3 — derive the candidate route

Write every intermediate map, constant and normalization in causal order:

\[
C_o
\xrightarrow{\text{typing}}T_1
\xrightarrow{f_1}T_2
\xrightarrow{f_2}\cdots
\xrightarrow{f_n}Y.
\]

For each arrow answer:

1. What does the map do conceptually?
2. What is its mathematical definition?
3. Which source fixes it?
4. What units or normalization apply?
5. What domain restrictions make it valid?
6. What tempting alternative does it exclude?

Do not begin the manuscript at \(Y=f_n\circ\cdots\circ f_1(C_o)\). The chain
of arrows is the explanation.

### 4.1 Constants and coefficients

Every coefficient should be derived or explicitly sourced. If

\[
k=\frac{(R-1)(F-1)}{D2^S},
\]

the reader should be shown the meaning of (R,F,D,S), their substitution,
the arithmetic and the role of (k) in the next map. A coefficient fitted to
an external dataset must be typed differently from one derived from a locked
primitive stack.

### 4.2 Exact versus approximate maps

Mark whether an arrow is an identity, a finite enumeration, a numerical
approximation, a comparator, an interpretation or an open relation. A
high-precision numerical equality is not silently renamed an algebraic proof;
an exact finite identity is not weakened into a vague resemblance.

## 5. Stage 4 — formulate the executable question

The executable question converts the derivation into a predicate or measured
output. A useful form is

\[
Q(x)=
\begin{cases}
1,&\text{if all declared identities, invariants and gates hold for }x,\\
0,&\text{otherwise.}
\end{cases}
\]

For a dataset (X), specify whether the result requires

\[
\forall x\in X:\ Q(x)=1,
\]

a declared aggregate statistic, or comparison with a fixed target. Name the
domain (X), row count, selection rule and omissions before execution when
they affect the result.

For an open mathematical route, the executable question may instead seek a
counterexample, sign pattern, factorization, rank, symbolic reduction or
boundary cell. The question should still be concrete enough that the output
changes the state of knowledge.

## 6. Stage 5 — derive controls from failure modes

Controls follow from the maps, not from a universal checklist. For each
load-bearing arrow \(f_i\), ask what would happen if it were:

- removed;
- replaced by a nearby but differently typed operator;
- supplied target information it should not see;
- evaluated on a held-out domain;
- subjected to a sign, coefficient or normalization mutation; or
- bypassed by an implementation shortcut.

The resulting control matrix is developed fully in `SAMA-D000050`.

## 7. Stage 6 — precommit, implement and execute

When the testing mode calls for a freeze, serialize the campaign map before the
runner sees the result. The implementation should then expose:

- exact input locators and hashes;
- the formula or algorithm manifest;
- environment and precision needed for replay;
- deterministic output paths;
- checks and tolerances;
- control outputs; and
- an append-only failure/correction trail.

Implementation must follow the technical definition, not copy ambiguous prompt
shorthand. A runner that cannot state which typed map it implements is not yet
the executable form of the concept.

## 8. Stage 7 — interpret within the result boundary

Interpretation runs backward through the map:

```text
runner output
→ executable predicate or statistic
→ tested technical relation
→ scoped conceptual question
→ authorized result classification, if assigned
```

If the run fails, identify the first broken arrow. It may be a conceptual
falsification, a boundary-domain counterexample, an implementation defect or an
unresolved dependency. Preserve the exact outcome and resist replacing it with
a broader philosophical caveat.

## 9. Stage 8 — install the evidence route

After execution, register the atomic result or boundary before drafting the
final synthesis. Link the claim to the result artifact and folder, then build
the document from its atomic units. If current authority changes, create the
numbered history entry and replace the affected live statement. Owner approval
and publication remain separate transitions.

## 10. Current boundaries

The campaign map does not require every idea to become executable immediately.
A conceptual relation may remain explicitly open after its types and missing
operator are identified. That is useful technical progress and should be
recorded as an open relation rather than filled with an invented bridge.

## 11. Related SAMA documents

The testing mode comes from `SAMA-D000048`. Control construction is developed
in `SAMA-D000050`. Failure preservation is developed in `SAMA-D000051`, and
promotion/install transitions in `SAMA-D000053`.

## Test and result index

No single test defines this cross-campaign translation method. Each volume
chapter instantiates the method with its own indexed evidence.

## Atomic SAMA source records

| Record ID | Role in this document |
|---|---|
| `SAMA-C000014-R001` | Source-bound concept-to-technical campaign map and collaborator responsibility. |

## External references

- [Repository collaboration and campaign rules](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/AGENTS.md)
- [Hybrid campaign review template](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/SAM_REVIEW/templates/HYBRID_CONCEPT_TECHNICAL_CAMPAIGN_REVIEW_TEMPLATE.md)

## Revision and approval

This exact revision has `reviewed_and_approved: false` until Sean Brady
explicitly approves it.

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000049`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/CONCEPT_TO_TECHNICAL_CAMPAIGN_TRANSLATION.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I–II–III–IV | SAMA-D000049 | Research Methodology | Concept-to-Technical Campaign Translation |

| Document field | Value |
|---|---|
| Purpose | Walk a SAM concept from owner-directed meaning through typed formalization, executable construction, controls, result interpretation and preserved evidence. |
| Prerequisite documents | `SAMA-D000048` |
| Used by | Every technical chapter and campaign; directly by `SAMA-D000050` and `SAMA-D000053` |

</details>
