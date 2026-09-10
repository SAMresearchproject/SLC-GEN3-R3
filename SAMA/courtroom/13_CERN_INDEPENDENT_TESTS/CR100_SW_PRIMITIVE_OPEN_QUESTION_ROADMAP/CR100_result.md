# CR100 SW Primitive Open Question - Sealed Roadmap

## Verdict

```text
CR100_SW_OPEN_QUESTION_PROVENANCE_LOCKED (PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF)
```

## The Question (Locked Verbatim)

> What is an SW dynamically, and what native propagation law turns SW contact, echoes, pairs, and physical interaction into resolved 3D ledger events?

**Question text sha256:** `29f4f30cd2e3423ca3d27d70b97269ed5a4629ea7822bdaa867253216e7b6b0b`

**Source:** [SW_CONTACT_ECHO_DYNAMICS_QGA013.md](file:///C:/VS/Stam_model-A-v1.0/discovery_briefs/QG_ASSEMBLY/SW_CONTACT_ECHO_DYNAMICS_QGA013.md)

**Source sha256 at runner time:** `8e9f9143e8390fdead5b9d690ffd42b3a5dd92a51c152c17419fcc47ee05d918`

## Cryptographic Lock

```text
prediction_commit_sha256 = 6ebf43e729e718032f5ab14bb44fba21bfc8c7e63e4845170135e534d10dfd5c
prediction_commit_utc    = 2026-06-13T21:55:11Z
question_lock_sha256     = fb310a23497308e9b0b92c23974cb08a230c7a8779c36aabd94feb628e145867
lock_sibling             = CR100_question_lock.json.sha256.txt
blindness_protocol_sha256= 6b0b0c189ddd6dff008f0e2a457341fc134b14d4c36c04da1daae15eface3a4e
```

## Why This Is A Roadmap

SW is SAM's atomic primitive (1 SW = A0; the smallest thing that
exists). A is accumulated SW displacement density. Particles are
pair-closed standing echoes of SW. Closing the dynamical law for SW
closes the foundation; leaving it open leaves a roadmap.

This CR locks the question itself - verbatim, with its provenance
and upstream source sha256 - so that any future closure proposal can
be checked against the sealed formulation. The question cannot be
quietly rewritten to fit a later answer.

## Primitive Commitments (Sealed)

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

## Candidate Equation (Violin-String Form)

```text
L_SW[u_H] = J_phys + J_recoil

L_SW[u_H] = d^2_t u_H - c_SW^2 * Delta_H u_H + K(A_H) u_H + R_res[u_H]

reading: propagation + tension response + resolution loss = source + paired recoil
```

## Downstream Partial-Answer Chain (QGA014 .. QGA024)

| Stage | Verdict | Contribution |
|---|---|---|
| **QGA014** | PASS_OPERATOR_FORM_CANDIDATE | operator form on closed 2D support; discrete standing modes; omega_l^2 = c_SW^2*l(l+1) + K0 |
| **QGA015** | PASS_PAIR_CLOSED_STANDING_ECHO_SELECTOR | stability selector PAIR_CLOSED_STANDING_ECHO; Delta A_source + Delta A_recoil = 0 |
| **QGA016** | PASS_UNRESOLVED_ECHO_PROBABILITY_MEASURE | P(i|unresolved) = |E_i|^2 / sum|E_j|^2 (Born-style bridge) |
| **QGA017** | PASS_CLOSED_SPHERE_CORRELATION_CANDIDATE | E(a,b) = -cos(a-b) closed-sphere correlation kernel |
| **QGA018** | PASS_GAMMA_RES_OPERATOR_BRIDGE | P_i = |E_i|^2 / sum |E|^2 -> I_phys threshold -> X_c ownership -> W_SAM |
| **QGA019** | PASS_I_PHYS_CONTACT_OVERLAP_FUNCTIONAL | I_phys[E,C] = |<C,E>|^2 / (<E,E><C,C>) coherent echo-contact overlap |
| **QGA020** | PASS_R_RES_PROJECTION_WRITE_REMOVAL | R_res[E,C,W] = -Pi_C(E) on completed write; Pi_C(E) = C*<C,E>/<C,C> |
| **QGA021** | PASS_THRESHOLD_HALF_SLOT_ORIGIN | D_route = 6 half-slots = 3; I_threshold = 1/2 |
| **QGA022** | PASS_PRIMITIVE_CLOSED_BOUNDARY_OVERLAP_KERNEL | K_AB(a,b) = -cos(a-b) from antipaired boundary contact modes |
| **QGA023** | PASS_SW_DYNAMIC_GENERATOR_PACKAGE | G = [[0,-1],[1,0]]; u'' + u = 0; recovers mode equation, antipaired recoil, K_AB, I_phys, threshold, R_res in one fixture |
| **QGA024** | PASS_PHASE_STRESS_SKELETON_ETA_EXTERNAL | compact dimensionless phase cycle; finite positive stress skeleton; K0 = 1; A_H = A0 * N_SW; eta/hbar magnitude remains external |

