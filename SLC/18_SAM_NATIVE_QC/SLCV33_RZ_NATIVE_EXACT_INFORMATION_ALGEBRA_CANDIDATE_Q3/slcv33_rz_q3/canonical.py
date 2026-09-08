"""Canonical exact serialization helpers for the Q3 candidate."""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields, is_dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


class CanonicalError(ValueError):
    """A value is not admitted to exact Q3 mathematical identity."""


@dataclass(slots=True)
class OrderedSemanticDigest:
    """Constant-memory canonical SHA-256 of an exact ordered tuple.

    The emitted grammar is byte-for-byte ``canonical_bytes(tuple(items))``.
    This retains predecessor tuple-digest identity while avoiding retention of
    the tuple or any normalized JSON tree.
    """

    _digest: Any
    count: int = 0

    ALGORITHM = "CANONICAL_SHA256_OF_EXACT_ORDERED_SEQUENCE_V1"

    @classmethod
    def create(cls) -> "OrderedSemanticDigest":
        digest = hashlib.sha256()
        digest.update(b"[")
        return cls(digest)

    def observe(self, value: Any) -> str:
        semantic = canonical_sha256(value)
        if self.count:
            self._digest.update(b",")
        previous: bytes | None = None
        for block in iter_canonical_bytes(value):
            if previous is not None:
                self._digest.update(previous)
            previous = block
        if previous != b"\n":
            raise CanonicalError("canonical item stream has no terminal LF")
        self.count += 1
        return semantic

    def observe_semantic_sha256(self, semantic_sha256: str) -> None:
        if (
            not isinstance(semantic_sha256, str)
            or len(semantic_sha256) != 64
            or any(character not in "0123456789abcdef" for character in semantic_sha256)
        ):
            raise CanonicalError("ordered semantic item is not lowercase SHA-256")
        self.observe(semantic_sha256)

    @property
    def hexdigest(self) -> str:
        digest = self._digest.copy()
        digest.update(b"]\n")
        return digest.hexdigest()

    def receipt(self) -> dict[str, Any]:
        return {
            "algorithm": self.ALGORITHM,
            "item_count": self.count,
            "semantic_sha256": self.hexdigest,
        }


def reject_floats(value: Any, *, path: str = "$") -> None:
    """Reject every binary float recursively, including mapping keys."""

    if isinstance(value, float):
        raise CanonicalError(f"binary float is barred at {path}")
    if isinstance(value, Mapping):
        for key, item in value.items():
            reject_floats(key, path=f"{path}.<key>")
            reject_floats(item, path=f"{path}.{key}")
    elif isinstance(value, (list, tuple, set, frozenset)):
        for index, item in enumerate(value):
            reject_floats(item, path=f"{path}[{index}]")


def fraction_dict(value: Fraction | int) -> dict[str, str]:
    exact = Fraction(value)
    return {"denominator": str(exact.denominator), "numerator": str(exact.numerator)}


def fraction_from_dict(value: Mapping[str, Any]) -> Fraction:
    return Fraction(int(value["numerator"]), int(value["denominator"]))


def exact_json_value(value: Any) -> Any:
    """Convert exact Python values to a canonical JSON-compatible tree."""

    reject_floats(value)
    if isinstance(value, Fraction):
        return {"__fraction__": fraction_dict(value)}
    if is_dataclass(value):
        return exact_json_value(asdict(value))
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise CanonicalError("canonical JSON mappings require string keys")
        return {key: exact_json_value(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [exact_json_value(item) for item in value]
    if isinstance(value, list):
        return [exact_json_value(item) for item in value]
    if isinstance(value, (set, frozenset)):
        normalized = [exact_json_value(item) for item in value]
        return sorted(normalized, key=lambda item: canonical_bytes(item))
    if value is None or isinstance(value, (str, int, bool)):
        return value
    raise CanonicalError(f"unsupported canonical value type: {type(value).__name__}")


def canonical_bytes(value: Any) -> bytes:
    normalized = exact_json_value(value)
    return json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8") + b"\n"


def iter_canonical_bytes(value: Any) -> Iterable[bytes]:
    """Yield the exact canonical JSON encoding without normalizing a full tree.

    This is byte-identical to :func:`canonical_bytes`.  Dataclasses and large
    nested catalog maps are traversed field by field, so hashing them does not
    require an ``asdict`` copy plus a second JSON-compatible copy.
    """

    def emit(item: Any) -> Iterable[bytes]:
        if isinstance(item, float):
            raise CanonicalError("binary float is barred")
        if isinstance(item, Fraction):
            yield b'{"__fraction__":{"denominator":'
            yield json.dumps(str(item.denominator), ensure_ascii=False).encode("utf-8")
            yield b',"numerator":'
            yield json.dumps(str(item.numerator), ensure_ascii=False).encode("utf-8")
            yield b"}}"
            return
        if is_dataclass(item) and not isinstance(item, type):
            yield b"{"
            for index, field in enumerate(sorted(fields(item), key=lambda row: row.name)):
                if index:
                    yield b","
                yield json.dumps(field.name, ensure_ascii=False).encode("utf-8")
                yield b":"
                yield from emit(getattr(item, field.name))
            yield b"}"
            return
        if isinstance(item, Mapping):
            if any(not isinstance(key, str) for key in item):
                raise CanonicalError("canonical JSON mappings require string keys")
            yield b"{"
            for index, key in enumerate(sorted(item)):
                if index:
                    yield b","
                yield json.dumps(key, ensure_ascii=False).encode("utf-8")
                yield b":"
                yield from emit(item[key])
            yield b"}"
            return
        if isinstance(item, (tuple, list)):
            yield b"["
            for index, child in enumerate(item):
                if index:
                    yield b","
                yield from emit(child)
            yield b"]"
            return
        if isinstance(item, (set, frozenset)):
            ordered = sorted(item, key=canonical_bytes)
            yield b"["
            for index, child in enumerate(ordered):
                if index:
                    yield b","
                yield from emit(child)
            yield b"]"
            return
        if item is None or isinstance(item, (str, int, bool)):
            yield json.dumps(
                item,
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
            ).encode("utf-8")
            return
        raise CanonicalError(f"unsupported canonical value type: {type(item).__name__}")

    yield from emit(value)
    yield b"\n"


def canonical_sha256(value: Any) -> str:
    digest = hashlib.sha256()
    for block in iter_canonical_bytes(value):
        digest.update(block)
    return digest.hexdigest()


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def seal(value: Mapping[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("semantic_sha256", None)
    body["semantic_sha256"] = canonical_sha256(body)
    return body


def validate_semantic_seal(value: Mapping[str, Any]) -> bool:
    observed = value.get("semantic_sha256")
    if not isinstance(observed, str):
        return False
    body = dict(value)
    body.pop("semantic_sha256", None)
    return canonical_sha256(body) == observed


def load_exact_json(path: str | Path) -> Any:
    value = json.loads(Path(path).read_bytes())
    reject_floats(value)
    return value
