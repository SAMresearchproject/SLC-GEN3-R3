# Corrected seven-prime interval result

Sean Brady corrected the intended sequence to **2, 3, 5, 7, 11, 13, 17**.
This successor changes both the payload and framing to seven data intervals.
The previous six-value experiments and their reports remain preserved.

Clean and bounded-noise prime cases recover the complete corrected sequence.
A seven-value even-message control recovers `4,6,8,10,12,14,16`. Each retains
two disjoint repeated packets and permutation rank1/100 under the same99
shuffled-gap controls. Clean/noisy unmodulated and drift-only cases remain
blocked with zero repeated packet candidates.

**The test result suggests the concept is possible.**

Execution used37 current STARBREAKER / SLC-GEN3-R4 native calls and560,479
native graph nodes. Independent verification passed92 evidence records,
64,104 exact source/residual sample checks and36 normal equations. The shared
test suite passes12 tests, including full seven-value recovery, retention of
the historical six-value framing, and rejection of a truncated seven-value
frame. The decoder still receives no expected payload or primality test.

This preserves the first pipeline's dimensionless C4 scope and carrier/model
controls. The continuous-control successor is
[GW_COM_CONTINUOUS1](../GW_COM_CONTINUOUS1/CONTRACT.json).

- [Run outcomes and evidence links](run001/records/RUN_RESULT.json)
- [Independent verification](run001/VALIDATION.json)
- [Corrected contract](CONTRACT.json)
- [Clean decoded hypothesis](run001/records/prime_clean.decoded.data.json)
- [Noisy decoded hypothesis](run001/records/prime_noisy.decoded.data.json)

Run from the repository root with a new output name:

```bash
.venv-r3/bin/python CURRENT_REVISION/engines/SLC/gen3/resources.py run -- \
  .venv-r3/bin/python SAM_REVIEW/campaigns/GW_COM_PIPELINE2/run.py --run run002
```

The scientific contract is copied from the original pipeline with the owner's
payload correction and seven-interval framing; all other experimental choices
are retained. Both rejected and admitted outcomes remain inspectable.
