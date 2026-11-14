import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_settings(env_changes):
    """Import config.settings in a fresh Python process and return the result."""
    env = os.environ.copy()
    env.pop("DJANGO_SECRET_KEY", None)
    env.update(env_changes)
    return subprocess.run(
        [sys.executable, "-c", "import config.settings"],
        check=False,  # a failing exit code is what the test inspects
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )


def test_settings_refuse_to_load_without_secret_key_when_debug_is_off():
    result = load_settings({"DJANGO_DEBUG": "False"})

    assert result.returncode != 0
    assert "ImproperlyConfigured" in result.stderr


def test_settings_load_with_dev_key_when_debug_is_on():
    result = load_settings({"DJANGO_DEBUG": "True"})

    assert result.returncode == 0
