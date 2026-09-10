# Test 7 — Input Schema

## density_matrices.csv (for `--mode analyze`)

One row per (run_id, time) pair. Required columns:

| column | type | notes |
|---|---|---|
| run_id | string | unique identifier per platform/run |
| platform | string | free text identifier (e.g., `nv_center_001`, `transmon_ibm_lima_q0`) |
| dimension | int | 2 or 3 |
| time | float | observation time |
| time_unit | string | free text (`us`, `ns`, `T2_units`, ...) |
| rho_real_flat | string | row-major flat real part, pipe-separated, length = `dimension^2` |
| rho_imag_flat | string | row-major flat imag part, pipe-separated, length = `dimension^2` |
| T1 | float | optional; blank if unknown |
| T2 | float | required for `t_over_T2` |
| notes | string | optional |

Row-major flatten order, 2x2:

```text
rho_real_flat = "rho00_real|rho01_real|rho10_real|rho11_real"
rho_imag_flat = "rho00_imag|rho01_imag|rho10_imag|rho11_imag"
```

3x3:

```text
rho_real_flat = "rho00|rho01|rho02|rho10|rho11|rho12|rho20|rho21|rho22"
```

(same for `rho_imag_flat`)

Each density matrix is validated:

- Hermiticity within `1e-8`
- Trace = 1 within `1e-8`
- Minimum eigenvalue `>= -1e-8`

A matrix failing validation is NOT silently repaired. Its row is flagged with
`matrix_valid = false` and one of: `NON_HERMITIAN, TRACE_NOT_ONE,
NEGATIVE_EIGENVALUE, BAD_FLAT_LENGTH, BAD_DIMENSION, PARSE_ERROR`.

## tomography_counts.csv (for `--mode counts`)

Counts mode is **NOT IMPLEMENTED** in this version. The runner will print
`COUNTS_MODE_NOT_IMPLEMENTED` and exit. Raw count reconstruction is reserved
for a later amendment.