## Three Open Gates (Sealed)

### GATE_1 - N_SW[u_H] functional

**Verbatim from upstream:** `choose exact N_SW[u_H] functional`

**Current candidates at seal time:**

- local echo intensity
- signed contact count
- closed-loop intersection count
- paired source/recoil count

**What closing it unlocks:**

> derives the action-count law that QGA034 selected (A0^2 SW action-cell backbone); turns the hbar normalization from selected to derived

**CERN data classes that bear on it:**

- particle multiplicity vs collision energy at LHC (ATLAS/CMS/ALICE)
- heavy-ion collision N_charged scaling
- any deviation from echo-intensity-derived multiplicity scaling constrains N_SW

### GATE_2 - c_SW relation to c

**Verbatim from upstream:** `define c_SW relation to c or converter triad`

**Current candidates at seal time:**

- c_SW = c (identity)
- c_SW = c * dimensionless_substrate_factor
- c_SW related to c via converter triad in A0 / R / D

**What closing it unlocks:**

> anchors the SW <-> photon bridge; closes 09a's particle ledger as standing-echo modes with propagation speed c; closes the action-phase identity bridge (CR073 in 11_QM_AND_GRAVITY) at theorem rather than structural grade

**CERN data classes that bear on it:**

- photon dispersion / Lorentz invariance tests
- heavy-ion collision QGP propagation speed measurements
- LHCb forward-physics speed-of-light tests
- if c_SW != c at observable precision, GATE_2 closure constrained

### GATE_3 - K(A_H) substrate tension

**Verbatim from upstream:** `derive K(A_H) from substrate tension`

**Current candidates at seal time:**

- K(A_H) = K_0 + linear in A_H
- K(A_H) = saturating at A=1 boundary condition
- K(A_H) derived from closed-sphere boundary tension

**What closing it unlocks:**

> closes the standing-echo stability rule in QGA015; turns the closed-sphere correlation kernel (QGA017) from candidate to primitive-derived; closes the K0 = 1 skeleton in QGA024 at first-principles grade

**CERN data classes that bear on it:**

- hadron mass-vs-binding-energy relations (touched in 09a)
- nuclear binding (LHC fixed-target / NA61 / LHCb heavy-ion)
- any structural deviation from the standing-echo stability rule constrains K(A_H)

## Downstream Dependencies On Closure

If GATE_1, GATE_2, GATE_3 all close, the following downstream
claims become derived rather than asserted:

- QGA034 selected the A0^2 SW action-cell backbone for hbar normalization; this depends on the SW primitive being well-defined dynamically
- 09a's 35-row particle closure surface treats particles as pair-closed standing echoes; if the standing-echo equation is incomplete, the structural reading of the closure surface inherits the same incompleteness
- 11_QM_AND_GRAVITY branch CR080 cites 'SW action-cell bridge' as the meeting of A=1 saturation and QM phase route - this bridge depends on closing GATE_1 / GATE_2
- CR098's SAM-X candidates use the partition algebra {alpha_H^i * D^j : product <= R} to predict masses; the partition algebra inherits the SW primitive as its underlying carrier
- CR099's negative prediction (no particle at (7,5)) rests on the same partition algebra and therefore on the same SW primitive

## What CR100 Does Not Do

- does not answer the question
- does not predict the form of N_SW[u_H], c_SW/c, or K(A_H)
- does not constrain how the gates will close
- does not gate the 09a verdict or the 13-branch comparisons
- does not modify any prior CR result file

## How Progress On Each Gate Is Tracked

```text
When upstream QGA work closes one of the three gates with a
specific functional form (e.g., N_SW = echo intensity per the
local-echo-intensity candidate; or c_SW = c via identity
derivation), an appeal row is appended:

    CR100a_<DATE>_<GATE>_<RESULT_CLASS>

e.g.:
    CR100a_2027_03_15_GATE_1_N_SW_CLOSED_AS_ECHO_INTENSITY
    CR100a_2027_07_22_GATE_2_C_SW_EQUALS_C_DERIVED
    CR100a_2028_01_10_GATE_3_K_A_H_DERIVED_FROM_BOUNDARY_TENSION

Each appeal row carries its own sha256 + utc. The original
question lock and the open-gate enumeration are NEVER modified.
```

## Rule-9 Line

```text
This CR could have failed if the question were paraphrased
instead of locked verbatim, if any primitive commitment were
introduced that does not appear in the upstream brief, if the
candidate equation were modified, or if the open-gate enumeration
were padded.

The seal locks the question. Any future closure proposal must be
checked against the sealed formulation. The question cannot be
quietly rewritten to fit a later answer.
```
