# CR006 Validation

| check | pass |
|---|---:|
| precommit was sealed before runner implementation/execution | true |
| target identity and geometry were locked before measurement reveal | true |
| JSON parses | true |
| source hashes match | true |
| no forbidden path was opened by research agent | true |
| all wrong controls executed | true |
| WC1-WC6 failed materially or by channel rule | true |
| WC7 near-surface diagnostic matched radial limit | true |
| no free parameter was introduced | true |
| no existing CR was modified | true |
| firewall fields are false | true |
| candidate hash was not requested or known | true |
| queue maintenance was not performed by research agent | true |
| forecast was not generated | true |
| exact-minus-weak passed precommitted gate | true |

## Verdict

```text
PASS_OPTICAL_CLOCK_ENDPOINT_HOLDOUT
```

## Hashes Verified During Runner

```text
precommit_sha256 = 73AE63A764F9B70EBAF865BC16EBE0A11F24C57C45571008811292AB50B8C953
target_identity_lock_sha256 = A6CEDD37FF8130B346F83E2524E06DA2F73D7330920C5E208A69F5B30B0CD795
geometry_lock_sha256 = CD63702E222E869688A36B42C0B6AEF2F99ACE1732CEF0A26EF608B5D1A66919
primary_source_sha256 = 7D4376361233F17082814D99CC46CD3263C9FEBFDBF273BB9BFBE9699723E2B3
runner_sha256 = 47E29CB7FD36E935DD858E7FD099C35284241DCC5EE852505F9DBB4EDA74F308
```

## Stop Condition

```text
one_cr_completed = true
queue_maintenance_performed = false
forecast_generated = false
sam_language_v0_3_consulted_during_development = false
```
