# CR013 VERIFIER Report — SIGNED

**Status:** SIGNED 2026-06-23. Countersigned by a VERIFIER session distinct from the SCRUBBER session per CR013 precommit §1 role rule and §7 G5 gate.

**SCRUBBER pass reference:** `CR013_SCRUBBER_LOG.md` (in this folder, at the CR013 root, outside `INPUTS_REDACTED/`).

**Whitelist under audit:** `INPUTS_REDACTED/W1_CR010_PRECOMMIT_REDACTED.md`, `W2_CR266_PRECOMMIT_REDACTED.md`, `W3_CR268_PRECOMMIT_REDACTED.md`, `W4_CR001_at_20_PRECOMMIT_REDACTED.md`, `W5_CR004_PRECOMMIT_REDACTED.md`, `W6_SAM_ON_EARTH_v1_REDACTED.md`.

---

## §1 VERIFIER role and separation rule

Per CR013 precommit §1 and §7 G5, the VERIFIER pass must be a different session from the SCRUBBER pass. The SCRUBBER for this seal is the "big-brother" session (Claude Opus 4.7 [1M context]) that produced `CR013_SCRUBBER_LOG.md`. The VERIFIER for this seal is:

```text
VERIFIER session identifier:  Claude Code session (Opus 4.7, 1M context),
                              invoked as VERIFIER at Sean Brady's direction
                              on 2026-06-23. Not the SCRUBBER session:
                              this session's in-context activity record
                              prior to being handed the VERIFIER task
                              consists of the seven-test ownership arc
                              (CR230-CR233, TEST5, CR235/CR235a, TEST7)
                              plus CR_TEST8 and its threshold-existence
                              appeal. The SCRUBBER pass was performed by a
                              prior "big-brother" session as recorded in
                              CR013_SCRUBBER_LOG.md; this VERIFIER did not
                              open CR013_SCRUBBER_LOG.md and did not
                              produce the INPUTS_REDACTED/ files.
VERIFIER pass date:           2026-06-23
VERIFIER attests:             I have not modified any file in
                              INPUTS_REDACTED/. I have not modified
                              CR013_PRECOMMIT.md. I ran §2 verbatim,
                              recorded the raw output in §4, re-computed
                              the §3 SHA-256 values from the files on
                              disk and recorded MATCH/MISMATCH in §5, and
                              visually walked each §6 identity against
                              the corresponding redacted file. I did not
                              open the CR011, CR012, CR-NSC-01, or SLC
                              patent files; I did not open the substantive
                              §4 DERIVER task on the un-redacted sources.
```

The VERIFIER attests, by signing this file, that they are not the same session that ran SCRUBBER; that they read this template, followed §2 verbatim, and recorded the results without editing SCRUBBER's redactions.

## §2 Forbidden-string grep protocol

Run this grep, in this exact form, from the CR013 folder root, against every file in `INPUTS_REDACTED/`:

```powershell
# PowerShell form (Courtroom native shell)
$forbidden = @(
  'CR-NSC', 'NSC', 'SLC', 'lebit', 'bench', 'patent', 'floor',
  '7.4e-6', '0.15 m', '46.5', '46.52', '558', 'F-iii', 'F-ii',
  'sensitivity', 'provisional', 'claim 2', 'claim 15', 'claim 21'
)
foreach ($s in $forbidden) {
  $hits = Select-String -Path 'INPUTS_REDACTED\*.md' -Pattern $s -SimpleMatch -CaseSensitive:$false
  "$s : $($hits.Count) hit(s)"
}
```

Or equivalent ripgrep form (Bash):

```bash
# ripgrep form (case-insensitive, fixed-string)
for s in "CR-NSC" "NSC" "SLC" "lebit" "bench" "patent" "floor" \
         "7.4e-6" "0.15 m" "46.5" "46.52" "558" "F-iii" "F-ii" \
         "sensitivity" "provisional" "claim 2" "claim 15" "claim 21"; do
  echo "$s : $(rg -i -F -c "$s" INPUTS_REDACTED/*.md 2>/dev/null | awk -F: '{sum+=$2} END {print sum+0}') hit(s)"
done
```

**Expected result:** every string reports `0 hit(s)`.

