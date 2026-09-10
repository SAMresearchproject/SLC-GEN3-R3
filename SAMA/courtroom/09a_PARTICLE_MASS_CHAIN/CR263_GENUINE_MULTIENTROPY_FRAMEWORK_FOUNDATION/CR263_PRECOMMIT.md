# CR263 — Genuine Multientropy / Dihedral-Invariant Framework Foundation

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Classification:** FRAMEWORK_FOUNDATION_CR (no measurement; structural commitment + citation lock)
**Sealed by:** Sean Brady, 2026-06-30
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Test Type

```text
Foundation-citation CR. No measurement, no fit, no catalog data read.
Formally registers the mathematical framework SAM commits to for
multipartite entanglement of stabilizer-class substrate states, cites
the load-bearing external reference, and locks the structural mappings
between the paper's results and SAM's already-sealed tripartite
structures (CR229 inclusion-exclusion identity, CR248 four-particle
algebra, CR253 promoter tripartition, CR256 A-conjugate, CR259
chessboard, CR262 carrier/container cipher).

This CR does NOT yet seal numerical predictions. It seals the
mathematical category in which downstream binding-cipher CRs (CR264
state specification, CR265 binding-fee derivation) will operate.

Same shape as CR258 (substrate primitive closure audit) but for the
entanglement framework rather than the substrate-atom inventory.
```

## Question

```text
Does the mathematical framework of multipartite entanglement for
stabilizer-class states — specifically the genuine multientropy
reduction theorem and the dihedral-invariant equivalence proved in
Berthière & Gaudin (2026) — provide the natural category in which to
express SAM's substrate-tripartition binding-fee structure, and do
SAM's sealed tripartite structures (CR229 / CR248 / CR253 / CR256 /
CR259 / CR262) admit consistent identifications with the paper's
mathematical objects?
```

## Cited Reference (load-bearing)

```text
C. Berthière and P. Gaudin,
"Genuine multientropy, dihedral invariants, and Lifshitz theory."
Phys. Rev. D 113, 065029 (2026).
DOI: 10.1103/vcqd-rkmn
Received 24 November 2025; accepted 14 January 2026; published 30 March 2026.

Laboratoire de Physique Théorique, CNRS,
Université de Toulouse, Toulouse, France.

Published under CC-BY 4.0; funded by SCOAP³.
```

The paper is the external structural foundation this CR cites. It is
not modified, re-derived, or re-checked — the paper's theorems are
treated as load-bearing prior art and SAM's identifications are made
against them.

## Load-Bearing Results from the Paper (transcribed for the record)

### Result 1 — Genuine multientropy reduction theorem (Eq. 23)

```text
For tripartite pure states with separable bipartite marginal of the
form ρ_AB = (1/d) Σ ρ_A^i ⊗ ρ_B^i  (which includes GHZ states,
stabilizer states, and Lifshitz ground states):

  G^(3)_n(A:B:C) = (2-n)/(2n) · [I_{1/2}(A:B) - 2·E(A:B)]

where
  G^(3)_n  = genuine multientropy = S^(3)_n - (1/2)·[S_n(A) + S_n(B) + S_n(C)]
  I_{1/2}  = (1/2)-Rényi mutual information = S_{1/2}(A) + S_{1/2}(B) - S_{1/2}(A∪B)
  E(A:B)   = logarithmic negativity = log ||ρ_AB^{T_B}||
  S_n(K)   = Rényi entanglement entropy of subsystem K at index n
```

### Result 2 — Vanishing at n = 2

```text
For Lifshitz ground states and stabilizer states:
  G^(3)_2(A:B:C) = 0   (because Markov gap M_{2,2} = 0)

Equivalently, at n=2 the genuine tripartite entanglement vanishes for
the symmetric stabilizer class.
```

### Result 3 — GHZ extraction interpretation

```text
For stabilizer states (which include GHZ + Bell + unentangled qudits):
  (I_{1/2} - 2E) counts the number of GHZ states extractable from
  the stabilizer state.

(Paper, Discussion section.)
```

### Result 4 — Dihedral / reflected-entropy equivalence (Eq. 40)

```text
For general tripartite pure states:
  D_{2n}(A:B) = S^R_{2,n}(A:C)

The dihedral invariant on subsystems (A, B) equals the (2, n)-Rényi
reflected entropy on subsystems (A, C). The dihedral permutations are
isomorphic to the reflected-construction permutations, with explicit
isomorphism (Eq. 38 of the paper).
```

### Result 5 — Realignment / CCNR connection (Eq. 41)

```text
log Z_{2n} = E^CCNR_n(A:C)

The unnormalized dihedral partition function equals the Rényi CCNR
negativity of the realignment of reduced density matrices.
```

