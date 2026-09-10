# CR148 Validation

```text
source_hashes_ok = true
target_source_hash_ok = true
precommit_sealed_before_runner = true
runner_sealed_before_target_reveal = true
target_locked_before_reveal = true
json_parse_ok = true
hashes_verified = true
existing_artifacts_modified = false
forbidden_source_paths_opened = false
firewall_fields_false = true
queue_maintenance_performed_by_research_agent = false
forecast_generated = false
analytic_numerical_agreement = true
wrong_controls_sensitive_count = 6
sealed_utc = 2026-07-11T17:34:52Z
```

Validation failures:

```text
NONE
```

## Correction Note

The sealed runner execution at `2026-07-11T17:34:52Z` produced the PASS
scientific values and valid summary JSON, but its process exit was incorrectly
set to failure because the validation aggregator treated required `false`
fields and `free_parameters_introduced = 0` as generic falsy failures.

The failed execution artifacts were preserved in:

```text
FAILED_RUN_20260711_173452_VALIDATION_BOOLEAN_BUG
```

No scientific input, target comparator, geometry, tolerance, wrong control, or
residual was changed by this markdown correction.
