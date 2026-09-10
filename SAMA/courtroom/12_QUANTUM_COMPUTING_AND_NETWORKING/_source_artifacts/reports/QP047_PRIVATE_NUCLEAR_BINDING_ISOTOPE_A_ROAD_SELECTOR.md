# QP047 - Private Nuclear Binding and Isotope A-road Selector

## Preflight

```text
test_id = QP047
test_name = PRIVATE_NUCLEAR_BINDING_ISOTOPE_A_ROAD_SELECTOR
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
QP047_ELEMENT_A_ROAD_CONTEXT_LAYER_FILLED
```

QP047 fills the element layer where the current private table already has
SAM-native A-local formation context. It also carries forward the existing
deuteron and alpha-particle nuclear support bridges.

## A-road Band Summary

| A band | rows | symbols | meaning |
| --- | ---: | --- | --- |
| A_LOCAL_NOT_PRESENT | 91 | Be;B;F;Na;Al;P;Cl;Ar;K;Sc;Ti;V;Mn;Co;Cu;Ga;Ge;As;Se;Br;Kr;Rb;Y;Zr;Nb;Mo;Tc;Ru;Rh;Pd;Cd;In;Sb;Te;Cs;La;Ce;Pr;Nd;Pm;Eu;Gd;Tb;Dy;Ho;Er;Tm;Yb;Lu;Hf;Ta;W;Re;Os;Ir;Hg;Tl;Bi;Po;At;Rn;Fr;Ra;Ac;Pa;Np;Pu;Am;Cm;Bk;Cf;Es;Fm;Md;No;Lr;Rf;Db;Sg;Bh;Hs;Mt;Ds;Rg;Cn;Nh;Fl;Mc;Lv;Ts;Og | A-local value is not present in the atlas row |
| A_SHARE_TO_QG_REORGANIZATION | 5 | Ag;I;Xe;Sm;Pb | 1/12 <= A_local < 1/3; reorganization-heavy context |
| A_SIDE_TO_A_SHARE_FUSION_ACCESS | 6 | Si;S;Ca;Cr;Fe;Ni | 1/24 <= A_local < 1/12; fusion/write-access band |
| BELOW_A_SIDE_COHERENT_FORMATION | 12 | H;He;Li;C;N;O;Ne;Mg;Zn;Sr;Sn;Ba | A_local < 1/24; coherent formation context |
| QG_TO_WRITE_MIDPOINT_DENSE_CONTEXT | 4 | Pt;Au;Th;U | 1/3 <= A_local < 1/2; dense r-process/compact context |

## Nuclear Support Bridges

| composite | symbol | constituents | SAM mass MeV | reading |
| --- | --- | --- | ---: | --- |
| deuteron | D | proton;neutron | 1.875575905532e+03 | FILLED_NATIVE_NUCLEAR_SUPPORT_BRIDGE |
| alpha_particle | alpha | proton;proton;neutron;neutron | 3.725771283469e+03 | FILLED_NATIVE_NUCLEAR_SUPPORT_BRIDGE |

## Key Fields

```text
element_rows = 118
filled_A_local_context_rows = 27
route_context_present_A_local_open_rows = 91
nuclear_support_bridge_rows = 2
free_parameters_introduced = 0
observed_isotope_masses_used = false
observed_abundance_used_as_selector = false
next_frontier = QP048_PRIVATE_PHASE4_FREEZE_AND_VISUAL_PACKAGE
```

## Interpretation

This moves the periodic element table out of blank territory for the rows that
already carry SAM A-local context. It does not claim a complete isotope mass
predictor. The next missing piece is narrower now:

```text
given an element A-road formation band plus nuclear support bridge,
select the isotope mass/readout layer.
```
