# Why the hidden lift selects sixteen Li-6 histories

This derives the selected family from the candidate operators fixed in
[TECHNICAL_MAP.md](TECHNICAL_MAP.md). The complete finite minimum calculation
is in [RESULT.json](RESULT.json); the following explanation uses its retained
contact kernel. [derive_selection.py](derive_selection.py) checks the formulas
against every selected source address in [SELECTION_DERIVATION.json](SELECTION_DERIVATION.json).

Use object order `P00,N00,P02,N02,P01,N01` and edge order
`000,002,003,004,006,007,008,084,216`. Every edge current `z_e` is one of
`1,i,-1,-i`. On the previous 256 contact minima, the site current is

```text
j = (0,0,0,0,-alpha,alpha),  |alpha| = 1.
```

The two residual-site equations and two inner core equations give

```text
z1 = z7 = t,  z4 = -t,
z2 + z3 = -(z0+t),
z5 + z6 = z0+t.
```

The oriented depth square has circulation `z0-z1+z4-z7 = z0-3t`.
Its squared magnitude is `10-6 Re(z0 conjugate(t))`, hence 4, 10 or 16.
The candidate hidden-nine contribution is `(9/16)|z0-3t|²/4`, giving
`9/16`, `45/32` or `9/4`. Its minimum forces `z0=t`. The other equations
then force the complete edge-current vector to be

```text
z = (t,t,-t,-t,-t,t,t,t,alpha).
```

There are four common phases `t` and four exterior phases `alpha`, giving
exactly sixteen histories. These histories attain both the independent motif
minimum and the hidden-loop minimum for COVER_03 and COVER_04. The full census
establishes that no other histories attain their total minimum.

Their four core triangle squared circulations are `9,9,1,1`; the depth
square has squared circulation 4. The last two triangles are
`P00-P01-N01` and `N00-P01-N01`. Each leaves six pair motifs. At the selected
currents, the remaining pair endpoint exposures sum to 2 and the normalized
three-owner response is `1/3`. The exact observed-channel action is therefore

```text
(43/4)*2 + 72*(1/3) + (9/16)*(4/4)
  = 91/2 + 9/16 = 737/16 = 46.0625.
```

The native-channel calculation is `12*2 + 108/3 + 9/16 = 969/16`.
All center TMR1 forms vanish on these currents, so all six center placements
and all 128 rho settings retain this same sixteen-history set. Both motif
covers remain tied and are retained.

The whole-column probes give `Phi_minus=2/3`, `Phi_plus=2`, hence signed
surface response `1/144`. This scalar has the same value across the previous
contact family: circulation supplies additional distinctions within that
family. States 14336 and 14373 have identical signed site currents but
different triangle/depth circulations, as recorded in
[CIRCULATION_WITNESS.json](CIRCULATION_WITNESS.json).

The site incidence has rank five and the cycle incidence rank four. Together
they have rank nine, with an exact rational inverse retained in
[GEOMETRY.json](GEOMETRY.json). The site and signed cycle responses jointly
recover all nine edge currents. Their squared scalar responses are readouts
of that information; they are not an invertible substitute for the signed
coordinates.

These values use the candidate source-action units. Assigning physical tensor
operators and a MeV scale remains the continuation. The row-to-isotope motif
projection and normalized circulation couplings are Codex's proposal, developed
from Sean Brady's isotope-specific construction and hidden-support direction.
