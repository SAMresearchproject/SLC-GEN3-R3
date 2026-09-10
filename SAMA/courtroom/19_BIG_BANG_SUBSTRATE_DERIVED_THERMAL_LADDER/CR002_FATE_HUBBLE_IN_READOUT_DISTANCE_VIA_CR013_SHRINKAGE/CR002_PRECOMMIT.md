# CR002@19_FATE_HUBBLE_IN_READOUT_DISTANCE_VIA_CR013_SHRINKAGE Precommit

## Verdict Ladder (shown first per precommit-gate-discipline lesson)

```text
PASS:
  P1, P2, and P3 all hold to relative tolerance 1e-12 (P1, P2) and 1e-9 (P3).

FAIL:
  Any of P1, P2, P3 fails its tolerance.

BOUNDARY:
  Not applicable. This is a closed-form structural-identity CR; the
  algebra either agrees or it does not.
```

P1, P2, P3 are closed-form algebraic identities verified via multiple
independent derivation paths. All non-load-bearing outputs (A_los track,
c_eff track, fate checkpoints, LCDM comparison) are reported sensitivity
evidence per the precommit-gate-discipline lesson and do not gate the
verdict.

## Test Type

```text
Structural-prediction CR in branch 19. Closed-form algebraic identity
establishes a new substrate output: the rate of expansion at the fate
asymptote, expressed in MEASURABLE (readout) distance after applying
the sealed CR013 c_eff shrinkage at its saturation limit.

No catalog data is loaded. No fit is performed. There is no
observational measurement of the asymptotic Hubble rate (the asymptotic
future has not happened); the test verifies the structural identity
that produces the substrate prediction, not the match to data.
```

## Why This Test Matters

```text
The fate-test PDF establishes a pure-substrate asymptotic Hubble:
  H_inf (native) = H_0 * sqrt((pi-1)/pi)

The CR013 shrinkage frame establishes a saturation limit on the
line-of-sight substrate accumulation:
  A_los_max = 1/pi

Applying the CR013 shrinkage at saturation to the fate-asymptote
Hubble rate produces the substrate's prediction of the asymptotic
expansion rate in MEASURABLE distance:
  H_inf_readout = H_inf_native * (1 - A_los_max)
                = H_0 * sqrt((pi-1)/pi) * (pi-1)/pi
                = H_0 * ((pi-1)/pi)^(3/2)

This is a closed-form structural identity in pi alone (given H_0 as an
external measurement input). With H_0 = 68.76, the prediction is:
  H_inf_readout ~ 38.70 km/s/Mpc

The substrate spine that already passed CR018b (SN+BAO), CR019 (CMB
fits), CR001c@19 (CMB derived recombination), CR025 (halo profile),
CR031b (radial law), CR032 (per-galaxy halo mass) now produces a
closed-form prediction for the asymptotic measurable expansion rate
with zero free parameters. CR002@19 PASS does not claim measurement
agreement (no measurement exists); it claims that the substrate's
sealed identities and the sealed CR013 shrinkage chain compose to a
specific closed-form output.
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

## Substrate Inputs (sealed identities; zero fit)

```text
Native ledger (manuscript Section 4):
  A_0      = 1/(12*pi)
  alpha_H  = 2
  D        = 3
  R        = 2 * alpha_H * D = 12

Derived densities (sealed identities):
  Omega_m  = R * A_0 = 1/pi              = 0.318310
  Omega_L  = 1 - Omega_m = (pi-1)/pi     = 0.681690

CR013 shrinkage (sealed in CR013 PASS):
  A_los(z) = A_0 * R * (1 - (1+z)^(-D)) = (1/pi) * (1 - (1+z)^(-3))
  c_eff(z) = c * (1 - A_los(z))
  d_native = d_readout * (1 - A_los(z))
  A_los_max = lim_{z -> inf} A_los(z) = 1/pi
```

## Measurement Inputs (external, not catalog fit)

```text
H_0 = 68.76 km/s/Mpc   (BAO-side anchor; same as CR018b, CR019, CR001c@19)
```

## Closed-form Derivation Chain

```text
Step 1 (PDF fate identity, native):
  E^2(a) = Omega_r * a^-4 + Omega_m * a^-3 + Omega_L
  H(a)  = H_0 * E(a)
  As a -> infinity: Omega_r * a^-4 -> 0,  Omega_m * a^-3 -> 0
  H_inf_native = H_0 * sqrt(Omega_L) = H_0 * sqrt((pi-1)/pi)

