# CR005i control-appeal precommit

- Campaign: `CR005i_STARBREAKER_PER_CARRIER_GW_CONTROL_APPEAL_AND_FREEZE`
- Task: `Appeal CR005h numerical controls and adjudicate the frozen per-carrier GW candidate ledger`
- Classification: `CONFIRMATION_OR_AUDIT_REQUIRES_PERMISSION`
- Permission: **granted by user** for the per-carrier campaign and necessary freeze work on 2026-07-20
- Preflight: `artifacts/preflight_filled/PREFLIGHT_20260720_235234_no_script.md`
- Frozen at: `2026-07-21T04:54:42.4692677Z`
- Runner present at seal: **no**
- Appeal results opened before seal: **no**
- Same-run repair: **prohibited**

## Immutable lower-court record

CR005h remains an immutable failed campaign. It nevertheless emitted a complete 53,568-row attribution ledger and candidate tables before failing exactly three gates. This appeal may not recalculate candidate scores, change candidate thresholds, change carrier histories, change the trajectory flow, or replace any candidate row.

## Bounded appeal

The appeal tests three implementation defects visible in the frozen record:

1. G02 compared the sealed parent verdict against the wrong string prefix: `PASS_CONTINUOUS_FLOW` instead of the actual sealed `PASS_CONTINUOUS_STARBREAKER_FLOW...` verdict.
2. G05 demanded an absolute post-third-difference equality without allowing the finite-difference operator to amplify floating summation residue.
3. G08 demanded literal post-third-difference zero rather than first testing the defining static and isotropic quadrupole symmetries and then bounding derivative roundoff.

The corrected controls are frozen in the contract before the appeal runner is written. Every CR005h release file must hash-match its manifest. Adoption, if earned, applies to the byte-identical CR005h carrier ledger, slot candidates, and occurrence shortlist.

## Claim firewall

This remains internal source attribution. No external waveform, QNM response, physical mass weighting, physical strain, luminosity, detector forecast, or claim that carriers are the material of a gravitational wave is permitted.
