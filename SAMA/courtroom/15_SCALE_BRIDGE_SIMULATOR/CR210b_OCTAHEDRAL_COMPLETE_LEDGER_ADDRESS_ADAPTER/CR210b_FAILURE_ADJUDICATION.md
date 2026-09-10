# CR210b Failure Adjudication

## Controlling verdict

`CR210b_FAIL_PRECOMMITTED_STRUCTURAL_CHECK`

The controlling executed artifacts are `CR210b_CHECKS.csv` and `CR210b_VALIDATION.json`: 15 of 17 gates passed; C14 and C15 failed.

## Exact failure

The frozen cross-kind map applies to all residues `r in {0,1,2,3,4,5}`:

```text
phi(b,q,r) = (8-b, q, (r+3) mod 6)
```

The inherited implementation instead used `for r in range(3)` for both pairing modes. That enumeration is complete for the same-kind mode because it visits both boundary blocks, but incomplete for the cross-kind mode because it visits only block 0. The observed cross-kind audit therefore contains:

```text
pair_count = 9
boundary_occurrences_used = 18
```

instead of the precommitted:

```text
pair_count = 18
boundary_occurrences_used = 36
```

C15 failed only because the same-kind comparator control reused the aggregate `pairing_ok` flag that C14 had made false.

## Scope of the failure

This record does not establish or reject the complete cross-kind quotient because the declared map was not fully enumerated. The other 15 gates passed as executed, including the exact source contract, 18/126/18 typing, W9 x K18 inventory, 64-way partition nonuniqueness, route-edge candidate, six 27-slot fibers, constructed ternary audit, H27 graph, prior selector reproduction and distinction, automorphisms, side reversal, and closed outcome/binding firewall.

The explanatory paragraph in `CR210b_result.md` saying both boundary candidates close is non-controlling because its own governing C14 check failed. This adjudication does not rewrite that generated artifact.

## Preservation

CR210b is frozen as FAIL. Its runner and artifacts must not be patched or rerun. Any corrected full-residue enumeration requires a new task-specific preflight, new record identifier, and freshly sealed precommit.
