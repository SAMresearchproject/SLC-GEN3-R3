[SAM](../../README.md) · [Volume I](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Galaxy Halos and Mass Distribution

## Current research connections — 14 September 2026

The global execution authority is SLC-GEN3-R3 / SLC-GEN3-CEV1-R3. The September 2026 research includes exact retained-history computation, RH arithmetic compensation, native Mersenne work, Starbreaker signed reception and ATOM3D contact/grammar. The research index connects the retained derivations to the latest code, results and current domain assignments.

[Current derivations, code and results](../../../docs/RESEARCH.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

A galaxy halo is not introduced by replacing the spherical source law. The
route begins by summing many individually nonzero source lifts:

\[
A_{\rm lift}(\mathbf x)
=
\sum_i
\frac{2GM_i}{c^2|\mathbf x-\mathbf x_i|}.
\]

For a spherical cumulative account this becomes

\[
A(<r)
=\frac{2GM(<r)}{c^2r}.
\]

Only after that source-conditioned field exists is a halo observable applied.
For circular support,

\[
V^2(r)=\frac{GM(<r)}r,
\qquad
A(<r)=\frac{2V^2(r)}{c^2}.
\]

The conceptual picture is a field assembled from many source contributions,
an inventory that says what supplies the clustered mass, and a radial readout
that asks how the assembled field is organized across a galaxy. Those are
three different questions. The branch history progressively isolated them:
first the many-source grammar, then the BB-origin versus post-BB inventory
split, then real SPARC residuals and clustered profile contact, then a
population radial law, a preserved below-threshold control result, its
statistical appeal, and finally a substrate \(X_\infty\) identity used for
outer-radius mass placement.

## 1. Opening question and conceptual picture

This chapter answers:

> How does Volume I proceed from the universal floor and single-source lift
> to a many-source galaxy field, separate clean cosmic inventory from the
> historical BB-PBH/trapped-\(A\) halo lane, expose the route to 175 SPARC
> galaxies, preserve the post-BB and uniform wrong controls, carry the
> radial-law control-threshold miss through its correction, and state exactly what remains
> open without importing current ATOM3D calibration?

The start-to-finish map is

\[
\begin{aligned}
\text{source lifts}
&\longrightarrow
\text{many-source accumulation}\\
&\longrightarrow
\text{typed halo inventory}\\
&\longrightarrow
\text{SPARC baryon residual}\\
&\longrightarrow
\text{clustered profile and seed-first scaffold}\\
&\longrightarrow
X(r)\text{ population law}\\
&\longrightarrow
X_\infty\text{ identity}\\
&\longrightarrow
M_{\rm halo}(<R_{\rm outer}).
\end{aligned}
\]

No arrow authorizes the next one automatically. Each arrow has its own
evidence, controls and remaining boundary.

## 2. Definitions, domains and units

| Quantity | Definition | Type | Units/domain |
|---|---|---|---|
| \(A_0\) | \(1/(12\pi)\) | universal floor | dimensionless |
| \(A_i(\mathbf x)\) | \(2GM_i/[c^2|\mathbf x-\mathbf x_i|]\) | source-conditioned lift | dimensionless |
| \(A_{\rm lift}\) | \(\sum_iA_i\) | many-source field before readout | dimensionless |
| \(M(<r)\) | total declared source mass inside radius \(r\) | cumulative source inventory | mass |
| \(V_{\rm obs}\) | observed circular-speed row | measured readout | km s\(^{-1}\) |
| \(V_{\rm bar}\) | gas, disk and bulge support under declared mass-to-light ratios | baryon model readout | km s\(^{-1}\) |
| \(V_{\rm dark}^2\) | \(V_{\rm obs}^2-V_{\rm bar}^2\) | residual support | km\(^2\) s\(^{-2}\) |
| \(X(r)\) | \(V_{\rm dark}^2/V_{\rm bar}^2\) | radial halo-to-baryon ratio | dimensionless |
| \(f_{\rm halo}\) | \(V_{\rm dark}^2/V_{\rm obs}^2=X/(1+X)\) | dark fraction in squared-speed support | dimensionless |
| \(X_\infty\) | \((R-\alpha_H)\Omega_m=10/\pi\) | outer population identity | dimensionless |
| \(R_{\rm outer}\) | outer measured galaxy radius | catalog geometry | kpc |
| \(\Omega_{\rm BB\text{-}PBH,A}\) | branch-08 BB-origin PBH/trapped-\(A\) inventory | historical application inventory | dimensionless fraction |
| \(\Omega_{\rm postBB}\) | bounded post-BB/window subchannel | wrong-control inventory for full-halo use | dimensionless fraction |

The radix \(R=12\) and the physical radius \(R_{\rm outer}\) share a letter in
the source lineage but not a type. Whenever both occur in one equation, this
chapter writes the physical radius with the `outer` subscript.

The universal \(A_0\) is part of the total account. A spatially uniform
contribution does not create a local gradient or replace the many-source lift.
The galaxy field is sourced by the nonuniform mass distribution.

## 3. From one source to many nonzero contributions

### 3.1 Single-source lift

For one spherical source,

\[
A_i(r_i)
=\frac{r_{s,i}}{r_i}
=\frac{2GM_i}{c^2r_i}.
\]

The quantity is dimensionless because \(GM_i/c^2\) has units of length.

### 3.2 Add before selecting the observable

In the weak many-source regime,

\[
\boxed{
A_{\rm lift}(\mathbf x)
=
\sum_i
\frac{2GM_i}{c^2|\mathbf x-\mathbf x_i|}
}.
\]

Linearity belongs to field construction. A clock, photon road or circular
support operator is applied only afterward. Summing already transformed
readouts would answer a different question.

For spherical cumulative mass,

\[
M(<r)=\sum_{r_i<r}M_i,
\]

so

\[
\boxed{
A(<r)
=\frac{2GM(<r)}{c^2r}
}.
\]

### 3.3 Connect accumulation to circular support

The circular-balance relation is

\[
\frac{V^2(r)}r=\frac{GM(<r)}{r^2}.
\]

Multiplying by \(r\) gives

\[
V^2(r)=\frac{GM(<r)}r.
\]

Substituting this into the cumulative lift yields

\[
\boxed{
A(<r)=\frac{2V^2(r)}{c^2}
}.
\]

This is a readout bridge. It does not say that \(A\) has velocity units, and
it does not make a rotation curve the definition of the substrate field.

## 4. Construct the SPARC residual

The fixed baryonic support used in the source chain is

\[
V_{\rm bar}^2
=
\operatorname{sgn}(V_{\rm gas})V_{\rm gas}^2
+\Upsilon_{\rm disk}V_{\rm disk}^2
+\Upsilon_{\rm bulge}V_{\rm bulge}^2,
\]

with

\[
\Upsilon_{\rm disk}=0.5,
\qquad
\Upsilon_{\rm bulge}=0.7.
\]

The residual is

\[
\boxed{
V_{\rm dark}^2
=V_{\rm obs}^2-V_{\rm bar}^2
}.
\]

The squared-speed fraction is

\[
f_{\rm dark}
=\frac{V_{\rm dark}^2}{V_{\rm obs}^2}.
\]

If

\[
X=\frac{V_{\rm dark}^2}{V_{\rm bar}^2},
\]

then

\[
V_{\rm obs}^2
=V_{\rm bar}^2(1+X),
\]

and therefore

\[
\boxed{
f_{\rm dark}
=\frac{X}{1+X}
}.
\]

This algebra later links the SPARC outer fraction to \(X_\infty\).

## 5. Keep clean and historical application inventories separate

The clean Volume I inventory is

\[
\Omega_m=\frac1\pi,
\qquad
\Omega_b=2A_0(1-\chi),
\qquad
\Omega_c=\Omega_m-\Omega_b.
\]

The historical branch-08 application carried

\[
\Omega_{\rm BB\text{-}PBH,A}
=0.26446190430295646
\]

for its BB-origin PBH/trapped-\(A\) halo lane and

\[
\Omega_{\rm postBB}
=0.02576714268055339
\]

for a bounded post-BB/window subchannel.

These are not silently exchanged with the clean \(\Omega_c\) identity. The
clean inventory owns the universal account. The branch values belong to the
declared historical halo operator and its tests. The distinction is
especially important because the post-BB number is a subchannel fraction, not
the complete halo inventory.

## 6. Historical halo inventory and organization discovery

### 6.1 Real-data residual and partial-inventory bound

`G:G392@SAM-ARCHIVE` loaded 175 SPARC galaxies and 3,391 mass-model points.
It recorded

\[
\operatorname{median}
\left(
\frac{V_{\rm dark}^2}{V_{\rm obs}^2}
\right)_{\rm outer}
=0.760699023482704.
\]

The selected post-BB window envelope supplied only

\[
2.576714268055339\%
\]

of that dark residual. Its source verdict is
`G392_PASS_REAL_SPARC_A_ACCUMULATION_PBH_INVENTORY_BOUND`. The result
localized a real residual and a partial-inventory bound; it did not yet supply
the organization law.

### 6.2 Write the forward stack and expose the missing selector

`G:G393@SAM-ARCHIVE` ordered the components:

\[
A_{\rm baryon},
\quad
A_{\rm baryon,many},
\quad
A_{\rm postBB},
\quad
A_{\rm postBB,many},
\quad
\text{organization response}.
\]

After the post-BB envelope, the recorded missing fraction of the dark
residual was

\[
97.42328573194466\%.
\]

Its source verdict,
`G393_PASS_STACK_LOCALIZES_ORGANIZATION_SELECTOR`, identifies the remaining
question as radial organization, mass-spectrum normalization and response
gradient.

### 6.3 Test a clustered compatibility profile

`G:G394@SAM-ARCHIVE` used a pseudo-isothermal clustered profile as the
comparison family. The tested halo operator was

\[
V_{\rm iso}^2(r;V_\infty,r_c)
=
V_\infty^2
\left[
1-\frac{r_c}{r}\arctan\!\left(\frac r{r_c}\right)
\right].
\]

The forward comparison kept the Lelli baryon conversion fixed,

\[
V_{\rm bar}^2
=V_{\rm gas}|V_{\rm gas}|
+0.5V_{\rm disk}^2
+0.7V_{\rm bulge}^2,
\]

and formed

\[
V_{\rm total,pred}^2(r)
=V_{\rm bar}^2(r)+V_{\rm iso}^2(r;V_\infty,r_c).
\]

Here \(V_\infty\) in km s\(^{-1}\) and \(r_c\) in kpc were the two
per-galaxy fitted comparison parameters, bounded in the archived runner by
\(0\leq V_\infty\leq600\) and \(0.01\leq r_c\leq300\). The gas, disk and
bulge conversion factors were fixed rather than fitted. Thus this is a
reconstructible fitted compatibility profile, not a parameter-free native
halo law.

The optimizer is also part of the tested operator. For every galaxy with at
least four valid positive-radius, positive-observed-speed rows, define

\[
\epsilon_i(V_\infty,r_c)
=\frac{
\sqrt{\max[V_{{\rm bar},i}^2+V_{\rm iso}^2(r_i),0]}-V_{{\rm obs},i}
}{\max(eV_{{\rm obs},i},1\ \mathrm{km\,s^{-1}})}.
\]

`least_squares` minimizes the vector \(\epsilon_i\), starting from

\[
V_{\infty,0}
=\max\!\left(
\sqrt{\max[V_{{\rm obs},\mathrm{outer}}^2
-V_{{\rm bar},\mathrm{outer}}^2,0]},
5\ \mathrm{km\,s^{-1}}
\right),
\qquad
r_{c,0}=\max\!\left(\frac{\operatorname{median}r_i}{2},0.2\ \mathrm{kpc}\right),
\]

with at most 2,000 function evaluations. The baryon and halo chi-squared
statistics are sums of squared weighted residuals; the fitted-profile reduced
value uses \(N-2\) degrees of freedom. The reported RMS values are instead
unweighted speed residuals in km s\(^{-1}\). The declared profile gate was

\[
\operatorname{median}
\left(\frac{\chi^2_{\rm baryon}}{\chi^2_{\rm halo}}\right)>3
\quad\text{and}\quad
\operatorname{medianRMS}_{\rm halo}
<\operatorname{medianRMS}_{\rm baryon}.
\]

Both clauses passed. Across all 175 galaxies it recorded

\[
\operatorname{median RMS}_{\rm baryon}
=40.95236813050122\
\mathrm{km\,s^{-1}},
\]

\[
\operatorname{median RMS}_{\rm halo}
=3.625430524040301\
\mathrm{km\,s^{-1}},
\]

and a median \(\chi^2\)-improvement factor of
\(150.7662388291606\). The clustered overdensity relative to the cosmic dark
mean was about \(7.9090\times10^4\).

Its source verdict is
`G394_PASS_BB_PBH_CLUSTERED_HALO_COMPATIBLE_PROFILE_OPEN`. “Compatible
profile” is the load-bearing phrase: the profile established contact while
leaving native radial organization, mass function and concentration open.

### 6.4 Test seed-first behavior and retain the better-fit diagnostic

`G:G677@SAM-ARCHIVE` removed the fitted \(V_\infty,r_c\) pair from the
candidate operator. Let

\[
g(x)=x-\arctan x,
\qquad
r_c=\frac{R_{\rm outer}}d,
\]

where \(d\) is the declared core denominator. The outer residual mass from
`G:G392@SAM-ARCHIVE` fixes the normalization:

\[
M(<r)
=M_{\rm outer}
\frac{g(r/r_c)}{g(R_{\rm outer}/r_c)},
\qquad
V_{\rm halo}^2(r)=\frac{G M(<r)}r.
\]

The total predicted speed is then

\[
V_{\rm pred}(r)
=\sqrt{V_{\rm bar}^2(r)+V_{\rm halo}^2(r)}.
\]

There is no per-galaxy profile fit in this seed-first operator:
\(M_{\rm outer}\) is measured residual normalization, \(d=12\) is the
declared primary row, and \(d=8,6,4,3\) are retained diagnostic alternatives.
The archived G394-fitted \(V_\infty,r_c\) values are loaded only for RMS
comparison and are explicitly not used in the seed construction.

The native base-12 candidate is therefore

\[
r_{\rm core}=\frac{R_{\rm outer}}{12}.
\]

Across 173 galaxies it recorded

\[
\operatorname{median RMS}_{\rm seed}
=10.382222996690356\
\mathrm{km\,s^{-1}},
\]

closing

\[
0.8191375474184742
\]

of the baryon-to-clustered-profile RMS gap.

A comparison candidate

\[
r_{\rm core}=\frac{R_{\rm outer}}6
\]

had the lower median RMS, \(8.75365780845026\ \mathrm{km\,s^{-1}}\), but was
not promoted into a primitive law merely because it scored better. The
uniform-cosmic control closed only
\(3.8495994978147876\times10^{-5}\) of the gap, and the post-BB-only
base-12 control closed \(0.02448481593940179\).

The candidate and its wrong controls were decided by explicit gates rather
than visual preference:

| G677 condition | Exact gate or construction | Recorded outcome |
|---|---|---|
| primary speed error | \(\operatorname{medianRMS}_{\rm seed}<0.35\operatorname{medianRMS}_{\rm baryon}\) | PASS: \(10.3822<0.35(41.0879)\) km s\(^{-1}\) |
| improvement | median baryon/seed RMS improvement \(>2.5\) | PASS: \(3.6524042938317947\) |
| gap closure | baryon-to-G394 RMS gap closed \(\geq0.65\) | PASS: \(0.8191375474184742\) |
| WC1 uniform cosmic mean | its RMS must exceed twice the primary RMS | PASS: \(40.9509>2(10.3822)\) km s\(^{-1}\) |
| WC2 post-BB/window-only mass | its RMS must exceed twice the primary RMS | PASS: \(40.1701>2(10.3822)\) km s\(^{-1}\) |
| WC3 fitted-profile leakage | G394-fitted \(V_\infty,r_c\) must not enter the seed operator | PASS: those columns are comparison-only and not consumed |
| WC4 reversed formation order | seed field must precede baryon infall | PASS: the ordering board is seed first, baryons second |
| WC5 constant-floor force | no constant-\(A_0\) velocity term may be inserted | PASS: only clustered seed mass enters the radial velocity term |

The verdict required all three primary conditions and all five wrong-control
rejections. The lower-RMS \(d=6\) row remained a diagnostic because it was
not the declared native base-12 candidate.

Its source verdict is
`G677_PASS_SEED_FIRST_CLUSTERING_SELECTOR_CANDIDATE__MASS_NORMALIZATION_AND_NATIVE_LAW_OPEN`.
The source-era label and its open boundary are retained without a new SAMA
classification.

## 7. Many-source inventory, SPARC profile and scaffold route

### 7.1 Structural root

[`CR:CR022@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr022-native-a-many-nonzero-accumulation/README.md) checked the many-source grammar directly. Its example compares

\[
A_{\rm single}=10^{-18}
\]

with

\[
\sum_iA_i=1.0000000000000001\times10^{-7}.
\]

Each contribution is nonzero even when one is below a particular readout
threshold. The sum is formed before the observable is read. The source record
is `CLEAN`/`BOUNDARY` because this structural root alone does not close a
galaxy observation.

### 7.2 Inventory split

[`CR:CR023@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr023-bb-pbh-trapped-a-inventory/README.md) records:

\[
\Omega_{\rm BB\text{-}PBH,A}
=0.26446190430295646,
\]

\[
\frac{\Omega_{\rm BB\text{-}PBH,A}}
{\Omega_{\rm hydrogen}}
=5.364446416084761,
\]

while the post-BB/window subchannel remains
\(0.02576714268055339\). The source record is `CLEAN`/`BOUNDARY`. It
supports the inventory ordering without claiming that the smaller subchannel
supplies the full halo.

### 7.3 Real SPARC wrong-control rejection

[`CR:CR024@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr024-real-sparc-residual-and-post-bb-rejection/README.md) replays 175 galaxies and 3,391 points. It records the median
outer dark fraction

\[
0.760699023482704
\]

and the post-BB contribution of only

\[
2.576714268055339\%
\]

of the required dark residual. The missing portion is

\[
97.42328573194466\%.
\]

Thus post-BB-only is an explicit wrong control for the full-halo inventory,
not an omitted alternative.

### 7.4 Clustered profile contact

[`CR:CR025@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr025-clustered-bb-pbh-profile-contact/README.md) carries the clustered comparison into the registered branch:

\[
40.95236813050122
\longrightarrow
3.625430524040301\
\mathrm{km\,s^{-1}}
\]

for the median RMS, with all 175 galaxy fits completed. The source record
preserves its `PASS` and the simultaneous radial-law boundary. This document
adds no separate SAMA classification.

### 7.5 Seed-first selector and wrong controls

[`CR:CR026@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr026-seed-first-clustering-selector/README.md) selects the base-12 seed-first behavior as the declared native
candidate while retaining the \(R_{\rm outer}/6\) row as a comparison, not a
law. The uniform-cosmic and post-BB-only controls remain weak. This prevents
the discovery process from turning “best RMS among tried rows” into an
untyped primitive.

### 7.6 Hydrogen catch-up

[`CR:CR027@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr027-hydrogen-catchup-first-star-scaffold/README.md) orders the scaffold:

\[
\text{BB-origin PBH/trapped-}A\text{ wells first}
\longrightarrow
\text{hydrogen/normal baryons catch up}.
\]

It identifies neutral protium as the terminal arrival, proton-electron plasma
as the hot arrival and the PBH/trapped-\(A\) mass distribution as the first
scaffold. The scope is a route selector, not a complete star-formation
history.

### 7.7 Baryon-scaffold support remains separate

[`CR:CR028@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr028-qp042-baryon-scaffold-support/README.md) records private QP042 support for filled proton/neutron
three-constituent scaffolds without observed baryon masses or free
parameters. It is source `CLEAN`/`BOUNDARY` and explicitly is not external
halo evidence. QP042 has no direct qualified key in this Volume I manifest;
the registered route is the Courtroom wrapper in this paragraph. No test key
is invented.

## 8. Halo radial-law debt and update

### 8.1 Original debt ledger

[`CR:CR029@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr029-native-radial-law-debt-ledger/README.md) gathered the structural, inventory, SPARC, clustered-profile,
seed-first and baryon-catch-up steps and asked what had not yet been supplied.
It recorded the debt as:

\[
\boxed{
\text{native radial organization}
\;+\;
\text{mass function}
\;+\;
\text{concentration relation}
}.
\]

Its source `BOUNDARY` is successful debt localization. Treating support
artifacts as a completed native halo law would have failed the ledger's
purpose.

### 8.2 Later formal update

[`CR:CR029b@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr029b-native-radial-law-debt-ledger-formal-update/README.md) reads the later population chain and records three
population-level developments:

1. the \(X(r)\) organization is statistically separated from its permutation
   nulls;
2. outer-radius mass placement closes at the population median; and
3. \(X_\infty\) receives the substrate identity \(10/\pi\).

It also preserves four specific debts:

- per-galaxy scatter of about \(0.3791\) dex;
- prospective evaluation on a non-SPARC catalog;
- a closed-form concentration selector independent of each measured
  \(R_{\rm outer}\); and
- cross-catalog universality of the \(X(r)\) population law.

The update supplements the original ledger. It does not erase why the ledger
was written.

### 8.3 Branch zipper

[`CR:CR030@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr030-branch-verdict-zipper/README.md) zips the then-complete support route while retaining the radial
law open in that source-era state. Its source record is `CLEAN`/`PASS`. The
later population rows extend that history; they do not alter CR030 in place.

Branch-08 uses “current” in its own historical chronology. That word does not
install present-day physical-calibration authority. The current
[ATOM3D authority](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/SAM_LIVE/05_ATOM3D_CURRENT.md) names
`SLCQ2-RZ-A3D-SR3` as the sole primary/default quality pointer for its
structural route, while physical calibration remains uninstalled. The later
`NZA1` symbolic relation receipt used no galaxy-halo input. None of those
present-tense ATOM3D facts is inferred from this chapter's historical halo
lane.

## 9. Population appeal and per-galaxy mass placement

### 9.1 Define the radial population statistic and galaxy-equal operator

At every usable radius,

\[
\boxed{
X(r)=
\frac{V_{\rm dark}^2(r)}
{V_{\rm bar}^2(r)}
}.
\]

Normalize the radius by the outer measured radius:

\[
\rho=\frac r{R_{\rm outer}}.
\]

The population operator is reconstructible in five steps.

1. Use the five normalized-radius bins
   \([0,0.2)\), \([0.2,0.4)\), \([0.4,0.6)\), \([0.6,0.8)\) and
   \([0.8,1]\).
2. Compute signed \(X\) at every usable measured point. The baryon operator is
   \(V_{\rm gas}|V_{\rm gas}|+0.5V_{\rm disk}^2+0.7V_{\rm bulge}^2\);
   points with nonpositive baryon support are unusable.
3. Within each galaxy and bin, take the median of the pointwise \(X\) values.
4. For each bin, take the population median across those galaxy medians. This
   gives every represented galaxy one population vote rather than weighting a
   galaxy by its number of radial rows.
5. For spread only, retain positive per-galaxy/bin medians, transform them by
   \(\log_{10}\), and compute the population standard deviation with divisor
   \(N\). Nonpositive values remain counted in the audit fields but do not
   enter a logarithm.

The two continuous endpoint statistics are

\[
\Delta_X
=\widetilde X_{[0.8,1]}-\widetilde X_{[0,0.2)},
\]

and

\[
\Delta_\sigma
=\sigma_{\log_{10}X,[0.8,1]}
-\sigma_{\log_{10}X,[0,0.2)}.
\]

The population claim requires a positive radial rise and a negative spread
change; the corrected null test asks where those continuous values fall in
the corresponding permutation distributions.

The complete declared decision surface is:

| Predicate | Exact condition | CR031 | CR031b |
|---|---|---:|---:|
| P1 radial rise | \(\Delta_X>0\), Spearman \(>0\), and at least three of four adjacent bin rises | PASS | PASS |
| P2 outer plateau | outer median in \([2.5,4.5]\) and below the sealed rounded cosmic cap \(0.85(5.364)=4.5594\) | PASS | PASS |
| P3 convergence | \(\Delta_\sigma<0\) and at least three of four adjacent spread decreases | PASS | PASS |
| P4 within-galaxy null | exact one-sided endpoint-rise permutation \(p<0.01\) | not the original score | PASS: \(0.000999\) |
| P5 randomized-radius null | exact one-sided spread-contraction permutation \(p<0.01\) | not the original score | PASS: \(0.000999\) |
| soft WC1 | \(\Upsilon_{\rm disk}=0.3,\ \Upsilon_{\rm bulge}=0.7\); P1 and P3 retained | PASS | PASS |
| soft WC2 | \(\Upsilon_{\rm disk}=0.7,\ \Upsilon_{\rm bulge}=0.7\); P1 and P3 retained | PASS | PASS |

CR031b's aggregate PASS required P1 through P5 plus both soft controls.
CR031's different hard-kill rule required at least \(95\%\) of WC3 trials
to destroy P1 and at least \(95\%\) of WC4 trials to destroy P3. Those two
kill fractions were \(83.9\%\) and \(80.8\%\), so the first result remained
`BOUNDARY` even though P1 through P3 and the soft controls passed.

### 9.2 Preserve the first result below its control threshold

[`CR:CR031@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr031-x-radial-law-population-test/README.md) loaded 175 galaxies and 3,391 radial points. Its five bin
medians were

\[
(1.1513,\ 1.7271,\ 2.4224,\ 2.6832,\ 3.1225),
\]

with Spearman coefficient \(+1.000\). The log-spread sequence was

\[
(0.6137,\ 0.4477,\ 0.4347,\ 0.4042,\ 0.3960),
\]

so the median rose and the cross-galaxy spread contracted toward the outer
edge.

The predeclared hard-control rule required the canonical signature to fail in
at least \(95\%\) of shuffled trials. The within-galaxy shuffle produced
\(83.9\%\), and the galaxy-randomized-\(\rho\) control produced \(80.8\%\).
Those rows missed the declared threshold, so the source verdict remained
`BOUNDARY`. The signal rows were not deleted or relabeled.

### 9.3 Correct the statistical comparison

The first control asked for the fraction of trials that failed a compound
pass/fail signature. The appeal instead located the observed continuous
statistics inside their own null distributions while keeping the same
canonical data and \(X(r)\) organization.

[`CR:CR031b@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr031b-x-radial-law-null-percentile-appeal/README.md) reports:

- zero of 1,000 within-galaxy shuffles matched or exceeded the canonical
  endpoint rise \(\Delta_X=1.9712194780646453\);
- zero of 1,000 randomized-\(\rho\) trials matched or exceeded the canonical
  spread contraction \(\Delta_\sigma=-0.2176778647899893\); and
- exact one-sided permutation values
  \((0+1)/(1000+1)=0.000999000999\ldots\) for both controls, satisfying the
  predeclared \(p<0.01\) gates.

Thus the chain is

\[
\text{canonical signal}
\to
\text{control threshold miss}
\to
\text{preserved boundary record}
\to
\text{null-distribution appeal}
\to
\text{corrected population result}.
\]

The appeal supplements the first run. It does not manufacture a new dataset,
change the mass-to-light ratios or fit one radial law per galaxy.

### 9.4 Derive the outer identity

The substrate identity is

\[
X_{\infty,\rm SAM}
=(R-\alpha_H)\Omega_m.
\]

Insert

\[
R=12,
\qquad
\alpha_H=2,
\qquad
\Omega_m=\frac1\pi.
\]

Then

\[
\boxed{
X_{\infty,\rm SAM}
=(12-2)\frac1\pi
=\frac{10}{\pi}
=3.183098861837907\ldots
}.
\]

The corresponding dark fraction is

\[
f_{\infty,\rm halo}
=\frac{X_\infty}{1+X_\infty}
=\frac{10}{\pi+10}
=0.7609427763893117\ldots.
\]

The earlier sealed rounded input \(X_\infty=3.18\) instead gives
\(3.18/4.18=0.7607655502392344\ldots\), which is the source of the
approximately \(0.760766\) value in the predecessor mass-placement lane.
Both are close to, but distinct from, the raw-SPARC outer median
\(0.760699023482704\); none of the three values is silently substituted for
another.

### 9.5 Derive outer-radius halo mass

At \(R_{\rm outer}\),

\[
V_{\rm dark}^2
=X_\infty V_{\rm bar}^2.
\]

The circular mass relation gives

\[
M_{\rm halo}(<R_{\rm outer})
=\frac{R_{\rm outer}V_{\rm dark}^2(R_{\rm outer})}{G}.
\]

The executed catalog calculation uses

\[
G=4.30091\times10^{-6}\
\mathrm{kpc}\,(\mathrm{km\,s^{-1}})^2\,M_\odot^{-1}.
\]

Substitute the ratio:

\[
\boxed{
M_{\rm halo}(<R_{\rm outer})
=
\frac{
R_{\rm outer}
X_\infty
V_{\rm bar}^2(R_{\rm outer})
}{G}
}.
\]

[`CR:CR032@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr032-sam-native-per-galaxy-halo-mass-derivation/README.md) applied the earlier sealed \(X_\infty=3.18\) value. Across 173
galaxies entering its median statistic it recorded

\[
\operatorname{median}
\left(
\frac{M_{\rm halo,predicted}}
{M_{\rm halo,measured}}
\right)
=
0.9983106800240439,
\]

with no per-galaxy fit. Its per-galaxy scatter remained about \(0.3791\) dex.
Random \(X_\infty\) and baryon-support permutations were retained as null
controls. These were reported evidence rather than additional load-bearing
gates: WC1 had 1 of 1,000 trials at least as tight, giving
\(p=(1+1)/(1000+1)=0.001998\), and WC2 had 7 of 1,000, giving
\(p=(7+1)/(1000+1)=0.007992\). All 175 parsed galaxies entered the outer-feature table; two with
zero measured halo mass were excluded from the positive-ratio logarithmic
median, leaving 173. The load-bearing gate was

\[
\left|
\operatorname{median}\log_{10}
\frac{M_{\rm halo,predicted}}{M_{\rm halo,measured}}
\right|
\leq0.05.
\]

[`CR:CR033@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr033-x-inf-substrate-derivation-identity/README.md) then evaluated the closed \(10/\pi\) identity from substrate
atoms without opening the forbidden earlier result files. It recorded

\[
\operatorname{median}
\left(
\frac{M_{\rm halo,SAM}}
{M_{\rm halo,measured}}
\right)
=0.999283518662
\]

and

\[
\left|
\operatorname{median}
\log_{10}
\frac{M_{\rm halo,SAM}}
{M_{\rm halo,measured}}
\right|
=0.000311275416.
\]

CR033 independently loaded 175 raw galaxies; none was excluded for fewer
than three radial points, all 175 passed parser validity, and the same two
zero-measured-halo rows were excluded from the positive-ratio P1 statistic.
Its load-bearing gate was again the exact
\(\lvert\operatorname{median}\log_{10}(M_{\rm halo,SAM}/
M_{\rm halo,measured})\rvert\leq0.05\) condition.

Its reported null controls were likewise not extra gates. The random-
\(X_\infty\) control had 1 of 1,000 trials at least as tight,
\(p=0.001998\); the baryon-support permutation had 4 of 1,000,
\(p=0.004995\).

CR033 is retrospective substrate identification recognized after the earlier
SPARC halo work, not a prospective pre-measurement prediction. Its
forbidden-file guard certifies that this execution reopened the raw SPARC
catalog without consuming CR025, CR031b, CR032 or CR205 result files; that
fresh execution discipline does not change the test's retrospective
chronology.

The first number belongs to the sealed \(3.18\) input; the second execution
uses the exact \(10/\pi\) identity. They are not averaged.

### 9.6 Locked-stack replay

[`LC:LC08`](../../tests/courtroom/16-the-last-campaign-lc08-halo-pbh-inventory-replay/README.md) restarts from the locked primitive stack and replays the many-source
grammar, inventory split, 175-galaxy SPARC residual and clustered-profile
numbers. It records 166/166 checks. It also rejects:

- configuration-as-law promotion;
- uniform/smooth PBH conflation;
- post-BB-only use as the full halo; and
- a claim that the entire native radial law is closed.

The registry exposes no structured status or verdict for this row, so the
pinned source artifact remains its detailed outcome authority. This chapter
adds no verdict and no SAMA classification.

## 10. Deviation chains and wrong controls

| Wrong or diagnostic route | Observed issue | Correction or retained boundary |
|---|---|---|
| Treat one tiny \(A_i\) as exactly zero | Removes a source contribution before accumulation. | Sum all nonzero source lifts, then apply the readout threshold. |
| Add already transformed observables | Changes field linearity into readout linearity. | Construct \(A_{\rm lift}\) before selecting the observable. |
| Use a uniform cosmic mean as the halo profile | G677 closes only \(3.85\times10^{-5}\) of the RMS gap. | Require clustered organization. |
| Use the post-BB/window envelope as the full halo | It supplies only \(2.5767\%\) of the dark residual. | Keep it as a bounded subchannel; retain the BB-origin inventory lane. |
| Promote \(R_{\rm outer}/6\) because it has the best tested RMS | Converts a diagnostic comparison into a primitive law. | Preserve the row; keep the native base-12 candidate and debt ledger explicit. |
| Treat the pseudo-isothermal comparison as the native law | Confuses compatibility with derivation. | Use it to measure contact while the native selector remains separate. |
| Treat private baryon-scaffold support as external halo evidence | Moves a matter-side construction into the data-comparison lane. | Route it only through the registered Courtroom wrapper and retain its boundary. |
| Delete the first radial-law control result | Hides why the statistical question was revised. | Preserve CR031 and append the CR031b null-percentile appeal. |
| Change \(X(r)\), data or mass-to-light ratios during appeal | Would create a new target-dependent statistic. | Retain the canonical signal; change only the null evaluation described in the appeal. |
| Fit \(X_\infty\) separately to each galaxy | Destroys the population-level identity. | Use the sealed common \(3.18\) or exact \(10/\pi\) value. |
| Treat population-median closure as per-galaxy precision | Ignores the recorded \(0.3791\)-dex scatter. | State population median and scatter separately. |
| Read historical branch “current” language as active authority | Bypasses the live-document contract. | Treat branch-08 chronology as historical; keep current ATOM3D calibration separate. |

## 11. Established result, exact evidence, forward connection and open boundary

The established conceptual and technical chain is

\[
\boxed{
A_{\rm lift}(\mathbf x)
=
\sum_i\frac{2GM_i}{c^2|\mathbf x-\mathbf x_i|}
}
\]

followed by

\[
\boxed{
X(r)=\frac{V_{\rm dark}^2(r)}{V_{\rm bar}^2(r)},
\qquad
X_{\infty,\rm SAM}=\frac{10}{\pi}
}
\]

and

\[
\boxed{
M_{\rm halo}(<R_{\rm outer})
=
\frac{
R_{\rm outer}
X_\infty
V_{\rm bar}^2(R_{\rm outer})
}{G}
}.
\]

Exact evidence is the 19-key sequence indexed below: four archived discovery
tests, 14 Courtroom rows and one locked-stack replay. It preserves the large
SPARC residual, the post-BB-only rejection, clustered-profile contact, the
seed-first candidate and its controls, the first population boundary, the
null-percentile correction, the common \(X_\infty\) identity and the
outer-radius population-median mass placement. No SAMA result classification
is assigned to these D22 rows.

The forward connection is to the Volume I synthesis as a galaxy-scale example
of source additivity, typed inventory and observable selection. Volume II owns
the detailed matter grammar; Volume III owns simulation and executable
history. The current
[ATOM3D authority](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/SAM_LIVE/05_ATOM3D_CURRENT.md) keeps
`SLCQ2-RZ-A3D-SR3` structural-primary scope separate from physical
calibration, which remains uninstalled; `NZA1` used no galaxy-halo input.

The specifically open boundary is per-galaxy scatter, prospective non-SPARC
evaluation, a closed-form concentration selector that does not consume each
catalog \(R_{\rm outer}\), cross-catalog universality of \(X(r)\), native mass
function/abundance development and any current physical calibration not
installed by the applicable live domain document.

## 12. Focused test and result index

Courtroom and Last Campaign links are pinned to commit
`b5e914f71377e86ef4c67e199973d9300795cda1`.

| Exact qualified key | Evidence role | Direct result | Test folder |
|---|---|---|---|
| `G:G392@SAM-ARCHIVE` | real-SPARC discovery premise | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G392_REAL_SPARC_PBH_HALO_INVENTORY_TEST/G392_summary.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G392_REAL_SPARC_PBH_HALO_INVENTORY_TEST) |
| `G:G393@SAM-ARCHIVE` | forward-stack construction | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G393_PBH_HALO_FORWARD_STACK_SELECTOR/G393_summary.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G393_PBH_HALO_FORWARD_STACK_SELECTOR) |
| `G:G394@SAM-ARCHIVE` | clustered-profile boundary | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G394_PBH_RADIAL_ORGANIZATION_PROFILE_TEST/G394_summary.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G394_PBH_RADIAL_ORGANIZATION_PROFILE_TEST) |
| `G:G677@SAM-ARCHIVE` | seed-first discovery result | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G677_BB_PBH_SEED_FIRST_CLUSTERING_SIMULATION/G677_summary.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/substrate_G_tests/G677_BB_PBH_SEED_FIRST_CLUSTERING_SIMULATION) |
| [`CR:CR022@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr022-native-a-many-nonzero-accumulation/README.md) | many-source construction | [result](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION/CR022_result.md) | [folder](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION) |
| [`CR:CR023@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr023-bb-pbh-trapped-a-inventory/README.md) | inventory premise | [result](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR023_BB_PBH_TRAPPED_A_INVENTORY/CR023_result.md) | [folder](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR023_BB_PBH_TRAPPED_A_INVENTORY) |
| [`CR:CR024@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr024-real-sparc-residual-and-post-bb-rejection/README.md) | post-BB wrong control | [result](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR024_REAL_SPARC_RESIDUAL_AND_POST_BB_REJECTION/CR024_result.md) | [folder](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR024_REAL_SPARC_RESIDUAL_AND_POST_BB_REJECTION) |
| [`CR:CR025@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr025-clustered-bb-pbh-profile-contact/README.md) | clustered-profile result | [result](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR025_CLUSTERED_BB_PBH_PROFILE_CONTACT/CR025_result.md) | [folder](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR025_CLUSTERED_BB_PBH_PROFILE_CONTACT) |
| [`CR:CR026@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr026-seed-first-clustering-selector/README.md) | seed-first selector control | [result](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR026_SEED_FIRST_CLUSTERING_SELECTOR/CR026_result.md) | [folder](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR026_SEED_FIRST_CLUSTERING_SELECTOR) |
| [`CR:CR027@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr027-hydrogen-catchup-first-star-scaffold/README.md) | hydrogen-catch-up result | [result](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR027_HYDROGEN_CATCHUP_FIRST_STAR_SCAFFOLD/CR027_result.md) | [folder](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR027_HYDROGEN_CATCHUP_FIRST_STAR_SCAFFOLD) |
| [`CR:CR028@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr028-qp042-baryon-scaffold-support/README.md) | scoped baryon-support boundary | [result](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR028_QP042_BARYON_SCAFFOLD_SUPPORT/CR028_result.md) | [folder](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR028_QP042_BARYON_SCAFFOLD_SUPPORT) |
| [`CR:CR029@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr029-native-radial-law-debt-ledger/README.md) | original debt ledger | [result](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029_NATIVE_RADIAL_LAW_DEBT_LEDGER/CR029_result.md) | [folder](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029_NATIVE_RADIAL_LAW_DEBT_LEDGER) |
| [`CR:CR029b@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr029b-native-radial-law-debt-ledger-formal-update/README.md) | formal debt correction | [result](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029b_NATIVE_RADIAL_LAW_DEBT_LEDGER_FORMAL_UPDATE/CR029b_result.md) | [folder](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029b_NATIVE_RADIAL_LAW_DEBT_LEDGER_FORMAL_UPDATE) |
| [`CR:CR030@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr030-branch-verdict-zipper/README.md) | branch zipper result | [result](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR030_BRANCH_VERDICT_ZIPPER/CR030_result.md) | [folder](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR030_BRANCH_VERDICT_ZIPPER) |
| [`CR:CR031@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr031-x-radial-law-population-test/README.md) | preserved population boundary predecessor and control-threshold miss | [result](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031_X_RADIAL_LAW_POPULATION_TEST/CR031_result.md) | [folder](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031_X_RADIAL_LAW_POPULATION_TEST) |
| [`CR:CR031b@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr031b-x-radial-law-null-percentile-appeal/README.md) | null-percentile correction/retest | [result](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031b_X_RADIAL_LAW_NULL_PERCENTILE_APPEAL/CR031b_result.md) | [folder](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031b_X_RADIAL_LAW_NULL_PERCENTILE_APPEAL) |
| [`CR:CR032@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr032-sam-native-per-galaxy-halo-mass-derivation/README.md) | per-galaxy mass-placement result | [result](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR032_SAM_NATIVE_PER_GALAXY_HALO_MASS_DERIVATION/CR032_result.md) | [folder](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR032_SAM_NATIVE_PER_GALAXY_HALO_MASS_DERIVATION) |
| [`CR:CR033@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr033-x-inf-substrate-derivation-identity/README.md) | \(X_\infty\) construction | [result](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR033_X_INF_SUBSTRATE_DERIVATION_IDENTITY/CR033_result.md) | [folder](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR033_X_INF_SUBSTRATE_DERIVATION_IDENTITY) |
| [`LC:LC08`](../../tests/courtroom/16-the-last-campaign-lc08-halo-pbh-inventory-replay/README.md) | locked-stack retest | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC08_HALO_PBH_INVENTORY_REPLAY/LC08_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN/LC08_HALO_PBH_INVENTORY_REPLAY) |

