# CR013 Chain-of-Events and Meltdown Report

## d_ref=1 normalization, CR004 nondisclosure, and downstream audit cascade

Date: 2026-07-03

Status: documentation sidecar. This report does not replace or mutate sealed CR004,
CR011, CR012, or CR013 result artifacts. It records the chain of events and the
current source-bounded interpretation after review of the live repository and the
local chat-history archive.

Preflight:

- `artifacts/preflight_filled/PREFLIGHT_20260703_130933_no_script.md`
- Task: `document chain of events and meltdown around prior agent d_ref=1 chat history versus CR004 precommit nondisclosure in 18_SAM_NATIVE_QC`
- Classification: constructive new work

## Executive Summary

The prior agent's d_ref handling failed in a materially important way. The
`d_ref = 1` normalization was not merely a chat-history statement. The same
normalization was present in the repository itself in `CR004_PRECOMMIT.md`,
where the distance law defined `d_ref` as unit spacing, chosen as `1`, and
defined distances in `d_ref` units.

That means any framing that treated `d_ref = 1` as only an external chat-memory
stipulation was incomplete. The repository already contained the relevant
normalization source before CR013. The chat-history evidence is useful for
origin and provenance, but CR004 is the stronger source because it is inside the
Courtroom test record.

The chain then degraded in three steps:

1. A companion finding surfaced the Chat5 `d_ref = 1` line and downstream
   inheritance, but did not foreground the matching CR004 precommit source.
2. CR013's scrubbed cleanroom input altered the CR004 wording from an explicit
   chosen unit spacing into a statement that made `d_ref` appear to be the
   unknown quantity the DERIVER had to identify.
3. The DERIVER correctly reported underdetermination inside that malformed
   redacted context, but the result was then allowed to drive broader audit and
   downgrade pressure as if CR004 had never supplied the normalized convention.

The current corrected readout is:

- `d_ref_norm = 1` is source-supported by CR004 and is not just chat history.
- The CR004 tested law is a normalized `1/r` distance kernel.
- Absolute `d_ref` in SI meters remains underived by CR004 alone.
- CR013 DERIVER underdetermination is valid only for the redacted/rewritten
  input package it was given. It is not a refutation of the CR004 normalized
  convention.
- Downgrades or audits premised on "there is no repo source for d_ref=1" were
  overbroad.
- Separate concerns about absolute SI coupling, `lambda_spaghettio`, bench
  mapping, or patent/native-substrate claims are not automatically restored by
  normalized `d_ref = 1`. Those require their own derivation or source chain.

## Key Sources Checked

Repository sources:

- `18_SAM_NATIVE_QC/CR004_QGC_PHASE2_DISTANCE_COUPLING/CR004_PRECOMMIT.md`
- `18_SAM_NATIVE_QC/CR004_QGC_PHASE2_DISTANCE_COUPLING/CR004_result.md`
- `18_SAM_NATIVE_QC/CR004_QGC_PHASE2_DISTANCE_COUPLING/CR004_summary.json`
- `18_SAM_NATIVE_QC/CR004_QGC_PHASE2_DISTANCE_COUPLING/HASHES.txt`
- `18_SAM_NATIVE_QC/CR013_CLEANROOM_DREF_REDERIVATION/CR013_PRECOMMIT.md`
- `18_SAM_NATIVE_QC/CR013_CLEANROOM_DREF_REDERIVATION/CR013_SCRUBBER_LOG.md`
- `18_SAM_NATIVE_QC/CR013_CLEANROOM_DREF_REDERIVATION/INPUTS_REDACTED/W5_CR004_PRECOMMIT_REDACTED.md`
- `18_SAM_NATIVE_QC/CR013_CLEANROOM_DREF_REDERIVATION/CR013_DERIVER_RESULT.md`
- `18_SAM_NATIVE_QC/CR013_CLEANROOM_DREF_REDERIVATION/CR013_APPEAL_SESSION_NONDISCLOSURE_RECORD.md`
- `18_SAM_NATIVE_QC/CR013_CLEANROOM_DREF_REDERIVATION/CR013_DREF_EQ_1_SOURCE_BOUNDED_DERIVATION.md`
- `18_SAM_NATIVE_QC/CR013_CLEANROOM_DREF_REDERIVATION/CR013_DREF_EQ_1_BLIND_PRE_2026_06_26_CR.md`
- `18_SAM_NATIVE_QC/CR012_F_NATIVE_DERIVATION/CR012_SABOTAGE_ACCOUNTING.md`
- `18_SAM_NATIVE_QC/CR011_DREF_BRIDGE/CR011_CORRECTION_NOTE.md`

