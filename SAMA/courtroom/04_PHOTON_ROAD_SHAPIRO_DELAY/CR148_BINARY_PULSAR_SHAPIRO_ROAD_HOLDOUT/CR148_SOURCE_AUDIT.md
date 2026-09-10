# CR148 Source Audit

## Internal Source Scope

Opened or queried:

- `04_PHOTON_ROAD_SHAPIRO_DELAY/README.md`
- `04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_result.md`
- `04_PHOTON_ROAD_SHAPIRO_DELAY/CR006_PHOTON_ROAD_SHAPIRO_EXTERNAL_CONTACT/CR006_PRECOMMIT.md`
- `04_PHOTON_ROAD_SHAPIRO_DELAY/CR147_GW170817_A_RELEASE_EM_ORIGIN_DIFFERENTIAL/CR147_result.md`
- `SAM_NATIVE_MASTER_FORMULA_V4_2.md`
- `SAM_NATIVE_ACTION_ENGINE_V4_2.md`
- `SAM_TESTING_RULES.md`
- `tools/run_sam_test.py`
- filled preflight report `artifacts/preflight_filled/PREFLIGHT_20260711_122410_no_script.md`

Formula confirmed:

```text
A(r) = r_s/r = 2GM/(c^2 r)
T_A^gamma = (1/c) integral A(r) ds
```

Branch 04 prior use checked only in existing CR006 and CR147 directories:

```text
patterns checked: J0737, binary pulsar, Double Pulsar, PSR
hits: none
```

The selected binary-pulsar system was therefore treated as not previously used
by SAM Branch 04 photon-road testing.

## External Source Scope

Primary selected paper:

```text
Kramer et al., Tests of general relativity from timing the double pulsar,
Science 314:97-102, 2006, arXiv:astro-ph/0609417.
```

Local source copies:

- `external_sources/astro-ph-0609417-eprint.tar.gz`
- `external_sources/astro-ph-0609417.pdf`
- `external_sources/astro-ph-0609417-src/ksm+06.tex`

Target readout lines were not opened before precommit. Non-target anchors were
read from `ksm+06.tex` lines 899-905 and 918-921.

## Firewall Status At Precommit

```text
sam_language_v0_3_consulted_during_development = false
sam_language_v0_3_candidate_hash_known_to_research_agent = false
sam_language_v0_3_incidental_exposure_detected = false
forbidden_source_paths_opened = false
queue_maintenance_performed_by_research_agent = false
forecast_generated = false
```

No SAM Language v0.3 source, registered contract, candidate implementation,
candidate expected output, candidate hash, forecast gate, or generalization
path was opened as a source for this CR.

