# CR035A2_PEAK_FINDER_AUDIT Precommit

## Appeal Basis

```text
CR035A v2 (precommit hash 0f20f2fde2afb66ed1bbeff8e43e6f183d4159a0d5310d5bdb714daac99a9ced;
runner hash 4b3d07483f331dd5a2dbf28681b69b476a7641e0e57b35c4c9ea8fbe6e222305;
summary hash e9ddae54b4e6000e53bf440356ea4411d99678d14e872889e4e1e3f56d40d11b)
sealed verdict FAIL on 2026-06-27 with the following characteristics:

  TT chi^2/dof  = 1.3464  (P2 PASS:  <= 2.0)
  TE chi^2/dof  = 1.1941  (reported PASS)
  EE chi^2/dof  = 1.1246  (reported PASS)
  P1a (first peak Delta_ell):  PASS  (Delta_ell = 0; theory 219, Planck 219)
  P1b (2nd/3rd peak Delta_ell): FAIL (2nd Delta_ell = 13; 3rd Delta_ell = 145)
  P1c (height ratios):          half (H2/H1 PASS; H3/H1 FAIL)
  P1 overall:                   FAIL (1 of 3 sub-gates)

  Run B optimum:  A_s +1.32 sigma, n_s +0.77 sigma, tau +0.47 sigma
                  chi^2/dof = 1.1881  (Run B rescues, within +-5 sigma window)

Two implementation flaws drove the FAIL token:

  Flaw A (peak finder):
    The runner used scipy.signal.find_peaks with prominence=0 on a
    Gaussian-smoothed (sigma_ell = 5) Planck per-multipole spectrum
    over ell in (50, 2700). The Planck PR3 COM_PowerSpect_CMB-TT-full
    file is per-multipole Plik bandpower estimates with substantial
    per-multipole noise above ell ~ 600. With prominence = 0 and only
    sigma_ell = 5 smoothing, the third "peak" caught a noise feature
    at ell = 661 rather than the true third acoustic peak near
    ell = 814-819.

  Flaw B (verdict-mapping logic):
    The precommit's BOUNDARY (iii) reads:
       "Run A FAILS but Run B (diagnostic optimization of A_s, n_s, tau
        with SAM densities frozen) rescues the shape using A_s, n_s, tau
        values all within +/- 5 sigma of the Planck 2018 posterior centroids."
    The runner v2 verdict-mapping elif chain only routed to BOUNDARY (iii)
    when P2 (chi^2/dof) was in the FAIL band (> 3.0). It did not handle
    the case "Run A overall not-PASS because P1 fails but P2 passes"
    even though Run B's perturbation movement was well within +-5 sigma
    (+1.32 / +0.77 / +0.47).

CR035A v2 strict FAIL is sealed at 2026-06-27 and is NOT overwritten.
CR035A2 is the appeal: same SAM density spine, same Planck data, same
Run A + Run B logic, same chi^2 calculation, same dof, same tolerances;
ONLY the peak-finder spec and the verdict-mapping tree are corrected.
```

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

BOUNDARY (iii) — Run B rescue (Run A overall not-PASS):
  Run A is not PASS for any reason
    (i.e. P1 fails OR P2 is BOUNDARY OR P2 is FAIL),
  AND Run B optimum satisfies ALL of:
    chi^2_TT/dof at Run B optimum <= 3.0
    chi^2_TE/dof at Run B optimum <= 5.0   (polarization sanity guard)
    chi^2_EE/dof at Run B optimum <= 5.0   (polarization sanity guard)
    |sigma-deviation| <= 5 sigma for ALL of A_s, n_s, tau
       relative to Planck 2018 posterior centroids.
  The polarization-sanity guard (TE/EE <= 5.0 at Run B optimum)
  prevents BOUNDARY (iii) from rescuing TT while destroying the
  TE/EE shape; if the optimum buys TT chi^2 at the cost of large
  polarization residuals, the rescue is rejected.

FAIL:
  None of the above; i.e. Run A is not PASS and Run B does NOT
  rescue within the BOUNDARY (iii) conditions. Specifically includes
  the case where Run B TT improves but TE or EE chi^2/dof > 5.0
  at the Run B optimum (polarization-sanity guard trips).
