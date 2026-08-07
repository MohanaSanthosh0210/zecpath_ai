import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "data" / "mock_demo"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class FeedbackCollector:

    @staticmethod
    def generate():

        report = {

            "presentation_quality": 9,

            "system_explanation": 9,

            "architecture_clarity": 9,

            "demo_flow": 9,

            "overall_rating": 9.0,

            "feedback": [

                "ATS explanation is clear.",

                "Architecture diagrams are easy to follow.",

                "Include additional recruiter dashboard screenshots.",

                "Reduce explanation time for governance slide."

            ]

        }

        with open(

            OUTPUT_DIR / "feedback_report.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(report, file, indent=4)

        return report