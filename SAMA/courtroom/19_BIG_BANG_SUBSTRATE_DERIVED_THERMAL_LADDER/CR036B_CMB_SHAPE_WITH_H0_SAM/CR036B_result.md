# CR036B_CMB_SHAPE_WITH_H0_SAM

## Verdict

```text
CR036B_PASS_SAM_DENSITY_SPINE_REPRODUCES_PLANCK_TT_FULL_PER_MULTIPOLE_SHAPE_AT_PEAK_AND_FULL_SHAPE_TOLERANCES
```

## Courtroom Fields

```text
execution_status                 = CLEAN
scientific_verdict               = PASS
verdict_case                     = PASS
triage_bin                       = A
free_parameters_introduced_RunA  = 0
external_perturbation_disclosed  = true
prior_CR_result_inputs           = false
forbidden_files_opened           = false
CR035A_files_opened              = false
CR035A2_files_opened             = false
CR036_files_opened               = false
opened_paths_count               = 1
precommit_sha256                 = ab2fea4b0822412cc5ca9978bab89822ea6fccffa76f94527bff05aaa660305e
engine                           = CAMB 1.6.6
peak_finder                      = windows + prominence >= 50 muK^2 + smoothed-curve heights
```

## Summary

```text
CR036B PASS confirms that the SAM density spine + H_0_SAM = 67.2503751950 (sealed from CR036) + Planck 2018 posterior-centroid perturbation parameters, run through CAMB 1.6.6, reproduces the Planck 2018 PR3 full per-multipole bandpower table at the CR035A2 P1 peak structure and P2 full-shape tolerances.

CR035A2 PASS and CR036 PASS both stand sealed and are NOT overwritten.
CR036B inherits the CR035A2 spec verbatim, replacing only the H_0 input:
  CR035A2:  H_0 = 68.76          (externally set)
  CR036B:   H_0 = 67.2503751950  (sealed from CR036; numeric literal
                                  cited by value; CR036 file NOT opened)
The runner did NOT open any CR036, CR035A, or CR035A2 file at runtime.
```

## SAM Density Spine (substrate-derived; unchanged)

| symbol | value |
|---|---:|
| A_0 = 1/(12π) | 0.026525823849 |
| χ = 2/(9π) | 0.070735530263 |
| Ω_m = 1/π | 0.318309886184 |
| Ω_b = 2·A_0·(1−χ) | 0.049299011266 |
| Ω_c = Ω_m − Ω_b | 0.269010874918 |
| H_0 | 67.250375195 km/s/Mpc |
| ω_b = Ω_b·h² | 0.022296034746 |
| ω_c = Ω_c·h² | 0.121663207032 |

## Fixed External Perturbations (Planck 2018 centroids; Run A)

| field | value |
|---|---:|
| A_s | 2.100e-09 |
| n_s | 0.9649 |
| τ | 0.0544 |
| N_eff | 3.046 |
| T_CMB | 2.7255 K |
| k_pivot | 0.05 Mpc⁻¹ |

## Peak Finder (NEW spec)

| field | value |
|---|---|
| smoothing | Gaussian σ_ell = 5 |
| min prominence | 50 μK² |
| Peak 1 window | ℓ ∈ [150, 300] |
| Peak 2 window | ℓ ∈ [400, 650] |
| Peak 3 window | ℓ ∈ [700, 900] |
| height rule | H_i = D_l,smoothed at detected ℓ_peak_i |

| peak | theory | Planck |
|---|---|---|
| 1 | ell=220.0  H_smoothed=5678.41  prom=4188.65 | ell=219.0  H_smoothed=5826.38  prom=4391.02 |
| 2 | ell=535.0  H_smoothed=2576.94  prom=858.39 | ell=520.0  H_smoothed=2580.98  prom=859.25 |
| 3 | ell=812.0  H_smoothed=2532.12  prom=729.81 | ell=814.0  H_smoothed=2535.54  prom=745.96 |

## P1 — Acoustic Geometry / Peak Structure (Run A)

| sub-gate | tolerance | pass |
|---|---|---:|
| P1a (1st peak Δℓ ≤ 5) | ±5 | **True** |
| P1b (2nd/3rd Δℓ ≤ 10) | ±10 each | **False** |
| P1c (H2/H1, H3/H1 within 15%) | ±15% each | **True** |
| **P1 (≥2 of 3)** | | **True** |

Peak deltas: Δℓ_1 = 1.0, Δℓ_{2,3} = [15.0, 2.0].
Height ratios (theory / Planck): H2/H1 0.4538 / 0.4430 → True;
H3/H1 0.4459 / 0.4352 → True.

## P2 — TT Full-Shape (Run A)

| stat | value |
|---|---:|
| χ²_TT | 2572.9920 |
| dof_TT | 2471 |
| **χ²_TT / dof_TT** | **1.0413** |
| P2 band | **PASS** |

## TE / EE — Reported (Run A)

| spectrum | χ² | dof | χ²/dof |
|---|---:|---:|---:|
| TE | 2054.1327 | 1967 | 1.0443 |
| EE | 2051.6677 | 1967 | 1.0430 |

Polarization debt (Run A): **False** (TT passes but TE or EE > 3.0 at Run A).

## Run B — Diagnostic Optimization

| param | optimized | fixed (Planck) | σ-deviation |
|---|---|---|---:|
| A_s | 2.1092e-09 | 2.1000e-09 | +0.305 σ |
| n_s | 0.9657 | 0.9649 | +0.185 σ |
| τ | 0.0536 | 0.0544 | -0.107 σ |
| χ²_TT/dof at optimum | 1.0326 | (<= 3.0 for BOUNDARY iii) | |
| χ²_TE/dof at optimum | 1.0449 | (<= 5.0 sanity guard) | |
| χ²_EE/dof at optimum | 1.0427 | (<= 5.0 sanity guard) | |
| optimizer | L-BFGS-B  (2 iters, 16 evals) | | |

Run B is diagnostic only. BOUNDARY (iii) additionally requires TE/EE chi^2/dof <= 5.0 at the optimum.

## Chronology

```text
CR035A2 sealed PASS at 2026-06-27 (precommit
6310c00f6f74de36475c0edbf7331f0f41960098983ee90adff5449063ae0697)
with the SAM density spine + H_0 = 68.76 (externally set) +
Planck-centroid (A_s, n_s, tau) at TT chi^2/dof = 1.35 and corrected
peak structure.
CR036 sealed PASS at 2026-06-27 (precommit
345a1a8dc180eb6b28141114a82315e3b8d92889537c1219eec4312d59ca33f2)
deriving H_0,SAM = 67.2503751950 from substrate atoms + FIRAS T_CMB +
CODATA 2018 / SI fixed constants.
CR036B is the natural follow-on: same CR035A2 pipeline, with H_0
replaced by H_0,SAM. The CR036B runner did NOT open any CR036, CR035A,
or CR035A2 file at runtime; H_0,SAM is cited as a numeric literal in
the precommit and used directly.
```

## Provenance Chain

```text
Stewardship    = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Precommit      = ab2fea4b0822412cc5ca9978bab89822ea6fccffa76f94527bff05aaa660305e
H_0 source     = CR036 sealed PASS (precommit 345a1a8d...; H_0_SAM cited by value)
External data  = Planck PR3 TT/TE/EE bandpowers (locally hashed in HASHES.txt)
Engine         = CAMB 1.6.6
```

---

**Sealed by:** CR036B runner, 2026-06-27.
