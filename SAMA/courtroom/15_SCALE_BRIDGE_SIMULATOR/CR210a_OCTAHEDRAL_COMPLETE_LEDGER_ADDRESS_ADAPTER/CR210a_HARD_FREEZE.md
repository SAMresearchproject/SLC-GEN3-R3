# CR210a Hard Freeze

`freeze_status = EXECUTION_FAILURE_PRESERVED`

`frozen_utc = 2026-07-15T03:43:20.3448647Z`

`execution_count = 1`

`structural_verdict = NONE`

`same_run_repair = NOT_PERFORMED`

This directory preserves the sealed precommit, the original sealed runner, every partial output produced before the exception, and the explicit failure record. CR210a is closed and must not be rerun or rewritten.

The failure does not adjudicate the structural candidate. A successor must use a new record identifier and a new task-specific preflight.
