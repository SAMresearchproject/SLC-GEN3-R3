"""Representative source-native adapters for the custody compiler."""

from __future__ import annotations

from itertools import product
from typing import Hashable, Iterable

from .compiler import CompiledCustodyMorphism


def reciprocal_dyadic_morphism(modulus: int) -> CompiledCustodyMorphism[tuple[int, int], tuple[int, int]]:
    """Compile the exact visible step (s,D) -> (s^2-2,sD) mod M."""

    m = int(modulus)
    if m <= 2:
        raise ValueError("modulus must exceed two")
    domain = ((common, directional) for common in range(m) for directional in range(m))
    return CompiledCustodyMorphism(
        f"RECIPROCAL_DYADIC_MOD_{m}",
        domain,
        lambda state: ((state[0] * state[0] - 2) % m, (state[0] * state[1]) % m),
        source_references=("unified_weil_complete_dyadic.py:dyadic_step",),
    )


def _unpack_z4(address: int, power: int) -> list[int]:
    digits: list[int] = []
    value = int(address)
    for _ in range(power):
        digits.append(value & 3)
        value >>= 2
    return digits


def _pack_z4(digits: Iterable[int]) -> int:
    value = 0
    for index, digit in enumerate(digits):
        value |= (int(digit) & 3) << (2 * index)
    return value


def z4_translation_morphism(power: int, shift: tuple[int, ...]) -> CompiledCustodyMorphism[int, int]:
    """Compile one fixed signed Z4^power translation over packed addresses."""

    n = int(power)
    if n < 1 or len(shift) != n:
        raise ValueError("shift length must equal positive Z4 power")
    normalized = tuple(int(value) % 4 for value in shift)
    size = 4**n

    def translate(address: int) -> int:
        digits = _unpack_z4(address, n)
        return _pack_z4((digit + delta) % 4 for digit, delta in zip(digits, normalized))

    return CompiledCustodyMorphism(
        f"Z4_POWER_{n}_FIXED_TRANSLATION_{normalized}",
        range(size),
        translate,
        source_references=("complete Exact Write fixed translation",),
    )


def frustrated_triangle_energy_morphism() -> CompiledCustodyMorphism[tuple[int, int, int], int]:
    """Three-spin antiferromagnetic triangle projected to its exact energy."""

    domain = tuple(product((-1, 1), repeat=3))
    return CompiledCustodyMorphism(
        "FRUSTRATED_TRIANGLE_CONFIGURATION_TO_ENERGY",
        domain,
        lambda spin: spin[0] * spin[1] + spin[1] * spin[2] + spin[2] * spin[0],
        source_references=("representative frustrated-spin exact finite control",),
    )


def finite_partition_morphism(
    name: str,
    domain: Iterable[Hashable],
    labels: dict[Hashable, Hashable],
) -> CompiledCustodyMorphism[Hashable, Hashable]:
    """Compile an already-declared finite partition without inventing labels."""

    frozen_domain = tuple(domain)
    if set(frozen_domain) != set(labels):
        raise ValueError("partition labels must cover the exact domain")
    return CompiledCustodyMorphism(name, frozen_domain, labels.__getitem__)

