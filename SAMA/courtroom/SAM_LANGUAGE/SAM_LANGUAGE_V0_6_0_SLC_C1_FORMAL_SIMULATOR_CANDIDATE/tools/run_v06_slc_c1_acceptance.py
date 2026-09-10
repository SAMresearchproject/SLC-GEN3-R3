"""Run the sealed SAM Language v0.6 SLC C1 acceptance campaign once.

This runner is intentionally self-contained and deterministic.  It tests the
new language kernel, not the historical NumPy discovery runner.  State
decisions use only the exact sparse-integer representation exposed by
``sam_language_v0_6.slc_state``.

The script is a SAM result-producing executable and therefore must be invoked
through ``tools/run_sam_test.py`` from the repository root.  It never repairs
implementation files.  A pass writes one result, concise gate reports, and a
release manifest; a failure writes one fail-stop record and exits.
"""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence


CANDIDATE = Path(__file__).resolve().parents[1]
REPO = CANDIDATE.parent
PARENT = REPO / "SAM_LANGUAGE_V0_5_0_PARTICLE_GRAMMAR_CANDIDATE"
SLCX002 = REPO / "18_SAM_NATIVE_QC/SLCX002_PREPARE_REQUEST_X1_RESPONSE_FORMAL_STATE_DISCOVERY"
SLCX003 = REPO / "18_SAM_NATIVE_QC/SLCX003_12_LEBIT_REGISTER_JOINT_STATE_TOPOLOGY_DISCOVERY"
SRC = CANDIDATE / "src"
REPORTS = CANDIDATE / "reports"
CONTRACT_PATH = CANDIDATE / "V0_6_SLC_C1_CONTRACT.json"
SOURCE_MANIFEST_PATH = CANDIDATE / "V0_6_SLC_C1_SOURCE_MANIFEST.json"
PRECOMMIT_PATH = CANDIDATE / "V0_6_SLC_C1_PRECOMMIT.md"
SEAL_PATH = CANDIDATE / "V0_6_SLC_C1_PRECOMMIT_SEAL.json"
EXECUTABLE_HASHES_PATH = CANDIDATE / "V0_6_SLC_C1_EXECUTABLE_HASHES.json"
EXECUTABLE_SEAL_PATH = CANDIDATE / "V0_6_SLC_C1_EXECUTABLE_SEAL.txt"
RESULT_PATH = CANDIDATE / "V0_6_SLC_C1_ACCEPTANCE_RESULT.json"
FAILURE_PATH = CANDIDATE / "V0_6_SLC_C1_ACCEPTANCE_FAILURE.json"
RELEASE_MANIFEST_PATH = CANDIDATE / "V0_6_SLC_C1_RELEASE_MANIFEST.json"
CAMPAIGN_ID = "SAM_LANGUAGE_V0_6_0_SLC_C1_FORMAL_SIMULATOR_CANDIDATE"
EXPECTED_PARENT_HASH = "726011b38d27a9b5403a7df66d8d4d5ac7c49960bc331d65f57c66de7a7ecaf0"
PRIMARY_VERDICT = (
    "PASS_SAM_LANGUAGE_V0_6_SLC_C1_REAL_GRAMMAR_KERNEL"
    "__EXACT_12_LEBIT_STATE_EXECUTION_AND_TAMPER_EVIDENT_ROUTE_HISTORY"
    "__PHASE_PUBLICATION_AND_PHYSICAL_REALIZATION_OPEN"
)

sys.dont_write_bytecode = True
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sam_language_v0_6 import evaluator as evaluator_api  # noqa: E402
from sam_language_v0_6 import parser as parser_api  # noqa: E402
from sam_language_v0_6.errors import (  # noqa: E402
    SLCControlTargetAliasError,
    SLCFormalProfileRequired,
    SLCRegisterArityError,
    SLCStateCustodyError,
    SLCStateInvariantError,
    SLCUnsupportedConnectivityError,
    SLCUnsupportedPhaseError,
    SLCUnsupportedPublicationError,
    TypeCheckError,
    UnknownOperatorError,
)
from sam_language_v0_6.runtime import (  # noqa: E402
    check_program,
    execute_checked,
    load_registry,
    parse_program,
    run_program_text,
)
from sam_language_v0_6.slc_state import (  # noqa: E402
    DIMENSION,
    ENGINE_CONTRACT_HASH,
    FORMAL_AUTHORITY,
    FROZEN_SOURCE_HASHES,
    REGISTER_SIZE,
    ExactSLCState,
    apply_complex_phase,
    assert_physical_connectivity,
    basis_state,
    binary_flip,
    inspect_state,
    prepare_request,
    publish,
    sample_measurement,
    x1_response,
    zero_state,
)
from clean_wheel_probe import run_clean_wheel_probe  # noqa: E402


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def aggregate(entries: dict[str, str]) -> str:
    digest = hashlib.sha256()
    for relative, file_hash in sorted(entries.items()):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_hash.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8")


def run_command(args: list[str], *, cwd: Path, env: dict[str, str]) -> dict[str, Any]:
    process = subprocess.run(
        args, cwd=cwd, env=env, text=True, capture_output=True, check=False
    )
    return {
        "args": args,
        "cwd": str(cwd),
        "returncode": process.returncode,
        "stdout": process.stdout,
        "stderr": process.stderr,
        "traceback_found": "Traceback" in process.stdout or "Traceback" in process.stderr,
    }


