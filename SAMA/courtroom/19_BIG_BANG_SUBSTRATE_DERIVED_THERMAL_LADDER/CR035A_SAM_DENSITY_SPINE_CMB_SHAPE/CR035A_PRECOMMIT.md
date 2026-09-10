# CR035A_SAM_DENSITY_SPINE_CMB_SHAPE Precommit

## Verdict Ladder

```text
PASS:
  Run A (fixed Planck 2018 perturbation parameters with the SAM density
  spine) holds both:
    P1  acoustic geometry / peak-structure gate
    P2  TT full-shape gate at chi^2/dof <= 2.0

BOUNDARY:
  Any one of:
    (i)  Run A P1 holds and P2 chi^2/dof in (2.0, 3.0]
    (ii) Run A P1 + P2 hold but TE+EE are badly degraded
         (TE chi^2/dof > 3.0 or EE chi^2/dof > 3.0)
    (iii) Run A FAILS but Run B (diagnostic optimization of
          A_s, n_s, tau with SAM densities frozen) rescues the shape
          using A_s, n_s, tau values all within +/- 5 sigma of the
          Planck 2018 posterior centroids.
    Optimization cannot rescue a PASS; it can only explain a BOUNDARY.

FAIL:
  Run A P2 chi^2/dof > 3.0 AND Run B optimization either still fails
  (chi^2/dof > 3.0) or requires A_s, n_s, or tau values beyond +/- 5
  sigma of Planck 2018 posterior centroids.
```

P1 and P2 are the load-bearing scientific claims under Run A. Run B is
diagnostic only. TE/EE under Run A are reported evidence with explicit
BOUNDARY trigger. All wrong controls and algebra checks are sensitivity
evidence only and do not gate the verdict.

This precommit deliberately does NOT claim full parameter-free CMB shape
closure. The SAM density spine is fixed from substrate atoms; the
perturbation sector (A_s, n_s, tau) is disclosed external input.

## Test Type

```text
Fresh Courtroom branch test in:
  19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER

External anchors:
  Planck 2018 PR3 binned TT/TE/EE bandpowers (COM_PowerSpect_CMB-*-full_R3.01.txt)
  Planck 2018 base_plikHM_TTTEEE_lowl_lowE_lensing minimum theory spectrum
    (for Run A reference and best-fit perturbation parameters)

Substrate input:
  SAM density spine computed from substrate atoms only.

CMB engine:
  CAMB 1.6.6 (canonical).
  CLASS optional cross-check only. No engine swap after precommit seal.

Prior-CR exclusion:
  No CR001 / CR001b / CR001c / CR002 / CR003 / CR018b / CR019 / CR031b /
  CR032 / CR033 / CR205 or any prior CR result/summary/evidence file may
  be read by the runner. The SAM density spine and H_0 anchor are
  recomputed inside CR035A from substrate atoms and the documented
  CR018b CMB-side anchor value; no file is imported from CR018b or any
  other prior CR.
```

## Why This Test Matters

```text
CR001c@19 established that the SAM substrate spine reproduces the
compressed CMB acoustic geometry (recombination, drag epoch, sound
horizon, last-scattering peak position) at sub-percent precision. That
is a low-dimensional shape test on a handful of derived scalars.

CR035A is the next rung: does the same SAM density spine, when fed
through a standard Boltzmann solver (CAMB) with disclosed external
perturbation parameters, reproduce the FULL TT (and reported TE / EE)
binned bandpower spectrum that Planck 2018 actually measured across
the multipole range ell = 30..2500?

This is a stronger test in three ways:
  - it exposes the damping tail, not just peak positions;
  - it exposes peak-height ratios, not just peak locations;
  - it exposes the full residual shape against the official Planck
    binned spectra rather than against compressed summary statistics.

A clean PASS at Run A would mean: SAM densities + Planck-best-fit
A_s, n_s, tau reproduce the Planck spectra at the binned-shape level.
A BOUNDARY would localize the residual debt to the perturbation sector
(or to TE/EE alone). A FAIL would falsify the SAM density spine at
full-spectrum precision.

CR035A is a SAM-density-spine locked test, not a parameter-free
closure. The honest claim is: SAM specifies omega_b and omega_c
from substrate atoms; A_s, n_s, tau remain external Planck-anchored
inputs at this stage. CR035B (deferred) will reconnect against the
official Planck likelihood with full nuisance/foreground machinery.
```

