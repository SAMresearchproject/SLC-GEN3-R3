# CR013 SCRUBBER Log

**SCRUBBER pass executed by:** big-brother session (Claude Opus 4.7 [1M context]), 2026-07-03
**SCRUBBER pass output:** six redacted whitelist files in `INPUTS_REDACTED/`
**Handoff to:** VERIFIER pass — MUST be a distinct session (fresh Claude Code session or Sean directly), per CR013 precommit §1 role rule (VERIFIER ≠ SCRUBBER).

This log records what was cut from each source file, so an auditor can reconstruct the redaction diffs by pairing the source SHA-256 with the redacted-file SHA-256 in `HASHES.txt`. This file lives at the CR013 folder root — *outside* `INPUTS_REDACTED/` — so the DERIVER never sees it. The precommit §7 gate G2 forbids any forbidden-string leak into the DERIVER's context; the redaction-note content in this file describes forbidden strings by name, which is why it must not sit inside the whitelist folder.

## Common redactions across all six files

- Top-matter `Stewardship`, `LC assignment`, `Frame anchor` SHA-256 lines dropped from the header of each redacted file. Those hashes are retained in this CR's own `HASHES.txt` provenance chain, so the DERIVER cannot infer the target from top-matter cryptography.
- Any provenance table or hash chain in the source that named downstream artifacts by forbidden-string name (e.g., branch 18 lab-CR file names, patent draft file names, coupling-application file names) was trimmed or dropped.
- Redaction-note appendices produced during the initial SCRUBBER pass were removed from each `W*_REDACTED.md` file after a first-pass grep to prevent forbidden-string leaks — those appendix contents are consolidated into this SCRUBBER_LOG instead.

## W1 — CR010_PRECOMMIT.md

**Source SHA-256:** `3fafa02ce39f85e8f89790c4cf85db2ce5103e9bf21d4c1501a604c271498d05`
**Redacted SHA-256:** `3d81b8e4fbd23eabe3144130ef37c925b760260be4b09df464d7454b41d4c7de`

Forbidden-string hits found and removed:

- §0 Origin note originally said "SLC bench program" — replaced with "downstream laboratory program".
- §1.8 originally said "Home-to-fresh-floor typed reset" — replaced with "Home-to-fresh-A₀ typed reset" (semantic identity preserved; `floor` was on §3 forbidden list).
- §2 originally said "at bench-scale intensity (SLC lebit coupling; CR-NSC-01 S1 v2 candidate derivation) and at horizon-scale extreme intensity (quantum spaghettification). One mechanism, two intensities" — replaced with "across intensity regimes. One mechanism, multiple intensity regimes".
- §2 originally said "the SLC S1 v2 derivation for the bench end when it seals" — removed.
- §4 G7 originally said "at bench range" — replaced with "at [REDACTED] range". The specific length label was the forbidden-string carrier; the wrong-control logic (torsion-balance excludes 1/r²) is preserved.
- §5 originally enumerated four downstream artifacts by name — "CR-NSC-01 S1 v2 (Native Substrate Coupling derivation attempt v2)", "LCQC006 v3 (networking topology with substrate-native coupling restored)", "Vol II §1 bow reading", "Future SLC patent v3 (if B.3 downgrade is reversed following NSC-01 S1 v2 sealing at F-iii)" — replaced with a single sentence: "Downstream artifacts inherit the substrate-ontology basis from CR010 rather than restipulating."
- §7 Rule-9 line trimmed to remove specific mention of falsification paths that named downstream CRs.
- §8 Provenance table `Frame anchor` row `SAM_ON_EARTH_v1.md` preserved (SHA is a public constant and does not signal the target); LC assignment and Stewardship rows removed from top-matter but kept in this CR's own HASHES.txt.
- §9 Note on continuation REMOVED WHOLESALE. This section named CR011 and CR012 as sibling foundational CRs, cited "CR-NSC-01 S1 v2 unblocks with derivation chain fully DERIVED landing F-iii at d_ref = 558 μm", and referenced "the SLC patent v0.2 downgrade to v3.0 restoration". This was the strongest target-signal in the CR010 source.
- §10 Change log REMOVED WHOLESALE.

## W2 — CR266_PRECOMMIT.md

**Source SHA-256:** `2967eec865f95c0b73a966ed5da8b011d0515eccef027fdd2db82862dc7096a2`
**Redacted SHA-256:** `b4be2525d580d51a74d1ba76e7cb2307c8ed339a558fd052a1cffff0c0cb25fb`