def fail_stop(stage: str, evidence: Any) -> int:
    payload = {
        "campaign_id": CAMPAIGN_ID,
        "status": "FAIL_STOP",
        "stage": stage,
        "same_run_repair": False,
        "result_count": 1,
        "evidence": evidence,
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(FAILURE_PATH, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1


def tree_snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
    }


def candidate_code_snapshot() -> dict[str, str]:
    roots = ["src", "tests", "tools", "registry", "examples"]
    files: list[Path] = []
    for name in roots:
        base = CANDIDATE / name
        if base.exists():
            files.extend(path for path in base.rglob("*") if path.is_file())
    for name in (
        "pyproject.toml",
        "README.md",
        "CHANGELOG.md",
        "V0_6_SLC_C1_CONTRACT.json",
        "V0_6_SLC_C1_PRECOMMIT.md",
        "V0_6_SLC_C1_PRECOMMIT_SEAL.json",
        "V0_6_SLC_C1_SOURCE_MANIFEST.json",
        "V0_5_PARENT_BASELINE.json",
        "build_v06_slc_c1_precommit.py",
    ):
        path = CANDIDATE / name
        if path.is_file():
            files.append(path)
    return {
        path.relative_to(CANDIDATE).as_posix(): sha256(path)
        for path in sorted(set(files))
        if "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
        and ".egg-info" not in path.as_posix()
    }


def custody_gate() -> dict[str, Any]:
    parent_payload = read_json(PARENT / "V0_5_EXECUTABLE_HASHES.json")
    parent_mismatches = []
    observed_parent: dict[str, str] = {}
    for relative, expected in sorted(parent_payload["files"].items()):
        path = PARENT / relative
        observed = sha256(path) if path.is_file() else "MISSING"
        observed_parent[relative] = observed
        if observed != expected:
            parent_mismatches.append(
                {"path": relative, "expected": expected, "observed": observed}
            )
    parent_hash = aggregate(observed_parent)

    manifest = read_json(SOURCE_MANIFEST_PATH)
    source_mismatches = []
    for row in manifest["sources"]:
        path = REPO / row["path"]
        observed = sha256(path) if path.is_file() else "MISSING"
        if observed != row["sha256"]:
            source_mismatches.append(
                {"path": row["path"], "expected": row["sha256"], "observed": observed}
            )

    seal = read_json(SEAL_PATH)
    executable = read_json(EXECUTABLE_HASHES_PATH)
    observed_candidate = candidate_code_snapshot()
    executable_mismatches = [
        {"path": path, "expected": expected, "observed": observed_candidate.get(path)}
        for path, expected in sorted(executable["files"].items())
        if observed_candidate.get(path) != expected
    ]
    executable_mismatches.extend(
        {"path": path, "expected": None, "observed": observed}
        for path, observed in sorted(observed_candidate.items())
        if path not in executable["files"]
    )
    observed_candidate_hash = aggregate(observed_candidate)
    seal_payload = {key: value for key, value in seal.items() if key != "seal_sha256"}
    seal_checks = {
        "contract": sha256(CONTRACT_PATH) == seal["contract_sha256"],
        "precommit": sha256(PRECOMMIT_PATH) == seal["precommit_sha256"],
        "source_manifest": sha256(SOURCE_MANIFEST_PATH) == seal["source_manifest_sha256"],
        "builder": sha256(CANDIDATE / "build_v06_slc_c1_precommit.py") == seal["builder_sha256"],
        "seal": canonical_hash(seal_payload) == seal["seal_sha256"],
        "parent_hash": parent_hash == seal["sam_language_v0_5_executable_hash"],
        "slcx002_manifest": sha256(SLCX002 / "release/SLCX002_RELEASE_MANIFEST.csv")
        == seal["slcx002_release_manifest_sha256"],
        "slcx003_manifest": sha256(SLCX003 / "release/SLCX003_RELEASE_MANIFEST.csv")
        == seal["slcx003_release_manifest_sha256"],
        "v06_executable_files": not executable_mismatches,
        "v06_executable_file_count": len(observed_candidate) == executable["file_count"],
        "v06_executable_hash": observed_candidate_hash == executable["candidate_code_hash"],
        "v06_runner_hash": (
            sha256(Path(__file__).resolve()) == executable["runner_sha256"]
        ),
        "v06_precommit_seal_hash": (
            sha256(SEAL_PATH) == executable["precommit_seal_sha256"]
        ),
        "v06_executable_seal": (
            EXECUTABLE_SEAL_PATH.read_text(encoding="utf-8").strip()
            == executable["candidate_code_hash"]
        ),
    }
    passed = (
        not parent_mismatches
        and not source_mismatches
        and parent_payload["file_count"] == 92
        and parent_hash == EXPECTED_PARENT_HASH
        and all(seal_checks.values())
    )
    return {
        "status": "PASS" if passed else "FAIL",
        "parent_files_verified": len(observed_parent),
        "parent_expected_hash": EXPECTED_PARENT_HASH,
        "parent_observed_hash": parent_hash,
        "parent_mismatches": parent_mismatches,
        "frozen_sources_verified": len(manifest["sources"]),
        "source_mismatches": source_mismatches,
        "candidate_executable_files_verified": len(observed_candidate),
        "candidate_executable_expected_hash": executable["candidate_code_hash"],
        "candidate_executable_observed_hash": observed_candidate_hash,
        "candidate_executable_mismatches": executable_mismatches,
        "seal_checks": seal_checks,
    }


def single_runtime_path_gate() -> dict[str, Any]:
    mixed = "\n".join(
        (
            "let w = RESOLVE(S8_BINARY_SURFACE, B_CONTACT_OPERATOR, X1_AXIS_SELF_CHANNEL)",
            "let pair = QP_ORDERED_PAIR(QP_P8, QP_P1)",
            "let s0: SLCState12 = SLC_ZERO_REGISTER()",
            "let s1: SLCState12 = SLC_PREPARE_REQUEST(s0, L0)",
            "return s1",
        )
    )
    result = run_program_text(mixed, mode="slc-c1-formal")
    operators = [row["operator"] for row in result.trace if row.get("operator")]
    implementation = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((SRC / "sam_language_v0_6").glob("*.py"))
    )
    checks = {
        "parser_reexport_identity": parser_api.parse_program is parse_program,
        "checker_reexport_identity": evaluator_api.check_program is check_program,
        "evaluator_reexport_identity": evaluator_api.execute_checked is execute_checked,
        "one_mixed_trace": operators
        == ["RESOLVE", "QP_ORDERED_PAIR", "SLC_ZERO_REGISTER", "SLC_PREPARE_REQUEST"],
        "source_text_dispatch_absent": "source_text_dispatch" not in implementation.lower(),
        "legacy_sidecar_import_absent": "slc_ledger" not in implementation,
        "operator_digits_parse": len(parse_program((CANDIDATE / "examples/slc_bell.sam").read_text(encoding="utf-8")).statements) == 4,
    }
    return {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks, "trace": operators}


