# CR005b Precommit: QNM Damping Substrate Dynamics

Branch: 21_GRAVITATIONAL_WAVES
CR: CR005b_QNM_DAMPING_SUBSTRATE_DYNAMICS
Classification: CONSTRUCTIVE_NEW_WORK
Sealed by: Codex research agent under Courtroom preflight
Task title for execution: CR005b QNM damping substrate dynamics

Required firewall block:

```text
sam_language_v0_3_consulted_during_development: false
sam_language_v0_3_candidate_hash_known_to_research_agent: false
```

## Purpose

CR003 found the Schwarzschild fundamental QNM damping expression by
substrate-expression search:

```text
omega_I*M = R/(L - V) = 4/45
```

CR005 later derived the real component `omega_R*M = 3/8` but explicitly did
not seal the imaginary/damping component. This CR tests a bounded derivation
for the damping component without search:

```text
damping_shell = closed ledger - committed write cell = L - V
omega_I*M     = route radix / damping shell = R/(L - V)
```

## Source manifest

The runner must verify the source hashes in `CR005b_SOURCE_MANIFEST.json`.
Hash mismatch is a FAIL-class invalid source condition.

Canonical source paths and expected SHA-256 values:

```text
COURTROOM_BRANCH_INTAKE_MAP.md                                              bb852bf9467718da7b7ce21d8768737520a0ec041d4faf7bb2e2cf4d1e46bcc6
SAM_NATIVE_MASTER_FORMULA_V4_2.md                                           1e0be6539763de0347c75af8eda2259b385a99b3585a13e3ccecad2f49744ae4
SAM_NATIVE_ACTION_ENGINE_V4_2.md                                            976c649d071db8e2320406899dca3aae8a10dad2bcef277b2954c9c931d600cd
SAM_TESTING_RULES.md                                                        6913e15b270ec16aba4c8985f6f9c2455d99d1debaf57cbf20575ed543e422a5
21_GRAVITATIONAL_WAVES/README.md                                            1a4a2e0d388f2a913ee68163a5b2636dfef44f0aa5712a48acbe6e17b4fb6595
21_GRAVITATIONAL_WAVES/CR_QUEUE.md                                          ef6f85bc02a1dd2a9fc62f4d14da865079f0705f25e73eeb815d1d6b6b810c66
21_GRAVITATIONAL_WAVES/GW_SUBSTRATE_FRAMING.md                              a19afc01a749e925d6e1e4f70321217dcaca95fd5981a68e0e52ebdfcb2ed941
21_GRAVITATIONAL_WAVES/STUDY_NOTES_FOR_QNM_DERIVATION.md                    80eacc60d0d772bba7082b54a35322872e106f8a7864ba5ccf6e03355acf6e86
21_GRAVITATIONAL_WAVES/CR003_RINGDOWN_FREQUENCY_IN_SUBSTRATE_UNITS/CR003_result.md  5716a8854584ca5eedeeeec07b57a7c829585e20d77a5ab21ebaefe1ab6cc2b7
21_GRAVITATIONAL_WAVES/CR003_RINGDOWN_FREQUENCY_IN_SUBSTRATE_UNITS/CR003_summary.json 4d9807f875c6175b66d07e7696a9439f134a369adb15fbe68cb9a3630fa03213
21_GRAVITATIONAL_WAVES/CR004_SAM_VS_GR_DISCRIMINATION_MAP/CR004_result.md   f816eb4b2e140a8f220e501fdb6e07c746a5c7cac5822720966a8d59be74b564
21_GRAVITATIONAL_WAVES/CR005_THETA_CARRIER_OVERFLOW_AND_QNM_DERIVATION/CR005_PRECOMMIT.md 624f0c2655333dd9e6e217f2bed0cbdbd97197281b6f06b462747b7896b13b6b
21_GRAVITATIONAL_WAVES/CR005_THETA_CARRIER_OVERFLOW_AND_QNM_DERIVATION/CR005_result.md d21c4e16b5bd4471f158c4ec19d617c11c133f89937eb33a95c0993397a1e6ec
21_GRAVITATIONAL_WAVES/CR005_THETA_CARRIER_OVERFLOW_AND_QNM_DERIVATION/CR005_summary.json b2f598b3eb746a4075410a8abad5a864f422fbcde44822af0c8a1dd22b3e59f5
```

## Sealed inputs

Exact integer SAM atoms:

```text
h_hat = 2
d_hat = 3
S     = h_hat^d_hat        = 8
V     = d_hat^d_hat        = 27
F     = d_hat^(d_hat + 1)  = 81
R     = h_hat^2*d_hat      = 12
R^2   = 144
Theta = h_hat*d_hat^2      = 18
L     = h_hat*F            = 162
M     = R^2 - Theta        = 126
```

