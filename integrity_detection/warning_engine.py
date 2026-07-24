import json
from pathlib import Path


class WarningEngine:

    BASE_DIR = Path(__file__).resolve().parent

    WARNING_FILE = (
        BASE_DIR /
        "config" /
        "warning_rules.json"
    )

    @staticmethod
    def load_rules():

        with open(
            WarningEngine.WARNING_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @staticmethod
    def get_actions():

        rules = WarningEngine.load_rules()

        return {

            item["condition"]: item["action"]

            for item in rules["warning_rules"]

        }


if __name__ == "__main__":

    print(

        WarningEngine.get_actions()

    )