## 13. Atomic record index

| Record | Role in this chapter |
|---|---|
| `SAMA-C000001-R001` | Supplies the universal floor and local-cancellation boundary. |
| `SAMA-C000002-R001` | Supplies the spherical source lift. |
| `SAMA-C000038-R001` | Defines many-source additivity before readout. |
| `SAMA-C000092-R001` | Supplies the clean inventory and road/inventory distinction. |
| `SAMA-C000093-R001` | Keeps clean and effective inventory lanes separate. |
| `SAMA-C000111-R001` | Records the many-nonzero halo root. |
| `SAMA-C000112-R001` | Records the BB-origin versus post-BB split. |
| `SAMA-C000113-R001` | Records the SPARC residual and post-BB-only rejection. |
| `SAMA-C000114-R001` | Records clustered profile contact and its boundary. |
| `SAMA-C000115-R001` | Orders seed-first scaffold, baryon catch-up and private support. |
| `SAMA-C000116-R001` | Preserves the population result and appeal chain. |
| `SAMA-C000117-R001` | Supplies \(X_\infty\) and outer-radius mass placement. |
| `SAMA-C000118-R001` | Updates the debt ledger and enforces the current-calibration boundary. |
| `SAMA-C000122-R001` | Enforces the Volume I and cross-volume subject boundary. |
| `SAMA-C000124-R001` | Separates source-era chronology from current authority. |
| `SAMA-C000125-R001` | Preserves source status, classification and approval typing. |

