[SAM](../../README.md) · [Volume II](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Mass, Lift, Debit and Particle Readout

## Opening question

> Once a finite row has been typed, which quantity is its native source,
> which operator supplies its lift or debit, which quantity returns support to
> accumulation, and where may a measured particle mass enter without
> collapsing those channels?

## Conceptual abstract

Volume II does not use one number called mass. It carries a typed sequence.
A row begins with a native source \(K\). A row-class operator supplies a
surface debit or credit \(X\). Their normalized relation is \(Y=X/K\) only
where \(K\ne0\). After a row has independently passed matter admission, a
source-support value \(q_A\) can return through the one-eighth carrier and
seven-eighths retained channels. A measured rest mass is a later comparator
or readout. These objects can share a scale without sharing a type.

The distinction was learned through a productive deviation. CR239 directly
tested \(m_i=m_g=\mu_QQ\). The one-anchor conversion closed its carbon-12
anchor but lost decisively to the locked mass-number control away from that
anchor. Its residual was not arbitrary: it organized almost monotonically
with neutron excess \(N-Z\). CR240 therefore separated the rest-source
channel \(Q_{\rm mass}\) from the coupling-source channel \(Q_{\rm sub}\).
The failure preserved the substrate source and corrected its type.

The same discipline makes the apparently irregular 139-row lift table exact.
CR243 separates five clean row classes; CR244 supplies two unequal-pair
classes. All 138 evaluable rows then close under their declared operators,
while the photon-road carrier remains a meaningful \(0/0\) endpoint with
undefined normalized lift. The 80-row structural surface admits another
compact description: 32 charged matter rows, 16 neutral matter rows and 32
charged antimatter transforms under a non-row \(A\) operator. The result is a
typed particle-readout grammar, not a global approximate mass formula.

## 1. The four-channel picture

The source-bound operation order is

\[
\text{typed row}
\longrightarrow K
\longrightarrow X=K\,Y_{\rm class}
\longrightarrow \text{matter admission}
\longrightarrow q_A
\longrightarrow \text{measured comparison or composite readout}.
\]

Each arrow has a distinct burden.

1. The row schema decides which operator is legal.
2. The native generator emits \(K\).
3. The lift/debit operator emits \(X\), often expressed through
   \(Y_{\rm class}=X/K\).
4. Matter admission is a separate predicate; a formula match does not admit a
   carrier or hidden-support row as matter.
5. An admitted row can emit \(q_A\) into the accumulation-support route.
6. A measured mass or nuclear binding value enters only as an authorized
   downstream comparison/readout.

The wrong compression is

\[
K=X=q_A=m_{\rm measured}.
\]

No source artifact authorizes that identity. The channels interact, but the
schema and the acting operator keep them distinct.

## 2. Definitions, domains and units

| Symbol or object | Definition | Domain or unit | Type boundary |
|---|---|---|---|
| \(r\) | one typed source-table row | row schema plus persistent key | A number or familiar name alone does not identify it. |
| \(K(r)\) | native source value | source-table native scale | Generated before measured comparison. |
| \(X(r)\) | surface debit or credit | same source scale as \(K\) within the lift table | Not automatically rest mass or \(q_A\). |
| \(Y(r)\) | normalized lift \(X/K\) | dimensionless where \(K\ne0\) | Selected by row class; undefined for \(K=X=0\). |
| \(p\) | partition coordinate | \(\{1,2,3,4,6,8,9,12\}\) in the compact rows | Address coordinate, not a particle label. |
| \(s\) | charged-row sign class | \(+\) or \(-\) | Selects a typed coefficient. |
| \(d\) | row closure depth | nonnegative source-defined integer | Distinct from \(D=3\). |
| \(D\) | support dimension | \(3\) | Structural constant, not row depth. |
| \(S\) | surface multiplicity | \(2^D=8\) | Fixes the one-eighth carrier share. |
| \(R\) | route radix | \(12\) | Gives \(R^2=144\) and \(R^4=20736\). |
| \(\Theta\) | released carrier value | \(18\) support units | Carrier, not measured matter. |
| \(q_A(r)\) | source support after matter admission | source-support scale | Not measured particle mass. |
| \(Q_{\rm mass}\) | typed nuclear rest-source channel | nuclear source units | A structural rest-source input, not itself a fitted binding output. |
| \(Q_{\rm sub}\) | typed nuclear coupling-source channel | nuclear source units | Coincides with \(Q_{\rm mass}\) only on its balanced domain. |
| \(A\) operator | non-row matter-to-antimatter conjugation | typed transform | Acts on rows and never adds a row. |

The row identity required by SAMA-C000139-R001 is

\[
\text{row identity}
=
\text{source table}
+\text{row schema}
+\text{typed address}
+\text{operator}.
\]

This identity is the firewall that prevents a lift value from being applied
to the wrong row class.

## 3. Normalized lift as a row-class operator

### 3.1 Why normalization helps

For \(K\ne0\), write

\[
Y=\frac{X}{K},
\qquad
X=KY.
\]

The quotient removes the native scale from the surface action. What remains
can be compared across rows only after class labels are preserved. CR243
starts with 139 source rows: 126 promoted rows and 13 carrier/tensor rows.
One photon-road carrier has

\[
K=0,\qquad X=0.
\]

Therefore \(Y=0/0\) is undefined. Assigning \(Y=0\) would assert no debit;
assigning \(Y=1\) would assert a fully supported source. Neither statement
follows from \(0/0\). The row is retained and excluded from quotient
evaluation, leaving

\[
139-1=138
\]

evaluable rows. This is SAMA-C000147-R001's endpoint boundary.

### 3.2 Five clean lift classes

CR243 resolves 96 of those rows into five exact classes.

#### Color triads

For a color-triad row,

\[
Y_{\rm color}
=\operatorname{sgn}(q)\frac{|q|+D}{R}.
\]

With \(D=3\) and \(R=12\), a \(q=+1\) row has

\[
Y_{\rm color}
=\frac{1+3}{12}
=\frac13,
\]

whereas a \(q=-2\) row has

\[
Y_{\rm color}
=-\frac{2+3}{12}
=-\frac5{12}.
\]

The sign is part of the operator, not a decorative row label. This law closes
14 color-triad rows, as recorded by SAMA-C000148-R001.

#### Equal bound pairs

The equal-pair operator is

\[
Y_{\rm equal}
=\frac{D+2}{R(D+1)}
=\frac{3+2}{12(3+1)}
=\frac5{48}.
\]

Six rows use this value. The denominator retains both the route radix and the
equal-pair depth factor.

#### OCTET pair

The separate OCTET row uses

\[
Y_{\rm OCTET}
=\frac{D^2+S}{DS^2}
=\frac{9+8}{3\cdot64}
=\frac{17}{192}.
\]

Although the OCTET and equal-pair values are both rational surface fractions,
their numerators and denominators arise from different typed structures.
SAMA-C000149-R001 therefore retains both formulas rather than averaging them.

#### Single-write and no-depth endpoints

For a single-write row,

\[
Y_{\rm single}=0,
\qquad
X=K\cdot0=0.
\]

For a no-surface-depth support or carrier row,

\[
Y_{\rm no\ depth}=1,
\qquad
X=K.
\]

The first endpoint says that the row carries no surface debit. The second says
that its source is fully in the support channel. They are not the same
physical role. CR243 contains 63 single-write rows and 12 no-depth rows,
corresponding to SAMA-C000150-R001.

The clean-class count is therefore

\[
14+6+1+63+12=96.
\]

### 3.3 Unequal-pair deviation and correction

The remaining

\[
138-96=42
\]

evaluable rows are unequal pairs. CR243 preserved them as a boundary because
one clean formula did not quantize all 42. CR244 retained the row-class trigger
and split the set into 30 ordinary and 12 OCTET-involved pairs.

For an ordinary unequal pair \((a,b)\),

\[
Y_{\rm unequal,ordinary}
=\operatorname{sgn}(a-b)
\frac{|a-b|+D}{R^4}.
\]

For an OCTET-involved unequal pair,

\[
Y_{\rm unequal,OCTET}
=\operatorname{sgn}(a-b)
\frac{|a-b|+D^2/R}{R^4}.
\]

Take \((a,b)=(1,2)\). The ordinary form gives

\[
Y_{\rm ordinary}
=-\frac{1+3}{20736}
=-\frac1{5184}.
\]

The OCTET form gives

\[
Y_{\rm OCTET\ unequal}
=-\frac{1+9/12}{20736}
=-\frac{7}{82944}.
\]

The same address difference therefore yields different exact values because
the operator class differs. CR244 closes 30/30 ordinary and 12/12
OCTET-involved rows. SAMA-C000151-R001 retains the two forms.

The correction chain matters as much as the final equations:

- using one unequal-pair formula erases the OCTET trigger;
- replacing \(R^4\) by \(R^3\) collapses both exact-match counts to zero;
- swapping the class trigger reduces the ordinary match from 30 to 4 and the
  OCTET match from 12 to 0; and
- the source-preserved alternative substitutions degrade rather than reproduce
  the typed closure.

Thus the exponent and trigger are load-bearing, not cosmetic fit labels.

## 4. From lift table to the 80-row structural surface

CR253 selects the stable tensor-compatible surface:

\[
80
=48\ \text{matter}+32\ \text{antimatter}
=64\ \text{charged}+16\ \text{neutral}.
\]

The minimal sufficient selection is

\[
\text{bin}\in
\{\text{stable matter},\text{antimatter conjugate}\}
\quad\land\quad
h_T\in\{0,1\}.
\]

Two proposed binary conditions became redundant after the upstream filters,
so the source retained a boundary status while preserving the exact 80 rows.
The semantic subtype is structural stable matter, not an 80-member list of
experimentally identified particles. This is the SAMA-C000143-R001 boundary.

The 48 matter rows split into 32 charged and 16 neutral rows. The remaining 32
are charged antimatter outputs of the non-row \(A\) transform:

\[
32+16+32=80.
\]

The operator itself is not added:

\[
80+\text{one operator}\ne81\ \text{particle rows}.
\]

## 5. Direct-bridge failure and typed-channel correction

### 5.1 The tested direct bridge

CR239 tested

\[
m_i(P)=m_g(P)=\mu_QQ(P)
\]

using a carbon-12 anchor

\[
Q(^{12}{\rm C})=\frac{7117}{16},
\qquad
\mu_Q=\frac{192}{7117}\ {\rm u\ per\ Q\!-\!unit}.
\]

The anchor closes exactly:

\[
\mu_QQ(^{12}{\rm C})
=\frac{192}{7117}\frac{7117}{16}
=12\ {\rm u}.
\]

An exact anchor does not decide the global question. On the source roster,
the direct bridge records RMS residual \(0.189480\), while the locked
mass-number control \(A=Z+N\) records \(0.00202\). The direct bridge is about
ninety times worse, where its precommitted non-failure condition required it
to beat the control by a factor of two.

The isotope increment exposes the missing scale:

\[
\Delta m_{\rm SAM}
=\mu_Q\frac18
=\frac{24}{7117}\ {\rm u}
\approx0.003372\ {\rm u}.
\]

Across the 14 measured isotope pairs, the measured-to-predicted increment
ratio has mean \(296.45\) and median \(296.66\).

CR239 therefore preserves FAIL_CR239_DIRECT_BRIDGE. That source verdict is
not a deletion of \(Q\). It rejects the type identity between a coupling
source and measured rest mass, as recorded by SAMA-C000155-R001.

### 5.2 The residual supplies the correction direction

The failure is organized:

| Diagnostic | Source result |
|---|---:|
| \(N=Z\) subset RMS | \(0.0023\) across 12 rows |
| \(N\ne Z\) subset RMS | \(0.2152\) across 37 rows |
| Spearman correlation with \(N-Z\) | \(+0.984\) |
| Spearman correlation with \(A\) | \(+0.961\) |

Shuffling \(Q\) worsens the RMS by about \(26\) times. The source channel
therefore retains structure, but one multiplicative conversion omits a
neutron-excess component.

CR240 corrects the typing. With

\[
\kappa
=\frac{(R-1)(\mathcal F S-1)}{D\alpha_H^S}
=\frac{7117}{768},
\]

define

\[
Q_{\rm mass}=4A\kappa
\]

and

\[
Q_{\rm sub}=8Z\kappa+\frac{N-Z}{8}.
\]

For \(N=Z\), \(A=2Z\), so

\[
Q_{\rm mass}
=4(2Z)\kappa
=8Z\kappa
=Q_{\rm sub}.
\]

For \(N>Z\), the channels differ. That gap becomes the exact asymmetry input
developed by SAMA-D000030 and SAMA-D000032. SAMA-C000156-R001 carries the
two-channel definition. SAMA-C000168-R001 preserves the CR240 candidate as a
usable downstream input while CR241's uniqueness boundary prevents an
unearned promotion.

## 6. Source support and rest-mass distinction

The compact \(q_A\) laws below are evaluated only on admitted matter rows.
They are source-support operators, not alternative equations for measured
rest mass. In the more general matter gate of SAMA-C000129-R001,

\[
q_A
=M_{\rm obs}\left(1+\frac{|q|}{R^2}\right)
\]

follows admission. Its support then separates as

\[
T=\frac{q_A}{8},
\qquad
W=\frac{7q_A}{8},
\qquad
T+W=q_A.
\]

LC03 replays this route through ledger compression before an accumulation
update. Direct \(q_A\)-as-mass, no compression, no carrier, wrong \(1/4\) and
\(1/16\) splits, carrier promotion and lane mixing are among the preserved
wrong controls. The replay retains \(q_A,T,W\) as source-support channels.

QP:QP112@SAM-ARCHIVE supplies an \(A\)-operator/\(\Theta\) correspondence.
That correspondence is a bridge of scale and operation. It does not make the
non-row conjugation operator, the \(\Theta18\) carrier and a matter row the
same type. This is why SAMA-C000131-R001 remains load-bearing even when
several channels contain familiar numerical values.

## 7. Worked channel bookkeeping

Consider a typed row with native source \(K=144\).

- If it is an equal pair, \(Y=5/48\), hence
  \(X=144(5/48)=15\).
- If it is the OCTET pair, \(Y=17/192\), hence
  \(X=144(17/192)=51/4\).
- If it is single-write, \(Y=0\), hence \(X=0\).
- If it is a no-depth support row, \(Y=1\), hence \(X=144\).

The native source is identical in this illustrative comparison, yet four
different typed rows produce different surface actions. Conversely, two
different row types can print the same scalar without becoming identical.
The operator and schema carry the meaning.

## 8. Compact row laws and A-conjugation

### 7.1 Charged matter rows

For \(32\) charged matter rows, CR254 gives

\[
q_A(p,s,d)
=R^d c_s p\left(1+\frac{p}{R^2}\right),
\qquad
c_+=\frac54,
\quad
c_-=\frac32.
\]

At \(p=1,d=0,s=+\),

\[
q_A
=\frac54\left(1+\frac1{144}\right)
=\frac54\frac{145}{144}
=\frac{725}{576}.
\]

At the same \(p,d\) with \(s=-\),

\[
q_A
=\frac32\frac{145}{144}
=\frac{145}{96}.
\]

The sign class changes the coefficient; it does not merely negate the value.
CR254 closes 32/32 source rows. Among 49 tested coefficient pairs, only
\((5/4,3/2)\) closes all rows. Exponent, scale and functional alternatives
reach at most 16/32, 4/32 and 4/32 respectively, and 1000 randomized
coefficients produce no exact closure. These are diagnostic comparisons on
the source roster, not a license to reclassify \(q_A\) as measured mass.
SAMA-C000152-R001 records the law and its type.

### 7.2 Neutral matter rows

For \(16\) neutral matter rows, CR255 gives

\[
q_A(p,d)=\frac{p}{8}R^d.
\]

The coefficient is independently readable as

\[
\frac18
=2^{-D}
=\frac{\Theta}{R^2}
=\frac{18}{144}.
\]

For \(p=8,d=0\),

\[
q_A=\frac88=1.
\]

For \(p=2,d=1\),

\[
q_A=\frac28\cdot12=3.
\]

CR255 closes 16/16 rows. The wrong divisor fails all 12 full nonzero cases;
wrong exponents reach at most 8/16, \(p\)-variants at most 2/16, and none of
1000 randomized alternatives closes the table. The neutral law does not
inherit \(c_+\) or \(c_-\). SAMA-C000153-R001 carries this exact boundary.

### 7.3 Non-row antimatter conjugation

CR256 acts on the 32 charged matter antecedents:

\[
q_{A,\bar m}=q_{A,m}C_A(s,p,d),
\]

\[
C_A(-,p,d)
=\frac56\left(1+\frac{p}{R^{d+1}}\right),
\]

\[
C_A(+,p,d)
=\frac65\left(1-\frac{p}{R^{d+1}}\right).
\]

For the positive row \(p=12,d=0\),

\[
C_A(+,12,0)
=\frac65\left(1-\frac{12}{12}\right)
=0.
\]

Thus

\[
q_{A,\bar m}=0
\]

regardless of the nonzero matter antecedent. This hard zero is an exact
operator endpoint, not a missing row. The canonical transform closes 32/32.
The wrong exponent and sign-swap controls close 0/32; the sign swap sends the
hard-zero output to \(39\). Randomized controls close 0/1000. Coefficient-only
alternatives can retain at most the forced hard zero, which is why one matching
endpoint cannot select the operator.

SAMA-C000154-R001 fixes the key census statement:

\[
48\ \text{matter rows}
+32\ \text{conjugate outputs}
=80\ \text{rows},
\]

with the \(A\) operator remaining non-row.

## 9. Established result and exact boundary

The current source chain establishes:

1. A normalized lift is a typed quotient \(Y=X/K\), not a global approximate
   mass equation.
2. CR243 and CR244 close all \(138\) evaluable lift rows under seven declared
   row classes; the massless photon-road endpoint remains undefined.
3. CR253 supplies an exact 80-row structural surface, not an observed-particle
   list.
4. CR254 and CR255 close the 48 matter rows under separate charged and neutral
   \(q_A\) laws.
5. CR256 transforms 32 charged antecedents under a non-row \(A\) operator and
   retains the positive \(p=12,d=0\) hard zero.
6. CR239 rejects the direct native-source/rest-mass identity; CR240 repairs
   the type map by separating \(Q_{\rm mass}\) and \(Q_{\rm sub}\).
7. LC03 keeps \(q_A,T,W\) in the support route and requires compression before
   an accumulation readout.

All crosswalk rows for this chapter carry
\(result\_classification=\mathrm{null}\). Source verdict and status tokens
are reported as provenance in the index; no new chapter-level classification
is assigned.

## 10. Deviation and wrong-control ledger

| Stage | Deviation or wrong control | Observed consequence | Corrected export |
|---|---|---|---|
| Direct source/rest bridge | Set \(m_i=m_g=\mu_QQ\) globally | Loses to \(A=Z+N\); residual tracks \(N-Z\) | Separate \(Q_{\rm mass}\) and \(Q_{\rm sub}\). |
| Lift normalization | Treat the 139 rows with one approximate \(Y\) law | Class structure is erased; photon becomes an artificial value | Retain the seven class operators and undefined \(0/0\) endpoint. |
| Unequal pairs | Use \(R^3\) or swap the OCTET trigger | Exact matches collapse | Preserve \(R^4\) and the row-class trigger. |
| Charged rows | Change coefficients, exponent or functional form | Full closure is lost | Retain \(c_+=5/4,c_-=3/2\). |
| Neutral rows | Import the charged law or wrong divisor | Full neutral closure is lost | Retain \(q_A=(p/8)R^d\). |
| Antimatter | Count the \(A\) transform as a row or swap its sign branch | Census/type error; hard zero becomes \(39\) | Keep \(A\) non-row and branch-specific. |
| Matter return | Set \(q_A\) equal to measured mass or omit compression | LC03 wrong controls reject the route | Preserve carrier split and ledger compression. |

No failed row is removed. Each failure either locates a type boundary, selects
an exponent or trigger, or prevents an operator from being promoted beyond
its source scope.

## 11. Connections and forward handoff

SAMA-D000026 supplies the row schema and the 80-row count firewall. This
chapter attaches the lift, \(q_A\) and conjugation operators to those typed
rows.

SAMA-D000029 receives the channel discipline for two special packets. It must
keep the Higgs retained-surface packet distinct from its later direct
\(A\)-source weld and keep the neutrino ratio packet distinct from its external
absolute scale.

SAMA-D000030 receives \(Q_{\rm mass}\), \(Q_{\rm sub}\), \(\kappa\) and the
neutron-excess correction direction. SAMA-D000032 then derives the normalized
square of their gap and joins it to the nonlinear binding route.

## Test and result index

| Test record key | Role | Source result/status | Result artifact | Test folder |
|---|---|---|---|---|
| LC:LC03 | Locked \(q_A\), carrier and compression replay | LC03_PASS_QA_LEDGER_COMPRESSION_GRAVITY_AS_A_REPLAY | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC03_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN) |
| CR:CR239@09a | Preserved failed direct source/rest-mass bridge | CLEAN; source verdict FAIL; artifact verdict FAIL_CR239_DIRECT_BRIDGE | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR239_NATIVE_MASS_GRAVITY_BRIDGE/CR239_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR239_NATIVE_MASS_GRAVITY_BRIDGE) |
| CR:CR240@09a | Typed rest-source/coupling-source correction | CLEAN; source verdict PASS | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR240_NEUTRON_REST_MASS_CHANNEL/CR240_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR240_NEUTRON_REST_MASS_CHANNEL) |
| CR:CR243@09a | Five clean typed lift classes and photon endpoint | CLEAN; source verdict PASS; 96 clean-class rows | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR243_MASSLIFT_CHANNEL_TYPING/CR243_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR243_MASSLIFT_CHANNEL_TYPING) |
| CR:CR244@09a | Ordinary/OCTET unequal-pair correction | CLEAN; source verdict PASS; 30/30 plus 12/12 | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR244_UNEQUAL_PAIR_TYPED_FORMS/CR244_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR244_UNEQUAL_PAIR_TYPED_FORMS) |
| CR:CR253@09a | Exact 80-row structural surface | Source artifact records 48 matter plus 32 antimatter and 64 charged plus 16 neutral | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW/CR253_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR253_PARTICLE_PROMOTER_80_ROW) |
| CR:CR254@09a | Compact charged matter-row law | Source artifact records 32/32 exact closure and diagnostic controls | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR254_COMPACT_MATTER_CHARGED_LAW/CR254_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR254_COMPACT_MATTER_CHARGED_LAW) |
| CR:CR255@09a | Compact neutral matter-row law | Source artifact records 16/16 exact closure and diagnostic controls | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR255_COMPACT_MATTER_NEUTRAL_LAW/CR255_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR255_COMPACT_MATTER_NEUTRAL_LAW) |
| CR:CR256@09a | Non-row \(A\)-conjugation and hard-zero boundary | Source artifact records 32/32 exact closure | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR256_A_OPERATOR_ANTIMATTER_CONJUGATE/CR256_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR256_A_OPERATOR_ANTIMATTER_CONJUGATE) |
| QP:QP112@SAM-ARCHIVE | \(A\)-operator/\(\Theta\) correspondence boundary | Source artifact records all seven gates passing | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/quantum_phase_QP_tests/qp112_A_operator_theta_bridge_correspondence/qp112_summary.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/0952ff63364f9406f389e63f4fdf13893255e828/reference%2520files_misc/archive/quantum_phase_QP_tests/qp112_A_operator_theta_bridge_correspondence) |