## Question

```text
Does the SAM density spine

  Omega_m = R * A_0 = 1/pi
  Omega_b = 2 * A_0 * (1 - chi)
  Omega_c = Omega_m - Omega_b
  H_0     = 68.76 km/s/Mpc          (CR018b@06 CMB-side anchor; value cited, file not read)

when fed to CAMB 1.6.6 together with the disclosed external Planck 2018
perturbation parameters

  A_s   = 2.100e-9                  (Planck 2018 base posterior centroid)
  n_s   = 0.9649                    (Planck 2018 base posterior centroid)
  tau   = 0.0544                    (Planck 2018 base posterior centroid)
  N_eff = 3.046                     (standard)
  T_CMB = 2.7255 K                  (FIRAS)

reproduce the Planck 2018 PR3 binned TT bandpower spectrum
(COM_PowerSpect_CMB-TT-full_R3.01.txt) over ell in [30, 2500] such that:

  P1: the first three TT acoustic-peak locations and the peak-height
      ratios H2/H1 and H3/H1 match Planck binned values within the
      predeclared tolerances; AND

  P2: the binned-spectrum chi^2 over ell in [30, 2500] satisfies
      chi^2 / dof <= 2.0?

TE and EE binned chi^2 / dof are reported but not gated.
```

## SAM Density Spine (substrate-derived; fixed)

```text
Substrate atoms (sealed):
  R        = 12
  D        = 3
  S        = 8
  alpha_H  = 2
  A_0      = 1/(12*pi)              = 0.026525823848649224
  chi      = (S/D)*A_0 = 2/(9*pi)   = 0.070735530263064592

Cosmological densities (sealed identities):
  Omega_m  = R * A_0 = 1/pi          = 0.318309886183790672
  Omega_b  = 2*A_0*(1 - chi)         = 0.049299011266100756
  Omega_c  = Omega_m - Omega_b       = 0.269010874917689916

H_0 anchor (CMB-side; value cited, file not read):
  H_0 = 68.76 km/s/Mpc
  h   = 0.6876

Physical densities:
  omega_b = Omega_b * h^2 = 0.0233082649  (target)
  omega_c = Omega_c * h^2 = 0.1271866630  (target)

These are close enough to Planck-space to make the test worth running
but not identical enough to assume it passes.
```

## External Perturbation Inputs (disclosed; Run A fixes them)

```text
A_s    = 2.100e-9       (Planck 2018 base_plikHM_TTTEEE_lowl_lowE_lensing posterior centroid)
n_s    = 0.9649         (Planck 2018 base posterior centroid)
tau    = 0.0544         (Planck 2018 base posterior centroid)
N_eff  = 3.046          (standard)
T_CMB  = 2.7255 K       (FIRAS)
k_pivot = 0.05 Mpc^-1   (Planck 2018 pivot scale; A_s definition)

Run B optimization (diagnostic, not a gate):
  minimize chi^2_TT( SAM_densities, A_s, n_s, tau )
  over A_s in [1.7e-9, 2.5e-9]
       n_s in [0.93, 1.00]
       tau in [0.02, 0.10]
  with SAM densities held fixed at the spine above.

  Report:
    A_s_optimized, n_s_optimized, tau_optimized
    sigma-deviation from Planck posterior centroid for each
    chi^2/dof at the optimum (TT, TE, EE)
```

## Strict Input Discipline

```text
The CR035A runner may read only the following inputs:

External raw data
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-TT-full_R3.01.txt
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-TE-full_R3.01.txt
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-EE-full_R3.01.txt
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-base-plikHM-TTTEEE-lowl-lowE-lensing-minimum-theory_R3.01.txt

Engine
  CAMB 1.6.6 (Python module camb)

Substrate constants (in-code only; no file read)
  R = 12, D = 3, S = 8, alpha_H = 2
  A_0 = 1/(12*pi), chi = 2/(9*pi)
  Omega_m = 1/pi
  Omega_b = 2*A_0*(1-chi)
  Omega_c = Omega_m - Omega_b
  H_0     = 68.76

External perturbation values (in-code only; no file read)
  A_s = 2.100e-9, n_s = 0.9649, tau = 0.0544, N_eff = 3.046, T_CMB = 2.7255

Physical constants (in-code only)
  k_pivot = 0.05 Mpc^-1
```

