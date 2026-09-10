# CR018 A0, Chi, and Baryon Inventory Derivation

## Verdict

```text
CR018_PASS_A0_CHI_BARYON_INVENTORY_DERIVATION
```

## Derived Packet

```text
A0 = 0.026525823848649
mu_H = 2.666666666666667
chi = 0.070735530263065
Omega_b = 0.049299011266101
```

## Source Tests

```text
G219  — initial chi / matter-budget derivation; retained historical but reframed.
G219B — corrected combinatorial chi derivation.
G219C — Monte Carlo structural confirmation.
G305  — horizon quotient measure under symmetry axioms.
```

## Pass Conditions

| condition | pass |
|---|---:|
| free_parameters_zero | true |
| G219_original_passed_but_reframed | true |
| G219B_corrected_passed | true |
| G219C_monte_carlo_passed | true |
| G305_predictions_passed | true |
| G305_wrong_controls_passed | true |
| A0_identity | true |
| mu_H_identity | true |
| chi_identity | true |
| Omega_b_identity | true |
