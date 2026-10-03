import unittest
from unittest.mock import Mock, patch
from services.api_service import ApiService

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

    @patch("services.api_service.requests.get")
    def test_get_character_events(
        self,
        mock_get
    ):
        mock_response = Mock()

        mock_response.json.return_value = {
            "status": "ok",
            "events": [
                {
                    "id": 12,
                    "event_type": "LEVEL_UP",
                    "event_data": {
                        "oldLevel": 6,
                        "newLevel": 7,
                    },
                }
            ],
            "pagination": {
                "limit": 20,
                "offset": 0,
                "hasMore": False,
                "total": 1,
            },
        }

        mock_response.raise_for_status.return_value = None

        mock_get.return_value = mock_response

        api_service = ApiService(
            "http://localhost:3000",
            "test-token"
        )

        response = api_service.get_character_events(
            4
        )

        self.assertEqual(
            response["status"],
            "ok"
        )

        self.assertEqual(
            len(response["events"]),
            1
        )

        self.assertEqual(
            response["events"][0]["event_type"],
            "LEVEL_UP"
        )

        mock_get.assert_called_once_with(
            "http://localhost:3000/api/characters/4/events",
            headers={
                "Authorization": "Bearer test-token"
            },
            params={
                "limit": 20,
                "offset": 0,
            },
            timeout=10
        )
            
if __name__ == "__main__":
    unittest.main()