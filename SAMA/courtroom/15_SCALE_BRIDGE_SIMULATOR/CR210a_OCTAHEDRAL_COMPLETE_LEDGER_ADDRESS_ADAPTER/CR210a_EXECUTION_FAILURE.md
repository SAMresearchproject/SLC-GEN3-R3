# CR210a Execution Failure

## Status

`EXECUTION_FAILURE_BEFORE_STRUCTURAL_VERDICT`

The single frozen execution began through `tools/run_sam_test.py` and stopped while serializing the expected display value for precommitted check `C05_PARTITION_NONUNIQUENESS`.

The exception was:

```text
TypeError: Object of type set is not JSON serializable
```

The failing value was the already-frozen expected fingerprint `{(64, 63, 7, True, 12, 6)}`. The error occurred in `compact_json`; it did not arise from a source hash, structural count, graph incidence, wrong control, firewall, outcome, or binding result.

## Preservation decision

The parent contract states `same_run_repair = FORBIDDEN`, and the sealed precommit says, “No same-run repair is permitted.” Therefore:

- the runner was not patched;
- CR210a was not rerun;
- the original runner hash remains `094d39be033db8dfe7bd1b78c845abf8839dbba1f36b31987af3d3bfb7616d1a`;
- all partial artifacts remain preserved exactly as emitted;
- no structural PASS or scientific FAIL is assigned.

A corrected execution requires a separately named, separately preflighted, freshly precommitted successor record. Its candidate and scientific predictions must remain unchanged; only the serializer defect may be corrected.

## Firewall status

No Starbreaker outcome, workbook membership, F81 target, isotope table, binding field, or binding residual was opened.
