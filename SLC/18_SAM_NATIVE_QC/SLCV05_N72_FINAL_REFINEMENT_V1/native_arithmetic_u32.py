#!/usr/bin/env python3
"""ctypes bridge for exact uint32 storage with uint64 modular arithmetic."""

from __future__ import annotations

import ctypes
from pathlib import Path
from typing import Any

import numpy as np


class NativeArithmeticU32P1:
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
        for dtype_name in ("uint8", "uint16", "uint32"):
            function = getattr(
                self.library,
                f"sam_u32_update_index_u{dtype_name[4:]}_p1",
            )
            function.argtypes = common
            function.restype = ctypes.c_int
            self.updaters[dtype_name] = function
        self.finish_function = self.library.sam_u32_finish_products
        self.finish_function.argtypes = [
            pointer,
            pointer,
            pointer,
            unsigned,
            unsigned,
        ]
        self.finish_function.restype = ctypes.c_int
        self.test_function = self.library.sam_u32_barrett_test
        self.test_function.argtypes = [unsigned, unsigned, unsigned]
        self.test_function.restype = unsigned

    @staticmethod
    def reciprocal(prime: int) -> int:
        return (1 << 64) // int(prime)

    def self_test(self, primes: list[int]) -> None:
        for prime in primes:
            if not 0 < prime <= np.iinfo(np.uint32).max:
                raise RuntimeError("prime does not fit exact uint32 storage")
            reciprocal = self.reciprocal(prime)
            products = [
                0,
                1,
                2,
                (prime - 1) * (prime - 1),
                (prime - 2) * (prime - 3),
                prime * prime - 1,
            ]
            for value in products:
                observed = int(self.test_function(value, prime, reciprocal))
                if observed != value % prime:
                    raise RuntimeError("uint32 native Barrett self-test failed")

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
            raise RuntimeError("uint32 lane received an unsupported index dtype")
        if not (
            product_zero.dtype == np.uint32
            and product_one.dtype == np.uint32
            and factor_values.dtype == np.uint32
            and product_zero.flags.c_contiguous
            and product_one.flags.c_contiguous
            and factor_values.flags.c_contiguous
            and base_index.flags.c_contiguous
        ):
            raise RuntimeError("uint32 native lane requires contiguous uint32 values")
        if product_zero.shape != product_one.shape or product_zero.shape[1] != 1:
            raise RuntimeError("uint32 native lane requires matched P1 products")
        status = self.updaters[dtype_name](
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
            raise RuntimeError("uint32 fused update rejected its inputs")

    def finish(
        self,
        output: np.ndarray,
        product_zero: np.ndarray,
        product_one: np.ndarray,
        prime: int,
    ) -> None:
        if not (
            output.dtype == np.uint32
            and product_zero.dtype == np.uint32
            and product_one.dtype == np.uint32
            and output.flags.c_contiguous
            and product_zero.flags.c_contiguous
            and product_one.flags.c_contiguous
        ):
            raise RuntimeError("uint32 finish requires contiguous uint32 arrays")
        status = self.finish_function(
            output.ctypes.data,
            product_zero.ctypes.data,
            product_one.ctypes.data,
            output.size,
            int(prime),
        )
        if status:
            raise RuntimeError("uint32 product finish rejected its inputs")


__all__ = ["NativeArithmeticU32P1"]
