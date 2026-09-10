# CR037C — Parameter-Free CMB Shape on ACT DR4 (External-Catalog Independence)

**Branch:** 19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER
**Classification:** EXTERNAL_CATALOG_INDEPENDENCE_CR (downstream of CR037B@19)
**Sealed by:** Sean Brady, 2026-06-29
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Test Type

```text
Fresh Courtroom branch test in 19. External catalog: ACT DR4 (Choi et
al. 2020), the cleaned-CMB foreground-marginalized bandpower likelihood
from the ACTPol survey 2013-2016. SAM cosmology is the SAME triplet
sealed in CR037B (densities + H_0 + perturbations, all from substrate
atoms via FIRAS T_CMB + CODATA 2018 / SI fixed constants). No new
fits. CAMB lmax is raised to 8000 to cover the ACT DR4 window-function
support up to lmax_win = 7925.

This is the external-catalog independence test placeholder named in
CR037B_PRECOMMIT.md (line: "CR037C placeholder — External-catalog
independence test for the CR037B PASS: re-run with a non-Planck
high-ell experiment if available"). The non-Planck high-ell experiment
is ACT DR4. Both deep (15mJy) and wide (100mJy) ACTPol patches are
included, jointly using TT, TE, EE bandpowers with the full 260x260
covariance via the published ACT bandpower window functions.

NO Run B optimizer. yp2 (polarization-efficiency calibration) is fixed
to 1.0 for the parameter-free test. The full-likelihood version with
yp2 marginalization is registered as CR037D placeholder.
```

## Question

```text
With the SAM-derived cosmology sealed in CR037B

  Omega_m = R*A_0 = 1/pi                          (substrate)
  Omega_b = 2*A_0*(1-chi)                          (substrate)
  Omega_c = Omega_m - Omega_b                      (substrate)
  H_0     = 67.2503751950 km/s/Mpc                 (CR036 sealed)
  A_s     = 2.1117473568e-9   = eta_SAM*sqrt(R)    (CR037A sealed)
  n_s     = 0.9646322349       = 1 - chi/2          (CR037A sealed)
  tau     = 0.0530516477       = 2 * A_0            (CR037A sealed)
  yp2     = 1.0                                    (no polarization fit)

does CAMB 1.6.6 reproduce the ACT DR4 cleaned-CMB bandpower table
(Choi et al. 2020; 260 bandpowers across deep + wide patches in TT, TE,
EE) within the ACTPol-only acceptable chi^2/dof tolerances, with NO
Run B optimizer?
```

## Why This Test Matters

```text
CR037B sealed PASS using Planck 2018 PR3 full per-multipole bandpowers:
the SAM cosmology reproduces Planck's TT shape at chi^2_TT/dof = 1.034
with zero free parameters.

CR037C closes the parameter-free CMB shape claim against an independent
instrument:
  - ACT is a ground-based survey; Planck is satellite. Different
    systematics, different calibration chain, different sky cuts.
  - ACT extends the lever arm to ell ~ 4000-7000 (Planck saturates
    at ell ~ 2500 in PR3).
  - The ACT DR4 cleaned-CMB bandpowers have already been marginalized
    over foreground emission (SZ + radio + dusty galaxies + tSZxCIB),
    so the only nuisance parameter the standard ACT likelihood
    samples is yp2 (polarization efficiency). For a strictly
    parameter-free test we fix yp2 = 1.0.

A PASS at this level means: the SAM cosmology is not a Planck artifact.
It reproduces the CMB shape AS MEASURED BY A NON-PLANCK INSTRUMENT,
including the high-ell extension where the ACT data dominate over
Planck. Zero free parameters.

A FAIL at this level would not invalidate CR037B (the Planck PASS is a
sealed standalone), but would localize the SAM-vs-Planck contact to
Planck-specific systematics or to the ell <= 2500 regime where Planck
dominates.
```

## SAM Cosmology (Numeric Literals — Prior CR Files NOT Opened)

