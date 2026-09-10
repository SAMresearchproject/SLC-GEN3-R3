from __future__ import annotations

import importlib.util
import itertools
import json
import unittest
from fractions import Fraction
from pathlib import Path

from sam_language_v0_6.errors import QPDomainError
from sam_language_v0_6.qp_grammar import (
    ALPHABET,
    CARRIER_NATIVE,
    CONTROL_NAMES,
    DEEP_CONJUGATE_EXCLUSIONS,
    DEPTHS,
    ROUTES,
    hidden_support,
    ordered_pair,
    unary_native,
    unordered_triad_candidate,
)
from sam_language_v0_6.qp_native import load_native_index, native_packet
from sam_language_v0_6.registry_qp import (
    enumerate_qp_productions,
    grammar_census,
    inspect_qp_production,
    load_triad_allowed,
    verify_qp_native_inverse,
    verify_qp_native_reconciliation,
    verify_qp_source_reconciliation,
)
from sam_language_v0_6.runtime import run_program_text


ROOT = Path(__file__).resolve().parents[1]


class ExhaustiveConstructorTests(unittest.TestCase):
    def test_all_72_direct_unaries_execute_with_exact_formula(self):
        seen = set()
        for p, depth, route in itertools.product(ALPHABET, DEPTHS, ROUTES):
            source = f"let x = QP_UNARY_DIRECT(QP_P{p}, QP_D{depth}, QP_ROUTE_{route.upper()})\nreturn x"
            result = run_program_text(source)
            seen.add(result.entity_id)
            self.assertEqual(result.entity_id, f"UD:{p}:{depth}:{route}")
            self.assertEqual(result.scalar_value, unary_native(p, depth, route))
            self.assertIsInstance(result.scalar_value, Fraction)
        self.assertEqual(len(seen), 72)

    def test_all_42_conjugates_execute_and_all_absent_packets_reject(self):
        seen = set()
        neutral_rejected = deep_rejected = 0
        for p, depth, route in itertools.product(ALPHABET, DEPTHS, ROUTES):
            source = f"let x = QP_UNARY_CONJUGATE(QP_P{p}, QP_D{depth}, QP_ROUTE_{route.upper()})\nreturn x"
            if route == "neutral" or (p, depth) in DEEP_CONJUGATE_EXCLUSIONS:
                with self.assertRaises(QPDomainError):
                    run_program_text(source)
                neutral_rejected += int(route == "neutral")
                deep_rejected += int(route != "neutral" and (p, depth) in DEEP_CONJUGATE_EXCLUSIONS)
            else:
                result = run_program_text(source)
                seen.add(result.entity_id)
                self.assertEqual(result.scalar_value, unary_native(p, depth, route))
        self.assertEqual((len(seen), neutral_rejected, deep_rejected), (42, 24, 6))

    def test_all_64_ordered_pairs_execute_and_preserve_orientation(self):
        seen = set()
        total = Fraction(0)
        for a, b in itertools.product(ALPHABET, repeat=2):
            source = f"let x = QP_ORDERED_PAIR(QP_P{a}, QP_P{b})\nreturn x"
            result = run_program_text(source)
            spec = ordered_pair(a, b)
            self.assertEqual((result.entity_id, result.scalar_value), (spec.signature, spec.native_account))
            seen.add(result.entity_id)
            total += result.scalar_value
            if a != b:
                self.assertNotEqual(result.entity_id, f"OP:{b}:{a}")
        self.assertEqual(len(seen), 64)
        self.assertEqual(total, 25074)

    def test_all_120_triads_canonicalize_all_permutations_and_gate(self):
        allowed = load_triad_allowed()
        admitted = rejected = 0
        total = Fraction(0)
        for labels in itertools.combinations_with_replacement(ALPHABET, 3):
            expected = unordered_triad_candidate(*labels)
            total += expected.native_account
            for perm in set(itertools.permutations(labels)):
                args = ", ".join(f"QP_P{p}" for p in perm)
                candidate = run_program_text(f"let x = QP_UNORDERED_TRIAD({args})\nreturn x")
                self.assertEqual(candidate.entity_id, expected.signature)
            args = ", ".join(f"QP_P{p}" for p in labels)
            source = f"let c = QP_UNORDERED_TRIAD({args})\nlet x = QP_TRIAD_SURFACE_GATE(c)\nreturn x"
            if expected.signature.split(":", 1)[1] in allowed:
                result = run_program_text(source)
                self.assertEqual((result.entity_id, result.semantic_type), (expected.signature, "QPLocalTriadTemplate"))
                admitted += 1
            else:
                with self.assertRaises(QPDomainError):
                    run_program_text(source)
                rejected += 1
        self.assertEqual((admitted, rejected, total), (107, 13, Fraction(575100)))

    def test_all_supports_carriers_global_and_controls(self):
        for p in ALPHABET:
            result = run_program_text(f"let x = QP_HIDDEN_SUPPORT(QP_P{p})\nreturn x")
            self.assertEqual(result.scalar_value, hidden_support(p).native_account)
        for name, native in CARRIER_NATIVE.items():
            result = run_program_text(f"let x = QP_CARRIER_TERMINAL(QP_CARRIER_{name})\nreturn x")
            self.assertEqual(result.scalar_value, native)
        parent = run_program_text("let x = QP_SCALAR_PARENT()\nreturn x")
        self.assertEqual(parent.scalar_value, Fraction(126000))
        for name in CONTROL_NAMES:
            result = run_program_text(f"let x = QP_EXPLICIT_CONTROL(QP_CONTROL_{name})\nreturn x")
            self.assertEqual((result.semantic_type, result.scalar_value), ("QPRejectedConstruction", Fraction(0)))


