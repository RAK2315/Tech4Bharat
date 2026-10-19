"""Setup diagnostics and safe acquisition; model commands are not implemented."""

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
        "stage": "runtime_diagnostics_only",
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
        "implemented_commands": ["doctor", "acquire", "prepare", "develop", "spike",
                                 "freeze", "calibrate", "evaluate", "stress", "report"],
        "models_ready": False,
        "datasets_downloaded": False,
        "readiness_note": (
            "Doctor readiness flags are conservative defaults, not a source or model audit. "
            "Use the implementation ledger and hash-verified frozen run for actual experiment status."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Tech4Bharat research component inspector")
    commands = parser.add_subparsers(dest="command", required=True)
    doctor = commands.add_parser("doctor", help="Report isolated setup runtime and scaffold status")
    doctor.add_argument("--json", action="store_true", help="Emit machine-readable diagnostics")
    acquisition = commands.add_parser("acquire", help="Acquire approved research data safely")
    acquisition.add_argument("--dataset", required=True, choices=["mvtec_ad", "mvtec_3d_ad", "ksdd2"])
    acquisition.add_argument("--category")
    acquisition.add_argument("--archive", type=Path)
    acquisition.add_argument("--root", type=Path, help="Isolated project root (default: components)")
    preparation = commands.add_parser('prepare', help='Verify sources and audit immutable data roles')
    preparation.add_argument('--config', type=Path, default=Path(__file__).resolve().parents[2]/'configs/protocol.yaml')
    development = commands.add_parser('develop', help='Fit B0 and score allowed development records only')
    development.add_argument('--config', type=Path, required=True)
    development.add_argument('--manifest', type=Path, required=True)
    feasibility = commands.add_parser('spike', help='Supervised native P0 development feasibility')
    feasibility.add_argument('--config',type=Path,required=True)
    feasibility.add_argument('--manifest',type=Path,required=True)
    feasibility.add_argument('--weights',type=Path,required=True)
    frozen = commands.add_parser('freeze', help='Verify and freeze both methods before calibration/test')
    for name in ('config','manifest','baseline-summary','candidate-summary','reconciliation'):
        frozen.add_argument('--'+name,type=Path,required=True)
    for name in ('calibrate','evaluate','stress','report'):
        phase_parser=commands.add_parser(name,help='Run frozen '+name)
        phase_parser.add_argument('--run',type=Path,required=True)
    args = parser.parse_args(argv)
    if args.command in ('freeze','calibrate','evaluate','stress','report'):
        try:
            if args.command=='freeze':
                from component_inspector.evaluation.freeze import freeze_experiment
                result=freeze_experiment(args.config,args.manifest,args.baseline_summary,args.candidate_summary,args.reconciliation)
            elif args.command=='report':
                from component_inspector.evaluation.reports import report
                result=report(args.run)
            else:
                from component_inspector.evaluation.runner import execute
                result=execute(args.run,'calibration' if args.command=='calibrate' else args.command)
            print(json.dumps(result,indent=2))
            return 0
        except (ValueError,OSError,RuntimeError) as exc:
            print(json.dumps({'status':'failed','error':str(exc)}),file=sys.stderr)
            return 1
    if args.command == 'spike':
        import logging
        logging.basicConfig(level=logging.INFO,format='%(message)s')
        from component_inspector.vision.spike import spike
        try:
            result=spike(args.config,args.manifest,args.weights)
            print(json.dumps(result,indent=2))
            return 0 if result['status']=='development_only_uncalibrated' else 3
        except (ValueError,OSError) as exc:
            print(json.dumps({'status':'failed','error':str(exc)}),file=sys.stderr)
            return 1
    if args.command == 'develop':
        import logging
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        from component_inspector.vision.develop import develop_reference
        try:
            print(json.dumps(develop_reference(args.config, args.manifest), indent=2))
            return 0
        except (ValueError, OSError) as exc:
            print(json.dumps({'status': 'failed', 'error': str(exc)}), file=sys.stderr)
            return 1
    if args.command == 'prepare':
        import logging
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        from component_inspector.data.prepare import prepare_project
        try:
            print(json.dumps(prepare_project(args.config), indent=2))
            return 0
        except (ValueError, OSError) as exc:
            print(json.dumps({'status': 'failed', 'error': str(exc)}), file=sys.stderr)
            return 1
    if args.command == "acquire":
        from component_inspector.data.acquire import acquire, AcquisitionError
        try:
            result = acquire(args.dataset, category=args.category, archive=args.archive, root=args.root)
        except AcquisitionError as exc:
            print(json.dumps({"status": "failed", "error": str(exc)}), file=sys.stderr)
            return 1
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "acquired" else 3
    report = doctor_report()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Python: {report['python']['version']}")
        print(f"Isolated environment: {report['python']['isolated']}")
        print(f"Project: {report['project_root']}")
        print("Runtime diagnostics only; see the implementation ledger for verified experiment status.")
    return 0 if report["setup_runtime_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
