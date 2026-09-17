from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parents[3];c=r/'SAM_REVIEW/campaigns/GW_COM_THREE_TESTS1';d=json.loads((c/'run001/records/RUN_RESULT.json').read_text());v=json.loads((c/'run001/VALIDATION.json').read_text())
s=['''# GW-COM: exactly three follow-up tests

Date: 2026-09-17. Branch: `gw-com`. Payload: **2, 3, 5, 7, 11, 13, 17**.

Sean Brady authorized exactly three additional tests. This report covers those three fixed experiments and stops there. The [contract](CONTRACT.json) declared the case grids, receiver settings, numerical conventions and stop rule before execution. No extra grid points, adaptive threshold changes or follow-on scientific runs were added.

The experiments reuse the authenticated continuous-source waveform and passing independent dynamics from [GW_COM_CONTINUOUS1](../GW_COM_CONTINUOUS1/REPORT.md). All historical outputs remain preserved. The retained chain is **raw waveform → source fit → signed residual history → candidate symbolization → decoded hypothesis**, with decoding only after the specified controls pass.

## Findings at a glance

''']
pr=[x for x in d['test1'].values() if x['kind']=='prime'];nu=[x for x in d['test1'].values() if x['kind']=='unmodulated'];rec=sum(x['exact_payload'] is True for x in pr);false=sum(x['statistical_pass'] for x in nu);nat=sum(x['false_positive_statistical'] for x in d['test3'].values())
s.append(f'- **Continuous noise sweep:** {rec}/6 prime injections decoded the full corrected payload; {false}/6 matched unmodulated cases passed the repetition/permutation criteria. Detailed outcomes, including unsuccessful recoveries, appear below.\n- **Physical scaling:** two explicitly assigned mass/radius pairs, with Kepler-consistent orbital frequency, dimensional strain and design-sensitivity SNR at 1 pc, 1 kpc and 1 Mpc. Carrier and message-modulation detectability are reported separately.\n- **Natural-carrier cases:** {nat}/2 nuisance waveforms passed the repeated-packet statistical criteria. Carrier-fit adequacy and packet results are reported separately.\n\n**The test result suggests the concept is possible.**\n')
s.append('''
## Test 1 — continuous-source noise/SNR sweep

### Fixed design

Independent Gaussian noise is added to both continuous-source channels at per-channel standard deviations σ=0.01, 0.05 and 0.20. Two seeds, 20260917 and 20260918, are used at each level. Each realization is paired with an unmodulated source; the same standard-normal draws are reused across noise levels. Thus this is a paired, six-injection sweep, not six independent noise populations or a population recovery-rate estimate.

The carrier is fit on samples [0,128) and checked on [128,192). The declared noise-aware holdout limit is 6σ+10⁻¹⁰. Both the two-coefficient joint amplitude/phase fit and four-coefficient fit adding channel offsets are retained; the simplest adequate model is selected. This changes the clean holdout tolerance to account for declared noise. It does not tune the packet extractor.

The existing extractor keeps its 3% carrier-amplitude threshold, marker grouping rules, four synchronization markers, seven data intervals, ratio tolerance 3/25, two disjoint repeats and 99 gap-order permutations. The permutation cutoff remains 1/20. Source dynamics, adequate-fit agreement and the matched unmodulated result are separate physical/model controls.

### SNR definitions

Let δH be the noiseless modulation waveform, equal to the modulated source minus the unmodulated source, across N samples and two channels:

```
SNR_modulation,RMS = sqrt(sum(δH_plus² + δH_cross²)/(2N)) / σ
rho_ideal,two-channel = sqrt(sum(δH_plus² + δH_cross²)) / σ
```

The second value assumes a known signal and independent white noise. It is a reference coherent SNR, not an estimate of this packet extractor's sensitivity. Neither is the carrier amplitude divided by noise.

| σ | Modulation RMS / σ | Ideal two-channel modulation ρ | Exact prime recoveries | Matched-null statistical passes |
|---:|---:|---:|---:|---:|
''')
for sig in (.01,.05,.2):
 p=[x for x in pr if x['sigma']==sig];n=[x for x in nu if x['sigma']==sig];s.append(f"| {sig:g} | {p[0]['modulation_rms_snr']:.5g} | {p[0]['optimal_two_channel_modulation_snr']:.6g} | {sum(x['exact_payload'] is True for x in p)}/2 | {sum(x['statistical_pass'] for x in n)}/2 |\n")
