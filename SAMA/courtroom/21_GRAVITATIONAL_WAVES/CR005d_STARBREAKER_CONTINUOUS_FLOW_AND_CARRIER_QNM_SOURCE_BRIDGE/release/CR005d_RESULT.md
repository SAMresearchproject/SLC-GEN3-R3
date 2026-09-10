# CR005d Continuous Starbreaker Flow and Carrier-QNM Source Bridge Result

## Primary verdict

`PASS_CONTINUOUS_STARBREAKER_FLOW_ESCAPE_BEFORE_CLOSURE__CARRIER_QNM_SOURCE_CONSTRUCTED__SOURCE_SEPARATION_OPEN`

All **14/14** construction gates and
**10/10** controls passed.

## Continuous Starbreaker result

The three stored Starbreaker states were lifted into a zero-fit continuous
structural flow: exponential radial collapse, a bounce impulse at `t=1`, then
constant radial and shortest-branch angular release. The maximum stored-state
reconstruction error was `2.191e-14`.

```text
dual carriers                     = 1993
escape before closure             = 1541
continuous-flow inequality fraction = 0.7732062217762168
median closure-minus-escape margin  = 0.04020605301428759
continuous transition roots         = 10515538
root failures                        = 0
```

| geometry | door | dual carriers | escape-before-closure fraction | median margin |
|---|---|---:|---:|---:|
| localized_ledger_cells | discovery | 927 | 0.7594390507011867 | 0.04545876521248715 |
| localized_ledger_cells | validation | 382 | 0.693717277486911 | 0.021479124764113067 |
| localized_ledger_cells | final | 420 | 0.780952380952381 | 0.03637120591110943 |
| dispersed_slots | discovery | 146 | 0.9383561643835616 | 0.06761421807783563 |
| dispersed_slots | validation | 77 | 0.8831168831168831 | 0.061437581076603465 |
| dispersed_slots | final | 41 | 0.9512195121951219 | 0.06453966541462819 |

## Carrier source bridge

The run constructed the trace-free unit-carrier quadrupole `Q_ab`, its source
`d^2Q_ab/dt^2`, its third-derivative power proxy, and a causal response using
the sealed kernel:

```text
omega_R M = 3/8
omega_I M = 4/45
g(u)      = exp[-(4/45)u] sin[(3/8)u] / (3/8)
```

| geometry | door | escape coherence | escape power/carrier | return power/carrier | escape > return |
|---|---|---:|---:|---:|---|
| localized_ledger_cells | discovery | 1.7978612366335915 | 0.09650401053415247 | None | False |
| localized_ledger_cells | validation | 3.4315320486506975 | 0.08336551490403596 | None | False |
| localized_ledger_cells | final | 1.7072070641983368 | 0.07697967839515579 | None | False |
| dispersed_slots | discovery | 0.5742899440898013 | 0.031435973944351756 | 0.008489363277406134 | True |
| dispersed_slots | validation | 0.5266661857593189 | 0.025479505247762015 | 0.006045694685260282 | True |
| dispersed_slots | final | 0.36939099339609516 | 0.030845698252177357 | 0.052442293946163496 | False |

The exact incoherent reference for `coherence_gain` is one: it is the expected
power after independent sign scrambling of the individual carrier tensors.

## Construction quality

- Frozen sources matched: **14/14**
- Scenarios: **96/96**
- Atoms: **482,112/482,112**
- Root scan-control maximum error: **7.105e-15**
- Median fine/coarse source-power error: **0.019361866885052904**
- Median fine/coarse QNM-response error: **0.0029729547468950466**
- Maximum relative trace error: **2.5997906629060057e-15**

## Meaning and boundary

This is the first prospective continuous Starbreaker source surface and the
first carrier-history-resolved QNM source bridge in the branch. It tests a
curved continuous path rather than relabeling the prior affine clock.

The clock remains dimensionless Starbreaker phase time. Unit carrier weights
are not matter masses, and the QNM convolution assumes a unit-clock bridge that
has not been derived from physical mass-scaled time. Therefore the output is a
dimensionless source and response candidate—not gravitational-wave strain,
luminosity, frequency in hertz, signal speed, or a detector forecast.
