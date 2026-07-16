from final_system.demo_runner import build_unified_candidate_report


def test_build_unified_candidate_report_includes_hiring_score():
    data = {
        "understood_answer": {
            "intent": "python developer",
            "skills": ["python", "fastapi"],
            "experience": "3 years"
        },
        "screening_score": {
            "final_screening_score": 78,
            "status": "Reviewed"
        },
        "behavior_report": {
            "communication_strength": "Strong",
            "confidence": "High",
            "sentiment": "Positive"
        },
        "screening_report": {},
        "conversation": {},
        "edge_case": {},
        "hr_score": {
            "final_hr_score": 82
        },
    }

    report = build_unified_candidate_report(
        data,
        role="python developer",
        candidate_id="C101",
        job_id="J101",
    )

    unified = report["unified_candidate_score"]

    assert unified["candidate_id"] == "C101"
    assert unified["job_id"] == "J101"
    assert unified["round_scores"]["ats"] == 0
    assert unified["round_scores"]["screening"] == 78
    assert unified["round_scores"]["hr_interview"] == 82
    assert 0 <= unified["hiring_fit_percentage"] <= 100
    assert unified["status"] in {"Strong Fit", "Good Fit", "Needs Review", "Not Fit"}
