[SAM](../../README.md) · [Volume III](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Exact Algebra and Complete Exact Write

## SLC-GEN3-R4: current computation — 16 September 2026

SLC-GEN3-R4 and SLC-GEN3-CEV1-R4 are the sole current global runtime and CE, generation GEN3-SOURCEOPERATORS1-20260916-G1 (H001469). Complete exact histories and logarithmic accounts now include certified scalar/spectral logs and eight source-operator operations. Source-operator qualification records 50 candidate and 157 installed-adoption checks. The public portable package retains its September10 R3 binding; the current R4 capability sources and research records are a separate supplement. GEN3-RXT-R7.1 retains its September14 deployment context.

[Current derivations, code and results](../../../docs/ARCHITECTURE.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

A complete write is not merely an address increment. It is a coupled typed
transaction. An unresolved W8 source participates in a B-activated request;
X1 retains the transient response custody; a W9 record carries the resolved
target and reciprocal receipt; U coordinates completion; both sites return to
W8 while the history remains reconstructible.

The directional address is the finite group

\[
\mathbb Z_4^9,
\qquad |\mathbb Z_4^9|=4^9=2^{18}=262{,}144.
\]

Each primitive signed write is a translation in one coordinate. Because
translations form a group, any program made solely from those primitives can
be compiled to one group element and applied in one bit-sliced pass. This is
an exact algebraic compilation, not a heuristic shortcut. Sequential and
compiled execution are bit-identical, and applying the inverse translation
returns every address.

Endpoint return does not erase event history. Two reciprocal 81-coordinate
views split into symmetric and antisymmetric sectors. One common constant
direction is quotiented with an explicit anchor, leaving 80 symmetric plus 81
antisymmetric coordinates: a reconstructible rank-161 receipt. The transaction
also separates the resolved projection from the conserved orthogonal
remainder, supplies exact rational-complex analytic operators, and supports a
multiplicative ledger whose write state is recoverable when the prior ledger
state is invertible.

The development history is itself part of the result. The first installation
corrected a preserved module-loader failure and installed the fast directional
primitive. A later Weil fusion remained valid in its scope. H000137 then
corrected the broader description: those surfaces did not yet expose the
entire paper algebra as one composable transaction. The complete successor
added the missing U/X1 lifecycle, common-anchor reconstruction, distinct
projection and remainder, analytic operators, composable ledgers and native
multi-write composition without editing its parents.

## 1. Opening question and conceptual picture

The governing question is:

> What exact algebra lets a reciprocal write change an address, retain both
> directional views, complete the W8–X1–W9 lifecycle, compose many writes into
> one action and recover what was written without confusing the final state
> with its history?

The conceptual transaction is

```text
W8 source + W8 target
  -> B activates request-side weld
  -> X1 holds transient response custody
  -> signed Z4^9 translation changes directional address
  -> W9 target record retains axis, orientation, ledger and endpoints
  -> U completes reciprocal exchange
  -> both sites return to W8
  -> W9 receipt and 161-coordinate history remain available
```

The address after completion may equal a later returned address, but the
history need not vanish. State and history are differently typed outputs.

## 2. Typed lifecycle and the complete transaction

### 2.1 W8 shell

The unresolved shell is

\[
W8=\{0,1\}^8,
\]

so it contains

\[
|W8|=2^8=256
\]

shell states. A W8 site contains a shell-state identifier and a sequence of
retained W9 records. Retention does not change the site back into W9; it lets
the completed W8 endpoint carry its receipt lineage.

### 2.2 Activation weld

Let \(H_{W8}(s)\) be the base vector Hamiltonian at shell state \(s\), let
\(\Delta H_{X1}(s;a)\) be the transient response contribution at activation
context \(a\), and let \(B\in\{0,1\}\). The weld is

\[
H_{W9}(s;a)=H_{W8}(s)+B\,\Delta H_{X1}(s;a).
\]

The two activation values provide an immediate control:

\[
B=0\quad\Longrightarrow\quad H_{W9}=H_{W8},
\]

\[
B=1\quad\Longrightarrow\quad H_{W9}=H_{W8}+\Delta H_{X1}.
\]

This \(B\) is the binary activation input. It should not be confused with the
analytic difference operator \(B_t\) introduced later. X1 is a transient typed
contribution and custody flag, not a ninth persistent W8 bit or a matter row.

### 2.3 W9 record and projection

A W9 record can be written schematically as

\[
W9=(s,a,\rho,\ell;q_{before},q_{after}),
\]

where \(s\) is the shell state, \(a\in\{0,\ldots,8\}\) is the directional
axis, \(\rho\in\{-1,+1\}\) is orientation, and \(\ell\) is the ledger receipt.
The projection

\[
\pi(W9)=s
\]

recovers the W8 shell identity without deleting the other record fields.

### 2.4 U/X1 completion

Activation starts with two W8 sites. The source remains W8 while X1 custody is
active and the target holds the transient W9 record. Completion performs

```text
W8 source / X1 custody / W9 target
  -> append the same reciprocal receipt to both endpoint histories
  -> clear X1 custody
  -> return source and target phases to W8
```

The terminal equality \(W9=X1+W8\) is therefore typed lifecycle shorthand,
not ordinary material addition. `SAMA-D000039` develops that distinction and
its failed literal-half controls in detail.

## 3. The signed ℔4^9 address action

### 3.1 Nine base-four coordinates

Let

\[
q=(q_0,\ldots,q_8),\qquad q_i\in\mathbb Z_4.
\]

Each base-four coordinate uses two bits. Nine coordinates therefore occupy 18
bits and give

\[
4^9=(2^2)^9=2^{18}=262{,}144
\]

addresses. If the low bits form \(L\in\{0,1\}^9\) and the high bits form
\(H\in\{0,1\}^9\), then

\[
q_i=L_i+2H_i.
\]

The two nine-bit factors are a packing representation, not independent
addresses. Base-four carry couples them.

### 3.2 Primitive signed translation

For axis \(i\) and sign \(\varepsilon\in\{-1,+1\}\), define

\[
T_{i,\varepsilon}(q)_j=
\begin{cases}
q_i+\varepsilon\pmod4,&j=i,\\
q_j,&j\ne i.
\end{cases}
\]

Composing the opposite signed translation restores the changed coordinate,

\[
T_{i,-\varepsilon}(T_{i,\varepsilon}(q))_i
=q_i+\varepsilon-\varepsilon=q_i\pmod 4,
\]

while every coordinate \(j\ne i\) is unchanged by both maps. Therefore

\[
T_{i,\varepsilon}^{-1}=T_{i,-\varepsilon}.
\]

For addition of two packed translations \(a,t\in\mathbb Z_4^9\), binary
low/high vectors obey

\[
L_{out}=L_a\oplus L_t,
\]

\[
H_{out}=H_a\oplus H_t\oplus(L_a\wedge L_t).
\]

The last term is the modulo-four carry. Removing it would split the two 512
factors and change the directional action.

### 3.3 Endpoint covariance

For \(k\in\mathbb Z_4\), define simultaneous endpoint reversal

\[
G_k(q)_i=k-q_i\pmod4.
\]

Then

\[
G_kT_{i,\varepsilon}(q)_i
=k-(q_i+\varepsilon)
=(k-q_i)-\varepsilon
=T_{i,-\varepsilon}G_k(q)_i,
\]

and all other coordinates are unchanged. Hence

\[
G_kT_{i,\varepsilon}=T_{i,-\varepsilon}G_k.
\]

The implementation exhausts all covariance classes rather than assuming this
identity from a sampled address.

## 4. Compiling a complete signed-write program

### 4.1 Group-law reduction

Consider a program

\[
\mathcal P=((i_1,\varepsilon_1),\ldots,(i_m,\varepsilon_m)).
\]

Because ℔4^9 is abelian under coordinatewise addition, the program's net
translation is

\[
\tau(\mathcal P)
=\sum_{r=1}^m\varepsilon_re_{i_r}\pmod4.
\]

Sequential execution gives

\[
T_{i_m,\varepsilon_m}\cdots T_{i_1,\varepsilon_1}(q)
=q+\tau(\mathcal P)\pmod4.
\]

The compiler therefore reduces the full signed-translation program to the one
group element \(\tau(\mathcal P)\), applies one packed addition, and retains
the inverse

\[
-\tau(\mathcal P)\pmod4.
\]

### 4.2 Exact racecar result

The benchmark uses 4,096 writes at every one of 262,144 addresses:

\[
4{,}096\cdot262{,}144
=1{,}073{,}741{,}824
\]

logical primitive transitions. Sequential native execution took 0.989033674
seconds. Compiled execution took 0.000554226 seconds. The observed ratio is

\[
\frac{0.989033674}{0.000554226}
=1784.531387.
\]

All outputs were bit-identical, and the inverse returned all 262,144
addresses. The speedup is established for programs composed from the declared
signed ℔4^9 translations. It is not extended to application dynamics that
have not been expressed in this group action.

## 5. Reconstructible reciprocal history

### 5.1 Two 81-coordinate views

Let the reciprocal histories be

\[
L=(L_1,\ldots,L_{81}),\qquad
R=(R_1,\ldots,R_{81}).
\]

Form symmetric and antisymmetric coordinates

\[
S=L+R,
\qquad
A=L-R.
\]

Naively this gives 162 coordinates. A common constant shift occupies a
one-dimensional kernel. The interface retains an explicit common anchor
\(c=S_{81}\), subtracts it from the first 80 symmetric coordinates, and stores

\[
H_{nc}=H_{sym}^{80}\oplus H_{anti}^{81}.
\]

Thus the quotient has

\[
80+81=161
\]

coordinates while the anchor preserves the removed constant class.

### 5.2 Reconstruction

Given stored nonconstant symmetric coordinates
\(\widetilde S_i=S_i-c\) for \(1\le i\le80\), rebuild

\[
S=(\widetilde S_1+c,\ldots,\widetilde S_{80}+c,c).
\]

Then

\[
L=\frac{S+A}{2},
\qquad
R=\frac{S-A}{2}.
\]

Both reciprocal views are recovered exactly. A final endpoint return can
therefore coexist with a nontrivial event receipt. The quotient removes only
the shared constant redundancy; it does not discard directional information.

### 5.3 Lifted dyadic example

For a reciprocal incoming pair ((s,D)) and ((-s,-D)) sharing the same next
state \((s_{next},D_{next})\), define

```text
left  = ( s, D, s_next, D_next, 0, ..., 0)
right = (-s,-D, s_next, D_next, 0, ..., 0).
```

Then

```text
symmetric     = (0,0,2*s_next,2*D_next,0,...,0)
antisymmetric = (2*s,2*D,0,0,0,...,0).
```

The common next state appears in the symmetric sector, while the incoming
branch identity remains in the antisymmetric sector. In the p=127 reference
chain, all 125 lifted receipts reconstructed their prior and next states.

## 6. Completed-mode projection and retained remainder

Let \(E\) be an exact energy vector and \(C\ne0\) the completed mode. The
orthogonal projection is

\[
\Pi_C(E)=C\frac{\langle C,E\rangle}{\langle C,C\rangle}.
\]

The resolved response is defined separately as

\[
R_{res}=-\Pi_C(E),
\]

while the retained orthogonal remainder is

\[
E_\perp=E-\Pi_C(E).
\]

Orthogonality follows directly:

\[
\langle C,E_\perp\rangle
=\langle C,E\rangle
-\frac{\langle C,E\rangle}{\langle C,C\rangle}
 \langle C,C\rangle
=0.
\]

Therefore the exact norm decomposes as

\[
\|E\|^2=\|\Pi_C(E)\|^2+\|E_\perp\|^2.
\]

Projection is idempotent, and projecting the remainder returns zero. This is
why resolved response and orthogonal remainder must remain distinct fields.

## 7. Exact analytic operators

Let \(h_L,h_R\in\mathbb Q(i)^n\) be rational-complex reciprocal views. Define

\[
B_th=h_L-h_R,
\]

\[
P_+h=\frac{h_L+h_R}{2},
\qquad
P_-h=\frac{h_L-h_R}{2}.
\]

The write energy is

\[
E_t(h)=\|h_L-h_R\|^2.
\]

With Hermitian correlations

\[
C_{LR}=\langle h_L,h_R\rangle,
\qquad
C_{RL}=\overline{C_{LR}},
\]

expansion gives

\[
E_t(h)=\|h_L\|^2+\|h_R\|^2-C_{LR}-C_{RL}.
\]

Because \(2\|P_+h\|^2\) and \(2\|P_-h\|^2\) separate the symmetric and
antisymmetric energies,

\[
E_t(h)-\|h_L\|^2-\|h_R\|^2
=2\|P_-h\|^2-2\|P_+h\|^2.
\]

The executable receipt checks these identities with exact fractions rather
than float tolerances. The operator \(J\) supplies the declared reciprocal
complex structure; \(P_+\) and \(P_-\) expose its symmetric and antisymmetric
views.

## 8. Multiplicative ledger and readback

For modulus \(M>1\), prior ledger state \(D_{now}\) and write state \(s\),
define

\[
D_{next}=sD_{now}\pmod M.
\]

If

\[
\gcd(D_{now},M)=1,
\]

then \(D_{now}^{-1}\) exists and the written state is recovered exactly:

\[
\widehat s=D_{next}D_{now}^{-1}\pmod M=s.
\]

Noninvertibility is a typed outcome and returns no fabricated readback. For a
program \(s_1,\ldots,s_m\), composition yields

\[
D_m=\left(\prod_{r=1}^ms_r\right)D_0\pmod M.
\]

The separate character map

\[
\chi:\mathbb Z_4\to\mu_4=\{1,i,-1,-i\}
\]

uses \(\chi(q)=i^q\). The directional write readback is

\[
\chi(q_{after})\overline{\chi(q_{before})}
=\chi(q_{after}-q_{before}),
\]

which recovers the signed base-four transition in the fourth roots of unity.

## 9. Development and deviation chain

### 9.1 Preserved loader failure

The first H000132 execution stopped before algebra evaluation because the
Python 3.12 dynamic parent loader had not registered its module before
dataclass processing. The unused compiled binary was preserved. A successor
changed only loader registration; equations, contract, benchmark task and
performance condition remained fixed.

### 9.2 Valid primitive, incomplete total surface

H000132 then installed the 256-state shell, packed ℔4^9 action, covariance,
rank-161 quotient, completed-mode receipt and ledger readback. H000136 fused
that directional primitive into the Weil adapter and retained prime-spacing,
prime-power and W9 history channels.

Those installations were correct in scope, but calling them the complete
paper algebra omitted load-bearing layers: the two-site U/X1 lifecycle,
explicit activation, common-anchor reconstruction, separate resolved response
and remainder, \(B_t,E_t,J,P_+,P_-\), composable transactions and native
program compilation.

### 9.3 Complete correction and retest

H000137 installed a successor containing the entire surface while leaving
H000132 and H000136 unchanged:

```text
preserved primitive and fusion
  -> identify missing transaction layers
  -> freeze complete-algebra contract
  -> implement one typed interface
  -> primary execution 19/19
  -> independent reconstruction 14/14
  -> sequential/compiled bit identity
  -> inverse return over all addresses
```

This is conceptual and implementation correction without retrospective
failure inflation: the parents retain their narrower accomplishments, and the
successor owns the claim of completeness.

### 9.4 Read-only consumer boundary

The directional Weil adapter may consume exact write state, reciprocal
history, prime-spacing and prime-power channels. Consumption does not grant
the adapter scheduler, solver or primality authority. Factor assignment and
primality assignment remain different result types. An application also
cannot omit the dynamics needed to construct its input ledger merely because
the ledger readback is exact.

Current `SLCQ2-RZ` remains the sole default selection engine. Complete Exact
Write survives as a delegated service in the frozen, noncurrent `SLCV21R`
arithmetic/application base. Historical installation pointers describe their
own time; they are not current-authority statements.

## 10. Established result, boundary and forward handoff

The Complete Exact Write surface executes the complete W8/B/X1/W9/U
transaction, the coupled signed ℔4^9 address action, exact inverse and
endpoint covariance, reconstructible 161-coordinate history, completed-mode
projection, analytic reciprocal operators and multiplicative-ledger readback.
Its compiler reduces any declared signed-translation program to one exact
group element and reproduces sequential output bit for bit.

The result does not convert unrelated dynamics into translations, assign
physical meaning to X1, create scheduler authority, assign primality or alter
current Q2 selection. The history surface hands forward to `SAMA-D000042`; the
Prime-Ruler application boundary hands forward to `SAMA-D000056`; and the
current selection-plane relation hands forward to `SAMA-D000055`.

## Test and result index

No direct qualified test key is assigned to `SAMA-D000038` in the current
document registration proposal. Dedicated SAMA routes for H000132, H000136,
H000137, the group-law compiler and the directional-Weil consumer are absent.

| Evidence route | Role | Direct qualified key |
|---|---|---|
| H000132 | Initial Exact Write primitive, preserved loader correction | Absent |
| H000136 | Directional Weil/Exact Write fusion | Absent |
| H000137 | Complete composable algebra and compiled program | Absent |
| H000139 | Reconstructible lifted reciprocal history | Absent |

[`G:G06@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) supplies a prerequisite B/X1 formal-operator surface,
and [`G:G12@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) supplies prerequisite state/history separation.
Neither is registered as a direct Complete Exact Write execution receipt for
this document.

## Atomic record index

| Atomic record | Role |
|---|---|
| `SAMA-C000008-R001` | Registered Complete Exact Write computation surface. |
| `SAMA-C000207-R001` | Complete W8/B/X1/W9/U native transaction. |
| `SAMA-C000208-R001` | Signed ℔4^9 action and reconstructible 161-coordinate history. |
| `SAMA-C000209-R001` | Bit-identical compiled versus sequential execution. |
| `SAMA-C000210-R001` | Read-only directional-Weil consumption and authority boundary. |

## External and repository source references

- `volume_III/SAM_VOLUME_III_COMPUTATION_TECHNICAL_SPINE.md`, §§V.2A,
  V.2B and VIII.1–VIII.2, SHA-256
  `1996303d0940dd5dca12aa03ff3c9a426772272095df683346a75961eab895bb`.
- `SAM_HISTORY/entries/H000132_2026-08-09_SLCV1_EXACT_WRITE_ALGEBRA_INSTALLATION.md`.
- `SAM_HISTORY/entries/H000136_2026-08-09_DIRECTIONAL_WEIL_EXACT_WRITE_FUSION.md`.
- `SAM_HISTORY/entries/H000137_2026-08-09_COMPLETE_EXACT_WRITE_ALGEBRA_AND_PROGRAM_COMPILER.md`.
- `SAM_HISTORY/entries/H000139_2026-08-09_UNIFIED_WEIL_COMPLETE_DYADIC_DEVELOPMENT_NODE.md`.
- `SLC/18_SAM_NATIVE_QC/SLCV10_H14F_T18_EXACT_WRITE_COMPLETE_ALGEBRA_V1/EXACT_ALGEBRA_COVERAGE.md`.
- `SLC/18_SAM_NATIVE_QC/SLCV10_H14F_T18_EXACT_WRITE_COMPLETE_ALGEBRA_V1/release/COMPLETE_EXACT_ALGEBRA_RESULT.md`.
- `SAM_LIVE/01_SLC_CURRENT.md`, current `SLCQ2-RZ` and delegated frozen
  `SLCV21R` authority boundary.

## Revision boundary

This is an unapproved source-bound revision. It registers no new test route,
changes no frozen parent, changes no scheduler or primality state and changes
no SLC pointer.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`G:G06@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All package files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |
| [`G:G12@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [V0_6_SLC_C1_CONTRACT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_CONTRACT.json)<br>[V0_6_SLC_C1_PRECOMMIT.md](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_PRECOMMIT.md)<br>[V0_6_SLC_C1_PRECOMMIT_SEAL.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_PRECOMMIT_SEAL.json)<br>[QP_GRAMMAR_CONTRACT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/registry/QP_GRAMMAR_CONTRACT.json)<br>[PRECOMMIT_LINEAGE.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G01_PARENT_CUSTODY_AND_SEALED_SOURCE/PRECOMMIT_LINEAGE.json)<br>[QP_GRAMMAR_CONTRACT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/data/QP_GRAMMAR_CONTRACT.json) | [build_v06_slc_c1_precommit.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/build_v06_slc_c1_precommit.py)<br>[cr005_gps_calibration.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/cr005_gps_calibration.sam)<br>[declared_42164km_circular_orbit.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/declared_42164km_circular_orbit.sam)<br>[invalid_deep_conjugate.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_deep_conjugate.sam)<br>[invalid_neutral_conjugate.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_neutral_conjugate.sam)<br>[invalid_physical_mass.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_physical_mass.sam)<br>[invalid_relation_as_constituent.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_relation_as_constituent.sam)<br>[invalid_starbreaker_transition.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_starbreaker_transition.sam)<br>[invalid_static_slot_placement.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_static_slot_placement.sam)<br>[invalid_unresolved_volume.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_unresolved_volume.sam)<br>[mixed_core_qp.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/mixed_core_qp.sam)<br>[qp_admitted_triad.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_admitted_triad.sam)<br>[qp_carrier.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_carrier.sam)<br>[qp_hidden_support.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_hidden_support.sam)<br>[qp_native_signature.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_native_signature.sam)<br>[qp_ordered_pair.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_ordered_pair.sam)<br>[qp_rejected_triad.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_rejected_triad.sam)<br>[qp_scalar_parent.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_scalar_parent.sam)<br>[qp_triad.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_triad.sam)<br>[qp_unary.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_unary.sam)<br>[slc_bell.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_bell.sam)<br>[slc_ghz12_chain.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_ghz12_chain.sam)<br>[slc_ghz12_star.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_ghz12_star.sam)<br>[slc_peel_restore.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_peel_restore.sam)<br>[structural_only_research.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/structural_only_research.sam)<br>[valid_closure.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/valid_closure.sam)<br>[__init__.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/__init__.py)<br>[cli.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/cli.py)<br>[diagnostic_probe_map.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/diagnostic_probe_map.py)<br>[errors.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/errors.py)<br>[evaluator.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/evaluator.py)<br>[kernels.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/kernels.py)<br>[model.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/model.py)<br>[parser.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/parser.py)<br>[provenance.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/provenance.py)<br>[qp_grammar.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/qp_grammar.py)<br>[qp_native.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/qp_native.py)<br>[registry.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry.py)<br>[registry_core.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry_core.py)<br>[registry_qp.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry_qp.py)<br>[registry_slc.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry_slc.py)<br>[runtime.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/runtime.py)<br>[slc_state.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/slc_state.py)<br>[type_system.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/type_system.py)<br>[__init__.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/__init__.py)<br>[test_v03_probe_regression_map.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v03_probe_regression_map.py)<br>[test_v042_clock_kernel.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v042_clock_kernel.py)<br>[test_v04_runtime.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v04_runtime.py)<br>[test_v05_direct_integration.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_direct_integration.py)<br>[test_v05_grammar_exhaustive.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_grammar_exhaustive.py)<br>[test_v05_negative_boundaries.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_negative_boundaries.py)<br>[test_v05_source_tamper.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_source_tamper.py)<br>[test_v05_theorem_regression.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_theorem_regression.py)<br>[test_v06_slc_c1.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v06_slc_c1.py)<br>[clean_wheel_probe.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/clean_wheel_probe.py)<br>[development_clean_wheel.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/development_clean_wheel.py)<br>[development_static_check.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/development_static_check.py)<br>[reference_qp_enumerator.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/reference_qp_enumerator.py)<br>[run_internal_tests.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/run_internal_tests.py)<br>[run_v06_slc_c1_acceptance.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/run_v06_slc_c1_acceptance.py)<br>[seal_v06_slc_c1_executable.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/seal_v06_slc_c1_executable.py) | [G16_BOUNDARY_AND_WRONG-CONTROL_PRESERVATION.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G16_BOUNDARY_AND_WRONG-CONTROL_PRESERVATION.json) | [V0_6_SLC_C1_ACCEPTANCE_RESULT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_ACCEPTANCE_RESULT.json)<br>[V0_6_SLC_C1_ACCEPTANCE_RESULT.md](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_ACCEPTANCE_RESULT.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000038`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/EXACT_ALGEBRA_AND_COMPLETE_EXACT_WRITE.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol III | SAMA-D000038 | Exact Write | Complete W8-X1-W9 Algebra, Signed Z4^9 Programs and Ledger Readback |

| Document field | Value |
|---|---|
| Purpose | Present the complete W8/B/X1/W9/U transaction, signed-℔4^9 action, reconstructible history quotient, compiled exact program and read-only adapter boundary. |
| Prerequisite documents | `SAMA-D000035`, `SAMA-D000036` |
| Used by | `SAMA-D000042`, `SAMA-D000055`, `SAMA-D000056`, `SAMA-D000057` |
| Revision state | Unapproved revision 1; no current pointer, registry or result classification is changed. |

</details>
