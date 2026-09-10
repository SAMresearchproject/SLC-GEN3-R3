# CR120Z Attempt 1 Execution Failure

## Status

`EXECUTION_FAILURE_NO_SCIENTIFIC_VERDICT`

The sealed quantum calculation reached artifact serialization, then stopped while writing `CR120Z_SUMMARY.json` because Python's standard JSON encoder could not serialize a NumPy `bool_` value.

```text
TypeError: Object of type bool is not JSON serializable
```

The failure occurred at `write_json(RELEASE / "CR120Z_SUMMARY.json", summary)`. No primary result or release manifest was emitted. The partial `release/` directory is retained exactly as generated and is not a valid release.

## Correction boundary

A successor may correct only conversion of NumPy scalar values to native Python JSON scalars. It may not change the input state, B analog, X1 analog, operation order, observables, Bell settings, controls, swapping construction, noise grid, thresholds, gates, or result language.

The original sealed runner remains unchanged.