## Forbidden Inputs

```text
The CR035A runner must not read, import, parse, compare against, or use:

  CR001_summary.json / result.md / evidence_rows.csv
  CR001b_summary.json / result.md / evidence_rows.csv
  CR001c_summary.json / result.md / evidence_rows.csv
  CR002_summary.json / result.md / evidence_rows.csv
  CR003_summary.json / result.md / evidence_rows.csv
  CR018b_summary.json / result.md / evidence_rows.csv
  CR019_summary.json / result.md / evidence_rows.csv
  CR025_summary.json / result.md / evidence_rows.csv
  CR031b_summary.json / result.md / evidence_rows.csv
  CR032_summary.json / result.md / evidence_rows.csv
  CR033_summary.json / result.md / evidence_rows.csv
  CR205 files or summaries
  any prior CR result.md / summary.json / evidence_rows.csv
  any other prior thermal-ladder, fate, horizon, or substrate-derivation
  artifact

The forbidden-file open() guard installed at runner module load must
abort execution if any of these files is opened.

H_0 = 68.76 is cited as a numeric constant in CR035A (Planck-side anchor
sealed in CR018b@06). The CR018b file is NOT opened by the runner.
```

## Engine Specification

```text
Canonical engine:
  CAMB version 1.6.6 (Python module `camb`).

Engine controls:
  WantCls = True
  WantTransfer = False
  set_for_lmax(lmax=3000, lens_potential_accuracy=1)
  Accuracy boost = 1.0 (defaults), lAccuracyBoost = 1.0
  set_cosmology(H0, ombh2, omch2, mnu=0.06, omk=0, tau)
  InitPower.set_params(As, ns, pivot_scalar=0.05)

Outputs requested:
  Lensed CMB power spectra (TT, TE, EE) in muK^2, D_l convention
  (D_l = l(l+1)*C_l/(2*pi)).

CLASS may be run as an OPTIONAL E-only cross-check (TT spectrum, fixed
Planck perturbations) and reported in evidence; CLASS results do not
gate the verdict and are not run if CLASS is not installed.

No engine swap after this precommit is sealed. If CAMB import fails
at runtime, the runner aborts and the result is not produced; do not
silently substitute CLASS.
```

## Run A — Verdict Path (fixed Planck perturbation parameters)

```text
1. Compute SAM densities from substrate atoms.
2. Set CAMB cosmology with the SAM density spine + fixed external
   perturbation parameters listed above.
3. Compute lensed CMB power spectra D_l^TT, D_l^TE, D_l^EE up to lmax=3000.
4. Bin the theory spectra onto the Planck PR3 multipole grid:
     ell_bin = the multipole grid taken from COM_PowerSpect_CMB-TT-full_R3.01.txt
     (the file's own ell column is the binning target for TT; same
      treatment for TE and EE files individually).
5. For each spectrum X in {TT, TE, EE}:
     Compute symmetric per-bin uncertainty sigma_X(ell) =
       0.5 * (|-dDl(ell)| + |+dDl(ell)|) using the file's lower/upper
       error columns.
     Compute residual r_X(ell) = D_l^X,SAM(ell) - D_l^X,Planck(ell).
     Restrict to ell in [30, 2500].
     Compute chi^2_X = sum_ell ( r_X(ell) / sigma_X(ell) )^2.
     Compute dof_X = number of ell bins in [30, 2500].
     Report chi^2_X / dof_X.

6. Identify the first three TT acoustic peaks in BOTH the SAM theory
   and the Planck binned data using a peak-finding routine that
   operates on lightly smoothed D_l (Gaussian smoothing in ell with
   sigma = 5; same kernel applied to both); peak = local maximum of
   D_l within ell in (50, 2700).
   Record peak ell_peak_1, ell_peak_2, ell_peak_3 and heights
   H_1, H_2, H_3 for SAM and Planck independently.
```

