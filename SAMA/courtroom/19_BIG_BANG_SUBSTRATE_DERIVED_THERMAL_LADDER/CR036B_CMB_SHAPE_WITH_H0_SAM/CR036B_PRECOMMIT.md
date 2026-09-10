# CR036B_CMB_SHAPE_WITH_H0_SAM Precommit

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
    (P1 fails OR P2 is BOUNDARY OR P2 is FAIL),
  AND Run B optimum satisfies ALL of:
    chi^2_TT/dof at Run B optimum <= 3.0
    chi^2_TE/dof at Run B optimum <= 5.0   (polarization sanity guard)
    chi^2_EE/dof at Run B optimum <= 5.0   (polarization sanity guard)
    |sigma-deviation| <= 5 sigma for ALL of A_s, n_s, tau

FAIL:
  None of the above.
```

P1 and P2 are load-bearing. TE/EE under Run A are reported with explicit
BOUNDARY trigger. Run B is diagnostic only. All gates are inherited
verbatim from CR035A2's sealed verdict ladder.

## Test Type

```text
Fresh Courtroom branch test in:
  19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER

External anchors (numeric constants; NOT read from files):
  Planck 2018 PR3 TT/TE/EE full per-multipole bandpower tables
  Planck 2018 base posterior centroids: A_s = 2.100e-9, n_s = 0.9649,
    tau = 0.0544

Substrate input + H_0:
  Same SAM density spine as CR035A2 (Omega_m = 1/pi, Omega_b = 2*A_0*(1-chi),
    Omega_c = Omega_m - Omega_b).
  NEW: H_0 = H_0_SAM = 67.2503751950 km/s/Mpc (sealed from CR036, cited as
    numeric constant in this precommit; CR036 file NOT read by the runner).

Engine:
  CAMB 1.6.6 (same as CR035A2; no swap).

Prior-CR exclusion (extended vs CR035A2):
  Forbidden: CR001 / CR001b / CR001c / CR002 / CR003 / CR018b / CR019 /
  CR025 / CR031b / CR032 / CR033 / CR035A / CR035A2 / CR036 / CR205
  family files. The CR036_summary.json file is NOT read; H_0_SAM is
  cited as a numeric constant in this precommit text.
```

## Why This Test Matters

```text
CR035A2 sealed PASS with the SAM density spine paired with H_0 = 68.76
set externally. CR036 sealed PASS deriving H_0_SAM = 67.2503751950 from
substrate atoms + FIRAS thermal anchor + CODATA 2018 / SI fixed
constants, with zero free parameters and zero CMB-spectrum input.

CR036B closes the cascade: SAM density spine + SAM-derived H_0 + fixed
Planck-centroid perturbation parameters, run through the same CAMB
pipeline and the same Planck shape gates as CR035A2. If CR036B PASSes,
the chain
  substrate atoms -> Omega_m, Omega_b, Omega_c, H_0 -> omega_b, omega_c
                  -> C_ell
holds at the Planck full-shape level with NO externally-set background
density anchor. The perturbation sector (A_s, n_s, tau) remains
externally anchored at Planck 2018 centroids; that's the next
open frontier, not CR036B's question.
```

## Question

```text
With the SAM density spine

  Omega_m = R*A_0 = 1/pi
  Omega_b = 2*A_0*(1-chi)
  Omega_c = Omega_m - Omega_b

and the SAM-derived

  H_0 = H_0_SAM = 67.2503751950 km/s/Mpc                  (sealed in CR036)

and the fixed Planck-centroid perturbation parameters

  A_s = 2.100e-9, n_s = 0.9649, tau = 0.0544
  N_eff = 3.046, T_CMB = 2.7255 K, k_pivot = 0.05 Mpc^-1

does CAMB 1.6.6 reproduce the Planck 2018 PR3 full per-multipole TT
bandpower table on ell in [30, 2500] within the CR035A2 P1 peak
structure + P2 full-shape tolerances?
```

## What Changes From CR035A2

```text
Exactly one input changes:

  CR035A2:  H_0 = 68.76          (externally set, BAO/CMB-side anchor)
  CR036B:   H_0 = 67.2503751950    (sealed from CR036, substrate-derived
                                  via FIRAS thermal anchor + CODATA)

