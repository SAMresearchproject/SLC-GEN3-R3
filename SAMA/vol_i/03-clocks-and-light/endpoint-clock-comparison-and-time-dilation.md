[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Endpoint Clock Comparison and Time Dilation

## Conceptual abstract

A static clock reads the accumulation at its own endpoint. Its exact lapse is

\[
\ell(A)=\frac{d\tau}{dt}=\sqrt{1-A},
\]

so two endpoint clocks compare through

\[
\frac{(d\tau_2/dt)}{(d\tau_1/dt)}
=\sqrt{\frac{1-A_2}{1-A_1}}.
\]

For nearby weak source values after the declared common-background treatment,
the comparison becomes

\[
\frac{\Delta f}{f}
\simeq\frac{A_s(r_1)-A_s(r_2)}2
=\frac{GM_s}{c^2}\left(\frac1{r_1}-\frac1{r_2}\right).
\]

The coefficient one-half belongs to an endpoint lapse. A photon road instead
integrates the full source lift along a route. GPS adds a third lane: the
gravitational endpoint gain is combined with a separately declared
special-relativistic orbital-motion loss. Their arithmetic sum is an
engineering correction; their physical provenance remains separate.

## 1. Opening question and conceptual picture

Two clocks at different radii do not need to know the path between them. Each
samples its local endpoint state. A signal exchanged between them may also
accumulate a route delay, but that is a different observable.

The clock chain is

\[
A_s(r_1),A_s(r_2)
\longrightarrow
\ell_1,\ell_2
\longrightarrow
\frac{\ell_2}{\ell_1}
\longrightarrow
\text{frequency or elapsed-time comparison}.
\]

For GPS, a separate motion chain joins only at the final ledger:

\[
v_o
\longrightarrow
-\frac{v_o^2}{2c^2}
\longrightarrow
\text{add to the endpoint gravitational fraction}.
\]

The chapter asks: **how does the same \(A\)-field generate exact and weak
clock comparisons, and how can GPS combine a gravitational endpoint term with
a kinematic term without calling them one mechanism?**

## 2. Definitions, domains and units

| Object | Definition | Type | Units |
|---|---|---|---|
| \(A_s(r)\) | \(2GM_s/(c^2r)\) | spherical source lift | dimensionless |
| \(A_{\rm total}(r)\) | \(A_0+A_s(r)\) for one source | pointwise total substrate account | dimensionless |
| \(\ell(A)\) | \(\sqrt{1-A}\) | static endpoint lapse | dimensionless rate ratio |
| \(\ell_2/\ell_1\) | ratio of two endpoint lapses | exact clock comparison | dimensionless |
| \(\Delta f/f\) | upper/second clock fractional gain under the declared sign convention | weak endpoint comparison | dimensionless |
| \(v_o\) | orbital speed | independent kinematic input | m s\(^{-1}\) |
| \(-v_o^2/(2c^2)\) | leading orbital SR correction | motion-channel fraction | dimensionless |
| \(\Delta t_{\rm day}\) | total fractional correction times \(86400\ \mathrm{s}\) | daily engineering readout | s/day or \(\mu\)s/day |

The exact static lapse requires \(0\le A<1\). At \(A\to1^-\), the
lapse approaches zero and weak expansion is no longer authorized. The present
clock document develops the exterior endpoint comparison; strong-field
closure is owned later.

## 3. Exact endpoint comparison

### 3.1 Evaluate each endpoint

Let the lower/first endpoint carry accumulation \(A_1\) and the
upper/second endpoint carry \(A_2\). Their lapse factors are

\[
\ell_1=\sqrt{1-A_1},
\qquad
\ell_2=\sqrt{1-A_2}.
\]

### 3.2 Form the ratio

\[
\boxed{
\frac{\ell_2}{\ell_1}
=\sqrt{\frac{1-A_2}{1-A_1}}
}.
\]

For a spherical source and \(r_2>r_1\),

\[
A_s(r_2)<A_s(r_1),
\]

so \(1-A_2>1-A_1\) and \(\ell_2/\ell_1>1\): the higher clock
runs faster in the selected comparison convention.

### 3.3 Keep the total-field expression honest

Before local background treatment, the total-field ratio is

\[
\frac{\ell_2}{\ell_1}
=\frac{\sqrt{1-[A_0+A_s(r_2)]}}
       {\sqrt{1-[A_0+A_s(r_1)]}}.
\]

Because the lapse is nonlinear, the common \(A_0\) does not literally
cancel from this exact ratio by ordinary numerator subtraction. The source
packet declares a local common-background subtraction for the weak clock
implementation, after which the endpoint inputs are the source lifts. This is
different from claiming that \(A_0\) is absent from the total substrate
state.

## 4. Weak endpoint limit

### 4.1 Expand one lapse

For \(|A|\ll1\), the binomial expansion gives

\[
\sqrt{1-A}
=1-\frac A2-\frac{A^2}{8}+O(A^3).
\]

To first order,

\[
\ell_i\simeq1-\frac{A_i}{2}.
\]

### 4.2 Expand the endpoint ratio

\[
\frac{\ell_2}{\ell_1}
\simeq
\frac{1-A_2/2}{1-A_1/2}.
\]

Using \((1-x)^{-1}\simeq1+x\),

\[
\frac{\ell_2}{\ell_1}
\simeq
\left(1-\frac{A_2}{2}\right)
\left(1+\frac{A_1}{2}\right)
\simeq1+\frac{A_1-A_2}{2}.
\]

Thus the fractional gain is

\[
\boxed{
\frac{\Delta f}{f}
\simeq\frac{A_1-A_2}{2}
}.
\]

The factor \(1/2\) comes from the first derivative of the square-root
lapse at weak field. It is not an adjustable coefficient.

### 4.3 Substitute the spherical source

\[
\begin{aligned}
\frac{\Delta f}{f}
&\simeq\frac12\left(\frac{2GM_s}{c^2r_1}
                         -\frac{2GM_s}{c^2r_2}\right)\\
&=\frac{GM_s}{c^2}\left(\frac1{r_1}-\frac1{r_2}\right).
\end{aligned}
\]

For a small upward height \(h\), \(r_2=r_1+h\), this becomes the
optical-height formula developed fully in `SAMA-D000006`.

## 5. Clock versus road: the type firewall

Consider fixed endpoints and two paths with different impact parameters. The
clock ratio above does not change, because \(A_1\) and \(A_2\) do not change.
The photon-road exposure

\[
T_A^\gamma[\Gamma]=\frac1c\int_\Gamma A_s\,ds
\]

does change. Conversely, moving an endpoint while preserving a path class
changes the clock comparison even when route changes are accounted for
separately.

`G:G374@SAM-ARCHIVE` executes this decomposition. With fixed endpoints, its
near and far roads differ by \(1.2385547434993276\times10^{-5}\) s while
the endpoint clock term changes by exactly zero. In its changed-endpoint
scenario, the clock fraction changes by
\(1.838357734854823\times10^{-10}\), and the road difference equals the
geometry difference to relative error \(2.01\times10^{-15}\). This is an
executed type-separation test, not only a verbal distinction.

## 6. GPS composition from separate ledgers

### 6.1 Gravitational endpoint term

Let \(r_g\) be ground radius and \(r_o\) orbital radius. Form

\[
A_g=\frac{2GM_\oplus}{c^2r_g},
\qquad
A_o=\frac{2GM_\oplus}{c^2r_o}.
\]

The exact endpoint gain is

\[
\delta_{\rm grav}^{\rm exact}
=\sqrt{\frac{1-A_o}{1-A_g}}-1,
\]

and its weak value is

\[
\delta_{\rm grav}^{\rm weak}
=\frac{A_g-A_o}{2}.
\]

### 6.2 Orbital-motion term

For the declared circular-orbit approximation,

\[
v_o=\sqrt{\frac{GM_\oplus}{r_o}},
\]

and the separately typed SR contribution is

\[
\delta_{\rm SR}=-\frac{v_o^2}{2c^2}.
\]

This term is not derived by adding another \(A\)-source. It is a motion
correction whose output units match the gravitational fraction.

### 6.3 Compose only at the output ledger

\[
\delta_{\rm net}
=\delta_{\rm grav}+\delta_{\rm SR},
\]

\[
\Delta t_{\rm day}
=86400\,\delta_{\rm net}.
\]

Multiplication by \(10^6\) converts seconds/day to microseconds/day. The
addition is valid because both lanes have already produced dimensionless clock
fractions; it does not merge their causes.

### 6.4 Registered GPS packet

[`CR:CR005@03`](../../tests/courtroom/03-clocks-and-gps-cr005-clocks-and-gps-external-contact/README.md) records

| Quantity | Value |
|---|---:|
| \(A_{\rm ground}\) | \(1.390697013601\times10^{-9}\) |
| \(A_{\rm orbit}\) | \(3.339629547528\times10^{-10}\) |
| orbital speed | \(3873.957505513\) m s\(^{-1}\) |
| gravitational gain | \(+45.650919844320\) \(\mu\)s/day |
| orbital SR loss | \(-7.213602515321\) \(\mu\)s/day |
| net correction | \(+38.437317328999\) \(\mu\)s/day |
| factory frequency | \(10229999.995448915288\) Hz |

The source execution is `CLEAN`, the source scientific verdict is `PASS`, and
no fitted parameters were introduced. Its scope excludes Shapiro delay, full
GPS engineering, full GR and an independent derivation of SR.

## 7. Endpoint-clock derivation and holdout

| Stage | Exact key | Surviving contribution and boundary |
|---|---|---|
| Endpoint construction | `G:G371@SAM-ARCHIVE` | Replayed exact and weak height/GPS endpoint ratios; preserved finite-radius GPS rather than treating near-surface \(gH/c^2\) as exact at orbit altitude. |
| Typed GPS composition | `G:G373@SAM-ARCHIVE` | Added the separate SR motion loss and rejected calling it an \(A\)-effect. |
| Channel-decomposition boundary | `G:G374@SAM-ARCHIVE` | Demonstrated that endpoint clock, route delay and orbital motion respond to different changes and rejected double counting. |
| Weak redshift result | `G:G409@SAM-ARCHIVE` | Recovered the Pound--Rebka-scale endpoint fraction, energy scaling and sign while rejecting road-delay substitution. |
| External contact | [`CR:CR005@03`](../../tests/courtroom/03-clocks-and-gps-cr005-clocks-and-gps-external-contact/README.md) | Re-ran the scoped GPS packet without older G-test outputs, with zero fitted parameters and wrong-control rejection. |
| Independent holdout | [`CR:CR006@03`](../../tests/courtroom/03-clocks-and-gps-cr006-optical-clock-height-holdout-endpoint-a-kernel/README.md) | Applied the fixed endpoint formula to an independently selected millimetre optical-clock geometry; the full result and classification are owned by `SAMA-D000006`. |

The chain keeps its deviations. G371 shows why the small-height approximation
cannot be extrapolated unchanged to GPS altitude. G373 shows why omitting the
SR term gives the wrong net engineering quantity. G374 shows why a generic
“gravity timing” bucket double counts distinct channels. The Courtroom tests
then recertify and independently hold out those repaired types.

## 8. Wrong controls and diagnostic alternatives

| Wrong control | Recorded effect | Corrective lesson |
|---|---|---|
| Use \(A=GM/(c^2r)\) | Halves the G371/G373 gravitational signal. | Retain \(r_s=2GM/c^2\). |
| Use \(\Delta A\) rather than \(\Delta A/2\) | Doubles the weak clock shift. | The half comes from the lapse expansion. |
| Reverse endpoint order | Makes the higher clock slower and reverses the sign. | Declare endpoint/sign convention before evaluation. |
| Use \(A_0\) as the height difference | G371 records a relative miss above \(2.4\times10^{12}\). | Background-subtract the shared floor in the local weak implementation. |
| Use constant surface \(gH/c^2\) at GPS altitude | Misses the finite-radius target by a factor-scale recorded relative miss \(3.167\). | Use the exact \(1/r_g-1/r_o\) difference. |
| Omit orbital SR | Leaves the net GPS correction too high. | Keep the motion ledger separate, then add outputs. |
| Treat SR loss as \(A\)-clock effect | Changes category and obscures provenance. | Retain \(-v_o^2/(2c^2)\) as declared external physics. |
| Make clock depend on impact parameter | Converts an endpoint operator into a road operator. | Fixed endpoints imply fixed clock term. |
| Add clock term again inside road delay | G374 records \(84.08589266868549\) \(\mu\)s versus \(38.43626928544392\) \(\mu\)s in its example. | Sum unique channels once. |

## 9. Established result, boundaries and forward handoff

Carry forward

\[
\boxed{
\frac{(d\tau_2/dt)}{(d\tau_1/dt)}
=\sqrt{\frac{1-A_2}{1-A_1}},
\qquad
\frac{\Delta f}{f}\simeq\frac{A_1-A_2}{2}
}
\]

and for the typed GPS ledger

\[
\boxed{
\delta_{\rm GPS}
=\frac{A_g-A_o}{2}-\frac{v_o^2}{2c^2}
}
\]

in the weak implementation, with exact lapse available for the gravitational
part. The total substrate field retains \(A_0\); the local implementation
must declare its common-background treatment rather than asserting nonlinear
exact cancellation.

No SAMA result classification is assigned in this chapter. The optical-clock
classification is stated in `SAMA-D000006`; the registered GPS source
`PASS` remains a source verdict here. `SAMA-D000007` receives the same field
with a route integral rather than the endpoint coefficient.

Exact evidence is the complete seven-key sequence in Section 10. The
specifically open boundary is strong-field clock comparison, a complete GPS
engineering model and every photon-road observable, each of which requires a
separate operator or focused document.

## 10. Focused test and result index

| Exact qualified key | Evidence role | Preserved outcome | Direct result | Result folder |
|---|---|---|---|---|
| `G:G371@SAM-ARCHIVE` | Endpoint construction | `G371_SAM_GRAVITATIONAL_REDSHIFT_WRITE_RATE_PASS` | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G371_SAM_gravitational_redshift_write_rate/G371_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G371_SAM_gravitational_redshift_write_rate) |
| `G:G373@SAM-ARCHIVE` | GPS composition | `G373_GPS_A_CLOCK_GAIN_WITH_SEPARATE_SR_MOTION_CORRECTION_PASS` | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G373_GPS_A_CLOCK_WITH_SR_MOTION_CORRECTION/G373_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G373_GPS_A_CLOCK_WITH_SR_MOTION_CORRECTION) |
| `G:G374@SAM-ARCHIVE` | Channel boundary | `G374_SAM_CLOCK_ROAD_DELAY_DECOMPOSITION_PASS` | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G374_SAM_CLOCK_ROAD_DELAY_DECOMPOSITION/G374_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G374_SAM_CLOCK_ROAD_DELAY_DECOMPOSITION) |
| `G:G409@SAM-ARCHIVE` | Weak-redshift result | `G409_POUND_REBKA_A_CLOCK_PHOTON_REDSHIFT_PASS` | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G409_POUND_REBKA_A_CLOCK_PHOTON_REDSHIFT/G409_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G409_POUND_REBKA_A_CLOCK_PHOTON_REDSHIFT) |
| [`CR:CR005@03`](../../tests/courtroom/03-clocks-and-gps-cr005-clocks-and-gps-external-contact/README.md) | GPS external result | Source execution `CLEAN`, scientific verdict `PASS`; zero-fit scoped clock/GPS packet. | [result](../../courtroom/03_CLOCKS_AND_GPS/CR005_CLOCKS_AND_GPS_EXTERNAL_CONTACT/CR005_result.md) | [folder](../../courtroom/03_CLOCKS_AND_GPS/CR005_CLOCKS_AND_GPS_EXTERNAL_CONTACT) |
| [`CR:CR006@03`](../../tests/courtroom/03-clocks-and-gps-cr006-optical-clock-height-holdout-endpoint-a-kernel/README.md) | Independent endpoint holdout | Registry has no structured status/verdict; pinned source records `PASS_OPTICAL_CLOCK_ENDPOINT_HOLDOUT`. | [result](../../courtroom/03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL/CR006_result.md) | [folder](../../courtroom/03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL) |

