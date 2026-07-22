import json
from pathlib import Path


class ExperienceEngine:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG_FILE = (
        BASE_DIR /
        "config" /
        "experience_levels.json"
    )

    @staticmethod
    def load_levels():

        with open(
            ExperienceEngine.CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data["experience_levels"]

    @staticmethod
    def determine_level(years):

        years = float(years)

        levels = ExperienceEngine.load_levels()

        for level in levels:

            lower, upper = level["years"].split("-")

            lower = int(lower)

            if "+" in upper:

                upper = 999

            else:

                upper = int(upper)

            if lower <= years <= upper:

                return level

        return levels[-1]


if __name__ == "__main__":

    print(

        ExperienceEngine.determine_level(4)

    )
    