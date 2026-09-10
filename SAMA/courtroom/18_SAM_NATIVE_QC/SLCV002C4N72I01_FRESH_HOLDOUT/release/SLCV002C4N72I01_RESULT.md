# Four-SLC Dense Exact v0.2 fresh N72 I01 holdout

Execution status: **CLEAN**

Scientific verdict: **PASS_NO_REFIT_EXACT_HOLDOUT**

## Prospective boundary

- Instance: `SLCV002C4_N72_I01`
- Instance SHA-256: `c6ceaf264c91794eef957647af71fa7f4cc03189d6a5fa46e08f43adbaae9b3c`
- Generator candidate index: **14654**
- Generator rule: **first structurally accepted candidate**
- Width-22 filtering: **none**
- DOS/runtime screening: **none**
- v0.2 refit after I00: **none**

## Exact result

- Portfolio-selected policy: `historical_min_degree`
- Induced graph width: **24**
- Per-SLC retained-batch capacity: **2^26 entries**
- Root shard: **4 roots per node task**
- Cluster: **4 persistent local SLC workers**
- Node checkpoints: **768/768**
- Four-node wave chains: **192/192**
- Configuration count: **4722366482869645213696 = 2^72**
- Occupied energy bins: **272**
- Internal exact verification: **PASS**
- Cluster wall time this invocation: **2825.225 s**
- Peak sampled aggregate worker RSS: **7.276 GiB**
- Executed node tasks: **768**
- Reused sealed node checkpoints: **0**

The graph width and capacity exponent name different quantities.
Here each node batch retains `4 x 2^24 = 67108864` entries.

## Claim ceiling

This is a clean no-refit exact-invariant PASS for one prospectively
generated N72 I01 instance on the local four-SLC v0.2 capacity-26
software profile. No independent reference implementation was run,
so this is not an independent coefficient-comparison claim, a
distributed-hardware result, a quantum claim, or a generic N72
guarantee.
