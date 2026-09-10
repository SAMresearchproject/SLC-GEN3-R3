# CR120O All-Depth p9 Eight-Plus-One Native/qA Discrimination - Precommit

record_id: `CR120O_ALL_DEPTH_P9_EIGHT_PLUS_ONE_NATIVE_QA_DISCRIMINATION`

task: `Execute attached proposal using fresh QP093A 100-row and 81-row spreadsheet sums`

run_class: `CONSTRUCTIVE_NEW_WORK`

source_manifest_sha256: `544c0a598831a18ca784f210604c013607be0654c6cee9034fc4933e93fa46c2`

matched_triple_precommit_sha256: `6c6550600852ee33d6d143b76bb9c5173859e51f01ab46f61011ccc8d9be8da6`

challenge_roster_precommit_sha256: `f261bb1953b4bca59dfe950a67e6eeb3eaeb3a3ad9e90db3eea2170721cec5ef`

## Question actually under test

With the current workbooks held only as sum context, does the frozen QP093A
generator support an identity-preserving, all-eligible-depth interpretation in
which every lawfully matched native `p=9` single-write row is linearly generated
by its same-type `p=8` and `p=1` rows, while its nonlinear `qA` residual follows
one source-derived typed law across untouched generations and conjugacy classes?

This is the first proposal in the attached text. It is not another spreadsheet
comparison and it is not the second, binding-residual proposal.

## Sum lock - no mean test

The current-sheet sums are frozen context:

```text
12600  = 100 * 7 * 18
14400  = 100 * 8 * 18   (derived midpoint; no observed sheet)
16200  = 100 * 9 * 18
```

The 81-row cardinality remains a separate sheet fact. It is not a denominator,
normalization, or multiplier in this test. No row mean is computed, scored, or
used as a signal. The 100-row/16200 observation may not select the p9 model.

The two workbook files are hash-locked current inputs, but their already-known
row and sum facts are not re-tested here.

## Frozen historical control

QP093A's original premise includes primitive `p=9`. Its catalog, premise,
identities, classifications, and result status remain unchanged. CR120O creates
only a read-only discrimination ledger. It does not delete p9, rewrite QP093A,
or install a derived-nine semantic type.

## Typed matching rule

A primary triple must match exactly on every non-p coordinate that is lawful to
hold fixed:

- generation;
- normalized single-write role (`plus`, `minus`, `neutral`, `anti_plus`, or
  `anti_minus`);
- bin and stability status;
- operator class and route class;
- charge-sign class and conjugacy class;
- native charge axis, spin/hand class, owner-closure class, closure status, and
  matter-admission status.

Only the partition coordinate changes from `1` to `8` to `9`. The frozen roster
is exactly the 10 triples in `CR120O_MATCHED_TRIPLE_PRECOMMIT.csv`: five at
`g=0` and five at `g=1`.

The three `g=2` single-write groups are predeclared numeric challenges, not
primary typed matches: their p1 records are stable while their p8 and p9 records
are unstable. All 51 composite p9 occurrences, the hidden p9 support row, and
the same-scalar carrier fixture are frozen in
`CR120O_CHALLENGE_ROSTER_PRECOMMIT.json`.

Missing, ambiguous, route-changing, or type-changing matches are retained as
boundaries. They may not be forced into the primary roster.

## Exact native claim

For every primary triple:

```text
Delta_native = M_native(9,g) - M_native(8,g) - M_native(1,g) = 0
```

All arithmetic uses exact rational conversion from source coordinates and
terminating native values. Tolerance, fitting, displayed rounding, and target
search are forbidden.

The g2 challenge evaluates the same numerical identity but must remain marked
`TYPED_INELIGIBLE_STABILITY_MISMATCH` even if its scalar residual is zero.

## Source-derived qA law

QP093A applies surface processing before:

```text
qA = M_observed * (1 + q_abs/144)
```

Let `G=12^g`. Let the frozen role coefficient be:

```text
a_plus      = 5/4
a_minus     = 3/2
a_neutral   = 1/8
a_anti_plus = 5/4
a_anti_minus= 3/2
```