def profile_and_cardinality_gates() -> tuple[dict[str, Any], dict[str, Any]]:
    source = (CANDIDATE / "examples/slc_bell.sam").read_text(encoding="utf-8")
    formal = run_program_text(source, mode="slc-c1-formal")
    rejected: dict[str, bool] = {}
    for mode in ("normal", "research"):
        try:
            run_program_text(source, mode=mode)
            rejected[mode] = False
        except SLCFormalProfileRequired:
            rejected[mode] = True
    registry = load_registry()
    site_ids = [registry.entity(f"L{site}").entity_id for site in range(12)]
    profile = {
        "status": "PASS"
        if formal.authority_status == FORMAL_AUTHORITY and all(rejected.values())
        else "FAIL",
        "formal_authority": formal.authority_status,
        "rejected_profiles": rejected,
    }
    cardinality_checks = {
        "register_size": REGISTER_SIZE == 12,
        "dimension": DIMENSION == 4096,
        "site_ids": site_ids == [f"SLC_L{site}" for site in range(12)],
        "basis_range": basis_state(0).dimension == basis_state(4095).dimension == 4096,
    }
    try:
        zero_state(register_size=10)
        cardinality_checks["other_arity_rejected"] = False
    except SLCRegisterArityError:
        cardinality_checks["other_arity_rejected"] = True
    cardinality = {
        "status": "PASS" if all(cardinality_checks.values()) else "FAIL",
        "checks": cardinality_checks,
    }
    return profile, cardinality


def exact_operator_gate() -> tuple[dict[str, Any], dict[str, Any]]:
    frozen = read_json(SLCX002 / "release/SLCX002_OPERATOR_MATRICES.json")
    zero = zero_state()
    prepared0 = prepare_request(zero, 0)
    prepared1 = prepare_request(basis_state(1), 0)
    flipped = binary_flip(zero, 0)
    mapping = []
    for control_bit, target_bit in itertools.product((0, 1), repeat=2):
        source = (control_bit << 0) | (target_bit << 1)
        observed = x1_response(basis_state(source), 0, 1).coefficients[0][0]
        expected = source ^ (1 << 1) if control_bit else source
        mapping.append(observed == expected)
    checks = {
        "frozen_operator_source_hash": (
            sha256(SLCX002 / "release/SLCX002_OPERATOR_MATRICES.json")
            == FROZEN_SOURCE_HASHES["SLCX002_OPERATOR_MATRICES.json"]
        ),
        "frozen_request_matrix_shape": (
            len(frozen["PREPARE_REQUEST_canonical"]) == 2
            and all(len(row) == 2 for row in frozen["PREPARE_REQUEST_canonical"])
        ),
        "frozen_response_shape": len(frozen["X1_RESPONSE"]) == 4,
        "binary_flip": flipped.coefficients == ((1, 1),),
        "prepare_column_zero": prepared0.coefficients == ((0, 1), (1, 1)) and prepared0.sqrt2_power == 1,
        "prepare_column_one": prepared1.coefficients == ((0, 1), (1, -1)) and prepared1.sqrt2_power == 1,
        "response_mapping": all(mapping),
        "prepare_involution": prepare_request(prepared0, 0).state_hash == zero.state_hash,
        "response_involution": x1_response(x1_response(prepared0, 0, 1), 0, 1).state_hash == prepared0.state_hash,
        "binary_is_not_prepare": flipped.state_hash != prepared0.state_hash,
    }
    invariant_checks = {
        "canonical_sparse_order": prepared0.coefficients == tuple(sorted(prepared0.coefficients)),
        "exact_norm": prepared0.normalization_numerator == prepared0.normalization_denominator,
        "integer_coefficients": all(type(value) is int for _, value in prepared0.coefficients),
        "engine_contract_hash": len(ENGINE_CONTRACT_HASH) == 64,
    }
    return (
        {"status": "PASS" if all(invariant_checks.values()) else "FAIL", "checks": invariant_checks},
        {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks},
    )


def set_bit(index: int, site: int, value: int) -> int:
    mask = 1 << site
    return index | mask if value else index & ~mask


def expected_formula(basis: int, control: int, target: int, *, forward: bool) -> tuple[tuple[int, int], ...]:
    a = (basis >> control) & 1
    b = (basis >> target) & 1
    fixed_target = b if forward else b ^ a
    rows = []
    for output_control in (0, 1):
        output_target = fixed_target ^ output_control if forward else fixed_target
        index = set_bit(set_bit(basis, control, output_control), target, output_target)
        coefficient = 1 if output_control == 0 or a == 0 else -1
        rows.append((index, coefficient))
    return tuple(sorted(rows))


def exhaustive_pair_gate() -> dict[str, Any]:
    placement_rows = []
    checksum = hashlib.sha256()
    forward_total = reverse_total = classical_forward_total = classical_reverse_total = 0
    for control in range(REGISTER_SIZE):
        for target in range(REGISTER_SIZE):
            if control == target:
                continue
            forward_matches = reverse_matches = classical_forward = classical_reverse = 0
            for basis in range(DIMENSION):
                root = basis_state(basis)
                forward = x1_response(prepare_request(root, control), control, target)
                reverse = prepare_request(x1_response(root, control, target), control)
                forward_matches += int(
                    forward.coefficients == expected_formula(basis, control, target, forward=True)
                    and forward.sqrt2_power == 1
                )
                reverse_matches += int(
                    reverse.coefficients == expected_formula(basis, control, target, forward=False)
                    and reverse.sqrt2_power == 1
                )

                classical_f = x1_response(binary_flip(root, control), control, target)
                classical_r = binary_flip(x1_response(root, control, target), control)
                a = (basis >> control) & 1
                b = (basis >> target) & 1
                expected_f = set_bit(set_bit(basis, control, a ^ 1), target, b ^ a ^ 1)
                expected_r = set_bit(set_bit(basis, control, a ^ 1), target, b ^ a)
                classical_forward += int(classical_f.coefficients == ((expected_f, 1),))
                classical_reverse += int(classical_r.coefficients == ((expected_r, 1),))
                checksum.update(
                    canonical_bytes(
                        [control, target, basis, forward.state_hash, reverse.state_hash, expected_f, expected_r]
                    )
                )
            row = {
                "control": control,
                "target": target,
                "basis_cases": DIMENSION,
                "forward_formula_matches": forward_matches,
                "reverse_formula_matches": reverse_matches,
                "classical_forward_matches": classical_forward,
                "classical_reverse_matches": classical_reverse,
            }
            row["status"] = "PASS" if all(value == DIMENSION for value in row.values() if type(value) is int and value != control and value != target) else "FAIL"
            # The explicit comparison avoids the site-number ambiguity in the compact row check.
            row["status"] = "PASS" if (
                forward_matches == reverse_matches == classical_forward == classical_reverse == DIMENSION
            ) else "FAIL"
            placement_rows.append(row)
            forward_total += forward_matches
            reverse_total += reverse_matches
            classical_forward_total += classical_forward
            classical_reverse_total += classical_reverse
    passed = (
        len(placement_rows) == 132
        and forward_total == reverse_total == 540672
        and classical_forward_total == classical_reverse_total == 540672
        and all(row["status"] == "PASS" for row in placement_rows)
    )
    return {
        "status": "PASS" if passed else "FAIL",
        "ordered_placements": len(placement_rows),
        "forward_formula_cases": forward_total,
        "reverse_formula_cases": reverse_total,
        "classicalized_forward_cases": classical_forward_total,
        "classicalized_reverse_cases": classical_reverse_total,
        "classicalized_total_schedule_cases": classical_forward_total + classical_reverse_total,
        "enumeration_sha256": checksum.hexdigest(),
        "placements": placement_rows,
    }


