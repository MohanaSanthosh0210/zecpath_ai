import glob
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from scoring.ats_scoring_engine import calculate_ats_score
from scoring.education_relevance import calculate_education_score
from scoring.semantic_matching import SemanticMatchingEngine
from parsers.education_parser import extract_education

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESUMES_DIR = os.path.join(ROOT_DIR, "data", "sectioned_resumes")
JOBS_DIR = os.path.join(ROOT_DIR, "data", "structured_jobs")
OUTPUT_DIR = os.path.join(ROOT_DIR, "scoring", "ats_scores")

JOB_EDUCATION_PATTERN = re.compile(
    r"education\s*[:\-]?\s*(.+?)(?:\.|$|experience|skills|certification)",
    flags=re.I,
)


def normalize_text(value: str) -> str:
    return " ".join(str(value or "").lower().strip().split())


def normalize_skill_list(skills: List[Any]) -> List[str]:
    normalized: List[str] = []
    for item in skills:
        if isinstance(item, str):
            for part in re.split(r"[,;]\s*", item):
                part = part.strip()
                if part:
                    normalized.append(part.lower())
        elif isinstance(item, dict):
            name = item.get("name") or item.get("skill")
            if isinstance(name, str) and name.strip():
                normalized.append(name.strip().lower())
        else:
            normalized.append(str(item).strip().lower())
    return [skill for skill in normalized if skill]


def build_resume_profile(sectioned_data: Dict[str, Any]) -> Dict[str, Any]:
    experience_items: List[Dict[str, Any]] = []
    for item in sectioned_data.get("experience", []):
        if isinstance(item, str):
            experience_items.append({"description": item})
        elif isinstance(item, dict):
            experience_items.append(item)
        else:
            experience_items.append({"description": str(item)})

    return {
        "skills": normalize_skill_list(sectioned_data.get("skills", [])),
        "experience": experience_items,
        "summary": " ".join(sectioned_data.get("profile", [])),
        "projects": sectioned_data.get("projects", []),
        "education_sections": sectioned_data.get("education", []),
    }


def load_sectioned_resumes() -> Iterable[Tuple[str, Dict[str, Any]]]:
    resume_paths = sorted(glob.glob(os.path.join(RESUMES_DIR, "*.json")))
    for resume_path in resume_paths:
        candidate_id = Path(resume_path).stem
        with open(resume_path, "r", encoding="utf-8") as stream:
            resume_data = json.load(stream)
        yield candidate_id, build_resume_profile(resume_data)


def load_job_profiles() -> Iterable[Tuple[str, Dict[str, Any]]]:
    job_paths = sorted(glob.glob(os.path.join(JOBS_DIR, "*.json")))
    for job_path in job_paths:
        job_id = Path(job_path).stem
        with open(job_path, "r", encoding="utf-8") as stream:
            job_data = json.load(stream)

        job_title = job_data.get("job_title", "")
        job_description = job_data.get("experience", "") or job_data.get("job_description", "")
        required_skills = job_data.get("skills", []) or job_data.get("required_skills", [])
        projects = job_data.get("projects", [])
        education = job_data.get("education") or _extract_job_education(job_title + " " + str(job_description))

        yield job_id, {
            "job_title": job_title,
            "job_description": job_description,
            "required_skills": required_skills,
            "projects": projects,
            "education": education,
        }


def _extract_job_education(text: str) -> str:
    match = JOB_EDUCATION_PATTERN.search(text)
    return match.group(1).strip() if match else ""


def calculate_skill_score(resume_profile: Dict[str, Any], job_profile: Dict[str, Any]) -> float:
    resume_skills = set(resume_profile.get("skills", []))
    required_skills = set(normalize_skill_list(job_profile.get("required_skills", [])))
    if not required_skills:
        return 0.0
    matched = resume_skills.intersection(required_skills)
    return round(min(len(matched) / len(required_skills), 1.0) * 100.0, 2)


