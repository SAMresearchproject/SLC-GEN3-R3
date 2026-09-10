# CR225 Precommit - Carrier/Hidden CLOCK Selector Candidate

## Task

Explore whether the carrier tensor -> split -> kappa/G/GR scaffold can produce
the physical CLOCK selector without peeking at element cards.

## Predeclared Native Formula Candidate

Use only the SAM constants and the already sealed carrier/hidden-source
identities:

```text
R = 12
D = 3
alpha_H = 2
split = 2^D = 8
capacity = R^2 * (1 - 2^-D) = 126

tensor_release T = R^2 / 2^D = 18
neutral_vector_carrier Zc = D^(D+1) = 81

hidden_set = { alpha_H^a * D^b | a,b >= 0 and alpha_H^a * D^b <= R }
hidden_set = {1,2,3,4,6,8,9,12}
hidden_sum H = 45

clock_boundary = Zc + alpha_H = 83
hole_seed = H - alpha_H = 43
hole_tensor_shift = hole_seed + T = 61

candidate_CLOCK_stable(Z) = (Z <= 83) and (Z not in {43,61})
```

This precommit does not claim a final physical mechanism. It tests a native
zero-free-parameter candidate against the HH001/CLOCK labels as a comparator
only.

## Inputs

- `CR217_carrier_block.csv`: verifies tensor and neutral-vector carrier values.
- `CR217_hidden_source_block.csv`: verifies hidden-source lift rows.
- `CR218_summary.json`: verifies hidden-source set derivation from the bigrade lattice.
- `CR224_sob_rows_126.csv`: native 126-row SOB scaffold for row fields only.
- `CR220_simulated_element_primary_rows_126.csv`: reference CLOCK comparator only.

## Forbidden Construction Inputs

- known element symbols/names
- measured matter masses
- public element cards
- HH001/CLOCK labels used as construction input
- reference-patched row exceptions

The HH001/CLOCK labels may be used only after candidate construction for scoring.

## Expected Outputs

- `CR225_formula_terms.csv`
- `CR225_clock_candidate_rows_126.csv`
- `CR225_selector_scores.csv`
- `CR225_wrong_controls.csv`
- `CR225_input_manifest.csv`
- `CR225_checks.csv`
- `CR225_summary.json`
- `CR225_result.md`
- `HASHES.txt`

