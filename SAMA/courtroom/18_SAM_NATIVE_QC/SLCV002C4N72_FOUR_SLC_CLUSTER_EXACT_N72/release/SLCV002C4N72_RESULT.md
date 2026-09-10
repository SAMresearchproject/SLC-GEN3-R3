# Four-SLC Dense Exact v0.2 N72 result

Execution status: **CLEAN**

Scientific verdict: **PASS**

## Exact result

- Instance: `SLCX025_N72_I00`
- Induced graph width: **22**
- Per-SLC retained-batch capacity: **2^26 entries**
- Root shard: **16 roots per node task**
- Cluster: **4 persistent local SLC workers**
- Node checkpoints: **192/192**
- Four-node wave chains: **48/48**
- Full 871-coefficient equality: **True**
- Configuration count: **4722366482869645213696 = 2^72**
- Cluster wall time: **1398.647 s**
- Historical fused-primary wall ratio: **6.107x**
- Peak sampled aggregate worker RSS: **8.171 GiB**
- Reused sealed node checkpoints: **0**

Width 22 and capacity exponent 26 name different quantities: each
16-root node batch retains `16 x 2^22 = 2^26` entries.

## Boundary

This validates one frozen N72 instance on a local four-SLC v0.2
software cluster. The historical comparison is descriptive and is
not a new independent reference implementation, distributed-hardware
result, repeated-physical-cell result, or quantum claim.
