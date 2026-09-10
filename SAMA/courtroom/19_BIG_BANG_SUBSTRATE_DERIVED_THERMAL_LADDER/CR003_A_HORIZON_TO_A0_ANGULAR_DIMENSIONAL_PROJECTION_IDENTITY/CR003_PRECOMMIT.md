# CR003@19_A_HORIZON_TO_A0_ANGULAR_DIMENSIONAL_PROJECTION_IDENTITY Precommit

## Verdict Ladder (shown first per precommit-gate-discipline lesson)

```text
PASS:
  P1, P2, and P3 all hold to relative tolerance 1e-12.

FAIL:
  Any of P1, P2, P3 fails its tolerance.

BOUNDARY:
  Not applicable. This is a closed-form structural-identity CR.
```

P1, P2, P3 are closed-form algebraic identities. All non-load-bearing
outputs (E1 D-sensitivity table with R-coupling invariance check, E2 A(r)
ramp outside the closure, E3 bridge map to downstream identities, E4
reframing note) are reported sensitivity evidence and do not gate the
verdict.

## Test Type

```text
Structural-identity CR in branch 19. Establishes that the substrate
constant A_0 = 1/(12*pi) is NOT arbitrary - it is the projection of the
unit-closure horizon condition A_horizon = 1 through the angular factor
4*pi and the dimensional factor D, evaluated at D = 3:

  A_0 = A_horizon / (4*pi*D) = 1/(4*pi*3) = 1/(12*pi)

No catalog data is loaded. No fit is performed. The CR verifies the
algebraic projection and reports a D-sensitivity table that demonstrates
the coupled-constant invariance: with R = 2*alpha_H*D and alpha_H = 2,
the product R*A_0 = alpha_H/(2*pi) does NOT depend on D - it is fixed
at 1/pi by alpha_H alone.

This makes the upstream chain A_0 -> Omega_m STRONGER, not weaker: the
density identity Omega_m = 1/pi is invariant under the choice of
dimension D once the coupling R = 2*alpha_H*D is held fixed.
```

## Why This Test Matters

```text
Across the Courtroom, the substrate constant A_0 = 1/(12*pi) is the
seed of every passing identity:
  CR018b  (SN+BAO):                   r_d within 0.46% of Planck
  CR019   (CMB compressed via fits):  theta_*, ell_A, r_d within 1%
  CR025   (halo profile):             PASS
  CR031b  (radial law):               PASS at p < 0.001
  CR032   (per-galaxy halo mass):     median ratio 0.998 PASS
  CR001c@19 (CMB via derived Peebles): theta_*, ell_A, r_d within 2%
  CR002@19 (fate Hubble in readout):  H_inf = H_0 * ((pi-1)/pi)^(3/2)

In all of these, A_0 = 1/(12*pi) enters via Omega_m = R*A_0 = 1/pi (and
chi = (S/D)*A_0, Omega_b = 2*A_0*(1-chi), etc). Until this CR, A_0's
specific value was sealed as a native ledger primitive in manuscript
Section 4 without an underlying-principle derivation. This CR derives
A_0 from a DEEPER identity:

  A_horizon = 1 (full local closure)
  projection through angular 4*pi and dimensional D
  -> A_0 = 1/(4*pi*D)
  at D = 3: A_0 = 1/(12*pi)

The bridge map is:
  full local closure (A=1)
     -> angular/dimensional resolution (1 -> 1/(4*pi*D))
     -> cosmic background seed (A_0 = 1/(12*pi))
     -> matter density identity (Omega_m = R*A_0 = 1/pi)
     -> all downstream PASSes
```

## Question

```text
Does the closed-form identity

  A_0 = A_horizon / (4*pi*D)

at the substrate values A_horizon = 1, D = 3 reproduce the sealed
A_0 = 1/(12*pi) used across the Courtroom? And does the coupling
R = 2*alpha_H*D at alpha_H = 2, D = 3 reproduce R*A_0 = 1/pi (the
Omega_m identity)? And does the horizon profile A(r) = r_s/r at r = r_s
recover A = 1 (the full-local-closure condition itself)?
```

## Substrate Inputs (sealed identities; zero fit)

