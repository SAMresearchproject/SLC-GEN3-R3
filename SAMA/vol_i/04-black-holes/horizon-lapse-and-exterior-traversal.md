[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Horizon Lapse and Exterior Traversal

## Current research connections — 14 September 2026

The global execution authority is SLC-GEN3-R3 / SLC-GEN3-CEV1-R3. The September 2026 research includes exact retained-history computation, RH arithmetic compensation, native Mersenne work, Starbreaker signed reception and ATOM3D contact/grammar. The research index connects the retained derivations to the latest code, results and current domain assignments.

[Current derivations, code and results](../../../docs/RESEARCH.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

The horizon branch contains two related but different measurements. A static
clock at accumulation \(A\) reads the exact lapse

\[
\ell(A)=\sqrt{1-A}.
\]

An outward radial signal consumes a route operator:

\[
dt=\frac{dr}{c[1-A(r)]}.
\]

The first is an endpoint rate. The second is an accumulated exterior road.
They meet at the same boundary, but they do not become the same operator. As
\(A\to1^-\), the lapse tends to zero, the redshift relative to infinity
diverges, and the radial road grows logarithmically. Exact \(A=1\) is therefore
the closure endpoint of this static exterior construction, not an ordinary
place from which one starts a finite road.

That distinction also controls the multimessenger handoff. After a dynamic
release, gravitational and electromagnetic packets share the post-release
road. Their observed seconds-scale offset is typed to source-engine or release
time, not to unequal propagation speeds and not to a static photon launched at
exact closure.

## 1. Opening question and conceptual picture

This chapter asks:

> Starting from the normalized source coordinate \(A=r_s/r\), what exact
> operators govern a static endpoint and an exterior radial route, how does
> each operator approach unit closure, and how must that boundary be kept
> separate from a dynamic source-release delay?

The conceptual picture has three layers.

1. The coordinate \(A\) labels where the exterior sample lies.
2. The lapse \(\ell\) reads a static clock at that sample.
3. The radial primitive integrates the coordinate traversal between two
   exterior samples.

The layers are joined by a common source profile, not by treating coordinate,
clock and route as synonyms.

## 2. Typed definitions, domains and units

| Quantity | Definition | Type | Units/domain |
|---|---|---|---|
| \(M\) | spherical source mass | source input | kg |
| \(r_s\) | \(2GM/c^2\) | source length | m |
| \(r\) | exterior areal radius | geometric coordinate | m, \(r>r_s\) |
| \(x\) | \(r/r_s\) | normalized exterior radius | dimensionless, \(x>1\) |
| \(A\) | \(r_s/r=1/x\) | accumulation coordinate | dimensionless, \(0<A<1\) on an ordinary exterior sample |
| \(\ell(A)\) | \(\sqrt{1-A}\) | static endpoint lapse | dimensionless |
| \(z(A)\) | \(\ell^{-1}-1\) | redshift relative to infinity | dimensionless |
| \(dt\) | \(dr/[c(1-A)]\) | exterior coordinate-traversal increment | s |
| \(\mathcal R(x_1,x_2)\) | \(c\Delta t/r_s\) | normalized exterior road | dimensionless |
| \(\tau_{\rm engine}\) | dynamic release/source-reorganization delay | source event interval | s |
| \(\Delta t_{\rm road}^{\rm GW-EM}\) | differential after both channels are released | propagation comparison | s |

Two domain statements are load-bearing:

- the static exterior formulas use \(x>1\), equivalently \(A<1\);
- the limit \(A\to1^-\) may be evaluated, but exact \(A=1\) is not substituted
  as a regular lower endpoint of a finite route.

The locally measured propagation constant remains \(c\). The factor \(1-A\)
belongs to the exterior coordinate road and does not redefine
\(c_{\rm local}\).

## 3. Derive the exact lapse and redshift

For the declared nonrotating exterior lane, the radial-time part of the static
line element is organized by

\[
ds^2=-c^2(1-A)\,dt^2+\frac{dr^2}{1-A}+\cdots.
\]

For a static endpoint, \(dr=0\). Proper time therefore satisfies

\[
-c^2d\tau^2=-c^2(1-A)\,dt^2,
\]

so

\[
\boxed{\frac{d\tau}{dt}=\ell(A)=\sqrt{1-A}}.
\]

The frequency ratio of the static endpoint to the reference at infinity is
the same lapse. Hence the redshift is

\[
1+z=\frac1{\ell(A)},
\]

and therefore

\[
\boxed{z(A)=\frac1{\sqrt{1-A}}-1}.
\]

### 3.1 Recover the weak endpoint limit

Use the binomial series:

\[
(1-A)^{-1/2}
=1+\frac A2+\frac{3A^2}{8}
+\frac{5A^3}{16}+\cdots.
\]

Then

\[
z(A)=\frac A2+\frac{3A^2}{8}
+\frac{5A^3}{16}+\cdots.
\]

The familiar \(A/2\) term is the first weak coefficient. It is not the exact
strong-field redshift.

At the ISCO, \(A=1/3\):

\[
z_{\rm exact}
=\sqrt{\frac32}-1
=0.224744871392\ldots,
\]

while

\[
z_{\rm weak}=\frac16=0.166666666667\ldots.
\]

At the photon sphere, \(A=2/3\):

\[
z_{\rm exact}=\sqrt3-1
=0.732050807569\ldots.
\]

The exact expression is therefore required before reaching closure.

### 3.2 Take the closure limit

Let

\[
A=1-\delta,\qquad \delta>0.
\]

Then

\[
\ell=\sqrt{\delta},
\qquad
z=\delta^{-1/2}-1.
\]

Thus

\[
\lim_{\delta\to0^+}\ell=0,
\qquad
\lim_{\delta\to0^+}z=\infty.
\]

No finite weak-series truncation can move or soften this boundary.

## 4. Derive the exterior radial primitive

For a radial null route, set \(ds^2=0\) in the declared exterior lane:

\[
0=-c^2(1-A)\,dt^2+\frac{dr^2}{1-A}.
\]

Choose the outward sign. Multiplying by \(1-A\) and taking the positive square
root gives

\[
\frac{dr}{dt}=c(1-A).
\]

Solve for the time increment:

\[
\boxed{
dt=\frac{dr}{c[1-A(r)]}
}.
\]

Now insert

\[
A(r)=\frac{r_s}{r},
\qquad
x=\frac r{r_s},
\qquad
dr=r_s\,dx.
\]

Then

\[
c\,dt
=\frac{r_s\,dx}{1-1/x}
=r_s\frac{x}{x-1}\,dx.
\]

Split the rational factor:

\[
\frac{x}{x-1}=1+\frac1{x-1}.
\]

Integrating gives

\[
\frac{ct}{r_s}
=\int\left(1+\frac1{x-1}\right)dx
=x+\ln|x-1|+C.
\]

For \(1<x_1<x_2\),

\[
\boxed{
\frac{c\Delta t}{r_s}
=(x_2-x_1)
+\ln\!\left(\frac{x_2-1}{x_1-1}\right)
}.
\]

This result contains a flat radial separation,
\(x_2-x_1\), and an accumulation-conditioned logarithmic extra. The two terms
have the same dimensionless normalization but distinct origins.

### 4.1 Make the logarithmic closure explicit

Let the starting radius be

\[
x_1=1+\varepsilon,\qquad \varepsilon>0.
\]

For a fixed exterior endpoint \(x_2\),

\[
\frac{c\Delta t}{r_s}
=(x_2-1-\varepsilon)
+\ln(x_2-1)-\ln\varepsilon.
\]

As \(\varepsilon\to0^+\), the bounded terms remain finite and

\[
\frac{c\Delta t}{r_s}
\sim-\ln\varepsilon.
\]

The divergence is logarithmic. It is a route result, whereas
\(\ell\sim\sqrt{\delta}\) is an endpoint result.

## 5. Horizon lapse and exterior road

[`CR:CR008@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr008-clock-traversal-closure/README.md) evaluates the two operators together while preserving their
types. Its near-horizon rows are:

| Exterior sample | \(A\) | Lapse | Redshift | \(c\Delta t/r_s\) to \(x=3\) |
|---:|---:|---:|---:|---:|
| \(10^{-3}\) cutoff | \(0.999000000000\) | \(3.162277660168\times10^{-2}\) | \(30.62277660168\) | \(9.599902459542\) |
| \(10^{-6}\) cutoff | \(0.999999000000\) | \(1.000000000014\times10^{-3}\) | \(998.9999999856\) | \(16.508656738606\) |
| \(10^{-9}\) cutoff | \(0.999999999000\) | \(3.162277615451\times10^{-5}\) | \(3.162177704886\times10^4\) | \(23.416412933766\) |
| \(10^{-12}\) cutoff | \(0.999999999999\) | \(9.999889390788\times10^{-7}\) | \(1.000010061044\times10^6\) | \(30.324079399857\) |

The source execution status is `CLEAN` and its scientific verdict is
`BOUNDARY`. The boundary grade is retained. It records exact exterior closure
without claiming a complete freely falling observer construction.

[`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) later replays the same lane from the locked primitive stack. It
retains \(A=1\) as the no-completed-parent-ledger/no-literal-photon-launch
boundary, reproduces the \(10^{-12}\) lapse and redshift row, and rejects
softening controls. The replay does not overwrite the earlier `BOUNDARY`
record.

### 5.1 Historical G90 modified-tortoise branch

`G:G90@SAM-ARCHIVE` is a construction ancestor, not a second name for the
settled primitive above. Its source-era lane introduced

\[
F(y)=1-5y^4+4y^5,\qquad y=3A-2,
\]

inside the photon sphere, with local adjustment

\[
\frac{(dr_*/dr)_{\rm SAM}}{(dr_*/dr)_{\rm GR}}
=\frac1{\sqrt{F(y)}}.
\]

That archived branch recorded unity outside the photon sphere, enhanced
traversal inside it, and a power-law near-horizon divergence for its modified
road. It also recorded that an earlier interpolation should not be used for
precision work in that lane.

The installed Volume I spine instead carries the declared exterior primitive

\[
dt=\frac{dr}{c(1-A)}
\]

and its logarithmic closure. The correct preservation rule is therefore:

- keep G90 as historical modified-road evidence;
- do not silently substitute its \(F(y)\) into the settled exterior formula;
- do not erase it merely because the later registered chain has a different
  operator.

This is a genuine deviation chain, not two mutually interchangeable formulas.

## 6. Why exact unit closure is not an ordinary launch

At exact \(A=1\):

\[
\ell(1)=0,
\qquad
z(1)=\infty,
\qquad
\int_{1}^{x_2}\frac{x\,dx}{x-1}=\infty.
\]

All three statements point to the same exterior boundary. An ordinary launch
would require a finite static endpoint rate and a finite first route segment.
Neither exists under this construction.

A dynamic release surface is different. It satisfies

\[
A_{\rm release}<1
\]

and is supplied by a source-engine model. Once a channel reaches that surface,
its outward propagation can use the shared exterior road. The release process
itself is not manufactured by inserting exact \(A=1\) as an ordinary starting
coordinate.

## 7. Historical source-engine discovery chain

### 7.1 G699c: separate engine time from propagation

`G:G699c@SAM-ARCHIVE` used a frozen \(2.7000M_\odot\) total mass and the
source-era scaling

\[
\tau_{\rm engine}
=0.620969982748\ \frac{\mathrm{s}}{M_\odot}M_{\rm total}.
\]

It obtained

\[
\tau_{\rm engine}=1.676618953419\ \mathrm{s}
\]

against a \(1.740000000000\ \mathrm{s}\) observed delay. The residual was
\(0.063381046581\ \mathrm{s}\), the absolute percent difference was
\(3.642589\%\), and the engine fraction was \(0.963574111\).

The one-sided propagation control assigned only one messenger the long
accumulation road. It produced \(9.524889\times10^7\ \mathrm{s}\), or about
\(3.018255\) years—more than \(5.47\times10^7\) times the observed delay. That
control localized the viable lane to a shared road plus local engine time.

### 7.2 G700c: investigate the residual without reopening the long road

`G:G700c@SAM-ARCHIVE` kept the shared-road differential at zero and split the
remaining \(0.063381046581\ \mathrm{s}\) into source-side diagnostics.

Its mass-equivalent residual was

\[
\Delta M=0.1020678106M_\odot,
\]

so a total mass \(2.8020678106M_\odot\) would close the source-era scaling.
At \(2.80M_\odot\), the residual fell to
\(0.001284048306\ \mathrm{s}\).

The alternative \(A\)-start product was

\[
A\,L=c\,\Delta t
=1.9001159745092\times10^7\ \mathrm{m}.
\]

At \(A=1\), \(A=0.3\), and \(A=0.1\), this corresponds formally to path
lengths of about \(19{,}001\), \(63{,}337\), and \(190{,}012\) km. Those rows
are source-structure diagnostics, not authorization for a static launch at
unit closure.

The weak radial lane required

\[
\ln(r_{\rm join}/r_{\rm emit})=2382.884,
\]

so the archived classifier recorded
`WEAK_RADIAL_A_ROAD_ALONE_DOES_NOT_CLOSE`. The long-distance split remained
closed.

### 7.3 G701c: blind mock before real-event reveal

`G:G701c@SAM-ARCHIVE` is registered at its Stage 0 mock, before a real event
delay was read. Its frozen status states:

\[
\text{real event delay read}=\mathrm{false}.
\]

For its typed mock,

\[
A_{\rm GW}=0.5,\qquad
A_{\rm light}=\frac16,\qquad
L=40\ \mathrm{m},
\]

the pipeline returned a \(0.290138771133\ \mathrm{s}\) combined delay. The
sign-inverted control returned \(0.509861228867\ \mathrm{s}\). All five Stage
0 readiness conditions passed. This record establishes blind arithmetic and
wrong-control discrimination only; it does not retrospectively become the
real-event result.

## 8. Source-engine and shared-road split

[`CR:CR147@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr147-gw170817-a-release-em-origin-differential/README.md) is the fresh established-reference result in this chapter. It
uses the published \(2.74^{+0.04}_{-0.01}M_\odot\) total mass rather than the
older rounded \(2.70M_\odot\) input. The declared release surface is

\[
\frac{r_{\rm release}}{r_s}=17.820688709132,
\qquad
A_{\rm release}=0.056114554063.
\]

The source-engine calculation gives

\[
\tau_{\rm release}=1.701457752729\ \mathrm{s},
\]

with residual

\[
1.740000000000-1.701457752729
=0.038542247271\ \mathrm{s}
=0.770845\,\sigma.
\]

The published mass band maps to

\[
1.695248052902\ \mathrm{s}
\le\tau_{\rm release}\le
1.726296552039\ \mathrm{s}.
\]

The static first-order local road across the declared gap is only

\[
7.774813823799\times10^{-5}\ \mathrm{s},
\]

about \(2.2380\times10^4\) below the observed seconds-scale lag. Forcing that
static operator to fit would require an implausible logarithmic lever arm
\(\ln(r_{\rm release}/r_{\rm origin})=64462.334846\).

The source execution is `CLEAN` and its scientific verdict is `PASS`. Its
typed conclusion is:

- dynamic release/source-engine reorganization carries the local lag;
- after release, the two messengers share the same \(A\)-road;
- exact \(A=1\) remains a no-ordinary-launch boundary.

## 9. Deviation chains and wrong controls

| Wrong or historical route | What happens | Correction retained by the registered chain |
|---|---|---|
| Use \(z=A/2\) at the ISCO or photon sphere | The weak truncation understates the exact redshift and cannot reach the closure divergence. | Use \(z=(1-A)^{-1/2}-1\). |
| Start the radial integral at \(x=1\) | The lower endpoint is singular; the road is not finite. | Work at \(x_1>1\) and take the exterior limit explicitly. |
| Identify lapse with route time | An endpoint scalar is substituted for an integral. | Keep \(\ell(A)\) and \(\mathcal R(x_1,x_2)\) separately typed. |
| Insert the G90 \(F(y)\) adjustment into the settled exterior primitive | A historical modified-tortoise lane silently replaces the registered current derivation. | Preserve G90 as history and use the spine/CR008 primitive for this chapter. |
| Give GW and EM different post-release speeds | The one-sided long-road differential is orders of magnitude too large. | Use a common road after release. |
| Explain \(1.74\) s by a plain static local \(A\)-integral | The fresh CR147 integral is \(7.77\times10^{-5}\) s. | Keep the seconds-scale term in dynamic source reorganization. |
| Fit an origin radius or exact-delay mass | The control targets the output after reveal and breaks the declared mass input. | Use the published mass band and fixed release law. |
| Treat the blind mock as the real event | Stage 0 explicitly did not read the observed delay. | Preserve mock readiness separately from CR147's real-event result. |
| Launch light from exact \(A=1\) | Static lapse is zero and the exterior road is divergent. | Launch only from a separately typed dynamic release surface with \(A<1\). |
| Convert the exterior result into a complete infaller theory | The measurable freely falling ruler has not been supplied by these operators. | Keep that construction as a precise continuation task. |

## 10. Evidence sequence and preserved statuses

| Sequence | Exact qualified key | Role | Preserved result or boundary |
|---:|---|---|---|
| 1 | `G:G90@SAM-ARCHIVE` | historical construction | Modified-tortoise adjustment and source-era power-law lane; not silently substituted into the settled exterior primitive. |
| 2 | [`CR:CR008@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr008-clock-traversal-closure/README.md) | boundary | Exact lapse, redshift divergence and logarithmic exterior road; source `CLEAN`/`BOUNDARY`. |
| 3 | [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | retest | Locked-stack replay, no-literal-launch boundary and scoped strong-field classification. |
| 4 | `G:G699c@SAM-ARCHIVE` | engine/road construction | Shared post-release road plus \(2.70M_\odot\) engine-time packet. |
| 5 | `G:G700c@SAM-ARCHIVE` | residual construction | Mass and \(A\)-start diagnostics; weak radial road alone does not close. |
| 6 | `G:G701c@SAM-ARCHIVE` | blind control | Stage 0 mock arithmetic and sign-control discrimination before real-event reveal. |
| 7 | [`CR:CR147@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr147-gw170817-a-release-em-origin-differential/README.md) | fresh result | Published-mass release calculation, static-road rejection and shared-road conclusion; source `CLEAN`/`PASS`. |

The chronology matters. A later correction supplements the earlier record; it
does not erase G90, the \(2.70M_\odot\) G699c row, the G700c residual, or the
blind mock.

## 11. Established result, boundary and forward handoff

The compression-safe exterior packet is

\[
\boxed{
\ell(A)=\sqrt{1-A},
\qquad
z(A)=\frac1{\sqrt{1-A}}-1,
\qquad
\frac{c\Delta t}{r_s}
=(x_2-x_1)+
\ln\!\frac{x_2-1}{x_1-1}
}.
\]

For the declared nonrotating exterior chain replayed by [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md):

**The test result suggests strong contact with the concept.**

That classification does not rewrite the source `BOUNDARY` verdict of
[`CR:CR008@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr008-clock-traversal-closure/README.md) and does not extend to a full infaller construction, Kerr
geometry, a complete Hawking spectrum, or a unique astrophysical engine.

`SAMA-D000017` receives the unit-closure gradient and thermodynamic conversion.
`SAMA-P000005` receives the endpoint/route distinction and the shared-road
multimessenger boundary.

Exact evidence is the complete seven-key sequence in Section 12. The
specifically open boundary is a substrate-native infaller ruler and road,
Kerr geometry, complete Hawking transport and any unique source-engine model.

## 12. Focused test and result index

| Exact qualified key | Evidence role | Preserved outcome | Direct result | Result folder |
|---|---|---|---|---|
| `G:G90@SAM-ARCHIVE` | Historical modified-road construction | G90 records \(F(y)\)-adjusted traversal inside the photon sphere and a source-era power-law divergence. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G90_SAM_tortoise_adjustment/results/G90_SAM_tortoise_adjustment_summary.md) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G90_SAM_tortoise_adjustment) |
| `G:G699c@SAM-ARCHIVE` | Engine/road construction | `G699c_PASS_NATIVE_MULTIMESSENGER_ENGINE_ROAD_SPLIT`; \(1.676618953419\) s engine row and zero shared-road differential. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G699c_GW170817_NATIVE_MULTIMESSENGER_ENGINE_ROAD_SPLIT/G699c_RESULT.md) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G699c_GW170817_NATIVE_MULTIMESSENGER_ENGINE_ROAD_SPLIT) |
| `G:G700c@SAM-ARCHIVE` | Residual construction | `G700c_PASS_LOCAL_SOURCE_A_START_RESIDUAL_SPLIT`; source residual localized without reopening long-distance propagation. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G700c_GW170817_LOCAL_SOURCE_A_START_RESIDUAL_SPLIT/G700c_RESULT.md) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G700c_GW170817_LOCAL_SOURCE_A_START_RESIDUAL_SPLIT) |
| `G:G701c@SAM-ARCHIVE` | Blind diagnostic control | `G701c_STAGE0_PASS_MOCK_AND_FREEZE_READY`; real-event delay unread and wrong sign distinguished. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G701c_BLIND_GW170817_SOURCE_OFFSET_A_DELAY/stage0_mock/G701c_STAGE0_MOCK_RESULT.md) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G701c_BLIND_GW170817_SOURCE_OFFSET_A_DELAY) |
| [`CR:CR008@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr008-clock-traversal-closure/README.md) | Exterior closure boundary | Source execution `CLEAN`, scientific verdict `BOUNDARY`; exact lapse and logarithmic road sequence. | [result](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_result.md) | [folder](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE) |
| [`CR:CR147@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr147-gw170817-a-release-em-origin-differential/README.md) | Fresh multimessenger result | Source execution `CLEAN`, scientific verdict `PASS`; \(1.701457752729\) s published-mass release row and static-road rejection. | [result](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/CR147_result.md) | [folder](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL) |
| [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | Locked-stack retest | `LC11_PASS_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY_FROM_LOCKED_PRIMITIVE_STACK`; 100/100 checks and 8/8 wrong controls. **The test result suggests strong contact with the concept.** | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY) |