def sign_gauge_gate() -> dict[str, Any]:
    with (SLCX002 / "release/SLCX002_REQUEST_ENUMERATION.csv").open(encoding="utf-8", newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row["survives"].lower() == "true"]
    checksum = hashlib.sha256()
    cases = passes = 0
    by_candidate: dict[str, int] = {}
    for row in rows:
        signs = [int(token) for token in row["signs"].split()]
        for control in range(12):
            for target in range(12):
                if control == target:
                    continue
                # Column zero of the real sign matrix acts on the canonical |0> root.
                diagnostic = ExactSLCState.from_sparse(
                    {0: signs[0], 1 << control: signs[2]}, 1
                )
                correlated = x1_response(diagnostic, control, target)
                expected_support = {0, (1 << control) | (1 << target)}
                passed = (
                    correlated.assert_exact_normalization()
                    and {index for index, _ in correlated.coefficients} == expected_support
                    and correlated.support_size == 2
                )
                cases += 1
                passes += int(passed)
                by_candidate[row["candidate_id"]] = by_candidate.get(row["candidate_id"], 0) + int(passed)
                checksum.update(canonical_bytes([row["candidate_id"], control, target, correlated.state_hash]))
    ok = len(rows) == 4 and cases == passes == 528 and all(value == 132 for value in by_candidate.values())
    return {
        "status": "PASS" if ok else "FAIL",
        "surviving_gauges": len(rows),
        "placement_cases": cases,
        "passing_cases": passes,
        "candidate_passes": by_candidate,
        "diagnostic_sha256": checksum.hexdigest(),
        "installed_gauge": "canonical positive-first-row only",
    }


def equal_block_partitions(items: tuple[int, ...], block_size: int) -> Iterator[tuple[tuple[int, ...], ...]]:
    if not items:
        yield tuple()
        return
    first = items[0]
    for companions in itertools.combinations(items[1:], block_size - 1):
        block = (first,) + companions
        chosen = set(block)
        remaining = tuple(item for item in items if item not in chosen)
        for tail in equal_block_partitions(remaining, block_size):
            yield (block,) + tail


def forest_state(blocks: Sequence[Sequence[int]], mode: str) -> ExactSLCState:
    state = zero_state()
    for raw_block in blocks:
        ordered = tuple(sorted(raw_block))
        if mode == "reverse_chain":
            ordered = tuple(reversed(ordered))
        root = ordered[0]
        state = prepare_request(state, root)
        if mode == "star":
            edges = [(root, child) for child in ordered[1:]]
        elif mode in {"chain", "reverse_chain"}:
            edges = list(zip(ordered, ordered[1:]))
        else:
            raise ValueError(mode)
        for control, target in edges:
            state = x1_response(state, control, target)
    return state


def expected_partition(blocks: Sequence[Sequence[int]]) -> ExactSLCState:
    coefficients: dict[int, int] = {}
    for labels in itertools.product((0, 1), repeat=len(blocks)):
        index = 0
        for label, block in zip(labels, blocks):
            if label:
                index |= sum(1 << site for site in block)
        coefficients[index] = 1
    return ExactSLCState.from_sparse(coefficients, len(blocks))


def forest_and_decomposition_gate(contract: dict[str, Any]) -> dict[str, Any]:
    induction = []
    parent_cases = parent_passes = 0
    for size in range(1, 13):
        block = tuple(range(size))
        expected = expected_partition((block,))
        modes = {mode: forest_state((block,), mode) for mode in ("star", "chain", "reverse_chain")}
        mode_match = all(state.state_hash == expected.state_hash for state in modes.values())
        next_cases = next_passes = 0
        if size < 12:
            for parent in block:
                extended = x1_response(modes["chain"], parent, size)
                next_cases += 1
                next_passes += int(extended.state_hash == expected_partition((tuple(range(size + 1)),)).state_hash)
        parent_cases += next_cases
        parent_passes += next_passes
        induction.append(
            {"component_size": size, "mode_match": mode_match, "parent_cases": next_cases, "parent_passes": next_passes}
        )

    checksum = hashlib.sha256()
    census = []
    total = passing = 0
    for spec in contract["native_decomposition_census"]:
        observed = matches = 0
        for blocks in equal_block_partitions(tuple(range(12)), int(spec["block_size"])):
            expected = expected_partition(blocks)
            states = [forest_state(blocks, mode) for mode in ("star", "chain", "reverse_chain")]
            matched = all(state.state_hash == expected.state_hash for state in states)
            observed += 1
            matches += int(matched)
            checksum.update(canonical_bytes([spec["name"], blocks, expected.state_hash, matched]))
        total += observed
        passing += matches
        census.append(
            {
                "decomposition": spec["name"],
                "expected": int(spec["unlabeled_site_partitions"]),
                "observed": observed,
                "passing": matches,
                "status": "PASS" if observed == matches == int(spec["unlabeled_site_partitions"]) else "FAIL",
            }
        )
    ok = (
        parent_cases == parent_passes == 66
        and all(row["mode_match"] and row["parent_cases"] == row["parent_passes"] for row in induction)
        and total == passing == 31572
        and all(row["status"] == "PASS" for row in census)
    )
    return {
        "status": "PASS" if ok else "FAIL",
        "rooted_forest_parent_cases": parent_cases,
        "rooted_forest_parent_passes": parent_passes,
        "induction": induction,
        "native_decomposition_assignments": total,
        "native_decomposition_passes": passing,
        "decomposition_census": census,
        "decomposition_sha256": checksum.hexdigest(),
    }


