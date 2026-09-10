"""Run the complete inherited and v0.6 SLC C1 unit-test tree."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


CANDIDATE = Path(__file__).resolve().parents[1]


def main() -> int:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(CANDIDATE / "src")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    process = subprocess.run(
        [
            sys.executable,
            "-B",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(CANDIDATE / "tests"),
            "-t",
            str(CANDIDATE),
            "-v",
        ],
        cwd=CANDIDATE,
        env=env,
        text=True,
        check=False,
    )
    return process.returncode


if __name__ == "__main__":
    raise SystemExit(main())
