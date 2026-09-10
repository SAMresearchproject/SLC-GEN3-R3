from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np


CAMPAIGN = "CR120ZA_X1_QUANTUM_SANDBOX_SERIALIZATION_CORRECTION"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE_RUNNER = ROOT / "14_FOUNDATIONAL_TESTS/CR120Z_X1_ENTANGLEMENT_RESPONSE_INTERFACE_QUANTUM_SANDBOX_DISCOVERY/CR120Z_runner.py"


def corrected_write_json(path: Path, payload) -> None:
    def native_scalar(value):
        if isinstance(value, np.generic):
            return value.item()
        raise TypeError(f"Object of type {value.__class__.__name__} is not JSON serializable")

    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=native_scalar) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    spec = importlib.util.spec_from_file_location("cr120z_attempt1", SOURCE_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load the sealed CR120Z attempt-1 runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module.CAMPAIGN = CAMPAIGN
    module.HERE = HERE
    module.ROOT = ROOT
    module.RELEASE = HERE / "release"
    module.__file__ = str(Path(__file__).resolve())
    module.write_json = corrected_write_json
    return int(module.main())


if __name__ == "__main__":
    raise SystemExit(main())
