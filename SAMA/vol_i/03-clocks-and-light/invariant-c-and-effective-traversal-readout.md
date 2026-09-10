[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Invariant c and Effective Traversal Readout

## Conceptual abstract

SAM keeps the locally measured light-speed invariant at \(c\). What changes in
an accumulation field is the measurable track: the road used to infer a
distance can be accumulated, compressed or stretched relative to an
unmodified coordinate convention. The shorthand

\[
c_{\rm eff}=c(1-A)
\]

expresses that coordinate or inferred-distance conversion. It does not assign
a new local propagation speed to light. This type boundary allows the same
accumulation structure to support endpoint clocks, photon-road delays,
multimessenger propagation and cosmological distance conversion without
silently identifying those distinct readouts.

## 1. Opening question and conceptual picture

This chapter answers:

> How can the same accumulation field preserve the locally measured invariant
> \(c\), generate the coordinate shorthand \(c_{\rm eff}=c(1-A)\), and feed
> endpoint-clock, local photon-road, multimessenger, cosmological-distance and
> strong-field lanes without substituting one lane's operator into another?

The source field is the dimensionless accumulation lift

\[
A(r)=\frac{r_s}{r}=\frac{2GM}{c^2r}.
\]

An observable is obtained only after an operator is assigned to that field.
A clock reads an endpoint lapse, a photon reads a route, and a distance catalog
records a coordinate inference. The symbol \(c_{\rm eff}\) belongs to the last
of these roles: it packages how an accumulation-conditioned road is represented
inside a conventional distance coordinate.

The physical picture is a tooth-rate and a track. The substrate tooth-rate is
locally invariant at \(c\); accumulation changes the measurable track. A
shorter native road represented by an unchanged readout convention can be
written as an effective coordinate rate below \(c\), but no local experiment
has been assigned a different invariant light-speed.

The typed construction is

\[
\text{accumulation field}
\longrightarrow
\text{declared road aggregate}
\longrightarrow
\frac{D_{\rm native}}{D_{\rm readout}}=1-A
\longleftrightarrow
\frac{c_{\rm eff}}c,
\]

while the local invariant remains \(c_{\rm local}=c\). Endpoint lapse and
route integration branch from the same field but do not pass through the
\(c_{\rm eff}\) shorthand as though it were a fundamental constant.

## 2. Definitions and type boundaries

### 2.1 Local invariant

The local statement is

\[
c_{\rm local}=c.
\]

This remains the invariant in every accumulation environment. Consequently,
\(c_{\rm eff}\) must not be substituted into local relativistic laws as a
position-dependent fundamental constant.

### 2.2 Effective traversal shorthand

For an accumulation value or declared route aggregate \(A\), the coordinate
shorthand is

\[
c_{\rm eff}=c(1-A),
\qquad
\frac{D_{\rm native}}{D_{\rm readout}}=\frac{c_{\rm eff}}c=1-A.
\]

The equality types a distance conversion. It says that a road inferred under
an unmodified convention differs from the native substrate road.

### 2.3 Endpoint clocks are separate

For a static endpoint clock,

\[
\frac{d\tau}{dt}=\sqrt{1-A}.
\]

Its weak comparison begins at \(\Delta A/2\). Applying that coefficient to a
photon road is a type error.

### 2.4 Photon roads are route integrals

A local photon road uses

\[
T_A^\gamma[\Gamma]=\frac1c\int_\Gamma A_s(\mathbf x)\,ds.
\]

The route samples the source lift along \(\Gamma\). It is not determined by one
endpoint value, and the uniform universal floor is not inserted as a visible
local source delay.

### 2.5 Cosmological roads use a declared line-of-sight account

The settled Volume I global road is

\[
A_{\rm los}(z)
=A_0R\left[1-(1+z)^{-D}\right]
=\frac1\pi\left[1-(1+z)^{-3}\right],
\]

with

\[
c_{\rm eff}(z)=c[1-A_{\rm los}(z)],
\qquad
D_{\rm native}(z)=D_{\rm readout}(z)[1-A_{\rm los}(z)].
\]

This line-of-sight operator vanishes at \(z=0\) and saturates at \(1/\pi\).
It is a global measurable-road conversion, not a host-mass correction and not
the integral of a uniform \(A_0\) across a Euclidean local path.

## 3. Technical development

For luminosity distance, the coordinate conversion propagates to the distance
modulus through

\[
\mu_{\rm native}
=\mu_{\rm obs}+5\log_{10}[1-A_{\rm los}(z)].
\]

The same factor may enter a declared transverse or radial ruler lane, but the
operator applied after that conversion remains typed. In particular, a common
speed factor at fixed redshift does not replace the derivative projection
needed by an anisotropic Alcock--Paczyński readout.

The local and global roads therefore share one invariant interpretation but
not one interchangeable formula:

| Lane | Accumulation input | Readout |
|---|---|---|
| Endpoint clock | endpoint values | lapse ratio |
| Local photon road | source lift along \(\Gamma\) | \(c^{-1}\int_\Gamma A_s ds\) |
| Coordinate traversal | declared \(A\) or route aggregate | \(c_{\rm eff}/c=1-A\) |
| Cosmological distance | \(A_{\rm los}(z)\) | \(D_{\rm native}=D_{\rm readout}(1-A_{\rm los})\) |
| Strong-field exterior road | \(A=r_s/r\) | radial traversal outside the closure boundary |

At exact \(A=1\), the ordinary effective coordinate rate vanishes. Volume I
therefore treats \(A=1\) as a no-ordinary-escape closure boundary, not as a
normal photon launch point with a slower local value of \(c\).

## 4. Connections across SAM

### 4.1 Accumulation floor and source lift

`SAMA-D000002` supplies the universal floor and `SAMA-D000003` supplies the
local source lift. The floor remains part of the total substrate account while
each readout declares whether a common contribution cancels, is background-
subtracted or enters through a separate global operator.

### 4.2 Time and local traversal

`SAMA-D000005` owns endpoint-clock comparison and `SAMA-D000007` owns the
local photon-road integral. Their separation is the type firewall that makes
\(c_{\rm eff}\) readable without turning it into a local variable light-speed.

### 4.3 Supernovae, BAO and acoustic roads

`SAMA-D000010` separates local and cosmological roads. `SAMA-D000011` and
`SAMA-D000012` carry the full supernova and BAO applications. This document
owns the common coordinate-conversion meaning; it does not absorb the full
datasets, ruler construction or compressed-acoustic analysis from those
documents.

### 4.4 Multimessenger propagation

The CR147 source record assigns the observed GW170817 seconds-scale lag to a
local dynamic release or source-engine reorganization. After release, the
electromagnetic and gravitational channels share the same \(A\)-road. A
different post-release propagation speed is rejected by that packet.

### 4.5 Strong-field closure

`SAMA-D000014` receives the invariant-\(c\) boundary and develops exterior
traversal near \(A=1\). The vanishing coordinate shorthand at closure does not
authorize a literal local \(c\mapsto0\) substitution.

## 5. Test evidence and results

### 5.1 Historical direct constructions

G688c constructed the explicit \(z\mapsto A_{\rm los}\mapsto c_{\rm eff}\)
ruler over 1,701 supernova rows. It recorded maximum distance-identity error
\(1.1369\times10^{-13}\) Mpc and reduced the reported centered RMS from
\(0.201750\) mag to \(0.146364\) mag. Its preserved source result is
`G688c_PASS_Z_A_EFFECTIVE_LIGHT_SPEED_RULER_BUILDS_NATIVE_DISTANCE_LANE`.

G693c applied the same explicit conversion to the declared BAO lanes. It
reported mean absolute row residual changing from \(29.990028\%\) to
\(7.412127\%\), while its speed-only anisotropic control remained insufficient
and the declared derivative projection supplied the applicable lane. Its
preserved source result is
`G693c_PASS_C_EFF_CONVERSION_FLATTENS_BAO_WITH_RADIAL_DERIVATIVE_BOUNDARY`.

These G records preserve the direct development path. They are not substituted
for the later Courtroom and Last Campaign custody.

### 5.2 Local photon-road contact and holdout

CR006@04 records `PASS` for the scoped first-order solar-system photon road.
Its \(131.215549519679\ \mu\mathrm{s}\) delay differs from the logarithmic
form by \(1.79\times10^{-13}\), while endpoint-only and wrong-road controls
reject.

CR148@04 is the later independent binary-pulsar holdout. It records
\(|z|=0.26\) for the declared Shapiro-shape comparator and numerical/analytic
road agreement within \(4\times10^{-9}\), with its wrong controls rejected.
**The test result suggests strong contact with the concept.**

### 5.3 Invariant propagation boundary

CR147@04 records `PASS` for the GW170817 dynamic-release/engine differential
with a shared post-release \(A\)-road. The different-post-release-speed control
rejects. This result supports the invariant local-\(c\) interpretation while
keeping the source-release mechanism separate from road propagation.

### 5.4 Cosmological distance road

CR013@06 records `PASS` with exact row identities for \(A_{\rm los}\),
\(c_{\rm eff}\), native distance and native distance modulus over 1,701
supernova rows. CR017@06 records `PASS` for the complete typed distance-road
dependency chain while leaving CMB modal and polarization closure open.

LC07 then replays the locked distance stack across all 1,701 SN rows and 19
BAO rows. It passes 113/113 checks, rejects 10/10 wrong controls, returns zero
same-redshift identity error and retains the \(0.240000255\%\) overlap value as
a local witness rather than a global residual. Across the scoped SN, BAO and
compressed-acoustic comparisons, **The test result suggests strong contact
with the concept.**

## 6. Controls, corrections and preserved failures

The evidence chain preserves several load-bearing controls:

- substituting a local variable light-speed for \(c\) is outside the typed
  meaning of \(c_{\rm eff}\);
- an endpoint-clock value does not reproduce photon-road shape;
- integrating the universal floor as a local source road produces a spurious
  contribution;
- a speed factor alone does not replace the derivative projection in the
  anisotropic BAO lane;
- the GW170817 lag is not assigned to different post-release propagation
  speeds or to a static integral launched from exact \(A=1\); and
- the distance replay rejects parameter refitting, bin selection, target
  substitution and shared-data leakage.

The later recombination residual belongs to its own substrate-native
recombination program. It does not redefine the line-of-sight road or the
invariant meaning of \(c_{\rm eff}\).

## 7. Current boundaries and open relations

This document installs no new propagation law. It preserves the following
boundaries:

1. \(c_{\rm eff}\) is a coordinate or inferred-distance shorthand, not a local
   fundamental constant.
2. Local photon roads, cosmological roads and exterior strong-field traversal
   require their own declared accumulation inputs and operators.
3. The distance conversion does not by itself supply full recombination,
   perturbation, polarization or lensing-time-delay closure.
4. A source-release delay and a propagation-road delay remain differently
   typed.
5. Exact \(A=1\) remains a closure boundary rather than an ordinary photon
   launch point.

## 8. Related SAMA documents

| Document | Connection |
|---|---|
| `SAMA-D000002` | Universal accumulation floor entering the global inventory. |
| `SAMA-D000003` | Local spherical source lift \(A(r)\). |
| `SAMA-D000004` | General typed weak-field readout split. |
| `SAMA-D000005` | Endpoint-clock comparison. |
| `SAMA-D000007` | Local photon-road and Shapiro development. |
| `SAMA-D000010` | Local/cosmological road distinction. |
| `SAMA-D000011` | Full supernova distance-road operator. |
| `SAMA-D000012` | BAO and acoustic ruler-road bridge. |
| `SAMA-D000014` | Horizon lapse and exterior traversal. |

## 9. Established result, exact evidence, forward connection and open boundary

The established type-safe packet is

\[
\boxed{
c_{\rm local}=c,
\qquad
c_{\rm eff}=c(1-A),
\qquad
D_{\rm native}=D_{\rm readout}(1-A)
}.
\]

For the global road this specializes to

\[
\boxed{
A_{\rm los}(z)
=\frac1\pi\left[1-(1+z)^{-3}\right],
\qquad
D_{\rm native}(z)
=D_{\rm readout}(z)[1-A_{\rm los}(z)]
}.
\]

Exact evidence is carried by `G:G688c@SAM-ARCHIVE`,
`G:G693c@SAM-ARCHIVE`, [`CR:CR006@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr006-photon-road-shapiro-external-contact/README.md), [`CR:CR148@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr148-binary-pulsar-shapiro-road-holdout/README.md),
[`CR:CR147@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr147-gw170817-a-release-em-origin-differential/README.md), [`CR:CR013@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr013-sn-luminosity-ledger-shrinkage/README.md), [`CR:CR017@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr017-distance-road-typed-bridge-closure/README.md) and [`LC:LC07`](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md).
The two registered strong-contact statements remain attached to the binary
pulsar holdout and the locked SN/BAO distance replay; source `PASS` fields on
other rows remain provenance.

The forward connection sends the operator boundary to `SAMA-D000010`, the
supernova application to `SAMA-D000011`, the BAO/acoustic application to
`SAMA-D000012` and the exact exterior road to `SAMA-D000014`.

The specifically open boundary is full native recombination, perturbation and
polarization development; strong-field infaller and endpoint construction;
and any new local, global or future-directed road that has not been assigned
its own accumulation input and operator. Exact \(A=1\) remains a closure
boundary, not an ordinary launch point.

## Test and result index

| Test record key | Role | Source result/status | Result artifact | Test folder |
|---|---|---|---|---|
| `G:G688c@SAM-ARCHIVE` | Direct \(z/A/c_{\rm eff}\) ruler construction | `G688c_PASS_Z_A_EFFECTIVE_LIGHT_SPEED_RULER_BUILDS_NATIVE_DISTANCE_LANE` | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G688c_Z_A_EFFECTIVE_LIGHT_SPEED_RULER/G688c_RESULT.md) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G688c_Z_A_EFFECTIVE_LIGHT_SPEED_RULER) |
| `G:G693c@SAM-ARCHIVE` | Explicit BAO distance conversion and derivative boundary | `G693c_PASS_C_EFF_CONVERSION_FLATTENS_BAO_WITH_RADIAL_DERIVATIVE_BOUNDARY` | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G693c_BAO_EXPLICIT_C_EFF_NATIVE_DISTANCE_CONVERSION/G693c_RESULT.md) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G693c_BAO_EXPLICIT_C_EFF_NATIVE_DISTANCE_CONVERSION) |
| [`CR:CR006@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr006-photon-road-shapiro-external-contact/README.md) | First-order solar-system photon road | `PASS` | [result](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_result.md) | [folder](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT) |
| [`CR:CR148@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr148-binary-pulsar-shapiro-road-holdout/README.md) | Independent binary-pulsar road holdout | `PASS_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT` | [result](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_result.md) | [folder](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT) |
| [`CR:CR147@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr147-gw170817-a-release-em-origin-differential/README.md) | Shared post-release \(A\)-road and invariant propagation boundary | `PASS` | [result](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/CR147_result.md) | [folder](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL) |
| [`CR:CR013@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr013-sn-luminosity-ledger-shrinkage/README.md) | Exact SN \(A_{\rm los}/c_{\rm eff}\) row identities | `PASS` | [result](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_result.md) | [folder](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE) |
| [`CR:CR017@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr017-distance-road-typed-bridge-closure/README.md) | Typed distance-road closure | `PASS` | [result](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_result.md) | [folder](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE) |
| [`LC:LC07`](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md) | Locked-stack SN/BAO distance replay | `LC07_PASS_SN_BAO_DISTANCE_ROAD_REPLAY_FROM_LOCKED_PRIMITIVE_STACK` | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY) |