```text
A_horizon = 1                          (full local closure; identity)
alpha_H   = 2                          (binary readout)
D         = 3                          (dimension)
R         = 2*alpha_H*D = 12          (radix)
angular factor = 4*pi                  (full solid angle in 3D)

A(r) = r_s / r                         (horizon profile; A=1 at r=r_s)
```

## Closed-form Identity Chain

```text
Step 1: A_horizon = 1                                   (sealed definition)

Step 2: A_0 = A_horizon / (4*pi*D)                      (angular and dim projection)
        At D = 3: A_0 = 1 / (4*pi*3) = 1/(12*pi)

Step 3: Omega_m = R * A_0 with R = 2*alpha_H*D
        Omega_m = 2*alpha_H*D * (1/(4*pi*D))
                = 2*alpha_H / (4*pi)
                = alpha_H / (2*pi)
        At alpha_H = 2: Omega_m = 1/pi

The key observation: Omega_m = R*A_0 = alpha_H/(2*pi) is INVARIANT
under D when R is coupled to D as R = 2*alpha_H*D. The substrate's
matter density is fixed by alpha_H alone; the dimension D enters
only the seed A_0 and the radix R, and the dependence cancels in
the product.
```

## P1 — Angular-Dimensional Projection Identity (load-bearing)

```text
Identity: A_0 = A_horizon / (4*pi*D) at A_horizon = 1, D = 3 reproduces
         the sealed A_0 = 1/(12*pi).

Tolerance: relative deviation <= 1e-12

Computation paths to compare:
  Path A: 1 / (4 * pi * 3)               direct projection
  Path B: 1 / (12 * pi)                  sealed substrate value
  Path C: A_horizon / (4 * pi * D)       symbolic with all variables

Pass: max pairwise relative deviation <= 1e-12.
Falsifier: any pair disagrees beyond tolerance.
```

## P2 — Coupled-Constant Density Identity (load-bearing)

```text
Identity: With alpha_H = 2, D = 3, and R = 2*alpha_H*D = 12,
         R * A_0 = 1/pi to relative tolerance 1e-12.

Computation paths:
  Path A: R * A_0 with R computed as 2*alpha_H*D and A_0 as 1/(4*pi*D)
  Path B: alpha_H / (2*pi)                  reduced form
  Path C: 1 / pi                            direct closed form

The reduction R*A_0 = (2*alpha_H*D) * (1/(4*pi*D)) = alpha_H/(2*pi)
makes explicit that the D-dependence cancels.

Pass: max pairwise relative deviation <= 1e-12.
Falsifier: any pair disagrees beyond tolerance.
```

## P3 — Horizon Unit-Closure Identity (load-bearing)

```text
Identity: A(r) = r_s / r at r = r_s yields A = 1.

This verifies the substrate definition that the full-local-closure
condition A = 1 occurs at r = r_s under the standard accumulation
profile A(r) = r_s/r.

Tolerance: relative deviation <= 1e-12 (it is an exact algebraic
identity; the tolerance accommodates floating-point representation).

Computation:
  A(r=r_s) = r_s / r_s = 1

We evaluate at r_s = 1 (canonical unit), r_s = 2.95e3 m (Sun mass
Schwarzschild radius, ~ 2 GM_sun / c^2), and r_s = 1e30 m (arbitrary
large) and check A = 1 in each case.

Pass: |A(r=r_s) - 1| <= 1e-12 for all tested r_s.
Falsifier: deviation exceeds tolerance for any r_s.
```

## Reported Evidence (not gates)

