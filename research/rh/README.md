# Riemann Hypothesis research

**Updated 14 September 2026.** The controlling mathematical task remains
uniform signed-growth control for the actual Möbius source on the original
common sequence. Signed prefix growth, full-energy control and forcing-excess
control are routes to that task. The uniform arithmetic estimate remains open.

Read [Signed Forcing and Arithmetic Compensation in the SAM Kernel, version 2](paper.md)
([PDF](paper.pdf), [HTML](paper.html)). Sean Brady, OpenAI ChatGPT and Codex are
the credited co-authors. Independent mathematical review is pending.

## Exact structure now available

For the stopped source a_i=μ(s+i)1_(i<t), retain the complete original energy:

```text
Q_s(a) = M_a²/s + Σ[r=1..s−1] q_a(r)²/[r(s−r)],
q_a(r) = Σ[i<r] a_i − r M_a/s.
```

The kernel spectrum is 1 and 1/[k(k+1)]. Retaining through
m=min(s−1,ceil(sqrt(s))) gives F_m≤Q≤F_m+1. The intrinsic resistance coordinate
preserves the complete derivative norm. Dyadic parity gives a full signed
transport identity Q(2s,2t)=Q(s,t)+E(s,t)+R(s,t), with R≤3. This is a one-sided
bound; an odd endpoint contributes its separately retained signed increment.

A uniform one-sided subpower bound E(s,t)≤C_ηs^η for every η>0 would give
uniform subpower full energy and then RH. The smaller-source transfer theorem
identifies another sufficient hypothesis: an exponent
p_j=2−κ/log(e+j), with 0<κ≤1, in the actual-source energy bound suffices.
The hypotheses are stated with all scales and stops in the paper; establishing
the arithmetic estimate is the remaining task.

## Complete forcing-excess scans

| Scale | Prefixes, including endpoints | Maximum E | Maximizing stop | E>1/2 cases |
|---:|---:|---:|---:|---:|
|32|33|0.063413987429|1|0|
|512|513|0.210217371429|481|0|
|4096|4097|0.514400059116|1071|5|
|8192|8193|0.520439137454|7798|8|
|Total|12,836|||13|

For the candidate E≤1 over this declared tested scope: **The test result
suggests the concept is possible.** For the uniform half-ceiling candidate:
**The test falsifies the concept.** A separate signed-divisor study has
15,364 prefixes; it measures a different quantity and is not added to this count.

## Arithmetic mechanisms and source certificates

An equal-admission run (β=α at every step) has the exact telescoping relation
E(t)−E(start)=Q(a_start)−Q(a_t)≤Q(a_start), independent of the run's length.
At the 8192 peak admission, the pair source receives zero net admission and
the excess rises through falling inherited energy. The larger buildup remains
forcing-led. The subsequent signed histories record compensation explicitly.

At scale4096, exact four-admission continuation bounds from stops1071,1077
and1130 are respectively0.589424758671,0.600499614290 and0.343086069882.
The recovery state therefore keeps E below one-half over its stated horizon.
For these conditional current-state bounds: **The test result suggests strong
contact with the concept.** Renewing that control through continuing admissions
remains open. Previously fitted sign-class forecasts failed their stated future
bounds: **The test falsifies the concept.**

The paper retains the historical selection audit:24 learned questions cost
2.059058 native CPU seconds and two fixed questions0.134178 seconds. These are
combined original derivative-plus-forcing costs. Neither arm improved the known
scale512 maximum; unequal counts and budgets are retained in the interpretation.

## Data and source documents

The [dated research release](https://github.com/SAMresearchproject/SLC-GEN3-R3/releases/tag/research-2026-09-14)
provides the original compressed exact scale-8192 output and paper PDF.
The coverage file contains all8193 exact rational prefix records and source
witnesses. Its original native metadata identifies186.531558 CPU seconds for
that scan. Download sizes and hashes are recorded in [the asset manifest](DATA_ASSETS.json).

Companion derivations are in [notes/](notes/); the [source index](../SOURCE_INDEX.md)
maps their upstream paths and authority. The paper's22 numbered equations,
finite certificates and conditional hypotheses are retained together. Full
private runtime recovery stores are separate from this public research data.
