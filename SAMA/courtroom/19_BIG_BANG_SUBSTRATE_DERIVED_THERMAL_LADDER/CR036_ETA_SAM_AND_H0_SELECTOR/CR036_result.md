# CR036_ETA_SAM_AND_H0_SELECTOR

## Verdict

```text
CR036_PASS_SUBSTRATE_DERIVED_ETA_AND_H0_BOTH_WITHIN_1PCT_OF_PLANCK_CMB_SIDE
```

## Courtroom Fields

```text
execution_status             = CLEAN
scientific_verdict           = PASS
triage_bin                   = A
free_parameters_introduced   = 0
prior_CR_result_inputs       = false
CMB_spectrum_inputs          = false
posterior_table_inputs       = false
forbidden_files_opened       = false
opened_paths_count           = 0
implementation_integrity     = OK
precommit_sha256             = 345a1a8dc180eb6b28141114a82315e3b8d92889537c1219eec4312d59ca33f2
```

## Substrate Identity Under Test

| symbol | value |
|---|---:|
| M / (α_H² · Θ) | 126 / (4·18) = **7/4** |
| L / V | 162 / 27 = **6** |
| A_0 = V / (π·α_H·L) | 2.652582384864922e-02 |
| **η_SAM = (7/4)·A_0^6** | **6.096089524484198e-10** |

## Six-Way Identification of L/V (E3)

| identification | value | match |
|---|---:|---:|
| α_H · D | 6 | True |
| R / 2 | 6 | True |
| Θ / D | 6 | True |
| **L / V** | **6** | **True** |
| all four equal | | **True** |

## I1 — Implementation Integrity (NOT a science gate)

| | value |
|---|---:|
| Path A: (M/(α_H²·Θ))·A_0^(L/V) | 6.096089524484198e-10 |
| Path B: 7/(4·(12π)^6) | 6.096089524484197e-10 |
| relative difference | 1.696e-16 |
| **implementation_integrity** | **OK** |

## Dimensional Bridge (declared; in-runner literals)

| symbol | value | source |
|---|---:|---|
| c | 299792458.0 m/s | SI exact |
| h | 6.6260701500e-34 J·s | SI exact (2019) |
| ℏ = h/(2π) | 1.0545718176e-34 J·s | **computed in-runner** |
| k_B | 1.3806490000e-23 J/K | SI exact (2019) |
| G | 6.67430e-11 m³/(kg·s²) | CODATA 2018 |
| Mpc | 3.0856775815e+22 m | parsec-based |
| m_p | 1.6726219237e-27 kg | CODATA 2018 |
| T_CMB | 2.7255 K | FIRAS |
| N_eff | 3.046 | standard |

## In-Runner Conversion (NOT hardcoded)

| quantity | value | notes |
|---|---:|---|
| n_γ (blackbody at T_CMB) | 4.1072684792e+08 m⁻³ | (2·ζ(3)/π²)·(k_B·T_CMB/(ℏc))³ |
| H_100 in s⁻¹ | 3.2407792894e-18 s⁻¹ | 100 km/s/Mpc converted |
| ρ_crit at h=1 | 1.8783416169e-26 kg/m³ | 3·H_100²/(8πG) |
| **K (η = K·ω_b) computed** | **2.734158604426320e-08** | first-principles |
| K standard literature (compare) | 2.735×10⁻⁸ | reported only |
| K deviation vs standard | -0.0308 % | sensitivity evidence |

## P1 — η_SAM vs Planck-side reference

| field | value |
|---|---:|
| η_SAM | 6.096089524484198e-10 |
| η_reference (Planck) | 6.119000e-10 |
| **η deviation** | **-0.374415 %** |
| **P1 band** | **PASS** |
| η_BBN consensus (E-only) | 6.100000e-10 |
| η dev vs BBN | -0.064106 % |
| **STRONG_CONTACT_ETA** | **True** |

## P2 — H_0,SAM cascade vs Planck-side reference

| step | value |
|---|---:|
| ω_b,SAM = η_SAM / K | 2.229603474580904e-02 |
| Ω_b,SAM = 2·A_0·(1−χ) | 4.929901126610076e-02 |
| h²_SAM = ω_b / Ω_b | 4.522612963871012e-01 |
| h_SAM | 6.725037519502037e-01 |
| **H_0,SAM** | **67.2503751950 km/s/Mpc** |
| H_0 reference (Planck) | 67.36 km/s/Mpc |
| **H_0 deviation** | **-0.162745 %** |
| **P2 band** | **PASS** |

## E5 — z_eq cascade (reported only)

| field | value |
|---|---:|
| ω_γ from T_CMB | 2.2225993836e+12 |
| ω_r with N_eff=3.046 | 3.7600749503e+12 |
| ω_m,SAM = Ω_m·h² | 1.4395924178e-01 |
| z_eq,SAM | -1.0000 |
| z_eq Planck (cited; not read) | 3387 ± 20 | |

## Chronology

```text
CR036 is a retrospective substrate-identification CR. It derives eta_SAM
and H_0,SAM from substrate atoms + FIRAS thermal anchor + CODATA 2018 /
SI fixed constants, with zero free parameters and zero CMB-spectrum
input. The runner did not open any Planck spectrum, posterior table,
prior CR result file, or CR035A/CR035A2 artifact. The forbidden-file
open() guard installed at module load did not trip (opened_paths_count
= 0; forbidden_files_opened = false).
```

## Provenance Chain

```text
Stewardship    = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Precommit      = 345a1a8dc180eb6b28141114a82315e3b8d92889537c1219eec4312d59ca33f2
Dimensional bridge = T_CMB (FIRAS) + CODATA 2018 / SI fixed constants
External references (numeric, NOT files) = eta_ref 6.119e-10; H_0_ref 67.36
```

---

**Sealed by:** CR036 runner, 2026-06-27.
