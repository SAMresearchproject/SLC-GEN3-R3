[SAM](../../README.md) · [Volume III](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# Exact State Spaces and SLC Computation

## SLC-GEN3-R3: current computation — 14 September 2026

SLC-GEN3-R3 and SLC-GEN3-CEV1-R3 are the sole current global runtime and CE, generation GEN3-UNIFIED-EXECUTION1-20260910-G2. Exact execution, acquired support, complete ordered history and exact U/D/V/net/M logarithmic accumulation share one durable machine. Installation records 617 core and 191 memory-admission checks; adoption records 75 checks and 49 managed receipts. Native hosts agree on 8,123,904 exact values. GEN3-RXT-R7.1 adds the C++/CUDA/GMP joint research implementation.

[Current derivations, code and results](../../../docs/ARCHITECTURE.md).

## Retained source-era derivation and results

The following development retains its original experimental context and revision fields. Historical engine selections and campaign status in this source-era account are superseded by the dated current section above.


## Conceptual abstract

An exact state-space computation answers a stronger question than an optimizer:
not merely which assignment has the lowest energy, but how many assignments
occupy every possible energy. For a declared binary Hamiltonian this complete
answer is the density of states, or DOS. Its coefficients are integers, their
sum is the complete formal configuration count, and their arrangement retains
the energy organization created by the graph, couplings and fields.

The computation can be exact without visiting every assignment one by one.
Gray enumeration, variable elimination, component convolution, modular
polynomial arithmetic, orbit sectors and rank-aware readout are different
routes to the same requested object. Their right to be called exact comes from
reconstruction and equality obligations: coefficientwise agreement, state-
count closure, moments, symmetries, port marginals, hashes and independent
readers. Runtime is useful evidence about an execution route; it is not the
definition of exactness.

This distinction has a second consequence. Exact mathematics and executable
custody are separate obligations. SLCX023 retained exact exhaustive and
NTT/variable-elimination authorities but failed its frozen same-run custody
gates. That failure remains part of the record. SLCX023A corrected the custody
mechanism in a separate successor, reproduced the unchanged coefficient
authorities and left the failed parent immutable. The chain demonstrates the
Courtroom method at its best: retain what failed, identify the type of failure,
change only the defective layer, replay the original question and preserve
both receipts.

The chapter ends by deriving exact thermodynamic readers from the frozen N96
DOS. Those readers are exact and dimensionless while the physical energy scale
remains symbolic. A polynomial can determine partition functions and moments
without thereby choosing joules, kelvin, a contact orientation or a physical
binding map.

## 1. Opening question and conceptual picture

The governing question is:

> How can a finite computational system account for every formal assignment,
> preserve the exact integer answer under different execution routes, and
> carry that answer into thermodynamics without importing an undeclared
> physical scale?

The full chain is

```text
declared typed grammar and Hamiltonian
  -> exact integer DOS g(E)
  -> independent route equality and state-count closure
  -> custody-qualified frozen artifact
  -> exact polynomial P(x)
  -> exact partition, moment and response readers
  -> symbolic-scale physical boundary
```

Every arrow changes the representation or the question, not the source
object. A component factorization may reduce work but may not reduce the state
space being counted. CRT may store residues but must reconstruct the original
integers. A thermodynamic reader may turn coefficients into rational functions
or numerical display values but may not retroactively change the DOS. A
physical unit conversion may occur only after a source-authorized scale exists.

## 2. Typed definitions and domains

### 2.1 Source grammar, assignment and Hamiltonian

Let \(V=\{1,\ldots,N\}\) be the declared independent binary sites, let
\(E_G\subseteq V\times V\) be the declared interaction edges, and let

\[
\sigma=(\sigma_1,\ldots,\sigma_N)\in\{-1,+1\}^N.
\]

For integer edge weights \(J_{ij}\) and integer local fields \(h_i\), the
Ising-type Hamiltonian used here is

\[
H(\sigma)=\sum_{(i,j)\in E_G}J_{ij}\sigma_i\sigma_j
          +\sum_{i\in V}h_i\sigma_i.
\]

The types are load-bearing:

- \(N\) counts independent binary coordinates;
- \(E_G\) is topology, not an energy histogram;
- \(J_{ij}\) and \(h_i\) are declared Hamiltonian coefficients;
- a native grammar-row value does not become \(J_{ij}\) merely because it is
  numerical; and
- a constrained occurrence ledger is not automatically an independent
  \(N\)-spin state space.

This is why the N100 compiler keeps source-row selection separate from
Hamiltonian coefficients and why later M126/N144/L162 readouts retain their
rank and sidecar types.

### 2.2 Density of states

For each attainable integer energy \(e\), define

\[
g(e)=\#\{\sigma\in\{-1,+1\}^N:H(\sigma)=e\}.
\]

The function \(g\) is an exact integer ledger. Summing over all energies
partitions the complete configuration space:

\[
\sum_e g(e)
=\sum_e\sum_{\sigma}\mathbf 1[H(\sigma)=e]
=\sum_{\sigma}1
=2^N.
\]

This derivation is elementary but decisive. Every assignment has exactly one
energy, so it contributes once. Frustration changes which energies occur and
how assignments are distributed among them. It does not change the cardinality
\(2^N\) of the formal assignment domain.

A ground-state solver keeps only

\[
e_0=\min_\sigma H(\sigma),\qquad g(e_0),
\]

whereas a DOS retains every pair ((e,g(e))). Interior bins, odd moments,
response sectors and finite-temperature behavior would be lost if the output
were reduced to an optimum.

### 2.3 Exactness, execution and custody

Three types must not be collapsed:

| Type | Question answered | Required evidence |
|---|---|---|
| Mathematical exactness | Are the requested coefficients the exact integers? | equality, closure, moments, symmetries, reconstruction |
| Execution policy | How was the exact object evaluated? | route declaration, worker/batch receipts, performance data |
| Artifact custody | Did the sealed code, inputs, receipts and outputs retain their declared identities? | hashes, domains, manifests, independent verification |

An exact tensor with a failed receipt is not a successful custody packet. A
fast route with no equality proof is not established as exact. A hash-correct
artifact does not become the right mathematical object unless the declared
calculation also closes.

## 3. Deriving the exact route family

### 3.1 Gray exhaustive authority

The direct definition suggests enumerating all \(2^N\) assignments. A Gray
code orders them so adjacent assignments differ in one spin. If spin \(k\)
changes sign, only terms incident to \(k\) change, giving the incremental
update

\[
\Delta H_k
=-2\sigma_k\left(h_k+\sum_{j:(k,j)\in E_G}J_{kj}\sigma_j\right).
\]

Thus one full energy need not be recomputed from scratch at every state. The
route is still exponential in the number of visited assignments, but for
small \(N\) it is transparent and supplies an independent authority against
more structured routes. In SLCX023, `GRAY_EXHAUSTIVE` covers the complete
address space through \(N=24\).

### 3.2 Variable elimination

Write a local factor for every edge and field contribution. Eliminating a
spin means summing its two values while retaining an exact table over the
still-live neighboring boundary. If \(B_k\) is that boundary and \(z\) marks
energy, a schematic elimination step is

\[
F_{k+1}(\sigma_{B_k};z)
=\sum_{\sigma_k=\pm1}
 z^{\Delta H_k(\sigma_k,\sigma_{B_k})}
 F_k(\sigma_k,\sigma_{B_k};z).
\]

The coefficients remain integers. Cost follows the largest induced boundary
width \(w\), roughly through tables of size \(2^w\), rather than nominal arity
alone. Different elimination orders therefore change work while leaving the
Hamiltonian and the final polynomial fixed.

SLCX023 deliberately used two distinct exact versions: a reference NTT/VE
route with a frozen min-degree order and a typed NTT/VE route with an
independently frozen cell-aware min-fill order. Their boundary tables were
retained so equality could be checked below the final scalar output.

### 3.3 Exact component convolution

Suppose the declared graph splits into independent components
\(G_1,\ldots,G_m\) after conditioning on an explicit boundary. If component
\(a\) has DOS polynomial

\[
P_a(z)=\sum_e g_a(e)z^e,
\]

then additivity of energy gives

\[
P_G(z)=\prod_{a=1}^mP_a(z),
\]

and therefore

\[
g_G(e)=\sum_{e_1+\cdots+e_m=e}
        \prod_{a=1}^m g_a(e_a).
\]

This is not a sample or truncation. Every combination of component
assignments appears once in the convolution. At \(z=1\), closure is inherited:

\[
P_G(1)=\prod_aP_a(1)=\prod_a2^{N_a}=2^{\sum_aN_a}.
\]

The N100 structure-first calculation in `SAMA-D000037` uses this exact
identity. The same logic also explains why a reduced work count can still
return a complete \(2^N\) census.

### 3.4 NTT lanes and CRT reconstruction

Large integer polynomial products can be evaluated modulo primes. For a
suitable prime \(p_ell\), an NTT transforms coefficients, multiplies pointwise
and applies the inverse transform, all in exact modular arithmetic. One lane
returns

\[
g(e)\bmod p_\ell.
\]

With pairwise-coprime primes \(p_1,\ldots,p_L\), CRT returns the unique integer
coefficient modulo

\[
M=\prod_{\ell=1}^Lp_\ell.
\]

If the declared coefficient bound is less than \(M\) (or less than \(M/2\)
for a signed reconstruction), the original integer is unique. The modular
lanes are therefore an exact representation of the coefficient only when the
prime product, reconstruction convention and bound all close. A displayed
floating-point polynomial is downstream and cannot replace these obligations.

### 3.5 Orbit sectors and rank-aware readout

When a dense graph is uniform under a declared permutation action, assignments
can be grouped by marked population. A sector with \(k\) marked sites has
multiplicity

\[
\binom Nk,
\]

provided the Hamiltonian is constant on that orbit or the remaining typed
coordinates are retained. This replaces assignment traversal with an exact
orbit census.

Likewise, an ambient readout with \(m\) slots may have only \(r<m\)
independent coordinates. The exact route evaluates the \(2^r\) independent
domain and applies the declared readout map. It must not report the ambient
\(2^m\) ceiling as independent state count. This distinction becomes critical
for N144 independent state and L162 constrained occurrence views.

### 3.6 Route-acceptance checklist

Two routes may differ internally and still compute the same object. Their
equivalence is established through a layered checklist:

1. identical occupied-energy support;
2. identical integer coefficient in every bin;
3. \(sum_e g(e)=2^N\);
4. matching exact raw moments \(\sum_e e^kg(e)\);
5. declared parity, complement and role-permutation symmetries;
6. matching retained-port marginals and conditional tensors;
7. stable semantic hashes; and
8. an independent reconstruction or reader.

A runtime comparison is interpreted only after these checks establish
same-object, same-output work.

## 4. Deviation chain: SLCX023 to SLCX023A

### 4.1 The frozen question

SLCX023 asked whether a frozen exact-DOS development ladder could close across
six instances of sizes (12,24,36) using independent Gray, reference NTT/VE
and typed NTT/VE authorities while also preserving execution and receipt
custody. The equality standard was exact: same occupied energies and same
integer coefficient in every bin.

The campaign also contained eight deliberately wrong controls and eighteen
metamorphic checks. Wrong controls were not noise to be deleted. They were
expected-invalid transformations used to demonstrate that the validation
surface could distinguish the declared computation from plausible but wrong
alternatives.

### 4.2 Preserved failure

The run completed all six instances, detected all eight wrong controls and
passed all eighteen metamorphic checks. Yet its frozen verdict remained

```text
SLCX023_FAIL__EXACT_DOS_MISMATCH_OR_CUSTODY
```

because the first coefficient, custody, invariant or execution failure was a
stop condition and same-run repair was forbidden. The historical G02 and G11
custody gates failed. This typed outcome matters: the available exact lane
structure did not authorize rewriting a failed executable receipt as a pass.

The parent preserved its precommit, executable and execution-ledger hashes and
recorded `same_run_repair = false`. The failed packet therefore remained
reconstructible.

### 4.3 Correction hypothesis

The appeal did not change the scientific question, Hamiltonians, route
definitions or coefficient authorities. It isolated two implementation and
custody mechanisms:

- execute the official retest from an isolated retained capsule whose runner,
  adapter and engine bytes are checked before and after work; and
- distinguish the external lane domain of legacy receipts from the
  boundary-table schema recorded by corrected receipts.

This is a narrow correction. It predicts that the unchanged scientific
outputs will reproduce while the custody gates now close.

### 4.4 Separate retest and cumulative record

SLCX023A executed as a successor rather than modifying SLCX023. It reproduced
all 16 of 16 lane-instance DOS hashes, passed 154 of 154 exactness checks, 64
of 64 moment checks and 18 of 18 metamorphic controls. Twelve of those
metamorphic controls reran transformed solvers and six diagnosed cell
repartitioning. All 432 corrected receipts verified with their domain and
boundary-table schema separated and with signed links back to the legacy
hashes.

The complete chain is therefore

```text
SLCX023 frozen design
  -> exact lanes execute
  -> custody G02/G11 do not close
  -> parent remains FAIL and immutable
  -> SLCX023A precommits two custody corrections
  -> unchanged 16/16 scientific hashes reproduce
  -> exactness, moment, metamorphic and 432 receipt checks pass
  -> corrected successor supplements the parent
```

No hidden \(N=48\) or \(N=60\) instance was opened. The appeal did not install
a SAM Language operator or create a physical Ising/gravity claim.

## 5. Frozen N96 worked example

### 5.1 Complete configuration count

For \(N=96\),

\[
2^{96}=79{,}228{,}162{,}514{,}264{,}337{,}593{,}543{,}950{,}336.
\]

The frozen H14C computation completed four CRT primes and 1,024 root-batch
checkpoints. It retained sixteen port rows, each summing to \(2^{92}\), hence

\[
16\cdot2^{92}=2^4\cdot2^{92}=2^{96}.
\]

The scalar DOS occupies 348 energy bins from \(-346\) through \(348\), with
ground-state degeneracy 12. State-count, support, parity and raw-moment checks
one through four passed. Both active \(512\times512\) fiber factors remained
installed and all four scalar marginals equal the exact N96 result.

The execution completed in 40,307.938817 seconds with the frozen DOS semantic
hash
`d74fb93facbebf18fa3cfe3ab2d33a0ec013f27b7ab6f326414bd5cdce4a11cb`.
The later H14F profile reproduced that DOS hash under a different execution
policy. That comparison concerns work routing; it does not replace the N96
Hamiltonian or create a second physical model.

### 5.2 Shifted exact polynomial

The energy spacing is two, so write

\[
E_k=-346+2k,\qquad 0\le k\le347,
\]

and define

\[
P_{96}(x)=\sum_{k=0}^{347}g(E_k)x^k.
\]

Then

\[
P_{96}(1)=\sum_kg(E_k)=2^{96},
\]

with \(a_0=12\) and \(a_{347}=7\). The degree records the complete occupied
energy span after shifting; its coefficients remain the exact degeneracies.

## 6. From DOS to exact thermodynamics

### 6.1 Partition function derivation

Let the dimensionless inverse scale be \(b=\beta\epsilon_E\), where
\(epsilon_E\) remains symbolic, and set

\[
x=e^{-2b}.
\]

The partition function is

\[
Z(b)=\sum_k g(E_k)e^{-bE_k}
=\sum_k g(E_k)e^{-b(-346+2k)}.
\]

Since \(e^{346b}=x^{-173}\) and \(e^{-2bk}=x^k\),

\[
Z_{96}(x)=x^{-173}P_{96}(x).
\]

This factorization separates the exact coefficient ledger from the chosen
thermodynamic reader.

### 6.2 Euler derivatives and moments

Let

\[
\Theta=x\frac{d}{dx}.
\]

Then

\[
\Theta P=\sum_k k g(E_k)x^k,
\qquad
\Theta^2P=\sum_k k^2g(E_k)x^k.
\]

The mean shifted index is \(\langle k\rangle=\Theta P/P\). Because
\(E=-346+2k\),

\[
\langle E\rangle=-346+2\frac{\Theta P}{P},
\]

and

\[
\operatorname{Var}(E)
=4\left(\frac{\Theta^2P}{P}
-\left(\frac{\Theta P}{P}\right)^2\right).
\]

Higher raw moments follow by expanding \((-346+2k)^m\) and replacing \(k^j\)
with \(\Theta^jP/P\). At \(x=1\), T1 records

\[
\langle E\rangle=0,
\quad\langle E^2\rangle=1286,
\quad\langle E^3\rangle=534,
\quad\langle E^4\rangle=4{,}952{,}792.
\]

The nonzero third moment retains an exact asymmetry hidden by the zero mean.
The microcanonical mode is \(E=0\) with

\[
g(0)=1{,}761{,}659{,}846{,}545{,}153{,}896{,}312{,}195{,}809.
\]

At the positive low-temperature end, the reader approaches \(E=-346\), zero
variance and entropy \(\log 12\). At \(x=1\), it returns mean zero, variance
1286 and entropy \(96\log2\).

### 6.3 Conditional response and the open/closed boundary

T2 refines the scalar polynomial into a frozen \(4\times5\times1181\)
integer attachment. Every q marginal reconstructs T1. There are twenty
response-sector polynomials, ten active and ten inactive, and eight distinct
signatures including zero.

The closed trace retains three q signatures and merges \(q=1\) with \(q=3\).
The open retained port retains four routing signatures and all five response
values. Thus a closed equality cannot be copied backward as an open-contact
identity. At \(x=1\), \(q=2\) has exact energy-response covariance 8, while
\(q=1\) and \(q=3\) have zero linear covariance but nonzero mutual information.
The conditional structure survives beyond a scalar covariance summary.

## 7. Wrong controls and type firewalls

The useful wrong controls answer specific failure questions:

| Control | What it preserves | What it changes or violates |
|---|---|---|
| Deterministic count permutation | \(2^{96}\), coefficient multiset | moment vector and energy placement |
| Exact sign reflection | even moments | signs of odd moments |
| Rational uniform spectrum | support and total weight | integer state-count semantics and moment vector |
| C4-to-C2 quotient | some aggregate response structure | distinct \(q=0\) and \(q=2\) lanes |
| Factorized response control | response totals and scalar marginals | actual \(q=1,2,3\) joint structure |
| Open-port/closed-trace comparison | shared source object | routing availability versus final occupancy |

These controls demonstrate why closure alone is necessary but insufficient.
Many wrong objects can sum to \(2^N\). Exactness belongs to the coefficient
ledger, its typed marginals and its independent reconstruction together.

The physical firewall is equally explicit:

```text
exact integer DOS       != physical energy calibration
symbolic epsilon_E      != measured joules
dimensionless b         != temperature in kelvin
q_A source support      != epsilon_E
A(r) accumulation lift  != Ising coupling J_ij
open routing signature  != closed-trace occupancy
```

BIPM constants may convert units after a physical scale is supplied; they do
not choose the scale. The current frozen `SLCQ2-RZ` selection engine delegates
byte-identical arithmetic/application work to the frozen `SLCV21R` base. The
historical N96, H14C/H14F, Exact Write and thermodynamic artifacts retain their
scoped results, but none replaces `SLCQ2-RZ` as the current/default SLC.

## 8. Established result, boundary and forward handoff

The established mathematical object is the complete exact DOS, not only a
ground sector. Multiple exact routes may evaluate it, but all must reconstruct
the same integer coefficients and close the same typed marginals. The frozen
N96 release accounts for every one of \(2^{96}\) assignments, and its exact
polynomial supports exact scalar and conditional thermodynamic readers.

The preserved deviation result is equally important: SLCX023 remains the
failed custody parent; SLCX023A is the separate correction and retest. The
successor repairs executable custody without rewriting the earlier run or
changing the scientific tensor.

The forward handoff has three branches:

1. `SAMA-D000037` shows how source grammar becomes an exact work certificate
   while preserving the full state space and H14F fallback.
2. `SAMA-D000038` develops the exact write transaction and compiled group-law
   execution surface.
3. A future direct evidence route must register SLCX023/SLCX023A, N96,
   T1–T6A and current `SLCQ2-RZ` artifacts before those sources can populate a
   qualified SAMA test crosswalk. Their absence is recorded, not filled with
   invented keys.

## Test and result index

No direct qualified test key is assigned to `SAMA-D000036` in the current
document registration proposal. The source artifacts below are documentary
authorities, not substitutes for absent test-registry rows.

| Evidence route | Role in this chapter | Direct qualified key |
|---|---|---|
| SLCX023 | Preserved exact-DOS/custody failure | Absent |
| SLCX023A | Separate custody correction and unchanged replay | Absent |
| SLCV0.4-96-H14C-512 | Frozen N96 exact regression | Absent |
| T1 | Exact scalar thermodynamic reader | Absent |
| T2 | Exact q/response conditional reader | Absent |
| T3–T6A | Downstream symbolic-scale ladder and boundary | Absent |
| SLCQ2-RZ | Current selection authority over delegated SLCV21R base | Absent |

`G:G1@SAM-RESEARCH` is a prerequisite compiler audit in `SAMA-D000034`; it is
not a direct DOS, thermodynamics or Q2 release test for this chapter.

## Atomic record index

| Atomic record | Role |
|---|---|
| `SAMA-C000008-R001` | Complete Exact Write computation surface used by the downstream handoff. |
| `SAMA-C000198-R001` | Exact DOS definition and \(2^N\) closure. |
| `SAMA-C000199-R001` | Exact route family and validation obligations. |
| `SAMA-C000200-R001` | Preserved SLCX023 custody failure. |
| `SAMA-C000201-R001` | Separate SLCX023A correction and retest. |
| `SAMA-C000202-R001` | Frozen N96 regression and execution-policy distinction. |
| `SAMA-C000203-R001` | Symbolic thermodynamic scale and energy boundary. |

## External and repository source references

- `volume_III/SAM_VOLUME_III_COMPUTATION_TECHNICAL_SPINE.md`, §§III.1–III.6,
  V.4–V.5, SHA-256
  `1996303d0940dd5dca12aa03ff3c9a426772272095df683346a75961eab895bb`.
- `SLC/18_SAM_NATIVE_QC/SLCX023_EXACT_FRUSTRATED_ISING_DENSITY_OF_STATES_DEVELOPMENT_LADDER/release/SLCX023_RESULT.md`.
- `SLC/18_SAM_NATIVE_QC/SLCX023A_EXECUTABLE_CUSTODY_AND_RECEIPT_DOMAIN_APPEAL_RETEST/release/SLCX023A_RESULT.md`.
- `SLC/18_SAM_NATIVE_QC/SLCV40_N96_CAPACITY_ADMITTED_H14C_512/release/SLCV0.4-96-H14C-512_RELEASE.md`.
- `SLC/SAM_LANGUAGE/SAM_LANGUAGE_CONTACT_NATIVE_SUCCESSOR_DESIGN/SLC_EXACT_THERMODYNAMICS_T1_N96_SCALAR_V1/T1_RESULT.md`.
- `SLC/SAM_LANGUAGE/SAM_LANGUAGE_CONTACT_NATIVE_SUCCESSOR_DESIGN/SLC_EXACT_THERMODYNAMICS_T2_N96_Q_RESPONSE_V1/T2_RESULT.md`.
- `SAM_LIVE/01_SLC_CURRENT.md`, current `SLCQ2-RZ` and delegated frozen
  `SLCV21R` authority boundary.

## Revision boundary

This is an unapproved source-bound revision. It proposes no new test key,
atomic promotion, SLC pointer change, physical scale or result classification.

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000036`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/EXACT_STATE_SPACES_AND_SLC_COMPUTATION.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

| Vol | Document | Branch | Topic |
|---|---|---|---|
| Vol III | SAMA-D000036 | SLC Exact Computation | Exact DOS Routes, Arithmetic Custody and Symbolic Thermodynamics |

| Document field | Value |
|---|---|
| Purpose | Present exact DOS definitions and route families, the preserved SLCX023 custody failure, its separate correction, the frozen N96 regression and symbolic thermodynamic boundaries. |
| Prerequisite documents | `SAMA-D000034` |
| Used by | `SAMA-D000037`, `SAMA-D000038`, `SAMA-D000055` |
| Revision state | Unapproved revision 1; no current pointer, registry or result classification is changed. |

</details>
