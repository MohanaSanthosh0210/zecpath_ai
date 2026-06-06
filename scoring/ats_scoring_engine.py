import sys
import os

sys.path.append(os.path.abspath("."))

from schemas.scoring_weights import ROLE_WEIGHTS

def calculate_ats_score(
    role,
    skill_score,
    experience_score,
    education_score,
    semantic_score
):

    # Handle missing values

    if skill_score is None:
        skill_score = 0

    if experience_score is None:
        experience_score = 0

    if education_score is None:
        education_score = 0

    if semantic_score is None:
        semantic_score = 0

    role = role.lower()

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

    return round(final_score, 2)