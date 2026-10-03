import requests


class ApiServiceError(Exception):
    """Erreur lors de la communication avec l'API."""


class ApiService:

    def __init__(self, base_url, access_token):
        self.base_url = base_url.rstrip("/")
        self.access_token = access_token

    def sync_characters(self, payload):
        url = f"{self.base_url}/api/characters/sync"

        headers = {
        "Authorization": f"Bearer {self.access_token}"
        }

        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=10
            )

            response.raise_for_status()

        except requests.HTTPError as error:
            status_code = error.response.status_code

            raise ApiServiceError(
                f"L'API a retourné une erreur HTTP {status_code}."
            ) from error

        except requests.RequestException as error:
            raise ApiServiceError(
                f"Erreur réseau lors de la communication avec l'API : {error}"
            ) from error

        try:
            return response.json()

        except ValueError as error:
            raise ApiServiceError(
                "L'API a retourné une réponse JSON invalide."
            ) from error

