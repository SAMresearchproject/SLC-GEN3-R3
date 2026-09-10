# CR120ZA Precommit — CR120Z Serialization-Only Successor

CR120Z attempt 1 is preserved as `EXECUTION_FAILURE_NO_SCIENTIFIC_VERDICT`. It completed the deterministic calculations but stopped while JSON attempted to serialize a NumPy boolean.

This successor imports the exact sealed attempt-1 runner. It changes no scientific calculation. The sole correction replaces the JSON writer with one that converts NumPy scalar values using `.item()` before standard JSON encoding.

Every input state, operation, order, observable, control, Bell setting, swapping construction, visibility grid, threshold, gate, result sentence, and boundary remains byte-for-byte supplied by the original runner implementation.

The successor uses a new folder, source manifest, contract, precommit, seal, and wrapper hash. It does not overwrite the failed attempt or its partial output.

No same-run scientific repair, refit, exclusion, or registry mutation is permitted.
