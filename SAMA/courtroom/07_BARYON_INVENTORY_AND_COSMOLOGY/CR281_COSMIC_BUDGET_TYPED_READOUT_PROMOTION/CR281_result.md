# CR281 Cosmic-Budget Typed-Readout Promotion Result

generated_utc: 2026-07-11T08:28:34+00:00
primary_verdict: PASS_COSMIC_BUDGET_TYPED_READOUT
execution_status: CLEAN

## Structural Inventory

```text
A0 = 1/(pi*R)
chi = (S/D)*A0
Omega_b = alpha_H*A0*(1-chi)
Omega_m = R*A0 = 1/pi
Omega_c = Omega_m - Omega_b
Omega_Lambda = 1 - Omega_m
```

- A0: 0.02652582384864922427
- chi: 0.07073553026306458880
- Omega_b: 0.04929901126610075623
- Omega_m: 0.31830988618379069122
- Omega_c: 0.26901087491768993498
- Omega_Lambda: 0.68169011381620925327
- Omega_m_eff (separate refinement): 0.31376091556905721935

## Physical-Density Cascade

```text
eta = (M/(alpha_H^2*Theta))*A0^6
omega_b = eta / K(T_CMB)
h^2 = omega_b / Omega_b
H0 = 100*sqrt(h^2)
```

- eta: 6.096089524484197716e-10
- K(T_CMB): 2.734158604426320018e-08
- omega_b: 0.022296034745809035
- h^2: 0.452261296387101219
- H0: 67.250375195020 km/s/Mpc

K(T_CMB) source: CR036@19 computed from FIRAS T_CMB=2.7255 K plus CODATA/SI constants. Planck values are comparators only.

## Implementation Note

The initial CR281 execution at PREFLIGHT_20260711_032722 failed because the runner checked CR114_summary.json for free_parameters_total. The precommitted source containing that field is CR114_cosmic_baryon_bridge.json; the lookup was corrected without changing the verdict tree.

## Wrong Controls

- [PASS] WC1_A0_zero_rejected
- [PASS] WC2_remove_one_minus_chi_rejected
- [PASS] WC3_noncanonical_R_or_D_rejected
- [PASS] WC4_Omega_m_eff_not_clean_Omega_m_spine
- [PASS] WC5_Planck_omega_b_comparator_not_input
- [PASS] WC6_unsourced_K_rejected
- [PASS] WC7_Omega_b_not_omega_b

## Boundaries Preserved

- Omega_m_eff is not substituted for the clean Omega_m=1/pi spine.
- CR117 CMB law/configuration boundary remains intact.
- No CMB spectrum campaign, forecast, or new bridge is generated.

## Verdict Statement

PASS_COSMIC_BUDGET_TYPED_READOUT. The cosmic budget is promoted as a typed readout from A0 through Omega_b/Omega_m and, through sealed CR036 support, eta, omega_b, h^2, and H0.
