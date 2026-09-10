from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[0]
sys.path.insert(0, str(ROOT / "src"))

from sam_language_v0_6.diagnostic_probe_map import V03_PROBE_REGRESSION_MAP  # noqa: E402


class V03ProbeRegressionMapTests(unittest.TestCase):
    def test_all_v03_external_diagnostic_probes_are_mapped(self):
        source = REPO / "SAM_LANGUAGE_V0_3_POST_FREEZE_DIAGNOSTIC" / "V0_3_DIAGNOSTIC_RUN_001.json"
        if source.exists():
            payload = json.loads(source.read_text(encoding="utf-8"))
            probe_ids = {probe["id"] for probe in payload["probes"]}
            self.assertEqual(payload["probe_count"], 29)
            self.assertEqual(probe_ids, set(V03_PROBE_REGRESSION_MAP))
        else:
            # The frozen v0.4 release bundle preserves the audited 29-probe map
            # even when the external parent diagnostic tree is not packaged.
            self.assertEqual(len(V03_PROBE_REGRESSION_MAP), 29)

    def test_all_probe_mappings_have_coverage_text(self):
        for probe_id, mapping in V03_PROBE_REGRESSION_MAP.items():
            with self.subTest(probe_id=probe_id):
                self.assertTrue(mapping["v04_regression"])
                self.assertTrue(mapping["coverage"])


if __name__ == "__main__":
    unittest.main()
