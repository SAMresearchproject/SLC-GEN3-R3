# CR005i Starbreaker per-carrier GW control appeal

## Verdict

**PASS_CR005H_CONTROL_APPEAL__PER_CARRIER_GW_CANDIDATE_LEDGER_ADOPTED_AND_FROZEN**

CR005h's unchanged 53,568-carrier ledger is adopted and frozen. Seven ledger slots are strong source-contributor candidates and one is directional.

CR005h itself remains an immutable failed run. CR005i changes no candidate value and no candidate rule; it corrects and independently replays only the three predeclared defective controls.

## Adopted primary candidates

| Rank | Slot | Status | Escape-only | Reinforcer | Median DeltaP/P | Worst door | Localized | Dispersed |
|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | 16 | strong_candidate | 91.700% | 56.552% | 7.172337e-04 | 3.149332e-04 | 8.381504e-04 | 5.621448e-04 |
| 2 | 13 | strong_candidate | 89.415% | 54.234% | 4.159677e-04 | 2.359475e-04 | 4.744274e-04 | 2.947623e-04 |
| 3 | 17 | directional_candidate | 92.540% | 52.151% | 3.278155e-04 | 1.218791e-04 | 7.015825e-04 | -3.246681e-04 |
| 4 | 14 | strong_candidate | 93.515% | 53.797% | 4.728078e-04 | 7.568201e-05 | 4.101499e-04 | 5.719192e-04 |
| 5 | 15 | strong_candidate | 92.742% | 54.032% | 1.105841e-04 | 5.642221e-05 | 1.782521e-04 | 1.091339e-05 |
| 6 | 4 | strong_candidate | 91.835% | 53.730% | 3.411334e-04 | 1.970101e-05 | 6.283349e-04 | 7.075032e-05 |
| 7 | 2 | strong_candidate | 93.212% | 52.587% | 4.511278e-04 | 1.945489e-05 | 6.506490e-04 | 2.638725e-04 |
| 8 | 3 | strong_candidate | 93.784% | 56.956% | 2.666704e-04 | 1.806179e-05 | 2.430774e-04 | 3.318332e-04 |

Strong slots: `16, 13, 14, 15, 4, 2, 3`. Directional slot: `17`.

## Corrected controls

- Parent authority: exact sealed verdict match = `True`.
- Full replay: `96` scenarios and `53568` carriers.
- Discrete linearity: maximum observed/bound ratio `5.253916e-03`; pass = `True`.
- Integrated-power ordering: maximum relative difference `1.616856e-09` against frozen limit `1.0e-06`; pass = `True`.
- Static quadrupole constancy residual `0.000000e+00`; derivative/bound `0.000000e+00`.
- Isotropic quadrupole cancellation residual `1.370646e-16`; derivative/bound `8.539898e-04`.

## What is now frozen

The authoritative occurrence ledger remains the byte-identical `CR005h_CARRIER_ATTRIBUTION.csv`. CR005i carries a hash pointer to that 53,568-row file and byte-identical copies of its 18-slot candidate table and 200-row occurrence shortlist.

## Interpretation boundary

These are internal quadrupole-source contributors. Positive leave-one-out influence means a carrier reinforces the aggregate Starbreaker source proxy; it does not mean the carrier is material transported by a gravitational wave. Physical strain, luminosity, seconds, signal speed, and detector visibility remain outside this result.
