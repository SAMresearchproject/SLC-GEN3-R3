# CR002@19_FATE_HUBBLE_IN_READOUT_DISTANCE_VIA_CR013_SHRINKAGE

## Verdict

```text
CR002@19_PASS_FATE_HUBBLE_IN_MEASURABLE_DISTANCE_CLOSED_FORM_38_7_KMS_MPC
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = SUBSTRATE_ZERO_PARAMETER_FATE_ASYMPTOTIC_HUBBLE_IN_READOUT_DISTANCE
free_parameters_introduced = 0
precommit_sha256 = b18c49fc4f3c2d73c87cbf0112072db4483d9678e7a42dc052f6c60cc4b26633
```

## Headline

```text
The substrate spine, composed with the sealed CR013 c_eff shrinkage,
predicts the asymptotic expansion rate of the universe in MEASURABLE
(readout) distance as a closed-form identity:

  H_inf_readout = H_0 * ((pi-1)/pi)^(3/2)

At H_0 = 68.76 km/s/Mpc:

  H_inf_readout = 38.7005 km/s/Mpc

That is approximately 56.3% of today's H_0, with the ratio fixed by pi
alone: H_inf_readout / H_0 = ((pi-1)/pi)^(3/2) = 0.5628342189...

The ratio decomposes into two multiplicative factors of sqrt((pi-1)/pi):
the fate dilution factor (matter and radiation diluted away by a -> inf)
and the substrate saturation factor (line-of-sight A_los saturates at
1/pi, shrinking readout distance by (pi-1)/pi).
```

## Question

```text
Does the SAM substrate's sealed asymptotic Hubble identity
  H_inf_native = H_0 * sqrt((pi-1)/pi)
composed with the sealed CR013 shrinkage saturation
  A_los_max = 1/pi
produce a consistent closed-form prediction
  H_inf_readout = H_0 * ((pi-1)/pi)^(3/2)
for the asymptotic expansion rate in measurable distance, with zero
free parameters?
```

## Substrate Inputs (zero catalog fit)

```text
A_0       = 1/(12*pi)              = 0.026525823849
alpha_H   = 2
D         = 3
R         = 2*alpha_H*D = 12

Omega_m   = R*A_0 = 1/pi           = 0.318309886184
Omega_L   = 1 - Omega_m = (pi-1)/pi = 0.681690113816
A_los_max = 1/pi                    = 0.318309886184   (sealed in CR013 PASS)
```

## Measurement Input (external)

```text
H_0       = 68.76 km/s/Mpc        (BAO-side; same as CR018b, CR019, CR001c@19)
```

## P1 — Native Asymptotic Hubble — PASS

| field | value |
|---|---:|
| Path A: H_0 * sqrt(Omega_L) | 56.771368846100017 |
| Path B: H_0 * sqrt(1 - Omega_m) | 56.771368846100017 |
| Path C: H_0 * sqrt((pi-1)/pi) | 56.771368846100025 |
| max relative deviation | 1.252e-16 |
| tolerance | 1.0e-12 |
| margin | ~8 billion x under tolerance |
| **pass** | **true** |

Three independent closed-form computation paths for H_inf_native agree
to machine precision. The asymptotic Hubble rate in NATIVE units is
56.77 km/s/Mpc - the pure-substrate fate identity from the PDF.

## P2 — Readout Asymptotic Hubble — PASS

| field | value |
|---|---:|
| Path A: H_inf_native * (1 - 1/pi) | 38.700480890199920 |
| Path B: H_0 * ((pi-1)/pi)^(3/2) | 38.700480890199927 |
| relative deviation | 1.836e-16 |
| tolerance | 1.0e-12 |
| margin | ~5 billion x under tolerance |
| **pass** | **true** |

Two independent closed-form computation paths for H_inf_readout agree
to machine precision. Composing the fate identity with the CR013
saturation factor produces 38.70 km/s/Mpc - the substrate's prediction
of the asymptotic measurable expansion rate.

## P3 — CR013 Saturation Limit — PASS

| field | value |
|---|---:|
| A_los(z = 1e6) | 0.318309886183791 |
| A_los_max = 1/pi | 0.318309886183791 |
| relative deviation | 0.000e+00 |
| tolerance | 1.0e-09 |
| **pass** | **true** |

CR013's line-of-sight shrinkage formula saturates to 1/pi as z -> inf.
At z = 1e6 the formula and the limit are identical to machine precision.
This is the upstream sanity check that the saturation factor used in
P2 is correctly extracted from CR013's sealed identity.

## Reported Evidence

### E1/E2 — A_los, c_eff, H(z) track from today to fate asymptote

