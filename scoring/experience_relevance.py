from difflib import SequenceMatcher
from typing import Dict, List, Optional

from parsers.experience_parser import RoleSimilarity


class ExperienceRelevanceScorer:
    """Score experience entries against job requirements."""

    def __init__(self, skill_match_weight: float = 0.25, title_weight: float = 0.55, responsibility_weight: float = 0.20):
        self.skill_match_weight = skill_match_weight
        self.title_weight = title_weight
        self.responsibility_weight = responsibility_weight

    def score_role_relevance(
        self,
        role: Dict,
        job_title: str = "",
        job_description: str = "",
        required_skills: Optional[List[str]] = None,
    ) -> Dict:
        required_skills = required_skills or []
        role_title = role.get("designation", "")
        responsibilities = " ".join(role.get("responsibilities", [])).strip() or role.get("raw_text", "")

        title_similarity = self._text_similarity(role_title, job_title)
        responsibility_similarity = self._text_similarity(responsibilities, job_description)
        skill_overlap = self._calculate_skill_overlap(responsibilities, required_skills)

        score = (
            self.title_weight * title_similarity
            + self.responsibility_weight * responsibility_similarity
            + self.skill_match_weight * skill_overlap
        )

        return {
            "role_title": role_title,
            "title_similarity": round(title_similarity, 3),
            "responsibility_similarity": round(responsibility_similarity, 3),
            "skill_overlap": round(skill_overlap, 3),
            "overall_relevance": round(min(max(score, 0.0), 1.0), 3),
        }

    def score_experience_profile(
        self,
        experience_items: List[Dict],
        job_title: str = "",
        job_description: str = "",
        required_skills: Optional[List[str]] = None,
    ) -> Dict:
        required_skills = required_skills or []
        scored_roles = []
        weighted_sum = 0.0
        total_months = 0

        for item in experience_items:
            score = self.score_role_relevance(item, job_title, job_description, required_skills)
            months = item.get("duration_months") or 0
            weighted_sum += score["overall_relevance"] * months
            total_months += months
            scored_roles.append({**item, **score})

        overall_relevance = round(weighted_sum / total_months, 3) if total_months else 0.0
        relevant_experience_years = round((weighted_sum / 12.0), 2)

        return {
            "role_scores": scored_roles,
            "overall_relevance": overall_relevance,
            "relevant_experience_years": relevant_experience_years,
            "required_skills": required_skills,
            "job_title": job_title,
        }

    def compare_roles(self, role_a: Dict, role_b: Dict) -> float:
        return RoleSimilarity.compare_roles(role_a, role_b)

    def _text_similarity(self, text_a: str, text_b: str) -> float:
        if not text_a or not text_b:
            return 0.0

        normalized_a = " ".join(text_a.lower().split())
        normalized_b = " ".join(text_b.lower().split())
        if not normalized_a or not normalized_b:
            return 0.0

        return SequenceMatcher(None, normalized_a, normalized_b).ratio()

    def _calculate_skill_overlap(self, responsibilities: str, required_skills: List[str]) -> float:
        if not required_skills:
            return 0.0

        responsibilities_lower = responsibilities.lower()
        matched = 0
        for skill in required_skills:
            if skill and skill.lower() in responsibilities_lower:
                matched += 1

        return matched / len(required_skills)
