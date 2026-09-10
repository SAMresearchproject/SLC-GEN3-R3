# CR036_ETA_SAM_AND_H0_SELECTOR Precommit

## Verdict Ladder

```text
PASS:
  P1 PASS  AND  P2 PASS.

BOUNDARY:
  At least one of (P1, P2) is BOUNDARY, AND neither is FAIL.

FAIL:
  P1 FAIL  OR  P2 FAIL.
```

P1 and P2 are the load-bearing scientific claims. I1 is reported
implementation-integrity only and does NOT gate the verdict. E1-E5
are reported sensitivity evidence and do NOT gate the verdict.

## Test Type

```text
Fresh Courtroom branch test in:
  19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER

External anchors (declared as numeric constants in this precommit;
files containing them are NOT read by the runner):
  T_CMB = 2.7255 K                  (FIRAS thermal anchor)
  eta_reference = 6.119e-10         (Planck 2018 CMB-side reference value)
  H_0_reference = 67.36 km/s/Mpc    (Planck 2018 TT,TE,EE+lowE+lensing
                                     base posterior central value)

Substrate input:
  Substrate atoms only. No prior CR file is read.

Engine:
  Pure Python + scipy.constants for fundamental constants.
  No CAMB, no CLASS, no Boltzmann solver. eta -> omega_b conversion is
  derived in-runner from first-principles photon counting and Friedmann
  critical density.

Prior-CR exclusion:
  No CR001 / CR001b / CR001c / CR002 / CR003 / CR018b / CR019 / CR025 /
  CR031b / CR032 / CR033 / CR035A / CR035A2 / CR205 or any prior CR
  result/summary/evidence file may be read by the runner.

Posterior-table / fitted-anchor exclusion:
  No Planck CMB spectra. No CR035A/CR035A2 outputs. No Planck best-fit
  H_0 file. No BAO-fitted H_0 file. No SN-fitted H_0 file. No posterior
  table used to choose H_0.
```

## Why This Test Matters

```text
CR035A2 sealed PASS with the SAM density spine (Omega_m=1/pi,
Omega_b=2*A_0*(1-chi), Omega_c=Omega_m-Omega_b) paired with H_0 = 68.76
set externally and Planck-centroid (A_s, n_s, tau) perturbations.

In a CAMB/Boltzmann run, H_0 enters via h = H_0/100 to fix the physical
densities omega_b = Omega_b*h^2 and omega_c = Omega_c*h^2. If H_0 is
external, then omega_b and omega_c are partly external. For a clean
order Omega_m,SAM, Omega_b,SAM, Omega_c,SAM, H_0,SAM -> omega -> C_ell,
H_0 must come from substrate atoms with a declared dimensional bridge.

CR036 derives H_0,SAM via the chain:
  substrate atoms ---> eta_SAM
  eta_SAM + T_CMB(FIRAS) + (c, hbar, k_B, G, Mpc, m_b=m_p)
                  ---> omega_b,SAM    (in-runner derivation)
  omega_b,SAM + Omega_b,SAM(substrate) ---> h_SAM
  H_0,SAM = 100 * h_SAM

The dimensional bridge is T_CMB plus fundamental physical constants;
it is declared explicitly and is NOT a CMB-spectrum input. The closed-
form eta_SAM identity uses substrate atoms only, with zero fitted
exponent (the 6 is identified as the closed-ledger-to-write-cell
reducer L/V = 162/27).

CR036 does NOT claim full parameter-free cosmology; the perturbation
sector (A_s, n_s, tau) remains externally anchored. The claim is
narrowly: the SAM density spine and the CMB-side H_0 anchor are both
derivable from substrate atoms + the FIRAS thermal anchor + fundamental
constants, with zero free parameters.
```

## Question

