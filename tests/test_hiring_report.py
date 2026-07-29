from hiring_report.report_generator import (
    HiringReportGenerator
)


def test_report_generation():

    sample = {

        "candidate_id": "TEST001",

        "role": "Software Engineer",

        "overall_score": {

            "hiring_fit": 85

        },

        "final_decision": {

            "decision": "Selected"

        }

    }

    report = HiringReportGenerator.generate(

        sample

    )

    assert report["candidate_id"] == "TEST001"

    assert report["final_decision"]["decision"] == "Selected"

    print(

        "\nHiring Report Test Passed."

    )


if __name__ == "__main__":

    test_report_generation()