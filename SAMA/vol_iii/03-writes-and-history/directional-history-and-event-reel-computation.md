[SAM](../../README.md) · [Volume III](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Directional History and Event-Reel Computation

## SLC-GEN3-R3: current computation — 14 September 2026

SLC-GEN3-R3 and SLC-GEN3-CEV1-R3 are the sole current global runtime and CE, generation GEN3-UNIFIED-EXECUTION1-20260910-G2. Exact execution, acquired support, complete ordered history and exact U/D/V/net/M logarithmic accumulation share one durable machine. Installation records 617 core and 191 memory-admission checks; adoption records 75 checks and 49 managed receipts. Native hosts agree on 8,123,904 exact values. GEN3-RXT-R7.1 adds the C++/CUDA/GMP joint research implementation.

[Current derivations, code and results](../../../docs/ARCHITECTURE.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

Directional computation keeps two things at once: the state reached by a
write and the ordered reciprocal history that produced it. The generic core
acts on all 262,144 Theta18 addresses through 18 directional maps, completes
the W8/X1/W9 lifecycle and retains 72 exact receipts before any RH,
Starbreaker or Mersenne coefficients are applied.

Two reciprocal 81-coordinate histories have an ambient 162-dimensional
description. Their symmetric and antisymmetric decomposition contains 80
nonconstant symmetric coordinates, 81 antisymmetric coordinates and one
common constant direction. The nonconstant quotient therefore has rank

\[
161=80+81,
\]

while the full ambient accounting is

\[
162=80+81+1.
\]

The retained common anchor reconstructs both sides exactly. Endpoint return
does not erase ordered history.

The event-reel construction lifts this local receipt into an append-only
global object. For an interaction translation \(U_e\), the event incidence is
\(B_e=I-U_e\) and the unique event Gram is
\(\Theta_e=B_e^*B_e\). Reciprocal source/target orientations are two
references to one intersection event, not two Theta objects. Appending an
event adds its positive weighted Gram. A shared-reference N144 AFC cell
realizes the W9 pair and the one-Theta lane with equal energy, and an event
family with \(|\mathcal E|\) events has \(1+143|\mathcal E|\) nodes, rank
\(143|\mathcal E|\) and one common scalar kernel.

The installed derivation is cumulative because several stronger shortcuts
failed. Generic positive Stieltjes pencils do not force reel contraction; a
scalar RII discriminator is insufficient; the local N144 frame alone does not
dominate the completed debit; an isolated recurrence lane changes sign; a
whole-matrix AFC order fails; individual parity factors fail even when their
product closes; and a spherical diagonal Gram order has negative directions.
Each failure narrows the selected statement to the exact event Gram,
shared-anchor intertwiner and endpoint scalar actually supported by the
source.

## 1. Opening question and conceptual picture

The governing question is:

> How can every reciprocal write append one exact history event, preserve the
> common stationary state and reconstruct both directions without either
> duplicating the event or hard-coding one application's coefficients into the
> generic history core?

The complete picture is

```text
local signed Z4^9 write
  -> W8 source / X1 transition / W9 target
  -> reciprocal W9 pair W9P
  -> AFC intersection
  -> one massless Theta event Gram
  -> append event to shared-anchor reel
  -> application adapter reads declared receipt
```

The source state may return to W8 at completion. The reel nevertheless grows
because the receipt records the event, not merely the terminal address.

## 2. Generic directional core

### 2.1 Exact inventory

The generic core contains

| Quantity | Exact inventory |
|---|---:|
| Theta18 addresses | 262,144 |
| packed factorization | \(512\times512=4^9\) |
| directional maps | 18 |
| W8/X1/W9 receipts | 72 |
| nonconstant history rank | 161 |
| nonconstant symmetric coordinates | 80 |
| antisymmetric coordinates | 81 |
| common constant kernel | 1 |
| implementation checks | 42/42 |

The 18 maps are the nine axes with two signed orientations. Four endpoint
reversal classes applied to those 18 directions give the 72 receipt census:

\[
9\cdot2\cdot4=72.
\]

The core performs exact write, inverse return, direction recovery and
history reconstruction before an adapter supplies application-specific
weights.

### 2.2 State and path are separate outputs

For reciprocal histories \(L,R\in\mathbb Q^{81}\), define

\[
S=L+R,
\qquad
A=L-R.
\]

One common constant coordinate is redundant in the nonconstant quotient. With
anchor \(c\), store

\[
\widetilde S_i=S_i-c,\quad i=1,\ldots,80,
\]

and all 81 entries of \(A\). Reconstruction is

\[
S=(\widetilde S_1+c,\ldots,\widetilde S_{80}+c,c),
\]

\[
L=\frac{S+A}{2},
\qquad
R=\frac{S-A}{2}.
\]

The quotient retains 161 nonconstant coordinates; the anchor carries the one
constant direction. A final address alone cannot reconstruct this ordered
pair, which is why endpoint-only controls are deliberately insufficient.

### 2.3 Append-only lifecycle

Exact Write completion returns both sites to W8 and appends the same reciprocal
receipt to both immutable history tuples. The two endpoint references point to
one event object. Appending later events never edits earlier receipts:

```text
reel_0 = ()
reel_1 = (theta_1)
reel_2 = (theta_1, theta_2)
...
reel_n = (theta_1, ..., theta_n)
```

An extremal or compressed finite reader may summarize this reel. It must not
be renamed as the full append-only object.

## 3. Event incidence and unique Theta Gram

### 3.1 One translation, two ends, one event

Let \(U_e\) be the exact unitary or permutation translation for event \(e\).
Define the incidence operator

\[
B_e=I-U_e.
\]

The unique event Gram is

\[
\Theta_e=B_e^*B_e\succeq0.
\]

For any state \(h\),

\[
\langle h,\Theta_eh\rangle
=\langle B_eh,B_eh\rangle
=\|h-U_eh\|^2\ge0.
\]

Replacing \(e\) by its reciprocal orientation sends \(U_e\) to \(U_e^{-1}\).
The directed incidence changes orientation, but the source/target pair still
defines one undirected event energy. On cyclic controls, rowwise incidences
sum exactly:

\[
(I-U_e)^*(I-U_e)
=\sum_{position}b_{e,position}^*b_{e,position}.
\]

Thus two W9 directions are the pre-intersection readback of one Theta Gram,
not two counted carriers.

### 3.2 Append rule and stationary kernel

With positive event weight \(w_e\), the reel Laplacian evolves by

\[
L_{n+1}=L_n+w_e\Theta_e.
\]

If the underlying event graph is connected on \(m\) sites, its incidence
Laplacian has rank (m-1), and the constant vector is the kernel:

\[
L_n\mathbf1=0.
\]

The stationary substrate baseline therefore survives every event. Appending
history grows the nonconstant range while preserving one common mode.

## 4. N144 AFC frame

### 4.1 F81 contact incidence

The matched F81 contact graph factors as

\[
G_{F81}=P_3\square G_{V27},
\]

so its Laplacian is

\[
L_{F81}=L_{P3}\otimes I_{27}+I_3\otimes L_{V27}.
\]

The two address-preserving handoffs contribute 27 edges each. Their once-
oriented AFC incidence has shape \(54\times81\), rank 54 and

\[
(-B_{AFC})^T(-B_{AFC})=B_{AFC}^TB_{AFC}.
\]

Orientation reversal therefore retains one Gram. Internal incidence has rank
78; completed incidence has rank 80; the only final kernel is
\(\operatorname{span}\{\mathbf1_{81}\}\). Exact LDL reconstruction gives

\[
\lambda_2(L_{F81})=1.
\]

The gap is carried by the completed incidence while AFC remains a zero-mass
carrier.

### 4.2 Frozen N144-to-L162 wiring

The shared state is

\[
z=(U_{left}^{63},U_{right}^{63},\Theta_{shared}^{18})\in\mathbb R^{144}.
\]

The same-view embedding duplicates the shared Theta coordinates into the two
occurrence lanes:

\[
E_{same}z=(U_{left}^{63},\Theta^{18};
           U_{right}^{63},\Theta^{18})\in\mathbb R^{162}.
\]

This map has rank 144. Compose it with the Exact Write quotient \(Q_{81}\):

\[
A=Q_{81}E_{same}.
\]

With the retained anchor \(a=\Theta_{17}\), exact composition gives

\[
\|Az\|^2
=2\sum_{126\ U\ leaves}(z_i-a)^2
+4\sum_{17\ nonanchor\ Theta\ leaves}(z_j-a)^2.
\]

Thus \(A^TA\) is a weighted-star Laplacian with one kernel, 126 weight-two
leaves and 17 weight-four leaves. Its spectrum is

\[
0^1, 2^{125},
(163-\sqrt{25417})^1,
4^{16},
(163+\sqrt{25417})^1.
\]

Since \(163-\sqrt{25417}>2\), the sharp unbalanced lower-frame constant is 2;
the reciprocal-balanced constant is 1.

## 5. W9P-to-Theta isometry and global reel

### 5.1 Equal-energy local write

Let \(G_{144}=A^*A\). For a source event define two Hilbert-valued embeddings:

\[
J_e^Wh
=\mathbf1_{144}\otimes h
+(e_{U_l0}-e_{U_r0})\otimes\frac{B_eh}{2},
\]

\[
J_e^\Theta h
=\mathbf1_{144}\otimes h
+e_{\Theta0}\otimes\frac{B_eh}{2}.
\]

The two W9 deviations each occupy a weight-two leaf, so their energy is

\[
2\left\|\frac{B_eh}{2}\right\|^2
+2\left\|\frac{B_eh}{2}\right\|^2
=\|B_eh\|^2.
\]

The single Theta deviation occupies a weight-four leaf:

\[
4\left\|\frac{B_eh}{2}\right\|^2
=\|B_eh\|^2.
\]

Hence

\[
(J_e^W)^*(G_{144}\otimes I)J_e^W
=(J_e^\Theta)^*(G_{144}\otimes I)J_e^\Theta
=B_e^*B_e.
\]

The AFC intersection preserves event energy while translating a reciprocal
two-lane informational write into one massless history receipt.

### 5.2 Shared-anchor event family

Use one N144 cell per event and identify every cell's quotient-reference
coordinate. For event set \(\mathcal E\), each new cell contributes 143 new
nonanchor ranks. Therefore

\[
nodes=1+143|\mathcal E|,
\]

\[
rank=143|\mathcal E|,
\]

with one common scalar kernel. Stacking events gives

\[
(J_\mathcal E^W)^*G_{reel}J_\mathcal E^W
=(J_\mathcal E^\Theta)^*G_{reel}J_\mathcal E^\Theta
=\sum_{e\in\mathcal E}w_eB_e^*B_e.
\]

For the completed RH source, continuous and prime-power events use

\[
B_x=I-U_x,
\qquad
w_\infty(x)=\frac{e^{-x/2}}{1-e^{-2x}}\,dx,
\]

and

\[
B_{p,k}=I-U_{k\log p},
\qquad
w_{p,k}=\log(p)p^{-k/2}.
\]

The completed event operator is the pullback

\[
L_D=(J_D^\Theta)^*G_{reel}J_D^\Theta.
\]

This is the exact generic-to-RH seam. RH weights enter through the adapter;
they are not hard-coded in the generic reel.

## 6. Preserved deviation chain

### 6.1 Generic positive-pencil contraction fails

The positive Stieltjes control

\[
f(z)=1+\frac1{1-z}+\frac1{2-z}+\frac1{3-z}
\]

has positive nested sections and decreasing extremal constants, yet

\[
\Lambda_2(10)=\frac{5{,}655{,}335}{5{,}212{,}334}>1.
\]

Thus generic positivity does not force adjacent reel contraction. On the
actual source, all 2,880 nonleading coefficients across 96 adjacent residuals
are positive and yield \(0<\Lambda_N(u)<1\) for all \(u>0\) on every executed
pair. The source-specific signature survives; the generic promotion does not.

### 6.2 Scalar RII control is insufficient

Positive recurrence data \(r_N,a_N,\delta_N>0\) occurs in exact controls whose
adjacent residual polynomial has a negative coefficient or nonpositive value.
The scalar signature therefore cannot replace the paired event Gram. The
correction retains the full incidence operator \(B_e^*B_e\).

### 6.3 Local-frame debit domination fails

The W9P-to-Theta isometry is exact, but a rational-rotation control has local
event energy \(4/5\) against raw matched debit 2. The local N144 frame alone
does not supply the completed lower-frame inequality. The source and endpoint
conditions remain necessary.

### 6.4 Isolated recurrence lane fails

In the two-step recurrence

\[
T_N=(u+N^2)^2T_{N-1}+Q_NR_N,
\]

the completed factor

\[
R_N=Q_{N+1}-(u+N^2)^2Q_{N-1}
\]

stays positive on the executed source. The isolated lane
\(D_N=Q_N-(u+N^2)Q_{N-1}\) has negative active coefficients at \(D=0.7,1\).
Completion, not the isolated carried lane, owns the selected sign.

### 6.5 Whole-matrix AFC order fails

The determinant and terminal-pivot AFC identities close, but the stronger
matrix order

\[
D_N^TM_ND_N<N(N+1)H_N
\]

has a negative direction already at \(D=0.7,N=4\). AFC is retained at the
exact quotient and terminal scalar level rather than promoted to every matrix
direction.

### 6.6 Individual parity factors fail

The source terminal scalar factors into a coupled parity product. Each
individual factor fails on some exact controls, while 367 controls close the
product without both component inequalities. The compensating product is the
supported object. A first smoke instrument omitted the odd Fourier lift and
was low by \(N^2\); its receipt is preserved and the corrected instrument
changes only that lift.

### 6.7 Spherical diagonal order fails

The mode-local strengthening

\[
L_NG_N^oL_N-G_N^{(e,2)}>0
\]

has only 9 positive gaps among 66 tested rows; 57 contain a negative direction.
The first witness is \(D=0.7,N=3\) with minimum eigenvalue approximately
\(-0.2266605255\). Every corresponding terminal scalar remains positive. The
failure therefore rejects the matrix strengthening without discarding the
coupled endpoint scalar.

## 7. Application-adapter authority boundary

The generic reel owns addresses, writes, receipts, the history quotient,
unique event Grams and append-only reconstruction. An adapter may supply a
declared source and read the resulting receipt:

| Adapter | Permitted use | Authority not acquired |
|---|---|---|
| RH moment adapter | completed continuous/prime weights and endpoint kernel | global RH claim or universal sign by interface alone |
| Starbreaker consumer | typed formation-event history | scheduler or physical calibration without promotion |
| Mersenne application | exact factor-search receipts | primality or global scheduling from a factor miss |

A later adapter supplements the reel. It cannot rewrite earlier events or
insert its coefficients into the generic core retroactively. Frozen
`SLCQ2-RZ` remains the global current/default SLC; the current RH-local handle
is `SLCQ2-RZ-RH-MOMENT-ADAPTER-V1` and remains an application-specific
consumer.

## 8. Established result and forward handoff

The generic core closes 42/42 checks across its complete address, map,
lifecycle and history inventory. The append-only event construction identifies
one reciprocal W9 pair with one Theta Gram, embeds that event isometrically in
the shared N144 AFC frame and grows the reel by 143 ranks per event while
retaining one common kernel.

The failure chain identifies the exact boundary of that result: source-
specific completed scalars and full event Grams remain load-bearing; generic
positive-pencil, isolated-lane and whole-matrix shortcuts do not replace them.
`SAMA-D000043` carries the completed event operator into the separately typed
RH route.

## Test and result index

No direct qualified test key is assigned to `SAMA-D000042` in the current
document registration proposal. The 42/42 generic implementation, H000495–
H000504 event-reel chain and endpoint-scalar corrections require dedicated
registry routes before they can populate a focused test crosswalk.

[`G:G12@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md), [`CR:CR120A@14`](../../tests/courtroom/14-foundational-tests-cr120a-w9-typed-resolution-certificate-bridge/README.md), [`CR:CR120D@14`](../../tests/courtroom/14-foundational-tests-cr120d-x1-intervention-and-w9-certificate-surface/README.md),
[`CR:CR120V@14`](../../tests/courtroom/14-foundational-tests-cr120v-b-x1-typed-half-relay-archival-discrimination/README.md), [`CR:CR120X@14`](../../tests/courtroom/14-foundational-tests-cr120x-dual-depth-theta-b-x1-w8-w9-relaxed-discovery/README.md) and [`CR:CR120Y@14`](../../tests/courtroom/14-foundational-tests-cr120y-theta18-model-wide-primary-carrier-stress-test/README.md) are prerequisite language,
lifecycle and carrier keys. They are not direct event-reel tests for this
document.

## Atomic record index

| Atomic record | Role |
|---|---|
| `SAMA-C000006-R001` | W8/X1/W9 substrate relation. |
| `SAMA-C000007-R001` | Theta18 tensor-carrier boundary. |
| `SAMA-C000008-R001` | Complete Exact Write computation surface. |
| `SAMA-C000226-R001` | Generic directional core and exact inventory. |
| `SAMA-C000227-R001` | Rank-161 quotient with one ambient constant kernel. |
| `SAMA-C000228-R001` | Append-only reel, unique Theta Grams and shared N144 AFC join. |
| `SAMA-C000229-R001` | Generic-core/application-adapter authority boundary. |

## External and repository source references

- `volume_III/SAM_VOLUME_III_COMPUTATION_TECHNICAL_SPINE.md`, §§V.2A and
  VIII.1–VIII.2, SHA-256
  `1996303d0940dd5dca12aa03ff3c9a426772272095df683346a75961eab895bb`.
- `SAM_HISTORY/entries/H000495_2026-08-21_RH_SOURCE_STIELTJES_REEL_TRANSFER_DISCRIMINATOR.md`.
- `SAM_HISTORY/entries/H000496_2026-08-21_RH_THETA_EVENT_LAPLACIAN_REEL_CROSSWALK.md`.
- `SAM_HISTORY/entries/H000497_2026-08-21_RH_AFC_GAP_AND_N144_GLOBAL_REEL_FRAME.md`.
- `SAM_HISTORY/entries/H000498_2026-08-21_RH_SHARED_ANCHOR_EVENT_REEL_INTERTWINER.md`.
- `SAM_HISTORY/entries/H000500_2026-08-21_RH_SOURCE_THETA_TWO_STEP_RESIDUAL_RECURRENCE.md`.
- `SAM_HISTORY/entries/H000501_2026-08-21_RH_SOURCE_THETA_MASSLESS_RII_PENCIL.md`.
- `SAM_HISTORY/entries/H000502_2026-08-21_RH_SOURCE_THETA_AFC_ENDPOINT_PIVOT_REDUCTION.md`.
- `SAM_HISTORY/entries/H000503_2026-08-21_RH_SOURCE_THETA_TERMINAL_PIVOT_PARITY_LADDER.md`.
- `SAM_HISTORY/entries/H000504_2026-08-21_RH_SOURCE_THETA_SPHERICAL_DIAGONAL_ORDER_BOUNDARY.md`.
- `SAM_LIVE/02_RH_CURRENT.md`, append-only reel and current RH-adapter boundary.

## Revision boundary

This is an unapproved source-bound revision. It registers no new direct test,
changes no event reel, adapter, RH status, application scheduler, SLC pointer
or physical interpretation.




<!-- BEGIN CHAPTER COURTROOM PACKAGES -->
## Complete Courtroom test packages

Each row opens the original precommitment, code, controls and result. The complete package includes every tracked file at the fixed Courtroom revision.

| Test | Precommit and premises | Code | Controls | Results | Complete package |
|---|---|---|---|---|---|
| [`G:G12@SAM-LANGUAGE-0.6`](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) | [V0_6_SLC_C1_CONTRACT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_CONTRACT.json)<br>[V0_6_SLC_C1_PRECOMMIT.md](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_PRECOMMIT.md)<br>[V0_6_SLC_C1_PRECOMMIT_SEAL.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_PRECOMMIT_SEAL.json)<br>[QP_GRAMMAR_CONTRACT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/registry/QP_GRAMMAR_CONTRACT.json)<br>[PRECOMMIT_LINEAGE.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G01_PARENT_CUSTODY_AND_SEALED_SOURCE/PRECOMMIT_LINEAGE.json)<br>[QP_GRAMMAR_CONTRACT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/data/QP_GRAMMAR_CONTRACT.json) | [build_v06_slc_c1_precommit.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/build_v06_slc_c1_precommit.py)<br>[cr005_gps_calibration.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/cr005_gps_calibration.sam)<br>[declared_42164km_circular_orbit.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/declared_42164km_circular_orbit.sam)<br>[invalid_deep_conjugate.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_deep_conjugate.sam)<br>[invalid_neutral_conjugate.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_neutral_conjugate.sam)<br>[invalid_physical_mass.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_physical_mass.sam)<br>[invalid_relation_as_constituent.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_relation_as_constituent.sam)<br>[invalid_starbreaker_transition.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_starbreaker_transition.sam)<br>[invalid_static_slot_placement.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_static_slot_placement.sam)<br>[invalid_unresolved_volume.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/invalid_unresolved_volume.sam)<br>[mixed_core_qp.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/mixed_core_qp.sam)<br>[qp_admitted_triad.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_admitted_triad.sam)<br>[qp_carrier.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_carrier.sam)<br>[qp_hidden_support.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_hidden_support.sam)<br>[qp_native_signature.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_native_signature.sam)<br>[qp_ordered_pair.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_ordered_pair.sam)<br>[qp_rejected_triad.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_rejected_triad.sam)<br>[qp_scalar_parent.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_scalar_parent.sam)<br>[qp_triad.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_triad.sam)<br>[qp_unary.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/qp_unary.sam)<br>[slc_bell.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_bell.sam)<br>[slc_ghz12_chain.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_ghz12_chain.sam)<br>[slc_ghz12_star.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_ghz12_star.sam)<br>[slc_peel_restore.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/slc_peel_restore.sam)<br>[structural_only_research.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/structural_only_research.sam)<br>[valid_closure.sam](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/examples/valid_closure.sam)<br>[__init__.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/__init__.py)<br>[cli.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/cli.py)<br>[diagnostic_probe_map.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/diagnostic_probe_map.py)<br>[errors.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/errors.py)<br>[evaluator.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/evaluator.py)<br>[kernels.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/kernels.py)<br>[model.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/model.py)<br>[parser.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/parser.py)<br>[provenance.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/provenance.py)<br>[qp_grammar.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/qp_grammar.py)<br>[qp_native.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/qp_native.py)<br>[registry.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry.py)<br>[registry_core.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry_core.py)<br>[registry_qp.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry_qp.py)<br>[registry_slc.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/registry_slc.py)<br>[runtime.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/runtime.py)<br>[slc_state.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/slc_state.py)<br>[type_system.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/src/sam_language_v0_6/type_system.py)<br>[__init__.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/__init__.py)<br>[test_v03_probe_regression_map.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v03_probe_regression_map.py)<br>[test_v042_clock_kernel.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v042_clock_kernel.py)<br>[test_v04_runtime.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v04_runtime.py)<br>[test_v05_direct_integration.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_direct_integration.py)<br>[test_v05_grammar_exhaustive.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_grammar_exhaustive.py)<br>[test_v05_negative_boundaries.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_negative_boundaries.py)<br>[test_v05_source_tamper.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_source_tamper.py)<br>[test_v05_theorem_regression.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v05_theorem_regression.py)<br>[test_v06_slc_c1.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tests/test_v06_slc_c1.py)<br>[clean_wheel_probe.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/clean_wheel_probe.py)<br>[development_clean_wheel.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/development_clean_wheel.py)<br>[development_static_check.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/development_static_check.py)<br>[reference_qp_enumerator.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/reference_qp_enumerator.py)<br>[run_internal_tests.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/run_internal_tests.py)<br>[run_v06_slc_c1_acceptance.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/run_v06_slc_c1_acceptance.py)<br>[seal_v06_slc_c1_executable.py](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/tools/seal_v06_slc_c1_executable.py) | [G16_BOUNDARY_AND_WRONG-CONTROL_PRESERVATION.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/reports/G16_BOUNDARY_AND_WRONG-CONTROL_PRESERVATION.json) | [V0_6_SLC_C1_ACCEPTANCE_RESULT.json](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_ACCEPTANCE_RESULT.json)<br>[V0_6_SLC_C1_ACCEPTANCE_RESULT.md](../../courtroom/SAM_LANGUAGE/SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE/V0_6_SLC_C1_ACCEPTANCE_RESULT.md) | [All 125 files](../../tests/courtroom/sam-language-sam-language-v0-6-0-slc-c1-formal-simulator-candidate/README.md) |
| [`CR:CR120A@14`](../../tests/courtroom/14-foundational-tests-cr120a-w9-typed-resolution-certificate-bridge/README.md) | [CR120A_PRECOMMIT.md](../../courtroom/14_FOUNDATIONAL_TESTS/CR120A_W9_TYPED_RESOLUTION_CERTIFICATE_BRIDGE/CR120A_PRECOMMIT.md)<br>[CR120A_PRECOMMIT.sha256.txt](../../courtroom/14_FOUNDATIONAL_TESTS/CR120A_W9_TYPED_RESOLUTION_CERTIFICATE_BRIDGE/CR120A_PRECOMMIT.sha256.txt) | [All package files](../../tests/courtroom/14-foundational-tests-cr120a-w9-typed-resolution-certificate-bridge/README.md) | [CR120A_WRONG_CONTROLS.json](../../courtroom/14_FOUNDATIONAL_TESTS/CR120A_W9_TYPED_RESOLUTION_CERTIFICATE_BRIDGE/CR120A_WRONG_CONTROLS.json) | [CR120A_VALIDATION_REPORT.json](../../courtroom/14_FOUNDATIONAL_TESTS/CR120A_W9_TYPED_RESOLUTION_CERTIFICATE_BRIDGE/CR120A_VALIDATION_REPORT.json)<br>[CR120A_result.md](../../courtroom/14_FOUNDATIONAL_TESTS/CR120A_W9_TYPED_RESOLUTION_CERTIFICATE_BRIDGE/CR120A_result.md)<br>[CR120A_summary.json](../../courtroom/14_FOUNDATIONAL_TESTS/CR120A_W9_TYPED_RESOLUTION_CERTIFICATE_BRIDGE/CR120A_summary.json) | [All 19 files](../../tests/courtroom/14-foundational-tests-cr120a-w9-typed-resolution-certificate-bridge/README.md) |
| [`CR:CR120D@14`](../../tests/courtroom/14-foundational-tests-cr120d-x1-intervention-and-w9-certificate-surface/README.md) | [CR120D_PRECOMMIT.md](../../courtroom/14_FOUNDATIONAL_TESTS/CR120D_X1_INTERVENTION_AND_W9_CERTIFICATE_SURFACE/CR120D_PRECOMMIT.md)<br>[CR120D_PRECOMMIT.sha256.txt](../../courtroom/14_FOUNDATIONAL_TESTS/CR120D_X1_INTERVENTION_AND_W9_CERTIFICATE_SURFACE/CR120D_PRECOMMIT.sha256.txt) | [All package files](../../tests/courtroom/14-foundational-tests-cr120d-x1-intervention-and-w9-certificate-surface/README.md) | [All package files](../../tests/courtroom/14-foundational-tests-cr120d-x1-intervention-and-w9-certificate-surface/README.md)<br>[CR120D_VALIDATION_REPORT.json](../../courtroom/14_FOUNDATIONAL_TESTS/CR120D_X1_INTERVENTION_AND_W9_CERTIFICATE_SURFACE/CR120D_VALIDATION_REPORT.json)<br>[CR120D_X1_CONTENT_REPORT.json](../../courtroom/14_FOUNDATIONAL_TESTS/CR120D_X1_INTERVENTION_AND_W9_CERTIFICATE_SURFACE/CR120D_X1_CONTENT_REPORT.json)<br>[CR120D_result.md](../../courtroom/14_FOUNDATIONAL_TESTS/CR120D_X1_INTERVENTION_AND_W9_CERTIFICATE_SURFACE/CR120D_result.md)<br>[CR120D_summary.json](../../courtroom/14_FOUNDATIONAL_TESTS/CR120D_X1_INTERVENTION_AND_W9_CERTIFICATE_SURFACE/CR120D_summary.json) | [CR120D_VALIDATION_REPORT.json](../../courtroom/14_FOUNDATIONAL_TESTS/CR120D_X1_INTERVENTION_AND_W9_CERTIFICATE_SURFACE/CR120D_VALIDATION_REPORT.json)<br>[CR120D_X1_CONTENT_REPORT.json](../../courtroom/14_FOUNDATIONAL_TESTS/CR120D_X1_INTERVENTION_AND_W9_CERTIFICATE_SURFACE/CR120D_X1_CONTENT_REPORT.json)<br>[CR120D_result.md](../../courtroom/14_FOUNDATIONAL_TESTS/CR120D_X1_INTERVENTION_AND_W9_CERTIFICATE_SURFACE/CR120D_result.md)<br>[CR120D_summary.json](../../courtroom/14_FOUNDATIONAL_TESTS/CR120D_X1_INTERVENTION_AND_W9_CERTIFICATE_SURFACE/CR120D_summary.json) | [All 15 files](../../tests/courtroom/14-foundational-tests-cr120d-x1-intervention-and-w9-certificate-surface/README.md) |
| [`CR:CR120V@14`](../../tests/courtroom/14-foundational-tests-cr120v-b-x1-typed-half-relay-archival-discrimination/README.md) | [CR120V_PRECOMMIT.md](../../courtroom/14_FOUNDATIONAL_TESTS/CR120V_B_X1_TYPED_HALF_RELAY_ARCHIVAL_DISCRIMINATION/CR120V_PRECOMMIT.md)<br>[CR120V_PRECOMMIT.sha256.txt](../../courtroom/14_FOUNDATIONAL_TESTS/CR120V_B_X1_TYPED_HALF_RELAY_ARCHIVAL_DISCRIMINATION/CR120V_PRECOMMIT.sha256.txt) | [CR120V_runner.py](../../courtroom/14_FOUNDATIONAL_TESTS/CR120V_B_X1_TYPED_HALF_RELAY_ARCHIVAL_DISCRIMINATION/CR120V_runner.py) | [CR120V_WRONG_CONTROLS.csv](../../courtroom/14_FOUNDATIONAL_TESTS/CR120V_B_X1_TYPED_HALF_RELAY_ARCHIVAL_DISCRIMINATION/CR120V_WRONG_CONTROLS.csv) | [CR120V_result.md](../../courtroom/14_FOUNDATIONAL_TESTS/CR120V_B_X1_TYPED_HALF_RELAY_ARCHIVAL_DISCRIMINATION/CR120V_result.md)<br>[CR120V_summary.json](../../courtroom/14_FOUNDATIONAL_TESTS/CR120V_B_X1_TYPED_HALF_RELAY_ARCHIVAL_DISCRIMINATION/CR120V_summary.json) | [All 13 files](../../tests/courtroom/14-foundational-tests-cr120v-b-x1-typed-half-relay-archival-discrimination/README.md) |
| [`CR:CR120X@14`](../../tests/courtroom/14-foundational-tests-cr120x-dual-depth-theta-b-x1-w8-w9-relaxed-discovery/README.md) | [CR120X_CONTRACT.json](../../courtroom/14_FOUNDATIONAL_TESTS/CR120X_DUAL_DEPTH_THETA_B_X1_W8_W9_RELAXED_DISCOVERY/CR120X_CONTRACT.json)<br>[CR120X_PRECOMMIT.md](../../courtroom/14_FOUNDATIONAL_TESTS/CR120X_DUAL_DEPTH_THETA_B_X1_W8_W9_RELAXED_DISCOVERY/CR120X_PRECOMMIT.md)<br>[CR120X_PRECOMMIT_SEAL.txt](../../courtroom/14_FOUNDATIONAL_TESTS/CR120X_DUAL_DEPTH_THETA_B_X1_W8_W9_RELAXED_DISCOVERY/CR120X_PRECOMMIT_SEAL.txt) | [CR120X_runner.py](../../courtroom/14_FOUNDATIONAL_TESTS/CR120X_DUAL_DEPTH_THETA_B_X1_W8_W9_RELAXED_DISCOVERY/CR120X_runner.py) | [CR120X_WRONG_CONTROLS.csv](../../courtroom/14_FOUNDATIONAL_TESTS/CR120X_DUAL_DEPTH_THETA_B_X1_W8_W9_RELAXED_DISCOVERY/release/CR120X_WRONG_CONTROLS.csv) | [CR120X_SUMMARY.json](../../courtroom/14_FOUNDATIONAL_TESTS/CR120X_DUAL_DEPTH_THETA_B_X1_W8_W9_RELAXED_DISCOVERY/release/CR120X_SUMMARY.json)<br>[CR120X_result.md](../../courtroom/14_FOUNDATIONAL_TESTS/CR120X_DUAL_DEPTH_THETA_B_X1_W8_W9_RELAXED_DISCOVERY/release/CR120X_result.md) | [All 18 files](../../tests/courtroom/14-foundational-tests-cr120x-dual-depth-theta-b-x1-w8-w9-relaxed-discovery/README.md) |
| [`CR:CR120Y@14`](../../tests/courtroom/14-foundational-tests-cr120y-theta18-model-wide-primary-carrier-stress-test/README.md) | [CR120Y_CONTRACT.json](../../courtroom/14_FOUNDATIONAL_TESTS/CR120Y_THETA18_MODEL_WIDE_PRIMARY_CARRIER_STRESS_TEST/CR120Y_CONTRACT.json)<br>[CR120Y_PRECOMMIT.md](../../courtroom/14_FOUNDATIONAL_TESTS/CR120Y_THETA18_MODEL_WIDE_PRIMARY_CARRIER_STRESS_TEST/CR120Y_PRECOMMIT.md)<br>[CR120Y_PRECOMMIT_SEAL.txt](../../courtroom/14_FOUNDATIONAL_TESTS/CR120Y_THETA18_MODEL_WIDE_PRIMARY_CARRIER_STRESS_TEST/CR120Y_PRECOMMIT_SEAL.txt) | [CR120Y_runner.py](../../courtroom/14_FOUNDATIONAL_TESTS/CR120Y_THETA18_MODEL_WIDE_PRIMARY_CARRIER_STRESS_TEST/CR120Y_runner.py) | [CR120Y_WRONG_CONTROLS.csv](../../courtroom/14_FOUNDATIONAL_TESTS/CR120Y_THETA18_MODEL_WIDE_PRIMARY_CARRIER_STRESS_TEST/release/CR120Y_WRONG_CONTROLS.csv) | [CR120Y_CORPUS_SUMMARY.json](../../courtroom/14_FOUNDATIONAL_TESTS/CR120Y_THETA18_MODEL_WIDE_PRIMARY_CARRIER_STRESS_TEST/release/CR120Y_CORPUS_SUMMARY.json)<br>[CR120Y_SUMMARY.json](../../courtroom/14_FOUNDATIONAL_TESTS/CR120Y_THETA18_MODEL_WIDE_PRIMARY_CARRIER_STRESS_TEST/release/CR120Y_SUMMARY.json)<br>[CR120Y_result.md](../../courtroom/14_FOUNDATIONAL_TESTS/CR120Y_THETA18_MODEL_WIDE_PRIMARY_CARRIER_STRESS_TEST/release/CR120Y_result.md) | [All 22 files](../../tests/courtroom/14-foundational-tests-cr120y-theta18-model-wide-primary-carrier-stress-test/README.md) |

Some tests put wrong-control definitions in the runner and their outcomes in the result or summary. Those original files are linked together when no separate controls file exists.

<!-- END CHAPTER COURTROOM PACKAGES -->

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000042`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/DIRECTIONAL_HISTORY_AND_EVENT_REEL_COMPUTATION.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol III | SAMA-D000042 | Directional History | Exact Directional Quotient, Append-Only Event Reels and AFC Join |

| Document field | Value |
|---|---|
| Purpose | Present the generic directional core, rank-161 quotient, append-only Exact Write reel, Theta-event/N144-AFC join and application-adapter authority boundary. |
| Prerequisite documents | `SAMA-D000038`, `SAMA-D000039`, `SAMA-D000040` |
| Used by | `SAMA-D000043` |
| Revision state | Unapproved revision 1; no current pointer, registry or result classification is changed. |

</details>
