# CR223d PR Real-Time Warning Contact

Streams sensor readings from CR223c_HF simulator and emits a PR warning
only when packet checksum (162), G_protocol (1), and sensor-proxy
confidence (>= P_ALARM=0.95) all close in the same sample. Wrong controls
verify gate-blocking under corrupted packets, G_protocol=0, and shuffled
sensor streams.

Run: `pip install -r requirements.txt && python CR223d_runner.py`
