"""JSON command-line interface with per-run custody records."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from uuid import uuid4
from . import open_runtime, current_generation, verify_sources, DEPLOYMENT_OPERATIONS

def exact(value):
    if isinstance(value, Fraction):
        return value.numerator if value.denominator == 1 else str(value)
    raise TypeError("No exact JSON encoding for " + type(value).__name__)

def encoded(value):
    return (json.dumps(value, default=exact, sort_keys=True, indent=2) + "\n").encode()

def main():
    parser = argparse.ArgumentParser(description="SLC-GEN3-R3 — research use only")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("verify", help="authenticate all exported upstream files")
    sub.add_parser("info", help="show release identity and deployment boundaries")
    run = sub.add_parser("run", help="execute one exact operation from JSON")
    run.add_argument("operation")
    run.add_argument("input", type=Path)
    run.add_argument("--output", type=Path)
    run.add_argument("--receipts", type=Path, default=Path("runs"))
    run.add_argument("--state-dir", type=Path, help="durable R3 state directory; reuse to continue")
    args = parser.parse_args()
    if args.command == "verify":
        print(encoded(verify_sources()).decode(), end="")
        return
    if args.command == "info":
        print(encoded({"engine": "SLC-GEN3-R3", "generation": current_generation(),
            "license": "SAM Research-Only Licence 1.0; commercial use requires separate written permission",
            "separate_deployments": DEPLOYMENT_OPERATIONS}).decode(), end="")
        return
    if args.output and args.output.exists():
        parser.error("Output already exists; choose a new path: " + str(args.output))
    request = {"operation": args.operation, "payload": json.loads(args.input.read_text())}
    destination = args.receipts / uuid4().hex
    destination.mkdir(parents=True, exist_ok=False)
    source_manifest = Path(__file__).resolve().parents[1] / "provenance/SOURCE_MANIFEST.json"
    (destination / "INPUT.json").write_bytes(encoded(request))
    try:
        with open_runtime(state_dir=args.state_dir) as runtime:
            result = runtime.execute(args.operation, request["payload"])
        output = encoded(result)
        (destination / "OUTPUT.json").write_bytes(output)
        receipt = {"status": "RETURNED", "engine": "SLC-GEN3-R3", "generation": current_generation(),
            "utc": datetime.now(timezone.utc).isoformat(), "operation": args.operation,
            "source_manifest_sha256": hashlib.sha256(source_manifest.read_bytes()).hexdigest(),
            "input_sha256": hashlib.sha256(encoded(request)).hexdigest(),
            "output_sha256": hashlib.sha256(output).hexdigest()}
        (destination / "RECEIPT.json").write_bytes(encoded(receipt))
        if args.output:
            with args.output.open("xb") as stream:
                stream.write(output)
        else:
            print(output.decode(), end="")
    except Exception as exc:
        (destination / "FAILED.json").write_bytes(encoded({"error": str(exc), "type": type(exc).__name__}))
        raise

if __name__ == "__main__":
    main()
