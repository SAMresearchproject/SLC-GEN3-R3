from __future__ import annotations

import unittest

from sam_language_v0_6.errors import (
    AuthorityError,
    QPDomainError,
    QPMultiplicityError,
    TypeCheckError,
    UnknownEntityError,
    UnknownOperatorError,
)
from sam_language_v0_6.runtime import load_registry, run_program_text


class DomainAndTypeBoundaryTests(unittest.TestCase):
    def test_neutral_conjugate_rejected(self):
        with self.assertRaises(QPDomainError):
            run_program_text("let x = QP_UNARY_CONJUGATE(QP_P1, QP_D0, QP_ROUTE_NEUTRAL)\nreturn x")

    def test_every_deep_conjugate_exclusion_rejected(self):
        for p in (8, 9, 12):
            for route in ("PLUS", "MINUS"):
                with self.subTest(p=p, route=route), self.assertRaises(QPDomainError):
                    run_program_text(f"let x = QP_UNARY_CONJUGATE(QP_P{p}, QP_D2, QP_ROUTE_{route})\nreturn x")

    def test_wrong_pair_type_rejected(self):
        with self.assertRaises(TypeCheckError):
            run_program_text("let x = QP_ORDERED_PAIR(QP_P1, QP_D1)\nreturn x")

    def test_pair_to_triad_gate_rejected(self):
        with self.assertRaises(TypeCheckError):
            run_program_text("let p = QP_ORDERED_PAIR(QP_P1, QP_P2)\nlet x = QP_TRIAD_SURFACE_GATE(p)\nreturn x")

    def test_rejected_triad_gate_rejected(self):
        with self.assertRaises(QPDomainError):
            run_program_text("let c = QP_UNORDERED_TRIAD(QP_P1, QP_P3, QP_P8)\nlet x = QP_TRIAD_SURFACE_GATE(c)\nreturn x")

    def test_outside_alphabet_depth_and_route_rejected_at_resolution(self):
        for source in (
            "let x = QP_UNARY_DIRECT(QP_P5, QP_D0, QP_ROUTE_PLUS)\nreturn x",
            "let x = QP_UNARY_DIRECT(QP_P1, QP_D3, QP_ROUTE_PLUS)\nreturn x",
            "let x = QP_UNARY_DIRECT(QP_P1, QP_D0, QP_ROUTE_OTHER)\nreturn x",
        ):
            with self.subTest(source=source), self.assertRaises(UnknownEntityError):
                run_program_text(source)


class MultiplicityAndCoercionBoundaryTests(unittest.TestCase):
    def test_repeat_scalar_parent_in_one_program_rejected(self):
        with self.assertRaises(QPMultiplicityError):
            run_program_text("let a = QP_SCALAR_PARENT()\nlet b = QP_SCALAR_PARENT()\nreturn b")

    def test_infrastructure_as_partition_rejected(self):
        with self.assertRaises(TypeCheckError):
            run_program_text("let h = QP_HIDDEN_SUPPORT(QP_P8)\nlet x = QP_ORDERED_PAIR(h, QP_P1)\nreturn x")

    def test_relation_as_constituent_rejected(self):
        with self.assertRaises(TypeCheckError):
            run_program_text("let p = QP_ORDERED_PAIR(QP_P8, QP_P1)\nlet x = QP_UNORDERED_TRIAD(p, QP_P1, QP_P2)\nreturn x")

    def test_global_as_partition_rejected(self):
        with self.assertRaises(TypeCheckError):
            run_program_text("let g = QP_SCALAR_PARENT()\nlet x = QP_ORDERED_PAIR(g, QP_P1)\nreturn x")

    def test_static_slot_placement_rejected(self):
        source = "let u = QP_UNARY_DIRECT(QP_P1, QP_D0, QP_ROUTE_PLUS)\nINSERT_LEDGER_ROW(u)\nreturn u"
        with self.assertRaises(AuthorityError):
            run_program_text(source)

    def test_same_scalar_cross_domain_assertion_rejected(self):
        source = "let q = QP_P8\nassert q == S8_BINARY_SURFACE\nreturn q"
        with self.assertRaises(AuthorityError):
            run_program_text(source)

    def test_candidate_id_entity_rejected(self):
        with self.assertRaises(UnknownEntityError):
            run_program_text("let x = QP093A_0001\nreturn x")

    def test_cb2250_legality_authority_rejected(self):
        with self.assertRaises(UnknownEntityError):
            run_program_text("let x = CB2250\nreturn x")


class OpenOperatorBoundaryTests(unittest.TestCase):
    def test_all_open_operators_are_documented_and_unregistered(self):
        registry = load_registry()
        self.assertTrue(registry.metadata["open_operators"])
        for operator in registry.metadata["open_operators"]:
            with self.subTest(operator=operator):
                self.assertNotIn(operator, registry.operators)

    def test_physical_mass_operator_rejected(self):
        with self.assertRaises(UnknownOperatorError):
            run_program_text("let u = QP_UNARY_DIRECT(QP_P1, QP_D0, QP_ROUTE_PLUS)\nlet x = QP_PHYSICAL_MASS(u)\nreturn x")

    def test_binding_operator_rejected(self):
        with self.assertRaises(UnknownOperatorError):
            run_program_text("let u = QP_UNARY_DIRECT(QP_P1, QP_D0, QP_ROUTE_PLUS)\nlet x = QP_BINDING_ENERGY(u)\nreturn x")

    def test_starbreaker_transition_rejected(self):
        with self.assertRaises(UnknownOperatorError):
            run_program_text("let u = QP_UNARY_DIRECT(QP_P1, QP_D0, QP_ROUTE_PLUS)\nlet x = STARBREAKER_FORMATION_TRANSITION(u)\nreturn x")

    def test_no_open_operator_has_an_evaluator(self):
        registry = load_registry()
        self.assertFalse(set(registry.metadata["open_operators"]) & set(registry.operators))


if __name__ == "__main__":
    unittest.main()