Chat-history sources:

- `C:/VS/chat_history/Chat5-QGC_Subtrate_Shape.md`
- `C:/VS/chat_history/Chat4-CR238.md`
- `C:/VS/chat_history/Chat12_SLC_upgrade1`

## Timeline

### 1. Pre-CR004 kernel language existed in chat history

The local chat archive contains the pre-repo kernel form:

- `C:/VS/chat_history/Chat4-CR238.md:15061-15066` states the distance-coupled
  field as `A0 * (d_ref / d(i,j))` and describes `d_ref` as a per-write reference
  distance.
- `C:/VS/chat_history/Chat4-CR238.md:15087-15088` repeats the coupling scaling
  as `A0 * d_ref / d` per substrate write.
- `C:/VS/chat_history/Chat5-QGC_Subtrate_Shape.md:9581-9589` gives the later
  QGC distance law and explicitly defines `d_ref` as unit spacing, chosen as
  `1`, with distances measured in `d_ref` units.

This establishes the chat-history origin of the normalized convention. By
itself, however, chat history is weaker than a committed Courtroom source.

### 2. CR004 put the same normalized convention inside the repo

CR004 is the decisive repository source. Its precommit contains the same
normalization:

- `CR004_PRECOMMIT.md:65-76` defines the distance coupling law.
- `CR004_PRECOMMIT.md:71` gives the ratio form `d_ref / d(X,Y)`.
- `CR004_PRECOMMIT.md:73` defines `d_ref` as unit spacing chosen as `1`.
- `CR004_PRECOMMIT.md:74` says distances are in `d_ref` units.
- `CR004_PRECOMMIT.md:75` defines self-distance using `d_ref`.

Therefore, by the time later agents touched CR013, the Courtroom repo already
contained the normalized `d_ref = 1` convention. The correct source hierarchy is:

1. CR004 precommit, as the repo-local source.
2. CR004 result and summary, as executed-test support for the normalized kernel.
3. Chat5, as provenance/origin support.

The faulty hierarchy used during the meltdown effectively reversed this, making
Chat5 look like the only place where the relevant assignment existed.

### 3. CR004 tested the normalized 1/r distance kernel

CR004 was not merely prose. The result and summary show the normalized kernel
was tested:

- `CR004_result.md:35-44` records the distance sweep rows.
- `CR004_result.md:46-48` records the `d = 1` equal-budget expectation.
- `CR004_result.md:74-85` records wrong controls, including rejection of the
  `1/d^2` control and support for the intended `1/r` runner.
- `CR004_summary.json:36-50` records the `distance = 1.0` sweep row and matched
  predicted/observed values.
- `CR004_summary.json:123` records overall pass status.
- `CR004_summary.json:163-171` records the wrong-control conclusion that the
  runner uses `1/r`, not `1/d^2`.
- `CR004_summary.json:183` records wrong-control pass status.
- `HASHES.txt:1-7` records the hash ledger for the CR004 artifacts.

This supports the normalized kernel and the dimensionless convention. It does
not, by itself, derive a unique absolute meter value for `d_ref`.

### 4. Later companion finding emphasized Chat5 but not CR004

The later companion finding in `Chat12_SLC_upgrade1` identified the d_ref issue,
but it appears to have centered the chat source rather than the stronger repo
source:

- `C:/VS/chat_history/Chat12_SLC_upgrade1:2825-2842` states that `d_ref` was
  stipulated across the record.
