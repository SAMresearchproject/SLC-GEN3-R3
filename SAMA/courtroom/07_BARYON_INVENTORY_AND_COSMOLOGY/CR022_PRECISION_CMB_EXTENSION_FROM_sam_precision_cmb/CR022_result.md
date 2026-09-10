# CR022 Precision-CMB Extension from sam_precision_cmb

## Verdict

```text
CR022_BOUNDARY_PASS_PRECISION_CMB_EXTENSION
```

## Key Packet

```text
A_s_native = 2.1262624258595048e-09
n_s_native = 0.9646322348684677
tau_native = 0.05445888635899759
REVEAL003 primary high-l delta = 0.012560524139317025
REVEAL003 imported-trio high-l delta = 3.1875955103627333e-05
r_d = 147.09353447852072 Mpc
theta_star_100 = 1.0411066266105615
route_status = CONDITIONAL_IMPORTED_RECOMBINATION_TRANSPORT_FROZEN
```

## Scope Boundary

```text
Scoped precision-CMB extension only. Imported-trio control remains closer to official Planck theory; recombination/acoustic-ruler bridge remains boundary-scoped.
```

## Pass Conditions

| condition | pass |
|---|---:|
| fixed_density_has_Omega_b | true |
| C010_precomparison_firewall | true |
| C011_As_native_precomparison | true |
| C012_ns_native_precomparison | true |
| C013_tau_native_precomparison | true |
| C014_prediction_sealed | true |
| C015_wrong_controls_frozen | true |
| TRIAD_lockbox_complete | true |
| REVEAL_no_parameter_fit | true |
| imported_trio_closer_than_primary | true |
| BAO002_recombination_boundary_preserved | true |
