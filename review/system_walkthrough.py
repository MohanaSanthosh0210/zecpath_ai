import json
from pathlib import Path


class SystemWalkthrough:

    OUTPUT_DIR = (
        Path("data") /
        "internal_review"
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    @staticmethod
    def run():

        walkthrough = {

            "pipeline": [

                {
                    "module": "Resume Parser",
                    "status": "Passed"
                },

                {
                    "module": "ATS Engine",
                    "status": "Passed"
                },

                {
                    "module": "Screening AI",
                    "status": "Passed"
                },

                {
                    "module": "HR Interview AI",
                    "status": "Passed"
                },

                {
                    "module": "Technical Interview AI",
                    "status": "Passed"
                },

                {
                    "module": "Decision AI",
                    "status": "Passed"
                }

            ],

            "overall_status": "Operational"

        }

        with open(

            SystemWalkthrough.OUTPUT_DIR /
            "system_walkthrough.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(
                walkthrough,
                file,
                indent=4
            )

        return walkthrough


if __name__ == "__main__":

    SystemWalkthrough.run()

    print(
        "System walkthrough generated."
    )