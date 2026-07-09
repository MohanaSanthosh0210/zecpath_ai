from reporting.interview_summary_generator import InterviewSummaryGenerator
from reporting.report_utils import load_json


def test_interview_summary_generation():
    answer_data = load_json("data/understood_answers/sample_answer.json")
    communication_data = load_json("data/communication/communication_score.json")
    behavior_data = load_json("data/behavioral_analysis/behavioral_report.json")
    hr_score_data = load_json("data/hr_scoring/hr_score_report.json")

    generator = InterviewSummaryGenerator()
    report = generator.generate_report(
        answer_data=answer_data,
        communication_data=communication_data,
        behavior_data=behavior_data,
        hr_score_data=hr_score_data,
    )

    assert isinstance(report, dict)
    assert "candidate_strengths" in report
    assert "candidate_weaknesses" in report
    assert "cultural_fit_indicators" in report
    assert "risk_flags" in report
    assert "inconsistencies" in report
    assert "overall_hr_performance" in report
    assert "natural_language_report" in report

    performance = report["overall_hr_performance"]
    assert performance["score"] >= 0
    assert performance["recommendation"] in {"Strong Hire", "Hire", "Review", "Reject"}
    assert report["natural_language_report"]

    print("Interview Summary Test Passed.")
    print(report["natural_language_report"])