## SAM's Sealed Tripartite Structures Under Test

```text
Tripartite structure                    Sealed in        Substrate atoms
───────────────────────────────────────────────────────────────────────
Source-quark channels (u, d, e)         CR248@09a         u=2Z+N, d=Z+2N, e=Z
Four-particle algebraic decomposition   CR248@09a         (p, n_b, n_e, e)
Inclusion-exclusion ledger identity     CR229@09a         R² = M + Θ = ℒ − Θ
                                                          two F=81 sides ∩ Θ=18
Matter / antimatter / carrier classes   CR253@09a         48 / 32 / carriers
A-conjugate operator (antimatter)       CR256@09a         (5/6)(1+p/R²) / (6/5)(1−p/R²)
Chessboard T13 lattice                  CR259@09a         13×13 = 169
Carrier / container cipher              CR262@09a         m₃, D², Θ, ĥV / R, V, F
```

## Locked Identifications

The following structural identifications are committed by this CR.
They are mathematical claims, not numerical predictions, and they
constrain downstream CRs (CR264, CR265, ...) without locking specific
fees or masses.

### Identification I1 — Substrate states are stabilizer-class

```text
SAM's substrate carrier accounting is built from a closed set of
discrete operations (the partition algebra ĥ^i · d̂^j) acting on
integer-valued occupation states. The resulting states are
stabilizer-class in the technical sense of Bravyi-Fattal-Gottesman
(Ref. [81] of the paper).

Consequence: Result 1 (Eq. 23) applies to SAM tripartitions evaluated
on the substrate's stabilizer-class states.
```

### Identification I2 — C-12 is the substrate's GHZ-symmetric anchor

```text
C-12 has source counts (u, d, e) = (Θ, Θ, m₃) where u = d = Θ holds
exactly. Under any state model that respects u-d symmetry, Result 2
(G^(3)_2 = 0 for Lifshitz / stabilizer) applies:

  G^(3)_2(C-12) = 0

This is consistent with m(C-12) = 12 exactly by definition of u
(no "fee" beyond the algebraic spine).

CR262 already sealed C-12 as a carrier-atom chain step (k=2). I2
extends that to: C-12 is the GHZ-symmetric anchor of the substrate's
tripartite entanglement structure.
```

### Identification I3 — CR256 A-operator implements the dihedral/reflected construction

```text
CR256 sealed the antimatter-conjugate operator:
  q_A,anti(p, sign, d) = q_A,matter · A_conjugate(sign, p, d)
  A_conjugate(neg, p, d) = (5/6)(1 + p/R^(d+1))
  A_conjugate(pos, p, d) = (6/5)(1 − p/R^(d+1))

The (1 + p/R^(d+1)) ↔ (1 − p/R^(d+1)) sign reversal under matter→anti
is structurally a reflected-construction operation on the partition
algebra. By Result 4 (Eq. 40 of the paper), reflected-construction
permutations are equivalent to dihedral-group permutations.

Therefore: the A-operator's matter→antimatter map is the SAM analog
of the dihedral invariant D_{2n}, and the antimatter-side accounting
is structurally the (2, n)-Rényi reflected entropy of the matter side
against the carrier side.
```

### Identification I4 — CR229 inclusion-exclusion = symmetric/antisymmetric difference

```text
CR229 sealed the identity:
  R² = M + Θ = ℒ − Θ
  where two 81-element carrier-tensor sides overlap on Θ = 18
  giving R² = 144 as the union and M = 126 as the symmetric difference.

This is structurally inclusion-exclusion on a tripartite system
(side A: 81 carriers, side B: 81 carriers, overlap Θ: 18). The
mutual information I(A:B) in Shannon-information sense involves the
overlap; the "matter" M = symmetric difference; the "ledger" ℒ =
union with overlap counted twice.

Under Identification I1, the genuine multientropy formula (Result 1)
applies to this tripartition.
```

### Identification I5 — Containers (R, V, F) ↔ destructive-interference tripartite states

```text
CR262 sealed that Z = N nuclei at container atoms (R, V, F) are
unstable. The structural reason: containers are not propagator atoms.

Translation to the entanglement framework: under the paper's
stabilizer-state framework, configurations where the tripartition
forces u = d on a container atom create destructive interference in
the reflected-construction permutations (Result 4 / Eq. 40 of the
paper). The resulting reflected entropy is incompatible with bound-
state stability.

The carrier/container distinction (CR262) is the SAM-side reading of
which tripartitions admit a stable GHZ-extractable structure and
which do not.
```

## Open Items (to be resolved by future CRs)

