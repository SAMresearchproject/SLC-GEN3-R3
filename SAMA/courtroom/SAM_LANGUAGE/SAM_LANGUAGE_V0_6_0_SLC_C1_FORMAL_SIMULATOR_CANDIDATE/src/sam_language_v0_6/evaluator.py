"""The one checked-execution path for core, QP, and exact formal SLC programs."""

from .runtime import check_program, execute_checked, run_program_text

__all__ = ["check_program", "execute_checked", "run_program_text"]
