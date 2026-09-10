# Starbreaker / Weak-CCSN Pixel Bridge Precommit

[Back to tests](README.md)

Test identity: `CR:CR005e@SAM-RESEARCH`.

## Failure

Locks the weak-CCSN pixel-bridge design whose execution stopped on the first Starbreaker scenario at the trace-residue gate before any morphology statistic or scientific verdict opened.

**Question:** Can the original Starbreaker weak-CCSN tensor construction pass its trace-residue gate and open the precommitted morphology comparison?

**Calculation:** Construct the original per-scenario tensor surface, evaluate the trace-residue gate, and only if it passes project both sides onto the fixed pixel/Hellinger comparison.

**Recorded outcome:** CR005e stopped on the first Starbreaker scenario because trace residue exceeded the precommitted threshold; no external morphology comparison, statistic, or scientific verdict was executed.

**Scope of this result:** This is a preserved construction failure, not a falsification of the Starbreaker concept or a waveform-comparison result.

**Controls:**

- External-waveform provenance fixed before execution.
- Trace-residue gate checked first.
- No morphology statistic or verdict opens after a failed construction gate.

**Diagnostic comparisons:**

- Continue to Hellinger comparison after trace failure.
- Repair the tensor inside the same run.
- Change source population, grid, view count, or statistic after seeing the failure.

[Read the original test](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/bba038648cc06ba92a671b4db9f3f0c746669c21/starbreaker/21_GRAVITATIONAL_WAVES/CR005e_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE/CR005e_PRECOMMIT.md)

<details>
<summary>Exact source record</summary>

```json
{
  "alternate_source_paths": [
    "starbreaker/21_GRAVITATIONAL_WAVES/CR005e_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE/CR005e_CONTRACT.json",
    "starbreaker/21_GRAVITATIONAL_WAVES/CR005e_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE/CR005e_FAILED_RUN_RECEIPT.json",
    "starbreaker/21_GRAVITATIONAL_WAVES/CR005e_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE/CR005e_PRECOMMIT_SEAL.json",
    "starbreaker/21_GRAVITATIONAL_WAVES/CR005e_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE/CR005e_RUNNER_SEAL.json",
    "starbreaker/21_GRAVITATIONAL_WAVES/CR005e_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE/CR005e_SOURCE_MANIFEST.json",
    "starbreaker/21_GRAVITATIONAL_WAVES/CR005e_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE/CR005e_runner.py"
  ],
  "approval": null,
  "description": "Starbreaker / Weak-CCSN Pixel Bridge Precommit",
  "family": "CR",
  "keywords": [
    "SN",
    "Starbreaker",
    "Weak",
    "CCSN",
    "Pixel",
    "Bridge",
    "Precommit"
  ],
  "qualified_test_id": "CR005e@SAM-RESEARCH",
  "record_key": "CR:CR005e@SAM-RESEARCH",
  "related_test_ids": [],
  "reviewed_and_approved": false,
  "source_basis": "SAM_REPOSITORY_SOURCE_ARTIFACT",
  "source_commit": "bba038648cc06ba92a671b4db9f3f0c746669c21",
  "source_path": "starbreaker/21_GRAVITATIONAL_WAVES/CR005e_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE/CR005e_PRECOMMIT.md",
  "source_repo": "SAM_Research_Project",
  "source_sha256": "40ecba8151b2c4b0374e4ad3b8a38acd771a0c95d2ea015d59eb77f342565596",
  "source_status": null,
  "source_url": "https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/bba038648cc06ba92a671b4db9f3f0c746669c21/starbreaker/21_GRAVITATIONAL_WAVES/CR005e_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE/CR005e_PRECOMMIT.md",
  "source_verdict": null,
  "test_id": "CR005e",
  "volume_numbers": [
    "I",
    "III"
  ]
}
```

</details>


Public Courtroom source recovered by exact file identity: [complete copied test package](../../../courtroom/21_GRAVITATIONAL_WAVES/CR005e_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE). This preserves code, precommitments, controls and results together.