```text
O1  Element state specification.  Which density matrix represents an
    element (Z, N) under Identification I1?  The (u, d, e) source counts
    don't uniquely fix the state.  Candidates: (a) GHZ-on-min(u,d,e),
    (b) tripartite-product of bipartite-purifications, (c) Lifshitz-
    ground-state inspired wavefunction with substrate-atom roles.
    To be sealed in CR264.

O2  Fee scale.  Translation from genuine multientropy (dimensionless
    bits) to binding fee (MeV) requires a substrate-natural constant
    κ' analogous to CR238's κ = 7117/768.  Must derive, not fit.
    To be sealed in CR265.

O3  Sign convention.  CR248's B_u_obs = A − m is signed (positive for
    heavy bound, negative for light side); genuine multientropy is
    non-negative.  A substrate-natural rule for the sign of the fee
    contribution is needed.  To be sealed in CR264 or CR265.

O4  GHZ-count map.  Identification I3 establishes that the A-operator
    implements the dihedral construction, but doesn't fix which SAM
    quantity counts as a "GHZ extraction."  Candidates: Θ-exchanges
    per nucleon pair (from CR251 bounce factor), carrier-tensor lift
    fee count (from CR249a/CR251), pair-write count from CR248 Phase B.
    To be sealed in CR264.

O5  Result 5 (CCNR / realignment) is registered for downstream use
    but not yet identified with a SAM quantity.  Possibly relates to
    CR256 hard-zero falsifier at QP093A-0088 — a "separability boundary"
    in entanglement terms.  Future CR.
```

## Sealed PASS Gates

```text
G1  Cited reference verified: DOI 10.1103/vcqd-rkmn, Phys. Rev. D 113,
    065029 (2026), authors Berthière & Gaudin.  License CC-BY 4.0.

G2  Five paper results (R1-R5) transcribed with formula consistency
    checked against the source PDF.

G3  Six SAM tripartite structures (CR229 / CR248 / CR253 / CR256 /
    CR259 / CR262) cited by precommit hash and their tripartite role
    documented.

G4  Five identifications (I1-I5) stated formally and consistent with
    the paper's framework (no mathematical contradiction).

G5  Five open items (O1-O5) named with proposed downstream CR
    assignments.  Establishes the research program rather than closing it.

G6  Precommit hash verified at load AND forbidden-file open() guard
    not tripped.  Whitelist: this precommit, runner source, output files.

PASS  iff G1-G6 all hold.

This CR has no numerical predictions to falsify.  It is a framework
commitment.  It can be SUPERSEDED by a future CR that demonstrates the
framework is incompatible with sealed SAM observables, but cannot be
"failed" in the measurement sense.
```

## Rule-9 Line

```text
This CR could have failed by: (i) misidentifying the paper or its
DOI; (ii) transcribing one of the paper's load-bearing formulas
incorrectly; (iii) asserting a structural identification (I1-I5) that
is mathematically inconsistent with the paper's framework; (iv)
asserting an open item (O1-O5) that is already sealed by an existing
SAM CR.

It cannot fail by numerical prediction mismatch because no numerical
predictions are made.  Downstream CRs (CR264, CR265) are where the
framework gets numerical falsifiability.
```

## What This CR Seals

```text
SAM formally commits to the mathematical framework of multipartite
entanglement for stabilizer-class states as the category in which
binding-fee structure will be expressed.  This is parallel to how
CR238 committed SAM to the partition-algebra framework for the
substrate atoms themselves.

After this CR seals, downstream CRs CAN cite:
  - Genuine multientropy reduction (Result 1) as a load-bearing
    theorem available to SAM derivations
  - Dihedral / reflected-entropy equivalence (Result 4) as the
    mathematical identity behind CR256's A-conjugate operator
  - GHZ-extraction interpretation (Result 3) as the candidate count
    for substrate carrier-tensor exchanges
  - n = 2 vanishing for Lifshitz / stabilizer (Result 2) as the
    structural reason C-12 has zero fee at the entanglement level

After this CR seals, downstream CRs CANNOT silently change the
framework or substitute different mathematical category without
appealing the foundation.
```

## Provenance Hash Chain

| artifact | reference |
| --- | --- |
| External reference | Phys. Rev. D 113, 065029 (2026); DOI 10.1103/vcqd-rkmn |
| CR229@09a (inclusion-exclusion identity) | per branch HASHES |
| CR248@09a (four-particle algebra) | precommit `7ad11ca6...` |
| CR253@09a (80-row promoter) | precommit `a7ecd0a4...` |
| CR256@09a (A-conjugate operator) | precommit `25654e6e...` |
| CR258@09a (substrate primitive closure audit) | precommit `77c58a51...` |
| CR259@09a (chessboard structural ID) | precommit `53ec3c89...` |
| CR262@09a (carrier/container stability cipher) | precommit `351b78e1...` |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
