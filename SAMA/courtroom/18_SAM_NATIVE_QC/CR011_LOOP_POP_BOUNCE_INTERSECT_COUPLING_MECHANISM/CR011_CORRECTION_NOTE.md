# CR011 CORRECTION NOTE — re-grade of §1.3 under CR013 DERIVER result

**Status:** Sidecar re-grade. Sealed CR011 artifacts NOT modified.
Recorded per repo discipline "never rewrite sealed; document via
sidecar."

## Source of the re-grade

`CR013_CLEANROOM_DREF_REDERIVATION/CR013_DERIVER_RESULT.md` sha256
`514f0721…`, sealed 2026-07-03 by a DERIVER session that read only
six redacted files (W1 CR010, W2 CR266, W3 CR268, W4 CR001@20,
W5 CR004, W6 SAM_ON_EARTH_v1) with all 19 CR013-forbidden strings
scrubbed to zero-hit. VERIFIER PASS on record at
`CR013_VERIFIER_REPORT.md` sha `9be2ec97…` (date drift documented
in `CR013_CORRECTION_NOTE_DATE.md`; gate outcomes unaffected).

CR013 constructs the one audit class immune to anti-retrofit
targeting: a re-derivation in an agent context where the target does
not exist. Any structural claim upstream of CR013 whose "forcing"
argument the DERIVER did not reproduce blind is, by definition,
under-supported by the sealed record.

## What CR011 §1.3 claimed

CR011 sealed 2026-07-02 as PASS with headline claim:

> `d_ref_base = R · λ_spaghettio = 12 · 3.877 μm = 46.52 μm (SI)`
>
> "This is the **mechanism-forced identification** from CR010 §1.5
> (endpoint elsewhere-propagation) + CR266 (mirror linear extent
> R = ĥ²·d̂ = 12) + CR010 §1.2 (per-address scale λ_spaghettio =
> m_3 Compton wavelength). Zero free parameters. Zero bench-scale
> reference in the derivation."
>
> — `CR011_result.md` §Headline (lines 20-26)

Four alternative candidates were enumerated in CR011 §4 G4 with
structural non-selection reasons; candidate (b) at 46.52 μm was
identified as **the** mechanism-forced reading; the other three were
refused.

## What the CR013 DERIVER found blind

Working from the same upstream substrate content (W1 CR010, W2 CR266,
W3 CR268, W4 CR001@20, W5 CR004) plus the SI-frame anchor
(W6 SAM_ON_EARTH_v1), redacted for CR013-forbidden strings and CR011
itself not in-context:

- **Candidate A** (natural dilute-limit reach): `d_ref = λ_spaghettio
  = 3.877 μm`. Self-reunion of the popped loop's own endpoints at the
  loop scale. Tier: COMPOSED via the CR268/CR001@20 mass-3 chain
  through standard Compton composition on m_3, with the loop-scale
  identification per W1 (CR010) §1.2.
- **Candidate B** (Home-nesting dressing): `d_ref = R^N × λ_spaghettio`
  per W1 (CR010) §1.8's R-power-dressing statement. The specific
  exponent N is UNDERDETERMINED by the whitelist. CR011's 46.52 μm is
  this candidate at N = 1.
- **Candidate C** (ratio-only non-observability): absolute d_ref not
  fixed by the coupling-law observable d_ref/d per W6 §3.
- **Dense-limit alternative** (reach < 3.877 μm): W1 (CR010) §1.5's
  termination condition is cross-reunion with endpoints of OTHER pops,
  which is intrinsically pop-density-dependent. Functional form and
  lab-scale pop density are both UNDERDETERMINED by the whitelist.

The DERIVER's Task 4 concluded UNDERDETERMINED as a single SI value,
with four collapse conditions the whitelist does not close: regime
identification (dilute vs dense), projection level N, mean-free-path
formula, observable specification.

## What this means for CR011 §1.3

**CR011's "mechanism-forced" language is too strong.** A DERIVER
reading the same upstream content blind did not land 46.52 μm as the
forced identification; the blind natural reading is Candidate A at
3.877 μm (dilute self-reunion), with 46.52 μm surviving only as
Candidate B at N = 1.

Concretely, CR011 §Headline "mechanism-forced identification" is
re-graded to:

> `d_ref = R × λ_spaghettio = 46.52 μm` is **one of four admissible
> candidates** for the base-substrate coupling reach. It corresponds
> to the N = 1 case of the Home-nesting R-power dressing family
> per W1 (CR010) §1.8. It is not blind-forced by CR010 §1.5 endpoint
> propagation alone: the propagation clause only says endpoints
> propagate elsewhere on the substrate; it does not fix the reach
> ceiling at R × λ_spaghettio rather than at λ_spaghettio (self-
> reunion), at R^N × λ_spaghettio for N ≠ 1, or at a density-dependent
> mean-free-path value in the dense limit.

