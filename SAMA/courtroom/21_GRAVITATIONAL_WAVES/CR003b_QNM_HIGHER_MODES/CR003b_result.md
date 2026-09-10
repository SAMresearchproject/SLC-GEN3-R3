# CR003b — QNM Higher Modes Strength Test — RESULT

```text
verdict           : STRONG_PASS
mode              : EXPLORATORY
execution_status  : CLEAN
sealed_utc        : 2026-06-28
precommit_hash    : 9ed16b1ebc02c8765db9ff3c307bf71380928ffb7954cb0bfb300a972d2703c5
runner_hash       : 0dad57ddfc7c59e0ee9899a0cc263047ed27e821679f8a5926fed318a484dea4
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Headline

All 10 dimensionless coefficients across the 5 higher Schwarzschild
QNM modes have a substrate-atom expression within the 0.5% PASS gate.

| mode | ω_R · M (GR) | best SAM form | SAM value | err |
| --- | ---: | --- | ---: | ---: |
| l=2 n=1 | 0.34671 | `𝒱/(F−π)` | 0.346783 | **0.021%** |
| l=3 n=0 | 0.59944 | `F/(ℒ−𝒱)` | 0.600000 | **0.093%** |
| l=3 n=1 | 0.58264 | `M/(S·𝒱)` | 0.583333 | **0.119%** |
| l=4 n=0 | 0.80918 | `S/π²` | 0.810569 | **0.172%** |
| l=5 n=0 | 1.01229 | `(ℒ+ĥ)/ℒ` | 1.012346 | **0.005%** |

| mode | ω_I · M (GR) | best SAM form | SAM value | err |
| --- | ---: | --- | ---: | ---: |
| l=2 n=1 | 0.27391 | `π²/(R·d̂)` | 0.274156 | **0.090%** |
| l=3 n=0 | 0.09270 | `(R+d̂)/ℒ` | 0.092593 | **0.116%** |
| l=3 n=1 | 0.28129 | `F/(ℒ+M)` | 0.281250 | **0.014%** |
| l=4 n=0 | 0.09416 | `S/(π·𝒱)` | 0.094314 | **0.164%** |
| l=5 n=0 | 0.09487 | `S/(F+π)` | 0.095078 | **0.219%** |

10/10 within 0.5%. 0 in BOUNDARY band. 0 FAIL.

## What changed from CR003 → CR003b

CR003 found the **fundamental** l=m=2 n=0 mode reproduced by pure
rational substrate forms (`d̂/S` and `R/(R²−d̂²)`). In the higher modes:

- **π starts appearing** in best matches. The l=2 n=1 overtone's real
  part is `𝒱/(F−π)`; the same overtone's imag part is `π²/(R·d̂)`.
  l=4 and l=5 also surface π in their best matches.
- **The ℒ ↔ 𝒱 substrate pair** (closed ledger vs write cell, the
  load-bearing ratio in CR036's η_SAM exponent) shows up in both
  ω_R and ω_I matches for l=3 n=0: `F/(ℒ−𝒱)` and `(R+d̂)/ℒ`.
- **`F/(ℒ+M)` for l=3 n=1 ω_I** evaluates to 81/288 = 0.28125,
  within 0.014% of GR — striking for a sum-of-named-atoms form.

The pattern: as the mode complexity rises (higher l, higher n),
the substrate matches pull in the **route-completion axis π**
along with the rational atoms. This is substrate-consistent with
CR258's framing — π enters when route-completion accounting is
needed; higher-mode oscillations are higher-order route completions.

## Forward-prediction extension (H1, H2): both fail

Two natural extensions of CR003's leading forms were evaluated and
reported in the runner. Both miss badly:

**H1**: extrapolate ω_R fundamental via `(d̂/S) · (l−1)`:

| mode | H1 prediction | GR target | err |
| --- | ---: | ---: | ---: |
| l=3 n=0 | 0.75000 | 0.59944 | 25.1% |
| l=4 n=0 | 1.12500 | 0.80918 | 39.0% |
| l=5 n=0 | 1.50000 | 1.01229 | 48.2% |

**H2**: scale ω_I overtone via `R/(ℒ−𝒱) · (2n+1)`:

| mode | H2 prediction | GR target | err |
| --- | ---: | ---: | ---: |
| l=2 n=1 | 0.26667 | 0.27391 | 2.6% |
| l=3 n=0 | 0.08889 | 0.09270 | 4.1% |
| l=3 n=1 | 0.26667 | 0.28129 | 5.2% |

Neither hypothesis extends the CR003 fundamental into a substrate
function of (l, n). The substrate encoding is **atom-by-atom**,
not a single closed parametric formula spanning the spectrum.

## What CR003 + CR003b together establish

| mode | ω_R · M form | err | ω_I · M form | err |
| --- | --- | ---: | --- | ---: |
| l=2 n=0 (CR003) | `d̂/S` | 0.36% | `R/(ℒ−𝒱)` | 0.08% |
| l=2 n=1 | `𝒱/(F−π)` | 0.02% | `π²/(R·d̂)` | 0.09% |
| l=3 n=0 | `F/(ℒ−𝒱)` | 0.09% | `(R+d̂)/ℒ` | 0.12% |
| l=3 n=1 | `M/(S·𝒱)` | 0.12% | `F/(ℒ+M)` | 0.01% |
| l=4 n=0 | `S/π²` | 0.17% | `S/(π·𝒱)` | 0.16% |
| l=5 n=0 | `(ℒ+ĥ)/ℒ` | 0.01% | `S/(F+π)` | 0.22% |

12 of 12 Schwarzschild QNM coefficients across 6 modes are within
0.5% of substrate-atom expressions.

## What this CR seals

1. The substrate atom set
   `{ ĥ, d̂, S, V, F, R, R², Θ, ℒ, M, π }` contains expressions
   within 0.5% of every Schwarzschild QNM coefficient tested.
2. Higher modes pull in π (the route-completion axis) more than
   the fundamental — substrate-consistent with π entering when
   route completion is non-trivial.
3. The CR003 fundamental forms (`d̂/S`, `R/(R²−d̂²)`) do not
   parametrically extend to higher modes via the simplest l- or
   n-multiplicative hypotheses. The encoding is per-mode.
4. The CR229@09a inclusion-exclusion identities (especially
   `ℒ − 𝒱 = R² − d̂² = 135`) appear repeatedly in the best matches —
   the same ledger structure that sets the CR001 cap also
   characterizes ringdown coefficients across the spectrum.

## What this CR does NOT seal

- A first-principles derivation chain from substrate atoms to
  Schwarzschild QNM. Each match is identified by enumeration, not
  by derivation. The substrate-physics path from carrier-tensor
  oscillation to the specific QNM dimensionless coefficient is
  open.
- A prediction for Kerr (spinning) QNM coefficients. The Kerr
  spectrum depends continuously on dimensionless spin a/M, and the
  substrate has no obvious atom for arbitrary a/M. CR003c is the
  candidate follow-up for spinning ringdowns.
- A discrimination against the null hypothesis "the substrate
  atom space is rich enough that good rational/π approximants exist
  for any nearby positive real number under 22,627 expressions."
  With a search space that large, hits at the 0.5% level for arbitrary
  targets are not improbable per se. The interpretive weight comes
  from (a) which atoms appear and (b) whether they connect to
  substrate identities — see "what CR003 + CR003b together
  establish" above.

## Source citations

- Berti, Cardoso, Starinets 2009, Living Rev. Rel. 12, 2,
  Table I (Schwarzschild QNM dimensionless frequencies for
  l ∈ {2, 3, 4, 5}, n ∈ {0, 1})
- Leaver 1985, Proc. Roy. Soc. A 402, 285

## Provenance hash chain

```text
precommit          : 9ed16b1ebc02c8765db9ff3c307bf71380928ffb7954cb0bfb300a972d2703c5
runner             : 0dad57ddfc7c59e0ee9899a0cc263047ed27e821679f8a5926fed318a484dea4
upstream CR003     : precommit ec90b9924a12ae760bd3cefb550ad602be442114b8a26c36b0fb9c37f5998cd3
upstream CR002     : precommit a42873eb1d3f68064c2d2540f93d6cc9f68f24c830daa36922240cab42733e18
upstream CR001     : precommit 1e37ca0a35394c2c6a1c36f8a124058c505f4ad9be339bdb1204d9cacf1d0805
CR258 closure      : 942b42dd5ec75e991af59e542f090f1a9f0676c04cbd58c05601f874fc045fb7
branch README      : 1a4a2e0d388f2a913ee68163a5b2636dfef44f0aa5712a48acbe6e17b4fb6595
stewardship        : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
```

## Verdict statement

**CR003b STRONG_PASS (EXPLORATORY).** All 10 higher-mode
Schwarzschild QNM dimensionless coefficients (5 modes × 2 parts)
land substrate-atom expressions within the 0.5% precommit gate.
Combined with CR003's fundamental match, all 12 QNM coefficients
across 6 Schwarzschild modes are reproduced by substrate atoms.

The higher modes pull in π (route-completion axis) more than the
fundamental, substrate-consistent with route-completion physics.
The forward-extension hypotheses H1 (d̂/S · (l−1) for fundamental
ω_R) and H2 (R/(ℒ−𝒱) · (2n+1) for overtone ω_I) both miss — the
substrate encodes the ringdown spectrum atom-by-atom, not by a
single parametric function of (l, n).

`SCHWARZSCHILD_QNM_HIGHER_MODES_10_OF_10_WITHIN_HALF_PERCENT_SUBSTRATE_ATOMS_ENCODE_PER_MODE_PI_APPEARS_IN_OVERTONES_H1_H2_PARAMETRIC_EXTENSIONS_REJECTED_STRONG_PASS_EXPLORATORY`
