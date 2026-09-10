# CR017 Precommit

## Test ID

```text
CR017_DISTANCE_ROAD_TYPED_BRIDGE_CLOSURE
```

## Test Type

```text
Fresh Courtroom branch closure test.
Only local CR012-CR016 summaries may close this branch.
External G verdicts are not accepted as dependency replacements.
```

## Question

```text
Does the local 06 courtroom evidence close the typed distance-road bridge after
CR012-CR016?
```

## Frozen Closure Packet

```text
CR012 typed bridge = PASS
CR013 SN ledger = PASS
CR014 BAO ledger = PASS
CR015 independent SN/BAO lock = PASS
CR016 CMB acoustic ratio = PASS
CMB modal/polarization = OPEN_NOT_CLAIMED
```

## Wrong Controls

```text
missing_dependency
external_G_verdict_replaces_local_CR
smuggle_CMB_modal_closure
nonzero_new_parameter
```

## Rule-9 Line

```text
This closure test could have falsified: the 06 branch if any local CR dependency
failed, if a new parameter appeared, if CMB modal or polarization closure was
smuggled into the branch, or if a dependency was replaced by an external G
verdict instead of a local courtroom result.
```

