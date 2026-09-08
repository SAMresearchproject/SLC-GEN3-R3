"""Canonical mathematical values; execution and provenance have separate records."""
from fractions import Fraction
import hashlib
import json


def rational(value):
    if isinstance(value, Fraction):
        return value
    if type(value) is int or type(value) is str:
        return Fraction(value)
    raise TypeError('An exact operand requires an integer or rational string')


def canonical(value):
    if isinstance(value, Fraction):
        return value.numerator if value.denominator == 1 else str(value)
    if isinstance(value, dict):
        if not all(type(k) is str for k in value):
            raise TypeError('Canonical object keys must be strings')
        return {k: canonical(value[k]) for k in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [canonical(v) for v in value]
    if value is None or type(value) in (str, int, bool):
        return value
    if hasattr(value, 'to_dict'):
        return canonical(value.to_dict())
    raise TypeError(f'Unsupported canonical value: {type(value).__name__}')


def canonical_bytes(value):
    return json.dumps(canonical(value), sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True).encode()


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def freeze(value):
    if isinstance(value, dict):
        return tuple((k, freeze(v)) for k, v in sorted(value.items()))
    if isinstance(value, (list, tuple)):
        return tuple(freeze(v) for v in value)
    return value
