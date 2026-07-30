import json
from pathlib import Path


class ConsistencyOptimizer:

    @staticmethod
    def calculate(candidate):

        scores = [

            candidate.get("ats_score", 0),

            candidate.get("screening_score", 0),

            candidate.get("hr_score", 0),

            candidate.get("technical_score", 0)

        ]

        difference = max(scores) - min(scores)

        consistency = max(

            0,

            100 - difference

        )

        return {

            "score_difference": difference,

            "consistency_score": consistency

        }

    @staticmethod
    def save(result, output_dir):

        output_dir.mkdir(

            parents=True,

            exist_ok=True

        )

        filepath = (

            output_dir /

            "consistency_report.json"

        )

        with open(

            filepath,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                result,

                file,

                indent=4,

                ensure_ascii=False

            )

        return filepath


if __name__ == "__main__":

    sample = {

        "ats_score": 88,

        "screening_score": 85,

        "hr_score": 82,

        "technical_score": 91

    }

    print(

        ConsistencyOptimizer.calculate(

            sample

        )

    )