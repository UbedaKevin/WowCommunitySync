class Character:
    def __init__(self, character_key, data):
        self.key = character_key

        # Identity
        self.name = data.get("name")
        self.realm = data.get("realm")

        # Character
        self.level = data.get("level")

        self.class_name = data.get("class")
        self.class_file = data.get("classFile")

        self.race = data.get("race")
        self.race_file = data.get("raceFile")
        self.race_id = data.get("raceID")

        self.faction = data.get("faction")

        # Guild
        self.guild = data.get("guild")

        self.guid = data.get("guid")

        # Professions
        self.professions = data.get(
            "professions",
            {}
        )

        # Equipment
        self.equipment = data.get(
            "equipment",
            {}

        )

    def to_dict(self):
        return {
            "key": self.key,

            "name": self.name,
            "realm": self.realm,

            "level": self.level,

            "class": self.class_name,
            "classFile": self.class_file,

            "race": self.race,
            "raceFile": self.race_file,
            "raceID": self.race_id,

            "faction": self.faction,

            "guild": self.guild,

            "guid": self.guid,

            "professions": self.professions,
            "equipment": self.equipment,
        }

    def __repr__(self):
        return (
            f"Character("
            f"key={self.key!r}, "
            f"name={self.name!r}, "
            f"realm={self.realm!r}, "
            f"level={self.level!r}, "
            f"class={self.class_name!r}"
            f")"
        )