# CR037B_PARAMETER_FREE_CMB_SHAPE_ATTEMPT

## Verdict

```text
CR037B_PASS_PARAMETER_FREE_SAM_COSMOLOGY_REPRODUCES_PLANCK_TT_FULL_PER_MULTIPOLE_SHAPE_AT_PEAK_AND_FULL_SHAPE_TOLERANCES
```

## Courtroom Fields

```text
execution_status               = CLEAN
scientific_verdict             = PASS
verdict_case                   = PASS
triage_bin                     = A
free_parameters_introduced     = 0
prior_CR_result_inputs         = false
Run_B_optimizer_used           = false
forbidden_files_opened         = false
CR035A_files_opened            = false
CR035A2_files_opened           = false
CR036_files_opened             = false
CR036B_files_opened            = false
CR037A_files_opened            = false
opened_paths_count             = 1
precommit_sha256               = 5b7bd931eb28a6123e848b37867735d627b0f59d4f09433c5bd64261cf0c149b
engine                         = CAMB 1.6.6
peak_finder                    = windows + prominence >= 50 muK^2 + smoothed-curve heights
```

## Summary

```text
CR037B PASS confirms that the SAM-derived cosmological inputs (densities + H_0_SAM + SAM perturbation triplet, all from substrate atoms via FIRAS T_CMB + CODATA 2018 / SI fixed constants) reproduce the Planck 2018 PR3 full per-multipole bandpower table at the CR035A2 P1 peak structure + P2 full-shape tolerances, with NO Run B optimizer and zero free parameters.

CR035A2, CR036, CR036B, and CR037A all stand sealed and are NOT
overwritten. CR037B inherits the CR036B spec verbatim except for the
perturbation triplet, which now comes from CR037A:

  CR036B:  A_s = 2.100e-9       n_s = 0.9649       tau = 0.0544       (Planck centroids)
  CR037B:  A_s = 2.1117473568e-9 n_s = 0.9646322349 tau = 0.0530516477 (SAM, CR037A)

All cosmology inputs (Omega_m, Omega_b, Omega_c, H_0, A_s, n_s, tau) are
SAM-derived from substrate atoms via the declared T_CMB FIRAS thermal
anchor + CODATA 2018 / SI fixed constants. There is no Run B optimizer.
The runner did NOT open any CR036, CR036B, CR035A2, CR035A, or CR037A
file at runtime.
```

## SAM Density Spine (substrate-derived)

| symbol | value |
|---|---:|
| A_0 = 1/(12π) | 0.026525823849 |
| χ = 2/(9π) | 0.070735530263 |
| Ω_m = 1/π | 0.318309886184 |
| Ω_b = 2·A_0·(1−χ) | 0.049299011266 |
| Ω_c = Ω_m − Ω_b | 0.269010874918 |
| H_0 (CR036) | 67.250375195 km/s/Mpc |
| ω_b = Ω_b·h² | 0.022296034746 |
| ω_c = Ω_c·h² | 0.121663207032 |

## SAM-Derived Perturbations (from CR037A)

| field | identity | value |
|---|---|---:|
| A_s,SAM | η_SAM·√R | 2.1117473568e-09 |
| n_s,SAM | 1 − χ/2 | 0.9646322349 |
| τ_SAM | 2·A_0 | 0.0530516477 |

## Fixed Non-Fit Ancillary Inputs (disclosed)

| field | value | note |
|---|---:|---|
| N_eff | 3.046 | standard radiation-sector input |
| T_CMB | 2.7255 K | measured thermal anchor (FIRAS) |
| k_pivot | 0.05 Mpc⁻¹ | scalar-amplitude convention |
| m_ν (sum) | 0.06 eV | Planck-baseline |

## CAMB Ancillary Settings (frozen; echoed from runtime)

