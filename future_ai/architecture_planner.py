import json
from pathlib import Path


class ArchitecturePlanner:

    BASE_DIR = Path(__file__).resolve().parent

    OUTPUT_DIR = (
        BASE_DIR /
        "data" /
        "roadmap"
    )

    @staticmethod
    def generate():

        ArchitecturePlanner.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        architecture = {

            "current_pipeline": [

                "Resume Upload",

                "ATS Analysis",

                "Screening AI",

                "HR Interview",

                "Technical Interview",

                "Behavior Analysis",

                "Integrity Detection",

                "Machine Test",

                "Hiring Recommendation"

            ],

            "future_modules": [

                "AI Coaching",

                "AI Video Analysis",

                "Emotion Detection",

                "Real-Time Feedback",

                "Interview Analytics Dashboard"

            ],

            "deployment_strategy":

                "Microservice Architecture"

        }

        filepath = (
            ArchitecturePlanner.OUTPUT_DIR /
            "future_architecture.json"
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                architecture,
                file,
                indent=4,
                ensure_ascii=False
            )

        return architecture


if __name__ == "__main__":

    print(
        json.dumps(
            ArchitecturePlanner.generate(),
            indent=4
        )
    )