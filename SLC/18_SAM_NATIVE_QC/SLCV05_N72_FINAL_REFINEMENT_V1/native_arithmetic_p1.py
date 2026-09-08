#!/usr/bin/env python3
"""Versioned ctypes bridge selecting the exact one-root native specialization."""

from __future__ import annotations

import ctypes
from pathlib import Path
from typing import Any

import numpy as np

from native_arithmetic import NativeArithmetic


class NativeArithmeticP1(NativeArithmetic):
    def __init__(self, library_path: Path) -> None:
        super().__init__(library_path)
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
        self.p1_updaters: dict[str, Any] = {}
        for dtype_name in ("uint8", "uint16", "uint32"):
            function = getattr(self.library, f"sam_update_u{dtype_name[4:]}_p1")
            function.argtypes = common
            function.restype = ctypes.c_int
            self.p1_updaters[dtype_name] = function

    def update(
        self,
        product_zero: np.ndarray,
        product_one: np.ndarray,
        factor_values: np.ndarray,
        base_index: np.ndarray,
        eliminated_bit: int,
        prime: int,
    ) -> None:
        if product_zero.shape[1] != 1:
            super().update(
                product_zero,
                product_one,
                factor_values,
                base_index,
                eliminated_bit,
                prime,
            )
            return
        dtype_name = base_index.dtype.name
        if dtype_name not in self.p1_updaters:
            raise RuntimeError("P1 arithmetic received an unsupported index dtype")
        if not (
            product_zero.flags.c_contiguous
            and product_one.flags.c_contiguous
            and factor_values.flags.c_contiguous
            and base_index.flags.c_contiguous
        ):
            raise RuntimeError("P1 arithmetic requires contiguous arrays")
        if product_zero.shape != product_one.shape:
            raise RuntimeError("P1 product-buffer shapes differ")
        status = self.p1_updaters[dtype_name](
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
            raise RuntimeError("P1 fused update rejected its inputs")


__all__ = ["NativeArithmeticP1"]
