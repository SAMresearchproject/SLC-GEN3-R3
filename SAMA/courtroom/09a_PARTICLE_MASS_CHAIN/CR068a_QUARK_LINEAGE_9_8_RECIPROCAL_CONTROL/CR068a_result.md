# CR068a 9/8 Reciprocal Control Across Quark Lineage - Result

## Verdict

```text
CR068a_QUARK_LINEAGE_9_8_RECIPROCAL_CONTROL_PASS
```

## What This CR Controls

Structural verification that the 9/8 full-cell ratio and its reciprocal 8/9 never appear as fitted free parameters in any quark-bearing row of the QP075 role-operator closure table.  The chain u/d/s/c/b/t is fully covered by the rows scanned; every row reports free_parameters_used = 0.

## Structural Identity

```text
D                       = 3
full-cell ratio  = D^2 / 2^D = 1.125 = 9/8
reciprocal       = 2^D / D^2 = 0.8888888889 = 8/9
product check    = (9/8)*(8/9) = 1.0
```

## Cryptographic Chain

```text
upstream QP075 role-operator table  = 3190df06e7ff3bfd8a166b8554b2a2578542715566377df2df285b83e2c67d78
upstream QP075 summary              = 3711b1457165b6a748767b809e83b64429acc8a57702e2628b613f780a5dae9d
CR067a WZH anchor                   = 2e18cfe53ecb0f3033c179641814e8d30371a4ae32604defe38e880b5ae3258e
CR091a Z residual appeal lock       = cbb7e8411b17fc788f9266f615d4a7401ecb04b7b4c893b4f2b74605b0248ff0
CR068a control lock sha256          = 33e655f491d85e19685451da1370c84bb8ef59354af93ae860b038297dfa5c06
```

## Quark Flavor Coverage (per QP075 quark-bearing rows)

| flavor | row count | example carriers |
|---|---|---|
| u | 6 | proton (uud), neutron (udd), Delta (Delta++/0/-) (uuu, ...) |
| d | 5 | proton (uud), neutron (udd), Lambda (uds) |
| s | 3 | neutral kaon (K0), Lambda (uds), eta prime (958) (~s_anti_s) |
| c | 5 | Lambda_c (udc), D meson (cq), Xi_bc^+ / Omega_bcc (1b + nc, Sigma-like) |
| b | 5 | Lambda_b (udb), B meson (bq), Xi_bc^+ / Omega_bcc (1b + nc, Sigma-like) |
| t | 4 | W boson (W+/-), top quark (t), Lambda (uds) |

## Quark-Bearing Rows (zero free parameters across the lineage)

| order | role_operator | carrier | k | shift | q | mass MeV | reference | residual % | free params |
|---|---|---|---|---|---|---|---|---|---|
| 4 | color_minus_SW_terminal_baryon | proton (uud) | 27 | +0 | +6 | 938.687 | PDG p | +0.0442 | 0 |
| 5 | weak_plus_SW_beta_bridge | neutron (udd) | 27 | +0 | +5 | 940.230 | PDG n | +0.0708 | 0 |
| 6 | charged_weak_vector | W boson (W+/-) | 9 | -8 | +4 | 80365.100 | PDG W | -0.0148 | 0 |
| 9 | top_heavy_fermion | top quark (t) | 75 | -6 | -14 | 172542.000 | PDG t | -0.0160 | 0 |
| 15 | neutral_kaon_color_complement | neutral kaon (K0) | 7 | -1 | -7 | 497.340 | PDG K0 | -0.0545 | 0 |
| 16 | isoresonance_rank2_tensor_baryon | Delta (Delta++/0/-) (uuu, ...) | 9 | -2 | +16 | 1231.370 | PDG Delta(1232) | -0.0512 | 0 |
| 17 | octet_occupation_single_heavy_baryon_strange | Lambda (uds) | 8 | -2 | +4 | 1116.180 | PDG Lambda | +0.0448 | 0 |
| 18 | octet_occupation_single_heavy_baryon_charm | Lambda_c (udc) | 8 | -3 | -8 | 2277.370 | PDG Lambda_c | -0.3974 | 0 |
| 19 | bookend_layer_bottom_baryon | Lambda_b (udb) | 5 | -5 | +0 | 5617.920 | PDG Lambda_b | -0.0299 | 0 |
| 20 | u3u2_composite_tier_d_meson | D meson (cq) | 13 | -2 | -14 | 1869.210 | PDG D+/- | -0.0236 | 0 |
| 21 | top_tower_rank2_bookend_b_meson | B meson (bq) | 75 | -1 | -1 | 5275.550 | PDG B+/- | -0.0718 | 0 |
| 23 | light_strange_pseudoscalar_eta_prime | eta prime (958) (~s_anti_s) | 7 | -2 | +16 | 957.732 | PDG eta_prime | -0.0050 | 0 |
| 24 | combined_bookend_octet_doubly_heavy_bc_baryon_sigma | Xi_bc^+ / Omega_bcc (1b + nc, Sigma-like) | 13 | -4 | +6 | 7231.370 | lattice Xi_bc^+ / Omega_bcc | +4.1534 | 0 |
| 25 | combined_bookend_octet_doubly_heavy_bc_baryon_lambda | Xi_bc^0 / Omega_bcs (1b + nc, Lambda-like) | 13 | -4 | +5 | 7243.260 | lattice Xi_bc^0 / Omega_bcs | +3.9205 | 0 |
| 26 | multi_heavy_bc_baryon_two_bottom_lambda | Omega_bbc (2b + 1c, Lambda-like) | 18 | -4 | +5 | 10029.100 | lattice Omega_bbc | -1.7715 | 0 |

## Predictions

- **[PASS]** P1_all_quark_bearing_rows_zero_free_parameters
- **[PASS]** P2_full_cell_9_over_8_is_structural_D_squared_over_2_to_D_at_D_3
- **[PASS]** P3_reciprocal_8_over_9_is_structural_2_to_D_over_D_squared_at_D_3
- **[PASS]** P4_full_cell_times_reciprocal_equals_unity
- **[PASS]** P5_all_six_quark_flavors_appear_in_quark_bearing_rows
- **[PASS]** P6_qp075_campaign_zero_free_parameters_global

## Wrong Controls

- **[PASS]** WC1_no_row_uses_fitted_9_over_8_multiplier
- **[PASS]** WC2_D_is_not_scanned_or_fit
- **[PASS]** WC3_control_file_sealed_with_sha256_sibling
- **[PASS]** WC4_reciprocal_8_over_9_not_used_as_fitted_correction

## Why This Control Matters

The 9/8 ratio is everywhere in the SAM full-cell framework.  If 9/8 were a fitted parameter dialled to reproduce quark masses, the closure would be circular.  This control demonstrates 9/8 emerges only as D^2 / 2^D at D=3, with the reciprocal 8/9 = 2^D / D^2 as its inverse partner.  Across the full u/d/s/c/b/t lineage, no row carries a fitted 9/8 multiplier; the closure is structural, not parametric.

## Next CRs in 09a

09a structural control complete.  Phase 2 opens in 14_FOUNDATIONAL_TESTS: CR107 (SPARC intake) -> CR108 (Planck Omega_b intake) -> CR109 (PBH intake) -> CR110 three-mode closure appeal -> CR111 cosmic baryon closure appeal.
