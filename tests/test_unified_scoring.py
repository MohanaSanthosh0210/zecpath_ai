from scoring.unified_scoring_engine import calculate_unified_score


def test_unified_scoring_aggregates_rounds_with_role_weights():
    result = calculate_unified_score(
        role="python developer",
        ats_score=85,
        screening_score=78,
        hr_score=82,
        candidate_id="C100",
        job_id="J100",
    )

    assert result["round_scores"]["ats"] == 85
    assert result["round_scores"]["screening"] == 78
    assert result["round_scores"]["hr_interview"] == 82
    assert result["weights"]["ats"] > 0
    assert result["weights"]["screening"] > 0
    assert result["weights"]["hr_interview"] > 0
    assert 0 <= result["hiring_fit_percentage"] <= 100
    assert result["status"] in {"Strong Fit", "Good Fit", "Needs Review", "Not Fit"}
    assert result["candidate_id"] == "C100"
    assert result["job_id"] == "J100"
