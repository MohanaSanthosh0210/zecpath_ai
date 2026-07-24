import json
from pathlib import Path


class RiskEngine:

    BASE_DIR = Path(__file__).resolve().parent

    RISK_FILE = (
        BASE_DIR /
        "config" /
        "risk_levels.json"
    )

    @staticmethod
    def load_levels():

        with open(
            RiskEngine.RISK_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @staticmethod
    def determine_level(score):

        levels = RiskEngine.load_levels()

        for level in levels["risk_levels"]:

            minimum, maximum = level["score_range"]

            if minimum <= score <= maximum:

                return level["level"]

        return "Unknown"


if __name__ == "__main__":

    print(

        RiskEngine.determine_level(64)

    )
    