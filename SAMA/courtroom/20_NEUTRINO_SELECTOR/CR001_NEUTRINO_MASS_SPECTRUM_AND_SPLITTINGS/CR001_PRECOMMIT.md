# CR001@20_NEUTRINO_MASS_SPECTRUM_AND_SPLITTINGS Precommit

**Sealed by:** Sean Brady, 2026-06-26.
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`
**Volume I seal:** `ab1e1e5030dc09a171c2699c5c1f3274d1790f4a79315915b3e076ffe2454e5b`

## Verdict Ladder (shown first per discipline)

```text
PASS:
  P1, P2, P3 all hold under canonical substrate inputs.

FAIL:
  Any of P1, P2, P3 fails.

BOUNDARY:
  Reserved for marginal P1 (within 20% of threshold) with explicit
  scope caveat. Not used for reported-evidence misses.
```

P1 is the load-bearing structural prediction (substrate splittings ratio
vs measured). P2 is the load-bearing internal-consistency falsifier
(SAM's Sigma m_nu cannot violate the Planck bound that derives from
SAM's same Omega_m = 1/pi). P3 is a positivity sanity check.

## Test Type

```text
Fresh Courtroom branch test in 20_NEUTRINO_SELECTOR.
External anchors:
  - Larger measured mass-squared splitting Delta m^2_31 = 2.515e-3 eV^2
    (PDG 2024, normal ordering) used as the sole eV scale anchor.
  - PDG ratio Delta m^2_31 / Delta m^2_21 = 33.90 (structural test target).
  - Planck 2018 + BAO Sigma m_nu upper bound 0.12 eV (internal-consistency
    falsifier; anchored at SAM's Omega_m = 1/pi per CR001c@19).

Substrate inputs: Volume I sealed atoms only. Zero new constants.
```

## Question

```text
Do the three smallest sealed substrate scaling ratios {1, sqrt(alpha_H),
alpha_H * D} read as the three neutrino mass eigenstates, with one
external eV anchor set by the measured larger mass-squared splitting,
deliver:
  (i)   a splittings ratio Delta m^2_31 / Delta m^2_21 within 10% of
        the measured 33.90,
  (ii)  a total Sigma m_nu below the Planck 2018 cosmological bound
        of 0.12 eV, and
  (iii) three strictly positive mass eigenvalues?
```

## Substrate Derivation Rule (LOCKED)

```text
The three neutrino mass eigenstates read from substrate as:

  m_1 = base_eV * 1                      (unit substrate scaling)
  m_2 = base_eV * sqrt(alpha_H)          (binary-readout square-root)
  m_3 = base_eV * (alpha_H * D)          (binary times dimension)

with sealed substrate atoms

  alpha_H = 2,   D = 3,   so:
  m_1 / base_eV = 1
  m_2 / base_eV = sqrt(2) = 1.41421356...
  m_3 / base_eV = 6

This produces the closed-form mass-squared splittings ratio

  Delta m^2_31 / Delta m^2_21
    = (m_3^2 - m_1^2) / (m_2^2 - m_1^2)
    = ((alpha_H * D)^2 - 1) / (alpha_H - 1)
    = (36 - 1) / (2 - 1)
    = 35.

The eV anchor is set by the larger measured splitting:

  base_eV = sqrt( Delta m^2_31 / 35 )

with Delta m^2_31 = 2.515e-3 eV^2 from PDG, giving

  base_eV = sqrt(2.515e-3 / 35) = sqrt(7.1857e-5) = 0.008477 eV.

Then:

  m_1 = 0.008477 eV
  m_2 = 0.011989 eV
  m_3 = 0.050864 eV
  Sigma m_nu = 0.008477 * (1 + sqrt(2) + 6) = 0.008477 * 8.41421
             = 0.07133 eV.

Ordering is normal by construction (m_3 > m_2 > m_1).
```

## P1 — Substrate Splittings Ratio Within 10% of Measured (load-bearing)

```text
SAM closed-form prediction:

  Delta m^2_31 / Delta m^2_21 = 35   (substrate; no fit, no anchor)

Measured:

  Delta m^2_31 / Delta m^2_21 = 2.515e-3 / 7.42e-5 = 33.895

Gate:

  | 35 - 33.895 | / 33.895 = 0.0326 = 3.26%
  Pass if relative deviation <= 0.10 (10%).

Pass:      |ratio_SAM - ratio_observed| / ratio_observed <= 0.10.
Falsifier: deviation > 10%.

This is the load-bearing structural prediction. The ratio derives from
substrate atoms (alpha_H, D) only; no eV anchor and no catalog fit
enter. If the substrate's reading (1, sqrt(2), 6) does not match the
observed ratio, the reading is wrong.
```

## P2 — Sigma m_nu Within the Planck Cosmological Bound (load-bearing)

```text
Gate:

  Sigma m_nu = m_1 + m_2 + m_3 < 0.12 eV    (Planck 2018 + BAO, 95% CL)

Pass:      Sigma m_nu < 0.12 eV.
Falsifier: Sigma m_nu >= 0.12 eV.

This is the internal-consistency falsifier. SAM's Omega_m = 1/pi anchors
the Planck CMB+BAO geometry (sealed CR018b@06, CR019@06, CR001c@19).
The Sigma m_nu < 0.12 eV bound derives from that same geometry. A SAM-
derived Sigma m_nu above 0.12 eV would falsify SAM's own substrate
identity chain, not just disagree with an external measurement.
```

## P3 — Three Positive Mass Eigenstates (load-bearing)

```text
Gate:

  m_1 > 0,  m_2 > 0,  m_3 > 0.

Pass:      all three positive.
Falsifier: any one is zero or negative.

This rules out a SAM reading that produces a vanishing eigenstate by
accident. Oscillation experiments require at least two nonzero masses.
The substrate reading (1, sqrt(2), 6) trivially satisfies this; the
gate is included for completeness and to make explicit that the SAM
reading does not collapse one eigenstate to zero.
```

## Reported Evidence (not gates)

```text
E1: Delta m^2_21 from SAM-anchor base
    SAM: Delta m^2_21 = base_eV^2 * (sqrt(alpha_H)^2 - 1)
       = base_eV^2 * (alpha_H - 1)
       = base_eV^2 * 1
       = base_eV^2 = 7.186e-5 eV^2.
    Observed: 7.42e-5 eV^2.
    Deviation: -3.15%.

E2: Individual mass eigenstates
    m_1 = 0.008477 eV
    m_2 = 0.011989 eV
    m_3 = 0.050864 eV.

E3: Ordering = normal (m_3 > m_2 > m_1 by construction).

E4: Lightest mass m_lightest = m_1 = 0.008477 eV
    Cosmological implications for 0-nubb if Dirac vs Majorana
    deferred to future CR.

E5: Effective beta-decay mass
    m_beta = sqrt( sum_i |U_ei|^2 m_i^2 )
    using PDG 2024 mixing:
      sin^2(theta_12) = 0.307,  sin^2(theta_13) = 0.0220,
    so |U_e3|^2 = sin^2(theta_13) = 0.0220,
       |U_e1|^2 = cos^2(theta_13) * cos^2(theta_12) = 0.978 * 0.693 = 0.678,
       |U_e2|^2 = cos^2(theta_13) * sin^2(theta_12) = 0.978 * 0.307 = 0.300.
    m_beta^2 = 0.678 * m_1^2 + 0.300 * m_2^2 + 0.0220 * m_3^2
             = 0.678 * 7.186e-5 + 0.300 * 1.437e-4 + 0.0220 * 2.587e-3
             = 4.87e-5 + 4.31e-5 + 5.69e-5
             = 1.487e-4 eV^2.
    m_beta = sqrt(1.487e-4) = 0.01220 eV.
    KATRIN 2024 bound: m_beta < 0.45 eV. SAM well below (factor ~37).

E6: Comparison to the tighter DESI+CMB Sigma m_nu < ~0.072 eV
    (Planck 2018 + DESI 2024). SAM = 0.0713 eV is just inside this
    tighter bound. Reported for context; the load-bearing falsifier
    in P2 is the looser Planck-only bound at 0.12 eV.
```

## No Wrong Controls Required

```text
Per Sean's directive 2026-06-26, this CR uses loose load-bearing gates
without statistical wrong-controls. The structural prediction (ratio
35 vs measured 33.9) is testable as a single number; the internal-
consistency falsifier (Sigma m_nu < 0.12 eV) is testable as a single
number; the positivity gate is a closed-form fact. Reviewers can apply
their own statistical analyses against the published result; this CR
ships the substrate-derived numbers as they are.
```

## Frozen Sources

```text
External (inline constants in runner):
  PDG 2024 mass splittings:
    Delta m^2_31 = 2.515e-3 eV^2 (used as eV anchor)
    Delta m^2_21 = 7.42e-5 eV^2  (used as comparison target)
  Planck 2018 + BAO Sigma m_nu upper bound: 0.12 eV.
  KATRIN 2024 m_beta bound: 0.45 eV.
  PDG 2024 mixing (sin^2 of three angles) used in E5 only.

Branch-local sealed:
  C:\VS\The_Courtroom\docs\SAM_VOLUME_I_SUBSTRATE.md
    SHA-256: ab1e1e5030dc09a171c2699c5c1f3274d1790f4a79315915b3e076ffe2454e5b
  C:\VS\The_Courtroom\19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER\CR001c_PEEBLES_PLUS_CORRECTED_OPTICAL_DEPTH_APPEAL\CR001c_summary.json
    (Omega_m = 1/pi anchors the Planck bound used in P2)

Substrate (read-only):
  alpha_H = 2, D = 3 (manuscript Vol I Section 3 / CR238)
```

## Rule-9 Line

```text
This test could falsify the claim that the three smallest sealed
substrate scaling ratios {1, sqrt(alpha_H), alpha_H * D} read as the
three neutrino mass eigenstates, with one external eV anchor from the
larger measured splitting, reproduce the measured mass-squared splittings
ratio within 10% and remain consistent with the Planck cosmological
Sigma m_nu bound.

It would falsify the claim if Delta m^2_31 / Delta m^2_21 = 35 is more
than 10% off the measured 33.895; if the resulting Sigma m_nu exceeds
0.12 eV; or if any of the three eigenstates is non-positive.

The structural test P1 is the cleanest because it has no external
calibration: 35 from substrate vs 33.895 from measurement, take it or
leave it.
```

## Manuscript Headline (conditional on PASS)

```text
SAM's substrate spine reads the three neutrino mass eigenstates as the
three smallest sealed substrate scaling ratios

  m_1 : m_2 : m_3 = 1 : sqrt(alpha_H) : (alpha_H * D)
                  = 1 : sqrt(2) : 6.

The substrate-derived mass-squared splittings ratio is

  Delta m^2_31 / Delta m^2_21 = (m_3^2 - m_1^2) / (m_2^2 - m_1^2)
                              = ((alpha_H D)^2 - 1) / (alpha_H - 1)
                              = (36 - 1) / (2 - 1)
                              = 35.

The measured ratio is

  Delta m^2_31 / Delta m^2_21 = 2.515e-3 / 7.42e-5 = 33.90.

SAM is within 3.26% of measurement, derived from one structural reading
with zero catalog-fit parameters and zero free coefficients. The base
eV scale is anchored from the larger measured splitting; this produces

  m_1 ~  8.48 meV
  m_2 ~ 12.0  meV
  m_3 ~ 50.9  meV
  Sigma m_nu ~ 71.3 meV.

The total Sigma m_nu = 71.3 meV is below the Planck 2018 cosmological
bound 0.12 eV (40% below), confirming the internal substrate-identity
consistency: the same Omega_m = 1/pi that anchors SAM's CMB acoustic
geometry (CR001c@19) constrains the neutrino sector through the
cosmological bound, and SAM's neutrino spectrum is consistent with
that constraint.

Standard Model has no derivation for any of these values.
```

## Stewardship

Every artifact in this CR references the stewardship declaration at
`d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`.
