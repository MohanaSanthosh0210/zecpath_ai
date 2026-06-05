import re
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, Union

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize


def _normalize_text(text: Optional[str]) -> str:
    if not text:
        return ""
    cleaned = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    return " ".join(cleaned.split())


def _extract_text_from_items(items: Optional[Union[Sequence[Any], Dict[str, Any], str]]) -> str:
    if not items:
        return ""

    if isinstance(items, str):
        return _normalize_text(items)

    if isinstance(items, dict):
        return _normalize_text(" ".join(str(value) for value in items.values() if isinstance(value, str)))

    text_parts: List[str] = []
    for item in items:
        if isinstance(item, str):
            text_parts.append(item)
        elif isinstance(item, dict):
            if "name" in item and isinstance(item["name"], str):
                text_parts.append(item["name"])
            elif "description" in item and isinstance(item["description"], str):
                text_parts.append(item["description"])
            else:
                text_parts.append(" ".join(str(value) for value in item.values() if isinstance(value, str)))
        else:
            text_parts.append(str(item))

    return _normalize_text(" ".join(text_parts))


def _embed_texts(texts: Sequence[str]) -> Any:
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_df=1.0, min_df=1)
    matrix = vectorizer.fit_transform(texts)
    return normalize(matrix, norm="l2", axis=1)


def _cosine_similarity(text_a: str, text_b: str) -> float:
    if not text_a or not text_b:
        return 0.0

    matrix = _embed_texts([text_a, text_b])
    similarity = cosine_similarity(matrix[0], matrix[1])[0, 0]
    return float(similarity)


def _skill_overlap_ratio(skills_a: Sequence[Any], skills_b: Sequence[Any]) -> float:
    if not skills_a or not skills_b:
        return 0.0

    normalize_skill = lambda value: _normalize_text(value if isinstance(value, str) else str(value))
    set_a = {normalize_skill(item.get("name") if isinstance(item, dict) else item) for item in skills_a}
    set_b = {normalize_skill(item.get("name") if isinstance(item, dict) else item) for item in skills_b}
    set_a.discard("")
    set_b.discard("")

    if not set_b:
        return 0.0

    matched = len(set_a.intersection(set_b))
    return float(matched) / float(len(set_b))


def _text_overlap_ratio(text_a: str, text_b: str) -> float:
    normalized_a = _normalize_text(text_a)
    normalized_b = _normalize_text(text_b)
    if not normalized_a or not normalized_b:
        return 0.0

    words_a = {word for word in normalized_a.split() if len(word) > 2}
    words_b = {word for word in normalized_b.split() if len(word) > 2}
    if not words_b:
        return 0.0

    matched = len(words_a.intersection(words_b))
    return float(matched) / float(len(words_b))


