# CR005h Starbreaker per-carrier GW candidate ledger

## Verdict

**FAIL_PER_CARRIER_GW_LEDGER_CONSTRUCTION**

The per-carrier ledger did not clear its construction controls.

## What was constructed

Each frozen Starbreaker carrier occurrence now has its own unit-occurrence trace-free quadrupole source, individual power, exact leave-one-out aggregate-power change, bind/escape class, and frozen carrier identity. Positive `DeltaP` marks reinforcement of the aggregate internal source proxy; negative `DeltaP` marks coherent cancellation.

This is the requested internal pixel-to-source track. No external waveform and no QNM response was used to decide the carrier list.

## Primary ledger-slot candidates

| Rank | Slot | Status | Escape-only | Reinforcer | Median DeltaP/P | Worst door | Localized | Dispersed |
|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | 16 | strong_candidate | 91.700% | 56.552% | 7.172337e-04 | 3.149332e-04 | 8.381504e-04 | 5.621448e-04 |
| 2 | 13 | strong_candidate | 89.415% | 54.234% | 4.159677e-04 | 2.359475e-04 | 4.744274e-04 | 2.947623e-04 |
| 3 | 17 | directional_candidate | 92.540% | 52.151% | 3.278155e-04 | 1.218791e-04 | 7.015825e-04 | -3.246681e-04 |
| 4 | 14 | strong_candidate | 93.515% | 53.797% | 4.728078e-04 | 7.568201e-05 | 4.101499e-04 | 5.719192e-04 |
| 5 | 15 | strong_candidate | 92.742% | 54.032% | 1.105841e-04 | 5.642221e-05 | 1.782521e-04 | 1.091339e-05 |

The full 18-slot table is in `CR005h_SLOT_CANDIDATES.csv`; the 200 strongest positive occurrences are in `CR005h_OCCURRENCE_SHORTLIST.csv`.

## Bind/escape source populations

| Frozen class | Occurrences | Share | Reinforcers | Reinforcer share | Median DeltaP/P |
|---|---:|---:|---:|---:|---:|
| escape_only | 49543 | 92.486% | 25696 | 51.866% | 9.214281e-05 |
| dual | 1993 | 3.721% | 1112 | 55.795% | 8.459645e-04 |
| return_only | 60 | 0.112% | 40 | 66.667% | 3.428489e-03 |
| neither | 1972 | 3.681% | 1030 | 52.231% | 4.937875e-04 |

## Source controls

- Direct leave-one-out validation: 16 samples, normalized error `3.862e-16`.
- Fine/coarse median aggregate-power difference: `1.938006%`.
- Maximum trace error: `4.855e-16`.
- Maximum translation-invariance error: `8.882e-16`.
- Static-source control: `3.729e-09`.
- Isotropic six-axis cancellation control: `1.605e-08`.

## Interpretation boundary

A carrier with positive leave-one-out influence is a candidate **source contributor** inside this frozen Starbreaker proxy. It is not thereby the substance of the outgoing gravitational wave. The current run remains dimensionless, unit-weighted, and internal: it does not claim physical strain, luminosity, seconds, or detector visibility.

The equal-occurrence all-atom centroid supplies translation invariance, but it is not called a physical mass center because the roster does not supply physical mass weights.
