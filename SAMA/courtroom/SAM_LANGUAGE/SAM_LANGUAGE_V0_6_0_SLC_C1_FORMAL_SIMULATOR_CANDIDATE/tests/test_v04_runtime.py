from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from sam_language_v0_6.errors import (  # noqa: E402
    AuthorityError,
    ContextRoleError,
    ProvenanceCycleError,
    RawProgramExecutionError,
    TypeCheckError,
)
from sam_language_v0_6.runtime import (  # noqa: E402
    PARENT_HASH,
    VALID_CLOSURE_PROGRAM,
    ProvenanceStore,
    check_program,
    execute_checked,
    load_registry,
    parse_program,
    registry_payload,
    run_program_text,
)


class RuntimePipelineTests(unittest.TestCase):
    def test_parent_hash_is_recorded(self):
        self.assertEqual(PARENT_HASH, "0ee6649ed0c8f863fd5de5ef54e6ce305e1b1c44a0e24a5a4f57c1ef544742d0")

    def test_valid_closure_program_executes_to_l162(self):
        result = run_program_text(VALID_CLOSURE_PROGRAM)
        self.assertEqual(result.entity_id, "L162_FULL_LEDGER")
        self.assertEqual(result.scalar_value, 162)
        self.assertEqual(result.semantic_type, "FullLedger")

    def test_raw_program_never_executes(self):
        program = parse_program(VALID_CLOSURE_PROGRAM)
        with self.assertRaises(RawProgramExecutionError):
            execute_checked(program)

    def test_direct_s8_volume_promotion_is_rejected(self):
        with self.assertRaises(TypeCheckError):
            run_program_text("let v = PROMOTE_VOLUME(S8_BINARY_SURFACE, D3_DIMENSION)\nreturn v")

    def test_a_equals_b_is_rejected(self):
        with self.assertRaises(AuthorityError):
            run_program_text("assert A_OPERATOR == B_CONTACT_OPERATOR\nreturn S8_BINARY_SURFACE")

    def test_b_equals_x1_is_rejected(self):
        with self.assertRaises(AuthorityError):
            run_program_text("assert B_CONTACT_OPERATOR == X1_AXIS_SELF_CHANNEL\nreturn S8_BINARY_SURFACE")

    def test_operator_insertion_is_rejected(self):
        with self.assertRaises(AuthorityError):
            run_program_text("INSERT_LEDGER_ROW(B_CONTACT_OPERATOR)\nreturn S8_BINARY_SURFACE")

    def test_axis_insertion_is_rejected(self):
        with self.assertRaises(AuthorityError):
            run_program_text("INSERT_LEDGER_ROW(X1_AXIS_SELF_CHANNEL)\nreturn S8_BINARY_SURFACE")

    def test_historical_a_row_proxy_is_retired(self):
        with self.assertRaises(AuthorityError):
            run_program_text("let a = HISTORICAL_A_FIELD_ROW_PROXY\nreturn a")

    def test_unknown_type_is_rejected(self):
        with self.assertRaises(TypeCheckError):
            run_program_text("let s: TotallyUnsupportedType = S8_BINARY_SURFACE\nreturn s")

    def test_unknown_entity_is_rejected(self):
        with self.assertRaises(Exception):
            run_program_text("let x = NO_SUCH_ENTITY\nreturn x")

    def test_unsupported_contextual_role_is_rejected(self):
        with self.assertRaises(ContextRoleError):
            run_program_text("ROLE S8_BINARY_SURFACE@domain_multiplicity = DOMAIN_MULTIPLICITY\nreturn S8_BINARY_SURFACE")

    def test_supported_s8_contextual_role_passes(self):
        result = run_program_text("ROLE S8_BINARY_SURFACE@binary_sign_state_surface = BINARY_SURFACE\nreturn S8_BINARY_SURFACE")
        self.assertEqual(result.entity_id, "S8_BINARY_SURFACE")

    def test_structural_only_edge_requires_research_mode(self):
        source = "let p = RESERVE_CLOSURE_ADDRESS(F81_COMPLETED_FACE, X1_AXIS_SELF_CHANNEL)\nreturn p"
        with self.assertRaises(AuthorityError):
            run_program_text(source)

    def test_structural_only_edge_research_mode_returns_p80(self):
        source = "let p = RESERVE_CLOSURE_ADDRESS(F81_COMPLETED_FACE, X1_AXIS_SELF_CHANNEL)\nreturn p"
        result = run_program_text(source, mode="research")
        self.assertEqual(result.entity_id, "P80_PARTICLE_FACE_CONTENT")
        self.assertEqual(result.authority_status, "STRUCTURAL_ONLY")
        self.assertTrue(result.warnings)

    def test_operator_scalars_are_null_and_x1_is_one(self):
        registry = load_registry()
        self.assertIsNone(registry.entity("B_CONTACT_OPERATOR").scalar_value)
        self.assertIsNone(registry.entity("A_OPERATOR").scalar_value)
        self.assertEqual(registry.entity("X1_AXIS_SELF_CHANNEL").scalar_value, 1)
        self.assertEqual(registry.entity("B_CONTACT_OPERATOR").metadata["acts_through"], "X1_AXIS_SELF_CHANNEL")
        self.assertEqual(registry.entity("A_OPERATOR").metadata["relation_to_B"], "OPEN")

    def test_canonical_scalar_one_occurrences_remain_distinct(self):
        registry = load_registry()
        ids = {
            registry.entity("X1_AXIS_SELF_CHANNEL").entity_id,
            registry.entity("C1_ROAD_LIGHT_CARRIER").entity_id,
            registry.entity("P1_LIFT_BEARING_SUPPORT").entity_id,
            registry.entity("A1_HISTORICAL_ROW_PROXY").entity_id,
        }
        self.assertEqual(len(ids), 4)
        self.assertEqual({registry.entity(entity_id).scalar_value for entity_id in ids}, {1})
        self.assertEqual(registry.entity("P1_LIFT_BEARING_SUPPORT").metadata["lift_excess"], "1/144")

    def test_scalar_one_compatibility_aliases_resolve(self):
        registry = load_registry()
        self.assertEqual(registry.entity("SCALAR_ONE_CARRIER").entity_id, "C1_ROAD_LIGHT_CARRIER")
        self.assertEqual(registry.entity("SCALAR_ONE_SUPPORT").entity_id, "P1_LIFT_BEARING_SUPPORT")
        self.assertEqual(registry.entity("HISTORICAL_A_FIELD_ROW_PROXY").entity_id, "A1_HISTORICAL_ROW_PROXY")

    def test_s8_carrier8_support8_remain_distinct(self):
        registry = load_registry()
        ids = {registry.entity(name).entity_id for name in ["S8_BINARY_SURFACE", "CARRIER8", "SUPPORT8"]}
        self.assertEqual(len(ids), 3)

    def test_w9_carrier9_support9_remain_distinct(self):
        registry = load_registry()
        ids = {registry.entity(name).entity_id for name in ["W9_CLOSURE_WITNESS", "CARRIER9", "SUPPORT9"]}
        self.assertEqual(len(ids), 3)

    def test_distinct_81_roles_exist(self):
        payload = registry_payload()
        eighty_one = [
            entity
            for entity in payload["entities"].values()
            if entity["scalar_value"] == 81
        ]
        self.assertGreaterEqual(len(eighty_one), 3)

    def test_parse_check_execute_are_separate_objects(self):
        program = parse_program(VALID_CLOSURE_PROGRAM)
        checked = check_program(program)
        result = execute_checked(checked)
        self.assertEqual(type(program).__name__, "Program")
        self.assertEqual(type(checked).__name__, "CheckedProgram")
        self.assertEqual(result.entity_id, "L162_FULL_LEDGER")


