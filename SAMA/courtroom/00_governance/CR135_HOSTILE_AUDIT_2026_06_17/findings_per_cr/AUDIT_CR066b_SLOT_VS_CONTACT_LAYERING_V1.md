# AUDIT — CR066b Slot vs Contact Layering of the 1/α_H⁴ Letter Increment v1.0

**Auditor stance:** hostile.

## Tier verdict

**Tier 4 — DEMAND_RETEST**

CR066b extends CR066a with a second-layer attribution (contact-level (1/32, 1/32, 0) split). It explicitly REJECTS an alternative attribution (the mini-1:2:1 packet (1/64, 1/32, 1/64)) which is the strongest part of the CR — it's the first CR in the cluster to formally reject a same-sum alternative. But the "Higgs 1/8 bridge attribution" leans on dozenal arithmetic to claim a structural identity (1/16 = HALF of the released 1/8) which is not a derivation but an arithmetic observation.

## Per-criterion findings

### C1 — HASH_CHAIN_INTEGRITY: PASS

CR060a (d5d3...), CR061a (c011...), CR065a (38d7...), CR066a (5eb9...), CR121 (01e4...), CR129b (8c3d...) all resolve inside The_Courtroom.

### C2 — FALSIFIER_PRECOMMITTED: PASS

Three layer-specific falsifiers (slot, contact, amplitude). All three are concrete and one-violation. Strongest C2 in the cluster.

### C3 — WRONG_CONTROLS_LOAD_BEARING: WEAK PASS

WC2 ("mini-1:2:1 packet explicitly REJECTED") is a REAL load-bearing test — it identifies a same-sum alternative and shows why it fails. This is the closest thing to a true wrong control in the cluster. Credit.

WC1, WC3, WC4, WC5, WC6, WC7 are mostly clarifications. WC3 is a structural disclosure: "The (1/32, 1/32, 0) contact-level split assumes reflection symmetry a <-> c. Asymmetric routes might split the bridge surcharge differently." Acceptable disclosure.

### C4 — FREE_PARAMETERS_HONESTLY_ZERO: WEAK PASS

The (1/32, 1/32, 0) symmetric split is asserted from a <-> c reflection symmetry. WC3 admits asymmetric variants exist. The choice of symmetric split is therefore one of multiple options — not derived, but explicitly disclosed. Acceptable disclosure of a constrained DoF.

### C5 — IN_SAMPLE_DISCLOSED: WEAK PASS

The Higgs 1/8 bridge attribution is the C5 risk:

> "Per CR-066b: the Paul Revere letter capacity = **1/16 = HALF of that released 1/8**."
> "Structural reading: the bridge slot carries HALF of each row's Higgs-released 1/8 burden as letter content."

This identification (1/16 = 1/2 × 1/8) is arithmetic: 1/16 is half of 1/8 by definition. Calling this a "structural reading" is post-hoc storytelling on the arithmetic.

WC5 partially admits this: "The 1/16 = (1/alpha_H) * 2^-D identity is dozenal arithmetic linking the Paul Revere letter capacity to the Higgs-released gravitational fraction. It does NOT claim the physical Higgs boson IS the bridge slot, only that they share the same surface-debit-channel arithmetic."

Good admission. But the result.md headline still leans on the identification as if structural. Demand: tighten language to "the 1/16 letter capacity and the 1/8 Higgs-released fraction share the dozenal-arithmetic relation 1/16 = 1/2 × 1/8; no physical identification is claimed."

### C6 — VERDICT_GRADE_MATCHES_EVIDENCE: PASS

The verdict (LOCKED slot-level center-only + LOCKED contact-level bridge-split + REJECTED mini-packet) matches the predictions (P1–P9 all arithmetic checks). Acceptable.

### C7 — APPEAL_VS_FALSIFICATION_BRIGHT_LINE: PASS

The three layer-specific falsifiers (outer slot lift > 0, outer-cross debit > 0, amplitude ratio ≠ 2:3:2) are each one-violation. The bright line is drawn. Credit.

### C8 — TEXT_MATCHES_VERDICT: WEAK PASS

The text claims structural identification (1/16 = half of 1/8 = Higgs-released) which is arithmetic, but WC5 admits the arithmetic nature. Net: acceptable IF the headline language is tightened (see C5 demand).

### C9 — TIMESTAMP_ORDERING_FORMULA_THEN_DATA: N/A

Algebraic identification, no data fit.

## Specific demands

1. **REWORD HIGGS ATTRIBUTION:** the headline "the bridge slot carries HALF of each row's Higgs-released 1/8 burden as letter content" implies physical identification. WC5 admits it's dozenal arithmetic. Demand: align the headline with WC5's disclosure.
2. **DERIVE OR DISCLOSE THE SYMMETRIC SPLIT:** the (1/32, 1/32, 0) symmetric split assumes a <-> c reflection (per WC3). Demand: state explicitly that the symmetric split is a structural assumption, not a derivation, and identify the appeal CR scope if asymmetric variants emerge.
3. **ELEVATE WC2 AS THE MODEL WC:** CR066b's WC2 (explicit rejection of (1/64, 1/32, 1/64)) is the cluster's best wrong-control example. The siblings should adopt this pattern.

## Quoted evidence

> "WC2_mini_1_2_1_packet_explicitly_REJECTED -- The (1/64, 1/32, 1/64) representation is documented in the layering table as REJECTED with explicit reasoning."

This is a real load-bearing wrong control. The mini-packet sums to 1/16 (same total) but preserves the (1/4, 1/2, 1/4) base shape rather than lifting the bridge. Rejection on structural grounds is clean.

> "WC5_Higgs_attribution_is_arithmetic_NOT_physical_identity"

Honest disclosure. Now propagate that honesty into the headline.
