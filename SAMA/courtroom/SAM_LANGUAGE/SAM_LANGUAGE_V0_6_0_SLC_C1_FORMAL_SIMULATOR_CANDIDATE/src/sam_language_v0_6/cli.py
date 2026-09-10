"""Command-line interface for the SAM Language v0.6.0 C1 candidate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .errors import CLIUsageError, InternalCLIError, SamLanguageError
from .runtime import (
    SOURCE_RECORDS,
    VALID_CLOSURE_PROGRAM,
    check_program,
    entity_trace,
    explain_operator,
    load_registry,
    parse_program,
    registry_payload,
    run_program_text,
    sources_for_entity,
    sources_for_operator,
    _serialize_exact,
)
from .registry_qp import (
    enumerate_qp_productions,
    grammar_census,
    inspect_qp_production,
    verify_qp_native_inverse,
    verify_qp_native_reconciliation,
    verify_qp_source_reconciliation,
)


def _emit(payload: object, *, stream=None) -> None:
    print(json.dumps(_serialize_exact(payload), indent=2, sort_keys=True), file=stream or sys.stdout)


def _read_source(path: str | None) -> str:
    if path is None:
        return VALID_CLOSURE_PROGRAM
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise CLIUsageError(f"Unable to read SAM source file '{path}': {exc.strerror or exc}") from exc


def _execution_mode(args: argparse.Namespace) -> str:
    if getattr(args, "slc_c1_formal", False):
        return "slc-c1-formal"
    if getattr(args, "research", False):
        return "research"
    return "normal"


def cmd_check(args: argparse.Namespace) -> int:
    source = _read_source(args.file)
    checked = check_program(parse_program(source), mode=_execution_mode(args))
    _emit({"status": "PASS", "return_entity": checked.return_entity.entity_id})
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    source = _read_source(args.file)
    result = run_program_text(source, mode=_execution_mode(args))
    _emit(result.as_dict())
    return 0


def cmd_trace(args: argparse.Namespace) -> int:
    if args.target and args.file:
        raise CLIUsageError("sam trace accepts either an ENTITY_ID or --file <program.sam>, not both")
    if args.target:
        _emit(entity_trace(args.target))
        return 0
    source = _read_source(args.file)
    result = run_program_text(source, mode=_execution_mode(args))
    _emit({"trace": result.trace, "source_trace": result.source_trace, "warnings": result.warnings})
    return 0


def cmd_trace_program(args: argparse.Namespace) -> int:
    source = _read_source(args.file)
    result = run_program_text(source, mode=_execution_mode(args))
    _emit({"trace": result.trace, "source_trace": result.source_trace, "warnings": result.warnings})
    return 0


def cmd_explain(args: argparse.Namespace) -> int:
    if args.operator_id:
        _emit(explain_operator(args.operator_id))
    else:
        payload = registry_payload()
        _emit({"hierarchy": {"entities": payload["entities"], "operators": payload["operators"]}})
    return 0


def cmd_sources(args: argparse.Namespace) -> int:
    if args.operator_id:
        _emit(sources_for_operator(args.operator_id))
    elif args.entity_id:
        _emit(sources_for_entity(args.entity_id))
    else:
        _emit({"sources": SOURCE_RECORDS})
    return 0


def cmd_validate_contract(args: argparse.Namespace) -> int:
    payload = registry_payload()
    required = {
        "H2_ARITY",
        "D3_DIMENSION",
        "R12_CLOSURE_RADIUS",
        "S8_BINARY_SURFACE",
        "X1_AXIS_SELF_CHANNEL",
        "W9_CLOSURE_WITNESS",
        "THETA18_NATIVE_BUDGET",
        "V27_VOLUME_CONTAINER",
        "F81_COMPLETED_FACE",
        "P80_PARTICLE_FACE_CONTENT",
        "M126_MATTER_CAPACITY",
        "N144_NATIVE_CLOSURE",
        "L162_FULL_LEDGER",
        "C1_ROAD_LIGHT_CARRIER",
        "P1_LIFT_BEARING_SUPPORT",
        "A1_HISTORICAL_ROW_PROXY",
        "A_OPERATOR",
        "B_CONTACT_OPERATOR",
        "QP_P1",
        "QP_P12",
        "QP_D0",
        "QP_D2",
        "QP_ROUTE_PLUS",
        "QP_ROUTE_NEUTRAL",
    }
    required.update({f"SLC_L{site}" for site in range(12)})
    missing = sorted(required - set(payload["entities"]))
    if missing:
        _emit({"status": "FAIL", "missing": missing})
        return 1
    registry = load_registry()
    alias_expectations = {
        "SCALAR_ONE_CARRIER": "C1_ROAD_LIGHT_CARRIER",
        "SCALAR_ONE_SUPPORT": "P1_LIFT_BEARING_SUPPORT",
        "HISTORICAL_A_FIELD_ROW_PROXY": "A1_HISTORICAL_ROW_PROXY",
    }
    alias_failures = {
        alias: registry.entity(alias).entity_id
        for alias, expected in alias_expectations.items()
        if registry.entity(alias).entity_id != expected
    }
    if alias_failures:
        _emit({"status": "FAIL", "alias_failures": alias_failures})
        return 1
    required_operators = {
        "QP_UNARY_DIRECT",
        "QP_UNARY_CONJUGATE",
        "QP_ORDERED_PAIR",
        "QP_UNORDERED_TRIAD",
        "QP_TRIAD_SURFACE_GATE",
        "QP_HIDDEN_SUPPORT",
        "QP_CARRIER_TERMINAL",
        "QP_SCALAR_PARENT",
        "QP_EXPLICIT_CONTROL",
        "QP_NATIVE_SIGNATURE",
        "QP_NATIVE_ACCOUNT",
        "QP_SURFACE_DEBIT_OR_CREDIT",
        "QP_OBSERVED_CANDIDATE_ACCOUNT",
        "QP_SOURCE_SUPPORT",
        "QP_TENSOR_SUPPORT",
        "QP_RETAINED_SUPPORT",
        "SLC_ZERO_REGISTER",
        "SLC_BINARY_FLIP",
        "SLC_PREPARE_REQUEST",
        "SLC_X1_RESPONSE",
        "SLC_INSPECT_STATE",
    }
    missing_operators = sorted(required_operators - set(registry.operators))
    source = verify_qp_source_reconciliation()
    native = verify_qp_native_reconciliation()
    slc_metadata = registry.metadata.get("slc_c1", {})
    slc_failures = []
    if slc_metadata.get("register_size") != 12:
        slc_failures.append("register_size")
    if slc_metadata.get("state_dimension") != 4096:
        slc_failures.append("state_dimension")
    for name in (
        "SLC_ZERO_REGISTER",
        "SLC_BINARY_FLIP",
        "SLC_PREPARE_REQUEST",
        "SLC_X1_RESPONSE",
        "SLC_INSPECT_STATE",
    ):
        if name in registry.operators and registry.operators[name].required_mode != "slc-c1-formal":
            slc_failures.append(f"{name}.required_mode")
    if missing_operators or source["status"] != "PASS" or native["status"] != "PASS" or slc_failures:
        _emit(
            {
                "status": "FAIL",
                "missing_operators": missing_operators,
                "source_reconciliation": source,
                "native_reconciliation": native,
                "slc_failures": slc_failures,
            }
        )
        return 1
    _emit(
        {
            "status": "PASS",
            "required_entities": len(required),
            "required_qp_operators": len(required_operators),
            "aliases": alias_expectations,
            "source_reconciliation": source,
            "native_reconciliation": native,
            "slc_c1": slc_metadata,
        }
    )
    return 0


def cmd_regress(args: argparse.Namespace) -> int:
    valid = run_program_text(VALID_CLOSURE_PROGRAM)
    _emit({"status": "PASS", "return_entity": valid.entity_id, "scalar_value": valid.scalar_value})
    return 0


def cmd_grammar(args: argparse.Namespace) -> int:
    if args.grammar_command == "census":
        _emit(grammar_census())
    elif args.grammar_command == "enumerate":
        _emit({"status": "PASS", "productions": enumerate_qp_productions()})
    elif args.grammar_command == "inspect":
        _emit(inspect_qp_production(args.signature))
    elif args.grammar_command == "verify-source":
        _emit(verify_qp_source_reconciliation())
    elif args.grammar_command == "verify-native":
        _emit(verify_qp_native_reconciliation())
    elif args.grammar_command == "verify-native-inverse":
        _emit(verify_qp_native_inverse())
    else:
        raise CLIUsageError(f"Unknown grammar command: {args.grammar_command}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sam", description="SAM Language v0.6.0 exact SLC C1 simulator candidate CLI"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check")
    check.add_argument("file", nargs="?")
    check_profiles = check.add_mutually_exclusive_group()
    check_profiles.add_argument("--research", action="store_true")
    check_profiles.add_argument("--slc-c1-formal", action="store_true")
    check.set_defaults(func=cmd_check)

    run = sub.add_parser("run")
    run.add_argument("file", nargs="?")
    run_profiles = run.add_mutually_exclusive_group()
    run_profiles.add_argument("--research", action="store_true")
    run_profiles.add_argument("--slc-c1-formal", action="store_true")
    run.set_defaults(func=cmd_run)

    trace = sub.add_parser("trace")
    trace.add_argument("target", nargs="?", help="Registered ENTITY_ID or alias")
    trace.add_argument("--file", help="Trace an executable SAM source file instead of an entity")
    trace_profiles = trace.add_mutually_exclusive_group()
    trace_profiles.add_argument("--research", action="store_true")
    trace_profiles.add_argument("--slc-c1-formal", action="store_true")
    trace.set_defaults(func=cmd_trace)

    trace_program = sub.add_parser("trace-program")
    trace_program.add_argument("file")
    trace_program_profiles = trace_program.add_mutually_exclusive_group()
    trace_program_profiles.add_argument("--research", action="store_true")
    trace_program_profiles.add_argument("--slc-c1-formal", action="store_true")
    trace_program.set_defaults(func=cmd_trace_program)

    explain = sub.add_parser("explain")
    explain.add_argument("operator_id", nargs="?")
    explain.set_defaults(func=cmd_explain)

    sources = sub.add_parser("sources")
    sources.add_argument("entity_id", nargs="?")
    sources.add_argument("--operator", dest="operator_id")
    sources.set_defaults(func=cmd_sources)

    grammar = sub.add_parser("grammar")
    grammar_sub = grammar.add_subparsers(dest="grammar_command", required=True)
    for command in ("census", "enumerate", "verify-source", "verify-native", "verify-native-inverse"):
        grammar_sub.add_parser(command).set_defaults(func=cmd_grammar)
    inspect = grammar_sub.add_parser("inspect")
    inspect.add_argument("signature")
    inspect.set_defaults(func=cmd_grammar)

    sub.add_parser("validate-contract").set_defaults(func=cmd_validate_contract)
    sub.add_parser("regress").set_defaults(func=cmd_regress)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except SamLanguageError as exc:
        _emit({"status": "FAIL", "error": type(exc).__name__, "message": str(exc)}, stream=sys.stderr)
        return 2
    except Exception as exc:  # Never expose an implementation traceback through the CLI.
        translated = InternalCLIError(f"Unexpected CLI failure: {type(exc).__name__}: {exc}")
        _emit({"status": "FAIL", "error": type(translated).__name__, "message": str(translated)}, stream=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
