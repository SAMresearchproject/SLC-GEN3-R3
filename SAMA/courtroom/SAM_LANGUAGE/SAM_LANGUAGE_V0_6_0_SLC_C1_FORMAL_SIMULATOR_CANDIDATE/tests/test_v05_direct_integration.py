from __future__ import annotations

import concurrent.futures
import importlib.util
import json
import os
import subprocess
import sys
import unittest
from fractions import Fraction
from pathlib import Path

import sam_language_v0_6.evaluator as evaluator_module
import sam_language_v0_6.parser as parser_module
import sam_language_v0_6.runtime as runtime_module
from sam_language_v0_6.errors import QPMultiplicityError
from sam_language_v0_6.registry_qp import (
    enumerate_qp_productions,
    inspect_qp_production,
    verify_qp_native_reconciliation,
)
from sam_language_v0_6.runtime import (
    entity_trace,
    load_registry,
    registry_payload,
    run_program_text,
    sources_for_operator,
)


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
IMPL = SRC / "sam_language_v0_6"


def implementation_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in sorted(IMPL.glob("*.py")))


class DirectIntegrationTests(unittest.TestCase):
    def test_DIRECT_001_ONE_CORE_RUNTIME(self):
        self.assertIs(parser_module.parse_program, runtime_module.parse_program)
        self.assertIs(evaluator_module.check_program, runtime_module.check_program)
        self.assertIs(evaluator_module.execute_checked, runtime_module.execute_checked)
        self.assertIs(evaluator_module.run_program_text, runtime_module.run_program_text)

    def test_DIRECT_002_NO_QP_TEXT_DISPATCH(self):
        forbidden = "if " + '"QP_"' + " in source_text"
        self.assertNotIn(forbidden, implementation_text())

    def test_DIRECT_003_NO_SYS_PATH_INJECTION(self):
        self.assertNotIn("sys.path" + ".insert", implementation_text())

    def test_DIRECT_004_NO_SIDECAR_IMPORT(self):
        text = implementation_text()
        forbidden = "sam_" + "qp_particle_grammar_v1"
        self.assertNotIn("import " + forbidden, text)
        self.assertNotIn("from " + forbidden, text)

    def test_DIRECT_005_NO_UI_DEPENDENCY(self):
        text = implementation_text().lower()
        for token in ("streamlit", "flask", "fastapi", "browser", "localhost", "127.0.0.1"):
            self.assertNotIn(token, text)

    def test_DIRECT_006_CLEAN_WHEEL_INSTALL(self):
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('sam = "sam_language_v0_6.cli:main"', pyproject)
        self.assertIn('sam_language_v0_6 = ["data/*.json", "data/*.csv", "data/*.bnf", "data/*.md"]', pyproject)
        self.assertNotIn("dependencies =", pyproject)

    def test_DIRECT_007_MIXED_CORE_QP_PROGRAM(self):
        result = run_program_text((ROOT / "examples" / "mixed_core_qp.sam").read_text(encoding="utf-8"))
        operators = [row["operator"] for row in result.trace if row.get("stage") == "typed_execution_plan"]
        self.assertEqual(operators, ["RESOLVE", "QP_ORDERED_PAIR", "PROMOTE_VOLUME", "QP_UNORDERED_TRIAD", "QP_TRIAD_SURFACE_GATE", "PROMOTE_FACE"])
        self.assertNotIn("lane", json.dumps(result.as_dict()).lower())

    def test_DIRECT_008_CORE_OPERATOR_AFTER_QP_OPERATOR(self):
        source = "let p = QP_ORDERED_PAIR(QP_P8, QP_P1)\nlet w = RESOLVE(S8_BINARY_SURFACE, B_CONTACT_OPERATOR, X1_AXIS_SELF_CHANNEL)\nlet v = PROMOTE_VOLUME(w, D3_DIMENSION)\nreturn v"
        self.assertEqual(run_program_text(source).entity_id, "V27_VOLUME_CONTAINER")

    def test_DIRECT_009_QP_OPERATOR_AFTER_CORE_OPERATOR(self):
        source = "let w = RESOLVE(S8_BINARY_SURFACE, B_CONTACT_OPERATOR, X1_AXIS_SELF_CHANNEL)\nlet p = QP_ORDERED_PAIR(QP_P8, QP_P1)\nreturn p"
        self.assertEqual(run_program_text(source).entity_id, "OP:8:1")

    def test_DIRECT_010_EXACT_RATIONAL_SERIALIZATION(self):
        result = run_program_text("let x = QP_UNARY_DIRECT(QP_P1, QP_D0, QP_ROUTE_PLUS)\nreturn x")
        self.assertEqual(result.scalar_value, Fraction(5, 4))
        self.assertEqual(result.as_dict()["scalar_value"], {"exact": "5/4", "decimal": 1.25})

    def test_DIRECT_011_DYNAMIC_ID_DETERMINISM(self):
        first = run_program_text("let x = QP_UNORDERED_TRIAD(QP_P6, QP_P3, QP_P4)\nreturn x")
        second = run_program_text("let x = QP_UNORDERED_TRIAD(QP_P4, QP_P6, QP_P3)\nreturn x")
        self.assertEqual(first.entity_id, second.entity_id)
        self.assertEqual(first.entity_id, "UT:3+4+6")

    def test_DIRECT_012_PROGRAM_STATE_ISOLATION(self):
        source = "let x = QP_SCALAR_PARENT()\nreturn x"
        self.assertEqual(run_program_text(source).entity_id, "GS:HIGGS_REVEAL_PARENT")
        self.assertEqual(run_program_text(source).entity_id, "GS:HIGGS_REVEAL_PARENT")
        with self.assertRaises(QPMultiplicityError):
            run_program_text("let a = QP_SCALAR_PARENT()\nlet b = QP_SCALAR_PARENT()\nreturn b")

    def test_DIRECT_013_PARALLEL_CONTEXT_ISOLATION(self):
        source = "let x = QP_SCALAR_PARENT()\nreturn x"
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda _: run_program_text(source).entity_id, range(24)))
        self.assertEqual(results, ["GS:HIGGS_REVEAL_PARENT"] * 24)

    def test_DIRECT_014_OPERATOR_SOURCE_INSPECTION(self):
        payload = sources_for_operator("QP_ORDERED_PAIR")
        self.assertEqual(payload["operator_id"], "QP_ORDERED_PAIR")
        self.assertTrue(payload["sources"])
        self.assertEqual(payload["semantic_scope"], "STRUCTURAL_GRAMMAR")

    def test_DIRECT_015_PRODUCTION_INSPECTION(self):
        payload = inspect_qp_production("UT:1+3+8")
        self.assertEqual(payload["production"]["semantic_type"], "QPRejectedConstruction")
        self.assertFalse(payload["ordinary_gate_executable"])

    def test_DIRECT_016_NATIVE_SIGNATURE_LOOKUP(self):
        sources = [
            "let p = QP_UNARY_DIRECT(QP_P1, QP_D0, QP_ROUTE_PLUS)",
            "let p = QP_UNARY_CONJUGATE(QP_P1, QP_D0, QP_ROUTE_PLUS)",
            "let p = QP_ORDERED_PAIR(QP_P1, QP_P2)",
            "let p = QP_UNORDERED_TRIAD(QP_P3, QP_P4, QP_P6)",
            "let c = QP_UNORDERED_TRIAD(QP_P3, QP_P4, QP_P6)\nlet p = QP_TRIAD_SURFACE_GATE(c)",
            "let p = QP_HIDDEN_SUPPORT(QP_P8)",
            "let p = QP_CARRIER_TERMINAL(QP_CARRIER_TENSOR_CARRIER)",
            "let p = QP_SCALAR_PARENT()",
            "let p = QP_EXPLICIT_CONTROL(QP_CONTROL_DIRECT_QA_AS_MASS)",
        ]
        for prefix in sources:
            with self.subTest(prefix=prefix):
                result = run_program_text(prefix + "\nlet n = QP_NATIVE_SIGNATURE(p)\nreturn n")
                self.assertEqual(result.semantic_type, "QPNativeSignature")
                self.assertIn("canonical_signature", result.result_payload)

    def test_DIRECT_017_NATIVE_SOURCE_RECONCILIATION(self):
        result = verify_qp_native_reconciliation()
        self.assertEqual((result["status"], result["rows"]), ("PASS", 321))

    def test_DIRECT_018_RUNTIME_REFERENCE_ENUMERATOR_MATCH(self):
        path = ROOT / "tools" / "reference_qp_enumerator.py"
        spec = importlib.util.spec_from_file_location("direct_reference_enumerator", path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        self.assertEqual(enumerate_qp_productions(), module.enumerate_reference(ROOT / "registry"))

    def test_DIRECT_019_NO_GLOBAL_REGISTRY_MUTATION(self):
        before = registry_payload()
        enumerate_qp_productions()
        run_program_text("let x = QP_ORDERED_PAIR(QP_P1, QP_P2)\nreturn x")
        after = registry_payload()
        self.assertEqual(before, after)

    def test_DIRECT_020_NO_RAW_TRACEBACK(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(SRC)
        proc = subprocess.run(
            [sys.executable, "-m", "sam_language_v0_6.cli", "run", str(ROOT / "examples" / "invalid_physical_mass.sam")],
            cwd=str(ROOT),
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertNotIn("Traceback", proc.stderr)
        self.assertEqual(json.loads(proc.stderr)["error"], "UnknownOperatorError")


if __name__ == "__main__":
    unittest.main()
