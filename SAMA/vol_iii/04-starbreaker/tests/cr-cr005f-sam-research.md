# Trace-Corrected Weak-CCSN Pixel Bridge Precommit

[Back to tests](README.md)

Test identity: `CR:CR005f@SAM-RESEARCH`.

## Correction

Freezes the sole permitted correction S_zz:=-(S_xx+S_yy) after finite differencing, with the source population, statistics, controls and claim boundary unchanged and CR005e left immutable.

**Question:** Does replacing only S_zz with -(S_xx+S_yy) after finite differencing repair the construction gate without changing the external comparison contract?

**Calculation:** After finite differencing, set S_zz:=-(S_xx+S_yy), then rerun the frozen construction and comparison pipeline.

**Recorded outcome:** CR005f precommits the sole trace-free projection correction S_zz:=-(S_xx+S_yy) after finite differencing and freezes all other CR005e choices.

**Scope of this result:** CR005f is a correction precommit, not a result. It repairs a construction fault without changing the external-comparison question or authorizing result-driven fitting.

**Controls:**

- Byte-identical non-S_zz inputs and parameters.
- No change to candidate-selection rules.
- Trace gate rerun before morphology.

**Diagnostic comparisons:**

- Alter S_xx or S_yy.
- Tune the correction against Hellinger outcomes.
- Replace the external waveform population.
- Delete the CR005e failed run.

[Read the original test](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/bba038648cc06ba92a671b4db9f3f0c746669c21/starbreaker/21_GRAVITATIONAL_WAVES/CR005f_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE_TRACE_CORRECTED/CR005f_PRECOMMIT.md)

<details>
<summary>Exact source record</summary>

```json
{
  "alternate_source_paths": [
    "starbreaker/21_GRAVITATIONAL_WAVES/CR005f_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE_TRACE_CORRECTED/CR005f_CONTRACT.json",
    "starbreaker/21_GRAVITATIONAL_WAVES/CR005f_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE_TRACE_CORRECTED/CR005f_FAILED_RUN_RECEIPT.json",
    "starbreaker/21_GRAVITATIONAL_WAVES/CR005f_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE_TRACE_CORRECTED/CR005f_PRECOMMIT_SEAL.json",
    "starbreaker/21_GRAVITATIONAL_WAVES/CR005f_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE_TRACE_CORRECTED/CR005f_RUNNER_SEAL.json",
    "starbreaker/21_GRAVITATIONAL_WAVES/CR005f_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE_TRACE_CORRECTED/CR005f_SOURCE_MANIFEST.json",
    "starbreaker/21_GRAVITATIONAL_WAVES/CR005f_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE_TRACE_CORRECTED/CR005f_runner.py"
  ],
  "approval": null,
  "description": "Trace-Corrected Weak-CCSN Pixel Bridge Precommit",
  "family": "CR",
  "keywords": [
    "SN",
    "Starbreaker",
    "Trace",
    "Corrected",
    "Weak",
    "CCSN",
    "Pixel",
    "Bridge"
  ],
  "qualified_test_id": "CR005f@SAM-RESEARCH",
  "record_key": "CR:CR005f@SAM-RESEARCH",
  "related_test_ids": [],
  "reviewed_and_approved": false,
  "source_basis": "SAM_REPOSITORY_SOURCE_ARTIFACT",
  "source_commit": "bba038648cc06ba92a671b4db9f3f0c746669c21",
  "source_path": "starbreaker/21_GRAVITATIONAL_WAVES/CR005f_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE_TRACE_CORRECTED/CR005f_PRECOMMIT.md",
  "source_repo": "SAM_Research_Project",
  "source_sha256": "aa2afd2a4d0b65707de359e1ce13af45acc520bf8afa8748d44ea04d19bb7495",
  "source_status": null,
  "source_url": "https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/bba038648cc06ba92a671b4db9f3f0c746669c21/starbreaker/21_GRAVITATIONAL_WAVES/CR005f_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE_TRACE_CORRECTED/CR005f_PRECOMMIT.md",
  "source_verdict": null,
  "test_id": "CR005f",
  "volume_numbers": [
    "I",
    "III"
  ]
}
```

</details>


Public Courtroom source recovered by exact file identity: [complete copied test package](../../../courtroom/21_GRAVITATIONAL_WAVES/CR005f_STARBREAKER_WEAK_CCSN_PIXEL_BRIDGE_TRACE_CORRECTED). This preserves code, precommitments, controls and results together.