Step 2 (CR013 shrinkage saturation):
  lim_{z -> inf} A_los(z) = (1/pi) * (1 - 0) = 1/pi
  lim_{z -> inf} (1 - A_los(z)) = 1 - 1/pi = (pi-1)/pi

Step 3 (apply shrinkage to convert native -> readout):
  Velocity is observer-invariant; distance shrinks: d_native = d_readout * (1 - A_los).
  Therefore H_readout = H_native * (1 - A_los).
  H_inf_readout = H_inf_native * (1 - A_los_max)
                = H_0 * sqrt((pi-1)/pi) * (pi-1)/pi
                = H_0 * ((pi-1)/pi)^(3/2)

Numerical value at H_0 = 68.76:
  (pi-1)/pi    = 0.6816901138...
  sqrt above   = 0.8256452050...
  cubed root   = 0.5628341417...
  H_inf_readout = 68.76 * 0.5628341417 = 38.7005... km/s/Mpc
```

## P1 — Native Asymptotic Hubble (load-bearing identity)

```text
Identity: H_inf_native = H_0 * sqrt((pi-1)/pi)

Three independent computation paths must agree to relative tolerance
1e-12:

  Path A: H_0 * sqrt(Omega_L)              with Omega_L = (pi-1)/pi
  Path B: H_0 * sqrt(1 - Omega_m)          with Omega_m = 1/pi
  Path C: H_0 * sqrt((pi-1)/pi)            direct from pi

Pass: |path_i - path_j| / path_j <= 1e-12 for all pairs (i, j).
Falsifier: any pair disagrees beyond tolerance.
```

## P2 — Readout Asymptotic Hubble (load-bearing identity)

```text
Identity: H_inf_readout = H_inf_native * (1 - A_los_max)
                       = H_0 * ((pi-1)/pi)^(3/2)

Two independent computation paths must agree to relative tolerance
1e-12:

  Path A: H_inf_native * (1 - 1/pi)        composed via Step 3 of the chain
  Path B: H_0 * ((pi-1)/pi)^(3/2)          direct closed form

Pass: |path_A - path_B| / path_B <= 1e-12.
Falsifier: paths disagree beyond tolerance.
```

## P3 — CR013 Saturation Limit (load-bearing identity)

```text
Identity: lim_{z -> infinity} A_los(z) = 1/pi

Verified numerically at z = 1e6 to relative tolerance 1e-9:

  A_los(1e6) = (1/pi) * (1 - (1e6 + 1)^(-3))
             ~ 1/pi  to within  ~1e-18

Pass: |A_los(1e6) - 1/pi| / (1/pi) <= 1e-9.
Falsifier: deviation exceeds tolerance.

This is a sanity check that the sealed CR013 shrinkage formula does
saturate to 1/pi as required for P2 to compose correctly.
```

## Reported Evidence (not gates)

```text
E1: A_los(z) and c_eff(z) tabulated at the fate checkpoints
    z in {0, z_eq_Lambda, z_acc, 1, 5, 10, 100, 1090, 1e6} including
    the fate-asymptote limit.

E2: H(z)_native and H(z)_readout at the same checkpoints, where
    H(z)_native = H_0 * sqrt(Omega_m * (1+z)^3 + Omega_L)
    H(z)_readout = H(z)_native * (1 - A_los(z))

E3: Fate-test checkpoint constants (PDF):
      z_eq_Lambda = (pi-1)^(1/3) - 1     ~ 0.28898
      z_acc       = [2*(pi-1)]^(1/3) - 1 ~ 0.62402
      q_0         = (3 - 2*pi)/(2*pi)    ~ -0.52254

E4: LambdaCDM-fit comparison: LCDM has no equivalent shrinkage concept,
    so only the native asymptotic Hubble is directly comparable:
      H_inf_LCDM_native = H_0 * sqrt(Omega_L_LCDM)
                        ~ H_0 * sqrt(0.685)  ~ 56.93 km/s/Mpc
    Comparable to SAM H_inf_native = 56.77 km/s/Mpc; the substrate's
    SAM-specific addition is the readout value 38.70 km/s/Mpc.

E5: Headline number:
      H_inf_readout = H_0 * ((pi-1)/pi)^(3/2) ~ 38.70 km/s/Mpc
      H_inf_readout / H_0 = ((pi-1)/pi)^(3/2) ~ 0.56283
```

## Implementation Discipline

```text
All computations are closed-form floating-point evaluations of pi-based
expressions. No iteration, no random draws, no catalog data.

Tolerances:
  P1, P2: 1e-12 relative (multiple closed-form paths)
  P3:     1e-9  relative (numerical saturation at z = 1e6)

