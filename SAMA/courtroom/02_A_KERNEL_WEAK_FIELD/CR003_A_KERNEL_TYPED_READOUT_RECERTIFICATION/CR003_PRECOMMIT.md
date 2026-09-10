# CR003 Precommit: A-Kernel Typed Readout Recertification

## Test ID

```text
CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION
```

## Branch

```text
02_A_KERNEL_WEAK_FIELD
```

## Question

Can `A(r)=r_s/r` recertify the native typed weak-field readout packet without
using older G-test outputs as inputs?

## Declared Premises

```text
r_s = 2GM/c^2
A(r) = r_s/r
Phi(A) = -c^2 A/2
clock(A) = sqrt(1 - A)
many_source_A(x) = sum_i r_s,i / |x - x_i|
```

## Candidate Kernels

```text
correct_A = r_s/r
half_A = GM/(c^2 r)
inverse_square_A = r_s/r^2
potential_doubled = Phi = -c^2 A
horizon_shifted = A = 1 at r = 2r_s
clock_linear = 1 - A
```

## Falsification Line

```text
This test could have falsified: the claim that A(r)=r_s/r uniquely supplies the native typed weak-field readout packet for horizon, potential, force, clock, and many-source accumulation lanes.
```

## Expected Verdict Ceiling

```text
scientific_verdict <= BOUNDARY
```

Reason: CR003 is a structural recertification. External-data branches are
needed for empirical PASS.
