from services.api_service import ApiService
from services.character_service import CharacterService
from wow_path import find_saved_variables
from wow_saved_variables import (
    load_characters,
    SavedVariablesError,
)


class SyncServiceError(Exception):
    """Erreur lors de la synchronisation."""


class SyncService:

    def __init__(self, api_service):
        self.api_service = api_service
        self.character_service = CharacterService()

    def sync(self):

        file_path = find_saved_variables()

        if not file_path:
            raise SyncServiceError(
                "SavedVariables introuvable."
            )

        try:
            data = load_characters(file_path)

        except SavedVariablesError as error:
            raise SyncServiceError(
                f"Impossible de lire les SavedVariables : {error}"
            ) from error

        characters = self.character_service.load_characters(
            data
        )

        payload = self.character_service.build_payload()

        # print("SYNC PAYLOAD:", payload)

        response = self.api_service.sync_characters(
            payload
        )

        for character_data in response.get("characters", []):
            for character in characters:
                if character.guid == character_data.get("guid"):
                    character.id = character_data.get("id")

        return response

    def get_character_events(
        self,
        character,
        limit=20,
        offset=0
    ):
        if character.id is None:
            raise SyncServiceError(
                f"ID PostgreSQL introuvable pour {character.name}."
            )

        try:
            return self.api_service.get_character_events(
                character.id,
                limit=limit,
                offset=offset
            )

        except Exception as error:
            raise SyncServiceError(
                f"Impossible de récupérer les événements : {error}"
            ) from error