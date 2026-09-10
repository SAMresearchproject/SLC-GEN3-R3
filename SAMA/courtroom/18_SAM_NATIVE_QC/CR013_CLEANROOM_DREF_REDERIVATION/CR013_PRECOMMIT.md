# CR013 — Cleanroom d_ref Re-Derivation (Context-Blind DERIVER)

**Branch:** 18_SAM_NATIVE_QC
**Classification:** PROTOCOL_CR (methodology + input-preparation; the load-bearing derivation itself runs in a fresh, context-blind DERIVER session and is graded separately)
**Stewardship:** `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88`
**LC assignment:** `3a88142743f3d5487a55dc99e29f51edd097660e3cb27625c79aee3f5f29d4a4`
**Frame anchor:** `7b0f225821e2aea55e02b0868997fa2acd4ee88b4711ab1b1fb161366e1c5137`
**Origin:** Chat-side Claude (Fabel 5 register) drafted `CLEANROOM_DREF_PROTOCOL_v1_0.md` at Sean Brady's direction after CR012 v1.0 was identified as sabotage of the structural test by SLC-bench targeting (`CR012_SABOTAGE_ACCOUNTING.md`, sealed 2026-07-03).

---

## §0 Why this CR and not a rewrite of CR012

CR012 v1.0 sealed downstream-verdict content (bench distances, sensitivity floors, patent-decision language, verdict labels) into what was supposed to be a structural-foundation CR. The sabotage accounting document in `CR012_NESTED_HOME_DISTANCE_AS_INFORMATION_FOUNDATION/` records the failure mode named **structural-seal sabotage via downstream targeting**; CR012 v1.0's sealed files remain on the record as-is, per Sean's direction not to rewrite.

CR011 §1.3's mechanism-forced identification (`d_ref_base = R · λ_spaghettio`) is also open to the audit critique that a sufficiently capable drafting agent with the SLC bench window in context can produce derivation text indistinguishable from honest work — including text that conspicuously refuses comfortable landings. Sean called this **anti-retrofit targeting**: performing conservatism toward a known target is itself targeting, and it is textually invisible. No textual re-audit of CR011 can settle §1.3.

CR013 exists to construct the one audit class immune to this hazard: a re-derivation in an agent-context where the target does not exist. Where CR011 landed a value with the target in context, CR013 asks whether that same value falls out of the sealed record with the target removed.

The CR012 sabotage accounting standing directive is preserved: CR013 does not rewrite or unseal CR011 or CR012 v1.0. It does not settle downstream bench decisions. It runs a re-derivation, records the outcome against §5's pre-committed readings, and stops.

## §1 Roles (verbatim from protocol v1.0 §1)

```text
DERIVER   = a fresh agent session (Claude Code, new context, no memory of
            this project beyond the whitelist below).
SCRUBBER  = a separate session (or Sean) that prepares redacted inputs.
VERIFIER  = a third pass (Sean, or another fresh session) that greps the
            prepared context for the forbidden strings before the DERIVER
            session opens. VERIFIER ≠ SCRUBBER.
OPERATOR  = Sean. Operator answers NO physics questions during the DERIVER
            session. The only permitted reply to any technical question is:
            "consult the sealed record provided." (This encodes the rule
            Sean enforced during the CR012 session: results must not hinge
            on the operator's memory, and an agent fishing for the
            operator's recalled beliefs is anchoring, not deriving.)
```

**Role bookkeeping for this seal:** the current "big-brother" session (working from the full project context) is executing SCRUBBER. The VERIFIER pass is a separate handoff — either Sean or a fresh session running the grep script and countersigning `CR013_VERIFIER_REPORT.md`. Under no circumstance does the SCRUBBER's own after-the-fact grep count as the VERIFIER pass.

## §2 Context whitelist (redacted copies only) — SCRUBBER output

The DERIVER receives ONLY the following, prepared by SCRUBBER as files in `INPUTS_REDACTED/`:

