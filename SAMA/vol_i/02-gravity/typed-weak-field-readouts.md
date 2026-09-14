[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Typed Weak-Field Readouts

## Current research connections — 14 September 2026

The global execution authority is SLC-GEN3-R3 / SLC-GEN3-CEV1-R3. The September 2026 research includes exact retained-history computation, RH arithmetic compensation, native Mersenne work, Starbreaker signed reception and ATOM3D contact/grammar. The research index connects the retained derivations to the latest code, results and current domain assignments.

[Current derivations, code and results](../../../docs/RESEARCH.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

The spherical source coordinate

\[
A_s(r)=\frac{2GM_s}{c^2r}
\]

is a dimensionless field lift. It is not yet potential, acceleration, clock
rate, escape speed, photon delay or distance. Each observable begins only when
a map with a declared input, output and domain acts on that field.

For the local weak-field lanes developed here,

\[
\Phi[A_s]=-\frac{c^2}{2}A_s,
\qquad
\mathbf g[A_s]=\frac{c^2}{2}\nabla A_s,
\qquad
v_{\rm esc}[A_s]=c\sqrt{A_s}.
\]

Substitution recovers \(-GM_s/r\),
\(-GM_s\hat{\mathbf r}/r^2\), and \(\sqrt{2GM_s/r}\) in full
intermediate steps. The universal floor remains part of the total substrate
account but vanishes from the local gradient and from shared potential
differences. At \(A_s=1\), the escape expression reaches \(c\); that is the
edge of the weak lane and the start of a separate strong-field closure chain.

The Earth, Moon and Sun packet applies these operators with zero fitted
parameters. Its scope is local weak-field acceleration and escape speed; it
does not absorb clock, photon-road, GPS or strong-field claims.

## 1. Opening question and conceptual picture

One field can feed many instruments. That reuse is economical only if the
operators remain distinct.

| Measurement question | Field input | Operator geometry | Output |
|---|---|---|---|
| What is the weak potential per unit test mass? | local source lift | value scaling | \(\Phi\), m\(^2\) s\(^{-2}\) |
| What acceleration does the source produce? | spatially varying lift | gradient | \(\mathbf g\), m s\(^{-2}\) |
| What speed reaches zero kinetic energy at infinity? | local lift/potential | energy balance | \(v_{\rm esc}\), m s\(^{-1}\) |
| How do two clocks compare? | two endpoint values | lapse ratio | dimensionless rate ratio; owned by `SAMA-D000005` |
| What delay does a photon accumulate? | source lift along a route | path integral | time; owned by `SAMA-D000007` |

The chapter's central question is: **given a common dimensionless source
field, what exact operator produces each weak observable, and what errors
appear when a coefficient, radial power, sign, floor treatment or domain is
moved from one lane to another?**

## 2. Definitions, domains and units

### 2.1 Field inputs

For one spherical source,

\[
r_s=\frac{2GM_s}{c^2},
\qquad
A_s(r)=\frac{r_s}{r}=\frac{2GM_s}{c^2r}.
\]

For several weak sources,

\[
A_{\rm lift}(\mathbf x)
=\sum_i\frac{2GM_i}{c^2|\mathbf x-\mathbf x_i|},
\qquad
A_{\rm total}=A_0+A_{\rm lift}.
\]

The weak-field domain is \(A_s\ll1\), with the exterior source profile
approaching but not ordinarily crossing the closure marker \(A_s=1\).

### 2.2 Operator signatures

| Operator | Signature | Definition | Output units |
|---|---|---|---|
| Potential | dimensionless scalar \(\to\) scalar | \(\Phi[A]=-(c^2/2)A\) | m\(^2\) s\(^{-2}\) |
| Acceleration | dimensionless scalar field \(\to\) vector | \(\mathbf g[A]=(c^2/2)\nabla A\) | m s\(^{-2}\) |
| Escape speed | nonnegative local lift \(\to\) scalar | \(v_{\rm esc}[A]=c\sqrt A\) | m s\(^{-1}\) |
| Endpoint lapse | \(0\le A<1\) \(\to\) dimensionless | \(\ell[A]=\sqrt{1-A}\) | dimensionless |
| Photon road | field on path \(\Gamma\) \(\to\) time | \(T_A^\gamma=c^{-1}\int_\Gamma A_sds\) | s |

The last two appear here only to mark the boundary. Clocks read endpoints and
photon signals read a route. The weak clock expansion begins with \(A/2\);
the first-order photon road integrates the full \(A\). Moving either
coefficient into the other lane is a type error.

### 2.3 Dimensional closure

Because \(A\) is dimensionless,

\[
[\Phi]=[c^2]=\mathrm{m^2,s^{-2}}.
\]

Because \([\nabla A]=\mathrm{m^{-1}}\),

\[
[\mathbf g]=[c^2][\nabla A]
=\mathrm{m^2,s^{-2}}\mathrm{m^{-1}}
=\mathrm{m,s^{-2}}.
\]

Finally,

\[
[c\sqrt A]=\mathrm{m,s^{-1}}.
\]

Units distinguish the field from its outputs before any numerical comparison
is made.

## 3. Potential derivation from start to finish

### 3.1 Declare the operator

The weak potential operator is

\[
\Phi[A]=-\frac{c^2}{2}A.
\]

The minus sign assigns an attractive bound-source potential relative to the
zero-at-infinity convention. The coefficient \(c^2/2\) converts the
dimensionless accumulation coordinate into potential per unit test mass.

### 3.2 Insert the spherical lift

\[
\Phi_s(r)
=-\frac{c^2}{2}\left(\frac{2GM_s}{c^2r}\right).
\]

### 3.3 Cancel the paired factors explicitly

The numerator and denominator contain the same \(c^2\), and the operator's
\(1/2\) cancels the source lift's \(2\):

\[
\Phi_s(r)
=-\left(\frac{c^2}{2}\right)
  \left(\frac{2GM_s}{c^2r}\right)
=-\frac{GM_s}{r}.
\]

Thus

\[
\boxed{\Phi_s(r)=-\frac{GM_s}{r}}.
\]

The exact coefficient is load-bearing. Using \(-c^2A\) doubles the
potential; using \(-c^2A/4\) halves it.

### 3.4 The uniform floor under potential comparisons

If the operator is formally applied to the pointwise total,

\[
\Phi[A_{\rm total}]
=-\frac{c^2}{2}A_0
 -\frac{c^2}{2}A_{\rm lift}.
\]

The first term is spatially constant. For a shared-background potential
difference,

\[
\Delta\Phi
=-\frac{c^2}{2}\Delta A_{\rm total}
=-\frac{c^2}{2}\Delta A_{\rm lift},
\]

because \(\Delta A_0=0\). The floor remains in the pointwise substrate
account; the comparison removes the common offset.

## 4. Acceleration derivation from start to finish

### 4.1 Differentiate the spherical scalar

Write

\[
A_s(r)=\frac{r_s}{r}=r_sr^{-1}.
\]

Because \(r_s\) is constant for the selected source,

\[
\frac{dA_s}{dr}
=r_s\frac d{dr}r^{-1}
=-r_sr^{-2}
=-\frac{r_s}{r^2}.
\]

For a spherically symmetric scalar field,

\[
\nabla A_s
=\frac{dA_s}{dr}\hat{\mathbf r}
=-\frac{r_s}{r^2}\hat{\mathbf r}.
\]

Insert \(r_s=2GM_s/c^2\):

\[
\nabla A_s
=-\frac{2GM_s}{c^2r^2}\hat{\mathbf r}.
\]

### 4.2 Apply the acceleration operator

\[
\mathbf g[A_s]
=\frac{c^2}{2}\nabla A_s
=\frac{c^2}{2}
  \left(-\frac{2GM_s}{c^2r^2}\hat{\mathbf r}\right).
\]

Cancel the same coefficient pair:

\[
\boxed{
\mathbf g(r)=-\frac{GM_s}{r^2}\hat{\mathbf r}
}.
\]

The negative sign is not cosmetic. With \(\hat{\mathbf r}\) oriented
outward, it makes the acceleration point toward the source.

### 4.3 Show why the floor produces no local acceleration

\[
\begin{aligned}
\mathbf g[A_{\rm total}]
&=\frac{c^2}{2}\nabla(A_0+A_{\rm lift})\\
&=\frac{c^2}{2}\nabla A_0
 +\frac{c^2}{2}\nabla A_{\rm lift}\\
&=\mathbf0+\frac{c^2}{2}\nabla A_{\rm lift}.
\end{aligned}
\]

This is cancellation by differentiation, not deletion of \(A_0\) from
\(A_{\rm total}\).

### 4.4 Many-source acceleration follows after summation

Because the gradient is linear,

\[
\begin{aligned}
\mathbf g(\mathbf x)
&=\frac{c^2}{2}\nabla
  \sum_i\frac{2GM_i}{c^2|\mathbf x-\mathbf x_i|}\\
&=-\sum_i
  \frac{GM_i(\mathbf x-\mathbf x_i)}
       {|\mathbf x-\mathbf x_i|^3}.
\end{aligned}
\]

This is the weak many-source vector readout. The source lifts were formed
first; the gradient was then applied to their sum.

## 5. Escape-speed derivation from energy balance

### 5.1 Write the conserved weak energy

For a test mass \(m\), the specific energy balance from radius \(r\) to
rest at infinity is

\[
\frac12mv_{\rm esc}^2+m\Phi_s(r)=0,
\]

using \(\Phi(\infty)=0\).

### 5.2 Cancel the test mass

Divide by \(m>0\):

\[
\frac12v_{\rm esc}^2+\Phi_s(r)=0.
\]

The escape speed therefore cannot depend on the test mass in this lane.

### 5.3 Insert the potential operator

\[
\frac12v_{\rm esc}^2-\frac{c^2}{2}A_s(r)=0.
\]

Multiply by two:

\[
v_{\rm esc}^2-c^2A_s(r)=0.
\]

For the nonnegative speed,

\[
v_{\rm esc}=c\sqrt{A_s(r)}.
\]

Insert the spherical source lift:

\[
\boxed{
v_{\rm esc}(r)
=c\sqrt{\frac{2GM_s}{c^2r}}
=\sqrt{\frac{2GM_s}{r}}
}.
\]

### 5.4 Reach the boundary without crossing it

At \(r=r_s\), \(A_s=1\), so

\[
v_{\rm esc}(r_s)=c.
\]

This exact equality is the weak expression reaching the source-scale closure
marker. It does not establish that the same energy formula is an ordinary interior
law for \(A>1\). Exact lapse, exterior radial-road and strong-field landmark
operators are developed in their own later documents.

## 6. Circular-orbit corollary

The potential and acceleration operators also supply a focused circular-orbit
check. For a test mass \(m\), set centripetal force equal to the magnitude of
the weak source force:

\[
\frac{mv_{\rm circ}^2}{r}
=m\frac{GM_s}{r^2}.
\]

Cancel \(m\) and multiply by \(r\):

\[
v_{\rm circ}^2=\frac{GM_s}{r}.
\]

In accumulation form,

\[
\frac{GM_s}{r}=\frac{c^2A_s}{2},
\]

so

\[
\boxed{v_{\rm circ}=c\sqrt{\frac{A_s}{2}}}.
\]

The orbital period is then

\[
T=\frac{2\pi r}{v_{\rm circ}}
=2\pi\sqrt{\frac{r^3}{GM_s}}.
\]

This is a corollary of the typed potential/gradient packet. It does not claim
\(N\)-body dynamics, perturbation theory or full strong-field orbital
dynamics.

## 7. Source-bound worked examples

### 7.1 Early Newtonian scaling anchor

The Newtonian sub-claim in `G:G284c@SAM-ARCHIVE` records, for its declared
Earth input,

\[
g_A=-9.798009038051548\ \mathrm{m,s^{-2}}
=g_N
\]

with zero recorded relative difference. Its radius scan gives log-log slope
\(-1.9999999999999996\), and its source-mass scan gives slope \(1\), as
the derivation predicts:

\[
|\mathbf g|\propto M_sr^{-2}.
\]

The source file also contains redshift and GPS sub-claims. They are not
promoted here: this document registers G284c only as the early weak-field
source anchor; endpoint-clock/GPS interpretation belongs to the clock chapter.

### 7.2 Circular-orbit replay

`G:G410@SAM-ARCHIVE` evaluates a declared orbit radius
\(6,778,137\ \mathrm m\) and test mass \(1000\ \mathrm{kg}\). It records

\[
F_A=F_N=8675.706224460017\ \mathrm N,
\]

\[
v_A=v_{\rm standard}=7668.449997303415\ \mathrm{m,s^{-1}},
\]

and

\[
T_A=5553.702615708044\ \mathrm s,
\qquad
T_{\rm standard}=5553.7026157080445\ \mathrm s.
\]

Doubling the test mass leaves the speed unchanged; doubling the source mass
multiplies speed by \(\sqrt2\); doubling radius multiplies it by
\(1/\sqrt2\). Those are direct checks of the cancellation and scalings
derived in Section 6.

### 7.3 Escape-boundary replay

`G:G411@SAM-ARCHIVE` records for its declared surface input

\[
A_{\rm surface}=1.3906577775666053\times10^{-9},
\]

\[
c\sqrt{A_{\rm surface}}
=11179.71770412214\ \mathrm{m,s^{-1}},
\]

against its standard calculation
\(11179.717704122138\ \mathrm{m,s^{-1}}\). It separately sets
\(A=1\) and obtains exactly \(299792458\ \mathrm{m,s^{-1}}=c\). The
test's scope fields remain false for full horizon dynamics, black-hole
interior, full GR and full quantum gravity.

### 7.4 Earth, Moon and Sun external-contact packet

[`CR:CR004@02`](../../tests/courtroom/02-a-kernel-weak-field-cr004-weak-field-a-kernel-external-contact/README.md) applies the selected \(A\)-kernel with zero fitted parameters
to three external weak-field anchors:

| Body | \(|\mathbf g|\) m s\(^{-2}\) | \(v_{\rm esc}\) m s\(^{-1}\) |
|---|---:|---:|
| Earth | 9.82025048706 | 11186.1356914 |
| Moon | 1.62490442956 | 2376.17716339 |
| Sun | 274.200111695 | 617674.700317 |

The G411 Earth-like value and CR004 Earth value use their own declared source
inputs; their numerical difference is not treated as an extra fit or averaged
into a new datum. The load-bearing CR004 statement is that the same typed
packet passes all three of its pinned body rows and that no wrong-control
candidate matches the full packet.

For this scoped established-reference lane, **The test result suggests strong
contact with the concept.**

## 8. Typed weak-field operator chain

### 8.1 Construction and focused corollaries

`G:G284c@SAM-ARCHIVE` supplies an early combined gate whose Newtonian lane
checks the exact \(Mr^{-2}\) dependence. `G:G410@SAM-ARCHIVE` isolates the
circular-orbit corollary. `G:G411@SAM-ARCHIVE` isolates the escape-energy and
\(A=1\) boundary. Together they expose coefficient, sign, power, test-mass
and scope controls before the later Courtroom recertification.

### 8.2 Native-kernel boundary retest

[`CR:CR003@02`](../../tests/courtroom/02-a-kernel-weak-field-cr003-a-kernel-typed-readout-recertification/README.md) uses no older test outputs as inputs. It compares six candidates
and selects the correct \(A_s=r_s/r\) packet uniquely. It records exact
potential closure, horizon closure and many-source closure while retaining the
scientific verdict `BOUNDARY` until external data attach.

### 8.3 External contact

[`CR:CR004@02`](../../tests/courtroom/02-a-kernel-weak-field-cr004-weak-field-a-kernel-external-contact/README.md) attaches the Earth, Moon and Sun rows. Its six pass conditions
include external-data use, zero introduced free parameters, all-body success
and rejection of the wrong controls. The source result is `CLEAN` / `PASS` in
the scoped local weak-field lane.

### 8.4 Mechanism replay after contact

[`LC:LC03`](../../tests/courtroom/16-the-last-campaign/README.md) then replays the upstream source mechanism from the locked primitive
stack through \(q_A\), one-eighth carrier and ledger compression into the
same field/readout packet. It prevents successful external contact from being
used to justify an incorrect mechanism such as direct \(q_A\)-as-mass or
carrier-to-matter promotion.

The causal order is therefore

\[
\text{construction}
\to\text{focused corollaries}
\to\text{typed boundary recertification}
\to\text{external contact}
\to\text{locked mechanism replay}.
\]

## 9. Wrong controls and their quantitative signatures

### 9.1 Coefficient and field-profile controls

| Wrong control | Predicted signature in the registered tests | Why it fails |
|---|---|---|
| Omit the operator's \(1/\alpha_H=1/2\) bookkeeping | G410 force is \(2\) times standard and speed is \(\sqrt2\) times standard. | Double-counts the source-profile factor two. |
| Omit \(\alpha_H=2\) from \(A_s\) | G410 force is \(1/2\) and speed \(1/\sqrt2\) of standard. | Produces a half-strength source field. |
| Use \(A\propto r^{-2}\) | CR003 inverse-square candidate misses the complete packet. | The gradient would then yield the wrong \(r^{-3}\) acceleration. |
| Double the potential | CR003 candidate preserves some relations and fails full selection. | Breaks \(\Phi=-GM/r\) and energy balance. |
| Shift the \(A=1\) boundary | G411's separate-boundary control gives speed ratio \(1.0488088481701516\). | Creates a second field scale not in the source kernel. |

### 9.2 Sign, test-mass and radial-power controls

- Reversing the sign makes the force outward and makes the registered wrong
  escape energy negative.
- Keeping test mass inside the final speed makes the G410/G411 wrong speed
  larger than standard by \(31.622776601683793\) for the declared test.
- A wrong potential power changes the doubled-radius speed ratio from
  \(1/\sqrt2\) to \(1/2\).
- Setting the gradient to zero discards the source variation entirely; keeping
  \(A_0\) as a nonzero gradient manufactures a uniform local acceleration.

### 9.3 Cross-lane controls

- Applying the endpoint-clock \(A/2\) coefficient to a photon route halves
  the wrong observable.
- Applying a path integral to an endpoint clock replaces local comparison with
  route exposure.
- Using the weak clock's linear form as the exact lapse is one of CR003's
  incomplete candidates.
- Reporting the weak packet as GPS, Shapiro, strong-field or full-GR closure
  crosses the explicit CR004 scope boundary.
- Continuing \(v_{\rm esc}=c\sqrt A\) as an ordinary interior rule for
  \(A>1\) crosses the G411 and Volume I closure boundary.

## 10. Established result and forward handoff

The compression-safe weak-field packet is

\[
\boxed{
A_{\rm total}=A_0+\sum_i\frac{2GM_i}{c^2r_i},\qquad
\Phi=-\frac{c^2A}{2},\qquad
\mathbf g=\frac{c^2}{2}\nabla A,\qquad
v_{\rm esc}=c\sqrt A
}.
\]

For a spherical source, it yields

\[
\Phi=-\frac{GM_s}{r},\qquad
\mathbf g=-\frac{GM_s}{r^2}\hat{\mathbf r},\qquad
v_{\rm esc}=\sqrt{\frac{2GM_s}{r}}.
\]

The floor is retained in the total substrate state and cancels under the
declared local derivative or shared difference. It must not be removed or
reinserted silently.

`SAMA-D000005` receives the field but changes operator geometry to endpoint
lapse. `SAMA-D000007` receives it for route integration. The strong-field
documents receive \(A=1\) as a closure marker, not as permission to continue
the weak approximation. The scoped Earth/Moon/Sun result does not merge those
lanes.

Exact evidence is the complete six-key sequence in Section 11. The
specifically open boundary is endpoint-clock, photon-road and exact
strong-field construction under their own operators; the weak packet does not
close those later lanes.

## 11. Focused test and result index

| Exact qualified key | Evidence role | Preserved outcome | Direct result | Result folder |
|---|---|---|---|---|
| `G:G284c@SAM-ARCHIVE` | Historical weak-field source anchor | Registry exposes no structured status/verdict; source records exact Newtonian scaling and its wrong controls inside a broader gate. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G284c_gate3_remaining/G284c_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G284c_gate3_remaining) |
| `G:G410@SAM-ARCHIVE` | Circular-orbit result | `G410_KEPLER_CIRCULAR_ORBIT_FROM_A_POTENTIAL_PASS` | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G410_KEPLER_CIRCULAR_ORBIT_FROM_A_POTENTIAL/G410_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G410_KEPLER_CIRCULAR_ORBIT_FROM_A_POTENTIAL) |
| `G:G411@SAM-ARCHIVE` | Escape boundary | `G411_ESCAPE_VELOCITY_A_BOUNDARY_PASS` | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G411_ESCAPE_VELOCITY_A_BOUNDARY/G411_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G411_ESCAPE_VELOCITY_A_BOUNDARY) |
| [`CR:CR003@02`](../../tests/courtroom/02-a-kernel-weak-field-cr003-a-kernel-typed-readout-recertification/README.md) | Native typed-kernel boundary | Source execution `CLEAN`, scientific verdict `BOUNDARY`; correct \(A\) uniquely matches the full packet. | [result](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION/CR003_result.md) | [folder](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION) |
| [`CR:CR004@02`](../../tests/courtroom/02-a-kernel-weak-field-cr004-weak-field-a-kernel-external-contact/README.md) | Established-reference result | Source execution `CLEAN`, scientific verdict `PASS`; zero-parameter Earth/Moon/Sun packet. **The test result suggests strong contact with the concept.** | [result](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT/CR004_result.md) | [folder](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT) |
| [`LC:LC03`](../../tests/courtroom/16-the-last-campaign/README.md) | Locked mechanism replay | `LC03_PASS_QA_LEDGER_COMPRESSION_GRAVITY_AS_A_REPLAY`; 15/15 wrong controls rejected. | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN) |

