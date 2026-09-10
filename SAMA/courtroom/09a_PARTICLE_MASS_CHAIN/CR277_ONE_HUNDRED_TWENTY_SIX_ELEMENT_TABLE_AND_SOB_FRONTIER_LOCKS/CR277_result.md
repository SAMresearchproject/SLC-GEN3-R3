# CR277 — 126-Element Table and Frontier Forecast Locks

**Verdict:** **PASS**
**Branch:** 09a_PARTICLE_MASS_CHAIN
**Classification:** FORECAST_LOCK_CR (K1 reveal-against-frozen-envelope)
**Free parameters introduced:** 0
**Precommit:** `50c429d0df9f449be7278adeff10cecba9a606af39643b39d04c54354a4c10c9`
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

## Gates

| gate | requirement | result | status |
| --- | --- | --- | --- |
| G0 | CR274 model regression < 1e-3 MeV on 55 training | max |Δ| = 4.864e-05 MeV | PASS |
| G1 | 126 rows, all Z covered | 126 rows, 118 observed, 8 frontier | PASS |
| G2 | anchor B_u_final CR277 vs CR274 < 1e-3 MeV | see table below | PASS |
| G3 | 8 frontier rows per CR273 verbatim, all Z=N | 8 rows, all Z=N | PASS |
| G4 | AME parse vs CR248 masses < 1e-5 u | max |Δ| = 5.311e-06 u | PASS |
| G5 | precommit + input hashes + forbidden-file guard | forbidden opens = 0 | PASS |

## Anchor comparison (CR274 vs CR277)

G2 model-fidelity check: CR277 prediction matches CR274 prediction. Reported residuals differ across mass sources (CR248 for CR274, AME2020 for CR277) by ~5 mMeV for mid-mass isotopes; this is a mass-table version divergence, not a model divergence.

| isotope | CR277 pred | CR274 pred | |Δ pred| MeV | CR277 resid (AME) | CR274 resid (CR248) | ok |
| --- | --- | --- | --- | --- | --- | --- |
| O-16 | +5.6287 | +5.6287 | 1.606579e-05 | -0.8917 | -0.8917 | ✓ |
| Fe-56 | +61.8373 | +61.8373 | 2.683550e-05 | -1.2302 | -1.2320 | ✓ |
| Au-197 | +27.4215 | +27.4215 | 2.298083e-05 | +3.7183 | +3.7195 | ✓ |
| Pb-208 | +21.7483 | +21.7483 | 1.000000e-05 | +0.0002 | +0.0000 | ✓ |

## Whole-set observed metrics

**CR274 benchmark**: 50/55 within 5 MeV, all 55 within 8 MeV, combined RMS 2.72 MeV.

| subset | n | RMS MeV | MAE MeV | within 5 | within 8 | within 15 | within 30 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| all observed (Z=1..118) | 118 | 6.672 | 4.336 | 82 | 107 | 114 | 117 |
| light (Z=1..7) | 7 | 19.907 | 13.288 | 4 | 4 | 4 | 6 |
| mid (Z=8..82) | 75 | 4.145 | 3.289 | 54 | 72 | 75 | 75 |
| heavy (Z=83..118) | 36 | 5.752 | 4.777 | 24 | 31 | 35 | 36 |
| extended-only (not in CR274) | 78 | 7.974 | 5.447 | 45 | 67 | 74 | 77 |

These are reported evidence, not gated. The base K was fit on 55 isotopes spanning Z=8..92; extrapolation to lighter or heavier extended-set rows is empirical readout, not a claim.

## Frontier forecast locks (Z=119..126)

Z=N balanced-anchor family per CR273. No observation exists. Any future AME entry for these isotopes is a K1 reveal against the sealed prediction.

| Z | isotope | name | N | A | B_u_base (MeV) | op contribution (MeV) | B_u_final (MeV) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 119 | Hl-238 | Harlium | 119 | 238 | -379.217 | +0.000 | -379.217 |
| 120 | Bx-240 | Brockium | 120 | 240 | -334.877 | +0.000 | -334.877 |
| 121 | Uq-242 | Uniquium | 121 | 242 | -400.642 | +0.000 | -400.642 |
| 122 | Lm-244 | Liamium | 122 | 244 | -355.470 | +0.000 | -355.470 |
| 123 | Cp-246 | Cooperium | 123 | 246 | -421.636 | +0.000 | -421.636 |
| 124 | Ly-248 | Lindesium | 124 | 248 | -375.398 | +0.000 | -375.398 |
| 125 | Di-250 | Dorisium | 125 | 250 | -441.662 | +0.000 | -441.662 |
| 126 | Jd-252 | Jerroldium | 126 | 252 | -395.513 | +7.180 | -388.333 |