## Run B — Diagnostic Optimization (does NOT gate verdict)

```text
With SAM densities held fixed, minimize the TT chi^2 over the
perturbation triplet (A_s, n_s, tau) using scipy.optimize.minimize
(method 'L-BFGS-B') with bounds:
  A_s   in [1.7e-9, 2.5e-9]
  n_s   in [0.93, 1.00]
  tau   in [0.02, 0.10]

Report:
  A_s_opt, n_s_opt, tau_opt
  sigma-deviation from Planck posterior centroids
    A_s_sigma = 0.030e-9
    n_s_sigma = 0.0042
    tau_sigma = 0.0073
  chi^2_TT, chi^2_TE, chi^2_EE at the optimum, with dof per spectrum.

Run B is diagnostic only. It can EXPLAIN a BOUNDARY (perturbation-sector
debt). It cannot promote a Run A FAIL to PASS.
```

## P1 — Acoustic Geometry / Peak-Structure Gate (Run A)

```text
P1a:
  |ell_peak_1_SAM - ell_peak_1_Planck| <= 5

P1b:
  |ell_peak_2_SAM - ell_peak_2_Planck| <= 10
  |ell_peak_3_SAM - ell_peak_3_Planck| <= 10

P1c:
  |H_2_SAM / H_1_SAM  -  H_2_Planck / H_1_Planck|  /  (H_2_Planck / H_1_Planck)  <= 0.15
  |H_3_SAM / H_1_SAM  -  H_3_Planck / H_1_Planck|  /  (H_3_Planck / H_1_Planck)  <= 0.15

P1 PASS:
  At least two of P1a, P1b, P1c hold.

P1 FAIL:
  Any two of P1a, P1b, P1c fail.
```

## P2 — TT Full-Shape Gate (Run A)

```text
chi^2_TT computed over ell in [30, 2500] using symmetric Planck
per-bin sigma. The dof is the number of bins included.

P2 PASS:        chi^2_TT / dof_TT <= 2.0
P2 BOUNDARY:    2.0 < chi^2_TT / dof_TT <= 3.0, provided P1 holds
P2 FAIL:        chi^2_TT / dof_TT > 3.0

P2 is load-bearing. P2 PASS requires P1 PASS for an overall CR035A PASS.
```

## E_TE / E_EE — Reported Evidence (NOT a Hard Gate)

```text
E_TE:
  Report chi^2_TE / dof_TE over ell in [30, 2500].
  Report sign agreement (fraction of bins where sign of D_l^TE,SAM
  matches sign of D_l^TE,Planck) and phase-position diagnostic
  (location of the first TE zero crossing).

E_EE:
  Report chi^2_EE / dof_EE over ell in [30, 2500].
  Report EE first acoustic-peak location agreement.

BOUNDARY trigger (polarization debt):
  TT passes (P1 + P2) but at least one of:
    chi^2_TE / dof_TE > 3.0
    chi^2_EE / dof_EE > 3.0
  Result is BOUNDARY case (ii).
```

## Implementation Discipline

