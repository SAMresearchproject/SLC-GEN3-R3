# CR264 — Element State Specification (Lifshitz-RK Substrate Tripartite State)

**Branch:** 09a_PARTICLE_MASS_CHAIN
**Classification:** STRUCTURAL_PREDICTION_CR (downstream of CR263 framework foundation)
**Sealed by:** Sean Brady, 2026-06-30
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Test Type

```text
Structural commitment + verification CR. Picks the specific state
model for SAM elements under the framework sealed in CR263, makes the
GHZ-count map explicit, and verifies the formula gives substrate-
natural results for three anchor cases (C-12, He-4, Au-197). No
catalog data, no fit, no measurement-vs-prediction.

This CR closes CR263's open item O1 (element state specification) and
partially closes O4 (GHZ-count map). Sign convention (O3) and fee
scale (O2) remain deferred to CR265.

After this CR seals: downstream CRs CAN compute genuine multientropy
for any (Z, N) by direct substitution into the Lifshitz formula
sealed here. The fee scale (CR265) is the only remaining unknown
between substrate counts and predicted binding contribution.
```

## Question

```text
Under the framework sealed in CR263, what density-matrix / wavefunction
representation should be used for an element with source counts
(u, d, e) = (2Z+N, Z+2N, Z)?  And does the natural choice — a Lifshitz-
Rokhsar-Kivelson ground state on a tripartite graph with subsystem
lengths set by the source counts — give substrate-natural multientropy
values for the C-12 anchor, the He-4 chain-step anchor, and a heavy
test case (Au-197)?
```

## Locked State Model

```text
For every element (Z, N), the SAM substrate state is the Lifshitz-RK
ground state on a tripartite graph (A, B, C) with subsystem lengths
set by the CR248 source-channel counts:

  ℓ_A = u_count = 2Z + N        (u-channel)
  ℓ_B = d_count = Z + 2N        (d-channel)
  ℓ_C = e_count = Z             (e-channel; the binding-glue channel)

Total length:
  ℓ = ℓ_A + ℓ_B + ℓ_C = (2Z+N) + (Z+2N) + Z = 4Z + 3N

The graph topology is "disjoint A and B with C between" — corresponding
to the periodic / interval Lifshitz configuration of Fig. 1(a) of the
cited paper (Berthière-Gaudin 2026; CR263 framework).  This topology is
the natural reading of CR248's four-particle algebra: u and d are the
"quark sides"; e is the electron channel that mediates between them
through atomic binding.

The Lifshitz mass parameter ω is left as an open structural parameter
for CR265; the precommit-ready formulas are written in both massive
(ω > 0) and massless (ω → 0) limits.
```

## Locked GHZ-Count Map (O4 partial)

```text
The GHZ extraction count for an element is

  G_count(Z, N) = min(ℓ_A, ℓ_B, ℓ_C)

For typical elements where Z ≤ N (the stable region of the chart):
  min(2Z+N, Z+2N, Z) = Z

i.e., the GHZ count equals the electron count = atomic number Z.
This is structurally cohesive: each electron mediates one tripartite
GHZ extraction across (u-source, d-source, e-channel).

For exotic regions with Z > N:
  min(2Z+N, Z+2N, Z) = depends on N vs Z relationship.
  Typically still min(...) = Z if N > 0.

For neutron-only states (hypothetical, Z = 0):
  min(N, 2N, 0) = 0  →  no GHZ extractions  →  no binding fee.
```

## Locked Multientropy Formulas (from paper Eq. 16 / Eq. 17)

```text
GENERAL FORM (massive Lifshitz, ω > 0):

  G^(3)_n(A:B:C) = (2-n)/(4n) · log[ sinh(ωℓ_AC) · sinh(ωℓ_BC)
                                     / (sinh(ωℓ_C) · sinh(ωℓ)) ]

where ℓ_AC = ℓ_A + ℓ_C, ℓ_BC = ℓ_B + ℓ_C, etc.

MASSLESS LIMIT (Lifshitz critical, ω → 0):

  G^(3)_n(A:B:C) = (2-n)/(4n) · log[ ℓ_AC · ℓ_BC / (ℓ_C · ℓ) ]

For SAM elements in the massless limit, substituting the source counts:

  ℓ_AC = (2Z+N) + Z = 3Z + N
  ℓ_BC = (Z+2N) + Z = 2Z + 2N = 2A
  ℓ_C  = Z
  ℓ    = 4Z + 3N

  G^(3)_n(Z, N) = (2-n)/(4n) · log[ (3Z+N) · 2A / (Z · (4Z+3N)) ]
```

## Sealed Vanishing at n = 2 (paper R2)

