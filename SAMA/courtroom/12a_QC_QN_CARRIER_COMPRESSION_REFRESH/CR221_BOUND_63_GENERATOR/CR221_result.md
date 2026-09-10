# CR221 Bound 63 Generator Result

**Result class:** `CR221_PASS_BOUND_63_GENERATOR__CONSTANTS_ONLY__14_7_42__DOWNSTREAM_CR219_SIGNATURE_MATCH`

**Checks:** 15/15

## Verdict

The bound Tier 1 surface is generated from closure operators as
`14 + 7 + 42 = 63`. The result is not a copy of CR220: it has its own
three-owner color closures, equal neutral pairs, and oriented charged pairs.

CR219 is used only after generation to confirm that the generated bound
signatures, operator classes, and native masses match the existing promoted
bound-composite rows.

## Outputs

- `Tier1_Bound63.csv`
- `CR221_pair_closures_49.csv`
- `CR221_triad_closures_14.csv`
- `CR221_downstream_validation_CR219_bound63.csv`
- `CR221_validation_against_CR219.csv`
- `CR221_checks.csv`
- `CR221_summary.json`
- `HASHES.txt`

## Next Gate

CR222 can assemble CR220 native 63 plus CR221 bound 63 into the no-name Tier 1
input for the carrier ledger and element-search stages.