```text
Does the substrate-atom identity

   eta_SAM = (M / (alpha_H^2 * Theta)) * A_0^(L/V) = 7 / (4 * (12*pi)^6)

evaluated together with the dimensional bridge

   T_CMB = 2.7255 K (FIRAS),
   plus the fundamental constants c, hbar, k_B, G,
   plus the Mpc length definition,
   plus the declared baryon mass m_b = m_p,

reproduce the CMB-side reference baryon-to-photon ratio
eta_reference = 6.119e-10 to within +/- 1.0% (P1 PASS band),

AND does the derived H_0 cascade

   omega_b,SAM = eta_SAM / K_eta_to_omega_b
                 where K_eta_to_omega_b is computed IN-RUNNER from
                 (c, hbar, k_B, G, T_CMB, m_b, Mpc)
   h_SAM^2     = omega_b,SAM / Omega_b,SAM     with Omega_b,SAM = 2*A_0*(1-chi)
   H_0,SAM     = 100 * h_SAM   km/s/Mpc

reproduce the CMB-side reference H_0_reference = 67.36 km/s/Mpc to
within +/- 1.0% (P2 PASS band),

with zero free parameters, zero CMB spectrum input, zero posterior
table input, and no prior-CR result file read?
```

## Substrate Identity Under Test

```text
Atoms used:
  M       = 126        (matter capacity = R^2 - Theta = 144 - 18)
  alpha_H = 2          (binary readout)
  Theta   = 18         (tensor bridge = alpha_H * D^2)
  L       = 162        (closed carrier ledger = alpha_H * F = 2 * 81)
  V       = 27         (resolved write cell = D^3)
  D       = 3
  A_0     = V / (pi * alpha_H * L) = 1/(12*pi)
  chi     = (S/D) * A_0 = 2/(9*pi)
  Omega_b = 2 * A_0 * (1 - chi)

Exponent identification (load-bearing structural step):
  6 = alpha_H * D = R/2 = Theta/D = L/V

  The fourth identification L/V = 162/27 = 6 is the closed-ledger to
  resolved-write-cell reducer. The six-lane operator
    SW | WRITE | OUTSIDE | INSIDE | WRITE | SW
  is the route by which the closed ledger L resolves into the write
  cell V; A_0 = V / (pi * alpha_H * L) is the write-cell share of the
  binary closed ledger after this reduction.

The eta identity:

  eta_SAM = (M / (alpha_H^2 * Theta)) * A_0^(L/V)
          = (7/4) * A_0^6
          = 7 / (4 * (12*pi)^6)

Numerical value (closed-form):
  (12*pi)^6      = 2,870,255,316
  7 / (4 * ...)  = 6.0970 x 10^-10
```

## Dimensional Bridge (declared)

```text
The substrate-atom identity above produces a dimensionless eta_SAM.
To carry that to physical units (omega_b in km^-2 s^2, then H_0 in
km/s/Mpc), CR036 declares the following dimensional bridge:

  T_CMB = 2.7255 K           (FIRAS measurement; H_0-independent)

  Fundamental constants (CODATA 2018 / SI fixed constants, in-code
  numeric literals):
    c     = 299792458 m/s            (defined, SI exact)
    h     = 6.62607015e-34 J*s       (defined since 2019 SI exact)
    hbar  = h / (2 * pi)             COMPUTED IN-RUNNER from h
    k_B   = 1.380649e-23 J/K         (defined since 2019 SI exact)
    G     = 6.67430e-11 m^3/(kg*s^2) (CODATA 2018)

  Length / distance:
    Mpc   = 3.0856775815e22 m        (parsec-based; H_0-independent)

  Baryon mass (declared):
    m_b   = m_p = 1.67262192369e-27 kg   (CODATA 2018)

These are the ONLY dimensional inputs. The runner has no other knobs.
None of them came from any CMB spectrum, BAO fit, SN fit, or posterior
table. T_CMB is from FIRAS direct thermal measurement.
```

## In-Runner Conversion Derivation (NOT hardcoded)

