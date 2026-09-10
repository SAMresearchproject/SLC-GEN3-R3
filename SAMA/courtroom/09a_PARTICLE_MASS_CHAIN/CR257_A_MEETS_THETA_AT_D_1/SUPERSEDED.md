# CR257 v1 — SUPERSEDED 2026-06-28

**Replacement:** [CR257b_A_MEETS_THETA_AT_D_1_W4_CORRECTION](../CR257b_A_MEETS_THETA_AT_D_1_W4_CORRECTION/CR257b_result.md) (verdict PASS)

## Why superseded

CR257 v1 sealed BOUNDARY because its W4 wrong-control runner branched on
`sign` and applied the power variant to both negative and positive
forms. The positive-side variant used `(1 - p²/R⁴)^power` — but
canonical positive is itself `(1 - p²/R⁴)^1`, so `power=1` left it
bit-identical to canonical and 8 positive rows matched trivially. That
collapsed W4 to 8/16 and triggered the BOUNDARY branch.

The v1 precommit text already scoped W4 correctly to the negative side
only:

> **W4 — Replace squared factor.** For neg side at d=1, replace
> `(1 + p/R²)²` with `(1 + p/R²)¹` (single power) or `(1 + p/R²)³`
> (cubed). Expected: 0 / 8 each.

CR257b uses an identical precommit (verbatim test spec) and a runner
that honors that scope. All five gates PASS.

## Discipline note

**The artifacts in this folder are not deleted, edited, or marked
"wrong."** They are the proof-of-process record: an honest BOUNDARY
result for a self-inflicted wrong-control bug, sealed and hashed at
their original values. The structural finding (A-Θ meeting at d=1 as
substrate-natural compact forms) was clean in this v1 across the
load-bearing gates (E + A + D + W3), with only W4 downgrading the
verdict.

## Hash chain (unchanged)

| artifact | sha256 |
| --- | --- |
| CR257_PRECOMMIT.md | `75ee3b884a8b4d25bebfa2fa847de75e7edc0d7a2e0264424a610469f6e64afd` |
| CR257_runner.py | `664ba986e013534e323758f9ec705e086d11ed32060771cbc903c2996391035b` |
| CR257_result.md | `eea3b57db301562992502c1b8ac76f7176b2f6cb64ac46338c2824e5961eb9b4` |
| CR257_summary.json | `db5b8ff0010a6984d82893e4c392320829f1408a20e02bde1376ecabe1768788` |
| CR257_d1_predictions.csv | `0adb50d8639a6f74dab1cdeae9be4f0e2433d1067ec3ce94a62f8f191a875c3f` |
| CR257_wrong_controls.csv | `2aa870a8cf6e5f6b8b5152d6f8531a615f0d6494903aa9df70a0611652439be5` |

CR257b's precommit references this v1 hash chain as upstream lineage
context.

Stewardship: `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`