class ProvenanceTests(unittest.TestCase):
    def test_same_assertion_new_source_retains_both_trails(self):
        store = ProvenanceStore()
        first = store.add_assertion("S8_BINARY_SURFACE", "scalar_value", 8, source_id="source_a")
        second = store.add_assertion("S8_BINARY_SURFACE", "scalar_value", 8, source_id="source_b")
        self.assertNotEqual(first["id"], second["id"])
        self.assertEqual(len(store.records), 2)

    def test_incompatible_assertion_creates_conflict(self):
        store = ProvenanceStore()
        store.add_assertion("S8_BINARY_SURFACE", "semantic_type", "BinarySurface", source_id="source_a")
        conflict = store.add_assertion("S8_BINARY_SURFACE", "semantic_type", "Carrier", source_id="source_b")
        self.assertEqual(conflict["status"], "CONFLICT")
        self.assertTrue(conflict["conflicts_with"])

    def test_supersession_requires_explicit_edge(self):
        store = ProvenanceStore()
        first = store.add_assertion("F81_COMPLETED_FACE", "status", "STRUCTURAL_ONLY", source_id="source_a")
        second = store.add_assertion("F81_COMPLETED_FACE", "status", "ACTIVE", source_id="source_b", supersedes=first["id"])
        self.assertEqual(second["supersedes"], first["id"])

    def test_dependency_cycle_raises_full_path(self):
        store = ProvenanceStore()
        store.add_dependency("A", "B")
        with self.assertRaises(ProvenanceCycleError) as context:
            store.add_dependency("B", "A")
        self.assertEqual(context.exception.cycle_path, ["A", "B", "A"])


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        env = dict()
        env.update({"PYTHONPATH": str(SRC)})
        return subprocess.run(
            [sys.executable, "-m", "sam_language_v0_6.cli", *args],
            cwd=str(ROOT),
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_cli_check(self):
        proc = self.run_cli("check")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["status"], "PASS")

    def test_cli_run(self):
        proc = self.run_cli("run")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["entity_id"], "L162_FULL_LEDGER")

    def test_cli_run_research(self):
        source = ROOT / "examples" / "structural_only_research.sam"
        proc = self.run_cli("run", "--research", str(source))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["entity_id"], "P80_PARTICLE_FACE_CONTENT")

    def test_cli_trace(self):
        proc = self.run_cli("trace")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("trace", json.loads(proc.stdout))

    def test_cli_explain(self):
        proc = self.run_cli("explain")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("entities", json.loads(proc.stdout)["hierarchy"])

    def test_cli_sources(self):
        proc = self.run_cli("sources")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("handoff_contract", json.loads(proc.stdout)["sources"])

    def test_cli_validate_contract(self):
        proc = self.run_cli("validate-contract")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["status"], "PASS")

    def test_cli_regress(self):
        proc = self.run_cli("regress")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["status"], "PASS")

    def test_cli_trace_entity_w9(self):
        proc = self.run_cli("trace", "W9_CLOSURE_WITNESS")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["canonical_entity_id"], "W9_CLOSURE_WITNESS")
        self.assertIn("S8 --B through X1--> W9", payload["derivation_trace"])

    def test_cli_trace_entity_l162(self):
        proc = self.run_cli("trace", "L162_FULL_LEDGER")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["scalar_value"], 162)
        self.assertIn("F81 * H2 -> L162", payload["derivation_trace"])

    def test_cli_explain_resolve(self):
        proc = self.run_cli("explain", "RESOLVE")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["operator_id"], "RESOLVE")
        self.assertEqual(payload["authority"]["status"], "ACTIVE")
        self.assertEqual(payload["signature"]["result_entity"], "W9_CLOSURE_WITNESS")

    def test_cli_sources_f81_are_branch_qualified_and_hashed(self):
        proc = self.run_cli("sources", "F81_COMPLETED_FACE")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["sources"])
        for source in payload["sources"]:
            self.assertIn("/", source["path"])
            self.assertEqual(len(source["sha256"]), 64)

    def test_cli_trace_canonical_scalar_one_entities(self):
        expectations = {
            "X1_AXIS_SELF_CHANNEL": ("AxisChannel", 1),
            "C1_ROAD_LIGHT_CARRIER": ("Carrier", 1),
            "P1_LIFT_BEARING_SUPPORT": ("LiftBearingSupport", 1),
            "A1_HISTORICAL_ROW_PROXY": ("HistoricalRowProxy", 1),
        }
        for entity_id, expected in expectations.items():
            with self.subTest(entity_id=entity_id):
                proc = self.run_cli("trace", entity_id)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                payload = json.loads(proc.stdout)
                self.assertEqual((payload["semantic_type"], payload["scalar_value"]), expected)
        p1 = json.loads(self.run_cli("trace", "P1_LIFT_BEARING_SUPPORT").stdout)
        self.assertEqual(p1["metadata"]["lift_excess"], "1/144")

    def test_cli_trace_operators_have_null_scalars(self):
        b = json.loads(self.run_cli("trace", "B_CONTACT_OPERATOR").stdout)
        a = json.loads(self.run_cli("trace", "A_OPERATOR").stdout)
        self.assertIsNone(b["scalar_value"])
        self.assertEqual(b["metadata"]["acts_through"], "X1_AXIS_SELF_CHANNEL")
        self.assertIsNone(a["scalar_value"])
        self.assertEqual(a["metadata"]["relation_to_B"], "OPEN")

    def test_cli_trace_file_interface(self):
        source = ROOT / "examples" / "valid_closure.sam"
        proc = self.run_cli("trace", "--file", str(source))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("trace", json.loads(proc.stdout))

    def test_cli_unknown_entity_has_typed_error_and_no_traceback(self):
        proc = self.run_cli("trace", "NO_SUCH_ENTITY")
        self.assertEqual(proc.returncode, 2)
        self.assertNotIn("Traceback", proc.stderr)
        payload = json.loads(proc.stderr)
        self.assertEqual(payload["error"], "UnknownEntityError")

    def test_cli_missing_file_has_typed_error_and_no_traceback(self):
        proc = self.run_cli("trace", "--file", "NO_SUCH_FILE.sam")
        self.assertEqual(proc.returncode, 2)
        self.assertNotIn("Traceback", proc.stderr)
        payload = json.loads(proc.stderr)
        self.assertEqual(payload["error"], "CLIUsageError")


if __name__ == "__main__":
    unittest.main()
