# CR120K p=9,g=0 W9 8+1 Independent-Inventory Discrimination

record_id: `CR120K_P9_G0_W9_8_PLUS_1_INDEPENDENT_INVENTORY_DISCRIMINATION`
mathematical_verdict: `PASS`
result_class: `STRUCTURAL_RESEARCH_BOUNDARY`
scientific_pass_claimed: `false`
disposition: `PASS_STRUCTURAL_P9_G0_DERIVED_W9_8_PLUS_1_OVERLAY_105_VISIBLE_100_INDEPENDENT_MNATIVE_16200_PHYSICAL_MAPPING_OPEN`

## Direct result

The precommitted structural candidate passes every exact gate and wrong
control. The frozen QP093A lane remains fully visible:

```text
visible records                         105
derived p=9,g=0 W9 witness records       5
independent-content records             100
baseline M_native                       16250.625
duplicated linear W9 content             50.625
independent-content M_native             16200
independent mean                         162
exact ledger relation                    100 * 162 = 16200
records deleted                          0
```

The five records are retained in
`CR120K_INDEPENDENT_INVENTORY_OVERLAY_105.csv` and classified only in the
derived overlay as `DERIVED_W9_WITNESS`. Their original QP093A fields and
identities remain unchanged.

## Sourced 8+1 provenance

The frozen language registry and CR120E execution jointly supply:

```text
S8_BINARY_SURFACE       scalar 8   BinarySurface
X1_AXIS_SELF_CHANNEL    scalar 1   AxisChannel
B_CONTACT_OPERATOR                 active ContactOperator
RESOLVE(S8,B,X1) -> W9  scalar 9   ClosureWitness   PASS
```

No W6/X3 route is substituted. The exact row selector is the unlifted
`p=9,g=0` family only; generation-lifted p9 rows remain untouched.

## Exact parent matrix

| derived W9 record | p8 parent | p1 parent | M9 | M8 + M1 | residual |
|---|---|---|---:|---:|---:|
| QP093A-0019 | QP093A-0016 | QP093A-0001 | 45/4 | 10 + 5/4 | 0 |
| QP093A-0020 | QP093A-0017 | QP093A-0002 | 27/2 | 12 + 3/2 | 0 |
| QP093A-0021 | QP093A-0018 | QP093A-0003 | 9/8 | 1 + 1/8 | 0 |
| QP093A-0085 | QP093A-0083 | QP093A-0073 | 45/4 | 10 + 5/4 | 0 |
| QP093A-0086 | QP093A-0084 | QP093A-0074 | 27/2 | 12 + 3/2 | 0 |

Every linear residual is exactly zero and the duplicated five-row content is
exactly `405/8 = 50.625`.

## Dependency discrimination

The direct-nine candidate remains fixed when a parent is perturbed. The
derived W9 candidate changes under isolated p8 or p1 perturbation while
preserving the unperturbed equality. This supplies a dependency discriminator
without mutating any source row.

## Nonlinear residuals remain visible

The p9 record and separate p8+p1 parents are not merged. Their downstream
fields can differ:

| record | M_native residual | M_observed residual | qA residual | debit/credit residual |
|---|---:|---:|---:|---:|
| QP093A-0019 | 0 | 0 | 27777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777/200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 | 0 |
| QP093A-0020 | 0 | 0 | 20833333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333/125000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 | 0 |
| QP093A-0021 | 0 | 0 | 0 | 0 |
| QP093A-0085 | 0 | 1666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666663/1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 | 490451388888888888888888888888888888888888888888888888888888888888888888888888888888888888888888887/250000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 | -16666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666663/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 |
| QP093A-0086 | 0 | -2 | -1010416666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666667/500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 | 2 |

The neutral qA residual is the precommitted null control. Charged and
conjugate residuals remain explicit and are not used to repair the mapping.

## Interpretation

Within this frozen candidate lane, the five bare p9 records have exact typed
8+1 parent matches and duplicate linear `M_native` content already present in
the p8 and p1 records. A provenance-preserving independent-content overlay
therefore contains 100 counted records with exact total 16200 while retaining
all 105 visible records.

The user supplied the round totals before precommit. They are reproduced
consequences, not blind evidence. The controlling discrimination is the prior
typed W9 route plus exact parent, dependency, identity, and residual gates.

## Authority boundary

This is a mathematical structural PASS inside a research boundary. It does
not alter QP093A, the SAM Language, either registry, the formal 126-row
promoted surface, or any historical Courtroom result. It does not establish a
complete physical particle inventory, physical W9 observation, or binding
energy law.

The CR120 frontier remains missing and preserved:

```text
PROPAGATE_CLOSURE       MISSING
LEDGER_SITE             MISSING
ADJACENT                MISSING
ADJACENT_LEDGER_STATE   MISSING
```