## 12. Atomic record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000003-R001` | Separates endpoint-clock and photon-road operator types. |
| `SAMA-C000036-R001` | Routes the universal floor under local and global operators. |
| `SAMA-C000039-R001` | Separates total accumulation from source lift. |
| `SAMA-C000041-R001` | Requires a typed operator before \(A\) becomes an observable. |
| `SAMA-C000042-R001` | Defines and closes the weak potential operator. |
| `SAMA-C000043-R001` | Defines and closes the weak acceleration operator. |
| `SAMA-C000044-R001` | Derives escape speed and marks \(A=1\) as its boundary. |
| `SAMA-C000045-R001` | Records the Earth/Moon/Sun external-contact packet and authorized classification. |
| `SAMA-C000122-R001` | Enforces the Volume I/II/III subject boundary. |
| `SAMA-C000124-R001` | Separates source-era chronology from current live authority. |
| `SAMA-C000125-R001` | Preserves source verdicts, authorized classifications and false approval state. |

## 13. Source, result-language and approval boundary

The direct evidence set is exactly the six qualified keys indexed above.
Courtroom links are pinned to commit
`b5e914f71377e86ef4c67e199973d9300795cda1`; G links resolve to the exact
local artifacts and hashes in the SAMA test registry. The sole SAMA result
classification in this document is the exact authorized CR004@02 sentence.
Source `PASS`/`BOUNDARY` tokens are otherwise kept as provenance.

