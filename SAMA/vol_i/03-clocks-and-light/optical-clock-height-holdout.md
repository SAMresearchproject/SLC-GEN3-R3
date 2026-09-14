[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Optical-Clock Height Holdout

## Current research connections — 14 September 2026

The global execution authority is SLC-GEN3-R3 / SLC-GEN3-CEV1-R3. The September 2026 research includes exact retained-history computation, RH arithmetic compensation, native Mersenne work, Starbreaker signed reception and ATOM3D contact/grammar. The research index connects the retained derivations to the latest code, results and current domain assignments.

[Current derivations, code and results](../../../docs/RESEARCH.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

An optical clock separated vertically from another clock by only one
millimetre tests the endpoint operator at a scale where the predicted
fractional shift is about \(10^{-19}\). The SAM weak endpoint formula is

\[
\frac{\Delta f}{f}
\simeq\frac{A_s(r)-A_s(r+h)}2.
\]

Substituting \(A_s(r)=2GM_\oplus/(c^2r)\) gives an exact finite-height
weak expression, and its near-surface limit is \(gh/c^2\). At
\(h=1\ \mathrm{mm}\), the fixed prediction was
\(1.089951994739\times10^{-19}\), compared with the selected
\(^{87}\mathrm{Sr}\) measurement
\((9.8\pm2.3)\times10^{-20}\). The standardized residual is
\(z=0.4781\).

The holdout is valuable not only for its agreement. Its rejected controls show
that the shared floor must not be inserted as a local height signal, the
endpoint coefficient cannot be doubled, the sign and radial dependence are
fixed, and a route-time integral has the wrong output type.

## 1. Holdout question and independence contract

The focused question is:

> Does the fixed, no-fit one-millimetre endpoint-clock prediction agree with an
> independently selected optical-clock measurement while the registered
> coefficient, sign, radial-power, floor and road substitutions reject?

The conceptual picture is two nearly coincident endpoints on Earth's source
profile. Each clock samples its own local lapse; the one-millimetre separation
enters only through the difference of those endpoint values. A road integral,
constant-floor insertion or doubled coefficient would connect different
objects and therefore serves as a control rather than an alternative clock
model.

The selected experiment in the pinned result is Bothwell et al., “Resolving
the gravitational redshift across a millimetre-scale atomic sample,” using a
vertical one-dimensional \(^{87}\mathrm{Sr}\) optical lattice clock. The
Courtroom record locks the target identity, geometry, primary source,
precommit and runner hashes. It also records that the frozen SAM Language v0.3
candidate and its expected outputs were not consulted during development.
That firewall makes the test eligible as a holdout for that separate language
campaign; the scientific clock result does not depend on promoting any
language artifact.

## 2. Typed inputs, outputs and units

| Quantity | Registered value | Type/unit |
|---|---:|---|
| \(c\) | \(2.99792458\times10^8\) | m s\(^{-1}\) |
| \(\mu_\oplus=GM_\oplus\) | \(3.986004418\times10^{14}\) | m\(^3\) s\(^{-2}\) |
| local \(g\) | \(9.796\) | m s\(^{-2}\) |
| height step \(h\) | \(1.000\times10^{-3}\) | m |
| lower radius \(r_l\) | \(6.378880989854540619\times10^6\) | m |
| upper radius \(r_u\) | \(6.378880990854540619\times10^6\) | m |
| observed upper-minus-lower fraction | \(9.8\times10^{-20}\) | dimensionless |
| reported uncertainty \(\sigma\) | \(2.3\times10^{-20}\) | dimensionless |

The tested output is a fractional frequency difference, not an acceleration
and not a time delay. The height and source values enter an endpoint
difference; the measurement uncertainty enters only the standardized
comparison after the prediction is fixed.

## 3. Derivation from the spherical lift

### 3.1 Write the two endpoint fields

At the lower endpoint,

\[
A_l=A_s(r)=\frac{2GM_\oplus}{c^2r}.
\]

At the upper endpoint \(r+h\),

\[
A_u=A_s(r+h)=\frac{2GM_\oplus}{c^2(r+h)}.
\]

Because \(h>0\), \(A_l>A_u\), so the upper clock's selected
upper-minus-lower frequency fraction is positive.

### 3.2 Apply the weak endpoint coefficient

\[
\frac{\Delta f}{f}
\simeq\frac{A_l-A_u}{2}.
\]

Insert the two fields:

\[
\frac{\Delta f}{f}
\simeq\frac12\left[
\frac{2GM_\oplus}{c^2r}
-\frac{2GM_\oplus}{c^2(r+h)}
\right].
\]

Cancel the factor two:

\[
\frac{\Delta f}{f}
\simeq\frac{GM_\oplus}{c^2}\left[
\frac1r-\frac1{r+h}
\right].
\]

Combine the fractions:

\[
\frac1r-\frac1{r+h}
=\frac{r+h-r}{r(r+h)}
=\frac{h}{r(r+h)}.
\]

Therefore the finite-height weak formula is

\[
\boxed{
\frac{\Delta f}{f}
\simeq\frac{GM_\oplus h}{c^2r(r+h)}
}.
\]

### 3.3 Take the millimetre near-surface limit

When \(h\ll r\),

\[
r(r+h)\simeq r^2.
\]

Using \(g=GM_\oplus/r^2\),

\[
\boxed{
\frac{\Delta f}{f}\simeq\frac{gh}{c^2}
}.
\]

This approximation is valid at millimetre height because \(h/r\) is
tiny. It is not the formula to use as an exact finite-radius substitute at GPS
altitude.

## 4. Exact lapse and weak prediction

After the declared local common-background treatment, the exact endpoint
comparison is

\[
\delta_{\rm exact}
=\sqrt{\frac{1-A_u}{1-A_l}}-1.
\]

The registered fields are

\[
A_l=1.390534812037245386\times10^{-9},
\]

\[
A_u=1.390534811819254987\times10^{-9}.
\]

Their difference is approximately \(2.179904\times10^{-19}\); the
endpoint half-coefficient gives the weak prediction

\[
\delta_{\rm weak}
=1.089951994739255776\times10^{-19}.
\]

The exact lapse gives

\[
\delta_{\rm exact}
=1.089951996254871970\times10^{-19}.
\]

The recorded difference is

\[
\delta_{\rm exact}-\delta_{\rm weak}
=1.515616194182489015\times10^{-28}.
\]

Thus the weak approximation is not assumed without a check: the exact and weak
operators agree far beyond the scale of the reported experimental
uncertainty.

## 5. Comparison with the locked measurement

The selected measurement is

\[
\delta_{\rm obs}=(9.8\pm2.3)\times10^{-20}.
\]

The standardized residual is

\[
z=\frac{\delta_{\rm weak}-\delta_{\rm obs}}{\sigma}.
\]

Substitution gives

\[
z=\frac{1.089951994739255776\times10^{-19}
          -9.8\times10^{-20}}
         {2.3\times10^{-20}}
=0.4780521370557475\ldots.
\]

The rounded source result is \(z=0.4781\). No normalization is fitted to
make the central values coincide. The registered free-parameter count is zero.

## 6. Wrong controls: deviations that reveal the operator

| Control | Prediction/result | Why it fails |
|---|---:|---|
| WC1: uncancelled local \(A_0/2\) | \(1.326291192432461142\times10^{-2}\), \(z\approx5.77\times10^{17}\) | Treats the universal floor as the one-millimetre endpoint difference. |
| WC2: double the endpoint coefficient | \(2.179903989478511552\times10^{-19}\), \(z=5.21697\) | Replaces \(\Delta A/2\) by \(\Delta A\). |
| WC3: force-like radial dependence | \(3.031232384031144335\times10^{-28}\), \(z=-4.26087\) | Uses a gradient/force scaling for an endpoint-value comparison. |
| WC4: wrong sign | \(-1.089951994739255776\times10^{-19}\), \(z=-8.99979\) | Reverses the frozen upper-minus-lower observable. |
| WC5: road-time substitution | \(4.638324864187361865\times10^{-21}\), z not applicable | A time integral in seconds is not a fractional endpoint frequency shift. |
| WC6: free-amplitude rescue | Fits exactly with \(k\approx0.899122\) | Uses the revealed central value to change a fixed prediction. |
| WC7: near-surface diagnostic | \(1.089951994910124616\times10^{-19}\), \(z=0.478052\) | This control agrees as an expected limit; it diagnoses the approximation and does not replace the radial kernel. |

The first five failures separate field, coefficient, gradient, sign and route
types. WC6 demonstrates why “closer after fitting” is not the holdout question.
WC7 is deliberately retained as a useful diagnostic rather than mislabeled as
a failed control.

## 7. Millimetre optical-clock holdout

The test does not overwrite earlier clock construction. It is a successor to
the endpoint derivation and GPS evidence in `SAMA-D000005`, with a separately
selected millimetre geometry and measurement. The process is:

1. freeze the endpoint formula and one-half coefficient;
2. lock the primary source, target identity and one-millimetre geometry;
3. seal the precommit and runner before the target reveal;
4. compute weak and exact predictions with no fitted parameter;
5. calculate the standardized residual using the quoted uncertainty;
6. execute the wrong controls and retain their failures;
7. preserve the language-firewall fields and hashes.

This ordering makes the holdout informative. A fitted-amplitude row is retained
as a prohibited rescue, not used as the result. The exact/weak difference is
retained even though it is negligible. The floor, sign, force-like and road
failures remain visible because each tells the reader which part of the
endpoint operator is load-bearing.

## 8. Established result and exact boundary

[`CR:CR006@03`](../../tests/courtroom/03-clocks-and-gps-cr006-optical-clock-height-holdout-endpoint-a-kernel/README.md) records the fixed prediction, selected measurement and
\(z=0.4781\), with every sensitive wrong control rejected and the
diagnostic near-surface limit retained.

**The test result suggests strong contact with the concept.**

The classification is scoped to the millimetre endpoint-clock holdout. It does
not classify photon-road traversal, GPS engineering as a whole, strong-field
clocks, clock hardware, atomic structure or a unique discrimination against
general relativity in the weak field. The source explicitly states the last
boundary.

Exact evidence is the registered holdout and sensitivity-control chain in
Section 10. The specifically open boundary is atomic/hardware modeling,
strong-field clock behavior and discrimination between frameworks that share
the same weak endpoint limit.

## 9. Forward handoff

The focused holdout returns this verified small-height endpoint packet to the
Volume I clock route:

\[
\boxed{
\frac{\Delta f}{f}
\simeq\frac{A(r)-A(r+h)}2
=\frac{GMh}{c^2r(r+h)}
\simeq\frac{gh}{c^2}
}.
\]

`SAMA-D000007` changes measurement geometry from endpoint difference to route
integration. It must not inherit the one-half clock coefficient.

## 10. Focused test and result index

| Exact qualified key | Evidence role | Preserved outcome | Direct result | Result folder |
|---|---|---|---|---|
| [`CR:CR006@03`](../../tests/courtroom/03-clocks-and-gps-cr006-optical-clock-height-holdout-endpoint-a-kernel/README.md) | Independent millimetre endpoint holdout | Pinned source records `PASS_OPTICAL_CLOCK_ENDPOINT_HOLDOUT`, prediction \(1.089951994739\times10^{-19}\), measurement \((9.8\pm2.3)\times10^{-20}\), and \(z=0.4781\). **The test result suggests strong contact with the concept.** | [result](../../courtroom/03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL/CR006_result.md) | [folder](../../courtroom/03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL) |

## 11. Atomic record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000047-R001` | Supplies the weak endpoint-clock comparison and one-half coefficient. |
| `SAMA-C000050-R001` | Derives the finite-height and \(gh/c^2\) optical-clock formula. |
| `SAMA-C000051-R001` | Records the no-fit prediction, measurement, residual and authorized classification. |
| `SAMA-C000052-R001` | Preserves the optical-clock wrong-control packet. |
| `SAMA-C000122-R001` | Enforces the Volume I/II/III subject boundary. |
| `SAMA-C000124-R001` | Separates source-era chronology from current live authority. |
| `SAMA-C000125-R001` | Preserves source verdicts, authorized classifications and false approval state. |

## 12. Source and approval boundary

The sole direct test key is listed literally above and is pinned to Courtroom
commit `b5e914f71377e86ef4c67e199973d9300795cda1`. The external paper and
measurement provenance are carried by that immutable result and its hashes;
this document introduces no replacement datum.

`reviewed_and_approved` remains `false`; `approval` remains `null`. Holdout
integrity, strong-contact classification and manuscript validation do not
constitute owner approval.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`CR:CR006@03`](../../tests/courtroom/03-clocks-and-gps-cr006-optical-clock-height-holdout-endpoint-a-kernel/README.md) | [CR006_PRECOMMIT.md](../../courtroom/03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL/CR006_PRECOMMIT.md)<br>[CR006_PREFLIGHT.md](../../courtroom/03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL/CR006_PREFLIGHT.md) | [CR006_runner.py](../../courtroom/03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL/CR006_runner.py) | [CR006_CONTROLS.csv](../../courtroom/03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL/CR006_CONTROLS.csv) | [CR006_INTERNAL_SOURCE_AUDIT.md](../../courtroom/03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL/CR006_INTERNAL_SOURCE_AUDIT.md)<br>[CR006_result.md](../../courtroom/03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL/CR006_result.md)<br>[CR006_summary.json](../../courtroom/03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL/CR006_summary.json) | [All 26 files](../../tests/courtroom/03-clocks-and-gps-cr006-optical-clock-height-holdout-endpoint-a-kernel/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000006`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/OPTICAL_CLOCK_HEIGHT_HOLDOUT.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000006 | Clock and Traversal | Millimetre Optical-Clock Holdout and Wrong Controls |

| Document field | Value |
|---|---|
| Purpose | Present the millimetre optical-clock height holdout from formula through fixed inputs, exact/weak comparison, standardized residual, wrong-control rejection and retained result. |
| Prerequisite documents | `SAMA-D000005` |
| Used by | Focused holdout child of `SAMA-P000002`; its result returns to the endpoint-clock route in `SAMA-D000005`. |
| Primary source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`, SHA-256 `2f22500f6583f567e350974610f00142e89b081a5b8c4c90c6dfe89bec43be0d`. |
| Revision state | Source-bound draft; mechanically registered proposal; not reviewed or approved. |

</details>
