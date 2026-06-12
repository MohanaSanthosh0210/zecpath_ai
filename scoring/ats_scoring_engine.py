import sys
import os

sys.path.append(
    os.path.abspath(".")
)

from schemas.scoring_weights import ROLE_WEIGHTS


def calculate_ats_score(
    role,
    skill_score,
    experience_score,
    education_score,
    semantic_score
):

    skill_score = skill_score or 0
    experience_score = experience_score or 0
    education_score = education_score or 0
    semantic_score = semantic_score or 0

    role = str(role).lower()

    weights = ROLE_WEIGHTS.get(
        role,
        {
            "skills": 0.35,
            "experience": 0.30,
            "education": 0.15,
            "semantic": 0.20
        }
    )

    final_score = (

        skill_score * weights["skills"]

        +

        experience_score * weights["experience"]

        +

        education_score * weights["education"]

        +

        semantic_score * weights["semantic"]

    )

    return round(
        final_score,
        2
    )