# CR225 Carrier/Hidden CLOCK Selector Candidate

Result: **CR225_PASS_CARRIER_HIDDEN_CLOCK_SELECTOR_CANDIDATE__BOUNDARY_83_AND_HOLES_43_61_NATIVE_FORMULA__HH001_MATCH_81_OF_81__MECHANISM_CANDIDATE_NOT_FINAL_PHYSICAL_PROOF**

## Direct Answer

The carrier/hidden formula candidate lands on the HH001 CLOCK comparator:

```text
stable iff Z <= 83 and Z not in {43,61}
```

It is generated without public element cards, known labels, measured masses, or
CLOCK labels as construction inputs.

## Native Formula

```text
R = 12
D = 3
alpha_H = 2
split = 2^D = 8

T = R^2 / 2^D = 18
Zc = D^(D+1) = 81
hidden_set = {1,2,3,4,6,8,9,12}
H = sum(hidden_set) = 45

clock_boundary = Zc + alpha_H = 83
hole_seed = H - alpha_H = 43
hole_tensor_shift = hole_seed + T = 61
```

So the candidate CLOCK selector is:

```text
CLOCK_stable_native(Z) = (Z <= 83) and (Z not in {43,61})
```

## Comparator Score

| Selector | Predicted | TP | FP | FN | TN | Accuracy |
|---|---:|---:|---:|---:|---:|---:|
| neutral-vector cardinality `Z <= 81` | 81 | 79 | 2 | 2 | 35 | 0.966102 |
| carrier boundary `Z <= 83` | 83 | 81 | 2 | 0 | 35 | 0.983051 |
| carrier/hidden CLOCK candidate | 81 | 81 | 0 | 0 | 37 | 1.000000 |

The boundary-only candidate reproduces the previous `83` surface and leaves the
two holes `43;61`. The carrier/hidden rejector removes exactly those two rows
and gives the 81-row CLOCK comparator surface.

## What Is Backed

- `T = 18` matches the CR217 tensor/graviton carrier row.
- `Zc = 81` matches the CR217 neutral-vector carrier row.
- `hidden_set = {1,2,3,4,6,8,9,12}` is the CR218 bigrade-derived set.
- The formula-derived holes are `43` and `61`.
- The resulting selector matches HH001/CLOCK over scored rows with no false
  positives and no false negatives.

## Boundary

This is a strong native selector candidate, not a final physical proof. The
CLOCK labels are still used only as a comparator. The next pressure test is to
ask whether the same carrier/hidden rule predicts a held-out surface or a new
isotope/decay boundary without reference labels.

## Artifacts

- `09a_PARTICLE_MASS_CHAIN/CR225_CARRIER_HIDDEN_CLOCK_SELECTOR/CR225_formula_terms.csv`
- `09a_PARTICLE_MASS_CHAIN/CR225_CARRIER_HIDDEN_CLOCK_SELECTOR/CR225_clock_candidate_rows_126.csv`
- `09a_PARTICLE_MASS_CHAIN/CR225_CARRIER_HIDDEN_CLOCK_SELECTOR/CR225_selector_scores.csv`
- `09a_PARTICLE_MASS_CHAIN/CR225_CARRIER_HIDDEN_CLOCK_SELECTOR/CR225_wrong_controls.csv`
- `09a_PARTICLE_MASS_CHAIN/CR225_CARRIER_HIDDEN_CLOCK_SELECTOR/CR225_input_manifest.csv`
- `09a_PARTICLE_MASS_CHAIN/CR225_CARRIER_HIDDEN_CLOCK_SELECTOR/CR225_checks.csv`
- `09a_PARTICLE_MASS_CHAIN/CR225_CARRIER_HIDDEN_CLOCK_SELECTOR/CR225_summary.json`
- `09a_PARTICLE_MASS_CHAIN/CR225_CARRIER_HIDDEN_CLOCK_SELECTOR/HASHES.txt`