## 11. Atomic record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000003-R001` | Separates endpoint-clock and photon-road readouts. |
| `SAMA-C000036-R001` | Types common-floor retention and local treatment. |
| `SAMA-C000046-R001` | Defines the exact static endpoint lapse ratio. |
| `SAMA-C000047-R001` | Derives the weak endpoint comparison and its one-half coefficient. |
| `SAMA-C000048-R001` | Defines the typed GPS gravitational-plus-SR composition. |
| `SAMA-C000049-R001` | Records the GPS external-contact numerical packet. |
| `SAMA-C000122-R001` | Enforces the Volume I/II/III subject boundary. |
| `SAMA-C000124-R001` | Separates source-era chronology from current live authority. |
| `SAMA-C000125-R001` | Preserves source verdicts, authorized classifications and false approval state. |

## 12. Source and approval boundary

The direct evidence set is exactly the six qualified keys above. Courtroom
links are pinned to commit `b5e914f71377e86ef4c67e199973d9300795cda1`;
archive links resolve to the exact locally registered artifacts. Older uses of
“latest” remain source-era chronology unless installed by live authority.

`reviewed_and_approved` remains `false`; `approval` remains `null`. Successful
clock contact, exact/weak agreement and mechanical validation do not imply
owner approval.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`CR:CR005@03`](../../tests/courtroom/03-clocks-and-gps-cr005-clocks-and-gps-external-contact/README.md) | [CR005_PRECOMMIT.md](../../courtroom/03_CLOCKS_AND_GPS/CR005_CLOCKS_AND_GPS_EXTERNAL_CONTACT/CR005_PRECOMMIT.md)<br>[CR005_declared_premises.json](../../courtroom/03_CLOCKS_AND_GPS/CR005_CLOCKS_AND_GPS_EXTERNAL_CONTACT/CR005_declared_premises.json) | [CR005_runner.py](../../courtroom/03_CLOCKS_AND_GPS/CR005_CLOCKS_AND_GPS_EXTERNAL_CONTACT/CR005_runner.py) | [CR005_candidate_rows.csv](../../courtroom/03_CLOCKS_AND_GPS/CR005_CLOCKS_AND_GPS_EXTERNAL_CONTACT/CR005_candidate_rows.csv) | [CR005_result.md](../../courtroom/03_CLOCKS_AND_GPS/CR005_CLOCKS_AND_GPS_EXTERNAL_CONTACT/CR005_result.md)<br>[CR005_summary.json](../../courtroom/03_CLOCKS_AND_GPS/CR005_CLOCKS_AND_GPS_EXTERNAL_CONTACT/CR005_summary.json) | [All 8 files](../../tests/courtroom/03-clocks-and-gps-cr005-clocks-and-gps-external-contact/README.md) |
| [`CR:CR006@03`](../../tests/courtroom/03-clocks-and-gps-cr006-optical-clock-height-holdout-endpoint-a-kernel/README.md) | [CR006_PRECOMMIT.md](../../courtroom/03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL/CR006_PRECOMMIT.md)<br>[CR006_PREFLIGHT.md](../../courtroom/03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL/CR006_PREFLIGHT.md) | [CR006_runner.py](../../courtroom/03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL/CR006_runner.py) | [CR006_CONTROLS.csv](../../courtroom/03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL/CR006_CONTROLS.csv) | [CR006_INTERNAL_SOURCE_AUDIT.md](../../courtroom/03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL/CR006_INTERNAL_SOURCE_AUDIT.md)<br>[CR006_result.md](../../courtroom/03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL/CR006_result.md)<br>[CR006_summary.json](../../courtroom/03_CLOCKS_AND_GPS/CR006_OPTICAL_CLOCK_HEIGHT_HOLDOUT_ENDPOINT_A_KERNEL/CR006_summary.json) | [All 26 files](../../tests/courtroom/03-clocks-and-gps-cr006-optical-clock-height-holdout-endpoint-a-kernel/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000005`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/ENDPOINT_CLOCK_COMPARISON_AND_TIME_DILATION.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000005 | Clock and Traversal | Exact and Weak Endpoint Lapse with Typed GPS Composition |

| Document field | Value |
|---|---|
| Purpose | Derive exact and weak endpoint lapse comparisons, compose the GPS gravitational and kinematic channels by type, and preserve the complete clock evidence route. |
| Prerequisite documents | `SAMA-D000003`, `SAMA-D000004` |
| Used by | `SAMA-D000006`, `SAMA-D000009`, `SAMA-D000014`; assembled into `SAMA-P000005` and `SAMA-P000002`. |
| Primary source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`, SHA-256 `2f22500f6583f567e350974610f00142e89b081a5b8c4c90c6dfe89bec43be0d`. |
| Revision state | Source-bound draft; mechanically registered proposal; not reviewed or approved. |

</details>
