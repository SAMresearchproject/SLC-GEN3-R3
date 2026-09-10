# Starbreaker External Collapse Contact v0.1

Status: `PASS_EXTERNAL_QUALITATIVE_DIRECTIONAL_CONTACT__NO_PHYSICAL_PROMOTION`

## Frozen external signature

One source was selected before comparison: [Black Hole Formation in Failing Core-Collapse Supernovae](https://arxiv.org/abs/1010.5550) by Evan O'Connor, Christian D. Ott, The Astrophysical Journal 730, 70 (2011), DOI [10.1088/0004-637X/730/2/70](https://doi.org/10.1088/0004-637X/730/2/70).

Locked direction: **Higher bounce compactness is associated with faster black-hole formation and progenitors that are harder to explode.**

Only this direction is tested. The paper's numerical compactness values, fit, thresholds, progenitor masses, and equation-of-state results do not enter Starbreaker.

## Locked Starbreaker result

| geometry | p=0 remnant | p=1 | p=2 | p=3 | p0→p3 | strict ladders | same-total wins | radial rank |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| localized_ledger_cells | 0.494604 | 0.595000 | 0.704559 | 0.788339 | +0.293735 | 21/21 | 21/21 | max of 24 |
| dispersed_slots | 0.555535 | 0.638630 | 0.747190 | 0.819046 | +0.263511 | 21/21 | 21/21 | max of 24 |

The two mean ladders are strictly ordered, all 42 individual anchor/seed ladders increase at every p step, all 42 inward p=3 rows beat their same-total uniform controls, and the aligned inward allocation is the maximum-remnant arrangement in both exhaustive 24-permutation families.

## Verdict

Starbreaker's locked 3D density ladder moves in the same qualitative collapse direction as the frozen compactness result: more inward concentration produces more internal remnant and less ejecta.

The ordering is strict in both aggregate ladders, all 42 individual anchor/seed ladders, all 42 same-total comparisons, and both exhaustive 24-permutation families.

## Boundary

This is directional contact with an external simulation result, not a fit, measurement, physical calibration, black-hole prediction, or validation of the A packing law.

In particular, `p` is not the physical compactness `ξ₂.₅`, and Starbreaker's remnant fraction is not a black-hole probability. This gate establishes qualitative directional contact only.

Next gate: freeze one genuinely time-resolved internal observable before any further external comparison; the current endpoint simulator cannot test the source paper's faster-time-to-black-hole signature.
