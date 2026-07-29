import json

from hiring_report.report_generator import (
    HiringReportGenerator
)


def main():

    sample_candidate = {

        "candidate_id": "C001",

        "role": "Software Engineer",

        "ats_summary": {
            "score": 88,
            "summary": "Strong resume match."
        },

        "screening_summary": {
            "score": 84,
            "summary": "Good communication."
        },

        "hr_summary": {
            "score": 82,
            "summary": "Positive HR interview."
        },

        "technical_summary": {
            "score": 91,
            "summary": "Excellent technical depth."
        },

        "behavior_summary": {
            "score": 86,
            "summary": "Highly engaged."
        },

        "integrity_summary": {
            "score": 94,
            "summary": "No integrity concerns."
        },

        "overall_score": {

            "hiring_fit": 89

        },

        "final_decision": {

            "decision": "Selected"

        }

    }

    report = HiringReportGenerator.generate(

        sample_candidate

    )

    print(

        "\n========== Hiring Intelligence Report ==========\n"

    )

    print(

        json.dumps(

            report,

            indent=4

        )

    )


if __name__ == "__main__":

    main()