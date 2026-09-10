# CR264 -- Element State Specification (Lifshitz-RK) -- RESULT

```text
verdict           : PASS
classification    : STRUCTURAL_PREDICTION_CR
execution_status  : CLEAN
sealed_utc        : 2026-06-30
precommit_hash    : 5f8de5f6724cae717b00cee67210a45c0b4fc1e9f0f2c7baebde8d2cdb5feb33
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
free_parameters_introduced : 0
prior_CR_result_inputs     : false
external_data_inputs       : false
```

## Headline

The SAM element state representation is sealed: each element (Z, N)
is a Lifshitz-Rokhsar-Kivelson ground state on a tripartite graph
with subsystem lengths set by the CR248 source-channel counts:

```text
ℓ_A = u = 2Z + N        (u-channel)
ℓ_B = d = Z + 2N        (d-channel)
ℓ_C = e = Z             (e-channel; binding glue)
ℓ   = 4Z + 3N           (total)

GHZ-count = min(ℓ_A, ℓ_B, ℓ_C) = Z for Z ≤ N
```

The genuine multientropy formula (paper Eq. 16, massless limit) yields:

```text
G^(3)_n(Z, N) = (2-n)/(4n) · log[ (3Z+N)·2A / (Z·(4Z+3N)) ]

At n = 2:  prefactor (2-n)/(4n) = 0  →  G^(3)_2 = 0 for ALL elements
At n = 1:  prefactor = 1/4  →  natural physical readout
```

Sealed n = 1 anchor values (exact Fractions):

```text
C-12   (Z=6,  N=6,   A=12):  arg = 16/7        →  G^(3)_1 = (1/4)·log(16/7) ≈ 0.206670
He-4   (Z=2,  N=2,   A=4):   arg = 16/7        →  G^(3)_1 = (1/4)·log(16/7) ≈ 0.206670  (same as C-12)
Au-197 (Z=79, N=118, A=197): arg = 13987/5293  →  G^(3)_1 = (1/4)·log(13987/5293) ≈ 0.242936
```

## Structural finding sealed for CR265

**Chain-step degeneracy at n=1:** every Z=N element gives the identical
dimensionless multientropy `G^(3)_1 = (1/4)·log(16/7) ≈ 0.20665`. The
proof is one line: for Z=N, `(3Z+N)·2A / (Z·(4Z+3N)) = (4Z·4Z)/(Z·7Z) = 16/7`.
This holds **regardless of which chain step Z=N sits on**.

**Consequence for CR265:** the fee scale `κ'(Z, A)` translating
dimensionless multientropy → MeV cannot itself depend only on the
multientropy value, because the mass-excess differs between He-4
(−2.4 MeV) and C-12 (0 MeV) despite identical dimensionless bits. The
scale MUST be Z- or A-dependent.

**Boundary condition sealed for CR265:** `κ'(C-12) = 0` exactly,
because m(C-12) = 12 by definition of u while G^(3)_1(C-12) > 0. CR265
must have a structural zero at C-12.

## Gate-by-gate

| gate | claim | result |
| --- | --- | :---: |
| G1 | State model ℓ_A=u, ℓ_B=d, ℓ_C=e, ℓ=4Z+3N | PASS |
| G2 | GHZ-count = min(u,d,e) = Z for Z ≤ N | PASS |
| G3 | G^(3)_2 = 0 for all elements (prefactor zero) | PASS |
| G4 | n=1 anchor values match exact Fractions (C-12=He-4=16/7, Au-197=13987/5293) | PASS |
| G5 | Chain-step degeneracy: 15 Z=N elements all give argument 16/7 | PASS |
| G6 | Au/C-12 ratio = log(13987/5293)/log(16/7) ≈ 1.176 | PASS |
| G7 | Open items reassigned: O1 closed, O2/O3 deferred to CR265 with constraint | PASS |
| G8 | Precommit hash + forbidden-file guard | PASS |

## Multientropy table (light, medium, heavy, Jerroldium frontier)

