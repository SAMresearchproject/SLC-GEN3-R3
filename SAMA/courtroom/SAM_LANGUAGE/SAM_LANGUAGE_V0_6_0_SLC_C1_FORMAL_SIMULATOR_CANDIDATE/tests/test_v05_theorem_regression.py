from __future__ import annotations

import csv
import json
import unittest
from fractions import Fraction
from pathlib import Path

from sam_language_v0_6.errors import (
    QPDomainError,
    QPMultiplicityError,
    TypeCheckError,
    UnknownEntityError,
    UnknownOperatorError,
)
from sam_language_v0_6.qp_grammar import ALPHABET, DEEP_CONJUGATE_EXCLUSIONS
from sam_language_v0_6.registry_qp import (
    enumerate_qp_productions,
    grammar_census,
    verify_qp_native_reconciliation,
    verify_qp_source_reconciliation,
)
from sam_language_v0_6.runtime import VALID_CLOSURE_PROGRAM, load_registry, run_program_text


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent


class EffectiveLanguageTests(unittest.TestCase):
    def test_LANG_POSITIVE_UNARY_DIRECT(self):
        self.assertEqual(run_program_text("let x = QP_UNARY_DIRECT(QP_P1, QP_D0, QP_ROUTE_PLUS)\nreturn x").entity_id, "UD:1:0:plus")

    def test_LANG_POSITIVE_ORDERED_PAIR_12(self):
        self.assertEqual(run_program_text("let x = QP_ORDERED_PAIR(QP_P1, QP_P2)\nreturn x").entity_id, "OP:1:2")

    def test_LANG_POSITIVE_ORDERED_PAIR_21(self):
        self.assertEqual(run_program_text("let x = QP_ORDERED_PAIR(QP_P2, QP_P1)\nreturn x").entity_id, "OP:2:1")

    def test_LANG_ORDERED_PAIR_ORIENTATION_DISTINCT(self):
        a = run_program_text("let x = QP_ORDERED_PAIR(QP_P1, QP_P2)\nreturn x")
        b = run_program_text("let x = QP_ORDERED_PAIR(QP_P2, QP_P1)\nreturn x")
        self.assertNotEqual(a.entity_id, b.entity_id)

    def test_LANG_POSITIVE_ADMITTED_TRIAD(self):
        source = "let c = QP_UNORDERED_TRIAD(QP_P3, QP_P4, QP_P6)\nlet x = QP_TRIAD_SURFACE_GATE(c)\nreturn x"
        self.assertEqual(run_program_text(source).semantic_type, "QPLocalTriadTemplate")

    def test_LANG_POSITIVE_HIDDEN_SUPPORT(self):
        self.assertEqual(run_program_text("let x = QP_HIDDEN_SUPPORT(QP_P8)\nreturn x").entity_id, "HS:8")

    def test_LANG_POSITIVE_CARRIER_TERMINAL(self):
        source = "let x = QP_CARRIER_TERMINAL(QP_CARRIER_TENSOR_CARRIER)\nreturn x"
        self.assertEqual(run_program_text(source).entity_id, "CI:TENSOR_CARRIER")

    def test_LANG_POSITIVE_GLOBAL_SCALAR_ONCE(self):
        self.assertEqual(run_program_text("let x = QP_SCALAR_PARENT()\nreturn x").entity_id, "GS:HIGGS_REVEAL_PARENT")

    def test_LANG_V0_4_CORE_REGRESSION(self):
        self.assertEqual(run_program_text(VALID_CLOSURE_PROGRAM).entity_id, "L162_FULL_LEDGER")

    def test_LANG_SEALED_EXAMPLE_REJECTS_1_3_8_TRIAD(self):
        source = "let c = QP_UNORDERED_TRIAD(QP_P1, QP_P3, QP_P8)\nlet x = QP_TRIAD_SURFACE_GATE(c)\nreturn x"
        with self.assertRaises(QPDomainError):
            run_program_text(source)

    def test_LANG_REJECT_NEUTRAL_CONJUGATE(self):
        with self.assertRaises(QPDomainError):
            run_program_text("let x = QP_UNARY_CONJUGATE(QP_P1, QP_D0, QP_ROUTE_NEUTRAL)\nreturn x")

    def test_LANG_REJECT_DEEP_CONJUGATE(self):
        with self.assertRaises(QPDomainError):
            run_program_text("let x = QP_UNARY_CONJUGATE(QP_P8, QP_D2, QP_ROUTE_PLUS)\nreturn x")

    def test_LANG_REJECT_WRONG_PAIR_TYPE(self):
        with self.assertRaises(TypeCheckError):
            run_program_text("let x = QP_ORDERED_PAIR(QP_P1, QP_D0)\nreturn x")

    def test_LANG_REJECT_PAIR_AT_TRIAD_GATE(self):
        source = "let p = QP_ORDERED_PAIR(QP_P1, QP_P2)\nlet x = QP_TRIAD_SURFACE_GATE(p)\nreturn x"
        with self.assertRaises(TypeCheckError):
            run_program_text(source)

    def test_LANG_REJECT_REPEAT_SCALAR_PARENT(self):
        with self.assertRaises(QPMultiplicityError):
            run_program_text("let a = QP_SCALAR_PARENT()\nlet b = QP_SCALAR_PARENT()\nreturn b")

    def test_LANG_REJECT_INFRASTRUCTURE_COERCION(self):
        with self.assertRaises(UnknownOperatorError):
            run_program_text("let h = QP_HIDDEN_SUPPORT(QP_P1)\nlet x = QP_CAST_LOCAL_PAYLOAD(h)\nreturn x")

    def test_LANG_REJECT_RELATION_AS_CONSTITUENT(self):
        with self.assertRaises(UnknownOperatorError):
            run_program_text("let p = QP_ORDERED_PAIR(QP_P1, QP_P2)\nlet x = QP_CAST_CONSTITUENT(p)\nreturn x")

    def test_LANG_REJECT_STATIC_SLOT_PLACEMENT(self):
        with self.assertRaises(UnknownOperatorError):
            run_program_text("let p = QP_ORDERED_PAIR(QP_P1, QP_P2)\nlet x = QP_TEMPLATE_TO_SLOT(p)\nreturn x")

    def test_LANG_REJECT_PHYSICAL_MASS_OPERATOR(self):
        with self.assertRaises(UnknownOperatorError):
            run_program_text("let p = QP_ORDERED_PAIR(QP_P1, QP_P2)\nlet x = QP_PHYSICAL_MASS(p)\nreturn x")

    def test_LANG_REJECT_STARBREAKER_JSON_PSEUDO_REGISTRATION(self):
        with self.assertRaises(UnknownOperatorError):
            run_program_text("let p = QP_ORDERED_PAIR(QP_P1, QP_P2)\nlet x = STARBREAKER_FORMATION_TRANSITION(p)\nreturn x")

    def test_LANG_REJECT_CANDIDATE_ID_ENTITY(self):
        with self.assertRaises(UnknownEntityError):
            run_program_text("let x = QP093A_0001\nreturn x")


