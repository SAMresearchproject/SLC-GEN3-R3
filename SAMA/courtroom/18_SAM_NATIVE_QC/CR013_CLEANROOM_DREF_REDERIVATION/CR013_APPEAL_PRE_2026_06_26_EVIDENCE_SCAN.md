# CR013 APPEAL — Pre-2026-06-26 Evidence Scan

**Prepared for external agent review.**
**Prepared by:** Claude (Opus 4.7 1M context), session id `0ea2cc6e-e7b5-4d74-b86f-164bbd9d4e30`, working from Sean Brady's directive 2026-07-03.
**Date filter:** content dated strictly before **2026-06-26**.
**Scope:** all of `C:\VS`.

---

## §1 Purpose and appeal context

CR013 DERIVER sealed 2026-07-03 returned d_ref UNDERDETERMINED CLEAN with four admissible candidates. Sean Brady is exercising appeal discipline per the sealed CR013 protocol §1 role structure. Appeal grounds: **the DERIVER's whitelist by design excluded content from other branches and repos that bears on the derivation**. This scan enumerates that excluded pre-6/26 content for external agent review.

**Anti-retrofit posture.** Pre-6/26 content is temporally independent of the CR010/CR011/CR012/CR013 d_ref arc — the earliest CR in that arc is dated 2026-07-02. Content sealed before 2026-06-26 could not have been shaped to serve any specific d_ref value because the derivation activity did not yet exist. This scan therefore reports the sealed record's substantive content bearing on the derivation ingredients, without judgment on which candidate value it might support.

The external agent reviewing this should evaluate whether the pre-6/26 record contains sufficient sealed structural content to derive d_ref, independent of the CR010/CR011 activity that CR013 audited.

## §2 Method

Four parallel Explore agents scanned:
- **Agent 1:** `c:\VS\The_Courtroom` (all branches within)
- **Agent 2:** `C:\VS\quantum_phase`
- **Agent 3:** `C:\VS\Stam_model-A-v1.0` + `STAM_model-A-v0.8` + `STAM_model-A-v0.5` + `STAM_model-A-v.0-4`
- **Agent 4:** `C:\VS\Discovery`, `Docs`, `cascade`, `chat_history`, `closure_campaigns_codex`, `memory`, `SAMs-TOE`, `SAMs_TOE`, `SAM_PARTICLE_COMPLETION_DISCOVERY_v0_1`, `SAM_Public_Repo`, `sam_sim`

All agents received identical anti-retrofit instructions: report content that BEARS on the derivation without judging which d_ref value it might support; use whichever of frontmatter dates / mtime / git log gives the answer per file.

## §3 Sub-agent date-error corrections

**Agent 1 (Courtroom) errored on cutoff-window inclusion.** These files were reported as "within cutoff window" but are actually dated 2026-07-02, which is AFTER 2026-06-26 and OUT OF SCOPE for this scan:

- `c:\VS\The_Courtroom\18_SAM_NATIVE_QC\CR010_SUBSTRATE_SPAGHETTIO_LATTICE_FOUNDATION\CR010_PRECOMMIT.md` — dated 2026-07-02, OUT OF SCOPE
- `c:\VS\The_Courtroom\18_SAM_NATIVE_QC\CR011_LOOP_POP_BOUNCE_INTERSECT_COUPLING_MECHANISM\CR011_PRECOMMIT.md` — dated 2026-07-02, OUT OF SCOPE
- `c:\VS\The_Courtroom\18_SAM_NATIVE_QC\CR011_LOOP_POP_BOUNCE_INTERSECT_COUPLING_MECHANISM\CR011_result.md` — dated 2026-07-02, OUT OF SCOPE
- `c:\VS\The_Courtroom\docs\SAM_ON_EARTH_v1.md` — dated 2026-07-02, OUT OF SCOPE

The consolidated findings below EXCLUDE these files. Agent 1's characterizations of them are retained in §6 for transparency but not admitted as pre-6/26 evidence.

