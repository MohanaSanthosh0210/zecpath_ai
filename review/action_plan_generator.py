import json
from pathlib import Path


class ActionPlanGenerator:

    OUTPUT_DIR = (
        Path("data") /
        "internal_review"
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    @staticmethod
    def generate():

        action_plan = {

            "phase_1": [

                "Improve ATS synonym matching",

                "Refine screening intent thresholds"

            ],

            "phase_2": [

                "Optimize HR follow-up logic",

                "Improve technical interview scoring consistency"

            ],

            "phase_3": [

                "Performance optimization",

                "Reporting enhancements",

                "Recruiter dashboard improvements"

            ]

        }

        with open(

            ActionPlanGenerator.OUTPUT_DIR /
            "action_plan.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(
                action_plan,
                file,
                indent=4
            )

        return action_plan


if __name__ == "__main__":

    ActionPlanGenerator.generate()

    print(
        "Action plan generated."
    )