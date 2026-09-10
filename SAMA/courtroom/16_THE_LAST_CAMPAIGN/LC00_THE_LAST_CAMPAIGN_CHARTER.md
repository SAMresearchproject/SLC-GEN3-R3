# LC00 - The Last Campaign Charter

## Question

With the latest promotion of the locked primitive stack, do all downstream SAM
branches replay from the theorem-grade primitive stack without mutation?

## Locked Primitive Stack

The campaign begins from the following locked stack:

- `alpha_H = 2`
- `R = 12`
- `D = 3`
- `A0 = 1/(pi*R)`
- `R^2 = 144`
- `split fraction = 2^-D = 1/8`
- `retained side = 7/8`
- `carrier side = 1/8`
- `bounce lift = D^2/2^D = 9/8`
- `resolved half-bounce = D^2/2^(D+1) = 9/16`
- `surface debit = D^2/R = 0.75`

## Pass Condition

All downstream branches must replay with:

- no formula mutation
- no constant mutation
- no target-value substitution
- no row deletion
- no retroactive relabeling
- no hidden correction term

Any downstream PASS that requires changing a primitive, changing a formula,
deleting a row, substituting a target value, or relabeling a failed output is
not a replay; it is a mutation.

## Replay Lanes

The Last Campaign will run one lane at a time:

- `LC02` - Higgs closed form
- `LC03` - qA / ledger compression / gravity-as-A update
- `LC04` - particle mass-chain table
- `LC05` - periodic/isotope vault
- `LC06` - baryon and matter inventory
- `LC07` - SN/BAO distance road
- `LC08` - halo/PBH inventory lane
- `LC09` - quantum pair-write / Born-rule lane
- `LC10` - quantum information thresholds
- `LC11` - black-hole/horizon thermodynamic lane

## Wrong Controls

The standing wrong controls are registered in `LC01_wrong_controls.csv`.
Lane-specific tests may add sharper controls, but they may not remove these.

## Discipline

`LC01` starts the campaign by locking the primitive stack, source chain, wrong
controls, and lane register. It does not claim the downstream lanes have already
replayed. Each later lane must earn its own result under the locked stack.
