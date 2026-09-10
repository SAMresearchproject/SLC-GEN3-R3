# CR120S — QP093A F81 Retained-Matter Projection

record_id: `CR120S_QP093A_F81_RETAINED_MATTER_PROJECTION`

task: `Execute the instructions in do this.pdf`

classification: `CONSTRUCTIVE_NEW_WORK`

## Controlling question

Is there a source-backed, executable, observation-blind row-selection operator
that selects the retained-matter projection using only row type, depth, charge
conjugation, partition role, closure/resonance status, and geometry — without
using `M_native`, the desired row count 81, or the desired sum 12600?

This is the PDF's CR-B finding. It is deliberately separate from CR120R.

## Reveal protocol

The operator must be defined and hash-sealed before any `M_native` value in
`UPDATED_WORKBOOK_81` is opened by the runner.

An admissible operator contract must contain:

1. a named canonical candidate universe;
2. a deterministic predicate or constructive geometry mapping for every row;
3. typed handling of matter, antimatter, neutral, closure-witness, and resonance rows;
4. a source path and exact source key for each rule;
5. no reference to candidate IDs as a whitelist;
6. no reference to current workbook membership;
7. no reference to target row count or target sum.

Only after such a contract exists may the runner reveal selected IDs, row
count, and the `M_native` sum.

## Allowed selector inputs

- row type: canonical operator/route/spin/owner-closure classes;
- depth: canonical closure depth and surface depth;
- charge conjugation: canonical sign, axis, and conjugate route type;
- partition role: typed partition occurrence, not an untyped numeral;
- closure/resonance status: canonical source status, not workbook-only user relabeling;
- geometry: an explicit source-derived finite-shape mapping.

## Forbidden selector inputs

- `M_native`, `M_observed_candidate`, `qA_source_support`,
  `tensor_carrier_support`, `retained_write_support`, or debit/credit values;
- the desired values 81, 12600, 100M, 7Theta, or any equivalent target test;
- current 81-workbook membership, row ordering, or sheet name;
- candidate-ID whitelists or direct enumeration of the desired roster;
- workbook-only `STABLE_USER_RECLASSIFIED_RESONANCE` or promotion labels;
- observed binding residuals or measured particle/nuclear targets;
- using CR120R's p9,g0 witness exclusion as an automatic F81 membership rule.

## Frozen candidate-operator status

The focused source pass found no admissible row-level operator contract.

- `CR119_typed_hierarchy.json` derives the scalar hierarchy
  `W9 -> V27 -> F81 -> L162`, but supplies no QP093A row predicate.
- `CR120N_SELECTION_AUTHORITY.json` records `OPEN_NOT_INSTALLED`.
- `CR120L_result.md` states that no frozen source independently selects the
  additional omissions and five manual heavy insertions.
- CR120R establishes only the p9,g0 closure-witness packet exclusion for the
  100-row full ledger; it does not derive an 81-row matter projection.

Accordingly:

```text
candidate_operator_contract = NONE_FOUND
M_native_reveal_authorized = false
```

The runner must fail closed. It may hash the workbook but may not parse its
rows or open `M_native` because no selector contract is sealed.

## Gates and disposition

- `G1_SOURCE_LOCK`: all manifest sources and the precommit match their frozen hashes.
- `G2_ALLOWED_FIELD_CONTRACT`: allowed and forbidden feature sets are emitted exactly.
- `G3_SOURCE_OPERATOR_PRESENT`: a source-backed executable row selector satisfying the reveal protocol exists.
- `G4_REVEAL_DISCIPLINE`: if G3 is false, the workbook is not parsed and no selected roster/count/sum is newly emitted.

```text
PASS_F81_RETAINED_MATTER_PROJECTION
  iff G1, G2, G3, and G4 all pass; only then may the selected set be revealed,
  and it must independently land on 81 rows and sum 12600.

BOUNDARY_F81_AND_M126_NUMERIC_WELD_PROJECTION_RULE_OPEN
  iff G1, G2, and G4 pass but G3 is false.

FAIL_REVEAL_LEAK_OR_INVALID_OPERATOR
  iff G1 or G2 fails, or target-aware information is used before a valid operator.
```

## Binding boundary

The known 81/12600 compatibility remains context, not a coefficient. Neither
126, 162, 12600, nor 16200 is inserted into a binding formula. Future binding
work must count only typed lift excess for supports required by independently
derived isotope geometry, with Theta zero-fee and W9 non-payload boundaries.

## Required outputs

- `CR120S_allowed_fields_contract.json`
- `CR120S_operator_search.json`
- `CR120S_summary.json`
- `CR120S_result.md`
- `CR120S_VALIDATION_REPORT.json`
- `HASHES.txt`
