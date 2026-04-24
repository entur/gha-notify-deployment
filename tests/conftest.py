"""Shared fixtures for bash script tests."""
import json
import os
import queue
import threading
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Generator

import pytest


@dataclass
class CapturedRequest:
    method: str
    path: str
    headers: dict
    body: dict = field(default_factory=dict)


class _CapturingHandler(BaseHTTPRequestHandler):
    """HTTP handler that captures one request and pushes it onto a queue."""

    def log_message(self, *args):
        pass  # silence access log noise

    def _capture(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        body = json.loads(raw) if raw else {}
        self.server.captured_requests.put(
            CapturedRequest(
                method=self.command,
                path=self.path,
                headers=dict(self.headers),
                body=body,
            )
        )
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        self._capture()

    def do_GET(self):
        self._capture()


class _CapturingServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.captured_requests: queue.Queue[CapturedRequest] = queue.Queue()


@pytest.fixture()
def mock_server() -> Generator[_CapturingServer, None, None]:
    """Start a local HTTP server that captures incoming requests.

    Yields the server so tests can read captured requests via
    server.captured_requests.get(timeout=5).
    """
    server = _CapturingServer(("127.0.0.1", 0), _CapturingHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        thread.join(timeout=5)


@pytest.fixture()
def script_env() -> dict:
    """Base environment for running bash scripts."""
    return os.environ.copy()