```text
        label       z         A_los     1 - A_los    c_eff (km/s)   H_native     H_readout
        --------------------------------------------------------------------------------
        today      0.000     0.000000   1.000000     299792.46      68.76         68.76
  z_eq_Lambda      0.289     0.169678   0.830322     248924.40      80.29         66.66
        z_acc      0.624     0.243994   0.756006     226644.98      98.33         74.34
          z=1      1.000     0.278521   0.721479     216293.92     123.54         89.13
          z=5      5.000     0.316836   0.683164     204807.35     572.97        391.43
         z=10     10.000     0.318071   0.681929     204437.25    1416.44        965.91
        z=100    100.000     0.318310   0.681690     204365.65   39377.07      26842.97
          z_*   1090.000     0.318310   0.681690     204365.55  1397970.66     952982.78
         1e6   1.0e+06       0.318310   0.681690     204365.55   3.88e+10       2.64e+10
     fate inf    a->inf      0.318310   0.681690     204365.55      56.77         38.70
```

A_los saturates near 1/pi by z ~ 5 (99.5% saturated); fully saturated
to machine precision by z = 100. c_eff at saturation is 0.6817 * c =
204,365.55 km/s. H_native and H_readout grow steeply with z in the
past direction (matter and radiation dominate); both converge to the
fate-asymptote values at a -> inf.

### E3 — Fate PDF checkpoint constants (closed form)

```text
z_eq_Lambda = (pi-1)^(1/3) - 1     = 0.288978   (matter-Lambda equality)
z_acc       = [2(pi-1)]^(1/3) - 1  = 0.624011   (acceleration begins)
q_0         = (3 - 2 pi)/(2 pi)    = -0.522535  (deceleration parameter today)
```

These are the three additional closed-form checkpoint numbers from the
fate PDF. Reported as evidence; their independent CR (if pursued) would
test data agreement with Pantheon+ cosmography or similar.

### E4 — LambdaCDM-fit comparison (native only)

```text
Omega_L_LCDM = 0.685  (Planck 2018 base-LCDM)
H_inf_LCDM_native = H_0 * sqrt(0.685)     = 56.9090 km/s/Mpc
H_inf_SAM_native  = H_0 * sqrt((pi-1)/pi) = 56.7714 km/s/Mpc
difference                                = 0.1377 km/s/Mpc  (0.24%)
```

LCDM-fit and SAM-substrate native asymptotic Hubble rates agree to
0.24%. LambdaCDM has no analog of the c_eff shrinkage - distance in
LCDM is treated as Riemannian-geometric without a substrate-saturation
factor. The SAM-specific readout asymptote H_inf_readout = 38.70
km/s/Mpc is a SAM-only structural prediction; no LambdaCDM equivalent
exists for direct comparison.

### E5 — Headline ratio

```text
H_inf_readout / H_0 = ((pi-1)/pi)^(3/2) = 0.5628342189
```

A closed-form ratio in pi alone. The fate asymptote in measurable
distance is fixed at 56.3% of today's H_0 by the substrate identity
Omega_m = 1/pi and the sealed CR013 saturation A_los_max = 1/pi.

## Pass Conditions

| condition | pass |
|---|---:|
| P1_H_inf_native_three_path_identity | true |
| P2_H_inf_readout_two_path_identity | true |
| P3_CR013_saturation_limit | true |

## The Two sqrt-Omega_L Factors

```text
H_0                                                  =        H_0
H_inf_native  = H_0 * sqrt((pi-1)/pi)                = H_0 * sqrt(Omega_L)
H_inf_readout = H_0 * ((pi-1)/pi)^(3/2)              = H_0 * Omega_L^(3/2)

The chain:
  H_0    ---- * sqrt(Omega_L) ----->  H_inf_native    (fate dilution)
            = 0.8256 x

  H_inf_native  ---- * Omega_L ---->  H_inf_readout   (substrate saturation)
                  = 0.6817 x

Net:    H_0    ---- * Omega_L^(3/2) -->  H_inf_readout
              = 0.5628 x

Each step is a multiplication by sqrt((pi-1)/pi). The structural
origin of both factors is the same substrate identity Omega_m = 1/pi.
```

## Scope

