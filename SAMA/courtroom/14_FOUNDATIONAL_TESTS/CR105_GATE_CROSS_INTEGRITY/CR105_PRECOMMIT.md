# CR105 GATE_CROSS_INTEGRITY

## Test Class

```text
META_CONSISTENCY_CHECK_BETWEEN_GATE_2_AND_GATE_3_PARTIAL_CLOSURES
```

## Preflight

```text
CR102 sealed GATE_2 partial closure (c_SW = c at astrophysical 1e-18
precision).
CR104 sealed GATE_3 partial closure (K(A_H) self-correction at
equivalence-principle 1e-19 precision).
CR103a locked the structural connection between the two via the
half-SW / half-write split with bounce cost.

CR105 asks: do these two partial closures interlock without
contradiction, in the regime where both apply (A < 11/12)?

The two gates carry implicit joint predictions for any measurement
that probes both simultaneously. The candidate cross-source anchors
are physical observations that test BOTH gates at once:

  - Atomic clock comparisons at gravitational potentials test
    c_SW = c (frequency = c*k locally) AND K(A_H) self-correction
    (clock rate at potential vs at infinity).

  - GW170817 tests c_gravity = c_light (GATE_2) AND zero EP violation
    in propagation (GATE_3).

  - Binary pulsar PSR B1913+16 tests c_SW = c via GW emission rate
    AND K(A_H) via orbital phase decay matching GR.

  - PSR J0740+6620 NICER tests c_SW = c locally at NS surface AND
    K(A_H) self-correction in the NS rest mass.

If CR102's c_SW = c and CR104's K(A_H) self-correction both hold in
the same data, the cross-product also holds. If they predicted
contradictory effects in any of these joint anchors, the
disagreement would surface here.
```

## Question

Do the joint anchors (atomic clocks, GW170817, binary pulsars,
NICER) confirm BOTH partial closures simultaneously, or does either
gate's closure conflict with the other when read against the same
measurement?

## SAM Joint Commitment (Locked Before Anchor Open)

```text
GATE_2:  c_SW = c           (locally at every A < 11/12)
GATE_3:  K(A_H) self-correct (K * r_bounce * m = const cost, A < 11/12)

JOINT IMPLICATION:
  At any A < 11/12 and any observer, a free particle of locally-
  measured mass m_local propagates with speed v <= c_local = c (a
  constant), where c is the same constant at all A.
  This is the equivalence principle plus Lorentz invariance, locally,
  in the SAM substrate.

Free parameters introduced: 0
Boundary of joint validity: A < 11/12

Beyond 11/12: GATE_2 self-correction breaks down (spaghettification
              regime per CR103a). Joint prediction does not extend
              past 11/12.
```

## Anchor Composition

```text
LIVE JOINT ANCHORS (each probes BOTH gates simultaneously):

  J1  Al+ optical clock at gravitational potential difference
      (Chou et al. 2010): tests local light speed AND clock rate
      vs gravitational potential.
      precision ~1e-18

  J2  GW170817: tests c_gravity vs c_light (GATE_2) AND signal
      propagation under EP (GATE_3).
      precision ~1e-15

  J3  PSR B1913+16 binary pulsar: orbital decay rate from GW
      emission tests c_SW = c (GW propagation) AND K(A_H) self-
      correction (orbital phase tracks GR).
      precision ~3e-3

  J4  PSR J0740+6620 NICER: NS surface gravity tests local c
      (GATE_2) AND NS rest mass (GATE_3) jointly.
      precision ~0.03

HONEST NEGATIVES:

  HN1  Withdrawn joint claim (CLASS_A)
  HN2  Unpublished joint claim (CLASS_X)
  HN3  Synthetic perturbation (CLASS_G)
```

## Test Method

```text
Step 1  Lock SAM joint commitment: equivalence-principle compatible
        zero deviation at every joint anchor's A.
Step 2  Hash prediction, commit BEFORE envelope opens.
Step 3  Open envelope; verify sibling sha256.
Step 4  For each joint anchor: compute residual against the joint
        zero-deviation commitment.
Step 5  Cross-check: a joint anchor passes only if BOTH gates'
        partial-closure verdicts hold in the same data point. If
        either gate would fail at this anchor, the joint test would
        detect the inconsistency.
Step 6  Emit evidence rows, summary, result.
```

## Pass Conditions (Reporting Completion)

CR105 is complete when:

- joint anchors are tested against the joint zero commitment
- temporal ordering is correct
- evidence rows show joint compatibility per anchor
- result.md cites CR102 and CR104 verdicts as upstream
- summary records GATE_CROSS_INTEGRITY_PASS or contradiction flagged

## Possible Outcomes

```text
GATE_CROSS_INTEGRITY_PASS
    all joint anchors confirm both GATE_2 and GATE_3 closures
    simultaneously within their stated precision; the two partial
    closures interlock cleanly.

GATE_CROSS_CONTRADICTION_FLAGGED
    at least one joint anchor reveals a measurement that one gate
    predicts inconsistently with the other; the contradiction is
    recorded without modifying CR102 or CR104 verdicts.

GATE_CROSS_INCONCLUSIVE
    some joint anchors at 2-sigma only; mixed verdict.
```

## Wrong Controls

- HN1 withdrawn must fail Gate A
- HN2 unpublished must fail Gate A
- HN3 synthetic must fail Gate R
- Modifying CR102 or CR104 from this CR is a protocol violation

## Blindness Protocol Citation

```text
blindness_protocol_cite = 13_CERN_INDEPENDENT_TESTS/BLINDNESS_PROTOCOL.md
blindness_protocol_sha256 = recorded at runner time
```

## Rule-9 Line

```text
This CR could have falsified the joint coherence of SAM's two partial
closures if any joint anchor (atomic clock, GW170817, binary pulsar,
NICER) showed a measurement consistent with one gate but contradicting
the other. The two gates predict the same thing (zero deviation from
SR + EP locally for A < 11/12), so joint anchors testing both
simultaneously give the same answer regardless of which gate the
analyst reads.

If the joint test passes, GATE_2 + GATE_3 partial closures form a
single coherent substrate-foundation reading. If it fails, the
contradiction is on the record and the foundation has a crack to
repair.
```

## Status

```text
PROVISIONAL_DRAFT_PRE_SEAL_SIGN_OFF
```