```text
The runner shall NOT hardcode the value 2.735e-8 or any equivalent
eta-to-omega_b conversion constant. It shall derive it from first
principles:

Step 1 - photon number density at T_CMB (Planck blackbody):
  hbar = h / (2 * pi)                        (computed in-runner)
  n_gamma = (2 * zeta(3) / pi^2) * (k_B * T_CMB / (hbar * c))^3
         where zeta(3) = 1.2020569031595942853997381...

Step 2 - critical density at h = 1:
  rho_crit_h1 = 3 * H_100^2 / (8 * pi * G)
              where H_100 = 100 km/s/Mpc converted to s^-1
                    = 100 * 1000 / Mpc  [s^-1]

Step 3 - baryon number density per omega_b:
  n_b_per_omega_b = rho_crit_h1 / m_b

Step 4 - conversion (eta = K * omega_b):
  K_eta_to_omega_b = n_b_per_omega_b / n_gamma

The runner SHALL report:
  K_eta_to_omega_b  (computed)
  Standard literature value 2.735e-8  (declared as numeric constant)
  Relative deviation between computed and standard
  These three are reported in E2 (sensitivity evidence, not a gate).
```

## Strict Input Discipline

```text
Allowed in-code numeric inputs (no file read):
  Substrate atoms (R, D, S, alpha_H, Theta, M, F, L, V, A_0, chi)
  T_CMB = 2.7255 K
  c, h, k_B, G, Mpc, m_b (CODATA 2018 / SI exact numeric literals)
    hbar derived as h/(2*pi) in-runner
  eta_reference = 6.119e-10
  H_0_reference = 67.36 km/s/Mpc

Expected closed-form values (verifiable against the seal):
  eta_SAM   = 6.09608952448e-10
  H_0_SAM   = 67.25037526 km/s/Mpc

Allowed engines:
  Python standard library
  numpy
  scipy.constants     (allowed only as a sanity cross-check; the
                       runner uses its own in-code CODATA literals as
                       canonical to preserve hash stability)

Allowed external sources:
  None at runtime. No file is opened by the runner except its own
  output artifacts.
```

## Forbidden Inputs

```text
The CR036 runner must not read, import, parse, compare against, or use:

  Any CMB power spectrum file (Planck PR3 *.txt, *.fits, *.cls)
  CR035A* and CR035A2* result/summary/evidence/residuals files
  CR035A_runner*.py and CR035A2_runner.py
  CR001 / CR001b / CR001c / CR002 / CR003 family files
  CR018b / CR019 family files
  CR025 / CR031b / CR032 / CR033 family files
  CR205 files
  Planck likelihood files (clik, plik, lite)
  Planck base parameter best-fit chain files / posterior tables
  BAO best-fit H_0 files / chains
  SN best-fit H_0 files / chains
  Any prior CR result.md / summary.json / evidence_rows.csv
  Any external H_0 measurement table read at runtime

The forbidden-file open() guard installed at module load aborts execution
if any path matching these patterns is opened.
```

## Frozen External References (numeric constants, not read from files)

```text
eta_reference (P1 comparison anchor):
  6.119e-10
  Source citation: Planck 2018 baseline base_plikHM_TTTEEE_lowl_lowE
  ω_b posterior central converted to eta via the standard relation.
  Declared in this precommit as a numeric literal. The runner does NOT
  open the Planck file; it cites this number as a frozen constant.

eta_BBN_consensus (E1 strong-contact comparison; reported only):
  6.10e-10
  Source citation: D/H consensus (Cooke et al. 2018) +/- 0.04e-10.
  Declared as a numeric literal in the precommit. Used only for E1
  strong-contact reporting, not in P1 gate.

H_0_reference (P2 comparison anchor):
  67.36 km/s/Mpc
  Source citation: Planck 2018 base_plikHM_TTTEEE_lowl_lowE_lensing
  baseline posterior central +/- 0.54.
  Declared in the precommit as a numeric literal. The runner does NOT
  open the Planck chain; it cites this number as a frozen constant.
```

