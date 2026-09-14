# GEN2 separates A3D41's tied Li-6 constructions

**Two independent native Write responses and one signed site-current bit
recover all 192 retained Li-6 configurations exactly.** At known initial
history 14336, one Write on EDGE_002 or EDGE_006 already distinguishes all
twelve cover/placement alternatives. The tested continuation uses rho=1.

**The test result suggests strong contact with the concept.** The concept
tested is native response-based distinction and recovery of the retained
Li-6 source construction family.

Sean Brady directed the exploration and required genuine GEN2 algorithmic
computation whenever possible. Codex supplied the perturbation question,
technical map, source-bound orchestration and derivation. Execution used
**A3D41-T18-CONTACT-R2 / SLC-GEN2-R4.2 / SLC-GEN2-CEV1-R4.2** through the
ATOM3D project session. These are actual local installed GEN2 computations.

## New result

The original sixteen histories, two covers and six placements have the same
observed action, 737/16. Their responses to a new native quarter Write differ.
GEN2 executed 288 source transitions and 3,264 construction evaluations, then
computed 3,456 exact signed response differences with retained arithmetic DAGs.

With the initial history unknown, all eighteen scalar action probes resolve
96 pairs. The only remaining ambiguity is simultaneous global current reversal.
GEN2 searched all 153 pairs of signed probes; eight pairs achieve the same
96-class distinction. Every single probe has at most 24 outputs on this roster.

The selected decoder uses:

1. Observed source-action change after `EDGE_003 +1` (edge index 2).
2. Observed source-action change after `EDGE_007 -1` (edge index 5).
3. Signed N01 site readout `Re(alpha)+Im(alpha)`, exactly +1 or -1.

Each Write starts from the **same restored initial configuration**. GEN2's
native inverse recovers the original state, cover and placement for **192/192**
observations. All eight optimal probe-pair ties are retained. No physical
population weighting is inferred from the uniform information-accounting roster.

The [derivation](DERIVATION.md) explains the reversal symmetry and source
mapping. [Exact results](COMPACT_RESULT.json), [all inverse cases](COMPACT_INVERSES.json)
and [decoder contract](DECODER_CONTRACT.json) make the result directly reusable.

## Actual algorithmic execution and checks

- `T18_WORD`: native signed state transitions and retained ordered histories.
- `GEN2_BOUNDARY_OPEN`, LI6 source: compiled isotope forms and new exact responses.
- `GEN2_SIGNED_LOG`: 3,456 signed differences with operand provenance.
- `GEN2_CUSTODY`: exact finite inverse fibers and information profiles.
- `GEN2_FORMAL_LOG`: exact single-probe entropy comparisons and all optimal ties.
- `GEN2_READOUT`: the additional signed site-current polynomial.
- `GEN2_SIGNED_LOG_RESUME`: fresh-process graph recovery and new arithmetic.

Python enumerates requests, indexes returned data and writes artifacts. Its
independent Fraction checks match all 3,456 native differences. The 96
full-response inverse pairs all have the predicted global-reversal association.
Fresh native recovery and the usable decoder CLI pass. The session verifies
**1,091 returned calls, zero failed calls and zero incomplete calls**.

The initial analysis wrapper used the wrong entropy-field name. That
orchestration failure is preserved in [F001_ENTROPY_FIELD.log](F001_ENTROPY_FIELD.log).
The correction reads `prime_log_coefficients` and reuses the already completed
native calculations from their exact saved inputs/outputs. No numerical result
was replaced by the correction.

The complete receipt index is [SESSION_STATUS.json](SESSION_STATUS.json).
Stage indexes: [construction/transition calls](ATLAS_CALLS.json),
[arithmetic and information calls](ANALYSIS_CALLS.json),
[compact decoder calls](COMPACT_CALLS.json). Compressed session records restore
the exact input/output JSON using `SAM_PROJECT.receipt_storage.read_record`.

## Use and continuation

From the repository root:

```sh
python3 SAM_REVIEW/campaigns/A3D41_GEN2_SIGNED_READOUT1/decode.py \
  --observations '[247727778763, 99767836844, 1]'
```

This returns state 14336, cover 3, placement 0 through `GEN2_CUSTODY`, with a
new project receipt. The decoder remains bound to this completed rho=1 source
family and current session generation. A later GEN2 generation requires a
fresh project session carrying this source contract forward.

The new continuation is to use this distinguishable source family for physical
readout assignments and to extend the response map across rho. Physical spin,
magnetic/quadrupole coefficients and the MeV conversion remain unassigned.
The native phase-plane coordinates retain their source meaning. Both source
covers and all placements remain admitted; the experiment supplies a decoder,
not an observed choice of one construction for physical Li-6.

Owner disclosure: exact arithmetic resolves a cover difference of **43** inside
EDGE_002 response values of order 10^12 in candidate source-action units.
Fresh graph continuation computes this difference while reusing all 560 prior
nodes. This identifies a useful place to preserve exact signed information
when developing physical receiver coefficients and resolution.

NEGATIVE DRIFT CHECK — COMPLETION: CLEAR.
