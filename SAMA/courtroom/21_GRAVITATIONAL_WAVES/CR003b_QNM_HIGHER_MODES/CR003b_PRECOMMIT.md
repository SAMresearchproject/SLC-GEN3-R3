# CR003b — QNM Higher Modes Strength Test

**Branch:** 21_GRAVITATIONAL_WAVES
**Mode:** EXPLORATORY
**Sealed by:** Sean Brady, 2026-06-28
**Upstream:** CR001 PASS, CR002 PASS, CR003 PASS
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`

---

## Question

CR003 found the Schwarzschild fundamental l=m=2, n=0 QNM
dimensionless frequency reproduced by simple substrate ratios:

```text
ω_R · M  =  d̂/S  =  3/8         (within 0.36% of GR 0.37367)
ω_I · M  =  R/(ℒ−𝒱)  =  4/45    (within 0.083% of GR 0.08896)
```

Does the substrate algebra encode the **full ringdown spectrum**,
or only the fundamental mode?

CR003b tests five higher Schwarzschild QNMs (l=2 n=1, l=3 n=0,
l=3 n=1, l=4 n=0, l=5 n=0) against the same substrate atom set and
search forms as CR003. Each higher mode either lands a substrate
expression within tolerance or it doesn't. Honest result either way.

## Target values

Schwarzschild QNM dimensionless complex frequencies, Berti et al.
2009, Living Rev. Rel. 12, 2, Table I:

| mode (l, n) | ω_R · M | ω_I · M |
| --- | ---: | ---: |
| 2, 1 (1st overtone) | 0.34671 | 0.27391 |
| 3, 0 (l=3 fundamental) | 0.59944 | 0.09270 |
| 3, 1 (l=3 1st overtone) | 0.58264 | 0.28129 |
| 4, 0 (l=4 fundamental) | 0.80918 | 0.09416 |
| 5, 0 (l=5 fundamental) | 1.01229 | 0.09487 |

Total: 10 dimensionless coefficients tested (5 modes × {real, imag}).

## Search space (same as CR003)

```text
atoms = { ĥ, d̂, S, V, F, R, R², Θ, ℒ, M, π }
forms = { a/b, a/(b+c), a/(b−c), (a+b)/c, (a−b)/c,
          (a·b)/c, a/(b·c), (a·b)/(c·d) }
```

For each target value, find the candidate with smallest relative
error. Report top 5.

## Verdict tree

Counted across all 10 coefficients (5 modes × 2 parts):

```text
STRONG_PASS:
  >= 9 of 10 coefficients within 0.5%

PASS:
  >= 7 of 10 coefficients within 0.5%

BOUNDARY:
  5 or 6 of 10 within 0.5%, OR
  >= 7 within 5% even if not all within 0.5%

FAIL:
  < 5 of 10 within 0.5% AND < 7 within 5%
  -> substrate atoms do not naturally encode higher modes;
     CR003's fundamental match stands alone
```

## Forward-prediction extension (also reported)

CR003's leading forms:
```text
ω_R · M = d̂/S  (carrier-tensor cap × dimensional readout)
ω_I · M = R/(ℒ−𝒱) = R/(R²−d̂²)
```

Two natural substrate-extension hypotheses to evaluate alongside
the per-mode search:

**H1 (Schutz-Will asymptotic-form analog)**: for fundamental modes
(n=0) at multipole l, hypothesize

```text
ω_R · M ≈ (l − 1) · (d̂/S) + something
ω_I · M ≈ R/(ℒ−𝒱)  (approximately constant for n=0, varies slowly)
```

The GR pattern shows ω_I·M increasing slowly with l (0.0890 → 0.0927
→ 0.0942 → 0.0949 for l=2, 3, 4, 5). Substrate has no obvious l-atom,
so an exact substrate function of l is unlikely.

**H2 (overtone scaling)**: for fixed l, increasing n approximately
scales the imaginary part by ≈ (2n+1)/(2·0+1) = (2n+1):
```text
ω_I · M (n=1) ≈ 3 · ω_I · M (n=0)
```

Both hypotheses are reported but **not gated**. The load-bearing
verdict is the per-mode search count.

## Provenance hash chain

| artifact | sha256 |
| --- | --- |
| CR003 PASS (upstream) | precommit `ec90b9924a12ae760bd3cefb550ad602be442114b8a26c36b0fb9c37f5998cd3` |
| CR002 PASS | precommit `a42873eb1d3f68064c2d2540f93d6cc9f68f24c830daa36922240cab42733e18` |
| CR001 PASS | precommit `1e37ca0a35394c2c6a1c36f8a124058c505f4ad9be339bdb1204d9cacf1d0805` |
| CR258 closure | `942b42dd5ec75e991af59e542f090f1a9f0676c04cbd58c05601f874fc045fb7` |
| branch README | `1a4a2e0d388f2a913ee68163a5b2636dfef44f0aa5712a48acbe6e17b4fb6595` |
| stewardship | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
