[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Photon Sphere and Shadow

## Current research connections — 14 September 2026

The global execution authority is SLC-GEN3-R3 / SLC-GEN3-CEV1-R3. The September 2026 research includes exact retained-history computation, RH arithmetic compensation, native Mersenne work, Starbreaker signed reception and ATOM3D contact/grammar. The research index connects the retained derivations to the latest code, results and current domain assignments.

[Current derivations, code and results](../../../docs/RESEARCH.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

The photon sphere is not the horizon and it is not the innermost stable
timelike orbit. It is the unstable circular landmark selected by the null
exterior operator. In the normalized accumulation coordinate,

\[
r_{\rm ph}=\frac32r_s
\quad\Longrightarrow\quad
A_{\rm ph}=\frac{r_s}{r_{\rm ph}}=\frac23.
\]

The same stationary condition fixes the critical impact parameter:

\[
b_{\rm crit}=\frac{3\sqrt3}{2}r_s.
\]

Doubling that diameter in the far-observer impact plane gives

\[
d_{\rm sh}=3\sqrt3\,r_s.
\]

The conceptual bridge is therefore a sequence:

\[
\text{source scale}
\to\text{normalized coordinate}
\to\text{null circular condition}
\to\text{critical impact}
\to\text{shadow diameter}.
\]

Every arrow has a type. The final number is not obtained by simply naming
\(A=2/3\); the null operator must be attached and differentiated.

## 1. Opening question and conceptual picture

This chapter asks:

> Does the same \(A=r_s/r\) coordinate that indexes the source profile place
> the nonrotating photon landmark at a mass-invariant value and, after the
> correct null operator is applied, recover the critical-impact and
> shadow-diameter packet without a source-specific fit?

Imagine a family of null rays arriving from far away. Rays with sufficiently
large impact parameters turn back outward. Rays below the critical value cross
the capture boundary. The boundary between those behaviors is governed by an
unstable circular null orbit. Its radius is the photon sphere; its apparent
impact-plane scale is \(b_{\rm crit}\).

The coordinate \(A\) labels the orbit. The exterior metric factor supplies the
turning operator. The impact parameter converts the orbit into a shadow scale.

## 2. Definitions, domains and units

| Quantity | Definition | Type | Units/domain |
|---|---|---|---|
| \(M\) | nonrotating spherical source mass | source input | kg |
| \(r_s\) | \(2GM/c^2\) | source length | m |
| \(r\) | exterior areal radius | geometric coordinate | m, \(r>r_s\) |
| \(x\) | \(r/r_s\) | normalized radius | dimensionless |
| \(A\) | \(1/x=r_s/r\) | accumulation landmark coordinate | dimensionless |
| \(f(r)\) | \(1-r_s/r=1-A\) | exterior lapse factor | dimensionless |
| \(r_{\rm ph}\) | unstable circular null radius | photon landmark | m |
| \(A_{\rm ph}\) | \(r_s/r_{\rm ph}\) | normalized photon landmark | dimensionless |
| \(b\) | \(Lc/E\) for a null ray | impact parameter | m |
| \(b_{\rm crit}\) | impact parameter at the unstable circular orbit | capture/shadow invariant | m |
| \(d_{\rm sh}\) | \(2b_{\rm crit}\) | far-observer shadow diameter scale | m |

The chapter is explicitly nonrotating. A Kerr photon region is a
spin- and latitude-dependent surface, not a scalar replacement for
\(r_{\rm ph}=3r_s/2\). The Kerr source records are included to preserve that
boundary and the historical correction of an interpolation.

## 3. Derive the null turning operator

For equatorial null motion in the declared nonrotating exterior, the conserved
energy \(E\) and angular momentum \(L\) reduce the radial equation to a form
whose turning points satisfy

\[
\frac{E^2}{c^2}
=f(r)\frac{L^2}{r^2}.
\]

Define the impact parameter

\[
b=\frac{Lc}{E}.
\]

At a turning point,

\[
\frac1{b^2}=\frac{f(r)}{r^2},
\]

or equivalently

\[
\boxed{
b^2(r)=\frac{r^2}{f(r)}
=\frac{r^2}{1-r_s/r}
}.
\]

The critical ray occurs when the turning-point family is stationary. One may
differentiate \(b^2(r)\), or equivalently maximize

\[
F_{\rm null}(r)=\frac{f(r)}{r^2}.
\]

Both routes are shown because their agreement is an algebraic control.

## 4. Stationary-route derivation of the photon sphere

### 4.1 Differentiate the null factor

Insert \(f(r)=1-r_s/r\):

\[
F_{\rm null}(r)
=\frac{1-r_s/r}{r^2}
=r^{-2}-r_sr^{-3}.
\]

Differentiate:

\[
\frac{dF_{\rm null}}{dr}
=-2r^{-3}+3r_sr^{-4}
=\frac{-2r+3r_s}{r^4}.
\]

The nonzero exterior stationary point satisfies

\[
-2r+3r_s=0,
\]

so

\[
\boxed{
r_{\rm ph}=\frac32r_s
}.
\]

Normalize:

\[
x_{\rm ph}=\frac{r_{\rm ph}}{r_s}=\frac32,
\]

and invert:

\[
\boxed{
A_{\rm ph}=\frac1{x_{\rm ph}}=\frac23
}.
\]

### 4.2 Differentiate the impact-parameter family

The same result follows from

\[
b^2(r)
=\frac{r^3}{r-r_s}.
\]

Differentiate:

\[
\frac{d b^2}{dr}
=\frac{3r^2(r-r_s)-r^3}{(r-r_s)^2}
=\frac{r^2(2r-3r_s)}{(r-r_s)^2}.
\]

The exterior stationary point is again

\[
r=\frac32r_s.
\]

This second derivation catches a missing \(1-A\) factor: if one used
\(b^2=r^2\), there would be no finite stationary photon orbit.

## 5. Derive critical impact and shadow diameter

At \(r_{\rm ph}=3r_s/2\),

\[
f(r_{\rm ph})
=1-\frac{r_s}{(3/2)r_s}
=1-\frac23
=\frac13.
\]

Therefore

\[
b_{\rm crit}
=\frac{r_{\rm ph}}{\sqrt{f(r_{\rm ph})}}
=\frac{(3/2)r_s}{\sqrt{1/3}}
=\boxed{\frac{3\sqrt3}{2}r_s}.
\]

The circular impact-plane boundary has radius \(b_{\rm crit}\), so its
diameter is

\[
\boxed{
d_{\rm sh}=2b_{\rm crit}=3\sqrt3\,r_s
}.
\]

The normalized packet is

\[
\left(
x_{\rm ph},
A_{\rm ph},
\frac{b_{\rm crit}}{r_s},
\frac{d_{\rm sh}}{r_s}
\right)
=
\left(
\frac32,
\frac23,
\frac{3\sqrt3}{2},
3\sqrt3
\right).
\]

Every physical length scales with \(r_s\propto M\), while every normalized
coefficient is mass independent.

## 6. Worked source examples

### 6.1 G338 mass-scale construction

`G:G338@SAM-ARCHIVE` evaluates Earth, Sun and \(10M_\odot\) source scales.
Its photon-sphere ratios are \(1.5\) in all three cases, and its \(A\)-values
are \(2/3\) up to floating-point spread
\(1.1102230246251565\times10^{-16}\).

This is a scale-invariance execution, not three independent astronomical
shadow measurements. It establishes that the normalized coordinate does not
change when the source mass changes.

### 6.2 G412 direct nonrotating operator

`G:G412@SAM-ARCHIVE` uses its own pinned solar-mass constant packet and records

\[
r_s=2953.3393820668784\ \mathrm{m},
\]

\[
r_{\rm ph}=4430.009073100317\ \mathrm{m},
\]

\[
b_{\rm crit}=7673.000792600858\ \mathrm{m}.
\]

The implied diameter is

\[
d_{\rm sh}=15346.001585201716\ \mathrm{m}.
\]

Its exact source verdict is
`G412_PHOTON_SPHERE_A_METRIC_BOUNDARY_PASS`. The source explicitly leaves
full shadow imaging, strong-lensing observables, accretion physics and full
metric derivation outside its grade.

The G338 and G412 meter values use different pinned source constant packets.
Their normalized identities agree; their raw meter rows should not be mixed
into one fabricated precision table.

## 7. Photon sphere and shadow packet

[`CR:CR009@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr009-photon-sphere-shadow-contact/README.md) takes the typed \(A=2/3\) premise and tests the full normalized
packet:

| Quantity | Candidate | Declared comparator |
|---|---:|---:|
| \(x_{\rm ph}\) | \(1.500000000000\) | \(1.500000000000\) |
| \(A_{\rm ph}\) | \(0.666666666667\) | \(0.666666666667\) |
| \(b_{\rm crit}/r_s\) | \(2.598076211353\) | \(2.598076211353\) |
| \(d_{\rm sh}/r_s\) | \(5.196152422707\) | \(5.196152422707\) |

The execution is `CLEAN`, its scientific verdict is `PASS`, it introduces
zero free parameters, and no wrong control matches the full packet. Its scope
is the nonrotating photon-sphere/shadow invariant.

[`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) later replays
\(b_{\rm crit}/r_s=2.5980762113533156\) and
\(d_{\rm sh}/r_s=5.196152422706631\) from the locked primitive stack while
retaining the horizon and ISCO as separate landmarks.

## 8. Kerr correction history and nonrotating boundary

### 8.1 G85: replace a source-era interpolation

`G:G85@SAM-ARCHIVE` examined the rotating photon-region surface. An earlier
source-era construction interpolated between prograde and polar radii with a
\(\sin^2\theta\) ansatz. G85 instead solved the spherical-null conditions
\(R(r_p)=0\) and \(dR/dr=0\), using

\[
\lambda(r_p)
=-\frac{r_p^3-3r_p^2+a^2r_p+a^2}
{a(r_p-1)}
\]

and the corresponding \(\eta(r_p)\) and angular root condition.

The interpolation missed the exact radius by as much as \(39.3454\%\) in that
test. The correction was to use the exact root surface for precision Kerr
work, while preserving the approximate construction as history.

### 8.2 G116: convert the exact surface into a reusable map

`G:G116@SAM-ARCHIVE` turned the G85 result into a numerical map. Its
spin-dependent maximum relative radial error for the discarded interpolation
grew from \(3.19\%\) at \(a=0.30\) to \(40.31\%\) at \(a=0.99\). At
\(a=0\), both routes return the nonrotating \(r=3M=3r_s/2\) limit.

These source records are not a Kerr derivation in this chapter. Their
load-bearing roles are:

- preserve a real failed precision interpolation and its correction;
- certify that rotating photon regions require extra coordinates and
  operators;
- prevent the nonrotating scalar \(A_{\rm ph}=2/3\) from being promoted as a
  complete Kerr shadow surface.

## 9. Deviation chains and wrong controls

| Wrong or diagnostic route | Failure produced | Correct route |
|---|---|---|
| Set \(r_{\rm ph}=2r_s\) | Gives \(A=1/2\), a \(25\%\) relative miss from \(2/3\). | Differentiate the null factor and obtain \(3r_s/2\). |
| Confuse horizon with photon sphere | Substitutes \(A=1\) for \(A=2/3\), a \(50\%\) relative miss. | Keep the landmark tuple ordered. |
| Use \(\alpha_H=1\) at the same physical radius | Halves the source scale and photon coordinate. | Retain \(r_s=2GM/c^2\). |
| Omit \(1-A\) from the impact operator | Leaves \(b^2=r^2\) with no finite extremum. | Use \(b^2=r^2/(1-A)\). |
| Reverse the metric sign | Produces a negative/unphysical critical radius in the G412 control. | Preserve the exterior sign. |
| Change the radial source power | Breaks linear mass scaling; G412 returns a \(\sqrt2\)-type two-mass ratio instead of \(2\). | Keep \(A=r_s/r\). |
| Tune source mass to match a normalized coefficient | The coefficient is already mass invariant, so the fit has no legitimate role. | Compare normalized values before inserting a source mass. |
| Substitute weak deflection for the critical orbit | A perturbative flyby formula does not supply the unstable circular condition. | Use the exact null stationary operator. |
| Keep the old Kerr \(\sin^2\theta\) interpolation for precision work | G85/G116 record large high-spin errors. | Use the exact Kerr root map in a separately typed rotating continuation. |
| Promote this packet into a full EHT image | Image formation also requires rotation, inclination, lens transport, emission and accretion inputs. | Retain the scoped shadow invariant. |

## 10. Evidence chain

| Sequence | Exact qualified key | Role | Preserved result or boundary |
|---:|---|---|---|
| 1 | `G:G85@SAM-ARCHIVE` | source anchor/correction | Exact rotating photon-region surface replaces a failed precision interpolation. |
| 2 | `G:G116@SAM-ARCHIVE` | construction | Reusable exact Kerr map and spin-dependent interpolation-error table. |
| 3 | `G:G338@SAM-ARCHIVE` | construction | Mass-invariant nonrotating landmark tuple across three source scales. |
| 4 | `G:G412@SAM-ARCHIVE` | result | Null circular condition, physical radius, critical impact and scope controls. |
| 5 | [`CR:CR009@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr009-photon-sphere-shadow-contact/README.md) | established-reference result | Exact normalized shadow packet; source `CLEAN`/`PASS`. |
| 6 | [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | locked retest | Replays photon and shadow invariants inside the complete nonrotating zipper. |

The rotating correction history precedes the registered nonrotating contact in
this evidence route, but it does not change the type of the later chapter.

## 11. Established result, boundary and forward handoff

The compression-safe result is

\[
\boxed{
r_{\rm ph}=\frac32r_s,\qquad
A_{\rm ph}=\frac23,\qquad
b_{\rm crit}=\frac{3\sqrt3}{2}r_s,\qquad
d_{\rm sh}=3\sqrt3\,r_s
}.
\]

For the declared nonrotating exterior chain replayed by [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md):

**The test result suggests strong contact with the concept.**

The classification is scoped to the registered nonrotating landmark,
critical-impact and shadow-diameter packet. It does not classify a Kerr image,
accretion model, strong-lensing catalog or complete exterior theory.

`SAMA-D000017` receives this photon member as one dependency in the
strong-field zipper. `SAMA-D000016` develops the distinct timelike ISCO member.

Exact evidence is the complete six-key sequence in Section 12. The
specifically open boundary is a Kerr image, accretion/emission model,
strong-lensing catalog and any complete exterior theory beyond the scoped
nonrotating packet.

## 12. Focused test and result index

| Exact qualified key | Evidence role | Preserved outcome | Direct result | Result folder |
|---|---|---|---|---|
| `G:G85@SAM-ARCHIVE` | Kerr correction anchor | Exact photon-region root replaces a source-era interpolation that missed by up to \(39.3454\%\). | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G85_exact_kerr_photon_region/results/G85_exact_kerr_photon_region_summary.md) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G85_exact_kerr_photon_region) |
| `G:G116@SAM-ARCHIVE` | Exact-map construction | Kerr map records interpolation errors through \(40.31\%\) at \(a=0.99\) and preserves the \(a=0\) limit. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G116_Kerr_exact_photon_region_SAM_map/results/G116_Kerr_exact_photon_region_map_summary.md) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G116_Kerr_exact_photon_region_SAM_map) |
| `G:G338@SAM-ARCHIVE` | Coordinate construction | `G338_PHOTON_SPHERE_ISCO_SUBSTRATE_GEOMETRY_PASS`; mass-invariant \(A_{\rm ph}=2/3\). | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G338_photon_sphere_isco_substrate_geometry/G338_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G338_photon_sphere_isco_substrate_geometry) |
| `G:G412@SAM-ARCHIVE` | Null-operator result | `G412_PHOTON_SPHERE_A_METRIC_BOUNDARY_PASS`; \(r_{\rm ph}=3r_s/2\), critical impact and six wrong controls. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G412_PHOTON_SPHERE_A_METRIC_BOUNDARY/G412_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G412_PHOTON_SPHERE_A_METRIC_BOUNDARY) |
| [`CR:CR009@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr009-photon-sphere-shadow-contact/README.md) | Scoped external contact | Source execution `CLEAN`, scientific verdict `PASS`; normalized photon/shadow packet with zero free parameters. | [result](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR009_PHOTON_SPHERE_SHADOW_CONTACT/CR009_result.md) | [folder](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR009_PHOTON_SPHERE_SHADOW_CONTACT) |
| [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | Locked-stack retest | `LC11_PASS_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY_FROM_LOCKED_PRIMITIVE_STACK`; exact critical-impact and diameter replay. **The test result suggests strong contact with the concept.** | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY) |

## 13. Atomic record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000074-R001` | Defines the normalized strong-field \(A\)-coordinate. |
| `SAMA-C000075-R001` | Supplies the mass-invariant landmark tuple. |
| `SAMA-C000076-R001` | Enforces mass scaling and the weak/strong formula boundary. |
| `SAMA-C000081-R001` | Defines \(r_{\rm ph}=3r_s/2\) and \(A_{\rm ph}=2/3\). |
| `SAMA-C000082-R001` | Supplies critical impact and shadow diameter. |
| `SAMA-C000083-R001` | Records the scoped photon-sphere/shadow contact. |
| `SAMA-C000090-R001` | Supplies the locked strong-field replay and classification. |
| `SAMA-C000122-R001` | Enforces the Volume I and cross-volume subject boundary. |
| `SAMA-C000124-R001` | Separates source-era chronology from current authority. |
| `SAMA-C000125-R001` | Preserves source statuses, classification and false approval state. |

## 14. Source chronology and approval boundary

The six exact evidence keys above are individually registered. The G85/G116
rotating sources are historical precision-correction evidence, not current
authorization to broaden this nonrotating document. Courtroom and Last
Campaign links are pinned to commit
`b5e914f71377e86ef4c67e199973d9300795cda1`.

Executable artifacts control their numerical outputs. Active `SAM_LIVE`
documents control present-tense interpretation. Matter and emission sources
may be named at the boundary, but their grammar remains Volume II; image,
transport and execution internals remain Volume III.

`reviewed_and_approved` remains `false`; `approval` remains `null`. The exact
packet, source `PASS` status, hashes and strong-contact classification do not
constitute owner approval.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`CR:CR009@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr009-photon-sphere-shadow-contact/README.md) | [CR009_PRECOMMIT.md](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR009_PHOTON_SPHERE_SHADOW_CONTACT/CR009_PRECOMMIT.md)<br>[CR009_declared_premises.json](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR009_PHOTON_SPHERE_SHADOW_CONTACT/CR009_declared_premises.json) | [CR009_runner.py](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR009_PHOTON_SPHERE_SHADOW_CONTACT/CR009_runner.py) | [CR009_candidate_rows.csv](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR009_PHOTON_SPHERE_SHADOW_CONTACT/CR009_candidate_rows.csv) | [CR009_result.md](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR009_PHOTON_SPHERE_SHADOW_CONTACT/CR009_result.md)<br>[CR009_summary.json](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR009_PHOTON_SPHERE_SHADOW_CONTACT/CR009_summary.json) | [All 9 files](../../tests/courtroom/05-strong-field-and-horizon-closure-cr009-photon-sphere-shadow-contact/README.md) |
| [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | [LC11_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_wrong_controls.csv) | [LC11_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_result.md)<br>[LC11_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_summary.json) | [All 11 files](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000015`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/PHOTON_SPHERE_AND_SHADOW.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000015 | Strong-Field Closure | Photon-Sphere Landmark, Critical Impact and Shadow Diameter |

| Document field | Value |
|---|---|
| Purpose | Derive the nonrotating photon-sphere coordinate, critical impact parameter and shadow diameter from the exterior null operator, preserve the exact Kerr correction history as a boundary, and route the invariant packet through external contact and locked replay. |
| Prerequisite documents | `SAMA-D000013` |
| Used by | `SAMA-D000017`; focused child of `SAMA-P000002`. |
| Primary source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`, SHA-256 `2f22500f6583f567e350974610f00142e89b081a5b8c4c90c6dfe89bec43be0d`. |
| Revision state | Source-bound draft; mechanically registered proposal; not reviewed or approved. |

</details>
