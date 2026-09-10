# CR012 — Nested-Home Distance-as-Information Foundation — RESULT

```text
verdict           : PASS
classification    : STRUCTURAL_FOUNDATION_CR
execution_status  : CLEAN
sealed_utc        : 2026-07-03
precommit_hash    : (see HASHES.txt)
runner_hash       : (see HASHES.txt)
stewardship_hash  : d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
lc_assignment_hash: 3a88142743f3d5487a55dc99e29f51edd097660e3cb27625c79aee3f5f29d4a4
frame_anchor_hash : 7b0f225821e2aea55e02b0868997fa2acd4ee88b4711ab1b1fb161366e1c5137
free_parameters_introduced : 0
prior_CR_result_inputs     : true (CR011 sealed d_ref_base = 46.52 μm)
external_data_inputs       : false
```

## Headline

The Home-nesting projection factor for the SLC bench context is sealed at:

```text
n_SLC_bench  =  0
d_ref_bench  =  R^0 · d_ref_base  =  d_ref_base  =  46.52 μm    (SI)
```

with zero free parameters and zero bench-target reference in the derivation. The identification rests on CR010 §1.2's sealed SI-per-loop identification: the substrate-loop-to-SI-meter conversion is already established at the CR010 level, so no additional R^n multiplication is required to translate the base-substrate reach into bench-observable SI meters.

The three-CR foundational chain (CR010 + CR011 + CR012) is now complete, and CR-NSC-01 S1 v2 can execute with a specific numerical bench prediction:

```text
H_pred(0.15 m) = A₀ · d_ref_bench / d = (1/12π) · 46.52e-6 / 0.15 = 8.23 × 10⁻⁶
CR-NSC-01 §7 overnight sensitivity floor       = 7.4  × 10⁻⁶
Ratio H_pred / floor                            = 1.11
```

**Landing: F-iii marginal.** The SLC bench experiment is predicted to observe a coupling signal above the overnight sensitivity floor by factor 1.11 — ~10% headroom on the m_3 spectrum's ~5% uncertainty.

## Gate results

| gate | claim | outcome |
| --- | --- | :---: |
| G1 | Upstream-only inputs (CR010, CR011, CR003@19, CR266, Vol I §7, project_sam_homes_naming, SAM_ON_EARTH) | PASS |
| G2 | No bench-target reference in §1-§2 derivation reasoning | PASS |
| G3 | Numerical composition d_ref_bench = R^0 · d_ref_base = 46.52 μm trivially exact | PASS |
| G4 | Alternative identifications (n=1, n=2, n=k from Earth-frame Home level) enumerated with structural non-selection reasons | PASS |
| G5 | Wrong control W1 — additional nesting sensitivity (n=1 lands 558 μm, would be F-iii solid, refused as bench-comfort retrofit) | PASS |
| G6 | Wrong control W2 — Home-nesting radix sensitivity (R = 12 forced by Vol I §7 A-accounting) | PASS |
| G7 | Wrong control W3 — SI mapping sensitivity (CR010 §1.2 SI-anchored via SAM_ON_EARTH) | PASS |
| G8 | Provenance chain | PASS |

All 8 gates PASS. **Verdict: PASS.**

## Numerical verification (from CR012_runner.py execution)

**Home-nesting radix R = 12 cross-consistency (4/4 sealed anchors):**

```text
CR266 mirror linear extent (ĥ²·d̂) = 12   PASS
Vol I §7 A_share = 1/R inverse       = 12   PASS
CR259 chessboard side (R+1=13) − 1   = 12   PASS
LCQC002 register radix                = 12   PASS
```

Four independent sealed CRs give R = 12 exactly. The Home-nesting radix is not a free parameter — it's the same integer appearing across the sealed record.

**CR011 base value carried forward:**

```text
d_ref_base = R · λ_spaghettio = 12 · 3.8768 μm = 46.5216 μm    (from CR011 §1.3 sealed)
```

**CR012 §1.4 projection identification:**

```text
n_SLC_bench   = 0
d_ref_bench   = R^n · d_ref_base = 12^0 · 46.5216 μm = 46.5216 μm
projection check: R^0 = 1, so bench value equals base value exactly. PASS.
```

**Final S1 v2 preview at bench distance 0.15 m:**

```text
A₀            = 1 / (12π)             = 0.02652582
d_bench       = 0.15 m
d_ref_bench_m = 4.6522 × 10⁻⁵ m
H_pred        = A₀ · d_ref_bench / d_bench
              = 0.02653 · 4.6522e-5 / 0.15
              = 8.2268 × 10⁻⁶
Floor         = 7.4 × 10⁻⁶            (CR-NSC-01 §7 overnight sensitivity)
Ratio         = 1.112                  (11.2% above floor)
Landing       = F-iii marginal
```

## Alternative candidate verifications

The alternative n values enumerated in §4.G4:

| candidate | d_ref_bench (μm) | H_pred at 0.15 m | ratio to floor | landing | status |
| --- | ---: | ---: | ---: | :---: | --- |
| **n = 0 (mechanism-forced)** | **46.52** | **8.23e-06** | **1.11×** | **F-iii marginal** | **SEALED (this CR)** |
| n = 1 | 558.26 | 9.87e-05 | 13.34× | F-iii solid | refused pending sealed intermediate nesting |
| n = 2 | 6699.11 | 1.18e-03 | 160.09× | F-iii excess | refused pending sealed intermediate nesting |

Note: n = 1 landing at 13.3× floor is the "comfortable F-iii" territory the earlier CR011 v1.2 draft flirted with under candidate (c). CR012 explicitly refuses to seal n = 1 without a specific structural anchor — even though it would land the bench prediction more comfortably. The refusal is the anti-retrofit-hazard check.

