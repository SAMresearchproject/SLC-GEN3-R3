from __future__ import annotations

import json
import hashlib
import os
import subprocess
import sys
import unittest
from pathlib import Path

from sam_language_v0_6.errors import (
    SLCControlTargetAliasError,
    SLCFormalProfileRequired,
    SLCStateCustodyError,
    SLCStateInvariantError,
    TypeCheckError,
    UnknownOperatorError,
)
from sam_language_v0_6.runtime import load_registry, parse_program, run_program_text
from sam_language_v0_6.slc_state import (
    DIMENSION,
    FROZEN_SOURCE_HASHES,
    REGISTER_SIZE,
    ExactSLCState,
    SLCHistoryRecord,
    apply_complex_phase,
    basis_state,
    binary_flip,
    inspect_state,
    prepare_request,
    publish,
    x1_response,
    zero_state,
)


ROOT = Path(__file__).resolve().parents[1]


def program(*lines: str) -> str:
    return "\n".join(lines)


def ghz_star() -> object:
    state = prepare_request(zero_state(), 0)
    for target in range(1, REGISTER_SIZE):
        state = x1_response(state, 0, target)
    return state


def ghz_chain() -> object:
    state = prepare_request(zero_state(), 0)
    for target in range(1, REGISTER_SIZE):
        state = x1_response(state, target - 1, target)
    return state


