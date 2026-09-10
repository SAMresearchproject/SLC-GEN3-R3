# SLCV002C4N72I01 post-run audit

Audit status: **PASS**

The fresh `SLCV002C4_N72_I01` holdout was generated and frozen before its
graph was opened. The unchanged `SLC_DENSE_EXACT_V0_2` portfolio selected
induced width 24, and its four-SLC capacity-26 plan was sealed in commit
`a9050754` before any DOS execution.

The post-run audit independently recomputed and checked:

- the result, candidate, instance, plan, checkpoint, step-roster, chain, and
  chain-link self-seals;
- 768/768 node checkpoints;
- 55,296/55,296 elimination-step receipts;
- 192/192 four-node wave chains and 768/768 chain links;
- exact root coverage `0..1023` once for each of all three primes;
- all DOS counts as nonnegative exact integers;
- configuration-count equality to `2^72`;
- energy parity, support, and the frozen energy bound;
- raw moments one through four against the independently derived values.

The result contains 272 occupied energy bins, from energy -275 through +267.
The ground-state degeneracy is 7. All frozen internal exact checks pass.

Execution was clean: 768 tasks executed, no checkpoints reused, no retry,
fallback, refit, same-run repair, or answer-dependent order selection. Wall
time was 2,825.225 seconds and peak sampled aggregate worker RSS was
7,812,272,128 bytes (7.276 GiB).

The result file SHA-256 is
`6823607b07a9d36e9303e3c797c428be65b6913a7d72f8913e598d0e55875c43`;
its self-seal is
`ecd396f0b2fdfdb93e1a062ad0d385e04acc09de0a29dfa59711d7cb0eb7ee48`.

This is a prospective no-refit exact-invariant holdout PASS for one N72
instance. It is not an independent implementation comparison, a
distributed-hardware result, a quantum claim, or a generic N72 guarantee.
