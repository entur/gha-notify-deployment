"""Tests for bash/notify_gitdailies.sh."""
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / "bash" / "notify_gitdailies.sh"

BASE_ENV = {
    "REPO": "test-org/test-repo",
    "BRANCH": "main",
    "COMMIT_SHA": "abc123",
    "GITDAILIES_KEY": "secret-key",
}


def run_script(env: dict, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(SCRIPT)],
        env=env,
        capture_output=True,
        text=True,
        cwd=str(cwd),
        check=False,
    )


@pytest.fixture()
def server_env(mock_server, script_env, tmp_path):
    """Return (server, env, tmp_path) with GITDAILIES_URL pointing at the mock server."""
    host, port = mock_server.server_address
    env = {**script_env, **BASE_ENV, "GITDAILIES_URL": f"http://{host}:{port}"}
    return mock_server, env, tmp_path


class TestPayload:
    def test_sends_correct_repo(self, server_env):
        server, env, tmp_path = server_env
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert req.body["repo"] == "test-org/test-repo"

    def test_sends_correct_branch(self, server_env):
        server, env, tmp_path = server_env
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert req.body["branch"] == "main"

    def test_sends_correct_commit_sha(self, server_env):
        server, env, tmp_path = server_env
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert req.body["commitSHA"] == "abc123"

    def test_kind_is_always_deployed(self, server_env):
        server, env, tmp_path = server_env
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert req.body["kind"] == "deployed"


class TestRequest:
    def test_uses_post_method(self, server_env):
        server, env, tmp_path = server_env
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert req.method == "POST"

    def test_sends_json_content_type(self, server_env):
        server, env, tmp_path = server_env
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert req.headers.get("Content-Type") == "application/json"

    def test_sends_webhook_key_header(self, server_env):
        server, env, tmp_path = server_env
        run_script(env, tmp_path)
        req = server.captured_requests.get(timeout=5)
        assert req.headers.get("webhook-key") == "secret-key"


class TestOutput:
    def test_prints_success_message_on_200(self, server_env):
        _, env, tmp_path = server_env
        result = run_script(env, tmp_path)
        assert "Notification dispatched to GitDailies" in result.stdout

    def test_prints_failure_message_when_server_unreachable(self, script_env, tmp_path):
        env = {
            **script_env,
            **BASE_ENV,
            "GITDAILIES_URL": "http://127.0.0.1:1",  # nothing listening here
        }
        result = run_script(env, tmp_path)
        assert "Failed to send notification to GitDailies" in result.stdout

    def test_logs_curl_error_to_file_on_failure(self, script_env, tmp_path):
        env = {
            **script_env,
            **BASE_ENV,
            "GITDAILIES_URL": "http://127.0.0.1:1",
        }
        run_script(env, tmp_path)
        log = tmp_path / "deployment_notification_errors.log"
        assert log.exists(), "error log file was not created"
        assert log.stat().st_size > 0, "error log file is empty"