class SLCStateKernelTests(unittest.TestCase):
    def test_zero_cardinality_and_genesis(self):
        state = zero_state()
        self.assertEqual((state.register_size, state.dimension), (12, 4096))
        self.assertEqual(state.coefficients, ((0, 1),))
        self.assertEqual(state.sqrt2_power, 0)
        self.assertEqual(state.normalization_numerator, 1)
        self.assertEqual(len(state.history), 1)
        self.assertEqual(state.history[0].operator, "SLC_ZERO_REGISTER")

    def test_prepare_request_exact(self):
        state = prepare_request(zero_state(), 0)
        self.assertEqual(state.coefficients, ((0, 1), (1, 1)))
        self.assertEqual(state.sqrt2_power, 1)
        self.assertEqual(state.normalization_numerator, 2)

    def test_response_exact_bell(self):
        state = x1_response(prepare_request(zero_state(), 0), 0, 1)
        self.assertEqual(state.coefficients, ((0, 1), (3, 1)))
        self.assertEqual(state.sqrt2_power, 1)

    def test_prepare_is_involutive(self):
        state = zero_state()
        restored = prepare_request(prepare_request(state, 4), 4)
        self.assertEqual(restored.state_hash, state.state_hash)
        self.assertNotEqual(restored.history_hash, state.history_hash)

    def test_binary_flip_is_not_prepare(self):
        flipped = binary_flip(zero_state(), 3)
        prepared = prepare_request(zero_state(), 3)
        self.assertEqual(flipped.coefficients, ((8, 1),))
        self.assertEqual(flipped.support_size, 1)
        self.assertEqual(prepared.support_size, 2)
        self.assertNotEqual(flipped.state_hash, prepared.state_hash)

    def test_response_is_involutive(self):
        state = prepare_request(zero_state(), 0)
        restored = x1_response(x1_response(state, 0, 7), 0, 7)
        self.assertEqual(restored.state_hash, state.state_hash)

    def test_control_target_alias_rejected_atomically(self):
        state = prepare_request(zero_state(), 0)
        before = (state.state_hash, state.history_hash, len(state.history))
        with self.assertRaises(SLCControlTargetAliasError):
            x1_response(state, 0, 0)
        self.assertEqual(before, (state.state_hash, state.history_hash, len(state.history)))

    def test_star_chain_same_state_distinct_history(self):
        star = ghz_star()
        chain = ghz_chain()
        self.assertEqual(star.coefficients, ((0, 1), (4095, 1)))
        self.assertEqual(star.state_hash, chain.state_hash)
        self.assertNotEqual(star.history_hash, chain.history_hash)

    def test_ghz_topology_is_exact_component_not_physical_edge(self):
        dossier = inspect_state(ghz_chain())
        self.assertEqual(dossier["state_topology"]["component_partition"], [list(range(12))])
        self.assertEqual(dossier["state_topology"]["ghz_like_component_count"], 1)
        self.assertIn("not a physical-connectivity", dossier["state_topology"]["classification_boundary"])

    def test_six_bell_component_partition(self):
        state = zero_state()
        for root in range(0, 12, 2):
            state = prepare_request(state, root)
            state = x1_response(state, root, root + 1)
        dossier = inspect_state(state)
        self.assertEqual(
            dossier["state_topology"]["component_partition"],
            [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9], [10, 11]],
        )
        self.assertEqual(dossier["state_topology"]["ghz_like_component_count"], 6)

    def test_peel_and_restore(self):
        ghz = ghz_star()
        peeled = x1_response(ghz, 0, 11)
        restored = x1_response(peeled, 0, 11)
        self.assertNotEqual(peeled.state_hash, ghz.state_hash)
        self.assertEqual(restored.state_hash, ghz.state_hash)
        self.assertNotEqual(restored.history_hash, ghz.history_hash)

    def test_basis_mapping_all_addresses_one_pair(self):
        for basis in range(DIMENSION):
            state = x1_response(basis_state(basis), 3, 9)
            expected = basis ^ (1 << 9) if basis & (1 << 3) else basis
            self.assertEqual(state.coefficients, ((expected, 1),))

    def test_tampered_coefficients_rejected(self):
        state = prepare_request(zero_state(), 0)
        object.__setattr__(state, "coefficients", ((0, 2), (1, 1)))
        with self.assertRaises(SLCStateInvariantError):
            prepare_request(state, 1)

    def test_tampered_receipt_rejected(self):
        state = prepare_request(zero_state(), 0)
        object.__setattr__(state.history[-1], "receipt_hash", "0" * 64)
        with self.assertRaises(SLCStateCustodyError):
            state.verify_custody()

    def test_boundary_entry_points_reject(self):
        with self.assertRaises(Exception):
            apply_complex_phase(zero_state())
        with self.assertRaises(Exception):
            publish(zero_state())

    def test_frozen_source_hashes_are_present(self):
        self.assertEqual(len(FROZEN_SOURCE_HASHES), 3)
        self.assertTrue(all(len(value) == 64 for value in FROZEN_SOURCE_HASHES.values()))

    def test_state_hash_is_sha256_of_canonical_json_without_hidden_prefix(self):
        state = prepare_request(zero_state(), 0)
        payload = {
            "schema": "SAM_LANGUAGE_SLC_C1_EXACT_STATE_V1",
            "register_size": 12,
            "sqrt2_power": 1,
            "coefficients": [[0, 1], [1, 1]],
        }
        expected = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        self.assertEqual(state.state_hash, expected)

    def test_false_but_rehashed_transition_fails_executable_custody(self):
        zero = zero_state()
        false_terminal = basis_state(2)
        forged = SLCHistoryRecord.build(
            sequence=2,
            operator="SLC_BINARY_FLIP",
            arguments=(0,),
            prior_state_hash=zero.state_hash,
            result_state_hash=false_terminal.state_hash,
            prior_history_hash=zero.history_hash,
        )
        with self.assertRaises(SLCStateCustodyError):
            ExactSLCState(false_terminal.coefficients, 0, zero.history + (forged,))

    def test_route_forest_validator_checks_prepare_and_order(self):
        complete = inspect_state(ghz_chain())["route_topology"]
        self.assertTrue(complete["is_complete_rooted_forest_history"])

        response_only = x1_response(zero_state(), 0, 1)
        invalid = inspect_state(response_only)["route_topology"]
        self.assertFalse(invalid["is_parent_before_child_forest_prefix"])
        self.assertIn(
            "CONTROL_NOT_REACHED_BEFORE_RESPONSE",
            [row["reason"] for row in invalid["invalid_forest_steps"]],
        )