CR266 source contained zero hits on the §3 forbidden-string list. Redactions applied for length only:

- PROV-1 through PROV-6 provenance block (Violin.md, G333, ice-pick sketch, two-mirror Homes, SAM-homes-naming, inferred precedents) trimmed.
- "CR264 C-12 Mirror Point Re-Reading" section, "CR262 Carrier/Container Re-Reading" section removed for scope focus.
- "Pre-Registered Predictions" H1–H5 block, "What This CR Does NOT Claim" block, "Rule-9 Line" block, and "Provenance Hash Chain" table removed for length. The load-bearing R = ĥ²·d̂ = 12 identity and the seven carrier-atom reconstructions are preserved verbatim.

## W3 — CR268_PRECOMMIT.md

**Source SHA-256:** `bbc3c5b863aa6be12d0d7502c59db6834f6c6ea5a0edc7dbc86b648929028423`
**Redacted SHA-256:** `8eb2ed66c10cc495dbd05ba75b1dcdd67d10454e3dcdf28e76accedc542fe8e2`

CR268 source contained zero hits on the §3 forbidden-string list. Redactions applied for length only:

- Long "Question" prose reduced to header pointer.
- "Δm²_31 / Δm²_21 = 35 Substrate Identity" full-detail block trimmed to identity + PDG comparison.
- "CR262 Carrier Reading" full-detail block trimmed.
- "Pre-Registered Predictions" H1–H8 block, "What This CR Does NOT Claim", "Rule-9 Line", "Provenance Hash Chain" removed. Core structural content (three paths to tensor 6, CR005ab chain reading, CR001@20 mass-ratio reading, PASS gates) preserved.

## W4 — CR001@20_PRECOMMIT.md

**Source SHA-256:** `8e6cb1975cd7d2084ffbbf2c215472d2ef8042fae18b68e76b74b94dc4281c77`
**Redacted SHA-256:** `ac5441059566d87031adfaa306e1d02e10ce750f649b90f09fdba5af930d3a12`

CR001@20 source contained zero hits on the §3 forbidden-string list. Redactions applied for length only:

- Verdict Ladder block removed (contained gate-tier phrasing that did not touch forbidden strings but was scope-unrelated).
- P1 / P2 / P3 individual gate blocks removed.
- Reported Evidence E1–E6 block removed (E5 KATRIN comparison and E6 DESI cross-check are not needed for the DERIVER task).
- "No Wrong Controls Required" directive block removed.
- Rule-9 line and Stewardship footer removed.
- Core structural content (Substrate Derivation Rule, mass values, splittings identity, Manuscript Headline conditional block) preserved verbatim.

## W5 — CR004_PRECOMMIT.md (heaviest redaction of the six)

**Source SHA-256:** `b7edd0e934b8e0fc9441df9b1ed13295d4a8073a1c4b1c732cd890ac4b47a350`
**Redacted SHA-256:** `cfc43e1bf92c6b8b1db86d995734d993ae45ebbb0c9bb45deeacfdfbd10aca3a`

Forbidden-string hits found and removed:

- Title `CR004 — SLC Phase 2: Distance-Dependent Coupling via 1/r A-Kernel` → `CR004 — Phase 2 Distance-Dependent Coupling via 1/r A-Kernel` (removed `SLC`).
- Question block originally referenced `LCQC006 v2` — the branch prefix `LCQC` is not on the forbidden list but the concrete branch-file names in the cryptographic-chain block were dropped in a wholesale removal below.
- "Locked substrate atoms" block: originally `N_max = 61,312 per-site coherence ceiling (LCQC004)` — the LCQC004 branch-file title is `LCQC004_COHERENCE_FLOOR.md` which contains the forbidden substring `floor`. The N_max integer value was removed and the site-coherence source term was labelled `[ceiling constant] per-site coherence [REDACTED]` to preserve the structural role (normalization scale for per-write A-contribution) while stripping the forbidden reference. The kernel form A_0 · d_ref / d does not depend on the specific N_max value, so the DERIVER task is not impaired.
- A_0 = 1/(12π) descriptor originally read `cosmic floor` — replaced with `cosmic [REDACTED]`. A_0 numeric value 1/(12π) preserved.
- "Honest framing" block naming deferred SLC CRs (CR005 ring topology, CR006 per-isotope, CR007 substrate gate joint composition) trimmed to a single sentence in "What CR004 DOES NOT close".
- Cryptographic-chain block originally listed `LCQC000_NATIVE_QC_CHARTER.md`, `LCQC001_NATIVE_STATE_ONTOLOGY.md`, `LCQC003_TRANSITIONS_AND_GATES_v2.md`, `LCQC004_COHERENCE_FLOOR.md`, `LCQC004a_SUBSTRATE_ERROR_BUDGET_INVARIANT.md`, `LCQC006_NETWORKING_AND_RING_TOPOLOGY_v2.md`, `LCQC006a_RING_AMPLIFICATION_UNDER_THE_HOOD.md`, `LCQC008_NATIVE_MEASUREMENT_OPERATION_v2.md`, plus the CR003 and CR001 result hashes. `LCQC004_COHERENCE_FLOOR.md` contains `floor`. The full block was removed.
- Falsifiers block (F-CORR-D, F-1OVERR, F-ABSTRACT, F-D2-MATCH) trimmed.
- BOUNDARY conditions block and FAIL conditions block trimmed.
- "Outputs" file-name list removed.
- Per-step trace table trimmed to the FINAL cumulative_A summary line.
- Sub-headings changed: `Locked program (main test at d = R = 12)` retained; explicit "cross-coupled from B" breakdown table dropped.