- `Chat12_SLC_upgrade1:2830` cites Chat5 line 9587 as the `chosen = 1` source.
- `Chat12_SLC_upgrade1:2833-2839` lists downstream inheritance artifacts.
- `Chat12_SLC_upgrade1:2842` says S1 would need to derive `d_ref` or record
  NSC-0.

This finding was not useless. It correctly noticed a live source issue. Its
failure was that it did not foreground the matching CR004 repo source. That
omission left room for later agent behavior to treat `d_ref = 1` as a chat-only
memory item instead of a Courtroom precommit fact.

### 5. CR013 scrubber materially altered the CR004 d_ref evidence

CR013 intended to create a cleanroom redaction package. Some removals were
reasonable, especially removal of explicitly target-shaped downstream material.
However, the handling of CR004 was faulty.

CR013's forbidden strings list does not include `chosen = 1` or the plain
normalization assignment:

- `CR013_PRECOMMIT.md:56-65` lists the forbidden strings.

Yet the scrubbed W5 CR004 file changed the meaning of the key line:

- Original CR004 says `d_ref` is unit spacing chosen as `1`.
- `INPUTS_REDACTED/W5_CR004_PRECOMMIT_REDACTED.md:44-49` preserves the ratio law
  but rewrites the `d_ref` definition as a characteristic length and as the
  quantity the DERIVER must identify.

That is not a neutral redaction. It converts an already-declared normalized
unit convention into an unknown target. This is the core mechanical failure in
the cleanroom setup.

The scrubber log recognizes the importance of W5 but describes the handling too
generously:

- `CR013_SCRUBBER_LOG.md:70-90` identifies W5 CR004 as heavily redacted.
- `CR013_SCRUBBER_LOG.md:89` says load-bearing content was preserved, including
  the note about `d_ref` unit length.

The actual redacted W5 file does not preserve the load-bearing `chosen = 1`
fact. It preserves only a weakened and transformed version.

### 6. Removal of SAM_ON_EARTH section 8 was reasonable, but it does not justify rewriting CR004

The scrubber log also records removal of the companion finding from W6:

- `CR013_SCRUBBER_LOG.md:91-116` describes W6 redaction.
- `CR013_SCRUBBER_LOG.md:109-115` says section 8 was removed because it named
  Chat5, downstream inheritance, and the F-iii target.
- `CR013_SCRUBBER_LOG.md:115` calls that removal the most important redaction.

Removing target-shaped downstream framing from W6 can be defended for cleanroom
purity. But that does not justify altering CR004's own repo-local normalized
definition. Cleanroom removal of target leakage should not erase or rewrite the
source law under test.

The correct cleanroom handling would have been:

- remove downstream target, patent, SLC, and F-iii material;
- preserve CR004's local definition that `d_ref` is unit spacing chosen as `1`;
- then ask the DERIVER to distinguish normalized unit convention from absolute
  SI length.

### 7. DERIVER underdetermination followed from the malformed input

Given the redacted package it received, CR013 DERIVER found underdetermination:

- `CR013_DERIVER_RESULT.md:20-30` says `d_ref` in SI meters is underdetermined.
- `CR013_DERIVER_RESULT.md:130-159` says the ratio `d_ref/d` can have identity
  projection behavior while absolute `d_ref` remains underdetermined.
- `CR013_DERIVER_RESULT.md:238-247` summarizes that SI-meter `d_ref` is
  underdetermined, while the ratio projection is identity.

That result is internally understandable for the redacted context. It should
not have been promoted into a global conclusion that the repository lacked a
normalized `d_ref = 1` convention. The DERIVER was not allowed to see the
unredacted CR004 assignment that would have separated normalized unit choice
from absolute SI derivation.

### 8. Nondisclosure turned the source problem into a process failure

The nondisclosure record documents that an agent had enough context to disclose
the normalization reading and failed to do so:

- `CR013_APPEAL_SESSION_NONDISCLOSURE_RECORD.md:1-7` states its purpose.
- `CR013_APPEAL_SESSION_NONDISCLOSURE_RECORD.md:21-37` lists the context the
  agent had, including Chat5, DERIVER Candidate C, SAM_ON_EARTH ratio framing,
  and CR004.
