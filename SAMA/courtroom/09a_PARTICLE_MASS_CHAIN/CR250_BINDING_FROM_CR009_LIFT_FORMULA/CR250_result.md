# CR250 — Binding from CR009 Lift Formula on CR247 Phi Decomposition — Result

**Verdict:** `BOUNDARY_WC_FAIL`
**Started / Completed:** 2026-06-25T01:27:02+00:00
**Dataset:** CR242_binding_dataset.csv (filtered to N >= Z; n = 67)
**Dataset sha256:** `bba9625c2662d6ac70255c14f7961a1e1b3a5c4032df6f459267898e55619c90`

## What this CR tested

Applied the sealed CR009 pair lift form `(q + D) / R^4` to the sealed CR247
phi positions (`phi_b` with `dQ = 0`, `phi_e` with `dQ = 7093/192`) and summed
per CR247 Block G's identity `B_u(Z, N) = Z·s_b + (N − Z)·s_e`. Zero free
parameters. No candidate-rule search. No outside-data comparison. Above-the-line
constants traceable to CR238 (R, D, S), CR221 (κ, g), CR240 (μ_Q), and CR247
(phi positions).

Per Sean's 2026-06-24 cascade synthesis (Chat5 line 14588):
> "The 'binding energy' of conventional physics IS the closure fee the substrate
> charges, expressed in mass-equivalent units."

## Sealed formula evaluated

```text
s_b = D / R^4 * mu_Q                 = 1 / (36 * 7117) = 1/256212 u
    ≈ 0.00000390301781 u  ≈ 0.003636 MeV per balanced position

s_e = (7093/192 + D) / R^4 * mu_Q    = 7669 / (20736 * 7117)
    ≈ 0.00005196570071 u  ≈ 0.048406 MeV per excess neutron

B_u_pred(Z, N) = Z * s_b + (N - Z) * s_e
```

## Aggregate residuals (unrescaled, raw substrate prediction)

| Metric | Value (u) | Value (MeV) |
|---|---|---|
| n | 67 | — |
| max \|Δ\| | 0.096564 | 89.949 |
| mean \|Δ\| | 0.041872 | 39.003 |
| RMS | 0.052139 | 48.567 |

## Shape verdict — single-scale rescale fit

Solve `B_obs ≈ α · B_pred` for the single multiplicative scale `α` that
minimizes residual RMS. If a single scalar closes the rescale-RMS gate
(< 1 MeV), the substrate composition has the right structural shape and
the missing piece is a single multiplicative constant traceable to a
follow-up CR. If it doesn't, the shape itself is incomplete and the
missing structure is more than a coefficient.

| Metric | Value |
|---|---|
| α (best single scale) | 18.545144 |
| rescale RMS | 43.4176 MeV |
| rescale max \|Δ\| | 101.9873 MeV |
| shape monotonic (Pearson > 0)? | **True** |
| rescale RMS < 1 MeV? | **False** |

## Top 10 worst residuals (unrescaled)

| isotope | Z | N | A | N−Z | B_obs (u) | B_pred (u) | Δ (u) | Δ (MeV) |
|---|---|---|---|---|---|---|---|---|
| Sn-120 | 50 | 70 | 120 | 20 | 0.097798 | 0.001234 | 0.096564 | 89.949 |
| Zr-90 | 40 | 50 | 90 | 10 | 0.095301 | 0.000676 | 0.094625 | 88.143 |
| Xe-132 | 54 | 78 | 132 | 24 | 0.095845 | 0.001458 | 0.094387 | 87.921 |
| I-127 | 53 | 74 | 127 | 21 | 0.095528 | 0.001298 | 0.094230 | 87.775 |
| Ag-107 | 47 | 60 | 107 | 13 | 0.094903 | 0.000859 | 0.094044 | 87.602 |
| Y-89 | 39 | 50 | 89 | 11 | 0.094162 | 0.000724 | 0.093438 | 87.037 |
| Ba-138 | 56 | 82 | 138 | 26 | 0.094753 | 0.001570 | 0.093183 | 86.800 |
| Cs-133 | 55 | 78 | 133 | 23 | 0.094548 | 0.001410 | 0.093138 | 86.758 |
| Nd-142 | 60 | 82 | 142 | 22 | 0.092271 | 0.001377 | 0.090894 | 84.667 |
| Kr-84 | 36 | 48 | 84 | 12 | 0.088502 | 0.000764 | 0.087738 | 81.728 |

## Best 10 (smallest |Δ|, unrescaled)

