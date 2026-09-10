# CR064a Particle Mass Chain Branch Verdict

## Verdict

```text
CR064a_PASS_QP075_PARTICLE_MASS_CHAIN_BRANCH_RERUN
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS_QP075_PARTICLE_MASS_CHAIN_BRANCH_RERUN
triage_bin = A
```

## Reason

```text
CR059a-CR063a all pass from QP075; the corrected branch exports the 35-row, 26-role-operator, zero-free-parameter particle surface.
```

## Prior CR Chain

| CR | Verdict | Status |
|---|---|---|
| CR059a | PASS_QP075_ALLOWED_INPUTS_AND_LATEST_SOURCE_LOCK | PASS |
| CR060a | PASS_QP075_SELECTOR_PROVENANCE_AND_FORBIDDEN_TARGETS | PASS |
| CR061a | PASS_QP075_MASS_CHAIN_REPRODUCTION | PASS |
| CR062a | PASS_QP075_ROW_BY_ROW_PARTICLE_LEDGER_35_ROWS | PASS |
| CR063a | PASS_WRONG_CONTROLS_AND_OLDER_FREEZE_MISROUTE_QUARANTINE | PASS |

## Branch Claim

See `CR064a_branch_strongest_claim.md`.

## Rule-9 Line

```text
This branch zipper could have falsified the corrected 09a particle branch if
any prior CR was missing, non-clean, non-PASS, or if QP075 failed to export the
35-row / 26-operator / zero-free-parameter branch state.
```
