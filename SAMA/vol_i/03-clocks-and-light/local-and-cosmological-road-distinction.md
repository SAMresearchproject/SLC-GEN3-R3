[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Local Road and Cosmological Road Distinction

## Conceptual abstract

The word *road* names a route-sensitive readout, but it does not make every
route operator identical. A local Shapiro road begins with a specified source
mass, constructs its lift \(A_s(\mathbf x)\), and integrates that lift along a
specified spatial path. A cosmological road begins with redshift and the
global accumulation account

\[
A_{\rm los}(z)=A_0R\left[1-(1+z)^{-D}\right].
\]

The two lanes share the same discipline: locally measured \(c\) remains
invariant, and accumulation modifies the measurable track. They differ in
their inputs, domains and operators. The global road is not obtained by
integrating the uniform floor over an arbitrary Euclidean distance, and it is
not a host-galaxy mass correction. Keeping that type boundary intact is what
allows the supernova, BAO and fate-distance chapters to reuse one global road
without corrupting the independently established local photon road.

## 1. Opening question

This chapter asks:

> How can Volume I use one accumulation language for local photon delays and
> cosmological distance conversion while retaining the exact construction,
> limits and evidentiary boundary of each road?

The answer has three parts:

1. identify the source and coordinate domain before writing an observable;
2. derive each operator from its own declared inputs; and
3. permit a shared interpretation only after the two typed maps are complete.

The shared interpretation is the invariant-tooth-rate picture of
`SAMA-D000009`: \(c_{\rm local}=c\), while an accumulated track can have a
different native length than its conventional readout coordinate.

The conceptual picture places two maps side by side: a finite path through a
localized source field and a redshift-indexed global road. They share an
accumulation vocabulary and invariant local \(c\), but their inputs, domains,
integrals and boundary values remain different.

## 2. Typed definitions, domains and units

| Symbol | Definition | Type | Units/domain |
|---|---|---|---|
| \(A_0\) | \(1/(\pi R)=1/(12\pi)\) | universal substrate floor | dimensionless |
| \(A_s(\mathbf x)\) | \(2GM_s/(c^2|\mathbf x-\mathbf x_s|)\) | local spherical-source lift | dimensionless, spatial domain |
| \(\Gamma\) | declared local photon path | local route geometry | length-parametrized curve |
| \(T_A^\gamma[\Gamma]\) | \(c^{-1}\int_\Gamma A_sds\) | local excess road time | seconds |
| \(z\) | observed redshift tag | cosmological route coordinate | \(z\ge0\) |
| \(A_{\rm los}(z)\) | \(A_0R[1-(1+z)^{-D}]\) | global line-of-sight account | dimensionless |
| \(c_{\rm eff}(z)\) | \(c[1-A_{\rm los}(z)]\) | coordinate traversal shorthand | speed units |
| \(D_{\rm readout}\) | distance inferred in the declared conventional coordinate | catalog/readout distance | Mpc or other length |
| \(D_{\rm native}\) | \(D_{\rm readout}[1-A_{\rm los}(z)]\) | substrate-native distance | same length unit |

The floor belongs to the pointwise total account, but operator treatment is
explicit:

\[
A_{\rm total}(\mathbf x)=A_0+A_{\rm lift}(\mathbf x).
\]

A gradient removes \(A_0\) because \(\nabla A_0=0\). A shared endpoint
difference cancels it. A local source-excess road background-subtracts it.
The cosmological line-of-sight construction can retain the floor through the
separate product \(A_0R\). These are operator decisions, not competing values
of the substrate state.

## 3. Construct the local source road from start to finish

For one spherical source of mass \(M_s\), first form its length scale

\[
r_s=\frac{2GM_s}{c^2}.
\]

The source lift at radius \(r\) is then

\[
A_s(r)=\frac{r_s}{r}=\frac{2GM_s}{c^2r}.
\]

Only now is the route operator applied:

\[
T_A^\gamma[\Gamma]
=\frac1c\int_\Gamma A_s(\mathbf x)\,ds
=\frac{2GM_s}{c^3}\int_\Gamma\frac{ds}{r(\mathbf x)}.
\]

The prefactor has units of time,

\[
\left[\frac{GM_s}{c^3}\right]=\mathrm s,
\]

and the remaining integral is dimensionless. For the straight-line geometry
developed in `SAMA-D000007`, \(r(x)=\sqrt{x^2+b^2}\), giving

\[
T_A^\gamma
=\frac{r_s}{c}
\left[\operatorname{asinh}\left(\frac{x_1}{b}\right)
     +\operatorname{asinh}\left(\frac{x_2}{b}\right)\right].
\]

The impact parameter \(b\) is load-bearing: fixed endpoints with a changed
near-source path give a changed road. An endpoint lapse cannot reproduce this
dependence. [`CR:CR006@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr006-photon-road-shapiro-external-contact/README.md) records the scoped solar result
\(131.215549519679\ \mu\mathrm{s}\), a logarithmic-form relative difference
\(1.790952533800\times10^{-13}\), and rejection of the endpoint-only and
wrong-radial-shape controls.

## 4. Construct the cosmological road from start to finish

The global input is not a source mass and not a Euclidean path length. It is
the redshift-tagged line-of-sight account

\[
A_{\rm los}(z)=A_0R\left[1-(1+z)^{-D}\right].
\]

Insert the locked Volume I values

\[
A_0=\frac1{\pi R},\qquad R=12,qquad D=3.
\]

The radix cancels only inside the declared global product:

\[
A_0R=\frac1{\pi R}R=\frac1\pi.
\]

Therefore

\[
\boxed{
A_{\rm los}(z)=\frac1\pi\left[1-(1+z)^{-3}\right]
}.
\]

### 4.1 Origin value

At \(z=0\),

\[
A_{\rm los}(0)
=\frac1\pi(1-1)=0.
\]

The cosmological conversion therefore has no fixed nonzero local offset.

### 4.2 Low-redshift slope

Differentiate before substituting \(z=0\):

\[
\frac{dA_{\rm los}}{dz}
=\frac1\pi\frac{d}{dz}\left[1-(1+z)^{-3}\right]
=\frac3\pi(1+z)^{-4}.
\]

Hence

\[
\left.\frac{dA_{\rm los}}{dz}\right|_{z=0}=\frac3\pi.
\]

The binomial expansion makes the same result visible:

\[
(1+z)^{-3}=1-3z+6z^2-10z^3+\cdots,
\]

so

\[
A_{\rm los}(z)=\frac3\pi z-\frac6\pi z^2
+\frac{10}\pi z^3+\cdots.
\]

### 4.3 High-redshift ceiling

Since \((1+z)^{-3}\rightarrow0\) as \(z\rightarrow\infty\),

\[
\boxed{
\lim_{z\to\infty}A_{\rm los}(z)=\frac1\pi
}.
\]

The road grows monotonically because its derivative is positive for every
\(z\ge0\), yet it remains bounded. Its surviving fraction obeys

\[
1-A_{\rm los}(z)\ge1-\frac1\pi>0.
\]

This boundedness is the technical distinction between the global operator and
the wrong uniform-floor integral \(A_0L/c\), which grows without limit with an
arbitrarily chosen local path length.

## 5. From accumulated road to coordinate distance

The coordinate shorthand is

\[
c_{\rm eff}(z)=c[1-A_{\rm los}(z)].
\]

Divide by the invariant local value \(c\):

\[
\frac{c_{\rm eff}(z)}c=1-A_{\rm los}(z).
\]

The distance identity assigns that ratio to two representations of the same
declared road:

\[
\boxed{
\frac{D_{\rm native}(z)}{D_{\rm readout}(z)}
=\frac{c_{\rm eff}(z)}c
=1-A_{\rm los}(z)
}.
\]

Thus

\[
D_{\rm native}(z)
=D_{\rm readout}(z)
\left\{1-\frac1\pi\left[1-(1+z)^{-3}\right]\right\}.
\]

At \(z=0\), native and readout distances coincide. At saturation their ratio
approaches \(1-1/\pi\). Neither statement changes the local invariant \(c\).

`G:G688c@SAM-ARCHIVE` evaluated this chain over 1,701 supernova rows and
recorded a maximum identity error of
\(1.136868377216\times10^{-13}\) Mpc. `G:G693c@SAM-ARCHIVE` applied the
same conversion to BAO coordinate distances and also exposed a further type
boundary: a common speed factor is insufficient for an anisotropic radial
observable, whose derivative projection must be applied after the shared road
conversion.

## 6. Local/global road type boundary

| Question | Local photon road | Cosmological line-of-sight road |
|---|---|---|
| What initiates the calculation? | source mass and source location | observed redshift and locked global packet |
| What field is consumed? | \(A_s(\mathbf x)=2GM_s/(c^2r)\) | \(A_{\rm los}(z)=(1/\pi)[1-(1+z)^{-3}]\) |
| What operator acts? | \(c^{-1}\int_\Gamma A_sds\) | multiplication by \(1-A_{\rm los}(z)\), followed by the observable-specific projection |
| What geometry matters? | explicit spatial path and impact parameter | redshift history and transverse/radial observable family |
| What happens to \(A_0\)? | background-subtracted from local source excess | retained through \(A_0R\) |
| What remains invariant? | local \(c\) | local \(c\) |
| What is excluded? | endpoint-only and uniform-floor substitutions | host-mass correction and naive Euclidean floor integral |

The common phrase “photon road” therefore indicates a family resemblance,
not an algebraic license to exchange the two formulas. A local solar path does
not determine \(A_{\rm los}(z)\). Conversely, the redshift road cannot be
inserted into a solar-system path integral as though \(z\) were a local radial
coordinate.

The evidence chain makes this construction order explicit:

| Sequence | Exact key | Role | Contribution |
|---:|---|---|---|
| 1 | `G:G688c@SAM-ARCHIVE` | construction | Builds \(z\mapsto A_{\rm los}\mapsto c_{\rm eff}\mapsto D_{\rm native}\). |
| 2 | `G:G693c@SAM-ARCHIVE` | construction | Carries the same distance conversion into BAO and exposes the derivative-projection boundary. |
| 3 | [`CR:CR006@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr006-photon-road-shapiro-external-contact/README.md) | premise | Supplies the independently executed local source-road comparator. |
| 4 | [`CR:CR013@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr013-sn-luminosity-ledger-shrinkage/README.md) | construction | Recomputes the global road identities over all 1,701 registered SN rows. |
| 5 | [`CR:CR017@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr017-distance-road-typed-bridge-closure/README.md) | boundary | Closes the typed distance branch while retaining CMB modal and polarization work as open. |
| 6 | [`LC:LC07`](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md) | retest | Replays the road from the locked primitive stack and rejects mutation and leakage controls. |

## 7. Deviation chains and wrong controls

### 7.1 Uniform floor multiplied by local path length

The wrong construction

\[
T_{\rm wrong}=\frac{A_0L_\Gamma}{c}
\]

turns an arbitrary coordinate length into a source delay. It neither contains
the source mass nor the near-source geometry and grows without the global
\(1/\pi\) ceiling. The correction is to background-subtract the floor for the
local source-excess question and retain it only through the declared global
operator.

### 7.2 Host-galaxy mass term

Adding a host stellar-mass correction to \(A_{\rm los}(z)\) changes the
line-of-sight operator into a source-environment fit. The supernova chain does
not require that term: the registered appeal uses no host-mass correction.
The correction is to keep host data outside this operator unless a distinct
test declares a separate source question.

### 7.3 Endpoint clock coefficient on a photon road

The weak endpoint comparison begins at \(\Delta A/2\). The photon road is
\(c^{-1}\int A_sds\) and carries no inserted one-half. Moving the clock
coefficient into either local or global road erases the observable type.

### 7.4 Literal variable local light speed

Interpreting \(c_{\rm eff}=c(1-A)\) as \(c_{\rm local}\ne c\) changes the
meaning of the shorthand and conflicts with the invariant local lane. The
correction is to read \(c_{\rm eff}/c\) as a coordinate-distance ratio.

### 7.5 Speed-only BAO anisotropy

At fixed \(z\), a common multiplicative road factor cancels from a ratio such
as \(F_{AP}=D_M/D_H\). `G:G693c@SAM-ARCHIVE` records poor speed-only pulls
but a much smaller derivative-projection packet. The correction is not a new
road coefficient; it is to apply the radial observable's derivative operator.

### 7.6 Refitting the dimension or selecting bins

[`LC:LC07`](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md) locks \(D=3\), replays all 1,701 SN rows and all 19 BAO rows, and
rejects the \(D=2\), row deletion, target substitution and shared-ledger
controls. The retest preserves the global road by reconstructing it from the
locked stack rather than selecting a favorable subset.

## 8. Established boundary and forward handoff

This chapter establishes the typed distinction

\[
\boxed{
T_A^\gamma[\Gamma]=\frac1c\int_\Gamma A_sds
\quad\ne\quad
A_{\rm los}(z)=\frac1\pi[1-(1+z)^{-3}]
}
\]

while preserving the common coordinate interpretation

\[
\boxed{
c_{\rm local}=c,
\qquad
D_{\rm native}=D_{\rm readout}(1-A_{\rm los}).
}
\]

No SAMA result classification is assigned in this distinction chapter.
`SAMA-D000011` receives the global distance operator for supernova luminosity
distance. `SAMA-D000012` receives the independently projected BAO and acoustic
ruler lanes. `SAMA-D000023` receives the \(1/\pi\) saturation value for the
fate readout. Local Shapiro evidence remains owned by `SAMA-D000007` and
`SAMA-D000008`.

Exact evidence is the complete registered sequence in Section 9. The
specifically open boundary is every application-specific projection after
road construction, including supernova, BAO, acoustic and future-direction
readouts under their own declared operators.

## 9. Focused test and result index

| Exact qualified key | Evidence role | Preserved outcome | Direct result | Result folder |
|---|---|---|---|---|
| `G:G688c@SAM-ARCHIVE` | Global-road construction | `G688c_PASS_Z_A_EFFECTIVE_LIGHT_SPEED_RULER_BUILDS_NATIVE_DISTANCE_LANE`; 1,701 rows and \(1.1369\times10^{-13}\) Mpc maximum identity error. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G688c_Z_A_EFFECTIVE_LIGHT_SPEED_RULER/G688c_RESULT.md) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G688c_Z_A_EFFECTIVE_LIGHT_SPEED_RULER) |
| `G:G693c@SAM-ARCHIVE` | BAO construction/boundary | `G693c_PASS_C_EFF_CONVERSION_FLATTENS_BAO_WITH_RADIAL_DERIVATIVE_BOUNDARY`; shared conversion retained and derivative projection required. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G693c_BAO_EXPLICIT_C_EFF_NATIVE_DISTANCE_CONVERSION/G693c_RESULT.md) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G693c_BAO_EXPLICIT_C_EFF_NATIVE_DISTANCE_CONVERSION) |
| [`CR:CR006@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr006-photon-road-shapiro-external-contact/README.md) | Local-road premise | Source execution `CLEAN`, scientific verdict `PASS`; scoped first-order solar source road. | [result](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_result.md) | [folder](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT) |
| [`CR:CR013@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr013-sn-luminosity-ledger-shrinkage/README.md) | Global SN construction | Source execution `CLEAN`, scientific verdict `PASS`; 1,701 exact road, distance and modulus rows. | [result](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_result.md) | [folder](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE) |
| [`CR:CR017@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr017-distance-road-typed-bridge-closure/README.md) | Typed closure boundary | Source execution `CLEAN`, scientific verdict `PASS`; branch closure with CMB modal/polarization left open. | [result](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_result.md) | [folder](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE) |
| [`LC:LC07`](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md) | Locked-stack retest | `LC07_PASS_SN_BAO_DISTANCE_ROAD_REPLAY_FROM_LOCKED_PRIMITIVE_STACK`; 113/113 checks and 10/10 wrong controls. | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY) |

## 10. Atomic record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000003-R001` | Separates clock endpoints from photon routes. |
| `SAMA-C000004-R001` | Types \(c_{\rm eff}\) as a coordinate readout. |
| `SAMA-C000036-R001` | Governs floor cancellation, subtraction and global retention. |
| `SAMA-C000060-R001` | Supplies the effective traversal distance identity. |
| `SAMA-C000062-R001` | Defines the global line-of-sight road. |
| `SAMA-C000063-R001` | Derives the origin value, low-\(z\) slope and \(1/\pi\) ceiling. |
| `SAMA-C000064-R001` | Enforces the local/global construction boundary. |
| `SAMA-C000122-R001` | Enforces the Volume I subject and cross-volume boundary. |
| `SAMA-C000124-R001` | Separates source-era chronology from current live authority. |
| `SAMA-C000125-R001` | Preserves source statuses, result-language law and false approval state. |

## 11. Source chronology and approval boundary

The August 11 Volume I spine is an immutable source-bound synthesis and the
six exact evidence keys above route to pinned artifacts. Words such as
“latest,” “current” or “strongest” inside those source-era artifacts are
historical chronology unless active `SAM_LIVE` authority separately installs
them as present-tense statements. Executable artifacts remain numerical
authority for their own recorded results.

Volume I owns the road types and gravitational readouts. Matter-source grammar
remains Volume II, and the internals of any executable engine remain Volume
III. This chapter consumes their outputs only at the typed interface.

`reviewed_and_approved` remains `false`; `approval` remains `null`. Exact
derivation, source hashes, successful executions and mechanical validation do
not constitute owner approval.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`CR:CR006@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr006-photon-road-shapiro-external-contact/README.md) | [CR006_PRECOMMIT.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_PRECOMMIT.md)<br>[CR006_declared_premises.json](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_declared_premises.json) | [CR006_runner.py](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_runner.py) | [CR006_candidate_rows.csv](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_candidate_rows.csv)<br>[CR006_wrong_radial_shape_rows.csv](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_wrong_radial_shape_rows.csv) | [CR006_result.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_result.md)<br>[CR006_summary.json](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_summary.json) | [All 10 files](../../tests/courtroom/04-photon-road-shapiro-delay-cr006-photon-road-shapiro-external-contact/README.md) |
| [`CR:CR013@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr013-sn-luminosity-ledger-shrinkage/README.md) | [CR013_PRECOMMIT.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_PRECOMMIT.md)<br>[CR013_declared_premises.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_declared_premises.json) | [CR013_runner.py](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_runner.py) | [CR013_candidate_rows.csv](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_candidate_rows.csv) | [CR013_result.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_result.md)<br>[CR013_summary.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_summary.json) | [All 8 files](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr013-sn-luminosity-ledger-shrinkage/README.md) |
| [`CR:CR017@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr017-distance-road-typed-bridge-closure/README.md) | [CR017_PRECOMMIT.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_PRECOMMIT.md)<br>[CR017_declared_premises.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_declared_premises.json) | [CR017_runner.py](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_runner.py) | [CR017_candidate_rows.csv](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_candidate_rows.csv) | [CR017_result.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_result.md)<br>[CR017_summary.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_summary.json) | [All 10 files](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr017-distance-road-typed-bridge-closure/README.md) |
| [`LC:LC07`](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md) | [LC07_bao_candidate_rows.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_bao_candidate_rows.csv)<br>[LC07_cmb_candidate_rows.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_cmb_candidate_rows.csv)<br>[LC07_sn_bao_independent_candidate_rows.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_sn_bao_independent_candidate_rows.csv)<br>[LC07_sn_candidate_rows.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_sn_candidate_rows.csv)<br>[LC07_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_wrong_controls.csv) | [LC07_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_result.md)<br>[LC07_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_summary.json) | [All 17 files](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000010`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/LOCAL_AND_COSMOLOGICAL_ROAD_DISTINCTION.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000010 | Clock and Traversal | Locally Sourced Roads versus the Global Cosmological Road |

| Document field | Value |
|---|---|
| Purpose | Keep a source-conditioned local photon road distinct from the separately constructed cosmological line-of-sight road, then derive the global road's limits, coordinate-distance readout, controls and evidence chain. |
| Prerequisite documents | `SAMA-D000007`, `SAMA-D000009` |
| Used by | `SAMA-D000011`, `SAMA-D000023`; focused child of `SAMA-P000002` and methodology child of `SAMA-P000005`. |
| Primary source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`, SHA-256 `2f22500f6583f567e350974610f00142e89b081a5b8c4c90c6dfe89bec43be0d`. |
| Revision state | Source-bound draft; mechanically registered proposal; not reviewed or approved. |

</details>
