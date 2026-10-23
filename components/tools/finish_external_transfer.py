"""Serialize external-study verification and software checks after inference."""
import argparse
import ctypes
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

import psutil

from external_transfer import ROOT, REPO, guard, read, write
from component_inspector.vision.ksdd2_ensemble import sha256
from component_inspector.vision.resources import run_bounded


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wait-controller-pid", type=int, required=True)
    args = parser.parse_args(); tools = Path(__file__).resolve().parent
    process = psutil.Process(args.wait_controller_pid)
    assert any(Path(v).name == "external_transfer.py" for v in process.cmdline()) and "run" in process.cmdline()
    deadline = time.monotonic() + 7200
    print("WAIT for all registered external inference; no parallel audit or ML", flush=True)
    while process.is_running():
        if time.monotonic() > deadline: raise TimeoutError("External inference wait expired")
        try: process.wait(timeout=30)
        except psutil.TimeoutExpired: continue
        break
    protocol = guard()
    assert all((ROOT / f"predictions-{d}.json").is_file() for d in protocol["datasets"])
    assert all(read(ROOT / f"score-{d}-resources.json")["status"] == "completed" for d in protocol["datasets"])
    audit = ROOT.parent / (ROOT.name + "-audit"); audit.mkdir(exist_ok=False)
    result = run_bounded([sys.executable, str(tools / "verify_external_transfer.py")], audit / "worker.log",
                         max_rss_bytes=min(4 * 1024**3, int(.6 * psutil.virtual_memory().available)), max_seconds=1800)
    write(audit / "resources.json", result); print("AUDIT", result, flush=True)
    if result["status"] != "completed": raise RuntimeError("Preserve failed external audit")
    subprocess.run([sys.executable, str(tools / "report_external_transfer.py")], check=True)
    software = ROOT.parent / (ROOT.name + "-software"); software.mkdir(exist_ok=False)
    command = [sys.executable, "-m", "pytest", "components/tests", "-q", "--junitxml", str(software / "junit.xml")]
    result = run_bounded(command, software / "worker.log",
                         max_rss_bytes=min(4 * 1024**3, int(.6 * psutil.virtual_memory().available)), max_seconds=1800)
    write(software / "resources.json", result); print("SOFTWARE", result, flush=True)
    if result["status"] != "completed": raise RuntimeError("Preserve failed external-study software check")
    xml = ET.parse(software / "junit.xml").getroot()
    suites = list(xml) if xml.tag == "testsuites" else [xml]
    counts = {key: sum(int(row.attrib.get(key, 0)) for row in suites) for key in ("tests", "failures", "errors", "skipped")}
    assert counts["failures"] == counts["errors"] == 0
    write(software / "summary.json", {"counts": counts, "passed": counts["tests"] - counts["skipped"],
          "command": command, "scope": "Software checks only; not independent image evaluations."})
    export = REPO / "docs/research/external-transfer-software"; export.mkdir(exist_ok=False); files = {}
    for path in software.iterdir():
        if not path.is_file(): continue
        shutil.copyfile(path, export / path.name)
        files[path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    write(export / "export-index.json", {"files": files, "scope": "Full software regression after external inference and audit."})
    for name in ("resources.json", "worker.log"):
        target = REPO / "docs/research" / ("2026-10-23-external-transfer-audit-" + name)
        assert not target.exists(); shutil.copyfile(audit / name, target)
    print("EXTERNAL TRANSFER PROOF AND REPORT COMPLETE", counts, flush=True)


if __name__ == "__main__":
    if sys.platform == "win32":
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.SetThreadExecutionState.argtypes = [ctypes.c_uint]; kernel.SetThreadExecutionState.restype = ctypes.c_uint
        if not kernel.SetThreadExecutionState(0x80000001): raise ctypes.WinError(ctypes.get_last_error())
        try: main()
        finally: kernel.SetThreadExecutionState(0x80000000)
    else: main()
