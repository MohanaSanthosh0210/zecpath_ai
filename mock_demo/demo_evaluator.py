import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "data" / "mock_demo"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class DemoEvaluator:

    @staticmethod
    def generate():

        improvements = {

            "changes": [

                "Added deployment architecture slide.",

                "Improved demo timing.",

                "Included API integration diagram.",

                "Added recruiter dashboard screenshots.",

                "Improved readability of hiring report."

            ]

        }

        with open(

            OUTPUT_DIR / "presentation_improvements.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(improvements, file, indent=4)

        return improvements