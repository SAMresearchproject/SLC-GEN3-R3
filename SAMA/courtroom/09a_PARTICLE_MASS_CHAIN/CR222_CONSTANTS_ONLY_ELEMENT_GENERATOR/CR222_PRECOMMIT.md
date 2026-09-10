# CR222 Precommit - Constants-Only Element Generator

## Task

Test whether the native element rows can be calculated from SAM constants and
sealed generator rules, without element cards, known names, symbols, downstream
masses, or reference CLOCK labels.

## Construction Inputs

The generator may use only:

```text
R = 12
D = 3
alpha_H = 2
split = 2^D = 8
native_capacity = R^2 * (1 - 2^-D) = 126
proton_qA = 145/2
electron_qA = 145/96
neutron_qA = 1/8
```

and native rules:

```text
Z = 1..native_capacity
P = Zp + Nn + Ze
quark address = (2Z+N)u + (Z+2N)d + Ze
radix_cycle = floor((Z-1)/R) + 1
radix_slot = ((Z-1) mod R) + 1
selected_depth = radix_cycle - 1
N_primary = Z + floor(Z * selected_depth / R)
residual_twelfths = (Z * selected_depth) mod R
G(P) = Z * (7117/768) + (N-Z)/64
GR(P) = 8G(P)
retained = 7G(P)
```

The shell vector is generated from constants as:

```text
n_path = [1, alpha_H, D, R/D, R/D, D, alpha_H, alpha_H]
shell_capacity = 2 * n^2
```

which gives:

```text
[2, 8, 18, 32, 32, 18, 8, 8]
```

## Verification Inputs

CR220 and CR119 may be used only after generation, as comparison surfaces.

## Pass Conditions

- 126 primary element-family rows are generated.
- 214 isotope-ladder rows are generated.
- The generated shell capacity vector sums to 126.
- Generated `Z`, `N`, `A`, `P`, quark counts, shell fields, `G`, `GR`, and
  retained support match CR220 for 126/126 rows.
- Generated `GR`, `G`, and retained support match CR119 for 126/126 rows.
- Generated rows contain no known element names, symbols, card values, or
  reference CLOCK construction labels.

