[SAM](../../README.md) · [Volume IV](../README.md) · [Branch](README.md) · [Related tests](tests/README.md)

# RH Evidence, Public Custody, and Reproducibility

## Conceptual abstract

Volume IV routes every concise statement to one of three evidence forms:
current interpretive authority, immutable numbered history, or executable
public custody. It does not copy the full SAM/SLC workspaces and does not use a
stale local public checkout as current authority.

## 1. Current source pin

The controlling source is the included
[RH current-authority snapshot](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/rh/RH_CURRENT_AUTHORITY_SNAPSHOT.md),
whose SHA-256 is recorded in `provenance/SOURCE_MANIFEST.json`. It identifies
H000689 as the current history entry, the Q2 RH adapter as current, and the
strong-contact classification.

## 2. Public custody

H000689 records public RH `main` at

```text
cb1c6529343b578528e9737e302d730a6650e665
```

with the source-transversality paper timestamped in HTML, PDF, and DOCX. The
included [publication-custody record](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/sources/rh/H000689_PUBLICATION_CUSTODY.md)
fixes the commit, timestamp, paths, and SHA-256 values.

The [curated migration ledger](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/provenance/PUBLIC_CURATED_MIGRATION.json)
records that the public chain retains bundles 0001–0009, 0011–0013, and 0015.
Bundle 0010 is withdrawn. Prepared bundle 0016 is excluded because H000689
states that it was not part of the paper-only publication.

## 3. Reproducibility layers

```text
atlas document
  -> atomic and result IDs
  -> source-qualified path and history IDs
  -> source commit or bundle manifest
  -> executable verifier and frozen artifact hashes
```

The atlas validator verifies its own source snapshots, mappings, content
hashes, and generated indices. Public bundle verifiers remain the authority
for their bundles; this repository does not reproduce large ledgers simply to
duplicate those checks.

## 4. Public-safe boundary

Excluded material includes executable RH-Q2/SLC internals, private physical
SLC mappings, patent/counsel material, personal paths, raw bulk ledgers,
withdrawn exports, and unpublished bundle 0016. Conceptual interfaces and
public hashes remain sufficient for the atlas reading surface.

## Evidence and records

Atomic records: `SAMA-C000283-R001`, `SAMA-C000288-R001`,
`SAMA-C000289-R001`.
RH result routes: `SAMA-RH-R0022`, `SAMA-RH-R0023`.

See the [master provenance matrix](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/provenance/MASTER_PROVENANCE_MATRIX.md)
and [RH result index](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/evidence/RH_RESULT_INDEX.md).

## Revision boundary

This unapproved chapter records custody only. It creates no remote, performs
no publication, and records no new external-validation result.

<details>
<summary>Source and revision details</summary>

Source document: `SAMA-D000072`. [Original published chapter](https://github.com/iwtbotiwtwot/SAMA/blob/5fa6bad8d4fec6596098755139db50b2eac37c05/documents/standard/RH_EVIDENCE_PUBLIC_CUSTODY_AND_REPRODUCIBILITY.md).

The source review fields remain `reviewed_and_approved: false` and `approval: null`. This reorganization changes presentation and navigation.

</details>