```

## What Changes From CR035A (explicit, line-by-line)

```text
Change 1: peak-finder windows + minimum prominence

CR035A spec:
  peak finder = local maximum of D_l, ell in (50, 2700),
  Gaussian smoothing sigma_ell = 5, prominence = 0.

CR035A2 spec:
  peak finder = local maximum of D_l within explicit per-peak ell windows
  with minimum prominence requirement, on the SAME Gaussian-smoothed
  D_l (sigma_ell = 5 unchanged).
    Peak 1 window:  ell in [150, 300]
    Peak 2 window:  ell in [400, 650]
    Peak 3 window:  ell in [700, 900]
    Minimum prominence:  >= 50 muK^2 (applies to Planck data;
                                       theory peaks are noise-free and
                                       use the same windows + prominence
                                       for symmetry).
  Peak height rule (load-bearing):
    H_i is evaluated from the same sigma_ell = 5 Gaussian-smoothed
    D_l curve used for peak detection, at the detected ell_peak_i.
    Do NOT measure H_i from the unsmoothed per-multipole table; that
    would reintroduce per-ell noise into the height-ratio gate.
  If no peak meeting the prominence requirement is found within a window,
  that peak is recorded as "not detected" and the corresponding sub-gate
  records FAIL.

Change 2: verdict-mapping tree fully implemented per the precommit text

CR035A runner v2 elif chain only routed to BOUNDARY (iii) when P2 was FAIL.
CR035A2 runner walks the tree exactly as written in the Verdict Ladder
above. Trace:
  IF P1 = PASS and P2 = PASS:
    IF polarization degraded:
      verdict = BOUNDARY (ii)
    ELSE:
      verdict = PASS
  ELIF P1 = PASS and P2 = BOUNDARY:
    verdict = BOUNDARY (i)
  ELSE:                                          # Run A overall not-PASS
    IF Run B chi^2_TT/dof <= 3.0
       AND Run B chi^2_TE/dof <= 5.0           # polarization sanity guard
       AND Run B chi^2_EE/dof <= 5.0           # polarization sanity guard
       AND |sigma_dev_As| <= 5
       AND |sigma_dev_ns| <= 5
       AND |sigma_dev_tau| <= 5:
      verdict = BOUNDARY (iii)
    ELSE:
      verdict = FAIL

Nothing else changes:
  - SAM density spine (A_0, chi, Omega_m, Omega_b, Omega_c, H_0): unchanged
  - External fixed perturbations (A_s = 2.100e-9, n_s = 0.9649,
    tau = 0.0544, N_eff, T_CMB, k_pivot): unchanged
  - Engine (CAMB 1.6.6, lens_potential_accuracy=1, lmax=2700): unchanged
  - Planck data files: unchanged
  - chi^2 calculation (symmetric sigma per bin, ell in [30, 2500]): unchanged
  - dof = n bins included: unchanged
  - Run B bounds and optimizer (L-BFGS-B over (A_s, n_s, tau) with
    Planck posterior sigmas 0.030e-9, 0.0042, 0.0073): unchanged
  - P1 sub-gate tolerances (Delta_ell <= 5 / 10 / 10, H ratio <= 15%): unchanged
  - P2 bands (PASS <= 2.0, BOUNDARY <= 3.0, FAIL > 3.0): unchanged
  - TE/EE reported, polarization-debt BOUNDARY trigger threshold 3.0: unchanged
