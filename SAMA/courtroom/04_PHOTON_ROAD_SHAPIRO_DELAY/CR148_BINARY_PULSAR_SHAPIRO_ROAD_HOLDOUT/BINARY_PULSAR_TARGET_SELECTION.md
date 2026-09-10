# CR148 Binary-Pulsar Target Selection

Selection sealed before target Shapiro comparator reveal.

## Selection Rule

Deterministic priority:

1. Exclude systems previously used in Branch 04 SAM photon-road testing.
2. Prefer independent input quality.
3. Prefer public geometry and timing data completeness.
4. Prefer usable uncertainty/covariance information.
5. Prefer bounded implementation scope.

The selection used metadata only: title, year, system name, data availability,
timing ephemeris presence, uncertainty/covariance-product presence, and Branch
04 prior-use status. No selected-system Shapiro target value was opened during
selection.

## Metadata Candidate Table

| rank | system | title | year | data availability | timing ephemeris | uncertainty/covariance products | prior SAM Branch 04 use | selection note |
|---:|---|---|---:|---|---|---|---|---|
| 1 | PSR J0737-3039A/B | Tests of general relativity from timing the double pulsar | 2006 | arXiv source package, PDF, Science journal reference, supporting material included | yes | published parameter uncertainties; table gives observed/expected comparison fields | no Branch 04 hit for J0737, Double Pulsar, binary pulsar, or PSR in CR006/CR147 | selected |
| 2 | PSR J1909-3744 | Shapiro Delay in the Binary Millisecond Pulsar PSR J1909-3744 / later high-precision timing | 2003/2020 | public papers and timing releases exist | yes | Shapiro parameters available | no Branch 04 hit | not selected: geometry and mass anchors are less independent of Shapiro fit for this campaign |
| 3 | PSR J1614-2230 | A two-solar-mass neutron star measured using Shapiro delay | 2010 | public paper and arXiv record exist | yes | Shapiro mass/inclination constraints available | no Branch 04 hit | not selected: companion mass and inclination primarily come from the Shapiro fit |
| 4 | PSR J2222-0137 | PSR J2222-0137. I. Improved physical parameters for the system | 2021 | public paper and arXiv record exist | yes | Shapiro and periastron constraints available | no Branch 04 hit | not selected: larger implementation scope and less direct independent-shape setup |

## Selected System

PSR J0737-3039A/B, using Kramer et al. 2006, "Tests of general relativity from
timing the double pulsar", arXiv:astro-ph/0609417 and Science 314:97-102.

Reason: the system has a theory-independent mass-ratio input from the two
projected semi-major axes and an independently locked total mass from the
periastron-advance relation before the Shapiro shape comparator is opened.

## Target Withheld

Withheld until after precommit and runner sealing:

- primary Shapiro shape comparator for the selected system;
- uncertainty attached to that comparator;
- observed-to-expected ratio if used by the source table for the shape readout.

