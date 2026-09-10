# CR120M Eight-Plus-One Binding-Transfer Source Gate

record_id: `CR120M_EIGHT_PLUS_ONE_BINDING_TRANSFER_SOURCE_GATE`  
execution_status: `CLEAN`  
mathematical_verdict: `BOUNDARY`  
result_class: `STRUCTURAL_RESEARCH_BOUNDARY`  
scientific_pass_claimed: `false`  
disposition: `BOUNDARY_BINDING_PANEL_PRESENT_P189_ISOTOPE_MAPPING_NOT_INSTALLED`

## Direct result

The proposal was run through its first load-bearing gate. The registered
binding baseline and a broader residual panel are present, but the required
identity-preserving isotope-to-QP093A `p=1,8,9` map is not installed.

```text
AU197 sealed residual                         3.718275 MeV
AU197 replay performed                       no
CR277 representative-isotope rows            126
CR277 observed binding rows                   118
QP094A isotope-closure rows                   214
qualifying matched p1/p8/p9 isotope records   0
feature C_i constructible                     no
MeV coupling fit allowed                      no
held-out binding comparison allowed           no
```

## What exists

The AU197 packet remains sealed at:

```text
B_u_base_MeV                    27.421477
operator_debit_MeV               0.000000
B_u_final_MeV                  27.421477
B_u_obs_MeV                    31.139752
residual_obs_minus_final_MeV    3.718275
```

CR277 supplies 118 observed representative-isotope residuals and preserves
its historical PASS. QP094A supplies 214 isotope-closure records.

## Decisive mapping readout

QP094A's installed component selectors are:

| role | QP093A id | route |
|---|---|---|
| proton | `QP093A-0115` | `color_triad[1+1+1]` |
| neutron | `QP093A-0003` | `neutral_single_write[p=1,g=0]` |
| electron | `QP093A-0002` | `minus_single_write[p=1,g=0]` |

Those records support proton/neutron/electron counts. They do not name
matched p1, p8, and p9 nuclear structures, typed signs, or multiplicities for
any isotope. The complete QP094A isotope catalog contains zero qualifying
matched-packet records.

CR120K remains useful structural context, but its own controlling boundary is
`physical_mapping = OPEN_NOT_INSTALLED`. Its exact `100 * 162 = 16200`
relation cannot supply the missing nuclear map.

## Binding verdict

The proposed dimensionless `1/9` excess cannot yet be converted into an
isotope feature `C_i`, much less an MeV correction. Fitting a coupling now
would require choosing eligibility or multiplicity from the observed binding
targets, which is the proposal's target-leakage wrong control.

This is therefore a clean, informative boundary—not a validation of the
mechanism and not a negative verdict on a future properly mapped test.

## Single next install

Supply an observation-blind isotope-to-QP093A mapping that, for every isotope,
lists distinct matched p1/p8/p9 candidate ids, multiplicities, signs,
unmatched cases, and provenance. Once that source exists, the feature,
holdout splits, conventional controls, and fit threshold can be precommitted
without touching AU197.