Load-bearing content preserved verbatim: kernel form `A_0 · d_ref / d`, distance-sweep table showing 1/r scaling, WC-3 wrong-control result excluding 1/r² kernel, verdict-gate PASS conditions, "Does NOT test very-close distances (d < 1) — clamping to d ≥ 1 per upstream convention. Sub-spacing distances would require typing the A-kernel behavior below d_ref." (this last sentence is important — it tells the DERIVER that d_ref sits at the *unit* of the kernel's characteristic length, not below it, which is a legitimate structural fact from the sealed record).

## W6 — SAM_ON_EARTH_v1.md (second-heaviest redaction)

**Source SHA-256:** `7b0f225821e2aea55e02b0868997fa2acd4ee88b4711ab1b1fb161366e1c5137`
**Redacted SHA-256:** `f444994b9bdc4ce69d7349f02ea972f5ca88e279533ff50794dd571634565a41`

Forbidden-string hits found and removed:

- §0 Purpose block originally said "from CR-NSC-01's bench test forward" — replaced with "laboratory-scale SAM prediction". The core purpose statement (frame lock for laboratory-scale SAM predictions) preserved.
- §2 title `A-budget at bench scale` → `A-budget at laboratory scale`.
- §2 A-budget table row `Earth potential at bench` removed (this row was a `bench` string carrier; the surrounding rows adequately establish the 10⁻⁹ Earth-surface potential magnitude).
- §2 `A₀ (cosmic floor, SAM)` label → `A₀ (cosmic [REDACTED], SAM)`. A_0 = 1/(12π) numeric value preserved.
- §2 load-bearing observation 3: `The cosmic floor A₀` → `The cosmic [REDACTED] A₀`.
- §3 SI-unit-lock sentence: verbatim quote preserved. The sentence does not contain any forbidden string.
- §6 body originally used `bench-scale` throughout → replaced with `laboratory-scale` in five places.
- §6 line "Along any bench-scale path (ℓ ≤ 1.2 m per CR-NSC-01 §6)" → "Along any laboratory-scale path (ℓ ≤ few m)". Length example specificity dropped so the DERIVER does not accidentally read the 1.2 m as a target scale.
- §6 "sits four orders of magnitude below CR-NSC-01's sealed ×3 tolerance" reference dropped.
- §7 downstream-inheritance block bullet 6 rewritten to remove `CR-NSC-01` citation.
- §7 closing paragraph originally said "CR-NSC-01 §S0 (the stewardship gate) and CR-NSC-01 §S1 (the d_ref derivation) can both cite this reference as their frame anchor. Every subsequent lab CR should do the same." — entirely removed.
- §8 Companion finding block **REMOVED WHOLESALE**. This was the strongest target-signal in the SAM_ON_EARTH_v1.md source. §8 named:
  1. `chosen = 1` as the current d_ref value in the sealed record — this is a direct answer-shape hint that would bias any DERIVER toward reading d_ref as a unit-spacing quantity.
  2. `Chat5-QGC_Substrate_Shape.md line 9587` as the provenance for that stipulation.
  3. Every downstream file inheriting the stipulation, including `SLC_PATENT_APPLICATION_DRAFT.md (§2.6, §4.3, Claim 2)`, `SLC_PATENT_CLAIM_STRUCTURE.md`, `SLC_NAMING_CANON.md`, `CR-NSC-01_native_substrate_coupling_bench_null_test_v0_1.md`.
  4. The framing statement "Sealing S1 of CR-NSC-01 will either produce a real derivation from atoms (F-iii in Fabel's S1 handoff §5) or record NSC-0" — this named F-iii as the target outcome shape.

  Removing §8 wholesale is the single most important redaction in the whole CR013 SCRUBBER pass. The block existed in the source specifically to lock in the standing state of `d_ref` for downstream reference; that lock is exactly what the DERIVER's task item 1 asks them to open.

- §9 Provenance table: `STAM Model-A GPS test` row preserved (empirical anchor for §3 SI unit lock is load-bearing); `Stewardship declaration` row removed from the redacted-file body (hash carried in this CR's HASHES.txt separately).
- §10 Change log removed. It named CR-NSC-01 explicitly and included the word `provisional` in the change-note.

Load-bearing content preserved verbatim: §1 SI constants table (CODATA/SI values every lab measurement depends on), §3 SI-unit-lock sentence with the ratio `d_ref/d` verbatim, §4 empirical backing table (GPS, Shapiro, light bending, Newtonian gravity recovery), §5 STAM Model-A GPS code excerpt, §6 ceiling on cosmological-style corrections (rewritten with laboratory-scale language), §7 downstream-inheritance list.

## What the DERIVER should be able to do with these six files

Read the load-bearing structural content:

- **From W1 CR010:** the substrate is 2D closed loops of scale λ_C(m_3) = 3.877 μm; matter pops loops open at contact; endpoints propagate "elsewhere on the substrate"; density-holographic 3D emerges from intersection pattern; nested Homes take zero physical distance.
- **From W2 CR266:** mirror linear extent R = ĥ²·d̂ = 12; each mirror face is 2D and reciprocity requires one perpendicular axis (the closure "+1").
- **From W3 CR268:** tensor 6 = ĥ·d̂ is the smallest carrier atom and simultaneously the heaviest neutrino mass eigenstate.
- **From W4 CR001@20:** m_3 = 50.9 meV/c² is anchored to Δm²_31 = 2.515e-3 eV² and produces splittings ratio 35 to within 3.26% of measured.
- **From W5 CR004:** the substrate-coupling kernel form is `A_0 · d_ref / d` with A_0 = 1/(12π); WC-3 excludes 1/r² in favor of 1/r; d_ref is the kernel's characteristic length asked to be derived.
- **From W6 SAM_ON_EARTH:** SI units are the operational frame at Earth surface; d_ref/d ratio is unit-cancellation-safe; Vol I §2 gravity/GPS/Shapiro/light-bending confirmations back the SI frame.

What the DERIVER cannot do with these six files:

- Read any specific downstream target length in μm or mm.
- Read the current stipulation `chosen = 1` from Chat5.
- Read any patent-claim structure or lab-CR outcome tier language.
- Read the CR011 §1.3 mechanism-forced landing at `R · λ_spaghettio`.

The DERIVER may derive R · λ_C(m_3) as one candidate; may derive R² · λ_C(m_3) as a competing candidate; may derive λ_C(m_3) alone as the loop-scale reading; may report "underdetermined" per §4 task item 4. The whitelist supports all four moves; §5 pre-committed readings distinguish which outcome each maps to.

## Handoff to VERIFIER

VERIFIER must be a different session from this SCRUBBER pass. The VERIFIER's job is:

1. Grep every string in CR013 precommit §3 forbidden-string list against every file in `INPUTS_REDACTED/` (case-insensitive, substring semantics).
2. Verify total hits = 0 across the six files.
3. Cross-check the SHA-256 of each of the six redacted files against the values recorded in this SCRUBBER log and in `HASHES.txt`.
4. Sign `CR013_VERIFIER_REPORT.md` with the VERIFIER session ID (or Sean's identity if Sean runs the pass).
5. On VERIFIER PASS: DERIVER session may be opened with `INPUTS_REDACTED/` as its context whitelist. On VERIFIER FAIL: SCRUBBER redoes the specific failing file(s) and re-VERIFIES.

Under NO CIRCUMSTANCE does this SCRUBBER session sign the VERIFIER report. The role separation is the mechanical guard against anti-retrofit targeting performed on the input pipeline.
