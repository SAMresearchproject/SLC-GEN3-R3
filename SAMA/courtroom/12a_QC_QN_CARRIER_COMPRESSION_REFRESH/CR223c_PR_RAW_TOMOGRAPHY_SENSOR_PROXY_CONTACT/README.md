# CR223c PR Raw Tomography & Sensor-Proxy Contact

CR223c is the first hardware-trajectory CR in the empirical-contact campaign.

Until raw shots are placed in raw/ with a matching raw/HASHES.txt, CR223c
stays in:

    CR223c_PIPELINE_SEALED__SELF_TEST_PASS__AWAITING_RAW_DATA

The self-test runs the complete pipeline on synthetic data manufactured by
the sealed CR223a M4 NV Lindblad. It validates that the analysis end-to-end
correctly resolves the precommitted crossing, calibrates a sensor proxy
matching tomography labels, and rejects zero-wait + no-decoherence controls.

Run: `pip install -r requirements.txt && python CR223c_runner.py`
