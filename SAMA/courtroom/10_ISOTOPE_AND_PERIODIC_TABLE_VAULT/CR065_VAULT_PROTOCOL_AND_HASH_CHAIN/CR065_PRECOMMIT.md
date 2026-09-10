# CR065 Vault Protocol and Hash Chain - Precommit

```text
document_id:    CR065_PRECOMMIT
branch:         10_ISOTOPE_AND_PERIODIC_TABLE_VAULT
cr_slot:        CR065
sealed_before:  CR065 runner exists and CR065 result exists
seal_anchor:    SEALED_ISOTOPE_AND_PERIODIC_TABLE_VAULT_SCOPE_APPROACH_2026_06_13
                (sha256: 9ff6d79e8e5c63c614e70a6cce2affa0510cc77e7fbf8781fc0a55fe940688b5)
manifest:       10_ISOTOPE_AND_PERIODIC_TABLE_VAULT/SOURCE_MANIFEST.csv  (155 entries)
date_local:     2026-06-13
```

## Rule

```text
Do not assert any physical claim in CR065. CR065 only certifies the
chain of custody.
Hash every QP049-QP061 + QP068 source artifact in quantum_phase BEFORE
declaring CR065 PASS.
Verify byte-equivalence between SAMs_TOE\sealed_results\QP061_isotope_vault\
and the quantum_phase QP061 artifact directory.
Verify that the IAEA LiveChart external anchor on disk matches the
sha256 recorded in qp061_external_source_manifest.csv.
Lock SOURCE_MANIFEST.csv as the only allowed input registry for
CR066-CR072.
```

## Question

```text
Can the QP isotope vault chain of custody be independently verified such
that:
  (a) every QP049-QP061 + QP068 source file's sha256 matches the
      SOURCE_MANIFEST.csv entry,
  (b) the sealed_results\QP061_isotope_vault\ package is byte-equivalent
      to its quantum_phase counterpart,
  (c) the IAEA LiveChart external roster on disk matches the sha256
      recorded by QP061 at retrieval time
      (8aee5dc431af1e35fcb49746387b83e927b3c300e7787defbda621a08212c795),
  (d) the SOURCE_MANIFEST.csv itself is hashed and sealed as the only
      allowed input registry for the remainder of the 10 branch?
```

## Declared Premises

