# CR016 Precommit

## Test ID

```text
CR016_CMB_ACOUSTIC_RULER_PHOTON_ROAD_RATIO
```

## Test Type

```text
Fresh Courtroom branch test.
Not a pointer to a G-test verdict.
Planck theta100 is downstream comparison only.
```

## Question

```text
Does the CMB acoustic-angle member enter as acoustic-write ruler over
photon-road denominator without using the Planck target to choose the formula?
```

## Frozen Formula Set

```text
theta100 = 100*r_star/D_M_photon_road
```

## External Reference

```text
Planck theta100 = 1.04109
comparison window = 0.5 percent
```

## Wrong Controls

```text
use_drag_ruler
wrong_H0_denominator
invert_ratio
half_ruler
drag_ruler_and_wrong_H0
```

## Rule-9 Line

```text
This test could have falsified: the CMB acoustic-ratio member if the frozen
acoustic-write ruler and photon-road denominator did not produce the declared
theta ratio, if the Planck target was needed to choose the formula, or if wrong
controls matched the ratio.
```

