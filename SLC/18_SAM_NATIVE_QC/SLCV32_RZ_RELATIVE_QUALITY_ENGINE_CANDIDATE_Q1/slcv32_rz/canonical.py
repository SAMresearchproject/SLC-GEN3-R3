"""Exact JSON custody primitives for the SLCV32-RZ Q1 candidate.

Q1 uses integer/string JSON only.  Semantic identities therefore do not
depend on a Python floating-point implementation, whitespace, or object-key
insertion order.  The helpers are deliberately standalone so frozen E1/A1
artifacts can be verified as data before any predecessor package is imported.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Iterable, Mapping


SEMANTIC_SEAL_FIELD = "semantic_sha256"


class CanonicalError(ValueError):
    """An object is outside Q1's exact canonical JSON contract."""


def _reject_float(token: str) -> None:
    raise CanonicalError(f"floating-point JSON is prohibited: {token}")


def _reject_constant(token: str) -> None:
    raise CanonicalError(f"non-finite JSON is prohibited: {token}")


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise CanonicalError(f"duplicate JSON key is prohibited: {key}")
        value[key] = item
    return value


def _validate_value(value: Any, path: str = "$") -> None:
    if value is None or isinstance(value, (bool, int, str)):
        return
    if isinstance(value, float):
        raise CanonicalError(f"floating-point value is prohibited at {path}")
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _validate_value(item, f"{path}[{index}]")
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalError(f"non-string object key at {path}")
            _validate_value(item, f"{path}.{key}")
        return
    raise CanonicalError(f"unsupported canonical value {type(value).__name__} at {path}")


def canonical_bytes(value: Any) -> bytes:
    """Return Q1's byte-stable canonical JSON representation."""

    _validate_value(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha256(path: str | Path, chunk_size: int = 1 << 20) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        while block := handle.read(chunk_size):
            digest.update(block)
    return digest.hexdigest()


def semantic_body(value: Mapping[str, Any], field: str = SEMANTIC_SEAL_FIELD) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise CanonicalError("semantic seal requires an object")
    if not isinstance(field, str) or not field:
        raise CanonicalError("semantic seal field must be a non-empty string")
    return {key: item for key, item in value.items() if key != field}


def seal_dict(
    value: Mapping[str, Any], field: str = SEMANTIC_SEAL_FIELD
) -> dict[str, Any]:
    body = semantic_body(value, field)
    body[field] = canonical_sha256(body)
    return body


def verify_seal(value: Mapping[str, Any], field: str = SEMANTIC_SEAL_FIELD) -> bool:
    if not isinstance(value, Mapping):
        return False
    claimed = value.get(field)
    return (
        isinstance(claimed, str)
        and len(claimed) == 64
        and claimed == canonical_sha256(semantic_body(value, field))
    )


def require_seal(
    value: Mapping[str, Any], label: str, field: str = SEMANTIC_SEAL_FIELD
) -> None:
    if not verify_seal(value, field):
        raise CanonicalError(f"{label} {field} is invalid")


def loads_exact(data: str | bytes) -> Any:
    try:
        return json.loads(
            data,
            object_pairs_hook=_reject_duplicate_pairs,
            parse_int=int,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
    except json.JSONDecodeError as exc:
        raise CanonicalError(f"invalid JSON: {exc}") from exc


def load_exact_json(path: str | Path) -> Any:
    try:
        return loads_exact(Path(path).read_bytes())
    except OSError as exc:
        raise CanonicalError(f"cannot read JSON file {path}: {exc}") from exc


def write_canonical_json(path: str | Path, value: Any) -> None:
    """Atomically write canonical JSON plus one trailing newline."""

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = canonical_bytes(value) + b"\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", dir=destination.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()


def write_canonical_jsonl(path: str | Path, rows: Iterable[Any]) -> tuple[int, str]:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", dir=destination.parent
    )
    temporary = Path(temporary_name)
    count = 0
    try:
        with os.fdopen(descriptor, "wb") as handle:
            for row in rows:
                handle.write(canonical_bytes(row) + b"\n")
                count += 1
            handle.flush()
            os.fsync(handle.fileno())
        digest = file_sha256(temporary)
        os.replace(temporary, destination)
        return count, digest
    finally:
        if temporary.exists():
            temporary.unlink()


def fraction_dict(value: Fraction) -> dict[str, str]:
    if not isinstance(value, Fraction):
        raise CanonicalError("value must be a Fraction")
    return {"denominator": str(value.denominator), "numerator": str(value.numerator)}


def fraction_from_dict(value: Mapping[str, Any]) -> Fraction:
    if not isinstance(value, Mapping) or set(value) != {"denominator", "numerator"}:
        raise CanonicalError("fraction fields must be denominator and numerator")
    numerator = value["numerator"]
    denominator = value["denominator"]
    if not isinstance(numerator, str) or not isinstance(denominator, str):
        raise CanonicalError("fraction components must be decimal strings")
    try:
        exact = Fraction(int(numerator), int(denominator))
    except (ValueError, ZeroDivisionError) as exc:
        raise CanonicalError(f"invalid exact fraction: {exc}") from exc
    if str(exact.numerator) != numerator or str(exact.denominator) != denominator:
        raise CanonicalError("fraction is not reduced canonical form")
    return exact


__all__ = [
    "SEMANTIC_SEAL_FIELD",
    "CanonicalError",
    "canonical_bytes",
    "canonical_sha256",
    "file_sha256",
    "fraction_dict",
    "fraction_from_dict",
    "load_exact_json",
    "loads_exact",
    "require_seal",
    "seal_dict",
    "semantic_body",
    "sha256_bytes",
    "verify_seal",
    "write_canonical_json",
    "write_canonical_jsonl",
]