```text
Substrate spine (computed in-runner from atoms):
  R = 12, D = 3, S = 8, alpha_H = 2
  A_0       = 1/(12*pi)
  chi       = (S/D) * A_0 = 2/(9*pi)
  Omega_m   = R*A_0 = 1/pi
  Omega_b   = 2 * A_0 * (1 - chi)
  Omega_c   = Omega_m - Omega_b

CR036 sealed H_0 (numeric literal; CR036 file NOT opened):
  H_0       = 67.2503751950 km/s/Mpc

CR037A sealed perturbation triplet (numeric literals; CR037A NOT opened):
  A_s       = 2.1117473568e-9   = eta_SAM * sqrt(R)
  n_s       = 0.9646322349       = 1 - chi/2
  tau       = 0.0530516477       = 2 * A_0

Fixed non-fit ancillary inputs (in-code literals):
  N_eff     = 3.046
  T_CMB     = 2.7255 K          (FIRAS)
  k_pivot   = 0.05 Mpc^-1
  m_nu(sum) = 0.06 eV           (Planck-baseline)

CAMB ancillary settings (frozen; full echo into summary):
  lmax                     = 8000   (raised from CR037B's 2700;
                                     covers ACT lmax_win = 7925)
  lens_potential_accuracy  = 4      (raised from CR037B's 1 for
                                     accuracy at high ell)
  WantTensors              = False
  WantScalars              = True
  r (tensor-to-scalar)     = 0.0
  NonLinear                = NonLinear_none
  omk                      = 0.0
  TCMB                     = 2.7255 K
  nnu                      = 3.046
  num_massive_neutrinos    = 1
  mnu (eV)                 = 0.06
  YHe handling             = CAMB BBN-consistency (default;
                             set via set_cosmology; YHe value echoed
                             in summary post-run)
  pivot_scalar             = 0.05 Mpc^-1
  CMB_unit                 = "muK"
  spectra requested        = ["lensed_scalar"]
```

## External Data Files (with sealed sha256)

```text
ACT DR4 likelihood data files
(downloaded 2026-06-29 from ACT Collaboration pyactlike repository
master branch; see https://github.com/ACTCollaboration/pyactlike)

C:\VS\Stam_model-A-v1.0\data\external_data\act_dr4\Binning.dat
  sha256 = fecc173092400f1b53505378a8b0af33f69c4ee2f11fbafdc6d0c1a5e6574738
  size   = 1962 bytes

C:\VS\Stam_model-A-v1.0\data\external_data\act_dr4\cl_cmb_ap.dat
  sha256 = 86a2a3d3cf5bd3b024681ad78fa67d614a9a56ede77ef41716623b45405d6f95
  size   = 16640 bytes
  format = ascii; 260 rows; columns (bin_center_ell, X_data [C_l muK^2], X_sig)
  layout = deep TT [0:40], deep TE [40:85], deep EE [85:130],
           wide TT [130:170], wide TE [170:215], wide EE [215:260]

C:\VS\Stam_model-A-v1.0\data\external_data\act_dr4\c_matrix_ap.dat
  sha256 = 3e550bca7f192749e221b9d6db0c323c1a85ca257c398880dea472be43867fea
  size   = 540808 bytes
  format = Fortran unformatted binary; (260, 260) doubles; symmetrized
           on load (lower-triangle into upper-triangle)

C:\VS\Stam_model-A-v1.0\data\external_data\act_dr4\coadd_bpwf_15mJy_191127_lmin2.npz
  sha256 = a4c58bbe02ccb8c132af4a47cf53ec07b261a39b709c598e8b95f6a0d0349225
  size   = 31765014 bytes  (deep patch bandpower window functions)
  format = numpy npz with key "bpwf"; (520, 7924) float64

C:\VS\Stam_model-A-v1.0\data\external_data\act_dr4\coadd_bpwf_100mJy_191127_lmin2.npz
  sha256 = 365de9b3f8b9598c433dbc4f49dc8b996393262d43a526e1a6e257cbb871a270
  size   = 31770622 bytes  (wide patch bandpower window functions)
  format = numpy npz with key "bpwf"; (520, 7924) float64

Window-function row layout (per pyactlike.like loglike):
  rows 2*52 : 3*52   = TT 150x150 cross
  rows 6*52 : 7*52   = TE 150x150 cross
  rows 9*52 : 10*52  = EE 150x150 cross
  (other rows are multi-frequency cross-spectra not used in the
   foreground-marginalized cleaned-CMB likelihood)

bmax = 52 bins per spectrum (with first 5 of TT skipped by b0=5)
nbintt = 40, nbinte = 45, nbinee = 45

Reference parser (provenance only; not imported at runtime):
  C:\VS\Stam_model-A-v1.0\data\external_data\act_dr4\pyactlike_like_reference.py
  sha256 = (computed at seal time and recorded in HASHES.txt)
```

## Theory-to-Bandpower Pipeline

