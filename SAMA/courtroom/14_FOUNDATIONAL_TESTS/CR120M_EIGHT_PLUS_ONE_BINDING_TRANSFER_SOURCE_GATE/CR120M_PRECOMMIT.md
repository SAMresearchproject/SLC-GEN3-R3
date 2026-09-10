# CR120M Eight-Plus-One Binding-Transfer Source Gate — Precommit

record_id: `CR120M_EIGHT_PLUS_ONE_BINDING_TRANSFER_SOURCE_GATE`

task: `Run attached proposal for investigation Ideas, not evidence`

run_class: `CONSTRUCTIVE_NEW_WORK`

source_manifest_sha256: `a224fc55ce95854824c2c253f5f1de21f807ec7a2c0664d91d910b8e68be766f`

## Claim under test

Before any coupling fit or held-out binding comparison, determine whether the
frozen repository supplies all three prerequisites required by the attached
proposal:

1. an immutable registered binding baseline and typed residual;
2. a multi-row binding panel with unchanged observations and residuals;
3. an observation-blind, identity-preserving isotope-to-QP093A map that names
   matched `p=1`, `p=8`, and `p=9` structures and their multiplicities.

The proposal is executable only through this source gate. It is not itself
evidence or runtime authority.

## Frozen baseline

The installed AU197 packet is read only. Its runner is not replayed. Required
values are reproduced from the sealed packet:

```text
B_u_base_MeV                    27.421477
operator_debit_MeV               0.000000
B_u_final_MeV                  27.421477
B_u_obs_MeV                    31.139752
residual_obs_minus_final_MeV    3.718275
```

CR277 is reused as a sealed representative-isotope binding panel only. Its
existing predictions, observations, residuals, model coefficients, and
historical verdict may not be changed.

## Mapping gate

QP094A may satisfy the mapping prerequisite only if a frozen source record:

- identifies isotope `(Z,N,A)` rows;
- names matched QP093A `p=1`, `p=8`, and `p=9` structures for each eligible
  isotope;
- preserves distinct candidate ids and typed roles;
- supplies predeclared multiplicities and signs;
- does not use observed binding residuals to choose eligibility.

A generic proton/neutron/electron component selector does not satisfy this
gate. A scalar `8`, `9`, `1`, `162`, `W9`, or `L162` resemblance does not
create the map.

## Precommitted decision rule

If the baseline and panel are present but the mapping gate fails:

```text
execution_status         CLEAN
mathematical_verdict     BOUNDARY
result_class             STRUCTURAL_RESEARCH_BOUNDARY
feature_constructible    false
coupling_fit_allowed     false
heldout_test_allowed     false
disposition              BOUNDARY_BINDING_PANEL_PRESENT_P189_ISOTOPE_MAPPING_NOT_INSTALLED
```

This is a successful source-gate execution, not a scientific failure and not
a PASS for the proposed binding mechanism.

If the exact map is present, the runner may mark the proposal eligible for a
separate precommit. It still may not fit a coupling or run a held-out test in
this CR.

## Required checks

1. Every frozen source path, byte count, and SHA-256 matches the source
   manifest before and after execution.
2. The attached artifacts identify themselves as `PROPOSAL_ONLY`,
   `NOT_EVIDENCE`, `UNVALIDATED`, and `Executable No`.
3. The AU197 hash ledger and source manifest reproduce the packet sources.
4. The AU197 typed packet and JSON reproduce the five baseline quantities.
5. CR277 remains `PASS` with 126 rows, 118 observed rows, and 8 frontier rows.
6. CR277 contains the declared binding columns but no p/g/candidate-id or
   isotope-to-QP093A multiplicity fields.
7. QP094A remains a CLEAN discovery catalog with 126 element rows and 214
   isotope rows.
8. QP094A component selectors and their QP093A routes are reproduced exactly.
9. The full QP094A catalog is searched for qualifying matched-packet records,
   not merely proposal language or scalar occurrences.
10. CR120K remains a structural research boundary with physical mapping
    `OPEN_NOT_INSTALLED`.
11. No AU197 replay, coefficient fit, feature construction, target-dependent
    selection, registry edit, or source mutation occurs.

## Wrong controls

The runner must detect and reject:

1. treating `1/9` as MeV;
2. fitting a coupling on AU197 and citing AU197 improvement;
3. using CR277 residuals to invent isotope eligibility or multiplicities;
4. treating the QP094A proton/neutron/electron selector as a matched p1/8/9
   occupancy map;
5. identifying QP093A p9 with W9 or 162 with L162;
6. deleting or merging p9 identities;
7. altering the installed operator debit;
8. running held-out scoring with an undefined or constant feature;
9. calling the source-gate boundary validation of the mechanism;
10. invoking missing CR120 relations.

## Required outputs

- `CR120M_AU197_BASELINE_LOCK.json`
- `CR120M_BINDING_PANEL_INVENTORY.json`
- `CR120M_ISOTOPE_MAPPING_AUDIT.json`
- `CR120M_HYPOTHESIS_GATE.json`
- `CR120M_WRONG_CONTROLS.json`
- `CR120M_VALIDATION_REPORT.json`
- `CR120M_summary.json`
- `CR120M_result.md`
- `COMMAND_LOG.txt`
- candidate manifest, candidate hash, and `HASHES.txt`

## Hard boundaries

- Do not replay or overwrite the AU197 packet.
- Do not fit a MeV coupling.
- Do not modify CR277, QP094A, QP093A, CR120K, or any registry.
- Do not infer missing multiplicities from `Z`, `N`, `A`, shell capacities,
  row totals, residual signs, or scalar labels.
- Do not turn a missing map into a zero-valued feature and score it anyway.
- Do not promote the proposal beyond its source-supported state.
