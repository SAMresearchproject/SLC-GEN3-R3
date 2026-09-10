# CR005a — Neutrino Substrate Identification + DUNE Forecast Lock — RESULT

```text
verdict           : FAIL  (one pre-registered claim failed; will be superseded by CR005a-b)
classification    : STRUCTURAL_IDENTIFICATION + FORECAST_LOCK
execution_status  : CLEAN
sealed_utc        : 2026-06-29
precommit_hash    : 5beb9ab51b03ee4ec29b18e9e60c743092d0f47e386072281d6f2c1a9e78dcd8
runner_hash       : 3b8fdec3a818f6db6659763fae71125d4f38ee71ee1c9944dc6e59a7c373f14d
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Headline

**22 of 23 pre-registered claims PASS.** One claim FAILed due to an
indexing error in the precommit text — not a substrate-physics problem
but a discipline-required FAIL per the precommit's "any single
arithmetic or identity claim fails → FAIL" rule.

The failure: claim A3.overflow asserted that `36 = (ĥ·d̂)² = m₃²` is
the **second element** of the partition-algebra overflow set
`{18, 24, 36, 72}`. The set was even listed in sorted order in the
precommit text. By inspection, the second element of that set is
**24**, not 36. **36 is the third element** (index 2 zero-based).
Internally inconsistent precommit text.

All other claims — including the structurally load-bearing ones
(`m₃² = ĥ·Θ = 2Θ`, the cross-branch identity with the GW carrier,
the splitting-ratio derivation `(h·Θ−1)/(h−1) = 35`, the DUNE
discrimination calculation at 6.5σ) — verified to exact rational
arithmetic.

This v1 result is sealed FAIL as audit trail. **CR005a-b will be
issued with the corrected claim** (either re-indexed to "third
element" or refocused on the algebraic identity `m₃² = ĥ·Θ` without
the ordinal-position sidecar). The substrate-physics content survives;
the precommit text needed editing before sealing.

## What passed (22/23)

```text
Block A — Substrate identification of mass-squared eigenvalues
  [PASS] A1   m₁² / base_eV² = 1 at partition-algebra (0, 0)
  [PASS] A2   m₂² / base_eV² = ĥ = 2 at partition-algebra (1, 0)
  [PASS] A3.value  m₃² / base_eV² = (ĥ·d̂)² = 36 at position (2, 2)
  [FAIL] A3.overflow  "36 is second element" — wrong; it's third
  [PASS] A4.a  m₃² = 2 · Θ
  [PASS] A4.b  m₃² = ĥ · Θ
  [PASS] A4.c  (ĥ·d̂)² = ĥ · Θ  (algebraic identity)

Block B — Mass-squared progression as substrate multiplicative chain (5/5)
Block C — Splittings derivation (5/5)
Block D — eV scale anchor (6/6)
Block E — Cross-check against CR001@20 sealed values (3/3)
Block F — DUNE / Hyper-K forecast lock (5/5)
```

## What was load-bearing (and passed)

The substrate-physics content of CR005a is intact:

- `m₁² = 1` at partition-algebra ground (0,0)
- `m₂² = ĥ = 2` at binary level (1,0) — a bigrade element
- `m₃² = (ĥ·d̂)² = 36 = ĥ·Θ = 2Θ` at position (2,2) — algebraically
  identical to twice the GW carrier overflow
- Cross-branch identity `m₃² = 2Θ` connects neutrino sector and GW
  sector through the same load-bearing substrate quantity
- Splitting ratio `(ĥ·Θ − 1)/(ĥ − 1) = 35` matches CR001@20 sealed
- Forecast lock: SAM commits to 35; DUNE+HK projected 6.5σ–11σ
  discrimination vs current measured 33.895 by ~2030

None of this depended on whether 36 is the "second" or "third" element
of the overflow set ordered by value. That ordinal claim was a sidecar
observation that I wrote incorrectly.

## The ordinal error in detail

Sorted overflow set from CR005's bounded partition algebra:

```text
{ 18, 24, 36, 72 }      sorted ascending

index 0 = 18 = Θ           = first overflow (the carrier itself)
index 1 = 24 = ĥ³·d̂        = second overflow
index 2 = 36 = (ĥ·d̂)²      = third overflow   ← m₃²
index 3 = 72 = ĥ³·d̂²       = fourth overflow (max in bounded grid)
```

The precommit claimed `m₃² = 36` is the "second element" of this set.
The actual second element is 24. The precommit text was internally
inconsistent — it listed the set `{18, 24, 36, 72}` correctly but
then misidentified 36's position within that ordering.

The runner caught this correctly per the precommit's discipline.
Verdict FAIL is honest per the precommit's verdict tree.

## Substrate-physics interpretation (corrected — for CR005a-b)

The structurally meaningful identification is **algebraic**, not
ordinal:

```text
m₃² = (ĥ·d̂)² = ĥ·Θ = 2Θ
```

This says the heaviest neutrino mass-squared equals the binary readout
times the carrier overflow — or equivalently, twice the carrier. The
fact that 36 happens to be the third element of the sorted overflow set
is incidental. The load-bearing structural content is the algebraic
identity, which CR005a-b will re-state as the primary claim.

## What CR005a does NOT achieve in this v1 form

Per precommit's verdict-tree discipline (any FAIL → FAIL), CR005a v1
cannot serve as the formal forecast lock for DUNE/Hyper-K. The
discrimination computations are correct (sealed in summary.json), but
the verdict per the precommit gate is FAIL.

**CR005a-b will re-seal the same content with corrected precommit
claims**, expected to verdict PASS. The DUNE forecast lock then stands
formally.

## Honest framing

This is exactly the kind of precommit-text error that the
"examine source before precommit" discipline (Sean's prior memo) was
intended to prevent. The substrate-physics derivation chain works;
the indexing claim in the precommit was a Claude-side editing error.
Sealing v1 as FAIL preserves the audit trail.

CR005a-b will be issued immediately. Same content. Corrected ordinal
claim (or refocused on the algebraic identity). Expected PASS.

## Provenance hash chain

```text
precommit          : 5beb9ab51b03ee4ec29b18e9e60c743092d0f47e386072281d6f2c1a9e78dcd8
runner             : 3b8fdec3a818f6db6659763fae71125d4f38ee71ee1c9944dc6e59a7c373f14d
upstream CR001@20  : sealed PASS (mass pattern + Σmν Planck bound)
upstream CR005@21  : 624f0c2655333dd9e6e217f2bed0cbdbd97197281b6f06b462747b7896b13b6b (Θ-overflow framework)
upstream CR229@09a : sealed (Θ = overlap; inclusion-exclusion identity)
upstream CR238@09a : sealed (closure axiom; d̂=3 unique)
stewardship        : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Verdict statement

**CR005a v1 FAIL.** Precommit text contained an internal indexing
inconsistency — claim A3.overflow said `36` is the "second element"
of `{18, 24, 36, 72}` when it is the third. All other 22 claims,
including the load-bearing substrate-identification and forecast-lock
content, PASSed to exact rational arithmetic. CR005a-b will be issued
with corrected precommit to re-seal the same content under PASS.

`NEUTRINO_SUBSTRATE_IDENTIFICATION_22_OF_23_PASS_ORDINAL_INDEXING_ERROR_IN_PRECOMMIT_FAIL_v1_SUPERSEDED_BY_CR005a_b`
