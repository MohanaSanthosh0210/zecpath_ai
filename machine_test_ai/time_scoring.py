import json
from pathlib import Path


class TimeScoring:

    BASE_DIR = Path(__file__).resolve().parent

    TIME_FILE = (
        BASE_DIR /
        "config" /
        "time_limits.json"
    )

    @staticmethod
    def load_time_limits():

        with open(
            TimeScoring.TIME_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @staticmethod
    def get_limit(level):

        limits = TimeScoring.load_time_limits()

        return limits.get(level, {})


if __name__ == "__main__":

    print(

        TimeScoring.get_limit("medium")

    )