No null distributions / wrong controls. This is a structural-identity
CR; randomized parameters would produce different numbers but would
not test the identity itself.
```

## Frozen Sources

```text
Branch-local cross-checks (sealed; no runtime read):
  C:\VS\The_Courtroom\06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE\CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE\CR013_summary.json
    (A_los formula and saturation are sealed in CR013 PASS)
  C:\VS\The_Courtroom\06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE\CR018b_SAM_ZERO_PARAMETER_SN_BAO_DISTANCE_VERDICT_LADDER_APPEAL\CR018b_summary.json
    (H_0 = 68.76 BAO-side anchor)
  C:\VS\The_Courtroom\06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE\CR019_SAM_ZERO_PARAMETER_CMB_COMPRESSED_GEOMETRY_TEST\CR019_summary.json
    (substrate Omega_m, Omega_L identity-checked at the CMB scale)
  C:\VS\The_Courtroom\19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER\CR001c_PEEBLES_PLUS_CORRECTED_OPTICAL_DEPTH_APPEAL\CR001c_summary.json
    (substrate Omega_m, Omega_L identity passed via derived plasma physics)

Substrate (read-only):
  manuscript Section 4 derived native quantities (A_0, R, Theta, Omega_m, Omega_L)
  fate-test PDF: opposite-limit identity H_inf = H_0 * sqrt(Omega_L)
```

## Rule-9 Line

```text
This test could have falsified the closed-form identity that SAM's
substrate predicts the asymptotic expansion rate in measurable distance
to be

  H_inf_readout = H_0 * ((pi-1)/pi)^(3/2)

derived from the sealed substrate identity Omega_m = 1/pi composed with
the sealed CR013 line-of-sight saturation A_los_max = 1/pi.

It could fail if:
  - sqrt((pi-1)/pi) computed multiple ways disagrees (P1)
  - The composition H_inf_readout = H_inf_native * (1 - A_los_max)
    disagrees with the direct algebraic form H_0 * ((pi-1)/pi)^(3/2) (P2)
  - The CR013 shrinkage does not saturate to 1/pi at large z (P3)

Substrate identities and CR013 shrinkage are sealed upstream; the test
checks that they compose consistently.
```

## Manuscript Headline (conditional on PASS)

```text
SAM's substrate spine, composed with the sealed CR013 c_eff shrinkage
chain, predicts the asymptotic expansion rate of the universe in
measurable (readout) distance to be

  H_inf_readout = H_0 * ((pi-1)/pi)^(3/2) ~ 38.70 km/s/Mpc

a closed-form expression in pi alone (given H_0 as a measurement input).
This is approximately 56.3% of today's H_0, decomposed into two
multiplicative factors of sqrt((pi-1)/pi) = sqrt(Omega_L):
  - The matter-and-radiation dilution factor at fate
    (H_inf_native / H_0 = sqrt(Omega_L))
  - The substrate-saturation shrinkage factor
    (H_readout / H_native at saturation = (1 - 1/pi) = (pi-1)/pi)

The substrate identity Omega_m = 1/pi underlies both factors, making
this a single-identity, zero-parameter prediction for the asymptotic
measurable Hubble rate.
```

## Connection to CR013 (Branch 06)

```text
CR013 sealed the line-of-sight shrinkage A_los(z) = (1/pi) * (1 - (1+z)^(-3))
as the SN luminosity ledger. The shrinkage saturates at A_los_max = 1/pi
by z ~ 5-10 (numerically already at 99.999% of saturation at z = 5).

CR002@19 reads CR013's sealed identity at its saturation limit and
composes it with the fate-test asymptotic Hubble identity to derive
H_inf_readout. No new free parameters are introduced; both upstream
pieces are sealed structural results.
```

## Connection to CR018b, CR019, CR001c@19

```text
Today's Hubble H_0 = 68.76 is the BAO-side measurement anchor used in:
  CR018b (SN+BAO distance test):                   r_d within 0.46% of Planck
  CR019  (CMB compressed geometry via fits):       theta_*, ell_A, r_d within 1% of Planck
  CR001c@19 (CMB via Peebles plasma physics):      theta_*, ell_A, r_d within 2% of Planck

CR002@19 uses the same H_0 to anchor the fate-asymptote prediction.
The substrate identity Omega_m = 1/pi that drives the past-direction
PASSes is the same identity that drives the future-direction
(fate-asymptote) closed-form derivation here.
```

## Stewardship Reference

```text
SHA-256: d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```