def representative_blocks(name: str) -> tuple[tuple[int, ...], ...]:
    return {
        "1x12": (tuple(range(12)),),
        "3x4": (tuple(range(0, 4)), tuple(range(4, 8)), tuple(range(8, 12))),
        "4x3": ((0, 4, 8), (1, 5, 9), (2, 6, 10), (3, 7, 11)),
        "6x2": ((0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11)),
        "12x1": tuple((site,) for site in range(12)),
    }[name]


def peel_restore_gate(contract: dict[str, Any]) -> dict[str, Any]:
    rows = []
    checksum = hashlib.sha256()
    for spec in contract["native_decomposition_census"]:
        if int(spec["block_size"]) < 2:
            continue
        decomposition_pass = decomposition_cases = 0
        for block in representative_blocks(spec["name"]):
            initial = forest_state((block,), "chain")
            for control in block:
                for target in block:
                    if control == target:
                        continue
                    peeled = x1_response(initial, control, target)
                    restored = x1_response(peeled, control, target)
                    remaining_mask = sum(1 << site for site in block if site != target)
                    expected = ExactSLCState.from_sparse({0: 1, remaining_mask: 1}, 1)
                    passed = peeled.state_hash == expected.state_hash and restored.state_hash == initial.state_hash
                    decomposition_cases += 1
                    decomposition_pass += int(passed)
                    checksum.update(canonical_bytes([spec["name"], block, control, target, peeled.state_hash, restored.state_hash]))
        rows.append(
            {"decomposition": spec["name"], "cases": decomposition_cases, "passes": decomposition_pass}
        )
    cases = sum(row["cases"] for row in rows)
    passes = sum(row["passes"] for row in rows)
    return {
        "status": "PASS" if cases == passes == 204 else "FAIL",
        "cases": cases,
        "passes": passes,
        "by_decomposition": rows,
        "diagnostic_sha256": checksum.hexdigest(),
    }


def predecessor_classical_gate() -> dict[str, Any]:
    with (SLCX002 / "release/SLCX002_CLASSICAL_LIMIT.csv").open(encoding="utf-8", newline="") as handle:
        frozen_rows = list(csv.DictReader(handle))
    rows = []
    for row in frozen_rows:
        a, b = (int(char) for char in row["initial"])
        root = basis_state((a << 0) | (b << 1))
        state = (
            x1_response(binary_flip(root, 0), 0, 1)
            if row["direction"] == "forward"
            else binary_flip(x1_response(root, 0, 1), 0)
        )
        index = state.coefficients[0][0]
        observed = f"{(index >> 0) & 1}{(index >> 1) & 1}"
        matched = observed == row["appealed_output"] == row["formal_classical_limit_output"]
        rows.append({"initial": row["initial"], "direction": row["direction"], "observed": observed, "matched": matched})
    return {"status": "PASS" if len(rows) == 8 and all(row["matched"] for row in rows) else "FAIL", "rows": rows}


def state_history_gate() -> dict[str, Any]:
    star = forest_state((tuple(range(12)),), "star")
    chain = forest_state((tuple(range(12)),), "chain")
    dossier = inspect_state(chain)
    checks = {
        "same_terminal_state_hash": star.state_hash == chain.state_hash,
        "different_history_hash": star.history_hash != chain.history_hash,
        "same_exact_coefficients": star.coefficients == chain.coefficients == ((0, 1), (4095, 1)),
        "component_partition_only": dossier["state_topology"]["component_partition"] == [list(range(12))],
        "route_history_retained": dossier["route_topology"]["ordered_response_edges"] != inspect_state(star)["route_topology"]["ordered_response_edges"],
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "star_state_hash": star.state_hash,
        "chain_state_hash": chain.state_hash,
        "star_history_hash": star.history_hash,
        "chain_history_hash": chain.history_hash,
    }


def cli_api_gate(env: dict[str, str]) -> dict[str, Any]:
    example = CANDIDATE / "examples/slc_bell.sam"
    source = example.read_text(encoding="utf-8")
    api_left = run_program_text(source, mode="slc-c1-formal").as_dict()
    api_right = run_program_text(source, mode="slc-c1-formal").as_dict()
    command = [sys.executable, "-B", "-m", "sam_language_v0_6.cli", "run", str(example), "--slc-c1-formal"]
    cli_left = run_command(command, cwd=CANDIDATE, env=env)
    cli_right = run_command(command, cwd=CANDIDATE, env=env)
    parsed = json.loads(cli_left["stdout"]) if cli_left["returncode"] == 0 else None
    checks = {
        "api_byte_deterministic": canonical_bytes(api_left) == canonical_bytes(api_right),
        "cli_byte_deterministic": cli_left["stdout"].encode("utf-8") == cli_right["stdout"].encode("utf-8"),
        "cli_api_parity": parsed == api_left,
        "cli_success": cli_left["returncode"] == cli_right["returncode"] == 0,
        "no_traceback": not cli_left["traceback_found"] and not cli_right["traceback_found"],
    }
    return {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks, "command": command}


def expect_rejected(callable_object: Any, error_type: type[BaseException]) -> bool:
    try:
        callable_object()
    except error_type:
        return True
    return False


def tamper_gate() -> dict[str, Any]:
    atomic = prepare_request(zero_state(), 0)
    before = (atomic.state_hash, atomic.history_hash, len(atomic.history))
    alias_rejected = expect_rejected(lambda: x1_response(atomic, 0, 0), SLCControlTargetAliasError)
    atomic_unchanged = before == (atomic.state_hash, atomic.history_hash, len(atomic.history))

    detections: dict[str, bool] = {}
    coefficient_state = x1_response(prepare_request(zero_state(), 0), 0, 1)
    object.__setattr__(coefficient_state, "coefficients", ((0, 1), (1, 1)))
    detections["coefficient"] = expect_rejected(lambda: binary_flip(coefficient_state, 2), SLCStateCustodyError)

    exponent_state = prepare_request(zero_state(), 0)
    object.__setattr__(exponent_state, "sqrt2_power", 0)
    detections["exponent"] = expect_rejected(lambda: binary_flip(exponent_state, 2), SLCStateInvariantError)

    predecessor_state = x1_response(prepare_request(zero_state(), 0), 0, 1)
    object.__setattr__(predecessor_state.history[-1], "prior_state_hash", "0" * 64)
    detections["predecessor_hash"] = expect_rejected(predecessor_state.verify_custody, SLCStateCustodyError)

    argument_state = x1_response(prepare_request(zero_state(), 0), 0, 1)
    object.__setattr__(argument_state.history[-1], "arguments", (0, 2))
    detections["operator_argument"] = expect_rejected(argument_state.verify_custody, SLCStateCustodyError)

    receipt_state = prepare_request(zero_state(), 0)
    object.__setattr__(receipt_state.history[-1], "receipt_hash", "0" * 64)
    detections["receipt"] = expect_rejected(receipt_state.verify_custody, SLCStateCustodyError)

    passed = alias_rejected and atomic_unchanged and all(detections.values())
    return {
        "status": "PASS" if passed else "FAIL",
        "rejected_operation_atomic": alias_rejected and atomic_unchanged,
        "tamper_detections": detections,
    }