```

## SAM Density Spine (unchanged from CR035A)

```text
A_0      = 1/(12*pi)               = 0.026525823848649224
chi      = (S/D)*A_0 = 2/(9*pi)    = 0.070735530263064592
Omega_m  = R*A_0 = 1/pi            = 0.318309886183790672
Omega_b  = 2*A_0*(1-chi)           = 0.049299011266100756
Omega_c  = Omega_m - Omega_b       = 0.269010874917689916
H_0      = 68.76 km/s/Mpc          (CMB-side anchor, value cited, file not read)
h        = 0.6876
ombh2    = 0.023308264901
omch2    = 0.127186663033
```

## External Perturbation Inputs (Run A fixed; unchanged from CR035A)

```text
A_s     = 2.100e-9
n_s     = 0.9649
tau     = 0.0544
N_eff   = 3.046
T_CMB   = 2.7255 K
k_pivot = 0.05 Mpc^-1
```

## Run A (verdict path; unchanged from CR035A)

```text
1. Compute SAM densities from substrate atoms.
2. CAMB with SAM cosmology + fixed external perturbations.
3. Lensed TT/TE/EE D_l up to lmax = 2700.
4. Evaluate theory at the Planck PR3 per-multipole grid (integer ell).
5. For each spectrum X in {TT, TE, EE}:
     sigma_X(ell) = 0.5 * (|-dDl| + |+dDl|)  per bin
     residual_X(ell) = D_l^X,SAM(ell) - D_l^X,Planck(ell)
     restrict to ell in [30, 2500]
     chi^2_X = sum ( residual_X / sigma_X )^2
     dof_X = number of bins included
6. CR035A2 peak detection (NEW spec):
     For each of Peak 1 (window [150,300]), Peak 2 ([400,650]),
     Peak 3 ([700,900]):
       Gaussian-smooth D_l with sigma_ell = 5  -> D_l,smooth
       scipy.signal.find_peaks on D_l,smooth with prominence >= 50 muK^2
       SELECT the single highest-prominence peak inside the window
       (if multiple), or the single peak (if exactly one), or RECORD
       "not detected" (if none meets prominence inside window).
       Record:
         ell_peak_i = location of selected peak
         H_i        = D_l,smooth(ell_peak_i)
                       (heights MUST come from the same smoothed curve
                        used for detection; not from the unsmoothed table)
     Apply same window+prominence+smoothed-height treatment to BOTH SAM
     theory and Planck data, symmetrically.
```

## Run B (diagnostic; unchanged from CR035A)

```text
With SAM densities frozen, scipy.optimize.minimize (L-BFGS-B) over:
  A_s   in [1.7e-9, 2.5e-9]
  n_s   in [0.93, 1.00]
  tau   in [0.02, 0.10]
Objective: chi^2_TT over ell in [30, 2500].
Report:
  A_s_opt, n_s_opt, tau_opt
  sigma-deviations vs Planck centroids (sigma_As = 0.030e-9,
    sigma_ns = 0.0042, sigma_tau = 0.0073)
  chi^2_TT/dof at optimum
  chi^2_TE/dof at optimum   (load-bearing: polarization sanity guard)
  chi^2_EE/dof at optimum   (load-bearing: polarization sanity guard)

Run B can establish BOUNDARY (iii); cannot promote to PASS.
BOUNDARY (iii) additionally requires Run B TE/EE chi^2/dof <= 5.0 at
the optimum (polarization sanity); if TE or EE exceeds 5.0 at the
Run B optimum, verdict = FAIL (TT rescue at cost of polarization is
not a valid rescue).
```

## P1 Sub-Gate Tolerances (unchanged from CR035A)

```text
P1a:  |ell_peak_1_SAM - ell_peak_1_Planck| <= 5
P1b:  |ell_peak_{2,3}_SAM - ell_peak_{2,3}_Planck| <= 10 each
P1c:  |H_{2,3}/H_1 deviation| <= 15% each
      where H_i is the peak height read from the sigma_ell = 5
      Gaussian-smoothed D_l curve at the detected ell_peak_i
      (the same smoothed curve used for peak detection),
      and the gate is |r_SAM - r_Planck| / |r_Planck| with
      r = H_2/H_1 or H_3/H_1.
P1 PASS iff >= 2 of (P1a, P1b, P1c) hold.
A "not detected" peak in either SAM or Planck side counts as sub-gate FAIL
for that peak.
```

## P2 (unchanged)

```text
chi^2_TT / dof_TT over ell in [30, 2500] with symmetric Planck per-bin sigma.
PASS     <= 2.0
BOUNDARY  (2.0, 3.0]
FAIL     > 3.0
```

## TE / EE (unchanged)

```text
Reported chi^2_TE / dof_TE and chi^2_EE / dof_EE over ell in [30, 2500].
Polarization-debt BOUNDARY trigger:  TE > 3.0 OR EE > 3.0.
```

## Strict Input Discipline (expanded vs CR035A)

```text
Allowed external sources (same as CR035A):
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-TT-full_R3.01.txt
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-TE-full_R3.01.txt
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-EE-full_R3.01.txt

