"""Run the v0.6 isolated-wheel probe before executable sealing."""

from __future__ import annotations

import json
from pathlib import Path

from clean_wheel_probe import run_clean_wheel_probe


CANDIDATE = Path(__file__).resolve().parents[1]
RESULT = CANDIDATE / "V0_6_SLC_C1_DEVELOPMENT_WHEEL_PROBE.json"


def main() -> int:
    payload = run_clean_wheel_probe(CANDIDATE)
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "wheel_name": payload.get("wheel_name"),
                "wheel_sha256": payload.get("wheel_sha256"),
                "wheel_data_missing": payload.get("wheel_data_missing"),
                "cli_cases": payload.get("cli_cases"),
                "api_payload": payload.get("api_payload"),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