## Operator predicate firings (extended-set audit)

Rows in the 126-element table where any CR274 operator fires: **21**. Predicate mode extends CR274's training-family reach to any rep isotope satisfying the operator predicate.

| Z | isotope | ops fired | total op MeV | in CR274 training? |
| --- | --- | --- | --- | --- |
| 21 | Sc-45 | op_3d_odd | +6.965 | no |
| 23 | V-51 | op_3d_odd | +6.965 | no |
| 25 | Mn-55 | op_3d_odd | +6.965 | yes |
| 27 | Co-59 | op_3d_odd | +6.965 | yes |
| 29 | Cu-63 | op_3d_odd | +6.965 | yes |
| 41 | Nb-93 | op_ms_fill | -0.906 | no |
| 42 | Mo-98 | op_ms_fill | -2.719 | no |
| 43 | Tc-98 | op_ms_fill | -2.266 | no |
| 44 | Ru-102 | op_ms_fill | -3.625 | no |
| 45 | Rh-103 | op_ms_fill | -3.625 | no |
| 46 | Pd-106 | op_ms_fill | -4.531 | no |
| 47 | Ag-107 | op_ms_fill | -4.531 | yes |
| 48 | Cd-114 | op_ms_fill | -7.250 | no |
| 49 | In-115 | op_ms_fill | -7.250 | no |
| 50 | Sn-120 | op_ms_fill | -9.063 | yes |
| 57 | La-139 | op_82pre | -0.727 | no |
| 58 | Ce-140 | op_82pre | -2.909 | no |
| 59 | Pr-141 | op_82pre | -6.546 | no |
| 60 | Nd-142 | op_82pre | -11.637 | yes |
| 82 | Pb-208 | op_dm_sat | +7.180 | yes |
| 126 | Jd-252 | op_dm_sat | +7.180 | no |

## Full 126-row element table

