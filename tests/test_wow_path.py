import unittest

from wow_path import (
    find_saved_variables,
    WoWPathError,
)
from pathlib import Path

class TestWowPath(unittest.TestCase):

    def test_saved_variables_found(self):
        path = find_saved_variables()

        self.assertIsNotNone(path)
        self.assertTrue(path.is_file())
        self.assertEqual(
            path.name,
            "WoWCommunityCollector.lua"
        )

    def test_saved_variables_not_found(self):
        install_path = Path(
            "C:/chemin/qui/nexiste/pas"
        )

        path = find_saved_variables(
            [install_path]
        )

        self.assertIsNone(path)
    
    def test_multiple_saved_variables(self):
        with self.subTest("plusieurs fichiers"):
            from tempfile import TemporaryDirectory

        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            file_1 = (
                root
                / "_classic_beta_"
                / "WTF"
                / "Account"
                / "Account1"
                / "SavedVariables"
                / "WoWCommunityCollector.lua"
            )

            file_2 = (
                root
                / "_classic_beta_"
                / "WTF"
                / "Account"
                / "Account2"
                / "SavedVariables"
                / "WoWCommunityCollector.lua"
            )

            file_1.parent.mkdir(parents=True)
            file_2.parent.mkdir(parents=True)

            file_1.write_text(
                "WoWCommunityCollectorDB = {}",
                encoding="utf-8"
            )

            file_2.write_text(
                "WoWCommunityCollectorDB = {}",
                encoding="utf-8"
            )

            with self.assertRaises(WoWPathError):
                find_saved_variables([root])

if __name__ == "__main__":
    unittest.main()