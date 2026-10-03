import unittest

from wow_path import find_saved_variables

from pathlib import Path
from tempfile import TemporaryDirectory

from wow_saved_variables import (
    SavedVariablesError,
    load_characters,
)

class TestSavedVariables(unittest.TestCase):

    def test_load_characters(self):
        file_path = find_saved_variables()

        self.assertIsNotNone(file_path)

        characters = load_characters(file_path)

        self.assertIsInstance(characters, dict)
        self.assertEqual(len(characters), 2)

        for key, character in characters.items():
            self.assertIn("name", character)
            self.assertIn("realm", character)
            self.assertIn("level", character)
            self.assertIn("guid", character)

    def test_invalid_saved_variables(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "invalid.lua"

            file_path.write_text(
                "WoWCommunityCollectorDB = { invalid",
                encoding="utf-8"
            )

            with self.assertRaises(SavedVariablesError):
                load_characters(file_path)
    def test_character_missing_guid(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "invalid.lua"

            file_path.write_text(
                """
                WoWCommunityCollectorDB = {
                    version = 1,
                    characters = {
                        ["Player-TEST-123"] = {
                            name = "Test",
                            realm = "TestRealm",
                            level = 10
                        }
                    }
                }
                """,
                encoding="utf-8"
            )

            with self.assertRaises(SavedVariablesError):
                load_characters(file_path)

if __name__ == "__main__":
    unittest.main()