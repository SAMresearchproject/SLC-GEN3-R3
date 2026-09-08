#!/usr/bin/env python3
"""ctypes bridge to the exact fused native arithmetic refinement."""

from __future__ import annotations

import ctypes
from pathlib import Path
from typing import Any

import numpy as np


class NativeArithmetic:
    def __init__(self, library_path: Path) -> None:
        self.library_path = library_path.resolve()
        self.library = ctypes.CDLL(str(self.library_path))
        pointer = ctypes.c_void_p
        unsigned = ctypes.c_uint64
        common = [
            pointer,
            pointer,
            pointer,
            pointer,
            unsigned,
            unsigned,
            unsigned,
            unsigned,
            unsigned,
        ]
        self.updaters: dict[str, Any] = {}
        self.p4_updaters: dict[str, Any] = {}
        for dtype_name in ("uint8", "uint16", "uint32"):
            function = getattr(self.library, f"sam_update_u{dtype_name[4:]}")
            function.argtypes = common
            function.restype = ctypes.c_int
            self.updaters[dtype_name] = function
            p4_function = getattr(
                self.library, f"sam_update_u{dtype_name[4:]}_p4"
            )
            p4_function.argtypes = common
            p4_function.restype = ctypes.c_int
            self.p4_updaters[dtype_name] = p4_function
        self.finish_function = self.library.sam_finish_products
        self.finish_function.argtypes = [
            pointer,
            pointer,
            pointer,
            unsigned,
            unsigned,
        ]
        self.finish_function.restype = ctypes.c_int
        self.test_function = self.library.sam_barrett_test
        self.test_function.argtypes = [unsigned, unsigned, unsigned]
        self.test_function.restype = unsigned

    @staticmethod
    def reciprocal(prime: int) -> int:
        return (1 << 64) // int(prime)

    def self_test(self, primes: list[int]) -> None:
        samples = [
            0,
            1,
            2,
            (1 << 32) - 1,
            (1 << 48) + 12345,
            (1 << 60) - 1,
        ]
        for prime in primes:
            reciprocal = self.reciprocal(prime)
            products = samples + [
                (prime - 1) * (prime - 1),
                (prime - 2) * (prime - 3),
                prime * prime - 1,
            ]
            for value in products:
                observed = int(self.test_function(value, prime, reciprocal))
                if observed != value % prime:
                    raise RuntimeError("native Barrett self-test failed")

    def update(
        self,
        product_zero: np.ndarray,
        product_one: np.ndarray,
        factor_values: np.ndarray,
        base_index: np.ndarray,
        eliminated_bit: int,
        prime: int,
    ) -> None:
        dtype_name = base_index.dtype.name
        if dtype_name not in self.updaters:
            raise RuntimeError("native arithmetic received an unsupported index dtype")
        if not (
            product_zero.flags.c_contiguous
            and product_one.flags.c_contiguous
            and factor_values.flags.c_contiguous
            and base_index.flags.c_contiguous
        ):
            raise RuntimeError("native arithmetic requires contiguous arrays")
        if product_zero.shape != product_one.shape:
            raise RuntimeError("native product-buffer shapes differ")
        if product_zero.shape[1] == 4:
            updater = self.p4_updaters[dtype_name]
        else:
            updater = self.updaters[dtype_name]
        status = updater(
            product_zero.ctypes.data,
            product_one.ctypes.data,
            factor_values.ctypes.data,
            base_index.ctypes.data,
            product_zero.shape[0],
            product_zero.shape[1],
            int(eliminated_bit),
            int(prime),
            self.reciprocal(prime),
        )
        if status:
            raise RuntimeError("native fused update rejected its inputs")

    def finish(
        self,
        output: np.ndarray,
        product_zero: np.ndarray,
        product_one: np.ndarray,
        prime: int,
    ) -> None:
        if not (
            output.flags.c_contiguous
            and product_zero.flags.c_contiguous
            and product_one.flags.c_contiguous
        ):
            raise RuntimeError("native finish requires contiguous arrays")
        status = self.finish_function(
            output.ctypes.data,
            product_zero.ctypes.data,
            product_one.ctypes.data,
            output.size,
            int(prime),
        )
        if status:
            raise RuntimeError("native product finish rejected its inputs")


__all__ = ["NativeArithmetic"]