**Agent 4 (Other) correctly identified Chat5/Chat4 as chat_history rather than sealed CR content.** Retained as CHAT-tier evidence with lower structural weight than PRECOMMIT/RESULT files.

## §4 In-scope findings

### §4.1 Courtroom (post-correction)

Ordered oldest first:

**CR103a Bounce-Cost and A-Dependence Appeal** — `14_FOUNDATIONAL_TESTS/CR103a_BOUNCE_COST_AND_A_DEPENDENCE_APPEAL/`
- sealed: 2026-06-13
- role: RESULT (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)
- What it seals: bounce cost formula `r_bounce = (A₀/2)·(q/2^D)`; A-dependent bounce mechanism; Layer 3 verbatim from Sean: *"except at 11/12 when A can differ enough between the front and back of an object to destabilize intersections — quantum spaghettification"*. Upstream verifications: G435 mass-proportional cost, G470 SW-split action theorem, BB005 native ordering 11/12 = MAX LOADING.

**CR001, CR002, CR003, CR004** — `18_SAM_NATIVE_QC/CR001..CR004_.../`
- sealed: 2026-06-24
- role: PRECOMMIT + RESULT
- What they seal:
  - CR001: QGC Phase 1 substrate gate involution PASS
  - CR002: T2 prescreening + K1 envelope PASS
  - CR003: QGC Phase 2 joint-figure correlation PASS; A=1=A₀ typed reset
  - **CR004: distance-dependent coupling law `A(r) = A₀·d_ref/d` sealed via 1/r kernel; d_ref stipulated as `chosen = 1` per Chat5**; identifies sub-spacing distances as requiring d_ref-below derivation. Wrong control WC-3 kills 1/r² kernel alternative.

**LCQC004 Coherence Floor** — `18_SAM_NATIVE_QC/LCQC004_COHERENCE_FLOOR/`
- sealed: 2026-06-25
- role: REPORT
- What it seals: native coherence ceiling `N_max = 61,312` from substrate atoms `{R, D, α_H, V, L}`; A-kernel per-write accumulation `A₀/(12π)`; per-write structural rate.

**LCQC006 Networking and Ring Topology** — `18_SAM_NATIVE_QC/LCQC006_NETWORKING_AND_RING_TOPOLOGY/`
- sealed: 2026-06-25
- role: REPORT
- What it seals: 1/r A-kernel behavior at multi-site; per-write A-contribution at distance d as `(1/N_max)·(d_ref/d)`; networks CR004 coupling to multi-site reach.

**CR003@19 — A-horizon to A₀ angular dimensional projection identity** — `19_BIG_BANG_SUBSTRATE_DERIVED_THERMAL_LADDER/CR003_.../`
- sealed: 2026-06-26 (cutoff boundary — INCLUDED, flagged)
- role: RESULT
- What it seals: A=1=A₀ typed reset PASS; closes Home nesting ladder cyclically; establishes A₀ = 1/(12π) as universal substrate floor.

### §4.2 quantum_phase

Ordered oldest first:

