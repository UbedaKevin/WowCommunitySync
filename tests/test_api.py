from wow_path import (
    find_saved_variables,
    WoWPathError,
)
from wow_saved_variables import load_characters
from services.character_service import CharacterService
from services.api_service import (
    ApiService,
    ApiServiceError,
)
import config

def main():

    try:
        file_path = find_saved_variables()

    except WoWPathError as error:
        print(
            f"Erreur WoW : {error}"
        )
        return

    if not file_path:
        print("SavedVariables introuvable.")
        return

    print(
        f"SavedVariables trouvé :\n{file_path}\n"
    )

    data = load_characters(
        file_path
    )
    
    print("Clés trouvées dans SavedVariables :")
    for key in data:
        print("-", key)

    character_service = CharacterService()

    characters = character_service.load_characters(
        data
    )

    print("Personnages trouvés :", len(characters))

    for character in characters:
        print(
            character.key,
            "->",
            character.name
        )

    payload = character_service.build_payload()

    api = ApiService(
        config.API_BASE_URL,
        config.API_ACCESS_TOKEN
    )
    # print("\nPayload envoyé à l'API :")
    # character_service.print_payload()

    try:
        response = api.sync_characters(
            payload
        )

    except ApiServiceError as error:
        print(
            f"Erreur API : {error}"
        )
        return

    print("API response:")
    print(response)


if __name__ == "__main__":
    main()