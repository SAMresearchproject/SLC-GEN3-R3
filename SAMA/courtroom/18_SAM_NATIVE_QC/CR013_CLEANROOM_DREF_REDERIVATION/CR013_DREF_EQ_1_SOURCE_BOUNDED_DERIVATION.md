# CR013 d_ref = 1 Source-Bounded Derivation

**Prepared:** 2026-07-03  
**Task preflight:** `artifacts/preflight_filled/PREFLIGHT_20260703_121748_no_script.md`  
**Input boundary:** pre-2026-06-26 source snapshot
`0cc5212671c7d69e20fa1c6159ff056e3bfbbbc1` only, after preflight. The
post-cutoff CR013 support note is excluded from source evidence for this blind
CR pass.  
**Cleanroom status:** NOT A TRUE CONTEXT-BLIND DERIVER RUN. The current session
has prior conversation context. This artifact is a source-bounded derivation
from pre-cutoff sources only, not from the post-cutoff support note.

## Claim

The pre-cutoff source set supports a normalized SLC coupling convention:

```text
d_ref_norm = 1
```

where `d_ref_norm` means "the reference spacing after distances are expressed
in `d_ref` units."

It does not derive an absolute SI length for `d_ref`.

## Inputs admitted from pre-cutoff sources

The pre-cutoff CR004/SLC source set admits the following statements:

```text
1. CR004_PRECOMMIT: d_ref = unit spacing (chosen = 1)
2. CR004_PRECOMMIT: d(X, Y) is measured in d_ref units
3. CR004_PRECOMMIT: d(X, X) = d_ref
4. CR004_PRECOMMIT: site Y receives A-shift contribution =
   (1/N_max) * (d_ref / d(X, Y))
5. CR004_result / CR004_distance_sweep: CR004 PASS tested the normalized
   1/r kernel at d = 1, 2, 6, 12, 100, 10000
6. CR004_wrong_controls: WC-3 passed; the runner matched 1/r and not 1/d^2
7. SLC_UNITS_AND_NORMALIZATION: physical distance is logical in CR004;
   physical magnitude remains open for LCQC018
```

## Derivation

Let `L_ref` denote the unknown absolute length corresponding to one reference
spacing. The pre-cutoff source set does not supply `L_ref` in meters.

Because distances are measured in `d_ref` units, define a dimensionless
distance:

```text
delta(X, Y) = d_abs(X, Y) / L_ref
```

The admitted statement `d(X, Y) is measured in d_ref units` means the test
quantity named `d(X, Y)` is this dimensionless `delta(X, Y)`.

By the admitted statement `d_ref = unit spacing (chosen = 1)`, the normalized
reference spacing is:

```text
d_ref_norm = L_ref / L_ref = 1
```

Substitute the normalized reading into the coupling law:

```text
A_shift(Y from X)
  = (1/N_max) * (d_ref / d(X, Y))
  = (1/N_max) * (1 / delta(X, Y))
```

So the tested kernel is the normalized inverse-distance law:

```text
A_shift = 1 / (N_max * delta)
```

At the unit-spacing row, `delta = 1`, so:

```text
A_shift(delta = 1) = 1/N_max
```

For the CR004 cumulative two-site budget reported in CR004_result, the
`d = 1` row makes the two asymmetric contributions equal:

```text
3 + 2/d = 2 + 3/d = 5       when d = 1
```

therefore:

```text
cumA_A = cumA_B = 5 * S^2 / N_max
```

CR004_result and CR004_distance_sweep record that CR004's `d = 1` row matched
this prediction and that the six-distance sweep passed. CR004_wrong_controls
records that WC-3 rejected `1/d^2` and retained `1/r`.

Therefore, from the admitted source boundary:

```text
d_ref_norm = 1 is the operational normalization required by, and supported by,
the CR004 normalized distance-coupling test.
```

## Why this does not derive an SI length

If the absolute distance is written:

```text
d_abs(X, Y) = delta(X, Y) * L_ref
```

then the ratio in the coupling law is:

```text
d_ref / d_abs(X, Y)
  = L_ref / (delta(X, Y) * L_ref)
  = 1 / delta(X, Y)
```

The unknown absolute length `L_ref` cancels. The CR004 evidence can therefore
support the normalized value:

```text
d_ref_norm = 1
```

but cannot determine:

```text
L_ref = ? meters
```

without an additional sealed rule that maps one SLC unit spacing to an
absolute SI length.

## Result

```text
DERIVED FROM PRE-CUTOFF SOURCE SET:
  d_ref_norm = 1

NOT DERIVED FROM PRE-CUTOFF SOURCE SET:
  d_ref_abs in SI meters
```

## Recommended wording

```text
From the pre-2026-06-26 CR004/SLC source set alone, d_ref = 1 derives as a
normalized unit-spacing convention: distances in the CR004/SLC coupling law are
expressed in d_ref units, so the reference spacing is one unit by construction.
CR004's PASS distance sweep and 1/r wrong-control rejection support that
normalized kernel operationally. The absolute SI value of d_ref remains
underdetermined because the coupling law depends on the ratio d_ref/d, in which
any absolute reference length cancels.
```
