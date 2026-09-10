# CR120ZB — X1 Ordered Quantum Instrument Finite-Shot NV Discovery

## Primary verdict

`BOUNDARY_X1_ORDERED_QUANTUM_INSTRUMENT_FINITE_SHOT_NV_DISCOVERY__ONE_OR_MORE_FROZEN_GATES_FAILED`

## Result

The B-then-X1 signal survives the move from exact matrices to randomized finite-shot tomography under all three frozen NV noise profiles. The result is not carried by labels, populations, unmatched duration, or one favorable apparatus regime.

| NV profile | Forward median N | Forward q05 N | Maximum control q95 N | Positive order gaps | Median CHSH | CHSH > 2 blocks |
|---|---:|---:|---:|---:|---:|---:|
| room_temp_NV | 0.4615 | 0.4496 | 0.0088 | 48/48 | 2.6915 | 48/48 |
| cryogenic_NV | 0.4708 | 0.4624 | 0.0123 | 48/48 | 2.7337 | 48/48 |
| noisy_NV | 0.4426 | 0.4126 | 0.0104 | 48/48 | 2.6256 | 48/48 |

Every condition used two matched stages. Each reconstructed state used all 15 nontrivial Pauli observables at 4,096 shots per observable, frozen readout correction, linear inversion, and PSD projection. All 2,160 reconstructed states were physical.

## Relay arm

Resolved Bell-response swapping retained remote nonseparability in every profile. Its 5th-percentile negativity stayed above 0.20, while product-measurement and unresolved-herald 95th percentiles remained below 0.05. Exact noisy-channel local marginals remained invariant, with maximum trace distance `1.67e-16`.

## What advanced

CR120Z's order discriminator is not a perfect-state artifact. It remains strongly visible after the repo's existing room-temperature, cryogenic, and noisy NV error profiles, finite sampling, readout confusion, SPAM, relaxation, dephasing, drift, and PSD reconstruction. That makes the functional B-request/X1-response interpretation ready for a real-device protocol handoff.

## Boundary

No live backend was available or executed. The inherited NV profiles are simulator contacts, and the two-qubit translation is prospective. This run does not identify physical B with H, physical X1 with CNOT, or install a SAM operation. A physical weld requires raw device shots from independently addressable request and response intervals under the frozen interface specification.

## Custody

- Sources: 13/13 hashes matched.
- Hard gates: 8/9.
- Wrong controls: 12/12.
- Same-run repair: false.
- Registry mutation: false.
