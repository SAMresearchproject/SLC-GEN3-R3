# Mersenne-prime and MP research

**Updated 14 September 2026.** The installed native domain is MP-GEN2-R4-V1
on SLC-GEN3-R3 / SLC-GEN3-CEV1-R3. The MP-B300 successor is
MP_B300 / MP-B300-GEN3-V2. **MP-B300 is PAUSED_BY_OWNER** at its documented
September11 stopping point. This page reports completed work and scoped timing.

## Native domain and acquired work selection

Operations include exact certificate validation, validated-reference reuse,
batched factor elimination, retained-component closure, certified-F histories
and complete checkpoint recovery. The installed farm head learns BULK_FIRST
from earlier sources and executes it on later sources. In its retained workload,
156 terminals agree after fresh recovery; median elapsed time changes from
2.077463s to0.962856s, with28 components built instead of71.

The installed domain's1,020,043 modular checks take0.185043s against2.859704s
for the recorded equal-work independent calculation. M1279's retained
certificate validates in0.103482s; repeated validated-reference reuse has a
median0.875ms in that specific custody context. Those are distinct workloads.

## MP-B300: proof reduction, factor work and learning

The checked recursive M1279 reduction changes277→163 powers and177→95 edges;
all18 large powers remain. Six native validations return
MERSENNE_PRIME_VERIFIED. During concurrent farm work, one CPU comparison was
222.115→183.862ms. The final quiet-pod measurements are different:

| Final single-M1279 execution | Total time | Powers |
|---|---:|---:|
|Recovered selected reduced proof|343.239230ms|163|
|Matched original proof, isolated CPU|331.883348ms|277|
|Selected CPU route after acquiring this comparison|349.868179ms|277|

GEN3 acquired that separate comparison, selected ISOLATED_CPU and executed it.
The useful result includes the changed choice and preserved regression: fewer
proof nodes did not give a speed advantage in that final quiet comparison.

The joint controller investigated seven actions across four source sets,
covering28 source/action combinations and150 proof-learning cycles. Its last
documented state has151 GPU batches and148,914,569,216 proper GPU lanes.
Native checks validate emitted factors and sampled boundaries. No-factor
coverage outside those checks remains GPU-only. It is not a primality certificate.

The earlier52-batch snapshot retains53,925,413,920 lanes and220GiB of populated
GPU histories in five buffers. Source recipes, outcomes and native roots are
durable; the VRAM buffers are volatile and reconstructible. Cumulative logical
history coverage is not measured memory-bus traffic.

For the executed sufficient-proof reduction and source-linked GPU history
readout: **The test result suggests strong contact with the concept.**
Frontier MP certification and subsecond frontier validation remain open.
The final quiet-test figures are preserved in the source handoff from actual
tool output; retrieval of its complete final remote receipt files was still
pending at that handoff. This public summary retains that provenance distinction.

## Other retained MP work

The R4 CSV training pass completed15,064 batches, with96,409 training rows and
24,096 evaluation rows across120,505 sampled exponents. That pass is complete;
its inspected services were inactive. Historical source and custody records
remain distinct from present availability of bulk payloads.

The MP52 factor trial at p=136279841 checks1,048,576 lanes in0.151517s and
returns KEEP_LOOKING with no factor found; next k=1,048,577. The bounded native
construction adapter in that trial accepts p≤4096, so it does not dispatch a
certificate construction for this exponent.

A candidate, ranking, timing observation or no-factor interval does not assign
primality. Native certified terminals and complete primality tests retain their
own authority. This update reports no newly certified frontier Mersenne prime.

[Source index](../SOURCE_INDEX.md) · [Public result summary](RESULTS.json) ·
[All research](../../docs/RESEARCH.md)
