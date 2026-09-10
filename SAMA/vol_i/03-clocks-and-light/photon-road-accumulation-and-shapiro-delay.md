[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Photon-Road Accumulation and Shapiro Delay

## Conceptual abstract

A clock reads accumulation at an endpoint. A photon samples accumulation along
its road. The local first-order photon functional is

\[
T_A^\gamma[\Gamma]
=\frac1c\int_\Gamma A_s(\mathbf x)\,ds.
\]

For an unperturbed straight road past a spherical source, with impact
parameter \(b\), longitudinal coordinate \(x\), and
\(r(x)=\sqrt{x^2+b^2}\), direct integration yields

\[
\Delta t_A
=\frac{r_s}{c}\left[
\operatorname{asinh}\left(\frac{x_1}{b}\right)
+\operatorname{asinh}\left(\frac{x_2}{b}\right)
\right],
\]

which is algebraically the first-order logarithmic Shapiro expression. The
impact parameter and full route geometry are therefore load-bearing. A pair
of endpoint values cannot reproduce the same shape.

The local road uses the source lift above the common background; integrating
the universal floor as a visible local source delay produces a spurious path-
scale term. Local \(c\) remains invariant. Multimessenger signals share the
same post-release road; a source-engine release delay is not a different
propagation speed.

## 1. Opening question and geometry

The technical question is:

> Can the fixed source lift \(A_s=r_s/r\), integrated over an explicitly
> declared path with no free amplitude, reproduce the first-order Shapiro road
> and its geometry dependence while endpoint-only, uniform-floor and
> variable-speed substitutes reject?

The conceptual picture is a chord passing a spherical source at impact
parameter \(b\). The field is sampled continuously along that chord, so the
road retains the whole route geometry rather than only its two endpoints.

Place the spherical source at the origin. Use the unperturbed straight path

\[
\mathbf x(x)=(x,b),
\]

where \(b>0\) is the closest approach. The radial distance is

\[
r(x)=\sqrt{x^2+b^2}.
\]

Let the emitter-side endpoint be at \(x=-x_1\) and the receiver-side
endpoint at \(x=x_2\), with \(x_1,x_2>0\). Their source-centered radii are

\[
r_1=\sqrt{x_1^2+b^2},
\qquad
r_2=\sqrt{x_2^2+b^2}.
\]

The projected endpoint separation on this straight road is

\[
R_{12}=x_1+x_2.
\]

Unlike an endpoint clock ratio, the road changes when \(b\) changes while
\(r_1\) and \(r_2\) remain fixed.

## 2. Typed definitions, domains and units

| Object | Definition | Type | Units |
|---|---|---|---|
| \(A_s(r)\) | \(r_s/r=2GM_s/(c^2r)\) | local source lift | dimensionless |
| \(\Gamma\) | declared photon route | oriented spatial path | m of line element |
| \(ds\) | path-length element | road measure | m |
| \(T_A^\gamma[\Gamma]\) | \(c^{-1}\int_\Gamma A_sds\) | first-order source-road exposure | s |
| \(b\) | closest-approach/impact parameter | geometric input | m |
| \(x_1,x_2\) | positive longitudinal endpoint distances | geometric inputs | m |
| \(r_1,r_2\) | source-centered endpoint radii | geometric inputs | m |
| \(r_s/c\) | \(2GM_s/c^3\) | road time scale | s |
| \(\omega T_A^\gamma\) | phase accumulated at angular frequency \(\omega\) | action/phase readout | radians |

The integral is first-order and local-source scoped. It is not the global
cosmological road, an exact strong-field null-geodesic derivation, or a new
local light-speed law.

## 3. Derive the straight-road integral

### 3.1 Insert the source field

Along the straight path,

\[
A_s(x)=\frac{r_s}{\sqrt{x^2+b^2}}.
\]

Because \(ds=dx\) on the chosen unperturbed longitudinal parameterization,

\[
\Delta t_A
=\frac1c\int_{-x_1}^{x_2}
 \frac{r_s}{\sqrt{x^2+b^2}}\,dx.
\]

Pull out the constants:

\[
\Delta t_A
=\frac{r_s}{c}\int_{-x_1}^{x_2}
 \frac{dx}{\sqrt{x^2+b^2}}.
\]

### 3.2 Obtain the antiderivative

For \(b>0\),

\[
\frac d{dx}\operatorname{asinh}\left(\frac xb\right)
=\frac{1/b}{\sqrt{1+(x/b)^2}}
=\frac1{\sqrt{x^2+b^2}}.
\]

Therefore

\[
\int\frac{dx}{\sqrt{x^2+b^2}}
=\operatorname{asinh}\left(\frac xb\right)+C.
\]

### 3.3 Evaluate the endpoints

\[
\begin{aligned}
\Delta t_A
&=\frac{r_s}{c}\left[
\operatorname{asinh}\left(\frac{x_2}{b}\right)
-\operatorname{asinh}\left(-\frac{x_1}{b}\right)
\right]\\
&=\frac{r_s}{c}\left[
\operatorname{asinh}\left(\frac{x_1}{b}\right)
+\operatorname{asinh}\left(\frac{x_2}{b}\right)
\right],
\end{aligned}
\]

because \(\operatorname{asinh}\) is odd.

The route coefficient is

\[
\frac{r_s}{c}=\frac{2GM_s}{c^3}.
\]

There is no endpoint-clock factor \(1/2\): the full source lift is
integrated along the path.

## 4. Convert the \(\operatorname{asinh}\) road to logarithmic form

### 4.1 Apply the elementary identity

\[
\operatorname{asinh}y=\ln\left(y+\sqrt{1+y^2}\right).
\]

With \(y=x_i/b\) and \(r_i=\sqrt{x_i^2+b^2}\),

\[
\operatorname{asinh}\left(\frac{x_i}{b}\right)
=\ln\left(\frac{x_i+r_i}{b}\right).
\]

The sum becomes

\[
\operatorname{asinh}\left(\frac{x_1}{b}\right)
+\operatorname{asinh}\left(\frac{x_2}{b}\right)
=\ln\left[\frac{(x_1+r_1)(x_2+r_2)}{b^2}\right].
\]

### 4.2 Express the same ratio in endpoint geometry

Using \(x_i^2=r_i^2-b^2\) and \(R_{12}=x_1+x_2\), direct
algebra gives

\[
\frac{(x_1+r_1)(x_2+r_2)}{b^2}
=\frac{r_1+r_2+R_{12}}{r_1+r_2-R_{12}}.
\]

Substitution yields the registered first-order logarithmic form

\[
\boxed{
\Delta t_A
=\frac{r_s}{c}
\ln\left(\frac{r_1+r_2+R_{12}}
                 {r_1+r_2-R_{12}}\right)
}.
\]

The equality of the two forms is a stringent implementation check: one comes
from direct path integration, the other from the endpoint/impact geometry.

## 5. Solar-system road example

[`CR:CR006@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr006-photon-road-shapiro-external-contact/README.md) uses an Earth-to-Cassini-style geometry with

\[
b=1.6R_\odot=1,113,120,000\ \mathrm m,
\]

and records

\[
r_s=2953.339382066878\ \mathrm m,
\]

\[
\int_\Gamma A_sds=39337.432118325312\ \mathrm m.
\]

Dividing by \(c\) gives

\[
\Delta t_A=131.215549519679\ \mu\mathrm s.
\]

The separately evaluated logarithmic form gives
\(131.215549519703\ \mu\mathrm s\), with registered relative
difference

\[
1.790952533800\times10^{-13}.
\]

The effective first-order PPN comparison is \(\gamma_{\rm eff}=1\), and
the maximum registered shape relative difference is
\(3.520710828705\times10^{-13}\). The wrong radial shape differs by as
much as \(0.7823263434636\) over the tested shape packet.

This source execution is `CLEAN` and its scientific verdict is `PASS` for the
scoped first-order solar-system road. No SAMA result classification is assigned
in this document; the later independent binary holdout owns the classified
road result.

## 6. Why endpoints and the universal floor cannot substitute

### 6.1 Fixed endpoints, different roads

For fixed \(r_1,r_2\), the endpoint lapse ratio is unchanged. But the road
contains \(b\):

\[
\Delta t_A(b)
=\frac{r_s}{c}\left[
\operatorname{asinh}(x_1/b)+\operatorname{asinh}(x_2/b)
\right].
\]

Increasing \(b\) lowers the near-source exposure. In
`G:G372@SAM-ARCHIVE`, changing \(b/R_\odot\) from \(1.6\) to
\(3.0\) changes the delay from
\(131.215549519679\ \mu\mathrm s\) to
\(118.830002084686\ \mu\mathrm s\). An endpoint-only estimate on a
symmetric configuration remains zero while the path delay is
\(110.214488630118\ \mu\mathrm s\).

### 6.2 The uniform floor is not a local source delay

If one incorrectly inserts the floor,

\[
\Delta t_{\rm wrong}\supset\frac{A_0}{c}\int_\Gamma ds
=\frac{A_0L_\Gamma}{c}.
\]

This grows with the arbitrary local path length even though the tested
question is the excess due to the spherical source. `G:G343@SAM-ARCHIVE`
records a uniform-floor baseline phase about
\(951106.972\) times the observable excess phase in its geometry. The
uniform floor remains part of the pointwise substrate account; it is
background-subtracted from this local source-delay operator.

## 7. Phase and bending consequences of the same road

### 7.1 Phase is a second typed readout

For angular frequency \(\omega\), the road phase is

\[
\phi_A=\omega T_A^\gamma.
\]

`G:G343@SAM-ARCHIVE` records a Cassini-style delay
\(1.3123688627870845\times10^{-4}\) s, path excess
\(39343.82871776048\) m, and identical time/path phase
\(6926519.675261585\) rad for its declared X-band frequency. Doubling
angular frequency doubles phase while leaving the underlying road time fixed.
Using ordinary frequency instead of angular frequency misses the phase by the
registered \(2\pi\) conversion.

### 7.2 Road gradient produces the weak bending corollary

`G:G407@SAM-ARCHIVE` applies the road/Fermat gradient and records

\[
\alpha_A=8.490267017584816\times10^{-6}\ \mathrm{rad}
=1.7512432813682448\ \mathrm{arcsec}
\]

for its solar-limb input, exactly matching its registered first-order
comparator. Doubling mass doubles the angle; doubling impact parameter halves
it. The endpoint-clock-only control gives zero bending. The source explicitly
limits this result to first-order weak-field bending rather than full lensing,
PPN closure, strong lensing or full GR.

## 8. Invariant \(c\) and the multimessenger boundary

The local propagation invariant remains

\[
c_{\rm local}=c.
\]

The delay is additional road exposure \(c^{-1}\int A_sds\), not a new
fundamental local speed. The coordinate shorthand \(c_{\rm eff}=c(1-A)\)
belongs to inferred road length and is developed fully in `SAMA-D000009`.

[`CR:CR147@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr147-gw170817-a-release-em-origin-differential/README.md) tests this boundary on GW170817. It records a dynamic source
release/engine delay of \(1.701457752729\) s against the observed
\(1.740000\pm0.050000\) s, with residual \(0.770845\) standard deviations.
The formal static local \(A\)-integral across its release gap is only
\(7.774813823799\times10^{-5}\) s and is rejected as the seconds-scale
mechanism. After release, electromagnetic and gravitational signals share the
same \(A\)-road. A different post-release speed, a one-sided 40 Mpc road, an
exact-mass fit and a literal photon launch from \(A=1\) are all rejected.

This result is routed here as an invariant-propagation boundary. Its source
mechanism and carrier theorem are not re-derived in this photon-road chapter.

## 9. Local photon-road construction and holdout

| Stage | Exact key | Contribution and preserved boundary |
|---|---|---|
| Phase construction | `G:G343@SAM-ARCHIVE` | Closed time/path phase identity and exposed the catastrophic uniform-floor baseline control. |
| Direct road construction | `G:G372@SAM-ARCHIVE` | Derived the \(\operatorname{asinh}\)/log road, mass and impact scalings, and endpoint-only rejection. |
| Fermat-gradient result | `G:G407@SAM-ARCHIVE` | Recovered first-order bending and achromatic road-gradient scaling without promoting full lensing. |
| Solar external contact | [`CR:CR006@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr006-photon-road-shapiro-external-contact/README.md) | Independently recertified the zero-fit solar road, logarithmic equality, shape and \(\gamma_{\rm eff}=1\). |
| Propagation boundary | [`CR:CR147@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr147-gw170817-a-release-em-origin-differential/README.md) | Separated dynamic release time from shared post-release road and rejected variable post-release speed. |
| Independent road holdout | [`CR:CR148@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr148-binary-pulsar-shapiro-road-holdout/README.md) | Applied the same fixed road coefficient to binary-pulsar timing geometry; its full classified result belongs to `SAMA-D000008`. |

The sequence retains every deviation. The early phase test shows why a
uniform background cannot be called observable source excess. The direct-road
test shows why endpoint redshift and local \(gH/c^2\) substitutions fail.
The multimessenger test shows why a static road cannot be stretched to explain
a dynamic release delay. The holdout then changes geometry without changing
the road amplitude.

## 10. Wrong controls and their failure modes

| Wrong control | Failure |
|---|---|
| No \(A\)-road | Gives zero excess delay. |
| Omit division by \(c\) | G343 records a phase miss by the factor-scale \(299792457\). |
| Use half source profile | Halves Shapiro delay or bending. |
| Drop logarithmic geometry | G372's substitute is about \(95.15\) times the target. |
| Use endpoint clock only | Cannot depend on impact parameter; symmetric endpoint estimate may be zero while road delay is nonzero. |
| Use surface \(gH/c^2\) over a solar-system road | G372 records a delay near \(7.91\) s instead of \(1.312\times10^{-4}\) s. |
| Integrate \(A_0\) as local source excess | Produces an enormous path-length baseline. |
| Use wrong radial power | Breaks the logarithmic shape and changes doubled-impact scaling. |
| Claim a new local speed law | Changes the invariant rather than the measurable road. |
| Explain GW170817 by static local road | Misses the seconds-scale lag by more than four orders of magnitude in the pinned event calculation. |
| Launch from exact \(A=1\) | Crosses the no-ordinary-escape boundary. |

## 11. Established result, boundary and forward handoff

The compression-safe local photon packet is

\[
\boxed{
T_A^\gamma[\Gamma]
=\frac1c\int_\Gamma A_sds
}
\]

and, for the declared straight spherical-source road,

\[
\boxed{
\Delta t_A
=\frac{r_s}{c}\left[
\operatorname{asinh}(x_1/b)+\operatorname{asinh}(x_2/b)
\right]
=\frac{r_s}{c}\ln\left(\frac{r_1+r_2+R_{12}}
                                      {r_1+r_2-R_{12}}\right)
}.
\]

The uniform floor is not a visible local source-delay term, the endpoint
clock coefficient is not applied, and local \(c\) remains invariant. No SAMA
result classification is assigned here. `SAMA-D000008` receives the same road
coefficient for the independent binary-pulsar holdout.

Exact evidence is the complete registered sequence in Section 12. The
specifically open boundary is independent-system holdout evidence, higher-order
or nonstraight routes and exact strong-field traversal; none is supplied by
the first-order local road alone.

## 12. Focused test and result index

| Exact qualified key | Evidence role | Preserved outcome | Direct result | Result folder |
|---|---|---|---|---|
| `G:G343@SAM-ARCHIVE` | Phase-road construction | `G343_SHAPIRO_PHOTON_SUBSTRATE_PHASE_PASS` | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G343_shapiro_photon_substrate_phase/G343_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G343_shapiro_photon_substrate_phase) |
| `G:G372@SAM-ARCHIVE` | Direct road construction | `G372_SAM_SHAPIRO_A_PATH_DELAY_PASS` | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G372_SAM_SHAPIRO_A_PATH_DELAY/G372_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G372_SAM_SHAPIRO_A_PATH_DELAY) |
| `G:G407@SAM-ARCHIVE` | Fermat-road result | `G407_PHOTON_A_ROAD_FERMAT_LIGHT_BENDING_PASS` | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G407_PHOTON_A_ROAD_FERMAT_LIGHT_BENDING/G407_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G407_PHOTON_A_ROAD_FERMAT_LIGHT_BENDING) |
| [`CR:CR006@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr006-photon-road-shapiro-external-contact/README.md) | Solar external result | Source execution `CLEAN`, scientific verdict `PASS`; zero-fit first-order Shapiro road and shape. | [result](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_result.md) | [folder](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT) |
| [`CR:CR147@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr147-gw170817-a-release-em-origin-differential/README.md) | Invariant-propagation boundary | Source execution `CLEAN`, scientific verdict `PASS`; dynamic release time and shared post-release road. | [result](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/CR147_result.md) | [folder](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL) |
| [`CR:CR148@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr148-binary-pulsar-shapiro-road-holdout/README.md) | Independent road holdout handoff | Registry has no structured status/verdict; pinned source records `PASS_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT`. | [result](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_result.md) | [folder](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT) |

## 13. Atomic record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000003-R001` | Separates endpoint clock from photon road. |
| `SAMA-C000036-R001` | Types local background subtraction versus global floor retention. |
| `SAMA-C000053-R001` | Defines the local photon-road functional. |
| `SAMA-C000054-R001` | Records the straight-road \(\operatorname{asinh}\) and logarithmic identity. |
| `SAMA-C000055-R001` | Records the solar-system external-contact packet. |
| `SAMA-C000056-R001` | Preserves endpoint-only and universal-floor road controls. |
| `SAMA-C000122-R001` | Enforces the Volume I/II/III subject boundary. |
| `SAMA-C000124-R001` | Separates source-era chronology from current live authority. |
| `SAMA-C000125-R001` | Preserves source verdicts, authorized classifications and false approval state. |

## 14. Source and approval boundary

The direct evidence set is exactly the six qualified keys above. Courtroom
links are pinned to commit `b5e914f71377e86ef4c67e199973d9300795cda1`;
archive links resolve to the exact registry artifacts. Source `PASS` and
historical “latest” wording remain provenance unless current live authority
installs a present-tense statement.

`reviewed_and_approved` remains `false`; `approval` remains `null`. Road
contact, invariant-\(c\) boundary checks and manuscript validation do not
constitute owner approval.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`CR:CR006@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr006-photon-road-shapiro-external-contact/README.md) | [CR006_PRECOMMIT.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_PRECOMMIT.md)<br>[CR006_declared_premises.json](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_declared_premises.json) | [CR006_runner.py](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_runner.py) | [CR006_candidate_rows.csv](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_candidate_rows.csv)<br>[CR006_wrong_radial_shape_rows.csv](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_wrong_radial_shape_rows.csv) | [CR006_result.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_result.md)<br>[CR006_summary.json](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_summary.json) | [All 10 files](../../tests/courtroom/04-photon-road-shapiro-delay-cr006-photon-road-shapiro-external-contact/README.md) |
| [`CR:CR147@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr147-gw170817-a-release-em-origin-differential/README.md) | [All package files](../../tests/courtroom/04-photon-road-shapiro-delay-cr147-gw170817-a-release-em-origin-differential/README.md) | [CR147_runner.py](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/CR147_runner.py) | [CR147_wrong_controls.csv](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/CR147_wrong_controls.csv) | [CR147_result.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/CR147_result.md)<br>[CR147_summary.json](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/CR147_summary.json) | [All 13 files](../../tests/courtroom/04-photon-road-shapiro-delay-cr147-gw170817-a-release-em-origin-differential/README.md) |
| [`CR:CR148@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr148-binary-pulsar-shapiro-road-holdout/README.md) | [CR148_PRECOMMIT.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_PRECOMMIT.md)<br>[CR148_PRECOMMIT.sha256](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_PRECOMMIT.sha256)<br>[CR148_PREFLIGHT.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_PREFLIGHT.md) | [CR148_runner.py](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_runner.py) | [CR148_wrong_controls.csv](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_wrong_controls.csv)<br>[CR148_wrong_controls.csv](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/FAILED_RUN_20260711_173452_VALIDATION_BOOLEAN_BUG/CR148_wrong_controls.csv) | [CR148_SOURCE_AUDIT.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_SOURCE_AUDIT.md)<br>[CR148_result.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_result.md)<br>[CR148_summary.json](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_summary.json)<br>[CR148_result.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/FAILED_RUN_20260711_173452_VALIDATION_BOOLEAN_BUG/CR148_result.md)<br>[CR148_summary.json](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/FAILED_RUN_20260711_173452_VALIDATION_BOOLEAN_BUG/CR148_summary.json) | [All 50 files](../../tests/courtroom/04-photon-road-shapiro-delay-cr148-binary-pulsar-shapiro-road-holdout/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000007`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/PHOTON_ROAD_ACCUMULATION_AND_SHAPIRO_DELAY.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000007 | Clock and Traversal | Local Photon-Road Integral, Closed Forms and Shapiro Contact |

| Document field | Value |
|---|---|
| Purpose | Derive the local photon-road functional and its \(\operatorname{asinh}\)/logarithmic forms, then route solar-system contact, endpoint controls, invariant propagation and the binary-pulsar handoff. |
| Prerequisite documents | `SAMA-D000003`, `SAMA-D000004` |
| Used by | `SAMA-D000008`, `SAMA-D000009`, `SAMA-D000010`; assembled into `SAMA-P000005` and `SAMA-P000002`. |
| Primary source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`, SHA-256 `2f22500f6583f567e350974610f00142e89b081a5b8c4c90c6dfe89bec43be0d`. |
| Revision state | Source-bound draft; mechanically registered proposal; not reviewed or approved. |

</details>