## 14. External references and custody boundary

The raw mass-model catalog and its fixed stellar mass-to-light conventions
come from Lelli, McGaugh and Schombert, “SPARC: Mass Models for 175 Disk
Galaxies with Spitzer Photometry and Accurate Rotation Curves,” *The
Astronomical Journal* 152 (2016) 157,
[DOI 10.3847/0004-6256/152/6/157](https://doi.org/10.3847/0004-6256/152/6/157).
The exact rows consumed by this chapter remain the copies hashed and pinned
inside the G and Courtroom artifacts listed in Section 12.

This chapter adds no new external catalog, measurement claim or conventional-
halo comparator result. External-data meaning, row selection and comparator
custody remain with those source artifacts and their exact registry hashes.

## 15. Source chronology, revision and approval boundary

The archived G-stage labels and branch-08 source verdicts are preserved as
historical provenance. Executable artifacts control their numerical results.
`SAM_LIVE/07_SAMA_CURRENT.md` controls present-tense SAMA document, test-index
and approval authority.

This chapter does not install a current ATOM3D physical calibration, does not
move particle grammar from Volume II into Volume I and does not move
simulation machinery from Volume III into the substrate ontology.

`reviewed_and_approved` remains `false`; `approval` remains `null`. Exact
source recovery, hashes, test execution and mechanical validation do not
constitute owner approval. The non-self-referential content-hash authority is
the catalog record in
[`documents/catalog/document_records.jsonl`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/catalog/document_records.jsonl),
supplemented at final review by
`reports/THREE_VOLUME_OWNER_REVIEW_HANDOFF.json`
and its Markdown companion. Sean Brady's explicit decision against that exact
external hash is the only action that can change the approval state.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`CR:CR022@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr022-native-a-many-nonzero-accumulation/README.md) | [CR022_PRECOMMIT.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION/CR022_PRECOMMIT.md)<br>[CR022_declared_premises.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION/CR022_declared_premises.json) | [CR022_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION/CR022_runner.py) | [CR022_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION/CR022_runner.py)<br>[CR022_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION/CR022_result.md)<br>[CR022_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION/CR022_summary.json) | [CR022_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION/CR022_result.md)<br>[CR022_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR022_NATIVE_A_MANY_NONZERO_ACCUMULATION/CR022_summary.json) | [All 9 files](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr022-native-a-many-nonzero-accumulation/README.md) |
| [`CR:CR023@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr023-bb-pbh-trapped-a-inventory/README.md) | [CR023_PRECOMMIT.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR023_BB_PBH_TRAPPED_A_INVENTORY/CR023_PRECOMMIT.md)<br>[CR023_declared_premises.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR023_BB_PBH_TRAPPED_A_INVENTORY/CR023_declared_premises.json) | [CR023_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR023_BB_PBH_TRAPPED_A_INVENTORY/CR023_runner.py) | [CR023_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR023_BB_PBH_TRAPPED_A_INVENTORY/CR023_runner.py)<br>[CR023_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR023_BB_PBH_TRAPPED_A_INVENTORY/CR023_result.md)<br>[CR023_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR023_BB_PBH_TRAPPED_A_INVENTORY/CR023_summary.json) | [CR023_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR023_BB_PBH_TRAPPED_A_INVENTORY/CR023_result.md)<br>[CR023_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR023_BB_PBH_TRAPPED_A_INVENTORY/CR023_summary.json) | [All 9 files](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr023-bb-pbh-trapped-a-inventory/README.md) |
| [`CR:CR024@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr024-real-sparc-residual-and-post-bb-rejection/README.md) | [CR024_PRECOMMIT.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR024_REAL_SPARC_RESIDUAL_AND_POST_BB_REJECTION/CR024_PRECOMMIT.md)<br>[CR024_declared_premises.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR024_REAL_SPARC_RESIDUAL_AND_POST_BB_REJECTION/CR024_declared_premises.json) | [CR024_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR024_REAL_SPARC_RESIDUAL_AND_POST_BB_REJECTION/CR024_runner.py) | [CR024_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR024_REAL_SPARC_RESIDUAL_AND_POST_BB_REJECTION/CR024_runner.py)<br>[CR024_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR024_REAL_SPARC_RESIDUAL_AND_POST_BB_REJECTION/CR024_result.md)<br>[CR024_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR024_REAL_SPARC_RESIDUAL_AND_POST_BB_REJECTION/CR024_summary.json) | [CR024_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR024_REAL_SPARC_RESIDUAL_AND_POST_BB_REJECTION/CR024_result.md)<br>[CR024_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR024_REAL_SPARC_RESIDUAL_AND_POST_BB_REJECTION/CR024_summary.json) | [All 8 files](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr024-real-sparc-residual-and-post-bb-rejection/README.md) |
| [`CR:CR025@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr025-clustered-bb-pbh-profile-contact/README.md) | [CR025_PRECOMMIT.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR025_CLUSTERED_BB_PBH_PROFILE_CONTACT/CR025_PRECOMMIT.md)<br>[CR025_declared_premises.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR025_CLUSTERED_BB_PBH_PROFILE_CONTACT/CR025_declared_premises.json) | [CR025_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR025_CLUSTERED_BB_PBH_PROFILE_CONTACT/CR025_runner.py) | [CR025_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR025_CLUSTERED_BB_PBH_PROFILE_CONTACT/CR025_runner.py)<br>[CR025_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR025_CLUSTERED_BB_PBH_PROFILE_CONTACT/CR025_result.md)<br>[CR025_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR025_CLUSTERED_BB_PBH_PROFILE_CONTACT/CR025_summary.json) | [CR025_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR025_CLUSTERED_BB_PBH_PROFILE_CONTACT/CR025_result.md)<br>[CR025_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR025_CLUSTERED_BB_PBH_PROFILE_CONTACT/CR025_summary.json) | [All 8 files](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr025-clustered-bb-pbh-profile-contact/README.md) |
| [`CR:CR026@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr026-seed-first-clustering-selector/README.md) | [CR026_PRECOMMIT.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR026_SEED_FIRST_CLUSTERING_SELECTOR/CR026_PRECOMMIT.md)<br>[CR026_declared_premises.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR026_SEED_FIRST_CLUSTERING_SELECTOR/CR026_declared_premises.json) | [CR026_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR026_SEED_FIRST_CLUSTERING_SELECTOR/CR026_runner.py) | [CR026_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR026_SEED_FIRST_CLUSTERING_SELECTOR/CR026_runner.py)<br>[CR026_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR026_SEED_FIRST_CLUSTERING_SELECTOR/CR026_result.md)<br>[CR026_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR026_SEED_FIRST_CLUSTERING_SELECTOR/CR026_summary.json) | [CR026_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR026_SEED_FIRST_CLUSTERING_SELECTOR/CR026_result.md)<br>[CR026_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR026_SEED_FIRST_CLUSTERING_SELECTOR/CR026_summary.json) | [All 8 files](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr026-seed-first-clustering-selector/README.md) |
| [`CR:CR027@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr027-hydrogen-catchup-first-star-scaffold/README.md) | [CR027_PRECOMMIT.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR027_HYDROGEN_CATCHUP_FIRST_STAR_SCAFFOLD/CR027_PRECOMMIT.md)<br>[CR027_declared_premises.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR027_HYDROGEN_CATCHUP_FIRST_STAR_SCAFFOLD/CR027_declared_premises.json) | [CR027_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR027_HYDROGEN_CATCHUP_FIRST_STAR_SCAFFOLD/CR027_runner.py) | [CR027_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR027_HYDROGEN_CATCHUP_FIRST_STAR_SCAFFOLD/CR027_runner.py)<br>[CR027_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR027_HYDROGEN_CATCHUP_FIRST_STAR_SCAFFOLD/CR027_result.md)<br>[CR027_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR027_HYDROGEN_CATCHUP_FIRST_STAR_SCAFFOLD/CR027_summary.json) | [CR027_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR027_HYDROGEN_CATCHUP_FIRST_STAR_SCAFFOLD/CR027_result.md)<br>[CR027_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR027_HYDROGEN_CATCHUP_FIRST_STAR_SCAFFOLD/CR027_summary.json) | [All 8 files](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr027-hydrogen-catchup-first-star-scaffold/README.md) |
| [`CR:CR028@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr028-qp042-baryon-scaffold-support/README.md) | [CR028_PRECOMMIT.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR028_QP042_BARYON_SCAFFOLD_SUPPORT/CR028_PRECOMMIT.md)<br>[CR028_declared_premises.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR028_QP042_BARYON_SCAFFOLD_SUPPORT/CR028_declared_premises.json) | [CR028_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR028_QP042_BARYON_SCAFFOLD_SUPPORT/CR028_runner.py) | [CR028_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR028_QP042_BARYON_SCAFFOLD_SUPPORT/CR028_runner.py)<br>[CR028_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR028_QP042_BARYON_SCAFFOLD_SUPPORT/CR028_result.md)<br>[CR028_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR028_QP042_BARYON_SCAFFOLD_SUPPORT/CR028_summary.json) | [CR028_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR028_QP042_BARYON_SCAFFOLD_SUPPORT/CR028_result.md)<br>[CR028_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR028_QP042_BARYON_SCAFFOLD_SUPPORT/CR028_summary.json) | [All 8 files](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr028-qp042-baryon-scaffold-support/README.md) |
| [`CR:CR029@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr029-native-radial-law-debt-ledger/README.md) | [CR029_PRECOMMIT.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029_NATIVE_RADIAL_LAW_DEBT_LEDGER/CR029_PRECOMMIT.md)<br>[CR029_declared_premises.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029_NATIVE_RADIAL_LAW_DEBT_LEDGER/CR029_declared_premises.json) | [CR029_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029_NATIVE_RADIAL_LAW_DEBT_LEDGER/CR029_runner.py) | [CR029_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029_NATIVE_RADIAL_LAW_DEBT_LEDGER/CR029_runner.py)<br>[CR029_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029_NATIVE_RADIAL_LAW_DEBT_LEDGER/CR029_result.md)<br>[CR029_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029_NATIVE_RADIAL_LAW_DEBT_LEDGER/CR029_summary.json) | [CR029_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029_NATIVE_RADIAL_LAW_DEBT_LEDGER/CR029_result.md)<br>[CR029_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029_NATIVE_RADIAL_LAW_DEBT_LEDGER/CR029_summary.json) | [All 8 files](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr029-native-radial-law-debt-ledger/README.md) |
| [`CR:CR029b@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr029b-native-radial-law-debt-ledger-formal-update/README.md) | [CR029b_PRECOMMIT.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029b_NATIVE_RADIAL_LAW_DEBT_LEDGER_FORMAL_UPDATE/CR029b_PRECOMMIT.md) | [CR029b_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029b_NATIVE_RADIAL_LAW_DEBT_LEDGER_FORMAL_UPDATE/CR029b_runner.py) | [CR029b_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029b_NATIVE_RADIAL_LAW_DEBT_LEDGER_FORMAL_UPDATE/CR029b_runner.py)<br>[CR029b_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029b_NATIVE_RADIAL_LAW_DEBT_LEDGER_FORMAL_UPDATE/CR029b_result.md)<br>[CR029b_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029b_NATIVE_RADIAL_LAW_DEBT_LEDGER_FORMAL_UPDATE/CR029b_summary.json) | [CR029b_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029b_NATIVE_RADIAL_LAW_DEBT_LEDGER_FORMAL_UPDATE/CR029b_result.md)<br>[CR029b_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR029b_NATIVE_RADIAL_LAW_DEBT_LEDGER_FORMAL_UPDATE/CR029b_summary.json) | [All 6 files](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr029b-native-radial-law-debt-ledger-formal-update/README.md) |
| [`CR:CR030@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr030-branch-verdict-zipper/README.md) | [CR030_PRECOMMIT.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR030_BRANCH_VERDICT_ZIPPER/CR030_PRECOMMIT.md)<br>[CR030_declared_premises.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR030_BRANCH_VERDICT_ZIPPER/CR030_declared_premises.json) | [CR030_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR030_BRANCH_VERDICT_ZIPPER/CR030_runner.py) | [CR030_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR030_BRANCH_VERDICT_ZIPPER/CR030_runner.py)<br>[CR030_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR030_BRANCH_VERDICT_ZIPPER/CR030_result.md)<br>[CR030_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR030_BRANCH_VERDICT_ZIPPER/CR030_summary.json) | [CR030_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR030_BRANCH_VERDICT_ZIPPER/CR030_result.md)<br>[CR030_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR030_BRANCH_VERDICT_ZIPPER/CR030_summary.json) | [All 8 files](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr030-branch-verdict-zipper/README.md) |
| [`CR:CR031@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr031-x-radial-law-population-test/README.md) | [CR031_PRECOMMIT.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031_X_RADIAL_LAW_POPULATION_TEST/CR031_PRECOMMIT.md)<br>[CR031_declared_premises.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031_X_RADIAL_LAW_POPULATION_TEST/CR031_declared_premises.json) | [CR031_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031_X_RADIAL_LAW_POPULATION_TEST/CR031_runner.py) | [CR031_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031_X_RADIAL_LAW_POPULATION_TEST/CR031_runner.py)<br>[CR031_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031_X_RADIAL_LAW_POPULATION_TEST/CR031_result.md)<br>[CR031_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031_X_RADIAL_LAW_POPULATION_TEST/CR031_summary.json) | [CR031_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031_X_RADIAL_LAW_POPULATION_TEST/CR031_result.md)<br>[CR031_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031_X_RADIAL_LAW_POPULATION_TEST/CR031_summary.json) | [All 8 files](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr031-x-radial-law-population-test/README.md) |
| [`CR:CR031b@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr031b-x-radial-law-null-percentile-appeal/README.md) | [CR031b_PRECOMMIT.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031b_X_RADIAL_LAW_NULL_PERCENTILE_APPEAL/CR031b_PRECOMMIT.md)<br>[CR031b_declared_premises.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031b_X_RADIAL_LAW_NULL_PERCENTILE_APPEAL/CR031b_declared_premises.json) | [CR031b_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031b_X_RADIAL_LAW_NULL_PERCENTILE_APPEAL/CR031b_runner.py) | [CR031b_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031b_X_RADIAL_LAW_NULL_PERCENTILE_APPEAL/CR031b_runner.py)<br>[CR031b_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031b_X_RADIAL_LAW_NULL_PERCENTILE_APPEAL/CR031b_result.md)<br>[CR031b_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031b_X_RADIAL_LAW_NULL_PERCENTILE_APPEAL/CR031b_summary.json) | [CR031b_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031b_X_RADIAL_LAW_NULL_PERCENTILE_APPEAL/CR031b_result.md)<br>[CR031b_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR031b_X_RADIAL_LAW_NULL_PERCENTILE_APPEAL/CR031b_summary.json) | [All 8 files](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr031b-x-radial-law-null-percentile-appeal/README.md) |
| [`CR:CR032@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr032-sam-native-per-galaxy-halo-mass-derivation/README.md) | [CR032_PRECOMMIT.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR032_SAM_NATIVE_PER_GALAXY_HALO_MASS_DERIVATION/CR032_PRECOMMIT.md)<br>[CR032_declared_premises.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR032_SAM_NATIVE_PER_GALAXY_HALO_MASS_DERIVATION/CR032_declared_premises.json) | [CR032_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR032_SAM_NATIVE_PER_GALAXY_HALO_MASS_DERIVATION/CR032_runner.py) | [CR032_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR032_SAM_NATIVE_PER_GALAXY_HALO_MASS_DERIVATION/CR032_runner.py)<br>[CR032_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR032_SAM_NATIVE_PER_GALAXY_HALO_MASS_DERIVATION/CR032_result.md)<br>[CR032_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR032_SAM_NATIVE_PER_GALAXY_HALO_MASS_DERIVATION/CR032_summary.json) | [CR032_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR032_SAM_NATIVE_PER_GALAXY_HALO_MASS_DERIVATION/CR032_result.md)<br>[CR032_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR032_SAM_NATIVE_PER_GALAXY_HALO_MASS_DERIVATION/CR032_summary.json) | [All 8 files](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr032-sam-native-per-galaxy-halo-mass-derivation/README.md) |
| [`CR:CR033@08`](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr033-x-inf-substrate-derivation-identity/README.md) | [CR033_PRECOMMIT.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR033_X_INF_SUBSTRATE_DERIVATION_IDENTITY/CR033_PRECOMMIT.md) | [CR033_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR033_X_INF_SUBSTRATE_DERIVATION_IDENTITY/CR033_runner.py) | [CR033_runner.py](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR033_X_INF_SUBSTRATE_DERIVATION_IDENTITY/CR033_runner.py)<br>[CR033_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR033_X_INF_SUBSTRATE_DERIVATION_IDENTITY/CR033_result.md)<br>[CR033_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR033_X_INF_SUBSTRATE_DERIVATION_IDENTITY/CR033_summary.json) | [CR033_result.md](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR033_X_INF_SUBSTRATE_DERIVATION_IDENTITY/CR033_result.md)<br>[CR033_summary.json](../../courtroom/08_GALAXY_HALOS_BB_PBH_TRAPPED_A/CR033_X_INF_SUBSTRATE_DERIVATION_IDENTITY/CR033_summary.json) | [All 8 files](../../tests/courtroom/08-galaxy-halos-bb-pbh-trapped-a-cr033-x-inf-substrate-derivation-identity/README.md) |
| [`LC:LC08`](../../tests/courtroom/16-the-last-campaign-lc08-halo-pbh-inventory-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc08-halo-pbh-inventory-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc08-halo-pbh-inventory-replay/README.md) | [LC08_seed_candidate_rows.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC08_HALO_PBH_INVENTORY_REPLAY/LC08_seed_candidate_rows.csv)<br>[LC08_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC08_HALO_PBH_INVENTORY_REPLAY/LC08_wrong_controls.csv) | [LC08_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC08_HALO_PBH_INVENTORY_REPLAY/LC08_result.md)<br>[LC08_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC08_HALO_PBH_INVENTORY_REPLAY/LC08_summary.json) | [All 11 files](../../tests/courtroom/16-the-last-campaign-lc08-halo-pbh-inventory-replay/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000022`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/GALAXY_HALOS_AND_MASS_DISTRIBUTION.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol I | SAMA-D000022 | Galaxy-Scale Accumulation | Many-Source Halo Accumulation, BB-PBH Inventory and SPARC Population Route |

| Document field | Value |
|---|---|
| Purpose | Build the galaxy-halo route from many nonzero \(A\) contributions and typed inventory through SPARC residuals, clustered profiles, scaffold formation, population appeal, mass placement and the remaining debt ledger. |
| Prerequisite documents | `SAMA-D000003`, `SAMA-D000018` |
| Used by | Focused child of `SAMA-P000002` and galaxy-scale handoff to the Volume I synthesis. |
| Primary source | [`volume_I/SAM_VOLUME_I_SUBSTRATE_TECHNICAL_SPINE.md`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_I_TECHNICAL_SPINE.md), SHA-256 `e2884e06ae8db8f7f9c98063f2cd075c90b355003348179a27cbbcc6b27fe825`. |
| Evidence registry | `index/registry/test_records.jsonl`, SHA-256 `2f22500f6583f567e350974610f00142e89b081a5b8c4c90c6dfe89bec43be0d`. |
| Courtroom pin | `iwtbotiwtwot/The_Courtroom` commit `b5e914f71377e86ef4c67e199973d9300795cda1`. |
| Revision state | Source-bound draft; mechanically registered proposal; not reviewed or approved. |

</details>
