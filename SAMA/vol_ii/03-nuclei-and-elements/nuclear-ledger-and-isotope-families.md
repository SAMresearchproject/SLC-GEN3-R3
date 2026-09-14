[SAM](../../README.md) · [Volume II](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Nuclear Ledger and Isotope Families

## ATOM3D: contact, grammar and signed decoding — 14 September 2026

A3D41-T18-CONTACT-R2 uses SLC-GEN3-R3; A3D41-RXT-R3 supplies the joint native successor. Ordinary contact retains four minima and 113,664 agreeing readouts. Li-6 grammar retains both selected covers and every tie across six placements and 128 rho settings. Two Write responses and a signed N01 bit recover all 192 tested configurations. The test result suggests strong contact with the concept. The separate distinct-selector and physical-coefficient/MeV work remain owner-paused.

[Current derivations, code and results](../../../research/atom3d/README.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Opening question

> How does a nucleus assemble from typed proton, balanced-neutron,
> excess-neutron and electron slots, and how can that exact ledger feed
> isotope and binding work without treating a periodic family, an isotope, a
> representative isotope or a fitted readout as the same row?

## Conceptual abstract

The nuclear ledger is an additive construction with a nonlinear downstream
readout. Its additive layer is exact. A nucleus \((Z,N)\) is represented by
four typed populations:

\[
(n_p,n_{n_b},n_{n_e},n_e)=(Z,Z,N-Z,Z).
\]

Each slot carries quark counts and three source channels. Summing them yields
six identities for \(u,d,e,Q_{\rm mass},Q_{\rm sub}\) and \(\Delta Q\).
The balanced neutron cancels the proton's signed source gap. Every excess
neutron instead carries the one-eighth coupling support and leaves the exact
residual \(7093/192\).

That additive closure is not a linear formula for binding energy. CR248
explicitly tests the simple per-population readout and preserves its
insufficiency. CR245 shows why the residual still matters: squaring and
normalizing it generates the exact neutron-asymmetry shape. Volume, surface,
Coulomb, asymmetry, pairing and gated family structure are subsequently
required.

The same type discipline governs the isotope vault. An element-family row is
indexed by \(Z\); an isotope row by \((Z,N,A)\); a representative isotope is
one selected row used for an element-table readout. LC05 deliberately replays
the 126-row periodic surface and the older 162-row isotope roster together so
their distinct meanings remain visible. Labels and measured masses are
downstream reveals, never construction inputs.

## 1. From two positions to four slots

CR247 first exposes a compact two-position basis for \(N\ge Z\):

\[
n_{\rm balanced}=Z,
\qquad
n_{\rm excess}=N-Z.
\]

Its balanced position includes one proton, one balanced neutron and one
electron:

\[
\phi_b=(3,3,1,8\kappa,8\kappa,0).
\]

Its excess-neutron position is

\[
\phi_x=
\left(1,2,0,4\kappa,\frac18,\frac{7093}{192}\right).
\]

Thus the compact aggregate is

\[
\Phi(Z,N)
=Z\phi_b+(N-Z)\phi_x.
\]

CR248 then disaggregates \(\phi_b\) into the four-particle ledger:

\[
\phi_b=\phi_p+\phi_{n_b}+\phi_e.
\]

This step does not alter the totals. It makes the internal roles explicit so
that proton, balanced neutron, excess neutron and electron occupancies can be
used independently by later operators.

## 2. Definitions, domains and units

| Object | Definition | Domain or unit | Boundary |
|---|---|---|---|
| \(Z\) | proton number and element-family index | nonnegative integer | Does not identify a unique isotope. |
| \(N\) | neutron number | nonnegative integer | The current slot form is stated on \(N\ge Z\). |
| \(A\) | \(Z+N\) | nucleon count | Not the accumulation field \(A(r)\). |
| \(\kappa\) | \(7117/768\) | exact nuclear source coefficient | Typed source constant. |
| \(\phi\) | \((u,d,e,Q_{\rm mass},Q_{\rm sub},\Delta Q)\) | mixed count/source vector | Components are not added across unlike units. |
| \(n_p\) | proton-slot population | count | Equals \(Z\). |
| \(n_{n_b}\) | balanced-neutron population | count | Equals \(Z\). |
| \(n_{n_e}\) | excess-neutron population | count | Equals \(N-Z\). |
| \(n_e\) | electron-slot population | count | Equals \(Z\) in the neutral-atom ledger. |
| \(Q_{\rm mass}\) | rest-source channel | exact source units | Precedes binding readout. |
| \(Q_{\rm sub}\) | substrate-coupling source | exact source units | Contains one-eighth support per excess neutron. |
| \(\Delta Q\) | \(Q_{\rm mass}-Q_{\rm sub}\) | exact source units | Binding-asymmetry input, not complete binding energy. |
| element-family row | row indexed by \(Z\) | periodic-table schema | May carry one representative isotope. |
| isotope row | row indexed by \((Z,N,A)\) | isotope-vault schema | Multiple isotopes can share one \(Z\). |
| representative isotope | selected isotope for one element-family readout | element-table schema | Does not stand for every isotope. |
| known label or measured mass | downstream reveal/comparator | external/source-record units | Never selects the native row. |

SAMA-C000144-R001 fixes the reveal order:

\[
\text{native schema and operators}
\longrightarrow
\text{constructed row}
\longrightarrow
\text{authorized label or comparator}.
\]

Where exact contact is absent, a reversible SAM identifier is retained.

## 3. Deriving the four slot vectors

### 3.1 Proton

A proton contributes two \(u\) counts and one \(d\) count. Its rest-source
share is \(4\kappa\). In the balanced position it carries the full
\(8\kappa\) coupling contribution, producing the signed gap
\(-4\kappa\):

\[
\phi_p=(2,1,0,4\kappa,8\kappa,-4\kappa).
\]

The final component checks directly:

\[
Q_{\rm mass}-Q_{\rm sub}
=4\kappa-8\kappa
=-4\kappa.
\]

### 3.2 Balanced neutron

The balanced neutron contributes one \(u\), two \(d\), rest source
\(4\kappa\), no separate coupling source, and gap \(+4\kappa\):

\[
\phi_{n_b}=(1,2,0,4\kappa,0,+4\kappa).
\]

Adding proton and balanced neutron cancels the signed gap:

\[
-4\kappa+4\kappa=0.
\]

Their source channels also meet:

\[
Q_{\rm mass}^{p+n_b}=4\kappa+4\kappa=8\kappa,
\]

\[
Q_{\rm sub}^{p+n_b}=8\kappa+0=8\kappa.
\]

This is the local balanced unit.

### 3.3 Excess neutron

An excess neutron keeps the same quark counts and rest-source contribution as
the balanced neutron but carries only the released one-eighth coupling share:

\[
\phi_{n_e}
=
\left(1,2,0,4\kappa,\frac18,
4\kappa-\frac18\right).
\]

Since

\[
4\kappa
=4\left(\frac{7117}{768}\right)
=\frac{7117}{192}
\]

and

\[
\frac18=\frac{24}{192},
\]

its gap is

\[
4\kappa-\frac18
=\frac{7117-24}{192}
=\frac{7093}{192}.
\]

Therefore

\[
\phi_{n_e}
=
\left(1,2,0,4\kappa,\frac18,\frac{7093}{192}\right).
\]

### 3.4 Electron

The electron slot closes the neutral-atom count without contributing to these
nuclear source channels:

\[
\phi_e=(0,0,1,0,0,0).
\]

The zero source entries are typed zeros, not an assertion that the electron
has no other physical structure.

## 4. Population map and exact summation

For \(N\ge Z\), the population map is

\[
(n_p,n_{n_b},n_{n_e},n_e)
=(Z,Z,N-Z,Z).
\]

This is SAMA-C000163-R001. The aggregate ledger is

\[
\Phi(Z,N)
=Z\phi_p+Z\phi_{n_b}+(N-Z)\phi_{n_e}+Z\phi_e.
\]

Now sum each component.

### 4.1 Up-type count

\[
\begin{aligned}
u
&=2Z+Z+(N-Z)+0\\
&=2Z+N.
\end{aligned}
\]

### 4.2 Down-type count

\[
\begin{aligned}
d
&=Z+2Z+2(N-Z)+0\\
&=3Z+2N-2Z\\
&=Z+2N.
\end{aligned}
\]

### 4.3 Electron count

\[
e=0+0+0+Z=Z.
\]

### 4.4 Rest-source channel

\[
\begin{aligned}
Q_{\rm mass}
&=4\kappa Z+4\kappa Z+4\kappa(N-Z)\\
&=4\kappa(2Z+N-Z)\\
&=4\kappa(Z+N)\\
&=4A\kappa.
\end{aligned}
\]

### 4.5 Coupling-source channel

\[
\begin{aligned}
Q_{\rm sub}
&=8\kappa Z+0+\frac18(N-Z)\\
&=8Z\kappa+\frac{N-Z}{8}.
\end{aligned}
\]

### 4.6 Channel gap

\[
\begin{aligned}
\Delta Q
&=(-4\kappa)Z+(+4\kappa)Z
 +(N-Z)\frac{7093}{192}\\
&=(N-Z)\frac{7093}{192}.
\end{aligned}
\]

These are the six identities in SAMA-C000164-R001:

\[
\boxed{
\begin{aligned}
u&=2Z+N,\\
d&=Z+2N,\\
e&=Z,\\
Q_{\rm mass}&=4A\kappa,\\
Q_{\rm sub}&=8Z\kappa+\frac{N-Z}{8},\\
\Delta Q&=(N-Z)\frac{7093}{192}.
\end{aligned}}
\]

## 5. Nuclear slot and population ledger

### 5.1 Balanced worked example: carbon-12

For \(Z=N=6\),

\[
A=12,
\qquad
(n_p,n_{n_b},n_{n_e},n_e)=(6,6,0,6).
\]

The count channels are

\[
u=2(6)+6=18,
\qquad
d=6+2(6)=18,
\qquad
e=6.
\]

The source channels are

\[
Q_{\rm mass}=4(12)\kappa=48\kappa=\frac{7117}{16},
\]

\[
Q_{\rm sub}=8(6)\kappa+0=48\kappa=\frac{7117}{16},
\]

and

\[
\Delta Q=0.
\]

Carbon-12 isolates the balanced unit: no excess-neutron slot is populated.

### 5.2 Single-excess worked example: carbon-13

For \(Z=6,N=7\),

\[
A=13,
\qquad
(n_p,n_{n_b},n_{n_e},n_e)=(6,6,1,6).
\]

Then

\[
u=19,\qquad d=20,\qquad e=6,
\]

\[
Q_{\rm mass}=52\kappa=\frac{92521}{192},
\]

\[
Q_{\rm sub}=48\kappa+\frac18=\frac{7119}{16},
\]

\[
\Delta Q=\frac{7093}{192}.
\]

This row isolates exactly one excess-neutron contribution.

### 5.3 Heavy worked example: gold-197

For \(Z=79,N=118\),

\[
A=197,
\qquad
N-Z=39.
\]

The populations are

\[
(79,79,39,79),
\]

and the count totals are

\[
u=2(79)+118=276,
\]

\[
d=79+2(118)=315,
\]

\[
e=79.
\]

The source channels are

\[
Q_{\rm mass}=4(197)\kappa=788\kappa
=\frac{1402049}{192},
\]

\[
Q_{\rm sub}=8(79)\kappa+\frac{39}{8}
=\frac{562711}{96},
\]

and

\[
\Delta Q
=39\frac{7093}{192}
=\frac{92209}{64}
=1440.765625.
\]

CR247 reproduces these six components exactly. Across its scoped \(69\)
\(N\ge Z\) rows, all six identities close under exact rational arithmetic.

### 5.4 From exact ledger to nonlinear boundary

CR248 disaggregates the two-position basis into these four slots and retains
the exact component identities. It then tests a linear surface-debit readout

\[
B_u^{\rm linear}
=\alpha Z+\beta(N-Z).
\]

The fitted source coefficients are approximately

\[
\alpha=+3.14\ {\rm MeV},
\qquad
\beta=-5.62\ {\rm MeV}.
\]

The result is not a binding closure:

\[
\mathrm{RMS}_{\rm train}\approx24.5\ {\rm MeV},
\qquad
\mathrm{RMS}_{\rm test}\approx25.2\ {\rm MeV}.
\]

Its light-nucleus anchor misses include \(+18.86\) MeV for carbon-12 and
\(+16.36\) MeV for carbon-13, while the heavier gold-197 row is closer at
\(-2.07\) MeV. This pattern locates the missing curvature. Exact additive
source identities survive, but binding requires nonlinear pair, surface,
Coulomb, asymmetry and pairing geometry.

### 5.5 The \(N=2Z\) label-swap boundary

CR278 consolidates the four slots and six identities. Its first wrong control
swaps balanced and excess labels and precommits that every \(N>Z\) row should
break. It breaks 55 of 56. The exception is tritium:

\[
Z=1,\qquad N=2,\qquad N-Z=1.
\]

Therefore

\[
n_{n_b}=Z=1
\]

and

\[
n_{n_e}=N-Z=1.
\]

Swapping two equally populated labels cannot change any aggregate:

\[
1\phi_{n_b}+1\phi_{n_e}
=1\phi_{n_e}+1\phi_{n_b}.
\]

More generally,

\[
n_{n_b}=n_{n_e}
\iff
Z=N-Z
\iff
N=2Z.
\]

SAMA-C000165-R001 records this exact population-label symmetry. It is not an
ambiguity in the six identities. The second CR278 wrong control makes every
neutron carry the excess gap; it breaks all 56 qualifying \(N>Z,Z>0\) rows,
confirming that the balanced/excess distinction remains load-bearing away
from the equal-population permutation.

### 5.6 Exact asymmetry handoff

The gap can be derived directly from the aggregate channels:

\[
\begin{aligned}
Q_{\rm mass}-Q_{\rm sub}
&=4(Z+N)\kappa-8Z\kappa-\frac{N-Z}{8}\\
&=(N-Z)\left(4\kappa-\frac18\right)\\
&=(N-Z)\frac{7093}{192}.
\end{aligned}
\]

Squaring and dividing by \(Q_{\rm mass}=A(7117/192)\) yields

\[
\frac{(\Delta Q)^2}{Q_{\rm mass}}
=
\frac{(N-Z)^2}{A}
\frac{7093^2}{192\cdot7117}.
\]

The exact coefficient is

\[
\frac{7093^2}{192\cdot7117}
=\frac{50310649}{1366464}
\approx36.81813.
\]

CR245 checks the identity on 71/71 rows. The identity is the binding handoff;
the full nonlinear operator remains separate, as required by
SAMA-C000169-R001, SAMA-C000170-R001 and SAMA-C000171-R001.

## 6. Isotope, periodic and frontier evidence

### 6.1 Three row types

SAMA-C000166-R001 separates:

1. element-family row \(E_Z\), indexed only by \(Z\);
2. isotope row \(I_{Z,N,A}\), indexed by the full nuclear address; and
3. representative-isotope row \(R_Z=I_{Z,N_Z,A_Z}\), chosen for one
   element-table readout.

The mapping

\[
I_{Z,N,A}\longrightarrow E_Z
\]

is many-to-one. The selection

\[
E_Z\longrightarrow R_Z
\]

chooses one isotope for a specific readout and does not erase the others.

### 6.2 Older isotope vault and permanent frontier

CR072 closes the scoped branch-10 zipper. Its older isotope roster records a
162/162 comparison for \(Z=1,\ldots,96\). CR071 separately seals the
\(Z=97,\ldots,118\) frontier map:

\[
22\ \text{island rows}
\subset
38\ \text{broader-band rows}.
\]

The CR071 map is permanent. Later observations enter its declared appeal
channel; the sealed map itself is not overwritten. The map is a set of
pre-registered \(Z,N,A\) targets, not a stability, chemistry or synthesis
operator.

### 6.3 Locked replay across both surfaces

LC05 replays:

\[
126/126\ \text{native element-family rows},
\]

\[
118/118\ \text{downstream known labels},
\]

\[
8/8\ \text{native frontier identities at }Z=119,\ldots,126,
\]

and

\[
162/162\ \text{rows in the older scoped isotope comparison}.
\]

No known label is used as a construction input on any of the 126 periodic
rows. The maximum decimal error in the one-eighth/seven-eighths \(q_A\) split
is \(10^{-96}\) against tolerance \(10^{-90}\). Ten wrong controls reject
label backfill, row deletion, constant mutation, frontier relabeling and
related type collapses.

SAMA-C000167-R001 preserves the open outputs. This packet supplies neither a
complete shell model nor half-life, decay-channel, chemistry or synthesis
derivations.

### 6.4 Representative-isotope extension

CR277 applies the frozen CR274 readout with zero refit to one representative
isotope for every

\[
Z=1,\ldots,126.
\]

The table contains 118 observed representative rows and eight \(Z=119\) to
\(126\) frontier rows. The latter are source-native identities and forecast
locks, not observations. Across the 118 observed representatives, the result
reports its extrapolation metrics while retaining that the base was fitted on
55 isotopes and that the light/heavy extension is a readout rather than a new
fit.

The exact statement is therefore:

\[
126\ \text{representative rows}
\ne
\text{all isotopes}.
\]

## 7. Binding-selector prerequisites

The QP route supplies a typed operator order:

\[
\text{QP:QP047}
\longrightarrow
\text{QP:QP051}
\longrightarrow
\text{QP:QP052}
\longrightarrow
\text{CR:CR274@09a}.
\]

QP:QP047 identifies the nuclear-binding/isotope \(A\)-road selector.
QP:QP051 selects neutron-excess binding depth. QP:QP052 supplies the numeric
\(\Delta N\) and binding-mass comparison route. None of those selectors alone
emits a complete binding energy.

CR274 is a historical fitted readout downstream of those prerequisites. Its
operation order is

\[
(Z,N)
\longrightarrow
\text{four typed populations}
\longrightarrow
Q_{\rm mass},Q_{\rm sub},\Delta Q
\longrightarrow
\text{nonlinear base geometry}
\longrightarrow
\text{four family gates}
\longrightarrow
\text{comparison}.
\]

On its 55-row benchmark, the base RMS is \(3.9102\) MeV and the gated RMS is
\(2.7160\) MeV, with 50/55 rows within 5 MeV. The four gate coefficients are
fitted readout parameters, not substrate primitives. Current binding authority
is handled by the dedicated live boundary and SAMA-D000032.

## 8. Established result and current boundaries

The source chain establishes:

1. Four typed populations sum to six exact nuclear ledger identities.
2. The balanced neutron cancels the proton gap; each excess neutron leaves
   \(7093/192\).
3. The \(N=2Z\) swap is an equal-population label symmetry, while the
   balanced/excess distinction remains load-bearing elsewhere.
4. Linear per-particle debit does not reproduce binding curvature.
5. The normalized square of the exact gap yields the
   \((N-Z)^2/A\) asymmetry shape.
6. Element families, isotopes and representative isotopes are different row
   types.
7. LC05 retains both the 126-row periodic surface and the older 162-row
   isotope roster with their frontier boundaries.
8. Binding selectors and the historical gated readout remain downstream of
   the exact ledger.

Every registered crosswalk row in this chapter carries
\(result\_classification=\mathrm{null}\). Source verdict/status values remain
attributed in the index.

## 9. Forward handoff

SAMA-D000032 receives the exact objects

\[
Q_{\rm mass}=4A\kappa,
\qquad
Q_{\rm sub}=8Z\kappa+\frac{N-Z}{8},
\qquad
\Delta Q=(N-Z)\frac{7093}{192}
\]

and develops their binding consequences from the failed direct bridge through
the exact asymmetry correction and nonlinear A-kernel route.

The periodic and computation branches receive typed element-family and isotope
rows with their source keys intact. Neither downstream branch may infer an
isotope from \(Z\) alone or treat a representative-isotope readout as a full
isotope family.

## Test and result index

| Test record key | Role | Source result/status | Result artifact | Test folder |
|---|---|---|---|---|
| LC:LC05 | Locked periodic/isotope replay | LC05_PASS_PERIODIC_ISOTOPE_VAULT_REPLAY_FROM_LOCKED_PRIMITIVE_STACK | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC05_PERIODIC_ISOTOPE_VAULT_REPLAY/LC05_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN/LC05_PERIODIC_ISOTOPE_VAULT_REPLAY) |
| CR:CR071@10 | Permanent \(Z=97\) to \(118\) frontier target map | CLEAN; BOUNDARY_PRE_REGISTERED_PREDICTION | [result](../../courtroom/10_ISOTOPE_AND_PERIODIC_TABLE_VAULT/CR071_SUPERHEAVY_MISS_BAND_TARGET_MAP/CR071_result.md) | [folder](../../courtroom/10_ISOTOPE_AND_PERIODIC_TABLE_VAULT/CR071_SUPERHEAVY_MISS_BAND_TARGET_MAP) |
| CR:CR072@10 | Scoped isotope/periodic branch zipper | CLEAN; PASS_SCOPED_10_BRANCH_K1_VERIFIED_WITH_FRONTIER_SEAL | [result](../../courtroom/10_ISOTOPE_AND_PERIODIC_TABLE_VAULT/CR072_ISOTOPE_PERIODIC_BRANCH_VERDICT/CR072_result.md) | [folder](../../courtroom/10_ISOTOPE_AND_PERIODIC_TABLE_VAULT/CR072_ISOTOPE_PERIODIC_BRANCH_VERDICT) |
| CR:CR245@09a | Exact channel-gap/asymmetry identity and nonlinear boundary | CLEAN; source verdict BOUNDARY; 71/71 exact identity | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR245_BINDING_CURVATURE_FROM_TYPED_SUBSTRATE/CR245_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR245_BINDING_CURVATURE_FROM_TYPED_SUBSTRATE) |
| CR:CR247@09a | Balanced/excess inverse decomposition | CLEAN; source verdict PASS; 69/69 exact six-component closure | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR247_SOB_INVERSE_SECOND_LAYER/CR247_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR247_SOB_INVERSE_SECOND_LAYER) |
| CR:CR248@09a | Four-slot disaggregation and linear-binding boundary | CLEAN; source verdict BOUNDARY | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR248_SOB_MICRO_CHANNEL_DEBIT_OCCUPANCY/CR248_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR248_SOB_MICRO_CHANNEL_DEBIT_OCCUPANCY) |
| CR:CR274@09a | Historical nonlinear gated readout | Source artifact records RMS \(3.9102\to2.7160\) MeV and 50/55 within 5 MeV | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR274_GATED_NUCLEAR_READOUT_OPERATORS/CR274_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR274_GATED_NUCLEAR_READOUT_OPERATORS) |
| CR:CR277@09a | Zero-refit 126-representative-element readout | Source verdict PASS; 126 rows, 118 observed representatives and 8 frontier locks | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR277_ONE_HUNDRED_TWENTY_SIX_ELEMENT_TABLE_AND_SOB_FRONTIER_LOCKS/CR277_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR277_ONE_HUNDRED_TWENTY_SIX_ELEMENT_TABLE_AND_SOB_FRONTIER_LOCKS) |
| CR:CR278@09a | Four-slot neutron-rule consolidation and \(N=2Z\) symmetry | Source verdict BOUNDARY; six exact identities retained | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR278_NEUTRON_RULE_CONSOLIDATION/CR278_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR278_NEUTRON_RULE_CONSOLIDATION) |
| QP:QP047 | Nuclear binding/isotope \(A\)-road selector | Source artifact supplies the selector | [result](../../courtroom/12_QUANTUM_COMPUTING_AND_NETWORKING/_source_artifacts/reports/QP047_PRIVATE_NUCLEAR_BINDING_ISOTOPE_A_ROAD_SELECTOR.md) | [folder](../../courtroom/12_QUANTUM_COMPUTING_AND_NETWORKING/_source_artifacts/reports) |
| QP:QP051 | Neutron-excess binding-depth selector | Source artifact supplies the selector | [result](../../courtroom/12_QUANTUM_COMPUTING_AND_NETWORKING/_source_artifacts/reports/QP051_PRIVATE_NEUTRON_EXCESS_BINDING_DEPTH_SELECTOR.md) | [folder](../../courtroom/12_QUANTUM_COMPUTING_AND_NETWORKING/_source_artifacts/reports) |
| QP:QP052 | Numeric \(\Delta N\) and binding-mass selector | Source artifact supplies the selector | [result](../../courtroom/12_QUANTUM_COMPUTING_AND_NETWORKING/_source_artifacts/reports/QP052_PRIVATE_NUMERIC_DELTA_N_AND_BINDING_MASS_SELECTOR.md) | [folder](../../courtroom/12_QUANTUM_COMPUTING_AND_NETWORKING/_source_artifacts/reports) |

