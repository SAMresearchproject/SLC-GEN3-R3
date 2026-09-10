# CR005a v1 — SUPERSEDED 2026-06-29

**Replacement:** [CR005ab_NEUTRINO_SUBSTRATE_IDENTIFICATION_APPEAL](../CR005ab_NEUTRINO_SUBSTRATE_IDENTIFICATION_APPEAL/CR005ab_result.md) (verdict PASS)

## Why superseded

CR005a v1 sealed FAIL on a single pre-registered claim **A3.overflow**.
The precommit text stated: *"the numerical value `36` is the second
element of the partition-algebra overflow set `{18, 24, 36, 72}`."*
The set was even listed in sorted order. By inspection the second
element of that set is `24`; `36` is the third (index 2 zero-based).
Internally inconsistent precommit text.

All 22 other pre-registered claims PASSed to exact rational
arithmetic, including:

- A1, A2, A3.value, A4.a/b/c — substrate identification of m_i²
- B1, B2, B3 — multiplicative chain
- C1-C4 — splittings derivation (ratio = 35)
- D1, D2, D3 — eV scale anchor + Σmν Planck bound check
- E1-E3 — cross-check against CR001@20 sealed values
- F1-F6 — DUNE/Hyper-K forecast lock (6.5σ projected discrimination)

The substrate-physics content (`m₃² = ĥ·Θ = 2Θ` cross-branch identity,
splitting ratio 35, DUNE forecast at 6.5σ) was verified correctly. The
single FAIL was a precommit text-editing error on my part — wrote
"second element" when 36 is the third — caught by the runner exactly
as the discipline is designed to catch internally inconsistent
precommits.

## Discipline note

CR005a v1 stays sealed bit-for-bit as the audit trail of the process.
Hash `5beb9ab5…` (precommit) and `aa46cddc…` (FAIL result) preserved.
CR005a-b re-runs the identical substrate-physics content with the
ordinal claim dropped (precommit refocused on the algebraic identity
`m₃² = ĥ·Θ` and membership in the overflow set, without the
unhelpful ordinal sidecar).

Per Sean's directive 2026-06-29: *"include the appeal reason in the
new precommit and fire again. This is what we do — show the process
and nobody needs to apologize for errors human or agent because we're
honest."*

## Hash chain (unchanged)

| artifact | sha256 |
| --- | --- |
| CR005a_PRECOMMIT.md | `5beb9ab51b03ee4ec29b18e9e60c743092d0f47e386072281d6f2c1a9e78dcd8` |
| CR005a_runner.py | `3b8fdec3a818f6db6659763fae71125d4f38ee71ee1c9944dc6e59a7c373f14d` |
| CR005a_summary.json | `e8de2a0941e0bd28cc61c4f2106c46e2c2b1056e339087fa15594839bedea2d1` |
| CR005a_result.md (FAIL) | `aa46cddc409b1dbdb541605e1a882be51761ded425385bfdb3c3e35230e3f24e` |

CR005a-b's precommit references this v1 hash chain in its provenance.

Stewardship: `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`
