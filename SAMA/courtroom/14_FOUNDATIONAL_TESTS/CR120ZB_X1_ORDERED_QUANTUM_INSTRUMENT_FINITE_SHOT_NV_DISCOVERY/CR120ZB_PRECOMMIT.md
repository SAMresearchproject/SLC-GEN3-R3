# CR120ZB Precommit — Ordered X1 Instrument, Finite-Shot NV Discovery

## Why this run

CR120Z established exact quantum capability. CR120ZB asks the next, harder question: does the forward-order advantage remain visible after finite shots, PSD tomography, readout confusion, SPAM, pulse error, dephasing, relaxation, drift, and matched-duration controls?

No live quantum backend is installed. This campaign therefore uses the three already frozen CR223c high-fidelity NV profiles. Its highest possible result is simulator contact suitable for a later hardware handoff.

## Frozen implementation

The B and X1 analogs remain `H_A` and `CNOT_A->B`; they are functional representatives, not physical definitions. Every direct condition has two stages and receives the same profile-specific noise opportunities. B-only and X1-only are padded with idle stages. The reverse circuit is duration matched. Local-unitary, dephased-request, identity-idle, and classical-return controls are included.

Each block reconstructs a two-qubit density matrix from all 15 nontrivial Pauli expectations using 4,096 shots per observable, frozen readout inversion, linear inversion, and PSD projection. Twenty-four calibration blocks precede 48 untouched validation blocks per profile. Only validation blocks decide the primary verdict.

## Frozen noise translation

CR223c profile values are consumed without fitting. The two-qubit channel translation is fully specified in the contract: profile SPAM, pulse error, `gamma_1*T2`, `gamma_phi*T2`, phase noise, drift, and readout confusion each receive one predeclared channel role. The normalized stage time is `tau/T2=0.01`.

## Frozen success criteria

For each of room-temperature, cryogenic, and noisy NV profiles:

- forward median negativity must exceed 0.30;
- its 5th percentile must exceed every control's 95th percentile by at least 0.15;
- forward-minus-reverse negativity must be positive in at least 47/48 matched blocks;
- forward median CHSH must exceed 2.30 and at least 45/48 blocks must exceed 2;
- every direct-control 95th-percentile negativity must remain below 0.05.

The swapping arm must retain resolved remote nonseparability while product and unresolved heralds remain separable. Exact noisy-channel local marginals must remain setting invariant.

No threshold can be changed after execution. No profile, block, condition, shot, or failed reconstruction may be excluded.

## Result meaning

A pass means the order-specific quantum target is not a fragile exact-matrix artifact: it survives a preregistered finite-shot, hardware-realistic simulation surface inherited from the repo's NV program. Real-device execution and the physical B/X1 weld remain the next tier.
