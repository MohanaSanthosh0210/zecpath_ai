import json
from pathlib import Path


class ErrorHandler:

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

        errors = {

            "error_handling": [

                {

                    "error_code":
                    "ATS_001",

                    "module":
                    "ATS Engine",

                    "message":
                    "Job description missing.",

                    "severity":
                    "High",

                    "resolution":
                    "Upload a valid job description."

                },

                {

                    "error_code":
                    "SCR_001",

                    "module":
                    "Screening AI",

                    "message":
                    "Candidate response unavailable.",

                    "severity":
                    "Medium",

                    "resolution":
                    "Retry screening process."

                },

                {

                    "error_code":
                    "HR_001",

                    "module":
                    "HR Interview AI",

                    "message":
                    "Conversation interrupted.",

                    "severity":
                    "Medium",

                    "resolution":
                    "Resume interview session."

                },

                {

                    "error_code":
                    "TECH_001",

                    "module":
                    "Technical Interview AI",

                    "message":
                    "Question generation failed.",

                    "severity":
                    "Low",

                    "resolution":
                    "Generate a new technical question."

                },

                {

                    "error_code":
                    "DEC_001",

                    "module":
                    "Decision AI",

                    "message":
                    "Insufficient evaluation data.",

                    "severity":
                    "High",

                    "resolution":
                    "Complete all interview stages."

                }

            ],

            "overall_status":
            "Standardized"

        }

        output_file = (

            ErrorHandler.OUTPUT_DIR /
            "error_handling.json"

        )

        with open(

            output_file,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(
                errors,
                file,
                indent=4
            )

        return errors


if __name__ == "__main__":

    ErrorHandler.generate()

    print(
        "Error handling definitions generated."
    )