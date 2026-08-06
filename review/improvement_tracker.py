import json
from pathlib import Path


class ImprovementTracker:

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

        improvements = {

            "improvements": [

                {

                    "module":
                    "ATS Engine",

                    "issue":
                    "Skill matching misses synonyms",

                    "priority":
                    "High"

                },

                {

                    "module":
                    "Screening AI",

                    "issue":
                    "Intent confidence threshold needs refinement",

                    "priority":
                    "Medium"

                },

                {

                    "module":
                    "HR Interview AI",

                    "issue":
                    "Follow-up questions occasionally repeat",

                    "priority":
                    "Medium"

                },

                {

                    "module":
                    "Technical Interview AI",

                    "issue":
                    "Difficulty progression can be improved",

                    "priority":
                    "Low"

                },

                {

                    "module":
                    "Decision AI",

                    "issue":
                    "Confidence explanation can be clearer",

                    "priority":
                    "Low"

                }

            ]

        }

        with open(

            ImprovementTracker.OUTPUT_DIR /
            "improvement_list.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(
                improvements,
                file,
                indent=4
            )

        return improvements


if __name__ == "__main__":

    ImprovementTracker.generate()

    print(
        "Improvement list generated."
    )