from hr_scoring.report_generator import (
    ReportGenerator
)


def test_hr_scoring():

    report = ReportGenerator.generate()

    assert isinstance(report, dict)

    assert "final_hr_score" in report

    assert "recommendation" in report

    assert (

        0 <=

        report["final_hr_score"]

        <= 100

    )

    print(

        "\nHR Scoring Test Passed."

    )

    print(

        report

    )


if __name__ == "__main__":

    test_hr_scoring()