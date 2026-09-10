# CR223c PRECOMMIT - PR Raw Tomography & Sensor-Proxy Contact

## Scope

Open the first hardware-trajectory CR. Seal:

```text
1. precommitted time grid (units of T2):
       0.0
       0.01
       0.02
       0.025
       0.03
       0.035
       0.04
       0.05
       0.07
       0.1

2. tomography pipeline = CR223b Gell-Mann basis + PSD projection
3. sensor observable  = P_0 photoluminescence readout (NV native)
4. train/test split   = trial-disjoint, seeded
5. crossing extractor = linear interpolation between consecutive grid points (no curve fit)
6. success criteria   = CR223c_INPUTS.yaml
```

## Locked invariants

```text
A_side                                   = 1/24
tomo shots per Gell-Mann setting         = 5000
sensor shots per time point              = 50000
n_trials_train                           = 100
n_trials_test                            = 100
seed_train                               = 70260621
seed_test                                = 80260621
seed_controls                            = 90260621
sensor_balanced_accuracy_target          = 0.8
sensor_vs_tomography_max_grid_intervals  = 1
CR223a M4 reference (analytic root)      = 0.0289614682
inputs_yaml_sha256                       = 3192ef9a72aa664a2a19ceb7ffe5592f9c4cfbceb7531580261b99938eed31c3
```

## Pre-data state

```text
CR223c_PIPELINE_SEALED__SELF_TEST_PASS__AWAITING_RAW_DATA
```

The self-test runs the entire pipeline on synthetic data manufactured by the
sealed CR223a M4 NV Lindblad. Any change to the runner, inputs, criteria, or
sensor form between this precommit and raw-data arrival is a campaign stop.
