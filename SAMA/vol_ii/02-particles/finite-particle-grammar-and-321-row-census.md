[SAM](../../README.md) · [Volume II](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Finite Particle Grammar and 321-Row Census

## ATOM3D: source construction and learned templates — 16 September 2026

A3D41-T18-CONTACT-R2 uses installed SLC-GEN3-R4. The source roster retains 3,496 targets and 3,489 assemblies, including 1,737 connected assemblies (H001479). The learned generator retains 1,872 templates across 25 inventories and 137/138 held-out continuation decisions (H001480). New-basis recipes cover all 68 formerly blocked inventories; their new assemblies remain to be constructed. Physical binding and stability remain unassigned. The test result suggests strong contact with the concept. Earlier contact and signed-decoder results retain their scope; the distinct-selector and physical-coefficient/MeV pauses remain.

[Current derivations, code and results](../../../research/atom3d/README.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Opening question

> How is the 321-row finite catalog reconstructed, which native laws generate
> its different row classes, and where do generation, stability, matter
> admission, observed naming and computation remain separate stages?

## Conceptual abstract

The 321-row catalog is not a list of 321 experimentally identified particles.
It is a finite typed vault containing stable matter candidates, unstable
resonances, antimatter conjugates, bound composites, carriers, hidden support
and rejected closures. Its exact bin census is current because CR252 rebuilt
the table deterministically and obtained a bit-identical 321-row result.

The grammar underneath that catalog is class-specific. A two-body bound-color
pair uses a product plus absolute-difference law. Three-body candidates use a
fully symmetric sum of squares. Single-write charged fermions use a radix
depth ladder with sign- and conjugation-dependent coefficients. Neutral
fermions use the same ladder architecture with a bare \(1/8\) coefficient.
Carrier rows occupy declared \((\alpha_H,D)\) lattice points. Hidden support
uses \(p+p^2/R^2\) while remaining outside matter and \(q_A\).

These laws generate native structural values. They do not themselves decide
that a generated candidate is stable matter. The three-body law demonstrates
the distinction sharply: all 13 rejected fake closures in its extension still
obey the generator. Stability is a downstream filter.

Most CR128–CR134 laws were found by inspecting the same catalog on which their
exact matches are reported. Their 100% in-sample results therefore establish
generator consistency, while each sealed forward-blind rule awaits future
eligible rows. That methodological boundary is part of the grammar, not a
reason to discard the exact closed formulas or their preserved wrong-control
chains.

## 1. Authority and reconstruction contract

### 1.1 Current sources, not manuscript memory

The owner-identified `SAM_321` PDF is retained only as an organizational
exemplar. Its prose is not current authority. The reconstruction order is:

```text
current typed source records
  -> CR119 historical reveal lineage
  -> CR252 bit-identical catalog refresh
  -> LC04 locked table/generator replay
  -> CR128–CR134 scoped law records
  -> QP093A bucket map
  -> Volume III serialization boundary.
```

No statement is copied from the older exemplar merely because its row count
or terminology looks familiar.

### 1.2 Base closure and full catalog answer different questions

The 35-row base surface is the compact particle mass-prediction closure. The
321-row surface is the full typed catalog used for bin resolution and extended
finite-object context. Thus

\[
\mathcal S_{35}\ne\mathcal C_{321},
\]

and neither supersedes the other. LC04 replays both while retaining their
schemas.

## 2. Definitions, domains and units

### 2.1 Structural constants

Throughout the registered generator suite,

\[
\alpha_H=2,
\qquad
D=3,
\qquad
R=12,
\qquad
R^2=144,
\qquad
R^3=1728,
\qquad
R^4=20736.
\]

The connector/partition alphabet is

\[
\mathcal P=\{1,2,3,4,6,8,9,12\}.
\]

### 2.2 Row-level quantities

| Quantity | Meaning | Domain/unit | Boundary |
|---|---|---|---|
| \(r\) | typed catalog row | source schema | Not reconstructed from one number. |
| \(p\) or \((a,b,c,\ldots)\) | partition address | \(\mathcal P\) or declared tuples over it | Address, not observed identity. |
| \((q_{\rm abs},q_{\rm sign})\) | charge magnitude and sign fields | schema-defined | Operator inputs only where declared. |
| \(d\) | closure depth in a row law | nonnegative integer in the source class | Distinct from foundation \(D=3\). |
| \(M_{\rm native}\) | native generated structural value | source-table mass scale | Not automatically measured mass. |
| \(S_{\rm debit}\) | signed surface debit | source-table scale | A separate channel from \(q_A\) and rest mass. |
| \(M_{\rm observed}\) | downstream table readout/comparator | source-table or external units | Never an input to native generation. |
| \(q_A\) | source-support channel after matter admission | source-support scale | Not direct rest mass. |
| \(\mathsf{stability\_status}\) | downstream filter field | finite label set | Does not alter the native generator. |
| \(A\) operator | matter/antimatter conjugation | non-row transform | Never counted as a row. |

### 2.3 Generation, filtering and reveal

The stages are

\[
\text{typed address}
\xrightarrow{G_{\rm class}}
M_{\rm native}
\xrightarrow{F_{\rm stability}}
\text{candidate status}
\xrightarrow{F_{\rm matter}}
\text{matter admission}
\xrightarrow{R_{\rm reveal}}
\text{authorized label/comparator}.
\]

The operators are not interchangeable. A row can pass \(G_{\rm class}\) and
fail \(F_{\rm stability}\); the three-body rejected closures do exactly that.

## 3. Typed reconstruction pipeline

Every reconstruction in this chapter preserves four keys before evaluating a
law: the source table, the row schema, the native address and the operator
class. Results are joined back to the original row ID. A formula match cannot
manufacture a label, stability state or matter admission absent from that
source row.

## 4. Base closure and full-catalog distinction

The 35-row surface is the compact base prediction closure. The 321-row catalog
is the extended typed vault. LC04 replays both because they are related, but a
base-law row and a catalog-bin row remain differently typed. The full census
therefore begins from CR252 rather than extrapolating 321 entries from the
35-row chain.

## 5. Current catalog reconstruction

### 5.1 Historical reveal layer

CR119 records 321 particle-catalog rows, 126 matter rows and 126 periodic
rows, with labels assigned only downstream. The source also preserves the
frontier Z119–Z126 identities, the `QP093A-0088` null conjugate, the rule
\(q_A\ne\text{mass}\) and the tensor-carrier exclusion.

### 5.2 Current refresh

CR252 regenerates the full catalog:

\[
N_{\rm baseline}=N_{\rm regen}=321,
\]

and the regenerated CSV is bit-identical to the baseline. Its exact schema
bins are

\[
\begin{aligned}
n_{\rm stable}&=63,\\
n_{\rm resonance}&=25,\\
n_{\rm antimatter}&=42,\\
n_{\rm bound}&=169,\\
n_{\rm carrier}&=6,\\
n_{\rm hidden}&=8,\\
n_{\rm rejected}&=8.
\end{aligned}
\]

Summing in stages makes the closure visible:

\[
63+25=88,
\]

\[
88+42=130,
\]

\[
130+169=299,
\]

\[
299+6+8+8=321.
\]

CR252 records all 321 rows as unchanged and present in both versions; a second
regeneration reproduces the same hash. Its wrong controls also preserve \(R\)
as load-bearing and keep all six carriers unpromoted.

### 5.3 Structural bucket map

QP093A provides the bucket interpretation that organizes candidates and
support rows. It is a map over the catalog, not authority to import stale
`SAM_321` prose. The map travels with the row IDs and the current CR252 table.

## 6. Scoped particle-law extensions

### 6.1 Two-body bound-color grammar

#### 6.1.1 Locked law

For a `BOUND_COLOR_PAIR` row with ordered or symmetric partition \((a,b)\),
CR128 locks

\[
\boxed{M_2(a,b)=Rab+D|a-b|.}
\]

The first term is symmetric:

\[
Rab=Rba.
\]

The absolute-difference correction is also symmetric under exchange:

\[
|a-b|=|b-a|.
\]

Thus \(M_2(a,b)=M_2(b,a)\), even though the source table may retain the two
orderings as separate rows for debit/sign structure.

#### 6.1.2 Worked asymmetric pair

For \((a,b)=(1,2)\),

\[
Rab=12\cdot1\cdot2=24,
\]

\[
D|a-b|=3|1-2|=3,
\]

so

\[
M_2(1,2)=24+3=27.
\]

Both catalog orderings carry that native value.

#### 6.1.3 Worked symmetric pair

For \((a,b)=(3,3)\), the difference term vanishes:

\[
M_2(3,3)=12\cdot3\cdot3+3|3-3|=108.
\]

The formula matches all 36 scoped rows: 30 asymmetric and 6 symmetric, with
zero parse or partition-algebra violations.

#### 6.1.4 Boundary and wrong controls

CR128 does not supply the asymmetric doublet's \(S_{\rm debit}\), the
observed-mass offset of symmetric pairs, or a three-body law. Numerical
coincidence with some three-body rows is explicitly rejected as a reason to
reuse the operator.

The law was extracted inductively from the current catalog. The 36/36 match is
therefore in-sample generator consistency. `CR128_PRED_1` fixes the formula,
zero free parameters and a one-row future falsifier for a newly eligible
two-body row.

### 6.2 Three-body generator

#### 6.2.1 OCTET law

For an `OCTET_COMPOSITE` three-element partition \((a,b,c)\), CR129 locks

\[
\boxed{
M_3(a,b,c)=RD(a^2+b^2+c^2)
=36(a^2+b^2+c^2).}
\]

Every term is a square and the sum is invariant under every permutation of
\((a,b,c)\). Unlike the two-body law, no linear absolute-difference term is
present.

#### 6.2.2 Worked triple

For \((1,2,3)\),

\[
1^2+2^2+3^2=1+4+9=14,
\]

and

\[
M_3(1,2,3)=12\cdot3\cdot14=36\cdot14=504.
\]

CR129 matches 76/76 three-body OCTET rows. It also routes 28 two-body OCTET
rows back through the distinct CR128 law, where all 28 match.

#### 6.2.3 Extension across stability classes

CR129c applies the same three-body generator to 44
`GROUND_BARYON_3BODY` rows:

| Source class/status | Rows | Matches |
|---|---:|---:|
| closed stable candidate | 14 | 14 |
| closed heavy candidate | 17 | 17 |
| rejected fake closure | 13 | 13 |
| total extension | 44 | 44 |

Together with CR129,

\[
76+44=120
\]

three-body rows match with zero violations. The 13 rejected rows are
load-bearing evidence for the stage split:

\[
G_3(a,b,c)=M_{\rm native}
\]

is evaluated before

\[
F_{\rm stability}(r)\in
\{\text{stable},\text{heavy},\text{rejected}\}.
\]

A rejected closure can therefore possess a valid generated value without
being promoted as physical matter.

#### 6.2.4 Generator boundary

CR129 and CR129c both preserve forward-blind one-row falsifiers for future
eligible triples. Their present exact match is a closed statement about the
current catalog and a sealed prediction for future rows, not a claim that
stability follows from the mass formula.

### 6.3 Three-body surface debit: deviation to corrected form

#### 6.3.1 Failed and insufficient stages

CR129b preserves the route by which the debit law was found:

| Stage | Proposed form | Outcome |
|---|---|---|
| 1 | sum of pairwise two-body debits | wrong sign and off by factors 7–15 |
| 2 | global \((1/8)M_{\rm native}\) surcharge | wrong scale |
| 2′ | global \((9/8)M/R^3\) surcharge | uniform \(18/17\) overshoot |
| 3 | charge-slot correction | residual scales linearly with \(|q|\) |
| 4 | middle-slot-only \(9/8\) weighting | exact neutral \(17/16\) form |

The unsuccessful controls are not removed. They identify both the correct
scale \(R^{-3}\) and the correct site: the \(9/8\) factor acts on the middle
slot of a \(1{:}2{:}1\) decomposition rather than on the whole mass.

#### 6.3.2 Neutral derivation

The slot weights are

\[
\frac14,
\qquad
\frac98\cdot\frac12=\frac9{16},
\qquad
\frac14.
\]

Their exact sum is

\[
\frac14+\frac9{16}+\frac14
=\frac4{16}+\frac9{16}+\frac4{16}
=\frac{17}{16}.
\]

Hence for \(q=0\),

\[
\boxed{
S_{\rm debit}
=\frac{17}{16}\frac{M_{\rm native}}{R^3}.}
\]

The coefficient also has the foundation form

\[
\frac{17}{16}
=\frac{R+D+\alpha_H}{\alpha_H^4}
=\frac{12+3+2}{2^4}.
\]

For the worked \((1,2,3)\) triple with \(M_{\rm native}=504\),

\[
S_{\rm debit}
=\frac{17}{16}\frac{504}{1728}
=\frac{17}{16}\frac7{24}
=\frac{119}{384}.
\]

#### 6.3.3 Unified magnitude and sign field

For the catalog rows, CR129b records

\[
|S_{3\rm body}|
=\frac{4q_{\rm eff}+D}{4R}\frac{M_{\rm native}}{R^3}
=M_{\rm native}\frac{4q_{\rm eff}+D}{4R^4},
\]

where

\[
q_{\rm eff}=
\begin{cases}
R,&q_{\rm abs}=0,\\
q_{\rm abs},&q_{\rm abs}>0.
\end{cases}
\]

The source row-sign rule is

\[
\operatorname{sgn}(S_{\rm debit})=
\begin{cases}
+1,&q_{\rm sign}\in\{\text{positive},\text{neutral}\},\\
-1,&q_{\rm sign}=\text{negative}.
\end{cases}
\]

Magnitude matches 76/76 rows; the row-sign field also matches 76/76. The
source separately keeps a first-principles derivation of the \(q\ge1\) sign
rule open. Thus empirical row-field closure and derivational closure are not
silently conflated.

### 6.4 Two-body/three-body structural bridge

#### 6.4.1 Expanding the identity

Define

\[
s_1=a+b+c
\]

and

\[
\Delta^2=(a-b)^2+(b-c)^2+(a-c)^2.
\]

Expand the sum coordinate:

\[
s_1^2=a^2+b^2+c^2+2ab+2bc+2ac.
\]

Expand the pairwise differences:

\[
\Delta^2
=2a^2+2b^2+2c^2-2ab-2bc-2ac.
\]

Adding cancels the mixed products:

\[
s_1^2+\Delta^2=3(a^2+b^2+c^2).
\]

Since \(D=3\), the CR129 law becomes

\[
M_3
=RD(a^2+b^2+c^2)
=R[s_1^2+\Delta^2].
\]

The result exposes a symmetric coordinate \(s_1^2\) plus a symmetrized
difference coordinate \(\Delta^2\). Linear signed differences cancel when all
ordered pairs are summed; squared differences survive.

#### 6.4.2 Why the two-body law stays separate

For \((1,2)\), incorrectly applying the three-body-style rewrite gives

\[
R[(1+2)^2+(1-2)^2]
=12(9+1)=120,
\]

whereas the locked two-body operator gives

\[
M_2(1,2)=27.
\]

The 2-to-3 transition is therefore not a notational rewrite of one universal
formula.

#### 6.4.3 Four-body conjecture boundary

CR130 proposes, for a future comparable four-body row,

\[
M_4=R[s_1^2+\Delta^2]
=4R(a^2+b^2+c^2+d^2)
=48\sum_i a_i^2.
\]

No four-body source rows exist in the scoped catalog. The formula is sealed as
`FORWARD_BLIND_NO_IN_SAMPLE_DATA`, not promoted into the current 321-row
generator census.

### 6.5 One-body charged-fermion ladder

#### 6.5.1 Class and formula

CR131 determines that `V4_1_SINGLE_WRITE` is a one-body
`fermion_half_write` family, not a scalar family. For its 90 rows,

\[
\boxed{
M_{\rm native}
=q_{\rm abs}R^dK(q_{\rm sign},\mathsf{status}).}
\]

For matter,

\[
K_+=\frac54
=\frac{\alpha_H^2+1}{\alpha_H^2},
\qquad
K_-=\frac32
=\frac{\alpha_H+1}{\alpha_H}.
\]

For antimatter, the coefficients swap across sign:

\[
\bar K_+=\frac32,
\qquad
\bar K_-=\frac54.
\]

#### 6.5.2 Radix-depth development

At \(q_{\rm abs}=1\), positive matter begins at

\[
d=0:\quad 1\cdot12^0\frac54=\frac54,
\]

then

\[
d=1:\quad 1\cdot12^1\frac54=15,
\]

and

\[
d=2:\quad 1\cdot12^2\frac54=180.
\]

Each depth step multiplies the bare ladder by \(R=12\). For negative matter
at the same address, the coefficient is \(3/2\), giving \((3/2,18,216)\).

#### 6.5.3 Conjugation correction

An initial sign-only coefficient hypothesis fails on the 42 antimatter rows.
Residual inspection reveals the matter/antimatter coefficient swap. With that
correction, all 90 rows match: 48 matter and 42 antimatter across depths
\((0,1,2)\). The correction is sealed for forward-blind use; it does not erase
the failed sign-only hypothesis.

### 6.6 One-body carriers

CR132 separates six bosonic carrier classes from the fermion ladder:

\[
M_{\rm native}(c)=\alpha_H^iD^j
\]

at the source-authorized lattice address for each massive class, with two
massless exceptions:

| Carrier class | Address | \(M_{\rm native}\) | \(S_{\rm debit}\) |
|---|---:|---:|---:|
| TENSOR_CARRIER | \((1,2)\) | \(2\cdot3^2=18\) | 0 |
| WEAK_VECTOR_CARRIER | \((0,2)\) | \(3^2=9\) | 0 |
| NEUTRAL_VECTOR_CARRIER | \((0,4)\) | \(3^4=81\) | 0 |
| COLOR_OWNER_CARRIER | \((3,0)\) | \(2^3=8\) | 0 |
| ROAD_LIGHT_CARRIER | massless | 0 | 0 |
| A_FIELD_CARRIER | massless | 0 | 0 |

The first attempted \(9/8\) carrier surcharge fails at the COLOR_OWNER row.
The corrected coefficient is \(C_1=1\): carriers occupy their bare structural
lattice values. All six source rows match, but their addresses remain
class-authorized; the result does not permit arbitrary new carrier classes to
claim unused lattice points.

### 6.7 One-body neutral-fermion ladder

CR133 retains the ladder architecture but changes its coefficient:

\[
\boxed{
M_{\rm native}
=pR^d\frac18
=pR^d2^{-D}.}
\]

The partition takes all eight values in \(\mathcal P\) across three depths,
giving \(8\times3=24\) rows. For \(p=3\),

\[
d=0:\quad \frac38,
\]

\[
d=1:\quad \frac{3\cdot12}{8}=\frac92,
\]

\[
d=2:\quad \frac{3\cdot144}{8}=54.
\]

All 24 rows match and all carry zero surface debit. Together CR131 and CR133
cover 114 one-body `fermion_half_write` rows with three coefficient families:
\(5/4\), \(3/2\) and \(1/8\).

### 6.8 Hidden source-support packet

#### 6.8.1 Native law

For `SOURCE_SUPPORT_PACKET`, CR134 locks

\[
\boxed{
M_{\rm native}(p)
=p+\frac{p^2}{R^2}
=p\left(1+\frac{p}{144}\right).}
\]

The derivation separates a bare connector value and its quadratic
radix-square response:

\[
M_{\rm native}-p=\frac{p^2}{R^2}.
\]

Dividing by \(p^2\) yields the exact invariant

\[
\frac{M_{\rm native}-p}{p^2}=\frac1{R^2}=\frac1{144}
\]

for all eight source rows.

#### 6.8.2 Worked endpoints

At \(p=1\),

\[
M_{\rm native}=1+\frac1{144}=\frac{145}{144}.
\]

At \(p=12=R\),

\[
M_{\rm native}=12+\frac{144}{144}=13.
\]

Despite their nonzero native values, every one of the eight rows is
`HIDDEN_SUPPORT_NOT_MATTER`, with

\[
S_{\rm debit}=0,
\qquad
q_A=0.
\]

The source-support packet is therefore structural inventory, not eight
physical particles and not a matter-source channel.

#### 6.8.3 Retest boundary

The formula was obtained by direct algebraic inspection of these same eight
rows. CR134 records 8/8 consistency and a forward-blind seal, while a dedicated
held-out/first-principles retest remains queued in its source record. Both facts
must travel with the law.

### 6.9 Law roster and scope firewall

| Class | Native operator | Current scoped evidence | Boundary |
|---|---|---|---|
| BOUND_COLOR_PAIR | \(Rab+D|a-b|\) | 36/36 | debit and symmetric observed offset separate; future-row falsifier open |
| OCTET three-body | \(RD\sum a_i^2\) | 76/76 | in-sample; debit separate |
| GROUND_BARYON three-body | same \(RD\sum a_i^2\) | 44/44, including 13 rejected | generation does not imply stability |
| three-body debit | \(M(4q_{\rm eff}+D)/(4R^4)\) plus source sign field | magnitude/sign 76/76 | first-principles \(q\ge1\) sign derivation open |
| four-body | \(4R\sum a_i^2\) | no rows | conjectural forward-blind boundary |
| V4_1 charged fermion | \(q_{\rm abs}R^dK\) | 90/90 | K swap found in-sample; observed/debit lane separate |
| carrier lattice | authorized \(\alpha_H^iD^j\) or massless | 6/6 | no free allocation of new classes |
| OUTER_BINARY_NEUTRAL | \(pR^d/8\) | 24/24 | scoped to neutral class |
| SOURCE_SUPPORT_PACKET | \(p+p^2/R^2\) | 8/8 | hidden support, no debit or \(q_A\); held-out derivation open |

## 7. Structural bucket interpretation

QP093A's bucket map attaches organizational roles to the current source rows.
It does not alter the law domains above. The load-bearing cross-bucket route is

    partition address -> native generator -> structural candidate value
                      -> stability bucket -> admitted, retained or rejected.

The 13 rejected three-body closures that still match \(M_3\) show that the
generator crosses stability buckets without erasing them. Carrier and hidden-
support buckets likewise retain valid structural values while remaining
outside matter. QP093A interprets CR252's 321 rows; it does not promote every
generated value or authorize the stale SAM_321 exemplar.

## 8. Locked replay and preserved controls

LC04 replays 65/65 checks across 13/13 layers and rejects 11/11 wrong
controls. It carries four essential boundaries into the present chapter:

1. labels and measured masses are reveal-only;
2. \(q_A\) and debit are not direct mass values;
3. \(\Theta18\) is carrier/support, not matter; and
4. CR128–CR134 exact matches remain in-sample generator consistency unless a
   separate source marks a genuinely forward-blind result.

The generator suite's own deviations remain visible:

- two-body and three-body operators are not merged;
- pairwise debit and global \(1/8\) surcharge fail for the three-body debit;
- the sign-only charged-fermion coefficient fails on antimatter before the
  conjugation swap is installed;
- a \(9/8\) carrier surcharge fails before \(C_1=1\) is installed; and
- the hidden-support law retains its requested held-out derivation.

This is the development chain, not merely a catalog of final formulas.

## 9. Typed serialization into computation

### 9.1 What Volume III receives

The computation interface receives typed records:

```text
connector address
carrier row
matter or antimatter row
native class operator
debit and source-support channels
stability/admission fields
closure addresses
exact rational values
source row key and provenance.
```

Exact rationals such as \(1/8\), \(5/4\), \(3/2\), \(17/16\) and \(1/144\)
are retained before decimal display. A scalar alone never selects the type.

### 9.2 N100 pruning

The current N100 computation basis follows five \(p{:}9\) removals. That
projection does not rewrite the 35- or 321-row source surfaces. A compiler must
retain the original key even when a row is excluded from one executable basis.

### 9.3 Current F81 join boundary

G1 audits 100/100 unique N100 source keys and a 72-row aggregate connector-
incidence partial domain. The F81 target has 81 semantic sites and ten contact
classes, but the source provides zero elementwise QP-to-F81 assignments.
Consequently the contact lane is not executed and the exact status is

```text
PARTIAL_DOMAIN__ELEMENTWISE_F81_JOIN_OPEN.
```

The missing executable input is one source-authorized relation from a QP
candidate/template to an F81 semantic site or source-native address class.
Geometry, hash proximity or outcome fitting cannot substitute for that key.

## 10. Established result and current boundaries

The current sources establish:

1. CR252 deterministically reconstructs the exact 321-row catalog and its
   seven-bin census.
2. Native row generation is class-specific; no one formula is applied across
   two-body, three-body, one-body fermion, carrier and hidden-support classes.
3. Generator output, stability, matter admission and observed reveal are
   separate stages.
4. The scoped formulas reproduce every eligible current row in their stated
   domains, with the in-sample/forward-blind status preserved per source.
5. Failed intermediate controls locate the corrected forms and remain part of
   the evidence chain.
6. The four-body continuation, some first-principles sign/law derivations and
   the elementwise N100-to-F81 compiler join remain open.
7. The stale `SAM_321` exemplar is organizational only; present sources
   control technical content.

No project-wide result classification is assigned in this document because
all registered crosswalk rows carry `result_classification: null`. Historical
source verdict/status values remain exactly attributed below.

## 11. Related SAMA documents and forward handoff

`SAMA-D000026` supplies the row schema and census firewall. This chapter fills
that contract with the current 321-row census and the scoped generator laws.

The downstream Volume II lift and binding documents receive three guarded
channels:

```text
M_native generation
S_debit lift/readout
qA source support after matter admission.
```

They must not be collapsed. The Volume III parent receives the same rows and
operators with exact source keys and rational arithmetic, while keeping its
N100 selection and F81 join as computation-layer decisions.

## Test and result index

| Test record key | Role | Source result/status | Result artifact | Test folder |
|---|---|---|---|---|
| [`CR:CR119@09a`](../../tests/courtroom/09a-particle-mass-chain-cr119-particle-matter-periodic-vault-reveal/README.md) | Historical 321-row reveal lineage | `CLEAN`; source verdict `PASS` | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/CR119_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL) |
| [`CR:CR252@09a`](../../tests/courtroom/09a-particle-mass-chain-cr252-particle-catalog-spine-refresh/README.md) | Current deterministic 321-row correction | Source verdict `PASS` | [result](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_result.md) | [folder](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH) |
| [`LC:LC04`](../../tests/courtroom/16-the-last-campaign-lc04-particle-mass-chain-table-replay/README.md) | Locked base/catalog/generator replay | `LC04_PASS_PARTICLE_MASS_CHAIN_TABLE_REPLAY_FROM_LOCKED_PRIMITIVE_STACK` | [result](../../courtroom/16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY/LC04_result.md) | [folder](../../courtroom/16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY) |
| [`CR:CR128@13`](../../tests/courtroom/13-cern-independent-tests-cr128-bound-color-pair-mass-law-v1/README.md) | Two-body BOUND_COLOR_PAIR law | `CLEAN`; source verdict `PASS`; 36/36 | [result](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR128_BOUND_COLOR_PAIR_MASS_LAW_V1/CR128_result.md) | [folder](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR128_BOUND_COLOR_PAIR_MASS_LAW_V1) |
| [`CR:CR129@13`](../../tests/courtroom/13-cern-independent-tests-cr129-octet-composite-3body-mass-law-v1/README.md) | OCTET three-body generator | `CLEAN`; source verdict `PASS`; 76/76 | [result](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129_OCTET_COMPOSITE_3BODY_MASS_LAW_V1/CR129_result.md) | [folder](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129_OCTET_COMPOSITE_3BODY_MASS_LAW_V1) |
| [`CR:CR129b@13`](../../tests/courtroom/13-cern-independent-tests-cr129b-3body-s-debit-magnitude-law-v1/README.md) | Three-body debit deviation and corrected law | `CLEAN`; source verdict `PASS`; magnitude 76/76 | [result](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129b_3BODY_S_DEBIT_MAGNITUDE_LAW_V1/CR129b_result.md) | [folder](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129b_3BODY_S_DEBIT_MAGNITUDE_LAW_V1) |
| [`CR:CR129c@13`](../../tests/courtroom/13-cern-independent-tests-cr129c-3body-universal-generator-ground-baryon/README.md) | Three-body extension across stability statuses | `CLEAN`; source verdict `PASS`; extension 44/44 | [result](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129c_3BODY_UNIVERSAL_GENERATOR_GROUND_BARYON/CR129c_result.md) | [folder](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129c_3BODY_UNIVERSAL_GENERATOR_GROUND_BARYON) |
| [`CR:CR130@13`](../../tests/courtroom/13-cern-independent-tests-cr130-2body-3body-structural-bridge/README.md) | Two-/three-body identity and four-body conjecture boundary | `CLEAN`; source verdict `PASS`; four-body no in-sample rows | [result](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR130_2BODY_3BODY_STRUCTURAL_BRIDGE/CR130_result.md) | [folder](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR130_2BODY_3BODY_STRUCTURAL_BRIDGE) |
| [`CR:CR131@13`](../../tests/courtroom/13-cern-independent-tests-cr131-v4-1-single-write-fermion-ladder-law-v1/README.md) | Charged one-body fermion ladder and K-swap correction | `CLEAN`; source verdict `PASS`; 90/90 | [result](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1/CR131_result.md) | [folder](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1) |
| [`CR:CR132@13`](../../tests/courtroom/13-cern-independent-tests-cr132-1body-carrier-lattice-law-v1/README.md) | One-body carrier lattice and no-surcharge correction | `CLEAN`; source verdict `PASS`; 6/6 | [result](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR132_1BODY_CARRIER_LATTICE_LAW_V1/CR132_result.md) | [folder](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR132_1BODY_CARRIER_LATTICE_LAW_V1) |
| [`CR:CR133@13`](../../tests/courtroom/13-cern-independent-tests-cr133-outer-binary-neutral-fermion-ladder-law-v1/README.md) | Neutral one-body fermion ladder | `CLEAN`; source verdict `PASS`; 24/24 | [result](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1/CR133_result.md) | [folder](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1) |
| [`CR:CR134@13`](../../tests/courtroom/13-cern-independent-tests-cr134-source-support-packet-law-v1/README.md) | Hidden source-support law and held-out retest boundary | `CLEAN`; source verdict `PASS`; 8/8 | [result](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR134_SOURCE_SUPPORT_PACKET_LAW_V1/CR134_result.md) | [folder](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR134_SOURCE_SUPPORT_PACKET_LAW_V1) |
| [`QP:QP093A`](../../tests/courtroom/workbench-misc/README.md) | 321-row structural bucket map | Source artifact recorded | [result](../../courtroom/Workbench-misc/QP093A_321_ROW_STRUCTURAL_INTERPRETATION.md) | [folder](../../courtroom/Workbench-misc) |
| `G:G1@SAM-RESEARCH` | Typed N100 serialization and open F81 join | `PARTIAL_DOMAIN__ELEMENTWISE_F81_JOIN_OPEN` | [result](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/2b45b6edf1fb80b70c0193f63e3d32dd218967d6/SLC/SAM_LANGUAGE/SAM_LANGUAGE_CONTACT_NATIVE_SUCCESSOR_DESIGN/SLC_H14F_EXACT_N100_PARTICLE_SPIN_G1_V1/G1_SOURCE_NATIVE_COMPILER_AUDIT.json) | [folder](https://github.com/iwtbotiwtwot/SAM_Research_Project/tree/2b45b6edf1fb80b70c0193f63e3d32dd218967d6/SLC/SAM_LANGUAGE/SAM_LANGUAGE_CONTACT_NATIVE_SUCCESSOR_DESIGN/SLC_H14F_EXACT_N100_PARTICLE_SPIN_G1_V1) |

## Atomic SAMA source records

| Record ID | Role in this document |
|---|---|
| `SAMA-C000139-R001` | Source/schema/address/operator row identity. |
| `SAMA-C000140-R001` | Finite-surface census firewall. |
| `SAMA-C000141-R001` | Exact current 321-row bin census. |
| `SAMA-C000144-R001` | Labels and measured masses as downstream reveals. |
| `SAMA-C000145-R001` | N100 pruning/physical-source firewall. |
| `SAMA-C000146-R001` | Current-source reconstruction route and stale-exemplar boundary. |
| `SAMA-C000184-R001` | Typed exact-rational matter-to-computation serialization. |

## External references

No external bibliographic source is used directly. Observed labels or masses
mentioned by source tests remain downstream comparators in those artifacts;
the chapter's construction is entirely registry-routed.

## Revision and approval

This exact revision has `reviewed_and_approved: false` until Sean Brady
explicitly approves it.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`QP:QP093A`](../../tests/courtroom/workbench-misc/README.md) | [All package files](../../tests/courtroom/workbench-misc/README.md) | [All package files](../../tests/courtroom/workbench-misc/README.md) | [All files](../../tests/courtroom/workbench-misc/README.md) | [All package files](../../tests/courtroom/workbench-misc/README.md) | [All 7 files](../../tests/courtroom/workbench-misc/README.md) |
| [`CR:CR119@09a`](../../tests/courtroom/09a-particle-mass-chain-cr119-particle-matter-periodic-vault-reveal/README.md) | [All package files](../../tests/courtroom/09a-particle-mass-chain-cr119-particle-matter-periodic-vault-reveal/README.md) | [CR119_runner.py](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/CR119_runner.py) | [CR119_wrong_controls.csv](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/CR119_wrong_controls.csv)<br>[CR119_wrong_controls.csv.sha256.txt](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/sha256_sidecars/CR119_wrong_controls.csv.sha256.txt) | [CR119_result.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/CR119_result.md)<br>[CR119_summary.json](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/CR119_summary.json)<br>[CR119_result.md.sha256.txt](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/sha256_sidecars/CR119_result.md.sha256.txt)<br>[CR119_summary.json.sha256.txt](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR119_PARTICLE_MATTER_PERIODIC_VAULT_REVEAL/sha256_sidecars/CR119_summary.json.sha256.txt) | [All 36 files](../../tests/courtroom/09a-particle-mass-chain-cr119-particle-matter-periodic-vault-reveal/README.md) |
| [`CR:CR128@13`](../../tests/courtroom/13-cern-independent-tests-cr128-bound-color-pair-mass-law-v1/README.md) | [All package files](../../tests/courtroom/13-cern-independent-tests-cr128-bound-color-pair-mass-law-v1/README.md) | [CR128_runner.py](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR128_BOUND_COLOR_PAIR_MASS_LAW_V1/CR128_runner.py) | [CR128_runner.py](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR128_BOUND_COLOR_PAIR_MASS_LAW_V1/CR128_runner.py)<br>[CR128_result.md](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR128_BOUND_COLOR_PAIR_MASS_LAW_V1/CR128_result.md)<br>[CR128_summary.json](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR128_BOUND_COLOR_PAIR_MASS_LAW_V1/CR128_summary.json) | [CR128_result.md](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR128_BOUND_COLOR_PAIR_MASS_LAW_V1/CR128_result.md)<br>[CR128_summary.json](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR128_BOUND_COLOR_PAIR_MASS_LAW_V1/CR128_summary.json) | [All 6 files](../../tests/courtroom/13-cern-independent-tests-cr128-bound-color-pair-mass-law-v1/README.md) |
| [`CR:CR129@13`](../../tests/courtroom/13-cern-independent-tests-cr129-octet-composite-3body-mass-law-v1/README.md) | [All package files](../../tests/courtroom/13-cern-independent-tests-cr129-octet-composite-3body-mass-law-v1/README.md) | [CR129_runner.py](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129_OCTET_COMPOSITE_3BODY_MASS_LAW_V1/CR129_runner.py) | [CR129_runner.py](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129_OCTET_COMPOSITE_3BODY_MASS_LAW_V1/CR129_runner.py)<br>[CR129_result.md](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129_OCTET_COMPOSITE_3BODY_MASS_LAW_V1/CR129_result.md)<br>[CR129_summary.json](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129_OCTET_COMPOSITE_3BODY_MASS_LAW_V1/CR129_summary.json) | [CR129_result.md](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129_OCTET_COMPOSITE_3BODY_MASS_LAW_V1/CR129_result.md)<br>[CR129_summary.json](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129_OCTET_COMPOSITE_3BODY_MASS_LAW_V1/CR129_summary.json) | [All 8 files](../../tests/courtroom/13-cern-independent-tests-cr129-octet-composite-3body-mass-law-v1/README.md) |
| [`CR:CR129b@13`](../../tests/courtroom/13-cern-independent-tests-cr129b-3body-s-debit-magnitude-law-v1/README.md) | [All package files](../../tests/courtroom/13-cern-independent-tests-cr129b-3body-s-debit-magnitude-law-v1/README.md) | [CR129b_runner.py](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129b_3BODY_S_DEBIT_MAGNITUDE_LAW_V1/CR129b_runner.py) | [CR129b_runner.py](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129b_3BODY_S_DEBIT_MAGNITUDE_LAW_V1/CR129b_runner.py)<br>[CR129b_result.md](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129b_3BODY_S_DEBIT_MAGNITUDE_LAW_V1/CR129b_result.md)<br>[CR129b_summary.json](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129b_3BODY_S_DEBIT_MAGNITUDE_LAW_V1/CR129b_summary.json) | [CR129b_result.md](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129b_3BODY_S_DEBIT_MAGNITUDE_LAW_V1/CR129b_result.md)<br>[CR129b_summary.json](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129b_3BODY_S_DEBIT_MAGNITUDE_LAW_V1/CR129b_summary.json) | [All 11 files](../../tests/courtroom/13-cern-independent-tests-cr129b-3body-s-debit-magnitude-law-v1/README.md) |
| [`CR:CR129c@13`](../../tests/courtroom/13-cern-independent-tests-cr129c-3body-universal-generator-ground-baryon/README.md) | [All package files](../../tests/courtroom/13-cern-independent-tests-cr129c-3body-universal-generator-ground-baryon/README.md) | [CR129c_runner.py](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129c_3BODY_UNIVERSAL_GENERATOR_GROUND_BARYON/CR129c_runner.py) | [CR129c_runner.py](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129c_3BODY_UNIVERSAL_GENERATOR_GROUND_BARYON/CR129c_runner.py)<br>[CR129c_result.md](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129c_3BODY_UNIVERSAL_GENERATOR_GROUND_BARYON/CR129c_result.md)<br>[CR129c_summary.json](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129c_3BODY_UNIVERSAL_GENERATOR_GROUND_BARYON/CR129c_summary.json) | [CR129c_result.md](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129c_3BODY_UNIVERSAL_GENERATOR_GROUND_BARYON/CR129c_result.md)<br>[CR129c_summary.json](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR129c_3BODY_UNIVERSAL_GENERATOR_GROUND_BARYON/CR129c_summary.json) | [All 6 files](../../tests/courtroom/13-cern-independent-tests-cr129c-3body-universal-generator-ground-baryon/README.md) |
| [`CR:CR130@13`](../../tests/courtroom/13-cern-independent-tests-cr130-2body-3body-structural-bridge/README.md) | [All package files](../../tests/courtroom/13-cern-independent-tests-cr130-2body-3body-structural-bridge/README.md) | [CR130_runner.py](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR130_2BODY_3BODY_STRUCTURAL_BRIDGE/CR130_runner.py) | [CR130_runner.py](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR130_2BODY_3BODY_STRUCTURAL_BRIDGE/CR130_runner.py)<br>[CR130_result.md](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR130_2BODY_3BODY_STRUCTURAL_BRIDGE/CR130_result.md)<br>[CR130_summary.json](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR130_2BODY_3BODY_STRUCTURAL_BRIDGE/CR130_summary.json) | [CR130_result.md](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR130_2BODY_3BODY_STRUCTURAL_BRIDGE/CR130_result.md)<br>[CR130_summary.json](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR130_2BODY_3BODY_STRUCTURAL_BRIDGE/CR130_summary.json) | [All 6 files](../../tests/courtroom/13-cern-independent-tests-cr130-2body-3body-structural-bridge/README.md) |
| [`CR:CR131@13`](../../tests/courtroom/13-cern-independent-tests-cr131-v4-1-single-write-fermion-ladder-law-v1/README.md) | [All package files](../../tests/courtroom/13-cern-independent-tests-cr131-v4-1-single-write-fermion-ladder-law-v1/README.md) | [CR131_runner.py](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1/CR131_runner.py) | [CR131_runner.py](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1/CR131_runner.py)<br>[CR131_result.md](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1/CR131_result.md)<br>[CR131_summary.json](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1/CR131_summary.json) | [CR131_result.md](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1/CR131_result.md)<br>[CR131_summary.json](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR131_V4_1_SINGLE_WRITE_FERMION_LADDER_LAW_V1/CR131_summary.json) | [All 7 files](../../tests/courtroom/13-cern-independent-tests-cr131-v4-1-single-write-fermion-ladder-law-v1/README.md) |
| [`CR:CR132@13`](../../tests/courtroom/13-cern-independent-tests-cr132-1body-carrier-lattice-law-v1/README.md) | [All package files](../../tests/courtroom/13-cern-independent-tests-cr132-1body-carrier-lattice-law-v1/README.md) | [CR132_runner.py](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR132_1BODY_CARRIER_LATTICE_LAW_V1/CR132_runner.py) | [CR132_runner.py](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR132_1BODY_CARRIER_LATTICE_LAW_V1/CR132_runner.py)<br>[CR132_result.md](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR132_1BODY_CARRIER_LATTICE_LAW_V1/CR132_result.md)<br>[CR132_summary.json](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR132_1BODY_CARRIER_LATTICE_LAW_V1/CR132_summary.json) | [CR132_result.md](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR132_1BODY_CARRIER_LATTICE_LAW_V1/CR132_result.md)<br>[CR132_summary.json](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR132_1BODY_CARRIER_LATTICE_LAW_V1/CR132_summary.json) | [All 7 files](../../tests/courtroom/13-cern-independent-tests-cr132-1body-carrier-lattice-law-v1/README.md) |
| [`CR:CR133@13`](../../tests/courtroom/13-cern-independent-tests-cr133-outer-binary-neutral-fermion-ladder-law-v1/README.md) | [All package files](../../tests/courtroom/13-cern-independent-tests-cr133-outer-binary-neutral-fermion-ladder-law-v1/README.md) | [CR133_runner.py](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1/CR133_runner.py) | [CR133_runner.py](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1/CR133_runner.py)<br>[CR133_result.md](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1/CR133_result.md)<br>[CR133_summary.json](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1/CR133_summary.json) | [CR133_result.md](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1/CR133_result.md)<br>[CR133_summary.json](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR133_OUTER_BINARY_NEUTRAL_FERMION_LADDER_LAW_V1/CR133_summary.json) | [All 7 files](../../tests/courtroom/13-cern-independent-tests-cr133-outer-binary-neutral-fermion-ladder-law-v1/README.md) |
| [`CR:CR134@13`](../../tests/courtroom/13-cern-independent-tests-cr134-source-support-packet-law-v1/README.md) | [All package files](../../tests/courtroom/13-cern-independent-tests-cr134-source-support-packet-law-v1/README.md) | [CR134_runner.py](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR134_SOURCE_SUPPORT_PACKET_LAW_V1/CR134_runner.py) | [CR134_runner.py](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR134_SOURCE_SUPPORT_PACKET_LAW_V1/CR134_runner.py)<br>[CR134_result.md](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR134_SOURCE_SUPPORT_PACKET_LAW_V1/CR134_result.md)<br>[CR134_summary.json](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR134_SOURCE_SUPPORT_PACKET_LAW_V1/CR134_summary.json) | [CR134_result.md](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR134_SOURCE_SUPPORT_PACKET_LAW_V1/CR134_result.md)<br>[CR134_summary.json](../../courtroom/13_CERN_INDEPENDENT_TESTS/CR134_SOURCE_SUPPORT_PACKET_LAW_V1/CR134_summary.json) | [All 7 files](../../tests/courtroom/13-cern-independent-tests-cr134-source-support-packet-law-v1/README.md) |
| [`CR:CR252@09a`](../../tests/courtroom/09a-particle-mass-chain-cr252-particle-catalog-spine-refresh/README.md) | [CR252_PRECOMMIT.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_PRECOMMIT.md)<br>[CR252_PRECOMMIT_AMENDMENT.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_PRECOMMIT_AMENDMENT.md) | [CR252_runner.py](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_runner.py) | [CR252_wrong_controls.csv](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_wrong_controls.csv)<br>[CR252_wrong_controls_FIRSTRUN_FAIL_spec_error.csv](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_wrong_controls_FIRSTRUN_FAIL_spec_error.csv) | [CR252_result.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_result.md)<br>[CR252_result_FIRSTRUN_FAIL_spec_error.md](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_result_FIRSTRUN_FAIL_spec_error.md)<br>[CR252_spine_input_audit.csv](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_spine_input_audit.csv)<br>[CR252_summary.json](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_summary.json)<br>[CR252_summary_FIRSTRUN_FAIL_spec_error.json](../../courtroom/09a_PARTICLE_MASS_CHAIN/CR252_PARTICLE_CATALOG_SPINE_REFRESH/CR252_summary_FIRSTRUN_FAIL_spec_error.json) | [All 20 files](../../tests/courtroom/09a-particle-mass-chain-cr252-particle-catalog-spine-refresh/README.md) |
| [`LC:LC04`](../../tests/courtroom/16-the-last-campaign-lc04-particle-mass-chain-table-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc04-particle-mass-chain-table-replay/README.md) | [All package files](../../tests/courtroom/16-the-last-campaign-lc04-particle-mass-chain-table-replay/README.md) | [LC04_wrong_controls.csv](../../courtroom/16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY/LC04_wrong_controls.csv) | [LC04_result.md](../../courtroom/16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY/LC04_result.md)<br>[LC04_summary.json](../../courtroom/16_THE_LAST_CAMPAIGN/LC04_PARTICLE_MASS_CHAIN_TABLE_REPLAY/LC04_summary.json) | [All 9 files](../../tests/courtroom/16-the-last-campaign-lc04-particle-mass-chain-table-replay/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000027`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/FINITE_PARTICLE_GRAMMAR_AND_321_ROW_CENSUS.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol II–III | SAMA-D000027 | Particle Grammar | Current Finite Particle Grammar and Exact 321-Row Census |

| Document field | Value |
|---|---|
| Purpose | Rebuild the current finite particle grammar and exact 321-row census from present authority rather than stale manuscript content. |
| Prerequisite documents | `SAMA-D000026` |
| Used by | Downstream Volume II lift, binding and matter-return documents; Volume III typed computation interface; generated from the document catalog |

</details>
