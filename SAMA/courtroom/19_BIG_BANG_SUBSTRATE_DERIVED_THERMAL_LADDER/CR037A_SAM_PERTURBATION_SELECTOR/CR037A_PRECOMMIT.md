# CR037A_SAM_PERTURBATION_SELECTOR Precommit

## Verdict Ladder

```text
Per-parameter band (used by P1, P2, P3):
  PASS:      |sigma_dev| <= 1.0
  BOUNDARY:  1.0 < |sigma_dev| <= 2.0
  FAIL:      |sigma_dev| >  2.0

Overall CR037A verdict:
  PASS:      All three of P1, P2, P3 are PASS.
  BOUNDARY:  At least one of P1, P2, P3 is BOUNDARY, AND none is FAIL.
  FAIL:      Any one of P1, P2, P3 is FAIL.
```

P1, P2, P3 are the load-bearing scientific claims. Strong-contact and
clean-contact flags are reported sensitivity evidence; they do NOT gate
the verdict.

## Test Type

```text
Fresh Courtroom branch test in:
  19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER

Frozen external references (numeric constants; runner does NOT open files):
  A_s_reference = 2.100e-9   +/- sigma_As  = 0.030e-9
  n_s_reference = 0.9649     +/- sigma_ns  = 0.0042
  tau_reference = 0.0544     +/- sigma_tau = 0.0073
  (Planck 2018 base_plikHM_TTTEEE+lowE+lensing posterior centroids
   and 1-sigma widths)

Substrate input:
  Substrate atoms only. No prior CR file is read.

Engine:
  Python standard library + math + (optional numpy).
  No CAMB, no scipy required.
  No Boltzmann run; this CR computes three closed-form substrate
  numbers and compares them to frozen references.

Prior-CR exclusion:
  No CR001 / CR001b / CR001c / CR002 / CR003 / CR018b / CR019 / CR025 /
  CR031b / CR032 / CR033 / CR035A / CR035A2 / CR036 / CR036B / CR205
  or any prior CR result/summary/evidence file may be read.
```

## Why This Test Matters

```text
CR035A2 sealed PASS with H_0 = 68.76 externally set and Planck-centroid
(A_s, n_s, tau) perturbations.
CR036 sealed PASS deriving H_0_SAM = 67.2503751950 from substrate atoms
+ FIRAS T_CMB + CODATA 2018 / SI fixed constants.
CR036B sealed PASS at TT chi^2/dof = 1.04 with H_0 = H_0_SAM + Planck-
centroid (A_s, n_s, tau) perturbations.

The perturbation sector (A_s, n_s, tau) is the last externally-anchored
input in the cosmology chain. CR037A is the selector: it proposes three
closed-form SAM identities for (A_s, n_s, tau) and tests whether they
land inside the Planck posterior at the +/- 2 sigma level. No CMB
spectrum is consulted.

Candidate identities under test:

  n_s_SAM   = 1 - chi/2
            = 1 - 1/(9*pi)
              ("scalar tilt = unit scale-invariant spectrum after a
                half-horizon quotient debit")

  A_s_SAM   = eta_SAM * sqrt(R)
              ("scalar amplitude = baryon/photon substrate number ratio
                lifted by the sqrt(R) route")

  tau_SAM   = 2 * A_0 = 1/(6*pi)
              ("reionization optical screen begins as the two-side
                accumulation floor")

These are the FIRST candidates Sean would seal. The n_s identity is
the cleanest structurally (chi/2 -> 1/(9*pi) is one substrate atom).
The A_s identity is structurally simple but conceptually weakest of
the three; obvious wrong-control comparators are reported in E.
The tau identity uses 2*A_0; the closer self-lifted candidate
2*A_0*(1+A_0) is NOT used because it "smells like a correction layer
unless we already have a sealed reason for the self-lift."

CR037A is the perturbation-selector. If all three PASS at +/- 2 sigma,
CR037B follows (parameter-free CMB shape attempt with these
perturbation values in the CR036B pipeline). If any FAIL, the
identity or identities that fail are rejected and the candidate
triplet does not advance to CR037B.
```

## Question

