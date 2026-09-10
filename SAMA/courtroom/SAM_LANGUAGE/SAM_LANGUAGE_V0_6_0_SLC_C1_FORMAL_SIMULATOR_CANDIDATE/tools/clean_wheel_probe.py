"""Offline clean-wheel build and execution probe for SAM Language v0.6."""

from __future__ import annotations

import hashlib
import base64
import csv
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
import venv
import zipfile
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _run(args: list[str], *, cwd: Path, env: dict[str, str], expected: int = 0) -> dict:
    try:
        proc = subprocess.run(
            args,
            cwd=str(cwd),
            env=env,
            text=True,
            capture_output=True,
            check=False,
            timeout=120,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "args": args,
            "cwd": str(cwd),
            "returncode": None,
            "expected_returncode": expected,
            "status": "FAIL",
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "traceback_found": False,
            "timed_out": True,
        }
    return {
        "args": args,
        "cwd": str(cwd),
        "returncode": proc.returncode,
        "expected_returncode": expected,
        "status": "PASS" if proc.returncode == expected else "FAIL",
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "traceback_found": "Traceback" in proc.stdout or "Traceback" in proc.stderr,
        "timed_out": False,
    }


def _wheel_digest(data: bytes) -> str:
    encoded = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=")
    return "sha256=" + encoded.decode("ascii")


