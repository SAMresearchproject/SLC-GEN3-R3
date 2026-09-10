# CR210c Failure Adjudication

## Controlling verdict

`CR210c_FAIL_PRECOMMITTED_STRUCTURAL_CHECK`

The controlling executed artifacts are `CR210c_CHECKS.csv` and `CR210c_VALIDATION.json`: 15 of 17 gates passed; C14 and dependent C15 failed.

## Exact failure

CR210c correctly expanded the cross-kind domain to all six residues. It therefore produced the precommitted 18 pairs and 36 distinct occurrences. The inherited partner expression, however, remained:

```text
right = partner_block*18 + q*6 + r + 3
```

The frozen map requires:

```text
right = partner_block*18 + q*6 + ((r+3) mod 6)
```

For `r=3,4,5`, the missing modulo operation advanced the partner into the next microcycle instead of preserving `q`; at `q=2` it produced invalid slots 162, 163, and 164 outside the 0..161 ledger. The executed cross-kind audit consequently reported:

```text
pair_count = 18
boundary_occurrences_used = 36
involution_no_fixed_points = true
kind_rule_satisfied = true
locality_and_antipode_satisfied = false
```

The same-kind comparator passed its local audit. C15 failed only because that comparator control reused the aggregate `pairing_ok` flag made false by C14.

## Scope of the failure

CR210c does not establish or reject the declared modulo-6 cross-kind quotient because the executed partner function did not implement it. The other 15 gates passed, including the full source contract, 18/126/18 ledger typing, W9 x K18 inventory, 64-way split nonuniqueness, route-edge map, six 27-slot fibers, constructed ternary audit, H27 graph, prior-selector distinction, automorphisms, side reversal, and outcome/binding firewall.

The explanatory sentence in `CR210c_result.md` saying both boundary candidates close is non-controlling because its governing C14 check failed. This adjudication preserves rather than rewrites that generated artifact.

## Anti-circling stop and next exact change

The cross-kind implementation blocker has now repeated in two successor records, so this turn stops here under the repository anti-circling rule. CR210c is frozen and must not be patched or rerun.

A future separately preflighted record should make exactly this implementation change:

```text
right = partner_block*18 + q*6 + ((r+3) % 6)
```

It should also precommit explicit implementation guards requiring every paired slot to remain in boundary blocks 0 or 8, the used-slot set to equal exactly `{0..17} union {144..161}`, and application of `phi` twice to return each original occurrence.
