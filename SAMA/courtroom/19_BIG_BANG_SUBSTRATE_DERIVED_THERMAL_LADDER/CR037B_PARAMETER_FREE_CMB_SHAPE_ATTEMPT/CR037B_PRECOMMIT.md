# CR037B_PARAMETER_FREE_CMB_SHAPE_ATTEMPT Precommit

## Verdict Ladder

```text
PASS:
  P1 PASS (>= 2 of 3 sub-gates hold)
  AND P2 PASS (chi^2_TT / dof_TT <= 2.0)
  AND polarization NOT degraded (TE <= 3.0 AND EE <= 3.0)

BOUNDARY (i)  — full-shape marginal:
  P1 PASS AND P2 BOUNDARY (2.0 < chi^2_TT/dof <= 3.0)

BOUNDARY (ii) — polarization debt:
  P1 PASS AND P2 PASS but TE chi^2/dof > 3.0 OR EE chi^2/dof > 3.0

FAIL:
  None of the above. There is NO Run B rescue branch.
```

P1 and P2 are load-bearing. TE/EE under Run A are reported with explicit
BOUNDARY trigger. **There is NO Run B optimizer in CR037B.** This is the
parameter-free attempt: the perturbation triplet is fixed to SAM-derived
values, not optimized.

## Test Type

```text
Fresh Courtroom branch test in:
  19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER

External data files (Planck PR3, hashes asserted at seal):
  Planck 2018 PR3 TT/TE/EE full per-multipole bandpower tables.

  COM_PowerSpect_CMB-TT-full_R3.01.txt
    SHA-256 ccf3113604020536f6f13ccf51680a7316ad0f32da558eee7f625e613bdd5522
  COM_PowerSpect_CMB-TE-full_R3.01.txt
    SHA-256 8b2c97d8865ebfdfb2b23c3e6883a39820734b804ba6e353533657b3a2f71425
  COM_PowerSpect_CMB-EE-full_R3.01.txt
    SHA-256 c865c56fe215e17e45eeed1069ddcd7d13365735f439fd63cc9c9325db97d67f

Substrate input + H_0 + perturbations (NEW vs CR036B: all three
perturbations replaced with SAM-derived values):

  Substrate spine (from atoms):
    Omega_m = R*A_0 = 1/pi
    Omega_b = 2*A_0*(1-chi)
    Omega_c = Omega_m - Omega_b

  H_0 (numeric literal cited from CR036 by value; CR036 file NOT opened):
    H_0 = 67.2503751950 km/s/Mpc

  Perturbations (numeric literals cited from CR037A by value;
  CR037A file NOT opened):
    A_s,SAM = 2.1117473568e-9
    n_s,SAM = 0.9646322349
    tau_SAM = 0.0530516477

  Other CAMB inputs unchanged:
    N_eff   = 3.046
    T_CMB   = 2.7255 K
    k_pivot = 0.05 Mpc^-1

Engine:
  CAMB 1.6.6 (same as CR035A2 / CR036B; no swap).

Prior-CR exclusion:
  Forbidden: CR001 / CR001b / CR001c / CR002 / CR003 / CR018b / CR019 /
  CR025 / CR031b / CR032 / CR033 / CR035A / CR035A2 / CR036 / CR036B /
  CR037A / CR205 family files. All H_0 and perturbation values are
  cited as numeric literals; no prior CR file is opened at runtime.
```

## Why This Test Matters

