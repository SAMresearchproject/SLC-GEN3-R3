[SAM](../../README.md) · [Volume II](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Binding and the Exact Asymmetry Bridge

## ATOM3D: contact, grammar and signed decoding — 14 September 2026

A3D41-T18-CONTACT-R2 uses SLC-GEN3-R3; A3D41-RXT-R3 supplies the joint native successor. Ordinary contact retains four minima and 113,664 agreeing readouts. Li-6 grammar retains both selected covers and every tie across six placements and 128 rho settings. Two Write responses and a signed N01 bit recover all 192 tested configurations. The test result suggests strong contact with the concept. The separate distinct-selector and physical-coefficient/MeV work remain owner-paused.

[Current derivations, code and results](../../../research/atom3d/README.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Opening question

> What exact nuclear-binding structure survives the failed direct
> source-to-rest-mass identity, how does the neutron-excess asymmetry term
> emerge one algebraic step at a time, and which additional geometric and
> readout operators are still required?

## Conceptual abstract

The binding route begins with a failure that reveals a difference of channels.
CR239 applies one conversion to the native coupling source and finds that the
result does not reproduce the rest-mass data. The residual aligns strongly
with neutron excess. CR240 therefore introduces two typed constructions:

\[
Q_{\rm mass}=4A\kappa,
\qquad
Q_{\rm sub}=8Z\kappa+\frac{N-Z}{8}.
\]

Their difference is not guessed from a binding curve. It follows exactly:

\[
\Delta Q
=Q_{\rm mass}-Q_{\rm sub}
=(N-Z)\frac{7093}{192}.
\]

Squaring that gap and normalizing by \(Q_{\rm mass}\) produces

\[
\frac{(\Delta Q)^2}{Q_{\rm mass}}
=
\frac{(N-Z)^2}{A}
\frac{50310649}{1366464}.
\]

The familiar neutron-asymmetry shape \((N-Z)^2/A\) is therefore the exact
normalized square of a typed rest-source/coupling-source mismatch. CR245
checks the identity under exact rational arithmetic across its 71-row roster.

That identity is one binding component, not the complete operator. A separate
linear connection-fee attempt misses the binding curvature by tens of MeV.
The registered CR249 A-kernel instead restores volume, surface, Coulomb,
asymmetry and pairing shapes. CR250 preserves a monotonic but nonseparating
intermediate route; CR251 removes coefficient degeneracy in its principal
lane and distinguishes the closed-ledger \(1/(S\mathcal L)\) asymmetry scale
from the bare-cycle \(1/(SR^2)\) alternative. CR274 is a later historical
fitted readout with family gates. Current binding authority has since moved
to B5T, so the Volume II records remain the exact source and derivation
history rather than an automatic statement of the present binding frontier.

## 1. Binding starts after source typing

The operation order is

\[
(Z,N)
\longrightarrow
Q_{\rm mass},Q_{\rm sub}
\longrightarrow
\Delta Q
\longrightarrow
\frac{(\Delta Q)^2}{Q_{\rm mass}}
\longrightarrow
\mathcal G_{\rm bind}
\longrightarrow
\mathcal R_{\rm nuclear}.
\]

Here:

- \(Q_{\rm mass}\) is a rest-source channel;
- \(Q_{\rm sub}\) is a substrate-coupling source;
- \(\Delta Q\) is their signed mismatch;
- the normalized square is the asymmetry-shape input;
- \(\mathcal G_{\rm bind}\) contains the nonlinear nuclear geometry; and
- \(\mathcal R_{\rm nuclear}\) is the downstream comparison or fitted
  readout.

The forbidden shortcut is

\[
Q_{\rm sub}
\longrightarrow
m_{\rm measured}
\longrightarrow
B_{\rm nucleus}
\]

with no type correction or nonlinear geometry. CR239 and the connection-fee
failure each reject one part of that shortcut.

## 2. Definitions, domains and units

| Symbol or object | Definition | Domain or unit | Boundary |
|---|---|---|---|
| \(Z\) | proton number | nonnegative integer | Element-family index, not a unique isotope. |
| \(N\) | neutron number | nonnegative integer | This derivation uses the declared nuclear row. |
| \(A\) | \(Z+N\) | nucleon count | Not the accumulation field \(A(r)\). |
| \(\kappa\) | \(7117/768\) | exact source coefficient | Fixed before binding comparison. |
| \(Q_{\rm mass}\) | \(4A\kappa\) | source units | Rest-source construction. |
| \(Q_{\rm sub}\) | \(8Z\kappa+(N-Z)/8\) | source units | Coupling-source construction. |
| \(\Delta Q\) | \(Q_{\rm mass}-Q_{\rm sub}\) | source units | Signed gap; zero for \(N=Z\). |
| \(X_A\) | \((\Delta Q)^2/Q_{\rm mass}\) | source units | Exact asymmetry-shape column, not complete binding energy. |
| \(\rho_A\) | \(A^{1/3}\) | dimensionless nuclear-size coordinate in the A-kernel | Geometric readout coordinate. |
| \(\delta_{\rm pair}\) | source-defined parity/pairing column | finite signed class | One model component. |
| \(B_u\) | source nuclear binding/mass-defect comparator | u or MeV after declared conversion | External/readout target, not a substrate primitive. |
| \(c_V,c_S,c_C,c_A,c_P\) | A-kernel coefficients | source-fit units | Fitted unless a separate source fixes a typed candidate. |
| \(\mathcal L\) | closed-ledger value | \(162\) | Distinct from \(R^2=144\). |

The lift coefficients \(5/48\), \(17/192\) and the unequal-pair forms from
SAMA-D000028 are row-class surface operators. They are not interchangeable
with \(Q_{\rm mass}\), \(Q_{\rm sub}\) or \(X_A\). SAMA-C000147-R001,
SAMA-C000149-R001 and SAMA-C000151-R001 retain that firewall.

## 3. Why the direct bridge had to deviate

CR239 tests

\[
m_i=m_g=\mu_QQ
\]

with one carbon-12 anchor. The anchor closes, but the Lane-A RMS residual is
\(0.189480\), compared with \(0.00202\) for the locked mass-number control.
The direct channel is therefore about ninety times worse than the control.

The residual carries a clear neutron-excess direction:

\[
\rho_S(\epsilon,N-Z)=+0.984,
\]

with \(N=Z\) subset RMS \(0.0023\) and \(N\ne Z\) subset RMS \(0.2152\).
The source artifact records FAIL_CR239_DIRECT_BRIDGE.

This result does two things at once:

1. it rejects \(Q_{\rm sub}\) as a direct measured-rest-mass channel; and
2. it retains the \(Q_{\rm sub}\) structure as a coupling source whose
   difference from a rest-source channel is organized by \(N-Z\).

SAMA-C000131-R001 and SAMA-C000155-R001 carry that distinction. Erasing the
failed run would erase the reason the two-channel derivation exists.

## 4. The typed correction before asymmetry

CR240 supplies

\[
Q_{\rm mass}=4A\kappa.
\]

With the carbon-12 bridge, its mass-number readout is \(A\,{\rm u}\). On 49
non-anchor Lane-A rows the source records RMS fractional residual
\(0.002024\), while the residual retains volume, surface, Coulomb and
asymmetry structure.

The coupling channel remains

\[
Q_{\rm sub}=8Z\kappa+\frac{N-Z}{8}.
\]

For \(N=Z\), the channels meet:

\[
Q_{\rm mass}
=4(2Z)\kappa
=8Z\kappa
=Q_{\rm sub}.
\]

For neutron excess, they separate. CR241 then challenges the candidate
extension on 20 unique holdout rows. It records holdout RMS
\(0.000686400048095\), anchor stability and intact control structure, but its
candidate scan contains 30 nucleon-window hits and six splitting-window hits.
Neither declared uniqueness threshold closes. The source artifact therefore
records FAIL_CR241_CANDIDATE_ARTIFACT while leaving the CR240 channel usable.

This is SAMA-C000168-R001's precise status: structure retained, uniqueness
unpromoted.

## 5. Direct-bridge deviation and exact asymmetry correction

This section carries the derivation at atomic granularity.

### 5.1 Start from the two typed channels

\[
Q_{\rm mass}=4A\kappa
\]

and

\[
Q_{\rm sub}=8Z\kappa+\frac{N-Z}{8}.
\]

Use

\[
A=Z+N.
\]

### 5.2 Substitute \(A=Z+N\)

\[
\begin{aligned}
\Delta Q
&=Q_{\rm mass}-Q_{\rm sub}\\
&=4A\kappa
 -\left(8Z\kappa+\frac{N-Z}{8}\right)\\
&=4(Z+N)\kappa-8Z\kappa-\frac{N-Z}{8}.
\end{aligned}
\]

The parentheses matter: the one-eighth term belongs to the coupling channel
and is subtracted with it.

### 5.3 Expand the rest-source term

\[
4(Z+N)\kappa=4Z\kappa+4N\kappa.
\]

Hence

\[
\Delta Q
=4Z\kappa+4N\kappa-8Z\kappa-\frac{N-Z}{8}.
\]

### 5.4 Collect the \(\kappa\) terms

\[
4Z\kappa-8Z\kappa=-4Z\kappa,
\]

so

\[
\Delta Q
=4N\kappa-4Z\kappa-\frac{N-Z}{8}.
\]

Factor \(4\kappa\):

\[
4N\kappa-4Z\kappa
=4\kappa(N-Z).
\]

Therefore

\[
\Delta Q
=4\kappa(N-Z)-\frac{N-Z}{8}.
\]

### 5.5 Factor neutron excess

Both terms contain \(N-Z\):

\[
\Delta Q
=(N-Z)\left(4\kappa-\frac18\right).
\]

This is the conceptual turning point. Nuclear imbalance is not inserted as an
independent empirical column; it appears because the balanced \(Z\)-dependent
parts cancel between the two source channels.

### 5.6 Reduce the per-excess gap exactly

Since

\[
\kappa=\frac{7117}{768},
\]

\[
4\kappa
=4\frac{7117}{768}
=\frac{7117}{192}.
\]

Put \(1/8\) over the same denominator:

\[
\frac18=\frac{24}{192}.
\]

Subtract:

\[
4\kappa-\frac18
=\frac{7117}{192}-\frac{24}{192}
=\frac{7117-24}{192}
=\frac{7093}{192}.
\]

Thus

\[
\boxed{
\Delta Q=(N-Z)\frac{7093}{192}.}
\]

This is the complete SAMA-C000169-R001 derivation.

### 5.7 Square the exact gap

\[
\begin{aligned}
(\Delta Q)^2
&=\left((N-Z)\frac{7093}{192}\right)^2\\
&=(N-Z)^2\frac{7093^2}{192^2}.
\end{aligned}
\]

The square removes the sign of the channel mismatch while retaining its
magnitude and makes the penalty symmetric under \(N-Z\mapsto Z-N\) at the
shape level.

### 5.8 Rewrite the normalizer

\[
Q_{\rm mass}=4A\kappa.
\]

Insert \(\kappa=7117/768\):

\[
\begin{aligned}
Q_{\rm mass}
&=4A\frac{7117}{768}\\
&=A\frac{7117}{192}.
\end{aligned}
\]

### 5.9 Divide and cancel

\[
\begin{aligned}
\frac{(\Delta Q)^2}{Q_{\rm mass}}
&=
\frac{(N-Z)^2\,7093^2/192^2}
     {A\,7117/192}\\
&=
(N-Z)^2\frac{7093^2}{192^2}
\frac{192}{A\,7117}.
\end{aligned}
\]

Cancel one factor of \(192\):

\[
\frac{192}{192^2}=\frac1{192}.
\]

Therefore

\[
\boxed{
\frac{(\Delta Q)^2}{Q_{\rm mass}}
=
\frac{(N-Z)^2}{A}
\frac{7093^2}{192\cdot7117}.}
\]

### 5.10 Reduce the coefficient

\[
7093^2=50310649
\]

and

\[
192\cdot7117=1366464.
\]

Hence

\[
\boxed{
\frac{(\Delta Q)^2}{Q_{\rm mass}}
=
\frac{(N-Z)^2}{A}
\frac{50310649}{1366464}.}
\]

Numerically,

\[
\frac{50310649}{1366464}
\approx36.8181298593.
\]

This completes SAMA-C000170-R001. The rational coefficient must be retained
exactly in computation before decimal display.

### 5.11 Balanced and single-excess checks

If \(N=Z\), then

\[
\Delta Q=0
\]

and

\[
\frac{(\Delta Q)^2}{Q_{\rm mass}}=0.
\]

For carbon-13, \(Z=6,N=7,A=13\), so

\[
\Delta Q=\frac{7093}{192},
\]

\[
Q_{\rm mass}=13\frac{7117}{192}
=\frac{92521}{192},
\]

and

\[
\frac{(\Delta Q)^2}{Q_{\rm mass}}
=\frac1{13}
\frac{50310649}{1366464}.
\]

These endpoint checks use no fitted binding coefficient.

### 5.12 CR245 execution and boundary

CR245 checks the identity on 71/71 rows with exact rational arithmetic.
Changing \(R\) to 10, 11 or 13 breaks all 58 nonzero-asymmetry rows for each
control; the 13 \(N=Z\) rows remain zero on both sides, as they must. Dropping
the asymmetry shape increases the source fit RMS from \(2.78\) to
\(12.47\) MeV, while shuffling the binding target increases it to
\(35.69\) MeV.

The exact export is the normalized-square identity. The same source preserves
that its zero-free typed coefficient substitutions do not recover the fitted
full curve. This is why SAMA-C000171-R001 requires nonlinear geometry beyond
the exact asymmetry component.

## 6. Native binding prerequisites

The registered precursor chain is:

\[
\text{QP:QP040}
\longrightarrow
\text{QP:QP047}
\longrightarrow
\text{QP:QP051}
\longrightarrow
\text{QP:QP052}.
\]

QP:QP040 supplies the native binding-residue operator framing. QP:QP047
selects the nuclear binding/isotope \(A\)-road. QP:QP051 selects
neutron-excess depth. QP:QP052 supplies the numeric \(\Delta N\) and
binding-mass comparison route.

Together they define the question and inputs. They do not close the
calibrated binding operator. In particular, a measured binding value remains
a comparator and cannot be used to select the native row or redefine
\(\kappa\).

The required nonlinear shape roster is

\[
\boxed{
\text{volume}
+\text{surface}
+\text{Coulomb}
+\text{asymmetry}
+\text{pairing}
+\text{gated family structure}.}
\]

The signs and coefficients are applied in a declared operation order; the
roster is not an invitation to add terms after reading residuals.

## 7. A-kernel failure, correction and historical retest

### 7.1 Linear connection-fee failure

SAMA-C000172-R001 preserves a separate source artifact that tests six
zero-fit sums of substrate-atom connection fees on 69 scored nuclei. Its best
rule is the per-excess-neutron sum, yet it records

\[
\max|\Delta|=89.85\ {\rm MeV}
\]

against the locked ceiling

\[
0.005\ {\rm MeV}.
\]

The candidate roster includes linear volume, proton-neutron pair,
channel-gap, squared-asymmetry and combined alternatives. None reproduces the
curvature. The failure establishes that a nucleus is not bound by a simple
linear count of particle-level connection fees.

Registry firewall: the current key CR:CR249@09a resolves to the A-kernel
artifact below. It does not resolve to this separate connection-fee artifact.
No second qualified SAMA test key is currently registered, so the
connection-fee source is carried through SAMA-C000172-R001 and is not given an
invented test-index row.

### 7.2 Registered A-kernel geometry

The registered CR:CR249@09a defines

\[
\rho_A=A^{1/3}.
\]

From that coordinate, the five shapes are

\[
V_A=\rho_A^3=A,
\]

\[
S_A=\rho_A^2=A^{2/3},
\]

\[
C_A=\frac{Z(Z-1)}{\rho_A}
=\frac{Z(Z-1)}{A^{1/3}},
\]

\[
X_A=\frac{(\Delta Q)^2}{Q_{\rm mass}},
\]

and the declared pairing column \(\delta_{\rm pair}\).

The fitted model is

\[
B_{\rm A\mbox{-}kernel}
=c_VA
-c_SA^{2/3}
-c_C\frac{Z(Z-1)}{A^{1/3}}
-c_AX_A
+c_P\delta_{\rm pair}.
\]

On the source split, the free-shape fit records

\[
\mathrm{RMS}_{\rm train}=2.7260\ {\rm MeV},
\qquad
R^2_{\rm train}=0.99458,
\]

\[
\mathrm{RMS}_{\rm test}=3.5218\ {\rm MeV},
\qquad
R^2_{\rm test}=0.98502.
\]

The fitted asymmetry coefficient is

\[
c_A^{\rm fit}=7.7504\times10^{-4}\ {\rm u},
\]

while the typed closed-ledger candidate is

\[
c_A^{\rm typed}
=\frac1{S\mathcal L}
=\frac1{8\cdot162}
=\frac1{1296}
\approx7.71605\times10^{-4}\ {\rm u}.
\]

Their relative difference is \(0.44\%\), the first within-1% typed
coefficient in this source arc.

The sensitivity ledger prevents over-compression:

- removing volume, surface, Coulomb or asymmetry worsens RMS by roughly
  \(7.49\), \(6.17\), \(5.26\) and \(4.54\) times;
- removing pairing worsens RMS by \(1.16\) times, below its declared
  \(1.5\)-times control gate;
- changing surface \(A^{2/3}\) to \(A^{1/2}\) worsens RMS by only
  \(1.14\) times, below its \(1.2\)-times gate;
- changing the Coulomb road from \(A^{-1/3}\) to \(A^{-2/3}\) worsens RMS
  by \(2.06\) times; and
- shuffling the target worsens RMS by \(13.02\) times.

Substituting all three within-5% typed candidates while retaining the other
two fitted coefficients raises RMS to \(21.71\) MeV on train and \(31.91\)
MeV on test. The A-kernel therefore recovers the needed geometry and a close
typed \(c_A\) candidate, but it is not a zero-free complete binding law.
This is SAMA-C000173-R001.

### 7.3 CR250 nonseparation

CR:CR250@09a applies the sealed particle-level lift form to the balanced and
excess positions. Its raw prediction is monotonic in the intended direction,
but the best single rescale still leaves

\[
\mathrm{RMS}=43.4176\ {\rm MeV}.
\]

Its designated wrong controls do not break the rescaled shape: depth,
\(D\), \(\mu_Q\), gap-label and shuffle substitutions remain nonseparating at
the locked gates. The source therefore records BOUNDARY_WC_FAIL. In the
coefficient-refinement lineage summarized by CR251, the corresponding
limitation is parameter degeneracy: the closed-ledger
\(1/(S\mathcal L)\) candidate is not separated from the bare-cycle
\(1/(SR^2)\) alternative by a coupled refit.

The precise export is failure of separation, not failure of monotonicity.

### 7.4 CR251 orthogonalized correction

CR251 removes non-asymmetry columns before comparing the two typed scales.
Let

\[
X_0=
\begin{bmatrix}
A&
-A^{2/3}&
-Z(Z-1)A^{-1/3}&
\delta_{\rm pair}
\end{bmatrix},
\]

and let \(X_A\) be the signed asymmetry column. Form

\[
P_0=X_0(X_0^TX_0)^{-1}X_0^T,
\]

\[
B_\perp=(I-P_0)B_u,
\qquad
X_{A,\perp}=(I-P_0)X_A.
\]

The isolated coefficient is

\[
c_{A,\rm orth}
=\frac{X_{A,\perp}^TB_\perp}
       {X_{A,\perp}^TX_{A,\perp}}.
\]

On the principal \(n=55\) lane,

\[
c_{A,\rm orth}
=7.339\times10^{-4}\ {\rm u},
\qquad
\mathrm{SE}=2.343\times10^{-5}\ {\rm u}.
\]

The closed-ledger candidate

\[
\frac1{S\mathcal L}=\frac1{1296}
\]

lies \(1.61\) standard errors from the estimate, inside the declared 95%
interval. The bare-cycle candidate

\[
\frac1{SR^2}=\frac1{8\cdot144}=\frac1{1152}
\]

lies \(5.73\) standard errors away, outside the declared 99% interval.
Thus the principal orthogonalized lane distinguishes the bounce-aware
closed-ledger scale.

The correction retains its own boundaries:

- the \(|N-Z|\ge20\) stress lane has only 24 rows and places both candidates
  inside its wider interval;
- the isobaric lane has only two pairs for three unknown contrast
  coefficients and is recorded as insufficient data; and
- four wrong controls pass: binding-target shuffle, \(N=Z\) degeneracy,
  a random added feature and asymmetry-column permutation.

SAMA-C000174-R001 therefore records a narrowed asymmetry scale without a
complete binding closure.

### 7.5 Historical CR274 retest/readout

CR:CR274@09a locks the exact CR245 asymmetry coefficient

\[
\frac{50310649}{1366464}
\approx36.81813
\]

inside a fitted Model K and applies four recorded family operators:

| Operator | Recorded role | Coefficient |
|---|---|---:|
| \(op_{82pre}\) | pre-82 family | \(-0.7273\) |
| \(op_{3d\_odd}\) | odd 3d family | \(+6.9654\) |
| \(op_{dm\_sat}\) | doubly-magic saturation | \(+7.1800\) |
| \(op_{ms\_fill}\) | mid-shell fill | \(-0.4531\) |

The source benchmark changes from

\[
\mathrm{RMS}_{\rm base}=3.9102\ {\rm MeV}
\]

to

\[
\mathrm{RMS}_{\rm gated}=2.7160\ {\rm MeV},
\]

with

\[
50/55
\]

rows within \(5\) MeV. Five source-listed outliers remain. The coefficients
and gate predicates are fitted nuclear-readout parameters. They are not new
substrate primitives. SAMA-C000175-R001 preserves CR274 as historical
readout evidence.

## 8. Current binding authority versus Volume II history

The current live binding authority is
[SAM_LIVE/06_BINDING_CURRENT.md](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/SAM_LIVE/06_BINDING_CURRENT.md).
It identifies B5T as the current completed representation/residual test and
records the authorized classification:

**The test result suggests strong contact with the concept.**

B5T installs an informational 3D tensor assignment and a leakage-safe held
chain. It does not install a physical tensor, nuclear geometry,
isotope-local tensor, \(A/q_A\) conversion, SI-energy law, Higgs law or final
binding formula.

Therefore:

- CR245 remains the exact Volume II asymmetry derivation;
- CR249–CR251 remain the A-kernel geometry and coefficient-control history;
- CR274 remains a historical fitted nuclear readout;
- B5T controls current binding status; and
- neither B5T nor current ATOM3D work retroactively turns CR274's fitted
  coefficients into substrate primitives.

This is a current-versus-historical boundary, not a competition between
results.

## 9. Established result and exact open work

The source chain establishes:

1. The direct coupling-source/rest-mass identity fails and its residual
   isolates neutron excess as the correction direction.
2. \(Q_{\rm mass}\) and \(Q_{\rm sub}\) are separately typed, and the CR240
   channel remains usable despite CR241's failed uniqueness promotion.
3. Their exact gap is \((N-Z)7093/192\).
4. The normalized square of that gap is exactly
   \((N-Z)^2/A\) times \(50310649/1366464\).
5. A linear connection-fee sum does not recover nuclear binding curvature.
6. The A-kernel supplies volume, surface, Coulomb, asymmetry and pairing
   shapes and locates \(1/(S\mathcal L)\) as the close typed asymmetry scale.
7. CR250 preserves nonseparation; CR251 corrects it on the principal
   orthogonalized lane while retaining low-power and isobaric boundaries.
8. CR274 supplies a historical gated readout, not current binding authority.

The exact open work is to derive the complete nonlinear binding operator from
the connector/carrier and current tensor geometry, including shared origins
for volume, surface, Coulomb, pairing and family gates, without changing the
exact asymmetry bridge.

All proposal crosswalk rows in this chapter carry
\(result\_classification=\mathrm{null}\). The exact current B5T
classification above is quoted from live authority, not assigned by this
document.

## 10. Forward handoff

SAMA-P000003 receives the full matter-side derivation. SAMA-P000006 receives
the finite-particle, binding and computation boundary. Volume III may consume
the exact rationals

\[
\kappa=\frac{7117}{768},
\qquad
\Delta Q=(N-Z)\frac{7093}{192},
\qquad
d_{\rm asym}=\frac{50310649}{1366464},
\]

but it must carry the source types and cannot infer a final binding operator
from those three values alone.

## Test and result index

| Test record key | Role | Source result/status | Result artifact | Test folder |
|---|---|---|---|---|
| CR:CR239@09a | Failed direct coupling-source/rest-mass bridge | CLEAN; source verdict FAIL; FAIL_CR239_DIRECT_BRIDGE | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR239_NATIVE_MASS_GRAVITY_BRIDGE/CR239_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR239_NATIVE_MASS_GRAVITY_BRIDGE) |
| CR:CR240@09a | Typed rest-source/coupling-source correction | CLEAN; source verdict PASS; rest-source channel identified | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR240_NEUTRON_REST_MASS_CHANNEL/CR240_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR240_NEUTRON_REST_MASS_CHANNEL) |
| CR:CR241@09a | Holdout uniqueness boundary | CLEAN; source verdict FAIL; FAIL_CR241_CANDIDATE_ARTIFACT | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR241_REST_MASS_HOLDOUT_UNIQUENESS/CR241_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR241_REST_MASS_HOLDOUT_UNIQUENESS) |
| CR:CR245@09a | Exact gap/asymmetry correction and full-binding boundary | CLEAN; source verdict BOUNDARY; 71/71 exact identity | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR245_BINDING_CURVATURE_FROM_TYPED_SUBSTRATE/CR245_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR245_BINDING_CURVATURE_FROM_TYPED_SUBSTRATE) |
| QP:QP040 | Native binding-residue operator framing | Source artifact supplies the premise | [result](../../courtroom/12_QUANTUM_COMPUTING_AND_NETWORKING/_source_artifacts/reports/QP040_PRIVATE_NATIVE_BINDING_RESIDUE_OPERATOR.md) | [folder](../../courtroom/12_QUANTUM_COMPUTING_AND_NETWORKING/_source_artifacts/reports) |
| QP:QP047 | Nuclear binding/isotope \(A\)-road selector | Source artifact supplies the selector | [result](../../courtroom/12_QUANTUM_COMPUTING_AND_NETWORKING/_source_artifacts/reports/QP047_PRIVATE_NUCLEAR_BINDING_ISOTOPE_A_ROAD_SELECTOR.md) | [folder](../../courtroom/12_QUANTUM_COMPUTING_AND_NETWORKING/_source_artifacts/reports) |
| QP:QP051 | Neutron-excess binding-depth selector | Source artifact supplies the selector | [result](../../courtroom/12_QUANTUM_COMPUTING_AND_NETWORKING/_source_artifacts/reports/QP051_PRIVATE_NEUTRON_EXCESS_BINDING_DEPTH_SELECTOR.md) | [folder](../../courtroom/12_QUANTUM_COMPUTING_AND_NETWORKING/_source_artifacts/reports) |
| QP:QP052 | Numeric \(\Delta N\) and binding-mass selector | Source artifact supplies the selector | [result](../../courtroom/12_QUANTUM_COMPUTING_AND_NETWORKING/_source_artifacts/reports/QP052_PRIVATE_NUMERIC_DELTA_N_AND_BINDING_MASS_SELECTOR.md) | [folder](../../courtroom/12_QUANTUM_COMPUTING_AND_NETWORKING/_source_artifacts/reports) |
| CR:CR249@09a | Registered A-kernel five-shape geometry | CLEAN; source verdict BOUNDARY; \(c_A=1/(S\mathcal L)\) within 0.44% of fit | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR249_A_KERNEL_BINDING_GEOMETRY/CR249_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR249_A_KERNEL_BINDING_GEOMETRY) |
| CR:CR250@09a | Monotonic but nonseparating lift-form route | CLEAN; source verdict BOUNDARY; artifact verdict BOUNDARY_WC_FAIL | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR250_BINDING_FROM_CR009_LIFT_FORMULA/CR250_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR250_BINDING_FROM_CR009_LIFT_FORMULA) |
| CR:CR251@09a | Orthogonalized asymmetry-scale correction | CLEAN; source verdict BOUNDARY; principal lane distinguishes \(1/(S\mathcal L)\) | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR251_BOUNCE_AWARE_ASYM_ISOLATION/CR251_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR251_BOUNCE_AWARE_ASYM_ISOLATION) |
| CR:CR274@09a | Historical fitted nuclear readout | Source verdict PASS; RMS \(3.9102\to2.7160\) MeV and 50/55 within 5 MeV | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR274_GATED_NUCLEAR_READOUT_OPERATORS/CR274_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR274_GATED_NUCLEAR_READOUT_OPERATORS) |