```text
Do the three closed-form substrate identities

  A_s_SAM = eta_SAM * sqrt(R) = 7 * sqrt(R) / (4 * (12*pi)^6)
  n_s_SAM = 1 - chi/2 = 1 - 1/(9*pi)
  tau_SAM = 2 * A_0 = 1/(6*pi)

all land within +/- 2 sigma of the Planck 2018 posterior centroids

  A_s_reference = 2.100e-9   sigma_As  = 0.030e-9
  n_s_reference = 0.9649     sigma_ns  = 0.0042
  tau_reference = 0.0544     sigma_tau = 0.0073

with zero free parameters and zero prior-CR file read?
```

## Substrate Identities Under Test

```text
Atoms:
  R = 12, D = 3, S = 8, alpha_H = 2
  Theta = 18, M = 126, F = 81, L = 162, V = 27
  A_0 = 1/(12*pi)
  chi = (S/D)*A_0 = 2/(9*pi)

Eta identity (from CR036, by value; CR036 file NOT opened):
  eta_SAM = (M / (alpha_H^2 * Theta)) * A_0^(L/V)
          = 7 / (4 * (12*pi)^6)
          = 6.09608952448e-10  (sealed in CR036)

Perturbation identities:

  n_s_SAM  = 1 - chi/2
           = 1 - 1/(9*pi)
           = 0.9646322349 (expected)

  A_s_SAM  = eta_SAM * sqrt(R)
           = 7 * sqrt(R) / (4 * (12*pi)^6)
           = 2.1117473568e-9 (expected)

  tau_SAM  = 2 * A_0
           = 2 / (12*pi)
           = 1 / (6*pi)
           = 0.0530516477 (expected)
```

## Frozen External References (numeric constants; NOT read at runtime)

```text
A_s_reference   = 2.100e-9     (Planck 2018 base posterior centroid)
sigma_As        = 0.030e-9     (Planck 2018 base posterior 1-sigma)

n_s_reference   = 0.9649       (Planck 2018 base posterior centroid)
sigma_ns        = 0.0042       (Planck 2018 base posterior 1-sigma)

tau_reference   = 0.0544       (Planck 2018 base posterior centroid)
sigma_tau       = 0.0073       (Planck 2018 base posterior 1-sigma)

Source citation: Planck 2018 results VI base_plikHM_TTTEEE+lowE+lensing.
Declared here as numeric literals. The runner does NOT open the Planck
chain or posterior table.
```

## Strict Input Discipline

```text
Allowed in-code numeric inputs (no file read):
  Substrate atoms (R, D, S, alpha_H, Theta, M, F, L, V, A_0, chi)
  Frozen Planck reference centroids and sigmas (above)
  Expected SAM values are computed in-runner from atoms; no hardcoded
    numeric crib of the expected output is checked against by the gate
    (verification of the closed-form math is part of the runner output)

Allowed engine:
  Python standard library + math (+ optional numpy)
  NO scipy required
  NO CAMB
  NO file open of any kind beyond writing the runner's own artifacts

Forbidden: see "Forbidden Inputs" below.
```

## Forbidden Inputs

```text
The CR037A runner must not read, import, parse, compare against, or use:

  Any Planck CMB power spectrum file
  Any Planck likelihood / posterior chain / posterior table file
  CR036B family files
  CR036 family files
  CR035A2 family files
  CR035A family files
  CR001 / CR001b / CR001c / CR002 / CR003 family files
  CR018b / CR019 family files
  CR025 / CR031b / CR032 / CR033 family files
  CR205 files
  Any prior CR result.md / summary.json / evidence_rows.csv

The forbidden-file open() guard aborts execution if any path matching
these patterns is opened.
```

## P1 — A_s_SAM vs Planck A_s reference (load-bearing)

```text
Statistic:
  sigma_dev_As = (A_s_SAM - A_s_reference) / sigma_As

P1 PASS:      |sigma_dev_As| <= 1.0
P1 BOUNDARY:  1.0 < |sigma_dev_As| <= 2.0
P1 FAIL:      |sigma_dev_As| >  2.0

Strong-contact reported flag (NOT gate):
  STRONG_CONTACT_AS  if |sigma_dev_As| <= 0.5
```

## P2 — n_s_SAM vs Planck n_s reference (load-bearing)

```text
Statistic:
  sigma_dev_ns = (n_s_SAM - n_s_reference) / sigma_ns

P2 PASS:      |sigma_dev_ns| <= 1.0
P2 BOUNDARY:  1.0 < |sigma_dev_ns| <= 2.0
P2 FAIL:      |sigma_dev_ns| >  2.0

Strong-contact reported flag (NOT gate):
  STRONG_CONTACT_NS  if |sigma_dev_ns| <= 0.5
```

