# CR005h precommit

- Campaign: `CR005h_STARBREAKER_PER_CARRIER_GW_CANDIDATE_LEDGER`
- Task: `Build a per-carrier Starbreaker gravitational-wave candidate ledger`
- Classification: `CONSTRUCTIVE_NEW_WORK`
- Preflight: `artifacts/preflight_filled/PREFLIGHT_20260720_233232_no_script.md`
- Frozen at: `2026-07-21T04:38:10.7546530Z`
- Runner present at seal: **no**
- Results opened before seal: **no**
- Same-run repair: **prohibited**

## Question frozen before computation

Construct a complete occurrence-level ledger for all 53,568 Starbreaker carriers. For each carrier, compute its unit-occurrence trace-free quadrupole source on the already-frozen post-collapse flow, its individual power, and its exact leave-one-out change in aggregate power. Reuse the sealed CR005d bind/escape timing ledger; do not refit histories and do not import an external waveform.

The primary identity test is the 18-value `ledger_slot` surface. A slot is a strong candidate only if its population is majority `escape_only`, its occurrence population is majority positive reinforcement, and its median normalized leave-one-out contribution is positive behind every frozen seed door and in both frozen geometries. The result may still be scientifically useful if the complete ledger constructs but no identity survives those gates.

## Interpretive firewall

This campaign ranks internal quadrupole-source contributors. It does not identify a material constituent of a gravitational wave, derive physical strain or luminosity, establish a physical mass center, or compare against detector data. Positive and negative leave-one-out values are coherent source reinforcement and cancellation within the frozen unit-occurrence proxy.

## Chronology

The contract, this precommit, and the source manifest are sealed before the runner is written. The runner must verify their hashes, validate every source before and after computation, write to a private staging directory, and publish the release atomically. A failed run is immutable.
