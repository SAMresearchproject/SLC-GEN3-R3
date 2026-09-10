# CR274 — Gated Nuclear-Readout Operators for CR261 Binding Closure

**Verdict:** PASS
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`
**Precommit:** `c09616e40e26f7d2df36350b0f3db62c7da81b17e01ce7607a1ed87c8431c3a9`

---

## Gates

| gate | requirement | result | status |
| --- | --- | --- | --- |
| G0 | cipher exact on all 55 | max|dev|=num=0, den=1 | PASS |
| G1 | base Model K RMS ≤ 4.5 MeV | 3.9102 | PASS |
| G2 | ≥3 of 4 operators pass | 4/4 | PASS |
| G3 | combined RMS ≤ 3.5 MeV | 2.7160 | PASS |
| G4 | ≥45/55 within 5 MeV | 50/55 | PASS |
| G5 | anchors within 10 MeV | O-16=-0.892, Fe-56=-1.232, Au-197=+3.719, Pb-208=+0.000 | PASS |
| G6 | hashes + whitelist | precommit/input verified | PASS |

## Model K coefficients (fitted, d locked from CR245)

```text
  vol              = +10.81472
  surf             = +27.55377
  coul             = +0.83304
  asym             = +36.81813
  pair             = -78.16972
  quadZ_A          = +4.25127
  quadN_A          = +1.40698
  quad_cross_A2    = -2.85268
  shell_prox       = -2.53936
  lightodd         = +17.70585
  alpha            = +0.74985
  reonset          = +13.61189
  doubmag          = -1.55859
