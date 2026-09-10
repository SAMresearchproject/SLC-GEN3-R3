[SAM](../../README.md) · [Volume III](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Jacobian Program and Clean Restart

## Conceptual abstract

The Jacobian program asks how an exact polynomial map can return its target
state while retaining a nontrivial history of sheets, braids, escape and
projective completion. That is a mathematical and computational question, so
JC1 and HF1--HF6TH belong in Volume III. Their earlier matter-volume-labelled files
remain immutable provenance, but relocation changes placement and current
interpretation rather than any executed result.

JC1 begins with the exact polynomial map

\[
\begin{aligned}
P(x,y,z)&=(1+xy)^3z+y^2(1+xy)(4+3xy),\\
Q(x,y,z)&=y+3x(1+xy)^2z+3xy^2(4+3xy),\\
R(x,y,z)&=2x-3x^2y-x^3z,
\end{aligned}
\]

whose Jacobian determinant simplifies identically to

\[
\det D(P,Q,R)=-2.
\]

An exact elimination chart produces a cubic fiber polynomial, its resultant
and discriminant. On the frozen slice \(V=-16/27,R=1\), one winding around
\(U=0\) transposes two escaping sheets, while double winding returns the sheet
permutation to the identity. The same winding programs compile through
Complete Exact Write on one Theta18 axis. Four positive writes, four negative
writes and eight positive writes all have zero compiled translation across all
262,144 addresses, yet their ordered W9 receipts retain four, four and eight
events with different orientations and semantic hashes. JC1 passes 18/18;
independent validation passes 9/9. Its exact classification is **The test result suggests strong contact with the concept.**

The portable result is narrower and stronger than an endpoint slogan:
endpoint equality does not imply program-history equality. It does not by
itself install JC1 monodromy, a quotient, a Newton field or a tensor/path-jet
field as a matter payload.

HF1--HF6TH then form a valuable but historically scaffolded discovery chain:
local reducers and a chosen `Z4^2` cell grammar; nonproper meridians and exact
polynomial cells; finite versus projective sheet custody; path-dependent
escape corrections; blinded path-jet discriminators; fresh-map transfer;
Newton-polygon signatures; and a complete mixed-jet compiler. Every executed
finding and correction remains in custody. The current clean restart does not
assume that the HF2 torus, its generators, `H_SAM`, W9 or any carrier/matter
meaning arises naturally from the polynomial map.

The restart therefore reverses the order of dependence: reconstruct the
source algebra independently, derive invariants from actual fibers and the
regular-value set, freeze algebraically generated loops, examine monodromy,
properness and infinity, and only then reveal legacy HF observations. An
optional SAM comparison requires an explicit compiler. A later matter application
requires carrier compilation, reciprocal preservation, an identified matter
consumer and a load-bearing controlled output change. None has executed. This
future bridge is not standalone SAMA Volume IV, which is the RH program.

## 1. Placement, question and authority

### 1.1 Governing question

The clean governing question is:

> What global algebraic or topological invariant arises naturally from the
> exact JC1 polynomial map before an SLC rewrite grammar, W9 receipt,
> A-field-carrier role or matter interpretation is imported?

The reading order is

```text
exact polynomial source
  -> affine fibers and eliminant
  -> regular-value loops and monodromy
  -> nonproper and projective behavior
  -> exact endpoint-return/history distinction
  -> preserved HF clue deck
  -> unexecuted source-derived restart
  -> optional explicit SAM compiler
  -> optional four-join future matter-applicability test
```

### 1.2 Current placement

H000211 relocates JC1/HF1--HF6TH from a former matter-volume interpretation into
Volume III computation. The current rule is:

- executable result artifacts control their exact outputs;
- immutable history preserves the route, including superseded literal
  bridges and corrections;
- `volume_III/SAM_VOLUME_III_JACOBIAN_PROGRAM.md` controls current program
  routing; and
- live SLC authority remains frozen `SLCQ2-RZ`, whose delegated base installs
  no Jacobian or physical-matter result.

No historical file is deleted or retroactively reclassified. In particular,
H000195/H000196 remain the record of a literal quotient/carrier bridge route,
while H000197 and H000211 remove that bridge interpretation from current
authority.

## 2. Exact JC1 source algebra

### 2.1 Polynomial map and constant Jacobian

Let

\[
F:\mathbb A^3\to\mathbb A^3,
\qquad
F(x,y,z)=(P,Q,R)
\]

with \(P,Q,R\) as stated above. The derivative matrix is formed by differentiating
each component with respect to ((x,y,z)). Exact polynomial expansion and
factorization of its determinant cancel every variable-dependent term and
leave

\[
\det DF=-2.
\]

The determinant is nonzero at every affine source point. Consequently the
affine map has no local Jacobian singularity. This does not imply properness:
source branches may still escape to infinity while their target values remain
finite.

### 2.2 Elimination chart

JC1 uses

\[
x=\frac1m,
\qquad
y=m(s-1),
\qquad
z=(5-3s-m)m^2.
\]

Substitution into \(P,Q,R\), followed by elimination of \(m\), gives the exact
resultant

\[
\operatorname{Res}_m(U-Q,V-P)
=s^3\Phi(U,V;s),
\]

where

\[
\Phi(U,V;s)=K(U,V)s^3+(U^2-12V)s-4V
\]

and

\[
K(U,V)=U^3-U^2-18UV+27V^2+16V.
\]

The cubic discriminant factors as

\[
\operatorname{Disc}_s\Phi
=-4\bigl(U^3-18UV+54V^2\bigr)^2K(U,V).
\]

Thus the two load-bearing target components are

\[
D(U,V)=U^3-18UV+54V^2
\]

and \(K(U,V)\). Their repeated and simple factors distinguish finite-root braid
behavior from coefficient loss and projective escape.

### 2.3 Exact calibration and loss fibers

The target \((P,Q,R)=(-1,1,-1)\) has the exact eliminated \(x\)-fiber

\[
(x-1)(3x+1)(3x+2),
\]

with three exact sources

\[
(1,-2,9),
\quad
(-1/3,4,27),
\quad
(-2/3,-1/2,-9/8).
\]

Each maps to the same target and has Jacobian \(-2\).

At the coefficient-loss target

\[
(U,V,R)=(0,-16/27,1),
\]

the unique finite source is

\[
(x,y,z)=(1/2,-8/3,16).
\]

The eliminated \(x\)-fiber drops to \((2x-1)/2\). Two other cubic branches have
moved to projective infinity rather than collided at an affine Jacobian zero.

## 3. Monodromy from the fiber

### 3.1 Frozen slice

On \(V=-16/27\),

\[
K(U,-16/27)=\frac{U(3U^2-3U+32)}3.
\]

At \(U=0\), the cubic coefficient vanishes while

\[
\Phi(0,-16/27;s)
=\frac{64}{9}s+\frac{64}{27}.
\]

One branch therefore tends to \(s=-1/3\). Balancing the cubic and linear terms
for the other two branches gives

\[
s^2U\longrightarrow-\frac23.
\]

Those branches escape with magnitude proportional to \(|U|^{-1/2}\).

### 3.2 Loop continuation

Take a small circle

\[
U(\theta)=\rho e^{i\theta},
\qquad
V=-16/27,
\qquad
R=1.
\]

At each step, numerically continue the three roots of \(\Phi\) by minimum
matching to the preceding roots. A positive winding and a negative winding
both return the finite branch and exchange the two escaping branches:

\[
[0,1,2]\longmapsto[0,2,1].
\]

The opposite loop orientation changes path direction but not the
transposition. A double winding applies the transposition twice:

\[
(1\ 2)^2=e,
\]

so the sheet permutation returns to `[0,1,2]`. The offset zero-winding control
also returns identity. Maximum recorded fiber residuals stay below
\(5\times10^{-13}\) on the winding paths.

This chain separates target return, sheet permutation and path winding. Double
winding can have identity permutation while still containing a nonempty
ordered program.

## 4. Exact Write compilation and retained history

### 4.1 Theta18 event map

Theta18 addresses form \(\mathbb Z_4^9\) in packed two-bit coordinates. On axis
\(j\), one positive or negative event applies the exact signed \(\mathbb Z_4\)
step. For axis zero and initial address zero, the positive program visits

```text
0 -> 1 -> 512 -> 513 -> 0
```

while the negative program visits

```text
0 -> 513 -> 512 -> 1 -> 0.
```

Four equal signed steps are zero modulo four. Hence the programs

\[
w_+=(0,+1)^4,
\qquad
w_-=(0,-1)^4,
\qquad
w_{++}=(0,+1)^8
\]

all compile to translation zero. Because the compiled action is a group
translation, zero translation returns every one of the 262,144 input
addresses, not only address zero. Sequential and compiled native execution
agree on the full address set.

### 4.2 Ordered receipt construction

Before endpoint collapse, retain for event \(r\)

\[
(j_r,\epsilon_r,a_{r-1},a_r).
\]

The JC1-to-W9 adapter assigns event \(r\) to reciprocal channel \(r\), with

\[
L_r=\epsilon_r,
\qquad
R_r=-\epsilon_r.
\]

The W9 common and directional components are

\[
C_r=L_r+R_r=0,
\qquad
A_r=L_r-R_r=2\epsilon_r.
\]

Therefore the positive four-event receipt begins
((2,2,2,2)), the negative receipt begins ((-2,-2,-2,-2)), and the double
receipt has eight positive entries. Their \(L^1\) receipt norms are 8, 8 and
16, and their semantic hashes are distinct. Reciprocal reconstruction is

\[
L_r=\frac{C_r+A_r}{2},
\qquad
R_r=\frac{C_r-A_r}{2}.
\]

The exact endpoint is the same; event count, sign, order and receipt remain
different.

### 4.3 JC1 result and boundary

The principal campaign passes 18/18 and independent validation passes 9/9.
The result is classified:

**The test result suggests strong contact with the concept.**

The established portable statement is:

```text
endpoint compilation can erase which closed program occurred;
an ordered event receipt can retain that distinction.
```

This directly joins the append-only reel of `SAMA-D000042`. It does not imply
that a particular carrier, intersection or matter ledger consumes the full
JC1 polynomial object.

## 5. Preserved HF1--HF6TH lineage

### 5.1 HF1: reducer foundation

HF1 separates endpoint action in \(\mathbb Z_4^9\) from an unwrapped signed lift
in \(\mathbb Z^9\). For an endpoint-returning word \(w\),

\[
\omega(w)=\widetilde z(w)/4\in\mathbb Z^9.
\]

It reduces only adjacent exact reciprocal writes with matching route,
payload, account anchor and completion type. Four same-orientation writes
retain a completed turn. Generic freeze passes 42/42, JC1 calibration 41/41
and independent reconstruction 54/54. A first 41/42 receipt is preserved:
its validator mistook boundary prose for embedded map coefficients. The
corrected validator checks actual coefficient markers. HF1's classification
is **The test result suggests strong contact with the concept.**

### 5.2 HF2: chosen local `Z4^2` grammar

HF2 installs reciprocal bigons and signed commuting squares on a chosen
(`x`,`y`) `Z4^2` surface. Termination yields normal form

\[
x^my^n,
\]

while endpoint compilation retains only \((m\bmod4,n\bmod4)\). The resulting
history quotient is

\[
H_{local}\cong\mathbb Z^2.
\]

Among 87,381 words through length eight, 8,909 return the endpoint, 5,341 are
locally null and 3,568 retain nonzero history. This falsifies the fixed target
that every endpoint-returning word in that installed grammar is locally
exact-null. The result does not establish that the chosen torus or its two
generators are natural invariants of JC1.

### 5.3 HF3/HF4: nonproper obstruction and exact regular cell

HF3 follows the (K/x) meridian. Its radial filling reaches coefficient loss:
one source stays finite while two escape with exponent \(-1/2\). Positive,
negative and double filling attempts remain `NONPROPER_OBSTRUCTION`; no exact
cell is promoted. HF3 passes 28/28, separated promotion 24/24 and independent
reconstruction 46/46, with strong contact at the obstruction-localization
scope.

HF4 shows the obstruction is not a fixed-slice artifact by constructing the
full nonproper hypersurface and its nonzero meridian linking. Separately, a
(D/y) meridian has identity sheet permutation, pure-braid winding one and no
escape. An exact Gaussian-rational source disk certifies boundary ((0,1)), so

\[
\Lambda_{JC1}^{certified}=\langle(0,1)\rangle,
\qquad
\mathbb Z^2/\Lambda_{JC1}^{certified}\cong\mathbb Z.
\]

Two implementation attempts are preserved: NumPy-boolean serialization and a
closed-path final-sample tracking defect. Corrected execution passes 37/37;
promotion and independent reconstructions pass their declared gates. The
result suggests strong contact.

### 5.4 HF5 and HF5A: selected-sheet fill versus global sheet custody

HF5 constructs an exact source disk with \(K\)-winding one and certifies a
regular finite sheet through the coefficient-loss center. Its first
interpretation promoted ((1,0)), combined it with ((0,1)) and concluded a full
lattice. H000195/H000196 preserve that literal bridge route and its exact
calculations.

HF5A corrects the current interpretation: the finite-sheet disk does not fill
all three typed sheets. Homogenizing

\[
\Phi^h=KS^3+BST^2-4VT^3
\]

gives at projective infinity

\[
\Phi^h|_{T=0}=KS^3.
\]

At the loss center the local infinity equation is

\[
\frac{64}{27}t^2(t+3)=0.
\]

One finite root survives and a double root remains at infinity. The response
\(I_\infty(k,d)=k\) retains the (K/x) global-history class. Current preserved HF
authority therefore returns to the rank-one certified lattice above. HF5A
passes 26/26 with 22/22 independent reconstruction and suggests strong
contact. Three pre-result field/dependency/alias faults remain preserved.

### 5.5 HF6 and the path-specific correction

HF6 emits anonymous finite-plus-projective receipts before attaching sector
labels. It reconstructs:

| Sector | finite/infinity sheets | infinity index | permutation | custody |
|---|---:|---:|---|---|
| `D/y` | 3/0 | 0 | identity | `GLOBALLY_DISCHARGED` |
| `K/x` | 1/2 | 1 | `[0,2,1]` | `MIXED` |

Seven nonslice deformations preserve \(K\)-winding one, the transposition and
the surviving class. Execution passes 19/19 and independent validation 24/24;
the result suggests strong contact.

H000199 corrects one overgeneralized coefficient. The escape exponent remains
\(-1/2\), but the leading coefficient depends on the exact path jet. The radial
route alone has \(s^2U\to-2/3\); six other slopes and the HF5 disk have their own
exact values. The correction passes 15/15 and 14/14 and does not change HF6's
classification or quotient.

### 5.6 HF6T/HF6TF: blinded jet rule and transfer boundary

HF6T freezes the eliminant-conditioned rule

```text
a3(0)=0 and ord_path(a3)=1 and b1(0)!=0
  -> PROJECTIVE_CUSTODY_CANDIDATE
otherwise
  -> FINITE_OR_UNRESOLVED
```

before reveal. It matches nine forward routes and nine reversals, reconstructs
path-specific escape and preserves the failed pure-tensor partition. A first
18/19 run used the wrong determinant sign after swapping target coordinate
order; correcting only that explicit sign gives 19/19. The result suggests
strong contact for the JC1 path-jet discriminator, not a universal tensor law.

HF6TF freezes the rule unchanged on ten fresh maps. It returns four true
positives, zero false positives, two false negatives and four true negatives.
It is exact 7/7 on the admitted proper-cubic/simple-transverse domain, but it
misses quadratic coefficient loss and simultaneous cubic/linear degeneration.
Those misses remain evidence and motivate the next signature rather than a
retroactive threshold change.

### 5.7 HF6TG/HF6TH: Newton signature and mixed-jet compiler

For

\[
\Phi_t(s)=\sum_j a_j(t)s^j,
\qquad
\nu_j=\operatorname{ord}_t a_j(t),
\]

HF6TG takes the lower convex hull of \((j,\nu_j)\). Positive-slope edge width,
slope and initial polynomial predict escaping-sheet count, exponent and
regular cycle structure. On 15 fresh fibers, projective presence, sheet counts
and coefficient winding close 15/15; 34/34 exponents and 10/10 regular cycle
types reconstruct. A repeated edge remains `SINGULARITY_OBSTRUCTION`. The
result suggests strong contact without installing a universal Newton law.

HF6TH then works in the triangular affine-path chart and freezes the complete
mixed coefficient

\[
\mathcal T_{rj}
=\frac1{r!j!}D^{r+j}F^2(v^r,w^j).
\]

For

\[
G(x,y)=\sum_{p,j}c_{pj}x^py^j,
\]

exact Taylor expansion gives

\[
\mathcal T_{rj}
=\sum_{p\ge r}c_{pj}\binom pr u_0^{p-r},
\qquad
\nu_j=\min\{r:\mathcal T_{rj}\ne0\}.
\]

The complete mixed jet therefore reconstructs the Newton signature in that
chart. Known calibration closes 15/15; twelve fresh maps reconstruct all
valuation tables, hulls, edge signatures and projective counts, with 40/40
escape exponents. This is a chart-specific exact compiler identity. Low-order
compression, nontriangular maps, nonaffine paths and coordinate-invariant
transfer remain open.

## 6. What the legacy lineage does and does not install

The HF lineage contains exact reducers, cells, obstructions, projective
receipts, blind-transfer results and compiler identities. Its stages remain
valid in their declared charts. The current program makes three distinctions:

1. the HF2 grammar is a constructed SLC object, not yet a source-derived JC1
   invariant;
2. projective and mixed-jet findings do not constitute a universal tensor law;
3. historically matter-volume-labelled carrier supplements are preserved route
   artifacts, not current matter interfaces.

No current JC1-specific history, sheet, quotient, Newton or tensor field is
consumed by AFC2--AFC4. No `q_A`, mass, SI energy or matter-generation relation
is installed.

## 7. Clean restart: frozen method, no execution

### 7.1 Premise firewall

JCR1 begins without the former matter-volume interpretation, A-field carrier,
\(q_A\), \(A(r)\), W8/X1/W9,
HF1 reducer roles, the HF2 torus, its generators, `H_SAM`, projective custody
as information custody or tensor-to-matter interpretation. These remain
available only after clean definitions are frozen.

### 7.2 Stage sequence

| Stage | Work | Required output or boundary |
|---|---|---|
| JCR1-0 | normalize exact source map, fields, coordinates, determinant, fibers, discriminant and assumptions | source normal form; no SLC encoding |
| JCR1-1 | independently reconstruct determinant, resultant, fibers, degree-loss set and homogenization | algebraic facts only; no history labels |
| JCR1-2 | derive candidates from regular-value complement, covering, monodromy, braid, homology, infinity divisors and cycles | typed invariant roster with domains and equivalences |
| JCR1-3 | freeze meridians, reversals, concatenations, null loops and map controls from algebraic components | clean loop campaign; failures retained |
| JCR1-4 | account for finite/infinity multiplicity, branch continuation, divisors and asymptotics | projective receipts with exact/numerical separation |
| JCR1-5 | ask the two-dimensional invariant question with all dimensions separated | no `Z4^2` substitution for polynomial geometry |
| JCR1-6 | reveal JC1/HF3--HF6TH observations one at a time | rediscovered/compatible/scaffold-dependent/conflicting/unresolved classifications |
| JCR1-7 | optionally compare stable invariant with SAM/SLC history | explicit compiler both ways or precise information loss |
| JCR1-8 | optionally test future matter applicability | four native bridge joins required |

### 7.3 Candidate-invariant contract

Every candidate invariant must state its definition, domain, equivalence
relation, composition law, base-point and coordinate dependence, loop-reversal
and concatenation behavior, ordinary invertible-map value and JC1 value or
unresolved status. A familiar shape is not enough to rename it `H_SAM`.

The legacy reveal occurs only after the clean source, definitions and first
predictions are sealed. Agreement, disagreement, partial rediscovery and
irrelevance are all retained. This prevents legacy success from becoming a
hidden premise.

### 7.4 Current status

JCR1 is a draft for owner review and has not executed. It installs no new
Volume III authority, invariant, tensor law, SLC training change, carrier
payload or matter mapping. This chapter does not authorize its execution.

## 8. Future matter-bridge boundary

A future Jacobian object reaches a matter application only if one bridge-native campaign
establishes all four joins:

1. an exact compiler from the source-derived invariant into a declared carrier
   payload;
2. exact preservation of that payload through reciprocal delivery;
3. an identified intersection or matter-ledger consumer that reads it; and
4. a load-bearing output change when the payload is altered under a controlled
   comparison.

The first two establish transport; the third establishes consumption; the
fourth establishes consequence. A history hash that survives delivery without
a consumer is not the completed bridge. A consumer that changes for an
undeclared correlated field is not the controlled payload result.

No current JC1/HF field has completed this chain. Depth training, Q2 selection,
W9 availability or A-field-carrier existence alone does not validate or
promote a Jacobian-to-matter interpretation.

The source program called this a prospective `Volume IV` boundary. That exact
wording remains in the immutable source and `SAMA-C000256-R001`. In this
standalone atlas, Volume IV is the Riemann Hypothesis program. The matter bridge
therefore remains unnumbered, unexecuted and outside the Volume IV dependency
graph unless a later source-bound RH relation is separately established.

## 9. Established result and forward handoff

The established current result is the isolated JC1 algebra/monodromy and
endpoint-history distinction, together with the preserved HF findings in
their exact charts. The relocated program establishes where those results
belong and which former interpretations are historical rather than current.

The next mathematical step is the unexecuted source-derived restart. Its first
output is independent affine/projective reconstruction, not an SLC or matter
bridge. Any later comparison must make the compiler and information loss
explicit.

## 10. Test and evidence index

### 10.1 Direct permanent SAMA test routes

The current document catalog assigns no direct qualified SAMA test-record key
to `SAMA-D000057`. None is invented here. JC1 and HF1--HF6TH retain source
campaign validations and immutable history receipts, while JCR1 has no
execution receipt because it is unexecuted.

### 10.2 Source evidence routes

| Evidence surface | Exact route | Role |
|---|---|---|
| current program | `volume_III/SAM_VOLUME_III_JACOBIAN_PROGRAM.md` | current placement, preserved lineage, restart and bridge boundary |
| relocation | H000211 | correction from former matter-volume ownership to Volume III program |
| JC1 result | `SLC/18_SAM_NATIVE_QC/SLC_JACOBIAN_GLOBAL_HISTORY_JC1_V1/release/JC1_RESULT.json` | exact algebra, monodromy, full address return and W9 receipts |
| JC1 independent validation | `SLC/18_SAM_NATIVE_QC/SLC_JACOBIAN_GLOBAL_HISTORY_JC1_V1/release/JC1_VALIDATION.json` | 9/9 independent checks |
| lineage manifest | `volume_III/JACOBIAN_SOURCE_MANIFEST.csv` | hashes and routing of JC1/HF artifacts |
| preserved HF history | H000189, H000191--H000203 | results, failures, corrections and supersessions |
| clean restart | `SAM_REVIEW/campaigns/JVR1_JACOBIAN_VOLUME_ROUTING_REVIEW_V1/JCR1_CLEAN_JACOBIAN_RESTART_CAMPAIGN_DRAFT.md` | unexecuted staged design |
| live boundary | `SAM_LIVE/01_SLC_CURRENT.md`, `SAM_LIVE/00_CURRENT.md` | current Q2 and no-current-matter-input statements |

These artifact and live/history citations preserve current claims that lack
permanent test keys; they do not create substitute keys.

## 11. Atomic-record index

| Atomic revision | Role in this chapter |
|---|---|
| `SAMA-C000251-R002` | keeps the complete JC1/HF program in Volume III and disambiguates the former matter-volume label |
| `SAMA-C000252-R001` | records the constant-Jacobian, monodromy and endpoint-return result |
| `SAMA-C000253-R001` | separates endpoint equality from ordered program-history equality |
| `SAMA-C000254-R002` | preserves HF results without installing a universal tensor, matter or RH law |
| `SAMA-C000255-R001` | fixes the unexecuted source-derived clean restart sequence |
| `SAMA-C000256-R002` | fixes the four-join, unnumbered future matter boundary and excludes it from standalone Volume IV RH |

## 12. Source and external-reference index

| Source | Load-bearing content |
|---|---|
| `volume_III/SAM_VOLUME_III_JACOBIAN_PROGRAM.md` | Current placement; Original JC1 result; Preserved HF lineage; Clean restart; source section historically named Volume IV boundary |
| `volume_III/JACOBIAN_SOURCE_MANIFEST.csv` | exact source paths, hashes, roles and current routing |
| JC1 source `run_jc1.py` | exact map, eliminant, monodromy and event-to-W9 implementation |
| H000188 | original isolated JC1 result and historical adapter route |
| H000189--H000203 | preserved HF discovery/deviation/correction lineage |
| H000211 | controlling relocation and current interpretation |
| JCR1 campaign draft | unexecuted stages and premise firewall |

No new external Jacobian citation or external theorem claim is introduced by
this chapter. The exact polynomial map, eliminant, monodromy, address return
and preserved HF lineage are carried by the JC1/HF artifacts and hashed source
manifest above. Public repository custody is fixed by the
[`Volume III public repository constellation`](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/spines/VOLUME_III_TECHNICAL_SPINE.md#public-repository-constellation).
The clean restart remains source-derived and unexecuted.

## 13. Revision and approval boundary

This is `SAMA-D000057`, revision 2. `reviewed_and_approved` remains `false`,
and `approval` remains `null`. It changes no source program, current pointer,
history entry, executable artifact, carrier payload, matter ledger, test route,
result classification or restart authorization. Revision 2 changes only the
standalone atlas routing language: its Volume IV is RH, while the preserved
source's prospective Jacobian-to-matter bridge remains unnumbered.

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000057`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/JACOBIAN_PROGRAM_AND_CLEAN_RESTART.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol III | SAMA-D000057 | Jacobian Program | Constant-Jacobian Polynomial Computation, Preserved HF Lineage and Clean Restart |

| Document field | Value |
|---|---|
| Purpose | Present the relocated JC1/HF lineage, exact endpoint-versus-history result, preserved interpretation boundaries, unexecuted source-derived clean restart and future matter-bridge requirements. |
| Prerequisite documents | `SAMA-D000038`, `SAMA-D000040`, `SAMA-D000042` |
| Used by | a future source-derived Jacobian campaign; a future matter application only after four native joins; no direct standalone Volume IV RH route |
| Revision state | Unapproved revision 2; revision 1's former matter-volume label remains in provenance. |

</details>
