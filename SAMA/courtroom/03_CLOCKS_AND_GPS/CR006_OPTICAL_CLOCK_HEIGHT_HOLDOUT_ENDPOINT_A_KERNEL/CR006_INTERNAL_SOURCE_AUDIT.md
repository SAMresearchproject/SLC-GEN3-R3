# CR006 Internal Scientific Source Audit

## Scope

This audit is restricted to the active clock/GPS branch, the A-kernel/foundation scientific branches, directly cited Courtroom dependencies, and the selected external paper source chain.

No repository-root recursive search was performed by the research agent.

## Active SAM Clock/A-Kernel Chain

The active weak-field A-kernel source is:

```text
A(r) = r_s/r = 2GM/(c^2 r)
r_s = 2GM/c^2
```

Live Courtroom sources:

- `02_A_KERNEL_WEAK_FIELD/README.md` records the weak-field exterior spherical profile, Newtonian potential bridge, gradient bridge, and clock approximation.
- `02_A_KERNEL_WEAK_FIELD/CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT/CR004_PRECOMMIT.md` freezes the scoped external-contact A-kernel formula packet.
- `02_A_KERNEL_WEAK_FIELD/CR004_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT/CR004_result.md` records `CR004_PASS_SCOPED_WEAK_FIELD_A_KERNEL_EXTERNAL_CONTACT`.
- `02_A_KERNEL_WEAK_FIELD/CR003_A_KERNEL_TYPED_READOUT_RECERTIFICATION/CR003_result.md` records the typed clock readout sample with `weak_clock_exact` and `weak_clock_first_order`.

## Endpoint Clock Channel

The active clock branch is:

```text
03_CLOCKS_AND_GPS
```

The active branch README freezes the endpoint clock channel as:

```text
dtau/dt = sqrt(1 - A)
Delta f/f ~= (A_ground - A_orbit)/2
```

The existing branch-local CR is:

```text
03_CLOCKS_AND_GPS/CR005_CLOCKS_AND_GPS_EXTERNAL_CONTACT
```

CR005 records the GPS clock lane using the exact clock expression and the weak-field half-factor:

```text
clock(A) = sqrt(1 - A)
gravity_fraction_exact = sqrt(1-A_orbit)/sqrt(1-A_ground) - 1
gravity_fraction_weak = (A_ground - A_orbit)/2
```

For CR006, the same endpoint logic is applied to a laboratory height separation:

```text
weak_fractional_shift = (A_lower - A_upper)/2
exact_fractional_shift = sqrt((1-A_upper)/(1-A_lower)) - 1
```

The observable is defined as upper clock minus lower clock for a 1 mm upward separation. With this sign convention, the SAM weak endpoint prediction is positive.

## Half Factor

The factor `1/2` is active in both the branch-02 weak-field clock approximation and branch-03 GPS clock formula. Removing it is a mandatory wrong control for this CR.

## Exact Lapse

The exact lapse form is active through the clock branch expression:

```text
dtau/dt = sqrt(1 - A)
```

CR006 therefore evaluates both weak and exact endpoint readouts. The exact-minus-weak difference is a numerical internal-consistency check, not the external agreement gate.

## Common Floor A0

The foundation branch records:

```text
A0 = 1/(12*pi)
```

as a composed SAM-native base accumulation unit, not a fitted empirical term. For this endpoint clock observable, any common A0 floor cancels before the local comparison is formed. CR006 does not insert A0 as a local redshift term. A wrong control intentionally adds an uncanceled local A0 contribution and is rejected by channel rule and by magnitude.

## Earth Source Constants And Units

CR006 uses SI units throughout. The primary source constants are:

```text
c = 299792458 m/s
Earth gravitational parameter mu = GM = 3.986004418e14 m^3/s^2
local gravitational acceleration magnitude from the selected paper = 9.796 m/s^2
height unit = 1 mm = 0.001 m
```

The radial A-kernel route uses the effective spherical lower radius:

```text
r_lower = sqrt(mu/a_local)
r_upper = r_lower + 0.001 m
```

This is a frozen public-geometry reduction from the paper's local redshift acceleration and the external Earth gravitational parameter. It introduces no fitted clock normalization and no post-result tuning.

## Prior Experiment Exclusion Summary

The active Courtroom source chain has already used or cited the following external clock/redshift anchors:

- Pound-Rebka redshift scale, via the branch-02 G284c provenance summary.
- Hafele-Keating altitude clock scale, via the branch-02 G284c provenance summary.
- GPS geoid-to-orbit gravitational fraction, net daily correction, factory frequency offset, and crossover-altitude scale, via branch 03 and CR005.

No active branch-local Courtroom artifact inspected for CR006 contained a prior use of the selected Bothwell et al. 2022 optical-clock millimetre-scale redshift experiment.

## Selected External Source Chain

Selected primary source:

```text
Bothwell et al., "Resolving the gravitational redshift across a millimetre-scale atomic sample", Nature 602, 420-424 (2022), DOI 10.1038/s41586-021-04349-7.
```

The paper is a primary peer-reviewed optical-clock gravitational-redshift measurement using ultracold strontium in a vertical one-dimensional optical lattice. It provides the apparatus, clock species, height/gradient geometry, local gravitational acceleration, reported fractional frequency gradient, uncertainty, and systematic discussion required for an independent endpoint clock test.

## Firewall Status

```json
{
  "sam_language_v0_3_consulted_during_development": false,
  "sam_language_v0_3_candidate_hash_known_to_research_agent": false,
  "sam_language_v0_3_incidental_exposure_detected": false
}
```