## 13. Atomic record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000003-R001` | Supplies the local photon-road operator type. |
| `SAMA-C000004-R001` | Preserves invariant local \(c\) and coordinate-road typing. |
| `SAMA-C000040-R001` | Types \(A=1\) as source-scale closure. |
| `SAMA-C000046-R001` | Supplies the exact static endpoint lapse ratio. |
| `SAMA-C000061-R001` | Separates common post-release propagation from engine delay. |
| `SAMA-C000074-R001` | Defines \(x=r/r_s\) and \(A=1/x\). |
| `SAMA-C000075-R001` | Supplies the ordered nonrotating landmark tuple. |
| `SAMA-C000076-R001` | Enforces the weak/strong operator-domain boundary. |
| `SAMA-C000077-R001` | Supplies exact lapse and redshift. |
| `SAMA-C000078-R001` | Supplies the integrated exterior radial primitive. |
| `SAMA-C000079-R001` | Records the executable logarithmic closure sequence. |
| `SAMA-C000080-R001` | Bars an ordinary static launch at exact unit closure. |
| `SAMA-C000090-R001` | Supplies the locked strong-field replay and scoped classification. |
| `SAMA-C000122-R001` | Enforces the Volume I and cross-volume subject boundary. |
| `SAMA-C000124-R001` | Separates source-era chronology from current authority. |
| `SAMA-C000125-R001` | Preserves source statuses, classification and false approval state. |

