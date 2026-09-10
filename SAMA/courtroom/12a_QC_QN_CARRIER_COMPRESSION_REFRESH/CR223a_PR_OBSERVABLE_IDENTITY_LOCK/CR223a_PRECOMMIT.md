# CR223a PRECOMMIT - PR Observable Identity Lock

## Scope

Lock the canonical PR observable identity and firing-time rule:

```text
A_leak(t) = 1 - Tr(rho(t)^2)
t_fire    = inf{ t : A_leak(t) >= 1/(D * 2^D) }
```

and emit the four-model firing-coefficient table so the repository can no
longer call a model-specific coefficient `c0 * T2` universal.

## Grounded in SAM SEALED_CONSTANTs {alpha_H, D}

```text
alpha_H = 2, D = 3              (SAM SEALED_CONSTANTs from CR227)
A_side                    = 1/(D * 2^D) = 1/24         (structural, not stipulated)
loaded qutrit             = (alpha_H |0> + D |+1> + alpha_H |-1>) / sqrt(2 alpha_H^2 + D^2)
populations               = (alpha_H^2, D^2, alpha_H^2)/(2 alpha_H^2 + D^2) = (4/17, 9/17, 4/17)
diagonal-purity term      = (2 alpha_H^4 + D^4) / (2 alpha_H^2 + D^2)^2 = 113/289
off-diagonal-purity term  = 2 alpha_H^2 (2 D^2 + alpha_H^2) / (2 alpha_H^2 + D^2)^2 = 176/289
M3 coefficient            = (1/2) ln(off*D*2^D / (off*D*2^D - norm^2))
                          = ln(4224/3935)/2 ~= 0.0354358
no universal t_fire = c0 * T2
hardware default = calibrated-trajectory rule
```

## Model roster (frozen pre-data)

```text
M1 scalar exponential-purity surrogate
M2 two-level pure dephasing
M3 loaded qutrit equal pure dephasing
M4 loaded qutrit NV Lindblad CR068a-style with T1 = T2 = 1 ms
M_hardware_default = calibrated rho_cal(t) per platform (CR223c sealing)
```

## Pre-run hash for firing-coefficient table

Expected `CR223a_firing_coefficients.csv` SHA-256:

```text
b32f6767c5b2a16cfba887fa8b8e340732ecce430b7d3083774465b46d9be4d2
```
