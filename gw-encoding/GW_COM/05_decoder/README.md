# 5. Decoder

Candidate decoding begins only when both the declared physical controls and
statistical controls have passed for the exact candidate lineage.

Input: a candidate symbolization and its alternatives, residual/source-fit/raw
parents, decoding grammar, and complete control-admission record. The decoder
must check that the control records address those same artifact versions.
Absent, stale, incomplete or failed records do not admit a candidate.

Output: decoded hypothesis or hypotheses, unresolved symbols, framing and
timing choices, error-correction steps, rejected alternatives and a complete
mapping from each output symbol back to its residual sample support and raw
waveform. Decoding failure remains a retained outcome. A successful parse does
not overwrite physical/statistical evidence or establish intent by itself.

Expected transmitter payload is used only for an explicitly labeled synthetic
evaluation after the decoder produces its output. Preserve corrections alongside
the original symbols; never replace the observed sequence with a repaired one.

The decoder-admission statuses and lineage fields are specified in
[the evidence contract](../EVIDENCE_CONTRACT.md). The
[runtime gate and decoder](../runtime/decoder.py) implement these checks for
the C4 pipeline, including individual control evidence and complete stage
status. [Nine tests](../tests/test_decoder_gate.py) exercise admission,
missing/failed evidence, changed bytes and lineage mismatches.

The earlier [receiver](../../SAM_REVIEW/campaigns/GW_COM_INTERVAL1/receiver.py)
remains a known-protocol demo component. It may be reused in an explicitly
labeled demonstration; it is not a shortcut around candidate admission.