Allowed engine:
  CAMB 1.6.6 (Python module camb)
  scipy.optimize.minimize (L-BFGS-B for Run B only)
  scipy.signal.find_peaks, scipy.ndimage.gaussian_filter1d
  numpy

Allowed substrate sources (in-code; no file read):
  R, D, S, alpha_H, A_0, chi, Omega_m, Omega_b, Omega_c, H_0

Forbidden inputs (EXPANDED — adds CR035A's family):
  CR001 / CR001b / CR001c / CR002 / CR003 family files
  CR018b / CR019 family files
  CR025 / CR031b / CR032 / CR033 family files
  CR205 files
  CR035A_summary.json
  CR035A_result.md
  CR035A_TT_residuals.csv, CR035A_TE_residuals.csv, CR035A_EE_residuals.csv
  CR035A_peaks.csv
  CR035A_runB_diagnostic.json
  CR035A_runA_theory_spectra.csv
  CR035A_runner.py (v2) and CR035A_runner_v1_aborted_json_bug.py
  any prior CR result/summary/evidence file

The runner installs a forbidden-file open() guard at module load that
aborts execution if any of these files is opened.
```

## Implementation Discipline

```text
The CR035A2 runner shall:

1. Install forbidden-file open() guard at module load (Python builtins.open
   wrapper), expanded to include all CR035A family files in the same folder.
2. Compute SAM density spine in-code; no file read.
3. Set fixed external perturbations as numeric literals; no prior CR read.
4. Parse Planck PR3 spectra with same column convention as CR035A.
5. Run CAMB Run A with SAM cosmology + fixed Planck-centroid perturbations.
6. Apply Gaussian smoothing (sigma_ell = 5) to D_l.
7. NEW: For each peak window [150,300], [400,650], [700,900], find peaks
   with prominence >= 50 muK^2 on the sigma_ell = 5 Gaussian-smoothed
   D_l curve using scipy.signal.find_peaks.
   Select the highest-prominence peak inside each window.
   Record ell_peak_i = location and H_i = D_l,smooth(ell_peak_i),
   reading H_i from the SAME smoothed curve used for detection.
   Apply identical treatment to SAM theory and Planck data.
8. Compute P1a/P1b/P1c gates.
9. Compute chi^2_TT, chi^2_TE, chi^2_EE on ell in [30, 2500].
10. Compute P2 band.
11. Run B optimization (L-BFGS-B, same bounds as CR035A).
12. NEW: Apply the verdict-mapping tree as written in Verdict Ladder
    section, with all branches explicit.
13. Emit:
    CR035A2_summary.json
    CR035A2_result.md
    CR035A2_TT_residuals.csv
    CR035A2_TE_residuals.csv
    CR035A2_EE_residuals.csv
    CR035A2_peaks.csv
    CR035A2_runB_diagnostic.json
    CR035A2_runA_theory_spectra.csv

Precision:
  pi = math.pi
  CAMB defaults (lens_potential_accuracy=1, lmax=2700)
  Reported chi^2 / sigma stats to >= 6 significant digits

No fitting in Run A:
  free_parameters_introduced_in_RunA = 0
  empirical_X_inf_input              = false
  prior_CR_result_inputs             = false
```

## Frozen Sources

```text
External data (same as CR035A; same hashes asserted by HASHES.txt at seal):
  COM_PowerSpect_CMB-TT-full_R3.01.txt
    SHA-256 ccf3113604020536f6f13ccf51680a7316ad0f32da558eee7f625e613bdd5522
  COM_PowerSpect_CMB-TE-full_R3.01.txt
    SHA-256 8b2c97d8865ebfdfb2b23c3e6883a39820734b804ba6e353533657b3a2f71425
  COM_PowerSpect_CMB-EE-full_R3.01.txt
    SHA-256 c865c56fe215e17e45eeed1069ddcd7d13365735f439fd63cc9c9325db97d67f

Engine: CAMB 1.6.6 (no swap after seal).

Forbidden branch-local sources: see Strict Input Discipline section above.
```

## Chronology and Honest Framing

```text
CR035A v2 sealed FAIL on 2026-06-27. The strict FAIL token stands and
is preserved in CR035A's folder; nothing in CR035A is overwritten.

CR035A2 is an appeal CR that:
  - Acknowledges CR035A's discipline (CLEAN execution, forbidden-file
    guard held, precommit hash recorded);
  - Identifies two implementation flaws (peak-finder noise feature and
    verdict-mapping (iii) gap) that drove the FAIL token away from
    the substantive science;
  - Corrects ONLY those two flaws, with the rest of the test (SAM
    densities, perturbation fixes, engine, Planck data, chi^2, dof,
    tolerances, Run B logic) held exactly as sealed in CR035A.