Everything else is identical to CR035A2:
  - SAM density spine (Omega_m, Omega_b, Omega_c) from substrate atoms
  - Fixed perturbations (A_s, n_s, tau, N_eff, T_CMB, k_pivot)
  - Engine: CAMB 1.6.6 with lens_potential_accuracy=1, lmax=2700
  - Planck PR3 files: COM_PowerSpect_CMB-TT/TE/EE-full_R3.01.txt
  - chi^2 over ell in [30, 2500], symmetric per-multipole sigma
  - Peak finder: windows [150,300], [400,650], [700,900]
    with prominence >= 50 muK^2 on sigma_ell = 5 smoothed D_l
  - Heights H_i from the same sigma_ell = 5 smoothed curve
  - P1 sub-gates (Delta_ell <= 5/10/10, H ratio <= 15%; >= 2 of 3)
  - P2 bands (PASS <= 2.0, BOUNDARY (2.0, 3.0], FAIL > 3.0)
  - TE/EE reporting + polarization-debt threshold 3.0 (Run A)
  - Run B bounds and L-BFGS-B optimizer
  - Run B polarization sanity guard (TE/EE <= 5.0 at optimum)
  - Verdict tree (PASS / BOUNDARY (i)(ii)(iii) / FAIL)
```

## SAM Density Spine (substrate-derived; unchanged from CR035A2)

```text
A_0      = 1/(12*pi)               = 0.026525823848649224
chi      = (S/D)*A_0 = 2/(9*pi)    = 0.070735530263064592
Omega_m  = R*A_0 = 1/pi            = 0.318309886183790672
Omega_b  = 2*A_0*(1-chi)           = 0.049299011266100756
Omega_c  = Omega_m - Omega_b       = 0.269010874917689916
```

## H_0 (NEW vs CR035A2)

```text
H_0  = H_0_SAM = 67.2503751950 km/s/Mpc
h    = 0.6725037526
ombh2 = Omega_b * h^2 = 0.049299011266 * 0.4522612983 = 0.022296...
omch2 = Omega_c * h^2 = 0.269010874918 * 0.4522612983 = 0.121658...

H_0_SAM provenance:
  Sealed in CR036 (precommit SHA-256
    345a1a8dc180eb6b28141114a82315e3b8d92889537c1219eec4312d59ca33f2)
  Derivation chain:
    eta_SAM = (M/(alpha_H^2*Theta)) * A_0^(L/V) = 7/(4*(12*pi)^6)
    K_eta_to_omega_b derived in-runner from CODATA 2018 + FIRAS T_CMB
    omega_b_SAM = eta_SAM / K_eta_to_omega_b
    h_SAM = sqrt(omega_b_SAM / Omega_b_SAM)
    H_0_SAM = 100 * h_SAM

The CR036 file is NOT opened at runtime; H_0_SAM is cited as a numeric
constant in this precommit.
```

## Fixed External Perturbations (unchanged from CR035A2)

```text
A_s     = 2.100e-9      (Planck 2018 base posterior centroid)
n_s     = 0.9649        (Planck 2018 base posterior centroid)
tau     = 0.0544        (Planck 2018 base posterior centroid)
N_eff   = 3.046         (standard)
T_CMB   = 2.7255 K      (FIRAS)
k_pivot = 0.05 Mpc^-1   (Planck pivot scale)
```

## Strict Input Discipline

```text
Allowed external sources:
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-TT-full_R3.01.txt
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-TE-full_R3.01.txt
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-EE-full_R3.01.txt

Allowed engine:
  CAMB 1.6.6 (Python module camb)
  scipy.optimize.minimize  (L-BFGS-B for Run B only)
  scipy.signal.find_peaks, scipy.ndimage.gaussian_filter1d
  numpy

