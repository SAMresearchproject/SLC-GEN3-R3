# CR224 Precommit - Zero-Free-Parameter SOB Row Engine

## Task

Build a truly zero-free-parameter multi-tier engine that produces 126 SOB rows
from SAM constants only, with card-facing fields corresponding to the visible
PNG layout.

## Construction Boundary

Allowed construction inputs:

```text
R = 12
D = 3
alpha_H = 2
split = 2^D = 8
native_capacity = R^2 * (1 - 2^-D) = 126
proton_qA = 145/2
electron_qA = 145/96
neutron_qA = 1/8
kappa_floor = 7117/768
neutron_G_unit = 1/64
```

Allowed native generation:

```text
Z = 1..126
N = Z + floor(Z * (radix_cycle - 1) / R)
A = Z + N
P = Zp + Nn + Ze
quark address = (2Z+N)u + (Z+2N)d + Ze
G(P) = Z * kappa_floor + (N-Z)/64
GR(P) = 8G(P)
retained = 7G(P)
```

Forbidden construction inputs:

- element cards / PNG values
- known names (`Gold`)
- known symbols (`Au`)
- measured mass (`196.967`)
- physical CLOCK labels (`stable`)

These may appear only as blank/reveal-status fields.

## Planned Outputs

- `CR224_declared_constants.csv`
- `CR224_tier_contract.csv`
- `CR224_sob_rows_126.csv`
- `CR224_field_provenance.csv`
- `CR224_png_field_reconciliation_Z079.csv`
- `CR224_verification_against_CR222.csv`
- `CR224_gold_like_native_card_row_Z079.json`
- `CR224_checks.csv`
- `CR224_summary.json`
- `CR224_result.md`
- `HASHES.txt`

