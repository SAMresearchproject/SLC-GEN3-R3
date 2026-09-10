# CR279 Precommit: Higgs Direct-Weld Promotion

record_id: CR279
record_name: HIGGS_DIRECT_WELD_PROMOTION
campaign: SAM_COURTROOM_THREE_RECORD_PROMOTION_CAMPAIGN_5_5_XHIGH
destination: 13_CERN_INDEPENDENT_TESTS/CR279_HIGGS_DIRECT_WELD_PROMOTION
precommit_written_before_runner: true

## Objective

Promote the completed G748c Higgs direct weld into a canonical Courtroom
record. This is a promotion and exact replay record, not a new formula search.

## Permitted Source Set

| source | role | sha256 |
| --- | --- | --- |
| G439_output.json | Higgs q-slot role | 3e499706868b10d4cc4a2b7ecb7c50a494871fec94ae9efb5aed70a6e6cd72cc |
| G439_HEAVY_ELECTROWEAK_TOP_SLOT_SELECTOR.py | q-slot source | 279d86de713447607e7f390857bdc3e373480b75b250ccd9287e4771c0e960b5 |
| G444_output.json | weak-triplet q derivation | 96ca5b74cdbb249e8e6128531e202e485932a70621250df3df9c69b584a7fb90 |
| G444_WRITE_SECTOR_Q_SLOT_DERIVATION.py | q alphabet source | aa702ff6a2bd4e236ccec30d12050a450f9ba69fbbedef8d32f81d9e442b7863 |
| G744c_output.json | source-strength bridge | 5d3ad959d780012190493e661658dc8280c981237c4b9c8adbb128900fde2c1d |
| G744c_Q_A_SOURCE_STRENGTH_BRIDGE.py | q_A bridge source | 055829fc7ed42296bed4adff456890fbce7f9b9a3db0b34f385a07d8ec5fcaed |
| G745c_output.json | Higgs scalar route | 6957514aa88104d22fb870004b51361a1fe201fb4617beb224c01209c352ca21 |
| G745c_HIGGS_NINE_SIXTEENTHS_SCALAR_ROUTE.py | scalar route source | e1b8559dfb06aa19f8dfa614f7d0ab205d61a4f314e8ed02106985caa12208da |
| G748c_PRECOMMIT.md | direct-weld precommit | d31e6dc0c3e5cf889947d3753af5d390e1f6b0e54f6b000753a6e214f5a4f195 |
| G748c_runner.py | direct-weld runner | 3520898c9abd2b5679b805378f5b07b4be86daa7878da2f49c413afa9afce3cf |
| G748c_summary.json | direct-weld summary | 244d7f04ba1ec74f5ea4041d7fe1a059764f0aec6e90f63b613842965fe63270 |
| G748c_result.md | direct-weld result | 22ed3cf38618dca38e6ada1437fba3ba24913d90cc480bb66827388a0057a64a |
| G748c_provenance.json | source contract ledger | 0d5ec5bb3bd5b22ad1370c3b0ad3eaa9978fae5b829f44e830c30cae8bde066d |
| CR120_summary.json | neighboring Higgs intake | 887f9ca58dde323f1c0a53cd1c05e3f3a6be6cf1315f3b32c9419799cb726179 |
| CR120_result.md | bounce bridge boundary contract | 5f01ecc521850597af164345d7e9d60fd6709e23bb44eb5a76823e010b170bde |

## Locked Source Contracts

```text
Resolved Higgs ontology -> q_H = 3
Higgs bounce ratio      -> r_bounce,H = 1/(64*pi)
General bridge          -> q_A = m * (1 + r_bounce)
Expected ratio          -> q_A,H / m_H = 1 + 1/(64*pi)
```

The Higgs mass input, if replayed, is the G745c scalar formula output:

```text
m_H_native_MeV = 125077.36096514532
source = G745c scalar formula output, not measured Higgs target
```

No measured Higgs residual, observed target value, new coefficient,
new normalization, or new Higgs-specific operator may enter the route.

## Required Typed Outputs

```text
ResolvedHiggsASourceOntology
HiggsQSlotRole[q=3]
HiggsBounceRatio[1/(64*pi)]
HiggsASourceReadout[q_A,H]
HiggsASourceRatio[q_A,H/m_H]
```

## Wrong Controls

The runner must preserve at least these controls:

1. Replace q_H = 3 with neighboring noncanonical q-slots.
2. Remove the bounce term.
3. Replace 1/(64*pi) with a sourced wrong-route control.
4. Apply a neighboring particle bridge through an unauthorized Higgs channel.
5. Attempt to construct q_A,H from an observed residual.

Every control must fail its relevant guard while the canonical route satisfies
the frozen source contracts.

## Verdict Tree

Return exactly one primary verdict:

```text
PASS_HIGGS_DIRECT_WELD_PROMOTION
BOUNDARY_SOURCE_CHAIN_INCOMPLETE
FAIL_HIGGS_DIRECT_WELD_REPLAY
INVALID_HIGGS_PROVENANCE
```

PASS requires:

- every required source exists and hashes to the precommitted value;
- G748c primary verdict is PASS_DIRECT_WELD;
- q_H = 3;
- r_bounce,H = 1/(64*pi);
- q_A,H/m_H = 1 + 1/(64*pi);
- measured_Higgs_mass_used is false;
- residual_used_to_choose_candidate is false;
- modified_prior_tests_or_CRs is false;
- all precommitted wrong-control guards pass.

If a required source is missing or hash-invalid, return
INVALID_HIGGS_PROVENANCE. If the source chain is present but incomplete,
return BOUNDARY_SOURCE_CHAIN_INCOMPLETE. If the replay arithmetic fails,
return FAIL_HIGGS_DIRECT_WELD_REPLAY.