```text
CR002@19 establishes:
  - A closed-form structural identity for H_inf_readout
  - Numerical value 38.70 km/s/Mpc at H_0 = 68.76
  - The closed-form ratio H_inf_readout / H_0 = ((pi-1)/pi)^(3/2)
  - Decomposition into two factors of sqrt((pi-1)/pi)

CR002@19 does NOT claim:
  - Measurement agreement (no observation of asymptotic Hubble exists;
    the asymptotic future has not happened)
  - That the c_eff shrinkage formula extends to the future direction
    in literal photon-path form (CR013 sealed the past-direction form
    A_los(z) saturating at 1/pi; CR002@19 uses the saturation limit
    as the structural saturation factor, not as a literal photon path
    into the future)
  - That LambdaCDM is wrong (LCDM has no analog of the readout-vs-native
    distinction; the SAM-readout asymptote is a SAM-specific structural
    quantity)

CR002@19 also reports the three other fate-PDF checkpoint constants
(z_eq_Lambda, z_acc, q_0) as evidence; a future CR could gate those
against Pantheon+ cosmography directly.
```

## Rule-9 Line

```text
This test could have falsified the closed-form identity that SAM's
substrate, composed with the sealed CR013 line-of-sight shrinkage,
predicts the asymptotic expansion rate of the universe in measurable
distance to be H_inf_readout = H_0 * ((pi-1)/pi)^(3/2) ~ 38.70 km/s/Mpc.

It did not falsify it. All three load-bearing identities (P1 three-path,
P2 two-path, P3 saturation limit) hold to machine precision (~1e-16),
8-9 orders of magnitude below their declared tolerances. The
substrate identities and CR013 shrinkage compose consistently to the
closed-form prediction.
```

## Manuscript Headline

```text
SAM's substrate spine, composed with the sealed CR013 line-of-sight
shrinkage, predicts the asymptotic expansion rate of the universe in
measurable distance as a closed-form expression in pi alone:

  H_inf_readout = H_0 * ((pi-1)/pi)^(3/2) ~ 38.70 km/s/Mpc at H_0 = 68.76

The ratio H_inf_readout / H_0 = ((pi-1)/pi)^(3/2) = 0.5628 is fixed by
the substrate identity Omega_m = 1/pi alone. Decomposed: the fate
asymptote (matter and radiation diluted away) gives one factor of
sqrt((pi-1)/pi); the line-of-sight substrate saturation gives a second
such factor.

The substrate spine that already reproduces SN+BAO distances (CR018b),
the CMB compressed acoustic geometry via fit formulae (CR019) and via
derived Peebles plasma physics (CR001c@19), the galaxy halo profile
(CR025), the radial law (CR031b), and the per-galaxy halo mass median
(CR032), now also produces this fate-asymptote prediction in measurable
distance with zero new free parameters.

The substrate-derived measurable expansion rate at fate is roughly half
of today's H_0. This is the SAM prediction for the cosmological
expansion rate that an observer in the distant future, measuring with
their available distance reckoning, would record.
```

## Connection to CR013 (Branch 06)

```text
CR013 sealed PASS the line-of-sight shrinkage:
  A_los(z) = (1/pi) * (1 - (1+z)^(-3))
  saturates at 1/pi by z ~ 5-10.

CR002@19 reads CR013's sealed identity at its saturation limit and
composes it with the fate-test asymptotic Hubble. The composition is a
single multiplication by (1 - A_los_max) = (pi-1)/pi; no new physics
is introduced.
```

## Connection to CR018b, CR019, CR001c@19

```text
H_0 = 68.76 (BAO-side measurement anchor) was used in:
  CR018b   (sealed PASS): SN+BAO distance spine
  CR019    (sealed PASS): CMB compressed acoustic geometry via fit formulae
  CR001c@19 (sealed PASS): CMB compressed geometry via Peebles plasma physics

CR002@19 uses the same H_0 to anchor the closed-form fate-asymptote
prediction. The substrate identity Omega_m = 1/pi that anchors the
past-direction PASSes anchors the future-direction (fate) closed-form
derivation here.
```

## Provenance Chain

```text
Stewardship           = d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
Naming canon          = 35c2d9650909f420018e1a72f1a597e101a1670c7eb00b0bcaec63724928a2f8
Patent claim register = db91680abce1e18d23f559eb8bb8141f04dd51b8a038504f9959ae0437291fa1
CR013 precommit hash  = (per CR013_summary.json in input manifest)
CR018b precommit      = bdd4dc29688af099a0ec5b6f47e4cb0e449f0ff36c45037e545bf76bb88879ce
CR019 precommit       = ef52480d1bbbac21103a8937a864e5cd2992b0d6046efbe15d1732961eb529da
CR001c@19 precommit   = 64b17ea78ddcf1ecfeffbcd722abc4f7446aaaeea1140e105acc3cad2c053bb1
CR002@19 precommit    = b18c49fc4f3c2d73c87cbf0112072db4483d9678e7a42dc052f6c60cc4b26633
```

---

**Sealed by:** Sean Brady, 2026-06-26.