```text
1. CAMB run with SAM cosmology + SAM perturbations + frozen settings;
   request lensed_scalar TT/TE/EE D_l at ell in [0, 8000].

2. Convert D_l to C_l per pyactlike convention:
     cl[ell] = D_ell * 2*pi / (ell * (ell + 1))   for ell >= 2
     cl[0] = cl[1] = 0

3. Truncate to ell in [2, lmax_win - 1] = [2, 7924] (with cl[0]=cl[1]=0).

4. Apply window functions (per pyactlike.like loglike):
     cl_tt_d = win_func_d[2*52 : 3*52, :] @ cl_tt[:7924]   (deep, 52 bins)
     cl_te_d = win_func_d[6*52 : 7*52, :] @ cl_te[:7924]
     cl_ee_d = win_func_d[9*52 : 10*52, :] @ cl_ee[:7924]
     cl_tt_w = win_func_w[2*52 : 3*52, :] @ cl_tt[:7924]   (wide, 52 bins)
     cl_te_w = win_func_w[6*52 : 7*52, :] @ cl_te[:7924]
     cl_ee_w = win_func_w[9*52 : 10*52, :] @ cl_ee[:7924]

5. Build the 260-element X_model vector exactly per pyactlike:
     X_model[ 0 :  40] = cl_tt_d[5 : 45]              # deep TT (b0=5, 40 bins)
     X_model[40 :  85] = cl_te_d[0 : 45] * yp2        # deep TE (45 bins)
     X_model[85 : 130] = cl_ee_d[0 : 45] * yp2**2     # deep EE (45 bins)
     X_model[130:170]  = cl_tt_w[5 : 45]              # wide TT
     X_model[170:215]  = cl_te_w[0 : 45] * yp2
     X_model[215:260]  = cl_ee_w[0 : 45] * yp2**2

   with yp2 = 1.0 (no polarization fit).

6. Compute residual Y = X_data - X_model (length 260).

7. Compute chi^2 via Fisher (inverse of subselected covariance):
     subcov_full  = cov                                (260 x 260)
     subcov_TT    = block-select [deep TT; wide TT]    (80 x 80)
     subcov_TE    = block-select [deep TE; wide TE]    (90 x 90)
     subcov_EE    = block-select [deep EE; wide EE]    (90 x 90)

     fisher_X     = cho_solve(cho_factor(subcov_X), I)
     diff_X       = corresponding subselected Y entries
     chi2_X       = diff_X . fisher_X . diff_X

   Reported quantities:
     chi2_TT       / dof_TT       (dof_TT  = 80)
     chi2_TE       / dof_TE       (dof_TE  = 90)
     chi2_EE       / dof_EE       (dof_EE  = 90)
     chi2_full     / dof_full     (dof_full = 260)
```

## Sealed PASS Gates

```text
PASS:
  P1  chi2_TT   / dof_TT   <= 2.0
  AND P2  chi2_full / dof_full <= 2.0
  AND P3  polarization NOT degraded
            (chi2_TE/dof_TE <= 3.0 AND chi2_EE/dof_EE <= 3.0)
  AND yp2 fixed = 1.0 (no calibration fit)
  AND free_parameters_introduced = 0
  AND forbidden-file open() guard NOT tripped

BOUNDARY (i) — TT marginal:
  P2 (full) PASS but P1 (TT-only) in (2.0, 3.0]

BOUNDARY (ii) — polarization debt:
  P1 PASS AND P2 PASS but P3 fails
  (TE chi^2/dof > 3.0 OR EE chi^2/dof > 3.0)

BOUNDARY (iii) — full-shape marginal:
  P1 PASS but P2 in (2.0, 3.0]

FAIL:
  None of the above.

There is NO Run B optimizer in CR037C. The verdict tree above is
applied to a single CAMB run with the SAM cosmology fixed.
```

## Reported Evidence (not gates)

```text
E1 — Per-patch chi^2/dof reporting:
  Report chi^2/dof separately for deep and wide patches in TT, TE, EE
  (six reported numbers + the four gated numbers).

E2 — Bandpower-by-bandpower residual table:
  Emit CR037C_residuals.csv: bin_index, bin_label (deep/wide+spec+i),
  ell_peak, X_data, X_sig, X_model, residual, residual_over_sigma.

E3 — Cross-experiment consistency check (reported):
  Compare bandpower predictions at overlap multipoles between ACT DR4
  and Planck PR3 TT (CR037B residuals). Report mean offset and rms.
  This is a diagnostic; not a gate.

E4 — yp2 sensitivity (reported):
  Re-evaluate chi^2_full at yp2 = 0.99 and yp2 = 1.01 to characterize
  sensitivity to the polarization-efficiency calibration. Reported only;
  no gate movement.

E5 — Algebraic verification (parity with CR037B E1):
  Verify the perturbation literals match their substrate identities to
  machine precision:
    A_s_literal == eta_SAM_from_atoms * sqrt(R)
    n_s_literal == 1 - chi_from_atoms / 2
    tau_literal == 2 * A_0_from_atoms
  Reported only; not gated.
```

## Implementation Discipline

