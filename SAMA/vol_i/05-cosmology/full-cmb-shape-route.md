[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Full CMB Shape Route

## Current research connections — 14 September 2026

The global execution authority is SLC-GEN3-R3 / SLC-GEN3-CEV1-R3. The September 2026 research includes exact retained-history computation, RH arithmetic compensation, native Mersenne work, Starbreaker signed reception and ATOM3D contact/grammar. The research index connects the retained derivations to the latest code, results and current domain assignments.

[Current derivations, code and results](../../../docs/RESEARCH.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

The full CMB route asks what happens when a cosmological packet is fixed
upstream and then exposed, unchanged, to measured spectral shape. The packet
is

\[
\mathcal C_{\rm SAM}
=
\{\Omega_m,\Omega_b,\Omega_c,H_0,A_s,n_s,\tau\}.
\]

Its density, Hubble and perturbation members are supplied by the substrate
chain. CAMB, standard recombination, the pivot convention, baseline neutrino
mass and radiation content are disclosed adapters. They turn the packet into
spectra; they are not additional substrate identities.

The conceptual picture is a sealed card moving through a transparent
instrument:

\[
\text{substrate identities}
\longrightarrow
\text{fixed parameter card}
\longrightarrow
\text{Boltzmann adapter}
\longrightarrow
\text{Planck shape}
\longrightarrow
\text{independent ACT shape}.
\]

The card is not adjusted after either catalog is seen. Diagnostics and wrong
controls act beside the main lane. A peak-finder defect is preserved as a
failed measurement rule, corrected without changing the cosmology, and then
retested. This makes the route a derivation, deviation and custody chain rather
than a table of final numbers.

## 1. Opening question and conceptual picture

This chapter answers:

> Starting from the clean inventory, substrate baryon-to-photon identity and
> selected perturbation triplet, can one construct a completely fixed
> cosmology, carry it through a declared standard-recombination Boltzmann
> adapter, recover the registered Planck and independent ACT spectral-shape
> results, and retain every wrong control, failed peak finder, correction and
> specifically open native-physics boundary?

There are two CMB lanes:

| Lane | Recombination | Question answered |
|---|---|---|
| Native thermal lane | corrected Peebles-style transport developed in `SAMA-D000020` | How far does internally built recombination carry the fixed background into acoustic epochs and compressed geometry? |
| Full-shape lane | standard recombination inside CAMB | What spectral shape follows when the complete fixed SAM cosmology is exposed through an established engine? |

The lanes share upstream identities but do not certify the same operator. The
native lane localizes the remaining recombination-development gap. The
full-shape lane isolates the density, Hubble and perturbation packet against
whole spectra. Their difference is a typed experimental design, not a license
to exchange whichever intermediate output is more convenient.

## 2. Typed definitions, domains and units

| Symbol | Definition | Type | Units/domain |
|---|---|---|---|
| \(A_0\) | \(1/(12\pi)\) | universal accumulation floor | dimensionless |
| \(R,D,S,\alpha_H\) | \(12,3,8,2\) | locked structural constants | dimensionless |
| \(\chi\) | \((S/D)A_0=2/(9\pi)\) | horizon quotient | dimensionless |
| \(\Omega_b\) | \(\alpha_HA_0(1-\chi)\) | clean baryon inventory | dimensionless fraction |
| \(\Omega_m\) | \(RA_0=1/\pi\) | clean matter inventory | dimensionless fraction |
| \(\Omega_c\) | \(\Omega_m-\Omega_b\) | clean cold/trapped inventory | dimensionless fraction |
| \(\eta\) | \((7/4)A_0^6\) | substrate baryon-to-photon identity | dimensionless number ratio |
| \(K(T_{\rm CMB})\) | \(\rho_{\rm crit,100}/(m_pn_\gamma)\) | dimensional conversion | dimensionless ratio in the declared unit convention |
| \(\omega_b\) | \(\Omega_bh^2=\eta/K\) | physical baryon density | dimensionless |
| \(H_0\) | \(100h\) | Hubble constant | km s\(^{-1}\) Mpc\(^{-1}\) |
| \(A_s\) | \(\eta\sqrt R\) | scalar-amplitude selector | dimensionless |
| \(n_s\) | \(1-\chi/2\) | scalar tilt selector | dimensionless |
| \(\tau\) | \(2A_0\) | reionization optical-depth selector | dimensionless |
| \(C_\ell^{XY}\) | angular power spectrum for \(XY\in\{TT,TE,EE\}\) | spectral observable | conventional CMB spectrum units |
| \(D_\ell\) | \(\ell(\ell+1)C_\ell/(2\pi)\) | plotted bandpower form | \(\mu{\rm K}^2\) |
| \(\chi^2/N\) | covariance-appropriate or declared residual score per datum | comparison statistic | dimensionless |

The same Greek letter \(\chi\) appears in the substrate quotient and in
\(\chi^2\) statistics, but the objects are different. The former is an input
identity; the latter scores residuals after a spectrum has been generated.

## 3. Build the density side of the fixed packet

### 3.1 Derive the horizon quotient

Start with

\[
S=2^D=2^3=8
\]

and

\[
A_0=\frac1{12\pi}.
\]

Then

\[
\chi
=\frac SD A_0
=\frac83\frac1{12\pi}
=\boxed{\frac2{9\pi}}
=0.0707355302630646\ldots.
\]

### 3.2 Derive the clean inventory

The baryon member is

\[
\Omega_b
=\alpha_HA_0(1-\chi)
=2\frac1{12\pi}
\left(1-\frac2{9\pi}\right)
=0.0492990112661008\ldots.
\]

The matter member is

\[
\Omega_m
=RA_0
=12\frac1{12\pi}
=\boxed{\frac1\pi}
=0.318309886183791\ldots.
\]

Therefore

\[
\Omega_c
=\Omega_m-\Omega_b
=0.269010874917690\ldots,
\]

and the clean complement is

\[
\Omega_\Lambda
=1-\Omega_m
=\frac{\pi-1}{\pi}.
\]

These are inventory quantities. Although \(A_0R=1/\pi\) also appears as the
cosmological road ceiling, the road and inventory remain different operators.

## 4. Derive the Hubble member

### 4.1 Substrate baryon-to-photon identity

The container identity is

\[
\eta
=\frac{M}{\alpha_H^2\Theta}
A_0^{\mathcal L/\mathcal V}.
\]

With

\[
\frac{M}{\alpha_H^2\Theta}
=\frac{126}{2^2\cdot18}
=\frac74
\]

and

\[
\frac{\mathcal L}{\mathcal V}
=\frac{162}{27}
=6,
\]

one obtains

\[
\boxed{
\eta
=\frac74A_0^6
=\frac7{4(12\pi)^6}
}
=6.0960895244842\times10^{-10}.
\]

### 4.2 Declared dimensional bridge

The measured background temperature supplies the photon density

\[
n_\gamma(T)
=\frac{2\zeta(3)}{\pi^2}
\left(\frac{k_BT}{\hbar c}\right)^3.
\]

At the \(h=1\) reference normalization,

\[
\rho_{\rm crit,100}
=\frac{3H_{100}^2}{8\pi G}.
\]

Define

\[
K(T_{\rm CMB})
=\frac{\rho_{\rm crit,100}}
{m_pn_\gamma(T_{\rm CMB})}.
\]

Then

\[
\omega_b=\frac{\eta}{K},
\qquad
h^2=\frac{\omega_b}{\Omega_b},
\qquad
H_0=100h.
\]

The source execution records

\[
K=2.73415860442632\times10^{-8},
\]

\[
\omega_b=0.0222960347458090,
\qquad
h^2=0.452261296387101,
\]

\[
\boxed{
H_0=67.2503751950\
\mathrm{km\,s^{-1}\,Mpc^{-1}}
}.
\]

FIRAS \(T_{\rm CMB}=2.7255\ {\rm K}\), CODATA/SI constants and the declared
radiation/neutrino conventions are external ingredients. They are disclosed
conversion inputs, not hidden identities and not quantities fitted to the CMB
shape in this route.

## 5. Derive the perturbation triplet

The amplitude selector begins from the dimensionless \(\eta\) and the radix:

\[
A_s=\eta\sqrt R.
\]

For \(R=12\),

\[
A_s
=6.0960895244842\times10^{-10}\sqrt{12}
=\boxed{2.1117473568\times10^{-9}}.
\]

The tilt selector is

\[
n_s
=1-\frac\chi2
=1-\frac1{9\pi}
=\boxed{0.9646322349}.
\]

The optical-depth selector is

\[
\tau=2A_0
=\frac1{6\pi}
=\boxed{0.0530516477}.
\]

The selected triplet is therefore

\[
\boxed{
(A_s,n_s,\tau)
=
(2.1117473568\times10^{-9},
0.9646322349,
0.0530516477)
}.
\]

The selectors are fixed before the full spectra are read. This order prevents
a Planck or ACT residual from becoming an undeclared parameter-selection
rule.

## 6. Assemble the fixed packet and declare the adapter

The full packet is

\[
\boxed{
\mathcal C_{\rm SAM}
=
\{\Omega_m,\Omega_b,\Omega_c,H_0,A_s,n_s,\tau\}
}.
\]

The Boltzmann route then supplies a deterministic map

\[
\mathfrak B:
\mathcal C_{\rm SAM}\times\mathcal A_{\rm ext}
\longrightarrow
\{C_\ell^{TT},C_\ell^{TE},C_\ell^{EE}\},
\]

where \(\mathcal A_{\rm ext}\) contains the disclosed ancillary settings:
standard recombination in the engine, \(T_{\rm CMB}\), \(N_{\rm eff}\), a
fixed baseline neutrino mass, the scalar pivot convention and numerical
accuracy choices.

This function typing matters. The statement is not
\(\mathfrak B\in\mathcal C_{\rm SAM}\). The engine is an adapter applied to the
packet, not a newly derived substrate primitive.

## 7. Fixed CMB parameter card and diagnostics

The earlier G-stage sequence established the execution grammar before the
later branch-19 full-shape zipper.

### 7.1 Freeze the parameter card

[`G:G379`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) wrote the parameter card and passed eight of eight validation checks.
Its exact historical source verdict is
`G379_PASS_SAM_CMB_PARAMETER_CARD_FROZEN`. The card freeze is the custody
step: downstream residuals may evaluate the packet but do not rewrite it.

### 7.2 Smoke-test the spectral route

[`G:G380`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) ran the fixed-background spectrum smoke and emitted primary,
boundary and wrong-control spectra. Its source verdict is
`G380_PASS_FIXED_BACKGROUND_CMB_SPECTRUM_SMOKE`. This step checks that the
adapter can consume the frozen card before any precision interpretation is
attached.

### 7.3 Planck-lite diagonal contact

[`G:G381`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) compared the fixed-density route with a diagonal Planck-lite
statistic. It recorded

\[
\Delta\chi^2_{\rm primary}/N
=0.0008836165765404745
\]

against

\[
\Delta\chi^2_{\rm wrong}/N
=1.472411841957094.
\]

The primary was better than the declared wrong control in TT, TE and EE. The
source verdict is `G381_PASS_PLANCK_LITE_DIAGONAL_CONTACT`. Its explicit
boundary is equally important: no full covariance, nuisance, calibration,
low-\(\ell\) or lensing likelihood was evaluated at this stage.

### 7.4 Localize residuals

[`G:G382`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) recorded 12/12 prediction checks and 8/8 wrong-control checks. Among
its diagnostics were

\[
\langle|\Delta\ell|\rangle_{TT}=0.2,
\qquad
\langle|\Delta\ell|\rangle_{EE}=0.5,
\]

\[
\langle\Delta\chi^2/N\rangle_{\rm damping}
=0.001745657606740653,
\]

and a TE sign-mismatch fraction of
\(0.002004040209319791\). Its source verdict is
`G382_PASS_RESIDUALS_LOCALIZED_PRIMARY_STABLE`.

### 7.5 Keep competitive and gross wrong controls distinct

[`G:G383`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) rejected the gross \(H_0=73.04\), \(A_L=2\) control, whose combined
high-\(\ell\) score was

\[
\Delta\chi^2/N=1.397435980086712.
\]

It also found a competitive matter-response neighbor with

\[
\Delta\chi^2/N=8.89905757918217\times10^{-5},
\]

better than the then-committed primary within that limited diagonal
diagnostic. The correct outcome was therefore not to hide the neighbor. The
source verdict records both facts:
`G383_PASS_GROSS_WRONG_CONTROLS__BOUNDARY_MATTER_RESPONSE_SELECTOR_OPEN`.

A post hoc \(H_0\) scan reaching \(67.4\) was also marked diagnostically
inadmissible as a native selector because the value was chosen after spectral
scoring.

### 7.6 Preserve the conditional boundary

[`G:G384`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) closed that G-stage packet with six of six checks, gross wrong
controls defeated and the matter-response selector still open. Its source
verdict is
`TOE_G22B_PASS_CONDITIONAL_IMPORTED_PERTURBATION_SPECTRUM__MATTER_RESPONSE_SELECTOR_OPEN`.

These G-stage labels are historical source metadata. They are not converted
into new SAMA classifications. The later branch-19 chain starts again with
explicitly derived \(H_0\) and perturbation selectors.

## 8. Planck density and precision extension

[`CR:CR021@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr021-planck-lite-cmb-density-and-bbn-contact/README.md) joined the G-stage density card to a Planck-lite CMB/BBN
contact packet. The source artifact is `CLEAN` and `BOUNDARY`. It records the
same primary-versus-wrong-control contrast as the G-stage summary and keeps
its Planck-lite scope.

[`CR:CR022@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr022-precision-cmb-extension-from-sam-precision-cmb/README.md) extended the route to a precision-CMB packet with then-native
values including

\[
A_s=2.1262624258595048\times10^{-9},
\qquad
n_s=0.9646322348684677,
\]

and

\[
100\theta_*=1.0411066266105615.
\]

It too is source `CLEAN`/`BOUNDARY`. Its stated boundary says that an imported
perturbation trio remained closer to the official Planck theory and that the
recombination/acoustic-ruler bridge remained open. These are bounded
precursors, not retroactive descriptions of the later derived triplet.

## 9. CR035A peak-finder failure and CR035A2 correction

### 9.1 What CR035A held fixed

[`CR:CR035A@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr035a-sam-density-spine-cmb-shape/README.md) fixed the SAM density spine, Planck-centroid perturbations,
CAMB 1.6.6, Planck PR3 files, full-shape statistic and predeclared tolerances.
Its TT full-shape score was

\[
\chi^2_{TT}/{\rm dof}=1.3464.
\]

That score passed its full-shape band. The run nevertheless received its
sealed source `FAIL` because the peak finder selected the wrong third feature:

\[
\ell_{3,\rm selected}=661
\]

instead of the Planck third-peak neighborhood around

\[
\ell_{3,\rm Planck}=814.
\]

The defect was in the measurement rule, not the cosmology execution. The
failed artifact stays part of the evidence chain.

### 9.2 Isolate the specification error

The unrestricted finder could treat a substructure or trough-adjacent feature
as the next global peak. That makes “third peak” dependent on implementation
details not encoded in the intended question. The correction therefore
declared:

- one search window per expected acoustic feature;
- minimum prominence \(50\ \mu{\rm K}^2\);
- heights evaluated on the smoothed curve at the selected multipole; and
- an explicit verdict mapping consistent with the frozen peak and shape
  tolerances.

### 9.3 Correct and retest without changing the packet

[`CR:CR035A2@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr035a2-peak-finder-audit/README.md) retained the same cosmology, engine, Planck files,
\(\chi^2\) calculation, tolerances and diagnostic-optimization bounds. Only
the peak finder and verdict tree changed. The corrected selector found

\[
\ell_3=814
\]

and recorded its source `PASS`. The first run remained sealed.

The deviation chain is therefore

\[
\text{fixed packet}
\to
\text{faulty peak selector}
\to
\text{preserved failure}
\to
\text{selector correction}
\to
\text{same-packet retest}.
\]

This chapter assigns no new SAMA classification to either row.

## 10. H0 cascade propagated to CMB shape

[`CR:CR036@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036-eta-sam-and-h0-selector/README.md) is the premise that derives

\[
\eta,\quad K,\quad\omega_b,\quad h^2,\quad H_0
\]

in the order developed in Section 4. It records

\[
H_{0,\rm SAM}=67.2503751950\
\mathrm{km\,s^{-1}\,Mpc^{-1}}.
\]

Its reported-only E5 diagnostic is not part of that cascade. E5 emits
\(\omega_\gamma=2.2225993836\times10^{12}\) and \(z_{\rm eq}=-1\). The
implementation treated photon energy density as though it were already mass
density, omitting the required \(c^{-2}\) conversion. `SAMA-C000098-R001`
therefore preserves E5 as a non-load-bearing implementation defect; neither
this chapter nor the background operator consumes it.

[`CR:CR036B@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036b-cmb-shape-with-h0-sam/README.md) replaces the earlier external \(H_0\) member with this sealed
value while leaving the density spine, Planck-centroid perturbations, engine,
files and corrected peak selector unchanged. It records

\[
\chi^2_{TT}/{\rm dof}\approx1.04.
\]

The propagation test answers a narrow causal question:

\[
H_0^{\rm external}
\longrightarrow
H_{0,\rm SAM}
\]

without altering the rest of the input card. It establishes that the derived
Hubble member survives the same shape route. It does not turn CAMB or standard
recombination into substrate identities.

Chronology is also load-bearing. The corrected native-recombination test
represented by `SAMA-C000105-R001` remains sealed at its BAO-side
\(H_0=68.76\ \mathrm{km\,s^{-1}\,Mpc^{-1}}\). The later independent CR036
value is used by CR036B and the CR037 full-shape chain; it is not substituted
backward into CR001c.

## 11. Perturbation selector, Planck/ACT results and zipper

### 11.1 Select the triplet before reading spectra

[`CR:CR037A@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr037a-sam-perturbation-selector/README.md) evaluated the three closed forms against frozen Planck
posterior centroids without loading a spectrum at runtime. The standardized
offsets were

\[
z_{A_s}=+0.3916,
\qquad
z_{n_s}=-0.0638,
\qquad
z_\tau=-0.1847.
\]

For the amplitude lane, the declared controls were:

| Candidate | Offset from the amplitude reference |
|---|---:|
| \(\eta\) | \(-49.6797\sigma\) |
| \(\eta\sqrt R\) | \(+0.3916\sigma\) |
| \(\eta\sqrt S\) | \(-12.5255\sigma\) |
| \(\eta\sqrt{R/2}\) | \(-20.2256\sigma\) |
| \(\eta\sqrt\Theta\) | \(+16.2117\sigma\) |
| \(D\eta\) | \(-9.0391\sigma\) |
| \(\pi\eta\) | \(-6.1619\sigma\) |

The controls show why the selected amplitude operator is
\(\eta\sqrt R\); bare dimensional proximity does not select an expression.

The source also retains the reported-only optical-depth diagnostic

\[
\tau_{\rm alt}=2A_0(1+A_0)=0.054458886359,
\]

whose frozen-reference displacement is \((+0.0080666\sigma)\). It was not used
in P3: the canonical selector remains \(\tau=2A_0=0.0530516477\). Keeping
the alternative visible records the nearby construction without silently
substituting it into the fixed packet.

### 11.2 Planck full-shape execution

[`CR:CR037B@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr037b-parameter-free-cmb-shape-attempt/README.md) assembled every member of \(\mathcal C_{\rm SAM}\). The
numerical density card passed to the engine was

\[
\omega_b=0.022296034746,
\qquad
\omega_c=0.121663207032,
\]

together with the Section 11.1 values of \(H_0,A_s,n_s,\tau\). The disclosed
non-fit settings were

| Adapter field | Frozen value |
|---|---|
| engine | CAMB 1.6.6 |
| radiation and thermal anchor | \(N_{\rm eff}=3.046\), \(T_{\rm CMB}=2.7255\ \mathrm K\) |
| scalar pivot | \(k_{\rm pivot}=0.05\ \mathrm{Mpc^{-1}}\) |
| neutrinos | summed mass \(0.06\ \mathrm{eV}\), one massive species |
| spectral execution | \(\ell_{\max}=2700\), `lens_potential_accuracy=1`, scalar and lensed |
| excluded branches | tensors false with \(r=0\); \(\Omega_k=0\); nonlinear corrections none |
| helium | CAMB BBN consistency, runtime \(Y_{\rm He}=0.245850873088\) |

No Run-B optimizer was used (`Run_B_optimizer_used=false`). The spectra are
therefore outputs of the fixed input card and these disclosed adapter
settings.

The comparison source is the Planck PR3 full per-multipole table with a
symmetric error constructed independently for each row. It is not the
official full Planck likelihood and does not claim its full covariance or
nuisance-parameter machinery. For each row,

\[
\sigma_\ell
=\frac{|\sigma_{\ell,-}|+|\sigma_{\ell,+}|}{2},
\qquad
\chi^2_X
=\sum_{\ell}
\left(
\frac{D_{\ell,X}^{\rm SAM}-D_{\ell,X}^{\rm PR3}}
{\sigma_{\ell,X}}
\right)^2,
\qquad
N_X=\#\{\text{rows scored}\}.
\]

The TT score covers integer multipoles \(30\leq\ell\leq2500\). With the
source's corresponding TE and EE tables, the execution recorded

\[
\frac{\chi^2_{TT}}{N_{TT}}=1.0339,
\qquad
\frac{\chi^2_{TE}}{N_{TE}}=1.0454,
\qquad
\frac{\chi^2_{EE}}{N_{EE}}=1.0430.
\]

Its audited first three TT peaks were

\[
(\ell_1,\ell_2,\ell_3)_{\rm SAM}
=(220,535,812),
\]

compared with

\[
(\ell_1,\ell_2,\ell_3)_{\rm Planck}
=(219,520,814).
\]

Those peaks are reconstructible from three separate windows,
\([150,300]\), \([400,650]\) and \([700,900]\). Each TT curve is smoothed
with a Gaussian of \(\sigma_\ell=5\); a candidate must have prominence at
least \(50\ \mu\mathrm K^2\); the highest-prominence candidate in a window
is selected, with a tie resolved toward larger \(\ell\); and the height is
read from the smoothed curve.

| CR037B gate | Exact condition | Recorded outcome |
|---|---|---|
| P1a | \(|\Delta\ell_1|\leq5\) | PASS: \(|220-219|=1\) |
| P1b | \(|\Delta\ell_2|\leq10\) and \(|\Delta\ell_3|\leq10\) | FAIL: \(15\) and \(2\); the second-peak displacement exceeds its gate |
| P1c | both \(H_2/H_1\) and \(H_3/H_1\) within \(15\%\) of the table ratios | PASS |
| aggregate P1 | at least two of P1a, P1b and P1c pass | PASS: two of three |
| P2 | TT full-per-multipole score in its declared PASS band | PASS: \(1.0339\) |

The failed P1b sub-gate remains visible inside the aggregate passing result;
it is not erased by the other two peak predicates.

### 11.3 Independent ACT holdout

[`CR:CR037C@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr037c-parameter-free-act-dr4-independence/README.md) carried the same packet to ACT DR4. The execution used
published bandpower windows, the full covariance and fixed polarization
efficiency \(y_{p2}=1\). It introduced no fitted cosmological parameter and
did not load Planck files at runtime.

The ACT engine call raises CAMB's reach to \(\ell_{\max}=8000\) and
`lens_potential_accuracy=4`, retaining the same fixed cosmology. Since CAMB's
returned arrays are in \(D_\ell\) form while the likelihood windows consume
\(C_\ell\), the source first applies

\[
C_\ell=\frac{2\pi D_\ell}{\ell(\ell+1)}.
\]

The published deep and wide bandpower windows convolve those spectra into a
260-component model vector: 80 TT, 90 TE and 90 EE values. Polarization
calibration multiplies the TT, TE and EE sectors by

\[
1,\qquad y_{p2},\qquad y_{p2}^2,
\]

respectively, with \(y_{p2}=1\) fixed rather than fitted. For

\[
Y=X_{\rm model}-X_{\rm data},
\]

the full statistic is

\[
\chi^2_{\rm full}=Y^{\mathsf T}C^{-1}Y
\]

using the published \(260\times260\) covariance; the TT, TE and EE rows use
the corresponding covariance sub-blocks. This pipeline recorded

\[
\frac{\chi^2_{TT}}{N_{TT}}=1.2996,
\qquad
\frac{\chi^2_{TE}}{N_{TE}}=0.9495,
\]

\[
\frac{\chi^2_{EE}}{N_{EE}}=1.0662,
\qquad
\frac{\chi^2_{\rm full}}{N_{\rm full}}=1.1218.
\]

| CR037C gate | Exact condition | Outcome |
|---|---|---|
| P1 | \(\chi^2_{TT}/N_{TT}\leq2\) | PASS: \(1.2996\) |
| P2 | \(\chi^2_{\rm full}/N_{\rm full}\leq2\) | PASS: \(1.1218\) |
| P3 | both TE and EE scores \(\leq3\) | PASS: \(0.9495\) and \(1.0662\) |

For this independently instrumented full-shape result:

**The test result suggests strong contact with the concept.**

The classification attaches to the registered result, not to every historical
G-stage or precursor row.

### 11.4 Zip the causal chain

[`CR:CR038@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr038-branch-verdict-zipper-parameter-free-cmb-shape/README.md) checks that six sealed branch-19 members retain:

- the same clean density inventory;
- \(H_0=67.2503751950\ \mathrm{km\,s^{-1}\,Mpc^{-1}}\);
- the same \(A_s,n_s,\tau\) triplet;
- the Planck full-shape score;
- the ACT independent-instrument scores;
- zero free cosmological parameters in the shape executions; and
- the preserved CR035A failure beside its corrected successor.

Its chain-level zipper is explicit:

| Gate | Chain predicate | Outcome |
|---|---|---|
| G1 | CR035A2, CR036, CR036B, CR037A, CR037B and CR037C are each source `PASS`, `CLEAN`, zero-free-parameter, prior-result-input-free and forbidden-open-free | PASS |
| G2 | \(\Omega_m,\Omega_b,\Omega_c\) are invariant across the chain | PASS |
| G3 | \(H_0=67.2503751950\ \mathrm{km\,s^{-1}\,Mpc^{-1}}\) propagates through CR036, CR036B, CR037B and CR037C | PASS |
| G4 | the CR037A \(A_s,n_s,\tau\) triplet propagates unchanged to CR037B and CR037C | PASS |
| G5 | Planck TT score \(\leq2\) | PASS: \(1.0339\) |
| G6 | ACT TT and full scores each \(\leq2\) | PASS: \(1.2996\), \(1.1218\) |
| G7 | ACT-only independence: no Planck data file enters CR037C | PASS |
| G8 | zipper precommit hash matches the sealed precommit | PASS |
| G9 | forbidden-file `open()` guard is not tripped | PASS |

CR035A is not one of the six passing predicates. It remains separately sealed
as the failed peak-finder audit trail that CR035A2 corrects.

The zipper does not average the Planck and ACT scores. It certifies exact
propagation and evidence custody across two instruments. For that registered
zipper:

**The test result suggests strong contact with the concept.**

## 12. Deviation, wrong-control and correction ledger

| Deviation or control | What it exposes | Correct route or retained boundary |
|---|---|---|
| Change the parameter card after residual scoring | Converts comparison into result-driven fitting. | Freeze the card before spectrum execution. |
| Treat a diagonal Planck-lite score as the full likelihood | Omits covariance, nuisance and calibration structure. | Keep the G381/branch-07 boundary; use the declared full-shape rows for their own scopes. |
| Promote the G383 post hoc \(H_0\) scan | Selects \(H_0\) after target access. | Derive \(H_0\) through the independent \(\eta\)-to-density cascade. |
| Hide the competitive G383 matter-response neighbor | Erases a source-era open selector. | Preserve it as a bounded diagnostic; do not read it as the later branch-19 formula. |
| Use bare \(\eta\), \(\eta\sqrt S\), \(\eta\sqrt{R/2}\), \(\eta\sqrt\Theta\), \(D\eta\) or \(\pi\eta\) for \(A_s\) | The declared wrong selectors sit much farther from the frozen reference. | Use the predeclared \(A_s=\eta\sqrt R\) identity. |
| Use an unrestricted global peak finder | CR035A selects \(\ell=661\) as the third feature and fails its peak gate. | Specify windows and prominence; rerun the unchanged packet in CR035A2. |
| Delete CR035A after correction | Destroys the implementation-failure record. | Preserve CR035A and add CR035A2 as correction/retest. |
| Import Planck-centroid perturbations into the final fixed packet | Leaves the perturbation lane externally supplied. | Replace them with the CR037A substrate triplet before CR037B. |
| Refit the packet for ACT | Defeats instrument independence. | Carry the unchanged packet and fixed \(y_{p2}=1\) to ACT. |
| Identify standard recombination with the native thermal lane | Collapses an adapter into an internal derivation. | Keep `SAMA-D000020` and this full-shape lane complementary. |
| Treat source `PASS`/`FAIL` tokens as SAMA classifications | Changes the project result language. | Preserve tokens as provenance and use only explicitly registered classifications. |

## 13. Evidence sequence and causal custody

| Chain | Exact qualified key | Role | Source-bound outcome |
|---|---|---|---|
| Frozen card | [`G:G379`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | premise | Card frozen; 8/8 validations. |
| Frozen card | [`G:G380`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | construction | Fixed-background spectrum smoke. |
| Frozen card | [`G:G381`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | result | Primary diagonal score \(0.0008836\), wrong control \(1.4724\); limited likelihood boundary. |
| Frozen card | [`G:G382`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | intended control | Residual localization, 12/12 predictions and 8/8 controls. |
| Frozen card | [`G:G383`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | wrong control | Gross controls rejected; competitive matter-response selector retained open. |
| Frozen card | [`G:G384`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | boundary | Conditional source close with imported perturbation and selector boundary. |
| Planck precursor | [`CR:CR021@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr021-planck-lite-cmb-density-and-bbn-contact/README.md) | premise | Source `CLEAN`/`BOUNDARY` Planck-lite density/BBN contact. |
| Planck precursor | [`CR:CR022@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr022-precision-cmb-extension-from-sam-precision-cmb/README.md) | boundary | Source `CLEAN`/`BOUNDARY` precision extension. |
| Peak correction | [`CR:CR035A@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr035a-sam-density-spine-cmb-shape/README.md) | preserved failure | Clean sealed failure caused by third-peak misidentification. |
| Peak correction | [`CR:CR035A2@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr035a2-peak-finder-audit/README.md) | correction/retest | Same packet, corrected finder, third peak \(\ell=814\). |
| Hubble cascade | [`CR:CR036@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036-eta-sam-and-h0-selector/README.md) | premise | Derives \(\eta\), \(\omega_b\), \(h^2\) and \(H_0\). |
| Hubble cascade | [`CR:CR036B@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036b-cmb-shape-with-h0-sam/README.md) | propagation result | Derived \(H_0\) survives the corrected Planck shape route. |
| Perturbations | [`CR:CR037A@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr037a-sam-perturbation-selector/README.md) | selector construction | Derives the fixed \(A_s,n_s,\tau\) triplet. |
| Full shape | [`CR:CR037B@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr037b-parameter-free-cmb-shape-attempt/README.md) | Planck result | Fixed packet through CAMB, no optimizer. |
| Full shape | [`CR:CR037C@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr037c-parameter-free-act-dr4-independence/README.md) | independent holdout | ACT full covariance and published windows, no new fit; strong contact. |
| Full shape | [`CR:CR038@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr038-branch-verdict-zipper-parameter-free-cmb-shape/README.md) | branch retest/zipper | Exact packet propagation and failure/correction custody; strong contact. |

## 14. Established result, exact evidence, forward connection and open boundary

The chapter establishes the complete fixed input packet

\[
\boxed{
\begin{aligned}
\Omega_m&=\frac1\pi,
&
\Omega_b&=2A_0(1-\chi),
&
\Omega_c&=\Omega_m-\Omega_b,\\
H_0&=67.2503751950\
\mathrm{km\,s^{-1}\,Mpc^{-1}},
&
A_s&=\eta\sqrt R,
&
n_s&=1-\frac\chi2,
&
\tau&=2A_0.
\end{aligned}
}
\]

Exact evidence is the registered 16-key sequence in Section 13. It includes
the frozen-card controls, the preserved peak-finder failure, the same-packet
correction, independently derived \(H_0\) and perturbations, the Planck
full-shape result and the ACT holdout. The authorized strong-contact
classification belongs to the ACT result and the branch zipper.

The forward connection sends this fixed cosmic packet to the Volume I
synthesis and sends the saturated-road member to `SAMA-D000023`. It does not
move particle grammar into Volume I or move the numerical engine into the
substrate ontology.

The specifically open boundary is:

1. refine substrate-native recombination beyond the current corrected Peebles
   transport and resolve or structurally explain its compressed-acoustic
   residual;
2. replace the schematic light-element lane with a full nucleosynthesis
   network;
3. add foreground-native treatment beyond cleaned experiment-marginalized
   ACT bandpowers;
4. execute declared polarization-efficiency marginalization and later
   independent-instrument extensions; and
5. keep clean \(\Omega_m=1/\pi\) separate from every
   \(\Omega_{m,\rm eff}\) application.

These open construction tasks do not rewrite the completed fixed-packet
executions recorded here.

## 15. Focused test and result index

All Courtroom links below are pinned to commit
`b5e914f71377e86ef4c67e199973d9300795cda1`.

| Exact qualified key | Evidence role | Direct result | Test folder |
|---|---|---|---|
| [`G:G379`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | frozen-card premise | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G379_output.json) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw) |
| [`G:G380`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | spectral smoke construction | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G380_output.json) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw) |
| [`G:G381`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | Planck-lite result | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G381_output.json) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw) |
| [`G:G382`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | residual control | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G382_output.json) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw) |
| [`G:G383`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | wrong-control result | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G383_output.json) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw) |
| [`G:G384`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | source-era boundary | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G384_output.json) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw) |
| [`CR:CR021@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr021-planck-lite-cmb-density-and-bbn-contact/README.md) | density/BBN premise | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_result.md) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT) |
| [`CR:CR022@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr022-precision-cmb-extension-from-sam-precision-cmb/README.md) | precision boundary | [result](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR022_PRECISION_CMB_EXTENSION_FROM_sam_precision_cmb/CR022_result.md) | [folder](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR022_PRECISION_CMB_EXTENSION_FROM_sam_precision_cmb) |
| [`CR:CR035A@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr035a-sam-density-spine-cmb-shape/README.md) | preserved peak-finder failure | [result](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A_SAM_DENSITY_SPINE_CMB_SHAPE/CR035A_result.md) | [folder](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A_SAM_DENSITY_SPINE_CMB_SHAPE) |
| [`CR:CR035A2@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr035a2-peak-finder-audit/README.md) | corrected audit/retest | [result](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A2_PEAK_FINDER_AUDIT/CR035A2_result.md) | [folder](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A2_PEAK_FINDER_AUDIT) |
| [`CR:CR036@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036-eta-sam-and-h0-selector/README.md) | \(\eta\)-to-\(H_0\) premise | [result](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_result.md) | [folder](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR) |
| [`CR:CR036B@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036b-cmb-shape-with-h0-sam/README.md) | derived-\(H_0\) propagation result | [result](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036B_CMB_SHAPE_WITH_H0_SAM/CR036B_result.md) | [folder](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036B_CMB_SHAPE_WITH_H0_SAM) |
| [`CR:CR037A@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr037a-sam-perturbation-selector/README.md) | perturbation selector | [result](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037A_SAM_PERTURBATION_SELECTOR/CR037A_result.md) | [folder](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037A_SAM_PERTURBATION_SELECTOR) |
| [`CR:CR037B@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr037b-parameter-free-cmb-shape-attempt/README.md) | Planck full-shape result | [result](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037B_PARAMETER_FREE_CMB_SHAPE_ATTEMPT/CR037B_result.md) | [folder](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037B_PARAMETER_FREE_CMB_SHAPE_ATTEMPT) |
| [`CR:CR037C@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr037c-parameter-free-act-dr4-independence/README.md) | ACT independent holdout | [result](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037C_PARAMETER_FREE_ACT_DR4_INDEPENDENCE/CR037C_result.md) | [folder](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037C_PARAMETER_FREE_ACT_DR4_INDEPENDENCE) |
| [`CR:CR038@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr038-branch-verdict-zipper-parameter-free-cmb-shape/README.md) | branch zipper/retest | [result](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR038_BRANCH_VERDICT_ZIPPER_PARAMETER_FREE_CMB_SHAPE/CR038_result.md) | [folder](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR038_BRANCH_VERDICT_ZIPPER_PARAMETER_FREE_CMB_SHAPE) |

## 16. External references and source custody

- D. J. Fixsen, [The Temperature of the Cosmic Microwave Background](https://doi.org/10.1088/0004-637X/707/2/916), supplies the external FIRAS \(T_{\rm CMB}=2.7255\ \mathrm K\) anchor named by the source tests.
- E. Tiesinga et al., [CODATA recommended values of the fundamental physical constants: 2018](https://doi.org/10.1103/RevModPhys.93.025010), supplies the CODATA 2018 values used by the dimensional bridge; NIST's [Fundamental Physical Constants](https://physics.nist.gov/cuu/Constants/) is the maintained table interface.
- A. Lewis, [CAMB 1.6.6](https://pypi.org/project/camb/1.6.6/), identifies the exact Boltzmann-engine release recorded by CR037B and CR037C.
- Planck Collaboration, [Planck 2018 results VI: cosmological parameters](https://doi.org/10.1051/0004-6361/201833910), supplies the PR3 comparison context. This chapter's CR037B score uses the pinned per-multipole tables and symmetric per-row errors, not the official full Planck likelihood.
- S. K. Choi et al., [The Atacama Cosmology Telescope: a measurement of the Cosmic Microwave Background power spectra at \(98\) and \(150\) GHz](https://doi.org/10.1088/1475-7516/2020/12/045), supplies the ACT DR4 bandpowers, window functions and covariance used by CR037C.

The exact files consumed at execution are the hashed copies in the pinned
Courtroom folders in Section 15. These bibliographic links explain their
external meaning; they do not replace the executable-artifact custody or add
a new comparison.

## 17. Atomic record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000091-R001` | Defines the horizon quotient \(\chi\). |
| `SAMA-C000092-R001` | Supplies the clean cosmic inventory and road/inventory type boundary. |
| `SAMA-C000096-R001` | Derives the substrate \(\eta\) identity. |
| `SAMA-C000098-R001` | Records the numerical \(\eta\)-to-\(H_0\) cascade. |
| `SAMA-C000099-R001` | Types the external dimensional inputs. |
| `SAMA-C000100-R001` | Supplies the background and thermal-clock adapter. |
| `SAMA-C000101-R001` | Supplies the sound-horizon and acoustic geometry route. |
| `SAMA-C000105-R001` | Supplies the corrected native-recombination prerequisite and its separate lane. |
| `SAMA-C000106-R001` | Defines the perturbation triplet. |
| `SAMA-C000107-R001` | Defines the fixed packet and adapter boundary. |
| `SAMA-C000108-R001` | Records the Planck full-shape result. |
| `SAMA-C000109-R001` | Records the ACT result and branch zipper. |
| `SAMA-C000110-R001` | Preserves the two CMB lanes and exact corrected-test route. |
| `SAMA-C000122-R001` | Enforces the Volume I and cross-volume subject boundary. |
| `SAMA-C000124-R001` | Separates historical source chronology from current authority. |
| `SAMA-C000125-R001` | Preserves status, classification and approval typing. |

## 18. Source chronology, revision and approval boundary

The source artifacts control their numerical results. Historical
`PASS`, `FAIL` and `BOUNDARY` tokens remain source metadata. Present-tense
SAMA authority comes from `SAM_LIVE/07_SAMA_CURRENT.md`, not from the date or
wording of an older branch result.

The full-shape result is limited to the fixed packet through the declared
standard-recombination adapters and registered datasets. The native thermal
lane remains separately owned by `SAMA-D000020`. Matter grammar remains
Volume II, and executable Boltzmann machinery remains Volume III.

`reviewed_and_approved` remains `false`; `approval` remains `null`. Exact
hashes, source fidelity, execution, mechanical validation and an authorized
result classification do not constitute owner approval.

The non-self-referential content-hash authority is the installed record in
[`documents/catalog/document_records.jsonl`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/catalog/document_records.jsonl).
Final owner review is transferred through
`reports/THREE_VOLUME_OWNER_REVIEW_HANDOFF.json`
and its Markdown companion. Only Sean Brady's explicit decision against the
exact external content hash can change the false/null approval state; this
document does not assert its own mutable hash inline.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`G:G379`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md)<br>[G379_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G379_output.json)<br>[G379_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G379_output.json) | [G379_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G379_output.json)<br>[G379_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G379_output.json) | [All 66 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) |
| [`G:G380`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md)<br>[G380_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G380_output.json)<br>[G380_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G380_output.json) | [G380_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G380_output.json)<br>[G380_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G380_output.json) | [All 66 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) |
| [`G:G381`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md)<br>[G381_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G381_output.json)<br>[G381_results_csv.csv](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G381_results_csv.csv)<br>[G381_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G381_output.json) | [G381_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G381_output.json)<br>[G381_results_csv.csv](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G381_results_csv.csv)<br>[G381_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G381_output.json) | [All 66 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) |
| [`G:G382`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md)<br>[G382_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G382_output.json)<br>[G382_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G382_output.json) | [G382_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G382_output.json)<br>[G382_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G382_output.json) | [All 66 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) |
| [`G:G383`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md)<br>[G383_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G383_output.json)<br>[G383_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G383_output.json) | [G383_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G383_output.json)<br>[G383_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G383_output.json) | [All 66 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) |
| [`G:G384`](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) | [All package files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md)<br>[G384_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G384_output.json)<br>[G384_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G384_output.json) | [G384_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/raw/G384_output.json)<br>[G384_output.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/_source_artifacts/summaries/G384_output.json) | [All 66 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-source-artifacts/README.md) |
| [`CR:CR021@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr021-planck-lite-cmb-density-and-bbn-contact/README.md) | [CR021_PRECOMMIT.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_PRECOMMIT.md)<br>[CR021_declared_premises.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_declared_premises.json) | [CR021_runner.py](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_runner.py) | [CR021_runner.py](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_runner.py)<br>[CR021_result.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_result.md)<br>[CR021_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_summary.json) | [CR021_result.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_result.md)<br>[CR021_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR021_PLANCK_LITE_CMB_DENSITY_AND_BBN_CONTACT/CR021_summary.json) | [All 7 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr021-planck-lite-cmb-density-and-bbn-contact/README.md) |
| [`CR:CR022@07`](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr022-precision-cmb-extension-from-sam-precision-cmb/README.md) | [CR022_PRECOMMIT.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR022_PRECISION_CMB_EXTENSION_FROM_sam_precision_cmb/CR022_PRECOMMIT.md)<br>[CR022_declared_premises.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR022_PRECISION_CMB_EXTENSION_FROM_sam_precision_cmb/CR022_declared_premises.json) | [CR022_runner.py](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR022_PRECISION_CMB_EXTENSION_FROM_sam_precision_cmb/CR022_runner.py) | [CR022_runner.py](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR022_PRECISION_CMB_EXTENSION_FROM_sam_precision_cmb/CR022_runner.py)<br>[CR022_result.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR022_PRECISION_CMB_EXTENSION_FROM_sam_precision_cmb/CR022_result.md)<br>[CR022_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR022_PRECISION_CMB_EXTENSION_FROM_sam_precision_cmb/CR022_summary.json) | [CR022_result.md](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR022_PRECISION_CMB_EXTENSION_FROM_sam_precision_cmb/CR022_result.md)<br>[CR022_summary.json](../../courtroom/07_BARYON_INVENTORY_AND_COSMOLOGY/CR022_PRECISION_CMB_EXTENSION_FROM_sam_precision_cmb/CR022_summary.json) | [All 7 files](../../tests/courtroom/07-baryon-inventory-and-cosmology-cr022-precision-cmb-extension-from-sam-precision-cmb/README.md) |
| [`CR:CR035A2@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr035a2-peak-finder-audit/README.md) | [CR035A2_PRECOMMIT.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A2_PEAK_FINDER_AUDIT/CR035A2_PRECOMMIT.md) | [CR035A2_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A2_PEAK_FINDER_AUDIT/CR035A2_runner.py) | [CR035A2_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A2_PEAK_FINDER_AUDIT/CR035A2_runner.py)<br>[CR035A2_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A2_PEAK_FINDER_AUDIT/CR035A2_result.md)<br>[CR035A2_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A2_PEAK_FINDER_AUDIT/CR035A2_summary.json) | [CR035A2_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A2_PEAK_FINDER_AUDIT/CR035A2_result.md)<br>[CR035A2_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A2_PEAK_FINDER_AUDIT/CR035A2_summary.json) | [All 11 files](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr035a2-peak-finder-audit/README.md) |
| [`CR:CR035A@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr035a-sam-density-spine-cmb-shape/README.md) | [CR035A_PRECOMMIT.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A_SAM_DENSITY_SPINE_CMB_SHAPE/CR035A_PRECOMMIT.md) | [CR035A_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A_SAM_DENSITY_SPINE_CMB_SHAPE/CR035A_runner.py)<br>[CR035A_runner_v1_aborted_json_bug.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A_SAM_DENSITY_SPINE_CMB_SHAPE/CR035A_runner_v1_aborted_json_bug.py) | [CR035A_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A_SAM_DENSITY_SPINE_CMB_SHAPE/CR035A_runner.py)<br>[CR035A_runner_v1_aborted_json_bug.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A_SAM_DENSITY_SPINE_CMB_SHAPE/CR035A_runner_v1_aborted_json_bug.py)<br>[CR035A_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A_SAM_DENSITY_SPINE_CMB_SHAPE/CR035A_result.md)<br>[CR035A_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A_SAM_DENSITY_SPINE_CMB_SHAPE/CR035A_summary.json) | [CR035A_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A_SAM_DENSITY_SPINE_CMB_SHAPE/CR035A_result.md)<br>[CR035A_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR035A_SAM_DENSITY_SPINE_CMB_SHAPE/CR035A_summary.json) | [All 12 files](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr035a-sam-density-spine-cmb-shape/README.md) |
| [`CR:CR036@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036-eta-sam-and-h0-selector/README.md) | [CR036_PRECOMMIT.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_PRECOMMIT.md) | [CR036_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_runner.py) | [CR036_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_runner.py)<br>[CR036_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_result.md)<br>[CR036_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_summary.json) | [CR036_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_result.md)<br>[CR036_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036_ETA_SAM_AND_H0_SELECTOR/CR036_summary.json) | [All 7 files](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036-eta-sam-and-h0-selector/README.md) |
| [`CR:CR036B@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036b-cmb-shape-with-h0-sam/README.md) | [CR036B_PRECOMMIT.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036B_CMB_SHAPE_WITH_H0_SAM/CR036B_PRECOMMIT.md) | [CR036B_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036B_CMB_SHAPE_WITH_H0_SAM/CR036B_runner.py) | [CR036B_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036B_CMB_SHAPE_WITH_H0_SAM/CR036B_runner.py)<br>[CR036B_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036B_CMB_SHAPE_WITH_H0_SAM/CR036B_result.md)<br>[CR036B_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036B_CMB_SHAPE_WITH_H0_SAM/CR036B_summary.json) | [CR036B_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036B_CMB_SHAPE_WITH_H0_SAM/CR036B_result.md)<br>[CR036B_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR036B_CMB_SHAPE_WITH_H0_SAM/CR036B_summary.json) | [All 11 files](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr036b-cmb-shape-with-h0-sam/README.md) |
| [`CR:CR037A@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr037a-sam-perturbation-selector/README.md) | [CR037A_PRECOMMIT.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037A_SAM_PERTURBATION_SELECTOR/CR037A_PRECOMMIT.md) | [CR037A_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037A_SAM_PERTURBATION_SELECTOR/CR037A_runner.py) | [CR037A_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037A_SAM_PERTURBATION_SELECTOR/CR037A_runner.py)<br>[CR037A_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037A_SAM_PERTURBATION_SELECTOR/CR037A_result.md)<br>[CR037A_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037A_SAM_PERTURBATION_SELECTOR/CR037A_summary.json) | [CR037A_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037A_SAM_PERTURBATION_SELECTOR/CR037A_result.md)<br>[CR037A_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037A_SAM_PERTURBATION_SELECTOR/CR037A_summary.json) | [All 6 files](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr037a-sam-perturbation-selector/README.md) |
| [`CR:CR037B@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr037b-parameter-free-cmb-shape-attempt/README.md) | [CR037B_PRECOMMIT.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037B_PARAMETER_FREE_CMB_SHAPE_ATTEMPT/CR037B_PRECOMMIT.md) | [CR037B_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037B_PARAMETER_FREE_CMB_SHAPE_ATTEMPT/CR037B_runner.py) | [CR037B_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037B_PARAMETER_FREE_CMB_SHAPE_ATTEMPT/CR037B_runner.py)<br>[CR037B_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037B_PARAMETER_FREE_CMB_SHAPE_ATTEMPT/CR037B_result.md)<br>[CR037B_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037B_PARAMETER_FREE_CMB_SHAPE_ATTEMPT/CR037B_summary.json) | [CR037B_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037B_PARAMETER_FREE_CMB_SHAPE_ATTEMPT/CR037B_result.md)<br>[CR037B_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037B_PARAMETER_FREE_CMB_SHAPE_ATTEMPT/CR037B_summary.json) | [All 10 files](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr037b-parameter-free-cmb-shape-attempt/README.md) |
| [`CR:CR037C@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr037c-parameter-free-act-dr4-independence/README.md) | [CR037C_PRECOMMIT.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037C_PARAMETER_FREE_ACT_DR4_INDEPENDENCE/CR037C_PRECOMMIT.md) | [CR037C_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037C_PARAMETER_FREE_ACT_DR4_INDEPENDENCE/CR037C_runner.py) | [CR037C_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037C_PARAMETER_FREE_ACT_DR4_INDEPENDENCE/CR037C_runner.py)<br>[CR037C_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037C_PARAMETER_FREE_ACT_DR4_INDEPENDENCE/CR037C_result.md)<br>[CR037C_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037C_PARAMETER_FREE_ACT_DR4_INDEPENDENCE/CR037C_summary.json) | [CR037C_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037C_PARAMETER_FREE_ACT_DR4_INDEPENDENCE/CR037C_result.md)<br>[CR037C_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR037C_PARAMETER_FREE_ACT_DR4_INDEPENDENCE/CR037C_summary.json) | [All 6 files](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr037c-parameter-free-act-dr4-independence/README.md) |
| [`CR:CR038@19`](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr038-branch-verdict-zipper-parameter-free-cmb-shape/README.md) | [CR038_PRECOMMIT.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR038_BRANCH_VERDICT_ZIPPER_PARAMETER_FREE_CMB_SHAPE/CR038_PRECOMMIT.md) | [CR038_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR038_BRANCH_VERDICT_ZIPPER_PARAMETER_FREE_CMB_SHAPE/CR038_runner.py) | [CR038_runner.py](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR038_BRANCH_VERDICT_ZIPPER_PARAMETER_FREE_CMB_SHAPE/CR038_runner.py)<br>[CR038_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR038_BRANCH_VERDICT_ZIPPER_PARAMETER_FREE_CMB_SHAPE/CR038_result.md)<br>[CR038_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR038_BRANCH_VERDICT_ZIPPER_PARAMETER_FREE_CMB_SHAPE/CR038_summary.json) | [CR038_result.md](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR038_BRANCH_VERDICT_ZIPPER_PARAMETER_FREE_CMB_SHAPE/CR038_result.md)<br>[CR038_summary.json](../../courtroom/19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR038_BRANCH_VERDICT_ZIPPER_PARAMETER_FREE_CMB_SHAPE/CR038_summary.json) | [All 6 files](../../tests/courtroom/19-big-bang-substrate-derived-thermal-ladder-cr038-branch-verdict-zipper-parameter-free-cmb-shape/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000021`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/FULL_CMB_SHAPE_ROUTE.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000021 | Early-Universe Cosmology | Fixed-Cosmology CMB Shape, Perturbation Selector and Correction Zipper |

| Document field | Value |
|---|---|
| Purpose | Separate native-recombination and standard-recombination CMB lanes, carry the fixed SAM cosmology through Planck and ACT shape tests, and preserve the CR035A-to-CR035A2 correction and branch zipper. |
| Prerequisite documents | `SAMA-D000020` |
| Used by | Focused child of `SAMA-P000002`; supplies the full-shape cosmology handoff to `SAMA-D000023` and the Volume I synthesis. |
| Primary source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`, SHA-256 `2f22500f6583f567e350974610f00142e89b081a5b8c4c90c6dfe89bec43be0d`. |
| Courtroom pin | `iwtbotiwtwot/The_Courtroom` commit `b5e914f71377e86ef4c67e199973d9300795cda1`. |
| Revision state | Source-bound draft; mechanically registered proposal; not reviewed or approved. |

</details>
