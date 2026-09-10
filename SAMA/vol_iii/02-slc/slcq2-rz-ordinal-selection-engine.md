[SAM](../../README.md) · [Volume III](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# SLCQ2-RZ Ordinal Selection Engine

## Conceptual abstract

Exact computation can return several admissible receipts for one query. The
arithmetic substrate certifies what every receipt is, while the selection
plane asks a different question: which admissible receipt has the best exact
return quality when the selector is permitted to see only source geometry?
`SLCQ2-RZ` is the frozen current answer to that ordinal question.

The target quality is not a learned label invented after execution. For each
candidate receipt it is the frozen reciprocal-quotiented lexicographic vector

\[
Q=(d_{direction},r_{inverse},r_{W8},r_{D81}),
\]

where lower is better and equal vectors remain a complete target tie. Q2 does
not read any component used to construct that target. It exposes 70 exact
integer features computed from axis, modulus, shell, direction and two typed
domain labels. It excludes inverse inputs, inverse directions, returned
endpoints, D81 checkpoints, target tiers, custody identities, hashes,
execution order and timing.

The data surface contains 5,120 inherited exact receipts, 1,024 canonical
queries and 512 reciprocal/replicate-safe groups. Each axis is frozen into 80
TRAIN, 24 HOLDOUT and 24 CONTROL groups. TRAIN supplies 640 queries; HOLDOUT
and CONTROL each expose a complete 192-query catalog. Three exact-rational
architectures at three predeclared ridge values form nine fits. HOLDOUT fixes
the winner before CONTROL is opened:

`Q2-HYBRID_LISTWISE_ADJACENT_ORDINAL_RIDGE-RIDGE-1D1000`.

Against frozen Q1 on the same fresh surfaces, Q2 raises weighted strict-pair
accuracy by exactly `63200/594823` on HOLDOUT and `83595/773858` on CONTROL,
while recovering every exact best set, creating no false singleton, making no
abstention and producing no strict score tie. The installed classification is
exactly: **The test result suggests strong contact with the concept.**

The architecture is deliberately layered. Q2 owns the current ordinal
selection plane. Frozen `SLCV21R` remains noncurrent as a revision but remains
the byte-identical delegated arithmetic and application base. Q1 is an
immutable fallback. Neither selection nor promotion assigns physical scale,
absorbs ATOM3D, changes Exact Write semantics or authorizes application work.

## 1. Opening question and conceptual picture

The governing question is:

> Can exact source-visible event geometry order the complete admissible
> receipt catalog more faithfully than Q1 without reading any executed value
> that defines the answer?

The typed route is

```text
frozen SLCV21R exact query and candidate receipts
  -> reciprocal/replicate-safe grouping
  -> target-only exact return-quality vector
  -> 70-field source-visible feature map
  -> exact listwise and adjacent-ordinal fitting on TRAIN
  -> winner lock on complete HOLDOUT
  -> one comparison on sealed complete CONTROL
  -> frozen Q2 selection service
  -> SLCQ2-RZ current pointer
```

Three separations carry the meaning of the result:

1. the exact substrate determines admissibility and computes receipts;
2. the target oracle evaluates return quality but is hidden from selection;
3. the selector orders candidates from permitted source geometry alone.

Collapsing these surfaces would make the question circular. Keeping them
separate lets the result say something precise: the visible structural fields
contain enough ordinal information for the selected exact model to recover
the complete best set and nearly all strict pair orderings on two held-out
complete catalogs.

## 2. Current authority and architectural planes

### 2.1 Sole current/default revision

`SLCQ2-RZ` has status `FROZEN_COMPLETE_STOPPED_PROMOTED_CURRENT` and is the
sole current/default SLC pointer. Older v1.x, V20R and `SLCV21R` revisions
retain their artifacts and scoped results; they are not alternative current
pointers. The older Volume III technical spine therefore supplies lineage,
not present-tense pointer authority.

Q1 remains frozen and immutable as the fallback selector. A fallback is not a
second default: it is a preserved predecessor available under the declared
service boundary.

### 2.2 Selection is not arithmetic

For a query \(q\), let \(\mathcal C(q)\) be the finite set of receipts certified
admissible by the exact base. Q2 supplies a score

\[
s_q(c)=w^T\phi(q,c),\qquad c\in\mathcal C(q),
\]

with exact rational coefficient vector \(w\) and exact integer feature vector
\(\phi(q,c)\in\mathbb Z^{70}\). It returns all candidates attaining the
maximum permitted score, subject to the ambiguity policy described below.

The delegated base still owns DOS construction, exact write, reciprocal
return, checkpoints and application execution. Installing a new \(w\) changes
the ordering of already-admissible candidates; it does not change what the
candidate means or how its exact receipt is computed.

### 2.3 Four distinct planes

| Plane | Owner in the installed architecture | Output |
|---|---|---|
| exact substrate | frozen `SLCV21R` services | admissible exact receipts and arithmetic |
| quality target | frozen reciprocal-quotiented oracle | exact lexicographic target vectors |
| ordinal selector | current `SLCQ2-RZ` Q2 model | score order and complete top-score set |
| application | separately declared adapter/model | application-specific interpretation or execution |

An ATOM3D model, RH adapter or Mersenne scheduler may call the service only
through its own typed contract. None becomes part of Q2 merely by using its
ordering.

## 3. Target construction and blindness contract

### 3.1 Exact target order

The target for candidate \(c\) is

\[
Q_q(c)=
\bigl(
d_{direction}(q,c),
r_{inverse}(q,c),
r_{W8}(q,c),
r_{D81}(q,c)
\bigr).
\]

Vectors compare lexicographically, with smaller values preferred. The first
coordinate at which two candidates differ decides their strict order. If no
coordinate differs, both belong to the same target tier. In particular, a
custody identifier never converts an exact target tie into a singleton.

The complete best set is

\[
B_q=\{c\in\mathcal C(q):Q_q(c)=\min_{c'\in\mathcal C(q)}Q_q(c')\}.
\]

Recovery is exact only when the returned set equals \(B_q\), not when it merely
contains one member of \(B_q\).

### 3.2 Permitted source fields

Q2 may read only:

```text
axis
modulus
left_shell, right_shell
left_direction, right_direction
route_domain
physical_relation_domain
```

From these it computes the fixed 70-field map. The two domain labels are
constant on this source; they serve as a typed zero-variation interaction
check, not as an undeclared ranking signal.

### 3.3 Forbidden target and custody fields

The selector may not read:

```text
inverse input lanes or inverse directions
returned endpoint lanes
D81 checkpoint lanes
quality vector or quality tier
receipt index or pair identity
group hash or source hash
execution sequence
timing
```

This prohibition is load-bearing. Inverse, endpoint and checkpoint values
construct the oracle and would leak the answer. Custody fields could create
memorized ordering without structural meaning. Timings could import hardware
and execution-order artifacts into a mathematical selector.

## 4. Fresh grouped custody

### 4.1 Why the unit is a physical group

Individual receipt splitting is a wrong control because reciprocal directions
and replicated views of one physical relation can then appear on opposite
sides of a split. A model could learn one view and be scored on its mate.
Q2 hashes a fresh namespace together with axis, modulus, unordered shell
endpoints and the two source domain labels. All reciprocal directions and
replicates sharing that identity remain in one group.

The frozen census is

| Quantity | Exact count |
|---|---:|
| inherited exact receipts | 5,120 |
| canonical queries | 1,024 |
| reciprocal/replicate-safe groups | 512 |
| reciprocal canonical queries per group | 2 |
| observed group multiplicities | 4, 10, 16 |

The nonuniform multiplicities matter. A group contributes according to its
actual candidate roster; assuming one uniform multiplicity changes the
catalog and its weights.

### 4.2 Split derivation

Within each axis, group hashes are sorted and frozen as

\[
80\ \text{TRAIN}+24\ \text{HOLDOUT}+24\ \text{CONTROL}=128
\]

groups. Across the four axes this gives the 512-group total. The query census
is

\[
4\cdot80\cdot2=640\quad\text{TRAIN queries},
\]

\[
4\cdot24\cdot2=192
\]

queries on each of HOLDOUT and CONTROL.

TRAIN uses the frozen harder tier rule and contains 18,654 group references
and 182,688 receipt exposures. HOLDOUT and CONTROL retain every split-local
candidate group, yielding complete 192-query catalogs. Selection therefore
cannot improve a metric by silently dropping difficult candidates.

## 5. Deriving the 70-feature representation

### 5.1 Direct and reciprocal alignment

Let the centered source shell endpoints of a query and candidate be exact
integers. Q2 forms both alignments:

```text
direct:  query left -> candidate left, query right -> candidate right
swapped: query left -> candidate right, query right -> candidate left
```

For each alignment it retains signed residuals before taking absolute or
squared summaries. Schematically, with query endpoints ((a,b)) and candidate
endpoints ((c,d)),

\[
\delta_{direct}=(c-a,d-b),
\qquad
\delta_{swap}=(d-a,c-b).
\]

The map includes the signed components, absolute components, squares,
alignment sums and best/other residual summaries. Because both constructions
are ordered by a source-visible canonical key before exposure, a whole-lane
swap exchanges internal work without changing the final visible vector.

### 5.2 Midpoint, span, direction and parity

For endpoints ((a,b)), define signed midpoint numerator and span

\[
m=a+b,
\qquad
\ell=b-a.
\]

Using the numerator avoids a floating-point half. Candidate-minus-query
relations for \(m\) and \(\ell\) retain orientation and separation that coarse
shell bins erased. Individual direction matches and endpoint parity relations
are then appended rather than compressed to a single flag.

### 5.3 Two-adic profiles and typed interactions

For a nonzero integer \(n\), \(v_2(n)\) is the largest \(e\ge0\) for which
\(2^e\mid n\). Q2 includes four direct/swapped alignment valuations and two
span-relation valuations, with the frozen convention for zero. These features
expose dyadic shell structure without reading any returned value.

Route-domain and physical-relation-domain equality fields and their declared
interactions preserve the type boundary. Fourteen bounded quadratic cross
terms add fixed pair interactions; each is clipped at exact magnitude
16,777,215. The clip is part of the pre-execution feature contract and not a
post-result adjustment.

### 5.4 Why Q2 succeeds where the 20-field map collided

Q1's coarser 20-feature map has strict-pair feature-collision rates
2.3255657565% on HOLDOUT and 2.1898074324% on CONTROL. When two candidates
with different target order have the same visible vector, any deterministic
linear score must tie them. Q2's signed, unbinned and reciprocal-invariant map
has zero strict feature collisions on both surfaces. This removes that
representational obstruction before model fitting; it does not guarantee a
correct order by itself.

## 6. Exact ordinal fitting

### 6.1 Three predeclared architectures

The bounded roster contains:

1. `EXPANDED_QUERY_CENTERED_LISTWISE_RIDGE`, which fits query-centered tier
   grades over the harder TRAIN catalog;
2. `HYBRID_LISTWISE_ADJACENT_ORDINAL_RIDGE`, which appends exact differences
   for adjacent strict tiers with frozen weight four; and
3. `LEXICOGRAPHIC_CONDITIONAL_MULTI_HEAD_RIDGE`, which learns the first target
   coordinate globally and later coordinates only inside equality classes of
   the preceding coordinates.

Each architecture is fitted at exact ridge values

\[
\lambda\in\left\{\frac1{1000},\frac1{100},\frac1{10}\right\},
\]

giving \(3\times3=9\) fits. There is no floating-point training and no
full-scale hyperparameter sweep.

### 6.2 Listwise and adjacent observations

For each training query, a target tier grade is centered within its complete
candidate list. The listwise design therefore learns relative order without
letting different query offsets dominate.

For adjacent strict tiers, choose \(c_+\) from the better tier and \(c_-\) from
the next worse tier. The hybrid supplies the exact difference row

\[
\Delta\phi=\phi(q,c_+)-\phi(q,c_-),
\]

with a positive ordinal target and frozen weight four. A fitted vector should
therefore satisfy

\[
w^T\Delta\phi>0
\]

for that adjacent relation. Chaining adjacent relations transports the order
through the tier sequence while the listwise rows retain the complete query
geometry.

With exact design matrix \(X\), target \(y\), diagonal frozen observation weights
\(W\) and ridge \(\lambda\), the rational normal system is

\[
(X^TWX+\lambda I)w=X^TWy.
\]

All inputs and outputs remain `Fraction` values. Exact fitting makes score
equality a mathematical event rather than a floating tolerance choice.

### 6.3 Winner and tie policy

The three hybrid fits have identical complete-catalog ranking metrics. Only
after mathematical metrics and parameter count tie does the frozen key order
select the lower regularization identifier. The resulting winner is

`Q2-HYBRID_LISTWISE_ADJACENT_ORDINAL_RIDGE-RIDGE-1D1000`.

At service time, a score tie spanning distinct target vectors triggers
abstention. A score tie wholly inside one exact target vector returns the
complete tied best set. The promoted wrapper names a top-score multiplicity
explicitly as `AMBIGUOUS_TOP_SCORE`; it does not choose by receipt ID.

## 7. HOLDOUT selection and sealed CONTROL

### 7.1 Predeclared material comparator

Before execution, success required all three conditions:

- at least one percentage point of weighted strict-pair gain over frozen Q1
  on HOLDOUT;
- positive gain on CONTROL; and
- perfect exact-best-set recovery on both complete surfaces.

HOLDOUT selected and locked the model. CONTROL was opened once afterward for
the comparison to the frozen Q1 baseline.

### 7.2 Exact results

| Split | Frozen Q1 | Q2 winner | Exact delta | Decimal point gain |
|---|---:|---:|---:|---:|
| HOLDOUT | `530826/594823` | `594026/594823` | `63200/594823` | +10.625009 |
| CONTROL | `689509/773858` | `386552/386929` | `83595/773858` | +10.802369 |

The CONTROL Q2 fraction has denominator half the Q1 display denominator, so
the like-denominator comparison is

\[
\frac{386552}{386929}
=\frac{773104}{773858},
\]

and

\[
\frac{773104-689509}{773858}
=\frac{83595}{773858}.
\]

Q2 retains 6,376 wrong weighted strict pairs on HOLDOUT and 6,032 on CONTROL.
Those residual errors remain in the record. At the service boundary, however,
best-tier accuracy and exact-best-set recovery are both \(1/1\) on both splits,
with zero false singletons, zero abstentions and zero strict score ties.

The authorized classification is:

**The test result suggests strong contact with the concept.**

## 8. Deviation, correction and retest chain

### 8.1 Candidate-construction failures

Five preserved attempts materially shaped the frozen candidate:

| Attempt | Failure | Correction | Retest consequence |
|---|---|---|---|
| 001 | a cross-axis unit fixture mixed an axis-specific assumption into the test | construct the fixture inside its declared axis/type | boundary tests reached the intended feature question |
| 002 | code assumed uniform group multiplicity | retain the frozen observed roster `{4,10,16}` | complete catalogs and exposure weights reconstructed exactly |
| 003 | reciprocal orientation changed the visible feature vector | canonicalize complete direct/swapped blocks by source-visible keys | whole-lane swap became invariant |
| 004 | a serializer could not carry the exact fraction surface | encode exact numerators/denominators through the declared receipt form | checkpoint and replay identity remained exact |
| 005 | the Q1 collision diagnostic read the wrong comparison source | recompute that diagnostic from the frozen Q1 comparator on Q2 surfaces | the corrected Q1 collision rates changed; Q2 model selection and CONTROL result did not |

The first four attempts stopped before model selection or CONTROL access. The
fifth corrected a predecessor diagnostic only. Keeping these attempts makes
clear which faults affected construction and which did not affect the frozen
winner.

### 8.2 Promotion-wrapper corrections

Promotion also preserved two distinct corrections:

- Attempt 001 expected an `assertions_passed` field, while the independent
  receipt records `assertion_count=165`. The wrapper was corrected to read the
  actual schema before installation continued.
- Attempt 002 installed an executable resolution correctly, but the pointer
  inherited explanatory usage language and stale promotion fields. Pointer
  metadata was corrected, producing current pointer SHA-256
  `751f6e6a6dbe01cfdc335cf303824887148c9eb657ded691264e37c6f61fa318`,
  and the promotion surface was revalidated.

Neither correction retrained Q2, reopened Q1 or mined CONTROL.

### 8.3 Wrong controls retained as lessons

The following alternatives would answer a different question and are not the
installed controls:

- receipt-level random splitting, because it leaks reciprocal or replicated
  physical relations;
- incomplete HOLDOUT or CONTROL candidate rosters, because they can hide
  misranking and false singleton behavior;
- target-visible fields, because they make ordinal prediction circular;
- custody-ID tie breaking, because it converts exact ambiguity into an
  arbitrary order;
- floating score tolerances, because exact equality would depend on runtime;
- opening CONTROL during model choice, because CONTROL would cease to be the
  postselection surface.

## 9. Freeze and promotion process

The candidate freeze passed 8/8 release checks, 14/14 reconstruction checks,
165/165 independent assertions and, after the diagnostic correction, 8/8
release checks again. The promotion wrapper then passed:

| Gate | Result |
|---|---:|
| pre-install | 22/22 |
| post-install | 12/12 |
| independent promotion validation | 20/20 |
| final release | 6/6 |

Promotion changed the live selection pointer through H000551; H000552 records
the pointer-metadata correction. It preserved the candidate, Q1 and delegated
base artifacts rather than rewriting them.

The promotion performed no retraining, CONTROL mining, physical calibration,
ATOM3D specialization, remote transfer, prime work, publication or
deployment. These are not missing steps in Q2. They are separate campaigns
requiring their own contracts and authority.

## 10. Established result and boundary

This document establishes the following typed statement:

> On the frozen Q2 grouped catalogs, the 70-feature exact hybrid
> listwise-plus-adjacent ordinal selector materially improves strict-pair
> ordering over frozen Q1 and recovers every complete exact best set. Its
> promotion makes `SLCQ2-RZ` the sole current/default SLC selection revision,
> while exact arithmetic remains delegated to frozen `SLCV21R` and Q1 remains
> the immutable fallback.

It does not establish a physical energy scale, a new DOS, a change to Exact
Write, a global optimizer for every application, native GPU credit, ATOM3D
specialization, an RH conclusion or a Mersenne status. The next chapter uses
Q2 only as a typed application dependency and keeps its Mersenne scheduler and
certificates separate.

## 11. Test and evidence index

### 11.1 Direct permanent SAMA test routes

The current document catalog assigns no direct qualified SAMA test-record key
to `SAMA-D000055`. None is invented here. The source campaign contains its
own frozen candidate and promotion validation receipts, but those source
receipts have not been registered as direct SAMA test records for this
document.

### 11.2 Source evidence route

| Stage | Source evidence | Recorded outcome |
|---|---|---|
| pre-execution map | `SLC/18_SAM_NATIVE_QC/SLCV32_RZ_RELATIVE_QUALITY_ENGINE_CANDIDATE_Q2/ARCHITECTURE_SPEC.md` | fixed target, feature map, grouped split, roster and boundaries |
| candidate result | `SLC/18_SAM_NATIVE_QC/SLCV32_RZ_RELATIVE_QUALITY_ENGINE_CANDIDATE_Q2/release/QUALITY_ENGINE_RESULT.json` | exact HOLDOUT/CONTROL comparisons and classification |
| candidate failures | `SLC/18_SAM_NATIVE_QC/SLCV32_RZ_RELATIVE_QUALITY_ENGINE_CANDIDATE_Q2/failed_attempts/` | attempts 001 through 005 preserved |
| current promotion | `SLC/18_SAM_NATIVE_QC/SLCQ2_RZ_CURRENT_REVISION_V1/release/PROMOTION_RESULT.json` | pointer transition and promotion gates |
| metadata correction | `SLC/18_SAM_NATIVE_QC/SLCQ2_RZ_CURRENT_REVISION_V1/release/POINTER_METADATA_CORRECTION.json` | corrected current pointer metadata and hash |
| live authority | `SAM_LIVE/01_SLC_CURRENT.md`, H000531, H000551, H000552 | current/default identity and lineage boundary |

These routes are documentary evidence references, not substitutes for absent
qualified test keys.

## 12. Atomic-record index

| Atomic revision | Role in this chapter |
|---|---|
| `SAMA-C000236-R001` | fixes frozen `SLCQ2-RZ` as the sole current/default SLC revision |
| `SAMA-C000237-R001` | records the 70-feature Q2 ordinal result and authorized classification |
| `SAMA-C000238-R001` | separates current selection from the delegated exact `SLCV21R` base and Q1 fallback |
| `SAMA-C000239-R001` | records promotion gates and the ATOM3D/physical-calibration boundary |

## 13. Source and external-reference index

| Source | Load-bearing sections |
|---|---|
| `SAM_LIVE/00_CURRENT.md` | Immediate state; Current technical routing |
| `SAM_LIVE/01_SLC_CURRENT.md` | current `SLCQ2-RZ` authority and predecessor boundary |
| H000531 | Q2 candidate freeze and exact result |
| H000551 | current revision promotion |
| H000552 | pointer metadata correction |
| Q2 `ARCHITECTURE_SPEC.md` | target, custody, feature map, selector roster and hardware/application boundaries |
| Q2 `QUALITY_ENGINE_RESULT.json` | exact metrics, winner and classification |
| current landing | sole pointer, delegation, fallback and ambiguity behavior |

No new external scholarly, measurement or benchmark reference is introduced
by this chapter. Its exact claims are internal source-bound results carried by
the live/history and frozen Q2 artifacts above. Public repository custody is
fixed by the [`Volume III public repository constellation`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_III_TECHNICAL_SPINE.md#public-repository-constellation).
This is an explicit no-new-external-claim boundary, not an absent citation.

## 14. Revision and approval boundary

This is `SAMA-D000055`, revision 1. It is documentary synthesis only.
`reviewed_and_approved` remains `false`, and `approval` remains `null`. No
registry, current pointer, model, split, receipt, test route or result
classification is changed by this document.

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000055`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/SLCQ2_RZ_ORDINAL_SELECTION_ENGINE.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol III | SAMA-D000055 | SLC Selection | Current Q2 Ordinal Selection over the Delegated Exact SLCV21R Base |

| Document field | Value |
|---|---|
| Purpose | Present the sole current Q2 pointer, 70-feature source-visible ordinal-selection result, complete promotion gates, delegated exact SLCV21R base, immutable Q1 fallback and application boundaries. |
| Prerequisite documents | `SAMA-D000036`, `SAMA-D000037`, `SAMA-D000038` |
| Used by | `SAMA-D000056` |
| Revision state | Unapproved revision 1; this document records the current authority but does not itself move a pointer or promote a result. |

</details>
