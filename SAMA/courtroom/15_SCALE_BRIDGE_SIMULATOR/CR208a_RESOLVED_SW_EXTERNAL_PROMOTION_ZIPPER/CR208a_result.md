# CR208a Resolved-SW External Promotion Zipper

## Verdict

```text
CR208a_PASS_EXTERNAL_RESOLVED_PARENT_TOPOLOGY_BRIDGE_ESTABLISHED__BOUNDARY_FULL_EW_THEOREM_OPEN
```

## Courtroom Fields

```text
execution_status = CLEAN
scientific_verdict = PASS
triage_bin = A
claim_tier = RESOLVED_SW_EXTERNAL_PROMOTION_ZIPPER
```

## Question

Can the resolved-SW external topology promotion ladder be zipped while preserving original boundary verdicts?

## Pass Conditions

| condition | pass |
|---|---:|
| cr204_remains_boundary | true |
| cr204a_external_topology_pass | true |
| cr207_remains_boundary | true |
| cr207a_external_chain_pass | true |
| cr204a_manifest_hash_preserved | true |
| cr204a_manifest_hash_sibling_present | true |
| cr208_wrong_controls_preserved | true |
| g756_replay_trace_hashes_present | true |
| cr207a_chain_fingerprint_present | true |
| no_free_parameters | true |

## Evidence Rows

| key | value | note |
|---|---:|---|
| claim_ladder | CR204 BOUNDARY; CR204a PASS; CR207 BOUNDARY; CR207a PASS | original boundaries preserved |
| scoped_pass | external resolved-parent topology bridge established | CR208a scoped verdict |
| remaining_boundary | full particle-sector / electroweak theorem closure remains open | not claimed by zipper |
| metadata_manifest_sha256 | 332599bd79e84ef74918561c296a7cc9783a0078c68c44b89881883e3a062235 | CR204a allowed-import manifest |
| wrong_control_report | 43/43 passed; 0 failed | from CR208 |
| wrong_control_report_sha256 | 00d1ae99917fd746073702ec2a47e9a9da76788febd723567d0413798b20a311 | CR208_summary.json |
| replay_trace_hash_count | 5 | from G756 closed-loop summary |
| replay_trace_hashes | G756c_run_A_replay_trace.jsonl=5627799a6e2d974546ca68f40914bce16f02dae37b5ecf6de2f93c3c442ea2ee; G756c_run_B_inventory_trace.jsonl=264965b9b4a48d413160646874a8b96a0bd146915f17d2012baa17160390153b; G756c_run_C_chladni_trace.jsonl=4a3cb7af36021f70a33103aab6bd8446f08b9565022d2f97b38e7de409fefc45; G756c_run_D_resolved_sw_trace.jsonl=18fb9045d730c48aa2a64c11b5e724a79d6a153a6c6cbdb737169306785e7ceb; G756c_run_E_wrong_control_trace.jsonl=7ff2e062eca3e716677561bc68f4643c500a5bd2ec6df08805d50e59e622baff | from G756 closed-loop summary |
| cr207a_chain_fingerprint | f72e4a1fe7e300b920e62f32aeb7c25ba94a6acac77ceca69db959e0970336d8 | external-chain replay fingerprint |
| cr208a_zipper_fingerprint | e4b10b634c18eb802a4e177b30506bf8821cdb169144294fc84034d35009878f | this zipper payload fingerprint |

## Rule-9 Line

```text
This test could have falsified the claim that the simulator's resolved-SW grammar has a clean external topology promotion path while preserving original boundary verdicts, metadata hashes, wrong-control evidence, and replay traces.
```

## Notes

- CR204 and CR207 remain BOUNDARY.
- CR204a and CR207a are the promotion artifacts that pass.
- The scoped pass is topology-bridge establishment; full particle-sector/electroweak theorem closure remains open.
