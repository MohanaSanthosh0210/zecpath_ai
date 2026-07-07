import json
import os

from hr_scoring.hr_scoring_engine import (
    HRInterviewScoringEngine
)


class ReportGenerator:

    OUTPUT_FOLDER = "data/hr_scoring"

    OUTPUT_FILE = (
        "data/hr_scoring/hr_score_report.json"
    )

    @staticmethod
    def recommendation(score):

        if score >= 85:
            return "Strong Hire"

        elif score >= 70:
            return "Hire"

        elif score >= 60:
            return "Review"

        return "Reject"

    @classmethod
    def generate(cls):

        engine = HRInterviewScoringEngine()

        report = engine.process()

        report["final_hr_score"] = report[
            "normalized_score"
        ]

        report["recommendation"] = (

            cls.recommendation(

                report["final_hr_score"]

            )

        )

        os.makedirs(

            cls.OUTPUT_FOLDER,

            exist_ok=True

        )

        with open(

            cls.OUTPUT_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                report,

                file,

                indent=4

            )

        return report


if __name__ == "__main__":

    report = ReportGenerator.generate()

    print(

        json.dumps(

            report,

            indent=4

        )

    )