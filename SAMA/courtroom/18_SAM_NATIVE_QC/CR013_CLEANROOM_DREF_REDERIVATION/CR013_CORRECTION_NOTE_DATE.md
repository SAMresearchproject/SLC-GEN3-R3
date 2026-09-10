# CR013 CORRECTION NOTE — VERIFIER report date drift

**Status:** Sidecar observation. Sealed VERIFIER artifact NOT modified.
Recorded per repo discipline "never rewrite sealed; document via
sidecar."

## Observation

`CR013_VERIFIER_REPORT.md` is signed with date `2026-06-23`
throughout — §1 signature block, §4 grep-execution timestamp, §5
SHA-256 re-computation timestamp, §7 verdict signature and date/time
line. `HASHES.txt` mirrors this date in its status header.

Every other CR013 artifact records `2026-07-03`:

- `CR013_PRECOMMIT.md` seal (per `HASHES.txt` header)
- `CR013_SCRUBBER_LOG.md` seal
- `CR013_DERIVER_RESULT.md` seal
- Sean Brady's session-of-record and this scribing session both under
  Courtroom system clock reading `2026-07-03`.

The VERIFIER report is dated **ten days earlier than every other
2026-07-03 seal in the same folder**. All other integrity gates on
the VERIFIER report pass:

- §7 verdict PASS on G1..G7.
- §2 grep 19/19 zero-hit output present verbatim in §4.
- §3 SHA-256 record MATCH 7/7 in §5.
- §6 structural-identity checklist ticked 13/13.
- SCRUBBER-vs-VERIFIER role separation §1 attestation present.

## Interpretation

The date field is the only place the VERIFIER-signed artifact
disagrees with the rest of the sealed record. Two admissible readings:

1. **Clock drift or template carryover.** The VERIFIER session
   inherited or entered `2026-06-23` as a date literal, possibly
   template default, and did not correct it against the Courtroom
   system clock at seal time. The gate outcomes are unaffected — every
   sealed-file SHA-256 recorded in §3 still matches those files today.
2. **A separately-scheduled VERIFIER session that ran genuinely on
   2026-06-23.** Ruled out: CR013 precommit was sealed 2026-07-03; the
   INPUTS_REDACTED/ SHA-256s the VERIFIER re-computed on 2026-06-23
   would have referred to files that did not yet exist. The precommit
   §11 provenance chain therefore requires reading (1) as correct.

## Action taken

- VERIFIER report and `HASHES.txt` are left untouched. Modifying a
  signed artifact from a non-VERIFIER session would violate CR013 §1
  role separation. If the VERIFIER session is re-invoked, it may
  correct its own date entries via a v1.1 signed report; the v1.0
  signed artifact and its sha256 `9be2ec97…` are preserved either way.
- This sidecar records the observation and its interpretation for the
  audit trail.

## Impact on downstream CR013 consequence register

None. The DERIVER session opened after the VERIFIER PASS was on
record, executed against `INPUTS_REDACTED/` whose SHA-256s the
VERIFIER cross-checked and matched, and sealed
`CR013_DERIVER_RESULT.md` (sha `514f0721…`) on 2026-07-03. The date
drift is a provenance-annotation issue, not a chain-of-trust issue.

## Change log

```text
v1.0  2026-07-03  Sidecar written by the SCRUBBER-lineage session
                  ("big-brother", session id 0ea2cc6e…) to record the
                  date-drift observation without touching the signed
                  VERIFIER artifact. Recommended by CR013 discipline
                  "never rewrite sealed; use sidecar."
```