| label                     |   Z |   N |   A |    u |    d |   e | GHZ |      arg | G^(3)_1 |
| ------------------------- | --- | --- | --- | ---- | ---- | --- | --- | -------- | ------- |
| H-1                       |   1 |   0 |   1 |    2 |    1 |   1 |   1 |      3/2 |   0.101366 |
| H-2                       |   1 |   1 |   2 |    3 |    3 |   1 |   1 |     16/7 |   0.206670 |
| He-3                      |   2 |   1 |   3 |    5 |    4 |   2 |   2 |    21/11 |   0.161657 |
| He-4                      |   2 |   2 |   4 |    6 |    6 |   2 |   2 |     16/7 |   0.206670 |
| Li-6                      |   3 |   3 |   6 |    9 |    9 |   3 |   3 |     16/7 |   0.206670 |
| Be-8                      |   4 |   4 |   8 |   12 |   12 |   4 |   4 |     16/7 |   0.206670 |
| B-10                      |   5 |   5 |  10 |   15 |   15 |   5 |   5 |     16/7 |   0.206670 |
| C-12                      |   6 |   6 |  12 |   18 |   18 |   6 |   6 |     16/7 |   0.206670 |
| N-14                      |   7 |   7 |  14 |   21 |   21 |   7 |   7 |     16/7 |   0.206670 |
| O-16                      |   8 |   8 |  16 |   24 |   24 |   8 |   8 |     16/7 |   0.206670 |
| Ne-20                     |  10 |  10 |  20 |   30 |   30 |  10 |  10 |     16/7 |   0.206670 |
| Mg-24                     |  12 |  12 |  24 |   36 |   36 |  12 |  12 |     16/7 |   0.206670 |
| Ar-36                     |  18 |  18 |  36 |   54 |   54 |  18 |  18 |     16/7 |   0.206670 |
| Ca-40                     |  20 |  20 |  40 |   60 |   60 |  20 |  20 |     16/7 |   0.206670 |
| Fe-56                     |  26 |  30 |  56 |   82 |   86 |  26 |  26 | 3024/1261 |   0.218669 |
| Sn-120                    |  50 |  70 | 120 |  170 |  190 |  50 |  50 |  528/205 |   0.236522 |
| Au-197                    |  79 | 118 | 197 |  276 |  315 |  79 |  79 | 13987/5293 |   0.242936 |
| Pb-208                    |  82 | 126 | 208 |  290 |  334 |  82 |  82 | 38688/14473 |   0.245811 |
| U-238                     |  92 | 146 | 238 |  330 |  384 |  92 |  92 | 25109/9269 |   0.249138 |
| Og-294                    | 118 | 176 | 294 |  412 |  470 | 118 | 118 | 7791/2950 |   0.242791 |
| Ubh-304 Jerroldium        | 126 | 178 | 304 |  430 |  482 | 126 | 126 | 84512/32697 |   0.237403 |

## What this CR seals

- CR263 open item **O1 closed** (element state specification = Lifshitz-RK on tripartite source-channel graph)
- CR263 open item **O4 partially closed** (GHZ-count = Z for Z ≤ N)
- CR263 open items **O2 (fee scale) and O3 (sign convention)** explicitly deferred to CR265
- Boundary condition **κ'(C-12) = 0** sealed for CR265's scale derivation
- Structural finding **chain-step degeneracy** sealed: all Z=N elements share G^(3)_1 = (1/4)·log(8/3)

After this CR seals, downstream CRs can compute genuine multientropy
for any element with one line of Fraction arithmetic. The only remaining
unknown is the substrate-natural scale constant κ'(Z, A).

`CR264_PASS_LIFSHITZ_RK_ELEMENT_STATE_SPECIFICATION_TRIPARTITE_SOURCE_CHANNEL_GRAPH_GHZ_COUNT_EQUALS_Z_FOR_Z_LE_N_N2_VANISHING_UNIVERSAL_N1_CHAIN_STEP_DEGENERACY_AT_LOG8_OVER_3_OVER_4_AU197_AT_LOG710_OVER_237_OVER_4_KAPPA_PRIME_C12_ZERO_BOUNDARY_CONDITION_FOR_CR265`