```text
P1. Source set:
      QP049 seed identity                          (qp_artifact + report + src)
      QP050 symmetric seed mass                    (cross-branch shared with 09)
      QP051 neutron-excess binding-depth lane      (no .py — derivation only)
      QP052 numeric ΔN binding mass                (cross-branch shared with 09)
      QP053 roster stability lane
      QP054 isotope neighbor ladder
      QP055 Phase 5 isotope freeze
      QP056 residual stability / decay pressure
      QP057 decay direction chain
      QP058 pressure freeze
      QP059 visual package
      QP060 sealed comparison protocol
      QP061 IAEA LiveChart comparison
      QP068 high-Z sealed miss structure readout
      All sourced from C:\VS\quantum_phase
      All sha256 captured in SOURCE_MANIFEST.csv at manifest build time.

P2. Sealed vault package:
      C:\VS\SAMs_TOE\sealed_results\QP061_isotope_vault\ contains:
        QP061_PRIVATE_APPROVED_SEALED_ISOTOPE_COMPARISON.md
        qp061_summary.json
        qp061_band_summary.csv
        qp061_external_source_manifest.csv
        README.md
      Each file must be byte-equivalent to its quantum_phase counterpart
      at the recorded source_commit b2a87e893068309352bf864f4d2efc48011ff40f.
      Current quantum_phase HEAD is f3d26b4b373d72d35856fc7050aa984982a00271
      (newer than the sealed-vault commit). CR065 must verify against the
      sealed-vault commit, not the current HEAD.

P3. External anchor authority - actual upstream:
      The QP arm pulls a single external authority for the isotope roster:
        Authority:   IAEA LiveChart of Nuclides
        Endpoint:    https://nds.iaea.org/relnsd/v1/data?fields=ground_states&nuclides=all
        Retrieval:   2026-06-08T22:49:23+00:00
        Approved by: Sean Brady
        sha256:      8aee5dc431af1e35fcb49746387b83e927b3c300e7787defbda621a08212c795
        Local path:  quantum_phase\artifacts\qp061\external\iaea_livechart_ground_states_all_qp061.csv
      The seal's prescriptive AME2020 / NIST / IUPAC import order is
      a future-expansion protocol; only IAEA LiveChart is in actual use.
      CR065 verifies the IAEA LiveChart chain only. If AME2020 / NIST /
      IUPAC are later added, a separate CR will be opened under M3 appeal.

P4. Manifest authority:
      SOURCE_MANIFEST.csv at 10_ISOTOPE_AND_PERIODIC_TABLE_VAULT root is
      the ONLY allowed input registry for CR066-CR072.
      Its sha256 is captured at CR065 execution into
      CR065_source_manifest_hash.json and promoted to
      10_ISOTOPE_AND_PERIODIC_TABLE_VAULT/SOURCE_MANIFEST.csv.sha256.txt.

P5. Cross-branch dependency:
      The 09 branch SOURCE_MANIFEST.csv hash is recorded in 10's manifest.
      CR065 verifies the 09 manifest hash matches the on-disk file.
      If the 09 manifest has drifted, CR065 flags but does not block.
      Cross-branch drift handling belongs to CR067.

P6. Forbidden (CR065-specific):
      - Asserting any physical claim about isotope masses or roster contact
      - Reading sealed_results\QP061_isotope_vault\ as anything other than
        a copy for byte-equivalence audit
      - Treating BOUNDARY as a valid CR065 outcome (this is chain of custody,
        not boundary structural derivation)
      - Importing any artifact not appearing in SOURCE_MANIFEST.csv
```

## Outcome Taxonomy

```text
PASS:
  - Every SOURCE_MANIFEST.csv sha256 verifies against the on-disk file.
  - The 5 sealed_vault_package files are byte-equivalent to their
    quantum_phase QP061 counterparts at the sealed-vault commit.
  - The IAEA LiveChart sha256 on disk equals
    8aee5dc431af1e35fcb49746387b83e927b3c300e7787defbda621a08212c795.
  - SOURCE_MANIFEST.csv sha256 is captured to
    CR065_source_manifest_hash.json and promoted to
    SOURCE_MANIFEST.csv.sha256.txt.
  - The 09 cross-branch manifest hash matches the on-disk 09 manifest
    (or is flagged with a non-blocking drift note).

DIAGNOSTIC:
  - Any sha256 in SOURCE_MANIFEST.csv does not verify against its
    on-disk file.
  - Any sealed_vault_package file is not byte-equivalent to its
    quantum_phase counterpart at the sealed-vault commit.
  - IAEA LiveChart sha256 on disk differs from the QP061-recorded value.
  - SOURCE_MANIFEST.csv references a file path that does not exist.
  - source_commit in SOURCE_MANIFEST.csv does not match the actual
    repository commit at hash time.

FAIL:
  - The vault is shown to have consumed an artifact not in
    SOURCE_MANIFEST.csv.
  - The IAEA LiveChart artifact contains rows that postdate the
    retrieval timestamp 2026-06-08T22:49:23+00:00 (would indicate
    a target-driven backfill).
  - The sealed_vault_package contains a file not present in
    quantum_phase, indicating post-hoc edit.

BOUNDARY:
  - Not a valid CR065 outcome per the 10 seal.
  - If CR065 cannot produce PASS / DIAGNOSTIC / FAIL, the test is rerun
    with the missing data supplied.
```

## Rule-9 Line

```text
This test could have falsified: the claim that the QP isotope vault has
an independently verifiable chain of custody from quantum_phase source
to sealed_results package, with byte-equivalent vault snapshot and a
hash-locked IAEA LiveChart external anchor, before any roster contact
is asserted.
```

