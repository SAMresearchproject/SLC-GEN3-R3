# CR100 SW_PRIMITIVE_OPEN_QUESTION_ROADMAP

## Test Class

```text
OPEN_QUESTION_PROVENANCE_LOCK_AND_ROADMAP
```

## The Question (Locked Verbatim From Upstream)

```text
What is an SW dynamically, and what native propagation law turns SW
contact, echoes, pairs, and physical interaction into resolved 3D
ledger events?
```

This question is the SAM foundation question. SW is the atomic primitive
(1 SW = A0). A is accumulated SW displacement density. Particles are
stable echo / intersection patterns of SW. Physical interaction fires
resolution. Closing the dynamical law for SW closes the foundation;
leaving it open leaves a roadmap.

## Preflight

```text
This CR is qualitatively different from CR089..CR099.

CR089..CR096 reported how 09a's locked predictions compare to CERN
published values. CR098..CR099 sealed forward-blind predictions and
falsifier hunts. CR100 does something different: it locks the OPEN
QUESTION ITSELF, with its full provenance, into the cryptographic
record.

Why: the user named this as a roadmap question. A roadmap question
deserves the same provenance discipline as any positive or negative
prediction. Sealing the question with sha256 + utc puts it on the
public record - so progress against it (closing one of its open gates)
can be tested against the sealed formulation, and so the question
cannot be quietly rewritten to fit later answers.

This CR does not answer the question. It records it, hashes it,
inventories what is already partially answered (the QGA013..QGA024
chain of structural equation candidates and downstream audits), and
names the three remaining open gates per the upstream brief.
```

## What CR100 Locks

```text
1. The verbatim question text from
   C:/VS/Stam_model-A-v1.0/discovery_briefs/QG_ASSEMBLY/SW_CONTACT_ECHO_DYNAMICS_QGA013.md

2. The primitive commitments:
   - 1 SW = A0
   - SW is the smallest thing that exists
   - horizon support is 2D
   - writes produce the 3D world
   - particles are stable echo/intersection patterns
   - physical interaction fires resolution
   - unresolved A has undetermined path
   - A=1 makes measurable traversal distance diverge in the parent chart
   - A=1 parent boundary maps to an A0-like 2D seed condition in the boundary lane
   - universe and black holes are closed spheres

3. The candidate equation (violin-string form):
   L_SW[u_H] = J_phys + J_recoil
   with:
     L_SW[u_H] = d^2_t u_H - c_SW^2 Delta_H u_H + K(A_H) u_H + R_res[u_H]
   reading:
     propagation + tension response + resolution loss = source + paired recoil

4. The downstream partial-answer chain (QGA014..QGA024):
   QGA014 = PASS_OPERATOR_FORM_CANDIDATE
   QGA015 = PASS_PAIR_CLOSED_STANDING_ECHO_SELECTOR
   QGA016 = PASS_UNRESOLVED_ECHO_PROBABILITY_MEASURE
   QGA017 = PASS_CLOSED_SPHERE_CORRELATION_CANDIDATE
   QGA018 = PASS_GAMMA_RES_OPERATOR_BRIDGE
   QGA019 = PASS_I_PHYS_CONTACT_OVERLAP_FUNCTIONAL
   QGA020 = PASS_R_RES_PROJECTION_WRITE_REMOVAL
   QGA021 = PASS_THRESHOLD_HALF_SLOT_ORIGIN
   QGA022 = PASS_PRIMITIVE_CLOSED_BOUNDARY_OVERLAP_KERNEL
   QGA023 = PASS_SW_DYNAMIC_GENERATOR_PACKAGE
   QGA024 = PASS_PHASE_STRESS_SKELETON_ETA_EXTERNAL

5. The three remaining open gates (from QGA013 Open Gates section):
   GATE_1  choose exact N_SW[u_H] functional
   GATE_2  define c_SW relation to c or converter triad
   GATE_3  derive K(A_H) from substrate tension

6. Why this matters for the rest of SAM:
   - QGA034 selected A0^2 SW action-cell backbone for hbar normalization;
     this depends on the SW primitive being well-defined dynamically.
   - 09a's 35-row particle closure surface treats particles as
     pair-closed standing echoes; if the standing-echo equation is
     incomplete, the structural reading of the closure surface
     inherits the same incompleteness.
   - 11_QM_AND_GRAVITY branch CR080 cites "SW action-cell bridge" as
     the meeting of A=1 saturation and QM phase route - this bridge
     depends on closing GATE_1 / GATE_2.
   - CR098's SAM-X candidates use the partition algebra
     {alpha_H^i * D^j : product <= R} to predict masses; the partition
     algebra inherits the SW primitive as its underlying carrier.
   - CR099's negative prediction (no particle at (7,5)) rests on the
     same partition algebra and therefore on the same SW primitive.

If GATE_1, GATE_2, GATE_3 all close, SAM's foundation is closed and
the downstream claims gain a derived rather than asserted basis. If
any one fails to close in a way consistent with the candidate equation,
the equation needs revision. Either way it is a roadmap.
```