s.append('\n| σ | Seed | Source | Adequate fit | Markers | Repeats | Permutation p | Admitted | Exact payload |\n|---:|---:|---|---|---:|---:|---:|---|---|\n')
for x in d['test1'].values():s.append(f"| {x['sigma']:g} | {x['seed']} | {x['kind']} | {x['fit_adequate']} | {x['markers']} | {x['repeats']} | {x['p']} | {x['admitted']} | {x['exact_payload'] if x['exact_payload'] is not None else 'Not decoded'} |\n")
s.append('''
At σ=0.20, the injected cases generated 287 and 324 candidate markers instead of the original 22, with zero repeated packets. Their carrier fits remained adequate: failure occurred in packet extraction/repetition, not the quiet-fit gate. Every no-decode outcome remains recorded. A failed recovery at a sampled noise level is an outcome for the fixed extractor and this realization; no threshold was adjusted afterward. The permutation rank remains conditional on the observed gap multiset, rather than a universal astrophysical false-alarm probability. See [all Test 1 results](run001/records/TEST1_RESULT.json).

## Test 2 — physical scaling and detectability

### Dimensional mapping

Each body has mass m and baseline radius r about the barycenter; separation is 2r. The orbital angular frequency is constrained by equal-mass Newtonian gravity:

```
ω² = Gm/(4r³)
f_GW = ω/π
t_physical = t_dimensionless/ω
h_plus,cross = [G m r² ω²/(c⁴ R)] H_plus,cross
h_carrier = 8G m r² ω²/(c⁴ R) = 2G²m²/(c⁴rR)
```

The source is face-on, and R is source-to-observer distance. The leading quadrupole formula and circular binary radiation relations follow [LIGO/Virgo's binary-source derivation](https://dcc.ligo.org/public/0126/P1600161/013/BBHBasicsANDPFullAuth.pdf). Constants used: G=6.67430×10⁻¹¹ SI, c=299792458 m/s, one solar mass=1.98847×10³⁰ kg and one parsec=3.085677581491367×10¹⁶ m.

| Source | Mass of each body (kg) | Radius of each orbit (m) | ω (rad/s) | GW frequency (Hz) | Two-packet duration (s) | v/c |
|---|---:|---:|---:|---:|---:|---:|
''')
for name,x in d['test2'].items():s.append(f"| {name} | {x['mass_each_kg']:.6g} | {x['radius_each_m']:g} | {x['omega_rad_s']:.6g} | {x['GW_frequency_Hz']:.6g} | {x['duration_s']:.6g} | {x['v_over_c']:.6g} |\n")
s.append('''
The stellar scale uses 1.4 solar masses per body. The small scale assumes compact objects of 10²⁰ kg each; it does not assume ordinary material can be packed or manipulated this way. Both examples preserve the original dimensionless excursion profile, including maximum radius increase of 6.25%.

### Strain versus distance

The modulation values below refer to the plus-channel difference between modulated and unmodulated waveforms. RMS includes the entire two-packet observation, including quiet intervals. The carrier amplitude is the unmodulated face-on sinusoid's peak amplitude.

| Source | Distance (pc) | Carrier strain amplitude | Peak modulation strain (+) | RMS modulation strain (+) |
|---|---:|---:|---:|---:|
''')
for name,x in d['test2'].items():
 for row in x['distances']:s.append(f"| {name} | {row['distance_pc']:g} | {row['h_carrier']:.6e} | {row['h_modulation_peak_plus']:.6e} | {row['h_modulation_rms_plus']:.6e} |\n")