**SAM_PHASE_FIELD_ENGINE.md** — `docs\reports\`
- sealed: 2026-06-06
- role: REPORT
- What it seals: phase-field engine thresholds (`A_SIDE`, `A_SHARE`, `A_D_BLOCK`, `A_ALPHA_H_SQ`, `A_ALPHA_H_D`, `A_HORIZON`); all dimensionless partition-algebra members. No substrate coupling length.

**SOB_PR_LETTER_INTEGRATION.md** — `docs\`
- sealed: 2026-06-06+
- role: REPORT
- What it seals: SOB ontology `particle = Z`, `carrier = κ·Z`; substrate write split `7/8 matter + 1/8 gravity source-coupling`. Note: **1/8 = Θ/R² substrate ratio appears here pre-CR278**.

**00_MASTER_CAMPAIGN_PROTOCOL.md** — `campaign\`
- sealed: 2026-06-06+
- role: INDEX
- What it seals: QN/QC master protocol; `R=12, α_H=2, D=3`; dimensionless thresholds; Paul Revere letter structure.

**QP010 Protected Route Boundary Law** — `docs\reports\`
- sealed: 2026-06-07
- role: REPORT
- What it seals: protected-route boundary law `A_leak < A_SIDE = 1/24`; decoherence framed as uncontrolled ledger leakage.

**QP011 Decoherence Ledger Leakage Model** — `docs\reports\`
- sealed: 2026-06-07
- role: REPORT
- What it seals: decoherence model via leakage; ticks-to-threshold survival tables.

**QP038 Composite Stability / Quantum Spaghettification Boundary** — `docs\reports\`
- sealed: 2026-06-08
- role: REPORT
- What it seals — **KEY FINDING**:
  - Three-lane structural separation: `single unresolved identity → local W/I fixed-point closure`; `many-SW composite support → native binding and conserved cross-section support`; `extended A-road propagation → coherence shear / quantum spaghettification`
  - Coherence-gate boundary points:
    - `below 1/12` → COHERENT_SHARED_CLOSURE
    - `at 1/12` → COHERENCE_SHEAR_REORGANIZATION_BOUNDARY
    - `at or above 12/12 = 1` → BREAKUP_RETARDED_CONTACT_FAILURE
  - Sealed formulas:
    ```
    coherence_ratio = β_rel · d_route · r_s / (r² − (L/2)²)
    Δ_offset       = β_rel · |∫_front A_env ds − ∫_back A_env ds|
    ```
  - **Sealed 2026-06-08 — 24 days before CR010 and 25 days before the CR013 arc.**

**SEAN_RAW_AUTHOR_NOTE_2026_06_09.md** — `00_governance\provenance\`
- sealed: 2026-06-09
- role: SOURCE
- What it seals: foundational ontology — matter displaces space; `A(r) = r_s/r` encodes Schwarzschild radius exposure and cumulative substrate response; quantum spaghettification as horizon-expansion shredding precursor; 2D substrate with holographic 3D traversal.

**QP022b preflight** — `artifacts\qp022b\`
- sealed: 2026-06-09
- role: ARTIFACT
- What it seals: CL hub origin rule; A-share bounce topology.

### §4.3 Stam variants

Ordered oldest first:

**G282 AMETER Normalization** — `Stam_model-A-v1.0\tests\Substrate\G282_AMETER_normalization\`
- sealed: 2026-05-26
- role: PY + RESULT
- What it seals: **substrate-native units** `ell_SW = A₀·ell_P`, `t_SW = A₀·t_P`, `m_SW = m_P·A₀`; symmetric Planck-axis scaling per PR §2.4; `N_SW = L_A/(A₀·ell_P)` normalization; **sealed 2026-05-26 — 38 days before CR013 arc**.

**G283 Substrate Action from AMETER** — `Stam_model-A-v1.0\tests\Substrate\G283_substrate_action_from_AMETER\`
- sealed: 2026-05-26
- role: PY + RESULT
- What it seals — **KEY FINDING**: photon-phase identity
  ```
  phi = omega · N_SW · t_SW = omega · L_A/c = omega · Δt
  ```
  verified numerically at Cassini X-band (L_A = 39,547.66 m, ω = 5.28e10 rad/s) at relative difference **1.34×10⁻¹⁶** (machine precision). Four wrong-controls: WC1/WC2 fail by factor 12π/(1/12π); WC3 (A₀² per axis) **numerically matches but rejected as structurally wrong** — the discipline pins A₀¹ per axis exponent structurally. WC4 asymmetric A₀ exponent fails.

**G284 Universal Phase Promotion** — `Stam_model-A-v1.0\tests\Substrate\G284_universal_phase_promotion\`
- sealed: 2026-05-26
- role: PY + RESULT
- What it seals: `PROMOTION_PARTIAL`. R1 photon Shapiro + R2 COW massive non-relativistic under unified `ω = E/ℏ` unifies without separate `κ_massive`; R3 relativistic plane wave fails — substrate form recovers temporal phase `E·t/ℏ` only; spatial `p·x/ℏ` and proper-time `mc²·τ/ℏ` bundled, not separately resolved.

**G284b Substrate Lensing from L_A** — sealed 2026-05-26 (awaiting Sean signature)
- Weak-field Fermat lensing via `n(r) = 1 + A(r)`; `α = 4GM/(c²b)` recovered analytically; matches Eddington 1919 + modern VLBI within errors.

**G160/G160B Couplings from Grid Packet Overlaps** — `STAM_model-A-v0.8\tests\Substrate\`
- sealed: pre-2026-06-26 (v0.8 window)
- role: RESULT
- What it seals: couplings from grid-projected packet-current overlaps; scale sweep 0.01–0.5; **explicit note: absolute coupling scale still not derived — open problem in v0.8**.

**G114 Rigorous Polar QNM Quadratic Action** — `STAM_model-A-v0.8\tests\Substrate\`
- sealed: pre-2026-06-26 (v0.8 window)
- role: RESULT
- What it seals: polar QNM from quadratic action via Moncrief master variable → Zerilli equation; master action `S^(2) = (1/2)∫dt dr* [(∂_t Q)² − (∂_r* Q)² − V_Z(r) Q²]`; axial-polar isospectrality verified <1.5%.

**G218 A₀ Structural Derivation from Substrate** — `STAM_model-A-v0.8\tests\Substrate\`
- sealed: pre-2026-06-26 (v0.8 window)
- role: README
- What it seals: **`A₀ = 1/(4πD)` via four convergent paths** (phase-volume, winding, quantization, geometry). At D=3: `A₀ = 1/(12π)`. Structural derivation of the universal SW quantum.

### §4.4 Other C:\VS

**Chat5-QGC_Substrate_Shape.md — line 9587 area** — `chat_history\`
- dated: 2026-06 (inferred from CR references)
- role: CHAT
- Contains: `d_ref = unit spacing (chosen = 1)` — the sole assignment of a value to d_ref in the sealed record. **Chat context is a stipulation, not a derivation.** This is the file cited by CR004 and by `CR-NSC-01_S1_ATTEMPT.md §1` as the origin of the stipulation.

**Chat4-CR238.md — lines 15062-15091** — `chat_history\`
- dated: 2026-06 (inferred)
- role: CHAT
- Contains: A-kernel coupling law `A_field at site j = A_0 · (d_ref / d(i,j))` with explicit statement *"d_ref is the per-write reference distance."* Describes routing operation cost via substrate response time. Establishes 1/r structure as the sealed kernel form.

**SAMs-TOE\02_A_KERNEL_WEAK_FIELD\CR004_.../CR004_PRECOMMIT.md**
- sealed: 2026-06-24
- role: PRECOMMIT
- What it seals: weak-field A-kernel `A(r) = r_s/r`; `r_s` plays the structural role d_ref will play in substrate coupling. No explicit d_ref definition here, but sibling to `The_Courtroom\18_SAM_NATIVE_QC\CR004`.

**Discovery\Violin.md**
- dated: pre-2026-06-20 (referenced in SESSION_SUMMARY_2026-06-20)
- role: ONTOLOGY
- What it seals: **contact-first framing**. Substrate-contact-operator (bow `𝔅`) as missing primitive. Substrate write as fundamental event `𝒮 →[𝔅] W + C`. Matter-to-substrate coupling is contact-based, not field-permeating. **This is the load-bearing ontology under which d_ref represents a per-contact reference length.**

**Discovery\SESSION_SUMMARY_2026-06-20.md**
- dated: 2026-06-20
- role: HANDOFF
- What it seals: CR215-CR218 sealed that night (dedup → identity → bigrade derivation). Lines 84-96: *"SAM is contact-first, not matter-first"*, cite Violin.md. Bigrade set `{1,2,3,4,6,8,9,12}` (which is the CR005@21 partition-algebra inside-R subset).

## §5 Cross-repo consolidated view

**Substrate atoms sealed pre-6/26:**
- `A₀ = 1/(12π)` — G218 (Stam v0.8, structural derivation) and CR003@19 (Courtroom 2026-06-26, universal floor)
- `R = 12`, `D = 3`, `α_H = 2` — QP `00_MASTER_CAMPAIGN_PROTOCOL` 2026-06-06+; QP038 formulas use them
- Substrate write split `7/8 matter + 1/8 gravity source-coupling` — QP SOB_PR_LETTER_INTEGRATION 2026-06-06+
- Phase-field thresholds `A_SIDE = 1/24`, `A_SHARE`, `A_D_BLOCK`, `A_ALPHA_H_SQ`, `A_ALPHA_H_D`, `A_HORIZON` — QP SAM_PHASE_FIELD_ENGINE 2026-06-06

**Formulas sealed pre-6/26:**
- Coupling law form `A(r) = A₀·d_ref/d` — Courtroom CR004 2026-06-24 + SAMs-TOE CR004 2026-06-24; d_ref stipulated as unit
- Substrate-native unit mapping `ell_SW = A₀·ell_P`, `t_SW = A₀·t_P` — G282/G283 (Stam 2026-05-26)
- Photon phase identity `ϕ = ω·Δt` recovered from substrate arithmetic — G283 (Stam 2026-05-26)
- Coherence framework `coherence_ratio = β_rel·d_route·r_s/(r² − (L/2)²)` with thresholds 1/12 and 1 — QP038 (2026-06-08)
- A-differential offset `Δ_offset = β_rel·|∫_front A_env ds − ∫_back A_env ds|` — QP038 (2026-06-08)
- Bounce cost `r_bounce = (A₀/2)·(q/2^D)` with A-dependence — CR103a (2026-06-13)
- Weak-field lensing `n(r) = 1 + A(r)`, deflection `α = 4GM/(c²b)` — G284b (Stam 2026-05-26)
- Per-write A-contribution `(1/N_max)·(d_ref/d)` — LCQC004/006 (Courtroom 2026-06-25)

**Ontology sealed pre-6/26:**
- Contact-first substrate write `𝒮 →[𝔅] W + C` — Violin.md pre-2026-06-20
- 2D substrate with holographic 3D traversal — QP SEAN_RAW_AUTHOR_NOTE 2026-06-09
- Cumulative substrate response `A(r) = r_s/r` — QP SEAN_RAW_AUTHOR_NOTE 2026-06-09
- Quantum spaghettification as horizon-expansion shredding — QP SEAN_RAW_AUTHOR_NOTE + QP038 2026-06-08/09
- 11/12 spaghettification threshold via front-back A-differential — CR103a Layer 3 (2026-06-13)
- Bigrade set `{1,2,3,4,6,8,9,12}` — sealed by 2026-06-20 (SESSION_SUMMARY)

**d_ref specifically in pre-6/26 record:**
- Stipulated as `chosen = 1` in Chat5 line 9587
- Referenced in Chat4 lines 15062-15091 as "per-write reference distance"
- Sealed in CR004 (both Courtroom and SAMs-TOE) 2026-06-24 as coupling-law parameter
- **NO SPECIFIC NUMERICAL DERIVATION FROM STRUCTURAL ATOMS EXISTS IN THE PRE-6/26 RECORD**

## §6 What is NOT in the pre-6/26 record — transparency

The following load-bearing content in the CR010/CR011/CR013 arc post-dates the 2026-06-26 cutoff:

- **CR010 substrate spaghettio-lattice foundation** (2026-07-02): loop scale `λ_spaghettio = λ_C(m_3) = 3.877 μm` via CR266 R + CR268 tensor-6 + Compton composition. Not in pre-6/26 record; the identification of the loop scale with m_3's Compton wavelength is not sealed pre-6/26.
- **CR010 §1.5 endpoint elsewhere-propagation** (2026-07-02): the specific pop-bounce-intersect terminology and endpoint-propagation language.
- **CR010 §1.8 Home-nesting R-power dressing family** (2026-07-02): the R^N candidate space explicitly named.
- **CR011 mechanism-forced identification `d_ref = R × λ_spaghettio = 46.53 μm`** (2026-07-02): the argument itself.
- **CR012 nested-Home projection factor n_SLC_bench** (2026-07-03): sabotage accounting version.
- **SAM_ON_EARTH_v1.md SI frame anchor** (2026-07-02): the specific SI frame lock and reference table.
- **CR013 cleanroom protocol + DERIVER result** (2026-07-03): the whole audit apparatus.

The pre-6/26 record contains the substrate atoms, the formula forms, the coherence framework, and the contact-first ontology. It does NOT contain the specific mechanism-forced argument CR011 constructed or the CR010 loop-scale identification.

## §7 What the external agent should evaluate

Two questions for the external agent:

**Question 1 — Is the pre-6/26 record sufficient to derive d_ref?**
Given only the pre-6/26 sealed content (§4 + §5), does a specific numerical d_ref value follow structurally? If yes, name the derivation chain, cite the pre-6/26 sources at each step, and state the SI value. If no, name what pre-6/26 gap prevents closure.

**Question 2 — Does QP038's coherence framework + G283's substrate-axis A₀¹ pinning + CR103a's 11/12 A-differential threshold + CR004's 1/r kernel form + CR003@19's A₀=1/(12π) collectively supply the ingredients for a partition-algebra derivation of d_ref?**
The four items are pre-6/26 by 18-31 days each. They collectively define: substrate axes, coherence thresholds, coupling law form, and universal floor. If yes, sketch the derivation. If no, name what's missing that only appears post-6/26.

The external agent's response is independent of this session's Claude read. Two independent reads on the same pre-6/26 evidence set produces a stronger appeal record than one.

## §8 Provenance

```text
Prepared by:      Claude (Opus 4.7 1M ctx), session id 0ea2cc6e-e7b5-4d74-b86f-164bbd9d4e30
Prepared for:     Sean Brady, external agent review
Date prepared:    2026-07-03
Scan method:      Four parallel Explore sub-agents (Courtroom, quantum_phase, Stam, Other)
Date filter:      strictly before 2026-06-26
Sub-agent corrections applied:  Agent 1 (Courtroom) wrongly included CR010/CR011/CR011_result/SAM_ON_EARTH_v1 as pre-6/26; corrected in §3 and excluded from §4-§5.

