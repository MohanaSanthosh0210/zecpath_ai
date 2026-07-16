from scoring.ats_scoring_runner import build_candidate_result


def test_build_candidate_result_includes_unified_candidate_score():
    resume_profile = {
        "skills": ["python"],
        "experience": [{"description": "worked on python applications"}],
        "summary": "python developer",
        "projects": [],
        "education_sections": [],
    }
    job_profile = {
        "job_title": "python developer",
        "job_description": "python developer",
        "required_skills": ["python"],
        "projects": [],
        "education": "bachelor",
    }

    result = build_candidate_result("C200", "J200", resume_profile, job_profile)

    assert "unified_candidate_score" in result
    assert result["unified_candidate_score"]["candidate_id"] == "C200"
    assert result["unified_candidate_score"]["job_id"] == "J200"
    assert result["unified_candidate_score"]["round_scores"]["ats"] == result["final_ats_score"]
