# CR221 Precommit - Kappa Derivation From P To G/GR

## Task

Assess whether `kappa` can now be derived from the P-centered element engine:

```text
P -> G(P) -> GR(P)
```

## Source Boundary

- CR220 supplies the computed 126-row P-centered element surface.
- CR220 component selector supplies proton, neutron, and electron qA support.
- CR119 remains the comparison surface for `GR(P)`, `G(P)`, and retained
  support.
- No element card/image values are used as construction input.

## Hypothesis

`G(P)` can be written as:

```text
G(P) = Z * kappa_floor + neutron_excess_term
```

where:

```text
kappa_floor = (proton_qA + electron_qA + neutron_qA) / 8
neutron_excess_term = (N - Z) * neutron_qA / 8
```

Equivalently:

```text
kappa_eff(P) = G(P) / Z
             = ((proton_qA + electron_qA) / 8)
               + (N/Z) * (neutron_qA / 8)
```

## Pass Conditions

- Component qA support reduces to the expected exact fractions:
  - proton qA = `145/2`
  - electron qA = `145/96`
  - neutron qA = `1/8`
- `kappa_floor = 7117/768`.
- `neutron_qA / 8 = 1/64`.
- All 126 rows satisfy:
  - `G(P) = Z*kappa_floor + (N-Z)/64`
  - `kappa_eff(P) = G(P)/Z`
  - `GR(P) = 8G(P)`
- `kappa_eff(P)` is reported as element-specific when `N != Z`; the fixed
  floor kappa is not overpromoted as the whole heavy-element kernel.

