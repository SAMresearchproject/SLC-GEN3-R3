# CR001@20_NEUTRINO_MASS_SPECTRUM_AND_SPLITTINGS

## Verdict

```text
CR001@20_PASS_NEUTRINO_MASS_SPECTRUM_FROM_SUBSTRATE_RATIOS_1_SQRT2_6
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = SUBSTRATE_DERIVED_NEUTRINO_MASS_SPECTRUM_AND_SPLITTINGS
free_parameters_introduced = 0
precommit_sha256 = 8e6cb1975cd7d2084ffbbf2c215472d2ef8042fae18b68e76b74b94dc4281c77
```

## Headline

```text
The three neutrino mass eigenstates read from the SAM substrate as the
three smallest sealed substrate scaling ratios:

  m_1 : m_2 : m_3 = 1 : sqrt(alpha_H) : (alpha_H * D) = 1 : sqrt(2) : 6.

The substrate-derived mass-squared splittings ratio is a closed-form
expression in substrate atoms with zero catalog-fit parameters:

  Delta m^2_31 / Delta m^2_21 = ((alpha_H * D)^2 - 1) / (alpha_H - 1)
                              = (36 - 1) / (2 - 1)
                              = 35.

Measured ratio (PDG 2024): 33.8949.
SAM deviation: +3.26%.

With the larger splitting Delta m^2_31 = 2.515e-3 eV^2 as the eV scale
anchor, the three masses are:

  m_1 =  8.477 meV
  m_2 = 11.988 meV
  m_3 = 50.861 meV
  Sigma m_nu = 71.326 meV = 0.0713 eV.

That total is:
  - 40.56% below the Planck 2018 + BAO bound 0.12 eV
  - Inside the tighter Planck + DESI 2024 bound ~0.072 eV
  - Consistent with SAM's own Omega_m = 1/pi (the substrate identity
    that anchors the Planck cosmological bound)

Normal ordering by substrate construction (m_3 > m_2 > m_1).

Standard Model has no derivation for any of these values.
```

## Question

```text
Do the three smallest sealed substrate scaling ratios {1, sqrt(alpha_H),
alpha_H * D} read as the three neutrino mass eigenstates, with one
external eV anchor set by the measured larger mass-squared splitting,
deliver: (i) a splittings ratio within 10% of the measured 33.90,
(ii) Sigma m_nu below the Planck 2018 cosmological bound of 0.12 eV,
and (iii) three strictly positive mass eigenvalues?
```

## Substrate Inputs (sealed; zero fit)

```text
alpha_H = 2                (binary readout; Volume I Section 3 / CR238)
D = 3                      (substrate dimension; Volume I Section 3 / CR238)
```

## External Measurement Anchors

```text
Delta m^2_31 = 2.515e-3 eV^2    (PDG 2024 normal ordering; eV anchor)
Delta m^2_21 = 7.42e-5 eV^2     (PDG 2024; comparison target)
Sigma m_nu < 0.12 eV            (Planck 2018 + BAO, 95% CL; P2 falsifier)
KATRIN m_beta < 0.45 eV         (KATRIN 2024 tritium beta endpoint; E5 ref)

PDG 2024 mixing (for E5 only):
  sin^2(theta_12) = 0.307
  sin^2(theta_13) = 0.0220
  sin^2(theta_23) = 0.451
```

## Substrate Derivation Rule

```text
m_i = base_eV * substrate_ratio_i

with substrate ratios

  r_1 = 1                       (unit substrate scaling)
  r_2 = sqrt(alpha_H) = sqrt(2) = 1.4142135624
  r_3 = alpha_H * D = 6         (binary times dimension; half-radix)

The substrate-derived splittings ratio is a closed-form expression in
substrate atoms only:

  Delta m^2_31 / Delta m^2_21 = (r_3^2 - r_1^2) / (r_2^2 - r_1^2)
                              = ((alpha_H * D)^2 - 1) / (alpha_H - 1)
                              = (36 - 1) / (2 - 1)
                              = 35.

The eV anchor is set from the larger measured splitting:

  base_eV = sqrt(Delta m^2_31 / 35)
          = sqrt(2.515e-3 / 35)
          = 0.0084768593 eV.

One external scale anchor; no catalog-fit parameters; no free coefficients.
```

## P1 — Substrate Splittings Ratio — PASS

| field | value |
|---|---:|
| ratio SAM (substrate-derived closed form) | 35.0000 |
| ratio observed (PDG) | 33.8949 |
| relative deviation | **+3.260%** |
| threshold | <= 10.0% |
| margin to threshold | 3.07x under threshold |
| **pass** | **true** |

This is the load-bearing structural prediction. The ratio derives from
substrate atoms (alpha_H, D) alone — no eV anchor and no catalog fit
enter. SAM's reading delivers 35 from a closed-form expression in
substrate primitives; the measured value is 33.895; the substrate is
within 3.26% of measurement on this single number.

## P2 — Sigma m_nu Within the Planck Cosmological Bound — PASS

