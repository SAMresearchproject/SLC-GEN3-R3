[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Strong-Field A-Coordinate

## Conceptual abstract

The spherical source profile does not disappear when the weak-field
approximation ends. What survives is its dimensionless coordinate role. Write

\[
r_s=\frac{2GM}{c^2},\qquad x=\frac r{r_s},\qquad A=\frac{r_s}{r}=\frac1x.
\]

The common source scale \(r_s\) removes the mass dimension from exterior
radius. Consequently, the nonrotating horizon, photon sphere and innermost
stable circular orbit occupy the fixed coordinate values

\[
(x_H,x_{\rm ph},x_{\rm ISCO})
=\left(1,\frac32,3\right),
\]

or equivalently

\[
(A_H,A_{\rm ph},A_{\rm ISCO})
=\left(1,\frac23,\frac13\right).
\]

This continuity is a coordinate statement. It does not authorize the weak
series \(\sqrt{1-A}\simeq1-A/2\), the Newtonian potential approximation, or
the weak photon-road formula as exact strong-field laws. The coordinate is the
spine on which the exact exterior operators are attached in the following
chapters.

## 1. Opening question and conceptual picture

This chapter asks:

> Can the same dimensionless accumulation coordinate that organizes the
> spherical weak field index the ordered nonrotating exterior landmarks,
> without importing weak readout formulas into a domain where they no longer
> apply?

The conceptual picture is a normalized ruler. A physical radius doubles when
the source mass doubles, because \(r_s\propto M\). Its normalized location
\(x=r/r_s\), however, remains fixed. The reciprocal coordinate \(A=1/x\)
therefore turns the exterior ordering into a simple accumulation ordering:

\[
r_H<r_{\rm ph}<r_{\rm ISCO}
\quad\Longleftrightarrow\quad
A_H>A_{\rm ph}>A_{\rm ISCO}.
\]

The coordinate tells us *where* a landmark sits in normalized accumulation.
An independently declared operator tells us *what is measured* there.

## 2. Definitions, domains and units

| Quantity | Definition | Type | Units/domain |
|---|---|---|---|
| \(M\) | spherical source mass | source input | kg |
| \(r_s\) | \(2GM/c^2\) | source length scale | m |
| \(r\) | exterior areal radius | geometric coordinate | m, \(r\ge r_s\) for this chapter |
| \(x\) | \(r/r_s\) | normalized exterior radius | dimensionless, \(x\ge1\) |
| \(A\) | \(r_s/r=1/x\) | normalized accumulation coordinate | dimensionless, \(0<A\le1\) outside/at closure |
| \(A_H\) | \(A(x=1)\) | horizon/closure coordinate | \(1\) |
| \(A_{\rm ph}\) | \(A(x=3/2)\) | photon-sphere coordinate | \(2/3\) |
| \(A_{\rm ISCO}\) | \(A(x=3)\) | timelike ISCO coordinate | \(1/3\) |

The source profile is

\[
A(r)=\frac{2GM}{c^2r}.
\]

It is dimensionless because \(GM/c^2\) is a length. At the source scale,

\[
A(r_s)=\frac{r_s}{r_s}=1.
\]

Volume I types this equality as unit-accumulation closure. It is not an
ordinary exterior sample followed automatically by a continuation to
\(A>1\).

## 3. Normalize the source profile

Begin with

\[
x=\frac r{r_s}.
\]

Then \(r=xr_s\), so substitution into the source lift gives

\[
A(r)=\frac{r_s}{xr_s}=\frac1x.
\]

The inverse map is equally important:

\[
x=\frac1A,
\qquad
r=\frac{r_s}{A}.
\]

For a fixed accumulation coordinate \(A_\star\), the corresponding physical
radius is

\[
r_\star(M)=\frac{2GM}{c^2A_\star}.
\]

If \(M\mapsto\lambda M\), then

\[
r_s\mapsto\lambda r_s,
\qquad
r_\star\mapsto\lambda r_\star,
\qquad
x_\star=\frac{r_\star}{r_s}\mapsto x_\star,
\qquad
A_\star\mapsto A_\star.
\]

This is the complete mass-invariance argument: physical lengths scale with
mass while the normalized landmark tuple remains fixed.

## 4. Strong-field coordinate and landmarks

### 4.1 Horizon coordinate

The nonrotating exterior closure radius is \(r_H=r_s\). Therefore

\[
x_H=\frac{r_H}{r_s}=1,
\qquad
A_H=\frac1{x_H}=1.
\]

This is both the first exterior landmark and the endpoint of the ordinary
exterior coordinate domain in this chapter.

### 4.2 Photon-sphere coordinate from the null circular condition

For the declared nonrotating exterior metric lane, the null circular-orbit
radial factor is proportional to

\[
F_{\rm null}(r)=\frac{1-r_s/r}{r^2}.
\]

Write it as

\[
F_{\rm null}(r)=r^{-2}-r_sr^{-3}.
\]

The circular condition is the stationary point

\[
\frac{dF_{\rm null}}{dr}
=-2r^{-3}+3r_sr^{-4}=0.
\]

Multiply by \(r^4\):

\[
-2r+3r_s=0.
\]

Hence

\[
r_{\rm ph}=\frac32r_s,
\qquad
x_{\rm ph}=\frac32,
\qquad
\boxed{A_{\rm ph}=\frac23}.
\]

The associated critical impact parameter follows from the same exterior
factor:

\[
b_c=\frac{r_{\rm ph}}{\sqrt{1-r_s/r_{\rm ph}}}
=\frac{(3/2)r_s}{\sqrt{1/3}}
=\frac{3\sqrt3}{2}r_s.
\]

`G:G412@SAM-ARCHIVE` records exact agreement of this location and impact
parameter with its nonrotating comparator, while explicitly leaving a full
shadow image, strong-lensing observables and accretion physics outside scope.

### 4.3 ISCO coordinate from the timelike stability boundary

For circular timelike orbits in the same exterior lane, the specific angular
momentum required at normalized radius \(x\) can be written

\[
\frac{L^2}{m^2c^2r_s^2}=\frac{x^2}{2x-3},
\qquad x>\frac32.
\]

The marginally stable orbit occurs at the minimum of this circular-orbit
requirement. Differentiate:

\[
\frac{d}{dx}\left(\frac{x^2}{2x-3}\right)
=\frac{2x(2x-3)-2x^2}{(2x-3)^2}
=\frac{2x(x-3)}{(2x-3)^2}.
\]

In the exterior timelike domain the nontrivial stationary point is

\[
x_{\rm ISCO}=3.
\]

Therefore

\[
r_{\rm ISCO}=3r_s=\frac{6GM}{c^2},
\qquad
\boxed{A_{\rm ISCO}=\frac13}.
\]

At that coordinate, the registered nonrotating values are

\[
\frac{E}{mc^2}=\frac{2\sqrt2}{3}=0.942809041582\ldots,
\]

\[
\frac{L}{mcr_s}=\sqrt3=1.732050807569\ldots,
\]

and

\[
\frac{\Omega r_s}{c}=\frac1{\sqrt{54}}
=0.136082763488\ldots.
\]

`G:G413@SAM-ARCHIVE` records those timelike boundary quantities, radius
scaling \(r_{\rm ISCO}\propto M\), frequency scaling
\(\Omega_{\rm ISCO}\propto M^{-1}\), and the ordered exterior tuple.

### 4.4 Assemble the tuple

The three derivations now join:

\[
\boxed{
(x_H,x_{\rm ph},x_{\rm ISCO})
=\left(1,\frac32,3\right)
}
\]

and, under \(A=1/x\),

\[
\boxed{
(A_H,A_{\rm ph},A_{\rm ISCO})
=\left(1,\frac23,\frac13\right).
}
\]

The reciprocal map reverses the ordering:

\[
1<\frac32<3
\quad\Longrightarrow\quad
1>\frac23>\frac13.
\]

## 5. Mass-scale replay

`G:G338@SAM-ARCHIVE` evaluates the tuple on Earth, the Sun and a
\(10M_\odot\) source. The physical source scales differ strongly:

| Source | Registered \(r_s\) |
|---|---:|
| Earth | \(0.0088701028718461\) m |
| Sun | \(2954.007736491099\) m |
| \(10M_\odot\) | \(29540.07736491099\) m |

Yet the normalized rows remain

\[
(1,1),\quad\left(\frac32,\frac23\right),\quad
\left(3,\frac13\right)
\]

for \((x,A)\). The registered maximum spreads are \(0\) for \(A_H\),
\(1.1102230246251565\times10^{-16}\) for \(A_{\rm ph}\), and
\(5.551115123125783\times10^{-17}\) for \(A_{\rm ISCO}\), consistent with
floating-point evaluation of the exact rational tuple.

This test is not an independent three-system empirical comparison. It is an
executable scale-invariance check of the normalized construction.

## 6. Coordinate continuity versus operator continuity

The same \(A=r_s/r\) coordinate labels weak and strong exterior locations.
That does not mean every weak operator remains exact at order-one \(A\).

Consider the exact static exterior lapse

\[
\ell(A)=\sqrt{1-A}.
\]

Its weak expansion is

\[
\ell(A)=1-\frac A2-\frac{A^2}{8}-\cdots.
\]

At \(A\ll1\), retaining \(1-A/2\) is appropriate. At the ISCO,
\(A=1/3\), the corresponding exact redshift is

\[
z_{\rm exact}=\frac1{\sqrt{1-A}}-1
=\sqrt{\frac32}-1
=0.224744871392\ldots.
\]

The weak substitution \(z_{\rm weak}=A/2=1/6\) misses by the registered
relative amount \(0.258418376203\). At the photon sphere,

\[
z_{\rm exact}=\sqrt3-1=0.732050807569\ldots.
\]

At \(A\to1^-\), \(\ell\to0\) and \(z\to\infty\). `G:G339@SAM-ARCHIVE`
therefore serves as a boundary test: it confirms low-\(A\) agreement, records
failure of the weak expression as an exact order-one formula, and preserves
the divergent approach to unit closure.

The exact lapse and exterior radial road are developed in `SAMA-D000014`.
This chapter supplies only the coordinate and the domain firewall required by
that derivation.

## 7. Deviation chains and wrong controls

### 7.1 Use \(\alpha_H=1\) at fixed exterior radii

The archived wrong control halves the source scale in the coordinate map. At
the standard photon-sphere and ISCO radii it returns \(A=1/3\) and \(A=1/6\)
instead of \(2/3\) and \(1/3\). `G:G338@SAM-ARCHIVE` records a \(50\%\)
relative miss. The correction is to retain the locked
\(r_s=2GM/c^2\).

### 7.2 Confuse the photon sphere with \(2r_s\)

Setting \(r_{\rm ph}=2r_s\) gives \(A=1/2\), a \(25\%\) relative miss from
\(2/3\). The derivative of the null circular factor selects \(3r_s/2\), not
an arbitrary round multiple.

### 7.3 Confuse the ISCO with the photon sphere

Setting \(r_{\rm ISCO}=3r_s/2\) gives half the required physical radius and
collapses a timelike stability boundary into a null circular orbit. The
timelike minimization instead selects \(3r_s\).

### 7.4 Remove the \(1-A\) exterior factor

`G:G412@SAM-ARCHIVE` records that omitting \(1-A\) leaves no photon-sphere
extremum. The coordinate \(A\) alone labels radius; the observable landmark
still requires the correctly typed exterior operator.

### 7.5 Substitute Newtonian no-critical-radius geometry

A purely Newtonian control has neither a finite photon sphere nor an ISCO.
That absence is an appropriate diagnostic control, not a competing landmark
packet. It shows why weak potential continuity is insufficient to construct
strong-field critical orbits.

### 7.6 Treat \(A/2\) as exact redshift

At \(A=1/3\), the weak expression misses the exact redshift by about
\(25.84\%\). The correction is to keep the exact \(1/\sqrt{1-A}-1\) operator
for order-one accumulation.

### 7.7 Soften or cross \(A=1\)

The wrong route treats the horizon as an ordinary register or literal photon
launch point. [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) rejects this: unit accumulation remains the
no-completed-parent-ledger/no-literal-launch boundary. Later exterior formulas
approach \(A=1\) from below; they do not redefine closure so an ordinary path
can begin on the other side.

### 7.8 Promote the tuple into full strong-field closure

The tuple by itself does not supply Kerr rotation, a full metric derivation,
an EHT image, quasinormal modes, accretion physics or a complete Hawking
spectrum. [`CR:CR007@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr007-strong-field-landmark-selector/README.md) deliberately retains a source scientific verdict of
`BOUNDARY`. The later locked-stack replay supplies broader scoped contact
without rewriting that earlier result.

## 8. Strong-field coordinate and landmarks evidence chain

| Sequence | Exact key | Role | Preserved result or boundary |
|---:|---|---|---|
| 1 | `G:G338@SAM-ARCHIVE` | construction | Builds the rational tuple and its mass-scale replay; rejects five landmark controls. |
| 2 | `G:G339@SAM-ARCHIVE` | boundary | Separates exact order-one lapse/redshift from its weak series and records horizon divergence. |
| 3 | `G:G412@SAM-ARCHIVE` | result | Recovers the nonrotating photon-sphere radius and critical impact parameter from the \(A\)-metric lane. |
| 4 | `G:G413@SAM-ARCHIVE` | result | Recovers the nonrotating timelike ISCO radius, energy, angular momentum and frequency. |
| 5 | [`CR:CR007@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr007-strong-field-landmark-selector/README.md) | boundary | Independently recertifies the exact tuple with zero free parameters while retaining its sealed structural grade. |
| 6 | [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | retest | Replays the full locked horizon stack, preserves earlier boundary grades and rejects softening and overpromotion controls. |

The sequence is cumulative. G338 constructs the coordinate packet. G339
blocks weak extrapolation. G412 and G413 attach null and timelike metric
operators. CR007 recertifies the root without borrowing older outputs. LC11
then replays the chain from the locked primitive stack without changing the
earlier artifacts or their source-era grades.

## 9. Established result and forward handoff

The compression-safe coordinate packet is

\[
\boxed{
x=\frac r{r_s},\qquad A=\frac1x,
\qquad
(A_H,A_{\rm ph},A_{\rm ISCO})
=\left(1,\frac23,\frac13\right).
}
\]

The tuple is mass invariant because each physical landmark is a fixed
multiple of \(r_s\). Coordinate continuity does not transfer weak operator
validity into the strong domain.

For the declared nonrotating exterior chain replayed by [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md):

**The test result suggests strong contact with the concept.**

That classification is scoped to the registered nonrotating exterior chain.
It does not alter the preserved `BOUNDARY` source verdict of
[`CR:CR007@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr007-strong-field-landmark-selector/README.md), and it does not classify Kerr, full strong-field metrics,
complete thermodynamics or interior structure.

`SAMA-D000014` receives \((x,A)\) for exact lapse and exterior radial
traversal. `SAMA-D000015` receives the closure boundary. `SAMA-D000016`
receives the photon-sphere/shadow operator. `SAMA-D000017` receives the
timelike ISCO operator.

Exact evidence is the complete six-key sequence in Section 10. The
specifically open boundary is every operator beyond coordinate placement:
full metric construction, Kerr geometry, interior dynamics and complete
thermodynamics remain separate.

## 10. Focused test and result index

| Exact qualified key | Evidence role | Preserved outcome | Direct result | Result folder |
|---|---|---|---|---|
| `G:G338@SAM-ARCHIVE` | Coordinate construction | `G338_PHOTON_SPHERE_ISCO_SUBSTRATE_GEOMETRY_PASS`; exact rational tuple and mass-scale invariance. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G338_photon_sphere_isco_substrate_geometry/G338_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G338_photon_sphere_isco_substrate_geometry) |
| `G:G339@SAM-ARCHIVE` | Weak/strong boundary | `G339_STRONG_FIELD_REDSHIFT_SUBSTRATE_BOUNDARY_PASS`; exact redshift, weak-limit agreement and order-one weak-control rejection. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G339_strong_field_redshift_substrate_boundary/G339_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G339_strong_field_redshift_substrate_boundary) |
| `G:G412@SAM-ARCHIVE` | Photon-sphere result | `G412_PHOTON_SPHERE_A_METRIC_BOUNDARY_PASS`; \(r_{\rm ph}=3r_s/2\) and \(b_c=3\sqrt3r_s/2\), with scope controls retained. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G412_PHOTON_SPHERE_A_METRIC_BOUNDARY/G412_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G412_PHOTON_SPHERE_A_METRIC_BOUNDARY) |
| `G:G413@SAM-ARCHIVE` | ISCO result | `G413_ISCO_A_METRIC_TIMELIKE_BOUNDARY_PASS`; \(r_{\rm ISCO}=3r_s\) and the registered nonrotating timelike packet. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G413_ISCO_A_METRIC_TIMELIKE_BOUNDARY/G413_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G413_ISCO_A_METRIC_TIMELIKE_BOUNDARY) |
| [`CR:CR007@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr007-strong-field-landmark-selector/README.md) | Structural boundary | Source execution `CLEAN`, scientific verdict `BOUNDARY`; exact zero-parameter landmark tuple and invariant ordering. | [result](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR/CR007_result.md) | [folder](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR) |
| [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | Locked-stack retest | `LC11_PASS_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY_FROM_LOCKED_PRIMITIVE_STACK`; 100/100 checks and 8/8 wrong controls. **The test result suggests strong contact with the concept.** | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY) |

## 11. Atomic record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000002-R001` | Supplies the spherical source lift \(A=r_s/r\). |
| `SAMA-C000040-R001` | Types \(A=1\) as the source-scale closure marker. |
| `SAMA-C000074-R001` | Defines \(x=r/r_s\) and \(A=1/x\). |
| `SAMA-C000075-R001` | Records the nonrotating landmark tuple. |
| `SAMA-C000076-R001` | Establishes mass invariance and the weak-formula domain boundary. |
| `SAMA-C000090-R001` | Supplies the locked-stack strong-field replay and scoped classification. |
| `SAMA-C000122-R001` | Enforces the Volume I subject and cross-volume boundary. |
| `SAMA-C000124-R001` | Separates source-era chronology from current live authority. |
| `SAMA-C000125-R001` | Preserves source statuses, authorized classification and false approval state. |

## 12. Source chronology and approval boundary

The six direct evidence keys above are individually registered. Archive
artifacts retain their executable verdict strings; Courtroom and Last Campaign
links are pinned to commit `b5e914f71377e86ef4c67e199973d9300795cda1`.
Source-era labels do not silently become current authority. Executable
artifacts control their numerical results, while active `SAM_LIVE` documents
control present-tense interpretation.

This is a Volume I coordinate chapter. Matter supplies the source at a typed
interface but its finite grammar remains Volume II. Executable internals remain
Volume III. No cross-volume ontology is imported by using their results.

`reviewed_and_approved` remains `false`; `approval` remains `null`. The exact
tuple, source replay, strong-contact classification and manuscript validation
do not constitute owner approval.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`CR:CR007@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr007-strong-field-landmark-selector/README.md) | [CR007_PRECOMMIT.md](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR/CR007_PRECOMMIT.md)<br>[CR007_declared_premises.json](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR/CR007_declared_premises.json) | [CR007_runner.py](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR/CR007_runner.py) | [CR007_candidate_rows.csv](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR/CR007_candidate_rows.csv) | [CR007_candidate_summary.csv](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR/CR007_candidate_summary.csv)<br>[CR007_result.md](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR/CR007_result.md)<br>[CR007_summary.json](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR/CR007_summary.json) | [All 10 files](../../tests/courtroom/05-strong-field-and-horizon-closure-cr007-strong-field-landmark-selector/README.md) |
| [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | [LC11_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_wrong_controls.csv) | [LC11_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_result.md)<br>[LC11_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_summary.json) | [All 11 files](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000013`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/STRONG_FIELD_A_COORDINATE.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000013 | Strong-Field Closure | Normalized Strong-Field A Coordinate and Landmark Tuple |

| Document field | Value |
|---|---|
| Purpose | Introduce the normalized nonrotating strong-field coordinate, derive the horizon/photon-sphere/ISCO tuple, establish its mass invariance, and enforce the boundary between coordinate continuity and weak-formula extrapolation. |
| Prerequisite documents | `SAMA-D000003` |
| Used by | `SAMA-D000014`, `SAMA-D000015`, `SAMA-D000016`, `SAMA-D000017`; focused child of `SAMA-P000002`. |
| Primary source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`, SHA-256 `2f22500f6583f567e350974610f00142e89b081a5b8c4c90c6dfe89bec43be0d`. |
| Revision state | Source-bound draft; mechanically registered proposal; not reviewed or approved. |

</details>