```text
W1  CR010_PRECOMMIT.md        (§"continuation"/downstream sections removed)
W2  CR266_PRECOMMIT.md        (primitive reduction, d̂ from ĥ; R = ĥ²·d̂ identity)
W3  CR268_PRECOMMIT.md        (tensor-6 heaviest-neutrino identification)
W4  CR001@20_PRECOMMIT.md     (neutrino spectrum, m_3 anchor to Δm²_31)
W5  CR004_PRECOMMIT.md        (kernel form A₀·d_ref/d; §"bench"/floor lines removed)
W6  SAM_ON_EARTH_v1.md        (SI frame anchor)
```

Redaction rule (SCRUBBER): where a forbidden string (§3) appears, either the enclosing section is removed wholesale or the sentence is blanked with a `[REDACTED]` marker that carries no citation back to CR013 or to the target. Structural equations and integer identities not carrying forbidden strings survive unredacted. Redaction is textually visible to the DERIVER as blank slots or removed sections — this is intentional; hiding that redaction happened would be a form of the same anti-retrofit hazard, but the DERIVER has no way to reconstruct what a redacted slot contained without external input.

## §3 Forbidden strings (must appear NOWHERE in the DERIVER's context)

```text
"CR-NSC" · "NSC" · "SLC" · "lebit" · "bench" · "patent" · "floor" ·
"7.4e-6" · "0.15 m" · "46.5" · "46.52" · "558" · "F-iii" · "F-ii" ·
"sensitivity" · "provisional" · "claim 2" / "claim 15" / "claim 21"
```

The VERIFIER greps the prepared context for every string above (case-insensitive, whole-word or substring per the string), records the (expected-empty) result in `CR013_VERIFIER_REPORT.md`, and records the SHA-256 of each redacted input file in `HASHES.txt` before the DERIVER session opens. Note: `"3.877"`, `"3.88"`, `"λ_C(m_3)"`, `"λ_spaghettio"`, `"m_3"`, `"R = 12"`, `"ĥ"`, `"d̂"` are NOT forbidden — they are sealed upstream inputs (CR010 §1.2 and CR266), not targets. The targets are the reach multiple (R^k factor selection) and any specific length answer at μm or mm scale.

## §4 The task statement (given to the DERIVER verbatim, sealed)

```text
From the provided sealed record only:

1. Derive the base-substrate coupling reach d_ref of the write-to-read
   pop-bounce-intersect mechanism (CR010 §1.4–1.6), as a specific number
   in SI meters, with a tier-tagged chain
   (ATOM / COMPOSED / DERIVED-with-citation / FITTED).

2. State whether translating that base reach into the SI scale of a
   laboratory apparatus requires any additional projection factor
   (e.g., a nesting or level factor), and if so, derive its value from
   the record with the same tier tagging.

3. State explicitly whether the reach depends on the density or rate of
   pop events (CR010 §1.5's termination condition is cross-reunion with
   endpoints of OTHER pops, which is density-dependent; §1.2's
   self-reunion route is the dilute limit). If the reach is
   density-dependent, give the functional form.

4. If the record underdetermines any of the above, say so plainly and
   enumerate the admissible candidate set, with what additional sealed
   content would select among them. "Underdetermined" is a fully
   acceptable answer and grades CLEAN.
```

The DERIVER is not told why the task is being run, that a prior derivation exists, or that any laboratory apparatus is planned. Operator answers no physics questions in-session (see §1 OPERATOR rule).

## §5 Pre-committed readings (this section hash-locked at seal time)

```text
OUTCOME A — DERIVER lands R · λ_C(m_3) ≈ [redacted value] (± m_3 band),
  zero FITTED steps, and answers the nesting question with the same
  chain:
  → CR011 §1.3 is vindicated as mechanism-forced. The voided CR012
    answer is regenerated cleanly. Primary target = the DERIVER's value.

OUTCOME B — DERIVER lands a different specific value:
  → CR011 §1.3 demoted to one admissible reading. Both values enter
    the downstream grid as rival sealed predictions. Candidates within
    3× of each other are treated as one band.

OUTCOME C — DERIVER reports underdetermined + candidate set:
  → CR011 §1.3 demoted to one admissible reading; the chain is
    descriptive-until-measured. Downstream test runs as a MEASUREMENT
    of d_ref over the candidate grid. Patent-limb strikes on the SLC
    application remain in force until data selects a value.

ALL OUTCOMES: the density-dependence answer (task item 3) is recorded
as a standing finding and becomes a pre-registered downstream knob
(predicted H vs. source write rate) in the successor downstream CR,
whichever outcome occurs.
```

