import json
from pathlib import Path


class ExportFormatter:

    BASE_DIR = Path(__file__).resolve().parent

    OUTPUT_DIR = (
        BASE_DIR /
        "data" /
        "hiring_reports"
    )

    @staticmethod
    def export(report):

        ExportFormatter.OUTPUT_DIR.mkdir(

            parents=True,

            exist_ok=True

        )

        filepath = (

            ExportFormatter.OUTPUT_DIR /

            "candidate_hiring_report.json"

        )

        with open(

            filepath,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                report,

                file,

                indent=4,

                ensure_ascii=False

            )

        return filepath


if __name__ == "__main__":

    sample = {

        "candidate_id": "C001",

        "role": "Software Engineer",

        "overall_score": {

            "hiring_fit": 88

        },

        "final_decision": {

            "decision": "Selected"

        }

    }

    output = ExportFormatter.export(sample)

    print(

        f"Report exported to:\n{output}"

    )