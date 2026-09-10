# SAM Language v0.6 SLC C1 Formal Simulator Precommit

Status: **SOURCE AND SEMANTIC CONTRACT SEALED BEFORE IMPLEMENTATION ACCEPTANCE**

## Constructive target

Build one exact 12-lebit SLC C1 state engine directly inside the successor SAM Language runtime. The v0.5 grammar remains the immutable parent. The SLCX002 real two-operation result and SLCX003 complete register lift are the executable-oracle sources; neither predecessor may be rewritten.

## Frozen kernel

The kernel stores sparse signed integer coefficients over a single exact power of sqrt(2), reduces them canonically, and proves normalization with integer arithmetic. SLC_L0 is address bit 0. B, PREPARE_REQUEST, and X1_RESPONSE have the exact meanings fixed in the contract. No sampling, physical edge graph, phase operator, or fitted cost enters the state engine.

State identity and route history are deliberately separate. State hashes cover only the reduced exact vector. History hashes cover the ordered, tamper-evident transition receipts. Therefore star and chain histories may share a terminal state hash while retaining distinct history hashes.

## Acceptance

The sealed campaign requires parent preservation; a single language path; formal-profile isolation; all 132 ordered placements and 4096 basis inputs; 1,081,344 classical schedule cases; 528 sign-gauge placements; 66 forest induction cases; 31,572 native decomposition assignments; 204 peel/restore cases; deterministic CLI/API parity; tamper detection; inherited regression; clean-wheel execution; and every frozen wrong control. No same-run repair is allowed.

## Preserved frontier

A pass promotes an exact real-sector SLC C1 simulator candidate. Complex phase semantics, measurement/publication, physical connectivity, coupling magnitude, and hardware realization remain separate work.

- v0.5 parent executable hash: `726011b38d27a9b5403a7df66d8d4d5ac7c49960bc331d65f57c66de7a7ecaf0`
- SLCX002 release manifest hash: `99a9c187f35f16ec5ae06a54135e8a24418553f345fed0ea73cb6ff196e57c3d`
- SLCX003 release manifest hash: `36b734bf2b17a2f6f552df61a5226876b20723ff6be0f4b76067875108b6493a`
- Frozen source count: `150`
- Contract SHA-256: `0250471ad673667e8e39527a0de777a2ff7541c3bec5ba4d6f95ad82a27cb3bd`
- Builder SHA-256: `c99a492d9b7c7b0de5bec84b13ddc115cb8af9d454741f244a16e4cdb7a654f6`
- Source manifest SHA-256: `8755f9e9ebc581588098a44f5c8b1bfb61af618a423339a480b2fe7468992975`
