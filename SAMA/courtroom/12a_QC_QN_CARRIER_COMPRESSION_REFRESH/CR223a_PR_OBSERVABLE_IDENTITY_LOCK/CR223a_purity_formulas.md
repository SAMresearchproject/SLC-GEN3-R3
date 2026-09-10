# CR223a Purity Formulas

A_leak(t) = 1 - Tr(rho(t)^2),  t_fire = inf{ t : A_leak(t) >= 1/(D * 2^D) }

## Structural grounding in SAM SEALED_CONSTANTs

The framework has exactly three SEALED_CONSTANTs (see CR227 in 09a_PARTICLE_MASS_CHAIN):

```text
R       = 12   radix / native route constant
D       = 3    closure depth
alpha_H = 2    hidden-source generator
```

CR223a uses {alpha_H, D} directly. R does not appear in the firing-time
calculation but gates the 126 native-row capacity and the 12-row carrier
ledger depth (CR222, CR227).

### A_side is constants-derived

```text
A_side = 1 / (D * 2^D) = 1 / (3 * 8) = 1/24    (was treated as "campaign-locked invariant")
```

### Loaded qutrit is the {alpha_H, D} Born extension

```text
|psi> proportional to (alpha_H * |0> + D * |+1> + alpha_H * |-1>)
populations (p0, p+, p-) = (alpha_H^2, D^2, alpha_H^2) / (2 alpha_H^2 + D^2)
                          = (4/17, 9/17, 4/17)                        (for alpha_H=2, D=3)
```

### Diagonal / off-diagonal purity terms

```text
diag_num   = 2 alpha_H^4 + D^4              = 2*16 + 81  = 113
off_num    = 2 alpha_H^2 (2 D^2 + alpha_H^2) = 2*4*22    = 176
norm^2     = (2 alpha_H^2 + D^2)^2          = 17^2       = 289
closure    : diag_num + off_num             = norm^2     = 289   (purity closes at t=0)
```

## M1 - scalar exponential-purity surrogate

```text
P(t) = exp(-2 t / T2)
A_leak(t) = 1 - exp(-2 t / T2)
t_fire/T2 = - ln(23/24) / 2 = ln(24/23) / 2 = 0.0212798072
```

## M2 - two-level pure dephasing of |+>

|+> = (|0> + |1>)/sqrt(2). Pure dephasing only (no T1):

```text
P(t) = 1/2 + 1/2 * exp(-2 t / T2)
A_leak(t) = (1/2) (1 - exp(-2 t / T2))
solve (1/2)(1 - exp(-2t/T2)) = 1/24:
    1 - exp(-2t/T2) = 1/12
    exp(-2t/T2) = 11/12
    t_fire/T2 = ln(12/11) / 2 = 0.0435056885
```

## M3 - loaded qutrit, equal pure dephasing on all coherences

State:

```text
|psi> = (2|0> + 3|+1> + 2|-1>) / sqrt(17)
populations (p0, p+, p-) = (4/17, 9/17, 4/17)
diagonal-purity contribution  : (4/17)^2 + (9/17)^2 + (4/17)^2 = 113/289
off-diagonal contribution at 0: 2 * ((4/17)(9/17) + (4/17)(4/17) + (9/17)(4/17))
                              = 2 * (36 + 16 + 36) / 289 = 176/289
```

Closure: 113/289 + 176/289 = 1.

Equal pure dephasing decays every |rho_ij|^2 by exp(-2t/T2):

```text
P(t) = diag_num/norm^2 + off_num/norm^2 * exp(-2t/T2)
A_leak(t) = (off_num/norm^2) * (1 - exp(-2t/T2))

solve A_leak = 1/(D 2^D):
    1 - exp(-2t/T2) = norm^2 / (off_num * D * 2^D)
    t_fire/T2 = (1/2) ln( (off_num * D * 2^D) / (off_num * D * 2^D - norm^2) )
```

Substituting the {alpha_H, D} structural forms:

```text
t_fire/T2 = (1/2) ln(
    2 alpha_H^2 (2 D^2 + alpha_H^2) * D * 2^D
    /
    [ 2 alpha_H^2 (2 D^2 + alpha_H^2) * D * 2^D - (2 alpha_H^2 + D^2)^2 ]
)

for (alpha_H, D) = (2, 3):
    numerator    = 176 * 24 = 4224
    denominator  = 4224 - 289 = 3935
    t_fire/T2    = ln(4224/3935) / 2 = 0.0354358323
```

Every term on the right is in {alpha_H, D}. The PR loaded-qutrit firing
coefficient under equal pure dephasing is a closed-form SAM prediction, not
a fit. The proportionality to T2 is the only apparatus piece.

## M4 - loaded qutrit, NV Lindblad with finite T1 = T2 (CR068a convention)

Lindblad collapse operators (in T2 = 1 units):

```text
L_+  = sqrt(Gamma_1) |0><+1|          amplitude damping +1 -> 0
L_-  = sqrt(Gamma_1) |0><-1|          amplitude damping -1 -> 0
L_phi = sqrt(gamma_phi / 2) S_z       pure dephasing via spin-1 S_z
gamma_phi = 1/T2 - 1/(2 T1)
T1 = T2 = 1  ->  Gamma_1 = 1, gamma_phi = 1/2
```

Analytic solution in basis (|0>, |+1>, |-1>):

```text
rho_++(t) = (9/17)  exp(-Gamma_1 t)
rho_--(t) = (4/17)  exp(-Gamma_1 t)
rho_00(t) = 1 - (13/17) exp(-Gamma_1 t)
rho_0+(t) = (6/17)  exp(-(Gamma_1/2 + gamma_phi/4) t)
rho_0-(t) = (4/17)  exp(-(Gamma_1/2 + gamma_phi/4) t)
rho_+-(t) = (6/17)  exp(-(Gamma_1 + gamma_phi) t)
```

(The factor gamma_phi/4 comes from S_z dephasing contributing rate
(gamma_phi/2) * (s_i - s_j)^2 / 2 to rho_ij; |0>-|+-1> coherence has
(s_i - s_j)^2 = 1.)

A_leak(t) = 1 - sum_i rho_ii(t)^2 - 2 sum_{i<j} |rho_ij(t)|^2

Numerical root with Gamma_1 = 1, gamma_phi = 1/2:

```text
t_fire/T2 (analytic continuous root)        = 0.0289614682
CR068a discrete-sample first-fire (s=58)    = 0.029146
CR068a discrete-sample prior (s=57, below)  = 0.028643
```

The analytic continuous root sits between samples 57 and 58 of the CR068a
200-sample / 100 us window, confirming that the CR068a simulator output is
the discrete-grid manifestation of this Lindblad model.

## Hardware default (locked, no universal coefficient)

```text
t_fire^pred = inf{ t : 1 - Tr[rho_cal(t)^2] >= 1/24 }
```

where rho_cal(t) is generated from independently measured T1, T2, SPAM, and
pulse parameters for the selected platform. CR223a does NOT lock a universal
t_fire = c0 * T2 coefficient; it locks the calibrated-trajectory rule.
