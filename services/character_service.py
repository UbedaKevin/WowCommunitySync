import json

from models.character import Character


class CharacterService:

    def __init__(self):
        self.characters = []

    def load_characters(self, data):
        """
        Transforme les données brutes des SavedVariables
        en objets Character.
        """

        characters_data = data

        self.characters = []

        for character_key, character_data in characters_data.items():

            character = Character(
                character_key,
                character_data
            )

            self.characters.append(
                character
            )

        return self.characters

    def build_payload(self):
        """
        Construit le payload qui sera envoyé à l'API.
        """

        return {
            "characters": [
                character.to_dict()
                for character in self.characters
            ]
        }

    def print_payload(self):
        """
        Affiche le payload JSON pour les tests.
        """

        payload = self.build_payload()

        print(
            json.dumps(
                payload,
                indent=4,
                ensure_ascii=False
            )
        )