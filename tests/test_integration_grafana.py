"""Integration tests for bash/notify_grafana.sh against a real Grafana endpoint.

Requires the following environment variables to be set:
  REAL_GRAFANA_URL        – the real Grafana base URL (e.g. https://grafana.example.com)
  REAL_GRAFANA_API_TOKEN  – the real Grafana API token
"""
import os
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / "bash" / "notify_grafana.sh"

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not os.environ.get("REAL_GRAFANA_URL") or not os.environ.get("REAL_GRAFANA_API_TOKEN"),
        reason="REAL_GRAFANA_URL and REAL_GRAFANA_API_TOKEN must be set to run integration tests",
    ),
]


def test_sends_annotation_to_grafana(script_env, tmp_path):
    env = {
        **script_env,
        "REPO": "entur/gha-notify-deployment",
        "ENVIRONMENT": "development",
        "GRAFANA_ANNOTATION_TEXT": "integration-test",
        "GRAFANA_ANNOTATION_TAGS": "",
        "START_TIME": "",
        "END_TIME": "",
        "GRAFANA_API_TOKEN": os.environ["REAL_GRAFANA_API_TOKEN"],
        "GRAFANA_URL": os.environ["REAL_GRAFANA_URL"],
    }
    result = subprocess.run(
        ["bash", str(SCRIPT)],
        env=env,
        capture_output=True,
        text=True,
        cwd=str(tmp_path),
        check=False,
    )
    assert "Notification dispatched to Grafana" in result.stdout
