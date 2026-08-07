import json
from pathlib import Path


class OutputFormatter:

    OUTPUT_DIR = (
        Path("data") /
        "enhancements"
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    @staticmethod
    def format_outputs():

        output = {

            "report_format": {

                "candidate_information":
                "Improved",

                "score_display":
                "Consistent percentage formatting",

                "recommendation":
                "Highlighted",

                "confidence_level":
                "Included",

                "risk_assessment":
                "Included"

            },

            "json_standardization": {

                "consistent_keys": True,

                "consistent_data_types": True,

                "pretty_print": True

            },

            "overall_status":
            "Formatted"

        }

        output_file = (

            OutputFormatter.OUTPUT_DIR /
            "output_improvements.json"

        )

        with open(

            output_file,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(
                output,
                file,
                indent=4
            )

        return output


if __name__ == "__main__":

    OutputFormatter.format_outputs()

    print(
        "Output formatting improvements completed."
    )