```

## Operator adoption

| operator | γ | |F| | family | mean_improve MeV | verdict |
| --- | --- | --- | --- | --- | --- |
| `op_82pre` | -0.7273 | 1 | Nd-142 | +11.637 | ADOPT |
| `op_3d_odd` | +6.9654 | 3 | Cu-63, Mn-55, Co-59 | +5.647 | ADOPT |
| `op_dm_sat` | +7.1800 | 1 | Pb-208 | +7.180 | ADOPT |
| `op_ms_fill` | -0.4531 | 2 | Ag-107, Sn-120 | +4.449 | ADOPT |

## Result summary

- Base Model K RMS (all 55): **3.9102 MeV**
- Base Model K 5-fold CV RMS: 6.1150 MeV (diagnostic)
- Base outliers (|resid|>5): 12/55
- Combined (base + adopted ops) RMS: **2.7160 MeV**
- Combined within 5 MeV: **50/55 (90.9%)**
- Remaining outliers: 5/55

## Anchor cases

| anchor | Z | N | A | B_u_obs | final_pred | resid | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| O-16 | 8 | 8 | 16 | +4.737 | +5.629 | -0.892 | PASS |
| Fe-56 | 26 | 30 | 56 | +60.605 | +61.837 | -1.232 | PASS |
| Au-197 | 79 | 118 | 197 | +31.141 | +27.421 | +3.719 | PASS |
| Pb-208 | 82 | 126 | 208 | +21.748 | +21.748 | +0.000 | PASS |

## Remaining outliers (|resid| > 5 MeV)

| isotope | Z | N | A | resid MeV | family membership |
| --- | --- | --- | --- | --- | --- |
| Mg-26 | 12 | 14 | 26 | +5.612 | none (Phase 7 candidate) |
| Ca-40 | 20 | 20 | 40 | -6.288 | none (Phase 7 candidate) |
| Zr-90 | 40 | 50 | 90 | -5.496 | none (Phase 7 candidate) |
| Hg-202 | 80 | 122 | 202 | +5.469 | none (Phase 7 candidate) |
| U-234 | 92 | 142 | 234 | -7.254 | none (Phase 7 candidate) |

## Per-isotope residuals (full)

| isotope | set | Z | N | A | B_u_obs | base_resid | final_resid |
| --- | --- | --- | --- | --- | --- | --- | --- |
| O-16 | train | 8 | 8 | 16 | +4.737 | -0.892 | -0.892 |
| O-17 | train | 8 | 9 | 17 | +0.809 | -1.716 | -1.716 |
| O-18 | train | 8 | 10 | 18 | +0.783 | +0.643 | +0.643 |
| F-19 | train | 9 | 10 | 19 | +1.487 | -2.009 | -2.009 |
| Ne-20 | train | 10 | 10 | 20 | +7.042 | +0.356 | +0.356 |
| Ne-22 | train | 10 | 12 | 22 | +8.025 | +3.389 | +3.389 |
| Na-23 | train | 11 | 12 | 23 | +9.530 | +0.437 | +0.437 |
| Mg-24 | train | 12 | 12 | 24 | +13.934 | +2.437 | +2.437 |
| Mg-25 | train | 12 | 13 | 25 | +13.193 | +0.930 | +0.930 |
| Mg-26 | train | 12 | 14 | 26 | +16.215 | +5.612 | +5.612 |
| Al-27 | train | 13 | 14 | 27 | +17.197 | +1.792 | +1.792 |
| Si-28 | train | 14 | 14 | 28 | +21.493 | +4.530 | +4.530 |
| P-31 | train | 15 | 16 | 31 | +24.441 | +2.041 | +2.041 |
| S-32 | train | 16 | 16 | 32 | +26.016 | +2.293 | +2.293 |
| Cl-35 | train | 17 | 18 | 35 | +29.014 | -1.475 | -1.475 |
| Ar-40 | train | 18 | 22 | 40 | +35.040 | +1.138 | +1.138 |
| Ca-40 | train | 20 | 20 | 40 | +34.846 | -6.288 | -6.288 |
| Ti-48 | train | 22 | 26 | 48 | +48.492 | -1.174 | -1.174 |
| Fe-56 | train | 26 | 30 | 56 | +60.605 | -1.232 | -1.232 |
| Ni-58 | train | 28 | 30 | 58 | +60.228 | -2.069 | -2.069 |
| Cu-63 | train | 29 | 34 | 63 | +65.579 | +5.065 | -1.901 |
| Zn-64 | train | 30 | 34 | 64 | +66.004 | -4.212 | -4.212 |
| Br-79 | train | 35 | 44 | 79 | +76.069 | -0.048 | -0.048 |
| Kr-84 | train | 36 | 48 | 84 | +82.439 | -0.207 | -0.207 |
| Ag-107 | train | 47 | 60 | 107 | +88.402 | -9.227 | -4.696 |
| Sn-120 | train | 50 | 70 | 120 | +91.099 | -6.715 | +2.348 |
| I-127 | train | 53 | 74 | 127 | +88.984 | -2.740 | -2.740 |
| Xe-132 | train | 54 | 78 | 132 | +89.279 | -0.421 | -0.421 |
| Cs-133 | train | 55 | 78 | 133 | +88.071 | +0.698 | +0.698 |
| Au-197 | train | 79 | 118 | 197 | +31.141 | +3.719 | +3.719 |
| Hg-200 | train | 80 | 120 | 200 | +29.504 | -0.065 | -0.065 |
| Pb-208 | train | 82 | 126 | 208 | +21.748 | +7.180 | +0.000 |
| Th-232 | train | 90 | 142 | 232 | -35.447 | +2.348 | +2.348 |
| U-235 | train | 92 | 143 | 235 | -40.920 | -0.594 | -0.594 |
| U-238 | train | 92 | 146 | 238 | -47.309 | +2.279 | +2.279 |
| Ti-46 | test | 22 | 24 | 46 | +44.128 | -1.152 | -1.152 |
| Cr-52 | test | 24 | 28 | 52 | +55.420 | -1.290 | -1.290 |
| Mn-55 | test | 25 | 30 | 55 | +57.713 | +8.943 | +1.978 |
| Co-59 | test | 27 | 32 | 59 | +62.230 | +6.888 | -0.077 |
| Y-89 | test | 39 | 50 | 89 | +87.711 | +4.203 | +4.203 |
| Zr-90 | test | 40 | 50 | 90 | +88.773 | -5.496 | -5.496 |
| Ba-138 | test | 56 | 82 | 138 | +88.262 | +3.773 | +3.773 |
| Nd-142 | test | 60 | 82 | 142 | +85.950 | -11.637 | +0.000 |
| Sm-152 | test | 62 | 90 | 152 | +74.763 | -2.177 | -2.177 |
| Gd-158 | test | 64 | 94 | 158 | +70.690 | +1.762 | +1.762 |
| Dy-162 | test | 66 | 96 | 162 | +68.181 | -0.550 | -0.550 |
| Er-166 | test | 68 | 98 | 166 | +64.924 | -3.010 | -3.010 |
| Yb-172 | test | 70 | 102 | 172 | +59.255 | -0.601 | -0.601 |
| Hf-178 | test | 72 | 106 | 178 | +52.435 | +0.642 | +0.642 |
| W-184 | test | 74 | 110 | 184 | +45.705 | +1.803 | +1.803 |
| Os-190 | test | 76 | 114 | 190 | +38.708 | +2.453 | +2.453 |
| Pt-194 | test | 78 | 116 | 194 | +34.760 | -1.744 | -1.744 |
| Hg-202 | test | 80 | 122 | 202 | +27.345 | +5.469 | +5.469 |
| Pb-206 | test | 82 | 124 | 206 | +23.786 | +0.459 | +0.459 |
| U-234 | test | 92 | 142 | 234 | -38.145 | -7.254 | -7.254 |

## Provenance

- CR261_bw_fit_per_row.csv sha256 = `3212a36064244e6addc30e465af6577d68df7997715f6c68ff9bb983b0d8eef2`
- Precommit sha256 = `c09616e40e26f7d2df36350b0f3db62c7da81b17e01ce7607a1ed87c8431c3a9`
- Stewardship sha256 = `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`
