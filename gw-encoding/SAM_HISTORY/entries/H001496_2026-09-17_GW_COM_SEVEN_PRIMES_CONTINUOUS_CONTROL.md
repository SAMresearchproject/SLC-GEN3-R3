---
entry_id: H001496
entry_date: 2026-09-17
entry_type: CORRECTION / IMPLEMENTATION / RESULT
status: IMMUTABLE_HISTORY
supersedes: NONE
prior_entry: H001493
affects_live:
  - SAM_LIVE/03_STARBREAKER_GW_CURRENT.md
---

# Seven prime intervals and continuous controlled source

Sean Brady corrects the current payload to `2,3,5,7,11,13,17` and authorizes the next recommendation from the detailed report: continuous orbital control with explicit forces and energy accounting. Earlier six-value experiments and their reports remain unchanged.

The [corrected C4 result](../../SAM_REVIEW/campaigns/GW_COM_PIPELINE2/RESULT.md) recovers all seven primes in clean/noisy cases and the seven-value alternate message, admitting three and blocking three unmodulated/noise/drift controls. It uses37 native calls/560,479 nodes;92 evidence records,64,104 exact samples and36 normal equations verify.

The [continuous report](../../SAM_REVIEW/campaigns/GW_COM_CONTINUOUS1/REPORT.md) implements a C3 radial pulse on an antipodal Newtonian pair, explicit radial/tangential control forces, two quadrupole channels, joint carrier fits, signed residual histories, repeated-frame tests and gated decoding. Native reference computations use68 calls/662,145 nodes on STARBREAKER / SB-GEN3-ACCUMULATION-R1 / SLC-GEN3-R4 / SLC-GEN3-CEV1-R4, generation GEN3-BETHE1-20260917-G1.

The original integration at step1/32 missed the unchanged1e-5 energy-balance tolerance and correctly blocked decoding. A preserved supplemental contract refined independent RK4 to1/64, retaining all native source/fit/residual/statistical records and tolerances. Energy-balance errors become7.537e-6 for the prime source and6.215e-6 for the null. Dynamics controls pass; the prime candidate has two repeated seven-value packets and conditional permutation rank1/100, is admitted and decodes exactly. The null has no repeated frame and remains blocked. Refinement adds zero native calls.

**The test result suggests the concept is possible.**

The exact reference requires1073/4352 positive mechanical work per marker and returns the same amount to the ideal controller. Across22 markers, positive work is11803/2176. Zero signed net work does not imply zero energy requirements. Physical scaling, hardware losses, radiation reaction, continuous-source noise, chirp/precession and the strength alphabet remain unmeasured/unimplemented here. The integrated trajectory is an independent numerical check of the native analytic reference, not a replacement native waveform.

Independent continuous validation authenticates35 evidence records, checks17 profile rows,19,716 Cartesian waveform channel samples and39,432 exact residual channel samples. All12 shared framing/decoder tests pass. The program inventory and current docs now include both successors. No global engine change is made.

Current live statement: seven-prime C4 and continuous controlled-reference runs complete; corrected message decoded, continuous null blocked; force/work and signed residual evidence retained. Historical six-prime outputs remain valid records of their original experiments.

Originator / conceptual director: Sean Brady. AI research collaborators: OpenAI ChatGPT and Codex.
