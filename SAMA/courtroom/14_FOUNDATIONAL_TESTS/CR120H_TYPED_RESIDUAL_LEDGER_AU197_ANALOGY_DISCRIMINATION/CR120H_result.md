# CR120H Typed Residual Ledger / Au-197 Analogy Discrimination

record_id: `CR120H_TYPED_RESIDUAL_LEDGER_AU197_ANALOGY_DISCRIMINATION`
result_class: `MATHEMATICAL_RESEARCH_BOUNDARY`
scientific_pass_claimed: `false`
disposition: `RESEARCH_BOUNDARY_TYPED_LEDGER_SHAPE_SHARED_AU197_OPERATOR_SLOT_NULL_CLOSURE_NUCLEAR_IDENTITY_REJECTED_MECHANISM_MAPPING_OPEN`

## Direct result

CR120G and the Au-197 packet support the same five-slot abstract accounting
shape:

```text
base + operator_adjustment = program_final
reference - program_final = post_program_residual
```

The frozen projections execute as:

```text
CR120G:  2 constructed counts + 1 constructed count = 3
         reference 3 - reconstructed 3 = 0

Au-197:  27.421477 MeV + 0.000000 MeV = 27.421477 MeV
         observed 31.139752 - predicted 27.421477 = 3.718275 MeV
```

That common ledger shape is reusable. The quantities are not interchangeable.
Every paired slot has different semantic types, units, provenance, and
authority.

## Decisive Au-197 boundary

Au-197's operator contribution is exactly `0.000000 MeV`. Its `3.718275 MeV`
quantity is the observation-minus-prediction residual after the program, not an
operator debit. Therefore Au-197 does not exercise a nonzero operator effect
and cannot establish that CR120G `kappa` corresponds to a nuclear operator
contribution.

The full frozen CR277 table confirms that the installed rule is a signed plus
contribution:

```text
B_u_final = B_u_base + op_contribution
```

Checked rows: 126
Positive / negative / zero contributions:
7 /
14 /
105
Maximum final-equation error: 0.000001 MeV
Maximum stored-residual error: 0.000001 MeV

Calling every contribution a debit would lose the installed sign information:
negative terms are debit-like, positive terms are credit-like, and Au-197 is
the null case.

## Discrimination

- Omitting CR120G `kappa` leaves reconciliation residual `1`.
- Replacing the CR277 plus rule with a universal minus rule fails every
  nonzero-contribution row.
- The frozen forced-operator Au-197 control remains rejected.
- The frozen observed-as-generator control remains rejected as target leakage.
- `kappa`, nuclear operator contribution, closure reconciliation residual, and
  Au-197 post-program residual remain separate entities.

## Authority boundary

This result establishes an abstract typed accounting interface only. No
closure-to-binding relation or common physical mechanism is installed.

- `P80_PARTICLE_FACE_CONTENT` remains `STRUCTURAL_ONLY` and unpopulated.
- No response scalar `q` is defined.
- No clock or supernova data are used.
- No registry or language operator is added.

The CR120 frontier remains unchanged:

```text
PROPAGATE_CLOSURE       MISSING
LEDGER_SITE             MISSING
ADJACENT                MISSING
ADJACENT_LEDGER_STATE   MISSING
```