| Z | sym | N | A | B_u_obs | B_u_final | resid | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | H | 0 | 1 | -7.289 | -36.979 | -29.690 | extended_observed |
| 2 | He | 2 | 4 | -2.425 | +16.133 | +18.558 | extended_observed |
| 3 | Li | 4 | 7 | -14.907 | -14.484 | +0.423 | extended_observed |
| 4 | Be | 5 | 9 | -11.348 | -13.489 | -2.140 | extended_observed |
| 5 | B | 6 | 11 | -8.668 | -11.020 | -2.353 | extended_observed |
| 6 | C | 6 | 12 | +0.000 | -0.644 | -0.644 | extended_observed |
| 7 | N | 7 | 14 | -2.863 | -42.074 | -39.211 | extended_observed |
| 8 | O | 8 | 16 | +4.737 | +5.629 | +0.892 | cr274_training |
| 9 | F | 10 | 19 | +1.487 | +3.497 | +2.009 | cr274_training |
| 10 | Ne | 10 | 20 | +7.042 | +6.686 | -0.356 | cr274_training |
| 11 | Na | 12 | 23 | +9.530 | +9.093 | -0.437 | cr274_training |
| 12 | Mg | 12 | 24 | +13.934 | +11.496 | -2.437 | cr274_training |
| 13 | Al | 14 | 27 | +17.197 | +15.404 | -1.792 | cr274_training |
| 14 | Si | 14 | 28 | +21.493 | +16.963 | -4.530 | cr274_training |
| 15 | P | 16 | 31 | +24.441 | +22.399 | -2.041 | cr274_training |
| 16 | S | 16 | 32 | +26.016 | +23.723 | -2.293 | cr274_training |
| 17 | Cl | 18 | 35 | +29.014 | +30.489 | +1.475 | cr274_training |
| 18 | Ar | 22 | 40 | +35.040 | +33.902 | -1.138 | cr274_training |
| 19 | K | 20 | 39 | +33.807 | +40.807 | +7.000 | extended_observed |
| 20 | Ca | 20 | 40 | +34.846 | +41.135 | +6.288 | cr274_training |
| 21 | Sc | 24 | 45 | +41.072 | +40.787 | -0.285 | extended_observed |
| 22 | Ti | 26 | 48 | +48.493 | +49.666 | +1.173 | cr274_training |
| 23 | V | 28 | 51 | +52.203 | +50.094 | -2.109 | extended_observed |
| 24 | Cr | 28 | 52 | +55.420 | +56.710 | +1.290 | cr274_training |
| 25 | Mn | 30 | 55 | +57.713 | +55.735 | -1.978 | cr274_training |
| 26 | Fe | 30 | 56 | +60.607 | +61.837 | +1.230 | cr274_training |
| 27 | Co | 32 | 59 | +62.230 | +62.307 | +0.077 | cr274_training |
| 28 | Ni | 30 | 58 | +60.229 | +62.297 | +2.069 | cr274_training |
| 29 | Cu | 34 | 63 | +65.580 | +67.480 | +1.900 | cr274_training |
| 30 | Zn | 34 | 64 | +66.004 | +70.216 | +4.212 | cr274_training |
| 31 | Ga | 38 | 69 | +69.328 | +66.815 | -2.513 | extended_observed |
| 32 | Ge | 42 | 74 | +73.422 | +75.905 | +2.482 | extended_observed |
| 33 | As | 42 | 75 | +73.034 | +71.278 | -1.756 | extended_observed |
| 34 | Se | 46 | 80 | +77.759 | +76.879 | -0.880 | extended_observed |
| 35 | Br | 44 | 79 | +76.068 | +76.117 | +0.049 | cr274_training |
| 36 | Kr | 48 | 84 | +82.439 | +82.647 | +0.207 | cr274_training |
| 37 | Rb | 48 | 85 | +82.167 | +78.565 | -3.603 | extended_observed |
| 38 | Sr | 50 | 88 | +87.922 | +88.155 | +0.233 | extended_observed |
| 39 | Y | 50 | 89 | +87.711 | +83.508 | -4.203 | cr274_training |
| 40 | Zr | 50 | 90 | +88.773 | +94.269 | +5.496 | cr274_training |
| 41 | Nb | 52 | 93 | +87.213 | +87.314 | +0.101 | extended_observed |
| 42 | Mo | 56 | 98 | +88.116 | +93.167 | +5.051 | extended_observed |
| 43 | Tc | 55 | 98 | +86.432 | +82.018 | -4.414 | extended_observed |
| 44 | Ru | 58 | 102 | +89.106 | +96.545 | +7.439 | extended_observed |
| 45 | Rh | 58 | 103 | +88.032 | +91.479 | +3.447 | extended_observed |
| 46 | Pd | 60 | 106 | +89.908 | +98.811 | +8.903 | extended_observed |
| 47 | Ag | 60 | 107 | +88.407 | +93.098 | +4.691 | cr274_training |
| 48 | Cd | 66 | 114 | +90.015 | +91.817 | +1.802 | extended_observed |
| 49 | In | 66 | 115 | +89.536 | +88.495 | -1.041 | extended_observed |
| 50 | Sn | 70 | 120 | +91.098 | +88.751 | -2.347 | cr274_training |
| 51 | Sb | 70 | 121 | +89.599 | +94.619 | +5.020 | extended_observed |
| 52 | Te | 78 | 130 | +87.353 | +78.049 | -9.304 | extended_observed |
| 53 | I | 74 | 127 | +88.983 | +91.724 | +2.741 | cr274_training |
| 54 | Xe | 78 | 132 | +89.279 | +89.700 | +0.421 | cr274_training |
| 55 | Cs | 78 | 133 | +88.071 | +87.373 | -0.698 | cr274_training |
| 56 | Ba | 82 | 138 | +88.262 | +84.489 | -3.773 | cr274_training |
| 57 | La | 82 | 139 | +87.222 | +81.716 | -5.506 | extended_observed |
| 58 | Ce | 82 | 140 | +88.074 | +89.870 | +1.796 | extended_observed |
| 59 | Pr | 82 | 141 | +86.015 | +82.485 | -3.529 | extended_observed |
| 60 | Nd | 82 | 142 | +85.950 | +85.950 | -0.000 | cr274_training |
| 61 | Pm | 84 | 145 | +81.268 | +87.252 | +5.984 | extended_observed |
| 62 | Sm | 90 | 152 | +74.763 | +76.940 | +2.177 | cr274_training |
| 63 | Eu | 90 | 153 | +73.367 | +74.195 | +0.828 | extended_observed |
| 64 | Gd | 94 | 158 | +70.690 | +68.928 | -1.762 | cr274_training |
| 65 | Tb | 94 | 159 | +69.533 | +66.575 | -2.958 | extended_observed |
| 66 | Dy | 98 | 164 | +65.968 | +60.494 | -5.474 | extended_observed |
| 67 | Ho | 98 | 165 | +64.898 | +58.526 | -6.372 | extended_observed |
| 68 | Er | 98 | 166 | +64.924 | +67.935 | +3.010 | cr274_training |
| 69 | Tm | 100 | 169 | +61.275 | +57.894 | -3.381 | extended_observed |
| 70 | Yb | 104 | 174 | +56.945 | +52.040 | -4.904 | extended_observed |
| 71 | Lu | 104 | 175 | +55.166 | +49.901 | -5.264 | extended_observed |
| 72 | Hf | 108 | 180 | +49.779 | +43.751 | -6.029 | extended_observed |
| 73 | Ta | 108 | 181 | +48.439 | +42.010 | -6.429 | extended_observed |
| 74 | W | 110 | 184 | +45.705 | +43.902 | -1.803 | cr274_training |
| 75 | Re | 112 | 187 | +41.217 | +34.330 | -6.886 | extended_observed |
| 76 | Os | 116 | 192 | +35.882 | +27.911 | -7.972 | extended_observed |
| 77 | Ir | 116 | 193 | +34.536 | +26.901 | -7.636 | extended_observed |
| 78 | Pt | 117 | 195 | +32.794 | +27.192 | -5.602 | extended_observed |
| 79 | Au | 118 | 197 | +31.140 | +27.421 | -3.718 | cr274_training |
| 80 | Hg | 122 | 202 | +27.345 | +21.876 | -5.469 | cr274_training |
| 81 | Tl | 124 | 205 | +23.821 | +13.266 | -10.555 | extended_observed |
| 82 | Pb | 126 | 208 | +21.749 | +21.748 | -0.000 | cr274_training |
| 83 | Bi | 126 | 209 | +18.259 | +12.266 | -5.993 | extended_observed |
| 84 | Po | 125 | 209 | +16.366 | +16.436 | +0.070 | extended_observed |
| 85 | At | 125 | 210 | +11.972 | +11.342 | -0.630 | extended_observed |
| 86 | Rn | 136 | 222 | -16.372 | -24.854 | -8.482 | extended_observed |
| 87 | Fr | 136 | 223 | -18.382 | -25.828 | -7.446 | extended_observed |
| 88 | Ra | 138 | 226 | -23.668 | -26.376 | -2.709 | extended_observed |
| 89 | Ac | 138 | 227 | -25.850 | -27.864 | -2.014 | extended_observed |
| 90 | Th | 142 | 232 | -35.447 | -37.795 | -2.348 | cr274_training |
| 91 | Pa | 140 | 231 | -33.424 | -30.383 | +3.041 | extended_observed |
| 92 | U | 146 | 238 | -47.308 | -49.588 | -2.280 | cr274_training |
| 93 | Np | 144 | 237 | -44.872 | -41.790 | +3.082 | extended_observed |
| 94 | Pu | 150 | 244 | -59.806 | -62.213 | -2.407 | extended_observed |
| 95 | Am | 148 | 243 | -57.175 | -54.069 | +3.106 | extended_observed |
| 96 | Cm | 151 | 247 | -65.533 | -65.373 | +0.160 | extended_observed |
| 97 | Bk | 150 | 247 | -65.490 | -58.439 | +7.051 | extended_observed |
| 98 | Cf | 153 | 251 | -74.135 | -69.938 | +4.197 | extended_observed |
| 99 | Es | 153 | 252 | -77.295 | -73.166 | +4.129 | extended_observed |
| 100 | Fm | 157 | 257 | -88.590 | -85.104 | +3.486 | extended_observed |
| 101 | Md | 157 | 258 | -91.690 | -88.474 | +3.217 | extended_observed |
| 102 | No | 157 | 259 | -94.079 | -82.815 | +11.264 | extended_observed |
| 103 | Lr | 163 | 266 | -111.662 | -115.161 | -3.499 | extended_observed |
| 104 | Rf | 163 | 267 | -113.444 | -109.186 | +4.258 | extended_observed |
| 105 | Db | 163 | 268 | -117.060 | -113.462 | +3.598 | extended_observed |
| 106 | Sg | 163 | 269 | -119.692 | -108.864 | +10.828 | extended_observed |
| 107 | Bh | 163 | 270 | -124.230 | -114.468 | +9.762 | extended_observed |
| 108 | Hs | 169 | 277 | -141.375 | -137.287 | +4.088 | extended_observed |
| 109 | Mt | 169 | 278 | -145.767 | -142.389 | +3.378 | extended_observed |
| 110 | Ds | 171 | 281 | -153.273 | -147.814 | +5.459 | extended_observed |
| 111 | Rg | 171 | 282 | -157.742 | -153.583 | +4.159 | extended_observed |
| 112 | Cn | 173 | 285 | -165.086 | -159.296 | +5.790 | extended_observed |
| 113 | Nh | 173 | 286 | -169.957 | -165.699 | +4.258 | extended_observed |
| 114 | Fl | 175 | 289 | -177.465 | -171.641 | +5.825 | extended_observed |
| 115 | Mc | 175 | 290 | -182.792 | -178.640 | +4.152 | extended_observed |
| 116 | Lv | 177 | 293 | -190.568 | -184.745 | +5.823 | extended_observed |
| 117 | Ts | 177 | 294 | -196.396 | -192.301 | +4.095 | extended_observed |
| 118 | Og | 176 | 294 | -199.320 | -183.421 | +15.899 | extended_observed |
| 119 | Hl | 119 | 238 | — | -379.217 | — | frontier_forecast |
| 120 | Bx | 120 | 240 | — | -334.877 | — | frontier_forecast |
| 121 | Uq | 121 | 242 | — | -400.642 | — | frontier_forecast |
| 122 | Lm | 122 | 244 | — | -355.470 | — | frontier_forecast |
| 123 | Cp | 123 | 246 | — | -421.636 | — | frontier_forecast |
| 124 | Ly | 124 | 248 | — | -375.398 | — | frontier_forecast |
| 125 | Di | 125 | 250 | — | -441.662 | — | frontier_forecast |
| 126 | Jd | 126 | 252 | — | -388.333 | — | frontier_forecast |

