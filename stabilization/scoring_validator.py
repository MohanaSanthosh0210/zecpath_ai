import json
from pathlib import Path


class ScoringValidator:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG = (

        BASE_DIR /

        "config" /

        "scoring_limits.json"

    )

    @staticmethod
    def load_limits():

        with open(

            ScoringValidator.CONFIG,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(file)

    @staticmethod
    def validate(score):

        limits = (

            ScoringValidator.load_limits()

        )

        minimum = limits["minimum_score"]

        maximum = limits["maximum_score"]

        return {

            "score":

                score,

            "valid":

                minimum <= score <= maximum

        }

    @staticmethod
    def validate_scores(score_dict):

        report = {}

        for key, value in score_dict.items():

            report[key] = (

                ScoringValidator.validate(

                    value

                )

            )

        return report


if __name__ == "__main__":

    scores = {

        "ats": 87,

        "screening": 82,

        "hr": 90,

        "technical": 85,

        "behavior": 95,

        "integrity": 91,

        "machine_test": 89

    }

    print(

        ScoringValidator.validate_scores(

            scores

        )

    )