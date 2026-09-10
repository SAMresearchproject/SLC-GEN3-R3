# QP050 - Private Symmetric Isotope Seed Mass Readout

## Preflight

```text
test_id = QP050
test_name = PRIVATE_SYMMETRIC_ISOTOPE_SEED_MASS_READOUT
test_type = FORWARD_MODEL_BUILD
new_forward_work = true
is_audit_or_retest = false
confirmation_or_double_check = false
if_audit_or_retest_reason = NOT_APPLICABLE
permission_required_before_run = false
public_repo_write = false
external_data_used = false
free_parameters_introduced = 0
```

## Result

```text
QP050_SYMMETRIC_ISOTOPE_SEED_MASS_SURFACE_EMITTED
```

QP050 emits the symmetric isotope seed mass surface:

```text
M_seed(Z) = floor(Z/2) * M_alpha + (Z mod 2) * M_deuteron
A_seed = 2Z
N_seed = Z
```

This is a baseline seed readout, not a final isotope-mass claim.

## Family Summary

| seed family | rows | A seed range | mass range MeV |
| --- | ---: | --- | --- |
| EVEN_Z_ALPHA_STACK_SEED | 58 | 8..236 | 7.451543e+03..2.198205e+05 |
| HELIUM_ALPHA_CLOSURE_SEED | 1 | 4..4 | 3.725771e+03..3.725771e+03 |
| HYDROGEN_PROTON_DEUTERON_SEED | 1 | 2..2 | 1.875576e+03..1.875576e+03 |
| ODD_Z_ALPHA_STACK_PLUS_RESIDUAL_SEED | 58 | 6..234 | 5.601347e+03..2.179703e+05 |

## Next Frontier

| frontier | rows | missing operator |
| --- | ---: | --- |
| NEUTRON_EXCESS_BINDING_DEPTH_SELECTOR | 118 | DeltaN(A_band,Z,seed_family) and binding-depth correction |
| A_BAND::A_LOCAL_NOT_PRESENT | 91 | band-specific neutron excess depth |
| A_BAND::A_SHARE_TO_QG_REORGANIZATION | 5 | band-specific neutron excess depth |
| A_BAND::A_SIDE_TO_A_SHARE_FUSION_ACCESS | 6 | band-specific neutron excess depth |
| A_BAND::BELOW_A_SIDE_COHERENT_FORMATION | 12 | band-specific neutron excess depth |
| A_BAND::QG_TO_WRITE_MIDPOINT_DENSE_CONTEXT | 4 | band-specific neutron excess depth |

## Key Fields

```text
seed_mass_rows_emitted = 118
observed_isotope_masses_used = false
free_parameters_introduced = 0
M_deuteron = 1.875575905532e+03
M_alpha = 3.725771283469e+03
next_frontier = QP051_PRIVATE_NEUTRON_EXCESS_BINDING_DEPTH_SELECTOR
```

## Interpretation

QP050 is the first isotope-layer mass surface, but it is deliberately the
baseline surface. It says every element has a native symmetric seed readout
built from alpha units and the deuteron residual. The remaining physical
question has sharpened:

```text
What selects neutron excess and binding depth above the N=Z seed?
```
