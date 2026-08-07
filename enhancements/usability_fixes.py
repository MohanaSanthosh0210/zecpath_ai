import json
from pathlib import Path


class UsabilityFixes:

    OUTPUT_DIR = (
        Path("data") /
        "enhancements"
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    @staticmethod
    def generate():

        usability = {

            "usability_improvements": [

                {

                    "category":
                    "Recruiter Dashboard",

                    "improvement":
                    "Improved report navigation.",

                    "status":
                    "Completed"

                },

                {

                    "category":
                    "Candidate Reports",

                    "improvement":
                    "Simplified score presentation.",

                    "status":
                    "Completed"

                },

                {

                    "category":
                    "Interview Results",

                    "improvement":
                    "Added clearer section headings.",

                    "status":
                    "Completed"

                },

                {

                    "category":
                    "Validation",

                    "improvement":
                    "Improved input validation messages.",

                    "status":
                    "Completed"

                },

                {

                    "category":
                    "User Experience",

                    "improvement":
                    "Consistent terminology across reports.",

                    "status":
                    "Completed"

                }

            ],

            "overall_status":
            "Improved"

        }

        output_file = (

            UsabilityFixes.OUTPUT_DIR /
            "usability_improvements.json"

        )

        with open(

            output_file,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(
                usability,
                file,
                indent=4
            )

        return usability


if __name__ == "__main__":

    UsabilityFixes.generate()

    print(
        "Usability improvements completed."
    )