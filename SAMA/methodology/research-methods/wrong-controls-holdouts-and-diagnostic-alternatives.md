[SAM](../../README.md) · [Research methodology](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Wrong Controls, Holdouts and Diagnostic Alternatives

## Current research connections — 14 September 2026

The global execution authority is SLC-GEN3-R3 / SLC-GEN3-CEV1-R3. The September 2026 research includes exact retained-history computation, RH arithmetic compensation, native Mersenne work, Starbreaker signed reception and ATOM3D contact/grammar. The research index connects the retained derivations to the latest code, results and current domain assignments.

[Current derivations, code and results](../../../docs/RESEARCH.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

A wrong control is not a careless calculation retained for decoration. It is a
deliberately inapplicable mutation, conflation, leakage route or alternative
operator chosen because its behavior distinguishes the intended construction.
When it fails in the declared way, it reveals what is load-bearing. When it
unexpectedly succeeds, it exposes non-uniqueness, leakage or an incomplete test.

Controls therefore participate in derivation. They answer “why this route?”
alongside the main formula. A holdout answers a different question: whether a
fixed route transfers to information that did not select it. The two are most
useful when their roles are named before result interpretation.

## 1. Four control types

Let \(F:X\to Y\) be the intended technical construction and \(M_j\) a declared
mutation. SAM distinguishes four recurring control roles.

| Control type | Construction | Question |
|---|---|---|
| Invariance control | Apply a transformation that should leave \(F\) unchanged | Does the implementation preserve the claimed invariant? |
| Wrong control | Replace a load-bearing map with \(M_j\) | Does the test distinguish the intended operator from a tempting wrong one? |
| Null or negative control | Use input outside the mechanism's activating condition | Does the output remain absent where the concept says it should? |
| Holdout | Evaluate the fixed \(F\) on independently withheld \(X_h\) | Does the construction transfer without result-driven selection? |

One campaign may use all four, but no mechanical roster is mandatory. The
controls should answer the actual question.

## 2. Deriving a wrong control

Start from the route

\[
X\xrightarrow{f_1}T_1\xrightarrow{f_2}T_2
\xrightarrow{f_3}Y.
\]

Suppose \(f_2\) is the proposed carrier compression. Three diagnostic
mutations are immediately available:

\[
M_1=f_3\circ f_1
\quad\text{(skip the carrier)},
\]

\[
M_2=f_3\circ g_2\circ f_1
\quad\text{(replace it with a nearby operator)},
\]

and

\[
M_3=f_3\circ f_2\circ \ell\circ f_1
\quad\text{(leak forbidden target information through }\ell\text{)}.
\]

Each mutation tests a different causal claim. If \(M_1\) performs as well as
the intended route, compression may not be load-bearing. If \(M_2\) also works,
the test may establish a family rather than a unique operator. If \(M_3\) is
the only successful route, the apparent contact is contaminated by leakage.

## 3. Wrong controls in locked replay

The Last Campaign registers 30 standing wrong controls. They are derived from
ways a downstream replay could appear to succeed while mutating the locked
primitive stack.

### 3.1 Primitive and formula mutations

`WC01`, `WC02`, `WC06`, `WC07` and `WC16` cover changing global primitives,
allowing branch-local overrides, patching formulas, restoring a rejected old
route or adding a hidden correction term. Their common logic is:

```text
source chain fixes primitive/formula
→ downstream lane declares its manifest
→ result is computed
→ no post-result change may be called a replay
```

If a mutation is scientifically useful, it becomes a separately named
successor candidate rather than being smuggled into the locked lane.

### 3.2 Target and selection leakage

`WC03`, `WC14`, `WC15`, `WC20`, `WC21`, `WC22` and `WC25` cover target-value
substitution, in-sample rescue, tolerance expansion, nearest-row assignment,
row suppression, data backfill and favorable-bin selection. These controls
protect the direction of information flow:

\[
\text{source and selector}\longrightarrow\text{prediction}
\longrightarrow\text{comparison},
\]

not

\[
\text{target}\longrightarrow\text{selector or formula}
\longrightarrow\text{reported match}.
\]

### 3.3 Type conflations

`WC08` rejects direct \(q_A\)-as-observed-mass identification. `WC09` rejects
promoting the 18-channel carrier to rest matter. `WC10` and `WC18` keep the
\(1/8\) carrier side, \(3/4\) surface debit and \(9/16\) half-bounce separate.
These are not arbitrary perturbations; they are tests of the typed distinctions
on which later derivations depend.

### 3.4 Application-specific mutations

Lane controls target the actual application: refitting \(D\) in a distance
road, patching Born normalization, softening the \(A=1\) closure boundary, or
fitting thermodynamic coefficients to external targets. A useful wrong control
is close enough to be tempting and different enough to test the mechanism.

## 4. Holdouts and independence

A holdout set \(X_h\) is informative only relative to a selection history.
Define

\[
I_{\rm select}=\{\text{all information used to choose }F\}.
\]

The holdout condition is not merely \(X_h\cap X_{\rm train}=\varnothing\).
It requires that target-bearing information from \(X_h\) not enter
\(I_{\rm select}\) through labels, preprocessing, threshold choice, row
selection or narrative tuning.

For reciprocal pairs or graph relations, rowwise splitting may leak the same
underlying relation into both sides. The grouping unit must match the object of
independence. For a physics comparison, provenance and measurement uncertainty
must travel with the holdout values.

## 5. Reading control outcomes

The main and control outputs should be interpreted as a pattern:

| Main route | Wrong control | Reading |
|---|---|---|
| works | rejects | Evidence isolates the declared distinction. |
| works | also works | The route may be non-unique or the test insufficiently separating. |
| fails | rejects | The intended mechanism fails under scope; the control still confirms the test can distinguish routes. |
| fails | also fails | Inspect whether both share a missing dependency or implementation defect. |

“Works” and “fails” in this table are local predicates, not replacement SAM
classifications. The scientific result still uses the exact three-class
contract when assigned.

## 6. Unexpectedly successful wrong controls

A wrong control that succeeds is a result, not an inconvenience. Preserve it
and ask which of three cases applies:

1. **Non-uniqueness:** multiple operators realize the scoped behavior.
2. **Leakage:** the control accesses information that makes the result circular.
3. **Weak discriminator:** the output statistic cannot distinguish the routes.

The correction is a new diagnostic or a narrower result boundary. It is not to
delete the control or rename it after seeing the output.

## 7. Implementation controls

Controls can also isolate code from concept:

- independent arithmetic for a key identity;
- route-equivalent exact algorithms that must produce the same tensor;
- serialization round trips;
- deliberate malformed inputs;
- hash verification before and after execution; and
- a known small case with analytically computed output.

If these fail while the conceptual predicate was never reached, the event is an
implementation fault. It remains part of the record and receives the repair
route in `SAMA-D000051`.

## 8. Current boundaries

Controls do not manufacture a requirement that every route beat every
alternative, nor do they turn exploratory work into a competition. Their job
is to reveal the behavior of the declared construction. Campaign-specific
controls remain campaign-specific.

## 9. Related SAMA documents

`SAMA-D000049` supplies the typed route from which controls are derived.
`SAMA-D000051` preserves the causal chain when a control or main run fails.
`SAMA-D000053` uses the same controls to define bounded promotion gates.

## Test and result index

| Test record key | Role | Source result/status | Result artifact | Test folder |
|---|---|---|---|---|
| [`LC:LC01`](../../tests/courtroom/16-the-last-campaign/README.md) | Primitive lock and standing wrong-control register | Historical campaign source; no SAMA classification assigned here | [LC01 result](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_result.md) | [Last Campaign folder](../../courtroom/16_THE_LAST_CAMPAIGN) |

## Atomic SAMA source records

| Record ID | Role in this document |
|---|---|
| `SAMA-C000015-R001` | Wrong controls as preserved productive diagnostics. |

## External references

- [Pinned global wrong-control register](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_wrong_controls.csv)
- [Pinned LC07 lane controls](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_wrong_controls.csv)
- [Pinned LC09 lane controls](../../courtroom/16_THE_LAST_CAMPAIGN/LC09_QUANTUM_PAIR_WRITE_BORN_RULE_REPLAY/LC09_wrong_controls.csv)
- [Pinned LC11 lane controls](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_wrong_controls.csv)

## Revision and approval

This exact revision has `reviewed_and_approved: false` until Sean Brady
explicitly approves it.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`LC:LC01`](../../tests/courtroom/16-the-last-campaign/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign/README.md) | [LC01_primitive_stack_lock_runner.py](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_primitive_stack_lock_runner.py) | [LC01_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_wrong_controls.csv)<br>[LC01_wrong_controls.csv.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_wrong_controls.csv.sha256.txt) | [LC01_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_result.md)<br>[LC01_result.md.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_result.md.sha256.txt)<br>[LC01_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_summary.json)<br>[LC01_summary.json.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_summary.json.sha256.txt) | [All 164 files](../../tests/courtroom/16-the-last-campaign/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000050`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/WRONG_CONTROLS_HOLDOUTS_AND_DIAGNOSTIC_ALTERNATIVES.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I–II–III–IV | SAMA-D000050 | Research Methodology | Wrong Controls, Holdouts and Diagnostic Alternatives |

| Document field | Value |
|---|---|
| Purpose | Derive controls from the actual technical route and explain how intended controls, wrong controls and holdouts locate structure, leakage, mutation and implementation faults. |
| Prerequisite documents | `SAMA-D000049` |
| Used by | `SAMA-D000051`, `SAMA-D000053`, and every document with a deviation chain |

</details>