Do not write:
  CR035A was wrong about SAM.
  CR035A2 "rescues" SAM.

Do write:
  CR035A v2 sealed verdict FAIL is a strict-runner artifact driven by
  peak-finder misidentification of the Planck third acoustic peak
  (ell = 661 noise feature vs true peak near ell = 814-819) and a
  verdict-mapping gap relative to the precommit's BOUNDARY (iii) spirit.
  CR035A2 re-runs the same SAM density spine and the same fixed Planck
  perturbation parameters through CAMB 1.6.6 with a peak finder that
  uses per-peak ell windows and minimum prominence, and a verdict tree
  that walks the precommit BOUNDARY (iii) branch explicitly.
```

## Rule-9 Line

```text
This test could have falsified the claim that the SAM density spine
Omega_m = 1/pi, Omega_b = 2*A_0*(1-chi), Omega_c = Omega_m - Omega_b,
H_0 = 68.76, when paired with fixed Planck 2018 posterior-centroid
perturbations (A_s = 2.100e-9, n_s = 0.9649, tau = 0.0544) and CAMB
1.6.6, reproduces the Planck 2018 PR3 full per-multipole bandpower table on
ell in [30, 2500] at peak-structure (P1) and full-shape (P2) tolerances,
when peak detection uses per-peak ell windows + minimum prominence
>= 50 muK^2 and the verdict tree walks the precommit Verdict Ladder
explicitly.

It fails if:
  Run A is not PASS for any reason (P1 fails, P2 fails, or polarization
  debt), AND Run B at optimum either:
    chi^2_TT/dof > 3.0, OR
    chi^2_TE/dof > 5.0 (polarization sanity guard), OR
    chi^2_EE/dof > 5.0 (polarization sanity guard), OR
    requires ANY of A_s, n_s, tau more than 5 sigma from the Planck
    2018 posterior centroid.

It is BOUNDARY if any of the three named BOUNDARY conditions hold
(full-shape marginal, polarization debt, or Run B rescue within +-5 sigma).
```

## Result Text Requirements

```text
If PASS:
  CR035A2 PASS confirms that the SAM density spine
  (Omega_m = 1/pi, Omega_b = 2*A_0*(1-chi), Omega_c = Omega_m - Omega_b,
   H_0 = 68.76), paired with Planck 2018 posterior-centroid perturbation
  parameters and CAMB 1.6.6, reproduces the Planck 2018 PR3 full
  per-multipole bandpower table on ell in [30, 2500] within the CR035A2
  peak-window / prominence-corrected P1 tolerances and the unchanged
  P2 full-shape gate.

If BOUNDARY (any case):
  State which BOUNDARY case triggered (i), (ii), or (iii) with the
  diagnostic numbers.

If FAIL:
  CR035A2 FAIL rejects the SAM density spine at the full per-multipole
  shape level under the corrected peak finder and verdict tree.

In all cases:
  execution_status                   = CLEAN or not CLEAN with reason
  free_parameters_introduced_RunA    = 0
  external_perturbation_disclosed    = true
  prior_CR_result_inputs             = false
  forbidden_files_opened             = false
  CR035A_files_opened                = false   (additional discipline)
  peak_finder_spec                   = "windows + prominence>=50 muK^2"