```text
CR036B sealed PASS with the SAM density spine + H_0_SAM derived from
substrate atoms + Planck-centroid (A_s, n_s, tau) perturbations, at
TT chi^2/dof = 1.04. CR037A sealed PASS with all three SAM perturbation
identities (A_s,SAM = eta*sqrt(R); n_s,SAM = 1 - chi/2; tau_SAM = 2*A_0)
inside the Planck posterior at STRONG_CONTACT (<= 0.5 sigma).

CR037B closes the cascade: substrate atoms supply ALL cosmological
inputs (densities + H_0 + perturbations); no externally-anchored
value remains. The Planck PR3 spectra are consulted only as comparison
data; no posterior, chain, or likelihood file is read.

CR037B is the parameter-free CMB shape attempt: there is NO Run B
optimizer. The SAM triplet is run through CAMB as-is. If P1 and P2
both PASS without optimizer rescue, the SAM cascade reproduces the
Planck full per-multipole shape with zero free parameters.

This is the strongest possible verdict the CR037 line can produce.
A PASS at this level is a hard claim: SAM specifies the cosmological
densities, H_0, A_s, n_s, and tau all from substrate atoms (with the
declared T_CMB FIRAS + CODATA dimensional bridge), and the resulting
Boltzmann spectrum matches Planck's binned bandpower table at the
predeclared shape tolerances.
```

## Question

```text
With the SAM density spine + H_0_SAM + SAM perturbation triplet

  Omega_m = R*A_0 = 1/pi                          (substrate)
  Omega_b = 2*A_0*(1-chi)                          (substrate)
  Omega_c = Omega_m - Omega_b                      (substrate)
  H_0     = 67.2503751950 km/s/Mpc                 (CR036 sealed)
  A_s     = 2.1117473568e-9                        (CR037A sealed = eta_SAM*sqrt(R))
  n_s     = 0.9646322349                           (CR037A sealed = 1 - chi/2)
  tau     = 0.0530516477                           (CR037A sealed = 2*A_0)
  N_eff   = 3.046                                  (standard)
  T_CMB   = 2.7255 K                               (FIRAS)
  k_pivot = 0.05 Mpc^-1                            (standard)

does CAMB 1.6.6 reproduce the Planck 2018 PR3 full per-multipole TT
bandpower table on ell in [30, 2500] within the CR035A2 P1 peak
structure + P2 full-shape tolerances, with NO Run B optimizer?
```

## What Changes From CR036B

```text
Three inputs change (all on the perturbation side):

  CR036B:  A_s   = 2.100e-9        (Planck 2018 centroid, externally set)
  CR037B:  A_s   = 2.1117473568e-9 (CR037A sealed; eta_SAM * sqrt(R))

  CR036B:  n_s   = 0.9649          (Planck 2018 centroid, externally set)
  CR037B:  n_s   = 0.9646322349    (CR037A sealed; 1 - chi/2)

  CR036B:  tau   = 0.0544          (Planck 2018 centroid, externally set)
  CR037B:  tau   = 0.0530516477    (CR037A sealed; 2*A_0)

Everything else is identical to CR036B:
  - SAM density spine (Omega_m, Omega_b, Omega_c)
  - H_0 = 67.2503751950 km/s/Mpc
  - Engine: CAMB 1.6.6 with lens_potential_accuracy=1, lmax=2700
  - Planck PR3 file paths + hashes
  - chi^2 over ell in [30, 2500], symmetric per-multipole sigma
  - Peak finder: windows [150,300]/[400,650]/[700,900], prominence >= 50 muK^2,
    sigma_ell=5 smoothing, heights from smoothed curve
  - P1 sub-gates (Delta_ell <= 5/10/10, H ratio <= 15%; >= 2 of 3)
  - P2 bands (PASS <= 2.0, BOUNDARY (2.0, 3.0], FAIL > 3.0)
  - TE/EE reporting + polarization-debt threshold 3.0

NO Run B optimizer. Run B is deleted entirely in CR037B; there is no
rescue branch.
```

## Frozen Sources

### External data files (Planck PR3, hashes asserted at seal)

