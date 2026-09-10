# CR004 Precommit: Weak-Field A-Kernel External Contact

## Test ID

```text
CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT
```

## Branch

```text
02_A_KERNEL_WEAK_FIELD
```

## Test Type

```text
new_forward_work = true
is_audit_or_retest = false
confirmation_or_double_check = false
```

This is not a rerun of G224, G284b, or G284c. It is a fresh Courtroom branch
test using declared weak-field anchors.

## Question

Does the SAM weak-field A-kernel:

```text
A(r) = r_s/r = 2GM/(c^2 r)
Phi = -c^2 A/2
g = (c^2/2) |dA/dr|
v_escape = c sqrt(A)
```

land external weak-field surface-gravity and escape-speed anchors without
post-target tuning?

## External Anchors

The declared external anchors are broad observational/standard ranges for
Earth, Moon, and Sun surface gravity and escape speed. The ranges are deliberately
loose enough to avoid geoid/model minutiae and tight enough to reject wrong
factor/radial controls.

## Wrong Controls

```text
half_A:                 A = GM/(c^2 r)
double_A:               A = 4GM/(c^2 r)
inverse_square_A:        A = (r_s/r)^2
potential_no_half:       Phi = -c^2 A
gravity_missing_half:    g = c^2 |dA/dr|
escape_missing_factor:   v_escape = c sqrt(A/2)
```

## Rule-9 Line

```text
This test could have falsified: the claim that SAM's weak-field A-kernel A(r)=r_s/r carries the correct factor, radial power, potential lane, acceleration lane, and escape-speed lane against external weak-field anchors.
```

## Expected Verdict

```text
execution_status = CLEAN
scientific_verdict = PASS_SCOPED_WEAK_FIELD
```

Reason: unlike the prior structural A-kernel recertification, this branch test
uses external weak-field anchor ranges.
