import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from services.api_service import (
    ApiService,
    ApiServiceError,
)

class ErrorHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        pass

class InvalidJsonHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        body = b"ceci n'est pas du json"

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "application/json"
        )
        self.send_header(
            "Content-Length",
            str(len(body))
        )
        self.end_headers()

        self.wfile.write(body)

    def log_message(self, format, *args):
        pass

class TestApiService(unittest.TestCase):

    def test_network_error(self):
        api = ApiService(
            "http://localhost:3999",
            "test-token"
        )

        with self.assertRaises(ApiServiceError):
            api.sync_characters({
                "characters": []
            })

    def test_http_error(self):
        server = HTTPServer(
            ("localhost", 0),
            ErrorHandler
        )

        thread = Thread(
            target=server.serve_forever,
            daemon=True
        )

        thread.start()

        try:
            port = server.server_port

            api = ApiService(
                f"http://localhost:{port}",
                "test-token"
            )

            with self.assertRaises(ApiServiceError):
                api.sync_characters({
                    "characters": []
                })

        finally:
            server.shutdown()
            server.server_close()

    def test_invalid_json_response(self):
        server = HTTPServer(
            ("localhost", 0),
            InvalidJsonHandler
        )

        thread = Thread(
            target=server.serve_forever,
            daemon=True
        )

        thread.start()

        try:
            port = server.server_port

            api = ApiService(
                f"http://localhost:{port}",
                "test-token"
            )

            with self.assertRaises(ApiServiceError):
                api.sync_characters({
                    "characters": []
                })

        finally:
            server.shutdown()
            server.server_close()
            
if __name__ == "__main__":
    unittest.main()