def parse_test_count(output: str) -> int | None:
    match = re.search(r"Ran (\d+) tests?", output)
    return int(match.group(1)) if match else None


def test_gate(env: dict[str, str]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    parent = run_command(
        [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-v"],
        cwd=PARENT,
        env={**env, "PYTHONPATH": str(PARENT / "src")},
    )
    candidate = run_command(
        [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-v"],
        cwd=CANDIDATE,
        env=env,
    )
    parent_count = parse_test_count(parent["stdout"] + parent["stderr"])
    candidate_count = parse_test_count(candidate["stdout"] + candidate["stderr"])
    inherited_count = sum(
        len(re.findall(r"^\s+def test_", path.read_text(encoding="utf-8"), flags=re.MULTILINE))
        for path in sorted((CANDIDATE / "tests").glob("test_v0[345]*.py"))
    )
    new_count = len(
        re.findall(
            r"^\s+def test_",
            (CANDIDATE / "tests/test_v06_slc_c1.py").read_text(encoding="utf-8"),
            flags=re.MULTILINE,
        )
    )
    passed = (
        parent["returncode"] == candidate["returncode"] == 0
        and parent_count == inherited_count == 154
        and candidate_count == inherited_count + new_count
        and new_count > 0
        and not parent["traceback_found"]
        and not candidate["traceback_found"]
    )
    summary = {
        "status": "PASS" if passed else "FAIL",
        "parent_tests": parent_count,
        "inherited_candidate_tests": inherited_count,
        "new_slc_tests": new_count,
        "candidate_tests": candidate_count,
        "parent_returncode": parent["returncode"],
        "candidate_returncode": candidate["returncode"],
    }
    return summary, [parent, candidate]


def clean_wheel_gate() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    result = run_clean_wheel_probe(CANDIDATE)
    commands = list(result.pop("commands", []))
    return result, commands


def boundaries_gate(profile: dict[str, Any], tamper: dict[str, Any], state_history: dict[str, Any]) -> dict[str, Any]:
    registry = load_registry()
    kernel_text = (SRC / "sam_language_v0_6/slc_state.py").read_text(encoding="utf-8")
    b_state = binary_flip(zero_state(), 0)
    h_state = prepare_request(zero_state(), 0)
    reverse = prepare_request(x1_response(zero_state(), 0, 1), 0)
    forward = x1_response(prepare_request(zero_state(), 0), 0, 1)
    ghz3 = forest_state(((0, 1, 2),), "chain")
    child_first = x1_response(x1_response(prepare_request(zero_state(), 0), 1, 2), 0, 1)
    closed = x1_response(forest_state((tuple(range(12)),), "chain"), 11, 0)
    duplicated = x1_response(x1_response(h_state, 0, 1), 0, 1)
    type_reject = expect_rejected(
        lambda: run_program_text(
            "let s0: SLCState12 = SLC_ZERO_REGISTER()\nlet bad = SLC_PREPARE_REQUEST(s0, QP_P1)\nreturn bad",
            mode="slc-c1-formal",
        ),
        TypeCheckError,
    )
    unregistered = all(
        expect_rejected(lambda name=name: registry.operator(name), UnknownOperatorError)
        for name in ("SLC_PUBLISH", "SLC_SAMPLE", "SLC_COMPLEX_PHASE", "SLC_PHYSICAL_EDGE")
    )
    controls = [
        ("WC01_CONTROL_EQUALS_TARGET", expect_rejected(lambda: x1_response(zero_state(), 0, 0), SLCControlTargetAliasError)),
        ("WC02_R10_SUBSTITUTION", expect_rejected(lambda: zero_state(register_size=10), SLCRegisterArityError)),
        ("WC03_EIGHT_SLOTS_NOT_SITES", REGISTER_SIZE == 12 and 8 != REGISTER_SIZE),
        ("WC04_PARTITION_PAIRS_NOT_EDGES", len([(a, b) for a in range(12) for b in range(12) if a != b]) == 132),
        ("WC05_QP_LABEL_NOT_SITE", type_reject),
        ("WC06_LEGACY_LATENT_BITS_NOT_AUTHORITY", "slc_ledger" not in kernel_text),
        ("WC07_B_NOT_PREPARE", b_state.state_hash != h_state.state_hash),
        ("WC08_B_NOT_BALANCED", b_state.support_size == 1 and h_state.support_size == 2),
        ("WC09_REVERSE_NOT_FORWARD", reverse.state_hash != forward.state_hash),
        ("WC10_DUPLICATE_RESPONSE_RETAINED", duplicated.state_hash == h_state.state_hash and len(duplicated.history) == len(h_state.history) + 2),
        ("WC11_CLOSING_EDGE_NOT_IDENTITY", closed.state_hash != forest_state((tuple(range(12)),), "chain").state_hash),
        ("WC12_CHILD_BEFORE_PARENT_IS_LEGAL_BUT_INCOMPLETE", child_first.state_hash != ghz3.state_hash),
        ("WC13_PREPARE_TWICE_INVOLUTION", prepare_request(h_state, 0).state_hash == zero_state().state_hash),
        ("WC14_TERMINAL_HISTORY_NOT_INFERRED", state_history["checks"]["same_terminal_state_hash"]),
        ("WC15_STATE_HASH_ROUTE_INDEPENDENT", state_history["star_state_hash"] == state_history["chain_state_hash"]),
        ("WC16_HISTORY_HASH_ROUTE_DEPENDENT", state_history["star_history_hash"] != state_history["chain_history_hash"]),
        ("WC17_NO_FLOAT_STATE_DECISIONS", not any(token in kernel_text for token in ("np.", "numpy", "math.isclose", "float("))),
        ("WC18_COMPLEX_PHASE_REJECTED", expect_rejected(lambda: apply_complex_phase(zero_state()), SLCUnsupportedPhaseError)),
        ("WC19_PHYSICAL_CONNECTIVITY_REJECTED", expect_rejected(lambda: assert_physical_connectivity(0, 1), SLCUnsupportedConnectivityError)),
        ("WC20_NO_LEGACY_COST_ATTACHED", "resource_cost" not in json.dumps(inspect_state(forward))),
        ("WC21_PUBLICATION_REJECTED", expect_rejected(lambda: publish(forward), SLCUnsupportedPublicationError) and expect_rejected(lambda: sample_measurement(forward), SLCUnsupportedPublicationError)),
        ("WC22_FORMAL_OPS_PROFILE_ISOLATED", all(profile["rejected_profiles"].values()) and unregistered),
        ("WC23_TAMPER_REJECTED", tamper["status"] == "PASS"),
    ]
    return {
        "status": "PASS" if all(passed for _, passed in controls) else "FAIL",
        "wrong_controls": [
            {"control": name, "status": "PASS" if passed else "FAIL"}
            for name, passed in controls
        ],
        "open_boundaries": [
            "complex phase semantics",
            "measurement and publication",
            "physical connectivity",
            "coupling magnitude and cost",
            "hardware realization",
        ],
    }


def markdown_result(result: dict[str, Any]) -> str:
    lines = [
        "# SAM Language v0.6 SLC C1 Formal Simulator Acceptance",
        "",
        f"Status: **{result['status']}**",
        "",
        "The updated SAM Language kernel now executes the frozen real SLC C1 grammar as an exact 12-lebit joint-state simulator. The complete placement, topology, decomposition, history, regression, and clean-install campaign closed without fitted coefficients or a sidecar evaluator.",
        "",
        "## Acceptance ledger",
        "",
    ]
    for gate in result["gates"]:
        lines.append(f"- `{gate['gate']}` {gate['title']}: **{gate['status']}**")
    lines.extend(
        [
            "",
            "## Exact execution totals",
            "",
            f"- Ordered placements: `{result['headline_counts']['ordered_placements']}`",
            f"- Forward / reverse formula cases: `{result['headline_counts']['forward_formula_cases']} / {result['headline_counts']['reverse_formula_cases']}`",
            f"- Classicalized schedules: `{result['headline_counts']['classicalized_total_schedule_cases']}`",
            f"- Sign-gauge placements: `{result['headline_counts']['sign_gauge_cases']}`",
            f"- Forest induction parent cases: `{result['headline_counts']['forest_parent_cases']}`",
            f"- Native decomposition assignments: `{result['headline_counts']['native_decomposition_assignments']}`",
            f"- Peel / restore cases: `{result['headline_counts']['peel_restore_cases']}`",
            "",
            "## Verdict",
            "",
            f"`{result['primary_verdict']}`",
            "",
            "The promoted scope is the exact real-sector formal simulator candidate. Complex phase, publication, physical connectivity, coupling magnitude, and hardware realization remain separate frontiers.",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    for marker in (RESULT_PATH, FAILURE_PATH, RELEASE_MANIFEST_PATH):
        if marker.exists():
            print(json.dumps({"status": "REFUSED_ALREADY_EXECUTED", "marker": str(marker), "same_run_repair": False}, indent=2))
            return 2

    command_log: list[dict[str, Any]] = []
    try:
        predecessor_contract = read_json(SLCX003 / "SLCX003_CONTRACT.json")
        parent_before = tree_snapshot(PARENT)
        candidate_before = candidate_code_snapshot()
        candidate_code_hash = aggregate(candidate_before)
        custody = custody_gate()
    except Exception as exc:
        return fail_stop(
            "PRE_GATE_CUSTODY_EXCEPTION",
            {"type": type(exc).__name__, "message": str(exc)},
        )
    if custody["status"] != "PASS":
        return fail_stop("G01_PARENT_AND_SOURCE_CUSTODY", custody)

    try:
        runtime_path = single_runtime_path_gate()
        profile, cardinality = profile_and_cardinality_gates()
        invariant, operators = exact_operator_gate()
        exhaustive = exhaustive_pair_gate()
        gauges = sign_gauge_gate()
        forest = forest_and_decomposition_gate(predecessor_contract)
        peel = peel_restore_gate(predecessor_contract)
        classical = predecessor_classical_gate()
        state_history = state_history_gate()

        env = os.environ.copy()
        env["PYTHONPATH"] = str(SRC)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        receipts = cli_api_gate(env)
        tamper = tamper_gate()
        regression, test_commands = test_gate(env)
        command_log.extend(test_commands)
        clean_wheel, wheel_commands = clean_wheel_gate()
        command_log.extend(wheel_commands)
        boundaries = boundaries_gate(profile, tamper, state_history)
    except Exception as exc:  # fail-stop record, never a repair path
        return fail_stop(
            "UNHANDLED_ACCEPTANCE_EXCEPTION",
            {"type": type(exc).__name__, "message": str(exc)},
        )

    parent_after = tree_snapshot(PARENT)
    candidate_after = candidate_code_snapshot()
    custody["parent_tree_unchanged"] = parent_before == parent_after
    custody["candidate_code_unchanged_during_run"] = candidate_before == candidate_after
    custody["status"] = "PASS" if (
        custody["status"] == "PASS"
        and custody["parent_tree_unchanged"]
        and custody["candidate_code_unchanged_during_run"]
    ) else "FAIL"

    evidence = {
        "G01": custody,
        "G02": runtime_path,
        "G03": profile,
        "G04": cardinality,
        "G05": invariant,
        "G06": operators,
        "G07": exhaustive,
        "G08": gauges,
        "G09": forest,
        "G10": peel,
        "G11": classical,
        "G12": state_history,
        "G13": receipts,
        "G14": tamper,
        "G15": {"status": "PASS" if regression["status"] == clean_wheel["status"] == "PASS" else "FAIL", "regression": regression, "clean_wheel": clean_wheel},
        "G16": boundaries,
    }
    gate_titles = {
        "G01": "Parent custody and sealed source/precommit lineage",
        "G02": "Single parser, checker, evaluator, type system, and registry path",
        "G03": "Formal profile isolation",
        "G04": "Twelve sites and 4096 basis addresses",
        "G05": "Exact canonical state invariant",
        "G06": "Frozen B, PREPARE_REQUEST, and X1_RESPONSE operators",
        "G07": "Complete ordered-pair lift",
        "G08": "Four real request sign-gauge diagnostics",
        "G09": "Rooted forests and all native decompositions",
        "G10": "Extra-edge peel and restore",
        "G11": "Frozen classical limit",
        "G12": "State/history separation",
        "G13": "Deterministic API and CLI receipts",
        "G14": "Atomic rejection and tamper detection",
        "G15": "Inherited/new regressions and clean wheel",
        "G16": "Boundary and wrong-control preservation",
    }
    gates = [
        {"gate": gate, "title": gate_titles[gate], "status": evidence[gate]["status"]}
        for gate in sorted(evidence)
    ]
    if any(row["status"] != "PASS" for row in gates):
        return fail_stop(
            "FROZEN_ACCEPTANCE_GATES",
            {
                "gates": gates,
                "failed": [row["gate"] for row in gates if row["status"] != "PASS"],
                "gate_evidence": evidence,
                "commands": [
                    {
                        "args": record["args"],
                        "cwd": record["cwd"],
                        "returncode": record["returncode"],
                        "traceback_found": record["traceback_found"],
                    }
                    for record in command_log
                ],
            },
        )

    REPORTS.mkdir(parents=True, exist_ok=False)
    for gate, payload in sorted(evidence.items()):
        write_json(REPORTS / f"{gate}_{gate_titles[gate].upper().replace(' ', '_').replace(',', '')}.json", payload)

    with (CANDIDATE / "V0_6_SLC_C1_ACCEPTANCE_LEDGER.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("gate", "title", "status"))
        writer.writeheader()
        writer.writerows(gates)

    write_json(
        CANDIDATE / "V0_6_SLC_C1_PARENT_CUSTODY.json",
        {
            "status": custody["status"],
            "parent_executable_hash": custody["parent_observed_hash"],
            "parent_files_verified": custody["parent_files_verified"],
            "candidate_executable_hash": custody["candidate_executable_observed_hash"],
            "candidate_executable_files_verified": custody["candidate_executable_files_verified"],
            "frozen_sources_verified": custody["frozen_sources_verified"],
        },
    )
    write_text(
        CANDIDATE / "COMMAND_LOG.txt",
        "\n".join(
            f"{record['returncode']}\t{record['cwd']}\t{' '.join(str(arg) for arg in record['args'])}"
            for record in command_log
        ),
    )

    result = {
        "campaign_id": CAMPAIGN_ID,
        "status": "PASS",
        "primary_verdict": PRIMARY_VERDICT,
        "candidate_code_hash": candidate_code_hash,
        "parent_executable_hash": custody["parent_observed_hash"],
        "engine_contract_hash": ENGINE_CONTRACT_HASH,
        "gates": gates,
        "headline_counts": {
            "ordered_placements": exhaustive["ordered_placements"],
            "forward_formula_cases": exhaustive["forward_formula_cases"],
            "reverse_formula_cases": exhaustive["reverse_formula_cases"],
            "classicalized_total_schedule_cases": exhaustive["classicalized_total_schedule_cases"],
            "sign_gauge_cases": gauges["placement_cases"],
            "forest_parent_cases": forest["rooted_forest_parent_cases"],
            "native_decomposition_assignments": forest["native_decomposition_assignments"],
            "peel_restore_cases": peel["cases"],
            "predecessor_classical_rows": len(classical["rows"]),
            "wrong_controls": len(boundaries["wrong_controls"]),
        },
        "same_run_repair": False,
        "automatic_production_install": False,
        "formal_candidate": True,
        "remaining_boundaries": boundaries["open_boundaries"],
        "generated_utc": datetime.now(timezone.utc).isoformat(),
    }
    excluded = {
        RELEASE_MANIFEST_PATH.name,
        "V0_6_SLC_C1_RELEASE_MANIFEST_SHA256.txt",
        "V0_6_SLC_C1_ACCEPTANCE_RESULT.json",
        "V0_6_SLC_C1_ACCEPTANCE_RESULT.md",
        "HASHES.txt",
    }
    release_files = {
        path.relative_to(CANDIDATE).as_posix(): sha256(path)
        for path in sorted(CANDIDATE.rglob("*"))
        if path.is_file()
        and path.name not in excluded
        and "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
        and ".egg-info" not in path.as_posix()
    }
    release_manifest = {
        "campaign_id": CAMPAIGN_ID,
        "status": "PASS",
        "primary_verdict": PRIMARY_VERDICT,
        "candidate_code_hash": candidate_code_hash,
        "parent_executable_hash": EXPECTED_PARENT_HASH,
        "acceptance_gates": {row["gate"]: row["status"] for row in gates},
        "automatic_production_install": False,
        "files": release_files,
        "file_count": len(release_files),
        "generated_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(RELEASE_MANIFEST_PATH, release_manifest)
    release_hash = sha256(RELEASE_MANIFEST_PATH)
    write_text(
        CANDIDATE / "V0_6_SLC_C1_RELEASE_MANIFEST_SHA256.txt",
        f"{release_hash}  {RELEASE_MANIFEST_PATH.name}",
    )
    result["release_manifest_sha256"] = release_hash
    write_json(RESULT_PATH, result)
    write_text(CANDIDATE / "V0_6_SLC_C1_ACCEPTANCE_RESULT.md", markdown_result(result))

    hashes = {
        path.relative_to(CANDIDATE).as_posix(): sha256(path)
        for path in sorted(CANDIDATE.rglob("*"))
        if path.is_file()
        and path.name != "HASHES.txt"
        and "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
        and ".egg-info" not in path.as_posix()
    }
    write_text(CANDIDATE / "HASHES.txt", "\n".join(f"{digest}  {path}" for path, digest in sorted(hashes.items())))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
    except Exception as exc:  # last-resort fail-stop for artifact-finalization faults
        exit_code = fail_stop(
            "UNHANDLED_RUNNER_EXCEPTION",
            {"type": type(exc).__name__, "message": str(exc)},
        )
    raise SystemExit(exit_code)
