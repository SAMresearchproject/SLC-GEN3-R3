# SAM S=8 Surface-State Provenance Audit

Generated UTC: `2026-07-12T02:51:32Z`

## Verdict

`S8_VALUE_BACKED_DOMAIN_MULTIPLICITY_LABEL_UNSUPPORTED`

The value `S=8` is well supported. CR114 gives the conditional derivation
`D=3 -> 2^D=8` face-states, and Volume I consistently calls `S` the split
atom, split inventory, and eight face-state branches. No audited upstream
source authorizes CR281's label `DOMAIN_MULTIPLICITY`.

## Exact Source Finding

- CR114: `D` independent binary closure axes give `2^D=8` face-states.
- CR114: one unresolved face-state gives `1/8`; seven retained states give `7/8`.
- Volume I: `S=8` is binary split inventory / eight face-state branches.
- CR238: `S=8` is held foundational while selecting `D=3`.
- CR281: `DOMAIN_MULTIPLICITY` first appears as the precommitted expected label and is returned by a hardcoded label/value branch.
- CR281's sealed source manifest does not include CR114.

## Provenance Direction

1. `CR114_D_ROOTED`: given `D=3` and binary closure axes, derive `S=2^D=8`.
2. `CR238_S_ROOTED`: given canonical `S=8` and the two closure axioms, select `D=3`.

These are opposite program directions. They may demonstrate consistency, but
the executable must not present both as one acyclic derivation.

## Correct Language Type

Use `BinaryFaceStateCount` or `SplitInventory` for `S=8`. Operators may consume
that inventory as a divisor, exponent, or coefficient input without changing
its source role.

`DOMAIN_MULTIPLICITY` should remain unsupported unless a separate scientific
source explicitly establishes that meaning.

## Mathematical Wording Boundary

Three independent binary coordinates have eight configurations. A geometric
cube has six faces, not eight. Three binary inputs also allow 256 Boolean
labelings, not eight generic classification hypotheses. `Face-state` is a
defined SAM term and should not be paraphrased as a generic boundary surface or
classification hypothesis without an additional definition.

## Prospective Protocol Note

CR281 target content has now been inspected during language-release analysis.
It cannot silently serve as pristine validation evidence for a modified
language candidate; an append-only eligibility review is required.
