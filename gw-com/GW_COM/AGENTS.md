# GW-COM working instructions

Apply the repository root instructions and the owner's five-layer architecture
in README.md. These rules also govern successor campaign code built for this
program, even when its frozen outputs are stored under SAM_REVIEW/campaigns.

- Keep carrier physics, intentional modulation, residual extraction,
  information testing and candidate decoding as distinct interfaces.
- Preserve raw waveform → source fit → residual history → candidate
  symbolization → decoded hypothesis, with artifact hashes and exact parent
  identities. Preserve alternatives and unsuccessful attempts.
- Preserve signed samples and their time order. Envelopes, spectra, rankings,
  entropy and compression summaries are derived views, never replacements.
- Run candidate decoding only after the declared physical and statistical
  controls pass for that exact source-fit/residual/symbolization lineage.
  NOT_RUN, INCOMPLETE and FAIL do not authorize candidate decoding.
- Retain the criteria and all individual control results. Do not replace them
  with a composite anomaly score or silently invent numerical thresholds.
- Keep transmitter truth and known messages out of source fitting, candidate
  symbol selection, information-test selection and decoding unless explicitly
  designated as training/calibration inputs in the experiment contract.
- Label controlled encoder/decoder demonstrations separately. The preserved
  GW_COM_INTERVAL1 decoder is not the new candidate-admission implementation.
- Future numerical work uses the current STARBREAKER DomainSession and real
  source-bound calculations. Architecture work needs no artificial runtime call.
