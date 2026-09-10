# Standalone license decision

Status: **RESOLVED — PUBLICATION ENABLED**

Sean Brady selected a layered, share-forward license for the standalone SAMA
repository on 2026-08-26:

| Material | License or rule |
|---|---|
| Original atlas prose, mathematical exposition, diagrams, tables, structured registries, metadata and generated navigation | `CC-BY-SA-4.0` |
| SAMA software under `tools/` and files explicitly marked as software | `AGPL-3.0-or-later` |
| Source snapshots and identified third-party material | Originating terms; no silent relicensing |
| SAM/SLC invention and physical-implementation patent rights, protected SLC internals, trademarks and private material | No license grant beyond any express AGPL contributor terms for covered software |

The complete scope and attribution terms are in [LICENSE.md](LICENSE.md), with
the standard legal texts under [LICENSES/](LICENSES/README.md) and notices in
[NOTICE.md](NOTICE.md).

## Decision rationale

CC BY-SA makes the public mathematical atlas readable, teachable, remixable
and commercially usable while requiring attribution and share-alike treatment
of adaptations. AGPL applies the same share-forward purpose to validation and
navigation software, including modified versions operated as network
services.

The license decision does not expose or license material excluded by the
[public disclosure policy](PUBLIC_DISCLOSURE_POLICY.md). It does not change
owner approval, result classification, external validation, patent status or
source-repository authority.