## Wrong controls

**W1 — additional nesting sensitivity.** If n = 1 were imposed without structural justification, d_ref_bench would jump to R × 46.52 μm = 558 μm, landing S1 v2 F-iii solid at 13× floor. The temptation to seal n = 1 for bench comfort is precisely what §4.G4 refuses. **W1 passes structurally** — n > 0 requires sealed structural anchor, not comfort.

**W2 — Home-nesting radix sensitivity.** If the Home-nesting radix were something other than R = 12 (say, R = 13 chessboard side, or trillion-per-level per loose "trillions of Homes" language), the R^n dressing structure would change. Vol I §7 A-accounting seals R = 12 exactly via A_share = 1/R, and four sealed CRs cross-verify R = 12 (CR266, CR259, LCQC002, Vol I §7). **W2 passes structurally** — R = 12 is the only value consistent with the sealed A-accounting ladder.

**W3 — SI mapping sensitivity.** If CR010 §1.2's identification of λ_spaghettio with m_3 Compton were not SI-anchored, additional projection would be required to translate substrate scale to SI bench scale. But CR010 §1.2 is anchored via SAM_ON_EARTH_v1.md's SI frame lock (SI meter realized through locally measured c). **W3 passes structurally** — no additional SI conversion is missing.

## Substantive findings

1. **n = 0 is the honest mechanism-forced Home-nesting projection for the SLC bench context.** CR010 §1.2's identification of λ_spaghettio = 3.877 μm as a physical SI Compton wavelength already carries the substrate-loop-to-SI-meter conversion. No additional R^n multiplication is required to translate the base-substrate coupling reach into bench-observable reach. The Home-nesting structure exists (per CR010 §1.7-1.8), but for the SLC bench context specifically, it doesn't add a projection factor above what CR010 §1.2 already provides.

2. **The Home-nesting radix R = 12 is triply-anchored in the sealed record.** CR266 mirror linear extent, Vol I §7 A-accounting ladder, CR259 chessboard side minus one, LCQC002 register radix — four sealed CRs give R = 12 exactly. Sean Brady's 11/12→12/12 apocalyptic-edge / 2D-horizon-arrival framing is the ontological reading of this same integer. Zero free parameters in the nesting-radix identification.

3. **Alternative n = 1 lands F-iii solid at 13× floor — refused as bench-comfort retrofit.** The R = 12 nesting factor is real (per S2 sealed), but applying it once (n = 1) to the SLC bench requires a specific structural anchor — an argument that the SLC bench sits one Home-nesting level above the base substrate — which does not exist in the current sealed record. Sealing n = 1 for the comfortable bench landing would be exactly the retrofit hazard CR011 v1.0/v1.1/v1.2 iterated through. CR012 refuses.

4. **F-iii marginal is the honest S1 v2 landing.** At 1.11× floor with ~5% m_3 spectrum uncertainty propagating to ~5% in d_ref, the F-iii verdict has small headroom. An honest S1 v2 will report the ±5% uncertainty band; the bench prediction may effectively straddle the floor. **The bench can speak** — it's above floor — but the margin is not comfortable.

5. **Patent decision implications.** SLC patent Claims 2, 15, 21 can be restored under an F-iii marginal landing, but the patent language should reflect the tight margin honestly (predicted signal 8e-6 vs sensitivity floor 7e-6, ~10% headroom). Not F-iii solid claim territory. A different bench design with a tighter sensitivity floor (or a longer-averaging night) would give more comfortable margin without changing the sealed derivation.

## What this CR seals

- **n_SLC_bench = 0** as the Home-nesting projection factor for the SLC bench context.
- **d_ref_bench = 46.52 μm** as the bench-observable coupling reach.
- **Home-nesting radix R = 12** with four-way cross-consistency in the sealed record.
- **A=1=A₀ typed reset** as the cyclic-closure identity that makes Home nesting well-defined structurally.
- **Alternative n ≥ 1 candidates** documented as refused pending sealed intermediate-nesting anchors.

## What this CR does not seal

- Earth-frame Home level derivation from cosmological Home structure.
- Whether any specific matter-chain depth (CR256/CR257b framework) has a Home-nesting projection interpretation.
- The SLC patent update decision itself (waits on S1 v2 execution).

## Verdict statement

**CR012 PASS.** The Home-nesting projection factor for the SLC bench context is sealed at n = 0, giving d_ref_bench = d_ref_base = 46.52 μm. Mechanism-forced from CR010 §1.2 SI-per-loop identification + CR011 sealed base-substrate reach + no sealed intermediate nesting anchor. Zero free parameters. Zero bench-target reference in derivation. The three-CR foundational chain (CR010 + CR011 + CR012) is complete; CR-NSC-01 S1 v2 unblocks with F-iii marginal landing at H_pred(0.15 m) = 8.23e-6 vs floor 7.4e-6 = 1.11× floor.

`CR012_PASS_NESTED_HOME_DISTANCE_AS_INFORMATION_FOUNDATION_n_SLC_bench_EQUALS_0_d_ref_bench_EQUALS_d_ref_base_EQUALS_46.52_MICRO_METER_MECHANISM_FORCED_FROM_CR010_1.2_SI_PER_LOOP_PLUS_CR011_BASE_REACH_PLUS_NO_SEALED_INTERMEDIATE_NESTING_S1_V2_H_PRED_8.23e-6_VS_FLOOR_7.4e-6_LANDING_F_III_MARGINAL_1.11X_FLOOR`
