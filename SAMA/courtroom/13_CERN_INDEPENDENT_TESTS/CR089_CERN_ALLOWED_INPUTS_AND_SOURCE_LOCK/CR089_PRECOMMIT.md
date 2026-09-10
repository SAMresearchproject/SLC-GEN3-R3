# CR089 CERN_ALLOWED_INPUTS_AND_SOURCE_LOCK

## Test Class

```text
FORWARD_COURTROOM_EXTENSION_INTO_CERN_INDEPENDENT_ANCHOR_SPACE
```

## Preflight

```text
This is the first CR of the 13_CERN_INDEPENDENT_TESTS branch. It locks
the upstream prediction side (the 09a-anchored QP075 closure surface)
as cite-only, declares the CERN-publication anchor class as the only
admissible external anchor for CR091 through CR095, and excludes PDG
world averages and non-CERN measurements from the anchor side.

It is not an audit of 09a. The 09a verdict (CR064a_PASS_QP075_
PARTICLE_MASS_CHAIN_BRANCH_RERUN) is taken as load-bearing.
```

## Question

Does the 13 branch lock the 09a/QP075 prediction surface as cite-only,
declare CERN-publication anchors (ATLAS / CMS / LHCb / ALICE, with
arXiv id or CDS record) as the only admissible external anchor class,
and explicitly exclude PDG world averages and non-CERN measurements
from the anchor side?

## Pass Conditions

- The seal `SEALED_CERN_INDEPENDENT_TESTS_SCOPE_APPROACH_2026_06_13.md`
  exists in the branch root.
- The branch `README.md` declares audit-chain inheritance from 09a.
- The branch `BLINDNESS_PROTOCOL.md` exists in the branch root and is
  cited from CR089 declared premises with its sha256 recorded.
- The branch `SOURCE_MANIFEST.csv` exists and:
  - lists the QP075 terminal-source files with their existing 09a
    sha256 hashes under role `upstream_prediction_cite`,
  - lists the 09a CR results (CR059a / CR062a / CR064a at minimum)
    under role `courtroom_upstream_cite`,
  - lists `BLINDNESS_PROTOCOL.md` under role `courtroom_seal_protocol`,
  - declares ATLAS / CMS / LHCb / ALICE publication-index slots under
    role `external_cern_anchor_index` for CR090 to populate.
- The CR089 declared premises file lists the 09a load-bearing CR ids
  and the QP075 closure-row count (35), role-operator count (26), and
  free-parameter count (0) verbatim.
- Anchor-side discipline is declared:
  - admissible: ATLAS, CMS, LHCb, ALICE, plus CERN antimatter programs.
  - inadmissible: PDG averages, Tevatron (CDF, D0), B-factories (Belle,
    BaBar, SuperKEKB / Belle II), Fermilab muon g-2, KamLAND, etc.
- Blindness protocol discipline is declared and the cite-in-rule is
  active: every later 13-branch CR result file must contain
  `blindness_protocol_cite` and `blindness_protocol_sha256`.
- The four blindness-protocol pillars are named verbatim in the
  declared premises:
  - PILLAR_1_STRUCTURAL_BLINDNESS_ZERO_FREE_PARAMETERS
  - PILLAR_2_PROCEDURAL_BLINDNESS_PRE_COMMIT_PREDICTION_HASH
  - PILLAR_3_CROSS_SOURCE_BLINDNESS_MULTI_EXPERIMENT_REDUNDANCY
  - PILLAR_4_HONEST_NEGATIVE_DISCIPLINE_CR096_MUST_REJECT
- The CERN-side blindness attestations are recorded in the declared
  premises (no private CERN data, no SAM sharing with CERN, no runner
  network access).

## Wrong Controls (Discipline Checks)

These are protocol-discipline checks. They verify that the branch
plumbing rejects malformed or off-protocol inputs at the right gate.
None of them gates the 09a verdict; they gate the 13-branch runner.

- A PDG-only anchor on any CR091-CR095 row must be rejected at
  **Gate A admissibility** (`cern_anchor_admissibility` check),
  BEFORE residual is computed. PDG is context-only per the seal.
- A Tevatron / B-factory / Fermilab / non-CERN-neutrino anchor on
  any CR091-CR095 row must be rejected at **Gate A admissibility**
  (`cern_anchor_admissibility` check), BEFORE residual is computed.
  These belong in CR096 honest-negative classes B/C/D/E and are
  rejected on source, not residual.
- An attempt to use a CERN measurement value as a free parameter on
  the prediction side must fail the
  `prediction_side_immutability_against_09a` check. 09a is the locked
  prediction side; 13 cite-onlies it.
- An anchor row missing arXiv id / CDS record / journal reference must
  fail the `cern_anchor_citation_completeness` check at envelope-seal
  time, BEFORE the runner is invoked.
- A runner whose evidence row has `anchor_envelope_open_utc` preceding
  `prediction_commit_utc` must fail the
  `temporal_ordering_blindness_check` and emit
  `BLINDNESS_VIOLATION_DETECTED`. The affected row falls to
  DIAGNOSTIC; the 09a prediction is unchanged.
- A runner that opens the anchor envelope before writing the
  prediction commit hash must fail the
  `procedural_blindness_step_order_check`. Same handling as above.
- A CR result file missing `blindness_protocol_cite` or
  `blindness_protocol_sha256` falls to DIAGNOSTIC. It is not counted
  in the CR097 agreement-count summary and it does not falsify 09a.

Per the BLINDNESS_PROTOCOL `09a Immutability Rule`, none of these
wrong-control checks can modify or re-fit 09a's prediction surface.
They protect the 13-branch plumbing; they do not put 09a on trial.

## Rule-9 Line

```text
This test could have falsified the 13 branch source-lock - the audit-
chain inheritance from 09a and the blindness-protocol cite-in
discipline - if the seal was missing or unsigned, if the BLINDNESS_PROTOCOL
was not cited and sha256-recorded, if the 09a verdict was not cited
cleanly as the immutable prediction-side audit chain, if PDG or non-CERN
values were allowed as CR091-CR095 anchors at Gate A, or if any CERN
value was permitted to modify the upstream 09a prediction surface.

This test does NOT falsify 09a. 09a stands as exemplary regardless of
what CR089 finds. CR089 protects the 13-branch plumbing only.
```

## Cross-CR Links

```text
upstream  09a/CR059a (allowed inputs lock; this CR mirrors that pattern
                       one layer up on the anchor side)
upstream  09a/CR064a (branch verdict; this CR cites it as audit-chain
                       head)
forward   CR090 CERN BLANK INVENTORY AND COVERAGE MAP
forward   CR091..CR095 CERN-class anchored tests
forward   CR096 CERN honest negatives
forward   CR097 13 branch verdict zipper
```

## Note On Seal Sha256

```text
CR089 may be drafted before the seal sha256 sibling exists. It may not
be claimed PASS until the seal sha256 sibling file
SEALED_CERN_INDEPENDENT_TESTS_SCOPE_APPROACH_2026_06_13.sha256.txt
exists in the branch root.
```