```text
The (2-n)/(4n) prefactor evaluates to ZERO at n = 2.

Therefore, for EVERY element (Z, N):
  G^(3)_2(Z, N) = 0

This is the structural meaning of "Markov gap M_{2,2} vanishes for
Lifshitz ground states" sealed in CR263 as Result R2: the genuine
multipartite entanglement at the Rényi-2 level vanishes for the
substrate's stabilizer-class state.

Element-specific discrimination happens at n ≠ 2, with n = 1 (von
Neumann entropy limit) the natural physical choice.
```

## Sealed n = 1 (von Neumann) Anchor Values

```text
At n = 1, the prefactor (2-n)/(4n) = 1/4.  The genuine multientropy is
the dimensionless quantity

  G^(3)_1(Z, N) = (1/4) · log[ (3Z+N) · 2A / (Z · (4Z+3N)) ]

For three anchor cases (massless limit; substrate-natural integer
arithmetic):

  C-12  (Z=6, N=6, A=12):
    (3Z+N) · 2A / (Z · (4Z+3N)) = (24 · 24) / (6 · 42) = 576/252 = 16/7
    G^(3)_1(C-12) = (1/4) · log(16/7) ≈ 0.20665 (dimensionless)

  He-4  (Z=2, N=2, A=4):
    (3Z+N) · 2A / (Z · (4Z+3N)) = (8 · 8) / (2 · 14) = 64/28 = 16/7
    G^(3)_1(He-4) = (1/4) · log(16/7) ≈ 0.20665 (dimensionless; same as C-12)

  Au-197 (Z=79, N=118, A=197):
    (3Z+N) · 2A / (Z · (4Z+3N)) = (355 · 394) / (79 · 670)
                                = 139870 / 52930 = 13987/5293
                                = (71·197) / (67·79)
    G^(3)_1(Au-197) = (1/4) · log(13987/5293) ≈ 0.24308 (dimensionless)
```

## Structural Finding (sealed for downstream)

```text
G^(3)_1(C-12) = G^(3)_1(He-4) = (1/4)·log(16/7) exactly.

The dimensionless genuine multientropy is identical for any element
satisfying Z = N (balanced).  This is the "chain-step degeneracy" of
the source-channel topology:

  For Z = N:  (3Z+N)·2A / (Z·(4Z+3N)) = (4Z · 4Z) / (Z · 7Z) = 16/7
  So  G^(3)_1 = (1/4) · log(16/7) ≈ 0.20665
  identical for all Z = N elements regardless of chain step.

Consequence: the dimensionless multientropy bits ARE the same for
He-4 and C-12 (~0.207 bits).  The mass-excess difference between He-4
(-2.4 MeV) and C-12 (0 MeV exact) MUST then come from the FEE SCALE
factor (CR265) — not from the dimensionless count.

This is a structural fingerprint that constrains CR265's scale
derivation: it must be Z-dependent or A-dependent (so He-4 and C-12
have different scales), not multientropy-dependent (same bits → same
scale would predict same fee, contradicting observation).

Specifically: scale factor κ'(Z, A) must satisfy
  κ'(He-4) × 0.20665 = -2.42 MeV  →  κ'(He-4) ≈ -11.71 MeV/bit
  κ'(C-12) × 0.20665 = 0 MeV      →  κ'(C-12) = 0 exactly

So κ' has a structural zero at C-12 (consistent with C-12 = atomic
mass anchor by definition).  This is a sealed boundary condition for
CR265's scale derivation.
```

## Pre-Registered Predictions

### H1 — n=2 vanishing holds for every element

For every (Z, N) with Z ≥ 1 and N ≥ 0: `G^(3)_2(Z, N) = 0` exactly,
by the (2-n)/(4n) prefactor.

### H2 — n=1 anchor values match the sealed integer arithmetic

```text
G^(3)_1(C-12)  = (1/4) · log(16/7)                ≈ 0.20665
G^(3)_1(He-4)  = (1/4) · log(16/7)                ≈ 0.20665
G^(3)_1(Au-197) = (1/4) · log(13987/5293)         ≈ 0.24308
```

### H3 — Chain-step degeneracy: Z = N elements give identical dimensionless multientropy

```text
For any Z = N element: G^(3)_1 = (1/4) · log(16/7) regardless of Z.
This is checkable on Li-6, Be-8 (unstable but well-defined),
N-14, O-16, Ne-20, Mg-24, etc.
```

### H4 — Au-197 dimensionless multientropy > C-12 by ~17.6%

```text
G^(3)_1(Au-197) / G^(3)_1(C-12) = log(13987/5293) / log(16/7)
                                 = log(2.6424) / log(2.2857)
                                 ≈ 1.176
17.6% more multientropy bits for Au-197 than C-12.
```

