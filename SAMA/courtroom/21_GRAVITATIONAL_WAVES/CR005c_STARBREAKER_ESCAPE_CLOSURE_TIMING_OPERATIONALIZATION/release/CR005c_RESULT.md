# CR005c Starbreaker Escape / Closure Timing Operationalization Result

## Primary verdict

`PASS_OPERATIONAL_ESCAPE_BEFORE_CLOSURE_STABLE_ACROSS_FROZEN_DOORS__PHYSICAL_TIME_OPEN`

The frozen Starbreaker trajectory surface was converted into an exact local
contact-crossing clock without importing a gravitational-wave timing formula.
All **10/10** construction gates and
**8/8** controls passed.

## Operational definitions

```text
stored-stage time: seed=0, collapse=1, final=2
release surface:   carrier-matter distance crosses outward through 0.076
closure surface:   carrier-matter distance crosses inward through 0.076
tau_escape_post:   earliest 010/110 outward crossing for one carrier
tau_closure:       earliest 101 inward crossing for the same carrier
```

This is a local relation clock. It is not seconds and the relation surface is
not a global horizon.

## Primary carrier-occurrence result

```text
dual post-collapse carriers = 1993
escape before closure       = 1535
inequality fraction         = 0.77019568489714
median closure-escape margin= 0.035812527449339715
```

| geometry | door | primary carriers | fraction escape before closure | median margin |
|---|---|---:|---:|---:|
| localized_ledger_cells | discovery | 927 | 0.7529665587918015 | 0.0408196843198958 |
| localized_ledger_cells | validation | 382 | 0.6910994764397905 | 0.01812887104234473 |
| localized_ledger_cells | final | 420 | 0.7833333333333333 | 0.03290831395197391 |
| dispersed_slots | discovery | 146 | 0.9383561643835616 | 0.06905355364502996 |
| dispersed_slots | validation | 77 | 0.8831168831168831 | 0.05994241816991175 |
| dispersed_slots | final | 41 | 0.9512195121951219 | 0.06325330507136906 |

## Source reconstruction

- Scenarios: **96/96**
- Atoms: **482,112/482,112**
- Carrier-matter transition crossings solved: **10,515,538**
- Crossing failures: **0**
- Carrier-matter history census: exact match = **True**
- Frozen sources: **14/14**

## Meaning

The result decides only whether the stored Starbreaker relation trajectories
support a stable operational ordering between ending-zero release and returned
`101` closure. The gravitational-wave branch was not allowed to define the
surface, the clock, or the verdict.

## Boundary

Starbreaker currently stores three states rather than a physical time series.
No physical escape duration, horizon-closure duration, gravitational strain,
luminosity, signal speed, detector observable, or universal timing law is
installed. A physical timing test requires a prospective time-resolved
Starbreaker evolution rule.