Let `c=1` for charged roles and `c=0` for neutral. Let the typed conjugate
surface sign be `sigma=0` for zero-contact matter/neutral, `sigma=+1` for the
negative-charge anti-plus surface credit, and `sigma=-1` for the positive-charge
anti-minus surface debit.

The predeclared generator-complete residual is:

```text
Delta_qA_expected = a * [c*G/9 + sigma*35/24]
```

The `G/9` term is the quadratic `8-by-1` cross-term. The conjugate term is the
additional source-mandated surface contribution:

```text
35/24 = (9^2-8^2-1^2)/12 + (9^3-8^3-1^3)/1728
      = 16/12 + 216/1728
```

Neutral predicts zero. The proposal's shorter `a*G/9` factorization is tested
separately: it is expected to apply only to charged zero-contact routes and is
not permitted to erase the conjugate surface term.

Each stored catalog decimal must also reconstruct under the generator's
100-digit Decimal operation order. Analytic residual verdicts use exact
fractions; displayed-decimal residuals are comparison-only and must differ from
the exact value by no more than `1e-96`.

## Frozen cross-depth evaluation

- `LEAVE_G0_OUT_TEST_G1`: the five g1 triples are untouched by the g0 block.
- `LEAVE_G1_OUT_TEST_G0`: the five g0 triples are untouched by the g1 block.
- No coefficient or threshold is fitted on either block; the law comes only
  from the frozen generator.
- The g2 numeric challenge is reported separately because its stability type
  prevents a lawful all-three typed match.

An all-depth structural claim passes only for lawfully eligible typed rows. A
base-depth-only interpretation requires an independent source rule. The 16200
sum is not such a rule.

## Primitive, all-depth, and base-depth models

1. `PRIMITIVE_NINE`: preserve the original p9 coordinate as independent.
2. `ALL_ELIGIBLE_DEPTH_8_PLUS_1`: mark exact native dependence for every
   lawfully matched single-write triple while preserving all identities.
3. `BASE_DEPTH_ONLY_8_PLUS_1`: apply derived status only at g0; this requires a
   separately sourced depth rule and cannot be selected by 16200.

Internal generator algebra can establish linear dependence but cannot, by
itself, falsify primitive-nine ontology. Model promotion therefore additionally
requires an independent SAM-internal comparator not used to define the algebra.
If none exists in the frozen sources, promotion must be blocked.

## Complete-family sum null

The null space is all 21 complete five-row family exclusions from the canonical
105-row stable-matter/neutral/conjugate lane: eight families at g0, eight at g1,
and five at g2. Each exclusion leaves 100 rows, so row count is non-discriminating.

For every exclusion the runner reports only the exact remaining sum and these
predeclared sum properties:

- integer-valued sum;
- exact divisibility by 18 when integer-valued;
- exact equality to one of `{12600, 14400, 16200}`;
- equality to the observed p9,g0 remaining sum.

No mean is calculated. The observed p9,g0 exclusion is located within all 21
possibilities, and hit counts divided by 21 are descriptive multiplicity rates,
not blind p-values, because 16200 was already observed.

## Wrong and adverse controls

The runner must retain and reject:

1. axis/role-shuffled p1 parents within generation;
2. g0/g1-swapped p1 parents while preserving charge and conjugacy;
3. forced g2 typed matching across the stable/unstable boundary;
4. forced composite matching that changes route arity or identity;
5. treating hidden nonlinear source support as native single-write matter;
6. treating the carrier scalar 9 as the partition coordinate p9;
7. applying the bare `a*G/9` law to conjugates and hiding the surface term;
8. approximate-decimal selection in place of exact rational arithmetic;
9. deleting or merging p9 identities after finding linear dependence;
10. selecting base-depth-only because it leaves the sum 16200;
11. treating a catalog sum as a physical conserved observable;
12. equating QP093A p9 with `W9_CLOSURE_WITNESS` by numeral or wording;
13. dividing 16200 by 100 and equating the resulting scalar with `L162`;
14. using the 81-row count as a normalization for 12600;
15. invoking `PROPAGATE_CLOSURE`, `LEDGER_SITE`, `ADJACENT`, or
    `ADJACENT_LEDGER_STATE` as installed relations;
