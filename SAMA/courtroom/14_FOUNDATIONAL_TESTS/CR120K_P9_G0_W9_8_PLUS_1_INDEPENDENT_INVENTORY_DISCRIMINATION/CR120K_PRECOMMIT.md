# CR120K Precommit: p=9,g=0 W9 8+1 Independent-Inventory Discrimination

record_id: `CR120K_P9_G0_W9_8_PLUS_1_INDEPENDENT_INVENTORY_DISCRIMINATION`
task: `Run CR for p9 g0 8 plus 1 W9 provenance and 100 row 16200 independent inventory`
classification: `CONSTRUCTIVE_NEW_WORK`
result_lane: `STRUCTURAL_RESEARCH_BOUNDARY`
scientific_pass_claimed: `false`

## Question

Given the previously executed typed SAM route

```text
RESOLVE(S8_BINARY_SURFACE, B_CONTACT_OPERATOR, X1_AXIS_SELF_CHANNEL)
    -> W9_CLOSURE_WITNESS
```

and the frozen QP093A catalog, are the five unlifted `p=9,g=0`
matter/neutral/conjugate records exact derived W9 witness presentations whose
linear `M_native` content is already supplied by their matched `p=8,g=0` and
`p=1,g=0` parents?

If so, does a provenance-preserving overlay retain all 105 records while
distinguishing exactly 100 independent-content records with exact
`M_native = 16200` and five derived W9 witness records with exact duplicated
linear content `50.625`?

## Status of the observed numbers

The user supplied the observations `105`, `50.625`, `100`, and `16200` before
this precommit. They are therefore not blind predictions and cannot by
themselves establish the verdict. The verdict is controlled by the already
sourced typed W9 route, exact parent matching, typed dependency behavior,
full-record visibility, nonlinear-residual visibility, and wrong controls.

The arithmetic totals are frozen consequences to reproduce exactly without
tuning.

## Frozen source boundary

The exact paths, hashes, sizes, and roles are recorded in
`CR120K_SOURCE_MANIFEST.json`. No source outside that manifest may determine a
row selection, formula, parent mapping, or verdict.

The source workbook `Updated Particle Rows.xlsx` is not an execution input.
The authoritative row data are the sealed QP093A CSV and generator named in the
manifest. The workbook remains a user presentation/analysis surface.

## Terminology lock

The registered entity is `S8_BINARY_SURFACE`. Where prior discussion used
`W8`, this test uses the installed identifier `S8` and makes no new W8 entity.

`p=9,g=1` and `p=9,g=2` are generation-lifted rows, not the bare unlifted
`p=9,g=0` candidate under test. This CR neither promotes nor demotes those
higher-depth rows.

The formal CR219/CR119 126-row promoted surface is a different selection and is
out of scope. This CR operates only on the frozen QP093A bins
`stable_matter_rows` and `antimatter_conjugate_rows`.

## Immutable baseline

QP093A remains historical and unchanged:

```text
partition algebra = {1,2,3,4,6,8,9,12}
catalog rows       = 321
stable matter      = 63
antimatter         = 42
selected lane      = 105 records
```

This CR may emit a derived overlay. It may not edit the QP093A generator,
catalog, declared premises, source hashes, original row identities,
`matter_row_allowed`, or promotion statuses.

## Frozen hypotheses

### H0: independent primitive-nine baseline

The five `p=9,g=0` records remain independent matter-content records. The lane
contains 105 independent records and retains the baseline `M_native` total.

### H1: derived W9 witness overlay

The five `p=9,g=0` records remain visible, but each receives typed parentage
from the matching `p=8,g=0` and `p=1,g=0` records and the prior
`S8 + B through X1 -> W9` route. They are classified in the overlay as derived
closure-witness presentations, not independent content.

H1 does not erase the five records and does not force qA, observed surface, or
debit/credit values to become additive.

## Frozen row family

Exactly these five QP093A records are the candidate W9 family:

```text
QP093A-0019  plus_single_write[p=9,g=0]
QP093A-0020  minus_single_write[p=9,g=0]
QP093A-0021  neutral_single_write[p=9,g=0]
QP093A-0085  anti(plus_single_write[p=9,g=0])
QP093A-0086  anti(minus_single_write[p=9,g=0])
```

Each must map to exactly one `p=8,g=0` parent and one `p=1,g=0` parent with
the same bin, route family, operator class, route class, generation depth,
axis/conjugate role, spin/hand class, owner-closure class, closure status, and
original matter-admission status.

## Exact arithmetic and dependency rules

All numeric comparisons use exact decimal-to-rational conversion. Floating
tolerance, fitting, rounding-based selection, and target search are forbidden.

For each of the five rows:

```text
M_native(9,0) = M_native(8,0) + M_native(1,0)
```

The derived candidate is a dependency claim, not a copied label. Under a
frozen symbolic parent perturbation `delta=1` applied to the p8 parent scalar:

```text
P9_DIRECT    remains fixed at scalar 9
W9_DERIVED   changes from 8+1 to (8+delta)+1
```

The p1 perturbation is tested analogously. This intervention is a mathematical
model discriminator only; no source row is mutated.

The qA and surface fields remain visible and may be non-additive. For the
un-debited plus/minus matter rows, the frozen qA rule implies a combined-versus-
separate cross term. The neutral row is the zero-q null control. Conjugate
surface debit/credit residuals must be reported exactly rather than hidden.

