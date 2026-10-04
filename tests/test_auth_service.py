import tempfile
import unittest
from pathlib import Path

from services.auth_service import AuthService


class FakeApiService:
    def login(self, email, password):
        return {
            "status": "ok",
            "accessToken": "test-access-token",
            "expiresAt": "2099-01-01T00:00:00.000Z",
            "user": {
                "id": 1,
                "email": email,
            },
        }
    def set_access_token(self, access_token):
        self.access_token = access_token
        
    def get_current_user(self, access_token):
        if access_token != "test-access-token":
            raise Exception("Invalid token")

        return {
            "status": "ok",
            "user": {
                "id": 1,
                "email": "test@example.com",
            },
            "session": {
                "expiresAt": "2099-01-01T00:00:00.000Z",
            },
        }


class AuthServiceTests(unittest.TestCase):

    def test_login_saves_session(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            session_file = Path(temp_dir) / "session.json"

            auth_service = AuthService(
                FakeApiService(),
                session_file=session_file,
            )

            response = auth_service.login(
                "test@example.com",
                "password",
            )

            self.assertEqual(
                response["accessToken"],
                "test-access-token",
            )

            self.assertTrue(
                session_file.exists()
            )

            self.assertEqual(
                auth_service.access_token,
                "test-access-token",
            )

    def test_load_session(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            session_file = Path(temp_dir) / "session.json"

            api_service = FakeApiService()

            first_auth = AuthService(
                api_service,
                session_file=session_file,
            )

            first_auth.login(
                "test@example.com",
                "password",
            )

            second_auth = AuthService(
                api_service,
                session_file=session_file,
            )

            self.assertTrue(
                second_auth.load_session()
            )

            self.assertEqual(
                second_auth.access_token,
                "test-access-token",
            )

            self.assertEqual(
                second_auth.user["email"],
                "test@example.com",
            )

    def test_logout_removes_session(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            session_file = Path(temp_dir) / "session.json"

            auth_service = AuthService(
                FakeApiService(),
                session_file=session_file,
            )

            auth_service.login(
                "test@example.com",
                "password",
            )

            auth_service.logout()

            self.assertFalse(
                session_file.exists()
            )

            self.assertFalse(
                auth_service.is_authenticated()
            )


if __name__ == "__main__":
    unittest.main()