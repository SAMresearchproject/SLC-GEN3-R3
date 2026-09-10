# CR005g Starbreaker / Weak-CCSN Pixel Bridge Result

## Primary verdict

`BOUNDARY_PIXEL_SURFACE_CONSTRUCTED__NO_STABLE_STARBREAKER_CCSN_MORPHOLOGY_MATCH`

All **12/12** construction gates and **11/11** controls passed.

## What was compared

Ten public three-dimensional core-collapse supernova matter-strain waveforms were compared directly with 96 Starbreaker post-bounce unit-carrier quadrupole sources across 13 fixed observer directions. No compact-binary chirp and no black-hole QNM response was used as the target.

Both sources were converted into the same 48 by 64 normalized time-frequency power grid. The primary statistic was all-pixel Hellinger affinity; every best-template search was repeated for 47 time-shift nulls and the locked reversal controls.

## Door results

| door | waveforms | observed median | shift q90 | shift q95 | p | clears q90 | clears q95/all |
|---|---:|---:|---:|---:|---:|---|---|
| discovery | 4 | 0.150857 | 0.155669 | 0.155861 | 0.500000 | False | False |
| validation | 3 | 0.068025 | 0.094694 | 0.096175 | 0.812500 | False | False |
| final | 3 | 0.076474 | 0.073062 | 0.073193 | 0.020833 | False | False |

## Closest individual morphology

The largest affinity was **0.407647** for `s9.0.swbj15.horo.3d.gw.dat` against Starbreaker `REF_0272` in view `face_yz_m`. This is a selected normalized morphology match, not a physical amplitude or mechanism identification.

## Boundary

Starbreaker still has unit carrier weights and dimensionless event phase. The run therefore does not calculate strain, luminosity, seconds, hertz, distance reach, or detector sensitivity. A morphology bridge can identify missing or shared source texture; physical prediction requires carrier mass/energy and a phase-to-seconds map.

The downloaded archive is retained as internal source evidence; this campaign does not assert redistribution rights.
