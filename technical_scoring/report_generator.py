import json
from pathlib import Path

from technical_scoring.technical_scoring_engine import (
    TechnicalScoringEngine
)


class TechnicalReportGenerator:

    BASE_DIR = Path(__file__).resolve().parent

    OUTPUT_DIR = (

        BASE_DIR /

        "data" /

        "technical_reports"

    )

    @staticmethod
    def generate(answer_data):

        result = (

            TechnicalScoringEngine.evaluate(

                answer_data

            )

        )

        report = {

            "candidate_id": answer_data.get(

                "candidate_id",

                "UNKNOWN"

            ),

            "question_id": answer_data.get(

                "question_id",

                "UNKNOWN"

            ),

            "difficulty": answer_data.get(

                "difficulty",

                "easy"

            ),

            "skill_breakdown": result[

                "skill_breakdown"

            ],

            "weighted_score": result[

                "weighted_score"

            ],

            "normalized_score": result[

                "normalized_score"

            ]

        }

        TechnicalReportGenerator.OUTPUT_DIR.mkdir(

            parents=True,

            exist_ok=True

        )

        filepath = (

            TechnicalReportGenerator.OUTPUT_DIR /

            "technical_report.json"

        )

        with open(

            filepath,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                report,

                file,

                indent=4,

                ensure_ascii=False

            )

        print(

            json.dumps(

                report,

                indent=4,

                ensure_ascii=False

            )

        )

        print(

            f"\nReport saved to:\n{filepath}"

        )

        return report


if __name__ == "__main__":

    sample = {

        "candidate_id": "C001",

        "question_id": "PY101",

        "difficulty": "hard",

        "accuracy_score": 90,

        "depth_score": 82,

        "reasoning_score": 88,

        "applicability_score": 80

    }

    TechnicalReportGenerator.generate(

        sample

    )