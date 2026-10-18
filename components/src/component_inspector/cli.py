"""Initial setup diagnostics; model and acquisition commands are not implemented."""

import argparse
from importlib import metadata
import json
from pathlib import Path
import platform
import shutil
import sys

import psutil
import yaml

from component_inspector import __version__


def doctor_report() -> dict:
    """Describe this scaffold's actual runtime, without claiming model readiness."""
    root = Path(__file__).resolve().parents[2]
    config_files = sorted((root / "configs").glob("*.yaml"))
    configurations = {}
    for path in config_files:
        with path.open(encoding="utf-8") as handle:
            config = yaml.safe_load(handle)
        configurations[path.name] = {
            "schema_version": config.get("schema_version"),
            "status": config.get("status", config.get("validation_status")),
        }

    packages = {}
    for name in ("PyYAML", "psutil", "pytest", "torch", "torchvision", "anomalib"):
        try:
            packages[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            packages[name] = None

    supported = sys.version_info[:2] == (3, 12)
    isolated = sys.prefix != sys.base_prefix
    return {
        "stage": "initial_scaffold",
        "package_version": __version__,
        "project_root": str(root),
        "python": {
            "version": platform.python_version(),
            "executable": sys.executable,
            "prefix": sys.prefix,
            "isolated": isolated,
            "supported": supported,
        },
        "setup_runtime_ready": supported and isolated,
        "resources": {
            "logical_cpu_count": psutil.cpu_count(),
            "available_ram_bytes": psutil.virtual_memory().available,
            "free_disk_bytes": shutil.disk_usage(root).free,
        },
        "packages": packages,
        "configurations": configurations,
        "implemented_commands": ["doctor"],
        "models_ready": False,
        "datasets_downloaded": False,
        "readiness_note": (
            "Initial scaffold only. Dataset acquisition, artifact validation and "
            "model inference are not implemented; these flags do not audit future data."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Tech4Bharat research component inspector")
    commands = parser.add_subparsers(dest="command", required=True)
    doctor = commands.add_parser("doctor", help="Report isolated setup runtime and scaffold status")
    doctor.add_argument("--json", action="store_true", help="Emit machine-readable diagnostics")
    args = parser.parse_args(argv)
    report = doctor_report()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Python: {report['python']['version']}")
        print(f"Isolated environment: {report['python']['isolated']}")
        print(f"Project: {report['project_root']}")
        print("Stage: initial scaffold; datasets and models are not ready.")
    return 0 if report["setup_runtime_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
