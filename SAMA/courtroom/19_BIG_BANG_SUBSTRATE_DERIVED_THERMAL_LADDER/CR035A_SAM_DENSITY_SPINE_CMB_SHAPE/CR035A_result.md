# CR035A_SAM_DENSITY_SPINE_CMB_SHAPE

## Verdict

```text
CR035A_FAIL_SAM_DENSITY_SPINE_BINNED_TT_SHAPE_OUTSIDE_TOLERANCES
```

## Courtroom Fields

```text
execution_status                 = CLEAN
scientific_verdict               = FAIL
triage_bin                       = A
free_parameters_introduced_RunA  = 0
external_perturbation_disclosed  = true
prior_CR_result_inputs           = false
forbidden_files_opened           = false
opened_paths_count               = 1
precommit_sha256                 = 0f20f2fde2afb66ed1bbeff8e43e6f183d4159a0d5310d5bdb714daac99a9ced
engine                           = CAMB 1.6.6
```

## SAM Density Spine (substrate-derived)

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

## Sample

| field | value |
|---|---:|
| TT bins (ℓ ∈ [30, 2500]) | 2471 |
| TE bins | 1967 |
| EE bins | 1967 |

## P1 — Acoustic Geometry / Peak Structure (Run A)

| peak | theory | Planck | Δℓ |
|---|---|---|---:|
| 1 | ell=219.0  D=5636.33 | ell=219.0  D=5826.38 | +0.00 |
| 2 | ell=533.0  D=2487.40 | ell=520.0  D=2580.98 | +13.00 |
| 3 | ell=806.0  D=2517.95 | ell=661.0  D=1837.11 | +145.00 |

| sub-gate | tolerance | pass |
|---|---|---:|
| P1a (first peak Δℓ ≤ 5) | ±5 | **True** |
| P1b (2nd/3rd Δℓ ≤ 10) | ±10 each | **False** |
| P1c (H2/H1, H3/H1 within 15%) | ±15% each | **False** |
| **P1 (≥2 of 3)** | | **False** |

Height ratios (theory / Planck):
- H2/H1: 0.4413 / 0.4430  → pass True
- H3/H1: 0.4467 / 0.3153  → pass False

## P2 — TT Full-Shape (Run A)

| stat | value |
|---|---:|
| χ²_TT | 3327.0128 |
| dof_TT | 2471 |
| **χ²_TT / dof_TT** | **1.3464** |
| P2 band | **PASS** |

P2 PASS ≤ 2.0; BOUNDARY (2.0, 3.0] with P1; FAIL > 3.0.

## E_TE / E_EE — Reported Evidence (Run A)

| spectrum | χ² | dof | χ²/dof |
|---|---:|---:|---:|
| TE | 2348.8782 | 1967 | 1.1941 |
| EE | 2212.0624 | 1967 | 1.1246 |

Polarization BOUNDARY triggered: **False** (TT passes but TE or EE > 3.0).

## Run B — Diagnostic Optimization (NOT a gate)

| param | optimized | fixed (Planck) | σ-deviation |
|---|---|---|---:|
| A_s | 2.1396e-09 | 2.1000e-09 | +1.319 σ |
| n_s | 0.9682 | 0.9649 | +0.775 σ |
| τ | 0.0510 | 0.0544 | +0.468 σ |
| χ²_TT/dof at optimum | 1.1881 | | |
| within ±5σ Planck posterior | **True** | | |
| optimizer | L-BFGS-B  (2 iters, 16 evals) | | |

Run B is diagnostic only. It cannot rescue PASS; it can explain BOUNDARY.

## Chronology

```text
CR035A is the next rung after CR001c@19 (which sealed CMB compressed
acoustic geometry at sub-percent precision). The SAM density spine is
FIXED from substrate atoms; the perturbation sector (A_s, n_s, tau)
is FIXED at Planck 2018 posterior centroids in Run A. CR035A does NOT
claim full parameter-free CMB shape closure. The forbidden-file open()
guard was installed at module load and did not trip
(opened_paths_count = 1; forbidden_files_opened = false).
```

## Provenance Chain

```text
Stewardship    = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Precommit      = 0f20f2fde2afb66ed1bbeff8e43e6f183d4159a0d5310d5bdb714daac99a9ced
External data  = Planck PR3 TT/TE/EE bandpowers (locally hashed in HASHES.txt)
Engine         = CAMB 1.6.6
```

---

**Sealed by:** CR035A runner, 2026-06-27.
