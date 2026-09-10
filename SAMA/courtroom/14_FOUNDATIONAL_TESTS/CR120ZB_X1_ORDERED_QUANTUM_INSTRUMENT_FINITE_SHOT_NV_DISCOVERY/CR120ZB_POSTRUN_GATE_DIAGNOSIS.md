# CR120ZB Postrun Gate Diagnosis

## Controlling verdict

The sealed primary verdict remains:

`BOUNDARY_X1_ORDERED_QUANTUM_INSTRUMENT_FINITE_SHOT_NV_DISCOVERY__ONE_OR_MORE_FROZEN_GATES_FAILED`

No in-place repair or regrade is performed.

## Failed gate

Only `G2_PROFILE_IMPORT` failed. Its implementation was:

```python
profile_order == list(profiles.keys())
```

The required profile names were all present and were all executed through the explicit `profile_order` iteration. The inherited JSON object stored its keys in a different insertion order. The gate therefore tested JSON key order rather than profile presence, content, or execution.

## Scientific gates

- Physical PSD reconstructions: PASS, 2,160 states.
- Independent calibration: PASS, 3/3 profiles.
- Forward-order validation: PASS, 3/3 profiles.
- Resolved swapping validation: PASS, 3/3 profiles.
- Exact noisy-channel marginal invariance: PASS.
- Matched two-stage randomized schedule: PASS.
- Wrong controls: PASS, 12/12 rejected.

All three validation profiles produced 48/48 positive forward-minus-reverse order gaps and 48/48 forward CHSH violations.

## Appeal boundary

A successor appeal may replace only the erroneous ordered-list equality with a presence/content check over the three frozen profile names. It may not change any profile value, random seed, shot count, state, channel, operation, schedule, reconstruction, threshold, gate, result metric, or scientific interpretation. The original BOUNDARY result and release remain immutable.
