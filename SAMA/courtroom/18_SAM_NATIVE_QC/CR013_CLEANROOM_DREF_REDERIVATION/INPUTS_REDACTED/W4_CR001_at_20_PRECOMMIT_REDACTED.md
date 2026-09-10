# CR001@20 — Neutrino Mass Spectrum and Splittings (REDACTED for CR013 DERIVER context)

**Sealed by:** Sean Brady, 2026-06-26.
**Volume I seal:** `ab1e1e5030dc09a171c2699c5c1f3274d1790f4a79315915b3e076ffe2454e5b`

---

## Test Type

```text
Fresh Courtroom branch test in 20_NEUTRINO_SELECTOR.
External anchors:
  - Larger measured mass-squared splitting Delta m^2_31 = 2.515e-3 eV^2
    (PDG 2024, normal ordering) used as the sole eV scale anchor.
  - PDG ratio Delta m^2_31 / Delta m^2_21 = 33.90 (structural test target).
  - Planck 2018 + BAO Sigma m_nu upper bound 0.12 eV.

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

## Frozen Sources

```text
External (inline constants in runner):
  PDG 2024 mass splittings:
    Delta m^2_31 = 2.515e-3 eV^2 (used as eV anchor)
    Delta m^2_21 = 7.42e-5 eV^2  (used as comparison target)
  Planck 2018 + BAO Sigma m_nu upper bound: 0.12 eV.
  KATRIN 2024 m_beta bound: 0.45 eV.

Substrate (read-only):
  alpha_H = 2, D = 3 (manuscript Vol I Section 3 / CR238)
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
```