```text
Planck 2018 PR3 TT/TE/EE full per-multipole bandpower tables.

COM_PowerSpect_CMB-TT-full_R3.01.txt
  SHA-256 ccf3113604020536f6f13ccf51680a7316ad0f32da558eee7f625e613bdd5522
COM_PowerSpect_CMB-TE-full_R3.01.txt
  SHA-256 8b2c97d8865ebfdfb2b23c3e6883a39820734b804ba6e353533657b3a2f71425
COM_PowerSpect_CMB-EE-full_R3.01.txt
  SHA-256 c865c56fe215e17e45eeed1069ddcd7d13365735f439fd63cc9c9325db97d67f

Full filesystem paths:
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-TT-full_R3.01.txt
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-TE-full_R3.01.txt
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-EE-full_R3.01.txt
```

### Fixed non-fit ancillary inputs (in-code literals; NO file read)

```text
T_CMB   = 2.7255 K         # measured thermal anchor
N_eff   = 3.046            # standard radiation-sector input
k_pivot = 0.05 Mpc^-1      # scalar-amplitude convention

These are not optimized, not read from posterior chains, and not
adjusted to improve the CR037B result. They are disclosed fixed
ancillary inputs. The six LCDM-shape parameters under test are
SAM-derived.
```

### CAMB ancillary settings (frozen)

```text
Every CAMB input/default that can affect spectra is frozen in this
precommit and echoed into the summary at runtime, so no hidden CAMB
default can carry the result.

  lmax                        = 2700
  lens_potential_accuracy     = 1
  WantTensors                 = false
  WantScalars                 = true
  r (tensor-to-scalar ratio)  = 0.0
  NonLinear                   = NonLinear_none (CAMB default; not enabled)
  omk (curvature)             = 0.0
  TCMB                        = 2.7255 K
  nnu (effective neutrinos)   = 3.046
  num_massive_neutrinos       = 1
  mnu (sum of neutrino masses) = 0.06 eV    (Planck-baseline)
  YHe handling                = CAMB BBN-consistency
                                (set via set_cosmology default; YHe
                                 computed from omega_b at runtime by
                                 CAMB's internal BBN table)
  pivot_scalar                = 0.05 Mpc^-1
  CMB_unit                    = "muK"
  spectra requested           = ["lensed_scalar"]

The runner shall:
  - emit every one of the above into CR037B_summary.json under
    'camb_settings'
  - emit the actual YHe value used by CAMB (after BBN-consistency
    resolution) into 'camb_settings.YHe_used'
  - emit the full CAMB version string into 'camb_settings.camb_version'
```

### CR036 provenance hash chain (provenance only; NOT read at runtime)

```text
CR036_PRECOMMIT.md SHA-256:
  345a1a8dc180eb6b28141114a82315e3b8d92889537c1219eec4312d59ca33f2
CR036_runner.py SHA-256:
  fe4e570215b2ee0d77b25f88fd4f019fefb1d7dbba4fdab895f7088323490289
CR036_summary.json SHA-256:
  97f3b07bba6e842a8474b62d5ab3b99fdcc8a3261536086d402c51b73ddae3af
CR036_result.md SHA-256:
  fe1c9ee9c6a4ccf3c6f3d7d6e68ca34f93620c2650811f6b519ce636e1c247a6

Canonical H_0_SAM copied from CR036_summary.json by value:
  H_0_SAM = 67.2503751950  km/s/Mpc
```

### CR037A provenance hash chain (provenance only; NOT read at runtime)

```text
CR037A_PRECOMMIT.md SHA-256:
  1b7da85b860825d7e9b0a8e7d231aef92ec980b020341800da81a09f48ba5d78
CR037A_runner.py SHA-256:
  cd7217a7a752f603c89c52160705b6adbbaf58424d1ac290f19ef0b70017a1e3
CR037A_summary.json SHA-256:
  14d8dce9f99c77a919a22bf2e787296b8f37bb6c69a52b582d18a464a8866661
CR037A_result.md SHA-256:
  6f203badf3f1c2c15d8be948e9c94a71fe4055f9fe73ad0b61a82d58db003ddb

Canonical SAM perturbation triplet copied from CR037A_summary.json by value:
  A_s,SAM = 2.1117473568e-9   = eta_SAM * sqrt(R)
  n_s,SAM = 0.9646322349       = 1 - chi/2
  tau_SAM = 0.0530516477       = 2 * A_0

The CR037B runner does NOT read any of the CR037A files. The triplet
above is frozen as numeric literals in this CR037B precommit and the
runner uses those literals directly.
```