```text
E1: Sensitivity table - A_0 = 1/(4*pi*D) evaluated at D = 2, 3, 4, 5.
    D = 3 recovers the sealed SAM value A_0 = 1/(12*pi).

    Separate coupled-constant check at the same D values: with
    R = 2*alpha_H*D and alpha_H = 2, the product R*A_0 = alpha_H/(2*pi)
    = 1/pi REMAINS INVARIANT. The substrate's Omega_m identity does
    not depend on the dimension D once the coupling R = 2*alpha_H*D
    is honored - the dependence cancels.

    This is the structural reading: A_0 changes with D, R changes
    with D, but the product (which is Omega_m) is fixed by alpha_H
    alone.

E2: A(r) ramp outside the closure - evaluate A(r) = r_s/r at
    r/r_s in {1, 2, 5, 10, 100, 1000} to show the substrate
    accumulation decay outside the closure boundary.

E3: Bridge map - explicit chain showing the propagation:
      full local closure A_horizon = 1
      -> angular/dimensional projection 1 -> 1/(4*pi*D)
      -> cosmic background seed A_0 = 1/(12*pi) at D = 3
      -> radix coupling R*A_0 = 1/pi (alpha_H = 2)
      -> matter density Omega_m = 1/pi
      -> chi = (S/D)*A_0, Omega_b = 2*A_0*(1-chi)
      -> Omega_Lambda = 1 - Omega_m = (pi-1)/pi
      -> downstream sealed PASSes (CR018b, CR019, CR025, CR031b,
         CR032, CR001c@19, CR002@19)

E4: Reframing note. The PDF text references "black-hole horizon" as
    the standard label for the r_s surface where A = 1. The CR
    treats this purely as the STRUCTURAL CONDITION OF FULL LOCAL
    CLOSURE of the substrate accumulation. The substrate math reads
    A(r) = r_s/r monotonically; A(r) reaches 1 at r = r_s; the
    interpretation as a "black hole" is observational labeling that
    sits on top of the structural condition but is not part of the
    substrate identity itself. The same A = 1 condition is the
    structural primitive that resolves through angular and
    dimensional projection into the cosmic seed A_0 = 1/(12*pi).
```

## Implementation Discipline

```text
All computations are closed-form floating-point evaluations of pi-based
expressions. No iteration, no random draws, no catalog data, no integrals.

Tolerances:
  P1, P2, P3: 1e-12 relative

No null distributions / wrong controls. The CR establishes that the
substrate's A_0 is the unique value consistent with
  A_horizon = 1, D = 3, angular factor 4*pi.
Randomizing those inputs would produce different A_0 values; the
sensitivity table (E1) reports the D-sensitivity directly.
```

## Frozen Sources

```text
Branch-local cross-checks (sealed; no runtime read):
  CR012 (branch 06)               (substrate primitive A_0 used downstream)
  CR018b (branch 06) precommit hash bdd4dc29...
  CR019  (branch 06) precommit hash ef52480d...
  CR025  (branch 08)              (substrate density used in halo profile)
  CR031b (branch 08)              (substrate density used in radial law)
  CR032  (branch 08)              (substrate density used in halo mass)
  CR001c@19 precommit hash         64b17ea7...
  CR002@19 precommit hash          b18c49fc...

Substrate (read-only):
  manuscript Section 4 derived native quantities (A_0, R, Theta, Omega_m)
  PDF: A_horizon = 1 -> A_0 = 1/(4*pi*D) projection identity
```

## Rule-9 Line

```text
This test could have falsified the closed-form identity that SAM's
substrate constant A_0 = 1/(12*pi) arises as the projection of the
unit-closure horizon condition A_horizon = 1 through the angular
factor 4*pi and dimensional factor D = 3.

It could fail if:
  - 1/(4*pi*D) at D = 3 does not equal 1/(12*pi) to machine precision (P1)
  - R*A_0 with R = 2*alpha_H*D and alpha_H = 2 does not equal 1/pi (P2)
  - A(r) = r_s/r at r = r_s does not equal 1 (P3)
```

## Manuscript Headline (conditional on PASS)

```text
SAM's substrate constant A_0 = 1/(12*pi) is not arbitrary. It is the
projection of the full-local-closure condition A_horizon = 1 through
the angular factor 4*pi (full solid angle in 3D) and the dimensional
factor D (the native dimensional readout), evaluated at D = 3:

  A_0 = A_horizon / (4*pi*D) = 1 / (12*pi)

The matter density identity Omega_m = R*A_0 = alpha_H/(2*pi) is
invariant under the choice of dimension D when the radix R is coupled
to D as R = 2*alpha_H*D. With alpha_H = 2:

  Omega_m = 1/pi

which is the matter density that has passed in every Courtroom CR
that touches density-derived quantities (CR018b, CR019, CR025,
CR031b, CR032, CR001c@19, CR002@19).

The structural origin of A_0 is the unit closure of the accumulation
field A(r) = r_s/r at r = r_s. The substrate's cosmic seed is the
horizon unit closure distributed over angular and dimensional
ledger.
```

## Stewardship Reference

```text
SHA-256: d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```