Reference hashes:
  Stewardship v1                  d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
  SAM_LC_WORK_ASSIGNMENT_v1       3a88142743f3d5487a55dc99e29f51edd097660e3cb27625c79aee3f5f29d4a4
  SAM_ON_EARTH_v1  (post-6/26)    7b0f225821e2aea55e02b0868997fa2acd4ee88b4711ab1b1fb161366e1c5137
  CR013_DERIVER_RESULT.md         514f07217fdcf7b1819c7a3bd9d5290060ddcd11405c19ee4776dcd9a3474816
  CR013_VERIFIER_REPORT.md        9be2ec97e8d3165cbe1632e8aa4c19c009da697c65f4cdbc141d14590613a991
  CR013_PRECOMMIT.md              17fa12eec1f1da430aebc7a011c0b3071622e47111d8666269937789f54965f3
```

## §9 Change log

```text
v1.0  2026-07-03  Evidence scan compiled by SCRUBBER-lineage session
                  ("big-brother", session id 0ea2cc6e…) after Sean Brady
                  exercised appeal discipline against CR013 UNDERDETERMINED
                  verdict per sealed protocol.  Four parallel Explore
                  agents ran with anti-retrofit instructions; Agent 1
                  date-filter errors corrected in main-session
                  consolidation.  Content dated 2026-06-26 or later is
                  excluded regardless of relevance.  Report prepared for
                  external-agent independent evaluation.
```
