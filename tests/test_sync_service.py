import unittest
from unittest.mock import Mock, patch

from services.sync_service import (
    SyncService,
    SyncServiceError,
)
from wow_saved_variables import SavedVariablesError

class TestSyncService(unittest.TestCase):

    @patch("services.sync_service.find_saved_variables")
    @patch("services.sync_service.load_characters")
    def test_sync(
        self,
        mock_load_characters,
        mock_find_saved_variables
    ):
        mock_find_saved_variables.return_value = (
            "C:/test/WoWCommunityCollector.lua"
        )

        mock_load_characters.return_value = {
            "Player-TEST-123": {
                "name": "Test",
                "realm": "TestRealm",
                "level": 10,
                "guid": "Player-TEST-123",
            }
        }

        api_service = Mock()

        api_service.sync_characters.return_value = {
            "status": "ok"
        }

        service = SyncService(api_service)

        response = service.sync()

        self.assertEqual(
            response,
            {"status": "ok"}
        )

        mock_find_saved_variables.assert_called_once()
        mock_load_characters.assert_called_once()

        api_service.sync_characters.assert_called_once()

        payload = (
            api_service
            .sync_characters
            .call_args
            .args[0]
        )

        self.assertIn(
            "characters",
            payload
        )

        self.assertEqual(
            len(payload["characters"]),
            1
        )

        self.assertEqual(
            payload["characters"][0]["name"],
            "Test"
        )
        
    @patch("services.sync_service.find_saved_variables")
    def test_sync_saved_variables_not_found(
        self,
        mock_find_saved_variables
    ):
        mock_find_saved_variables.return_value = None

        api_service = Mock()

        service = SyncService(api_service)

        with self.assertRaises(SyncServiceError):
            service.sync()

        api_service.sync_characters.assert_not_called()

    @patch("services.sync_service.find_saved_variables")
    @patch("services.sync_service.load_characters")
    def test_sync_invalid_saved_variables(
        self,
        mock_load_characters,
        mock_find_saved_variables
    ):
        mock_find_saved_variables.return_value = (
            "C:/test/WoWCommunityCollector.lua"
        )

        mock_load_characters.side_effect = (
            SavedVariablesError("Fichier invalide.")
        )

        api_service = Mock()

        service = SyncService(api_service)

        with self.assertRaises(SyncServiceError) as context:
            service.sync()

        self.assertIn(
            "Impossible de lire les SavedVariables",
            str(context.exception)
        )

        api_service.sync_characters.assert_not_called()
        
    @patch("services.sync_service.find_saved_variables")
    @patch("services.sync_service.load_characters")
    def test_sync_assigns_character_ids(
        self,
        mock_load_characters,
        mock_find_saved_variables
    ):
        mock_find_saved_variables.return_value = (
            "C:/test/WoWCommunityCollector.lua"
        )

        mock_load_characters.return_value = {
            "Player-TEST-123": {
                "name": "Test",
                "realm": "TestRealm",
                "level": 10,
                "guid": "Player-TEST-123",
            }
        }

        api_service = Mock()

        api_service.sync_characters.return_value = {
            "status": "ok",
            "characters": [
                {
                    "id": 42,
                    "guid": "Player-TEST-123",
                    "name": "Test",
                }
            ],
        }

        service = SyncService(api_service)

        service.sync()

        characters = service.character_service.characters

        self.assertEqual(len(characters), 1)

        self.assertEqual(
            characters[0].id,
            42
        )

        # print(
        #     f"{characters[0].name} -> PostgreSQL ID {characters[0].id}"
        # )

    def test_get_character_events(self):
        api_service = Mock()

        api_service.get_character_events.return_value = {
            "status": "ok",
            "events": [
                {
                    "id": 12,
                    "event_type": "LEVEL_UP",
                }
            ],
            "pagination": {
                "limit": 20,
                "offset": 0,
                "hasMore": False,
                "total": 1,
            },
        }

        service = SyncService(api_service)

        character = Mock()
        character.id = 4
        character.name = "Mjolnir Fury"

        response = service.get_character_events(
            character
        )

        self.assertEqual(
            response["status"],
            "ok"
        )

        self.assertEqual(
            len(response["events"]),
            1
        )

        api_service.get_character_events.assert_called_once_with(
            4,
            limit=20,
            offset=0
        )

if __name__ == "__main__":
    unittest.main()