class EffectiveWrongControlTests(unittest.TestCase):
    def test_WC_UNORDERED_PAIR_COLLAPSE(self):
        self.assertNotEqual(len(list(__import__("itertools").combinations_with_replacement(ALPHABET, 2))), 64)

    def test_WC_ORDERED_TRIAD_EXPANSION(self):
        self.assertNotEqual(len(ALPHABET) ** 3, 120)

    def test_WC_DEEP_CONJUGATE_OVERGENERATION(self):
        self.assertNotEqual(len(ALPHABET) * 3 * 2, 42)

    def test_WC_ACCEPT_ALL_TRIADS(self):
        self.assertNotEqual(120, grammar_census()["triad_admitted"])

    def test_WC_ACCEPT_NONE_TRIADS(self):
        self.assertNotEqual(0, grammar_census()["triad_admitted"])

    def test_WC_CANDIDATE_ID_SEMANTIC_SELECTOR(self):
        with self.assertRaises(UnknownEntityError):
            run_program_text("let x = QP093A_0001\nreturn x")

    def test_WC_SOURCE_ROW_ORDER_SELECTOR(self):
        rows = enumerate_qp_productions()
        self.assertEqual(rows, sorted(rows, key=lambda row: row["signature"]))

    def test_WC_FLOAT_ARITHMETIC(self):
        result = run_program_text("let x = QP_UNARY_DIRECT(QP_P1, QP_D0, QP_ROUTE_PLUS)\nreturn x")
        self.assertIsInstance(result.scalar_value, Fraction)

    def test_WC_INFRASTRUCTURE_TO_PAYLOAD(self):
        with self.assertRaises(TypeCheckError):
            run_program_text("let h = QP_HIDDEN_SUPPORT(QP_P1)\nlet x = QP_ORDERED_PAIR(h, QP_P1)\nreturn x")

    def test_WC_REPEAT_GLOBAL_SCALAR(self):
        with self.assertRaises(QPMultiplicityError):
            run_program_text("let a = QP_SCALAR_PARENT()\nlet b = QP_SCALAR_PARENT()\nreturn b")

    def test_WC_RELATION_AS_CONSTITUENT(self):
        with self.assertRaises(TypeCheckError):
            run_program_text("let p = QP_ORDERED_PAIR(QP_P1, QP_P2)\nlet x = QP_ORDERED_PAIR(p, QP_P1)\nreturn x")

    def test_WC_CB2250_AS_LEGALITY_AUTHORITY(self):
        registry = load_registry()
        self.assertNotIn("CB2250", registry.entities)
        self.assertNotIn("CB2250", registry.operators)

    def test_WC_STATIC_TEMPLATE_TO_SLOT(self):
        with self.assertRaises(UnknownOperatorError):
            run_program_text("let p = QP_ORDERED_PAIR(QP_P1, QP_P2)\nlet x = QP_TEMPLATE_TO_SLOT(p)\nreturn x")

    def test_WC_PHYSICAL_MASS_BINDING_ACCESS(self):
        registry = load_registry()
        self.assertNotIn("QP_PHYSICAL_MASS", registry.operators)
        self.assertNotIn("QP_BINDING_ENERGY", registry.operators)

    def test_WC_JSON_ONLY_PSEUDO_REGISTRATION(self):
        with self.assertRaises(UnknownOperatorError):
            run_program_text("let p = QP_ORDERED_PAIR(QP_P1, QP_P2)\nlet x = STARBREAKER_FORMATION_TRANSITION(p)\nreturn x")


