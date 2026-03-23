'''A simple mock server to capture webhook payloads for testing purposes.'''
import http.server
import json
import threading


class _Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # suppress access log noise

    def do_POST(self):
        '''Handle incoming POST requests by capturing the payload and headers.'''
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        body["webhook-key"] = self.headers.get("webhook-key", "")
        self.send_response(200)
        self.end_headers()
        with open("captured.json", "w", encoding="UTF-8") as f:
            json.dump(body, f)
        threading.Thread(target=self.server.shutdown).start()


if __name__ == "__main__":
    http.server.HTTPServer(("", 8080), _Handler).serve_forever()