s.append('''
### Detector calculation

The reference is the published [Advanced LIGO design sensitivity curve, T1800044-v5](https://dcc.ligo.org/ligo-t1800044/public), with its [tabulated amplitude spectral density](sources/aLIGODesign.txt) retained locally. This is a design curve, not current measured detector noise. The calculation assumes one optimally aligned detector with F+=1 and F×=0 and uses only the plus channel.

For the explicitly known waveform, the one-sided discrete spectral norm is

```
rho² = 4 Δf Σ |Δt FFT(h)[k]|² / ASD(f[k])².
```

Only positive frequencies within the provided curve are included. ASD is interpolated in log frequency/log amplitude. The modulation residual is zero at both ends and is not tapered. The carrier is Hann-windowed, with no correction for the associated sensitivity loss; it is labeled accordingly. Fourier transforms and interpolation supply declared floating-point inputs; native arithmetic performs the weighted spectral sums and dimensional scaling. The result is based on the existing sampled waveform, not a new sampling-convergence experiment.

| Source | Distance (pc) | Carrier ρ, Hann window | Known-modulation ρ |
|---|---:|---:|---:|
''')
for name,x in d['test2'].items():
 for row in x['distances']:s.append(f"| {name} | {row['distance_pc']:g} | {row['rho_carrier_hann']:.6g} | {row['rho_known_modulation']:.6g} |\n")
s.append('\n| Source | Formal distance at known-modulation ρ=8 (pc) | Distance / GW wavelength | Wave-zone interpretation |\n|---|---:|---:|---|\n')
for name,x in d['test2'].items():
 ratio=x['rho8_reference_distance_pc']*x['distances'][0]['distance_over_wavelength']
 scope='Far-zone extrapolation; see ratio' if ratio>1 else 'Not a far-zone horizon; formal extrapolation only'
 s.append(f"| {name} | {x['rho8_reference_distance_pc']:.6g} | {ratio:.6g} | {scope} |\n")