## Expected Artifacts

```text
CR065_PRECOMMIT.md                          (this file)
CR065_VAULT_PROTOCOL_AND_HASH_CHAIN.py      (runner script)
CR065_input_manifest.csv                    (subset of SOURCE_MANIFEST
                                             that CR065 reads)
CR065_qp_artifact_hash_check.csv            (per QP file: declared sha256
                                             / observed sha256 / status)
CR065_sealed_vault_byte_equivalence.csv     (per sealed_results file:
                                             quantum_phase counterpart /
                                             diff status)
CR065_external_anchor_verification.json     (IAEA LiveChart hash check)
CR065_source_manifest_hash.json             (sha256 of SOURCE_MANIFEST.csv
                                             at CR065 execution)
CR065_cross_branch_manifest_check.json      (09 SOURCE_MANIFEST.csv hash
                                             / observed / drift status)
CR065_wrong_controls.csv                    (declared wrong inputs - see
                                             below)
CR065_summary.json                          (machine-readable verdict)
CR065_result.md                             (human-readable verdict)
HASHES.txt                                  (sha256 of all CR065 output
                                             files)
SOURCE_MANIFEST.csv.sha256.txt              (sealed at CR065 PASS)
```

## Wrong Controls (declared in advance)

CR065's wrong-control set must include at least these injections, and
each must trigger a DIAGNOSTIC or FAIL outcome:

```text
WC1: corrupt one sha256 in SOURCE_MANIFEST.csv so the on-disk hash
     differs  -> expected: DIAGNOSTIC on hash mismatch
WC2: add a row to SOURCE_MANIFEST.csv pointing at a file that does
     not exist  -> expected: DIAGNOSTIC on missing file
WC3: edit one byte of the local
     iaea_livechart_ground_states_all_qp061.csv so the hash differs
     from 8aee5dc4...  -> expected: DIAGNOSTIC on external anchor
     hash mismatch
WC4: edit one byte of a sealed_vault_package file so it differs from
     the quantum_phase counterpart  -> expected: DIAGNOSTIC on
     byte-equivalence failure
WC5: inject a fabricated IAEA-LiveChart row dated after the
     2026-06-08 retrieval timestamp  -> expected: FAIL on
     target-driven backfill detection
WC6: reference a 09-branch-only artifact (a G611c file) as a target_cr
     for CR065  -> expected: DIAGNOSTIC on cross-branch boundary
     violation
```

If any wrong control passes, CR065's own verdict downgrades to
DIAGNOSTIC and the test is rerun.

## Vault Protocol Statement

```text
The vault protocol sealed by CR065 is the chain-of-custody contract for
the entire 10 branch:

  1. Every artifact consumed by any later CR (CR066-CR072) must appear
     in SOURCE_MANIFEST.csv with a verified sha256.
  2. The sealed_results\QP061_isotope_vault\ package is treated as a
     read-only snapshot of QP061 at source_commit
     b2a87e893068309352bf864f4d2efc48011ff40f. Any later quantum_phase
     change beyond that commit is out of scope for CR065.
  3. The IAEA LiveChart external anchor is fixed at the 2026-06-08
     retrieval. Any later IAEA-LiveChart update is out of scope until
     a new CR is opened under M3 appeal (APPEAL_FRONTIER_HIT or
     APPEAL_FRONTIER_MISS channel).
  4. SOURCE_MANIFEST.csv becomes immutable at CR065 PASS. Any later
     manifest edit triggers a new CR065-equivalent re-verification.
  5. If new QP tests post-dating QP075 are added under M3 appeal, they
     require a separate manifest extension CR, not an in-place edit.
```

## Sealed Premise Set

```text
The premise set P1-P6 above is sealed at CR065_PRECOMMIT write time.
No CR065 runner may add or alter a premise. If a premise needs revision
after CR065 runs, the revision belongs to an appeal CR per the Appeal
Channel section of the 10 seal.
```
