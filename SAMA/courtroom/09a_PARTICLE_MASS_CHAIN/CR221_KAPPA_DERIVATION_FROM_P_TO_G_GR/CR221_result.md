# CR221 Kappa Derivation From P To G/GR

Result: **CR221_PASS_KAPPA_DERIVATION_FROM_P_TO_G_GR__KAPPA_FLOOR_7117_OVER_768__G_EQUALS_Z_KAPPA_FLOOR_PLUS_N_MINUS_Z_OVER_64__KAPPA_EFF_IS_ELEMENT_QUOTIENT_NOT_SINGLE_GLOBAL_HEAVY_ELEMENT_CONSTANT**

## Direct Answer

Yes, `kappa` is now derivable from the P-centered component writes, but with an
important split:

```text
kappa_floor = (proton_qA + electron_qA + neutron_qA) / 8
            = (145/2 + 145/96 + 1/8) / 8
            = 7117/768
            = 9.266927083333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
```

That floor value is exact for rows where `N = Z`.

For general element rows, the live kernel is an effective quotient:

```text
kappa_eff(P) = G(P) / Z
             = 7105/768 + (N/Z) * 1/64
```

or, equivalently:

```text
G(P) = Z * (7117/768) + (N - Z) / 64
```

## Gold Row

For `Z=79`, `N=118`:

```text
G(P) = 79 * 7117/768 + 39/64
     = 732.6966145833333333333333333333333333333333333333333333333333333333333333333333333333333333333333333

kappa_eff(P) = G(P)/79
             = 562711/60672
             = 9.274640690928270042194092827004219409282700421940928270042194092827004219409282700421940928270042194
```

That is why the current Courtroom value is:

```text
G(P)  = 732.6966145833333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
GR(P) = 5861.572916666666666666666666666666666666666666666666666666666666666666666666666666666666666666666667
```

## What Changed

Before CR220, `kappa` was only a displayed/card-style coefficient. After CR220
and CR221, the coefficient is decomposed into component-write terms:

- proton qA = `145/2`
- electron qA = `145/96`
- neutron qA = `1/8`
- `G` carrier split = divide by `8`

The fixed floor kappa is therefore backed. The heavy-element kernel is not a
single global constant; it is the floor kappa plus the native neutron-excess
term.

## Checks

- 126/126 rows satisfy `G(P) = Z*kappa_floor + (N-Z)/64`.
- 126/126 rows satisfy `GR(P) = 8G(P)`.
- 126/126 rows satisfy `kappa_eff(P) = G(P)/Z`.
- 12 rows have the floor constant exactly (`N=Z`).
- 114 rows use an element-specific effective quotient.

## Boundary

This does not use element cards or known labels. It uses CR220 component writes
and CR220 P-centered element rows. The correct current reading is:

```text
kappa_floor is derived.
kappa_eff(P) is derived row by row.
G(P) = Z*kappa_floor alone is only valid where N=Z.
```

## Artifacts

- `09a_PARTICLE_MASS_CHAIN/CR221_KAPPA_DERIVATION_FROM_P_TO_G_GR/CR221_kernel_terms.csv`
- `09a_PARTICLE_MASS_CHAIN/CR221_KAPPA_DERIVATION_FROM_P_TO_G_GR/CR221_element_kappa_rows_126.csv`
- `09a_PARTICLE_MASS_CHAIN/CR221_KAPPA_DERIVATION_FROM_P_TO_G_GR/CR221_input_manifest.csv`
- `09a_PARTICLE_MASS_CHAIN/CR221_KAPPA_DERIVATION_FROM_P_TO_G_GR/CR221_checks.csv`
- `09a_PARTICLE_MASS_CHAIN/CR221_KAPPA_DERIVATION_FROM_P_TO_G_GR/CR221_summary.json`
- `09a_PARTICLE_MASS_CHAIN/CR221_KAPPA_DERIVATION_FROM_P_TO_G_GR/HASHES.txt`