### Allowed engine

```text
CAMB 1.6.6 (python module camb)
scipy.signal.find_peaks, scipy.ndimage.gaussian_filter1d
numpy

NOTE: scipy.optimize is NOT used in CR037B. There is no Run B optimizer.
```

### Allowed substrate sources (in-code only; no file read)

```text
R = 12, D = 3, S = 8, alpha_H = 2
A_0 = 1/(12*pi)
chi = (S/D)*A_0 = 2/(9*pi)
Omega_m = R*A_0 = 1/pi
Omega_b = 2*A_0*(1-chi)
Omega_c = Omega_m - Omega_b
H_0    = 67.2503751950 km/s/Mpc       (in-code literal cited from CR036)
A_s    = 2.1117473568e-9              (in-code literal cited from CR037A)
n_s    = 0.9646322349                 (in-code literal cited from CR037A)
tau    = 0.0530516477                 (in-code literal cited from CR037A)
```

### Forbidden branch-local sources

```text
CR037A family files
CR036B family files
CR036 family files
CR035A2 family files
CR035A family files
All other CR family files (CR001-CR003, CR018b, CR019, CR025, CR031b,
  CR032, CR033, CR205)
Any prior CR result.md / summary.json / evidence_rows.csv

The forbidden-file open() guard installed at module load aborts execution
if any of these is opened.
```

## Run A — Single Verdict Path (NO Run B)

```text
1. SAM densities computed in-runner from substrate atoms.
2. H_0 = 67.2503751950 set as numeric literal.
3. A_s, n_s, tau set as numeric literals from CR037A by value.
4. CAMB with SAM cosmology + SAM-derived perturbations + ALL ancillary
   settings frozen per "CAMB ancillary settings (frozen)" above.
5. Compute lensed TT/TE/EE D_l up to lmax = 2700.
6. Evaluate theory at Planck PR3 per-multipole grid (integer ell).
7. For each spectrum X in {TT, TE, EE}:
     sigma_X(ell) = 0.5 * (|-dDl| + |+dDl|)
     residual_X(ell) = D_l^X,SAM(ell) - D_l^X,Planck(ell)
     restrict ell in [30, 2500]
     chi^2_X = sum (residual_X / sigma_X)^2
     dof_X = number of bins included
8. Peak detection (same as CR036B / CR035A2):
     Gaussian smooth D_l with sigma_ell = 5 -> D_l,smooth
     For each window [150,300], [400,650], [700,900]:
       scipy.signal.find_peaks with prominence >= 50 muK^2
       Select single highest-prominence peak in window
       Record ell_peak_i and H_i = D_l,smooth(ell_peak_i)
     Apply symmetrically to SAM theory and Planck data.

There is no Run B. The verdict is determined by Run A only.
```

## P1, P2, TE/EE, Verdict Tree

```text
P1a:  |ell_peak_1_SAM - ell_peak_1_Planck| <= 5
P1b:  |ell_peak_{2,3}_SAM - ell_peak_{2,3}_Planck| <= 10 each
P1c:  |H_{2,3}/H_1 deviation| <= 15% each (heights from sigma_ell=5 smoothed curve)
P1 PASS iff >= 2 of (P1a, P1b, P1c) hold.

P2 PASS:     chi^2_TT/dof <= 2.0
P2 BOUNDARY: 2.0 < chi^2_TT/dof <= 3.0
P2 FAIL:     chi^2_TT/dof > 3.0

TE/EE Run A reported; polarization-debt BOUNDARY (ii) trigger at > 3.0.

Verdict tree:
  IF P1 = PASS and P2 = PASS:
    IF pol_debt:
      verdict = BOUNDARY (ii)
    ELSE:
      verdict = PASS
  ELIF P1 = PASS and P2 = BOUNDARY:
    verdict = BOUNDARY (i)
  ELSE:
    verdict = FAIL

There is no BOUNDARY (iii) branch in CR037B because there is no Run B.
```