## P3 — tau_SAM vs Planck tau reference (load-bearing)

```text
Statistic:
  sigma_dev_tau = (tau_SAM - tau_reference) / sigma_tau

P3 PASS:      |sigma_dev_tau| <= 1.0
P3 BOUNDARY:  1.0 < |sigma_dev_tau| <= 2.0
P3 FAIL:      |sigma_dev_tau| >  2.0

Strong-contact reported flag (NOT gate):
  STRONG_CONTACT_TAU  if |sigma_dev_tau| <= 0.5
```

## Reported Evidence (not gates)

```text
E1 — Wrong-control sanity (A_s candidate comparators):
  Compute and report:
    eta_SAM          ("bare" baryon/photon ratio)
    eta_SAM * sqrt(S)
    eta_SAM * sqrt(R/2)
    eta_SAM * sqrt(Theta)
    eta_SAM * D
    eta_SAM * pi
  Report each as sigma_dev vs A_s_reference. The canonical A_s_SAM =
  eta_SAM * sqrt(R) "earns its place" if its sigma_dev is the smallest
  of the set (or tied for smallest). This is sensitivity evidence;
  not gated.

E2 — Closer self-lifted tau candidate (reported for completeness):
  tau_alt = 2 * A_0 * (1 + A_0) = 0.0544588864
  Report sigma_dev_tau_alt = (tau_alt - tau_reference) / sigma_tau.
  The canonical CR037A tau_SAM = 2*A_0 is used for P3; tau_alt is
  reported only.

E3 — Substrate-form algebraic checks:
  Verify chi = 2/(9*pi) exactly from atoms.
  Verify A_0 = 1/(12*pi) exactly.
  Verify n_s_SAM = 1 - 1/(9*pi) by two paths
    (1 - chi/2 and 1 - 1/(9*pi)) agree to machine precision.
  Verify A_s_SAM = eta_SAM * sqrt(R) and also
                 = 7 * sqrt(R) / (4 * (12*pi)^6) agree to machine precision.
  Verify tau_SAM = 2 * A_0 = 1 / (6*pi) by two paths agree to machine precision.

E4 — Strong-contact summary:
  Report a single dictionary:
    {STRONG_CONTACT_AS, STRONG_CONTACT_NS, STRONG_CONTACT_TAU}
  where each flag is true iff |sigma_dev| <= 0.5 for the corresponding
  parameter.
```

## Implementation Discipline

```text
The CR037A runner shall:

1. Install forbidden-file open() guard at module load (expanded to
   include CR036/CR036B/CR035A2/CR035A family + all prior CRs).
2. Define all substrate atoms in-code as numeric literals or integers.
3. Compute eta_SAM in-runner from atoms (no read of CR036 files).
4. Compute n_s_SAM, A_s_SAM, tau_SAM in two paths each and verify
   machine-precision agreement (E3).
5. Compute sigma_dev for each of A_s, n_s, tau.
6. Apply P1, P2, P3 gates.
7. Compute and report E1 wrong-control comparators for A_s.
8. Compute and report E2 self-lifted tau alternative.
9. Compute and report E4 strong-contact / clean-contact flags.
10. Emit:
    CR037A_summary.json
    CR037A_result.md
    CR037A_evidence_rows.csv

Precision:
  pi = math.pi
  Reported values to >= 10 significant digits
  Reported sigma deviations to >= 4 significant digits

No fitting:
  free_parameters_introduced     = 0
  prior_CR_result_inputs         = false
  CMB_spectrum_inputs            = false
  posterior_table_inputs         = false
```

## Frozen Sources

```text
Allowed (in-code numeric literals only):
  Substrate atoms (R, D, S, alpha_H, Theta, M, F, L, V, A_0, chi)
  Planck posterior centroids (A_s_ref, n_s_ref, tau_ref)
  Planck posterior sigmas (sigma_As, sigma_ns, sigma_tau)

Forbidden: see "Forbidden Inputs" section.

CR036 provenance (provenance only; the CR036 file is NOT opened):
  CR036_PRECOMMIT.md SHA-256
    345a1a8dc180eb6b28141114a82315e3b8d92889537c1219eec4312d59ca33f2
  eta_SAM value cited from CR036 by value:
    eta_SAM = 6.09608952448e-10 (verified in CR037A runner from atoms)

CR036B provenance (provenance only):
  CR036B_PRECOMMIT.md SHA-256
    ab2fea4b0822412cc5ca9978bab89822ea6fccffa76f94527bff05aaa660305e
```