| isotope | Z | N | A | N−Z | B_obs (u) | B_pred (u) | Δ (u) | Δ (MeV) |
|---|---|---|---|---|---|---|---|---|
| N-15 | 7 | 8 | 15 | 1 | -0.000109 | 0.000079 | -0.000188 | -0.175 |
| O-18 | 8 | 10 | 18 | 2 | 0.000840 | 0.000135 | 0.000705 | 0.657 |
| O-17 | 8 | 9 | 17 | 1 | 0.000868 | 0.000083 | 0.000785 | 0.731 |
| F-19 | 9 | 10 | 19 | 1 | 0.001597 | 0.000087 | 0.001510 | 1.406 |
| He-4 | 2 | 2 | 4 | 0 | -0.002603 | 0.000008 | -0.002611 | -2.432 |
| N-14 | 7 | 7 | 14 | 0 | -0.003074 | 0.000027 | -0.003101 | -2.889 |
| C-14 | 6 | 8 | 14 | 2 | -0.003242 | 0.000127 | -0.003369 | -3.139 |
| C-13 | 6 | 7 | 13 | 1 | -0.003355 | 0.000075 | -0.003430 | -3.195 |
| O-16 | 8 | 8 | 16 | 0 | 0.005085 | 0.000031 | 0.005054 | 4.708 |
| Ne-20 | 10 | 10 | 20 | 0 | 0.007560 | 0.000039 | 0.007521 | 7.006 |

## Worst 10 rescale residuals (after best single-scale α)

| isotope | Z | N | A | N−Z | B_obs (u) | α·B_pred (u) | residual (MeV) |
|---|---|---|---|---|---|---|---|
| U-238 | 92 | 146 | 238 | 54 | -0.050788 | 0.058700 | -101.9873 |
| U-235 | 92 | 143 | 235 | 51 | -0.043930 | 0.055808 | -92.9057 |
| U-234 | 92 | 142 | 234 | 50 | -0.040950 | 0.054845 | -89.2325 |
| Th-232 | 90 | 142 | 232 | 52 | -0.038054 | 0.056627 | -88.1951 |
| Zr-90 | 40 | 50 | 90 | 10 | 0.095301 | 0.012532 | 77.0987 |
| Y-89 | 39 | 50 | 89 | 11 | 0.094162 | 0.013424 | 75.2071 |
| Ag-107 | 47 | 60 | 107 | 13 | 0.094903 | 0.015930 | 73.5629 |
| Sn-120 | 50 | 70 | 120 | 20 | 0.097798 | 0.022893 | 69.7736 |
| Kr-84 | 36 | 48 | 84 | 12 | 0.088502 | 0.014170 | 69.2398 |
| I-127 | 53 | 74 | 127 | 21 | 0.095528 | 0.024074 | 66.5589 |

## Best 10 rescale residuals (after best single-scale α)

| isotope | Z | N | A | N−Z | B_obs (u) | α·B_pred (u) | residual (MeV) |
|---|---|---|---|---|---|---|---|
| F-19 | 9 | 10 | 19 | 1 | 0.001597 | 0.001615 | -0.0171 |
| Os-190 | 76 | 114 | 190 | 38 | 0.041555 | 0.042122 | -0.5286 |
| O-17 | 8 | 9 | 17 | 1 | 0.000868 | 0.001543 | -0.6283 |
| N-15 | 7 | 8 | 15 | 1 | -0.000109 | 0.001470 | -1.4711 |
| O-18 | 8 | 10 | 18 | 2 | 0.000840 | 0.002506 | -1.5520 |
| He-4 | 2 | 2 | 4 | 0 | -0.002603 | 0.000145 | -2.5598 |
| N-14 | 7 | 7 | 14 | 0 | -0.003074 | 0.000507 | -3.3354 |
| O-16 | 8 | 8 | 16 | 0 | 0.005085 | 0.000579 | 4.1976 |
| C-13 | 6 | 7 | 13 | 1 | -0.003355 | 0.001398 | -4.4272 |
| Pt-194 | 78 | 116 | 194 | 38 | 0.037317 | 0.042267 | -4.6112 |

## Cascade-cited anchor rows (Au-197, C-12, C-13)

These rows were cited in the 2026-06-24 cascade derivation as headline matches.
They are reported here for tracking; not load-bearing for the verdict.

| isotope | Z | N | A | N−Z | B_obs (u) | B_pred (u) | Δ (MeV) | α·B_pred residual (MeV) |
|---|---|---|---|---|---|---|---|---|
| C-13 | 6 | 7 | 13 | 1 | -0.003355 | 0.000075 | -3.195 | -4.4272 |
| Au-197 | 79 | 118 | 197 | 39 | 0.033431 | 0.002335 | 28.966 | -9.1954 |

