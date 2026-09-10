[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Universal Accumulation Floor \(A_0\)

## Conceptual abstract

The relation was discovered before its present primitive vocabulary was
named. Sean Brady identifies the antecedent form as

\[
A_0=\frac1{h\pi\,h\,d}
=\frac1{(2\pi)\cdot2\cdot3}.
\]

The later compact-cycle, distinction-arity and spatial-support labels are the
typed crosswalk that explains the composition without replacing that
discovery genealogy.

The universal accumulation floor is

\[
A_0=\frac1{\pi R}=\frac1{12\pi}
=0.026525823848649224\ldots.
\]

It is a background component of the substrate account, not a fitted offset
added separately to each observation. Its source derivation resolves three
different factors: the primitive compact phase cycle \(2\pi\), the distinction
arity \(\alpha_H=2\), and the support dimension \(D=3\). The same value is
also reached by projecting the unit local-closure marker through the angular-
dimensional denominator \(4\pi D\).

The most important conceptual point is operational. Universality does not mean
that every observable displays the floor as an additive signal. A pointwise
substrate account retains \(A_0\); a gradient differentiates it to zero; a
shared endpoint difference cancels it; a global inventory or cosmological
road can retain it. The question is never simply “is the floor present?” It is
**which typed operator is reading the accumulated field?**

## 1. Opening question and conceptual picture

Suppose the total accumulated state at a point is

\[
A_{\rm total}(\mathbf x)=A_0+A_{\rm lift}(\mathbf x).
\]

Four apparently conflicting statements can then all be true:

- the floor belongs to the total substrate state;
- the floor produces no local acceleration;
- the floor cancels from a comparison of two endpoints sharing the same
  background;
- the floor remains load-bearing in a global inventory such as \(RA_0\).

The resolution is that these are four different maps from a field to a
readout. A universal constant survives the identity map, lies in the kernel of
a derivative, cancels under a difference, and survives multiplication in a
global inventory. The chapter develops the floor and its operator table
together so that no later document has to remove or insert it by convention.

## 2. Definitions, domains and units

| Symbol or map | Definition | Type | Units/output |
|---|---|---|---|
| \(A_0\) | \(1/(12\pi)\) | uniform universal accumulation floor | dimensionless scalar |
| \(A_{\rm lift}(\mathbf x)\) | source-conditioned contribution | local source lift | dimensionless scalar field |
| \(A_{\rm total}\) | \(A_0+A_{\rm lift}\) | pointwise total substrate account | dimensionless scalar field |
| \(\mathcal I[A]\) | \(A(\mathbf x)\) | pointwise-value operator | dimensionless |
| \(\mathcal G[A]\) | \(\nabla A\) | local gradient operator | inverse length |
| \(\mathcal D_{21}[A]\) | \(A(\mathbf x_2)-A(\mathbf x_1)\) | shared-endpoint difference | dimensionless |
| \(\mathcal R_\Gamma[A]\) | route integral declared for path \(\Gamma\) | road operator | depends on normalization; local photon exposure has time units after division by \(c\) |
| \(\mathcal C[A_0,R]\) | e.g. \(RA_0\) | global inventory operator | dimensionless |

The floor is dimensionless. It is not an acceleration, a speed, a delay, a
distance, an energy or a density parameter until a declared operator maps it
into the corresponding readout. This typing rule is the firewall between the
universal state and its many downstream uses.

## 3. Foundation derivation, with every factor exposed

### 3.1 Discovery genealogy and typed reconstruction

The historical order is equation first, explicit primitive naming later. The
owner-originated chronology is recorded by `SAMA-C000258-R001`; the recovered
Courtroom factorization is anchored by `SAMA-C000257-R001`. The derivation in
the rest of this section is the current typed reconstruction of the antecedent
relation. It identifies which structural object supplies each factor and
prevents numerical equality from collapsing their provenance.

### 3.2 Start from the typed factors

The source packet assigns

\[
\alpha_H=2,\qquad D=3,\qquad
\text{primitive compact phase cycle}=2\pi.
\]

The factors have different roles:

| Factor | Numerical contribution | Provenance |
|---|---:|---|
| Compact phase cycle | \(2\pi\) | one complete primitive phase period |
| Primitive arity | \(\alpha_H=2\) | binary distinction/worldsheet pair |
| Spatial support | \(D=3\) | dimension of support |

The two appearances of the numeral \(2\) may be multiplied, but they may
not be identified. One belongs to periodic completion; the other belongs to
primitive arity.

### 3.3 Form the denominator

The foundation definition is

\[
A_0=\frac1{(2\pi)\alpha_HD}.
\]

Insert the arity:

\[
(2\pi)\alpha_HD
=(2\pi)(2)D
=4\pi D.
\]

Insert the support dimension:

\[
4\pi D=4\pi(3)=12\pi.
\]

Thus

\[
\boxed{A_0=\frac1{12\pi}}.
\]

### 3.4 Recover the radix form

From `SAMA-D000001`,

\[
R=\alpha_H^2D=2^2\cdot3=12.
\]

At the declared \(\alpha_H=2\),

\[
(2\pi)\alpha_HD
=\pi\alpha_H^2D
=\pi R.
\]

Therefore

\[
A_0
=\frac1{(2\pi)\alpha_HD}
=\frac1{\pi\alpha_H^2D}
=\frac1{\pi R}.
\]

This equality is evaluated at the registered binary arity. It should not be
silently generalized by replacing \(\alpha_H\) with an arbitrary variable: the
step \(2\alpha_H=\alpha_H^2\) holds here because \(\alpha_H=2\).

### 3.5 Numerical evaluation and reciprocal checks

Using \(\pi\) in the registered source computation,

\[
A_0=0.026525823848649224\ldots.
\]

Two convenient exact checks are

\[
A_0^{-1}=12\pi=37.69911184307752\ldots
\]

and

\[
\pi A_0=\frac1R=\frac1{12}.
\]

These are algebraic replay checks. They do not by themselves assign an
observational result classification.

## 4. Horizon-to-floor projection

### 4.1 Declare the input type

For the spherical source coordinate developed in `SAMA-D000003`, the local
closure marker is

\[
A_H=1.
\]

Here \(A_H\) is a local unit-closure value. It is not the universal floor.

### 4.2 Project through angular and dimensional support

The registered projection is

\[
A_0=\frac{A_H}{4\pi D}.
\]

At \(A_H=1\) and \(D=3\),

\[
A_0
=\frac1{4\pi\cdot3}
=\frac1{12\pi}.
\]

The foundation and projection paths therefore agree exactly:

\[
\frac1{(2\pi)\alpha_HD}
=\frac{A_H}{4\pi D}
\quad\text{at}\quad
\alpha_H=2, A_H=1.
\]

### 4.3 Reverse check

Multiplying the projection by its declared denominator gives

\[
(4\pi D)A_0
=(4\pi\cdot3)\frac1{12\pi}
=1
=A_H.
\]

This reverse check is important because it exposes what the equality says: the
floor is the projected value of closure, not closure itself. Their numerical
relation does not erase their different domains.

### 4.4 Coupled product, kept in its own lane

The Courtroom projection also checks the coupled product. At the source packet,

\[
R=2\alpha_HD=12
\]

(which agrees with \(\alpha_H^2D\) because \(\alpha_H=2\)). Hence

\[
RA_0
=(2\alpha_HD)\frac{A_H}{4\pi D}
=\frac{A_H\alpha_H}{2\pi}
=\frac1\pi.
\]

That product is the input to a later cosmic-inventory operator. It is shown
here as an exact consequence and not promoted into this chapter's local-floor
question. The CR003@19 higher-dimensional table is an algebraic sensitivity
check under its declared coupled formula; its own scope warns that the
three-dimensional angular factor \(4\pi\) must not be asserted as the full solid
angle in arbitrary dimension.

## 5. Operator-dependent cancellation and retention

### 5.1 Pointwise total: retain the floor

For source lifts \(A_i\), the accumulated state is

\[
A_{\rm total}(\mathbf x)=A_0+\sum_i A_i(\mathbf x).
\]

The identity operator gives

\[
\mathcal I[A_{\rm total}]
=A_0+\sum_i A_i(\mathbf x).
\]

Nothing cancels. Saying that a later local observable does not display the
uniform term must never be rewritten as \(A_0=0\).

### 5.2 Local gradient: differentiate the floor to zero

Because \(A_0\) is spatially uniform,

\[
\nabla A_0=\mathbf0.
\]

Therefore

\[
\nabla A_{\rm total}
=\nabla A_0+\sum_i\nabla A_i
=\sum_i\nabla A_i.
\]

The floor is removed by the kernel of the gradient operator, not by a change
to the accumulated field. This is why `SAMA-D000004` can derive local
acceleration from the source lift while retaining \(A_0\) in the total account.

### 5.3 Shared endpoint difference: cancel the common term

For two endpoints in the same universal background,

\[
\begin{aligned}
\Delta A_{\rm total}
&=A_{\rm total}(\mathbf x_2)-A_{\rm total}(\mathbf x_1)\\
&=[A_0+A_{\rm lift}(\mathbf x_2)]
 -[A_0+A_{\rm lift}(\mathbf x_1)]\\
&=A_{\rm lift}(\mathbf x_2)-A_{\rm lift}(\mathbf x_1).
\end{aligned}
\]

The cancellation is algebraic and operator-specific. It does not establish a
new source-only ontology for \(A\).

### 5.4 Local photon road: do not manufacture a source delay

A local source-delay operator is declared on the source lift along a path,
not on an indefinitely repeated uniform floor. Its first-order form is

\[
T_A^\gamma[\Gamma]
=\frac1c\int_\Gamma A_s(\mathbf x)\,ds.
\]

Inserting \(A_0\) as a visible local source delay would change the question
from “what delay does this source produce?” to an undeclared global-baseline
road. The floor's universality does not authorize that operator substitution.

### 5.5 Global road and inventory: retain the declared floor combination

The global Volume I line-of-sight road is built from the finite combination

\[
A_0R=\frac1\pi,
\]

and the clean inventory likewise uses \(RA_0\). These operators are neither
local gradients nor shared endpoint differences. Their retention of the floor
is therefore consistent with its cancellation in the preceding local lanes.

### 5.6 Decision table

| Question | Input | Operator | Treatment of \(A_0\) |
|---|---|---|---|
| What is accumulated here? | \(A_0+\sum_iA_i\) | local value | Retained. |
| What local source acceleration is read? | source lift / total field | gradient, later scaled by \(c^2/2\) | Vanishes under \(\nabla A_0=0\). |
| How do two shared-background endpoints compare? | two total endpoint values | difference or lapse ratio | Common term cancels. |
| What is a local source photon delay? | \(A_s\) along \(\Gamma\) | route integral | Not inserted as a visible local source delay. |
| What is the global cosmological road amplitude? | \(A_0,R,z\) | declared line-of-sight map | Retained through \(A_0R\). |
| What is the clean cosmic inventory? | \(A_0,R\) | product \(RA_0\) | Retained and load-bearing. |

## 6. Universal-floor derivation and replay

### 6.1 The preserved discovery limitation

The owner-supplied chronology reaches farther back than the staged G-test
record: the relation itself predates the explicit naming of \(2\), \(3\) and
\(\pi\) as primitives. `G:G7@SAM-ARCHIVE` therefore marks one preserved
artifact stage in the later provenance program, not the origin date of the
equation.

`G:G7@SAM-ARCHIVE` is valuable precisely because it did not present the final
status retroactively. It committed to
\(A_0=1/(12\pi)\), compared consequences, and explicitly said that it had not
yet derived why the universal value should equal the inverse thermal/
dimensional product. It also preserved a successful bridge-term comparison
and a failed/tensioned cosmological lane in the same record. The \(+13.53\%\)
CMB \(\theta_\star\) offset belonged to that historical implementation and was
not erased when the foundation improved.

### 6.2 The theorem-pressure correction

`G:G356@SAM-ARCHIVE` asked what changed after \(D=3\) received stronger
derivational status. The answer was deliberately narrow:

- the numerical \(A_0\), \(\chi\) and \(RA_0\) values did not change;
- the \(D\) slot was tightened;
- the compact-cycle provenance remained open at that stage;
- downstream independence and theorem grade did not upgrade automatically.

Its seven wrong controls preserve these non-implications. That is a correction
to the dependency status, not a failed numerical retest.

### 6.3 Compact-cycle provenance

`G:G357@SAM-ARCHIVE` then separated the primitive phase period from several
tempting alternatives. Its phase residual is nonzero at \(\pi\), returns to
floating-point zero at \(2\pi\), and treats \(4\pi\) as a second cycle rather than
the primitive cycle. It rejects the identification of the cycle's two with
\(\alpha_H\), rejects a real exponential as the periodic object, and leaves the
action-scale magnitude and larger theory outside the result.

### 6.4 Independent selector and locked replay

[`CR:CR001@A0-a`](../../tests/courtroom/a0-a-h-d-cr001-foundation-selector-recertification/README.md) recertified the foundation without reading older G-test
outputs. Its candidate selector uniquely returned exchange count \(2\),
identity-support dimension \(3\), compact phase cycle \(2\pi\), and the
finite positive floor. [`LC:LC01`](../../tests/courtroom/16-the-last-campaign/README.md) then locked the value into the primitive
replay stack with the radix, carrier and retained sectors.

### 6.5 Independent projection result

[`CR:CR003@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr003-a-horizon-to-a0-angular-dimensional-projection-identity/README.md) evaluated three paths to \(A_0\):

\[
\frac1{4\pi\cdot3},\qquad
\frac1{12\pi},\qquad
\frac{A_H}{4\pi D}.
\]

All agreed with maximum recorded relative deviation \(0.000\times10^0\)
at tolerance \(10^{-12}\). The source records execution `CLEAN`, scientific
verdict `PASS`, and zero introduced free parameters. Its boundary is exact:
the executed projection does not by itself establish the larger completed-surface
Home conjecture or authorize an arbitrary-dimensional \(4\pi\) solid-angle claim.

## 7. Wrong controls and diagnostic alternatives

| Wrong control | Immediate consequence | Correction |
|---|---|---|
| Treat \(A_0\) as a fitted offset | Moves the value after observing a target and loses foundation provenance. | Derive it from the fixed primitive packet before the readout. |
| Identify the two numerical twos | Collapses phase-cycle provenance into arity. | Keep \(2\pi\) and \(\alpha_H=2\) as separately typed factors. |
| Derive \(D\), then declare all of \(A_0\) derived | Skips the compact-cycle dependency. | Preserve the G356 correction and G357 provenance step. |
| Remove the floor from \(A_{\rm total}\) because a gradient cancels it | Confuses the field with one operator's kernel. | Retain the pointwise term; show \(\nabla A_0=0\). |
| Insert \(A_0\) into every local photon road | Manufactures a visible uniform source delay. | Apply the declared local road to \(A_s\); use the separately declared global road when appropriate. |
| Equate \(A_H=1\) with \(A_0\) | Confuses local closure with its projection. | Preserve \(A_0=A_H/(4\pi D)\) and the distinct types. |
| Treat \(RA_0=1/\pi\) as local acceleration | Applies an inventory product to a gradient question. | Route the product only to its registered global operators. |
| Promote historical source wording to current authority | Makes an August source-era “latest” claim present-tense without live installation. | Use `SAM_LIVE/07_SAMA_CURRENT.md` for present status and preserve source-era chronology as provenance. |

## 8. Worked examples

### 8.1 Constant floor under a spatial derivative

Let one spherical lift be \(A_s(r)=k/r\). Then

\[
A_{\rm total}(r)=A_0+\frac kr.
\]

The radial derivative is

\[
\frac{dA_{\rm total}}{dr}
=\frac{dA_0}{dr}+\frac d{dr}\left(\frac kr\right)
=0-\frac{k}{r^2}.
\]

The total field still contains \(A_0\); the derivative readout does not.

### 8.2 Constant floor in an endpoint difference

At radii \(r_1\) and \(r_2\),

\[
\begin{aligned}
A_{\rm total}(r_2)-A_{\rm total}(r_1)
&=\left(A_0+\frac{k}{r_2}\right)
 -\left(A_0+\frac{k}{r_1}\right)\\
&=k\left(\frac1{r_2}-\frac1{r_1}\right).
\end{aligned}
\]

The cancellation follows from shared background and identical coefficient. It
would not license deleting a spatially varying background or a term that an
operator weights differently at the two endpoints.

### 8.3 Floor retained in the radix product

\[
RA_0
=12\left(\frac1{12\pi}\right)
=\frac1\pi
=0.3183098861837907\ldots.
\]

Here there is no subtraction or derivative. The same floor that disappears
from Examples 8.1 and 8.2 is load-bearing in this declared global product.

## 9. Established result, boundaries and forward handoff

The established source-bound statement is

\[
\boxed{
A_0
=\frac1{(2\pi)\alpha_HD}
=\frac1{\pi R}
=\frac{A_H}{4\pi D}
=\frac1{12\pi}
}
\]

at \(\alpha_H=2\), \(D=3\), \(R=12\), and \(A_H=1\). The
field-level statement is

\[
\boxed{A_{\rm total}=A_0+A_{\rm lift}},
\]

followed by an explicit operator that retains or cancels the constant term.

No SAMA result classification is assigned to this chapter. The registered
source `PASS` and `BOUNDARY` fields are preserved as source provenance rather
than translated. `SAMA-D000003` now receives the floor as the background term
for a spherical source lift. `SAMA-D000004` receives \(\nabla A_0=0\) for the
weak-field gradient. Later clock, photon-road, distance and inventory chapters
must each declare their own floor treatment.

Exact evidence is the complete six-key sequence in Section 10. The
specifically open boundary is not the numerical floor but the operator chosen
to read it in each later lane; no local, road or inventory observable is
licensed without that declared map.

## 10. Focused test and result index

| Exact qualified key | Evidence role | Preserved outcome | Direct result | Result folder |
|---|---|---|---|---|
| `G:G7@SAM-ARCHIVE` | Historical premise | Registry has no structured verdict; source preserves the initial commitment, bridge comparison and unresolved derivation/cosmology lanes. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G7_a0_from_first_principles/results/G7_a0_first_principles_summary.md) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G7_a0_from_first_principles/results) |
| `G:G356@SAM-ARCHIVE` | Dependency correction | `G356_A0_FOUNDATION_TIGHTENED_COMPACT_CYCLE_REMAINS` | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G356_a0_foundation_status_after_d_theorem/G356_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G356_a0_foundation_status_after_d_theorem) |
| `G:G357@SAM-ARCHIVE` | Compact-cycle premise | `G357_A0_COMPACT_CYCLE_PHASE_PROVENANCE_LOCKED` | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G357_a0_compact_cycle_phase_provenance/G357_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G357_a0_compact_cycle_phase_provenance) |
| [`CR:CR001@A0-a`](../../tests/courtroom/a0-a-h-d-cr001-foundation-selector-recertification/README.md) | Independent foundation retest | Structural packet recertified; source execution `CLEAN`, scientific verdict `BOUNDARY`. | [result](../../courtroom/A0-a_h-D/CR001_foundation_selector_recertification/CR001_result.md) | [folder](../../courtroom/A0-a_h-D/CR001_foundation_selector_recertification) |
| [`LC:LC01`](../../tests/courtroom/16-the-last-campaign/README.md) | Locked primitive replay | `LC01_PASS_LOCKED_PRIMITIVE_STACK_AND_REPLAY_REGISTER`; downstream lanes stay separate. | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN) |
| [`CR:CR003@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr003-a-horizon-to-a0-angular-dimensional-projection-identity/README.md) | Horizon-floor projection result | Source execution `CLEAN`, scientific verdict `PASS`; three paths agree with recorded zero deviation and zero new parameters. | [result](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR003_A_HORIZON_TO_A0_ANGULAR_DIMENSIONAL_PROJECTION_IDENTITY/CR003_result.md) | [folder](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR003_A_HORIZON_TO_A0_ANGULAR_DIMENSIONAL_PROJECTION_IDENTITY) |

## 11. Atomic record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000001-R001` | Defines the universal accumulation floor \(A_0=1/(12\pi)\). |
| `SAMA-C000030-R001` | Supplies \(R=12\) and its local thresholds. |
| `SAMA-C000033-R001` | Separates compact-cycle, primitive-arity and support factors. |
| `SAMA-C000034-R001` | Records the complete foundation derivation of \(A_0\). |
| `SAMA-C000035-R001` | Records the horizon-to-floor projection. |
| `SAMA-C000036-R001` | Types pointwise retention, gradient cancellation, endpoint cancellation and global retention. |
| `SAMA-C000122-R001` | Enforces the Volume I/II/III subject boundary. |
| `SAMA-C000124-R001` | Separates source-era chronology from current live authority. |
| `SAMA-C000125-R001` | Preserves source verdicts, authorized classifications and false approval state. |
| `SAMA-C000257-R001` | Anchors the recovered exact factorization and typed source provenance. |
| `SAMA-C000258-R001` | Records that the relation predates explicit primitive naming. |

## 12. Source and approval boundary

The direct test set is exactly the six qualified keys indexed above. The
separately registered branch-level derivation source supplies conceptual
genealogy and source provenance, not a seventh test. Courtroom links are
pinned to commit `b5e914f71377e86ef4c67e199973d9300795cda1`, and archive
links resolve to the locally hashed artifacts registered by SAMA.

`reviewed_and_approved` is `false`; `approval` is `null`. Neither the executed
projection nor document validation constitutes owner approval.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`CR:CR001@A0-a`](../../tests/courtroom/a0-a-h-d-cr001-foundation-selector-recertification/README.md) | [CR001_PRECOMMIT.md](../../courtroom/A0-a_h-D/CR001_foundation_selector_recertification/CR001_PRECOMMIT.md)<br>[CR001_declared_premises.json](../../courtroom/A0-a_h-D/CR001_foundation_selector_recertification/CR001_declared_premises.json) | [CR001_foundation_selector_recertification.py](../../courtroom/A0-a_h-D/CR001_foundation_selector_recertification/CR001_foundation_selector_recertification.py) | [CR001_candidate_rows.csv](../../courtroom/A0-a_h-D/CR001_foundation_selector_recertification/CR001_candidate_rows.csv)<br>[CR001_wrong_controls.csv](../../courtroom/A0-a_h-D/CR001_foundation_selector_recertification/CR001_wrong_controls.csv) | [CR001_result.md](../../courtroom/A0-a_h-D/CR001_foundation_selector_recertification/CR001_result.md)<br>[CR001_summary.json](../../courtroom/A0-a_h-D/CR001_foundation_selector_recertification/CR001_summary.json) | [All 9 files](../../tests/courtroom/a0-a-h-d-cr001-foundation-selector-recertification/README.md) |
| [`CR:CR003@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr003-a-horizon-to-a0-angular-dimensional-projection-identity/README.md) | [CR003_PRECOMMIT.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR003_A_HORIZON_TO_A0_ANGULAR_DIMENSIONAL_PROJECTION_IDENTITY/CR003_PRECOMMIT.md)<br>[CR003_declared_premises.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR003_A_HORIZON_TO_A0_ANGULAR_DIMENSIONAL_PROJECTION_IDENTITY/CR003_declared_premises.json) | [CR003_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR003_A_HORIZON_TO_A0_ANGULAR_DIMENSIONAL_PROJECTION_IDENTITY/CR003_runner.py) | [CR003_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR003_A_HORIZON_TO_A0_ANGULAR_DIMENSIONAL_PROJECTION_IDENTITY/CR003_runner.py)<br>[CR003_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR003_A_HORIZON_TO_A0_ANGULAR_DIMENSIONAL_PROJECTION_IDENTITY/CR003_result.md)<br>[CR003_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR003_A_HORIZON_TO_A0_ANGULAR_DIMENSIONAL_PROJECTION_IDENTITY/CR003_summary.json) | [CR003_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR003_A_HORIZON_TO_A0_ANGULAR_DIMENSIONAL_PROJECTION_IDENTITY/CR003_result.md)<br>[CR003_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR003_A_HORIZON_TO_A0_ANGULAR_DIMENSIONAL_PROJECTION_IDENTITY/CR003_summary.json) | [All 8 files](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr003-a-horizon-to-a0-angular-dimensional-projection-identity/README.md) |
| [`LC:LC01`](../../tests/courtroom/16-the-last-campaign/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign/README.md) | [LC01_primitive_stack_lock_runner.py](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_primitive_stack_lock_runner.py) | [LC01_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_wrong_controls.csv)<br>[LC01_wrong_controls.csv.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_wrong_controls.csv.sha256.txt) | [LC01_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_result.md)<br>[LC01_result.md.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_result.md.sha256.txt)<br>[LC01_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_summary.json)<br>[LC01_summary.json.sha256.txt](../../courtroom/16_THE_LAST_CAMPAIGN/LC01_summary.json.sha256.txt) | [All 164 files](../../tests/courtroom/16-the-last-campaign/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000002`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/UNIVERSAL_ACCUMULATION_FLOOR_A0.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000002 | Substrate Foundations | Universal Floor Provenance, Derivation, Projection and Operator Typing |

| Document field | Value |
|---|---|
| Purpose | Derive the universal accumulation floor from typed primitive factors, connect it to the horizon projection, and state exactly when local operators cancel or global operators retain it. |
| Prerequisite documents | `SAMA-D000001` |
| Used by | `SAMA-D000003`, `SAMA-D000011`, `SAMA-D000018`; assembled into `SAMA-P000002`. |
| Primary source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Recovered derivation source | [Courtroom `A0-a_h-D/README.md`](../../courtroom/A0-a_h-D/README.md), SHA-256 `809051264082265b49889094154787fe2026e8f7395d9e23d53c1795e651a671`. |
| Evidence registry | `index/registry/test_records.jsonl`, SHA-256 `8e1aeabc294f40d19793ff4db4f04e6fdac1b9617f113d5f32706167cde46302`. |
| Revision state | Source-bound draft; mechanically registered proposal; not reviewed or approved. |

</details>
