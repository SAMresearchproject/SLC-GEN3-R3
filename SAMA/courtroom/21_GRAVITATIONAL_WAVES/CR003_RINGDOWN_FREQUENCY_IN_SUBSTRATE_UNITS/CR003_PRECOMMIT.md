# CR003 — Ringdown Frequency in Substrate Units

**Branch:** 21_GRAVITATIONAL_WAVES
**Mode:** EXPLORATORY
**Sealed by:** Sean Brady, 2026-06-28
**Upstream:** CR001 PASS, CR002 PASS
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Idea under test

GR gives the dominant Schwarzschild quasi-normal mode (l=2, m=2,
fundamental, non-spinning BH) a dimensionless complex frequency

```text
omega_QNM · M · G / c^3   =   omega_R · M  +  i · omega_I · M
                          =   0.37367168    +  i · 0.08896232
                              (Berti et al. 2009, Living Rev. Rel. 12, 2)
```

These two numbers are obtained by numerical solution of the
Regge-Wheeler / Zerilli equation. **GR does not provide a
closed-form rational/transcendental expression for either coefficient.**

SAM's discipline (CR258 primitive-closure audit) says every load-bearing
constant in any sealed CR should reduce to a finite expression in
the primitive base `(ĥ=2, d̂=3, π)` plus the derived atoms
`(S=8, V=27, F=81, R=12, Θ=18, ℒ=162, M=126)`. If the ringdown
coefficients are substrate-derivable, SAM lands a coefficient GR
only computes numerically — a substantive discrimination.

If no substrate expression lands within tolerance, that itself is
information: the ringdown coefficients live in the route-completion
sector (π-mediated, not pure substrate algebra), and the test
honestly surfaces the structural gap.

## Question

Does there exist a finite expression in the substrate atoms
`{ĥ, d̂, S, V, F, R, R², Θ, ℒ, M, π}` constructed via the
operations `{ /, ·, +, − }` over at most 5 atoms that evaluates to:

- `ω_R · M = 0.37367168` within ±0.5%, AND
- `ω_I · M = 0.08896232` within ±0.5%?

## Search space (declared at precommit)

```text
atoms   = { ĥ, d̂, S, V, F, R, R², Θ, ℒ, M, π }
ops     = { + , − , × , / }
forms   = exhaustive enumeration of:
            a / b
            a / (b + c)
            a / (b − c)
            (a + b) / c
            (a − b) / c
            (a · b) / c
            a / (b · c)
            (a · b) / (c · d)
          for a, b, c, d ∈ atoms (with repetition allowed)

tolerance gates:
  PASS     : best match has relative error <= 0.5%
  BOUNDARY : best match has 0.5% < relative error <= 5%
  FAIL     : best match has relative error > 5%

Both ω_R·M and ω_I·M must independently pass for joint PASS.
```

## Cross-checks reported (not gated)

- **Quality factor** Q = ω_R / (2·ω_I) — GR value ≈ 2.1004.
  If both candidates pass, the SAM-derived Q computes from substrate
  algebra and can be compared to GR.
- **2nd-best matches** for each part — if the second-best is also
  substrate-clean and close, that's confirming structure; if it's
  far away, the leading match is isolated.
- **Search-space size** — how many forms were tested, so the reader
  can judge whether a sub-0.5% match could be a coincidence (small
  search space → impressive; large search → less so).

## What this CR seals

If PASS on both parts: SAM provides **a closed-form substrate
expression for both the Schwarzschild fundamental QNM real and
imaginary parts**. The substrate algebra encodes what GR computes
numerically. First substantive substrate-vs-GR discrimination in
the GW branch.

If BOUNDARY: the substrate atoms are close to the QNM coefficients
but no expression within tested forms hits the 0.5% gate. The
framing survives but flags that higher-order forms (or a missing
substrate atom) are required.

If FAIL: the substrate algebra does not reach the QNM coefficients
within tolerance. The ringdown frequency lives outside the
substrate's rational sector — a structural gap worth documenting.
Subsequent CRs in the branch (CR004 donut, CR005 polarization)
would then carry the discrimination load.

## Honest framing notes (EXPLORATORY)

- This is a search, not a forward prediction. The substrate atoms
  were sealed by CR258 before this CR; the search enumerates
  combinations of them. A sub-0.5% match is suggestive of
  structural encoding, but not proof against coincidence over the
  search-space size.
- A PASS here does not say "SAM derives the QNM" in the sense that
  CR037B says "SAM derives the CMB shape" — CR037B's η_SAM was
  identified by a substrate-derivation path (L/V exponent = 6), then
  evaluated. CR003's match is identified by enumeration, then
  evaluated. Both are valid substrate-physics evidence, but they
  carry different epistemic weight. The result.md will spell this
  out.
- CR003b can extend to higher modes (l=3, n=1, l=4 fundamental).
  If the SAME substrate atoms predict the higher modes within
  tolerance, the encoding hypothesis strengthens substantially.

## Target values (declared external numeric literals)

```text
Schwarzschild l=m=2 n=0 QNM dimensionless complex frequency
  source: Berti, Cardoso, Starinets 2009, Living Rev. Rel. 12, 2
          (also Leaver 1985; Nollert 1993; tabulated in many texts)

  omega_R · M (real)      = 0.37367168
  omega_I · M (imaginary) = 0.08896232
  Q = omega_R / (2 omega_I) = 2.10039...
```

## Provenance hash chain

| artifact | sha256 |
| --- | --- |
| CR001 PASS (upstream)   | precommit `1e37ca0a35394c2c6a1c36f8a124058c505f4ad9be339bdb1204d9cacf1d0805` |
| CR002 PASS (upstream)   | precommit `a42873eb1d3f68064c2d2540f93d6cc9f68f24c830daa36922240cab42733e18` |
| CR258 primitive closure | `942b42dd5ec75e991af59e542f090f1a9f0676c04cbd58c05601f874fc045fb7` |
| branch README           | `1a4a2e0d388f2a913ee68163a5b2636dfef44f0aa5712a48acbe6e17b4fb6595` |
| branch GW_SUBSTRATE_FRAMING | `a19afc01a749e925d6e1e4f70321217dcaca95fd5981a68e0e52ebdfcb2ed941` |
| branch CR_QUEUE         | `ef6f85bc02a1dd2a9fc62f4d14da865079f0705f25e73eeb815d1d6b6b810c66` |
| stewardship             | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