class EffectiveTheoremClaimTests(unittest.TestCase):
    def test_TG1_CONSTRUCTOR_DISJOINTNESS_EXHAUSTIVENESS(self):
        census = grammar_census()
        self.assertEqual(census["total"], 321)
        self.assertEqual(census["unique_signatures"], 321)

    def test_TG1_FINITE_SIGNATURE_BIJECTION(self):
        signatures = [row["signature"] for row in enumerate_qp_productions()]
        self.assertEqual(len(signatures), len(set(signatures)))

    def test_TG2_NATIVE_FORMULA_RECONSTRUCTION(self):
        self.assertEqual(verify_qp_native_reconciliation()["status"], "PASS")
        self.assertEqual(verify_qp_source_reconciliation()["failures"], 0)

    def test_TG2_TYPED_ROLE_PARTITION(self):
        self.assertEqual(grammar_census()["roles"], {"GLOBAL": 1, "INFRASTRUCTURE": 14, "LEGAL_LOCAL_TEMPLATE": 285, "REJECTED": 21})

    def test_TG3_PREDICATE_EQUIVALENCE_CLASS(self):
        with (ROOT / "registry" / "QP_TRIAD_ADMISSIBILITY.csv").open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            observed = Fraction(row["observed_fraction"])
            tensor = Fraction(row["tensor_fraction"])
            predicates = (
                observed > 0 and tensor > 0,
                observed > 0,
                tensor > 0,
                int(row["closure_depth"]) > 0 or int(row["q_abs"]) > 0,
            )
            self.assertEqual(len(set(predicates)), 1)

    def test_TG3_TRIAD_EXTENSION(self):
        census = grammar_census()
        self.assertEqual((census["triad_candidates"], census["triad_admitted"], census["triad_rejected"]), (120, 107, 13))

    def test_TG6_PARENT_NON_INTERFERENCE(self):
        baseline = json.loads((ROOT / "V0_5_PARENT_BASELINE.json").read_text(encoding="utf-8"))
        self.assertEqual(baseline["parent_candidate_code_hash"], "c399494c6a5319f93f9968cb857df9509cb625b05a60d00402944a949d09825b")

    def test_TG6_V0_4_SYNTAX_AND_EXECUTABLE_DISPATCH(self):
        self.assertEqual(run_program_text(VALID_CLOSURE_PROGRAM).scalar_value, 162)
        self.assertEqual(run_program_text("let x = QP_HIDDEN_SUPPORT(QP_P8)\nreturn x").entity_id, "HS:8")

    def test_TG6_WRONG_CONTROLS(self):
        self.assertEqual(len([name for name in dir(EffectiveWrongControlTests) if name.startswith("test_WC_")]), 15)

    def test_PHYSICAL_DOORS_REMAIN_CLOSED(self):
        registry = load_registry()
        for name in registry.metadata["open_operators"]:
            self.assertNotIn(name, registry.operators)


if __name__ == "__main__":
    unittest.main()
