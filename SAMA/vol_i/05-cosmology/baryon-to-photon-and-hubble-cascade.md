[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Baryon-to-Photon and Hubble Cascade

## Conceptual abstract

The clean inventory of `SAMA-D000018` is dimensionless. A conventional
Hubble constant is dimensional. This chapter makes every bridge between those
types visible.

The native side begins with the closed substrate containers:

\[
\eta_{\rm SAM}
=\frac{M}{\alpha_H^2\Theta}
A_0^{\mathcal L/\mathcal V}.
\]

The container ratios reduce independently,

\[
\frac{M}{\alpha_H^2\Theta}=\frac74,
\qquad
\frac{\mathcal L}{\mathcal V}=6,
\]

so the baryon-to-photon identity is

\[
\eta_{\rm SAM}=\frac74A_0^6
=6.0960895244842\times10^{-10}.
\]

The dimensional side begins with measured \(T_{\rm CMB}\), the blackbody
photon number density, exact SI constants and declared CODATA quantities. It
constructs

\[
K(T)=\frac{\rho_{\rm crit,100}}{m_pn_\gamma(T)},
\qquad
\omega_b=\frac{\eta_{\rm SAM}}{K},
\qquad
h^2=\frac{\omega_b}{\Omega_b},
\qquad
H_0=100h\ \mathrm{km\,s^{-1}\,Mpc^{-1}}.
\]

The endpoint is \(H_0=67.2503751950\)
\(\mathrm{km\,s^{-1}\,Mpc^{-1}}\). Calling it a substrate-derived cascade
does not mean the measured temperature or SI conversion constants were
derived by SAM. Conversely, disclosing those adapters does not turn \(\eta\)
or \(\Omega_b\) into fitted catalog values. The type boundary is the result.

## 1. Opening question and conceptual picture

This chapter asks:

> How does a finite substrate-container identity become a conventional
> present-day Hubble scale, step by step, without concealing measured thermal
> inputs, confusing \(\Omega_b\) with \(\omega_b\), or selecting \(H_0\) from
> the spectrum it will later be used to compute?

The cascade has two visibly different halves:

\[
\underbrace{
(M,\alpha_H,\Theta,\mathcal L,\mathcal V,A_0)
\longrightarrow\eta_{\rm SAM}
}_{\text{substrate identity}}
\]

and

\[
\underbrace{
T_{\rm CMB},\mathrm{SI},\mathrm{CODATA}
\longrightarrow n_\gamma,\rho_{\rm crit,100},K
\longrightarrow\omega_b,h,H_0
}_{\text{dimensional adapter}}.
\]

The clean baryon fraction \(\Omega_b\) joins those halves at the conversion
from physical density to dimensionless Hubble parameter. Nothing downstream
is allowed to reach back and tune \(\eta\), \(K\), or \(\Omega_b\).

## 2. Definitions, domains, units and symbol disambiguation

| Symbol | Definition | Type | Units/domain |
|---|---|---|---|
| \(A_0\) | \(1/(12\pi)\) | universal accumulation floor | dimensionless |
| \(M\) | \(R^2-\Theta=126\) | retained substrate sector | dimensionless count |
| \(\alpha_H\) | \(2\) | primitive arity | dimensionless integer |
| \(\Theta\) | \(18\) | tensor carrier | dimensionless count |
| \(\mathcal L\) | \(162\) | closed ledger container | dimensionless count |
| \(\mathcal V\) | \(D^3=27\) | volume container | dimensionless count |
| \(\eta\) | \(n_b/n_\gamma\) | baryon-to-photon number ratio | dimensionless |
| \(T_{\rm CMB}\) | \(2.7255\ \mathrm K\) in the registered execution | measured thermal anchor | K |
| \(n_\gamma\) | blackbody photon number density | external physical adapter | m\(^{-3}\) |
| \(H_{100}\) | \(100\ \mathrm{km\,s^{-1}\,Mpc^{-1}}\) | conventional reference rate | s\(^{-1}\) after conversion |
| \(\rho_{\rm crit,100}\) | \(3H_{100}^2/(8\pi G)\) | critical density at \(h=1\) | kg m\(^{-3}\) |
| \(K(T)\) | \(\rho_{\rm crit,100}/[m_pn_\gamma(T)]\) | eta-to-density conversion | dimensionless |
| \(\Omega_b\) | \(\rho_b/\rho_{\rm crit,0}\) | baryon fraction at the emitted \(H_0\) | dimensionless |
| \(\omega_b\) | \(\Omega_bh^2=\rho_b/\rho_{\rm crit,100}\) | physical baryon-density parameter | dimensionless |
| \(h\) | \(H_0/(100\ \mathrm{km\,s^{-1}\,Mpc^{-1}})\) | dimensionless Hubble parameter | dimensionless |
| \(h_{\rm P}\) | Planck constant | external SI constant | J s |
| \(\hbar\) | \(h_{\rm P}/(2\pi)\) | reduced Planck constant | J s |

The notation \(h\) is reserved here for the dimensionless Hubble parameter;
\(h_{\rm P}\) denotes Planck's constant. This prevents a common symbol from
silently crossing physical types.

## 3. Derive the substrate baryon-to-photon identity

### 3.1 Start from the registered container relation

The source relation is

\[
\eta_{\rm SAM}
=\frac{M}{\alpha_H^2\Theta}
A_0^{\mathcal L/\mathcal V}.
\]

Every factor is dimensionless, so the result has the correct type for a number
ratio. The prefactor compares the retained sector with the squared primitive
arity acting on the carrier. The exponent compares the closed ledger with the
volume container.

### 3.2 Reduce the prefactor without skipping cancellation

Insert \(M=126\), \(\alpha_H=2\), and \(\Theta=18\):

\[
\frac{M}{\alpha_H^2\Theta}
=\frac{126}{2^2\cdot18}.
\]

Evaluate the denominator:

\[
2^2\cdot18=4\cdot18=72.
\]

Thus

\[
\frac{126}{72}.
\]

Divide numerator and denominator by \(18\):

\[
\boxed{
\frac{M}{\alpha_H^2\Theta}=\frac74
}.
\]

The ratio exposes the same seven-retained to one-carrier split encoded in
\(M=7\Theta\), but it does not promote \(\Theta\) into matter.

### 3.3 Reduce the exponent

Insert \(\mathcal L=162\) and \(\mathcal V=27\):

\[
\frac{\mathcal L}{\mathcal V}
=\frac{162}{27}
=6.
\]

The source execution also checks the coincident structural identifications

\[
\alpha_HD=2\cdot3=6,
\]

\[
\frac R2=\frac{12}{2}=6,
\]

\[
\frac\Theta D=\frac{18}{3}=6,
\]

\[
\frac{\mathcal L}{\mathcal V}=\frac{162}{27}=6.
\]

These are explicit container identities. The exponent in this equation is
specifically \(\mathcal L/\mathcal V\); the other equal forms are integrity
checks, not independent fitted exponents.

### 3.4 Substitute the universal floor

The relation becomes

\[
\eta_{\rm SAM}=\frac74A_0^6.
\]

With \(A_0=1/(12\pi)\),

\[
A_0^6
=\left(\frac1{12\pi}\right)^6
=\frac1{(12\pi)^6}.
\]

Therefore

\[
\boxed{
\eta_{\rm SAM}
=\frac7{4(12\pi)^6}
}
=6.0960895244842\times10^{-10}.
\]

[`CR:CR036@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036-eta-sam-and-h0-selector/README.md) evaluated the container form and the reduced closed form
independently in code. Their relative difference was
\(1.696\times10^{-16}\), an implementation-integrity check on the
substitution rather than a new science gate.

## 4. Derive blackbody photon number density

### 4.1 Begin with the two-polarization phase-space count

For a photon gas at temperature \(T\), the occupation number for momentum
magnitude \(p\) is

\[
f(p)=\frac1{\exp(pc/k_BT)-1}.
\]

There are two photon polarizations. The number density is therefore

\[
n_\gamma(T)
=\frac{2}{(2\pi\hbar)^3}
\int_{\mathbb R^3}f(|\mathbf p|)\,d^3p.
\]

Spherical momentum coordinates give \(d^3p=4\pi p^2dp\), hence

\[
n_\gamma(T)
=\frac{8\pi}{8\pi^3\hbar^3}
\int_0^\infty
\frac{p^2}{\exp(pc/k_BT)-1}\,dp.
\]

Cancel the common factor:

\[
n_\gamma(T)
=\frac1{\pi^2\hbar^3}
\int_0^\infty
\frac{p^2}{\exp(pc/k_BT)-1}\,dp.
\]

### 4.2 Nondimensionalize the integral

Set

\[
x=\frac{pc}{k_BT}.
\]

Then

\[
p=\frac{k_BT}{c}x,
\qquad
dp=\frac{k_BT}{c}\,dx,
\]

so

\[
p^2dp
=\left(\frac{k_BT}{c}\right)^3x^2dx.
\]

Substitution yields

\[
n_\gamma(T)
=\frac1{\pi^2\hbar^3}
\left(\frac{k_BT}{c}\right)^3
\int_0^\infty\frac{x^2}{e^x-1}\,dx.
\]

Using the Bose integral

\[
\int_0^\infty\frac{x^2}{e^x-1}\,dx=2\zeta(3),
\]

one obtains

\[
\boxed{
n_\gamma(T)
=\frac{2\zeta(3)}{\pi^2}
\left(\frac{k_BT}{\hbar c}\right)^3
}.
\]

The dimensions close because \(k_BT/(\hbar c)\) has units of inverse length.
Cubing it produces m\(^{-3}\). At \(T_{\rm CMB}=2.7255\ \mathrm K\), the
registered execution reports

\[
n_\gamma=4.1072684792\times10^8\ \mathrm{m^{-3}}.
\]

This is the first explicit external-input step. The temperature is measured;
the photon-density formula is standard blackbody physics.

## 5. Build the eta-to-density conversion

### 5.1 Convert the reference Hubble rate to SI

Define

\[
H_{100}=100\ \mathrm{km\,s^{-1}\,Mpc^{-1}}.
\]

Using \(1\ \mathrm{km}=10^3\ \mathrm m\) and
\(1\ \mathrm{Mpc}=3.0856775815\times10^{22}\ \mathrm m\),

\[
H_{100}
=\frac{100\times10^3\ \mathrm{m\,s^{-1}}}
{3.0856775815\times10^{22}\ \mathrm m}.
\]

Meters cancel, giving

\[
\boxed{H_{100}=3.2407792894\times10^{-18}\ \mathrm{s^{-1}}}.
\]

### 5.2 Compute critical density at \(h=1\)

The critical-density adapter is

\[
\rho_{\rm crit,100}=\frac{3H_{100}^2}{8\pi G}.
\]

Its units are

\[
\frac{\mathrm{s^{-2}}}
{\mathrm{m^3\,kg^{-1}\,s^{-2}}}
=\mathrm{kg\,m^{-3}},
\]

as required for a mass density. With the declared CODATA \(G\),

\[
\boxed{
\rho_{\rm crit,100}
=1.8783416169\times10^{-26}\ \mathrm{kg\,m^{-3}}
}.
\]

### 5.3 Relate number ratio to physical baryon density

By definition,

\[
\eta=\frac{n_b}{n_\gamma},
\]

so

\[
n_b=\eta n_\gamma.
\]

Under the proton-mass conversion used by the registered runner,

\[
\rho_b=m_pn_b=m_p\eta n_\gamma.
\]

The physical baryon-density parameter is

\[
\omega_b=\frac{\rho_b}{\rho_{\rm crit,100}}.
\]

Substituting \(\rho_b\) gives

\[
\omega_b
=\frac{m_p\eta n_\gamma}{\rho_{\rm crit,100}}.
\]

Define

\[
K(T)=\frac{\rho_{\rm crit,100}}{m_pn_\gamma(T)}.
\]

Then

\[
\boxed{\eta=K(T)\omega_b},
\qquad
\boxed{\omega_b=\frac\eta{K(T)}}.
\]

Both numerator and denominator in \(K\) are mass densities, so \(K\) is
dimensionless. The registered inputs yield

\[
\boxed{K(T_{\rm CMB})=2.73415860442632\times10^{-8}}.
\]

The temperature dependence is visible:

\[
n_\gamma\propto T^3,
\qquad
K\propto T^{-3},
\qquad
\omega_b\propto \eta T^3
\]

when the other adapter constants are held fixed. The measured thermal anchor
is therefore load-bearing and must remain disclosed.

## 6. Substrate eta and dimensional H0 cascade

### 6.1 Compute physical baryon density

Insert the derived ratio and computed conversion factor:

\[
\omega_b
=\frac{6.0960895244842\times10^{-10}}
{2.73415860442632\times10^{-8}}.
\]

Dividing gives

\[
\boxed{
\omega_b=0.0222960347458090
}.
\]

This is not the same object as
\(\Omega_b=0.0492990112661008\ldots\). Their relationship is the next
step, not an equality.

### 6.2 Solve for the dimensionless Hubble parameter

By definition,

\[
\omega_b=\Omega_bh^2.
\]

Because \(\Omega_b>0\), divide by \(\Omega_b\):

\[
h^2=\frac{\omega_b}{\Omega_b}.
\]

Substitute the two derived values:

\[
h^2
=\frac{0.0222960347458090}
{0.0492990112661008}
=\boxed{0.452261296387101}.
\]

The expanding-branch convention selects the positive square root:

\[
h=\sqrt{0.452261296387101}
=0.672503751950204\ldots.
\]

### 6.3 Restore conventional units

Use the definition of \(h\):

\[
H_0=hH_{100}.
\]

In conventional units,

\[
H_0
=100h\ \mathrm{km\,s^{-1}\,Mpc^{-1}}.
\]

Therefore

\[
\boxed{
H_{0,\rm SAM}
=67.2503751950\ \mathrm{km\,s^{-1}\,Mpc^{-1}}
}.
\]

The dependency chain is now reconstructible:

\[
\boxed{
\frac{M}{\alpha_H^2\Theta}A_0^{\mathcal L/\mathcal V}
\to\eta
\xrightarrow[T_{\rm CMB},\mathrm{SI},\mathrm{CODATA}]{K(T)}
\omega_b
\xrightarrow{\Omega_b}
h^2
\to H_0
}.
\]

## 7. Source and adapter boundaries

| Quantity | Provenance type | May this chapter call it substrate-derived? |
|---|---|---|
| \(A_0,M,\alpha_H,\Theta,\mathcal L,\mathcal V\) | registered substrate identities | yes, within their source-bound definitions |
| \(\eta_{\rm SAM}\) | exact container consequence | yes |
| \(\Omega_b\) | clean inventory consequence | yes |
| \(T_{\rm CMB}=2.7255\ \mathrm K\) | FIRAS thermal measurement | no; explicit external anchor |
| \(c,h_{\rm P},k_B\) | exact SI constants in the source execution | no; conversion constants |
| \(G,m_p\) | declared CODATA values | no; external constants |
| Mpc conversion | parsec-based conventional unit | no; unit adapter |
| \(K(T_{\rm CMB})\) | computed from the disclosed external inputs | derived adapter, not a substrate primitive |
| \(\omega_b,h,H_0\) | mixed substrate-plus-adapter cascade outputs | yes as outputs of the complete named cascade, not as purely native constants |

Standard \(N_{\rm eff}\) enters when the radiation background is constructed;
it is not required to derive \(\eta\), \(K\), \(\omega_b\), or \(H_0\) in
the chain above. It remains an explicit external ingredient in subsequent
thermal-background calculations.

## 8. Deviation chain, predecessor and downstream propagation

### 8.1 G395 is a predecessor, not the final native selector

`G:G395@SAM-ARCHIVE` recorded a density-closure selector candidate near
\(67.4\ \mathrm{km\,s^{-1}\,Mpc^{-1}}\), with primary consensus
\(67.4359538109\). Its own scope boundary says the selector is
CMB-data-conditioned and that an exact native parameter-free selector remains
open. That number is therefore not silently substituted into the container
cascade.

[`CR:CR036@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036-eta-sam-and-h0-selector/README.md) asks a different and sharper question: given the registered
container identity, measured blackbody temperature and disclosed constants,
what dimensional \(H_0\) follows? The answer is the value derived in Section
6. The predecessor remains in the index because it records how the route
developed and what it did not yet establish.

### 8.2 CR036 primary result and its reported-only diagnostic defect

The source execution records clean status, zero introduced free parameters,
no opened prior-result or CMB-spectrum files, and the exact arithmetic chain
used here. It compared \(\eta\) and \(H_0\) with predeclared numerical
references, but those values did not enter the equations.

The same artifact contains an E5 equality row explicitly labeled “reported
only.” That row emits a physically unusable
\(\omega_\gamma=2.2225993836\times10^{12}\) and \(z_{\rm eq}=-1\). This
chapter preserves the row as a diagnostic implementation defect and does not
consume it. The dimensionless radiation density used by the thermal ladder is
reconstructed in `SAMA-D000020` from the correctly typed radiation-energy
density. No correction to the sealed CR036 artifact is made here.

### 8.3 CR036B propagates the fixed Hubble output

[`CR:CR036B@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036b-cmb-shape-with-h0-sam/README.md) cited \(H_{0,\rm SAM}\) as a precommitted literal and ran the
SAM density spine through CAMB 1.6.6. It did not open the CR036 or earlier
shape result files at runtime. Run A preserved external Planck-centroid
perturbation values; it was therefore a downstream propagation test, not a
derivation of every CMB input from the substrate.

The source execution recorded a passing TT full-shape statistic
\(\chi^2/\mathrm{dof}=1.0413\), with its declared peak gate passing two of
three subconditions. That evidence belongs in the full-shape development of
`SAMA-D000021`. Its role here is narrower: the emitted \(H_0\) survived
independent downstream use without being tuned to that spectrum.

## 9. Wrong controls and dimensional checks

| Wrong or diagnostic route | What fails | Correct route |
|---|---|---|
| Treat \(T_{\rm CMB}\) as a substrate identity | Conceals a measured thermal anchor. | Declare it before evaluating \(n_\gamma\). |
| Import a literature coefficient for \(\eta=K\omega_b\) without reconstruction | Hides unit and constant choices. | Derive \(n_\gamma\), \(H_{100}\), \(\rho_{\rm crit,100}\), and \(K\). |
| Set \(\Omega_b=\omega_b\) | Drops \(h^2\) and confuses fraction with physical-density parameter. | Use \(\omega_b=\Omega_bh^2\). |
| Use \(\Omega_{m,\mathrm{eff}}\) to change this baryon cascade | Imports an unrelated effective total-matter operator. | Consume the clean \(\Omega_b\), which is unchanged across the two inventory lanes. |
| Use a Planck \(\omega_b\) comparator as input | Selects the density from the target. | Compute \(\omega_b=\eta/K\) before comparison. |
| Fit \(H_0\) in the downstream spectrum | Reverses the dependency arrow. | Freeze the CR036 value and propagate it as CR036B did. |
| Use the G395 consensus as the exact native result | Exceeds its CMB-conditioned candidate boundary. | Preserve G395, then use the explicit CR036 container cascade. |
| Consume CR036's reported-only E5 row | Propagates an unusable radiation-density implementation output. | Rebuild radiation density in the typed thermal background. |
| Omit the positive-root convention | Leaves \(h=\pm\sqrt{h^2}\) formally ambiguous. | Select the positive expanding-background branch. |
| Interpret a hash, source `PASS`, or clean execution as approval | Mixes custody with owner review. | Keep the revision false/null. |

## 10. Established result, exact boundary and forward handoff

The substrate identity is

\[
\boxed{
\eta_{\rm SAM}
=\frac{M}{\alpha_H^2\Theta}A_0^{\mathcal L/\mathcal V}
=\frac74A_0^6
=6.0960895244842\times10^{-10}
}.
\]

The disclosed dimensional adapter gives

\[
\boxed{
K=2.73415860442632\times10^{-8},
\quad
\omega_b=0.0222960347458090,
\quad
h^2=0.452261296387101,
\quad
H_0=67.2503751950\ \mathrm{km\,s^{-1}\,Mpc^{-1}}
}.
\]

No new chapter-level SAMA result classification is assigned because none of
the three registered crosswalk rows carries an authorized SAMA
classification. Historical source verdict strings remain evidence metadata.

This result does not derive \(T_{\rm CMB}\), \(G\), \(m_p\), the Mpc, or
standard radiation content from SAM. It does not make CR036B's external
perturbation centroids native. It does not use the defective reported-only E5
row as an equality result. It does establish a complete, dimensionally typed
route from the registered \(\eta\) and \(\Omega_b\) identities through the
declared adapters to \(H_0\).

`SAMA-D000020` receives \(H_0\), \(T_{\rm CMB}\), \(\Omega_b\),
\(\Omega_m\), and the radiation adapter to build the background thermal clock,
Peebles transport, optical depths and acoustic geometry. `SAMA-D000021`
receives the same fixed density/Hubble packet for the separately scoped full-
shape calculation.

## 11. Focused test and result index

| Exact qualified key | Role | Preserved outcome or boundary | Direct result | Test folder |
|---|---|---|---|---|
| `G:G395@SAM-ARCHIVE` | premise/predecessor | Source verdict `G395_PASS_H0_67P4_DENSITY_CLOSURE_SELECTOR_CANDIDATE__EXACT_NATIVE_SELECTOR_OPEN`; CMB-conditioned candidate, not the exact container cascade. | result (source locator: `../reference files_misc/archive/substrate_G_tests/G395_H0_DENSITY_CLOSURE_SELECTOR/G395_output.json`; no public file URL is supplied) | folder (source locator: `../reference files_misc/archive/substrate_G_tests/G395_H0_DENSITY_CLOSURE_SELECTOR`; no public file URL is supplied) |
| [`CR:CR036@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036-eta-sam-and-h0-selector/README.md) | cascade result | Exact \(\eta,K,\omega_b,h^2,H_0\) chain; external adapters disclosed; reported-only E5 defect not consumed. | [result](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_result.md) | [folder](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR) |
| [`CR:CR036B@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036b-cmb-shape-with-h0-sam/README.md) | downstream result | Fixed \(H_{0,\rm SAM}\) propagated through CAMB with disclosed external perturbations; earlier sealed artifacts not overwritten. | [result](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036B_CMB_SHAPE_WITH_H0_SAM/CR036B_result.md) | [folder](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036B_CMB_SHAPE_WITH_H0_SAM) |

## 12. Atomic SAMA source-record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000001-R001` | Supplies \(A_0=1/(12\pi)\). |
| `SAMA-C000032-R001` | Supplies \(M=126\), \(\Theta=18\), \(\mathcal L=162\), and the carrier split. |
| `SAMA-C000091-R001` | Supplies \(\chi=2/(9\pi)\), used through the baryon fraction. |
| `SAMA-C000092-R001` | Supplies the clean \(\Omega_b\) and inventory typing. |
| `SAMA-C000096-R001` | Defines the exact substrate \(\eta\) identity. |
| `SAMA-C000097-R001` | Defines photon density and \(K(T)\). |
| `SAMA-C000098-R001` | Records the CR036 eta-to-Hubble numerical result. |
| `SAMA-C000099-R001` | Enforces the substrate/external-input boundary. |
| `SAMA-C000122-R001` | Enforces the cross-volume subject boundary. |
| `SAMA-C000124-R001` | Separates source-era chronology from current authority. |
| `SAMA-C000125-R001` | Enforces historical-status, classification and approval typing. |

## 13. Sources and external references

- Sean Brady and SAM collaborators, [Volume I technical spine, V.3--V.4](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md).
- D. J. Fixsen, [The Temperature of the Cosmic Microwave Background](https://doi.org/10.1088/0004-637X/707/2/916), for the external FIRAS thermal anchor used by the registered source execution.
- Planck Collaboration, [Planck 2018 results VI: cosmological parameters](https://doi.org/10.1051/0004-6361/201833910), for source-declared comparison context only.
- SI Brochure, [The International System of Units](https://www.bipm.org/en/publications/si-brochure), for the exact SI constants and unit convention named in the source artifact.

The external references define measurements, units and comparison context.
They do not supply the substrate container exponents or select the cascade's
native side.

## 14. Revision, hash and approval boundary

This is registered document `SAMA-D000019`, revision \(1\). The document
catalog and generated manifests bind this exact content to its computed
SHA-256. The primary source-spine hash is fixed above, and each evidence row is
bound to the artifact hash in the permanent test registry. These hashes
establish exact custody only.

All eleven assigned atomic records and all three exact test keys appear
individually above. `reviewed_and_approved` remains `false`; `approval`
remains `null`. Derivation completeness, dimensional closure, source `PASS`
fields, downstream propagation and mechanical validation do not constitute
owner approval.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`CR:CR036@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036-eta-sam-and-h0-selector/README.md) | [CR036_PRECOMMIT.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_PRECOMMIT.md) | [CR036_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_runner.py) | [CR036_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_runner.py)<br>[CR036_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_result.md)<br>[CR036_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_summary.json) | [CR036_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_result.md)<br>[CR036_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_summary.json) | [All 7 files](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036-eta-sam-and-h0-selector/README.md) |
| [`CR:CR036B@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036b-cmb-shape-with-h0-sam/README.md) | [CR036B_PRECOMMIT.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036B_CMB_SHAPE_WITH_H0_SAM/CR036B_PRECOMMIT.md) | [CR036B_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036B_CMB_SHAPE_WITH_H0_SAM/CR036B_runner.py) | [CR036B_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036B_CMB_SHAPE_WITH_H0_SAM/CR036B_runner.py)<br>[CR036B_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036B_CMB_SHAPE_WITH_H0_SAM/CR036B_result.md)<br>[CR036B_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036B_CMB_SHAPE_WITH_H0_SAM/CR036B_summary.json) | [CR036B_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036B_CMB_SHAPE_WITH_H0_SAM/CR036B_result.md)<br>[CR036B_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036B_CMB_SHAPE_WITH_H0_SAM/CR036B_summary.json) | [All 11 files](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036b-cmb-shape-with-h0-sam/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000019`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/BARYON_TO_PHOTON_AND_HUBBLE_CASCADE.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000019 | Early-Universe Cosmology | Baryon-to-Photon Identity, Photon Density and Hubble Cascade |

| Document field | Value |
|---|---|
| Purpose | Derive the substrate baryon-to-photon identity, expose every thermal and SI adapter, convert the dimensionless inventory into \(\omega_b\), \(h\), and \(H_0\), and preserve predecessor, downstream-propagation and implementation boundaries. |
| Prerequisite document | `SAMA-D000018` |
| Used by | `SAMA-D000020`; focused child of `SAMA-P000002`. |
| Primary theory source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), V.3--V.4; SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`; all three qualified keys below resolve there. |
| Revision state | Source-bound revision 1; `reviewed_and_approved: false`; `approval: null`. |

</details>