## Wrong controls — load-bearing check on each formula element

Each WC perturbs ONE sealed element and reports whether the perturbation BREAKS
the shape gate (rescale RMS inflates ≥ 1.5× the unperturbed value; 1.05× for
μ_Q since it's a precision constant). A passing WC means the unperturbed element
was load-bearing.

Unperturbed rescale RMS: **43.4176 MeV** (threshold reference)

| WC | Description | rescale RMS (MeV) | α | Broke shape? |
|---|---|---|---|---|
| WC-1_swap_phi_dQ | swap dQ_b <-> dQ_e | 39.0170 | 12.798867 | **False** |
| WC-2_triadic_depth | use R denominator (triadic) instead of R^4 (pair) | 43.4176 | 0.010732 | **False** |
| WC-3_drop_D | drop the +D term (s_b vanishes, s_e shrinks) | 44.0389 | 21.909969 | **False** |
| WC-4_perturb_mu_Q | use mu_Q = 192/7118 instead of 192/7117 | 43.4176 | 18.547750 | **False** |
| WC-5_shuffle_NminusZ | shuffle (N-Z) across rows, preserve Z | 43.5632 | 19.543497 | **False** |

All WCs broke as predicted: **False**

## Verdict logic

- Shape monotonic (Pearson > 0): **True**
- Rescale RMS < 1 MeV: **False**
- All WCs passed (broke as predicted): **False**
- **Overall verdict: `BOUNDARY_WC_FAIL`**

Verdict ladder (sealed in precommit):
- `STRUCTURAL_PASS`: shape monotonic AND rescale RMS < 1 MeV AND all WCs broke
- `BOUNDARY`: shape monotonic AND all WCs broke, but rescale RMS ≥ 1 MeV
  (substrate composition right structure, additional terms or different depth needed)
- `BOUNDARY_WC_FAIL`: shape monotonic but a WC failed to break
  (element identified as non-load-bearing — composition needs revision)
- `FAIL`: shape not monotonic (composition has wrong structure, not missing-coefficient)

## Structural reading

**Substrate composition produces the right structural shape with magnitude offset.**
Pearson correlation positive across 69 nuclei, but rescale RMS 43.4176 MeV
> 1 MeV target. The minimal CR009 + CR247 composition is missing structure beyond
a single multiplicative scale — candidate follow-up directions (each its own future CR):

- (a) phi_b position carries non-trivial channel-gap structure via an internal q value
  not visible in dQ_b = 0 (e.g., internal proton/neutron/electron lifts within the
  balanced bundle that CR247's nucleon-decomposition doesn't expose)
- (b) Depth selection between R (triadic) and R^4 (pair) should be position-dependent
  rather than uniform (e.g., balanced position connects via triadic depth, excess neutron
  via pair depth)
- (c) CR248's phase-A four-particle structure contains the missing per-position fee
  that CR250 would inherit when sealed

The unscaled prediction undershoots heavy nuclei by factor α = 18.5451.
If α reduces to a sealed substrate constant in a follow-up CR, this composition closes
the binding curve structurally.

## Provenance chain (cryptographic)

```text
30f8d2674e40240777c35466bb749a2c8ef5cf0883bd1caf2cb2fb4df2e598ee  CR009_result.md
ed0eb192ca708e33fb6a044ac5a11e20cfdf1ab507b0bc241110a14646b662d7  CR247_result.md
c2637851d8ec24b48b5272dbca8f92ab44dd516985d1568a885c92579db9527b  CR240_result.md
6ee047f445290dc2becda4ae565bf93172576569d1decc0fa55ed0361806a22a  CR005_result.md
914e01d1e035e26fd1991a406fcbdc00944de7809f18a18f1c10f4af07cc80bc  CR250_PRECOMMIT.md
bba9625c2662d6ac70255c14f7961a1e1b3a5c4032df6f459267898e55619c90  CR242_binding_dataset.csv
```

## What CR250 does NOT do

- Does not search candidate rules — single sealed composition only
- Does not compare to PDG / ΛCDM / GR / QM or any outside model
- Does not modify CR009, CR247, CR238, CR240, or any sealed upstream CR
- Does not search for the rescale α value — reports what least-squares gives
- Does not extend to N < Z (CR247 scope is N >= Z)

## Rule of Immutability

Sealed 2026-06-25 by Sean Brady. Formula, phi positions, lift form, test corpus,
verdict ladder, wrong controls, K-gates all frozen above the line.
