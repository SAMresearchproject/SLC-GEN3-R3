[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# ISCO and Timelike-Orbit Landmarks

## Current research connections — 14 September 2026

The global execution authority is SLC-GEN3-R3 / SLC-GEN3-CEV1-R3. The September 2026 research includes exact retained-history computation, RH arithmetic compensation, native Mersenne work, Starbreaker signed reception and ATOM3D contact/grammar. The research index connects the retained derivations to the latest code, results and current domain assignments.

[Current derivations, code and results](../../../docs/RESEARCH.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

The photon sphere answers a null-orbit question. The innermost stable circular
orbit answers a timelike stability question. Their radii are not selected by
the same extremum.

For the nonrotating exterior, circular timelike motion requires

\[
\frac{L^2}{m^2c^2r_s^2}
=\frac{x^2}{2x-3},
\qquad x=\frac r{r_s}.
\]

Stable circular orbits exist on the outer side of the minimum of this
requirement. Differentiating selects

\[
x_{\rm ISCO}=3,
\qquad
r_{\rm ISCO}=3r_s,
\qquad
A_{\rm ISCO}=\frac13.
\]

At that coordinate, the dimensionless orbit packet is

\[
\frac{E}{mc^2}=\sqrt{\frac89},
\qquad
\frac{L}{mcr_s}=\sqrt3,
\qquad
\frac{\Omega r_s}{c}=\frac1{\sqrt{54}}.
\]

The \(A\)-coordinate identifies the landmark. The timelike orbit equations
supply the invariants. Neither step replaces the other.

## 1. Opening question and conceptual picture

This chapter asks:

> When the nonrotating source profile is written in the normalized
> \(A=1/x\) coordinate, does the timelike circular-orbit stability condition
> select the mass-invariant landmark \(A=1/3\), and does the same operator
> recover the complete energy, angular-momentum and frequency packet without
> tuning?

The conceptual picture is an energy landscape. A circular orbit is a
stationary radial configuration. A stable circular orbit sits at a local
minimum. As one moves inward, that minimum flattens and then disappears. The
transition point is the ISCO.

The photon sphere at \(x=3/2\) is an unstable null orbit and remains distinct.
The horizon at \(x=1\) is the unit-closure boundary. The ordered exterior
sequence is

\[
1=x_H<\frac32=x_{\rm ph}<3=x_{\rm ISCO},
\]

or, after inversion,

\[
1=A_H>\frac23=A_{\rm ph}>\frac13=A_{\rm ISCO}.
\]

## 2. Definitions, domains and units

| Quantity | Definition | Type | Units/domain |
|---|---|---|---|
| \(M\) | nonrotating spherical source mass | source input | kg |
| \(r_s\) | \(2GM/c^2\) | source length | m |
| \(x\) | \(r/r_s\) | normalized orbit radius | dimensionless, \(x>3/2\) for circular timelike lane |
| \(A\) | \(1/x\) | accumulation landmark coordinate | dimensionless |
| \(m\) | test-particle rest mass | timelike probe input | kg |
| \(\varepsilon\) | \(E/(mc^2)\) | specific energy | dimensionless |
| \(\lambda\) | \(L/(mcr_s)\) | normalized specific angular momentum | dimensionless |
| \(\Omega\) | \(d\phi/dt\) | coordinate orbital angular frequency | rad s\(^{-1}\) |
| \(V_{\rm eff}\) | \(f(x)[1+\lambda^2/x^2]\) | timelike radial effective potential | dimensionless |

The test-particle, nonrotating and circular-orbit assumptions are explicit.
Self-force, spin coupling, accretion stress and Kerr rotation do not enter the
registered packet.

## 3. Build the timelike radial operator

Write the nonrotating exterior factor as

\[
f(x)=1-\frac1x.
\]

For equatorial timelike motion, conservation of specific energy and angular
momentum reduces the radial equation to

\[
\frac{\dot r^2}{c^2}
+V_{\rm eff}(x;\lambda)
=\varepsilon^2,
\]

with

\[
V_{\rm eff}(x;\lambda)
=\left(1-\frac1x\right)
\left(1+\frac{\lambda^2}{x^2}\right).
\]

A circular orbit has

\[
\dot r=0
\]

and

\[
\frac{\partial V_{\rm eff}}{\partial x}=0.
\]

The first condition gives the orbit energy once the radius and angular
momentum are known. The derivative condition fixes the angular momentum
required at each circular radius.

## 4. Derive the circular-orbit angular momentum

Expand the effective potential:

\[
V_{\rm eff}
=1-\frac1x
+\frac{\lambda^2}{x^2}
-\frac{\lambda^2}{x^3}.
\]

Differentiate at fixed \(\lambda\):

\[
\frac{\partial V_{\rm eff}}{\partial x}
=\frac1{x^2}
-\frac{2\lambda^2}{x^3}
+\frac{3\lambda^2}{x^4}.
\]

Set the derivative to zero and multiply by \(x^4\):

\[
x^2-2\lambda^2x+3\lambda^2=0.
\]

Collect the angular-momentum term:

\[
x^2=\lambda^2(2x-3).
\]

Therefore

\[
\boxed{
\lambda^2(x)
=\frac{x^2}{2x-3}
},
\qquad x>\frac32.
\]

The lower domain boundary \(x=3/2\) is already informative: the timelike
circular-orbit angular momentum diverges as the photon sphere is approached.
The null landmark is not a candidate stable timelike orbit.

## 5. Select the marginal stability point

Along the family of circular timelike orbits, stability changes where the
required \(\lambda^2(x)\) reaches its minimum. Differentiate:

\[
\frac{d\lambda^2}{dx}
=\frac{2x(2x-3)-2x^2}{(2x-3)^2}.
\]

Simplify the numerator:

\[
2x(2x-3)-2x^2
=4x^2-6x-2x^2
=2x(x-3).
\]

Hence

\[
\frac{d\lambda^2}{dx}
=\frac{2x(x-3)}{(2x-3)^2}.
\]

In the physical domain \(x>3/2\), the nontrivial stationary point is

\[
\boxed{x_{\rm ISCO}=3}.
\]

For \(3/2<x<3\), the derivative is negative. For \(x>3\), it is positive.
Thus \(x=3\) is the local minimum of the circular-orbit requirement.

Convert back to physical and accumulation coordinates:

\[
\boxed{
r_{\rm ISCO}=3r_s=\frac{6GM}{c^2}
},
\]

\[
\boxed{
A_{\rm ISCO}=\frac1{x_{\rm ISCO}}=\frac13
}.
\]

## 6. Derive the ISCO invariant packet

### 6.1 Angular momentum

Insert \(x=3\) into the circular-orbit formula:

\[
\lambda_{\rm ISCO}^2
=\frac{3^2}{2(3)-3}
=\frac93
=3.
\]

Taking the positive magnitude,

\[
\boxed{
\frac{L_{\rm ISCO}}{mcr_s}
=\lambda_{\rm ISCO}
=\sqrt3
}.
\]

### 6.2 Energy

At a circular orbit,

\[
\varepsilon^2
=V_{\rm eff}(x;\lambda).
\]

Substitute the circular-orbit value
\(\lambda^2=x^2/(2x-3)\):

\[
\varepsilon^2
=\left(1-\frac1x\right)
\left(
1+\frac1{2x-3}
\right).
\]

The second factor becomes

\[
1+\frac1{2x-3}
=\frac{2x-2}{2x-3}
=\frac{2(x-1)}{2x-3}.
\]

Therefore

\[
\varepsilon^2
=\frac{x-1}{x}
\frac{2(x-1)}{2x-3}
=\frac{2(x-1)^2}{x(2x-3)}.
\]

Equivalently,

\[
\varepsilon(x)
=\frac{1-1/x}
{\sqrt{1-3/(2x)}}.
\]

At \(x=3\):

\[
\varepsilon_{\rm ISCO}
=\frac{2/3}{\sqrt{1/2}}
=\frac{2\sqrt2}{3}
=\boxed{\sqrt{\frac89}}.
\]

Numerically,

\[
\frac{E_{\rm ISCO}}{mc^2}
=0.942809041582\ldots.
\]

The binding fraction in this test-particle lane is

\[
1-\sqrt{\frac89}
=0.057190958418\ldots.
\]

### 6.3 Orbital frequency

The nonrotating circular frequency satisfies

\[
\Omega^2=\frac{GM}{r^3}.
\]

Since \(GM=c^2r_s/2\) and \(r=xr_s\),

\[
\Omega^2
=\frac{c^2r_s/2}{x^3r_s^3}
=\frac{c^2}{2x^3r_s^2}.
\]

Thus

\[
\boxed{
\frac{\Omega r_s}{c}
=\frac1{\sqrt{2x^3}}
}.
\]

At \(x=3\):

\[
\boxed{
\frac{\Omega_{\rm ISCO}r_s}{c}
=\frac1{\sqrt{54}}
=0.136082763488\ldots
}.
\]

## 7. Mass-scaling derivation

The normalized coordinate and invariants are fixed numbers. Therefore

\[
r_{\rm ISCO}=3r_s\propto M.
\]

For frequency,

\[
\Omega_{\rm ISCO}
=\frac c{r_s\sqrt{54}}
\propto M^{-1}.
\]

Under \(M\mapsto\alpha M\),

\[
r_{\rm ISCO}\mapsto\alpha r_{\rm ISCO},
\qquad
\Omega_{\rm ISCO}\mapsto\frac{\Omega_{\rm ISCO}}{\alpha},
\]

while

\[
A_{\rm ISCO},\quad
\frac{E}{mc^2},\quad
\frac{L}{mcr_s},\quad
\frac{\Omega r_s}{c}
\]

remain unchanged.

## 8. ISCO and timelike-orbit packet

### 8.1 G338 coordinate premise

`G:G338@SAM-ARCHIVE` first records \(x_{\rm ISCO}=3\) and
\(A_{\rm ISCO}=1/3\) for Earth, Sun and a \(10M_\odot\) source. The maximum
spread of \(A_{\rm ISCO}\) is
\(5.551115123125783\times10^{-17}\). Its exact source verdict is
`G338_PHOTON_SPHERE_ISCO_SUBSTRATE_GEOMETRY_PASS`.

That test supplies the coordinate and scale-invariance premise. It does not by
itself supply the energy, angular momentum or frequency operator.

### 8.2 G413 complete timelike construction

`G:G413@SAM-ARCHIVE` executes the full packet. For its pinned solar-mass row,
it records

\[
r_s=2953.3393820668784\ \mathrm{m},
\]

\[
r_{\rm ISCO}=8860.018146200635\ \mathrm{m},
\]

\[
\frac{E}{mc^2}=0.9428090415820634,
\]

\[
\frac{L}{m}=1.5335385118998396\times10^{12}
\ \mathrm{m^2\,s^{-1}},
\]

\[
\Omega=13813.714199326194\ \mathrm{rad\,s^{-1}}.
\]

Doubling the source mass doubles the ISCO radius and halves the frequency.
The source verdict is
`G413_ISCO_A_METRIC_TIMELIKE_BOUNDARY_PASS`. Its declared grade remains a
nonrotating test-particle ISCO.

### 8.3 CR010 scoped contact

[`CR:CR010@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr010-isco-orbital-contact/README.md) replays the normalized packet with zero free parameters:

| Quantity | Candidate | Declared comparator |
|---|---:|---:|
| \(x_{\rm ISCO}\) | \(3.000000000000\) | \(3.000000000000\) |
| \(A_{\rm ISCO}\) | \(0.333333333333\) | \(0.333333333333\) |
| \(E/(mc^2)\) | \(0.942809041582\) | \(0.942809041582\) |
| \(L/(mcr_s)\) | \(1.732050807569\) | \(1.732050807569\) |
| \(\Omega r_s/c\) | \(0.136082763488\) | \(0.136082763488\) |

Its numerical stability probe evaluates the derivative on either side of
\(x=3\):

\[
\left.\frac{d\lambda^2}{dx}\right|_{\rm left}
=-6.673339658647\times10^{-4},
\]

\[
\left.\frac{d\lambda^2}{dx}\right|_{\rm right}
=+6.660008100567\times10^{-4}.
\]

The sign change confirms the local minimum. The source execution is `CLEAN`
and its scientific verdict is `PASS`.

### 8.4 Locked replay

[`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) reproduces

\[
\frac{E}{mc^2}=0.9428090415820634,
\qquad
\frac{L}{mcr_s}=1.7320508075688774,
\qquad
\frac{\Omega r_s}{c}=0.13608276348795434.
\]

It keeps the horizon, photon sphere and ISCO distinct, rejects horizon-only
fits, and preserves the nonrotating scope.

## 9. Deviation chains and wrong controls

| Wrong or diagnostic route | Failure produced | Correct route |
|---|---|---|
| Set the ISCO at the photon sphere | \(r=3r_s/2\) is half the ISCO radius and the timelike circular requirement diverges there. | Minimize \(\lambda^2(x)\) and obtain \(x=3\). |
| Set \(r_{\rm ISCO}=2r_s\) | Gives \(A=1/2\), a \(50\%\) relative miss from \(1/3\). | Retain the timelike stability point \(3r_s\). |
| Use \(\alpha_H=1\) | Halves the source scale at the same comparator radius. | Keep \(r_s=2GM/c^2\). |
| Use Newtonian circular dynamics alone | Newtonian point-mass orbits have no finite ISCO. | Use the declared strong-field timelike effective potential. |
| Reverse the exterior sign | G413's control produces a negative/unphysical ISCO radius. | Preserve \(f=1-r_s/r\). |
| Introduce a separate landmark field | A \(10\%\) shifted field can mimic a nearby scalar but not the full packet. | Use the same \(A=r_s/r\) coordinate for all landmarks. |
| Treat coordinate continuity as weak-formula continuity | Weak circular formulas do not carry the strong stability transition. | Attach the exact timelike operator to the shared coordinate. |
| Fit the source mass to a normalized invariant | The normalized packet is already independent of mass. | Test scale covariance separately from the coefficients. |
| Promote the packet to Kerr | Spin changes the orbit family and prograde/retrograde ISCO radii. | Keep Kerr as a separately typed continuation. |
| Promote the packet to accretion or self-force closure | Disk stress, radiation, finite mass ratio and feedback are absent. | Retain the test-particle nonrotating boundary. |

## 10. Evidence chain and preserved statuses

| Sequence | Exact qualified key | Role | Preserved result or boundary |
|---:|---|---|---|
| 1 | `G:G338@SAM-ARCHIVE` | premise | Mass-invariant \(x=3,A=1/3\) coordinate across three source scales. |
| 2 | `G:G413@SAM-ARCHIVE` | construction | Complete energy, angular-momentum, frequency and scaling packet with six wrong controls. |
| 3 | [`CR:CR010@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr010-isco-orbital-contact/README.md) | scoped result | Exact normalized timelike packet and local stability minimum; source `CLEAN`/`PASS`. |
| 4 | [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | locked retest | Replays the packet inside the complete nonrotating strong-field zipper. |

The construction proceeds from coordinate to operator to established-reference
contact. The later replay does not erase the earlier source verdict strings.

## 11. Established result, boundary and forward handoff

The compression-safe ISCO packet is

\[
\boxed{
r_{\rm ISCO}=3r_s,\quad
A_{\rm ISCO}=\frac13,\quad
\frac{E}{mc^2}=\sqrt{\frac89},\quad
\frac{L}{mcr_s}=\sqrt3,\quad
\frac{\Omega r_s}{c}=\frac1{\sqrt{54}}
}.
\]

For the declared nonrotating exterior chain replayed by [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md):

**The test result suggests strong contact with the concept.**

The classification is scoped to the registered test-particle, nonrotating
ISCO landmark and invariant packet. It does not classify Kerr orbits,
accretion dynamics, self-force corrections or a complete strong-field metric.

`SAMA-D000017` receives this timelike member alongside the separate lapse,
photon and thermal members of the strong-field zipper.

Exact evidence is the complete four-key sequence in Section 12. The
specifically open boundary is Kerr motion, self-force, accretion dynamics and
any complete strong-field metric beyond the scoped test-particle,
nonrotating packet.

## 12. Focused test and result index

| Exact qualified key | Evidence role | Preserved outcome | Direct result | Result folder |
|---|---|---|---|---|
| `G:G338@SAM-ARCHIVE` | Coordinate premise | `G338_PHOTON_SPHERE_ISCO_SUBSTRATE_GEOMETRY_PASS`; mass-invariant \(x_{\rm ISCO}=3,A_{\rm ISCO}=1/3\). | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G338_photon_sphere_isco_substrate_geometry/G338_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G338_photon_sphere_isco_substrate_geometry) |
| `G:G413@SAM-ARCHIVE` | Timelike construction | `G413_ISCO_A_METRIC_TIMELIKE_BOUNDARY_PASS`; complete orbit packet, mass scaling and wrong-control rejection. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G413_ISCO_A_METRIC_TIMELIKE_BOUNDARY/G413_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G413_ISCO_A_METRIC_TIMELIKE_BOUNDARY) |
| [`CR:CR010@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr010-isco-orbital-contact/README.md) | Scoped external contact | Source execution `CLEAN`, scientific verdict `PASS`; exact normalized packet and local stability minimum. | [result](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR010_ISCO_ORBITAL_CONTACT/CR010_result.md) | [folder](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR010_ISCO_ORBITAL_CONTACT) |
| [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | Locked-stack retest | `LC11_PASS_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY_FROM_LOCKED_PRIMITIVE_STACK`; exact energy, angular momentum and frequency replay. **The test result suggests strong contact with the concept.** | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY) |

## 13. Atomic record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000074-R001` | Defines the normalized strong-field \(A\)-coordinate. |
| `SAMA-C000075-R001` | Supplies the ordered nonrotating landmark tuple. |
| `SAMA-C000076-R001` | Enforces mass invariance and the weak/strong domain boundary. |
| `SAMA-C000084-R001` | Defines \(r_{\rm ISCO}=3r_s\) and \(A_{\rm ISCO}=1/3\). |
| `SAMA-C000085-R001` | Supplies the exact nonrotating invariant packet. |
| `SAMA-C000086-R001` | Records the scoped ISCO orbital contact. |
| `SAMA-C000090-R001` | Supplies the locked strong-field replay and classification. |
| `SAMA-C000122-R001` | Enforces the Volume I and cross-volume subject boundary. |
| `SAMA-C000124-R001` | Separates source-era chronology from current authority. |
| `SAMA-C000125-R001` | Preserves source statuses, classification and false approval state. |

## 14. Source chronology and approval boundary

The four exact evidence keys above are individually registered. Raw meter and
frequency values remain tied to their pinned constant packets. Courtroom and
Last Campaign links are pinned to commit
`b5e914f71377e86ef4c67e199973d9300795cda1`.

Executable artifacts control their numerical results. Active `SAM_LIVE`
documents control present-tense interpretation. The source can be a matter
body, but its finite matter grammar remains Volume II; orbital execution and
simulation internals remain Volume III.

`reviewed_and_approved` remains `false`; `approval` remains `null`. Exact
algebra, source `PASS` status, hashes, validation and the strong-contact
classification do not constitute owner approval.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`CR:CR010@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr010-isco-orbital-contact/README.md) | [CR010_PRECOMMIT.md](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR010_ISCO_ORBITAL_CONTACT/CR010_PRECOMMIT.md)<br>[CR010_declared_premises.json](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR010_ISCO_ORBITAL_CONTACT/CR010_declared_premises.json) | [CR010_runner.py](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR010_ISCO_ORBITAL_CONTACT/CR010_runner.py) | [CR010_candidate_rows.csv](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR010_ISCO_ORBITAL_CONTACT/CR010_candidate_rows.csv) | [CR010_result.md](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR010_ISCO_ORBITAL_CONTACT/CR010_result.md)<br>[CR010_summary.json](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR010_ISCO_ORBITAL_CONTACT/CR010_summary.json) | [All 9 files](../../tests/courtroom/05-strong-field-and-horizon-closure-cr010-isco-orbital-contact/README.md) |
| [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | [LC11_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_wrong_controls.csv) | [LC11_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_result.md)<br>[LC11_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_summary.json) | [All 11 files](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000016`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/ISCO_AND_TIMELIKE_ORBIT_LANDMARKS.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000016 | Strong-Field Closure | ISCO Landmark, Orbital Invariants and Timelike Contact |

| Document field | Value |
|---|---|
| Purpose | Derive the nonrotating innermost stable circular orbit from the timelike stability condition, compute its energy, angular momentum and frequency packet, and route that packet through scoped external contact and locked replay. |
| Prerequisite documents | `SAMA-D000013` |
| Used by | `SAMA-D000017`; focused child of `SAMA-P000002`. |
| Primary source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`, SHA-256 `2f22500f6583f567e350974610f00142e89b081a5b8c4c90c6dfe89bec43be0d`. |
| Revision state | Source-bound draft; mechanically registered proposal; not reviewed or approved. |

</details>
