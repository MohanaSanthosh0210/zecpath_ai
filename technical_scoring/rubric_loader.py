import json
from pathlib import Path


class RubricLoader:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG_FILE = (
        BASE_DIR /
        "config" /
        "technical_scoring_weights.json"
    )

    @staticmethod
    def load_weights():

        with open(
            RubricLoader.CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


if __name__ == "__main__":

    print(

        RubricLoader.load_weights()

    )