# CR242 Precommit - SAM Binding-Curvature Derivation

Task: CR242 SAM binding-curvature derivation

Preflight: `artifacts/preflight_filled/PREFLIGHT_20260623_084748_no_script.md`

## Purpose

CR242 tests whether the residual left by the CR240/CR241 integer-mass
surface has a reproducible binding-curvature structure.

The target residual is the positive binding defect:

```text
B_u = A - m_measured
```

This test does not promote free proton or free neutron candidates. It does not
use C5/C6/C7 as fitted particle rows. The question is only whether a
SAM-native typed binding surface can beat or reproduce a Bethe-Weizsacker-style
binding structure.

## Locked typed quantities

The SAM typed basis is restricted to quantities derived from:

```text
A, Z, N - Z, R, S, M, Theta, V
```

Locked spine values:

```text
R = 12
S = 8
M = 126
Theta = 18
V = 27
```

The cubic write cell is `V = 27`. The symbol `p` is not used for this cell.

Parity pairing is allowed only as a derived integer from `Z` and `N - Z`:

```text
pairing_sign = +1 for even-even, -1 for odd-odd, 0 otherwise
```

## Inputs

Training/reference input:

```text
09a_PARTICLE_MASS_CHAIN/CR240_NEUTRON_REST_MASS_CHANNEL/CR240_extended_kernel_predictions.csv
```

Training rows are limited to `LANE_A_HARD_MEASURED` rows. The C-12 anchor row
is excluded from coefficient fitting.

Out-of-sample holdout input:

```text
09a_PARTICLE_MASS_CHAIN/CR241_REST_MASS_HOLDOUT_UNIQUENESS/CR241_holdout_predictions.csv
```

The CR241 holdout is used only for testing. CR242 coefficients must not be fit
on CR241 holdout rows.

## Model surfaces

### BW benchmark fit

The benchmark is an ordinary fitted Bethe-Weizsacker-style linear surface:

```text
1
A
A^(2/3)
Z(Z - 1) / A^(1/3)
(N - Z)^2 / A
pairing_sign / sqrt(A)
```

This model is a comparison target, not a SAM claim.

### SAM typed basis fit

The SAM typed basis is a fitted linear surface over typed quantities:

```text
1
A / (S M)
A^(2/3) / (R V)
Z(Z - 1) / (A^(1/3) S M V)
(N - Z)^2 / (A S Theta)
pairing_sign / (M sqrt(A))
((Z - 1) mod R) / (R M)
abs(N - Z) / (A R)
```

All coefficients are fit on the CR240 training rows only.

### Zero-free typed diagnostic

The strict zero-free diagnostic candidate is:

```text
B_zero =
  A / (S M)
  - A^(2/3) / (R V)
  - Z(Z - 1) / (A^(1/3) S M V)
  - (N - Z)^2 / (A S Theta)
  + pairing_sign / (M sqrt(A))
```

This candidate is reported as a wrong-control/diagnostic surface. It is not
required for a BOUNDARY verdict, but it blocks a STRONG derivation claim unless
it also reproduces the holdout binding curve.

## Verdict gates

STRONG requires all of the following:

```text
all wrong controls complete
CR241 holdout is not used in coefficient fitting
SAM typed basis test RMS <= BW benchmark test RMS
SAM typed basis test R^2 >= 0.98
zero-free typed diagnostic test R^2 >= 0.95
no disallowed promotion or theorem-grade claims
```

BOUNDARY requires all of the following:

```text
all wrong controls complete
CR241 holdout is not used in coefficient fitting
SAM typed basis test R^2 >= 0.95
SAM typed basis test RMS <= 1.10 * BW benchmark test RMS
no disallowed promotion or theorem-grade claims
```

FAIL is returned if any BOUNDARY condition fails, if coefficient fitting leaks
holdout rows, if the shuffled-label control still preserves the typed
explanation, or if disallowed claims are emitted.

## Wrong controls

The following controls are verdict-relevant:

```text
WC1 shuffled train B_u labels must degrade the SAM typed holdout fit
WC2 train/test boundary guard must confirm CR241 holdout rows are never fit
WC3 untyped decimal basis is diagnostic and suppresses STRONG if it beats SAM
WC4 zero-free typed candidate must be reported and suppresses STRONG if weak
WC5 disallowed-claim guard must remain clear
```

## Disallowed claims

CR242 does not claim:

```text
free proton candidate promotion
free neutron candidate promotion
theorem-grade nuclear binding derivation
full nuclear binding-energy derivation
Bethe-Weizsacker replacement
C5/C6/C7 particle promotion
```

CR242 may claim only the verdict actually earned by the train/holdout metrics.