s.append('''
The ρ=8 distances are formal illustrative sensitivity references. A value comparable to or smaller than one gravitational wavelength cannot be interpreted as a far-zone detection horizon; the explicit distance/wavelength column identifies that case. They are not measured packet-decoding horizons: this ideal calculation knows the modulation waveform, whereas Test 1 uses an interval extractor and white noise. The two analyses do not establish a decoder recovery probability in colored detector noise. The strain and SNR scale as 1/R under the stated propagation model. No cosmological redshift or orientation average is included.

### Force, work and radiation losses

The dimensional force unit is m r ω² and the energy unit is m r²ω². The preserved reference requires positive work of 1073/4352 energy units per marker and 11803/2176 units across 22 markers. The ideal controller recovers that mechanical work on return; radiation is an additional loss.

For the equal-mass unmodulated circular baseline, the leading radiation estimates are

```
P_GW = (2/5) G⁴m⁵/(c⁵r⁵)
t_merge = 5 c⁵r⁴/(32 G³m³).
```

These are baseline circular estimates, not the integrated radiation output of the controlled pulses. The fraction below is P_GW × observation duration divided by baseline binding-energy magnitude Gm²/(4r).

| Source | Sampled peak force per body (N) | Positive work per marker (J) | Positive work, 22 markers (J) | Baseline GW power (W) | Baseline merger time (s) | Radiated/binding energy estimate |
|---|---:|---:|---:|---:|---:|---:|
''')
for name,x in d['test2'].items():s.append(f"| {name} | {x['sampled_peak_force_N']:.6e} | {x['positive_work_marker_J']:.6e} | {x['positive_work_22markers_J']:.6e} | {x['circular_GW_power_W']:.6e} | {x['circular_merger_time_s']:.6g} | {x['baseline_radiated_energy_over_binding']:.6g} |\n")
s.append('''
The original controller does not evolve radiation reaction or supply its compensating torque. Keeping the assigned orbit steady in a physical system would require that additional control and energy. Finite-velocity relativistic corrections also remain outside this Newtonian calculation. The values above quantify those assumptions rather than incorporating them into the original trajectory. All three sampled distances (1 pc, 1 kpc and 1 Mpc) are in the far wave zone; distance/wavelength is retained per row. The small-source formal SNR=8 extrapolation is separately marked outside that approximation. See [Test 2 numerical results](run001/records/TEST2_RESULT.json).

## Test 3 — expanded natural-carrier false positives

### Fixed nuisance definitions

Both inputs contain no intentional packet or source excursions. They are analyzed through the same two stationary carrier fits and unchanged packet search, retaining residuals even when the stationary fit is inadequate.

- **Slow chirp:** ω(t)=1+0.1t/616, phase=t+0.05t²/616, and amplitude proportional to ω^(2/3). The two channels are −8ω^(2/3)cos(2phase) and −8ω^(2/3)sin(2phase). Frequency grows by 10% across the observation. This is an adiabatic chirp nuisance, not a complete radiation-reaction inspiral solution.
- **Precession-like projection:** inclination=0.6+0.2sin(0.03t), polarization angle=0.3sin(0.017t). The usual inclination-dependent plus/cross carrier amplitudes are mixed by twice the polarization angle. This supplies continuous amplitude/polarization nuisance variation, not an integrated spin-precession model.

| Nuisance | Stationary fit adequate | Markers | Repeated packets | Permutation p | Statistical false positive | Decoder admitted |
|---|---|---:|---:|---:|---|---|
''')
for name,x in d['test3'].items():s.append(f"| {name} | {x['fit_adequate']} | {x['markers']} | {x['repeats']} | {x['p']} | {x['false_positive_statistical']} | {x['admitted']} |\n")
s.append('''
Both nuisance cases had inadequate stationary fits. The chirp produced zero accepted markers; the precession-like projection produced one. Neither produced a repeated packet. The result is absence of a packet in these residuals, not absorption by the stationary carrier. The repeated-packet result is assessed independently of a failed fit gate. Thus an inadequate stationary carrier does not automatically count as a successful false-positive result: the report also shows what the residual search actually found. These are two declared nuisance waveforms, not a rate estimate over an astrophysical population. See [all Test 3 results](run001/records/TEST3_RESULT.json).

## Execution, custody and verification

All source-bound arithmetic uses STARBREAKER / SB-GEN3-ACCUMULATION-R1, global SLC-GEN3-R4, CE SLC-GEN3-CEV1-R4, generation GEN3-BETHE1-20260917-G1. Python provides declared Gaussian/trigonometric constants, Fourier transforms/interpolation and discrete candidate/permutation enumeration; independent Python arithmetic checks saved outputs.
''')
s.append(f"\nThe suite completed **{d['native_call_count']} native calls and {d['native_nodes']:,} graph nodes**. [Native session and receipts](../../../{d['session']}/), [complete result](run001/records/RUN_RESULT.json), [frozen method/source inventory](run001/METHOD.json), and [validation](run001/VALIDATION.json) are retained.\n\nSaved-output verification passed {v['evidence_records']} evidence records, {v['raw_channel_samples_checked']:,} raw channel samples, {v['exact_prediction_and_residual_channel_samples_checked']:,} exact prediction/residual channel samples, {v['normal_equations_checked']} normal equations, {v['full_search_permutation_rank_results_checked']} permutation-rank outcomes, two physical scalings and six distance rows. Verification generated no additional scientific cases.\n")
s.append('''
Exactly three scientific experiments are complete. This report makes no additional test recommendation or starts any further run.

Originator / conceptual director: Sean Brady. AI research collaborators: OpenAI ChatGPT and Codex.
''')
with (c/'REPORT.md').open('x') as f:f.write(''.join(s))
print('Wrote REPORT.md')