External comparator, reveal-only:

```text
omega_I_M_Berti_2009 = 0.08896232
```

The comparator is not used to choose, tune, search, or repair the formula.

## Canonical equations and rules

Primary damping-shell selector:

```text
damping_shell = L - V
omega_I_M     = R / damping_shell
```

Equivalent source identities that must hold exactly:

```text
L - V = 162 - 27 = 135
R^2 - d_hat^2 = 144 - 9 = 135
(R - d_hat)(R + d_hat) = 9*15 = 135
R/(L - V) = R/(R^2 - d_hat^2) = 12/135 = 4/45
R/(R^2 - d_hat^2) = (1/2)*(1/(R - d_hat) + 1/(R + d_hat))
```

Interpretation:

```text
L - V is the unresolved damping shell: closed ledger minus committed write cell.
R is the route radix: damping leaks per route, not per dimension.
The harmonic split over (R - d_hat, R + d_hat) is a two-side shell identity,
not an added fitted coefficient.
```

## Output fields

The runner must emit at least:

```text
artifact
branch
verdict
execution_status
precommit_hash
runner_hash
source_hashes
firewall_fields
free_parameter_count
external_anchors
external_comparators
atoms
identities
primary_output
wrong_controls
exceptions
rule_9_falsification
```

## Tolerances

Exact identity tolerance:

```text
0; use integer and Fraction arithmetic.
```

External comparator gates:

```text
PASS comparator gap:     relative error <= 0.1 percent
BOUNDARY comparator gap: relative error > 0.1 percent and <= 0.5 percent
FAIL comparator gap:     relative error > 0.5 percent
```

Wrong-control separation:

```text
PASS requires every wrong control to be rejected by source-role rules and
requires every rational wrong control to have relative error > 1.0 percent.
The pi-neighbor control must fail the PASS gate (> 0.1 percent) and fail
source-role admissibility because pi is not sourced in this damping-shell rule.
```

## Wrong controls

The runner must compute:

```text
WC1_capacity_denominator = R/R^2
WC2_closed_ledger_denominator = R/L
WC3_matter_denominator = R/M
WC4_dimension_numerator = d_hat/(L - V)
WC5_theta_numerator = Theta/(L - V)
WC6_pi_neighbor = (pi + S)/M
```

Expected wrong-control behavior:

- WC1-WC5 must miss the Berti comparator by more than 1 percent.
- WC6 may be numerically near but must miss the PASS gate and be rejected by
  source role.
- None of the wrong controls may be selected or substituted.

## Forbidden files and target-bearing inputs

Forbidden by path/purpose:

```text
SAM_LANGUAGE*
SAM-Language*
*V0_3_GENERALIZATION*
*PROSPECTIVE_HOLDOUT*
*FORECAST_GATE*
*LANGUAGE_CONTRACT*
any executable-language candidate implementation
any frozen executable-language contract
any expected language output
any forecast-gate or holdout adjudication result
```

Forbidden construction moves:

```text
reading an observed target to select a formula
searching formula space at runtime
fitting an arbitrary coefficient
using the Berti comparator as a derivation input
importing or consulting any executable-language system
changing the source hierarchy after precommit
opening another test result at runtime unless listed in the source manifest
silently repairing missing data
```

## Verdict tree

PASS iff all conditions hold:

```text
G0 precommit hash matches the hash sealed before runner implementation
G1 all source hashes match CR005b_SOURCE_MANIFEST.json
G2 forbidden-file guard is not tripped
G3 firewall fields are false in precommit, summary, provenance, and result
G4 exact SAM atoms match the sealed integer definitions
G5 damping shell identities all hold exactly
G6 primary output equals 4/45 exactly
G7 comparator relative error <= 0.1 percent
G8 wrong controls separate as specified
G9 free_parameter_count = 0
```

BOUNDARY iff:

```text
G0-G6 and G9 hold, but G7 is > 0.1 percent and <= 0.5 percent, or a
source-role-rejected wrong control is too numerically close for PASS.
```

FAIL iff:

```text
G0, G1, G2, G3, G4, G5, G6, or G9 fails, or comparator relative error > 0.5
percent.
```

## Rule-9 falsification sentence

One source-hash mismatch, one precommit-hash mismatch, one forbidden-file guard
trip, one exact integer/rational identity failure, one hidden fitted parameter,
one runtime formula search, or one comparator miss outside the precommitted
PASS/BOUNDARY bands falsifies the CR005b PASS claim.

## Non-goals

This CR does not:

- revise CR003, CR004, or CR005;
- claim a full substrate equation of motion;
- derive higher QNM modes;
- derive Kerr spin dependence;
- generate a forecast;
- perform queue maintenance;
- consult any executable-language artifact.
