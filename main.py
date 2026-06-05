import glob
import json
import os
import re
from typing import Any, Dict, Iterable, List

from scoring.semantic_matching import SemanticMatchingEngine
from utils.logger import logger

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


def _normalize_skill_list(skills: List[Any]) -> List[str]:
    normalized = []
    for item in skills:
        if isinstance(item, str):
            parts = re.split(r"[,;]\s*", item)
            for part in parts:
                trimmed = part.strip()
                if trimmed:
                    normalized.append(trimmed)
        elif isinstance(item, dict):
            name = item.get("name") or item.get("skill")
            if isinstance(name, str) and name.strip():
                normalized.append(name.strip())
        else:
            normalized.append(str(item).strip())
    return normalized


def build_resume_profile(sectioned_data: Dict[str, Any], file_name: str) -> Dict[str, Any]:
    experience_items: List[Dict[str, Any]] = []
    for item in sectioned_data.get("experience", []):
        if isinstance(item, str):
            experience_items.append({"description": item})
        elif isinstance(item, dict):
            experience_items.append(item)
        else:
            experience_items.append({"description": str(item)})

    return {
        "file_name": file_name,
        "skills": _normalize_skill_list(sectioned_data.get("skills", [])),
        "experience": experience_items,
        "summary": " ".join(sectioned_data.get("profile", [])),
        "projects": sectioned_data.get("projects", []),
    }


def load_sectioned_resumes() -> Iterable[Dict[str, Any]]:
    resumes_dir = os.path.join(ROOT_DIR, "data", "sectioned_resumes")
    for resume_path in sorted(glob.glob(os.path.join(resumes_dir, "*.json"))):
        with open(resume_path, "r", encoding="utf-8") as stream:
            sectioned_resume = json.load(stream)
        yield build_resume_profile(sectioned_resume, os.path.basename(resume_path))


def load_job_profile() -> Dict[str, Any]:
    job_path = os.path.join(ROOT_DIR, "data", "structured_jobs", "jd1.json")
    if not os.path.exists(job_path):
        return {
            "job_title": "Data Scientist",
            "job_description": "Seeking a data scientist to develop ML models and analyze large datasets.",
            "required_skills": ["machine learning", "python", "data analysis"],
            "projects": [],
        }

    with open(job_path, "r", encoding="utf-8") as stream:
        job_data = json.load(stream)

    return {
        "job_title": job_data.get("job_title", ""),
        "job_description": job_data.get("experience", ""),
        "required_skills": job_data.get("skills", []),
        "projects": job_data.get("projects", []),
    }


def main() -> None:
    logger.info("Zecpath AI Hiring System Started")
    print("AI Hiring System Running")

    resumes = list(load_sectioned_resumes())
    job_profile = load_job_profile()
    engine = SemanticMatchingEngine()

    if not resumes:
        print("No sectioned resumes found in data/sectioned_resumes.")
        return

    results = []
    for resume_profile in resumes:
        score = engine.score_pair(resume_profile, job_profile)
        results.append({
            "resume_file": resume_profile["file_name"],
            "score": score,
        })

    output_dir = os.path.join(ROOT_DIR, "data", "semantic_matches")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "resume_scores.json")
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump({"job_profile": job_profile, "results": results}, out, indent=2)

    print(f"Wrote resume scores for {len(results)} resumes to {output_path}")


if __name__ == "__main__":
    main()