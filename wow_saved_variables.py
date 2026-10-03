import re

class SavedVariablesError(Exception):
    """Erreur lors de la lecture ou du parsing des SavedVariables."""

class LuaParser:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.length = len(text)

    def skip_whitespace(self):
        while self.pos < self.length:
            char = self.text[self.pos]

            if char.isspace():
                self.pos += 1
                continue

            # Commentaire Lua sur une ligne
            if (
                char == "-"
                and self.pos + 1 < self.length
                and self.text[self.pos + 1] == "-"
            ):
                self.pos += 2

                while (
                    self.pos < self.length
                    and self.text[self.pos] != "\n"
                ):
                    self.pos += 1

                continue

            break

    def peek(self):
        self.skip_whitespace()

        if self.pos >= self.length:
            return None

        return self.text[self.pos]

    def consume(self, expected):
        self.skip_whitespace()

        if not self.text.startswith(expected, self.pos):
            raise ValueError(
                f"Expected '{expected}' at position {self.pos}"
            )

        self.pos += len(expected)

    def parse_string(self):
        self.skip_whitespace()

        quote = self.text[self.pos]

        if quote not in ('"', "'"):
            raise ValueError(
                f"Expected string at position {self.pos}"
            )

        self.pos += 1

        result = []

        while self.pos < self.length:
            char = self.text[self.pos]

            if char == "\\":
                self.pos += 1

                if self.pos >= self.length:
                    break

                escaped = self.text[self.pos]

                escape_map = {
                    "n": "\n",
                    "r": "\r",
                    "t": "\t",
                    "\\": "\\",
                    '"': '"',
                    "'": "'",
                }

                result.append(
                    escape_map.get(escaped, escaped)
                )

                self.pos += 1
                continue

            if char == quote:
                self.pos += 1
                return "".join(result)

            result.append(char)
            self.pos += 1

        raise ValueError("Unterminated string")

    def parse_number(self):
        self.skip_whitespace()

        match = re.match(
            r"-?\d+(?:\.\d+)?",
            self.text[self.pos:]
        )

        if not match:
            raise ValueError(
                f"Expected number at position {self.pos}"
            )

        value = match.group(0)
        self.pos += len(value)

        if "." in value:
            return float(value)

        return int(value)

    def parse_identifier(self):
        self.skip_whitespace()

        match = re.match(
            r"[A-Za-z_][A-Za-z0-9_]*",
            self.text[self.pos:]
        )

        if not match:
            raise ValueError(
                f"Expected identifier at position {self.pos}"
            )

        value = match.group(0)
        self.pos += len(value)

        return value

    def parse_value(self):
        self.skip_whitespace()

        char = self.peek()

        if char is None:
            raise ValueError("Unexpected end of file")

        if char in ('"', "'"):
            return self.parse_string()

        if char == "{":
            return self.parse_table()

        if char.isdigit() or char == "-":
            return self.parse_number()

        identifier = self.parse_identifier()

        if identifier == "true":
            return True

        if identifier == "false":
            return False

        if identifier == "nil":
            return None

        return identifier

    def parse_key(self):
        self.skip_whitespace()

        # ["key"]
        if self.text.startswith("[\"", self.pos):
            self.pos += 1

            key = self.parse_string()

            self.skip_whitespace()
            self.consume("]")

            return key

        # ['key']
        if self.text.startswith("['", self.pos):
            self.pos += 1

            key = self.parse_string()

            self.skip_whitespace()
            self.consume("]")

            return key

        # [123]
        if self.peek() == "[":
            self.pos += 1

            key = self.parse_number()

            self.skip_whitespace()
            self.consume("]")

            return key

        # clé simple : name = value
        return self.parse_identifier()

    def parse_table(self):
        self.consume("{")

        result = {}
        array_index = 1

        while True:
            self.skip_whitespace()

            if self.peek() == "}":
                self.pos += 1
                break

            if self.peek() is None:
                raise ValueError(
                    "Unexpected end of table"
                )

            # Détermine si on a une clé explicite
            if self.peek() == "[":
                key = self.parse_key()

                self.skip_whitespace()
                self.consume("=")

                value = self.parse_value()

                result[key] = value

            else:
                # Peut être :
                #
                # name = "Peter"
                #
                # ou :
                #
                # {
                #     ...
                # }
                #
                # sans clé explicite.

                save_position = self.pos

                try:
                    possible_key = self.parse_identifier()

                    self.skip_whitespace()

                    if self.peek() == "=":
                        self.pos += 1

                        value = self.parse_value()

                        result[possible_key] = value

                    else:
                        self.pos = save_position

                        value = self.parse_value()

                        result[array_index] = value
                        array_index += 1

                except ValueError:
                    self.pos = save_position

                    value = self.parse_value()

                    result[array_index] = value
                    array_index += 1

            self.skip_whitespace()

            if self.peek() == ",":
                self.pos += 1
                continue

            if self.peek() == "}":
                self.pos += 1
                break

            raise ValueError(
                f"Expected ',' or '}}' at position {self.pos}"
            )

        return result

def load_saved_variables(file_path):
    try:
        with open(
            file_path,
            "r",
            encoding="utf-8-sig"
        ) as file:
            content = file.read()

    except OSError as error:
        raise SavedVariablesError(
            f"Impossible de lire les SavedVariables : {error}"
        ) from error

    match = re.search(
        r"\bWoWCommunityCollectorDB\s*=",
        content
    )

    if not match:
        raise SavedVariablesError(
            "WoWCommunityCollectorDB introuvable."
        )

    parser = LuaParser(
        content[match.end():]
    )

    try:
        data = parser.parse_value()
    except (ValueError, IndexError) as error:
        raise SavedVariablesError(
            f"Impossible de parser les SavedVariables : {error}"
        ) from error

    if not isinstance(data, dict):
        raise SavedVariablesError(
            "WoWCommunityCollectorDB n'est pas une table Lua."
        )
    characters = data.get("characters")

    if not isinstance(characters, dict):
        raise SavedVariablesError(
            "La section 'characters' est absente ou invalide."
        )

    for character_key, character_data in characters.items():
        if not isinstance(character_data, dict):
            raise SavedVariablesError(
                f"Le personnage '{character_key}' est invalide."
            )

        required_fields = (
            "name",
            "realm",
            "level",
            "guid",
        )

    for field in required_fields:
        if field not in character_data:
            raise SavedVariablesError(
                f"Le personnage '{character_key}' "
                f"ne contient pas le champ '{field}'."
            )   
    if "version" not in data:
        raise SavedVariablesError(
            "Version des SavedVariables introuvable."
        )

    if "characters" not in data:
        raise SavedVariablesError(
            "Liste des personnages introuvable."
        )

    if not isinstance(data["characters"], dict):
        raise SavedVariablesError(
            "La liste des personnages doit être une table."
        )
    
    return data

def load_characters(file_path):
    data = load_saved_variables(file_path)

    characters = data["characters"]

    return characters