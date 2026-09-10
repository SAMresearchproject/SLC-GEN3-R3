# CR015 Precommit

## Test ID

```text
CR015_SN_BAO_INDEPENDENT_LEDGER_LOCK
```

## Test Type

```text
Fresh Courtroom branch test.
Not a pointer to a G-test verdict.
The SN row artifact is used for downstream overlap only after the identity
functions are declared.
```

## Question

```text
Do the independent SN and BAO ledgers reduce to the same A_los kernel before the
downstream overlap diagnostic is applied?
```

## Frozen Formula Set

```text
A0 = 1/(pi*R)
A_SN(z) = A0*R*(1-(1+z)^(-D))
A_BAO(z) = A0*R*(1-(1+z)^(-D))
same_z_identity_error = A_SN(z)-A_BAO(z)
```

## Downstream Overlap Sites

```text
z = 0.38, 0.51, 0.61
half_width_z = 0.05
maximum allowed absolute shrinkage-percent difference = 0.25
```

## Wrong Controls

```text
SN_half_A
BAO_D2
SN_constant_median_A
BAO_no_shrink
opposite_sign_BAO
```

## Rule-9 Line

```text
This test could have falsified: the independent-ledger claim if separately
computed SN luminosity/flux and BAO ruler/projection ledgers did not reduce to
the same A_los(z), or if the BAO-site SN overlap failed without using the
overlap as a formula source.
```