Allowed substrate sources (in-code; no file read):
  R = 12, D = 3, S = 8, alpha_H = 2
  A_0 = 1/(12*pi), chi = 2/(9*pi)
  Omega_m = 1/pi

H_0_SAM (in-code numeric literal; cited from CR036; CR036 file NOT read):
  H_0 = 67.2503751950 km/s/Mpc
```

## Forbidden Inputs

```text
The CR036B runner must not read, import, parse, compare against, or use:

  CR036_summary.json, CR036_result.md, CR036_evidence_rows.csv,
    CR036_substrate_atoms.csv, CR036_runner.py
  CR035A2 family files (summary, result, residuals, peaks, runB diag,
    theory spectra, runner)
  CR035A family files (same)
  CR001 / CR001b / CR001c / CR002 / CR003 family files
  CR018b / CR019 family files
  CR025 / CR031b / CR032 / CR033 family files
  CR205 files
  Planck likelihood files (clik, plik, lite)
  Planck base parameter best-fit chain files
  BAO best-fit H_0 / chain files
  SN best-fit H_0 / chain files
  Any prior CR result.md / summary.json / evidence_rows.csv

The forbidden-file open() guard installed at module load aborts execution
if any path matching these patterns is opened.
```

## Run A — Verdict Path (fixed Planck perturbations + H_0_SAM)

```text
1. SAM densities computed in-runner from substrate atoms.
2. H_0 = 67.2503751950 km/s/Mpc set as a numeric literal.
3. CAMB with SAM cosmology + fixed external perturbations + H_0_SAM.
4. Compute lensed TT/TE/EE D_l up to lmax = 2700.
5. Evaluate theory at Planck PR3 per-multipole grid (integer ell).
6. For each spectrum X in {TT, TE, EE}:
     sigma_X(ell) = 0.5 * (|-dDl| + |+dDl|)
     residual_X(ell) = D_l^X,SAM(ell) - D_l^X,Planck(ell)
     restrict ell in [30, 2500]
     chi^2_X = sum (residual_X / sigma_X)^2
     dof_X = number of bins included
7. Peak detection (same as CR035A2):
     Gaussian smooth D_l with sigma_ell = 5 -> D_l,smooth
     For each window [150,300], [400,650], [700,900]:
       scipy.signal.find_peaks with prominence >= 50 muK^2
       Select single highest-prominence peak in window
       Record ell_peak_i and H_i = D_l,smooth(ell_peak_i)
     Apply symmetrically to SAM theory and Planck data.
```

## Run B — Diagnostic Optimization (same as CR035A2)

```text
With SAM densities + H_0_SAM held fixed, scipy.optimize.minimize
(L-BFGS-B) over:
  A_s   in [1.7e-9, 2.5e-9]
  n_s   in [0.93, 1.00]
  tau   in [0.02, 0.10]
Objective: chi^2_TT over ell in [30, 2500].
Report A_s_opt, n_s_opt, tau_opt; sigma-deviations vs Planck posterior
centroids (sigma_As = 0.030e-9, sigma_ns = 0.0042, sigma_tau = 0.0073);
chi^2_TT/dof, chi^2_TE/dof, chi^2_EE/dof at optimum.

Run B can establish BOUNDARY (iii). BOUNDARY (iii) additionally requires
TE/EE chi^2/dof <= 5.0 at the optimum.
```

## P1, P2, TE/EE, Verdict Tree (unchanged from CR035A2)

```text
P1a:  |ell_peak_1_SAM - ell_peak_1_Planck| <= 5
P1b:  |ell_peak_{2,3}_SAM - ell_peak_{2,3}_Planck| <= 10 each
P1c:  |H_{2,3}/H_1 deviation| <= 15% each
       (using sigma_ell = 5 smoothed heights as defined in CR035A2)
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
    IF Run B chi^2_TT/dof <= 3.0
       AND Run B chi^2_TE/dof <= 5.0
       AND Run B chi^2_EE/dof <= 5.0
       AND |sigma_dev_As|  <= 5
       AND |sigma_dev_ns|  <= 5
       AND |sigma_dev_tau| <= 5:
      verdict = BOUNDARY (iii)
    ELSE:
      verdict = FAIL
