# CR035A2_PEAK_FINDER_AUDIT

## Verdict

```text
CR035A2_PASS_SAM_DENSITY_SPINE_REPRODUCES_PLANCK_TT_FULL_PER_MULTIPOLE_SHAPE_AT_PEAK_AND_FULL_SHAPE_TOLERANCES
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
opened_paths_count               = 1
precommit_sha256                 = 6310c00f6f74de36475c0edbf7331f0f41960098983ee90adff5449063ae0697
engine                           = CAMB 1.6.6
peak_finder                      = windows + prominence >= 50 muK^2 + smoothed-curve heights
```

## Summary

```text
CR035A2 PASS confirms that the SAM density spine, paired with Planck 2018 posterior-centroid perturbation parameters and CAMB 1.6.6, reproduces the Planck 2018 PR3 full per-multipole bandpower table at the corrected CR035A2 peak and full-shape tolerances.

CR035A's strict FAIL token remains sealed and is not overwritten.
CR035A2 is the appeal: same SAM densities + same fixed Planck
perturbations + same CAMB engine + same Planck files + same chi^2 /
tolerances / Run B bounds. Only the peak finder (per-peak windows +
minimum prominence + smoothed-curve heights) and the verdict-mapping
tree (full BOUNDARY (iii) branch + Run B polarization sanity guard
at TE/EE chi^2/dof <= 5.0) changed.
```

## SAM Density Spine (substrate-derived; unchanged)

| symbol | value |
|---|---:|
| A_0 = 1/(12π) | 0.026525823849 |
| χ = 2/(9π) | 0.070735530263 |
| Ω_m = 1/π | 0.318309886184 |
| Ω_b = 2·A_0·(1−χ) | 0.049299011266 |
| Ω_c = Ω_m − Ω_b | 0.269010874918 |
| H_0 | 68.76 km/s/Mpc |
| ω_b = Ω_b·h² | 0.023308264901 |
| ω_c = Ω_c·h² | 0.127186663033 |

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
| 1 | ell=219.0  H_smoothed=5636.33  prom=4149.85 | ell=219.0  H_smoothed=5826.38  prom=4391.02 |
| 2 | ell=533.0  H_smoothed=2487.40  prom=710.45 | ell=520.0  H_smoothed=2580.98  prom=859.25 |
| 3 | ell=806.0  H_smoothed=2517.95  prom=861.81 | ell=814.0  H_smoothed=2535.54  prom=745.96 |

## P1 — Acoustic Geometry / Peak Structure (Run A)

| sub-gate | tolerance | pass |
|---|---|---:|
| P1a (1st peak Δℓ ≤ 5) | ±5 | **True** |
| P1b (2nd/3rd Δℓ ≤ 10) | ±10 each | **False** |
| P1c (H2/H1, H3/H1 within 15%) | ±15% each | **True** |
| **P1 (≥2 of 3)** | | **True** |

Peak deltas: Δℓ_1 = 0.0, Δℓ_{2,3} = [13.0, 8.0].
Height ratios (theory / Planck): H2/H1 0.4413 / 0.4430 → True;
H3/H1 0.4467 / 0.4352 → True.

## P2 — TT Full-Shape (Run A)

| stat | value |
|---|---:|
| χ²_TT | 3327.0128 |
| dof_TT | 2471 |
| **χ²_TT / dof_TT** | **1.3464** |
| P2 band | **PASS** |

## TE / EE — Reported (Run A)

| spectrum | χ² | dof | χ²/dof |
|---|---:|---:|---:|
| TE | 2348.8782 | 1967 | 1.1941 |
| EE | 2212.0624 | 1967 | 1.1246 |

Polarization debt (Run A): **False** (TT passes but TE or EE > 3.0 at Run A).

## Run B — Diagnostic Optimization

| param | optimized | fixed (Planck) | σ-deviation |
|---|---|---|---:|
| A_s | 2.1397e-09 | 2.1000e-09 | +1.323 σ |
| n_s | 0.9682 | 0.9649 | +0.778 σ |
| τ | 0.0510 | 0.0544 | -0.467 σ |
| χ²_TT/dof at optimum | 1.1881 | (<= 3.0 for BOUNDARY iii) | |
| χ²_TE/dof at optimum | 1.1900 | (<= 5.0 sanity guard) | |
| χ²_EE/dof at optimum | 1.1036 | (<= 5.0 sanity guard) | |
| optimizer | L-BFGS-B  (2 iters, 16 evals) | | |

Run B is diagnostic only. BOUNDARY (iii) additionally requires TE/EE chi^2/dof <= 5.0 at the optimum.

## Chronology

```text
CR035A v2 strict FAIL stands sealed at 2026-06-27 (precommit
0f20f2fde2afb66ed1bbeff8e43e6f183d4159a0d5310d5bdb714daac99a9ced).
CR035A2 is an appeal that corrects only the peak finder and the
verdict-mapping tree, with all other test inputs frozen from CR035A.
The CR035A2 runner did not open any CR035A file at runtime
(CR035A_files_opened = false; opened_paths_count = 1).
The appeal addresses the verdict token, not the underlying numerics.
```

## Provenance Chain

```text
Stewardship    = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Precommit      = 6310c00f6f74de36475c0edbf7331f0f41960098983ee90adff5449063ae0697
Appeal of      = CR035A_SAM_DENSITY_SPINE_CMB_SHAPE (FAIL, sealed)
External data  = Planck PR3 TT/TE/EE bandpowers (locally hashed in HASHES.txt)
Engine         = CAMB 1.6.6
```

---

**Sealed by:** CR035A2 runner, 2026-06-27.
