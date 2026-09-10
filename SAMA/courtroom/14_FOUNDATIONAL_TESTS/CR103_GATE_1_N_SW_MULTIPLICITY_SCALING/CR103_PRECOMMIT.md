# CR103 GATE_1_N_SW_MULTIPLICITY_SCALING

## Test Class

```text
MULTIPLICITY_SCALING_EXPONENT_TEST_FOR_GATE_1_SIMPLEST_READING
```

## Preflight

```text
CR100 sealed three open gates for the SW dynamical question. CR101 and
CR102 closed GATE_2 partially at CERN (1e-6) and astrophysical (1e-18)
precision respectively.

GATE_1 asks: choose exact N_SW[u_H] functional. CR100's sealed
enumeration listed four candidates:

  1. local echo intensity
  2. signed contact count
  3. closed-loop intersection count
  4. paired source/recoil count

These differ in WHAT they count, not in how counting maps to observable
particle multiplicity. To get a testable observable prediction at LHC
we need to combine an N_SW candidate with an N_SW -> multiplicity
mapping.

CR103 tests the SIMPLEST READING of candidate #4 (paired source/recoil
count): one source-recoil pair maps to one produced particle, and the
total N_SW count grows linearly with the collision's available energy
because each unit of energy supports one pair. Under this reading:

  predicted multiplicity scaling exponent alpha_SAM = 1.0
  where N_ch_predicted proportional to s^(alpha_SAM/2) = s^0.5 = sqrt(s)

(Equivalently, N proportional to E_collision in linear-energy reading.)

Measured charged-particle multiplicity in inelastic pp at LHC scales
as N_ch_meas proportional to s^alpha_meas with alpha_meas ~ 0.11
(well-established from ATLAS, CMS, ALICE at 0.9, 7, 8, 13 TeV).

If the SIMPLEST reading of candidate #4 matches data, the measured
alpha_meas would be ~1.0. It isn't. So CR103 commits to one specific
testable scaling and lets the data return a verdict.
```

## Question

Does the SIMPLEST reading of GATE_1 candidate #4 (paired source/recoil
count linear in collision energy) reproduce the measured LHC charged-
particle multiplicity scaling exponent?

If not, this specific reading is DISFAVORED at LHC precision, and the
GATE_1 closure space narrows: SAM needs either a non-trivial N_SW ->
multiplicity mapping, OR one of the other three candidates with a
specific scaling derivation, OR an upstream reformulation.

## SAM Commitment (Locked Before Anchor Open)

```text
GATE_1 candidate tested: #4 paired source/recoil count
N_SW -> multiplicity reading: simplest (one source-recoil pair = one
                              produced particle; total pairs linear
                              in available collision energy)
Predicted multiplicity scaling: N_ch proportional to sqrt(s)
                                 alpha (where N_ch proportional to s^alpha) = 0.5
                                 (equivalently, N_ch proportional to E_collision^1.0)
Free parameters introduced: 1 (overall normalization fit at lowest
                            anchor; CR103 verdict depends only on the
                            scaling exponent, which is parameter-free)
Upstream CR100 question lock sha256:
  fb310a23497308e9b0b92c23974cb08a230c7a8779c36aabd94feb628e145867
```

Note: The SAM substrate algebra (09a/QP075) has zero free parameters
in the closure surface. Here, CR103 introduces ONE normalization
parameter to anchor the scaling law at one data point. The scaling
exponent itself, however, is the SAM structural prediction and is
NOT fit. The Pillar 1 (structural blindness) zero-free-parameter
claim applies to the exponent; the normalization is an anchor offset.

## Anchor Envelope Composition

```text
LIVE ANCHORS (LHC inelastic pp <dN_ch/d_eta> at eta=0, NSD or INEL,
peer-reviewed):

  A1  ATLAS pp <dN_ch/d_eta>|_eta=0 at sqrt(s) = 0.9 TeV
  A2  ATLAS pp <dN_ch/d_eta>|_eta=0 at sqrt(s) = 7 TeV
  A3  ATLAS pp <dN_ch/d_eta>|_eta=0 at sqrt(s) = 13 TeV
  A4  CMS pp <dN_ch/d_eta>|_eta=0 at sqrt(s) = 7 TeV
  A5  CMS pp <dN_ch/d_eta>|_eta=0 at sqrt(s) = 13 TeV
  A6  ALICE pp <dN_ch/d_eta>|_eta=0 at sqrt(s) = 7 TeV
  A7  ALICE pp <dN_ch/d_eta>|_eta=0 at sqrt(s) = 13 TeV

HONEST NEGATIVES:

  HN1  Withdrawn / superseded multiplicity result (CLASS_A)
  HN2  Unpublished preprint multiplicity claim (CLASS_X_UNPUBLISHED)
  HN3  Synthetic perturbation: ATLAS 13 TeV value shifted by 5x
       quoted uncertainty (CLASS_G)
```

