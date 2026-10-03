from pathlib import Path


SAVED_VARIABLES_NAME = "WoWCommunityCollector.lua"

WOW_INSTALL_PATHS = [
    Path(r"C:\Program Files (x86)\World of Warcraft"),
    Path(r"C:\Program Files\World of Warcraft"),
]

class WoWPathError(Exception):
    """Erreur lors de la recherche des SavedVariables."""

def find_saved_variables(install_paths=None):
    """
    Recherche automatiquement le fichier
    WoWCommunityCollector.lua dans les installations
    WoW connues.
    """
    if install_paths is None:
        install_paths = WOW_INSTALL_PATHS
    
    found_files = []

    for wow_path in install_paths:
        if not wow_path.exists():
            continue

        matches = wow_path.glob(
            f"_classic_beta_/WTF/Account/*/SavedVariables/{SAVED_VARIABLES_NAME}"
        )

        for path in matches:
            if path.is_file():
                found_files.append(path)

    if not found_files:
        return None

    if len(found_files) > 1:
        raise WoWPathError(
            "Plusieurs fichiers SavedVariables ont été trouvés."
        )

    return found_files[0]