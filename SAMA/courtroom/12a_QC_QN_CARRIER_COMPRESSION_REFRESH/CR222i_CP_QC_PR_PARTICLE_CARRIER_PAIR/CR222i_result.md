# CR222i CP/QC PR Particle-Carrier Pair Result

**Result class:** `CR222i_PASS_CP_QC_PR_PARTICLE_CARRIER_PAIR__QP093A_0002_PLUS_QP093A_0301_CONTROL_0018`

**Checks:** 23/23

**CR222i_particle_carrier_roster.csv SHA-256:** `eccba1b1a30e4656661aa2dbd9c02ee0362d8969ff1be84fb35f45103e870b1a`

## Verdict

CR222i locks the strongest lab-facing particle-carrier pair for CP/QC Paul
Revere work:

```text
QP093A-0002 + QP093A-0301
```

The selected roles are:

```text
QP093A-0002 = negative fermion write, p=1, qA/T/W = 1.510416667 / 0.188802083 / 1.321614583
QP093A-0301 = ROAD_LIGHT_CARRIER, p=1, M=qA=T=W=0
QP093A-0018 = split control, qA/T/W = 1 / 0.125 / 0.875
QP093A-0300 = tensor witness/floor, not transmitted payload
```

The successful trial state is:

```text
PARTICLE_CARRIER_PR_PAIR_BOUND -> WARNING_TRANSMISSION_ALLOWED
```

This keeps the campaign architecture clean: photon-road route for preparation,
tomography, and warning transmission; matter row for the write split; tensor
carrier as the predicted witness/floor.