```text
The CR037C runner shall:

1. Install forbidden-file open() guard at module load (expanded to
   include CR037A + CR037B + CR036 + CR036B + CR035A2 + CR035A + all
   prior CRs in 19 and other branches). Whitelist only:
     - CR037C_PRECOMMIT.md (this file)
     - CR037C runner source
     - Five ACT DR4 data files listed above
     - CR037C output files (HASHES.txt, summary.json, etc.)

2. Compute SAM density spine in-code from substrate atoms.

3. Set H_0 = 67.2503751950 as a numeric literal.
4. Set A_s = 2.1117473568e-9, n_s = 0.9646322349, tau = 0.0530516477
   as numeric literals from CR037A by value.
5. Set yp2 = 1.0 as a numeric literal.

6. Verify ACT data file sha256 hashes match the sealed values in this
   precommit; FAIL execution if any mismatch.

7. Run CAMB with full SAM cosmology + SAM perturbations at lmax = 8000.

8. Apply ACT bandpower window functions per the pipeline above.

9. Build full Fisher matrices for TT-only, TE-only, EE-only, and full.

10. Compute chi^2_TT, chi^2_TE, chi^2_EE, chi^2_full and dof for each.

11. Apply P1, P2, P3 gates and verdict tree.

12. Emit:
     CR037C_summary.json
     CR037C_result.md
     CR037C_residuals.csv
     HASHES.txt

13. Discipline flags:
     free_parameters_introduced       = 0
     prior_CR_result_inputs           = false
     Run_B_optimizer_used             = false
     yp2_fitted                       = false
     yp2_value                        = 1.0
     CR036_files_opened               = false
     CR036B_files_opened              = false
     CR037A_files_opened              = false
     CR037B_files_opened              = false
     pyactlike_imported               = false
     act_data_sha256_verified         = true
     forbidden_files_opened           = false
```

## Rule-9 Line

```text
This test could have falsified the claim that the SAM-derived cosmology
sealed in CR037B (densities + H_0 + perturbation triplet, all from
substrate atoms via FIRAS T_CMB + CODATA 2018 / SI fixed constants)
reproduces the ACT DR4 (Choi et al. 2020) cleaned-CMB bandpower table
at acceptable ACTPol-only tolerances (chi^2_TT/dof <= 2.0 AND
chi^2_full/dof <= 2.0 AND polarization not degraded), with NO Run B
optimizer and yp2 fixed at 1.0.

It fails if any of P1, P2, P3 evaluate beyond their PASS or BOUNDARY
thresholds, or if the forbidden-file guard trips, or if the ACT data
hashes do not match the sealed values above.
```

## Connection to Future Work

```text
CR037D placeholder
  Full ACT DR4 likelihood with yp2 marginalization. Adds one free
  parameter (yp2) and finds its profile-likelihood best fit. Tests
  whether the parameter-free CR037C result is calibration-limited.

CR037E placeholder
  SPT-3G 2018 TT/TE/EE cross-check. SPT covers ell ~ [300, 3000] with
  different systematics from ACT.

CR037F placeholder
  ACT DR6 (Calabrese et al. 2025) when the public release files are
  available in the same likelihood format.

CR038 (branch verdict zipper)
  Zip the branch CMB chain CR035A -> CR036 -> CR036B -> CR037A ->
  CR037B -> CR037C into a citable closure record. Updates README.
```

## Provenance Hash Chain

| artifact | sha256 |
| --- | --- |
| CR037B@19 sealed PASS | precommit `5b7bd931eb28a6123e848b37867735d627b0f59d4f09433c5bd64261cf0c149b` |
| CR037A@19 sealed PASS | precommit `1b7da85b860825d7e9b0a8e7d231aef92ec980b020341800da81a09f48ba5d78` |
| CR036@19 sealed PASS  | precommit `345a1a8dc180eb6b28141114a82315e3b8d92889537c1219eec4312d59ca33f2` |
| CR036B@19 sealed PASS | precommit `ab2fea4b...`  (per CR037B precommit citation) |
| CR035A2@19 sealed PASS | precommit `6310c00f...` (per CR037B precommit citation) |
| pyactlike like.py reference | `(computed at seal; recorded in HASHES.txt)` |
| ACT DR4 Binning.dat | `fecc173092400f1b53505378a8b0af33f69c4ee2f11fbafdc6d0c1a5e6574738` |
| ACT DR4 cl_cmb_ap.dat | `86a2a3d3cf5bd3b024681ad78fa67d614a9a56ede77ef41716623b45405d6f95` |
| ACT DR4 c_matrix_ap.dat | `3e550bca7f192749e221b9d6db0c323c1a85ca257c398880dea472be43867fea` |
| ACT DR4 coadd_bpwf_15mJy_191127_lmin2.npz | `a4c58bbe02ccb8c132af4a47cf53ec07b261a39b709c598e8b95f6a0d0349225` |
| ACT DR4 coadd_bpwf_100mJy_191127_lmin2.npz | `365de9b3f8b9598c433dbc4f49dc8b996393262d43a526e1a6e257cbb871a270` |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
