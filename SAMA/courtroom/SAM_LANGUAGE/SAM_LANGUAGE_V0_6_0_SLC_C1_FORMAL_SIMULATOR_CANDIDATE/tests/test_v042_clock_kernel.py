from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from sam_language_v0_6.errors import TypeCheckError  # noqa: E402
from sam_language_v0_6.runtime import run_program_text  # noqa: E402


class EarthOrbitClockKernelTests(unittest.TestCase):
    def source(self, name: str) -> str:
        return (ROOT / "examples" / name).read_text(encoding="utf-8")

    def test_cr005_calibration_matches_sealed_packet(self):
        result = run_program_text(self.source("cr005_gps_calibration.sam"))
        sealed = json.loads(
            (
                REPO_ROOT
                / "03_CLOCKS_AND_GPS"
                / "CR005_CLOCKS_AND_GPS_EXTERNAL_CONTACT"
                / "CR005_summary.json"
            ).read_text(encoding="utf-8")
        )["sam_row"]
        packet = result.result_payload

        field_map = {
            "A_ground": "A_ground",
            "A_orbit": "A_orbit",
            "orbit_speed_m_s": "gps_orbit_speed_m_s",
            "gravity_exact_us_day": "gravity_exact_us_day",
            "gravity_weak_us_day": "gravity_weak_us_day",
            "sr_exact_us_day": "sr_exact_us_day",
            "sr_weak_us_day": "sr_weak_us_day",
            "net_exact_us_day": "net_exact_us_day",
            "net_weak_us_day": "net_weak_us_day",
            "factory_frequency_hz": "factory_frequency_hz",
        }
        for actual_key, sealed_key in field_map.items():
            with self.subTest(field=actual_key):
                self.assertEqual(packet[actual_key], sealed[sealed_key])

        self.assertEqual(result.semantic_type, "EarthOrbitClockPacket")
        self.assertEqual(result.entity_id, "EARTH_ORBIT_CLOCK_PACKET_R26560000M")

    def test_declared_42164km_orbit_produces_new_packet(self):
        calibration = run_program_text(self.source("cr005_gps_calibration.sam"))
        result = run_program_text(self.source("declared_42164km_circular_orbit.sam"))
        packet = result.result_payload

        self.assertEqual(packet["orbit_radius_m"], 42164000.0)
        self.assertEqual(result.entity_id, "EARTH_ORBIT_CLOCK_PACKET_R42164000M")
        self.assertNotEqual(packet["net_exact_us_day"], calibration.result_payload["net_exact_us_day"])
        expected = {
            "A_orbit": 2.1037036519863726e-10,
            "orbit_speed_m_s": 3074.6662841276843,
            "gravity_exact_us_day": 50.99012412301818,
            "sr_exact_us_day": -4.544000375972246,
            "net_exact_us_day": 46.44612374704593,
            "factory_frequency_hz": 10229999.99450065,
        }
        for field, value in expected.items():
            with self.subTest(field=field):
                self.assertEqual(packet[field], value)
        self.assertAlmostEqual(
            packet["net_exact_us_day"],
            packet["gravity_exact_us_day"] + packet["sr_exact_us_day"],
            places=12,
        )

    def test_calibration_program_does_not_embed_expected_outputs(self):
        source = self.source("cr005_gps_calibration.sam")
        for expected_fragment in ("45.650919", "-7.213602", "38.437317", "10229999.995448"):
            self.assertNotIn(expected_fragment, source)

    def test_nonpositive_input_is_typed_failure(self):
        source = self.source("cr005_gps_calibration.sam").replace(
            "let orbit_radius = 26560000.0", "let orbit_radius = -1.0"
        )
        with self.assertRaises(TypeCheckError):
            run_program_text(source)

    def test_cli_emits_structured_packet(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(SRC)
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "sam_language_v0_6.cli",
                "run",
                str(ROOT / "examples" / "declared_42164km_circular_orbit.sam"),
            ],
            cwd=str(ROOT),
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["semantic_type"], "EarthOrbitClockPacket")
        self.assertEqual(payload["result_payload"]["orbit_radius_m"], 42164000.0)


if __name__ == "__main__":
    unittest.main()
