# CR098 CERN Gaps Forward-Blind Predictions - Sealed Registry

## Verdict

```text
CR098_FORWARD_BLIND_PREDICTION_REGISTRY_SEALED (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)
```

## Commitment Proof

```text
prediction_commit_sha256 = cf0cec19b5ce8a91cf5888eded94dc8ac8fa213296215fee674fc52bd3734a91
prediction_commit_utc    = 2026-06-13T21:41:50Z
registry_sha256          = 6884850496ee233ed799c886dc114c70e9930b9a6c9b9c7d5df867064751fb1e
registry_sha256_sibling  = CR098_forward_blind_prediction_registry.csv.sha256.txt
blindness_protocol_sha256= 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
```

## What This Is

This CR is qualitatively different from CR091..CR096. The earlier
CRs compared 09a's locked predictions against CERN values that were
already public when 09a was sealed. CR098 commits SAM forward
predictions BEFORE CERN publishes a matching measurement. The hash
plus the utc timestamp on every row is the cryptographic record
that SAM committed first. The registry is sha256-sealed by its
sibling file. Future CERN publications matching any registered
candidate are appended as APPEAL rows; the registry itself is
never modified.

## Counts

```text
Total forward-blind predictions registered : 24
Per source family:
  SAM_X                          12
  SUK055_COMPOSITE               12
Per prediction-status class:
  FORWARD_BLIND_SEARCH_ACTIVE                   22
  FORWARD_BLIND_NO_SEARCH_DEFINED               1
  FORBIDDEN_PARTITION_NEGATIVE_PREDICTION       1
```

## SAM-X Novel Native Candidates

Twelve novel native-sector predictions from closure_campaign03. Each
is sha256-locked at the prediction commit utc. SAM-X-012 is a
NEGATIVE prediction (forbidden partition).

