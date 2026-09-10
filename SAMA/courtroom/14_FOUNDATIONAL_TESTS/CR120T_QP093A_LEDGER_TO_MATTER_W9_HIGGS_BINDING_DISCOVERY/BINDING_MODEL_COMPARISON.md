# Frozen Binding Model Comparison

Candidate: `B3_SURFACE_EXCESS_REPLACES_82` with frozen training-only `gamma_surface=0.09121089246081573`. The candidate replaces `op_82pre`; it does not add a free parameter.

| Lane | n | CR274 RMS MeV | B3 RMS MeV | Delta B3-CR274 |
|---|---:|---:|---:|---:|
| CR261 held-out test | 20 | 3.017113068 | 4.071613571 | +1.054500503 |
| CR277 extended-only | 78 | 7.974144225 | 8.067445504 | +0.093301279 |
| CR277 whole observed | 118 | 6.672483502 | 6.828884165 | +0.156400663 |

Frozen validation status: **NO_FROZEN_BINDING_IMPROVEMENT**.

The typed zero-fee cleanup is numerically identical to CR274. W9 is not double-counted, Theta remains zero-fee, and QP093A-0299 remains a global reveal rather than a repeated isotope constituent.
