---
entry_id: H001497
entry_date: 2026-09-17
entry_type: RESEARCH / RESULT / APPLICATION
status: IMMUTABLE_HISTORY
supersedes: NONE
prior_entry: H001496
affects_live:
  - SAM_LIVE/03_STARBREAKER_GW_CURRENT.md
---

# Exactly three GW-COM follow-up experiments

Sean Brady authorizes exactly three tests: continuous-source noise/SNR sweep, physical scaling/detectability, and expanded natural-carrier false positives. The [fixed contract](../../SAM_REVIEW/campaigns/GW_COM_THREE_TESTS1/CONTRACT.json) precedes execution and prohibits adaptive grid additions or receiver tuning. The [completed report](../../SAM_REVIEW/campaigns/GW_COM_THREE_TESTS1/REPORT.md) contains every declared outcome; no fourth experiment is started.

1. Continuous analytic-source Gaussian noise uses σ=0.01,0.05,0.20 and two fixed seeds, each paired with an unmodulated control. Both seeds recover all seven primes at the first two levels; neither recovers at0.20. All six matched controls have zero repeated packets. Noise-aware quiet holdout tolerance6σ+1e-10 is predeclared; packet and permutation criteria remain unchanged. High-noise carrier fits remain adequate, but hundreds of candidate markers yield no repeated frame. Results are finite paired realizations, not population rates.
2. Two equal-mass scales assign m,r and Kepler-consistent omega, restore dimensional quadrupole strain, and report distances1pc/1kpc/1Mpc. At1Mpc the1.4-solar-mass-per-body,200km-radius example has carrier strain1.385e-21 and ideal known-modulation SNR52.554 against published Advanced LIGO design ASD. Formal rho8 distance is6.569Mpc, not a measured decoder horizon. Positive mechanical work is1.594e44J per marker; baseline circular radiation over the packet is2.14% of binding energy. The1e20kg/25m example is far below sensitivity at1pc; its formal rho8 extrapolation falls inside one wavelength and is outside the far-zone model. Radiation-reaction compensation and realizable actuation are not implemented by this scaling calculation.
3. A10% slow chirp and a changing-inclination/polarization nuisance produce zero repeated packets and no decoding. Stationary carrier fits are inadequate, so the result is absence of a packet in retained residuals, not carrier absorption. The latter nuisance is a precession-like projection, not integrated spin dynamics.

**The test result suggests the concept is possible.**

Current STARBREAKER / SB-GEN3-ACCUMULATION-R1 / SLC-GEN3-R4 / SLC-GEN3-CEV1-R4 execution uses466 native calls and4,506,394 graph nodes. Native arithmetic covers source/noise combinations, fits, signed residuals, exact statistical ranks, physical scaling and spectral weighted sums. Python supplies declared Gaussian/trigonometric constants, Fourier/interpolation inputs and discrete searches. No engine revision is changed.

Saved-output verification passes168 evidence records,138,012 raw channel samples,276,024 exact prediction/residual channel samples,84 normal equations,14 permutation results, two SI scalings and six distance rows. It creates no new scientific cases. Original continuous results and numerical refinement remain frozen; code/contracts and downloaded design-curve provenance are retained in the successor.

Current live statement: exactly three follow-ups complete;4/6 noisy injections decode, matched controls and two natural nuisances yield no repeated packet, and SI detectability/work are quantified. Stop after these three experiments.

Originator / conceptual director: Sean Brady. AI research collaborators: OpenAI ChatGPT and Codex.