## Implementation Discipline

```text
The CR037B runner shall:

1. Install forbidden-file open() guard at module load (expanded to
   include CR037A + CR036 + CR036B + CR035A2 + CR035A family + all
   prior CRs).
2. Compute SAM density spine in-code from substrate atoms.
3. Set H_0 = 67.2503751950 as a numeric literal.
4. Set A_s = 2.1117473568e-9, n_s = 0.9646322349, tau = 0.0530516477
   as numeric literals from CR037A by value.
5. Optionally verify (E1 below) that the literals match the substrate-
   atom closed-form computations to machine precision.
6. Parse Planck PR3 spectra files (same column convention as CR036B).
7. Run CAMB Run A with full SAM cosmology + SAM perturbations.
8. Apply Gaussian smoothing sigma_ell = 5; find peaks in windows with
   prominence >= 50 muK^2; record heights from smoothed curve.
9. Compute P1, P2, polarization-debt, verdict tree.
10. Emit:
    CR037B_summary.json
    CR037B_result.md
    CR037B_TT_residuals.csv
    CR037B_TE_residuals.csv
    CR037B_EE_residuals.csv
    CR037B_peaks.csv
    CR037B_runA_theory_spectra.csv

No fitting in CR037B:
  free_parameters_introduced       = 0
  external_perturbation_disclosed  = false (SAM perturbations replace Planck centroids)
  prior_CR_result_inputs           = false
  CR036_files_opened               = false
  CR036B_files_opened              = false
  CR037A_files_opened              = false
  Run_B_optimizer_used             = false
  camb_settings                    = (full echo per "CAMB ancillary settings (frozen)")
  YHe_used                         = (extracted from CAMB at runtime;
                                       BBN-consistency value)
  camb_version                     = (recorded from camb.__version__)
```

## Reported Evidence (not gates)

```text
E1 — Algebraic verification:
  Verify A_s_literal       == eta_SAM_from_atoms * sqrt(R)  to machine precision
  Verify n_s_literal       == 1 - chi_from_atoms / 2        to machine precision
  Verify tau_literal       == 2 * A_0_from_atoms            to machine precision
  Report relative deviations.
  This is implementation integrity; not gated.

E2 — Direct comparison vs CR036B (reported only):
  The CR036B result.md is NOT read at runtime. The numeric values
    CR036B TT chi^2/dof = 1.0413
    CR036B TE chi^2/dof = 1.0443
    CR036B EE chi^2/dof = 1.0430
  are cited in this precommit as numeric constants for comparison
  context. The runner does NOT consult CR036B summary or residuals.

E3 — Run A spectra products for downstream re-use:
  Emit CR037B_runA_theory_spectra.csv with the full TT/TE/EE D_l on
  integer ell up to 2700, plus the SAM cosmology inputs used.
```

## Chronology and Honest Framing

