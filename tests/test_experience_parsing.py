import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.experience_parser import ExperienceParser, RoleSimilarity
from scoring.experience_relevance import ExperienceRelevanceScorer


def test_experience_parser_extracts_company_title_and_duration():
    resume_text = """
Professional Experience:
- Senior Software Engineer @ Acme Corp | Jan 2019 - Dec 2021
  Led a cloud modernization effort with Python, Kubernetes, and AWS.
- Software Developer at Bolt Inc | Jun 2017 - Dec 2018
  Built backend APIs, improved database performance, and supported CI/CD pipelines.
"""

    parser = ExperienceParser()
    result = parser.extract_experience(resume_text)

    assert len(result["experience_items"]) == 2
    assert result["total_experience_months"] == 55
    assert result["gaps"] == []
    assert result["overlaps"] == []

    first = result["experience_items"][0]
    assert first["company"] == "Acme Corp"
    assert "Senior Software Engineer" in first["designation"]
    assert first["duration_months"] == 36


def test_experience_relevance_scoring_produces_reasonable_values():
    resume_text = """
Professional Experience:
- Senior Software Engineer @ Acme Corp | Jan 2019 - Dec 2021
  Led a cloud modernization effort with Python, Kubernetes, and AWS.
"""

    parser = ExperienceParser()
    result = parser.extract_experience(resume_text)
    experience_items = result["experience_items"]

    scorer = ExperienceRelevanceScorer()
    job_title = "Senior Software Engineer"
    job_description = "We need a senior engineer with strong Python, Kubernetes, and AWS experience."
    required_skills = ["Python", "Kubernetes", "AWS"]

    role_score = scorer.score_role_relevance(experience_items[0], job_title, job_description, required_skills)
    assert role_score["overall_relevance"] >= 0.7
    assert role_score["skill_overlap"] == 1.0

    profile_score = scorer.score_experience_profile(experience_items, job_title, job_description, required_skills)
    assert profile_score["overall_relevance"] == role_score["overall_relevance"]
    assert profile_score["relevant_experience_years"] == round((36 * role_score["overall_relevance"]) / 12.0, 2)


def test_role_similarity_identifies_similar_titles():
    role_a = {
        "designation": "Senior Software Engineer",
        "company": "Acme Corp",
        "responsibilities": ["Designed and delivered Kubernetes-native microservices."],
    }
    role_b = {
        "designation": "Software Engineering Lead",
        "company": "Acme Corporation",
        "responsibilities": ["Built and operated APIs on AWS and Kubernetes."],
    }

    score = RoleSimilarity.compare_roles(role_a, role_b)
    assert score > 0.5
