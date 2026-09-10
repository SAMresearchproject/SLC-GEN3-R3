# CR249 Binding as Substrate-Atom Connection-Fee Sum — Result

**Verdict:** `FAIL`
**Started:** 2026-06-25T00:03:39+00:00
**Completed:** 2026-06-25T00:03:39+00:00
**Dataset:** CR242_binding_dataset.csv (69 nuclei)
**Best rule:** `R1_per_excess_neutron`
**Best max |Δ|:** 89.85 MeV (target: 0.005 MeV)

## The question this CR answered

Per Sean's 2026-06-24 framing: tensor carriers are substrate atoms that
carry zero mass but produce a mass-lift, and the sum of these lifts across
a nucleus's substrate-atom connections IS the binding curvature B_u.
CR249 tests whether the connection-fee formula structure verified at the
particle level by CR009 ((R+q+D)/R triadic, (q+D)/R⁴ pair) extends to
derive B_u for all 71 nuclei in the CR242 binding dataset with zero free
parameters and max |Δ| ≤ 0.005 MeV.

## Candidate rules tested (all locked above the line)

| Rule | Formula |
|---|---|
| `R1_per_excess_neutron` | `(N-Z)·(F·S-1+D)/R^4·μ_Q` |
| `R2_per_A_volume` | `A·D/R^4·μ_Q` |
| `R3_per_pn_pair` | `Z·N·(1+D)/R^4·μ_Q` |
| `R4_channel_gap_linear` | `(N-Z)·7093/(7117·R^4)` |
| `R5_asymmetry_squared` | `(N-Z)^2/A·1/(R·D)·7093^2/7117^2` |
| `R6_volume_plus_asym_squared` | `R2 + R5` |

All formulas use only CR238 substrate atoms and named derived rationals.
Zero fitted parameters in any rule.

## Rule-by-rule comparison

| Rule | n | max |Δ| MeV | mean |Δ| MeV | RMS MeV | exact | close | approx | miss |
|---|---|---|---|---|---|---|---|---|
| R1_per_excess_neutron | 69 | 89.85 | 33.46 | 43.64 | 0 | 1 | 1 | 67 |
| R2_per_A_volume | 69 | 90.66 | 38.46 | 48.22 | 0 | 0 | 1 | 68 |
| R3_per_pn_pair | 69 | 112.4 | 34.51 | 45.50 | 0 | 0 | 3 | 66 |
| R4_channel_gap_linear | 69 | 90.20 | 38.30 | 48.03 | 0 | 0 | 1 | 68 |
| R5_asymmetry_squared | 69 | 362.2 | 64.37 | 106.8 | 0 | 0 | 2 | 67 |
| R6_volume_plus_asym_squared | 69 | 363.1 | 64.52 | 107.1 | 0 | 0 | 1 | 68 |

**Sean's target ceiling:** max |Δ| ≤ 0.005 MeV across all 71 nuclei.

## Best rule — per-nucleus detail

Best: **`R1_per_excess_neutron`** — formula `(N-Z)·(F·S-1+D)/R^4·μ_Q`

**Top 10 worst residuals (descending |Δ|):**

| isotope | Z | N | A | B_u_obs (u) | B_u_pred (u) | Δ (u) | Δ (MeV) | class |
|---|---|---|---|---|---|---|---|---|
| U-238 | 92 | 146 | 238 | -0.0507883 | 0.0456653 | -0.0964536 | -89.85 | systematic_miss |
| U-235 | 92 | 143 | 235 | -0.0439299 | 0.0431283 | -0.0870583 | -81.09 | systematic_miss |
| Zr-90 | 40 | 50 | 90 | 0.0953012 | 0.00845654 | 0.0868447 | 80.90 | systematic_miss |
| Y-89 | 39 | 50 | 89 | 0.0941618 | 0.00930219 | 0.0848597 | 79.05 | systematic_miss |
| Ag-107 | 47 | 60 | 107 | 0.0949032 | 0.0109935 | 0.0839097 | 78.16 | systematic_miss |
| U-234 | 92 | 142 | 234 | -0.0409503 | 0.0422827 | -0.0832330 | -77.53 | systematic_miss |
| Th-232 | 90 | 142 | 232 | -0.0380540 | 0.0439740 | -0.0820280 | -76.41 | systematic_miss |
| Sn-120 | 50 | 70 | 120 | 0.0977984 | 0.0169131 | 0.0808853 | 75.34 | systematic_miss |
| Kr-84 | 36 | 48 | 84 | 0.0885023 | 0.0101478 | 0.0783544 | 72.99 | systematic_miss |
| I-127 | 53 | 74 | 127 | 0.0955281 | 0.0177587 | 0.0777694 | 72.44 | systematic_miss |