## P1 — eta_SAM vs CMB-side eta reference (load-bearing)

```text
Statistic:
  eta_dev_pct = 100 * (eta_SAM - eta_reference) / eta_reference

Bands:
  PASS:      |eta_dev_pct| <= 1.0
  BOUNDARY:  1.0 < |eta_dev_pct| <= 2.0
  FAIL:      |eta_dev_pct| > 2.0

Strong-contact evidence (reported, not gated):
  |eta_dev_pct| <= 0.5  -> flagged as STRONG_CONTACT_ETA
```

## P2 — H_0,SAM vs frozen external CMB-side H_0 reference (load-bearing)

```text
Cascade:
  omega_b,SAM = eta_SAM / K_eta_to_omega_b      (K computed in-runner)
  h_SAM^2     = omega_b,SAM / Omega_b,SAM       (Omega_b from substrate atoms)
  H_0,SAM     = 100 * h_SAM                     km/s/Mpc

Statistic:
  H0_dev_pct  = 100 * (H_0,SAM - H_0_reference) / H_0_reference

Bands:
  PASS:      |H0_dev_pct| <= 1.0
  BOUNDARY:  1.0 < |H0_dev_pct| <= 2.0
  FAIL:      |H0_dev_pct| > 2.0
```

## I1 — H_0,SAM Implementation Self-Consistency (NOT a science gate)

```text
The runner shall recompute the cascade through two paths and check
that they agree to floating-point precision (relative agreement
< 1e-12):

Path A:
  eta_SAM_atoms      = (M / (alpha_H^2 * Theta)) * A_0^(L/V)
  omega_b,SAM        = eta_SAM_atoms / K_eta_to_omega_b
  h_SAM_A^2          = omega_b,SAM / (2 * A_0 * (1 - chi))

Path B (algebraic compact form):
  eta_SAM_compact    = 7 / (4 * (12 * pi)^6)
  omega_b,SAM_B      = eta_SAM_compact / K_eta_to_omega_b
  h_SAM_B^2          = omega_b,SAM_B / (2 * A_0 * (1 - chi))

Report agreement |h_SAM_A^2 - h_SAM_B^2| / h_SAM_A^2.

I1 PASS:  agreement < 1e-12  -> implementation_integrity = OK
I1 FAIL:  otherwise           -> implementation_integrity = FLOATING_POINT_DRIFT

I1 is reported as implementation integrity and does NOT gate the
scientific verdict.
```

## Reported Evidence (not gates)

```text
E1 - Strong-contact eta comparison:
  Compare eta_SAM also against eta_BBN_consensus = 6.10e-10.
  Report STRONG_CONTACT_ETA flag if |dev| <= 0.5% against EITHER
  eta_reference OR eta_BBN_consensus.

E2 - Conversion constant cross-check:
  Computed K_eta_to_omega_b
  Standard literature value 2.735e-8
  Relative deviation

E3 - Four-way 6-identity verification:
  Verify alpha_H*D = R/2 = Theta/D = L/V = 6 to integer equality.
  Verify 162/27 = 6 exactly.

E4 - A_0 dual-form verification:
  Verify A_0 = V/(pi*alpha_H*L) = 1/(12*pi) to floating-point precision.
  Verify cancellation: A_0 = (L/6)/(pi*alpha_H*L) = 1/(6*pi*alpha_H)
                        = 1/(12*pi) when alpha_H = 2.

E5 - Downstream cascade values reported:
  omega_b,SAM
  h_SAM
  H_0,SAM
  z_eq,SAM via z_eq + 1 = omega_m,SAM / (omega_gamma * (1 + 0.2271*N_eff))
            with omega_gamma computed in-runner from T_CMB blackbody.
            (N_eff = 3.046 as standard.)
  Reported deviations vs Planck z_eq ~ 3387 (cited as numeric constant,
  not read).
```

