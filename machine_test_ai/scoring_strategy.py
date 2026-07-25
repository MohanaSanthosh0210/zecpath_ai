import json
from pathlib import Path


class ScoringStrategy:

    BASE_DIR = Path(__file__).resolve().parent

    WEIGHT_FILE = (
        BASE_DIR /
        "config" /
        "evaluation_weights.json"
    )

    @staticmethod
    def load_weights():

        with open(
            ScoringStrategy.WEIGHT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @staticmethod
    def get_weights():

        return ScoringStrategy.load_weights()


if __name__ == "__main__":

    print(

        ScoringStrategy.get_weights()

    )