```

## Implementation Discipline

```text
The CR036B runner shall:

1. Install forbidden-file open() guard at module load (expanded to include
   CR036 family + CR035A2 family + all prior CRs above).
2. Compute SAM density spine in-code from substrate atoms; no file read.
3. Set H_0 = 67.2503751950 as a numeric literal (cited from CR036 by
   value; CR036 file NOT opened).
4. Set fixed perturbations as numeric literals.
5. Parse Planck PR3 spectra files (same column convention).
6. Run CAMB Run A with SAM cosmology + H_0_SAM + fixed perturbations.
7. Apply Gaussian smoothing sigma_ell = 5; find peaks in windows with
   prominence >= 50 muK^2; record heights from smoothed curve.
8. Compute P1, P2, polarization-debt, verdict tree.
9. Run B optimization.
10. Apply Run B polarization sanity guard if BOUNDARY (iii) considered.
11. Emit:
    CR036B_summary.json
    CR036B_result.md
    CR036B_TT_residuals.csv
    CR036B_TE_residuals.csv
    CR036B_EE_residuals.csv
    CR036B_peaks.csv
    CR036B_runB_diagnostic.json
    CR036B_runA_theory_spectra.csv

Precision:
  pi = math.pi
  CAMB defaults (lens_potential_accuracy = 1)
  Reported chi^2 / sigma stats to >= 6 significant digits

No fitting in Run A:
  free_parameters_introduced_in_RunA = 0
  external_inputs (H_0_SAM + Planck perturbations) = disclosed
  prior_CR_result_inputs = false
  CR036_files_opened = false
  CR035A2_files_opened = false
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

Full filesystem paths (read-only):
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-TT-full_R3.01.txt
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-TE-full_R3.01.txt
  C:\VS\Stam_model-A-v1.0\data\external_data\planck_pr3\COM_PowerSpect_CMB-EE-full_R3.01.txt
```

### Frozen external numeric constants (in-code literals; NO file read)

```text
A_s     = 2.100e-9         (Planck 2018 base posterior centroid)
n_s     = 0.9649           (Planck 2018 base posterior centroid)
tau     = 0.0544           (Planck 2018 base posterior centroid)
N_eff   = 3.046            (standard)
T_CMB   = 2.7255 K         (FIRAS)
k_pivot = 0.05 Mpc^-1      (Planck pivot scale)
```

### CR036 provenance hash chain (provenance only; NOT read at runtime)

```text
CR036 sealed 2026-06-27 in:
  19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/

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

The CR036B runner does NOT read any of the CR036 files. The H_0_SAM
value above is frozen as a numeric literal in this CR036B precommit;
the runner uses that literal directly. The CR036 hashes are recorded
here purely as provenance for audit-trail verification.
```

### Allowed engine

```text
CAMB 1.6.6 (python module camb)
scipy.optimize.minimize  (L-BFGS-B for Run B only)
scipy.signal.find_peaks, scipy.ndimage.gaussian_filter1d
numpy
```

### Allowed substrate sources (in-code only; no file read)

```text
R = 12, D = 3, S = 8, alpha_H = 2
A_0 = 1/(12*pi)
chi = (S/D)*A_0 = 2/(9*pi)
Omega_m = R*A_0 = 1/pi
Omega_b = 2*A_0*(1-chi)
Omega_c = Omega_m - Omega_b
H_0    = 67.2503751950 km/s/Mpc
         (in-code numeric literal cited from CR036 by value;
          CR036 file NOT opened at runtime)
```

### Forbidden branch-local sources

```text
CR036 family files (PRECOMMIT, runner, summary, result, evidence,
  substrate_atoms)
CR035A2 family files
CR035A family files
All other CR family files (CR001-CR003, CR018b, CR019, CR025, CR031b,
  CR032, CR033, CR205)
Any prior CR result.md / summary.json / evidence_rows.csv