## Implementation Discipline

```text
The CR036 runner shall:

1. Install forbidden-file open() guard at module load.
2. Define all substrate atoms in-code as numeric literals.
3. Define all fundamental constants in-code as CODATA-cited numeric
   literals. Do NOT import constants from scipy.constants at runtime
   for canonical values; scipy.constants may be used only as a
   sanity-check report.
4. Compute n_gamma (blackbody at T_CMB) from first principles.
5. Compute rho_crit_h1 from Friedmann equation at h=1.
6. Compute K_eta_to_omega_b = rho_crit_h1 / (m_b * n_gamma).
7. Compute eta_SAM_atoms and eta_SAM_compact (Paths A and B).
8. Compute omega_b,SAM, h_SAM, H_0,SAM.
9. Apply P1, P2, I1.
10. Compute z_eq cascade for E5.
11. Emit:
    CR036_summary.json
    CR036_result.md
    CR036_evidence_rows.csv     (atom values, intermediate quantities,
                                  conversion constant, cascade products)
    CR036_substrate_atoms.csv   (sealed atom table with provenance)

Precision:
  pi = math.pi
  Substrate-atom math is integer where possible.
  Floating-point arithmetic to native double precision.
  Reported quantities to >= 6 significant digits.

No fitting:
  free_parameters_introduced = 0
  external_inputs            = {T_CMB, c, hbar, k_B, G, Mpc, m_b}
                               (declared as dimensional bridge; NOT
                                fitted, NOT chosen from CMB)
  prior_CR_result_inputs     = false
  CMB_spectrum_inputs        = false
  posterior_table_inputs     = false
```

## Frozen Sources

```text
Allowed (in-code numeric literals; no file read):
  Substrate atoms (R, D, S, alpha_H, Theta, M, F, L, V, A_0, chi)
  T_CMB = 2.7255 K
  c, hbar, k_B, G, Mpc, m_b (CODATA 2018 values)
  eta_reference = 6.119e-10
  eta_BBN_consensus = 6.10e-10
  H_0_reference = 67.36 km/s/Mpc

Forbidden:
  See "Forbidden Inputs" section.
```

## Chronology and Honest Framing

```text
This precommit is retrospective relative to CR035A2. The eta_SAM
identity was recognized after CR035A2 sealed PASS with H_0 = 68.76 set
externally. The exponent 6 = L/V identification (162/27 = 6) was the
piece that elevated the candidate from "phenomenologically fitted
integer power" to "substrate-derived ledger-to-write-cell reducer."

The honest framing is:

  CR036 is a retrospective substrate-identification CR. It derives
  eta_SAM and H_0,SAM from substrate atoms plus a declared dimensional
  bridge (T_CMB FIRAS + fundamental constants), with zero free
  parameters and zero CMB-spectrum input. It compares the derived
  values to frozen external CMB-side references (Planck 2018) declared
  as numeric constants in the precommit, not read by the runner.

Do not write:
  SAM predicted eta and H_0 before measurement.

Do write:
  SAM identifies eta and H_0 retrospectively from the substrate atoms
  R, D, S, alpha_H, Theta, M, L, V and the closure A_0 = V/(pi*alpha_H*L),
  with the dimensional bridge T_CMB(FIRAS) + (c, hbar, k_B, G, Mpc, m_p).
  CR036 confirms the derived values land within the predeclared
  tolerances vs the frozen external Planck 2018 references, without
  reading any CMB spectrum or posterior file.

Prospective validation requires CR036B (rerun the CR035A2 pipeline with
H_0 = H_0,SAM) and/or further independent anchors.
```

## Rule-9 Line

