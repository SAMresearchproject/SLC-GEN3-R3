# CR222 Constants-Only Element Generator

Result: **CR222_PASS_CONSTANTS_ONLY_ELEMENT_GENERATOR__126_NATIVE_ELEMENT_ROWS__214_ISOTOPE_LADDER_ROWS__MATCHES_CR220_CR119_126_OF_126__NO_CARDS_NO_KNOWN_LABELS_NO_CLOCK_INPUTS**

## Direct Answer

Yes: within the SAM-native boundary, the elements can now be calculated from
constants only.

The run generated:

- **126** native element-family rows.
- **214** isotope-ladder rows.
- **8** closed-shell rows.
- **8** constant frontier-tail rows (`Z=119..126`).

No element cards, known symbols, known names, measured masses, or CLOCK labels
were used to construct the rows.

## Construction Formula

```text
R = 12
D = 3
alpha_H = 2
split = 2^D = 8
native_capacity = R^2 * (1 - 2^-D) = 126

Z = 1..126
P = Zp + Nn + Ze
N = Z + floor(Z * (radix_cycle - 1) / R)
G(P) = Z * 7117/768 + (N - Z)/64
GR(P) = 8G(P)
retained = 7G(P)
```

The shell vector was generated from:

```text
n_path = [1, alpha_H, D, R/D, R/D, D, alpha_H, alpha_H]
capacity = 2n^2
```

giving:

```text
[2, 8, 18, 32, 32, 18, 8, 8]
```

## Verification

The generated rows were compared after construction:

- Generated core fields match CR220: **126/126**
- Generated `G(P)` matches CR220 and CR119: **126/126**
- Generated `GR(P)` matches CR220 and CR119: **126/126**
- Generated retained support matches CR220 and CR119: **126/126**

## Boundary

This calculates the SAM-native element-family table, not the public chemistry
labels. Names like Hydrogen or Gold remain downstream reveal labels. Physical
stability/CLOCK still remains a comparator surface; CR220 showed the count
threshold gets to `Z<=83` with the `43/61` holes still requiring a native
derivation.

## Artifacts

- `09a_PARTICLE_MASS_CHAIN/CR222_CONSTANTS_ONLY_ELEMENT_GENERATOR/CR222_declared_constants.csv`
- `09a_PARTICLE_MASS_CHAIN/CR222_CONSTANTS_ONLY_ELEMENT_GENERATOR/CR222_constants_only_elements_126.csv`
- `09a_PARTICLE_MASS_CHAIN/CR222_CONSTANTS_ONLY_ELEMENT_GENERATOR/CR222_constants_only_isotopes_214.csv`
- `09a_PARTICLE_MASS_CHAIN/CR222_CONSTANTS_ONLY_ELEMENT_GENERATOR/CR222_verification_against_cr220_cr119.csv`
- `09a_PARTICLE_MASS_CHAIN/CR222_CONSTANTS_ONLY_ELEMENT_GENERATOR/CR222_boundary_tests.csv`
- `09a_PARTICLE_MASS_CHAIN/CR222_CONSTANTS_ONLY_ELEMENT_GENERATOR/CR222_input_manifest.csv`
- `09a_PARTICLE_MASS_CHAIN/CR222_CONSTANTS_ONLY_ELEMENT_GENERATOR/CR222_checks.csv`
- `09a_PARTICLE_MASS_CHAIN/CR222_CONSTANTS_ONLY_ELEMENT_GENERATOR/CR222_summary.json`
- `09a_PARTICLE_MASS_CHAIN/CR222_CONSTANTS_ONLY_ELEMENT_GENERATOR/HASHES.txt`
