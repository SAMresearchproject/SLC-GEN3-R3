[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Horizon Closure and Thermal Readout

## Current research connections — 14 September 2026

The global execution authority is SLC-GEN3-R3 / SLC-GEN3-CEV1-R3. The September 2026 research includes exact retained-history computation, RH arithmetic compensation, native Mersenne work, Starbreaker signed reception and ATOM3D contact/grammar. The research index connects the retained derivations to the latest code, results and current domain assignments.

[Current derivations, code and results](../../../docs/RESEARCH.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

At unit closure, the accumulation coordinate reaches

\[
A(r_s)=1.
\]

The value alone is not a temperature. The thermal route begins with the
spatial gradient:

\[
\left|\frac{dA}{dr}\right|_{r_s}=\frac1{r_s}.
\]

The declared surface-gravity readout is

\[
\kappa_A
=\frac{c^2}{2}
\left|\nabla A\right|_{r_s}
=\frac{c^2}{2r_s}
=\frac{c^4}{4GM}.
\]

Only after a separate thermal conversion is applied does one obtain

\[
T_H
=\frac{\hbar\kappa_A}{2\pi c k_B}
=\frac{\hbar c^3}{8\pi GMk_B}.
\]

This chain keeps coordinate, gradient, acceleration and temperature in
different type slots. A parallel historical route counts four Planck-area
cells per horizon ledger entry, derives the entropy area law and, after a
correction to the pair premise, recovers the same temperature through an
energy-area-mass step. The two routes meet at the same closed form but retain
their different premises and unresolved continuation tasks.

## 1. Opening question and conceptual picture

This chapter asks:

> Can the unit-closure source profile be differentiated and converted into
> the registered nonrotating thermal packet from start to finish, while the
> entropy/pair discovery chain, its wrong selectors, the original boundary
> grades and the limits of the thermodynamic continuation all remain visible?

The conceptual picture is a typed ladder:

\[
A
\longrightarrow
\nabla A
\longrightarrow
\kappa_A
\longrightarrow
T_H.
\]

Beside it is a ledger ladder:

\[
\mathcal A_H
\longrightarrow
N_{\rm ledger}
\longrightarrow
S_H
\longrightarrow
\Delta\mathcal A_H,\Delta M,\Delta E
\longrightarrow
T_H.
\]

Here \(A\) is dimensionless accumulation, while \(\mathcal A_H\) is geometric
area. The distinct typography is load-bearing: identifying the two would
collapse a field coordinate into a surface measure.

## 2. Definitions, domains and units

| Quantity | Definition | Type | Units/domain |
|---|---|---|---|
| \(M\) | nonrotating spherical source mass | source input | kg |
| \(r_s\) | \(2GM/c^2\) | source length | m |
| \(A(r)\) | \(r_s/r\) | accumulation coordinate | dimensionless |
| \(\nabla A\) | spatial gradient of the coordinate | geometric differential | m\(^{-1}\) |
| \(\kappa_A\) | \((c^2/2)|\nabla A|_{r_s}\) | surface-gravity readout | m s\(^{-2}\) |
| \(T_H\) | \(\hbar\kappa_A/(2\pi ck_B)\) | horizon thermal conversion | K |
| \(\mathcal A_H\) | \(4\pi r_s^2\) | horizon surface area | m\(^2\) |
| \(\ell_P^2\) | \(\hbar G/c^3\) | Planck area | m\(^2\) |
| \(N_{\rm ledger}\) | \(\mathcal A_H/(4\ell_P^2)\) | source-era ledger count | dimensionless |
| \(S_H\) | \(k_BN_{\rm ledger}\) | entropy readout | J K\(^{-1}\) |
| \(\alpha_H\) | \(2\) in the source-era two-face channel packet | channel-count premise | dimensionless |

The gradient is evaluated from the exterior profile at the closure surface.
That does not turn exact \(A=1\) into an ordinary static launch point. The
thermal conversion consumes a boundary gradient; it does not consume a finite
photon route starting at closure.

## 3. Derive the unit-closure gradient

Begin with

\[
A(r)=\frac{r_s}{r}.
\]

Differentiate with respect to radius:

\[
\frac{dA}{dr}
=-\frac{r_s}{r^2}.
\]

The inward sign records that accumulation decreases outward. The magnitude is

\[
\left|\frac{dA}{dr}\right|
=\frac{r_s}{r^2}.
\]

At \(r=r_s\),

\[
\boxed{
\left|\frac{dA}{dr}\right|_{r_s}
=\frac{r_s}{r_s^2}
=\frac1{r_s}
}.
\]

The dimensions close:

\[
[A]=1,
\qquad
\left[\frac{dA}{dr}\right]=\mathrm{m}^{-1}.
\]

A uniform accumulation floor has zero local gradient. It may belong to the
total account, but it cannot generate this surface derivative.

## 4. Convert gradient to surface gravity

The source lineage fixes the readout coefficient \(c^2/2\). Applying it to the
closure gradient gives

\[
\kappa_A
=\frac{c^2}{2}
\left|\nabla A\right|_{r_s}
=\frac{c^2}{2r_s}.
\]

Now substitute

\[
r_s=\frac{2GM}{c^2}.
\]

Then

\[
\kappa_A
=\frac{c^2}
{2(2GM/c^2)}
=\boxed{\frac{c^4}{4GM}}.
\]

The inverse mass scaling is explicit:

\[
M\mapsto\lambda M
\quad\Longrightarrow\quad
\kappa_A\mapsto\frac{\kappa_A}{\lambda}.
\]

This is a surface-gravity readout at closure. It is connected to the
weak-field gradient operator by source lineage, but it is not an assertion
that a static weak-field acceleration formula remains an ordinary local force
at the horizon.

## 5. Convert surface gravity to temperature

Apply the declared horizon thermal conversion:

\[
T_H=\frac{\hbar\kappa_A}{2\pi c k_B}.
\]

Insert \(\kappa_A=c^4/(4GM)\):

\[
T_H
=\frac{\hbar}{2\pi c k_B}
\frac{c^4}{4GM}.
\]

Cancel one power of \(c\):

\[
\boxed{
T_H
=\frac{\hbar c^3}{8\pi GMk_B}
}.
\]

Again,

\[
T_H\propto M^{-1}.
\]

No entropy count, emission rate or spectral distribution was required for
this gradient-to-temperature route. Those are separate operators.

## 6. Derive the horizon area and entropy count

The nonrotating closure area is

\[
\mathcal A_H=4\pi r_s^2.
\]

Substitute \(r_s=2GM/c^2\):

\[
\mathcal A_H
=4\pi
\left(\frac{2GM}{c^2}\right)^2
=\boxed{\frac{16\pi G^2M^2}{c^4}}.
\]

The Planck area is

\[
\ell_P^2=\frac{\hbar G}{c^3}.
\]

The source-era four-cell ledger rule assigns one independent entry per
\(4\ell_P^2\):

\[
N_{\rm ledger}
=\frac{\mathcal A_H}{4\ell_P^2}.
\]

Substitute both expressions:

\[
N_{\rm ledger}
=\frac{16\pi G^2M^2/c^4}
{4\hbar G/c^3}.
\]

Cancel \(4\), one \(G\), and three powers of \(c\):

\[
\boxed{
N_{\rm ledger}
=\frac{4\pi GM^2}{\hbar c}
}.
\]

If each independent entry contributes \(k_B\) to the entropy count,

\[
\boxed{
S_H
=k_BN_{\rm ledger}
=\frac{k_B\mathcal A_H}{4\ell_P^2}
}.
\]

The algebraic area law and the structural explanation of the factor four are
different questions. The discovery chain below exists because the first
calculation was exact while the uniqueness of its two-by-two interpretation
was initially unresolved.

## 7. Unit-closure gradient and thermal route

### 7.1 G18: correct area count with an explicit premise gap

`G:G18@SAM-ARCHIVE` proposed

\[
\alpha
=
(\text{two-face factor }2)
\times
(\text{gravity-bridge factor }2)
=4.
\]

It then computed

\[
\frac{S_{\rm ledger}}{k_B}
=\frac{\mathcal A_H}{4\ell_P^2}
\]

for six mass scales. The ledger and comparator ratios were \(1.0000\)
throughout; examples include approximately
\(1.0494\times10^{77}\) for a \(1M_\odot\) source,
\(1.0494\times10^{79}\) for \(10M_\odot\), and
\(4.4338\times10^{96}\) for the source-era M87-class row.

The source itself preserved a gap: its two factors were structurally
plausible, but that execution did not establish that the decomposition was
forced or that the emission event had exactly the asserted pair structure.
Keeping that gap is essential to the correction chain.

### 7.2 G59: install the ledger-channel commitment

`G:G59@SAM-ARCHIVE` revisited the same factor after the source-era
ledger-channel/configuration-volume commitment. In its notation,

\[
\alpha_H=2
\]

is the two-face horizon channel count, and the gravity-bridge factor is already
load-bearing in

\[
A=\frac{2GM}{c^2r}.
\]

The source therefore promoted the decomposition within its declared
primitive packet:

\[
\alpha=\alpha_H\times2=4.
\]

It reproduced the same six entropy rows. The correction was conceptual rather
than numerical: G18's area-law values were retained, while the source-era
reason for the two factors was strengthened.

G59 still left the pair structure and complete radiation spectrum open.

### 7.3 G60: elevator correction of the pair premise

`G:G60@SAM-ARCHIVE` supplied the source-era elevator argument. An outward
emission and the corresponding source-mass decrease are two faces of one
event:

\[
\Delta M=-\frac{\Delta E}{c^2}.
\]

The horizon area depends on mass:

\[
\mathcal A_H(M)
=\frac{16\pi G^2M^2}{c^4}.
\]

Differentiate:

\[
\frac{d\mathcal A_H}{dM}
=\frac{32\pi G^2M}{c^4}.
\]

One four-cell ledger step has magnitude

\[
|\Delta\mathcal A_H|=4\ell_P^2.
\]

Use

\[
|\Delta M|=\frac{\Delta E}{c^2}.
\]

To first order,

\[
4\ell_P^2
=\frac{32\pi G^2M}{c^4}
\frac{\Delta E}{c^2}.
\]

Solve for the event energy:

\[
\Delta E
=\frac{4\ell_P^2c^6}{32\pi G^2M}.
\]

Insert \(\ell_P^2=\hbar G/c^3\):

\[
\Delta E
=\frac{4(\hbar G/c^3)c^6}
{32\pi G^2M}
=\boxed{\frac{\hbar c^3}{8\pi GM}}.
\]

With \(\Delta E=k_BT\), this becomes

\[
\boxed{
T=\frac{\hbar c^3}{8\pi GMk_B}
},
\]

identical to the independently derived surface-gradient temperature.

The correction closes the source-era pair premise under its declared
no-interior, mass-conservation and two-face commitments. It still imports a
separate luminosity law when an absolute emission rate is calculated, and it
does not supply greybody factors or a complete spectrum.

### 7.4 G260: broad pair-write hypothesis retained as source history

`G:G260@SAM-ARCHIVE` tested the source-era equation

\[
P(\text{event})
=\left|
\sum_{i=1}^{\alpha_H}\psi_i
\right|^2,
\qquad
\alpha_H=2,
\]

across a double-slit/Hawking pair-write hypothesis. Its source artifact records
seven of seven internal probes and the source label
`G260_DOUBLE_SLIT_HAWKING_UNIFICATION_VERIFIED`.

That label is preserved as historical provenance. This document does not
convert it into a SAMA result classification and does not treat a broad
cross-phenomenon interpretation as a hidden premise of the narrower
gradient-to-temperature identity. The thermal derivation above stands on its
registered operators even when the larger unification hypothesis is held at
its source-era boundary.

### 7.5 G294: entropy alone is the wrong selector

`G:G294@SAM-ARCHIVE` asked whether horizon entropy selects a ledger-local
connection. It first replayed \(\alpha=4\) with zero ledger/Bekenstein-Hawking
ratio error. Then it applied diagnostic controls.

A generic \(U(4)\) transformation preserved total von Neumann entropy but
changed the face weights:

\[
(0.7,0.3)
\longrightarrow
(0.622101879979,\ 0.377898120021).
\]

The maximum face-weight change was \(0.077898120021\), so entropy preservation
alone was too weak.

Requiring two-face distinguishability selected the block-preserving algebra:

\[
\dim u(4)=16,
\]

\[
\dim[u(2)_{\rm outer}\oplus u(2)_{\rm inner}]=8,
\]

with determinant-one block dimension \(7\). The block face leakage was zero,
whereas generic face leakage was about \(1.200737746368\).

The source verdict is
`G294_GATE8_HORIZON_ENTROPY_SELECTOR_VERIFIED`, with seven of seven predictions
and seven of seven wrong controls. Its scope note is equally important: this
selector does not derive the Standard Model gauge group or close its broader
gate.

The deviation teaches a general rule: a scalar entropy equality cannot replace
the typed relational structure the test intends to select.

## 8. Keep the thermal types separate

The complete conversion is

\[
A
\xrightarrow{\nabla}
\frac1{\mathrm{length}}
\xrightarrow{c^2/2}
\frac{\mathrm{length}}{\mathrm{time}^2}
\xrightarrow{\hbar/(2\pi ck_B)}
\mathrm{temperature}.
\]

Each arrow contributes dimensions and premises.

| Substitution error | Why it fails |
|---|---|
| \(A=T\) | A dimensionless coordinate is equated with kelvin. |
| \(\nabla A=T\) | An inverse-length gradient omits both conversion operators. |
| \(\kappa_A=A\) | A surface acceleration is collapsed into its source coordinate. |
| \(T_H=\) emission rate | Temperature does not supply luminosity, species or greybody transmission. |
| \(S_H=T_H\) | Entropy and temperature are different thermodynamic readouts with different units. |
| \(A=1=\) ordinary photon start | The static lapse and exterior road forbid a regular launch from exact closure. |

## 9. Strong-field dependency zipper

The four focused predecessors provide separate members:

| Dependency | Registered member |
|---|---|
| `SAMA-D000013` | \((A_H,A_{\rm ph},A_{\rm ISCO})=(1,2/3,1/3)\) |
| `SAMA-D000014` | exact lapse, redshift and logarithmic exterior road |
| `SAMA-D000015` | photon critical impact and shadow diameter |
| `SAMA-D000016` | timelike ISCO energy, angular momentum and frequency |
| this chapter | closure gradient, surface gravity, temperature and scoped entropy continuation |

The zipper is a dependency graph. It does not turn each member into the same
equation and it does not authorize a later record to overwrite an earlier
source verdict.

## 10. Strong-field zipper and locked replay

### 10.1 CR007 root

[`CR:CR007@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr007-strong-field-landmark-selector/README.md) establishes the exact mass-invariant landmark tuple with zero
free parameters. Its execution is `CLEAN` and its scientific verdict is
`BOUNDARY`. The grade is preserved because the sealed root did not claim broad
external closure.

### 10.2 CR008 boundary

[`CR:CR008@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr008-clock-traversal-closure/README.md) attaches the exact lapse, redshift and outside-ledger radial road.
It records zero lapse, divergent redshift and logarithmic traversal as
\(A\to1^-\). Its execution is `CLEAN` and its scientific verdict is also
`BOUNDARY`.

The later photon and ISCO documents supply the distinct downstream contact
members. They do not change these original fields.

### 10.3 CR011 deferred-support readback

[`CR:CR011@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr011-deferred-support-zipper/README.md) reads the branch dependency graph after the photon and ISCO
members exist. Its source execution is `CLEAN` and scientific verdict is
`PASS`. It appends scoped appeal readouts for the earlier root and closure
boundary while recording:

\[
\text{original grades preserved}=\mathrm{true}.
\]

This is the promotion pattern embodied by the zipper:

1. preserve the original boundary record;
2. add independently scoped downstream evidence;
3. write a successor readback;
4. leave the predecessor artifact unchanged.

### 10.4 LC11 locked-stack replay

[`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) restarts from

\[
R=12,\qquad D=3,\qquad \alpha_H=2
\]

and the sealed \(A\)-kernel. It reproduces:

- \(A_H=1\), \(A_{\rm ph}=2/3\), \(A_{\rm ISCO}=1/3\);
- the near-horizon lapse and redshift row;
- \(b_{\rm crit}/r_s=2.5980762113533156\);
- \(d_{\rm sh}/r_s=5.196152422706631\);
- the exact ISCO energy, angular momentum and frequency packet.

It also retains:

- \(A=1\) as no completed parent-ledger crossing and no literal photon launch;
- the original `BOUNDARY` grades;
- the source-era functional-form debt it names;
- the open greybody, species, rate, spectrum, correlation and endpoint work.

The replay records 100/100 checks and rejects 8/8 wrong controls.

## 11. Deviation chains and wrong controls

| Wrong or diagnostic route | Failure produced | Correction or boundary |
|---|---|---|
| Use \(A(r_s)=1\) directly as temperature | Omits the gradient, acceleration and thermal conversions and is dimensionally invalid. | Follow \(A\to\nabla A\to\kappa_A\to T_H\). |
| Add the uniform floor to the local gradient | A constant has zero gradient; the extra term is spurious. | Differentiate the source lift. |
| Drop the factor \(1/2\) in \(\kappa_A\) | Doubles the thermal readout. | Retain the registered \(c^2/2\) coefficient. |
| Treat exact \(A=1\) as a finite photon launch | The static lapse is zero and the exterior road diverges. | Evaluate the gradient at the boundary without launching an ordinary path there. |
| Claim G18 forced the two-by-two structure | G18 itself preserved the uniqueness and pair-premise gaps. | Keep G18, then add G59 and G60 as corrections. |
| Erase G18 after G59/G60 | Removes the discovery chain and the reason later premises were required. | Preserve all three source records. |
| Use scalar entropy preservation as a connection selector | G294 shows generic \(U(4)\) can preserve entropy while mixing face weights. | Require the declared two-face block structure. |
| Read the G294 block dimension as the Standard Model | The source explicitly records that the gauge group and broader gate remain open. | Keep the selector scoped. |
| Promote G260's broad source label into a SAMA classification | Conflates historical internal status with authorized current result language. | Preserve the source label and assign no new classification to that row. |
| Derive absolute emission rate from \(T_H\) alone | Rate requires an additional luminosity law; spectrum requires further physics. | Keep rate, species, greybody and endpoint tasks open. |
| Overwrite CR007/CR008 after downstream contact | Destroys the original sealed `BOUNDARY` records. | Append the CR011 readback and retain predecessor grades. |
| Extend the zipper to Kerr or full strong-field closure | The registered chain is nonrotating and externally scoped. | Route rotating geometry and full observables to separate successors. |

## 12. Evidence sequence and status ledger

| Sequence | Exact qualified key | Role | Preserved result or boundary |
|---:|---|---|---|
| 1 | `G:G18@SAM-ARCHIVE` | construction with preserved gap | Exact four-cell entropy count; uniqueness and pair premises initially open. |
| 2 | `G:G59@SAM-ARCHIVE` | boundary/correction | Ledger-channel commitment strengthens the factor-four derivation while leaving pair and spectrum work. |
| 3 | `G:G60@SAM-ARCHIVE` | construction/correction | Elevator argument supplies the pair step and independently recovers \(T_H\). |
| 4 | `G:G260@SAM-ARCHIVE` | source-era premise | Seven-probe broad pair-write hypothesis retained without a new SAMA classification. |
| 5 | `G:G294@SAM-ARCHIVE` | selector result | Entropy-only control rejected; block-preserving two-face connection selected with broader gauge boundary. |
| 6 | [`CR:CR007@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr007-strong-field-landmark-selector/README.md) | landmark premise | Exact tuple; source `CLEAN`/`BOUNDARY`. |
| 7 | [`CR:CR008@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr008-clock-traversal-closure/README.md) | closure boundary | Exact lapse and road closure; source `CLEAN`/`BOUNDARY`. |
| 8 | [`CR:CR011@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr011-deferred-support-zipper/README.md) | successor readback | Scoped deferred-support zipper; source `CLEAN`/`PASS`; originals preserved. |
| 9 | [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | locked retest | Complete nonrotating replay, 100/100 checks, 8/8 control rejections and scoped classification. |

The table has two chains. The first develops thermal and entropy structure.
The second assembles the nonrotating exterior dependency zipper. Their joint
appearance in one chapter does not erase their different source histories.

## 13. Established result, open boundary and forward handoff

The compression-safe thermal route is

\[
\boxed{
\left|\nabla A\right|_{r_s}
=\frac1{r_s},
\qquad
\kappa_A
=\frac{c^2}{2r_s}
=\frac{c^4}{4GM},
\qquad
T_H
=\frac{\hbar c^3}{8\pi GMk_B}
}.
\]

The parallel source-era entropy route is

\[
\boxed{
\mathcal A_H=4\pi r_s^2,
\qquad
\frac{S_H}{k_B}
=\frac{\mathcal A_H}{4\ell_P^2}
}.
\]

For the declared nonrotating exterior chain replayed by [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md):

**The test result suggests strong contact with the concept.**

The classification does not rewrite the `BOUNDARY` fields of
[`CR:CR007@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr007-strong-field-landmark-selector/README.md) or [`CR:CR008@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr008-clock-traversal-closure/README.md). It does not classify a full Hawking spectrum,
absolute emission rate, species inventory, greybody factors, endpoint
evolution, Kerr solution, EHT image or complete strong-field metric.

The strong-field chapter now hands the mass-scaled thermal and closure packet
forward to the Volume I synthesis. Matter grammar remains a typed source-side
dependency, and executable simulation remains outside this document.

## 14. Focused test and result index

| Exact qualified key | Evidence role | Preserved outcome | Direct result | Result folder |
|---|---|---|---|---|
| `G:G18@SAM-ARCHIVE` | Entropy construction | Direct \(S_H/k_B=\mathcal A_H/(4\ell_P^2)\) count across six masses, with the original structural-premise gap retained. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G18_entropy_from_ledger_counting/results/G18_entropy_from_ledger_counting_summary.md) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G18_entropy_from_ledger_counting) |
| `G:G59@SAM-ARCHIVE` | Ledger-channel correction | Same numerical area law under the source-era \(\alpha_H=2\) channel commitment; spectrum remains open. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G59_entropy_under_ledger_channel/results/G59_entropy_under_ledger_channel_summary.md) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G59_entropy_under_ledger_channel) |
| `G:G60@SAM-ARCHIVE` | Pair-structure correction | Elevator argument and independent energy-area derivation of the registered temperature; absolute rate and spectrum remain separate. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G60_pair_structure_from_elevator/results/G60_pair_structure_from_elevator_summary.md) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G60_pair_structure_from_elevator) |
| `G:G260@SAM-ARCHIVE` | Historical premise | Source label `G260_DOUBLE_SLIT_HAWKING_UNIFICATION_VERIFIED` and 7/7 internal probes; no SAMA classification added. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G260_double_slit_hawking_unification/results/G260_summary.md) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G260_double_slit_hawking_unification) |
| `G:G294@SAM-ARCHIVE` | Selector result | `G294_GATE8_HORIZON_ENTROPY_SELECTOR_VERIFIED`; 7/7 predictions, 7/7 controls, \(u(2)\oplus u(2)\) selector and explicit non-SM boundary. | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G294_horizon_entropy_selector/G294_output.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G294_horizon_entropy_selector) |
| [`CR:CR007@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr007-strong-field-landmark-selector/README.md) | Landmark premise | Source execution `CLEAN`, scientific verdict `BOUNDARY`; exact ordered tuple and mass invariance. | [result](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR/CR007_result.md) | [folder](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR) |
| [`CR:CR008@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr008-clock-traversal-closure/README.md) | Closure boundary | Source execution `CLEAN`, scientific verdict `BOUNDARY`; zero lapse, divergent redshift and logarithmic road. | [result](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_result.md) | [folder](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE) |
| [`CR:CR011@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr011-deferred-support-zipper/README.md) | Deferred-support result | Source execution `CLEAN`, scientific verdict `PASS`; appended appeal readbacks with original grades preserved. | [result](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR011_DEFERRED_SUPPORT_ZIPPER/CR011_result.md) | [folder](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR011_DEFERRED_SUPPORT_ZIPPER) |
| [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | Locked-stack retest | `LC11_PASS_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY_FROM_LOCKED_PRIMITIVE_STACK`; 100/100 checks and 8/8 wrong controls. **The test result suggests strong contact with the concept.** | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY) |

## 15. Atomic record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000043-R001` | Supplies the source-lineage \(c^2/2\) gradient readout coefficient and constant-floor cancellation. |
| `SAMA-C000075-R001` | Supplies the ordered nonrotating landmark tuple. |
| `SAMA-C000079-R001` | Records executable logarithmic exterior closure. |
| `SAMA-C000083-R001` | Supplies the photon-sphere/shadow contact member. |
| `SAMA-C000086-R001` | Supplies the ISCO orbital contact member. |
| `SAMA-C000087-R001` | Defines the unit-closure gradient \(1/r_s\). |
| `SAMA-C000088-R001` | Defines the surface-gravity and thermal conversion chain. |
| `SAMA-C000089-R001` | Preserves the open thermodynamic continuation. |
| `SAMA-C000090-R001` | Records the deferred-support zipper, locked replay and scoped classification. |
| `SAMA-C000122-R001` | Enforces the Volume I and cross-volume subject boundary. |
| `SAMA-C000124-R001` | Separates source-era chronology from current authority. |
| `SAMA-C000125-R001` | Preserves source statuses, classification and false approval state. |

## 16. Source chronology and approval boundary

The nine exact evidence keys above are individually registered. G18, G59,
G60, G260 and G294 retain their source-era progression and internal labels.
They are not silently installed as new present-tense authority. Courtroom and
Last Campaign links are pinned to commit
`b5e914f71377e86ef4c67e199973d9300795cda1`.

Executable artifacts control their numerical results. Active `SAM_LIVE`
documents control present-tense interpretation. This chapter owns the
substrate closure coordinate and typed thermal readout. Particle or isotope
grammar remains Volume II; executable emission, image or simulation machinery
remains Volume III.

`reviewed_and_approved` remains `false`; `approval` remains `null`. Source
fidelity, exact derivations, source `PASS`/`BOUNDARY` fields, mechanical
validation and the strong-contact classification do not constitute owner
approval.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`CR:CR007@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr007-strong-field-landmark-selector/README.md) | [CR007_PRECOMMIT.md](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR/CR007_PRECOMMIT.md)<br>[CR007_declared_premises.json](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR/CR007_declared_premises.json) | [CR007_runner.py](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR/CR007_runner.py) | [CR007_candidate_rows.csv](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR/CR007_candidate_rows.csv) | [CR007_candidate_summary.csv](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR/CR007_candidate_summary.csv)<br>[CR007_result.md](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR/CR007_result.md)<br>[CR007_summary.json](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR007_STRONG_FIELD_LANDMARK_SELECTOR/CR007_summary.json) | [All 10 files](../../tests/courtroom/05-strong-field-and-horizon-closure-cr007-strong-field-landmark-selector/README.md) |
| [`CR:CR008@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr008-clock-traversal-closure/README.md) | [CR008_PRECOMMIT.md](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_PRECOMMIT.md)<br>[CR008_declared_premises.json](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_declared_premises.json) | [CR008_runner.py](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_runner.py) | [CR008_runner.py](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_runner.py)<br>[CR008_candidate_summary.csv](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_candidate_summary.csv)<br>[CR008_result.md](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_result.md)<br>[CR008_summary.json](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_summary.json) | [CR008_candidate_summary.csv](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_candidate_summary.csv)<br>[CR008_result.md](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_result.md)<br>[CR008_summary.json](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR008_CLOCK_TRAVERSAL_CLOSURE/CR008_summary.json) | [All 11 files](../../tests/courtroom/05-strong-field-and-horizon-closure-cr008-clock-traversal-closure/README.md) |
| [`CR:CR011@05`](../../tests/courtroom/05-strong-field-and-horizon-closure-cr011-deferred-support-zipper/README.md) | [CR011_PRECOMMIT.md](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR011_DEFERRED_SUPPORT_ZIPPER/CR011_PRECOMMIT.md)<br>[CR011_declared_premises.json](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR011_DEFERRED_SUPPORT_ZIPPER/CR011_declared_premises.json) | [CR011_runner.py](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR011_DEFERRED_SUPPORT_ZIPPER/CR011_runner.py) | [CR011_runner.py](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR011_DEFERRED_SUPPORT_ZIPPER/CR011_runner.py)<br>[CR011_result.md](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR011_DEFERRED_SUPPORT_ZIPPER/CR011_result.md)<br>[CR011_summary.json](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR011_DEFERRED_SUPPORT_ZIPPER/CR011_summary.json) | [CR011_result.md](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR011_DEFERRED_SUPPORT_ZIPPER/CR011_result.md)<br>[CR011_summary.json](../../courtroom/05_STRONG_FIELD_AND_HORIZON_CLOSURE/CR011_DEFERRED_SUPPORT_ZIPPER/CR011_summary.json) | [All 9 files](../../tests/courtroom/05-strong-field-and-horizon-closure-cr011-deferred-support-zipper/README.md) |
| [`LC:LC11`](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) | [LC11_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_wrong_controls.csv) | [LC11_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_result.md)<br>[LC11_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC11_BLACK_HOLE_HORIZON_THERMODYNAMIC_REPLAY/LC11_summary.json) | [All 11 files](../../tests/courtroom/16-the-last-campaign-lc11-black-hole-horizon-thermodynamic-replay/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000017`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/HORIZON_CLOSURE_AND_THERMAL_READOUT.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000017 | Strong-Field Closure | Unit-Closure Gradient, Thermal Conversion and Strong-Field Zipper |

| Document field | Value |
|---|---|
| Purpose | Carry the \(A=1\) source gradient through the surface-gravity and thermal conversions, preserve the entropy/pair/selector discovery chain with its failures and corrections, and assemble the nonrotating landmark, lapse, road, shadow and ISCO zipper without rewriting predecessors. |
| Prerequisite documents | `SAMA-D000013`, `SAMA-D000014`, `SAMA-D000015`, `SAMA-D000016` |
| Used by | Focused child of `SAMA-P000002`. |
| Primary source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`, SHA-256 `2f22500f6583f567e350974610f00142e89b081a5b8c4c90c6dfe89bec43be0d`. |
| Revision state | Source-bound draft; mechanically registered proposal; not reviewed or approved. |

</details>
