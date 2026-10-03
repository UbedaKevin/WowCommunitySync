import unittest

from models.character import Character
from services.character_service import CharacterService


class TestCharacterService(unittest.TestCase):

    def test_load_characters(self):
        data = {
            "Player-TEST-123": {
                "name": "Test",
                "realm": "TestRealm",
                "level": 10,
                "class": "Warrior",
                "classFile": "WARRIOR",
                "race": "Human",
                "raceFile": "Human",
                "raceID": 1,
                "faction": "Alliance",
                "guild": None,
                "guid": "Player-TEST-123",
                "professions": {},
                "equipment": {},
            }
        }

        service = CharacterService()

        characters = service.load_characters(data)

        self.assertEqual(len(characters), 1)

        character = characters[0]

        self.assertIsInstance(character, Character)
        self.assertEqual(character.key, "Player-TEST-123")
        self.assertEqual(character.name, "Test")
        self.assertEqual(character.realm, "TestRealm")
        self.assertEqual(character.level, 10)
        self.assertEqual(character.class_name, "Warrior")
        self.assertEqual(character.guid, "Player-TEST-123")

    def test_build_payload(self):
        data = {
            "Player-TEST-123": {
                "name": "Test",
                "realm": "TestRealm",
                "level": 10,
                "class": "Warrior",
                "classFile": "WARRIOR",
                "race": "Human",
                "raceFile": "Human",
                "raceID": 1,
                "faction": "Alliance",
                "guild": None,
                "guid": "Player-TEST-123",
                "professions": {},
                "equipment": {},
            }
        }

        service = CharacterService()
        service.load_characters(data)

        payload = service.build_payload()

        self.assertIn("characters", payload)
        self.assertEqual(len(payload["characters"]), 1)

        character = payload["characters"][0]

        self.assertEqual(
            character["key"],
            "Player-TEST-123"
        )

        self.assertEqual(
            character["name"],
            "Test"
        )

        self.assertEqual(
            character["level"],
            10
        )

        self.assertEqual(
            character["guid"],
            "Player-TEST-123"
        )

if __name__ == "__main__":
    unittest.main()