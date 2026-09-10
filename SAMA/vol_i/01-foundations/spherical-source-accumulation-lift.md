[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Spherical Source Accumulation Lift \(A(r)\)

## Conceptual abstract

A finite spherical source contributes the dimensionless accumulation lift

\[
A_s(r)=\frac{r_s}{r}=\frac{2GM_s}{c^2r},
\qquad
r_s=\frac{2GM_s}{c^2}.
\]

The formula is the end of a typed source-interface chain, not its whole
meaning. Closed matter is written upstream; \(q_A\) supplies source support;
the one-eighth unresolved tensor channel carries the write; ledger compression
produces the outward \(A\)-coordinate. Only after that field exists does a
declared operator read potential, acceleration, clock, road or another
observable.

The source lift is not the complete pointwise substrate account. With the
universal floor from `SAMA-D000002`,

\[
A_{\rm total}=A_0+A_{\rm lift}.
\]

For several weak sources, their lifts add before any readout is taken. At the
source scale \(r=r_s\), the spherical profile reaches \(A_s=1\). This is a
closure marker and a handoff to the strong-field chain, not permission to
continue weak formulas ordinarily into \(A>1\).

## 1. Opening question and conceptual picture

The chapter answers two connected questions.

1. How does a finite matter source enter Volume I without identifying matter,
   \(q_A\), tensor carrier and accumulation as the same object?
2. Once the source contribution has been formed, how does one combine sources
   and attach the universal floor before selecting an observable?

The source-bound route is

\[
\begin{aligned}
\text{closed matter write}
&\longrightarrow q_A\text{ source support}\\
&\longrightarrow \frac18\text{ unresolved tensor carrier}\\
&\longrightarrow \text{ledger compression}\\
&\longrightarrow A_s(r)=\frac{r_s}{r}\\
&\longrightarrow \text{declared readout operator}.
\end{aligned}
\]

Every arrow is a type transition. The matter write is a source condition.
\(q_A\) is support in that source route. The one-eighth channel is carrier.
\(A_s\) is the resulting dimensionless field lift. Potential or acceleration
is an output of an operator on that field. Skipping an arrow makes the
construction shorter on paper and changes the question being answered.

## 2. Typed definitions, domains and units

| Symbol/object | Definition or role | Type/domain | SI units |
|---|---|---|---|
| \(M_s\) | mass of the finite source supplied at the Volume II/I boundary | positive source parameter | kg |
| \(G\) | gravitational conversion constant used in the spherical source scale | constant | m\(^3\) kg\(^{-1}\) s\(^{-2}\) |
| \(c\) | invariant local light speed | positive constant | m s\(^{-1}\) |
| \(r\) | exterior radial distance from source center | positive coordinate, with weak source lane at \(r>r_s\) | m |
| \(r_s\) | \(2GM_s/c^2\) | source length scale | m |
| \(A_s(r)\) | \(r_s/r\) | spherical source accumulation lift | dimensionless |
| \(A_{\rm lift}(\mathbf x)\) | sum of source-conditioned lifts | weak many-source scalar field | dimensionless |
| \(A_0\) | \(1/(12\pi)\) | uniform background floor | dimensionless |
| \(A_{\rm total}\) | \(A_0+A_{\rm lift}\) | complete pointwise substrate account | dimensionless |
| \(q_A\) | source support inside the registered compression route | Volume II/I interface object | not promoted here to mass or to \(A\) |
| \(\Theta\) | \(\alpha_HD^2=18\) | carrier count/first overflow | dimensionless count, not kg |

The dimensional check for the source scale is explicit:

\[
[r_s]
=\frac{[G][M_s]}{[c]^2}
=\frac{(\mathrm{m^3,kg^{-1},s^{-2}})(\mathrm{kg})}
        {\mathrm{m^2,s^{-2}}}
=\mathrm m.
\]

Consequently

\[
[A_s]=\frac{[r_s]}{[r]}=1.
\]

This unit closure is necessary but not sufficient: many dimensionless
expressions exist. The registered source packet also fixes the factor two and
the radial power.

## 3. From source scale to spherical lift

### 3.1 Form the source length

Begin with the mass-length combination

\[
\frac{GM_s}{c^2}.
\]

Multiplication by the registered binary coefficient gives the source scale

\[
r_s=\frac{2GM_s}{c^2}.
\]

The factor two must remain visible. Omitting it would produce a half-strength
field downstream; adding another would double the potential and acceleration.

### 3.2 Normalize by exterior radius

To obtain a dimensionless spherical coordinate, divide the source length by
the observation radius:

\[
A_s(r)=\frac{r_s}{r}.
\]

Substitution yields

\[
\boxed{A_s(r)=\frac{2GM_s}{c^2r}}.
\]

The inverse first power of \(r\) belongs to the field lift. The inverse-
square dependence of acceleration appears only after the gradient operator in
`SAMA-D000004`. Writing \(A\propto r^{-2}\) at this stage would collapse the
field and its readout into one object.

### 3.3 Verify the source-scale closure marker

Set \(r=r_s\):

\[
A_s(r_s)=\frac{r_s}{r_s}=1.
\]

For radii outside the source scale, write \(r=\lambda r_s\) with
\(\lambda>1\). Then

\[
A_s(\lambda r_s)
=\frac{r_s}{\lambda r_s}
=\frac1\lambda,
\]

so the field decreases monotonically from the closure marker:

| \(r/r_s\) | \(A_s\) |
|---:|---:|
| \(1\) | \(1\) |
| \(2\) | \(1/2\) |
| \(5\) | \(1/5\) |
| \(10\) | \(1/10\) |
| \(100\) | \(1/100\) |

The equality \(A_s=1\) is exact for every positive source scale. It is a
boundary identity, not an empirical fit and not a normal weak-field launch
state.

## 4. The matter-to-\(q_A\)-to-\(A\) interface

### 4.1 Closed matter supplies a source write

Volume I accepts a finite source characterized at this boundary by \(M_s\).
It does not derive the particle, isotope or composite grammar that closes that
source; those constructions remain Volume II. The interface therefore begins
with “closed matter write,” not with a claim that substrate is matter.

### 4.2 \(q_A\) supplies source support

The registered bridge uses \(q_A\) as source support. That role is upstream of
the macroscopic \(A_s(r)\) field. Directly replacing \(M_s\) with a particle-
level \(q_A\) expression inside the weak spherical law is not the Last Campaign
mechanism route.

The historical `G:G744c@SAM-ARCHIVE` construction explored how its upstream
\(q_A\) rows add through composite and macroscopic mixtures. It recorded a
native macro \(\sum q_A/\sum m\) range from
\(1.0066314559621623\) to \(1.0099471839432435\), with fractional spread
\(0.003286777770728273\); a random-assignment control produced the much
larger spread \(0.11820137636373475\). Those values document the source-
strength discovery branch. They do not authorize Volume I to import its
particle species formulas or to substitute \(q_A\) directly for mass.

### 4.3 The one-eighth unresolved channel carries the write

From the foundation packet,

\[
2^{-D}=\frac18,
\qquad
R^2 2^{-D}=18=\Theta.
\]

This is the unresolved tensor carrier side. It transports the source write
through the ledger route. It is not an additional eighteen units of rest mass,
and it is not the \(3/4\) surface debit.

### 4.4 Ledger compression produces the outward field coordinate

After the carrier step, the route compresses into the spherical macroscopic
coordinate \(A_s(r)=r_s/r\). At this point the field no longer carries the
particle labels needed to construct the source. It carries the source-
conditioned accumulation available to Volume I operators.

This is the precise cross-volume seam:

| Upstream/downstream side | Owns | Does not become |
|---|---|---|
| Volume II matter side | finite closed source and \(q_A\) support grammar | substrate field ontology |
| Carrier interface | one-eighth unresolved tensor transport | matter/rest-mass row |
| Volume I field side | \(A_s(r)\), superposition, total account and readout routing | particle/isotope grammar |
| Volume III execution side | computation of declared maps and receipts | conceptual source authority |

## 5. Many-source accumulation root

### 5.1 Form each source lift

For a weak source \(i\) at \(\mathbf x_i\), define

\[
A_i(\mathbf x)
=\frac{2GM_i}{c^2|\mathbf x-\mathbf x_i|}.
\]

Each term is dimensionless and retains its own source location and strength.

### 5.2 Sum the source-conditioned terms

The weak many-source lift is

\[
\boxed{
A_{\rm lift}(\mathbf x)
=\sum_i\frac{2GM_i}{c^2|\mathbf x-\mathbf x_i|}
}.
\]

The sum occurs **before** selecting potential, gradient, clock or route
operators. This ordering preserves linear source traceability and prevents a
halo profile or other collective readout from being assumed before the
primitive contributions exist.

### 5.3 Attach the universal floor

Only after the source-conditioned lift is formed do we state the full
pointwise account:

\[
\boxed{A_{\rm total}(\mathbf x)=A_0+A_{\rm lift}(\mathbf x)}.
\]

For two sources,

\[
A_{\rm total}(\mathbf x)
=A_0
 +\frac{2GM_1}{c^2|\mathbf x-\mathbf x_1|}
 +\frac{2GM_2}{c^2|\mathbf x-\mathbf x_2|}.
\]

If the next operator is a gradient, \(A_0\) differentiates to zero and
each source gradient remains. If it is a pointwise substrate inventory, all
three terms remain. The choice belongs to the readout, not to the source sum.

### 5.4 Cumulative spherical form is a later specialization

For a spherically organized distribution, the registered halo-root source
also names

\[
A(r)=\frac{r_s(<r)}r.
\]

[`CR:CR022@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr022-native-a-many-nonzero-accumulation/README.md) treats this as a structural many-nonzero construction. It does
not establish a completed halo inventory, a selected radial law, or an
external galaxy observation. Those questions remain with their later focused
documents and tests.

## 6. Worked source examples

### 6.1 The typed-kernel sample

[`CR:CR003@02`](../../tests/courtroom/02-a-kernel-weak-field-cr003-a-kernel-typed-readout-recertification/README.md) records the sample

\[
r_s=0.0088701028718461,
\qquad
A_s=1.3922622621010988\times10^{-9}.
\]

It then applies the separate potential operator and obtains

\[
\Phi[A_s]=-62565145.91115995,
\]

against the independently evaluated Newtonian value

\[
\Phi_N=-62565145.91115994.
\]

The field and potential are intentionally displayed on separate lines. The
first is dimensionless; the second is the output of \(-c^2/2\) and has
potential units. The same Courtroom packet records a many-source value
\(2.297220655470099\times10^{-9}\), confirming that its construction keeps a
many-source lane distinct from the one-source sample.

### 6.2 A simple two-source sum

Let an observation point be at distances \(d_1\) and \(d_2\) from two weak
sources. Then

\[
A_{\rm lift}
=\frac{2G}{c^2}\left(\frac{M_1}{d_1}+\frac{M_2}{d_2}\right).
\]

If \(M_2=M_1\) and \(d_2=2d_1\),

\[
A_{\rm lift}
=\frac{2GM_1}{c^2d_1}\left(1+\frac12\right)
=\frac32 A_1.
\]

Nothing in that sum yet says “acceleration” or “halo.” It is the accumulated
input on which a later typed operator may act.

### 6.3 Many tiny nonzero contributions

[`CR:CR022@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr022-native-a-many-nonzero-accumulation/README.md) records a single nonzero contribution of \(10^{-18}\) and a
declared many-nonzero sum of
\(1.0000000000000001\times10^{-7}\). The example demonstrates the
constructional point that individually sub-threshold nonzero entries may form
a collective field. The test explicitly stops before claiming that this
arithmetic alone closes a galaxy-halo observation.

## 7. Closed source to spherical accumulation

### 7.1 Historical source-strength construction

`G:G744c@SAM-ARCHIVE` is the construction-stage source-strength bridge. It
tests upstream elementary, composite and macroscopic rows with no per-species
or per-composite fit and records
`G744c_Q_A_SOURCE_STRENGTH_BRIDGE_PASS`. For Volume I, its load-bearing role is
the existence of a source-support bridge. Its particle rows remain Volume II
material, and its verdict does not itself define the final gravity-as-\(A\)
mechanism.

### 7.2 Typed kernel boundary

[`CR:CR003@02`](../../tests/courtroom/02-a-kernel-weak-field-cr003-a-kernel-typed-readout-recertification/README.md) tests six candidate kernels. Only

\[
A(r)=\frac{r_s}{r}
\]

reproduces the complete potential, horizon, clock and many-source packet. The
half-\(A\), inverse-square-\(A\), doubled-potential, shifted-horizon and
linear-clock candidates each miss at least one part. Its execution is `CLEAN`
and its source scientific verdict is `BOUNDARY`, because it is a native
recertification rather than an external comparison.

### 7.3 External weak-field result

[`CR:CR004@02`](../../tests/courtroom/02-a-kernel-weak-field-cr004-weak-field-a-kernel-external-contact/README.md) applies the selected source kernel to external Earth, Moon and
Sun rows with zero fitted parameters. Its execution is `CLEAN` and source
scientific verdict is `PASS`. In this document, it shows that the constructed
source lift reaches a functioning typed readout. The authorized SAMA result
classification for that scoped external contact is owned and stated in
`SAMA-D000004`, where the readout derivation and controls are complete.

### 7.4 Mechanism replay and repaired type boundary

[`LC:LC03`](../../tests/courtroom/16-the-last-campaign/README.md) replays the complete route from the locked primitive stack:

\[
\text{closed write}\to q_A\to\frac18\text{ carrier}
\to\text{compression}\to A(r)\to\text{readout}.
\]

It rejects 15/15 wrong controls, including direct \(q_A\)-as-mass, no ledger
compression, missing carrier, wrong \(1/4\) and \(1/16\) splits, carrier-to-
matter promotion, random \(q_A\), lane mixing, static-\(A\) treatment of a GW
release delay and \(A=1\) as a normal launch point. This later replay is why
the source interface is written as a chain rather than collapsed into a direct
substitution.

### 7.5 Many-source construction boundary

[`CR:CR022@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr022-native-a-many-nonzero-accumulation/README.md) confirms that the native formula/action packet contains explicit
many-source and cumulative spherical forms, while its `BOUNDARY` verdict
prevents the construction from being reported as completed halo contact. The
preserved boundary is a forward pointer, not a defect in the source sum.

## 8. Wrong controls, with their causal failure

| Wrong or diagnostic control | Where the chain breaks | Correct route |
|---|---|---|
| \(q_A\) substituted directly as mass | Erases the source-support and compression stages. | Closed matter write \(\to q_A\) support \(\to\) carrier \(\to A\). |
| \(\Theta=18\) promoted to matter | Counts a transport carrier as rest mass. | Keep \(\Theta\) carrier-only. |
| No one-eighth carrier | Removes the exact \(R^2/8=18\) interface. | Retain the locked \(1/8\) unresolved route. |
| Use \(1/4\) or \(1/16\) | Breaks the primitive \(2^{-D}\) split. | Use \(2^{-3}=1/8\). |
| Set \(A\propto r^{-2}\) | Puts the acceleration radial power into the field before differentiation. | Use \(A_s\propto r^{-1}\); the gradient supplies \(r^{-2}\). |
| Replace \(A_{\rm total}\) with \(A_s\) | Deletes the universal floor from the pointwise state. | State \(A_{\rm total}=A_0+A_{\rm lift}\), then declare the readout. |
| Read each source before summing | Can make a nonlinear readout masquerade as linear source addition. | Form the weak source sum first; apply the selected operator second. |
| Impose a halo profile before the source sum | Assumes the collective result being tested. | Preserve all source contributions, then test later halo/radial operators. |
| Continue the weak law normally through \(A>1\) | Crosses the closure marker without the strong-field operator. | Stop the weak source lane at \(A=1\) and hand off. |
| Treat \(A=1\) as a normal launch state | Contradicts the registered closure/road boundary. | Use the exterior \(A\to1^-\) chain in the strong-field document. |

## 9. Established result, boundaries and forward handoff

The complete source-bound packet to carry forward is

\[
\boxed{
r_s=\frac{2GM_s}{c^2},\qquad
A_s(r)=\frac{r_s}{r},\qquad
A_{\rm lift}(\mathbf x)=\sum_i\frac{2GM_i}{c^2|\mathbf x-\mathbf x_i|},\qquad
A_{\rm total}=A_0+A_{\rm lift}
}.
\]

At \(r=r_s\), \(A_s=1\) exactly. The weak exterior lane is read for
\(r>r_s\); the strong-field meaning of closure belongs to later Volume I
documents. The source route may name matter and \(q_A\) at its interface, but
particle/isotope grammar remains Volume II. Execution internals remain Volume
III.

No SAMA result classification is assigned in this chapter. The registered
source statuses and verdicts document construction, boundary, external result
and replay. `SAMA-D000004` receives the source field and owns the scoped
weak-field external-contact classification after deriving the typed
observables.

Exact evidence is the complete five-key sequence in Section 10. The
specifically open boundary is the detailed matter-to-\(q_A\) source mechanism
in Volume II, native many-source halo organization in the later galaxy lane,
and every exact strong-field operator beyond the \(A=1\) handoff.

## 10. Focused test and result index

| Exact qualified key | Evidence role | Preserved outcome | Direct result | Result folder |
|---|---|---|---|---|
| `G:G744c@SAM-ARCHIVE` | Source-strength construction | `G744c_Q_A_SOURCE_STRENGTH_BRIDGE_PASS`; particle-detail claims remain upstream of Volume I. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G744_SOURCE_STRENGTH_GRAVITY_BRIDGE_CAMPAIGN/G744c_Q_A_SOURCE_STRENGTH_BRIDGE/G744c_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G744_SOURCE_STRENGTH_GRAVITY_BRIDGE_CAMPAIGN/G744c_Q_A_SOURCE_STRENGTH_BRIDGE) |
| [`CR:CR003@02`](../../tests/courtroom/02-a-kernel-weak-field-cr003-a-kernel-typed-readout-recertification/README.md) | Typed-kernel boundary | Source execution `CLEAN`, scientific verdict `BOUNDARY`; unique complete \(A=r_s/r\) packet. | [result](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION/CR003_result.md) | [folder](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION) |
| [`CR:CR004@02`](../../tests/courtroom/02-a-kernel-weak-field-cr004-weak-field-a-kernel-external-contact/README.md) | Downstream external result | Source execution `CLEAN`, scientific verdict `PASS`; scoped weak-field contact with zero fitted parameters. | [result](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT/CR004_result.md) | [folder](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT) |
| [`LC:LC03`](../../tests/courtroom/16-the-last-campaign/README.md) | Locked mechanism replay | `LC03_PASS_QA_LEDGER_COMPRESSION_GRAVITY_AS_A_REPLAY`; 15/15 wrong controls rejected. | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN) |
| [`CR:CR022@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr022-native-a-many-nonzero-accumulation/README.md) | Many-source construction | Source execution `CLEAN`, scientific verdict `BOUNDARY`; native many-nonzero root without completed halo contact. | [result](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION/CR022_result.md) | [folder](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION) |

## 11. Atomic record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000002-R001` | Defines \(r_s\), \(A_s(r)\), and \(A_s(r_s)=1\). |
| `SAMA-C000031-R001` | Supplies the \(\Theta=18\) carrier type. |
| `SAMA-C000036-R001` | Routes the floor through pointwise, gradient, endpoint and global operators. |
| `SAMA-C000037-R001` | Records the closed-matter-to-\(q_A\)-to-carrier-to-\(A\) interface. |
| `SAMA-C000038-R001` | Defines weak many-source additivity before readout. |
| `SAMA-C000039-R001` | Separates source lift from total accumulation. |
| `SAMA-C000040-R001` | Types \(A=1\) as the source-scale closure marker. |
| `SAMA-C000122-R001` | Enforces the Volume I/II/III subject boundary. |
| `SAMA-C000124-R001` | Separates source-era chronology from current live authority. |
| `SAMA-C000125-R001` | Preserves source verdicts, authorized classifications and false approval state. |

## 12. Source and approval boundary

The direct evidence set is exactly the five qualified keys above. Courtroom
links are pinned to commit `b5e914f71377e86ef4c67e199973d9300795cda1`;
the G744c link resolves to its exact locally registered artifact. Terms such as
“current” or “latest” in older sources are treated as source-era chronology;
present SAMA state is controlled by `SAM_LIVE/07_SAMA_CURRENT.md`.

`reviewed_and_approved` remains `false`, and `approval` remains `null`.
Source replay, external contact and document validation do not imply approval.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`CR:CR003@02`](../../tests/courtroom/02-a-kernel-weak-field-cr003-a-kernel-typed-readout-recertification/README.md) | [CR003_PRECOMMIT.md](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION/CR003_PRECOMMIT.md)<br>[CR003_declared_premises.json](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION/CR003_declared_premises.json) | [CR003_A_kernel_typed_readout_recertification.py](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION/CR003_A_kernel_typed_readout_recertification.py) | [CR003_candidate_rows.csv](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION/CR003_candidate_rows.csv) | [CR003_result.md](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION/CR003_result.md)<br>[CR003_summary.json](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION/CR003_summary.json) | [All 8 files](../../tests/courtroom/02-a-kernel-weak-field-cr003-a-kernel-typed-readout-recertification/README.md) |
| [`CR:CR004@02`](../../tests/courtroom/02-a-kernel-weak-field-cr004-weak-field-a-kernel-external-contact/README.md) | [CR004_PRECOMMIT.md](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT/CR004_PRECOMMIT.md)<br>[CR004_declared_premises.json](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT/CR004_declared_premises.json) | [CR004_weak_field_external_contact.py](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT/CR004_weak_field_external_contact.py) | [CR004_candidate_rows.csv](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT/CR004_candidate_rows.csv) | [CR004_result.md](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT/CR004_result.md)<br>[CR004_summary.json](../../courtroom/02_A_KERNEL_WEAK_FIELD/CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT/CR004_summary.json) | [All 8 files](../../tests/courtroom/02-a-kernel-weak-field-cr004-weak-field-a-kernel-external-contact/README.md) |
| [`CR:CR022@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr022-native-a-many-nonzero-accumulation/README.md) | [CR022_PRECOMMIT.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION/CR022_PRECOMMIT.md)<br>[CR022_declared_premises.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION/CR022_declared_premises.json) | [CR022_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION/CR022_runner.py) | [CR022_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION/CR022_runner.py)<br>[CR022_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION/CR022_result.md)<br>[CR022_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION/CR022_summary.json) | [CR022_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION/CR022_result.md)<br>[CR022_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION/CR022_summary.json) | [All 9 files](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr022-native-a-many-nonzero-accumulation/README.md) |
| [`LC:LC03`](../../tests/courtroom/16-the-last-campaign/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign/README.md) | [LC03_qa_ledger_compression_gravity_a_replay_runner.py](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_qa_ledger_compression_gravity_a_replay_runner.py) | [LC03_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_wrong_controls.csv)<br>[LC03_wrong_controls.csv.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_wrong_controls.csv.sha256.txt) | [LC03_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_result.md)<br>[LC03_result.md.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_result.md.sha256.txt)<br>[LC03_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_summary.json)<br>[LC03_summary.json.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_summary.json.sha256.txt) | [All 164 files](../../tests/courtroom/16-the-last-campaign/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000003`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/SPHERICAL_SOURCE_ACCUMULATION_LIFT.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000003 | Accumulation Field | Matter-to-qA Source Interface, Spherical Lift and Many-Source Additivity |

| Document field | Value |
|---|---|
| Purpose | Carry the source route from closed matter through \(q_A\) support and carrier compression into the spherical lift, then distinguish total accumulation, many-source additivity and the \(A=1\) source-scale boundary. |
| Prerequisite documents | `SAMA-D000001`, `SAMA-D000002` |
| Used by | `SAMA-P000005`, `SAMA-D000004`, `SAMA-D000005`, `SAMA-D000007`, `SAMA-D000013`, `SAMA-D000022`; assembled into `SAMA-P000002`. |
| Primary source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`, SHA-256 `2f22500f6583f567e350974610f00142e89b081a5b8c4c90c6dfe89bec43be0d`. |
| Revision state | Source-bound draft; mechanically registered proposal; not reviewed or approved. |

</details>