The audit lesson is the CR012-v1.0-adjacent failure mode named in
`CR012_SABOTAGE_ACCOUNTING.md` and generalised by CR013: a sealed CR
can claim "no bench-scale reference in the derivation" and still be
target-shaped through candidate-selection privileging that is
textually invisible on a same-session re-read. Only a cleanroom
re-derivation in an agent context blind to the target can flag it,
which is what happened here.

## Neighbouring CR011 claims

- **Alternative candidates are correctly enumerated in CR011 §4 G4**
  (candidates a/b/c/d). The DERIVER's blind enumeration overlaps with
  CR011's a/b/c set (dilute λ_spaghettio, R × λ_spaghettio, R² × …)
  plus adds the ratio-only observation from W6 §3. **Not re-graded.**
- **A-operator domain restriction to stable charged matter** per
  Vol II §11C (sealed 2026-06-28) is upstream of CR011 and correctly
  used to refuse candidate (c) at 558 μm. **Not re-graded.** The
  DERIVER's Candidate B family at N = 2 would land in this range
  numerically but the DERIVER did not identify Vol II §11C content
  (redacted or out-of-whitelist), so this refusal is a CR011-side
  discipline the DERIVER could not exercise. It remains valid.
- **Kernel form `A₀ · d_ref / d` from CR004** and **CR266 seven-atom
  identities** are DERIVED-with-citation in the CR013 DERIVER chain
  and hold as-is. **Not re-graded.**
- **The F-iii marginal 1.11× floor landing at n = 0** in CR011 §Headline
  is downstream of CR011's d_ref choice; it inherits the re-grade.
  Under Candidate A the equivalent landing would be F-ii (below floor).
  Under Candidate C, no absolute landing is defined. Under dense-limit
  alternative, landing is UNDERDETERMINED. This inheritance is
  informational; CR011's verdict field remains PASS on gates G1..G8
  as-executed, but the SEALED-content grading of §Headline is
  re-graded per this sidecar.

## Impact on downstream artifacts

- **CR-NSC-01 S1 attempt** (`CR-NSC-01_S1_ATTEMPT.md`, sealed
  2026-07-02, landing F-i / NSC-0): patent limb strikes on Claims
  2/15/21 stay struck. The CR013 DERIVER result reinforces the strike —
  UNDERDETERMINED d_ref does not restore any struck claim. Separate
  continuation note in the CR-NSC-01 folder records this.
- **SLC patent draft and claim structure**: no restoration action.
  The CR-NSC-01 §5 strike list stands.
- **Any successor apparatus CR** (CR-NSC-02 or renamed): primary
  target must be closing one or more of the four CR013 §Task 4
  collapse conditions BEFORE apparatus design. Recorded in the
  CR-NSC-01 continuation note.

## What is NOT changed

- CR011 sealed files (precommit, runner, result, HASHES.txt) are
  untouched. Verdict remains PASS on the gates as-executed; the
  re-grade is on the strength of the §Headline identification.
- CR011's audit-trail value is undiminished. The four-candidate
  enumeration + explicit alternative-refusal reasoning is exactly the
  content that made this re-grade tractable; the sidecar builds on
  that structure rather than replacing it.
- CR012 v1.0 sealed files (precommit, result, sabotage accounting)
  are untouched per Sean Brady's 2026-07-03 directive.

## Change log

```text
v1.0  2026-07-03  Sidecar written by SCRUBBER-lineage session
                  ("big-brother", session id 0ea2cc6e…), scribing
                  CR013 DERIVER result consequences into the CR011
                  audit trail. CR011 sealed artifacts not modified.
                  Recommended by repo discipline "never rewrite sealed;
                  use sidecar."
```

## Provenance chain

```text
CR013_DERIVER_RESULT.md   sha256 514f07217fdcf7b1819c7a3bd9d5290060ddcd11405c19ee4776dcd9a3474816
CR013_VERIFIER_REPORT.md  sha256 9be2ec97e8d3165cbe1632e8aa4c19c009da697c65f4cdbc141d14590613a991
CR013_PRECOMMIT.md        sha256 17fa12eec1f1da430aebc7a011c0b3071622e47111d8666269937789f54965f3
STEWARDSHIP_DECLARATION   sha256 d9fe07c9b87bb52bc20b08bc1c8b24cb4fb312fbd35653b5d1030b14ed0a7e88
SAM_LC_WORK_ASSIGNMENT_v1 sha256 3a88142743f3d5487a55dc99e29f51edd097660e3cb27625c79aee3f5f29d4a4
SAM_ON_EARTH_v1           sha256 7b0f225821e2aea55e02b0868997fa2acd4ee88b4711ab1b1fb161366e1c5137
```