(Note: the reach-multiple value at Outcome A is deliberately not restated numerically in this precommit body, so that a leak from this file into the DERIVER's context would not itself telegraph the target. The value is fixed by CR011 §1.3 and CR010 §1.2 as sealed and can be read at seal time by any auditor with access to those CRs, which the DERIVER does not.)

No outcome unseals CR011; no outcome unseals CR012 v1.0; no outcome redesigns downstream apparatus except the primary-target annotation, because the successor downstream CR is designed to bracket the full candidate grid regardless.

## §6 What this protocol does not do

- Does not rewrite, unseal, or grade CR011.
- Does not touch CR012 v1.0's sealed files (its own accounting already voids it for composition).
- Does not design or gate the downstream apparatus (that is the successor downstream CR's job).
- Does not treat Outcome A as apparatus-grade proof: a vindicated derivation still meets the substrate at the successor downstream CR before any patent claim struck by CR-NSC-01 S1's F-i landing is considered for restoration.

## §7 Gates on the SCRUBBER + VERIFIER pass (this CR seals these; DERIVER outcome sealed separately)

```text
G1  Whitelist coverage. Exactly W1..W6 as enumerated in §2 are present
    in INPUTS_REDACTED/. No additional files. No file from outside the
    whitelist is included by mistake.

G2  Forbidden-string grep (VERIFIER). Every string in §3 grepped
    case-insensitively across INPUTS_REDACTED/*.md returns zero hits.
    The VERIFIER report records the grep command, per-string count
    (all must be 0), and total lines scanned. VERIFIER session ID or
    signature is distinct from SCRUBBER session.

G3  SHA-256 record. Each of the six redacted files has its SHA-256
    recorded in HASHES.txt alongside the source-file SHA-256 (so an
    auditor can reproduce the redaction). Source-file SHA-256s are
    pulled from their branch HASHES where available.

G4  Structural equations preserved. In each redacted file, the sealed
    substrate-atom identities that the DERIVER may compose are still
    readable (e.g., R = ĥ²·d̂ = 12, m_3 identifications, kernel form
    A(r) = A₀·d_ref/d, SI-frame constants table). Redaction did not
    strip mathematical content the task requires.

G5  Role separation. SCRUBBER and VERIFIER are distinct passes.
    VERIFIER ≠ SCRUBBER is recorded in VERIFIER report.

G6  Task statement locked. §4 verbatim task statement matches this
    precommit at DERIVER open time; no wording drift.

G7  Provenance chain. Stewardship + LC assignment + frame anchor +
    CR010 hash + CR266 hash + CR268 hash + CR001@20 hash + CR004 hash
    + SAM_ON_EARTH_v1 hash present in HASHES.txt.

PASS (SCRUBBER+VERIFIER pass only)  iff G1-G7 all hold.

FAIL (SCRUBBER+VERIFIER pass only)  iff G1 misses a whitelist file,
    OR G2 finds any forbidden-string hit, OR G3 omits a SHA-256, OR G4
    strips a required identity, OR G5 collapses roles, OR G6 drifts
    §4, OR G7 misses a required hash.

The DERIVER's own outcome (A / B / C per §5) is sealed as a separate
result artifact in a later pass; this precommit gates only the setup.
```

## §8 Timing rule (hard)

This protocol must complete and seal — SCRUBBER + VERIFIER + DERIVER session + DERIVER result — before any downstream apparatus produces data. A cleanroom number sealed after apparatus data exists is postdiction and grades UNGRADEABLE. Parts may be *ordered* and the successor downstream CR may be *drafted* in parallel; data-taking waits.

## §9 What this CR seals

**On PASS of §7 gates (SCRUBBER + VERIFIER pass):** the DERIVER input package is certified as target-blind under §3, and the DERIVER session is unblocked. The DERIVER's substantive result (Outcome A / B / C per §5) is sealed by a separate artifact `CR013_DERIVER_RESULT.md` produced after that session runs.

**On FAIL of §7 gates:** the SCRUBBER pass must be redone (specific failing gate is fixed and re-verified). The DERIVER does not open until §7 PASS is on the record.

**Not sealed by this CR (deferred):**
- The DERIVER's numerical answer (deferred to `CR013_DERIVER_RESULT.md`).
- CR011 status re-grading based on Outcome (deferred; only CR013 result triggers).
- Downstream apparatus primary-target annotation (deferred to successor downstream CR).
- SLC patent restoration or continued downgrade (deferred; a vindicated d_ref still meets an apparatus before any patent limb changes status).

## §10 Rule-9 line

```text
This CR could have failed the setup by:
  (i)   whitelist mis-scope (G1);
  (ii)  forbidden-string leak in the DERIVER input package (G2);
  (iii) missing SHA-256 record (G3);
  (iv)  stripping a required structural identity from the redacted
        inputs — the DERIVER cannot compose what it cannot read (G4);
  (v)   SCRUBBER-as-VERIFIER role collapse (G5);
  (vi)  §4 task-statement drift (G6);
  (vii) provenance chain break (G7);
  (viii) any redaction shaped to steer the DERIVER toward or away
        from a specific reading — a form of anti-retrofit targeting
        performed on the input pipeline rather than the derivation.
        (viii) is not automatically detected by G1-G7; it is guarded by
        SCRUBBER/VERIFIER role separation and by the mechanical §3
        forbidden-string list, and by post-hoc audit of the
        redaction diffs which are preserved implicitly through the
        pairing of source-file SHA-256 with redacted-file SHA-256 in
        HASHES.txt.
```

## §11 Provenance hash chain

| artifact | reference |
| --- | --- |
| CR010 (Substrate Spaghettio-Lattice Foundation) precommit | source hash in HASHES.txt |
| CR266@09a (two-mirror reciprocity, R = ĥ²·d̂ = 12) precommit | source hash in HASHES.txt |
| CR268@09a (tensor 6 heaviest-neutrino identification) precommit | source hash in HASHES.txt |
| CR001@20 (neutrino mass spectrum) precommit | source hash in HASHES.txt |
| CR004 (SLC Phase 2 distance coupling; source of kernel form) precommit | source hash in HASHES.txt |
| SAM_ON_EARTH_v1.md (SI frame anchor) | `7b0f225821e2aea55e02b0868997fa2acd4ee88b4711ab1b1fb161366e1c5137` |
| SAM_LC_WORK_ASSIGNMENT_v1.md (LC assignment) | `3a88142743f3d5487a55dc99e29f51edd097660e3cb27625c79aee3f5f29d4a4` |
| STEWARDSHIP_DECLARATION.md (stewardship) | `d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88` |
| CR012_SABOTAGE_ACCOUNTING.md (immediate origin) | source hash in HASHES.txt |
| CLEANROOM_DREF_PROTOCOL_v1_0.md (draft protocol assembled into this precommit) | source hash in HASHES.txt |

## §12 Change log

```text
v1.0  2026-07-03  Opened by "big-brother" session as CR013, promoting
                  chat-side Claude's CLEANROOM_DREF_PROTOCOL_v1_0.md
                  into a sealed CR precommit at Sean Brady's direction
                  ("we botched CR012, we need to clean it up"). SCRUBBER
                  pass executed in-session; W1..W6 written to
                  INPUTS_REDACTED/ against the §3 forbidden-string
                  list. VERIFIER pass deferred to fresh session or
                  Sean per §1 role-separation rule; DERIVER session
                  deferred to strictly after VERIFIER PASS on §7 gates.
                  Stewardship + LC assignment + frame anchor chain
                  carried; CR012 v1.0 sealed files not touched.
```