## Independent-inventory overlay

The overlay must contain all 105 original records in original order and with
their original fields intact. It adds only derived audit fields.

For the five candidate W9 records:

```text
derived_partition_expression = 8+1
derived_entity                = W9_CLOSURE_WITNESS
independent_inventory_role    = DERIVED_W9_WITNESS
independent_content_counted   = no
```

For the other 100 records:

```text
independent_inventory_role    = INDEPENDENT_BASELINE_RECORD
independent_content_counted   = yes
```

The original 105-row record count must remain separate from the derived
independent-content count.

## Precommitted gates

`G0 SOURCE_AND_PRECOMMIT_LOCK`
: Every source hash and the embedded precommit hash match before calculation.

`G1 INSTALLED_W9_PROVENANCE`
: The frozen registries contain scalar 8 `S8_BINARY_SURFACE`, scalar 1
  `X1_AXIS_SELF_CHANNEL`, scalar 9 `W9_CLOSURE_WITNESS`, active
  `B_CONTACT_OPERATOR`, and active `RESOLVE` with typed result W9. The frozen
  CR120E execution trace contains that exact successful plan step.

`G2 QP093A_BASELINE_LOCK`
: Catalog count is 321; selected bins contain exactly 63 + 42 = 105 records;
  the selected lane's exact baseline `M_native` total is reproduced.

`G3 EXACT_UNLIFTED_P9_FAMILY`
: Exactly the five frozen IDs, and no other row, satisfy the exact unlifted
  p9 family selector.

`G4 TYPED_PARENT_MATCH`
: Every p9 row has exactly one p8 and one p1 parent matching all frozen type
  and role fields.

`G5 EXACT_LINEAR_DERIVATION`
: All five `M_native(9)=M_native(8)+M_native(1)` identities hold exactly and
  the five-row duplicated content totals exactly `50.625`.

`G6 DEPENDENCY_INTERVENTION`
: Derived W9 responds to isolated p8 and p1 parent perturbations while direct
  primitive p9 remains unchanged; no source row is changed.

`G7 RECORD_PRESERVATION_AND_COUNT`
: Overlay record count remains 105; exactly five records are derived witnesses;
  exactly 100 are independently counted; every original field is preserved.

`G8 INDEPENDENT_TOTAL_CONSEQUENCE`
: Removing only duplicated linear content from the independent-content sum
  yields exact total `16200`, while the 105-row baseline remains separately
  visible.

`G9 NONLINEAR_RESIDUAL_VISIBILITY`
: qA, observed-surface, carrier, retained-write, and conjugate debit/credit
  differences between direct p9 and separate p8+p1 are emitted exactly. No
  residual is used to repair the mapping.

`G10 WRONG_CONTROLS_AND_SCOPE`
: Every frozen wrong control is detected and rejected.

`G11 AUTHORITY_BOUNDARY`
: No language/registry/source mutation, no physical-particle claim, no
  deletion, no generated Python, no empirical fitting, and no promotion of
  the overlay into installed authority occurs.

## Frozen wrong controls

1. `DELETE_FIVE_ROWS`: physically remove the W9 records instead of retaining
   them as derived witnesses.
2. `TOTAL_TARGET_SELECTOR`: select or reclassify rows solely because a desired
   count or total is obtained.
3. `COPY_8_PLUS_1_WITHOUT_PROVENANCE`: attach the label without typed parents
   and the executed W9 route.
4. `FORCE_QA_ADDITIVITY`: overwrite the nonlinear/direct residual.
5. `W6_PLUS_X3`: substitute an untested 6+3 route for the sourced S8/X1 route.
6. `RECLASSIFY_G1_OR_G2_AS_BARE_W9`: expand the unlifted selector to lifted
   generations.
7. `MERGE_PARENT_IDENTITIES`: replace distinct p8, p1, and p9 record identities
   with one scalar record.
8. `COUNT_126_PROMOTED_SURFACE`: mix the separate formal promoted-row surface
   into this 105-row QP093A lane.
9. `HIDE_CONJUGATE_OR_NEUTRAL_CONTROLS`: evaluate only the favorable charged
   matter rows.
10. `PROMOTE_TO_PHYSICAL_PARTICLE_LAW`: turn a structural candidate into a
    scientific or empirical PASS.

## Verdict rules

If all gates pass and all wrong controls are rejected, emit:

```text
mathematical_verdict = PASS
result_class = STRUCTURAL_RESEARCH_BOUNDARY
scientific_pass_claimed = false
disposition = PASS_STRUCTURAL_P9_G0_DERIVED_W9_8_PLUS_1_OVERLAY_105_VISIBLE_100_INDEPENDENT_MNATIVE_16200_PHYSICAL_MAPPING_OPEN
```

If the arithmetic passes but typed W9 provenance or parent matching fails,
emit `BOUNDARY_NUMERICAL_DUPLICATION_WITHOUT_DERIVED_W9_PROVENANCE`.

Any source-hash failure, row deletion, hidden residual, changed original field,
or failed wrong control emits `FAIL`.

## Hard boundary

This CR can establish an exact provenance-preserving structural overlay and an
independent-content accounting rule for the frozen candidate lane. It cannot
establish that the 100 rows are the complete physical particle inventory, that
W9 is experimentally observed, or that the qA cross term is physical binding
energy. The CR120 local-propagation frontier remains unchanged.
