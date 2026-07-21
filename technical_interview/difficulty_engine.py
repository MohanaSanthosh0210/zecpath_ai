import json
from pathlib import Path


class DifficultyEngine:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG_FILE = (
        BASE_DIR /
        "config" /
        "difficulty_progression.json"
    )

    @staticmethod
    def load_progression():

        with open(
            DifficultyEngine.CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @staticmethod
    def get_progression(level):

        data = DifficultyEngine.load_progression()

        return data["difficulty_progression"].get(level)


if __name__ == "__main__":

    print(

        DifficultyEngine.get_progression(
            "intermediate"
        )

    )