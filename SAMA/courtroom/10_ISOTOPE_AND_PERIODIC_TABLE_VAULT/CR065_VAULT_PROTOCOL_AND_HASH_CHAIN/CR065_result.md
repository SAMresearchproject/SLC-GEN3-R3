# CR065 Vault Protocol and Hash Chain

## Verdict

```text
CR065_PASS_VAULT_CHAIN_OF_CUSTODY_VERIFIED
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
```

## Reason

```text
vault chain of custody verified end-to-end
```

## Phase Summary

```text
Phase 1 hash verification           verified=155  mismatches=0  missing=0
Phase 2 vault byte-equivalence      checked=5  byte_equivalent=5  diverged=0
Phase 3 IAEA external anchor        status=verified  iaea_sha_matches=True  retrieval_within_seal=True
Phase 4 09 cross-branch manifest    status=match  match=True
Phase 5 wrong control injections    passed=6/6
```

## Sealed-Vault Commit

```text
quantum_phase commit b2a87e893068309352bf864f4d2efc48011ff40f
sealed_results files byte-equivalent against quantum_phase at that commit
```

## External Anchor

```text
authority    = IAEA LiveChart of Nuclides
endpoint     = https://nds.iaea.org/relnsd/v1/data?fields=ground_states&nuclides=all
retrieval    = 2026-06-08T22:49:23.035093+00:00
declared sha = 8aee5dc431af1e35fcb49746387b83e927b3c300e7787defbda621a08212c795
local sha    = 8aee5dc431af1e35fcb49746387b83e927b3c300e7787defbda621a08212c795
qp061 sha    = 8aee5dc431af1e35fcb49746387b83e927b3c300e7787defbda621a08212c795
```

## Manifest Hash

```text
SOURCE_MANIFEST.csv sha256 = cd7cf11094ae00cfcbdae7c0be5c4577da715c65d1463b187f9596021e8d60d2
captured_at_utc            = 2026-06-13T07:05:24Z
```

## Rule-9 Line

```text
This test could have falsified: the claim that the QP isotope vault has
an independently verifiable chain of custody from quantum_phase source
to sealed_results package, with byte-equivalent vault snapshot and a
hash-locked IAEA LiveChart external anchor, before any roster contact
is asserted.
```

## Courtroom Reading

CR065 certifies the vault protocol and hash chain. PASS means the entire
chain is independently reproducible from the sealed-vault commit and the
declared IAEA retrieval. CR065 makes no physical claim about isotope
masses or roster contact - that is reserved for CR069.

## Artifacts

- `CR065_input_manifest.csv`
- `CR065_qp_artifact_hash_check.csv`
- `CR065_sealed_vault_byte_equivalence.csv`
- `CR065_external_anchor_verification.json`
- `CR065_source_manifest_hash.json`
- `CR065_cross_branch_manifest_check.json`
- `CR065_wrong_controls.csv`
- `CR065_summary.json`
- `HASHES.txt`