The forbidden-file open() guard installed at module load aborts execution
if any of these is opened.
```

## Chronology

```text
CR036B is the natural follow-on to CR036 sealed PASS (eta_SAM and
H_0_SAM derived from substrate atoms + FIRAS thermal anchor + CODATA
2018 / SI fixed constants). The H_0_SAM value 67.2503751950 is sealed
in CR036 (precommit SHA-256 345a1a8dc180eb6b28141114a82315e3b8d92889537c1219eec4312d59ca33f2)
and is cited as a numeric constant in this precommit; the CR036
file is NOT opened by the runner.

CR036B replaces CR035A2's externally-set H_0 = 68.76 with the
substrate-derived H_0_SAM = 67.2503751950, keeping all other CR035A2
spec items unchanged. The test asks whether the SAM density spine
PLUS the SAM-derived H_0 still passes the Planck PR3 full per-multipole
shape gates that CR035A2 passed at H_0 = 68.76.

Do not write:
  CR036B "proves" the SAM cosmology.

Do write:
  CR036B tests whether the SAM density spine + SAM-derived H_0 + fixed
  Planck-centroid perturbation parameters still reproduces the Planck
  PR3 full per-multipole TT shape at the same tolerances CR035A2 used.
  Perturbation-sector derivation remains open and is out of scope.
```

## Rule-9 Line

```text
This test could have falsified the claim that the SAM density spine
plus the SAM-derived H_0_SAM = 67.2503751950, paired with fixed Planck-
centroid perturbation parameters and CAMB 1.6.6, reproduces the Planck
2018 PR3 full per-multipole TT bandpower table at the CR035A2 peak
structure and full-shape tolerances.

It fails if Run A is not PASS for any reason and Run B does not rescue
within the CR035A2 BOUNDARY (iii) conditions (Run B TT/dof <= 3.0 AND
TE/dof <= 5.0 AND EE/dof <= 5.0 AND |sigma_dev| <= 5 sigma for all of
A_s, n_s, tau).
```

## Result Text Requirements

```text
If PASS:
  CR036B PASS confirms that the SAM density spine + H_0_SAM = 67.2503751950
  + Planck-centroid (A_s, n_s, tau), run through CAMB 1.6.6, reproduces
  the Planck 2018 PR3 full per-multipole TT bandpower table within the
  CR035A2 P1 peak structure + P2 full-shape tolerances.

If BOUNDARY: state which case (i)/(ii)/(iii) triggered with diagnostic values.

If FAIL: state which gate failed and by how much; report Run B values.

In all cases:
  execution_status                = CLEAN or not CLEAN with reason
  free_parameters_introduced_RunA = 0
  prior_CR_result_inputs          = false
  CR036_files_opened              = false
  CR035A2_files_opened            = false
  forbidden_files_opened          = false
```

## Manuscript Headline If PASS (conditional)

```text
SAM derives the cosmological density spine AND the CMB-side H_0 from
substrate atoms (chain: substrate -> eta_SAM -> H_0_SAM via FIRAS T_CMB
+ CODATA 2018 / SI fixed constants), and the resulting cosmology paired
with Planck-centroid perturbation parameters reproduces the Planck 2018
full per-multipole TT bandpower table at the CR035A2 peak-structure and
full-shape tolerances. CR036 supplies the H_0 derivation; CR036B confirms
the spectrum passes the Planck shape gates under that H_0. Perturbation-
sector derivation remains open.
```

## Connection to Future Work

```text
CR037 placeholder (open)
  Derive A_s, n_s, tau from substrate atoms, or document the structural gap.

CR038 placeholder (independent BBN/D/H validation; queued earlier)
  Compare eta_SAM to a frozen BBN D/H-based eta measurement
  independently of CMB.

CR036A_E5_FIX placeholder
  Correct the E5 z_eq_SAM unit bug in CR036 (rho_gamma needs /c^2 for
  mass-equivalent density). Does not affect CR036's P1, P2, or I1.
```

## Stewardship Reference

```text
STEWARDSHIP_DECLARATION.md SHA-256
  d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```