def calculate_education_score_for_resume(resume_profile: Dict[str, Any], job_profile: Dict[str, Any]) -> float:
    job_education = normalize_text(job_profile.get("education", ""))
    if not job_education:
        return 0.0

    academic_profile = extract_education({
        "education": resume_profile.get("education_sections", []),
        "certifications": [],
    })
    education_entries = academic_profile.get("education", [])
    if not education_entries:
        return 0.0

    best_score = 0
    for entry in education_entries:
        candidate_field = entry.get("field_of_study") or entry.get("raw_text") or ""
        candidate_degree = entry.get("degree_type") or ""
        score = calculate_education_score(candidate_field, job_education, candidate_degree, job_education)
        best_score = max(best_score, score)

    return round(best_score, 2)


def calculate_semantic_scores(resume_profile: Dict[str, Any], job_profile: Dict[str, Any]) -> Dict[str, float]:
    engine = SemanticMatchingEngine()
    semantic_result = engine.score_pair(resume_profile, job_profile)
    return {
        "skills_similarity": round(semantic_result["skills_similarity"] * 100, 2),
        "experience_similarity": round(semantic_result["experience_similarity"] * 100, 2),
        "project_similarity": round(semantic_result["project_similarity"] * 100, 2),
        "overall_similarity": round(semantic_result["overall_similarity"] * 100, 2),
    }


def compose_reason(components: Dict[str, float], final_score: float) -> str:
    strong_components = [name for name, value in components.items() if value >= 70.0]
    if final_score >= 70.0:
        if strong_components:
            return f"Shortlisted: strong {' and '.join(strong_components)}." if len(strong_components) <= 2 else "Shortlisted: strong match across multiple components."
        return "Shortlisted: overall candidate fit is good."
    weak_components = [name for name, value in components.items() if value < 50.0]
    if weak_components:
        return f"Rejected: weak {' and '.join(weak_components)}." if len(weak_components) <= 2 else "Rejected: weak match across multiple components."
    return "Rejected: overall fit is below threshold."


def build_candidate_result(
    candidate_id: str,
    job_id: str,
    resume_profile: Dict[str, Any],
    job_profile: Dict[str, Any],
) -> Dict[str, Any]:
    skill_score = calculate_skill_score(resume_profile, job_profile)
    education_score = calculate_education_score_for_resume(resume_profile, job_profile)
    semantic_scores = calculate_semantic_scores(resume_profile, job_profile)
    experience_score = semantic_scores["experience_similarity"]
    semantic_score = semantic_scores["overall_similarity"]

    final_ats_score = calculate_ats_score(
        role=job_profile.get("job_title", ""),
        skill_score=skill_score,
        experience_score=experience_score,
        education_score=education_score,
        semantic_score=semantic_score,
    )

    breakdown = {
        "skills": skill_score,
        "experience": experience_score,
        "education": education_score,
        "semantic": semantic_score,
    }

    result = {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "resume_file": f"{candidate_id}.json",
        "job_file": f"{job_id}.json",
        "role": job_profile.get("job_title", ""),
        "skill_score": skill_score,
        "experience_score": experience_score,
        "education_score": education_score,
        "semantic_score": semantic_score,
        "final_ats_score": final_ats_score,
        "status": "Shortlisted" if final_ats_score >= 70.0 else "Rejected",
        "breakdown": breakdown,
        "reason": compose_reason(breakdown, final_ats_score),
        "details": {
            "skills_similarity": semantic_scores["skills_similarity"],
            "experience_similarity": semantic_scores["experience_similarity"],
            "project_similarity": semantic_scores["project_similarity"],
            "job_education": job_profile.get("education", ""),
        },
    }
    return result


def generate_ats_scores(output_dir: Optional[str] = None) -> List[Dict[str, Any]]:
    output_dir = output_dir or OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)
    results: List[Dict[str, Any]] = []

    resumes = list(load_sectioned_resumes())
    jobs = list(load_job_profiles())

    for job_id, job_profile in jobs:
        for candidate_id, resume_profile in resumes:
            result = build_candidate_result(candidate_id, job_id, resume_profile, job_profile)
            file_name = f"{job_id}_{candidate_id}.json"
            output_path = os.path.join(output_dir, file_name)
            with open(output_path, "w", encoding="utf-8") as out:
                json.dump(result, out, indent=4)
            results.append(result)

    summary_path = os.path.join(output_dir, "summary.json")
    with open(summary_path, "w", encoding="utf-8") as out:
        json.dump({"results": results}, out, indent=4)

    return results


def main() -> None:
    results = generate_ats_scores()
    print(f"Generated {len(results)} ATS score files in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()