## Test Method

```text
Step 1  Lock SAM commitment: N_ch_pred(s) = K * s^(alpha_SAM / 2)
                              with alpha_SAM = 1.0 (linear in energy)
Step 2  Hash prediction file BEFORE opening envelope.
Step 3  Open envelope; verify sha256.
Step 4  Compute pairwise scaling exponents from live anchors:
        alpha_obs = 2 * ln(N_ch(s1) / N_ch(s2)) / ln(s1/s2)
        for cross-source pairs from ATLAS/CMS/ALICE.
Step 5  Fit single anchor (lowest sqrt(s)) to set K.
Step 6  Predict N_ch at higher sqrt(s) using SAM linear scaling.
Step 7  Compute residual percent at each higher anchor.
Step 8  Compare alpha_SAM = 1.0 to median alpha_obs across cross-source
        pairs. Compute distance in sigma using quoted statistical
        uncertainties.
Step 9  Emit evidence rows, summary, result.
```

## Pass Conditions (Reporting Completion)

CR103 is complete when:

- prediction is hashed and committed BEFORE envelope opens
- envelope sha256 matches sibling
- temporal ordering is correct
- evidence rows include alpha_SAM, alpha_obs (per pair), residual
  percent at predicted multiplicity, and row labels
- summary records the verdict against candidate #4 simple reading
- result.md reports the per-anchor comparison and the verdict

## Possible Outcomes

```text
CANDIDATE_4_SIMPLE_READING_CONFIRMED
    alpha_obs / alpha_SAM within 2 sigma at all cross-source pairs;
    all predicted multiplicities within 2 sigma of measured.
    (Unlikely - measured alpha is ~0.11, SAM simple reading is 1.0.)

CANDIDATE_4_SIMPLE_READING_DISFAVORED_BY_LHC
    alpha_obs / alpha_SAM differs by more than 3 sigma;
    GATE_1 candidate #4 simple reading does not reproduce LHC scaling;
    SAM needs a non-trivial N_SW -> multiplicity mapping OR another
    candidate OR upstream reformulation.

VERDICT_INCONCLUSIVE
    if cross-source measurements disagree more than they constrain
    alpha_SAM; or if the synthetic CLASS_G perturbation slips past
    Gate R (indicating insufficient residual gate teeth at this CR's
    declared band).
```

## Wrong Controls (Discipline Checks)

- HN1 (withdrawn) must fail at Gate A admissibility.
- HN2 (unpublished) must fail at Gate A admissibility.
- HN3 (synthetic CLASS_G) must pass admissibility (real ATLAS framing)
  but fail at Gate R residual.
- Temporal ordering violation -> DIAGNOSTIC.
- Any change to alpha_SAM = 1.0 commitment after envelope opens is
  a protocol violation.

## Blindness Protocol Citation

```text
blindness_protocol_cite = 13_CERN_INDEPENDENT_TESTS/BLINDNESS_PROTOCOL.md
blindness_protocol_sha256 = recorded at runner time
```

## Rule-9 Line

```text
This CR could disfavor SAM's GATE_1 candidate #4 SIMPLEST reading.
It does NOT disfavor candidate #4 in full generality - a more
sophisticated N_SW -> multiplicity mapping could rescue it.
It does NOT disfavor the other three candidates - they remain in
CR100's sealed enumeration and remain testable at future CRs.

What CR103 tests is whether the most direct, naive reading of
"N_SW = paired source/recoil count" maps to observed LHC pp
multiplicity scaling. The answer the data will return determines
whether SAM needs more sophistication on this lane, or whether the
simplest reading happens to work.

If we build from the ground up, even a disfavoring result is a step:
it tells SAM exactly which simple reading is closed off, narrowing
the closure space for GATE_1.
```

## Status

```text
PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF
```
