# GW-COM: corrected prime intervals and continuous binary control

Date: 2026-09-17. Branch: `gw-com`.

**The test result suggests the concept is possible.**

The current message is **2, 3, 5, 7, 11, 13, 17**. The corrected C4 pipeline recovers all seven values in both clean and bounded-noise cases. Its continuous successor recovers the same seven values twice from signed two-polarization residuals after the declared model, numerical and statistical controls pass. The unmodulated continuous control remains blocked before decoding.

Sean Brady supplied the communication concept, five-layer architecture and correction adding 3. Codex implemented the continuous control experiment as the next recommendation from the [earlier detailed report](../GW_COM_PIPELINE1/DETAILED_REPORT.md). That report and the earlier six-value results remain historical records.

## 1. Corrected interval experiment

[GW_COM_PIPELINE2](../GW_COM_PIPELINE2/RESULT.md) explicitly declares seven data intervals per frame. Historical six-interval framing remains supported; new tests cover seven-value recovery and rejection of an incomplete frame.

| Case | Repeated packets | Permutation rank | Admission |
|---|---:|---:|---|
| Clean corrected prime message | 2 | 1/100 | Decoded all seven primes |
| Noisy corrected prime message | 2 | 1/100 | Decoded all seven primes |
| Alternate message 4,6,8,10,12,14,16 | 2 | 1/100 | Decoded alternate message |
| Clean/noisy unmodulated; drift only | 0 each | 1 each | All blocked |

The corrected run used 37 native calls and 560,479 graph nodes. Independent verification checked 92 evidence records, 64,104 exact source/residual samples and 36 normal equations. See its [validation](../GW_COM_PIPELINE2/run001/VALIDATION.json).

## 2. Continuous source and control law

The [execution contract](CONTRACT.json) uses dimensionless Newtonian mechanics: two equal unit masses, G=4, baseline radius 1 per body and angular speed 1. The bodies remain opposite, at ±r(t)(cos t, sin t). Each marker produces a smooth radial excursion. With u=t−marker time,

```
r = 1 + (1-u²)^4/16                 for |u| < 1; otherwise r=1
rdot = -u(1-u²)^3/2
rddot = (1-u²)^2(7u²-1)/2
```

The profile joins the circular orbit with three continuous derivatives. Its maximum radius is 17/16. The reference force per body, resolved along the rotating radial and tangential directions, is

```
f_r = rddot - r + 1/r²
f_theta = 2 rdot
```

The other body receives the opposite force. This makes the required acceleration and force explicit throughout the excursion. An independent integration evolves the actual Cartesian position and velocity under mutual Newtonian attraction, this reference feedforward force, and Cartesian tracking feedback with kp=kd=4. The feedback is zero on the exact reference and controls numerical deviations.

The simulated two-body system has an external controller. Its energy accounting includes the controller's signed mechanical work. Radiation reaction and hardware losses are not included.

## 3. Two waveform channels

