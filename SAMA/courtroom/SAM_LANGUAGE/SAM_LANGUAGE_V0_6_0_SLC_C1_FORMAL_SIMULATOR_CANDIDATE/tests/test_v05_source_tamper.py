from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from sam_language_v0_6.errors import ContractValidationError
from sam_language_v0_6.qp_native import default_data_dir, validate_packaged_sources
from sam_language_v0_6.runtime import load_registry


def flip_one_byte(path: Path) -> None:
    data = bytearray(path.read_bytes())
    index = next(i for i, value in enumerate(data) if value not in b"\r\n, \t")
    data[index] = ord("Z") if data[index] != ord("Z") else ord("Y")
    path.write_bytes(bytes(data))


class SourceTamperTests(unittest.TestCase):
    def fixture(self):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name) / "data"
        shutil.copytree(default_data_dir(), root)
        return temporary, root

    def test_grammar_registry_byte_tamper_fails_startup(self):
        temporary, root = self.fixture()
        self.addCleanup(temporary.cleanup)
        flip_one_byte(root / "QP_TRIAD_ADMISSIBILITY.csv")
        with self.assertRaises(ContractValidationError):
            load_registry(data_dir=root)

    def test_native_registry_byte_tamper_fails_startup(self):
        temporary, root = self.fixture()
        self.addCleanup(temporary.cleanup)
        flip_one_byte(root / "QP_TEMPLATE_NATIVE_SIGNATURES.csv")
        with self.assertRaises(ContractValidationError):
            load_registry(data_dir=root)

    def test_missing_registry_file_fails_startup(self):
        temporary, root = self.fixture()
        self.addCleanup(temporary.cleanup)
        (root / "QP_SOURCE_RECONCILIATION.csv").unlink()
        with self.assertRaises(ContractValidationError):
            load_registry(data_dir=root)

    def test_manifest_hash_substitution_fails_validation(self):
        temporary, root = self.fixture()
        self.addCleanup(temporary.cleanup)
        path = root / "QP_SOURCE_MANIFEST.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        key = next(iter(manifest["packaged_registry_hashes"]))
        manifest["packaged_registry_hashes"][key] = "0" * 64
        path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        with self.assertRaises(ContractValidationError):
            validate_packaged_sources(root)

    def test_untampered_fixture_validates(self):
        temporary, root = self.fixture()
        self.addCleanup(temporary.cleanup)
        self.assertEqual(validate_packaged_sources(root)["status"], "PASS")
        self.assertIn("QP_P8", load_registry(data_dir=root).entities)


if __name__ == "__main__":
    unittest.main()
