# CR210 Hard Freeze

```text
freeze_id = CR210_HARD_FREEZE_STARBREAKER_3D_EXTERNAL_COLLAPSE_CONTACT
status = FROZEN
generated_at_utc = 2026-07-15T01:45:56.839984+00:00
execution_status = CLEAN
scientific_verdict = PASS
result_class = CR210_PASS_SCOPED_STARBREAKER_3D_EXTERNAL_COLLAPSE_DIRECTIONAL_CONTACT__NO_PHYSICAL_PROMOTION__OPEN_TIME_RESOLVED_COLLAPSE
three_dimensional_replay = 1218/1218
starbreaker_regression_tests = 58/58
exact_precommit_replay = 28/28
runwise_monotonic_ladders = 42/42
same_total_inward_wins = 42/42
aligned_radial_permutation_rank = 2/2 maximum of 24
fitted_parameters = 0
wrong_controls = 8/8
frozen_payload_file_count = 22
payload_fingerprint_sha256 = ae60c1b744b2d2ea5ec7fe89aacc491065b83207288fa872f28232ea83d0f77d
frozen_manifest_sha256 = 59fa277b6b1b71b3d9c56e20c6fc05c1e59d116c35d3b77a884760a05e24627c
```

Frozen Courtroom readout: CR210 records the approved replay of the latest
Starbreaker 3D carrier-density geometry and its no-fit external-collapse
directional contact. The replay regenerated all 1,218 simulations, passed the
full 58-test Starbreaker regression chain, and reproduced all 28 precommitted
source and output hashes exactly.

The positive directional result also remains intact: all 42 runwise remnant
ladders rise strictly, all 42 inward allocations beat their same-total uniform
controls, and the aligned radial allocation is the maximum-remnant arrangement
for both geometry families over all 24 permutations.

Preserved boundaries:

- `p` is not physical bounce compactness `xi_2.5`.
- `A` is not assigned compactness units or physically calibrated.
- Starbreaker remnant fraction is not black-hole probability or mass.
- Starbreaker ejecta fraction is not explosion energy or observed ejecta mass.
- The endpoint simulator does not test faster time to black-hole formation.
- No stellar hydrodynamic or relativistic field equation is solved.
- The `A` packing law is not physically promoted.

The frozen HTML plate is presentation-only. The JSON, CSV, replay log,
preflight record, manifest, and SHA-256 ledgers are the authority.

Next gate: freeze one time-resolved internal collapse observable before any
formation-time comparison. Do not reopen or overwrite this endpoint freeze.