| Candidate | Mass (MeV) | Q | Structural reading | Status | Suggested CERN program |
|---|---|---|---|---|---|
| SAM-X-001 | 19.32 | -R/R = -1 | (12,)__single_block_integer_winding | FORWARD_BLIND_SEARCH_ACTIVE | NA64 dark-sector / FASER forward search (low-mass charged scalar window) |
| SAM-X-002 | 3318 | undetermined__pending_outer_binary_assignment | (12,)__single_block_REORG_symmetric | FORWARD_BLIND_SEARCH_ACTIVE | ATLAS / CMS resonance searches (~3 GeV scalar lane) |
| SAM-X-003 | 0.6422 | undetermined | (12,)__single_block_REORG_plus_one_symme | FORWARD_BLIND_SEARCH_ACTIVE | NA64 / FASER hidden-sector (sub-MeV scalar window) |
| SAM-X-004 | 0.0001243 | 0__INTEGER_WINDING_NEUTRAL_IDENTITY | (12,)__single_block_PAIRCOUPLING_symmetr | FORWARD_BLIND_SEARCH_ACTIVE | FASERnu / SND@LHC forward neutrino program; KATRIN-class nu-mass experiments (no |
| SAM-X-005 | 2.745e+04 | -R/R = -1 | (12,)__single_block_BOUNDARY | FORWARD_BLIND_SEARCH_ACTIVE | ATLAS / CMS heavy charged-lepton-like search (~27 GeV) |
| SAM-X-006 | 1.025 | -alpha_H^3/R = -8/12 = -2/3 | (8,4)__asymmetric_binary__alpha_H^3__alp | FORWARD_BLIND_SEARCH_ACTIVE | MoEDAL fractional-charge search at LHC (Q=-2/3 with negative winding) |
| SAM-X-007 | 1.537 | -D^2/R = -9/12 = -3/4 | (9,3)__paired_transition__D^2__D | FORWARD_BLIND_SEARCH_ACTIVE | MoEDAL fractional-charge search (Q=-3/4 is NON-SM rational charge - novel) |
| SAM-X-008 | 228.2 | +(alpha_H*D)/R - alpha_H^2/R + alpha_H/R = +(6-4+2)/12 = +1/3 | (6,4,2)__mixed_layered__alpha_H*D__alpha | FORWARD_BLIND_SEARCH_ACTIVE | MoEDAL + LHCb fixed-target Q=+1/3 primary search (no SM primary +1/3 exists) |
| SAM-X-009 | 342.3 | depends on block occupancy; uniform_neutral = 0; single-block-screen = -3/12 = -1/4 (NOT IN SM) | (3,3,3,3)__uniform_quadripartite__4_D_bl | FORWARD_BLIND_SEARCH_ACTIVE | ATLAS / CMS quaternary owner-algebra search (SU(4)-like discriminator) |
| SAM-X-010 | 9.563e-06 | 0__INTEGER_WINDING_NEUTRAL_IDENTITY__asymmetric | (8,4)__asymmetric_binary__outer_binary_a | FORWARD_BLIND_SEARCH_ACTIVE | FASERnu / SND@LHC (sterile-neutral asymmetric outer-binary; ~9 eV) |
| SAM-X-011 | 1.785e-10 | 0__NEUTRAL_IDENTITY_PHASE | (6,6)__symmetric_binary__outer_binary_ac | FORWARD_BLIND_NO_SEARCH_DEFINED | Ultra-light scalar (sub-meV) - OSQAR / IAXO axion-class searches not yet at this |
| SAM-X-012 | N/A_FORBIDDEN_PARTITION | N/A | (7,5)__BOTH_PARTS_AT_RADIX_WALLS | FORBIDDEN_PARTITION_NEGATIVE_PREDICTION | MoEDAL / any LHC exotics - SAM predicts NO particle at (7,5) radix-wall partitio |

## SUK055 Composite Pair Mass Coordinates

Twelve heavy q-anti-q composite pair coordinates. Pairs involving
the top quark (b<->t, c<->t, d<->t, s<->t, t<->u) are radically new:
the top quark decays before hadronization in the SM, so a top-involved
bound state at the predicted mass coordinate would be a major discovery.

| Pair | Mass (MeV) | Charge class | Grade | Suggested CERN program |
|---|---|---|---|---|
| b<->c | 5459.9630 | charged | heavy q-anti-q composite pair  | LHCb exotic spectroscopy + ATLAS/CMS heavy-flavour resonance |
| b<->d | 4186.5590 | neutral | heavy q-anti-q composite pair  | LHCb exotic spectroscopy + ATLAS/CMS heavy-flavour resonance |
| b<->s | 4274.7210 | neutral | heavy q-anti-q composite pair  | LHCb exotic spectroscopy + ATLAS/CMS heavy-flavour resonance |
| b<->t | 176945.0000 | charged | heavy q-anti-q composite pair  | LHCb + ATLAS + CMS top-quark physics program (radically new: |
| b<->u | 4184.0560 | charged | heavy q-anti-q composite pair  | LHCb exotic spectroscopy + ATLAS/CMS heavy-flavour resonance |
| c<->d | 1282.7000 | charged | heavy q-anti-q composite pair  | LHCb exotic spectroscopy + ATLAS/CMS heavy-flavour resonance |
| c<->s | 1370.8620 | charged | heavy q-anti-q composite pair  | LHCb exotic spectroscopy + ATLAS/CMS heavy-flavour resonance |
| c<->t | 174041.1000 | neutral | heavy q-anti-q composite pair  | LHCb + ATLAS + CMS top-quark physics program (radically new: |
| c<->u | 1280.1970 | neutral | heavy q-anti-q composite pair  | LHCb exotic spectroscopy + ATLAS/CMS heavy-flavour resonance |
| d<->t | 172767.7000 | charged | heavy q-anti-q composite pair  | LHCb + ATLAS + CMS top-quark physics program (radically new: |
| s<->t | 172855.9000 | charged | heavy q-anti-q composite pair  | LHCb + ATLAS + CMS top-quark physics program (radically new: |
| t<->u | 172765.2000 | neutral | heavy q-anti-q composite pair  | LHCb + ATLAS + CMS top-quark physics program (radically new: |

## Rule-9 Line

```text
CR098 puts SAM on the line for predictions CERN has not made yet.
The sealed registry, with cryptographic prediction-commit hash and
UTC timestamp, is the on-record cryptographic proof that SAM
committed BEFORE any CERN publication on these gaps.

If CERN publishes a measurement that confirms a registered
prediction, that's strong evidence in SAM's favor. If CERN
publishes a contradicting measurement, that's evidence against
SAM, and the appeal row records the residual honestly. If
SAM-X-012 is observed (a particle at (7,5) radix-wall partition),
SAM's partition-algebra commitment is falsified.
```

## Open Debts

```text
- BLINDNESS_PROTOCOL sha256 sibling not yet written by curator
- Seal sha256 sibling not yet written by curator
- Upstream source files have not been independently re-hashed by curator
- suggested_CERN_search_program assignments are best-fit; curator verification pending
```