## Atomic SAMA source records

| Record ID | Role in this document |
|---|---|
| SAMA-C000129-R001 | Matter-admission-before-\(q_A\) gate. |
| SAMA-C000131-R001 | Source-support/rest-mass distinction. |
| SAMA-C000139-R001 | Source/schema/address/operator row identity. |
| SAMA-C000143-R001 | 80-row structural, not observed-particle, surface. |
| SAMA-C000147-R001 | Typed normalized lift and undefined photon endpoint. |
| SAMA-C000148-R001 | Color-triad lift law. |
| SAMA-C000149-R001 | Equal-pair and OCTET lift laws. |
| SAMA-C000150-R001 | Single-write and no-depth endpoints. |
| SAMA-C000151-R001 | Two unequal-pair lift forms. |
| SAMA-C000152-R001 | Compact charged \(q_A\) law. |
| SAMA-C000153-R001 | Compact neutral \(q_A\) law. |
| SAMA-C000154-R001 | Non-row \(A\)-conjugation operator. |
| SAMA-C000155-R001 | Rejected direct native-source/rest-mass bridge. |
| SAMA-C000156-R001 | Typed nuclear rest and coupling channels. |
| SAMA-C000168-R001 | Usable CR240 candidate with uniqueness unpromoted. |

## External references

No external bibliographic source is used directly. Measured masses mentioned
by the source tests remain downstream comparators in those artifacts.

## Revision and approval

This exact revision has reviewed_and_approved: false and approval: null until
Sean Brady explicitly approves it.

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000028`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/MASS_LIFT_DEBIT_AND_PARTICLE_READOUT.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol II | SAMA-D000028 | Particle Readout | Rest Mass, Source Support, Lift and Debit Typing |

| Document field | Value |
|---|---|
| Purpose | Derive the typed lift table and compact matter-row laws, preserve the failed direct source-to-rest-mass bridge, and show why native source, lift/debit, source support and measured particle readout remain separate channels. |
| Prerequisite documents | SAMA-D000026 |
| Used by | SAMA-D000029, SAMA-D000030 and the downstream binding route; generated from the document catalog |

</details>
