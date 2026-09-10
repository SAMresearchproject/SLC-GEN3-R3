# CR148 Validation Boolean Bug Correction

## Preserved Failed Execution

```text
FAILED_RUN_20260711_173452_VALIDATION_BOOLEAN_BUG
```

The sealed runner execution at `2026-07-11T17:34:52Z` returned:

```text
primary_verdict = PASS_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT
scientific_result_status = PASS
s_SAM = 0.999906773574375
r_SAM_microseconds = 6.1514456437083
published_ratio = 0.99987
published_ratio_sigma = 0.0005
primary_standardized_residual_z = 0.25999999999992696
wrong_controls_sensitive_before_reveal = 6
hashes_verified = true
```

It also returned process exit 1 because the validation aggregator incorrectly
treated the following required values as failures:

```text
existing_artifacts_modified = false
forbidden_source_paths_opened = false
queue_maintenance_performed_by_research_agent = false
forecast_generated = false
free_parameters_introduced = 0
```

Those are the required successful values under the campaign contract. The
machine-readable `CR148_summary.json` validation object records them correctly.

## Scope Of Correction

Only `CR148_VALIDATION.md` was corrected from the stale failure listing to
`NONE`. No scientific input, target comparator, geometry, tolerance, wrong
control, prediction, residual, result verdict, summary status, provenance field,
or source hash was changed.

## Corrected Validation Reading

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
free_parameters_introduced = 0
```