## Atomic SAMA source records

| Record ID | Role in this document |
|---|---|
| SAMA-C000144-R001 | Construction-before-label/reveal boundary. |
| SAMA-C000156-R001 | Typed \(Q_{\rm mass}\) and \(Q_{\rm sub}\) channels. |
| SAMA-C000162-R001 | Four nuclear slot vectors. |
| SAMA-C000163-R001 | Population map \((Z,Z,N-Z,Z)\). |
| SAMA-C000164-R001 | Six exact aggregate identities. |
| SAMA-C000165-R001 | \(N=2Z\) equal-population label symmetry. |
| SAMA-C000166-R001 | Element-family/isotope/representative distinction. |
| SAMA-C000167-R001 | Isotope-vault and frontier open-output boundary. |
| SAMA-C000169-R001 | Exact neutron-excess channel gap. |
| SAMA-C000170-R001 | Normalized-square asymmetry shape. |
| SAMA-C000171-R001 | Nonlinear binding requirement. |

## External references

The AME/IAEA and other comparison values used by the source artifacts remain
inside those registered test records. This chapter introduces no independent
external dataset or updated comparison.

## Revision and approval

This exact revision has reviewed_and_approved: false and approval: null until
Sean Brady explicitly approves it.

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000030`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/NUCLEAR_LEDGER_AND_ISOTOPE_FAMILIES.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol II | SAMA-D000030 | Nuclear Structure | Nuclear Slot Populations, Aggregate Identities and Isotope Families |

| Document field | Value |
|---|---|
| Purpose | Construct the four-slot nuclear ledger, derive its six exact aggregate identities, preserve the linear-binding and label-swap boundaries, and distinguish element families, isotopes and representative-isotope readouts. |
| Prerequisite documents | SAMA-D000026; SAMA-D000028 |
| Used by | SAMA-D000032 and the Volume II binding, periodic and computation handoffs; generated from the document catalog |

</details>
