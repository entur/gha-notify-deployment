"""Integration tests for bash/notify_gitdailies.sh against a real GitDailies endpoint.

Requires the following environment variables to be set:
  REAL_GITDAILIES_URL  – the real GitDailies webhook URL
  REAL_GITDAILIES_KEY  – the real GitDailies webhook key
"""
import os
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / "bash" / "notify_gitdailies.sh"

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not os.environ.get("REAL_GITDAILIES_URL") or not os.environ.get("REAL_GITDAILIES_KEY"),
        reason="REAL_GITDAILIES_URL and REAL_GITDAILIES_KEY must be set to run integration tests",
    ),
]


def test_sends_notification_to_gitdailies(script_env, tmp_path):
    env = {
        **script_env,
        "REPO": "entur/gha-notify-deployment",
        "BRANCH": "main",
        "COMMIT_SHA": "8d1a8c6537bf44189c3d05635efd8373a5d3ef2f",
        "GITDAILIES_KEY": os.environ["REAL_GITDAILIES_KEY"],
        "GITDAILIES_URL": os.environ["REAL_GITDAILIES_URL"],
    }
    result = subprocess.run(
        ["bash", str(SCRIPT)],
        env=env,
        capture_output=True,
        text=True,
        cwd=str(tmp_path),
        check=False,
    )
    assert "Notification dispatched to GitDailies" in result.stdout