| setting | value |
|---|---:|
| camb_version | 1.6.6 |
| lmax | 2700 |
| lens_potential_accuracy | 1 |
| WantTensors | False |
| WantScalars | True |
| r (tensor-to-scalar) | 0.0 |
| NonLinear | NonLinear_none |
| omk | 0.0 |
| TCMB | 2.7255 |
| nnu | 3.046 |
| num_massive_neutrinos | 1 |
| mnu (eV) | 0.06 |
| YHe_used | 0.24585087308813788 |
| YHe_handling | CAMB BBN-consistency (default; set via set_cosmology) |
| pivot_scalar | 0.05 |
| CMB_unit | muK |
| spectra_requested | ['lensed_scalar'] |

## Peak Finder

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
| 1 | ell=220.0  H_smoothed=5727.11  prom=4224.57 | ell=219.0  H_smoothed=5826.38  prom=4391.02 |
| 2 | ell=535.0  H_smoothed=2598.54  prom=865.75 | ell=520.0  H_smoothed=2580.98  prom=859.25 |
| 3 | ell=812.0  H_smoothed=2553.94  prom=736.58 | ell=814.0  H_smoothed=2535.54  prom=745.96 |

## P1 — Acoustic Geometry / Peak Structure (Run A)

| sub-gate | tolerance | pass |
|---|---|---:|
| P1a (1st peak Δℓ ≤ 5) | ±5 | **True** |
| P1b (2nd/3rd Δℓ ≤ 10) | ±10 each | **False** |
| P1c (H2/H1, H3/H1 within 15%) | ±15% each | **True** |
| **P1 (≥2 of 3)** | | **True** |

Peak deltas: Δℓ_1 = 1.0, Δℓ_{2,3} = [15.0, 2.0].
Height ratios (theory / Planck): H2/H1 0.4537 / 0.4430 → True;
H3/H1 0.4459 / 0.4352 → True.

## P2 — TT Full-Shape (Run A)

| stat | value |
|---|---:|
| χ²_TT | 2554.8502 |
| dof_TT | 2471 |
| **χ²_TT / dof_TT** | **1.0339** |
| P2 band | **PASS** |

## TE / EE — Reported (Run A)

| spectrum | χ² | dof | χ²/dof |
|---|---:|---:|---:|
| TE | 2056.3861 | 1967 | 1.0454 |
| EE | 2051.6208 | 1967 | 1.0430 |

Polarization debt (Run A): **False** (TT passes but TE or EE > 3.0 at Run A).

## Chronology

```text
CR037B is the parameter-free CMB shape attempt. It follows:
  CR035A2 (precommit 6310c00f...; PASS at TT chi^2/dof = 1.35 with
    H_0 = 68.76 externally set + Planck-centroid perturbations)
  CR036    (precommit 345a1a8d...; PASS deriving H_0_SAM = 67.2503751950
    from substrate atoms + FIRAS T_CMB + CODATA 2018 / SI)
  CR036B   (precommit ab2fea4b...; PASS at TT chi^2/dof = 1.04 with
    SAM density spine + H_0_SAM + Planck-centroid perturbations)
  CR037A   (precommit 1b7da85b...; PASS with all three SAM perturbation
    identities (A_s,SAM = eta*sqrt(R); n_s,SAM = 1 - chi/2;
    tau_SAM = 2*A_0) inside Planck posterior at STRONG_CONTACT)

CR037B closes the cascade: the full SAM-derived cosmology (densities +
H_0 + perturbation triplet) runs through CAMB 1.6.6 with NO Run B
optimizer. The runner did NOT open any CR036, CR036B, CR035A, CR035A2,
or CR037A file at runtime; all values are numeric literals cited by
hash provenance in the precommit.
```

## Provenance Chain

```text
Stewardship    = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Precommit      = 5b7bd931eb28a6123e848b37867735d627b0f59d4f09433c5bd64261cf0c149b
H_0 source     = CR036 sealed PASS (precommit 345a1a8d...; cited by value)
Perturbations  = CR037A sealed PASS (precommit 1b7da85b...; cited by value)
External data  = Planck PR3 TT/TE/EE bandpowers (locally hashed in HASHES.txt)
Engine         = CAMB 1.6.6
```

---

**Sealed by:** CR037B runner, 2026-06-27.
