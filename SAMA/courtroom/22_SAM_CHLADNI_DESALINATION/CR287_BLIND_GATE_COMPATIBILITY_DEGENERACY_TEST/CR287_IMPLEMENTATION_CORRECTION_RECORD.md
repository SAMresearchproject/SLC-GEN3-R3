# CR287 Implementation Correction Record

## First Attempt

The first wrapper execution occurred at preflight artifact time
`20260714_224113`. It stopped before result emission with:

```text
KeyError: 'species_rank_groups'
```

## Classification

This was an implementation/schema lookup defect, not a scientific failure.
The declared premises store the two precommitted tie counts as
`expected_species_rank_groups` and `expected_gate_rank_groups`; the runner
incorrectly looked for unprefixed keys while assembling the inventory check.

## Bounded Correction

The runner was changed only to map the actual inventory field names to the
existing prefixed premise keys. No source, compatibility rule, expected count,
control disposition, boundary condition, or result class changed.

The corrected runner must be executed through the same task-scoped Courtroom
wrapper. This record remains in the final hash ledger.

## Pre-Freeze Documentation Packaging

Before final rerun, the exact branch README used by CR287 was copied into
`CR287_BRANCH_README_INPUT_SNAPSHOT.md`; its byte count and SHA-256 are
identical to source S01. The input manifest was pointed to that immutable
snapshot so the live branch README could record the CR287 boundary without
destroying input reproducibility. This changed no scientific input content or
expected result.