## Atomic SAMA source records

| Record ID | Role in this document |
|---|---|
| `SAMA-C000001-R001` | Universal accumulation floor and global inventory role. |
| `SAMA-C000002-R001` | Spherical source accumulation lift \(A(r)\). |
| `SAMA-C000003-R001` | Endpoint-clock and photon-road type distinction. |
| `SAMA-C000004-R001` | Effective traversal shorthand as coordinate readout. |
| `SAMA-C000053-R001` | Path-dependent local photon-road accumulation functional. |
| `SAMA-C000060-R001` | Equivalent effective-traversal distance identity. |
| `SAMA-C000061-R001` | Shared post-release road and source-engine delay distinction. |
| `SAMA-C000122-R001` | Volume I subject and cross-volume boundary. |
| `SAMA-C000124-R001` | Current-authority versus source-chronology distinction. |
| `SAMA-C000125-R001` | Evidence-status, classification and owner-approval boundary. |

## External references

External measurements and comparator provenance are carried by the pinned test
artifacts in the test and result index. This revision introduces no new
external source.

## Revision and approval

This exact revision has `reviewed_and_approved: false` until Sean Brady
explicitly approves it. It assembles existing source-bound concepts and test
results into the first complete standard-document exemplar; it introduces no
new test classification or current research pointer.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`CR:CR006@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr006-photon-road-shapiro-external-contact/README.md) | [CR006_PRECOMMIT.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_PRECOMMIT.md)<br>[CR006_declared_premises.json](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_declared_premises.json) | [CR006_runner.py](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_runner.py) | [CR006_candidate_rows.csv](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_candidate_rows.csv)<br>[CR006_wrong_radial_shape_rows.csv](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_wrong_radial_shape_rows.csv) | [CR006_result.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_result.md)<br>[CR006_summary.json](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_summary.json) | [All 10 files](../../tests/courtroom/04-photon-road-shapiro-delay-cr006-photon-road-shapiro-external-contact/README.md) |
| [`CR:CR013@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr013-sn-luminosity-ledger-shrinkage/README.md) | [CR013_PRECOMMIT.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_PRECOMMIT.md)<br>[CR013_declared_premises.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_declared_premises.json) | [CR013_runner.py](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_runner.py) | [CR013_candidate_rows.csv](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_candidate_rows.csv) | [CR013_result.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_result.md)<br>[CR013_summary.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR013_SN_LUMINOSITY_LEDGER_SHRINKAGE/CR013_summary.json) | [All 8 files](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr013-sn-luminosity-ledger-shrinkage/README.md) |
| [`CR:CR017@06`](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr017-distance-road-typed-bridge-closure/README.md) | [CR017_PRECOMMIT.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_PRECOMMIT.md)<br>[CR017_declared_premises.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_declared_premises.json) | [CR017_runner.py](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_runner.py) | [CR017_candidate_rows.csv](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_candidate_rows.csv) | [CR017_result.md](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_result.md)<br>[CR017_summary.json](../../courtroom/06_DISTANCE_ROAD_SN_BAO_SHARED_SHRINKAGE/CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE/CR017_summary.json) | [All 10 files](../../tests/courtroom/06-distance-road-sn-bao-shared-shrinkage-cr017-distance-road-typed-bridge-closure/README.md) |
| [`CR:CR147@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr147-gw170817-a-release-em-origin-differential/README.md) | [All package files](../../tests/courtroom/04-photon-road-shapiro-delay-cr147-gw170817-a-release-em-origin-differential/README.md) | [CR147_runner.py](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/CR147_runner.py) | [CR147_wrong_controls.csv](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/CR147_wrong_controls.csv) | [CR147_result.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/CR147_result.md)<br>[CR147_summary.json](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/CR147_summary.json) | [All 13 files](../../tests/courtroom/04-photon-road-shapiro-delay-cr147-gw170817-a-release-em-origin-differential/README.md) |
| [`CR:CR148@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr148-binary-pulsar-shapiro-road-holdout/README.md) | [CR148_PRECOMMIT.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_PRECOMMIT.md)<br>[CR148_PRECOMMIT.sha256](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_PRECOMMIT.sha256)<br>[CR148_PREFLIGHT.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_PREFLIGHT.md) | [CR148_runner.py](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_runner.py) | [CR148_wrong_controls.csv](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_wrong_controls.csv)<br>[CR148_wrong_controls.csv](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/FAILED_RUN_20260711_173452_VALIDATION_BOOLEAN_BUG/CR148_wrong_controls.csv) | [CR148_SOURCE_AUDIT.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_SOURCE_AUDIT.md)<br>[CR148_result.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_result.md)<br>[CR148_summary.json](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_summary.json)<br>[CR148_result.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/FAILED_RUN_20260711_173452_VALIDATION_BOOLEAN_BUG/CR148_result.md)<br>[CR148_summary.json](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/FAILED_RUN_20260711_173452_VALIDATION_BOOLEAN_BUG/CR148_summary.json) | [All 50 files](../../tests/courtroom/04-photon-road-shapiro-delay-cr148-binary-pulsar-shapiro-road-holdout/README.md) |
| [`LC:LC07`](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md) | [LC07_bao_candidate_rows.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_bao_candidate_rows.csv)<br>[LC07_cmb_candidate_rows.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_cmb_candidate_rows.csv)<br>[LC07_sn_bao_independent_candidate_rows.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_sn_bao_independent_candidate_rows.csv)<br>[LC07_sn_candidate_rows.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_sn_candidate_rows.csv)<br>[LC07_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_wrong_controls.csv) | [LC07_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_result.md)<br>[LC07_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC07_SN_BAO_DISTANCE_ROAD_REPLAY/LC07_summary.json) | [All 17 files](../../tests/courtroom/16-the-last-campaign-lc07-sn-bao-distance-road-replay/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000009`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/INVARIANT_C_AND_EFFECTIVE_TRAVERSAL_READOUT.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000009 | Clock and Traversal | Invariant Local c, Effective Traversal Distance and Engine/Road Separation |

| Document field | Value |
|---|---|
| Purpose | Define `c_eff` as a typed coordinate-distance readout, preserve invariant local `c`, and connect the local and cosmological road tests without merging their operators. |
| Prerequisite documents | `SAMA-D000005`, `SAMA-D000007` |
| Used by | `SAMA-D000010`, `SAMA-D000011`, `SAMA-D000012`, `SAMA-D000014`; focused child of `SAMA-P000002` and `SAMA-P000005`. |
| Primary source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`, SHA-256 `2f22500f6583f567e350974610f00142e89b081a5b8c4c90c6dfe89bec43be0d`. |
| Courtroom pin | `iwtbotiwtwot/The_Courtroom` commit `b5e914f71377e86ef4c67e199973d9300795cda1`. |
| Revision state | Source-bound draft; mechanically registered; not reviewed or approved. |

</details>