```text
This test could have falsified the claim that the substrate-atom
identities

  eta_SAM = (M / (alpha_H^2 * Theta)) * A_0^(L/V) = 7 / (4 * (12*pi)^6)

and the derived cascade

  H_0,SAM = 100 * sqrt( (eta_SAM / K_eta_to_omega_b) / (2*A_0*(1-chi)) )

with K_eta_to_omega_b computed in-runner from (c, hbar, k_B, G, T_CMB,
m_p, Mpc), reproduce the CMB-side reference values eta_reference =
6.119e-10 and H_0_reference = 67.36 km/s/Mpc to within +/- 1.0%.

It fails if:
  |eta_dev_pct|  > 2.0   (P1 FAIL)
  OR
  |H0_dev_pct|   > 2.0   (P2 FAIL)
```

## Result Text Requirements

```text
If P1 PASS and P2 PASS, CR036_result.md must state:

  CR036 PASS confirms that the substrate-atom identities
  eta_SAM = (M / (alpha_H^2 * Theta)) * A_0^(L/V) = 7 / (4 * (12*pi)^6)
  and the derived H_0,SAM = 100 * sqrt(omega_b,SAM / Omega_b,SAM)
  reproduce the CMB-side reference values eta = 6.119e-10 and
  H_0 = 67.36 km/s/Mpc to within +/- 1.0% (eta_dev_pct = X.XX,
  H0_dev_pct = Y.YY), using only substrate atoms and the declared
  dimensional bridge (T_CMB FIRAS + c, hbar, k_B, G, Mpc, m_p).

If BOUNDARY, state which gate is in the boundary band and the
diagnostic deviation values.

If FAIL, state which gate failed and by how much.

In all cases:
  execution_status                = CLEAN or not CLEAN with reason
  free_parameters_introduced      = 0
  prior_CR_result_inputs          = false
  CMB_spectrum_inputs             = false
  posterior_table_inputs          = false
  forbidden_files_opened          = false
  K_eta_to_omega_b_computed       = the in-runner derived value
  implementation_integrity        = OK or FLOATING_POINT_DRIFT
```

## Manuscript Headline If PASS (conditional)

```text
SAM derives the bound-cosmology H_0 reference from substrate atoms
through the chain:

  eta_SAM = (M / (alpha_H^2 * Theta)) * A_0^(L/V) = 7 / (4 * (12*pi)^6)
  K_eta_to_omega_b derived from (c, hbar, k_B, G, T_CMB(FIRAS), m_p, Mpc)
  omega_b,SAM = eta_SAM / K_eta_to_omega_b
  Omega_b,SAM = 2 * A_0 * (1 - chi)        (substrate atoms)
  h_SAM = sqrt(omega_b,SAM / Omega_b,SAM)
  H_0,SAM = 100 * h_SAM

This chain uses zero free parameters and zero CMB-spectrum input. The
dimensional bridge is the FIRAS thermal anchor T_CMB = 2.7255 K plus
fundamental physical constants. CR036 confirms that eta_SAM and H_0,SAM
land within +/- 1.0% of the Planck 2018 CMB-side references.

Do not claim:
  SAM-predicted H_0 before measurement.
  Full perturbation-sector derivation.

Do write:
  SAM identifies eta and H_0 retrospectively from substrate atoms and
  the FIRAS thermal anchor. Prospective validation in CR036B will
  re-run the CR035A2 pipeline with H_0 = H_0,SAM.
```

## Connection to Future Work

```text
CR036B placeholder
  Re-run the CR035A2 SAM-density-spine CMB shape test with H_0 set
  to H_0,SAM (derived in CR036) instead of the externally set 68.76.
  Verdict gates same as CR035A2 (P1 peak structure, P2 TT chi^2/dof).
  Will be drafted as a separate precommit after CR036 is sealed and
  hashed.

CR037 placeholder (open derivation)
  Derive A_s, n_s, tau from substrate atoms, or document the structural
  gap.

CR038 placeholder (independent BBN/D/H validation)
  Compare eta_SAM to a frozen BBN D/H-based eta measurement
  independently of CMB.
```

## Stewardship Reference

```text
STEWARDSHIP_DECLARATION.md SHA-256
  d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```