## Sealed PASS Gates

```text
G1  State model formula transcribed correctly: ℓ_A=u, ℓ_B=d, ℓ_C=e
    with disjoint-A-B-C-between topology (paper Fig. 1(a)).

G2  GHZ-count formula: G_count = min(ℓ_A, ℓ_B, ℓ_C) = Z for
    Z ≤ N regime.

G3  H1: G^(3)_2 = 0 verified for C-12, He-4, Au-197 via prefactor.

G4  H2 anchor values: C-12 = He-4 = (1/4)·log(16/7) ≈ 0.20665 and
    Au-197 = (1/4)·log(13987/5293) ≈ 0.24308 verified at exact Fraction
    precision.

G5  H3 chain-step degeneracy: every Z=N element gives same
    dimensionless multientropy at n=1.  Verified for {Z=N=1, 2, 3,
    4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20}.

G6  H4 Au/C-12 ratio: G^(3)_1(Au-197) / G^(3)_1(C-12) within 1e-6
    of log(13987/5293)/log(16/7) ≈ 1.176.

G7  Open items registered: O1 closed by this CR; O3 (sign) and O2
    (scale) explicitly assigned to CR265; structural constraint κ'(C-12)
    = 0 sealed as a boundary condition for CR265.

G8  Precommit hash verified at load AND forbidden-file open() guard
    not tripped.

PASS  iff G1-G8 all hold.

BOUNDARY  iff G1-G5 hold but the H4 ratio differs from the locked
          value by more than floating-point precision (would indicate
          formula transcription error).

FAIL  iff G3 fails (n=2 prefactor mistake), or G4 anchor values miss,
      or G7 mis-assigns an open item that's already sealed.
```

## Reported Evidence (not gated)

```text
E1  Tabulate G^(3)_1 for Z=1..20 stable elements (using most-abundant
    isotope where ambiguous) to surface any additional structural
    patterns.

E2  Z = N row dimensionless multientropy: all equal to (1/4)·log(8/3).
    Variation with Z=N must therefore live in CR265's fee scale.

E3  N = Z + 1 (just-asymmetric) dimensionless multientropy: how it
    grows as A → ∞ (asymptotic structure for heavy nuclei).

E4  Identify any element where (3Z+N) hits a sealed substrate atom
    (carrier or container).  These are candidates for special
    structural treatment in CR265.
```

## Pre-Registered Frozen Inputs

This CR has NO external input files.  All computations are pure
substrate-atom integer arithmetic.  The runner verifies the locked
formulas symbolically using Fraction arithmetic, with no I/O beyond
its own output artifacts and this precommit.

## Rule-9 Line

```text
This test could have falsified the claim that the Lifshitz-RK
ground-state model with subsystem lengths set by CR248 source counts
gives substrate-natural genuine multientropy values for SAM elements,
by:
  (i) the (2-n)/(4n) prefactor failing to give G^(3)_2 = 0 for any
      tested element;
  (ii) the n=1 anchor values for C-12, He-4, Au-197 not matching
       the exact Fraction values (1/4)·log(16/7), (1/4)·log(16/7),
       (1/4)·log(13987/5293);
  (iii) the chain-step degeneracy (all Z=N elements give identical
        dimensionless multientropy) failing for any tested Z=N
        element.
```

## What This CR Seals

```text
The Lifshitz-RK ground-state model is committed as the SAM element
state representation.  Source-channel lengths (u, d, e) become Lifshitz
subsystem lengths.  The genuine multientropy formula becomes computable
for any (Z, N) by integer arithmetic.

CR263 open item O1 closes.  Open items O3 (sign), O2 (scale) defer to
CR265 with the new structural constraint κ'(C-12) = 0 as a boundary
condition for the scale derivation.

Structural finding sealed: chain-step degeneracy at n=1 forces CR265's
fee scale to be Z- or A-dependent, NOT multientropy-dependent.  This
is a substantive constraint on CR265.
```

## Provenance Hash Chain

| artifact | reference |
| --- | --- |
| External reference (framework) | CR263@09a precommit `ab68c100fa7dd117dbd704d0d3b0cdeb7ec275ebbb931a8c145a4d5d8739d9b0` |
| Paper cited | Phys. Rev. D 113, 065029 (2026); DOI 10.1103/vcqd-rkmn |
| CR248@09a (source-count identities) | precommit `7ad11ca6...` |
| CR262@09a (carrier/container cipher) | precommit `351b78e1...` |
| CR263@09a (framework foundation) | precommit `ab68c100...` |
| stewardship declaration | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
