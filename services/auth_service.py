import json
from pathlib import Path

from services.api_service import ApiService, ApiServiceError


class AuthServiceError(Exception):
    """Erreur lors de l'authentification."""


class AuthService:
    def __init__(self, api_service, session_file=None):
        self.api_service = api_service

        if session_file is None:
            session_file = Path.home() / ".wowcommunity_session.json"

        self.session_file = Path(session_file)

        self.access_token = None
        self.expires_at = None
        self.user = None

    def login(self, email, password, remember_me=True):
        try:
            response = self.api_service.login(email, password)
        except ApiServiceError as error:
            raise AuthServiceError(
                f"Impossible de se connecter : {error}"
            ) from error

        self.access_token = response.get("accessToken")
        self.expires_at = response.get("expiresAt")
        self.user = response.get("user")

        if not self.access_token:
            raise AuthServiceError(
                "L'API n'a pas retourné de token d'accès."
            )

        self.api_service.set_access_token(
            self.access_token
        )

        if remember_me:
            self._save_session()

        return response

    def load_session(self):
        if not self.session_file.exists():
            return False

        try:
            with self.session_file.open(
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError) as error:
            raise AuthServiceError(
                "Impossible de lire la session locale."
            ) from error

        self.access_token = data.get("accessToken")
        self.expires_at = data.get("expiresAt")
        self.user = data.get("user")

        if not self.access_token:
            return False
        
        self.api_service.set_access_token(self.access_token)
        
        try:
            response = self.api_service.get_current_user(
                self.access_token
            )
        except ApiServiceError:
            self.access_token = None
            self.expires_at = None
            self.user = None

            try:
                self.session_file.unlink()
            except OSError:
                pass

            return False

        self.user = response.get("user")
        self.expires_at = response.get(
            "session",
            {}
        ).get("expiresAt", self.expires_at)

        return True

    def logout(self):
        self.access_token = None
        self.expires_at = None
        self.user = None

        try:
            if self.session_file.exists():
                self.session_file.unlink()
        except OSError as error:
            raise AuthServiceError(
                "Impossible de supprimer la session locale."
            ) from error

    def is_authenticated(self):
        return bool(self.access_token)

    def _save_session(self):
        data = {
            "accessToken": self.access_token,
            "expiresAt": self.expires_at,
            "user": self.user,
        }

        try:
            with self.session_file.open(
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )
        except OSError as error:
            raise AuthServiceError(
                "Impossible de sauvegarder la session locale."
            ) from error