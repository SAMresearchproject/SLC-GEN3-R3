# ATOM3D — exact contact, Li-6 grammar and signed decoding

**14 September 2026: A3D41-T18-CONTACT-R2 on SLC-GEN3-R3 / SLC-GEN3-CEV1-R3; joint native successor A3D41-RXT-R3 on GEN3-RXT-R7.1.** Sean Brady is originator and conceptual director; OpenAI ChatGPT and Codex are research collaborators.

## What the model computes

ATOM3D constructs typed site, relation, phase and circulation inventories and computes their contact actions and complete minimum sets. The current ordinary contact family retains four native minima at action 2 and EDGE_000 closure; 113,664 readouts agree across the recorded implementations and nineteen check groups pass. **The test result suggests strong contact with the concept.**

The Li-6 grammar retains six one-body addresses, four center leaves, nine relations and five covers. Its site rank is 5 and cycle rank is 4, together recovering nine currents. Three-owner circulation selects COVER_03 and COVER_04, 64 histories each from 256; the hidden-nine/depth square selects the same 16 in both. Observed action is 737/16 and native action is 969/16. Six center placements and all 128 rho settings retain both covers and every tie. All 5,563,227 recorded values agree across H14F, Ryzen, 780M and T500; 216 result and 13 installation checks pass. **The test result suggests strong contact with the concept.**

## Code, simulation inputs and results

| Material | Public artifact |
|---|---|
| Native common-minimum calculation | [atom3d.cpp](../gen3-rxt/native/src/atom3d.cpp), [CUDA kernels](../gen3-rxt/native/src/atom3d_cuda.cu) |
| Engine, source bundles and build | [GEN3-RXT source guide](../gen3-rxt/README.md) |
| Li-6 inputs | [geometry](../evidence/A3D41_LI6_GRAMMAR_ASSEMBLY1/GEOMETRY.json), [contract](../evidence/A3D41_LI6_GRAMMAR_ASSEMBLY1/CONTRACT.json) |
| Li-6 simulation | [result](../evidence/A3D41_LI6_GRAMMAR_ASSEMBLY1/RESULT.json), [minimum bitsets](../evidence/A3D41_LI6_GRAMMAR_ASSEMBLY1/MINIMUM_BITSETS.npz), [validation](../evidence/A3D41_LI6_GRAMMAR_ASSEMBLY1/VALIDATION.json) |
| Construction derivation | [derivation](../evidence/A3D41_LI6_GRAMMAR_ASSEMBLY1/DERIVATION.md), [analysis code](../evidence/A3D41_LI6_GRAMMAR_ASSEMBLY1/analyze.py) |
| Signed readout simulation | [atlas](../evidence/A3D41_GEN2_SIGNED_READOUT1/ATLAS.json), [deltas](../evidence/A3D41_GEN2_SIGNED_READOUT1/DELTAS.json), [result](../evidence/A3D41_GEN2_SIGNED_READOUT1/RESULT.md) |
| Exact decoder | [decoder contract](../evidence/A3D41_GEN2_SIGNED_READOUT1/DECODER_CONTRACT.json), [decode.py](../evidence/A3D41_GEN2_SIGNED_READOUT1/decode.py), [recovered inverses](../evidence/A3D41_GEN2_SIGNED_READOUT1/COMPACT_INVERSES.json) |
| Shared receiver | [derivation and 98,304-history result](../evidence/VOLUME_I_A3D41_COMMON_RECEIVER3/RESULT.md) |
| Joint R7.1 simulation and policies | [completion](../evidence/GEN3_RXT_RH_WEEKEND1/results/R71_DOMAIN_FEEDBACK_COMPLETION.json), [learned models](../evidence/GEN3_RXT_RH_WEEKEND1/results/R71_FINAL_DOMAIN_FIT.json) |

The signed decoder recovers all 192 state/cover/placement configurations at rho=1 from two independent Write responses and one signed N01 bit. Eight of 153 probe pairs distinguish 96 global-reversal pairs; the signed bit restores orientation. The recorded 192 native inverses, 3,456 arithmetic checks and fresh recovery pass across 1,091 native calls. **The test result suggests strong contact with the concept.**

## Implications and current work

These constructions connect observed responses to exact hidden state alternatives while preserving phase, circulation, identity and ties. The native R7.1 extension computes complete common minima and supplies their features to acquired construction policies. Its completed feedback cycle contains 36,864 fresh families, with common-minimum development balanced accuracy 847/936.

The separate GEN3 distinct selector reduces reports from 516 to 508 on 224 histories and from 633 to 625 on 256 fresh histories; all 256 opposite-host replays match. That selector campaign remains owner-paused. Physical spin, magnetic and quadrupole coefficients and MeV work are also owner-paused. The earlier unit-source transfer of 37.585174231 MeV against the 1.473758321 MeV atomic reference retains **The test falsifies the concept.** for that transfer. These recorded outcomes have their own source mappings; the completed contact and decoder results retain their classifications.

The [SAMA matter volume](../../SAMA/vol_ii/README.md) supplies the conceptual development. [Reproduction scope](../REPRODUCIBILITY.md) describes the original Python orchestrators and the native source distribution.

The complete [98,304-history reception/inverse dataset](../evidence/VOLUME_I_A3D41_COMMON_RECEIVER3/runs/run002/RECEPTION_INVERSE.jsonl.gz) and its [native word receipts](../evidence/VOLUME_I_A3D41_COMMON_RECEIVER3/runs/run002/NATIVE_WORD_RECEIPTS.jsonl.gz) are included as compressed JSON Lines.