The leading quadrupole relationship between source motion and wave strain supplies the physical foundation; see the LIGO/Virgo paper [The basic physics of the binary black hole merger GW150914](https://dcc.ligo.org/public/0126/P1600161/013/BBHBasicsANDPFullAuth.pdf). The control profile above is this campaign's construction.

We retain two unscaled face-on channels:

```
A = rdot² + r*rddot - 2r²
B = 4r*rdot
Hplus  = 4(A cos(2t) - B sin(2t))
Hcross = 4(A sin(2t) + B cos(2t))
```

The common dimensional propagation factor is omitted. There is no assigned source mass in kilograms, distance, calibrated detector strain or detector noise spectrum. These are explicit source channels in the stated dimensionless model.

Sampling is dt=1/8 over t=0 through 616, giving 4,929 samples per case. Trigonometric inputs are rounded to 14 decimal places and then admitted as rational numbers. Native arithmetic evaluates the reference mechanics, channels, fits and residuals exactly relative to those inputs. Independent verification also constructs the quadrupole directly from Cartesian positions, velocities and accelerations; its maximum discrepancy is 5.87×10⁻¹⁴.

## 4. Five-layer retained analysis

1. **Carrier:** joint two-channel amplitude/phase fit, with a second retained model adding one DC offset per channel. Both use 128 quiet calibration samples and a separate 64-sample quiet holdout. The selected carrier has α=−8 and β=0; offset alternatives have zero offsets.
2. **Modulation:** four synchronization markers followed by seven data intervals, two packets, time unit 4 and a 23-unit guard. Each marker uses the same excursion strength. Strength encoding remains a later layer.
3. **Residual:** retain the signed plus and cross differences for every sample and every fit. Squared residual norm is a derived marker-detection view; it does not replace those histories.
4. **Information:** locate marker groups, search the declared frame format and require two disjoint repeated packets. Compare the maximum repetition statistic with 99 shuffled gap orders, repeating the framing search for each permutation.
5. **Decoder:** admit only after matching evidence lineage, physical/model controls and statistical controls pass. Compare the decoded hypothesis with transmitter truth afterward.

The corrected bins `[2,3,5,7,11,13,17]` appear in both packets and both adequate carrier models. The continuous prime candidate has permutation rank 1/100; the unmodulated candidate has no markers or repeated frame and rank 1. This rank is conditional on the observed gap multiset and exchangeable gap order. It is not an astrophysical false-alarm rate or a probability of intentional origin.

The clean continuous test and null are separate from the noisy C4 test. Noise has not yet been added to the continuous source experiment. Chirp, precession and error-correcting structure are also not exercised here.

## 5. Numerical refinement and admission

The original [run result](run001/records/RUN_RESULT.json) remains intact. Although its prime symbols repeated correctly, the energy-balance error exceeded the declared 10⁻⁵ tolerance, so both cases were blocked. A [supplemental contract](REFINEMENT_CONTRACT.json) refined integration to h=1/64 while retaining the source, waveforms, fits, residuals, candidates, statistical criteria and numerical tolerances.

| Case | RK4 step | Maximum state error | Energy-balance error | Dynamics disposition |
|---|---:|---:|---:|---|
| Prime | 1/16 | 4.849×10⁻⁶ | 2.040×10⁻³ | Coarse comparison |
| Prime | 1/32 | 2.902×10⁻⁷ | 1.228×10⁻⁴ | Failed energy tolerance |
| Prime | 1/64 | 1.775×10⁻⁸ | 7.537×10⁻⁶ | PASS |
| Unmodulated | 1/16 | 2.506×10⁻⁶ | 1.676×10⁻³ | Coarse comparison |
| Unmodulated | 1/32 | 1.511×10⁻⁷ | 1.011×10⁻⁴ | Failed energy tolerance |
| Unmodulated | 1/64 | 9.277×10⁻⁹ | 6.215×10⁻⁶ | PASS |

At the refined step, maximum waveform errors are 2.594×10⁻⁷ for the prime source and 1.412×10⁻⁷ for the unmodulated source, below the unchanged 10⁻⁴ tolerance. State errors pass the unchanged 10⁻⁵ tolerance and errors decrease on refinement. The prime candidate is now admitted and decoded; the null remains statistically blocked. See the [final refinement result](refinement001/records/RESULT.json) and [decoded data](refinement001/records/continuous_prime.decoded.data.json).

The primary native waveform is the analytic controlled reference. The RK4 trajectory is an identified independent numerical check, with its own retained trajectory and error history. Refinement adds no native calls and does not substitute integrated samples into the original waveform lineage.

## 6. Force and work findings

The reference pair energy and controller power are

```
E = rdot² + r² - 2/r
P = 2(f_r*rdot + f_theta*r)
  = 2 rdot(rddot + r + 1/r²) = dE/dt.
```

Native arithmetic verifies this identity at every sampled profile position. The [work ledger](run001/records/work_ledger.data.json) records:

| Quantity | Value in dimensionless units |
|---|---:|
| Positive mechanical work per marker | 1073/4352 ≈ 0.2465533 |
| Marker count across both packets | 22 |
| Total positive mechanical work | 11803/2176 ≈ 5.4241728 |
| Mechanical work returned to ideal controller | Same magnitude |
| Signed net work after complete excursions | 0 |
| Maximum force magnitude over sampled profile, per body | ≈ 0.6766869 |

The positive-work amount follows the reference energy rise from −1 to −3279/4352. Energy increases on the outward half and decreases on return: the factor rddot+r+1/r² is positive throughout, so the sign of power follows rdot. This gives the excursion work from endpoints rather than numerical power quadrature.

Zero signed net work is an ideal recovery result, not a zero energy requirement. A physical controller must supply the positive work and handle the returned energy. Efficiencies, radiation losses and physical scaling have not been assigned. The sampled force maximum is not claimed as a continuous-time optimized maximum.

## 7. Execution and verification

Both native runs used STARBREAKER / SB-GEN3-ACCUMULATION-R1 on SLC-GEN3-R4 and SLC-GEN3-CEV1-R4, generation GEN3-BETHE1-20260917-G1. Continuous execution used **68 native calls and 662,145 native graph nodes**. Session receipts are retained under [the run session](run001/sessions/STARBREAKER_9f9e28360c974e39a7785761c6e51d8e/).

The independent [validation](VALIDATION.json) passes:

- 35 evidence records authenticated.
- 17 native mechanics profile rows checked independently.
- 19,716 waveform channel samples checked against Cartesian quadrupoles.
- 39,432 exact signed residual channel samples checked.
- Positive-work identity and final prime/null admission outcomes checked.
- All 12 shared framing and decoder-gate unit tests pass.

[run.py](run.py), [refine.py](refine.py) and [verify.py](verify.py) retain the executable route; each run retains its code/contract snapshots. The shared implementation is [continuous.py](../../../GW_COM/runtime/continuous.py). Completed run directories must not be overwritten.

## 8. Next useful experiment

The next recommended step is to pass the same continuous channels through a declared receiver/noise model and measure recovery versus signal level, while retaining the signed channel histories and matched unmodulated controls. This would connect the completed continuous source experiment with the bounded-noise success already obtained in the corrected C4 experiment. The second strength-based prime layer can then be added as a separately specified alphabet, with interval-only and strength-only recovery measured independently.

Originator / conceptual director: Sean Brady. AI research collaborators: OpenAI ChatGPT and Codex.