## 14. Source chronology and approval boundary

The seven exact evidence keys above are individually registered. Archive tests
retain their source-era formulas and verdict strings. Courtroom and Last
Campaign links are pinned to commit
`b5e914f71377e86ef4c67e199973d9300795cda1`. Executable artifacts control
their numerical results; active `SAM_LIVE` documents control present-tense
interpretation.

This chapter owns the substrate coordinate, static lapse, exterior route and
source/road timing split. Matter supplies a source through a typed interface
but its carrier grammar remains Volume II. Executable carrier internals remain
Volume III.

`reviewed_and_approved` remains `false`; `approval` remains `null`. Source
fidelity, hashes, validation, the preserved `PASS`/`BOUNDARY` statuses and the
strong-contact classification do not constitute owner approval.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`CR:CR008@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr008-clock-traversal-closure/README.md) | [CR008_PRECOMMIT.md](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_PRECOMMIT.md)<br>[CR008_declared_premises.json](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_declared_premises.json) | [CR008_runner.py](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_runner.py) | [CR008_runner.py](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_runner.py)<br>[CR008_candidate_summary.csv](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_candidate_summary.csv)<br>[CR008_result.md](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_result.md)<br>[CR008_summary.json](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_summary.json) | [CR008_candidate_summary.csv](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_candidate_summary.csv)<br>[CR008_result.md](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_result.md)<br>[CR008_summary.json](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_summary.json) | [All 11 files](../../tests/courtroom/05-strong-field-and-horizon-closure-cr008-clock-traversal-closure/README.md) |
| [`CR:CR147@04`](../../tests/courtroom/04-photon-road-shapiro-delay-cr147-gw170817-a-release-em-origin-differential/README.md) | [All package files](../../tests/courtroom/04-photon-road-shapiro-delay-cr147-gw170817-a-release-em-origin-differential/README.md) | [CR147_runner.py](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/CR147_runner.py) | [CR147_wrong_controls.csv](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/CR147_wrong_controls.csv) | [CR147_result.md](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/CR147_result.md)<br>[CR147_summary.json](../../courtroom/04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/CR147_summary.json) | [All 13 files](../../tests/courtroom/04-photon-road-shapiro-delay-cr147-gw170817-a-release-em-origin-differential/README.md) |
| [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | [LC11_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_wrong_controls.csv) | [LC11_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_result.md)<br>[LC11_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_summary.json) | [All 11 files](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000014`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/HORIZON_LAPSE_AND_EXTERIOR_TRAVERSAL.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000014 | Strong-Field Closure | Exact Horizon Lapse, Exterior Radial Primitive and Closure Boundary |

| Document field | Value |
|---|---|
| Purpose | Separate exact endpoint lapse from exterior radial traversal, derive the logarithmic road from start to finish, preserve the earlier modified-tortoise deviation, and state why exact unit closure is not an ordinary launch point. |
| Prerequisite documents | `SAMA-D000005`, `SAMA-D000009`, `SAMA-D000013` |
| Used by | `SAMA-D000017`; focused child of `SAMA-P000002` and `SAMA-P000005`. |
| Primary source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`, SHA-256 `2f22500f6583f567e350974610f00142e89b081a5b8c4c90c6dfe89bec43be0d`. |
| Revision state | Source-bound draft; mechanically registered proposal; not reviewed or approved. |

</details>
