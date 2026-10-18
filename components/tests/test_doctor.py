"""Verify the setup command reports the real isolated runtime honestly."""

import json
from pathlib import Path
import subprocess
import sys


def test_doctor_reports_actual_environment_without_claiming_model_readiness():
    result = subprocess.run(
        [sys.executable, "-m", "component_inspector.cli", "doctor", "--json"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert Path(report["python"]["executable"]).resolve() == Path(sys.executable).resolve()
    assert Path(report["python"]["prefix"]).resolve() == Path(sys.prefix).resolve()
    assert report["python"]["isolated"] is True
    assert report["python"]["supported"] is True
    assert report["models_ready"] is False
    assert report["datasets_downloaded"] is False


def test_unimplemented_training_command_fails_instead_of_implying_training_ran():
    result = subprocess.run(
        [sys.executable, "-m", "component_inspector.cli", "fit"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "invalid choice" in result.stderr

