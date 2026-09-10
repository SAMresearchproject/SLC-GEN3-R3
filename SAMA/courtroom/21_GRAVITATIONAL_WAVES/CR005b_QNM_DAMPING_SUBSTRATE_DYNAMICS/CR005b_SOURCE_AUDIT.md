# CR005b Source Audit

## Canonical source chain

The active branch is `21_GRAVITATIONAL_WAVES`.

Canonical sources:

1. `COURTROOM_BRANCH_INTAKE_MAP.md` identifies branch 21 as an active
   gravitational-wave branch with executed CR records.
2. `21_GRAVITATIONAL_WAVES/README.md` defines the carrier-tensor framing:
   `Theta = 18`, `Theta/R^2 = 1/8`, `R = 12`, and `d_hat = 3`.
3. `21_GRAVITATIONAL_WAVES/CR_QUEUE.md` originally queued ringdown frequency
   and related gravitational-wave tests.
4. `21_GRAVITATIONAL_WAVES/GW_SUBSTRATE_FRAMING.md` states the carrier-wave
   hypothesis, including ringdown as the substrate-frequency frontier.
5. `CR003_RINGDOWN_FREQUENCY_IN_SUBSTRATE_UNITS` found both fundamental QNM
   components by substrate-expression search:
   `omega_R*M = 3/8` and `omega_I*M = R/(L - V) = 4/45`.
6. `CR004_SAM_VS_GR_DISCRIMINATION_MAP` classified the Schwarzschild QNM row
   as a future LISA discriminator and opened derivation work.
7. `CR005_THETA_CARRIER_OVERFLOW_AND_QNM_DERIVATION` sealed a derivation of
   the real component only and explicitly left the imaginary/damping component
   open as a future CR005b candidate.
8. `STUDY_NOTES_FOR_QNM_DERIVATION.md` states that damping is less crisp than
   the real part and suggests it likely requires the two ledger sides or
   unresolved inventory separately.

## Active, superseded, appealed, conflicting

- Active controlling real-frequency derivation: CR005 PASS.
- Active exploratory damping match: CR003 PASS, but exploratory/search grade.
- Active open boundary: CR005 result says the damping rate is not sealed as a
  first-principles derivation.
- No existing `CR005b_QNM_DAMPING_SUBSTRATE_DYNAMICS` folder exists.
- The older CR queue labels were superseded by executed CR003/CR004/CR005
  records. The new suffix `CR005b` follows the open item named by CR005.
- No conflicting active result fully seals the damping-shell derivation.

## Derivation existence check

The necessary expression already exists as an exploratory match in CR003:

```text
omega_I*M = R/(L - V) = R/(R^2 - d_hat^2) = 4/45
```

The required derivation does not already exist. CR005 explicitly excludes the
imaginary part from its sealed derivation and names it as open future work.

Therefore this CR is not a documentation promotion or a direct replay. It tests
whether the CR003 expression can be promoted to a source-role derivation:

```text
damping_shell = closed ledger - committed write cell = L - V
damping rate  = route radix / damping_shell = R/(L - V)
```

## Sealed premises

- `h_hat = 2`
- `d_hat = 3`
- `S = h_hat^d_hat = 8`
- `V = d_hat^d_hat = 27`
- `F = d_hat^(d_hat + 1) = 81`
- `R = h_hat^2*d_hat = 12`
- `R^2 = 144`
- `Theta = h_hat*d_hat^2 = 18`
- `L = h_hat*F = 162`
- `M = R^2 - Theta = 126`
- CR005 real-frequency derivation remains intact and is not retested.

## Candidate assumptions

- Damping is a loss/readout over the unresolved ledger shell, not propagation
  over writable capacity.
- The unresolved damping shell is `L - V`, closed ledger minus committed write
  cell.
- The numerator is `R`, the route radix, because damping is route-leak per
  route rather than dimension-propagation per spatial dimension.
- The identity `L - V = R^2 - d_hat^2` provides a second source-form check.

## External anchors and comparators

External comparator:

```text
Berti/Cardoso/Starinets 2009 Schwarzschild fundamental omega_I*M = 0.08896232
```

The comparator is reveal-only in this CR. It is quoted from CR003's source
chain and is not used to select or alter the formula.

No external dataset is downloaded. No external target file is opened by the
runner.

## Missing physics preserved

This CR does not claim a full substrate equation of motion for all QNM modes.
It tests one damping-shell selector for the fundamental Schwarzschild damping
coefficient. Higher modes, Kerr spin, memory effects, and a full dynamical
operator remain open.

## Opened scientific files

The machine-readable list and hashes are in `CR005b_SOURCE_MANIFEST.json`.