## Chronology and Honest Framing

```text
This precommit is forward of CR036/CR036B. The substrate identities

  n_s_SAM = 1 - chi/2
  A_s_SAM = eta_SAM * sqrt(R)
  tau_SAM = 2 * A_0

were proposed by Sean as the FIRST candidate perturbation triplet to
test. They are not yet uniquely structurally derived; they are
candidate identities chosen for substrate-simplicity and obvious
wrong-control structure.

CR037A asks one question only: do these three SAM identities land
within +/- 2 sigma of the Planck posterior centroids? If yes, CR037B
runs them through CR036B's pipeline (parameter-free CMB shape
attempt). If no, the failing identity is rejected and the candidate
triplet does not advance.

Do not write:
  CR037A "proves" the SAM perturbation sector.
  SAM derives all six cosmological parameters.

Do write:
  CR037A is a selector test. Three closed-form SAM candidates for
  the perturbation triplet (A_s, n_s, tau) are compared to the
  Planck 2018 posterior centroids at the +/- 2 sigma envelope. The
  selector does not consult the Planck CMB spectra; it tests only
  whether the candidate identities are inside the posterior window.
```

## Rule-9 Line

```text
This test could have falsified the claim that all three of the
substrate-atom identities

  n_s_SAM = 1 - chi/2
  A_s_SAM = eta_SAM * sqrt(R)
  tau_SAM = 2 * A_0

land within +/- 2 sigma of the Planck 2018 posterior centroids
(A_s_ref = 2.100e-9, n_s_ref = 0.9649, tau_ref = 0.0544).

It fails if any of |sigma_dev_As|, |sigma_dev_ns|, |sigma_dev_tau|
exceeds 2.0. It returns BOUNDARY if at least one is in (1.0, 2.0] AND
none exceeds 2.0.
```

## Result Text Requirements

```text
If PASS:
  CR037A PASS confirms that all three SAM perturbation identities
  (n_s_SAM = 1 - chi/2; A_s_SAM = eta_SAM * sqrt(R); tau_SAM = 2*A_0)
  land within +/- 2 sigma of the Planck 2018 posterior centroids
  (sigma_dev_As = X.XX, sigma_dev_ns = Y.YY, sigma_dev_tau = Z.ZZ),
  using only substrate atoms.

If FAIL:
  State which gate(s) failed and the corresponding sigma deviation(s).

In all cases:
  execution_status               = CLEAN or not CLEAN with reason
  free_parameters_introduced     = 0
  prior_CR_result_inputs         = false
  CMB_spectrum_inputs            = false
  posterior_table_inputs         = false
  forbidden_files_opened         = false
```

## Manuscript Headline If PASS (conditional)

```text
SAM identifies three closed-form substrate candidates for the
cosmological perturbation triplet:
  n_s = 1 - chi/2 = 1 - 1/(9*pi)
  A_s = eta_SAM * sqrt(R)
  tau = 2 * A_0 = 1/(6*pi)
All three land within +/- 2 sigma of the Planck 2018 base posterior
centroids. CR037A is the selector; CR037B follows with the parameter-
free CMB shape attempt that pipes these three values through the CR036B
pipeline in place of the Planck-centroid perturbation inputs.
```

## Connection to Future Work

```text
CR037B placeholder
  Parameter-free CMB shape attempt. Replace the Planck-centroid
  (A_s, n_s, tau) inputs in the CR036B pipeline with
  (A_s_SAM, n_s_SAM, tau_SAM). No Run B optimizer. Verdict gates
  inherited from CR035A2 (P1 peak structure, P2 TT chi^2/dof <= 2.0,
  TE/EE polarization-debt threshold 3.0).

CR036A_E5_FIX placeholder (open from CR036 sealing)
  Correct the E5 z_eq_SAM unit bug in CR036.
```

## Stewardship Reference

```text
STEWARDSHIP_DECLARATION.md SHA-256
  d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```