## Question Why It Could Be A Roadmap

```text
A closed answer would cascade:
  GATE_1 closure -> derives the action-count law that QGA034 selected
  GATE_2 closure -> connects substrate propagation speed to c, anchoring
                    the SW <-> photon bridge
  GATE_3 closure -> derives the K(A_H) tension term, closing the
                    standing-echo stability rule in QGA015

A clean closure of all three would:
  - turn 09a's particle ledger from structurally-reproduced to
    dimensionally-derived
  - turn the QGA034 hbar normalization from selected to derived
  - turn the closed-sphere correlation kernel (QGA017) from candidate
    to primitive-derived
  - close the action-phase identity bridge (CR073 in 11_QM_AND_GRAVITY)
    at theorem rather than structural grade

A failure to close any one gate would tell us specifically which
substrate primitive needs reconsideration. That is the roadmap value
even of a NULL closure.
```

## CERN Angle (Where Experimental Data Bears On SW)

```text
Direct probes are limited - SW is sub-A0, below any LHC scale. But
several CERN observable classes bear on SW indirectly:

  GATE_2 (c_SW vs c)
    - photon dispersion / Lorentz invariance tests
    - heavy-ion collision QGP propagation speed measurements
    - LHCb forward-physics speed-of-light tests
    - if c_SW != c at observable precision, GATE_2 closure constrained

  GATE_1 (N_SW[u_H] functional)
    - particle multiplicity vs collision energy at LHC (ATLAS/CMS/ALICE)
      - if echo-intensity functional, multiplicity follows specific scaling
    - heavy-ion collision N_charged scaling
    - any deviation from the predicted scaling constrains N_SW

  GATE_3 (K(A_H) substrate tension)
    - hadron mass-vs-binding-energy relations (already touched in 09a)
    - nuclear binding (LHC fixed-target / NA61 / LHCb heavy-ion)
    - any structural deviation from the standing-echo stability rule
      constrains K(A_H)

These connections are indirect and structural. CR100 does NOT predict
CERN observables here - it records the gaps and notes which CERN
data classes could in principle bear on each gate.
```

## Pass Conditions (Sealing Completion)

CR100 is complete when:

- `CR100_question_lock.json` exists with the verbatim question, the
  primitive commitments, the candidate equation, the QGA014..QGA024
  closure chain, and the three open gates - and is sealed with sha256.
- `CR100_question_lock.json.sha256.txt` sibling exists.
- The upstream source file SW_CONTACT_ECHO_DYNAMICS_QGA013.md has its
  sha256 recorded in the lock.
- `CR100_predictions.csv` carries the open-gate enumeration as the
  prediction-side commitment (predicting that closing each gate would
  cascade in the named direction).
- `CR100_prediction_commit.json` records the prediction sha256 + utc.
- `CR100_summary.json` and `CR100_result.md` are written and cite
  BLINDNESS_PROTOCOL.md.

## What CR100 Does Not Do

```text
- does not answer the question
- does not predict the form of N_SW[u_H], c_SW/c, or K(A_H)
- does not constrain how the gates will close
- does not gate the 09a verdict or the 13-branch comparisons
```

## Blindness Protocol Citation

```text
blindness_protocol_cite = 13_CERN_INDEPENDENT_TESTS/BLINDNESS_PROTOCOL.md
blindness_protocol_sha256 = recorded at runner time
```

## Rule-9 Line

```text
This CR could have failed if the question were paraphrased instead
of locked verbatim, if any of the primitive commitments were
introduced that do not appear in the upstream brief, if the candidate
equation were modified, or if the open-gate enumeration were padded.

The seal locks the question. Any future closure proposal must be
checked against the sealed formulation. The question cannot be
quietly rewritten to fit a later answer.
```

## Status

```text
PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF
The runner writes the question lock and its sha256 sibling at execution
time. Curator sign-off of the broader 13-branch seal sibling remains
pending.
```