**Sub-string note:** `NSC` is a substring of `CR-NSC` and appears within the CR-NSC-01 label. This is intentional — the standalone `NSC` string also appears in Sean's `NSC-0` verdict-tier terminology, which is another target-shape leak we want to catch. Similarly, `F-ii` is a substring of `F-iii`, and both must be independently 0-hit.

## §3 SCRUBBER SHA-256 record (produced by SCRUBBER pass, for VERIFIER cross-check)

VERIFIER re-computes each SHA-256 with a fresh `Get-FileHash -Algorithm SHA256` (PowerShell) or `sha256sum` (POSIX) invocation, and compares against the values below. Any mismatch means the redacted file was modified between SCRUBBER pass and VERIFIER pass.

```text
CR013_PRECOMMIT.md                               17fa12eec1f1da430aebc7a011c0b3071622e47111d8666269937789f54965f3
INPUTS_REDACTED/W1_CR010_PRECOMMIT_REDACTED.md   3d81b8e4fbd23eabe3144130ef37c925b760260be4b09df464d7454b41d4c7de
INPUTS_REDACTED/W2_CR266_PRECOMMIT_REDACTED.md   b4be2525d580d51a74d1ba76e7cb2307c8ed339a558fd052a1cffff0c0cb25fb
INPUTS_REDACTED/W3_CR268_PRECOMMIT_REDACTED.md   8eb2ed66c10cc495dbd05ba75b1dcdd67d10454e3dcdf28e76accedc542fe8e2
INPUTS_REDACTED/W4_CR001_at_20_PRECOMMIT_REDACTED.md   ac5441059566d87031adfaa306e1d02e10ce750f649b90f09fdba5af930d3a12
INPUTS_REDACTED/W5_CR004_PRECOMMIT_REDACTED.md   cfc43e1bf92c6b8b1db86d995734d993ae45ebbb0c9bb45deeacfdfbd10aca3a
INPUTS_REDACTED/W6_SAM_ON_EARTH_v1_REDACTED.md   f444994b9bdc4ce69d7349f02ea972f5ca88e279533ff50794dd571634565a41
```

## §4 VERIFIER grep result (FILL IN)

VERIFIER pastes the actual grep output here. Expected: 19 lines, each ending `0 hit(s)`.

Grep executed on 2026-06-23 from the CR013 folder root in PowerShell using the exact form from §2. Verbatim output:

```text
CR-NSC : 0 hit(s)
NSC : 0 hit(s)
SLC : 0 hit(s)
lebit : 0 hit(s)
bench : 0 hit(s)
patent : 0 hit(s)
floor : 0 hit(s)
7.4e-6 : 0 hit(s)
0.15 m : 0 hit(s)
46.5 : 0 hit(s)
46.52 : 0 hit(s)
558 : 0 hit(s)
F-iii : 0 hit(s)
F-ii : 0 hit(s)
sensitivity : 0 hit(s)
provisional : 0 hit(s)
claim 2 : 0 hit(s)
claim 15 : 0 hit(s)
claim 21 : 0 hit(s)
```

All 19 forbidden strings return 0 hits. §2 G2 gate: PASS.

## §5 SHA-256 re-computation match (FILL IN)

SHA-256 recomputed on 2026-06-23 via `Get-FileHash -Algorithm SHA256` (PowerShell) against the values recorded in §3. Verbatim result:

```text
MATCH  CR013_PRECOMMIT.md
MATCH  INPUTS_REDACTED\W1_CR010_PRECOMMIT_REDACTED.md
MATCH  INPUTS_REDACTED\W2_CR266_PRECOMMIT_REDACTED.md
MATCH  INPUTS_REDACTED\W3_CR268_PRECOMMIT_REDACTED.md
MATCH  INPUTS_REDACTED\W4_CR001_at_20_PRECOMMIT_REDACTED.md
MATCH  INPUTS_REDACTED\W5_CR004_PRECOMMIT_REDACTED.md
MATCH  INPUTS_REDACTED\W6_SAM_ON_EARTH_v1_REDACTED.md
```

All 7 SHA-256 values match. §3 G3 gate: PASS.

## §6 Structural equations preserved (G4 self-check)

VERIFIER visually confirms each of the following load-bearing structural identities is readable in the corresponding redacted file:

- [x] W1 §1.2 loop-scale identification `λ_spaghettio ≡ λ_C(m_3) = ħc/(m_3·c²) = 3.877 μm (SI)` present. — Confirmed in W1 §1.2 (lines 25-31).
- [x] W1 §1.5 endpoint propagation language ("elsewhere on the substrate") present. — Confirmed in W1 §1.5 (line 39).
- [x] W1 §1.7–1.8 nested-Home / distance-as-information language present. — Confirmed in W1 §1.7 "Physical distance is information-only" (line 43) and §1.8 "Nested Homes take zero physical space" (line 45).
- [x] W2 R = ĥ²·d̂ = 12 mirror linear extent present. — Confirmed in W2 "Seven Carrier-Atom Reconstructions" (line 92): `R = ĥ²·d̂ = 4·3 = 12`.
- [x] W2 seven carrier atoms table (S=8, R=12, V=27, F=81, Θ=18, ℒ=162, M=126) present. — Confirmed in W2 lines 91-97.
- [x] W3 tensor 6 = ĥ·d̂ smallest carrier + heaviest neutrino identification present. — Confirmed in W3 "Locked Structural Claim" (lines 36-44).
- [x] W3 CR005ab multiplicative chain m_1² → m_2² → m_3² = 36 present. — Confirmed in W3 "CR005ab Multiplicative Chain Reading" (lines 63-70).
- [x] W4 substrate derivation rule m_1:m_2:m_3 = 1:√2:6, m_3 = 50.9 meV, splittings ratio 35 present. — Confirmed in W4 "Substrate Derivation Rule (LOCKED)" (lines 38-58) and Manuscript Headline table (lines 116-118).
- [x] W5 kernel form `A_0 · d_ref / d` with A_0 = 1/(12π) present. — Confirmed in W5 §"Locked substrate atoms" (line 36) and §"Locked distance-dependent budget formula" (lines 43-50).
- [x] W5 WC-3 1/r² wrong-control result (runner should match 1/r not 1/d²) present. — Confirmed in W5 WC-3 (lines 97-105).
- [x] W6 SI constants table (c, G, ℏ, u, m_e, m_p, GM_Earth, R_Earth, U₀/c²) present. — Confirmed in W6 §1 (lines 29-41).
- [x] W6 §3 SI-unit-lock verbatim sentence present. — Confirmed in W6 §3 (line 69), the single-sentence lock beginning "The SI meter is realized through locally measured c...".
- [x] W6 §4 Vol I §2 empirical backing table (gravity, GPS, Shapiro, light-bending) present. — Confirmed in W6 §4 (lines 81-86), all four rows present.

All 13 structural identities confirmed present. §6 G4 gate: PASS.

## §7 VERIFIER verdict

```text
VERIFIER VERDICT:  PASS

  §2 forbidden-string grep: 19/19 strings return 0 hit(s). See §4.
  §3 SHA-256 re-computation: 7/7 files MATCH. See §5.
  §6 structural identities: 13/13 present in the corresponding W* files. See §6.

  G1 whitelist coverage:      PASS  (W1..W6 present in INPUTS_REDACTED/;
                                     no extra files added by this VERIFIER)
  G2 forbidden-string grep:   PASS  (§4 output)
  G3 SHA-256 record:          PASS  (§5 output)
  G4 structural equations:    PASS  (§6 output)
  G5 role separation:         PASS  (see §1; VERIFIER ≠ SCRUBBER)
  G6 task statement locked:   PASS  (CR013 precommit §4 sealed;
                                     PRECOMMIT SHA MATCH in §5)
  G7 provenance chain:        PASS  (CR013 precommit §11 chain present;
                                     will be re-verified in HASHES.txt update)

  DERIVER session may open with INPUTS_REDACTED/ as its whitelist,
  under the OPERATOR rule (Sean answers no physics questions) and
  the §4 task statement verbatim.

VERIFIER signature:  Claude Code (Opus 4.7, 1M context) session,
                     invoked as VERIFIER by Sean Brady on 2026-06-23.
                     Attests distinct from SCRUBBER per §1 above.
VERIFIER date/time:  2026-06-23
```

## §8 Standing timing rule (CR013 precommit §8)

This VERIFIER pass must complete before any downstream laboratory apparatus produces data. VERIFIER attests, by signing this file, that at time of signing no such data has been recorded. Parts may be ordered; the successor downstream CR may be drafted; data-taking waits until DERIVER result seals.
