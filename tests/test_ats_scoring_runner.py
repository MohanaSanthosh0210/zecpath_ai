import unittest

from scoring.ats_scoring_runner import (
    build_candidate_result,
    calculate_education_score_for_resume,
    calculate_skill_score,
    normalize_skill_list,
)


class TestATSRunnner(unittest.TestCase):
    def test_normalize_skill_list_splits_and_lowercases(self):
        skills = ["Python, Django", {"name": "AWS"}, "machine learning"]
        normalized = normalize_skill_list(skills)

        self.assertIn("python", normalized)
        self.assertIn("django", normalized)
        self.assertIn("aws", normalized)
        self.assertIn("machine learning", normalized)

    def test_calculate_skill_score_returns_percent_match(self):
        resume_profile = {"skills": ["python", "docker", "aws"]}
        job_profile = {"required_skills": ["Python", "AWS", "Kubernetes"]}
        score = calculate_skill_score(resume_profile, job_profile)

        self.assertEqual(score, 66.67)

    def test_calculate_education_score_for_resume_matches_job_requirement(self):
        resume_profile = {
            "education_sections": [
                "Masters Degree in Computer Science, Some University",
                "Bachelor Degree in Information Technology, Other College",
            ]
        }
        job_profile = {"education": "M.Tech in Computer Science"}
        score = calculate_education_score_for_resume(resume_profile, job_profile)

        self.assertGreaterEqual(score, 80)

    def test_build_candidate_result_includes_final_score_and_breakdown(self):
        resume_profile = {
            "skills": ["python", "data analysis", "machine learning"],
            "experience": [{"description": "Worked on machine learning models using Python and data pipelines."}],
            "summary": "Experienced data scientist.",
            "projects": ["Forecasting model"],
            "education_sections": ["Master of Science in Data Science, University"],
        }
        job_profile = {
            "job_title": "Data Scientist",
            "job_description": "Build ML models and analyze large datasets.",
            "required_skills": ["Python", "Machine Learning", "SQL"],
            "projects": ["data science project"],
            "education": "MSc in Data Science",
        }

        result = build_candidate_result("resume1", "jd1", resume_profile, job_profile)

        self.assertEqual(result["candidate_id"], "resume1")
        self.assertEqual(result["job_id"], "jd1")
        self.assertIn("final_ats_score", result)
        self.assertEqual(result["breakdown"]["skills"], 66.67)
        self.assertGreaterEqual(result["breakdown"]["experience"], 0)
        self.assertGreaterEqual(result["breakdown"]["semantic"], 0)
        self.assertIn(result["status"], {"Shortlisted", "Rejected"})