# QP007 - Private Role Operator Mass Closure Trial

Location: `D:\quantum_phase`

## Verdict

`QP007_PRIVATE_ROLE_OPERATOR_MASS_CLOSURE_TRIAL_BUILT`

QP007 takes the P1/P2 rows from QP006 and asks what native integer shift would
be required if an existing QGA076 meson role operator is used as the seed. It
does not use observed composite masses.

## Main Read

Best internal contact:

```text
pair = b<->c
surface = INTERACTION_COORDINATE_SURFACE
seed role = charged_kaon_D_b_square
required effective shift = 1.01267186772
integer shift delta = 0.0126718677232
```

A-share integer contacts found: `4`

## Trial Table

| Pair | Surface | Seed role | Required shift | Delta | Contact class |
| --- | --- | --- | ---: | ---: | --- |
| b<->c | INTERACTION_COORDINATE_SURFACE | charged_kaon_D_b_square | 1.01267186772 | 0.0126718677232 | INTEGER_SHIFT_A_SHARE_CONTACT |
| b<->s | CLOSURE_COMPLEMENT_SURFACE | neutral_kaon_color_complement | -3.97543352784 | 0.0245664721564 | INTEGER_SHIFT_A_SHARE_CONTACT |
| b<->t | INTERACTION_COORDINATE_SURFACE | charged_kaon_D_b_square | -1.04776672258 | -0.0477667225795 | INTEGER_SHIFT_A_SHARE_CONTACT |
| c<->s | CLOSURE_COMPLEMENT_SURFACE | charged_kaon_D_b_square | 2.94660883726 | -0.053391162742 | INTEGER_SHIFT_A_SHARE_CONTACT |
| b<->s | CONSTITUENT_SUM_SURFACE | neutral_kaon_color_complement | -4.1035263591 | -0.103526359102 | INTEGER_SHIFT_HALF_WINDOW_CONTACT |
| b<->t | CLOSURE_COMPLEMENT_SURFACE | charged_kaon_D_b_square | -4.34555200027 | -0.345552000272 | INTEGER_SHIFT_HALF_WINDOW_CONTACT |
| b<->c | CLOSURE_COMPLEMENT_SURFACE | charged_kaon_D_b_square | 2.35483810061 | 0.354838100611 | INTEGER_SHIFT_HALF_WINDOW_CONTACT |
| b<->s | INTERACTION_COORDINATE_SURFACE | neutral_kaon_color_complement | -0.546449056809 | 0.453550943191 | INTEGER_SHIFT_HALF_WINDOW_CONTACT |
| b<->c | CONSTITUENT_SUM_SURFACE | charged_kaon_D_b_square | 0.53299845439 | -0.46700154561 | INTEGER_SHIFT_HALF_WINDOW_CONTACT |
| c<->s | CONSTITUENT_SUM_SURFACE | charged_kaon_D_b_square | 2.52680645494 | -0.473193545061 | INTEGER_SHIFT_HALF_WINDOW_CONTACT |
| b<->t | CONSTITUENT_SUM_SURFACE | charged_kaon_D_b_square | -4.48526709696 | -0.48526709696 | INTEGER_SHIFT_HALF_WINDOW_CONTACT |
| c<->s | INTERACTION_COORDINATE_SURFACE | charged_kaon_D_b_square | 4.5126055081 | -0.487394491903 | INTEGER_SHIFT_HALF_WINDOW_CONTACT |

## Counts

```text
priority rows used = 4
trial rows = 12
contact class counts = {'INTEGER_SHIFT_A_SHARE_CONTACT': 4, 'INTEGER_SHIFT_HALF_WINDOW_CONTACT': 8}
surface counts = {'INTERACTION_COORDINATE_SURFACE': 4, 'CLOSURE_COMPLEMENT_SURFACE': 4, 'CONSTITUENT_SUM_SURFACE': 4}
```

## Next Frontier

`QP008_PRIVATE_HEAVY_ROLE_SHIFT_SELECTOR`

QP008 should select among the internal surfaces and integer shifts using only
SAM-native route class, charge class, and A-share contact.

Generated at UTC: `2026-06-07T02:40:05.389747+00:00`