class CensusAndNativeTests(unittest.TestCase):
    def test_complete_census_and_role_partition(self):
        census = grammar_census()
        self.assertEqual(census["constructors"], {"CI": 6, "GS": 1, "HS": 8, "OP": 64, "UC": 42, "UD": 72, "UT": 120, "XC": 8})
        self.assertEqual(census["roles"], {"GLOBAL": 1, "INFRASTRUCTURE": 14, "LEGAL_LOCAL_TEMPLATE": 285, "REJECTED": 21})
        self.assertEqual((census["total"], census["unique_signatures"]), (321, 321))

    def test_constituent_payload_only_on_114_unaries(self):
        rows = enumerate_qp_productions()
        self.assertEqual(sum(bool(row["constituent_payload"]) for row in rows), 114)
        self.assertTrue(all(not row["constituent_payload"] for row in rows if row["constructor"] in {"OP", "UT"}))

    def test_all_321_native_packets_are_keyed_by_canonical_signature(self):
        rows = enumerate_qp_productions()
        index = load_native_index()
        self.assertEqual(set(index), {row["signature"] for row in rows})
        required = {
            "canonical_signature",
            "source_row_id",
            "assembly_template_id",
            "opaque_token_id",
            "M_native_exact",
            "S_debit_or_credit_exact",
            "M_observed_candidate_exact",
            "qA_source_support_exact",
            "tensor_carrier_support_exact",
            "retained_write_support_exact",
            "lift_excess_exact",
        }
        for row in rows:
            packet = native_packet(row["signature"])
            self.assertTrue(required <= set(packet))
            self.assertEqual(packet["canonical_signature"], row["signature"])
            for field in required & {key for key in packet if key.endswith("_exact")}:
                Fraction(packet[field])

    def test_candidate_and_admitted_triad_share_native_identity(self):
        source = "let c = QP_UNORDERED_TRIAD(QP_P3, QP_P4, QP_P6)\nlet n = QP_NATIVE_SIGNATURE(c)\nreturn n"
        candidate = run_program_text(source).result_payload
        source = "let c = QP_UNORDERED_TRIAD(QP_P3, QP_P4, QP_P6)\nlet t = QP_TRIAD_SURFACE_GATE(c)\nlet n = QP_NATIVE_SIGNATURE(t)\nreturn n"
        admitted = run_program_text(source).result_payload
        self.assertEqual(candidate, admitted)

    def test_each_native_readout_is_exact_and_structural(self):
        operators = {
            "QP_NATIVE_ACCOUNT": "M_native_exact",
            "QP_SURFACE_DEBIT_OR_CREDIT": "S_debit_or_credit_exact",
            "QP_OBSERVED_CANDIDATE_ACCOUNT": "M_observed_candidate_exact",
            "QP_SOURCE_SUPPORT": "qA_source_support_exact",
            "QP_TENSOR_SUPPORT": "tensor_carrier_support_exact",
            "QP_RETAINED_SUPPORT": "retained_write_support_exact",
        }
        packet = native_packet("UD:8:2:neutral")
        for operator, field in operators.items():
            source = f"let p = QP_UNARY_DIRECT(QP_P8, QP_D2, QP_ROUTE_NEUTRAL)\nlet n = QP_NATIVE_SIGNATURE(p)\nlet x = {operator}(n)\nreturn x"
            result = run_program_text(source)
            self.assertEqual(result.scalar_value, Fraction(packet[field]))
            self.assertEqual(result.semantic_scope, "STRUCTURAL_GRAMMAR")

    def test_source_and_native_reconciliation_are_complete(self):
        self.assertEqual(verify_qp_source_reconciliation(), {"status": "PASS", "rows": 321, "unique_signatures": 321, "failures": 0, "candidate_id_semantic_selector": False})
        native = verify_qp_native_reconciliation()
        self.assertEqual((native["status"], native["rows"], native["unique_signatures"]), ("PASS", 321, 321))

    def test_native_inverse_reproduces_frozen_scope(self):
        result = verify_qp_native_inverse()
        self.assertEqual(result["verdict"], "PASS_QP_TENSOR_NATIVE_INVERSE")
        self.assertEqual((result["source_rows"], result["applicable_nonzero_support_rows"], result["noninvertible_zero_support_rows"]), (321, 285, 36))
        self.assertEqual((result["exact_both_rows"], result["source_precision_bounded_both_rows"], result["exceptions"]), (74, 285, 0))
        self.assertFalse(result["physical_mass_operator_registered"])

    def test_independent_reference_enumerator_is_byte_equivalent(self):
        path = ROOT / "tools" / "reference_qp_enumerator.py"
        spec = importlib.util.spec_from_file_location("v05_reference_enumerator", path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        reference = module.enumerate_reference(ROOT / "registry")
        runtime = enumerate_qp_productions()
        canonical = lambda value: json.dumps(value, sort_keys=True, separators=(",", ":"))
        self.assertEqual(canonical(runtime), canonical(reference))

    def test_rejected_triad_remains_inspectable(self):
        payload = inspect_qp_production("UT:1+3+8")
        self.assertEqual(payload["production"]["census_role"], "REJECTED")
        self.assertFalse(payload["ordinary_gate_executable"])


if __name__ == "__main__":
    unittest.main()