**Best 10 (smallest |Δ|):**

| isotope | Z | N | A | B_u_obs (u) | B_u_pred (u) | Δ (u) | Δ (MeV) | class |
|---|---|---|---|---|---|---|---|---|
| C-14 | 6 | 8 | 14 | -0.00324199 | 0.00169131 | -0.00493330 | -4.595 | systematic_miss |
| C-13 | 6 | 7 | 13 | -0.00335484 | 0.000845654 | -0.00420049 | -3.913 | systematic_miss |
| N-14 | 7 | 7 | 14 | -0.00307400 | 0 | -0.00307400 | -2.863 | systematic_miss |
| He-4 | 2 | 2 | 4 | -0.00260325 | 0 | -0.00260325 | -2.425 | systematic_miss |
| Hg-200 | 80 | 120 | 200 | 0.0316741 | 0.0338262 | -0.00215205 | -2.005 | systematic_miss |
| N-15 | 7 | 8 | 15 | -0.000108898 | 0.000845654 | -0.000954552 | -0.8892 | systematic_miss |
| O-18 | 8 | 10 | 18 | 0.000840387 | 0.00169131 | -0.000850921 | -0.7926 | systematic_miss |
| F-19 | 9 | 10 | 19 | 0.00159684 | 0.000845654 | 0.000751183 | 0.6997 | systematic_miss |
| Au-197 | 79 | 118 | 197 | 0.0334312 | 0.0329805 | 0.000450704 | 0.4198 | approximate_match |
| O-17 | 8 | 9 | 17 | 0.000868244 | 0.000845654 | 0.0000225896 | 0.02104 | close_match |

## Cascade-cited anchor nuclei (Au-197, C-12, C-13)

| isotope | rule | Z | N | A | B_u_obs (u) | B_u_pred (u) | Δ (MeV) | class |
|---|---|---|---|---|---|---|---|---|
| Au-197 | R1_per_excess_neutron | 79 | 118 | 197 | 0.0334312 | 0.0329805 | 0.4198 | approximate_match |
| C-13 | R1_per_excess_neutron | 6 | 7 | 13 | -0.00335484 | 0.000845654 | -3.913 | systematic_miss |

## Wrong controls

- **WC-1_shuffle_BZN**: passed=False
  - perturb max |Δ|: 88.98 MeV vs best 89.85 MeV (ratio 0.9904)
- **WC-2_perturb_R_10**: passed=False
  - perturb max |Δ|: 135.5 MeV vs best 89.85 MeV (ratio 1.508)
- **WC-3_perturb_D_2**: passed=False
  - perturb max |Δ|: 89.78 MeV vs best 89.85 MeV (ratio 0.9993)
- **WC-4_substrate_atom_integrity**: passed=True

## Verdict logic

- Best rule max |Δ| MeV: 89.85
- Target ceiling: 0.005 MeV
- All WC pass: False
- Verdict: `FAIL`

## Provenance chain

- Dataset: `CR242_binding_dataset.csv` (71 nuclei AME2020-derived)
- Particle-level formula: CR009 PASS (charged-triadic + charged-pair)
- Substrate atoms: CR238 (R, D, S, Θ, ℱ, V, M, κ, g)
- Per-rule predictions: `CR249_per_row_predictions.csv`
- Aggregate metrics: `CR249_rule_comparison.csv`
- Wrong controls: `CR249_wrong_controls.csv`