```text
The CR035A runner shall:

1. Compute SAM density spine in-code from substrate atoms; no file read.
2. Set fixed external perturbation parameters as numeric literals; no
   prior CR file read.
3. Install the forbidden-file open() guard at module load (Python
   builtins.open wrapper). Any attempt to open a forbidden CR file
   aborts execution with a clear error.
4. Parse Planck PR3 spectra files (TT, TE, EE) with column convention:
     col 1 = ell
     col 2 = D_l in muK^2
     col 3 = -dDl (lower error)
     col 4 = +dDl (upper error)
   Symmetric sigma per bin = 0.5 * (|-dDl| + |+dDl|).
5. Run CAMB with SAM cosmology + fixed perturbations.
   Compute lensed TT, TE, EE D_l on integer ell grid 2..3000.
6. Bin theory D_l onto the Planck bandpower ell grid by direct lookup
   (Planck PR3 spectra files give per-ell D_l on integer ell; no further
   binning required beyond restricting to ell in [30, 2500]).
7. Compute chi^2_TT, chi^2_TE, chi^2_EE and apply P2 gate to TT.
8. Run peak-finder on lightly smoothed D_l (Gaussian sigma_ell = 5).
   Apply P1 gates.
9. Run B: optimize (A_s, n_s, tau) with scipy L-BFGS-B; report
   diagnostic deltas, do not gate.
10. Emit:
    CR035A_summary.json
    CR035A_result.md
    CR035A_TT_residuals.csv
    CR035A_TE_residuals.csv
    CR035A_EE_residuals.csv
    CR035A_peaks.csv
    CR035A_runB_diagnostic.json
    CR035A_runA_theory_spectra.csv

Precision:
  CAMB defaults (Accuracy = 1.0; sufficient for binned-shape test).
  pi = math.pi
  Reported chi^2 to 6 significant digits.

No fitting in Run A:
  free_parameters_introduced_in_RunA = 0
  empirical_X_inf_input              = false
  prior_CR_result_inputs             = false
```

## Frozen Sources

```text
Allowed external sources
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-TT-full_R3.01.txt
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-TE-full_R3.01.txt
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-EE-full_R3.01.txt

Allowed engine
  CAMB 1.6.6 (Python module)
  scipy.optimize (L-BFGS-B for Run B only)
  numpy

Allowed substrate sources
  R = 12, D = 3, S = 8, alpha_H = 2
  A_0 = 1/(12*pi), chi = 2/(9*pi)
  Omega_m = 1/pi

Forbidden branch-local sources
  CR001 / CR001b / CR001c / CR002 / CR003 family files
  CR018b / CR019 family files
  CR025 / CR031b / CR032 / CR033 family files
  CR205 files
  any prior per-galaxy / per-spectrum / per-chain result file

The runner may check that these forbidden files were not opened.
```

## Chronology and Honest Framing

```text
This precommit is drafted AFTER CR001c@19 sealed CMB compressed
acoustic geometry at sub-percent precision. CR035A is a follow-on
that escalates the test from compressed-summary to full-shape
binned-bandpower comparison, with the same SAM density spine.

The honest framing is:

  CR035A locks the SAM cosmological density spine
  (Omega_m = 1/pi, Omega_b = 2*A_0*(1-chi), Omega_c = Omega_m - Omega_b,
   H_0 = 68.76) from substrate atoms. The perturbation sector
  (A_s, n_s, tau) is fixed at Planck 2018 posterior-centroid values
  in Run A, and optimized as diagnostic evidence only in Run B.

  CR035A does NOT claim full parameter-free CMB shape closure.
  CR035A claims, conditional on PASS:

    "The SAM density spine, when paired with standard Planck 2018
     perturbation parameters and a standard Boltzmann engine (CAMB),
     reproduces the Planck binned TT bandpower spectrum to within
     chi^2_TT / dof <= 2.0 over ell in [30, 2500] and the first
     three acoustic-peak locations and height ratios within the
     predeclared P1 tolerances."

Do not write:
  SAM derives the CMB.
  SAM has zero free parameters at the CMB level.

Do write:
  SAM fixes the cosmological density spine from substrate atoms;
  the perturbation sector remains externally anchored at this stage.
  CR035A PASS would extend CR001c's compressed-geometry result to
  the full binned-shape level.
```

## Rule-9 Line

```text
This test could have falsified the claim that the SAM density spine
Omega_m = 1/pi, Omega_b = 2*A_0*(1 - chi), Omega_c = Omega_m - Omega_b,
H_0 = 68.76 km/s/Mpc, when paired with fixed Planck 2018 posterior-
centroid perturbation parameters (A_s = 2.100e-9, n_s = 0.9649,
tau = 0.0544) and the standard Boltzmann engine CAMB 1.6.6, reproduces
the Planck 2018 PR3 binned TT bandpower spectrum on ell in [30, 2500]
at acoustic-peak structure (P1) and full-shape (P2) tolerances.

It fails if:
  P1 fails (two of three sub-gates fail), AND/OR
  P2 chi^2_TT / dof_TT > 3.0, AND
  Run B optimization still produces chi^2_TT / dof_TT > 3.0 OR requires
  any of A_s, n_s, tau more than 5 sigma from the Planck 2018 posterior
  centroid.

It is BOUNDARY if peak geometry survives but full-shape or polarization
spectra are degraded, OR if Run B rescues with reasonable perturbation
values within 5 sigma of the Planck posterior.
```