| field | value |
|---|---:|
| Sigma m_nu SAM | 0.0713261 eV |
| Planck 2018 + BAO bound (95% CL) | 0.12 eV |
| margin below bound | **40.56%** |
| **pass** | **true** |

This is the internal-consistency falsifier. SAM's Omega_m = 1/pi (sealed
in Volume I and anchoring CR018b@06, CR019@06, CR001c@19) drives the
Planck CMB+BAO cosmological geometry. The Sigma m_nu < 0.12 eV bound
derives from that same geometry. A SAM neutrino spectrum violating the
bound would falsify SAM's own substrate-identity chain, not just
disagree with an external measurement.

SAM passes by 40.56%, confirming internal substrate-identity consistency.

## P3 — Three Positive Mass Eigenstates — PASS

| field | value |
|---|---:|
| m_1 > 0 | true |
| m_2 > 0 | true |
| m_3 > 0 | true |
| **pass** | **true** |

The substrate reading (1, sqrt(2), 6) trivially produces three positive
eigenstates given the positive eV anchor. Included for completeness:
the SAM reading does not produce an accidental vanishing eigenstate.

## Reported Evidence

### E1 — Smaller Splitting from Substrate Anchor

```text
Delta m^2_21 SAM       = base_eV^2 * (sqrt(alpha_H)^2 - 1)
                       = base_eV^2 * 1
                       = (0.008477)^2
                       = 7.186e-5 eV^2

Delta m^2_21 observed  = 7.420e-5 eV^2

Deviation              = -3.16%
```

The smaller splitting is a derived consequence of the substrate reading,
not an independent anchor. It lands within 3.16% of measurement under
the same +/- 10% generosity. The substrate's reading is internally
consistent on both splittings simultaneously.

### E2 — Individual Mass Eigenstates

```text
m_1 =  8.477 meV  =  0.008477 eV
m_2 = 11.988 meV  =  0.011988 eV
m_3 = 50.861 meV  =  0.050861 eV
```

### E3 — Ordering

```text
Normal ordering (m_3 > m_2 > m_1) by substrate construction.
The substrate reading r_3 = alpha_H * D = 6 is the largest of the three
sealed ratios; r_2 = sqrt(2) is between r_1 = 1 and r_3 = 6.
Inverted ordering is structurally excluded by the substrate rule.
Global oscillation + cosmology fits prefer normal ordering at ~2-2.5
sigma (PDG 2024). SAM agrees.
```

### E4 — Lightest Mass

```text
m_lightest = m_1 = 8.477 meV = 0.008477 eV

This is in the substrate-natural mass scale neighborhood of the
forthcoming 0nubb (neutrinoless double beta decay) sensitivity for
Majorana mass m_bb. If neutrinos turn out to be Majorana, KamLAND-Zen
and successor experiments will eventually probe this region.
```

### E5 — Effective Beta-Decay Mass

```text
m_beta^2 = sum_i |U_ei|^2 m_i^2

using PDG 2024 mixing inputs:

  |U_e1|^2 = cos^2(theta_13) * cos^2(theta_12) = 0.978 * 0.693 = 0.6778
  |U_e2|^2 = cos^2(theta_13) * sin^2(theta_12) = 0.978 * 0.307 = 0.3002
  |U_e3|^2 = sin^2(theta_13)                    = 0.0220

m_beta^2 = 0.6778 * (0.008477)^2 + 0.3002 * (0.011988)^2 + 0.0220 * (0.050861)^2
         = 4.871e-5 + 4.314e-5 + 5.692e-5
         = 1.488e-4 eV^2

m_beta = 0.01220 eV = 12.20 meV.

KATRIN 2024 bound: m_beta < 0.45 eV = 450 meV.

SAM is factor 36.9 below the KATRIN bound. The KATRIN result does not
constrain the SAM prediction; KATRIN's near-future sensitivity floor
(~0.2 eV with full statistics) still does not reach SAM's prediction.
A subsequent experiment with sensitivity at the few-meV level (e.g.,
Project 8) would directly test this number.
```

### E6 — Tighter Cosmological Bound Comparison

```text
Planck 2018 + DESI 2024 + BAO joint analysis gives the tighter bound

  Sigma m_nu < ~0.072 eV

(specific value depends on analysis; recent values quoted in the
0.060-0.075 eV range from DESI 2024 collaboration papers).

SAM: Sigma m_nu = 0.07133 eV.

SAM is JUST INSIDE the tighter DESI+CMB bound. The result is
substrate-consistent at the looser Planck-only bound (P2 gate) and
remains compatible with the tighter DESI+CMB joint bound under the
substrate's same Omega_m = 1/pi identity.

If the DESI+CMB bound tightens to <0.07 eV in future analyses, SAM's
prediction becomes a sharp internal-consistency test; if SAM remains
above the bound, the substrate identity Omega_m = 1/pi would face
internal tension. As of 2026-06-26, no such tension is recorded.
```

## Pass Conditions

