# CR263 -- Genuine Multientropy / Dihedral-Invariant Framework Foundation -- RESULT

```text
verdict           : PASS
classification    : FRAMEWORK_FOUNDATION_CR
execution_status  : CLEAN
sealed_utc        : 2026-06-30
precommit_hash    : ab68c100fa7dd117dbd704d0d3b0cdeb7ec275ebbb931a8c145a4d5d8739d9b0
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
free_parameters_introduced : 0
prior_CR_result_inputs     : false
numerical_predictions_made : false
framework_commitment       : true
```

## Headline

SAM formally commits to the mathematical framework of **multipartite
entanglement for stabilizer-class states** as the category in which
binding-fee structure will be expressed. The external reference

> C. Berthière and P. Gaudin, "Genuine multientropy, dihedral
> invariants, and Lifshitz theory," Phys. Rev. D 113, 065029 (2026).
> DOI: 10.1103/vcqd-rkmn

is cited as the load-bearing prior art. Five of its results (R1–R5)
are transcribed into the SAM provenance chain; five structural
identifications (I1–I5) are made against SAM's already-sealed
tripartite structures (CR229, CR248, CR253, CR256, CR259, CR262);
five open items (O1–O5) are registered for downstream CR closure.

This CR makes **no numerical predictions** and **does not modify any
sealed SAM observable**. It is the framework commitment that downstream
binding-cipher CRs (CR264 element state specification, CR265 fee
derivation, ...) will operate within.

## Gate-by-gate

| gate | claim | result |
| --- | --- | :---: |
| G1 | Citation block verified (DOI, journal, authors, license) | PASS |
| G2 | Five load-bearing paper results transcribed | PASS |
| G3 | Six SAM tripartite structures registered with sealed CR provenance | PASS |
| G4 | Five structural identifications (I1–I5) stated | PASS |
| G5 | Five open items (O1–O5) registered for downstream CRs | PASS |
| G6 | Precommit hash verified + forbidden-file guard | PASS |

## Load-bearing paper results (transcribed for the record)

```text
R1  Genuine multientropy reduction (Eq. 23 of paper):
    G^(3)_n(A:B:C) = (2-n)/(2n) * [I_{1/2}(A:B) - 2*E(A:B)]
    for Lifshitz / stabilizer-class states.

R2  Vanishing at n=2 (Markov gap M_{2,2} = 0):
    G^(3)_2 = 0 for symmetric Lifshitz / stabilizer tripartitions.

R3  GHZ-extraction interpretation:
    (I_{1/2} - 2*E) counts GHZ states extractable from the stabilizer.

R4  Dihedral / reflected-entropy equivalence (Eq. 40):
    D_{2n}(A:B) = S^R_{2,n}(A:C)
    with explicit isomorphism (Eq. 38).

R5  CCNR / realignment connection (Eq. 41):
    log Z_{2n} = E^CCNR_n(A:C); unnormalized dihedral = Rényi CCNR
    negativity of realignment of reduced density matrices.
```

## SAM tripartite structures registered

| ref | sealed in | structure |
| --- | --- | --- |
| CR229 inclusion-exclusion identity | CR229@09a | Two 81-element carrier-tensor sides ∩ Θ=18 overlap; R² = M + Θ = ℒ − Θ |
| CR248 source channels | CR248@09a | (u, d, e) = (2Z+N, Z+2N, Z) |
| CR253 promoter classes | CR253@09a | 80 = 32 charged matter + 16 neutral matter + 32 antimatter |
| CR256 A-conjugate operator | CR256@09a | (5/6)(1+p/R^(d+1)) / (6/5)(1−p/R^(d+1)) |
| CR259 chessboard | CR259@09a | T13 × T13 = 169 lattice |
| CR262 carrier/container cipher | CR262@09a | {m₃, D², Θ, ĥV} vs {R, V, F} |

## Structural identifications (locked)

```text
I1  Substrate states are stabilizer-class. Partition algebra ĥ^i·d̂^j
    closes as a discrete group on integer occupation states.
    → Paper Result 1 (Eq. 23) applies to SAM tripartitions.

I2  C-12 is the substrate's GHZ-symmetric anchor.
    (u, d, e) = (Θ, Θ, m₃) = (18, 18, 6); u = d exactly.
    → G^(3)_2(C-12) = 0 by Result 2.
    → m(C-12) = 12 has no entanglement-fee contribution.

I3  CR256 A-operator implements the dihedral / reflected construction.
    Sign flip on (1 ± p/R^(d+1)) is a reflected-construction operation.
    → By Result 4 (Eq. 40), this equals dihedral-group action.
    → Matter↔antimatter map = SAM analog of dihedral invariant D_{2n}.

I4  CR229 inclusion-exclusion is tripartite in the paper's sense.
    Two 81-element sides + 18-element overlap = standard tripartition.
    → Genuine multientropy at n=2 of this tripartition vanishes (Result 2).

I5  Containers force destructive interference in reflected construction.
    CR262 carrier/container distinction = stabilizer-state GHZ extraction
    boundary. Containers admit no stable extraction; carriers do.
```

## Open items registered (downstream)

```text
O1  Element state specification           → CR264
O2  Fee-scale constant (MeV per bit)     → CR265
O3  Sign convention for signed fee        → CR264 or CR265
O4  GHZ-count ↔ substrate quantity map    → CR264
O5  CCNR / realignment SAM identification → future CR
```

## Verdict statement

CR263 PASS. SAM commits to the multipartite-entanglement-of-stabilizer-
states framework, with Berthière & Gaudin (Phys. Rev. D 113, 065029,
2026) as the load-bearing citation. Five paper results are now
available to downstream SAM derivations under the provenance chain;
five structural identifications connect SAM's sealed tripartite
structures to the paper's mathematical objects; five open items are
explicit work targets for CR264 / CR265 and future CRs.

After this CR seals, downstream CRs CAN cite the paper's theorems by
hash provenance and cannot silently change the framework without
appealing the foundation.

`CR263_PASS_GENUINE_MULTIENTROPY_DIHEDRAL_INVARIANT_FRAMEWORK_FOUNDATION_CITATION_LOCKED_FIVE_RESULTS_TRANSCRIBED_SIX_SAM_TRIPARTITIONS_REGISTERED_FIVE_IDENTIFICATIONS_STATED_FIVE_OPEN_ITEMS_ASSIGNED_TO_CR264_CR265_FUTURE_NUMERICAL_FALSIFIABILITY_DEFERRED_TO_DOWNSTREAM_BINDING_CIPHER_CRS`