```

## Manuscript Headline If PASS (conditional)

```text
The SAM density spine (Omega_m = 1/pi, Omega_b = 2*A_0*(1-chi)),
paired with the standard Planck 2018 posterior-centroid perturbation
parameters (A_s = 2.100e-9, n_s = 0.9649, tau = 0.0544) and the
standard Boltzmann engine CAMB 1.6.6, reproduces the Planck 2018
full per-multipole bandpower table at full-shape precision (TT chi^2/dof
<= 2.0) and at the first three acoustic-peak locations and height
ratios within the predeclared CR035A2 tolerances, when peak detection
uses per-peak ell windows + minimum prominence to suppress per-multipole
noise features in the Planck PR3 full per-multipole bandpower table.

Do not claim:
  Full parameter-free CMB shape closure.
  Zero-parameter perturbation derivation.

Do write:
  SAM specifies the cosmological density spine (omega_b, omega_c) from
  substrate atoms with zero free parameters in the density sector. The
  perturbation sector (A_s, n_s, tau) is fixed at externally measured
  Planck 2018 values. Joint substrate + Planck-perturbation closure on
  the full per-multipole bandpower table is documented in CR035A2; full Planck
  likelihood treatment is deferred to CR035B.
```

## Stewardship Reference

```text
SHA-256: d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

---

## Reasoning Document (what this appeal does and does not change)

```text
Why an appeal CR rather than overwriting CR035A:
  - Hostile-environment discipline: sealed tests are never deleted.
  - CR035A's strict FAIL is a recorded outcome and stays in the audit
    trail. The appeal stands beside it, not on top of it.
  - The science substance (TT chi^2/dof = 1.35, TE = 1.19, EE = 1.12;
    Run B within +-1.5 sigma) is documented in CR035A's result.md and
    is not in dispute. The appeal addresses the verdict TOKEN, not the
    underlying numerics.

What the appeal corrects:
  - Peak finder: per-peak ell windows + minimum prominence >= 50 muK^2.
    Justification: the Planck PR3 COM_PowerSpect_CMB-TT-full file is
    a per-multipole bandpower estimate with substantial per-ell noise
    above ell ~ 600. With sigma_ell = 5 Gaussian smoothing and no
    prominence requirement, the peak finder mistook a noise feature
    at ell = 661 for the third acoustic peak. Sean independently
    verified that the same smoothing with even a modest prominence
    requirement gives peaks (219, 520, 814), matching SAM theory
    (219, 533, 806) much more closely.
  - Verdict-mapping tree: written out fully and walked explicitly,
    matching the precommit's BOUNDARY (iii) text. The CR035A v2
    runner's elif chain skipped the case "P1 fails but P2 passes and
    Run B rescues," routing it to FAIL instead of BOUNDARY (iii).

What the appeal does NOT change:
  - SAM density spine (every constant).
  - External perturbation values (Planck 2018 posterior centroids).
  - Engine (CAMB 1.6.6, lens_potential_accuracy = 1, lmax = 2700).
  - Planck PR3 file paths and column convention.
  - chi^2 / dof / symmetric per-bin sigma.
  - P1 sub-gate tolerances (Delta_ell <= 5/10/10, H ratio <= 15%).
  - P2 bands (PASS <= 2.0, BOUNDARY (2.0, 3.0], FAIL > 3.0).
  - TE/EE reporting and polarization-debt threshold (3.0).
  - Run B bounds and optimizer (L-BFGS-B over (A_s, n_s, tau)).
  - Planck posterior sigmas for the +-5 sigma window
    (sigma_As = 0.030e-9, sigma_ns = 0.0042, sigma_tau = 0.0073).

What this appeal cannot do:
  - Promote CR035A's FAIL to PASS retroactively. CR035A's seal stands.
  - Substitute for an official Plik-lite binned bandpower ingest (would
    be a separate follow-up: CR035C if needed).
  - Substitute for the official Planck likelihood test (CR035B).

What an honest CR035A2 PASS would mean:
  - The SAM density spine, paired with Planck-centroid perturbations
    and a peak finder that suppresses per-multipole noise features in
    the Planck PR3 full per-multipole bandpower table, reproduces the
    Planck TT shape within the predeclared tolerances.
  - It does not mean SAM derives the CMB. It does not mean SAM is
    parameter-free at the CMB level. The perturbation sector remains
    an externally anchored input. Full likelihood treatment is deferred.
```