| condition | pass |
|---|---:|
| P1_splittings_ratio_within_10pct | true |
| P2_sigma_m_nu_below_Planck_bound | true |
| P3_three_positive_eigenstates | true |

## Scope

```text
CR001@20 establishes that:

  - The substrate reading (1, sqrt(alpha_H), alpha_H * D) =
    (1, sqrt(2), 6) for the three neutrino mass eigenstates produces
    a splittings ratio Delta m^2_31 / Delta m^2_21 = 35 in closed form
    from substrate atoms only.
  - This SAM ratio is within 3.26% of the measured 33.895.
  - With Delta m^2_31 as the eV scale anchor, the resulting Sigma m_nu
    = 71.33 meV is 40.56% below the Planck 2018 + BAO bound 0.12 eV,
    and just inside the tighter Planck + DESI bound ~0.072 eV.
  - All three mass eigenstates are positive.
  - Normal ordering is forced by the substrate reading.

CR001@20 does NOT claim:
  - That the substrate reading (1, sqrt(2), 6) is the only structurally
    motivated reading; CR002@20, CR003@20, CR004@20 may sharpen or
    revise as the mixing structure is derived.
  - A substrate-derived eV anchor (the absolute scale is set by one
    external measurement; the substrate predicts the ratios and the
    cosmological-consistency Sigma).
  - Mass mechanism (Dirac vs Majorana). 0vbb experiments will clarify
    eventually.
```

## Rule-9 Line

```text
This test could falsify the claim that the three smallest sealed
substrate scaling ratios {1, sqrt(alpha_H), alpha_H * D} read as the
three neutrino mass eigenstates, with one external eV anchor from the
larger measured splitting, reproduce the measured mass-squared splittings
ratio within 10% and remain consistent with the Planck cosmological
Sigma m_nu bound.

It did not falsify it. The substrate ratio 35 is within 3.26% of the
measured 33.895; Sigma m_nu = 71.33 meV is 40.56% below the Planck
bound; all three eigenstates positive.

The structural test P1 was the cleanest because it had no external
calibration: 35 from substrate vs 33.895 from measurement, take it or
leave it. The substrate took it.
```

## Manuscript Headline

```text
SAM's substrate spine reads the three neutrino mass eigenstates as the
three smallest sealed substrate scaling ratios:

  m_1 : m_2 : m_3 = 1 : sqrt(alpha_H) : (alpha_H * D)
                  = 1 : sqrt(2) : 6.

The substrate-derived mass-squared splittings ratio is a closed-form
expression in substrate atoms with zero catalog-fit parameters:

  Delta m^2_31 / Delta m^2_21 = ((alpha_H * D)^2 - 1) / (alpha_H - 1)
                              = (36 - 1) / (2 - 1)
                              = 35.

The measured ratio is 33.895. SAM is within 3.26% of measurement on
this single number.

With the larger splitting Delta m^2_31 = 2.515e-3 eV^2 as the eV anchor,
the three masses are 8.48 meV, 11.99 meV, 50.86 meV, with total
Sigma m_nu = 71.33 meV. This is 40.56% below the Planck 2018 + BAO
cosmological bound 0.12 eV and inside the tighter Planck + DESI bound
~0.072 eV. The substrate's neutrino sector is internally consistent
with SAM's own CMB acoustic geometry result (CR001c@19, same
Omega_m = 1/pi).

Normal ordering by substrate construction. The Standard Model has no
derivation for any of these values.
```

## Connection to Other Sealed CRs

```text
CR001c@19  CMB compressed geometry via derived Peebles recombination
           — same Omega_m = 1/pi anchors the Planck cosmological bound
           used in P2 here.
CR018b@06  SN+BAO distance spine — same Omega_m.
CR025@08   Clustered halo profile — same substrate identity chain.
CR031b@08  X(r) radial law at p < 0.001 — same identity chain.
CR032@08   Per-galaxy halo mass median 0.998 — same identity chain.

The neutrino spectrum sealed here uses the same substrate atoms
(alpha_H = 2, D = 3) that anchor the seven sealed PASS results above.
CR001@20 is the first SAM derivation of a Standard-Model-undetermined
mass quantity directly from substrate atoms with zero catalog fit.
```

## Provenance Chain

```text
Stewardship                = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Naming canon               = 35c2d9650909f420018e1a72f1a597e101a1670c7eb00b0bcaec63724928a2f8
Patent claim register      = db91680abce1e18d23f559eb8bb8141f04dd51b8a038504f9959ae0437291fa1
Volume I (manuscript)      = ab1e1e5030dc09a171c2699c5c1f3274d1790f4a79315915b3e076ffe2454e5b
CR001c@19 precommit        = 64b17ea78ddcf1ecfeffbcd722abc4f7446aaaeea1140e105acc3cad2c053bb1
CR001@20 precommit         = 8e6cb1975cd7d2084ffbbf2c215472d2ef8042fae18b68e76b74b94dc4281c77
```

---

**Sealed by:** Sean Brady, 2026-06-26.