The separate connection-fee source described by SAMA-C000172-R001 has no
distinct current SAMA test-record key and is intentionally absent from this
table.

## Atomic SAMA source records

| Record ID | Role in this document |
|---|---|
| SAMA-C000131-R001 | Source-support/rest-mass distinction. |
| SAMA-C000147-R001 | Typed lift rather than a global mass equation. |
| SAMA-C000149-R001 | Equal/OCTET class separation. |
| SAMA-C000151-R001 | Unequal-pair class separation. |
| SAMA-C000155-R001 | Failed direct source/rest-mass bridge. |
| SAMA-C000156-R001 | Typed \(Q_{\rm mass}\) and \(Q_{\rm sub}\). |
| SAMA-C000164-R001 | Nuclear aggregate identities. |
| SAMA-C000168-R001 | CR240 candidate retained without uniqueness promotion. |
| SAMA-C000169-R001 | Exact \(\Delta Q\) derivation. |
| SAMA-C000170-R001 | Exact normalized-square asymmetry derivation. |
| SAMA-C000171-R001 | Nonlinear binding-shape requirement. |
| SAMA-C000172-R001 | Separate linear connection-fee failure and registry firewall. |
| SAMA-C000173-R001 | Registered A-kernel geometry and typed \(c_A\) candidate. |
| SAMA-C000174-R001 | Nonseparation-to-orthogonalization correction chain. |
| SAMA-C000175-R001 | Historical CR274 fitted-readout boundary. |

## External references

All measured nuclear comparators remain inside the registered source
artifacts. Current status is taken only from the linked live binding
authority. No independent external dataset is introduced here.

## Revision and approval

This exact revision has reviewed_and_approved: false and approval: null until
Sean Brady explicitly approves it.

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000032`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/BINDING_AND_THE_EXACT_ASYMMETRY_BRIDGE.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol II | SAMA-D000032 | Binding | Exact Neutron-Excess Asymmetry and Nonlinear Binding Routes |

| Document field | Value |
|---|---|
| Purpose | Carry the failed direct source/rest-mass bridge through the exact neutron-excess channel-gap derivation, then locate that exact component inside the nonlinear binding and historical nuclear-readout chain. |
| Prerequisite documents | SAMA-D000030 |
| Used by | Volume II and III synthesis through SAMA-P000003 and SAMA-P000006; generated from the document catalog |

</details>
