# Exact source operators and exchange in R4

Eight operations run in the shared warm C++/GMP worker. Python admits metadata,
routes calls and retains authenticated records in the existing unified checkpoint.
GEN3 operation names work through each active CE domain. `ATOM3D_` aliases replace
`GEN3_` for ATOM3D only. All arithmetic is exact over Q or a declared real quadratic
field Q(sqrt(D)); there is no fitted physical scale or numerical root finder.

Every computational request has exactly `name`, `source_binding`, `context`,
`data`. Names are immutable within the source record namespace. Context contains
`basis` (1–64 distinct integer/string identities), `field: {radicand: D}` (0 for Q,
otherwise a positive nonsquare integer 2–1000000), nonempty `units` and `history`
objects, and a `spectral_coordinate` string. These describe the source and remain
attached to the output; the worker does not infer units or reconstruct source
history from the matrix. Rational scalars are integers or rational strings;
quadratic scalars are `{a: rational, b: rational}` meaning a+b sqrt(D). Floats
are rejected. All source matrices have at most64 rows/columns.

| Operation | `data` and result |
|---|---|
| `GEN3_SOURCE_OPERATOR_WORD` | `operators`, ordered `program`, `output`; exact matrix, rank and program. Steps have immutable `name`, `op`, and `inputs`; identity instead has `dimension`; scale additionally has `factor`. Operations: identity, multiply, add, columns, scale, transpose, subtract, tensor, commutator. At most64 initial matrices/256 steps. Tensor order is left factor then right factor. |
| `GEN3_SOURCE_SUBSPACE` | Exact self-adjoint `H`, `seeds`, `mode: ADMIT` or `CLOSURE`; optional `reference` and `reference_energy` together. Returns an independent basis W, Gram G, compressed H=G^-1 W^T H W, full-source residual, rank, growth and nonleaking coefficient kernel. CLOSURE repeatedly includes H W. |
| `GEN3_NATIVE_PAIR_ROOTS` | `H`, four-column `frame`, `parameters: {mu,a,b,c,g,offset}`. Validates the full-source quartet action and common orthogonal frame norm. Returns exact pair and reciprocal-root polynomial relations, energy formula and singular-chart flags. |
| `GEN3_BLOCK_SOURCE_RECURRENCE` | `H`, independent `seeds` of width1–8, optional `max_levels`1–64. Returns Q/G/A/B blocks, ascending matrix polynomials, retained terminal, closed flag and dimension. Budget exhaustion or partial block breakdown is explicit and does not silently deflate channels. |
| `GEN3_SOURCE_SPECTRAL_CREATION` | Closed `recurrence`, optional `reference`/`reference_energy` together and `x`. Returns ascending coefficients C, terminal factor, normalization and optional evaluation. Eigenstate reference is checked exactly. |
| `GEN3_SOURCE_WORD_EXCHANGE` | `mode: LIFT_RANK`, `lift`, `u`, `v`, `primes`, optional Boolean `include_terminal`/`on_reference`; or `mode: CONSTANT_EXCHANGE`, polynomial `family`, supplied `R`. The first returns reproducible minor certificates; the second returns coefficientwise exchange, braid and reversal residuals. |
| `GEN3_SOURCE_TERMINAL_ACTION` | `lift`, independent H-invariant `frame`, `mode: EXACT_ACTION` or `MODULAR_ACTION` (latter requires `primes`). Exact mode returns stacked terminal action, exact kernel, transported kernel and ranks. Modular mode returns rank lower-bound certificates and the column upper bound. |
| `GEN3_SOURCE_SPECTRAL_EXPORT` | Top-level `name`, `source_binding` only. Exports retained record, digest and `recomputed: false`. Recovery performs zero native arithmetic. |

A `recurrence` is either the explicit native recurrence result or
`{record: name}`. Retained dependencies authenticate the original source binding,
basis and field, record the dependency digest, and are revalidated algebraically.
All original input, context, dependency hashes and native manifest identity remain
in `GEN3_SOURCE_OPERATOR_RECORD_V1` records.

