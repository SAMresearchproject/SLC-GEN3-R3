[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Binary-Pulsar Road Holdout

## Current research connections — 14 September 2026

The global execution authority is SLC-GEN3-R3 / SLC-GEN3-CEV1-R3. The September 2026 research includes exact retained-history computation, RH arithmetic compensation, native Mersenne work, Starbreaker signed reception and ATOM3D contact/grammar. The research index connects the retained derivations to the latest code, results and current domain assignments.

[Current derivations, code and results](../../../docs/RESEARCH.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

The solar-system Shapiro result is not the end of the photon-road question. A
focused holdout asks whether the same fixed source coefficient and route
operator survive on independently selected binary-pulsar timing geometry.

For companion mass \(M_B\), the source lift is

\[
A_c(r)=\frac{2GM_B}{c^2r}.
\]

The road integral carries the time coefficient

\[
\frac{2GM_B}{c^3}.
\]

Pulsar timing convention writes that coefficient as \(2r_{\rm timing}\),
where

\[
r_{\rm timing}=\frac{GM_B}{c^3}.
\]

The timing map is therefore

\[
\Delta_S(E)=-2r_{\rm timing}\ln q(E).
\]

The factor two has not disappeared and no free amplitude has been introduced;
it has moved into a standard notation map. On PSR J0737-3039A/B, the holdout
records \(r_{\rm timing}=6.1514456437083\ \mu\mathrm s\),
\(s=\sin i=0.999906773574375\), standardized residual
\(|z|=0.26\), and analytic/numerical road agreement better than
\(4\times10^{-9}\).

## 1. Holdout question and selected system

The test asks:

> Does the unchanged photon-road source lift reproduce the independently
> locked binary-pulsar Shapiro timing comparator and analytic road while
> endpoint-only, wrong-power, missing-source-scale, local-floor, geometry and
> free-amplitude controls reject?

The conceptual picture is the companion's source field swept by a changing
orbital line of sight. The source coefficient fixes the time scale, while the
locked orbital geometry supplies the logarithmic phase dependence. Neither
part is fitted after the timing comparator is revealed.

The selected system is PSR J0737-3039A/B. The pinned Courtroom result identifies
Kramer et al. (2006) and its Table 2 Shapiro-shape observed/expected comparison
as the target source/readout. The holdout records that the target, source
hashes, precommit and runner were locked before reveal. It also records that
the frozen SAM Language v0.3 candidate and its expected output were not
consulted, so the scientific result remains eligible as a separate language
holdout.

The independent change is geometry and comparison source, not a changed SAM
road amplitude.

## 2. Typed quantities, conventions and units

| Quantity | Definition/role | Type | Units |
|---|---|---|---|
| \(M_B\) | companion mass | locked source input | kg |
| \(A_c(r)\) | \(2GM_B/(c^2r)\) | companion source lift | dimensionless |
| \(2GM_B/c^3\) | source-road coefficient | physical road time scale | s |
| \(r_{\rm timing}\) | \(GM_B/c^3\) | pulsar timing range parameter | s |
| \(i\) | orbital inclination | locked geometry angle | rad/degree convention in source geometry |
| \(s\) | \(\sin i\) | timing shape parameter | dimensionless |
| \(E\) | orbital anomaly/phase coordinate in timing map | route-state input | angular/parametric |
| \(q(E)\) | positive dimensionless orbital geometry factor in the locked timing model | logarithm input | dimensionless |
| \(\Delta_S(E)\) | Shapiro timing contribution | road-time readout | s |

The exact form of \(q(E)\) is supplied by the locked timing geometry. This
document does not invent or refit it. The load-bearing relation is that the
source coefficient multiplies the fixed logarithmic geometry.

## 3. Map the photon road into timing notation

### 3.1 Start from the source lift

\[
A_c(r)=\frac{2GM_B}{c^2r}.
\]

### 3.2 Apply the photon-road operator

\[
T_A^\gamma=\frac1c\int_\Gamma A_c(r)\,ds.
\]

Insert \(A_c\):

\[
T_A^\gamma
=\frac1c\int_\Gamma
\frac{2GM_B}{c^2r}\,ds
=\frac{2GM_B}{c^3}\int_\Gamma\frac{ds}{r}.
\]

The source-dependent coefficient has units

\[
\left[\frac{GM_B}{c^3}\right]
=\frac{\mathrm{m^3,s^{-2}}}{\mathrm{m^3,s^{-3}}}
=\mathrm s.
\]

### 3.3 Isolate the timing range parameter

Define

\[
r_{\rm timing}=\frac{GM_B}{c^3}.
\]

Then

\[
\frac{2GM_B}{c^3}=2r_{\rm timing}.
\]

The binary timing convention packages the dimensionless orbital route
integral into \(-\ln q(E)\), so

\[
\boxed{
\Delta_S(E)=-2r_{\rm timing}\ln q(E)
}.
\]

This notation contains the same factor two as the original spherical source
lift. Calling \(r_{\rm timing}\) “half the prediction” would be a convention
error; comparing \(2r_{\rm timing}\) with the road coefficient closes the
map exactly.

## 4. Locked prediction and comparator

### 4.1 Source and geometry prediction

The holdout records

\[
r_{\rm timing}=6.151445643708300\ \mu\mathrm s
\]

and

\[
s_{\rm SAM}=\sin i=0.999906773574375.
\]

No new amplitude is fitted. The companion mass fixes the range scale; the
locked inclination fixes the shape parameter; the orbital timing geometry
fixes \(q(E)\).

### 4.2 Published comparison

The pinned source records

\[
s_{\rm observed}=0.999740000000000,
\qquad
\sigma_s=0.000390000000000,
\]

and, for the chosen primary comparator,

\[
\rho_{\rm obs/exp}=0.999870000000000,
\qquad
\sigma_\rho=0.000500000000000.
\]

The locked comparator asks whether the observed/expected ratio is consistent
with unity. Therefore

\[
z=\frac{\rho_{\rm obs/exp}-1}{\sigma_\rho}
=\frac{0.99987-1}{0.00050}
=-0.26,
\]

so

\[
\boxed{|z|=0.26}.
\]

This calculation is kept distinct from directly subtracting the two listed
\(s\)-values; the primary target in the source is the table's
observed/expected comparison.

## 5. Analytic versus numerical road check

The analytic timing form is evaluated against numerical integration at two
resolutions. The registered maxima are

\[
\max|\Delta_{\rm numerical,8192}
      -\Delta_{\rm analytic}|
=3.770677103887010\times10^{-9},
\]

and

\[
\max|\Delta_{\rm numerical,8192}
      -\Delta_{\rm numerical,4096}|
=1.131203575255313\times10^{-8}.
\]

Both are below the declared tolerance

\[
2.0\times10^{-8}.
\]

The first comparison checks implementation against the closed form. The
second checks numerical refinement. Passing both prevents a lucky match from
one discretization from standing in for road convergence.

## 6. Wrong controls and what each one diagnoses

### 6.1 Endpoint-only substitution

`WC1_ENDPOINT_ONLY_SUBSTITUTION` is rejected. Endpoint lapse values do not
contain the orbital-phase route function \(q(E)\), so they cannot reproduce
the Shapiro timing shape.

### 6.2 Wrong radial power

`WC2_WRONG_RADIAL_POWER` is rejected. The logarithmic road follows from
\(A_c\propto r^{-1}\). A different radial power changes the orbital-phase
shape and destroys the mapped analytic integral.

### 6.3 Missing source-radius factor

`WC3_MISSING_SOURCE_RADIUS_FACTOR` is rejected. Removing
\(2GM_B/c^2\) breaks both units and the zero-fit amplitude
\(2GM_B/c^3\).

### 6.4 Universal floor as local road source

`WC4_A0_TREATED_AS_LOCAL_ROAD_SOURCE` is rejected as illegal type use. The
holdout tests the companion's differential source road. A uniform
\(A_0\)-times-path term is not that source contribution.

### 6.5 Remove near-source enhancement

`WC5_NO_NEAR_SOURCE_ENHANCEMENT` is rejected. Flattening the road removes the
geometry dependence that makes the edge-on Shapiro shape informative.

### 6.6 Wrong inclination orientation

`WC6_WRONG_INCLINATION_ORIENTATION` is rejected. The sign/orientation of the
locked orbital geometry is part of \(q(E)\) and \(s=\sin i\), not a
post-result choice.

### 6.7 Free-amplitude rescue

`WC7_FREE_AMPLITUDE_RESCUE` is rejected as prohibited. Changing the coefficient
after target reveal would replace the source prediction
\(2GM_B/c^3\) with a fit and destroy the holdout question.

Together the controls locate four load-bearing layers:

| Layer | Preserved element |
|---|---|
| Source | \(2GM_B/c^2\) and no free amplitude |
| Field | inverse-first-power \(A_c(r)\) |
| Geometry | inclination, phase and near-source road |
| Operator | path integral rather than endpoint comparison |

## 7. Independent binary-pulsar road holdout

The source records the following custody checks as true:

- source and target hashes verified;
- precommit sealed before runner execution;
- runner sealed before target reveal;
- target locked before reveal;
- existing artifacts not modified;
- forbidden language-candidate paths not opened;
- no forecast generated;
- no queue maintenance performed by the research agent.

These checks do not replace the scientific comparison. They establish why the
comparison counts as an independent holdout rather than a retrospective fit.
The seven wrong controls are retained even though the canonical packet passes;
their failure is the evidence that source scale, road geometry, field power
and fixed amplitude jointly matter.

## 8. Relation to the solar road and its boundary

`SAMA-D000007` derived the solar-system straight-road
\(\operatorname{asinh}\)/log map. The binary timing geometry is more
specialized, but the source coefficient is unchanged:

\[
\text{solar/binary road coefficient}
=\frac{r_s}{c}
=\frac{2GM}{c^3}.
\]

The holdout therefore tests transport of the same operator to a new system,
not a new binary-only formula. Its strong-gravity binary environment does not
turn the scoped timing result into full strong-field photon propagation,
binary dynamics or a general interior law.

## 9. Established result and forward handoff

[`CR:CR148@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr148-binary-pulsar-shapiro-road-holdout/README.md) records the fixed timing range, shape, primary standardized
residual, numerical/analytic agreement, zero introduced free parameters and
rejection of all sensitive controls.

**The test result suggests strong contact with the concept.**

The classification is limited to the independently selected binary-pulsar
photon-road holdout. It does not classify endpoint clocks, cosmological roads,
full binary dynamics, full GR, or strong-field launch from \(A=1\).

The packet returned to Volume I is

\[
\boxed{
A_c(r)=\frac{2GM_B}{c^2r},
\qquad
r_{\rm timing}=\frac{GM_B}{c^3},
\qquad
\Delta_S(E)=-2r_{\rm timing}\ln q(E)
}.
\]

`SAMA-D000009` receives the invariant-\(c\), measurable-road interpretation;
the binary holdout does not authorize a variable fundamental light speed.

Exact evidence is the registered holdout and wrong-control packet in Section
10. The specifically open boundary is full binary dynamics, strong-field
launch and every timing contribution outside the scoped Shapiro road.

## 10. Focused test and result index

| Exact qualified key | Evidence role | Preserved outcome | Direct result | Result folder |
|---|---|---|---|---|
| [`CR:CR148@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr148-binary-pulsar-shapiro-road-holdout/README.md) | Independent binary-pulsar road holdout | Pinned result records `PASS_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT`, \(r_{\rm timing}=6.1514456437083\ \mu\mathrm s\), \(s=0.999906773574375\), \(|z|=0.26\), and analytic/numerical agreement better than \(4\times10^{-9}\). **The test result suggests strong contact with the concept.** | [result](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_result.md) | [folder](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT) |

## 11. Atomic record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000053-R001` | Supplies the local photon-road functional. |
| `SAMA-C000057-R001` | Maps the source-road coefficient into binary timing notation. |
| `SAMA-C000058-R001` | Records the timing range, shape, residual, numerical agreement and authorized classification. |
| `SAMA-C000059-R001` | Preserves the seven binary-road wrong controls. |
| `SAMA-C000122-R001` | Enforces the Volume I/II/III subject boundary. |
| `SAMA-C000124-R001` | Separates source-era chronology from current live authority. |
| `SAMA-C000125-R001` | Preserves source verdicts, authorized classifications and false approval state. |

## 12. Source and approval boundary

The sole direct test key is listed literally above and is pinned to Courtroom
commit `b5e914f71377e86ef4c67e199973d9300795cda1`. External timing data,
geometry and source provenance are carried by that immutable result and its
verified hashes; this document introduces no substitute comparator.

`reviewed_and_approved` remains `false`; `approval` remains `null`. Holdout
integrity, strong-contact classification and document validation do not
constitute owner approval.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`CR:CR148@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr148-binary-pulsar-shapiro-road-holdout/README.md) | [CR148_PRECOMMIT.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_PRECOMMIT.md)<br>[CR148_PRECOMMIT.sha256](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_PRECOMMIT.sha256)<br>[CR148_PREFLIGHT.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_PREFLIGHT.md) | [CR148_runner.py](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_runner.py) | [CR148_wrong_controls.csv](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_wrong_controls.csv)<br>[CR148_wrong_controls.csv](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/FAILED_RUN_20260711_173452_VALIDATION_BOOLEAN_BUG/CR148_wrong_controls.csv) | [CR148_SOURCE_AUDIT.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_SOURCE_AUDIT.md)<br>[CR148_result.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_result.md)<br>[CR148_summary.json](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/CR148_summary.json)<br>[CR148_result.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/FAILED_RUN_20260711_173452_VALIDATION_BOOLEAN_BUG/CR148_result.md)<br>[CR148_summary.json](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR148_BINARY_PULSAR_SHAPIRO_ROAD_HOLDOUT/FAILED_RUN_20260711_173452_VALIDATION_BOOLEAN_BUG/CR148_summary.json) | [All 50 files](../../tests/courtroom/04-photon-road-shapiro-delay-cr148-binary-pulsar-shapiro-road-holdout/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000008`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/BINARY_PULSAR_ROAD_HOLDOUT.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000008 | Clock and Traversal | Binary-Pulsar Shapiro Holdout and Wrong Controls |

| Document field | Value |
|---|---|
| Purpose | Present the binary-pulsar Shapiro road as an independently selected holdout, including timing-convention mapping, analytic/numerical equality, standardized comparison and all registered wrong controls. |
| Prerequisite documents | `SAMA-D000007` |
| Used by | Focused holdout child of `SAMA-P000002`; its result returns to the photon-road route in `SAMA-D000007`. |
| Primary source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`, SHA-256 `2f22500f6583f567e350974610f00142e89b081a5b8c4c90c6dfe89bec43be0d`. |
| Revision state | Source-bound draft; mechanically registered proposal; not reviewed or approved. |

</details>