def _build_wheel_stdlib(build_source: Path, wheelhouse: Path) -> Path:
    """Build a standards-compliant pure-Python wheel without external tools."""

    distribution = "sam_language_v0_6_0_slc_c1_formal_simulator_candidate"
    version = "0.6.0"
    wheel = wheelhouse / f"{distribution}-{version}-py3-none-any.whl"
    dist_info = f"{distribution}-{version}.dist-info"
    members: dict[str, bytes] = {}
    package_root = build_source / "src" / "sam_language_v0_6"
    for path in sorted(package_root.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        archive_path = (Path("sam_language_v0_6") / path.relative_to(package_root)).as_posix()
        members[archive_path] = path.read_bytes()
    members[f"{dist_info}/METADATA"] = (
        "Metadata-Version: 2.1\n"
        "Name: sam-language-v0-6-0-slc-c1-formal-simulator-candidate\n"
        "Version: 0.6.0\n"
        "Summary: SAM Language v0.6 exact SLC C1 simulator candidate\n"
        "Requires-Python: >=3.10\n"
        "\n"
    ).encode("utf-8")
    members[f"{dist_info}/WHEEL"] = (
        "Wheel-Version: 1.0\n"
        "Generator: SAM-v0.6-stdlib-wheel-builder\n"
        "Root-Is-Purelib: true\n"
        "Tag: py3-none-any\n"
        "\n"
    ).encode("utf-8")
    members[f"{dist_info}/entry_points.txt"] = (
        "[console_scripts]\n"
        "sam = sam_language_v0_6.cli:main\n"
    ).encode("utf-8")
    members[f"{dist_info}/top_level.txt"] = b"sam_language_v0_6\n"
    record_name = f"{dist_info}/RECORD"
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    for name, data in sorted(members.items()):
        writer.writerow((name, _wheel_digest(data), str(len(data))))
    writer.writerow((record_name, "", ""))
    members[record_name] = buffer.getvalue().encode("utf-8")
    with zipfile.ZipFile(wheel, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(members.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    return wheel


def run_clean_wheel_probe(candidate: str | Path) -> dict:
    candidate = Path(candidate).resolve()
    commands: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="sam_v06_c1_clean_") as temporary:
        temp = Path(temporary)
        build_source = temp / "build_source"
        (build_source / "src").mkdir(parents=True)
        shutil.copyfile(candidate / "pyproject.toml", build_source / "pyproject.toml")
        shutil.copytree(candidate / "src" / "sam_language_v0_6", build_source / "src" / "sam_language_v0_6")
        wheelhouse = temp / "wheelhouse"
        wheelhouse.mkdir()
        clean_env = {
            key: value for key, value in os.environ.items() if not key.upper().startswith("PIP_")
        }
        clean_env.pop("PYTHONPATH", None)
        clean_env.pop("PYTHONHOME", None)
        clean_env["PYTHONNOUSERSITE"] = "1"
        clean_env["PIP_NO_INDEX"] = "1"
        clean_env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
        clean_env["PIP_NO_INPUT"] = "1"
        clean_env["PIP_CONFIG_FILE"] = os.devnull
        built_wheel = _build_wheel_stdlib(build_source, wheelhouse)
        build = {
            "args": ["stdlib-wheel-builder", str(build_source)],
            "cwd": str(temp),
            "returncode": 0,
            "expected_returncode": 0,
            "status": "PASS",
            "stdout": str(built_wheel),
            "stderr": "",
            "traceback_found": False,
        }
        commands.append(build)
        wheels = sorted(wheelhouse.glob("*.whl"))
        if build["status"] != "PASS" or len(wheels) != 1:
            return {
                "status": "FAIL",
                "stage": "BUILD",
                "commands": commands,
                "wheel_count": len(wheels),
            }
        wheel = wheels[0]
        with zipfile.ZipFile(wheel) as archive:
            members = sorted(archive.namelist())
            metadata_name = next(name for name in members if name.endswith(".dist-info/METADATA"))
            metadata = archive.read(metadata_name).decode("utf-8")
            python_source = b"\n".join(
                archive.read(name) for name in members if name.endswith(".py")
            ).decode("utf-8", errors="replace")
            entry_points_name = next(
                name for name in members if name.endswith(".dist-info/entry_points.txt")
            )
            entry_points = archive.read(entry_points_name).decode("utf-8")
        required_data = {
            (Path("sam_language_v0_6/data") / path.name).as_posix()
            for path in (candidate / "src/sam_language_v0_6/data").iterdir()
            if path.is_file()
        }
        wheel_data_missing = sorted(required_data - set(members))
        dependency_lines = [line for line in metadata.splitlines() if line.startswith("Requires-Dist:")]
        pyproject = tomllib.loads((candidate / "pyproject.toml").read_text(encoding="utf-8"))
        package_globs = set(pyproject["tool"]["setuptools"]["package-data"]["sam_language_v0_6"])
        pyproject_checks = {
            "project_name": pyproject["project"]["name"]
            == "sam-language-v0-6-0-slc-c1-formal-simulator-candidate",
            "project_version": pyproject["project"]["version"] == "0.6.0",
            "console_entry": pyproject["project"]["scripts"]["sam"]
            == "sam_language_v0_6.cli:main",
            "wheel_metadata_name": "Name: sam-language-v0-6-0-slc-c1-formal-simulator-candidate"
            in metadata,
            "wheel_metadata_version": "Version: 0.6.0" in metadata,
            "wheel_entry_point": "sam = sam_language_v0_6.cli:main" in entry_points,
            "package_data_extensions": {
                "data/*.json",
                "data/*.csv",
                "data/*.bnf",
                "data/*.md",
            }.issubset(package_globs),
        }

        venv_root = temp / "venv"
        venv.EnvBuilder(with_pip=True, clear=True).create(venv_root)
        python = venv_root / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        console = venv_root / ("Scripts/sam.exe" if os.name == "nt" else "bin/sam")
        install = _run(
            [str(python), "-I", "-m", "pip", "install", "--no-index", "--no-deps", str(wheel)],
            cwd=temp,
            env=clean_env,
        )
        commands.append(install)
        copied_examples = temp / "examples"
        shutil.copytree(candidate / "examples", copied_examples)

        cli_cases = [
            ("core_closure", ["run", str(copied_examples / "valid_closure.sam")], 0),
            ("clock_kernel", ["run", str(copied_examples / "cr005_gps_calibration.sam")], 0),
            ("qp_unary", ["run", str(copied_examples / "qp_unary.sam")], 0),
            ("qp_triad", ["run", str(copied_examples / "qp_admitted_triad.sam")], 0),
            ("mixed", ["run", str(copied_examples / "mixed_core_qp.sam")], 0),
            ("rejected_triad", ["run", str(copied_examples / "qp_rejected_triad.sam")], 2),
            ("census", ["grammar", "census"], 0),
            ("verify_source", ["grammar", "verify-source"], 0),
            ("verify_native", ["grammar", "verify-native"], 0),
            ("verify_inverse", ["grammar", "verify-native-inverse"], 0),
            ("validate_contract", ["validate-contract"], 0),
            ("slc_bell", ["run", str(copied_examples / "slc_bell.sam"), "--slc-c1-formal"], 0),
            ("slc_ghz12", ["run", str(copied_examples / "slc_ghz12_chain.sam"), "--slc-c1-formal"], 0),
        ]
        case_results = {}
        case_records = {}
        for case_id, cli_args, expected in cli_cases:
            record = _run(
                [str(python), "-I", "-m", "sam_language_v0_6.cli", *cli_args],
                cwd=temp,
                env=clean_env,
                expected=expected,
            )
            commands.append(record)
            case_results[case_id] = record["status"]
            case_records[case_id] = record

        api_code = (
            "import json, pathlib, sam_language_v0_6 as s; "
            "r=s.run_program_text('let z: SLCState12 = SLC_ZERO_REGISTER()\\n"
            "let h: SLCState12 = SLC_PREPARE_REQUEST(z, L0)\\n"
            "let b: SLCState12 = SLC_X1_RESPONSE(h, L0, L1)\\nreturn b', "
            "mode='slc-c1-formal'); "
            "print(json.dumps({'id':r.entity_id,'module':str(pathlib.Path(s.__file__).resolve()),"
            "'census':len(s.enumerate_qp_productions()),"
            "'source':s.verify_qp_source_reconciliation()['status'],"
            "'slc_support':r.result_payload['support_size'],"
            "'state_hash':r.result_payload['state_hash'],"
            "'history_hash':r.result_payload['history_hash']}))"
        )
        api = _run([str(python), "-I", "-c", api_code], cwd=temp, env=clean_env)
        commands.append(api)
        try:
            api_payload = json.loads(api["stdout"])
        except json.JSONDecodeError:
            api_payload = {}
        console_probe = _run(
            [str(console), "run", str(copied_examples / "slc_bell.sam"), "--slc-c1-formal"],
            cwd=temp,
            env=clean_env,
        )
        commands.append(console_probe)
        try:
            bell_cli_payload = json.loads(case_records["slc_bell"]["stdout"])
        except json.JSONDecodeError:
            bell_cli_payload = {}
        try:
            console_payload = json.loads(console_probe["stdout"])
        except json.JSONDecodeError:
            console_payload = {}
        sidecar = _run(
            [
                str(python),
                "-I",
                "-c",
                "import importlib.util; "
                "assert importlib.util.find_spec('sam_qp_particle_grammar_v1') is None; "
                "assert importlib.util.find_spec('sam_language_v0_5') is None",
            ],
            cwd=temp,
            env=clean_env,
        )
        commands.append(sidecar)
        no_repo_path = all(str(candidate).lower() not in value.lower() for value in (api["stdout"], api["stderr"]))
        no_tracebacks = all(not record["traceback_found"] for record in commands)
        module_in_venv = str(venv_root).lower() in str(api_payload.get("module", "")).lower()
        ui_dependency_absent = not any(
            token in ("\n".join(members) + "\n" + metadata + "\n" + python_source).lower()
            for token in ("streamlit", "flask", "fastapi", "sam_ui")
        )
        cli_api_parity = (
            bell_cli_payload.get("entity_id") == api_payload.get("id")
            and bell_cli_payload.get("result_payload", {}).get("support_size")
            == api_payload.get("slc_support")
            and bell_cli_payload.get("result_payload", {}).get("state_hash")
            == api_payload.get("state_hash")
            and bell_cli_payload.get("result_payload", {}).get("history_hash")
            == api_payload.get("history_hash")
        )
        console_parity = console_probe["status"] == "PASS" and console_payload == bell_cli_payload
        all_pass = (
            build["status"] == "PASS"
            and install["status"] == "PASS"
            and all(value == "PASS" for value in case_results.values())
            and api["status"] == "PASS"
            and str(api_payload.get("id", "")).startswith("SLC_STATE_")
            and api_payload.get("census") == 321
            and api_payload.get("source") == "PASS"
            and api_payload.get("slc_support") == 2
            and cli_api_parity
            and console_parity
            and sidecar["status"] == "PASS"
            and not wheel_data_missing
            and not dependency_lines
            and all(pyproject_checks.values())
            and no_repo_path
            and no_tracebacks
            and module_in_venv
            and ui_dependency_absent
        )
        wheel_hash = sha256(wheel)
        durable_wheel = None
        if all_pass:
            dist = candidate / "dist"
            dist.mkdir(exist_ok=True)
            durable_wheel = dist / wheel.name
            shutil.copyfile(wheel, durable_wheel)
        return {
            "status": "PASS" if all_pass else "FAIL",
            "wheel_path": str(durable_wheel) if durable_wheel else None,
            "wheel_name": wheel.name,
            "wheel_sha256": wheel_hash,
            "wheel_members": len(members),
            "wheel_data_missing": wheel_data_missing,
            "requires_dist": dependency_lines,
            "cli_cases": case_results,
            "api_payload": api_payload,
            "cli_api_parity": cli_api_parity,
            "console_entry_point_parity": console_parity,
            "pyproject_checks": pyproject_checks,
            "sidecar_absent": sidecar["status"] == "PASS",
            "ui_dependency_absent": ui_dependency_absent,
            "repository_path_absent": no_repo_path,
            "module_loaded_from_venv": module_in_venv,
            "tracebacks_found": not no_tracebacks,
            "commands": commands,
        }