For the pair frame ordered --,-+,+-,++, let delta=(a-b)/2 and J=(a+b)/2.
The quartet exchange block has diagonal mu+J-2c, mu-J, mu-J, mu+J+2c;
corner entries delta and central off-diagonal entries -delta.
H frame = frame [offset I+g block] is checked on the entire supplied source.
The exact collective pair relation is delta z²-4cz-delta=0;
E=offset+g(mu+J-2c+delta z). In the g*c nonzero chart, the reciprocal
roots have product1, sum s satisfying c s²+2delta s-4c=0, and each root
satisfies c x⁴+2delta x³-2c x²+2delta x+c=0. The collective z and reciprocal
root x are distinct coordinates. Polynomial relations are retained even in singular
charts, whose flags govern the interpretation; no numerical roots are returned.

The block recurrence is H Qn=Q(n+1)+Qn An+Q(n-1)Bn, Gn=Qn^T Qn.
F0=I and F(n+1)=(xI-An^T)Fn-Bn^T F(n-1). Creation is
C(x)=sum Qn Gn^-1 Fn(x), with Q0^T C=I and
(H-x)C=-Qlast Glast^-1 Fterminal. Every coefficient is checked exactly.
The dimension reported by a partial recurrence counts its complete retained blocks.

A `lift` supplies `recurrence`, square `seed_operators`, nonzero `reference`, and
`action: LEFT` or `COMMUTATOR_REFERENCE`. The second requires `reference_energy`;
H reference=Eref reference and Sa reference=Q0[:,a] are exact admission conditions.
LEFT acts by H L; COMMUTATOR_REFERENCE acts by H L-L H+Eref L. Thus the latter
uses the excitation coordinate omega=x-Eref and retains the exact identity

```
[H,B(x)]-(x-Eref)B(x)
 = Lterminal Glast^-1 Flast(x) - Llast Glast^-1 Fterminal(x).
```

Lterminal annihilates the reference but can act on excited states. Adding terminal
channels retains those operators as additional constant polynomial channels.
LIFT_RANK admits up to8 total channels and1–4 primes3..10000019. For quadratic
fields this implementation requires a prime congruent3 modulo4 with an admitted
sqrt(D) embedding; denominators must survive reduction. A nonzero minor gives a
rigorous characteristic-zero rank lower bound. A combined forward/reverse rank
above the reverse-family column upper bound returns NONCLOSURE_CERTIFIED. Otherwise
the result is MODULAR_TEST_INCONCLUSIVE; equal modular ranks do not establish closure.
At a regular sampled (u,v), such a nonzero polynomial minor also certifies generic
nonclosure for the specified polynomial lift.

CONSTANT_EXCHANGE admits1–4 equal-degree polynomial families and a supplied
k² by k² matrix R, using
Ba(u)Bb(v)=sum R[ab,cd] Bc(v)Bd(u). It checks all coefficient pairs and returns
the braid residual R12 R23 R12-R23 R12 R23 and reversal residual R²-I separately.
It verifies a proposed constant law; it does not solve a spectral-parameter-dependent
R matrix. A positive noncommuting Pauli fixture exercises all three identities.

The installed Li-6 fixture uses x=64E and the exact eigenstate
|-->+(sqrt(5)-2)|++>, Eref=15408-64sqrt(5) for H64. It retains the source's33-dimensional
complement and11-level,3-channel recurrence. Three-channel exchange ranks are9/18;
adding three terminal channels gives18/36. The commutator terminal action has exact
rank33, certified by a33-column upper bound and nonzero33-minors at two primes.
The reference is an eigenstate of the protected quartet, not the full-source groundstate;
signed excitation shifts are retained. These tested compact exchange families fail
closure. General native factorized scattering remains an open research question.
