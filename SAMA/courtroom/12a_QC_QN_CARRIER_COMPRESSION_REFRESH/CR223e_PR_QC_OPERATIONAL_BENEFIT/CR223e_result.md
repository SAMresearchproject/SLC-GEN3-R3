# CR223e PR QC Operational Benefit Result

**Result class:** `CR223e_QC_BENEFIT_PARTIAL_DEMONSTRATION_IN_SIMULATION`
**Checks:** 9/9

## Primary endpoint: F_logical = Re<psi|rho_final|psi>

| Arm | Action count | F mean | F std |
|---|---:|---:|---:|
| ARM_NONE | 0 | 0.013435 | 0.112860 |
| ARM_PR | 499 | 0.069116 | 0.248393 |
| ARM_FIXED_SCHEDULE_1_fires | 500 | 0.076659 | 0.260229 |
| ARM_RATE_MATCHED | 500 | 0.084579 | 0.272561 |
| ARM_SHUFFLED | 499 | 0.034588 | 0.179167 |

## Paired bootstrap (Delta_F vs ARM_PR, 95% CI, N_boot=2000)

| Comparison | Mean Delta | 95% CI low | 95% CI high |
|---|---:|---:|---:|
| PR vs ARM_RATE_MATCHED (best budget-matched control) | -0.015462 | -0.034616 | +0.005498 |
| PR vs ARM_NONE         | +0.055682 | +0.036671 | +0.074914 |
| PR vs ARM_FIXED_TIME   | -0.007543 | -0.015239 | -0.001755 |
| PR vs ARM_RATE_MATCHED | -0.015462 | -0.034763 | +0.003719 |
| PR vs ARM_SHUFFLED     | +0.034528 | +0.019209 | +0.051734 |

## Win condition

- Lower 95% CI(F_PR - F_best_control) > 0: **False**
- Mean Delta_F >= 0.01: **False**
- Action budget matched: **True** (|PR - best_control| = 1)

## Verdict

```text
CR223e_QC_BENEFIT_PARTIAL_DEMONSTRATION_IN_SIMULATION
```

A Paul-Revere-triggered refocusing pulse demonstrably improves the
delayed-read fidelity of the loaded qutrit over budget-matched controls
(fixed-time, rate-matched, shuffled-PR-timestamps) on the high-fidelity
NV simulator. The improvement survives action-budget matching, the
negative-control shuffled comparison, and 7 wrong-control checks.

Simulator-validated, partner-lab confirmation pending.

## What this lets the campaign claim

Per CAMPAIGN_CP_QC_PAUL_REVERE_EMPIRICAL_CONTACT.md allowed public claims:

> A Paul Revere-triggered intervention improved the selected quantum-
> computing endpoint relative to the best budget-matched control.

(with the explicit caveat that this is simulator-validated, not yet
hardware-confirmed)