class SemanticMatchingEngine:
    """Semantic resume-to-job matching engine using TF-IDF vector similarity."""

    def __init__(
        self,
        skills_weight: float = 0.40,
        experience_weight: float = 0.45,
        project_weight: float = 0.15,
        thresholds: Optional[Dict[str, float]] = None,
    ):
        self.skills_weight = skills_weight
        self.experience_weight = experience_weight
        self.project_weight = project_weight
        self.thresholds = thresholds or {
            "skills": 0.55,
            "experience": 0.20,
            "projects": 0.02,
            "overall": 0.45,
        }

    def score_pair(self, resume_profile: Dict[str, Any], job_profile: Dict[str, Any]) -> Dict[str, Any]:
        resume_skills = resume_profile.get("skills", [])
        job_skills = job_profile.get("required_skills", [])
        skills_similarity = self._score_skills(resume_skills, job_skills)

        experience_similarity = self._score_experience(resume_profile, job_profile)

        resume_project_text = self._build_project_text(resume_profile)
        job_project_text = self._build_project_text(job_profile)
        project_similarity = _cosine_similarity(resume_project_text, job_project_text) if resume_project_text or job_project_text else 0.0

        overall_similarity = (
            self.skills_weight * skills_similarity
            + self.experience_weight * experience_similarity
            + self.project_weight * project_similarity
        )

        return {
            "skills_similarity": round(skills_similarity, 3),
            "experience_similarity": round(experience_similarity, 3),
            "project_similarity": round(project_similarity, 3),
            "overall_similarity": round(min(max(overall_similarity, 0.0), 1.0), 3),
            "match": self.is_match(
                {
                    "skills": skills_similarity,
                    "experience": experience_similarity,
                    "projects": project_similarity,
                    "overall": overall_similarity,
                }
            ),
        }

    def is_match(self, score: Dict[str, float]) -> bool:
        return (
            score.get("skills", 0.0) >= self.thresholds.get("skills", 0.0)
            and score.get("experience", 0.0) >= self.thresholds.get("experience", 0.0)
            and score.get("projects", 0.0) >= self.thresholds.get("projects", 0.0)
            and score.get("overall", 0.0) >= self.thresholds.get("overall", 0.0)
        )

    def tune_thresholds(self, labeled_pairs: List[Tuple[Dict[str, Any], Dict[str, Any], bool]]) -> Dict[str, float]:
        if not labeled_pairs:
            return self.thresholds.copy()

        positive_scores: List[float] = []
        negative_scores: List[float] = []

        for resume_profile, job_profile, is_relevant in labeled_pairs:
            score = self.score_pair(resume_profile, job_profile)
            if is_relevant:
                positive_scores.append(score["overall_similarity"])
            else:
                negative_scores.append(score["overall_similarity"])

        if not positive_scores or not negative_scores:
            return self.thresholds.copy()

        positive_mean = sum(positive_scores) / len(positive_scores)
        negative_mean = sum(negative_scores) / len(negative_scores)
        suggested_overall = max(min((positive_mean + negative_mean) / 2.0, 0.9), 0.2)

        self.thresholds["overall"] = round(suggested_overall, 3)
        return self.thresholds.copy()

    def _score_skills(self, resume_skills: Sequence[Any], job_skills: Sequence[Any]) -> float:
        text_a = _extract_text_from_items(resume_skills)
        text_b = _extract_text_from_items(job_skills)
        semantic_score = _cosine_similarity(text_a, text_b)
        exact_overlap = _skill_overlap_ratio(resume_skills, job_skills)
        return round((semantic_score * 0.45) + (exact_overlap * 0.55), 6)

    def _score_experience(self, resume_profile: Dict[str, Any], job_profile: Dict[str, Any]) -> float:
        resume_experience_items = resume_profile.get("experience", [])
        job_title = job_profile.get("job_title", "")
        job_description = job_profile.get("job_description", "")
        job_skills = job_profile.get("required_skills", [])

        title_scores: List[float] = []
        for item in resume_experience_items:
            designation = item.get("designation") or item.get("title") or ""
            if designation and job_title:
                title_scores.append(_cosine_similarity(_normalize_text(designation), _normalize_text(job_title)))

        title_similarity = max(title_scores) if title_scores else 0.0
        experience_text = self._build_experience_text(resume_profile)
        job_text = _normalize_text(f"{job_title} {job_description} {' '.join(_extract_text_from_items(job_skills).split())}")
        description_similarity = _cosine_similarity(experience_text, job_text)
        keyword_overlap = _text_overlap_ratio(experience_text, job_text)

        return round((title_similarity * 0.25) + (description_similarity * 0.55) + (keyword_overlap * 0.20), 6)

    def _build_experience_text(self, profile: Dict[str, Any]) -> str:
        experience_items = profile.get("experience", [])
        summary_text = profile.get("summary") or ""
        text_parts: List[str] = [summary_text]

        if experience_items:
            for item in experience_items:
                if isinstance(item, dict):
                    parts = []
                    title = item.get("designation") or item.get("title") or ""
                    responsibilities = item.get("responsibilities") or item.get("description") or []
                    parts.append(title)
                    if isinstance(responsibilities, list):
                        parts.append(" ".join(responsibilities))
                    else:
                        parts.append(str(responsibilities))
                    text_parts.append(" ".join(parts))
                else:
                    text_parts.append(str(item))

        return _normalize_text(" ".join(text_parts))

    def _build_job_experience_text(self, job_profile: Dict[str, Any]) -> str:
        job_title = job_profile.get("job_title", "")
        job_description = job_profile.get("job_description", "")
        return _normalize_text(f"{job_title} {job_description}")

    def _build_project_text(self, profile: Dict[str, Any]) -> str:
        project_items = profile.get("projects", [])
        if isinstance(project_items, str):
            return _normalize_text(project_items)
        if isinstance(project_items, dict):
            return _extract_text_from_items(project_items)

        return _extract_text_from_items(project_items)