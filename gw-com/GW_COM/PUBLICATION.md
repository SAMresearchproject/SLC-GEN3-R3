# GW-COM folder publication

Destination: [SAMresearchproject/SLC-GEN3-R3, main/gw-com](https://github.com/SAMresearchproject/SLC-GEN3-R3/tree/main/gw-com).

This folder publishes the GW-COM implementation, campaign contracts, frozen code snapshots, scientific reports, signed waveform/residual histories, candidate/control/decoded records and validation summaries. Five successive campaigns are included, from the original interval demonstration through the exactly-three-tests study. Earlier six-value payloads remain historical records; the current payload includes 3.

The research source repository and this public repository have distinct Git histories. The publication is a new `gw-com/` folder on the destination main branch. It preserves the original GW_COM/, SAM_REVIEW/ and selected SAM_HISTORY/ layout beneath that folder so existing relative links and frozen artifact paths remain meaningful. Selected numbered GW history records are provenance excerpts; they do not install the full research repository's live-authority system into this public repository.

## Execution and archive boundary

The experiments executed on SLC-GEN3-R4 / SLC-GEN3-CEV1-R4, STARBREAKER / SB-GEN3-ACCUMULATION-R1, generation GEN3-BETHE1-20260917-G1. The runners require the full research environment, including SAM_PROJECT DomainSession and its domain registry/resource launcher. This publication does not upgrade or replace the destination's runtime distribution. The entrypoint paths and original hashes remain unchanged for custody.

The research repository's existing slim-sync policy excludes native-call archives and other generated trees from ordinary Git publication. [LOCAL_ARCHIVE_MANIFEST.json](LOCAL_ARCHIVE_MANIFEST.json) lists every excluded GW-COM file with its size and SHA-256. Original files remain in the local research repository. Consequently, links to excluded call archives and full receipt-chain verification require those local files; the public folder alone is not a complete execution archive. Published waveform, fit, signed residual and scientific-result files remain available for inspection.

Native archive contents are not replaced by invented or empty receipts. Saved validation summaries describe checks made against the complete local evidence before publication.

The Advanced LIGO design curve is retained with its upstream URL and checksum in the three-tests campaign's sources/PROVENANCE.json. Other paper references remain links. Attribution: Sean Brady, originator/conceptual director; OpenAI ChatGPT and Codex, AI research collaborators.
