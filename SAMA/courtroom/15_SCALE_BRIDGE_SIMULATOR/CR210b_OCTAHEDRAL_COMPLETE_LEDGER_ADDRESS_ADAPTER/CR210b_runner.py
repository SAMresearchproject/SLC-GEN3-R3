#!/usr/bin/env python3
"""CR210b serializer-corrected successor for the frozen CR210a algorithm.

The scientific algorithm body is loaded from the immutable CR210a runner and
verified byte-for-byte.  Only successor identity/contract administration and
JSON-safe check-display normalization are transformed before one execution.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
BASE_RUNNER = (
    ROOT
    / "15_SCALE_BRIDGE_SIMULATOR"
    / "CR210a_OCTAHEDRAL_COMPLETE_LEDGER_ADDRESS_ADAPTER"
    / "CR210a_runner.py"
)
EXPECTED_BASE_SHA256 = "094d39be033db8dfe7bd1b78c845abf8839dbba1f36b31987af3d3bfb7616d1a"
TASK = (
    "Execute CR210b as a fresh successor to the frozen CR210a implementation "
    "failure, preserving the identical octahedral complete-ledger structural "
    "candidate, predictions, controls, source firewall, and verdict ceiling, "
    "correcting only expected-value set serialization, with outcomes and binding "
    "closed, and stop after one execution"
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replace_exact(source: str, old: str, new: str, expected_count: int = 1) -> tuple[str, int]:
    count = source.count(old)
    if count != expected_count:
        raise RuntimeError(
            f"administrative transform count mismatch: expected {expected_count}, "
            f"found {count} for {old!r}"
        )
    return source.replace(old, new), count


def main() -> int:
    base_bytes = BASE_RUNNER.read_bytes()
    base_hash = sha256(base_bytes)
    if base_hash != EXPECTED_BASE_SHA256:
        raise RuntimeError(
            f"immutable CR210a runner hash mismatch: {base_hash} != {EXPECTED_BASE_SHA256}"
        )
    source = base_bytes.decode("utf-8")
    substitutions: list[dict[str, object]] = []

    prefix_count = source.count("CR210a_")
    if prefix_count < 1:
        raise RuntimeError("CR210a successor prefix not found")
    source = source.replace("CR210a_", "CR210b_")
    substitutions.append(
        {
            "kind": "successor_identity",
            "occurrences": prefix_count,
            "scientific_algorithm_change": False,
        }
    )

    replacements = [
        (
            "dbf10c2802fdfc22c04e9b4a9db33f6797107c412eaa62a6e92c8282102cfe0c",
            "ac35e67bfa5905b20051c0e45b27de567116e6928492189932892ab37bf678f3",
            "successor_source_manifest_hash",
        ),
        (
            "26d3a407d498212460331fe837cc3900c18253f47ffb8ba07ada3cd85072ab93",
            "adb13e002dc394adaa279c59827eee789d71632eb1ccf12922183171f11290cf",
            "successor_premises_hash",
        ),
        (
            "55d583f6f7697a24e28d5a1031a4eeb329fe0680ed3548a3ea1d2f0ffe475b45",
            "a898c53609958556ae5a43e6c409bb0e32037c9c2b1042538e067f35d3b97224",
            "successor_precommit_hash",
        ),
    ]
    for old, new, label in replacements:
        source, count = replace_exact(source, old, new)
        substitutions.append(
            {
                "kind": label,
                "occurrences": count,
                "scientific_algorithm_change": False,
            }
        )

    source, count = replace_exact(
        source,
        'len(source_rows) == manifest["source_count"] == 17',
        'len(source_rows) == manifest["source_count"] == 20',
    )
    substitutions.append(
        {
            "kind": "successor_source_count_gate",
            "occurrences": count,
            "scientific_algorithm_change": False,
        }
    )
    source, count = replace_exact(
        source,
        '{"source_count": 17, "hash_and_byte_errors": 0}',
        '{"source_count": 20, "hash_and_byte_errors": 0}',
    )
    substitutions.append(
        {
            "kind": "successor_source_count_display",
            "occurrences": count,
            "scientific_algorithm_change": False,
        }
    )

    old_serializer = '''def compact_json(value: Any) -> str:
    return json.dumps(value, separators=(",", ":"), sort_keys=True)
'''
    new_serializer = '''def compact_json(value: Any) -> str:
    def normalize(item: Any) -> Any:
        if isinstance(item, dict):
            return {str(key): normalize(value) for key, value in item.items()}
        if isinstance(item, (set, frozenset)):
            return [normalize(value) for value in sorted(item, key=repr)]
        if isinstance(item, tuple):
            return [normalize(value) for value in item]
        if isinstance(item, list):
            return [normalize(value) for value in item]
        return item

    return json.dumps(normalize(value), separators=(",", ":"), sort_keys=True)
'''
    source, count = replace_exact(source, old_serializer, new_serializer)
    substitutions.append(
        {
            "kind": "set_safe_check_display_serializer",
            "occurrences": count,
            "scientific_algorithm_change": False,
        }
    )

    transformed_bytes = source.encode("utf-8")
    transform_contract = {
        "record_id": "CR210b_OCTAHEDRAL_COMPLETE_LEDGER_ADDRESS_ADAPTER",
        "base_runner_path": str(BASE_RUNNER),
        "base_runner_sha256": base_hash,
        "transformed_in_memory_sha256": sha256(transformed_bytes),
        "substitutions": substitutions,
        "scientific_candidate_changed": False,
        "predictions_changed": False,
        "controls_changed": False,
        "firewall_changed": False,
        "verdict_ceiling_changed_except_successor_prefix": False,
        "transformed_source_persisted": False,
    }
    (HERE / "CR210b_TRANSFORM_CONTRACT.json").write_text(
        json.dumps(transform_contract, indent=2) + "\n", encoding="utf-8"
    )

    namespace: dict[str, object] = {
        "__name__": "cr210b_inherited_core",
        "__file__": str(Path(__file__).resolve()),
        "__builtins__": __builtins__,
    }
    exec(compile(source, str(Path(__file__).resolve()), "exec"), namespace)
    namespace["TASK"] = TASK
    return int(namespace["main"]())  # type: ignore[operator]


if __name__ == "__main__":
    raise SystemExit(main())
