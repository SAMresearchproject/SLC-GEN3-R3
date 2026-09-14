[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Time Dilation and Traversal Accumulation

## Current research connections — 14 September 2026

The global execution authority is SLC-GEN3-R3 / SLC-GEN3-CEV1-R3. The September 2026 research includes exact retained-history computation, RH arithmetic compensation, native Mersenne work, Starbreaker signed reception and ATOM3D contact/grammar. The research index connects the retained derivations to the latest code, results and current domain assignments.

[Current derivations, code and results](../../../docs/RESEARCH.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

One accumulation field can be read in several ways without those readouts
becoming one formula. A static clock compares the field at two endpoints. A
photon delay integrates a source lift along a route. A catalogued distance
can be converted through a declared accumulation-conditioned coordinate
factor. A cosmological road uses a separately constructed line-of-sight
account. Near a strong-field closure boundary the exact lapse and exterior
radial integral replace weak approximations.

The shared picture is a substrate tooth-rate and measurable tracks. The local
tooth-rate remains the invariant light speed (c). Accumulation changes the
clock lapse or the road by which an inferred distance is assembled. The
technical work of this parent is therefore a type-preserving synthesis:

\[
A\quad\xrightarrow[\text{choose geometry}]{\text{choose operator}}\quad
\begin{cases}
\text{endpoint lapse},\\
\text{local route delay},\\
\text{coordinate-distance conversion},\\
\text{cosmological road},\\
\text{exterior strong-field traversal}.
\end{cases}
\]

The operator label above the arrow is load-bearing. Removing it creates the
most important wrong controls in this branch.

## Reading map

| Order | Child | Question answered |
|---:|---|---|
| 1 | `SAMA-D000005` | How does a static clock compare two endpoint accumulations, and how is the weak limit composed with a separately typed kinematic term? |
| 2 | `SAMA-D000007` | How does a photon sample the source lift along a path, and why does the full geometry produce the Shapiro logarithm? |
| 3 | `SAMA-D000009` | How can `c_eff` describe an accumulation-conditioned coordinate road while local `c` remains invariant? |
| 4 | `SAMA-D000010` | Why is a local source integral not the same construction as the cosmological line-of-sight road? |
| 5 | `SAMA-D000014` | What happens to lapse and exterior traversal as the strong-field coordinate approaches exact unit closure? |

The optical-clock and binary-pulsar holdouts remain focused evidence leaves
under the main Volume I parent. They support this synthesis through the
clock and photon-road children without being silently reparented.

## 1. Starting object and notation

### 1.1 Source lift

For a spherical source of mass \(M\), define

\[
r_s=\frac{2GM}{c^2},
\qquad
A_s(r)=\frac{r_s}{r}=\frac{2GM}{c^2r}.
\]

Both \(r_s\) and \(r\) have units of length, so \(A_s\) is dimensionless.
The source surface \(r=r_s\) is therefore the exact coordinate value \(A=1\).
This algebraic identity does not yet state what any instrument reads.

### 1.2 Universal floor and total field

The universal floor is

\[
A_0=\frac{1}{\pi R}=\frac{1}{12\pi}.
\]

When the total account is required, write schematically

\[
A_{\rm total}=A_0+A_s+\cdots.
\]

A local comparison must then declare how a common floor is handled. If both
endpoints or the entire local experiment share the same background and the
operator is background-subtracted, the common part cancels. It is not deleted
from the substrate inventory, and it is not integrated as though it were a
local source profile.

### 1.3 Operator table

| Readout | Input | Operator | Output type |
|---|---|---|---|
| Static clock | endpoint values \(A_1,A_2\) | square-root lapse ratio | dimensionless frequency/rate ratio |
| Local photon road | \(A_s(\mathbf x)\) along \(\Gamma\) | \(c^{-1}\int_\Gamma A_s\,ds\) | time delay |
| Coordinate traversal | declared \(A\) or aggregate | multiplication by \(1-A\) | coordinate distance or speed-valued shorthand |
| Cosmological road | \(A_{\rm los}(z)\) | redshift-indexed distance conversion | native inferred distance/modulus |
| Exterior radial road | \(A=r_s/r\), \(r>r_s\) | \(dr/[c(1-A)]\) | exterior coordinate time |

The table is the minimal type firewall for everything that follows.

## 2. Endpoint clocks from the exact lapse

### 2.1 Question

Given two static clocks in the same declared background, what ratio follows
from their endpoint accumulations?

### 2.2 Exact relation

The static lapse assigned to one endpoint is

\[
\ell(A)=\frac{d\tau}{dt}=\sqrt{1-A},
\qquad 0\le A<1.
\]

For endpoints 1 and 2, divide the two rates rather than subtracting fields
prematurely:

\[
\frac{d\tau_2/dt}{d\tau_1/dt}
=\frac{\sqrt{1-A_2}}{\sqrt{1-A_1}}
=\sqrt{\frac{1-A_2}{1-A_1}}.
\]

This is dimensionless and becomes one when \(A_1=A_2\), as an endpoint
comparison must.

### 2.3 Weak difference, step by step

Let the field difference be small. Use

\[
\sqrt{1-u}=1-\frac{u}{2}-\frac{u^2}{8}+O(u^3).
\]

Then

\[
\ell(A_i)=1-\frac{A_i}{2}+O(A_i^2).
\]

The ratio may be expanded as

\[
\frac{1-A_2/2+O(A_2^2)}{1-A_1/2+O(A_1^2)}.
\]

Since \(1/(1-v)=1+v+O(v^2)\),

\[
\frac{\ell(A_2)}{\ell(A_1)}
=\left(1-\frac{A_2}{2}\right)
 \left(1+\frac{A_1}{2}\right)+O(A^2)
=1+\frac{A_1-A_2}{2}+O(A^2).
\]

Therefore the leading fractional comparison is

\[
\frac{\Delta f}{f}
\simeq\frac{A(r_1)-A(r_2)}{2}
=\frac{GM}{c^2}\left(\frac1{r_1}-\frac1{r_2}\right).
\]

The factor \(1/2\) appeared because the observable was the square-root lapse.
It is not a universal coefficient to be copied into a road integral.

### 2.4 Small height specialization

For an upward displacement \(h\ll r\), expand

\[
\frac1{r+h}=\frac1r\frac1{1+h/r}
=\frac1r\left(1-\frac hr+O(h^2/r^2)\right).
\]

Hence

\[
\frac1r-\frac1{r+h}=\frac{h}{r^2}+O(h^2/r^3).
\]

Substituting into the endpoint result gives

\[
\frac{\Delta f}{f}
\simeq\frac{GMh}{c^2r^2}
=\frac{gh}{c^2},
\]

where \(g=GM/r^2\) is introduced only at the last equality. Conceptually,
this remains an endpoint height difference; the force-like symbol \(g\) does
not change its type.

### 2.5 Executed evidence and deviations

CR005@03 keeps the endpoint gravitational gain and the special-relativistic
orbital loss as separate contributions before adding their readouts. It
records \(+45.650919844320\ \mu\mathrm{s/day}\),
\(-7.213602515321\ \mu\mathrm{s/day}\), and the resulting
\(+38.437317328999\ \mu\mathrm{s/day}\).

CR006@03 then applies the no-fit one-millimetre height formula. Its prediction
is \(1.089951994739\times10^{-19}\), compared with the selected strontium
clock measurement \((9.8\pm2.3)\times10^{-20}\), giving \(z=0.4781\).
**The test result suggests strong contact with the concept.**

The preserved wrong controls explain the retained formula. Leaving a common
floor uncancelled introduces a background contribution that is not an
endpoint difference. Doubling the coefficient removes the square-root lapse
origin. Reversing the sign reverses which clock runs faster. A force-like
radial power changes an endpoint potential difference into another operator.
A route-time substitution makes the result path-dependent when the question
fixed only two endpoints.

## 3. Photon roads from path geometry

### 3.1 Question

If the same source field is sampled by a photon along a path, what quantity
replaces the endpoint comparison?

### 3.2 Functional definition

For a route \(\Gamma\), define

\[
T_A^\gamma[\Gamma]
=\frac1c\int_\Gamma A_s(\mathbf x)\,ds.
\]

Because \(A_s\) is dimensionless and \(ds/c\) has units of time, the output is
a time. Two paths with the same endpoints can have different values; route
geometry is part of the input.

### 3.3 Straight-path derivation

Take a straight coordinate \(x\) with impact parameter \(b\), so

\[
r(x)=\sqrt{x^2+b^2},
\qquad
A_s(x)=\frac{r_s}{\sqrt{x^2+b^2}}.
\]

Then

\[
T_A^\gamma
=\frac{r_s}{c}\int_{x_1}^{x_2}
  \frac{dx}{\sqrt{x^2+b^2}}.
\]

To integrate, set \(x=b\sinh u\). Then

\[
dx=b\cosh u\,du,
\qquad
\sqrt{x^2+b^2}=b\sqrt{\sinh^2u+1}=b\cosh u.
\]

The factors cancel:

\[
\int\frac{dx}{\sqrt{x^2+b^2}}
=\int du
=u+C
=\operatorname{asinh}(x/b)+C.
\]

Therefore

\[
T_A^\gamma
=\frac{r_s}{c}
 \left[\operatorname{asinh}(x/b)\right]_{x_1}^{x_2}.
\]

Using

\[
\operatorname{asinh}y=\ln\left(y+\sqrt{1+y^2}\right),
\]

the same result becomes a difference of logarithms. After endpoint geometry
is substituted, this is the first-order logarithmic Shapiro form. The
logarithm is not inserted by analogy; it is the antiderivative of the declared
spherical source profile on the declared route.

### 3.4 Executed evidence and deviations

CR006@04 evaluates the fixed Earth-to-Cassini-style geometry with impact
parameter \(1.6R_\odot\). It records
\(131.215549519679\ \mu\mathrm{s}\), relative analytic/numerical difference
\(1.79\times10^{-13}\), and \(\gamma_{\rm eff}=1\).

The endpoint-only control cannot reproduce impact-parameter dependence. The
uniform-floor road produces a spurious contribution proportional to the path
scale because it treats a background account as a local source profile.

The independent binary-pulsar holdout CR148@04 uses the convention map

\[
r_{\rm timing}=\frac{GM_B}{c^3},
\qquad
\Delta_S(E)=-2r_{\rm timing}\ln q(E).
\]

The source-road coefficient \(2GM_B/c^3\) is thus \(2r_{\rm timing}\); the
factor two is a notation map, not a fitted amplitude. The holdout records
\(r_{\rm timing}=6.1514456437083\ \mu\mathrm{s}\),
\(s=\sin i=0.999906773574375\), \(|z|=0.26\), and analytic/numerical
agreement better than \(4\times10^{-9}\). **The test result suggests strong
contact with the concept.** Endpoint-only, wrong-power, missing-source-radius,
local-\(A_0\) and free-amplitude controls reject.

## 4. Invariant local c and coordinate traversal

### 4.1 Question

How can an accumulation-conditioned road be expressed as an effective speed
without claiming that a local light-speed experiment measures a new constant?

### 4.2 Type-preserving identity

Begin with the declared native/readout distance ratio

\[
\frac{D_{\rm native}}{D_{\rm readout}}=1-A.
\]

Multiplying both sides by the invariant speed (c) defines the speed-valued
coordinate shorthand

\[
c_{\rm eff}=c(1-A),
\qquad
\frac{c_{\rm eff}}c=1-A.
\]

Nothing in this algebra changes

\[
c_{\rm local}=c.
\]

The new symbol records how a native road is represented in a chosen
coordinate readout. Substituting (c_{\rm eff}(r)) for (c) in local
relativistic laws would reverse the definition and commit a type error.

### 4.3 Source release and common propagation

CR147@04 separates a dynamic source-release differential from the later
road. Once released, electromagnetic and gravitational channels share the
same accumulation road. The different-post-release-speed control rejects.
The result therefore supports the invariant-propagation boundary without
claiming that the packet uniquely identifies every source-engine detail.

## 5. Local and cosmological roads

### 5.1 Why the global operator is separate

A local road starts with a spatial source profile \(A_s(\mathbf x)\) and a
path \(\Gamma\). The settled cosmological road starts with redshift \(z\) and
the declared line-of-sight account

\[
A_{\rm los}(z)
=A_0R\left[1-(1+z)^{-D}\right].
\]

Using \(A_0=1/(\pi R)\) and \(D=3\), perform the substitutions explicitly:

\[
A_0R=\frac{1}{\pi R}R=\frac1\pi,
\]

so

\[
A_{\rm los}(z)
=\frac1\pi\left[1-(1+z)^{-3}\right].
\]

This is neither a host-mass correction nor the Euclidean integral of a
uniform \(A_0\) along a local path.

### 5.2 Boundary checks

At \(z=0\),

\[
A_{\rm los}(0)=\frac1\pi(1-1)=0.
\]

Differentiate:

\[
\frac{d}{dz}(1+z)^{-3}=-3(1+z)^{-4},
\]

hence

\[
\frac{dA_{\rm los}}{dz}
=\frac{3}{\pi}(1+z)^{-4},
\qquad
\left.\frac{dA_{\rm los}}{dz}\right|_{z=0}=\frac3\pi.
\]

As \(z\to\infty\), \((1+z)^{-3}\to0\), so

\[
A_{\rm los}(z)\to\frac1\pi.
\]

The zero prevents a fixed local-redshift anomaly; the ceiling prevents an
unbounded distance conversion.

### 5.3 Distance and modulus

Apply the coordinate identity with the cosmological input:

\[
D_{\rm native}(z)
=D_{\rm readout}(z)[1-A_{\rm los}(z)].
\]

For distance modulus, use

\[
\mu=5\log_{10}(D/10\ \mathrm{pc}).
\]

Then

\[
\begin{aligned}
\mu_{\rm native}-\mu_{\rm obs}
&=5\log_{10}\left(\frac{D_{\rm native}}{D_{\rm readout}}\right)\\
&=5\log_{10}[1-A_{\rm los}(z)],
\end{aligned}
\]

and therefore

\[
\mu_{\rm native}
=\mu_{\rm obs}+5\log_{10}[1-A_{\rm los}(z)].
\]

The derivation shows exactly why no host stellar-mass term appears in this
operator.

### 5.4 Evidence boundary

The focused child documents carry the full SN/BAO sequence. At this parent
level, the important distinction is that a common distance factor does not
replace every later observable operator. In particular, an anisotropic radial
BAO lane can require a derivative projection after the distance conversion.
The speed-only diagnostic control is therefore informative precisely because
it fails to reproduce that typed projection.

## 6. Exterior strong-field traversal

### 6.1 Exact coordinate

Set

\[
x=\frac r{r_s},
\qquad
A=\frac1x.
\]

The same dimensionless profile marks the horizon, photon sphere and ISCO at

\[
(A_H,A_{\rm ph},A_{\rm ISCO})
=\left(1,\frac23,\frac13\right),
\]

corresponding to \(x=(1,3/2,3)\). Because every radius is a fixed multiple of
\(r_s\), the normalized tuple is mass invariant. This coordinate continuity
does not extend weak-field series outside their domain.

### 6.2 Exact lapse and redshift

Use

\[
\ell(A)=\sqrt{1-A},
\qquad
z(A)=\frac1{\sqrt{1-A}}-1.
\]

As \(A\to1^-\), \(\ell\to0\) and \(z\to\infty\). The weak expansion beginning
at \(A/2\) cannot be used to evaluate this limit.

### 6.3 Radial road derivation

For the declared outward exterior road,

\[
dt=\frac{dr}{c[1-A(r)]}
=\frac{dr}{c(1-r_s/r)}.
\]

Substitute \(r=r_sx\), so \(dr=r_s\,dx\):

\[
\frac{c\,dt}{r_s}=\frac{dx}{1-1/x}.
\]

Simplify without skipping the singular structure:

\[
\frac1{1-1/x}=\frac{x}{x-1}=1+\frac1{x-1}.
\]

Integrate:

\[
\frac{ct}{r_s}
=\int\left(1+\frac1{x-1}\right)dx
=x+\ln|x-1|+C.
\]

Between two exterior radii \(1<x_1<x_2\),

\[
\frac{c\Delta t}{r_s}
=(x_2-x_1)+\ln\left(\frac{x_2-1}{x_1-1}\right).
\]

As \(x_1\to1^+\), the logarithm diverges. CR008@05 executes this sequence:
for \(A=1-10^{-3}\) through \(1-10^{-12}\), the normalized road to \(x=3\)
grows from about \(9.60\) to \(30.32\), while lapse tends to zero and redshift
diverges.

### 6.4 Closure interpretation

At exact \(A=1\), the ordinary coordinate shorthand gives \(c_{\rm eff}=0\),
the static lapse is zero and the exterior radial road diverges. The consistent
endpoint is a no-ordinary-escape closure boundary. It is not a local
\(c\mapsto0\) law and not an ordinary launch point for subsequent \(A>1\)
bookkeeping. A dynamic source-release surface in the multimessenger branch is
a separately typed object.

## 7. Integrated deviation chain

| Selected route | Diagnostic deviation | What the deviation reveals |
|---|---|---|
| endpoint lapse ratio | route integral substituted for two endpoints | path dependence was introduced into an endpoint question |
| weak coefficient \(1/2\) | doubled coefficient | the square-root origin was removed |
| background-differenced clock | uncancelled universal floor | a common background was turned into a local difference |
| photon source-road integral | endpoint-only value | impact-parameter and path shape disappear |
| source lift on a local road | uniform \(A_0\) integrated locally | a spurious path-scale delay appears |
| fixed pulsar road amplitude | free-amplitude rescue | the holdout ceases to test transfer |
| shared post-release road | different EM/GW propagation speeds | source release and propagation were conflated |
| coordinate \(c_{\rm eff}\) | local variable-\(c\) substitution | an inferred-distance readout was treated as a fundamental constant |
| cosmological \(A_{\rm los}(z)\) | host-mass or Euclidean-floor road | the global construction was replaced by a local one |
| derivative-projected BAO lane | speed-only factor | a common distance conversion was asked to replace an anisotropic operator |
| exact strong-field lapse | weak series at closure | an asymptotic expansion was used outside its domain |
| exterior road from \(x>1\) | launch from exact \(A=1\) | a closure boundary was treated as an ordinary initial point |

These are not decorative alternatives. Each failed or rejecting route locates
the dependency that makes the retained construction typed and executable.

## 8. What is established and what connects forward

The parent establishes the following integrated structure:

1. Endpoint clocks read a square-root lapse ratio; the weak coefficient is
   one-half because of that operator.
2. Photon roads read a path integral whose spherical-source evaluation gives
   the asinh/logarithmic Shapiro form.
3. The coordinate shorthand \(c_{\rm eff}=c(1-A)\) preserves local invariant
   \(c\) and is equivalently a native/readout distance conversion.
4. Local source roads and the cosmological line-of-sight road are different
   constructions even though both are accumulation-conditioned.
5. Exact lapse and exterior radial traversal provide the strong-field
   continuation to the \(A=1\) closure boundary.

Volume I's supernova, BAO, horizon-thermodynamic and cosmological chapters use
these operators next. Volume II may provide the material source through its
typed return, but particle grammar is not developed here. Volume III may
execute these routes, but its computational internals are not imported into
the physical definition.

## 9. Exact open boundaries

- The clock and road packets do not by themselves close recombination,
  perturbation, polarization or lensing-time-delay programs.
- A successful distance-road conversion does not make one operator sufficient
  for every SN, BAO or CMB observable.
- The shared post-release road does not uniquely solve the source engine.
- Strong-field coordinate continuity does not validate weak expressions at
  the photon sphere, ISCO or horizon.
- Exact \(A=1\) remains a boundary; no ordinary interior launch rule is
  installed by this parent.

## Child-document map

| Child | Technical ownership |
|---|---|
| `SAMA-D000005` | Exact and weak endpoint clocks, GPS composition and clock evidence |
| `SAMA-D000007` | Photon-road functional, asinh/log derivation and Shapiro evidence |
| `SAMA-D000009` | Invariant local `c`, effective traversal and engine/road separation |
| `SAMA-D000010` | Local/global road distinction and cosmological road boundary checks |
| `SAMA-D000014` | Exact lapse, exterior radial primitive and closure interpretation |

## Test and result-reference index

The focused test routes for this synthesis reside on its child documents.
Their complete concept, operator, input, control, outcome, classification,
relationship, atomic-record and source-custody fields are generated in
[`VOLUME_I_TEST_REFERENCE_INDEX.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/generated/VOLUME_I_TEST_REFERENCE_INDEX.md).
The formal and deviation order is generated in
[`VOLUME_I_DERIVATION_DEVIATION_CHAIN_INDEX.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/reports/VOLUME_I_DERIVATION_DEVIATION_CHAIN_INDEX.md).

## Atomic source records

| Record | Role in the synthesis |
|---|---|
| `SAMA-C000002-R001` | Spherical source lift. |
| `SAMA-C000003-R001` | Clock/road type distinction. |
| `SAMA-C000004-R001` | Coordinate-readout meaning of `c_eff`. |
| `SAMA-C000046-R001` | Exact endpoint lapse ratio. |
| `SAMA-C000053-R001` | Local photon-road functional. |
| `SAMA-C000060-R001` | Effective traversal distance identity. |
| `SAMA-C000061-R001` | Source-engine/shared-road distinction. |
| `SAMA-C000062-R001` | Cosmological line-of-sight road. |
| `SAMA-C000064-R001` | Local/cosmological road type boundary. |
| `SAMA-C000078-R001` | Exterior radial-traversal primitive. |
| `SAMA-C000080-R001` | Exact-unit closure boundary. |
| `SAMA-C000122-R001` | Volume I subject boundary. |
| `SAMA-C000123-R001` | Parent reading route. |
| `SAMA-C000124-R001` | Current versus historical authority. |
| `SAMA-C000125-R001` | Classification and approval boundary. |

## Revision and approval

This parent integrates existing source-bound children and atomic records. It
introduces no new result classification and performs no owner approval, live
promotion or public release.

`reviewed_and_approved: false`

`approval: null`

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-P000005`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/parents/TIME_DILATION_AND_TRAVERSAL_ACCUMULATION.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Parent field | Value |
|---|---|
| Document | `SAMA-P000005` |
| Volume | I |
| Purpose | Integrate endpoint clocks, local photon roads, invariant-`c` coordinate traversal, local/cosmological road separation and exterior horizon traversal in dependency order. |
| Prerequisites | `SAMA-D000003`, `SAMA-D000004` |
| Focused children | `SAMA-D000005`, `SAMA-D000007`, `SAMA-D000009`, `SAMA-D000010`, `SAMA-D000014` |
| Review state | `reviewed_and_approved: false` |

</details>