```text
This precommit follows CR037A sealed PASS (all three SAM perturbation
identities inside Planck posterior at STRONG_CONTACT). CR037B closes
the cascade by running the full SAM-derived cosmology (densities + H_0
+ perturbations) through the CR036B/CR035A2 CAMB pipeline with NO
Run B optimizer.

The honest framing is:

  CR037B is the parameter-free CMB shape attempt. The SAM perturbation
  triplet (A_s, n_s, tau) is fixed at the CR037A-sealed values. There
  is no Run B optimizer; the spectra are computed once and the verdict
  follows from P1 and P2 directly.

  A CR037B PASS means: SAM specifies the cosmological densities, H_0,
  and (A_s, n_s, tau) all from substrate atoms plus the FIRAS T_CMB
  thermal anchor and CODATA 2018 / SI fixed constants. The Boltzmann
  spectrum computed from these inputs reproduces the Planck PR3 binned
  TT shape inside the CR035A2 P1 / P2 tolerances with zero free
  parameters.

Do not write:
  CR037B "proves" cosmology.
  CR037B closes the SM-LCDM joint.

Do write:
  CR037B is the parameter-free CMB shape attempt. The SAM-derived
  cosmological inputs (densities + H_0 + perturbation triplet) are
  fixed; the resulting CAMB spectrum is compared to the Planck PR3
  TT bandpower table at the CR035A2 shape tolerances.
```

## Rule-9 Line

```text
This test could have falsified the claim that the SAM-derived
cosmological inputs

  Omega_m = 1/pi, Omega_b = 2*A_0*(1-chi), Omega_c = Omega_m - Omega_b
  H_0 = 67.2503751950 km/s/Mpc
  A_s = 2.1117473568e-9   = eta_SAM * sqrt(R)
  n_s = 0.9646322349       = 1 - chi/2
  tau = 0.0530516477       = 2 * A_0

paired with CAMB 1.6.6 (lens_potential_accuracy=1, lmax=2700),
reproduce the Planck 2018 PR3 full per-multipole TT bandpower table
at the CR035A2 P1 peak structure + P2 full-shape tolerances, with NO
Run B optimizer.

It fails if either P1 fails or P2 returns FAIL (chi^2_TT/dof > 3.0).
There is no Run B rescue branch.
```

## Result Text Requirements

```text
If PASS:
  CR037B PASS confirms that the SAM-derived cosmological inputs
  (densities + H_0 + perturbation triplet, all from substrate atoms
  via FIRAS T_CMB + CODATA 2018 / SI fixed constants) reproduce the
  Planck 2018 PR3 full per-multipole TT bandpower table within the
  CR035A2 P1 peak structure + P2 full-shape tolerances, with NO free
  parameters and NO Run B optimizer.

If BOUNDARY: state which case (i)/(ii) triggered with diagnostic values.

If FAIL: state which gate failed and by how much.

In all cases:
  execution_status                = CLEAN or not CLEAN with reason
  free_parameters_introduced      = 0
  prior_CR_result_inputs          = false
  Run_B_optimizer_used            = false
  CR036_files_opened              = false
  CR036B_files_opened             = false
  CR037A_files_opened             = false
  forbidden_files_opened          = false
  camb_settings                   = full echo (lmax, lens_potential_accuracy,
                                    WantTensors, WantScalars, r, NonLinear,
                                    omk, TCMB, nnu, num_massive_neutrinos,
                                    mnu, YHe_used, pivot_scalar, CMB_unit,
                                    spectra, camb_version)
```

## Manuscript Headline If PASS (conditional)

```text
SAM derives the full cosmological input set from substrate atoms + the
FIRAS thermal anchor + CODATA 2018 / SI fixed constants:
  Omega_m, Omega_b, Omega_c   from substrate atoms (CR018b road, sealed)
  H_0                          from eta_SAM cascade (CR036 sealed)
  A_s, n_s, tau                from substrate atoms (CR037A sealed)
The resulting CAMB Boltzmann spectrum reproduces the Planck 2018 PR3
full per-multipole TT bandpower table at the CR035A2 P1 / P2
tolerances, with zero free parameters and no perturbation-sector
optimizer.
```

## Connection to Future Work

```text
CR037C placeholder
  External-catalog independence test for the CR037B PASS: re-run with
  a non-Planck high-ell experiment if available.

CR036A_E5_FIX placeholder (open from CR036 sealing)
  Correct the E5 z_eq_SAM unit bug in CR036 reported evidence.
```

## Stewardship Reference

```text
STEWARDSHIP_DECLARATION.md SHA-256
  d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```