## Provenance

- Precommit SHA256: `50c429d0df9f449be7278adeff10cecba9a606af39643b39d04c54354a4c10c9`
- AME2020 mass_1.mas20 SHA256: `e8599c6d7f724fac91934e59f1b9de8fb8f63e820f4b39456b790665ed2a3307` (fetched from https://amdc.impcas.ac.cn/masstables/Ame2020/mass_1.mas20; Chinese Physics C 45, 030002 (2021))
- CR274 summary.json SHA256: `c46843357aa7fe681c602b3c5e75fa7504f6b0bbec2bcfa5961bdd76d47e854d`
- CR274 residuals.csv SHA256: `ec71a6c2f8cf5bed0f1ec64efb7f57a394e6cef8f9ad3fe268d528009a8476e5`
- CR250 SOB126_ledger.csv SHA256: `3bfdd083457b187c156bf331b2997bb904be1f45adb335a724c12100d9c6e72b`
- CR248 train_lane_a.csv SHA256: `54c2c28d869b71cd19f4989866b9db49881ace1d38c36b67b846dbfda9da5efc`
- CR248 test_holdout.csv SHA256: `8a5253f61067e1a22158257c6f77c39f722036f2f06bd701e041126e404016f8`
- Stewardship SHA256: `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

## Verdict statement

CR277 verdict: **PASS**. The frozen CR274 binding-closure model (base K + 4 gated operators) is applied to a canonical 126-element table with zero refit. The eight Z=119..126 rows constitute K1 forecast locks per the CR273 Z=N balanced-anchor family (Harlium, Brockium, Uniquium, Liamium, Cooperium, Lindesium, Dorisium, Jerroldium).
