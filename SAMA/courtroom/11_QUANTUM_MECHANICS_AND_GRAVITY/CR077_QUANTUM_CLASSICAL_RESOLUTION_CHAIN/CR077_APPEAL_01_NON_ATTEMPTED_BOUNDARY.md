# CR077 Appeal 01 - Non-Attempted Boundary Language

```text
appeal_id:       CR077_APPEAL_01
parent_result:   CR077_result.md
appeal_type:     INTERPRETATION_APPEAL
disposition:     ACCEPTED_APPEND_ONLY
date_local:      2026-07-10
appellant:       Sean Brady
```

## Appeal Request

The appellant requests that the boundary language attached to CR077 be
removed as a qualifier on the result because the listed non-claims were not
the subject of the CR077 question.

CR077 asked whether the following chain is preserved:

```text
QGA016 unresolved echo measure
    -> QGA018 Gamma_res threshold and X_c ownership
    -> QGA019 I_phys contact-overlap functional
    -> G678 interaction-caused ledger resolution
```

The answer is yes. The chain passed `27/27` checks and rejected `5/5` wrong
controls.

## Reasoning

The original CR077 result already contains the complete answer to its tested
question. The checks establish that:

```text
route probabilities remain 1/7, 4/7, 2/7
the selected route remains r1
I_phys(r1) = 4/7 crosses Gamma_res = 1/2
physical interaction causes the ledger resolution
human observation is a delayed readout
```

The subsequent list concerning Hilbert space, eta/hbar, Planck-cell origin,
Bell closure, and full quantum gravity was not tested by CR077 and was not
needed to answer its question. Those items therefore cannot qualify, weaken,
or convert the CR077 PASS into a boundary reading.

This appeal does not challenge the original numbers, checks, wrong controls,
source hashes, or upstream result files. It challenges only the attachment of
non-attempted work as a boundary on a result that passed the question it
actually asked.

## Appeal Rule For Future Courtroom Work

An unattempted claim is not a negative result. Future result summaries should
include a limitation only when it is one of the following:

```text
1. the test attempted the claim and the claim failed or remained unresolved;
2. the exact test question required the limitation as a declared scope rule;
3. the limitation is necessary to prevent a direct misreading of the result.
```

Generic lists of things a test did not attempt should not be used as a
qualifier or counterweight when the tested question passed cleanly. Claims
that were actually attempted remain fully open to challenge, including
numerical, structural, provenance, and wrong-control failures.

## Record Handling

This appeal is append-only. The original `CR077_PRECOMMIT.md`,
`CR077_result.md`, `CR077_summary.json`, and `HASHES.txt` remain unchanged as
the historical execution record. The second result below records the current
appeal disposition.
