# CR211 - HH001 Content Verification Against Courtroom Data

Result: **CR211_PASS_HH001_CONTENT_VERIFICATION_AGAINST_COURTROOM_DATA__COURTROOM_COLUMNS_MATCH__REFERENCE_COLUMNS_FLAGGED__DIAGNOSTICS_PRESERVED**

Question: do the HH001 tables/PDF contents match the live Courtroom data they claim to use?

Verdict: the Courtroom-backed HH001 content matches Courtroom data row by row. The test also flags the HH001 embedded reference-data columns explicitly instead of treating them as CR119-derived.

Courtroom-backed matches:
- PARTICLE = CR119 proton + electron + neutron: 126/126
- ELEMENT = CR119 Z: 126/126
- symbols/names/frontier labels = CR119 reveal labels: 126/126
- GRAVITY = CR119 qA_total_primary: 126/126
- GRAVITON = CR119 tensor_carrier_support_primary = qA/8: 126/126
- all Courtroom-backed row checks: 126/126

SAM address/Fano checks:
- R=12, D=3, R^2=144, 2^D=8
- carrier cells=18; retained nonzero Fano cells=126
- Fano line XOR closure: 7/7

Reference-data columns flagged:
- MATTER: embedded atomic-weight table in HH001 builder, not CR119/Courtroom-native data.
- CLOCK: embedded stability rule in HH001 builder; Courtroom has partial context only, not a 126-row source.
- LIGHT: embedded wavelength table in HH001 builder, not Courtroom-native data.
- ACTION: embedded nuclear-spin table in HH001 builder, not Courtroom-native data.

Diagnostics preserved:
- ACTION residual = physical nuclear spin remains falsified/diagnostic: 1/102.
- per-element XOR binary closures remain diagnostic: 7/102 and 7/102.
- six-channel signatures are diagnostic only: XOR 101/126 distinct; SUM 120/126 distinct.

Wrong controls:
- 8/8 rejected.

Primary artifacts:
- `CR211_input_manifest.csv`
- `CR211_content_claims.csv`
- `CR211_row_verification.csv`
- `CR211_external_reference_columns.csv`
- `CR211_fano_algebra_checks.csv`
- `CR211_wrong_controls.csv`
- `CR211_checks.csv`
- `CR211_summary.json`
- `HASHES.txt`