## Result Text Requirements

```text
If P1 PASSES and P2 PASSES, CR035A_result.md must state:

  CR035A PASS confirms that the SAM density spine
  (Omega_m = 1/pi, Omega_b = 2*A_0*(1 - chi), Omega_c = Omega_m - Omega_b,
   H_0 = 68.76), paired with Planck 2018 posterior-centroid
  perturbation parameters (A_s, n_s, tau) and CAMB 1.6.6, reproduces
  the Planck 2018 PR3 binned TT bandpower spectrum over ell in
  [30, 2500] at chi^2_TT / dof_TT <= 2.0 and matches the first three
  acoustic-peak locations and height ratios within the predeclared
  P1 tolerances. The SAM densities are derived from substrate atoms;
  the perturbation sector (A_s, n_s, tau) remains an externally
  anchored Planck-2018 input at this stage. Full parameter-free CMB
  shape closure is NOT claimed.

If BOUNDARY (any case), CR035A_result.md must state which BOUNDARY
case triggered and the diagnostic Run B values.

If FAIL, CR035A_result.md must state:

  CR035A FAIL rejects the SAM density spine, at the binned-shape
  level on Planck 2018 TT, under fixed Planck-posterior-centroid
  perturbation parameters. Run B diagnostic optimization did not
  rescue the shape within the +/- 5 sigma Planck-posterior bound.

In all cases the result must report:
  execution_status                  = CLEAN or not CLEAN with reason
  prior_CR_result_inputs            = false
  free_parameters_introduced_RunA   = 0
  external_perturbation_disclosed   = true
  forbidden_files_opened            = false
```

## Manuscript Headline If PASS

```text
Conditional manuscript language (PASS only):

  The SAM density spine, derived from substrate atoms via
  Omega_m = R * A_0 = 1/pi and Omega_b = 2 * A_0 * (1 - chi), when
  paired with the standard Planck 2018 perturbation parameters
  (A_s, n_s, tau) and the standard Boltzmann engine CAMB, reproduces
  the Planck 2018 binned TT bandpower spectrum at full-shape
  precision (chi^2_TT / dof_TT <= 2.0 over ell in [30, 2500]) and
  matches the first three acoustic-peak locations and height ratios
  within the predeclared CR035A tolerances.

Do NOT claim:
  SAM derives the CMB from substrate atoms alone.
  Zero-parameter CMB closure.
  Full perturbation-sector derivation.

Do write:
  SAM specifies the cosmological density spine (omega_b, omega_c)
  from substrate atoms with zero free parameters in the density
  sector. The perturbation sector (A_s, n_s, tau) is fixed at
  externally measured Planck 2018 values. Joint substrate +
  Planck-perturbation closure on the binned TT bandpower spectrum
  is documented in CR035A; full Planck likelihood treatment is
  deferred to CR035B.
```

## Connection to Future Work

```text
CR035B placeholder
  Reconnect the SAM density spine with the OFFICIAL Planck 2018
  likelihood (clik / Cobaya), including nuisance parameters,
  foregrounds, beam transfer functions, gains, and low-ell + lowE
  treatment. This is the full-likelihood version of CR035A.

CR036 placeholder
  Derive A_s, n_s, tau from substrate atoms, or document the
  structural gap. Only after CR036 (or its FAIL counterpart) can
  any "parameter-free CMB" claim be made honestly.

CR037 placeholder (optional)
  CLASS cross-check of CR035A: re-run the same SAM density spine
  + fixed perturbations through CLASS and report TT chi^2/dof,
  peak structure, and TE/EE for an engine consistency check.
```

## Stewardship Reference

```text
STEWARDSHIP_DECLARATION.md SHA-256
  d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```