class SLCLanguageIntegrationTests(unittest.TestCase):
    BELL = program(
        "let s0: SLCState12 = SLC_ZERO_REGISTER()",
        "let s1: SLCState12 = SLC_PREPARE_REQUEST(s0, L0)",
        "let bell: SLCState12 = SLC_X1_RESPONSE(s1, L0, L1)",
        "return bell",
    )

    def test_digit_operator_parses(self):
        ast = parse_program(self.BELL)
        self.assertEqual(len(ast.statements), 4)

    def test_registry_installs_twelve_sites_and_five_operators(self):
        registry = load_registry()
        self.assertEqual(
            [registry.entity(f"L{i}").entity_id for i in range(12)],
            [f"SLC_L{i}" for i in range(12)],
        )
        for name in (
            "SLC_ZERO_REGISTER",
            "SLC_BINARY_FLIP",
            "SLC_PREPARE_REQUEST",
            "SLC_X1_RESPONSE",
            "SLC_INSPECT_STATE",
        ):
            self.assertEqual(registry.operator(name).required_mode, "slc-c1-formal")

    def test_formal_program_executes(self):
        result = run_program_text(self.BELL, mode="slc-c1-formal")
        self.assertEqual(result.semantic_type, "SLCState12")
        self.assertEqual(
            [row["basis_index"] for row in result.result_payload["coefficients"]],
            [0, 3],
        )
        self.assertEqual(result.authority_status, "FORMAL_CANDIDATE")

    def test_normal_and_research_profiles_reject(self):
        for mode in ("normal", "research"):
            with self.subTest(mode=mode), self.assertRaises(SLCFormalProfileRequired):
                run_program_text(self.BELL, mode=mode)

    def test_qp_coordinate_is_not_a_site(self):
        source = program(
            "let s0: SLCState12 = SLC_ZERO_REGISTER()",
            "let bad = SLC_PREPARE_REQUEST(s0, QP_P1)",
            "return bad",
        )
        with self.assertRaises(TypeCheckError):
            run_program_text(source, mode="slc-c1-formal")

    def test_core_qp_and_slc_share_one_program_path(self):
        source = program(
            "let w = RESOLVE(S8_BINARY_SURFACE, B_CONTACT_OPERATOR, X1_AXIS_SELF_CHANNEL)",
            "let pair = QP_ORDERED_PAIR(QP_P8, QP_P1)",
            "let s0: SLCState12 = SLC_ZERO_REGISTER()",
            "let s1: SLCState12 = SLC_PREPARE_REQUEST(s0, L0)",
            "return s1",
        )
        result = run_program_text(source, mode="slc-c1-formal")
        operators = [row["operator"] for row in result.trace if row.get("operator")]
        self.assertEqual(
            operators,
            ["RESOLVE", "QP_ORDERED_PAIR", "SLC_ZERO_REGISTER", "SLC_PREPARE_REQUEST"],
        )

    def test_inspection_is_read_only(self):
        source = self.BELL.replace("return bell", "let dossier: SLCStateInspection = SLC_INSPECT_STATE(bell)\nreturn dossier")
        result = run_program_text(source, mode="slc-c1-formal")
        self.assertEqual(result.semantic_type, "SLCStateInspection")
        self.assertEqual(result.result_payload["history_length"], 3)

    def test_repeated_execution_is_byte_deterministic(self):
        left = json.dumps(
            run_program_text(self.BELL, mode="slc-c1-formal").result_payload,
            sort_keys=True,
            separators=(",", ":"),
        )
        right = json.dumps(
            run_program_text(self.BELL, mode="slc-c1-formal").result_payload,
            sort_keys=True,
            separators=(",", ":"),
        )
        self.assertEqual(left, right)

    def test_publication_and_phase_symbols_are_unregistered(self):
        registry = load_registry()
        for name in ("SLC_PUBLISH", "SLC_SAMPLE", "SLC_COMPLEX_PHASE", "SLC_PHYSICAL_EDGE"):
            with self.assertRaises(UnknownOperatorError):
                registry.operator(name)

    def test_cli_formal_profile_and_profile_exclusion(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "src")
        command = [
            sys.executable,
            "-m",
            "sam_language_v0_6.cli",
            "run",
            str(ROOT / "examples" / "slc_bell.sam"),
            "--slc-c1-formal",
        ]
        completed = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["result_payload"]["support_size"], 2)

        conflict = subprocess.run(
            command + ["--research"], cwd=ROOT, env=env, capture_output=True, text=True
        )
        self.assertNotEqual(conflict.returncode, 0)


if __name__ == "__main__":
    unittest.main()
