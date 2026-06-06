import json
import os
import sys

sys.path.append(os.path.abspath("."))

from ats_scoring_engine import calculate_ats_score


candidate = {

    "candidate_id": "C001",

    "job_id": "J001",

    "role": "python developer",

    "skill_score": 90,

    "experience_score": 85,

    "education_score": 80,

    "semantic_score": 88
}

final_score = calculate_ats_score(

    role=candidate["role"],

    skill_score=candidate["skill_score"],

    experience_score=candidate["experience_score"],

    education_score=candidate["education_score"],

    semantic_score=candidate["semantic_score"]

)

result = {

    "candidate_id": candidate["candidate_id"],

    "job_id": candidate["job_id"],

    "skill_score": candidate["skill_score"],

    "experience_score": candidate["experience_score"],

    "education_score": candidate["education_score"],

    "semantic_score": candidate["semantic_score"],

    "final_ats_score": final_score,

    "status": "Shortlisted" if final_score >= 70 else "Rejected",

    "breakdown": {

        "skills": candidate["skill_score"],

        "experience": candidate["experience_score"],

        "education": candidate["education_score"],

        "semantic": candidate["semantic_score"]

    },

    "reason": "Strong skill match and relevant experience"
}

os.makedirs(
    "scoring/ats_scores",
    exist_ok=True
)

with open(
    "scoring/ats_scores/candidate1.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        result,
        f,
        indent=4
    )

print("ATS Score Generated Successfully")