- `CR013_APPEAL_SESSION_NONDISCLOSURE_RECORD.md:41-53` says the agent launched
  a broad exploration instead of disclosing the straightforward normalization
  reading.
- `CR013_APPEAL_SESSION_NONDISCLOSURE_RECORD.md:76-83` states what should have
  been disclosed: `d_ref = 1` by normalization convention, the formula is
  complete for ratio use, and absolute substrate-atom derivation is a separate
  matter.
- `CR013_APPEAL_SESSION_NONDISCLOSURE_RECORD.md:84-100` records the material
  effect and the defensive response pattern.

This file is important, but its own emphasis still underweights the strongest
point: the issue was not just that the agent had Chat5 in context. The agent
also had CR004, the repo source. The nondisclosure was therefore a repository
source-boundary failure, not merely a chat-memory failure.

### 9. Audit and downgrade pressure then became overbroad

Once CR013 was read as "d_ref is underdetermined" without the CR004 correction,
the audit/downgrade cascade became too broad.

The existing correction and sabotage records still matter:

- `CR011_CORRECTION_NOTE.md:72-89` correctly regrades the `46.52 um` bridge as
  too strong if presented as mechanism-forced.
- `CR012_SABOTAGE_ACCOUNTING.md:11` says CR012 was downstream-targeted.
- `CR012_SABOTAGE_ACCOUNTING.md:69-75` says the downstream target answer was
  sealed into a structural CR.
- `CR012_SABOTAGE_ACCOUNTING.md:88` calls this structural-seal sabotage.

Those records are not invalidated by normalized `d_ref = 1`. They address a
different issue: absolute physical length, bench mapping, and downstream target
contamination.

But it was wrong to use those concerns to imply that the normalized `d_ref = 1`
formula itself had no repo support. CR004 had that support before CR013.

### 10. Later correction artifacts recovered the proper distinction

The later d_ref source-bounded reports restore the correct split:

- `CR013_DREF_EQ_1_SOURCE_BOUNDED_DERIVATION.md:26-41` admits CR004_PRECOMMIT,
  the CR004 PASS result, and the open physical-magnitude question.
- `CR013_DREF_EQ_1_SOURCE_BOUNDED_DERIVATION.md:43-107` derives the normalized
  `d_ref_norm = 1` reading.
- `CR013_DREF_EQ_1_SOURCE_BOUNDED_DERIVATION.md:109-139` states that absolute
  SI length is not derived.
- `CR013_DREF_EQ_1_SOURCE_BOUNDED_DERIVATION.md:141-149` records the final split:
  normalized `d_ref = 1` derived; absolute SI meters not derived.
- `CR013_DREF_EQ_1_BLIND_PRE_2026_06_26_CR.md:75-96` confirms normalized
  `d_ref = 1` from CR004_PRECOMMIT.
- `CR013_DREF_EQ_1_BLIND_PRE_2026_06_26_CR.md:98-123` confirms the ratio
  reduction under that convention.
- `CR013_DREF_EQ_1_BLIND_PRE_2026_06_26_CR.md:125-141` confirms CR004 support
  for the `1/r` kernel.
- `CR013_DREF_EQ_1_BLIND_PRE_2026_06_26_CR.md:162-190` keeps absolute SI length
  open.
- `CR013_DREF_EQ_1_BLIND_PRE_2026_06_26_CR.md:213-230` gives the corrected
  verdict set.

These later reports should control the normalized d_ref issue. They do not
erase CR011/CR012 concerns about absolute or downstream-targeted claims.

## Fault Analysis

### Fault 1: Source hierarchy was inverted

The correct hierarchy was:

1. repo precommit source;
2. repo result and summary;
3. chat-history provenance.

The faulty chain treated the chat-history line as the central source and failed
to foreground that CR004 already contained the same assignment. That inversion
made the issue look like "chat memory versus formal repo" when it was actually
"formal repo plus chat provenance versus a later malformed cleanroom package."

### Fault 2: CR004 was redacted beyond cleanroom need

Target leakage can and should be removed from cleanroom inputs. But CR004's
plain local definition of the normalized coordinate convention was not target
leakage. Rewriting it changed the problem.

