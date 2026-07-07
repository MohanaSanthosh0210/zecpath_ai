import json

from hr_scoring.report_generator import (
    ReportGenerator
)


def main():

    report = ReportGenerator.generate()

    print(
        "\n======================================="
    )

    print(
        "      HR INTERVIEW REPORT"
    )

    print(
        "=======================================\n"
    )

    print(

        json.dumps(

            report,

            indent=4

        )

    )

    print(

        "\nHR Interview Evaluation Completed."

    )

    print(

        "Output saved to:\n"

        "data/hr_scoring/hr_score_report.json"

    )


if __name__ == "__main__":

    main()