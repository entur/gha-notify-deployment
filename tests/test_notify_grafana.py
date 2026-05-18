"""Tests for bash/notify_grafana.sh."""
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / "bash" / "notify_grafana.sh"

BASE_ENV = {
    "REPO": "test-org/test-repo",
    "ENVIRONMENT": "production",
    "GRAFANA_API_TOKEN": "grafana-token",
    "END_TIME": "1778150692337",
    "START_TIME": "1778152550281",
    "GRAFANA_ANNOTATION_TEXT": "",
    "GRAFANA_ANNOTATION_TAGS": "",
}


def run_script(env: dict, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(SCRIPT)],
        env=env,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )


@pytest.fixture()
def server_env(mock_server, script_env, tmp_path):
    """Return (server, env, tmp_path) with GRAFANA_URL pointing at the mock server."""
    host, port = mock_server.server_address
    env = {**script_env, **BASE_ENV, "GRAFANA_URL": f"http://{host}:{port}"}
    return mock_server, env, tmp_path


class TestPayload:
    def test_sends_deployment_tag(self, server_env):
        server, env, tmp_path = server_env
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert "deployment" in req.body["tags"]

    def test_sends_environment_tag(self, server_env):
        server, env, tmp_path = server_env
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert "production" in req.body["tags"]

    def test_sends_repo_tag(self, server_env):
        server, env, tmp_path = server_env
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert "test-org/test-repo" in req.body["tags"]

    def test_message_contains_annotation_text(self, server_env):
        server, env, tmp_path = server_env
        env["GRAFANA_ANNOTATION_TEXT"] = "my-app:1.2.3"
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert "my-app:1.2.3" in req.body["text"]

    def test_sends_start_time(self, server_env):
        server, env, tmp_path = server_env
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert req.body["time"] == 1778152550281

    def test_sends_end_time(self, server_env):
        server, env, tmp_path = server_env
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert req.body["timeEnd"] == 1778150692337


class TestAnnotation:
    def test_annotation_text_sent_as_message(self, server_env):
        server, env, tmp_path = server_env
        env["GRAFANA_ANNOTATION_TEXT"] = "my-app:v1.2.3"
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert req.body["text"] == "my-app:v1.2.3"

    def test_extra_tags_included_when_set(self, server_env):
        server, env, tmp_path = server_env
        env["GRAFANA_ANNOTATION_TAGS"] = "team-a service-x"
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert "team-a" in req.body["tags"]
        assert "service-x" in req.body["tags"]

    def test_extra_tags_absent_when_not_set(self, server_env):
        server, env, tmp_path = server_env
        env["GRAFANA_ANNOTATION_TAGS"] = ""
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert req.body["tags"] == ["deployment", "test-org/test-repo", "production"]


class TestTimeDefaults:
    def test_end_time_defaults_to_current_utc_when_empty(self, server_env):
        server, env, tmp_path = server_env
        # The script treats empty string the same as unset: it calls `date -u`
        env["END_TIME"] = ""
        env["START_TIME"] = ""
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert isinstance(req.body["timeEnd"], int), "expected a unix timestamp"

    def test_start_time_defaults_to_end_time_when_empty(self, server_env):
        server, env, tmp_path = server_env
        env["END_TIME"] = "1778150692337"
        env["START_TIME"] = ""
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert req.body["time"] == req.body["timeEnd"]


class TestRequest:
    def test_uses_post_method(self, server_env):
        server, env, tmp_path = server_env
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert req.method == "POST"

    def test_posts_to_annotations_path(self, server_env):
        server, env, tmp_path = server_env
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert req.path == "/api/annotations"

    def test_sends_json_content_type(self, server_env):
        server, env, tmp_path = server_env
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert req.headers.get("Content-Type") == "application/json"

    def test_sends_bearer_token(self, server_env):
        server, env, tmp_path = server_env
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert req.headers.get("Authorization") == "Bearer grafana-token"


class TestOutput:
    def test_prints_success_message_on_200(self, server_env):
        _, env, tmp_path = server_env
        result = run_script(env, tmp_path)
        assert "Notification dispatched to Grafana" in result.stdout

    def test_prints_failure_message_when_server_unreachable(self, script_env, tmp_path):
        env = {
            **script_env,
            **BASE_ENV,
            "GRAFANA_URL": "http://127.0.0.1:1",  # nothing listening here
        }
        result = run_script(env, tmp_path)
        assert "Failed to send notification to Grafana" in result.stdout

    def test_logs_curl_error_to_file_on_failure(self, script_env, tmp_path):
        env = {
            **script_env,
            **BASE_ENV,
            "GRAFANA_URL": "http://127.0.0.1:1",
        }
        run_script(env, tmp_path)
        log = tmp_path / "deployment_notification_errors.log"
        assert log.exists(), "error log file was not created"
        assert log.stat().st_size > 0, "error log file is empty"