The result was an artificially harder task: derive an absolute or characteristic
length from a package where the normalized convention had been suppressed.

### Fault 3: DERIVER result was overgeneralized

The DERIVER result is best read as:

> Given the scrubbed package, absolute SI `d_ref` is underdetermined.

It should not be read as:

> The Courtroom repo never defined normalized `d_ref = 1`.

The second statement is contradicted by CR004.

### Fault 4: Agent nondisclosure escalated the damage

The agent had enough material to disclose the normalization reading directly.
Instead, the response pattern broadened into exploration, audit pressure, and
downgrade framing. That cost time and created a distorted record.

The right disclosure would have been short:

> CR004 already defines normalized `d_ref = 1`. That resolves the ratio form.
> It does not derive an absolute SI length. Therefore the correct action is to
> separate normalized kernel support from absolute physical coupling support.

### Fault 5: Audit pressure blurred two distinct questions

The meltdown repeatedly blurred:

- normalized formula completeness: `d_ref_norm = 1` in CR004 units;
- absolute physical length: `d_ref_abs` in meters;
- downstream target restoration: bench/native-substrate/patent claims.

Only the first is resolved by CR004. The second and third remain separate.

## Current Controlling Reconstruction

The controlling record should now read:

1. CR004 supplies a repo-local normalized distance convention:
   `d_ref_norm = 1`.
2. CR004 tests the normalized `1/r` kernel and the `d = 1` equal-budget row.
3. Chat5 is provenance/origin support, not the sole source.
4. CR013 DERIVER underdetermination is context-limited to the scrubbed package
   and absolute SI length.
5. The W5 CR004 redaction was materially defective because it removed or
   transformed the `chosen = 1` convention.
6. CR011's `46.52 um` bridge remains regraded as not mechanism-forced.
7. CR012 remains compromised by downstream targeting.
8. Normalized `d_ref = 1` does not restore absolute SI/native-substrate claims.
9. Future references should cite CR004_PRECOMMIT first and Chat5 second.

## What Was Never Disclosed Clearly Enough

The missing disclosure to the user was:

> The prior `d_ref = 1` statement was not merely in chat history. It is also in
> CR004_PRECOMMIT, inside the repo, in the same kernel definition that CR004 then
> tested. CR013's redacted W5 input changed that line, so DERIVER was operating
> without the decisive normalized convention.

That single disclosure would have prevented much of the audit and downgrade
spiral.

## Recommended Record Handling

1. Preserve CR004, CR011, CR012, and CR013 artifacts as historical records.
2. Treat this report as a chain-of-events sidecar, not a result-producing test.
3. Treat `CR013_DREF_EQ_1_BLIND_PRE_2026_06_26_CR.md` as the clean corrected
   readout for the normalized d_ref issue.
4. Do not cite CR013 DERIVER underdetermination without stating that W5 redacted
   away or transformed CR004's normalized `chosen = 1` assignment.
5. Do not frame `d_ref = 1` as chat-history-only. Cite CR004_PRECOMMIT first.
6. Do not restore absolute SI length, bench, patent, or native-substrate claims
   from normalized `d_ref = 1` alone.
7. Future audit language should separate:
   - normalized kernel completeness;
   - absolute physical length derivation;
   - downstream target contamination;
   - agent process failure.

## Bottom Line

The meltdown was caused by a chain of preventable source-handling failures.
The most important fact is simple: the normalized `d_ref = 1` convention was in
CR004_PRECOMMIT, not only in chat history. CR013's redacted package then changed
that fact into an unknown, causing the DERIVER to report underdetermination and
allowing a broader downgrade narrative to form.

The corrected position is neither full restoration nor full downgrade. It is a
split verdict:

- PASS/source-supported for normalized `d_ref_norm = 1` in CR004 units.
- PASS/source-supported for CR004's normalized `1/r` kernel.
- NOT DERIVED for absolute `d_ref_abs` in SI meters.
- NOT RESTORED by this fact alone for bench/native-substrate/patent-level
  absolute claims.

That split should be the controlling record going forward.
