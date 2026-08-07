import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "data" / "mock_demo"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class ReadinessChecker:

    @staticmethod
    def generate():

        readiness = {

            "presentation_complete": True,

            "demo_script_ready": True,

            "diagrams_complete": True,

            "qa_prepared": True,

            "estimated_demo_time": "12 minutes",

            "readiness_status": "Ready for Final Presentation"

        }

        with open(

            OUTPUT_DIR / "demo_readiness.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(readiness, file, indent=4)

        return readiness