16. calling the qA cross-term binding energy;
17. using a prior CR instead of the frozen QP093A generator/catalog to create
    the matched roster or residuals;
18. mutating either workbook, QP093A, a registry, or any source artifact.

## Precommitted gates

`G0 SOURCE_PRECOMMIT_LOCK`
: All source and precommit hashes match before calculation.

`G1 ROSTER_RECONSTRUCTION`
: The exact 10 primary triples and every frozen challenge id reconstruct from
  the catalog with no missing or duplicate identity.

`G2 TYPE_PRESERVING_MATCH`
: All 10 primary triples satisfy every frozen type key; g2 and composite
  challenges remain explicitly ineligible.

`G3 EXACT_NATIVE_REDUCIBILITY`
: All 10 primary native residuals are exactly zero.

`G4 GENERATOR_QA_RECONSTRUCTION`
: Every primary row's stored qA reproduces from the source operation order.

`G5 TYPED_QA_CROSS_TERM_LAW`
: All 10 exact qA residuals equal the generator-complete predeclared law;
  neutral is zero and conjugate surface terms remain visible.

`G6 CROSS_DEPTH_HOLDOUT`
: The same frozen law passes all five g0 and all five g1 triples separately.

`G7 UNSTABLE_AND_COMPOSITE_CHALLENGES`
: g2 numeric behavior, all 51 composite occurrences, hidden p9 support, and the
  carrier scalar fixture are fully reported without forced matching.

`G8 SUM_ONLY_NEATNESS_NULL`
: All 21 family exclusions are enumerated with exact sums and no mean signal.

`G9 WRONG_CONTROLS`
: Every frozen wrong control is detected; shuffled parent controls do not
  produce a zero native residual.

`G10 MODEL_AND_AUTHORITY_BOUNDARY`
: Primitive-nine remains the historical control; base-depth-only receives no
  authority from 16200; no physical, binding, W9, L162, or registry promotion
  occurs; missing independent discrimination blocks proposal promotion.

`G11 SOURCE_IMMUTABILITY_AND_OUTPUT_VALIDATION`
: Sources remain byte-identical and every required output is nonempty, hashed,
  and internally consistent.

## Conditional disposition

If all structural gates pass while the independent comparator remains absent:

`PASS_STRUCTURAL_TYPED_P9_8_PLUS_1_NATIVE_QA_LAW__PROPOSAL_PROMOTION_BLOCKED_NO_INDEPENDENT_DISCRIMINATOR`

with:

```text
mathematical_verdict          PASS
typed_primary_scope          stable/conjugate single-write g0 and g1
g2_status                     numeric challenge, typed ineligible
composite_status              unmatched route-changing challenge
primitive_nine_status         preserved, not falsified
base_depth_only_status        unsupported without independent depth rule
proposal_promotion            BLOCKED
physical_or_binding_claim     NOT MADE
```

## Required outputs

- `CR120O_SOURCE_SNAPSHOT.json`
- `CR120O_TYPED_MATCH_REPORT.json`
- `CR120O_TRIPLE_RESIDUALS.csv`
- `CR120O_QA_LAW_REPORT.json`
- `CR120O_HOLDOUT_REPORT.json`
- `CR120O_G2_CHALLENGE.csv`
- `CR120O_COMPOSITE_CHALLENGE.csv`
- `CR120O_NEATNESS_NULL.csv`
- `CR120O_NEATNESS_NULL.json`
- `CR120O_MODEL_DISCRIMINATION.json`
- `CR120O_WRONG_CONTROLS.json`
- `CR120O_VALIDATION_REPORT.json`
- `CR120O_summary.json`
- `CR120O_result.md`
- `COMMAND_LOG.txt`
- candidate manifest, candidate hash, and `HASHES.txt`