Terms such as “latest” in the Volume I spine describe source-era chronology
unless current live authority installs them. `reviewed_and_approved` remains
`false`, and `approval` remains `null`; successful execution, classification
and document validation do not constitute owner approval.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`CR:CR003@02`](../../tests/courtroom/02-a-kernel-weak-field-cr003-a-kernel-typed-readout-recertification/README.md) | [CR003_PRECOMMIT.md](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION/CR003_PRECOMMIT.md)<br>[CR003_declared_premises.json](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION/CR003_declared_premises.json) | [CR003_A_kernel_typed_readout_recertification.py](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION/CR003_A_kernel_typed_readout_recertification.py) | [CR003_candidate_rows.csv](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION/CR003_candidate_rows.csv) | [CR003_result.md](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION/CR003_result.md)<br>[CR003_summary.json](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION/CR003_summary.json) | [All 8 files](../../tests/courtroom/02-a-kernel-weak-field-cr003-a-kernel-typed-readout-recertification/README.md) |
| [`CR:CR004@02`](../../tests/courtroom/02-a-kernel-weak-field-cr004-weak-field-a-kernel-external-contact/README.md) | [CR004_PRECOMMIT.md](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT/CR004_PRECOMMIT.md)<br>[CR004_declared_premises.json](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT/CR004_declared_premises.json) | [CR004_weak_field_external_contact.py](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT/CR004_weak_field_external_contact.py) | [CR004_candidate_rows.csv](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT/CR004_candidate_rows.csv) | [CR004_result.md](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT/CR004_result.md)<br>[CR004_summary.json](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT/CR004_summary.json) | [All 8 files](../../tests/courtroom/02-a-kernel-weak-field-cr004-weak-field-a-kernel-external-contact/README.md) |
| [`LC:LC03`](../../tests/courtroom/16-the-last-campaign/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign/README.md) | [LC03_qa_ledger_compression_gravity_a_replay_runner.py](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_qa_ledger_compression_gravity_a_replay_runner.py) | [LC03_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_wrong_controls.csv)<br>[LC03_wrong_controls.csv.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_wrong_controls.csv.sha256.txt) | [LC03_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_result.md)<br>[LC03_result.md.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_result.md.sha256.txt)<br>[LC03_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_summary.json)<br>[LC03_summary.json.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_summary.json.sha256.txt) | [All 164 files](../../tests/courtroom/16-the-last-campaign/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000004`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/TYPED_WEAK_FIELD_READOUTS.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000004 | Typed Weak-Field Readouts | Potential, Gradient, Escape-Speed and Weak-Field Contact Operators |

| Document field | Value |
|---|---|
| Purpose | Define each weak-field observable as a typed operator on \(A\), derive potential, acceleration, circular-orbit and escape-speed consequences, and route the Earth/Moon/Sun contact packet without field/readout conflation. |
| Prerequisite documents | `SAMA-D000003` |
| Used by | `SAMA-P000005`, `SAMA-D000005`, `SAMA-D000007`; assembled into `SAMA-P000002`. |
| Primary source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`, SHA-256 `2f22500f6583f567e350974610f00142e89b081a5b8c4c90c6dfe89bec43be0d`. |
| Revision state | Source-bound draft; mechanically registered proposal; not reviewed or approved. |

</details>
